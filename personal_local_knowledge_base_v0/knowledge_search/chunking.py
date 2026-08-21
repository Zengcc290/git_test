"""按段落和长度切分文档。"""

from __future__ import annotations

from collections.abc import Iterable, Iterator
from dataclasses import dataclass, replace

# Chunk 是分段结果的数据结构。
from .block_parsing import build_embedding_content
from .constants import (
    DEFAULT_CHUNK_OVERLAP_CHARS,
    DEFAULT_CORE_CHUNK_CHARS,
    DEFAULT_MAX_CHUNK_CHARS,
    DEFAULT_MAX_CHUNK_TOKENS,
    DEFAULT_MIN_CHUNK_CHARS,
    DEFAULT_SEMANTIC_MERGE_THRESHOLD,
)
from .embedding import (
    EmbeddingBackend,
    cosine_similarity,
    fingerprint_payload,
    validate_vectors,
)
from .models import Chunk, DocumentBlock


@dataclass(frozen=True)
class ChunkingConfig:
    """Stable V5 chunking parameters; its fingerprint participates in caching."""

    core_chunk_chars: int = DEFAULT_CORE_CHUNK_CHARS
    overlap_chars: int = DEFAULT_CHUNK_OVERLAP_CHARS
    min_chunk_chars: int = DEFAULT_MIN_CHUNK_CHARS
    max_chunk_chars: int = DEFAULT_MAX_CHUNK_CHARS
    semantic_merge_threshold: float = DEFAULT_SEMANTIC_MERGE_THRESHOLD
    max_chunk_tokens: int = DEFAULT_MAX_CHUNK_TOKENS

    def __post_init__(self) -> None:
        if self.core_chunk_chars <= 0:
            raise ValueError("core_chunk_chars 必须大于 0")
        if self.overlap_chars < 0 or self.overlap_chars >= self.max_chunk_chars:
            raise ValueError("overlap_chars 必须满足 0 <= overlap < max_chunk_chars")
        if not 0 < self.min_chunk_chars <= self.core_chunk_chars:
            raise ValueError("min_chunk_chars 必须在 1 到 core_chunk_chars 之间")
        if self.max_chunk_chars < self.core_chunk_chars:
            raise ValueError("max_chunk_chars 不能小于 core_chunk_chars")
        if not -1.0 <= self.semantic_merge_threshold <= 1.0:
            raise ValueError("semantic_merge_threshold 必须在 -1 到 1 之间")
        if self.max_chunk_tokens <= 0:
            raise ValueError("max_chunk_tokens 必须大于 0")

    @property
    def fingerprint(self) -> str:
        return self.fingerprint_for(None)

    def fingerprint_for(
        self,
        backend: EmbeddingBackend | None,
        *,
        semantic_merge_enabled: bool | None = None,
    ) -> str:
        if semantic_merge_enabled is None:
            semantic_merge_enabled = backend is not None
        payload: dict[str, object] = {
            "algorithm": "structure-core-semantic-overlap-v1",
            "core_chunk_chars": self.core_chunk_chars,
            "overlap_chars": self.overlap_chars,
            "min_chunk_chars": self.min_chunk_chars,
            "max_chunk_chars": self.max_chunk_chars,
            "semantic_merge_threshold": self.semantic_merge_threshold,
            "max_chunk_tokens": self.max_chunk_tokens,
            "semantic_merge_enabled": semantic_merge_enabled,
        }
        if backend is not None:
            payload.update(
                {
                    "semantic_model": backend.settings.model_name,
                    "semantic_model_revision": backend.model_revision,
                    "semantic_dimension": backend.settings.dimension,
                    "normalize_embeddings": backend.settings.normalize,
                }
            )
        return fingerprint_payload(payload)


def _find_stream_split_end(text: str, chunk_size: int) -> int:
    """在流式缓存的前 chunk_size 个字符中寻找较自然的切分点。"""

    hard_end = min(len(text), chunk_size)
    if hard_end == len(text):
        return hard_end

    # 只在窗口后半段寻找边界，避免产生过短的分段。
    minimum_boundary = max(1, int(chunk_size * 0.55))
    candidates = [
        text.rfind(mark, minimum_boundary, hard_end)
        for mark in "。！？.!?；;，,\n"
    ]
    boundary = max(candidates, default=-1)
    if boundary >= minimum_boundary:
        return boundary + 1

    # 没有标点时，尽量在空格处切开；中文连续文本会退化为硬切分。
    whitespace = text.rfind(" ", minimum_boundary, hard_end)
    return whitespace if whitespace > 0 else hard_end


