"""文件发现、增量索引和异常隔离。"""

from __future__ import annotations

# fnmatch 支持按目录名或相对路径配置通配符排除规则。
import fnmatch
import hashlib
# logging 用于记录发现、跳过、完成和失败的文件。
import logging
# os.walk 可以在遍历时剪枝，避免进入被排除的目录。
import os
import threading
import time
# Callable 让 CLI 可以订阅单文件进度事件；Iterable/Iterator 保持发现流式化。
from collections.abc import Callable, Iterable, Iterator
from dataclasses import replace
from datetime import datetime
# Path 负责跨平台的目录递归和扩展名判断。
from pathlib import Path

# 索引流水线依次调用流式清洗、流式分段和数据库写入模块。
from .block_parsing import iter_document_blocks
from .chunking import (
    ChunkingConfig,
    iter_chunk_blocks_batched,
    iter_chunk_text,
)
from .constants import (
    DEFAULT_CHUNK_OVERLAP_CHARS,
    DEFAULT_CORE_CHUNK_CHARS,
    DEFAULT_DATASET_SPLIT,
    DEFAULT_MAX_CHUNK_CHARS,
    DEFAULT_MAX_CHUNK_TOKENS,
    DEFAULT_MIN_CHUNK_CHARS,
    DEFAULT_SEMANTIC_MERGE_THRESHOLD,
)
from .embedding import EmbeddingBackend
from .cleaning import iter_clean_text
from .database import KnowledgeBase
from .dataset_reader import iter_dataset_blocks, iter_local_dataset
from .extractors import SUPPORTED_SUFFIXES, extract_document, iter_document_text
from .json_parser import (
    DEFAULT_MAX_JSON_SIZE,
    DEFAULT_JSON_RECORD_PROBE_SIZE,
    JsonProfile,
    JsonSizeLimitError,
    ensure_json_size,
)
from .models import Chunk, ExtractedDocument, IndexProgress, IndexStats


logger = logging.getLogger(__name__)

# 这些目录通常是版本控制、虚拟环境或构建缓存，不应进入默认索引。
DEFAULT_EXCLUDED_DIRS = (
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    "build",
    "dist",
)


