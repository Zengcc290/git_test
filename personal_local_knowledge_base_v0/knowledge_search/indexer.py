"""文件发现、增量索引和异常隔离。"""

from __future__ import annotations

# fnmatch 支持按目录名或相对路径配置通配符排除规则。
import fnmatch
# logging 用于记录发现、跳过、完成和失败的文件。
import logging
# os.walk 可以在遍历时剪枝，避免进入被排除的目录。
import os
# Callable 让 CLI 可以订阅单文件进度事件；Iterable/Iterator 保持发现流式化。
from collections.abc import Callable, Iterable, Iterator
# Path 负责跨平台的目录递归和扩展名判断。
from pathlib import Path

# 索引流水线依次调用流式清洗、流式分段和数据库写入模块。
from .chunking import iter_chunk_text
from .cleaning import iter_clean_text
from .database import KnowledgeBase
from .extractors import SUPPORTED_SUFFIXES, extract_document, iter_document_text
from .json_parser import (
    DEFAULT_MAX_JSON_SIZE,
    JsonProfile,
    JsonSizeLimitError,
    ensure_json_size,
)
from .models import Chunk, IndexProgress, IndexStats


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

    chunk_index = 0
    for record_text in text_chunks:
        cleaned_text = iter_clean_text([record_text])
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


def index_paths(
    knowledge_base: KnowledgeBase,
    inputs: Iterable[Path],
    *,
    chunk_size: int = 800,
    overlap: int = 100,
    force: bool = False,
    json_profile: JsonProfile | None = None,
    exclude_dirs: Iterable[str | Path] | None = None,
    exclude_files: Iterable[Path] = (),
    max_files: int | None = None,
    max_json_size: int = DEFAULT_MAX_JSON_SIZE,
    progress_callback: Callable[[IndexProgress], None] | None = None,
) -> IndexStats:
    # stats 汇总本次索引结果，供日志和 CLI 摘要使用。
    stats = IndexStats()
    if max_json_size < 0:
        raise ValueError("JSON 最大文件大小不能小于 0")

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

    def report(current: int, path: Path, status: str) -> None:
        if progress_callback is None:
            return
        try:
            progress_callback(
                IndexProgress(
                    current=current,
                    total=len(paths),
                    path=path,
                    status=status,
                )
            )
        except Exception:
            # 进度回调属于展示层，不能因为输出失败而中断索引任务。
            logger.exception("索引进度回调失败：%s", path)

    for current, path in enumerate(paths, start=1):
        report(current, path, "processing")
        status = "failed"
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
            if not force and knowledge_base.is_unchanged(document):
                # 内容哈希不变时不重复清洗、分段和写数据库。
                stats.skipped += 1
                status = "skipped"
                logger.info("跳过未变化文件：%s", path)
                continue

            # 抽取器、清洗器和分段器全部返回迭代器，不在索引器中保存全文。
            source_text = iter_document_text(
                document,
                json_profile=profile,
                max_json_size=max_json_size,
            )
            chunks = _iter_index_chunks(
                source_text,
                chunk_size=chunk_size,
                overlap=overlap,
                separate_records=profile is not None and profile.index_mode == "record",
            )

            # 用计数器包装分段流，只记录数量，不保存已经写入数据库的分段。
            chunk_count = 0

            def counted_chunks():
                nonlocal chunk_count
                for chunk in chunks:
                    chunk_count += 1
                    yield chunk

            # 在事务中替换旧文档，并由数据库层逐个消费分段生成器。
            knowledge_base.replace_document(document, counted_chunks())
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
            report(current, path, status)

    # 返回完整汇总，让 CLI 决定显示和退出状态码。
    return stats