def iter_chunk_text(
    text_chunks: Iterable[str],
    chunk_size: int = DEFAULT_CORE_CHUNK_CHARS,
    overlap: int = DEFAULT_CHUNK_OVERLAP_CHARS,
) -> Iterator[Chunk]:
    """把文本块流式切分为 Chunk，内存中最多保留一个窗口及其重叠部分。"""

    # 与 chunk_text 保持相同的参数约束，避免两套实现行为不一致。
    if chunk_size <= 0:
        raise ValueError("chunk_size 必须大于 0")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap 必须满足 0 <= overlap < chunk_size")

    # buffer 是唯一的文本缓存，不会随着整个文件大小无限增长。
    buffer = ""
    chunk_index = 0
    for text_chunk in text_chunks:
        if not text_chunk:
            continue
        buffer += text_chunk

        # 输入块到达后尽快产出完整分段，避免继续累积。
        while len(buffer) > chunk_size:
            end = _find_stream_split_end(buffer, chunk_size)
            content = buffer[:end].strip()
            if content:
                yield Chunk(index=chunk_index, content=content)
                chunk_index += 1

            # 保留尾部 overlap 个字符，让相邻分段共享少量上下文。
            next_start = max(end - overlap, 1)
            buffer = buffer[next_start:]

    # 文件结束后输出最后一个不足目标长度的分段。
    if buffer.strip():
        yield Chunk(index=chunk_index, content=buffer.strip())


def chunk_text(
    text: str,
    chunk_size: int = DEFAULT_CORE_CHUNK_CHARS,
    overlap: int = DEFAULT_CHUNK_OVERLAP_CHARS,
) -> list[Chunk]:
    """兼容小文本调用，并复用流式实现保证相邻分段始终保留重叠。"""

    # [text] 只包装调用者已经提供的这段文本；大文件索引路径使用 iter_chunk_text。
    return list(iter_chunk_text([text], chunk_size=chunk_size, overlap=overlap))


def iter_chunk_blocks(
    blocks: Iterable[DocumentBlock],
    chunk_size: int = DEFAULT_CORE_CHUNK_CHARS,
    overlap: int = DEFAULT_CHUNK_OVERLAP_CHARS,
    *,
    min_chunk_chars: int = DEFAULT_MIN_CHUNK_CHARS,
    max_chunk_chars: int = DEFAULT_MAX_CHUNK_CHARS,
    semantic_merge_threshold: float = DEFAULT_SEMANTIC_MERGE_THRESHOLD,
    max_chunk_tokens: int = DEFAULT_MAX_CHUNK_TOKENS,
    embedding_backend: EmbeddingBackend | None = None,
) -> Iterator[Chunk]:
    """Chunk on non-overlapping cores, merge semantically, then add context."""

    config = ChunkingConfig(
        core_chunk_chars=chunk_size,
        overlap_chars=overlap,
        min_chunk_chars=min(min_chunk_chars, chunk_size),
        max_chunk_chars=max_chunk_chars,
        semantic_merge_threshold=semantic_merge_threshold,
        max_chunk_tokens=max_chunk_tokens,
    )
    core_chunks = [
        core
        for block in blocks
        if block.content.strip()
        for core in _make_core_chunks(block, config, embedding_backend)
    ]
    if not core_chunks:
        return

    if embedding_backend is None:
        vectors = None
    else:
        vectors = validate_vectors(
            embedding_backend.embed_documents(
                [core.content for core in core_chunks]
            ),
            expected_count=len(core_chunks),
            dimension=embedding_backend.settings.dimension,
            normalized=embedding_backend.settings.normalize,
        )

    groups: list[_MergedCore] = []
    current = _MergedCore.from_core(core_chunks[0])
    for index, next_core in enumerate(core_chunks[1:], start=1):
        previous = core_chunks[index - 1]
        separator = "" if previous.block.block_id == next_core.block.block_id else "\n\n"
        candidate_content = f"{current.content}{separator}{next_core.content}"
        similarity = (
            cosine_similarity(vectors[index - 1], vectors[index])
            if vectors is not None
            else -1.0
        )
        can_merge = (
            _same_structure(previous, next_core)
            and not _crosses_hard_boundary(previous, next_core)
            and similarity >= config.semantic_merge_threshold
            and len(candidate_content) <= config.max_chunk_chars
            and _within_token_limit(
                candidate_content,
                current.first.block,
                config,
                embedding_backend,
            )
        )
        if can_merge:
            current = current.append(next_core, separator)
        else:
            groups.append(current)
            current = _MergedCore.from_core(next_core)
    groups.append(current)

    final_texts = [
        _add_final_overlap(groups, index, config, embedding_backend)
        for index in range(len(groups))
    ]
    embedding_inputs = [
        build_embedding_content(_located_block(group), content)
        for group, content in zip(groups, final_texts)
    ]
    final_vectors = (
        validate_vectors(
            embedding_backend.embed_documents(embedding_inputs),
            expected_count=len(embedding_inputs),
            dimension=embedding_backend.settings.dimension,
            normalized=embedding_backend.settings.normalize,
        )
        if embedding_backend is not None
        else None
    )

    for output_index, (group, content, embedding_content) in enumerate(
        zip(groups, final_texts, embedding_inputs)
    ):
        block = _located_block(group)
        yield Chunk(
            index=output_index,
            content=content,
            start_offset=group.first.start_offset,
            embedding_content=embedding_content,
            block_id=_group_block_id(group),
            block_type=block.block_type,
            language=block.language,
            heading_path=block.heading_path,
            symbol_path=block.symbol_path,
            start_line=block.start_line,
            end_line=block.end_line,
            page_number=block.page_number,
            record_path=block.record_path,
            slide_number=block.slide_number,
            shape_index=block.shape_index,
            module_name=block.module_name,
            parameters=block.parameters,
            docstring=block.docstring,
            comments=block.comments,
            hard_boundary_before=group.first.hard_boundary_before,
            hard_boundary_after=group.last.hard_boundary_after,
            embedding_vector=(
                tuple(float(value) for value in final_vectors[output_index])
                if final_vectors is not None
                else None
            ),
        )