class _IndexProgressTracker:
    """Thread-safe dynamic chunk progress and ETA monitor for one task."""

    def __init__(
        self,
        paths: list[Path],
        *,
        chunk_size: int,
        overlap: int,
        progress_callback: Callable[[IndexProgress], None] | None = None,
    ) -> None:
        self._lock = threading.Lock()
        self._callback_lock = threading.Lock()
        self._started = time.monotonic()
        self._stop = threading.Event()
        self._file_sizes: dict[Path, int] = {
            path: self._file_size(path) for path in paths
        }
        self._estimates: dict[Path, int] = {
            path: self._estimate(
                self._file_sizes[path], chunk_size, overlap
            )
            for path in paths
        }
        self._observed: dict[Path, int] = {path: 0 for path in paths}
        self._observed_bytes: dict[Path, int] = {path: 0 for path in paths}
        self.estimated_chunks = sum(self._estimates.values())
        self.completed_chunks = 0
        self.current_path: Path | None = None
        self.current_file = 0
        self.total_files = len(paths)
        self._progress_callback = progress_callback
        self._last_reported_milestone = 0
        self._thread = threading.Thread(
            target=self._monitor,
            name="index-progress-monitor",
            daemon=True,
        )
        self._thread.start()

    @staticmethod
    def _file_size(path: Path) -> int:
        try:
            return path.stat().st_size
        except OSError:
            return 0

    @staticmethod
    def _estimate(size: int, chunk_size: int, overlap: int) -> int:
        if size <= 0:
            return 0
        stride = max(1, chunk_size - overlap)
        return max(1, (size + stride - 1) // stride)

    def start_file(self, current: int, path: Path) -> None:
        with self._lock:
            self.current_file = current
            self.current_path = path

    def chunk_completed(
        self,
        count: int = 1,
        *,
        processed_bytes: int | None = None,
    ) -> None:
        if count <= 0:
            return
        milestones: list[int] = []
        snapshot: dict[str, object] = {}
        with self._lock:
            self.completed_chunks += count
            if self.current_path is not None:
                self._observed[self.current_path] = (
                    self._observed.get(self.current_path, 0) + count
                )
                if processed_bytes is not None and processed_bytes > 0:
                    self._observed_bytes[self.current_path] = (
                        self._observed_bytes.get(self.current_path, 0)
                        + processed_bytes
                    )
            self._recalculate_estimate_locked()
            milestone = self.completed_chunks // 200
            if milestone > self._last_reported_milestone:
                milestones = list(
                    range(self._last_reported_milestone + 1, milestone + 1)
                )
                self._last_reported_milestone = milestone
                snapshot = self._snapshot_locked()
        for milestone in milestones:
            logger.info(
                "索引分块进度：预估分块 %s，当前完成的分块 %s，预计完成时间 %s",
                snapshot["estimated_chunks"],
                milestone * 200,
                snapshot["estimated_completion_time"] or "计算中",
            )

    def finish_file(self, path: Path, actual_chunks: int) -> None:
        """Replace the rough file-size estimate with the observed chunk count."""

        with self._lock:
            self._estimates.pop(path, None)
            observed = self._observed.pop(path, 0)
            self._observed_bytes.pop(path, None)
            self._file_sizes.pop(path, None)
            self.completed_chunks = max(
                0, self.completed_chunks + actual_chunks - observed
            )
            self._last_reported_milestone = min(
                self._last_reported_milestone,
                self.completed_chunks // 200,
            )
            self._recalculate_estimate_locked()
            self.current_path = path

    def skipped_file(self, path: Path) -> None:
        with self._lock:
            self._estimates.pop(path, None)
            self._observed.pop(path, None)
            self._observed_bytes.pop(path, None)
            self._file_sizes.pop(path, None)
            self._recalculate_estimate_locked()
            self.current_path = path

    def failed_file(self, path: Path, attempted_chunks: int) -> None:
        with self._lock:
            self._estimates.pop(path, None)
            self._observed.pop(path, None)
            self._observed_bytes.pop(path, None)
            self._file_sizes.pop(path, None)
            self.completed_chunks = max(0, self.completed_chunks - attempted_chunks)
            self._last_reported_milestone = self.completed_chunks // 200
            self._recalculate_estimate_locked()
            self.current_path = path

    def _recalculate_estimate_locked(self) -> None:
        remaining = 0
        for path, rough_estimate in self._estimates.items():
            observed = self._observed.get(path, 0)
            observed_bytes = self._observed_bytes.get(path, 0)
            if observed > 0 and observed_bytes > 0:
                file_size = self._file_sizes.get(path, 0)
                predicted = (file_size * observed + observed_bytes - 1) // observed_bytes
                estimate = max(observed, predicted)
            else:
                estimate = max(observed, rough_estimate)
            remaining += max(0, estimate - observed)
        self.estimated_chunks = self.completed_chunks + remaining

    def snapshot(self) -> dict[str, object]:
        with self._lock:
            return self._snapshot_locked()

    def _snapshot_locked(self) -> dict[str, object]:
        elapsed = max(0.0, time.monotonic() - self._started)
        rate = self.completed_chunks / elapsed if elapsed > 0 else 0.0
        remaining = max(0, self.estimated_chunks - self.completed_chunks)
        eta_seconds = remaining / rate if rate > 0 else None
        eta_text = None
        if eta_seconds is not None:
            eta_text = datetime.fromtimestamp(
                datetime.now().astimezone().timestamp() + eta_seconds
            ).astimezone().isoformat(timespec="seconds")
        return {
            "estimated_chunks": max(0, int(self.estimated_chunks)),
            "completed_chunks": max(0, int(self.completed_chunks)),
            "elapsed_seconds": elapsed,
            "estimated_remaining_seconds": eta_seconds,
            "estimated_completion_time": eta_text,
            "chunks_per_second": rate,
        }

    def _monitor(self) -> None:
        while not self._stop.wait(1.0):
            snapshot = self.snapshot()
            remaining = snapshot["estimated_remaining_seconds"]
            remaining_text = (
                f"{remaining:.1f} 秒"
                if isinstance(remaining, (int, float))
                else "计算中"
            )
            # logger.info(
            #     "索引进度追踪：预估分块 %s，当前完成的分块 %s，耗时 %.1f 秒，"
            #     "预计剩余 %s，预计完成时间 %s",
            #     snapshot["estimated_chunks"],
            #     snapshot["completed_chunks"],
            #     snapshot["elapsed_seconds"],
            #     remaining_text,
            #     snapshot["estimated_completion_time"] or "计算中",
            # )
            self._notify(snapshot)

    def notify_status(self, current: int, path: Path, status: str) -> None:
        self._notify(
            self.snapshot(),
            current=current,
            path=path,
            status=status,
        )

    def _notify(
        self,
        snapshot: dict[str, object],
        *,
        current: int | None = None,
        path: Path | None = None,
        status: str = "progress",
    ) -> None:
        with self._lock:
            callback = self._progress_callback
            current_path = path or self.current_path
            current_file = current if current is not None else self.current_file
        if callback is None or current_path is None:
            return
        try:
            with self._callback_lock:
                callback(
                    IndexProgress(
                        current=current_file,
                        total=self.total_files,
                        path=current_path,
                        status=status,
                        estimated_chunks=int(snapshot["estimated_chunks"]),
                        completed_chunks=int(snapshot["completed_chunks"]),
                        elapsed_seconds=float(snapshot["elapsed_seconds"]),
                        estimated_remaining_seconds=(
                            float(snapshot["estimated_remaining_seconds"])
                            if snapshot["estimated_remaining_seconds"] is not None
                            else None
                        ),
                        estimated_completion_time=(
                            str(snapshot["estimated_completion_time"])
                            if snapshot["estimated_completion_time"] is not None
                            else None
                        ),
                        chunks_per_second=float(snapshot["chunks_per_second"]),
                    )
                )
        except Exception:
            logger.exception("索引进度回调失败：%s", current_path)

    def close(self) -> dict[str, object]:
        self._stop.set()
        self._thread.join(timeout=2.0)
        return self.snapshot()


def _store_progress_snapshot(stats: IndexStats, snapshot: dict[str, object]) -> None:
    stats.estimated_chunks = int(snapshot["estimated_chunks"])
    stats.completed_chunks = int(snapshot["completed_chunks"])
    stats.elapsed_seconds = float(snapshot["elapsed_seconds"])
    remaining = snapshot["estimated_remaining_seconds"]
    stats.estimated_remaining_seconds = (
        float(remaining) if isinstance(remaining, (int, float)) else None
    )
    completion = snapshot["estimated_completion_time"]
    stats.estimated_completion_time = str(completion) if completion is not None else None


def _normalise_rule(rule: str | Path) -> str:
    """把用户输入的目录规则转换为跨平台、可比较的形式。"""

    text = str(rule).strip().replace("\\", "/")
    while text.startswith("./"):
        text = text[2:]
    return text.rstrip("/")


def _matches_excluded_directory(
    directory: Path,
    root: Path,
    rules: tuple[str, ...],
    absolute_rules: tuple[Path, ...],
) -> bool:
    """判断目录是否命中名称、相对路径或绝对路径规则。"""

    resolved = directory.resolve()
    if any(
        resolved == rule or rule in resolved.parents
        for rule in absolute_rules
    ):
        return True

    try:
        relative = directory.relative_to(root).as_posix()
    except ValueError:
        relative = directory.name
    # 对 ``generated/*`` 这类规则，当前目录本身也视为匹配点，这样可以在
    # 进入 generated 之前完成剪枝，而不是只排除它下面更深一层的目录。
    candidates = (directory.name, relative, f"{relative}/*")
    return any(
        fnmatch.fnmatchcase(candidate.casefold(), rule.casefold())
        for rule in rules
        for candidate in candidates
    )


def discover_files(
    inputs: Iterable[Path],
    *,
    include_json: bool = False,
    exclude_dirs: Iterable[str | Path] | None = None,
    exclude_files: Iterable[Path] = (),
    max_files: int | None = None,
) -> Iterator[Path]:
    """递归发现支持的文件，并应用排除、去重和数量上限规则。

    目录规则可以是目录名（如 ``.git``）、通配符（如 ``cache*``）或相对
    输入根目录的路径（如 ``generated/cache``）。``max_files`` 为 0 或
    ``None`` 时表示不限制数量。
    """

    supported_suffixes = SUPPORTED_SUFFIXES if include_json else SUPPORTED_SUFFIXES - {".json"}
    if max_files is not None and max_files < 0:
        raise ValueError("最大文件数不能小于 0")

    raw_rules = (
        DEFAULT_EXCLUDED_DIRS
        if exclude_dirs is None
        else (*DEFAULT_EXCLUDED_DIRS, *exclude_dirs)
    )
    rules = tuple(
        rule
        for rule in (_normalise_rule(value) for value in raw_rules)
        if rule
    )
    absolute_rules = tuple(
        Path(rule).expanduser().resolve()
        for rule in rules
        if Path(rule).expanduser().is_absolute()
    )
    excluded_files = {
        Path(path).expanduser().resolve()
        for path in exclude_files
    }
    seen: set[Path] = set()
    emitted = 0
    limit = None if max_files in (None, 0) else max_files

    def emit(path: Path) -> Iterator[Path]:
        nonlocal emitted
        resolved = path.resolve()
        if resolved in excluded_files or resolved in seen:
            return
        if limit is not None and emitted >= limit:
            return
        seen.add(resolved)
        emitted += 1
        yield resolved

    # 逐个处理 CLI 传入的文件或目录参数。
    for raw_input in inputs:
        # 展开用户目录符号，但保留相对路径以便根据当前工作目录解析。
        path = Path(raw_input).expanduser()
        if path.is_file():
            # 单文件输入只接受支持的扩展名。
            if path.suffix.lower() in supported_suffixes:
                yield from emit(path)
            else:
                logger.warning("忽略不支持的文件：%s", path)
            continue
        if path.is_dir():
            root = path.resolve()
            if _matches_excluded_directory(root, root.parent, rules, absolute_rules):
                logger.info("排除目录：%s", root)
                continue
            # 目录输入使用 os.walk，并在进入子目录前剪枝，避免扫描虚拟环境等大目录。
            for current, dirnames, filenames in os.walk(root, topdown=True):
                current_path = Path(current)
                dirnames[:] = sorted(
                    directory
                    for directory in dirnames
                    if not _matches_excluded_directory(
                        current_path / directory,
                        root,
                        rules,
                        absolute_rules,
                    )
                )
                for filename in sorted(filenames):
                    child = current_path / filename
                    if child.is_file() and child.suffix.lower() in supported_suffixes:
                        yield from emit(child)
                        if limit is not None and emitted >= limit:
                            return
            continue
        # 不存在的输入只记录警告，不影响其他输入继续处理。
        logger.warning("索引输入不存在：%s", path)


def _iter_index_chunks(
    text_chunks: Iterable[str],
    *,
    chunk_size: int,
    overlap: int,
    separate_records: bool = False,
) -> Iterator[Chunk]:
    """清洗并分段；JSON record 模式下不让相邻记录合并到同一分段。"""

    if not separate_records:
        yield from iter_chunk_text(
            iter_clean_text(text_chunks),
            chunk_size=chunk_size,
            overlap=overlap,
        )
        return

    source_iterator = iter(text_chunks)
    chunk_index = 0
    while True:
        try:
            first_block = next(source_iterator)
        except StopIteration:
            break

        def record_blocks():
            """消费当前记录的块，不把超大记录拼回单个字符串。"""

            block = first_block
            yield block
            if not getattr(block, "record_end", True):
                while True:
                    block = next(source_iterator)
                    yield block
                    if getattr(block, "record_end", True):
                        break

        cleaned_text = iter_clean_text(record_blocks())
        for chunk in iter_chunk_text(
            cleaned_text,
            chunk_size=chunk_size,
            overlap=overlap,
        ):
            yield Chunk(
                index=chunk_index,
                content=chunk.content,
                start_offset=chunk.start_offset,
            )
            chunk_index += 1


def _extract_dataset_document(
    path: Path,
    *,
    dataset_name: str | None,
    split: str,
    file_format: str | None,
) -> ExtractedDocument:
    """Build database metadata for an arbitrary-suffix dataset file."""

    source_path = path.expanduser().resolve()
    if not source_path.is_file():
        raise FileNotFoundError(f"数据集文件不存在：{source_path}")
    hasher = hashlib.sha256()
    with source_path.open("rb") as stream:
        while data := stream.read(64 * 1024):
            hasher.update(data)
    stat = source_path.stat()
    parser_fingerprint = hashlib.sha256(
        "\0".join(
            (
                "huggingface-datasets",
                (dataset_name or "auto").strip().lower(),
                split,
                (file_format or "auto").strip().lower(),
            )
        ).encode("utf-8")
    ).hexdigest()
    return ExtractedDocument(
        path=source_path,
        file_type="dataset",
        text=None,
        sha256=hasher.hexdigest(),
        size=stat.st_size,
        modified_ns=stat.st_mtime_ns,
        parser_fingerprint=parser_fingerprint,
        parser="huggingface-datasets",
    )


def _iter_dataset_chunks(
    records,
    *,
    source_name: str,
    chunk_size: int,
    overlap: int,
    min_chunk_chars: int,
    max_chunk_chars: int,
    semantic_merge_threshold: float,
    max_chunk_tokens: int,
    embedding_backend: EmbeddingBackend | None,
) -> Iterator[Chunk]:
    """Chunk records lazily and embed final chunks in bounded batches.

    Dataset records are hard boundaries, so semantic merging between records
    can never happen.  Running the semantic-merging path for every record
    would nevertheless issue a separate "core" embedding request for every
    record.  The batched chunker keeps that semantic pass within each record,
    batches core requests across records, and batches final vectors as well.
    Memory remains bounded by ``backend.settings.batch_size`` records.
    """

    chunk_index = 0
    # The batched chunker preserves semantic merging within each record while
    # keeping records as hard boundaries and batching final vectors.
    chunks = iter_chunk_blocks_batched(
        iter_dataset_blocks(records, source_name=source_name),
        chunk_size=chunk_size,
        overlap=overlap,
        min_chunk_chars=min_chunk_chars,
        max_chunk_chars=max_chunk_chars,
        semantic_merge_threshold=semantic_merge_threshold,
        max_chunk_tokens=max_chunk_tokens,
        embedding_backend=embedding_backend,
    )
    for chunk in chunks:
        yield replace(chunk, index=chunk_index)
        chunk_index += 1


def index_paths(
    knowledge_base: KnowledgeBase,
    inputs: Iterable[Path],
    *,
    chunk_size: int = DEFAULT_CORE_CHUNK_CHARS,
    overlap: int = DEFAULT_CHUNK_OVERLAP_CHARS,
    min_chunk_chars: int = DEFAULT_MIN_CHUNK_CHARS,
    max_chunk_chars: int = DEFAULT_MAX_CHUNK_CHARS,
    semantic_merge_threshold: float = DEFAULT_SEMANTIC_MERGE_THRESHOLD,
    max_chunk_tokens: int = DEFAULT_MAX_CHUNK_TOKENS,
    embedding_backend: EmbeddingBackend | None = None,
    force: bool = False,
    json_profile: JsonProfile | None = None,
    exclude_dirs: Iterable[str | Path] | None = None,
    exclude_files: Iterable[Path] = (),
    max_files: int | None = None,
    max_json_size: int = DEFAULT_MAX_JSON_SIZE,
    json_record_probe_size: int = DEFAULT_JSON_RECORD_PROBE_SIZE,
    progress_callback: Callable[[IndexProgress], None] | None = None,
) -> IndexStats:
    # stats 汇总本次索引结果，供日志和 CLI 摘要使用。
    stats = IndexStats()
    if max_json_size < 0:
        raise ValueError("JSON 最大文件大小不能小于 0")
    if json_record_probe_size <= 0:
        raise ValueError("JSON 单条记录探测窗口必须大于 0")
    chunking_config = ChunkingConfig(
        core_chunk_chars=chunk_size,
        overlap_chars=overlap,
        min_chunk_chars=min(min_chunk_chars, chunk_size),
        max_chunk_chars=max_chunk_chars,
        semantic_merge_threshold=semantic_merge_threshold,
        max_chunk_tokens=max_chunk_tokens,
    )
    excluded_files = list(exclude_files)
    # 配置文件可能位于待索引目录中；它是规则而不是知识内容，必须从候选
    # 文件中排除。discover_files 同时还会去重重叠输入目录产生的路径。
    if json_profile is not None and json_profile.config_path is not None:
        excluded_files.append(json_profile.config_path)

    # 先物化路径列表，便于同时统计总数、显示总进度和逐个处理。
    paths = list(
        discover_files(
            inputs,
            include_json=json_profile is not None,
            exclude_dirs=exclude_dirs,
            exclude_files=excluded_files,
            max_files=max_files,
        )
    )
    stats.files_found = len(paths)
    logger.info("发现 %s 个待处理文件", stats.files_found)
    if not paths:
        return stats
    chunker_fingerprint = chunking_config.fingerprint_for(embedding_backend)

    def report(current: int, path: Path, status: str) -> None:
        tracker.notify_status(current, path, status)

    tracker = _IndexProgressTracker(
        paths,
        chunk_size=chunk_size,
        overlap=overlap,
        progress_callback=progress_callback,
    )
    for current, path in enumerate(paths, start=1):
        tracker.start_file(current, path)
        report(current, path, "processing")
        status = "failed"
        chunk_count = 0
        progress_chunks = 0

        def track_completed(
            count: int = 1,
            *,
            processed_bytes: int | None = None,
        ) -> None:
            nonlocal progress_chunks
            progress_chunks += count
            tracker.chunk_completed(count, processed_bytes=processed_bytes)

        try:
            profile = json_profile if path.suffix.lower() == ".json" else None
            if path.suffix.lower() == ".json" and profile is None:
                raise ValueError("索引 JSON 文件必须提供 --json-config 配置文件")
            if profile is not None:
                # 在计算哈希和打开解析器之前完成大小检查，超大 JSON 不会进入
                # 任何正文读取逻辑，也不会覆盖已有的旧索引。
                ensure_json_size(path, max_json_size)

            # 根据后缀读取文件、计算哈希并抽取文本。
            document = extract_document(
                path,
                parser_fingerprint=profile.fingerprint if profile else "",
            )
            if not force and knowledge_base.is_unchanged(
                document, chunker_fingerprint=chunker_fingerprint
            ):
                if embedding_backend is not None:
                    generated = knowledge_base.ensure_document_embeddings(
                        document.path,
                        embedding_backend,
                        chunker_fingerprint=chunker_fingerprint,
                        progress_callback=track_completed,
                    )
                    stats.embeddings_generated += generated
                # 内容哈希不变时不重复清洗、分段和写数据库。
                stats.skipped += 1
                status = "skipped"
                if embedding_backend is not None and generated:
                    tracker.finish_file(path, generated)
                else:
                    tracker.skipped_file(path)
                logger.info("跳过未变化文件：%s", path)
                continue

            # 先产生结构块，再只在单个结构块内部执行长度切分。
            source_blocks = iter_document_blocks(
                document,
                json_profile=profile,
                max_json_size=max_json_size,
                json_record_probe_size=json_record_probe_size,
            )
            chunks = iter_chunk_blocks_batched(
                source_blocks,
                chunk_size=chunk_size,
                overlap=overlap,
                min_chunk_chars=min_chunk_chars,
                max_chunk_chars=max_chunk_chars,
                semantic_merge_threshold=semantic_merge_threshold,
                max_chunk_tokens=max_chunk_tokens,
                embedding_backend=embedding_backend,
            )

            # 用计数器包装分段流，只记录数量，不保存已经写入数据库的分段。
            def counted_chunks():
                nonlocal chunk_count
                for chunk in chunks:
                    chunk_count += 1
                    track_completed(
                        processed_bytes=len(chunk.content.encode("utf-8"))
                    )
                    yield chunk

            # 在事务中替换旧文档，并由数据库层逐个消费分段生成器。
            knowledge_base.replace_document(
                document,
                counted_chunks(),
                embedding_backend=embedding_backend,
                chunker_fingerprint=chunker_fingerprint,
            )
            tracker.finish_file(path, chunk_count)
            if embedding_backend is not None:
                stats.embeddings_generated += chunk_count
            if chunk_count == 0:
                # 文件可能从有内容变成空文件，清理刚写入的空记录和旧索引。
                knowledge_base.remove_document(document.path)
                stats.empty += 1
                status = "empty"
                logger.warning("文件没有可索引文本：%s", path)
                continue

            stats.indexed += 1
            status = "indexed"
            logger.info("完成索引：%s（%s 个分段）", path, chunk_count)
        except JsonSizeLimitError as exc:
            stats.oversized += 1
            status = "oversized"
            logger.warning("跳过超出 JSON 大小上限的文件：%s", exc)
        except Exception:
            # 单个文件失败不应中断整个目录；记录堆栈并累加失败数。
            stats.failed += 1
            logger.exception("处理文件失败：%s", path)
        finally:
            if status in {"failed", "oversized"}:
                tracker.failed_file(path, progress_chunks)
            report(current, path, status)

    # 返回完整汇总，让 CLI 决定显示和退出状态码。
    _store_progress_snapshot(stats, tracker.close())
    logger.info(
        "索引任务结束：预估分块 %s，当前完成的分块 %s，总耗时 %.1f 秒",
        stats.estimated_chunks,
        stats.completed_chunks,
        stats.elapsed_seconds,
    )
    return stats


def index_datasets(
    knowledge_base: KnowledgeBase,
    inputs: Iterable[Path],
    *,
    dataset_name: str | None = None,
    split: str = DEFAULT_DATASET_SPLIT,
    file_format: str | None = None,
    chunk_size: int = DEFAULT_CORE_CHUNK_CHARS,
    overlap: int = DEFAULT_CHUNK_OVERLAP_CHARS,
    min_chunk_chars: int = DEFAULT_MIN_CHUNK_CHARS,
    max_chunk_chars: int = DEFAULT_MAX_CHUNK_CHARS,
    semantic_merge_threshold: float = DEFAULT_SEMANTIC_MERGE_THRESHOLD,
    max_chunk_tokens: int = DEFAULT_MAX_CHUNK_TOKENS,
    embedding_backend: EmbeddingBackend | None = None,
    force: bool = False,
    max_files: int | None = None,
    progress_callback: Callable[[IndexProgress], None] | None = None,
) -> IndexStats:
    """Stream local datasets into the index without relying on file suffixes.

    Every input must be an individual local file. ``iter_local_dataset`` owns
    format detection and delegates decoding to Hugging Face ``datasets`` with
    ``streaming=True``. Records are chunked and persisted one at a time.
    """

    if dataset_name is not None and not dataset_name.strip():
        raise ValueError("dataset_name 不能为空")
    adapter = dataset_name.strip() if dataset_name is not None else None
    if adapter is not None and adapter.lower() in {"auto", "infer"}:
        adapter = None
    if not split.strip():
        raise ValueError("split 不能为空")
    if max_files is not None and max_files < 0:
        raise ValueError("最大文件数不能小于 0")

    limit = None if max_files in (None, 0) else max_files
    paths: list[Path] = []
    seen: set[Path] = set()
    for raw_input in inputs:
        path = Path(raw_input).expanduser().resolve()
        if path in seen:
            continue
        seen.add(path)
        if not path.is_file():
            logger.warning("数据集输入不存在或不是文件：%s", path)
            continue
        paths.append(path)
        if limit is not None and len(paths) >= limit:
            break

    stats = IndexStats(files_found=len(paths))
    logger.info("发现 %s 个待处理数据集文件", stats.files_found)
    if not paths:
        return stats
    chunking_config = ChunkingConfig(
        core_chunk_chars=chunk_size,
        overlap_chars=overlap,
        min_chunk_chars=min(min_chunk_chars, chunk_size),
        max_chunk_chars=max_chunk_chars,
        semantic_merge_threshold=semantic_merge_threshold,
        max_chunk_tokens=max_chunk_tokens,
    )
    # Dataset records remain independent hard-boundary retrieval units, while
    # semantic merging is retained inside records and executed in batches.
    chunker_fingerprint = chunking_config.fingerprint_for(embedding_backend)

    def report(current: int, path: Path, status: str) -> None:
        tracker.notify_status(current, path, status)

    tracker = _IndexProgressTracker(
        paths,
        chunk_size=chunk_size,
        overlap=overlap,
        progress_callback=progress_callback,
    )
    for current, path in enumerate(paths, start=1):
        tracker.start_file(current, path)
        report(current, path, "processing")
        status = "failed"
        chunk_count = 0
        progress_chunks = 0

        def track_completed(
            count: int = 1,
            *,
            processed_bytes: int | None = None,
        ) -> None:
            nonlocal progress_chunks
            progress_chunks += count
            tracker.chunk_completed(count, processed_bytes=processed_bytes)

        try:
            document = _extract_dataset_document(
                path,
                dataset_name=adapter,
                split=split,
                file_format=file_format,
            )
            if not force and knowledge_base.is_unchanged(
                document,
                chunker_fingerprint=chunker_fingerprint,
            ):
                if embedding_backend is not None:
                    generated = knowledge_base.ensure_document_embeddings(
                        document.path,
                        embedding_backend,
                        chunker_fingerprint=chunker_fingerprint,
                        progress_callback=track_completed,
                    )
                    stats.embeddings_generated += generated
                stats.skipped += 1
                status = "skipped"
                if embedding_backend is not None and generated:
                    tracker.finish_file(path, generated)
                else:
                    tracker.skipped_file(path)
                logger.info("跳过未变化数据集：%s", path)
                continue

            records = iter_local_dataset(
                document.path,
                adapter,
                split=split,
                file_format=file_format,
            )
            chunks = _iter_dataset_chunks(
                records,
                source_name=document.path.name,
                chunk_size=chunk_size,
                overlap=overlap,
                min_chunk_chars=min_chunk_chars,
                max_chunk_chars=max_chunk_chars,
                semantic_merge_threshold=semantic_merge_threshold,
                max_chunk_tokens=max_chunk_tokens,
                embedding_backend=embedding_backend,
            )
            def counted_chunks() -> Iterator[Chunk]:
                nonlocal chunk_count
                for chunk in chunks:
                    chunk_count += 1
                    track_completed(
                        processed_bytes=len(chunk.content.encode("utf-8"))
                    )
                    yield chunk

            knowledge_base.replace_document(
                document,
                counted_chunks(),
                embedding_backend=embedding_backend,
                chunker_fingerprint=chunker_fingerprint,
            )
            tracker.finish_file(path, chunk_count)
            if embedding_backend is not None:
                stats.embeddings_generated += chunk_count
            if chunk_count == 0:
                knowledge_base.remove_document(document.path)
                stats.empty += 1
                status = "empty"
                logger.warning("数据集没有可索引文本：%s", path)
                continue

            stats.indexed += 1
            status = "indexed"
            logger.info("完成数据集索引：%s（%s 个分段）", path, chunk_count)
        except Exception:
            stats.failed += 1
            logger.exception("处理数据集失败：%s", path)
        finally:
            if status == "failed":
                tracker.failed_file(path, progress_chunks)
            report(current, path, status)

    _store_progress_snapshot(stats, tracker.close())
    logger.info(
        "数据集索引任务结束：预估分块 %s，当前完成的分块 %s，总耗时 %.1f 秒",
        stats.estimated_chunks,
        stats.completed_chunks,
        stats.elapsed_seconds,
    )
    return stats