def iter_chunk_blocks_batched(
    blocks: Iterable[DocumentBlock],
    chunk_size: int = DEFAULT_CORE_CHUNK_CHARS,
    overlap: int = DEFAULT_CHUNK_OVERLAP_CHARS,
    *,
    min_chunk_chars: int = DEFAULT_MIN_CHUNK_CHARS,
    max_chunk_chars: int = DEFAULT_MAX_CHUNK_CHARS,
    semantic_merge_threshold: float = DEFAULT_SEMANTIC_MERGE_THRESHOLD,
    max_chunk_tokens: int = DEFAULT_MAX_CHUNK_TOKENS,
    embedding_backend: EmbeddingBackend | None = None,
) -> Iterator[Chunk]:
    """Chunk a block stream with bounded core/final embedding batches.

    Batch boundaries are transport boundaries only.  The current merged group
    and its last core vector are carried across batches, so adjacent blocks
    retain the same semantic merge behavior as :func:`iter_chunk_blocks`.
    Callers such as dataset indexing can mark records as hard boundaries on
    their ``DocumentBlock`` values to prevent cross-record merges.
    """

    config = ChunkingConfig(
        core_chunk_chars=chunk_size,
        overlap_chars=overlap,
        min_chunk_chars=min(min_chunk_chars, chunk_size),
        max_chunk_chars=max_chunk_chars,
        semantic_merge_threshold=semantic_merge_threshold,
        max_chunk_tokens=max_chunk_tokens,
    )
    batch_limit = embedding_backend.settings.batch_size if embedding_backend else 1
    pending_cores: list[_CoreChunk] = []
    pending_drafts: list[tuple[_MergedCore, str, str]] = []
    current_group: _MergedCore | None = None
    current_vector = None
    previous_group: _MergedCore | None = None
    output_index = 0

    def flush_drafts() -> Iterator[Chunk]:
        nonlocal pending_drafts, output_index
        if not pending_drafts:
            return
        if embedding_backend is None:
            ready = [None] * len(pending_drafts)
        else:
            vectors = validate_vectors(
                embedding_backend.embed_documents(
                    [embedding_input for _group, _content, embedding_input in pending_drafts]
                ),
                expected_count=len(pending_drafts),
                dimension=embedding_backend.settings.dimension,
                normalized=embedding_backend.settings.normalize,
            )
            ready = list(vectors)
        drafts = pending_drafts
        pending_drafts = []
        for draft, vector in zip(drafts, ready):
            if vector is None:
                yield _materialize_chunk(draft, None, output_index)
            else:
                yield _materialize_chunk(draft, vector, output_index)
            output_index += 1

    def finish_group(group: _MergedCore) -> Iterator[Chunk]:
        nonlocal previous_group
        groups = [group] if previous_group is None else [previous_group, group]
        group_index = 0 if previous_group is None else 1
        content = _add_final_overlap(groups, group_index, config, embedding_backend)
        pending_drafts.append(
            (
                group,
                content,
                build_embedding_content(_located_block(group), content),
            )
        )
        previous_group = group
        if len(pending_drafts) >= batch_limit:
            yield from flush_drafts()

    def consume_core(core: _CoreChunk, vector) -> Iterator[Chunk]:
        nonlocal current_group, current_vector
        if current_group is None:
            current_group = _MergedCore.from_core(core)
            current_vector = vector
            return

        previous = current_group.last
        separator = "" if previous.block.block_id == core.block.block_id else "\n\n"
        similarity = (
            cosine_similarity(current_vector, vector)
            if current_vector is not None and vector is not None
            else -1.0
        )
        candidate_content = f"{current_group.content}{separator}{core.content}"
        can_merge = (
            _same_structure(previous, core)
            and not _crosses_hard_boundary(previous, core)
            and similarity >= config.semantic_merge_threshold
            and len(candidate_content) <= config.max_chunk_chars
            and _within_token_limit(
                candidate_content,
                current_group.first.block,
                config,
                embedding_backend,
            )
        )
        if can_merge:
            current_group = current_group.append(core, separator)
            current_vector = vector
            return

        yield from finish_group(current_group)
        current_group = _MergedCore.from_core(core)
        current_vector = vector

    def flush_cores() -> Iterator[Chunk]:
        nonlocal pending_cores
        if not pending_cores:
            return
        cores = pending_cores
        pending_cores = []
        if embedding_backend is None:
            vectors = [None] * len(cores)
        else:
            vectors = validate_vectors(
                embedding_backend.embed_documents([core.content for core in cores]),
                expected_count=len(cores),
                dimension=embedding_backend.settings.dimension,
                normalized=embedding_backend.settings.normalize,
            )
        for core, vector in zip(cores, vectors):
            yield from consume_core(core, vector)

    for block in blocks:
        if not block.content.strip():
            continue
        block_cores = _make_core_chunks(block, config, embedding_backend)
        # A singleton hard-boundary block can never participate in a semantic
        # merge, so do not spend an embedding request just to compare it.
        if (
            embedding_backend is not None
            and len(block_cores) == 1
            and block_cores[0].hard_boundary_before
            and block_cores[0].hard_boundary_after
        ):
            yield from flush_cores()
            yield from consume_core(block_cores[0], None)
            continue
        for core in block_cores:
            pending_cores.append(core)
            if len(pending_cores) >= batch_limit:
                yield from flush_cores()
    yield from flush_cores()
    if current_group is not None:
        yield from finish_group(current_group)
    yield from flush_drafts()


def _materialize_chunk(draft, vector, output_index: int) -> Chunk:
    group, content, embedding_content = draft
    block = _located_block(group)
    return Chunk(
        index=output_index,
        content=content,
        start_offset=group.first.start_offset,
        embedding_content=embedding_content,
        block_id=_group_block_id(group),
        block_type=block.block_type,
        language=block.language,
        heading_path=block.heading_path,
        symbol_path=block.symbol_path,
        start_line=block.start_line,
        end_line=block.end_line,
        page_number=block.page_number,
        record_path=block.record_path,
        slide_number=block.slide_number,
        shape_index=block.shape_index,
        module_name=block.module_name,
        parameters=block.parameters,
        docstring=block.docstring,
        comments=block.comments,
        hard_boundary_before=group.first.hard_boundary_before,
        hard_boundary_after=group.last.hard_boundary_after,
        embedding_vector=(
            tuple(float(value) for value in vector)
            if vector is not None
            else None
        ),
    )


@dataclass(frozen=True)
class _CoreChunk:
    block: DocumentBlock
    content: str
    part_number: int
    start_offset: int
    start_line: int | None
    end_line: int | None
    hard_boundary_before: bool
    hard_boundary_after: bool


@dataclass(frozen=True)
class _MergedCore:
    cores: tuple[_CoreChunk, ...]
    content: str

    @classmethod
    def from_core(cls, core: _CoreChunk) -> "_MergedCore":
        return cls((core,), core.content)

    @property
    def first(self) -> _CoreChunk:
        return self.cores[0]

    @property
    def last(self) -> _CoreChunk:
        return self.cores[-1]

    def append(self, core: _CoreChunk, separator: str) -> "_MergedCore":
        return _MergedCore((*self.cores, core), f"{self.content}{separator}{core.content}")


def _make_core_chunks(
    block: DocumentBlock,
    config: ChunkingConfig,
    backend: EmbeddingBackend | None,
) -> list[_CoreChunk]:
    """Split one structural unit without overlap; rebalance only a short tail."""

    original = block.content.strip()
    positions: list[tuple[int, int, str]] = []
    cursor = 0
    while cursor < len(original):
        remaining = original[cursor:]
        end = _find_stream_split_end(remaining, config.core_chunk_chars)
        end = _fit_core_to_token_limit(block, remaining, end, config, backend)
        raw = remaining[:end]
        content = raw.strip()
        leading = len(raw) - len(raw.lstrip())
        if content:
            positions.append((cursor + leading, cursor + end, content))
        cursor += max(end, 1)

    if (
        len(positions) > 1
        and len(positions[-1][2]) < config.min_chunk_chars
        and len(positions[-2][2]) + len(positions[-1][2]) <= config.max_chunk_chars
        and _within_token_limit(
            original[positions[-2][0] : positions[-1][1]].strip(),
            block,
            config,
            backend,
        )
    ):
        previous = positions[-2]
        tail = positions[-1]
        positions[-2:] = [(previous[0], tail[1], original[previous[0] : tail[1]].strip())]

    result: list[_CoreChunk] = []
    for part_number, (start, _end, content) in enumerate(positions):
        start_line = block.start_line
        end_line = block.end_line
        if start_line is not None:
            start_line += original[:start].count("\n")
            end_line = start_line + content.count("\n")
        result.append(
            _CoreChunk(
                block=block,
                content=content,
                part_number=part_number,
                start_offset=start,
                start_line=start_line,
                end_line=end_line,
                hard_boundary_before=block.hard_boundary_before and part_number == 0,
                hard_boundary_after=(
                    block.hard_boundary_after and part_number == len(positions) - 1
                ),
            )
        )
    return result


def _fit_core_to_token_limit(
    block: DocumentBlock,
    text: str,
    proposed_end: int,
    config: ChunkingConfig,
    backend: EmbeddingBackend | None,
) -> int:
    if backend is None or _within_token_limit(
        text[:proposed_end].strip(), block, config, backend
    ):
        return proposed_end
    low, high = 1, proposed_end - 1
    best = 0
    while low <= high:
        middle = (low + high) // 2
        if _within_token_limit(text[:middle].strip(), block, config, backend):
            best = middle
            low = middle + 1
        else:
            high = middle - 1
    if best == 0:
        raise ValueError(
            "Embedding 元数据本身已超过 max_chunk_tokens，无法生成有效 Chunk"
        )
    return _find_stream_split_end(text, best)


def _same_structure(left: _CoreChunk, right: _CoreChunk) -> bool:
    return (
        left.block.block_type == right.block.block_type
        and left.block.heading_path == right.block.heading_path
        and left.block.symbol_path == right.block.symbol_path
        and left.block.language == right.block.language
        and left.block.page_number == right.block.page_number
        and left.block.record_path == right.block.record_path
        and left.block.slide_number == right.block.slide_number
    )


def _crosses_hard_boundary(left: _CoreChunk, right: _CoreChunk) -> bool:
    return left.hard_boundary_after or right.hard_boundary_before


def _located_block(group: _MergedCore) -> DocumentBlock:
    return replace(
        group.first.block,
        start_line=group.first.start_line,
        end_line=group.last.end_line,
    )


def _within_token_limit(
    content: str,
    block: DocumentBlock,
    config: ChunkingConfig,
    backend: EmbeddingBackend | None,
) -> bool:
    if backend is None:
        return True
    fits_token_limit = getattr(backend, "fits_token_limit", None)
    if callable(fits_token_limit):
        return bool(fits_token_limit(build_embedding_content(block, content), config.max_chunk_tokens))
    return backend.token_count(build_embedding_content(block, content)) <= config.max_chunk_tokens


def _add_final_overlap(
    groups: list[_MergedCore],
    index: int,
    config: ChunkingConfig,
    backend: EmbeddingBackend | None,
) -> str:
    group = groups[index]
    if index == 0 or config.overlap_chars == 0:
        return group.content
    previous = groups[index - 1]
    if (
        not _same_structure(previous.last, group.first)
        or _crosses_hard_boundary(previous.last, group.first)
    ):
        return group.content

    available = config.max_chunk_chars - len(group.content)
    overlap_size = min(config.overlap_chars, max(available, 0))
    while overlap_size > 0:
        prefix = previous.content[-overlap_size:]
        separator = "" if previous.last.block.block_id == group.first.block.block_id else "\n\n"
        candidate = f"{prefix}{separator}{group.content}"
        if len(candidate) <= config.max_chunk_chars and _within_token_limit(
            candidate, group.first.block, config, backend
        ):
            return candidate
        overlap_size -= 1
    return group.content


def _group_block_id(group: _MergedCore) -> str:
    first = group.first
    last = group.last
    if first.block.block_id == last.block.block_id:
        return f"{first.block.block_id}.{first.part_number}-{last.part_number}"
    return f"{first.block.block_id}.{first.part_number}+{last.block.block_id}.{last.part_number}"
