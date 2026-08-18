"""Use the local FTS5 indexes as the retrieval stage for RAG."""

from __future__ import annotations

from dataclasses import dataclass

from ..chunking import ChunkingConfig, chunk_text
from ..database import KnowledgeBase
from ..embedding import EmbeddingBackend
from ..models import SearchResult
from ..vector_search import VectorIndex


@dataclass(frozen=True)
class RetrievedChunk:
    """A source chunk and the exact excerpt included in the prompt."""

    citation_id: int
    chunk_id: int
    document_path: str
    filename: str
    file_type: str
    chunk_index: int
    score: float
    content: str
    chunk_indexes: tuple[int, ...] = ()
    heading_path: tuple[str, ...] = ()
    symbol_path: tuple[str, ...] = ()
    start_line: int | None = None
    end_line: int | None = None
    page_number: int | None = None
    record_path: str | None = None
    slide_number: int | None = None
    shape_index: int | None = None

    @property
    def location_parts(self) -> tuple[str, ...]:
        parts: list[str] = []
        if self.heading_path:
            parts.append(f"标题 {' > '.join(self.heading_path)}")
        if self.record_path:
            parts.append(f"JSON 路径 {self.record_path}")
        if self.page_number is not None:
            parts.append(f"第 {self.page_number} 页")
        if self.slide_number is not None:
            parts.append(f"幻灯片 {self.slide_number}")
        if self.shape_index is not None:
            parts.append(f"形状 {self.shape_index}")
        if self.symbol_path:
            separator = "." if self.file_type == "py" else "::"
            parts.append(f"符号 {separator.join(self.symbol_path)}")
        if self.start_line is not None:
            line_range = str(self.start_line)
            if self.end_line is not None and self.end_line != self.start_line:
                line_range += f"-{self.end_line}"
            parts.append(f"行 {line_range}")
        return tuple(parts)

    @property
    def citation(self) -> str:
        indexes = self.chunk_indexes or (self.chunk_index,)
        if len(indexes) == 1:
            chunk_label = str(indexes[0])
        else:
            chunk_label = "、".join(str(index) for index in indexes)
        suffix = "".join(f"，{part}" for part in self.location_parts)
        return f"[{self.citation_id}] {self.filename}，分段 {chunk_label}{suffix}"


@dataclass(frozen=True)
class RetrievalResult:
    """Retrieved chunks plus the bounded context sent to the model."""

    chunks: tuple[RetrievedChunk, ...]
    context: str
    truncated: bool = False

    @property
    def context_chars(self) -> int:
        return len(self.context)


class ChunkRetriever:
    """Match question chunks to structured document chunks without jieba."""

    def __init__(
        self,
        knowledge_base: KnowledgeBase,
        *,
        top_k: int = 5,
        max_context_chars: int = 12_000,
    ) -> None:
        if top_k <= 0:
            raise ValueError("top_k 必须大于 0")
        if max_context_chars <= 0:
            raise ValueError("max_context_chars 必须大于 0")
        self.knowledge_base = knowledge_base
        self.top_k = top_k
        self.max_context_chars = max_context_chars

    def _search(self, question: str) -> list[SearchResult]:
        config = ChunkingConfig()
        question_chunks = chunk_text(
            question,
            chunk_size=config.core_chunk_chars,
            overlap=config.overlap_chars,
        )
        candidates: dict[int, SearchResult] = {}
        per_chunk_limit = max(self.top_k * 4, 20)
        for question_chunk in question_chunks:
            for result in self.knowledge_base.search_chunk_matches(
                question_chunk.content,
                limit=per_chunk_limit,
            ):
                previous = candidates.get(result.chunk_id)
                if previous is None or result.score < previous.score:
                    candidates[result.chunk_id] = result

        return sorted(
            candidates.values(),
            key=lambda result: (
                result.score,
                result.document_path,
                result.chunk_index,
            ),
        )[: self.top_k]

    def retrieve(self, question: str) -> RetrievalResult:
        if not question or not question.strip():
            raise ValueError("问题不能为空")

        search_results = self._search(question)
        blocks: list[str] = []
        chunks: list[RetrievedChunk] = []
        current_length = 0
        truncated = False

        for result in search_results:
            citation_id = len(chunks) + 1
            separator = "\n\n" if blocks else ""
            window = self.knowledge_base.chunk_window(result.chunk_id, radius=1)
            if window:
                chunk_indexes = tuple(chunk.index for chunk in window)
                # 结构信息只放在来源头部；正文保持可直接引用的 canonical 原文。
                window_content = "\n\n".join(chunk.canonical_content for chunk in window)
            else:
                chunk_indexes = (result.chunk_index,)
                window_content = result.content
            chunk_label = "、".join(str(index) for index in chunk_indexes)
            location_parts: list[str] = []
            if result.heading_path:
                location_parts.append(f"标题：{' > '.join(result.heading_path)}")
            if result.record_path:
                location_parts.append(f"JSON 路径：{result.record_path}")
            if result.page_number is not None:
                location_parts.append(f"页码：{result.page_number}")
            if result.slide_number is not None:
                location_parts.append(f"幻灯片：{result.slide_number}")
            if result.shape_index is not None:
                location_parts.append(f"形状：{result.shape_index}")
            if result.symbol_path:
                separator_symbol = "." if result.file_type == "py" else "::"
                location_parts.append(
                    f"符号：{separator_symbol.join(result.symbol_path)}"
                )
            if result.start_line is not None:
                line_range = str(result.start_line)
                if result.end_line is not None and result.end_line != result.start_line:
                    line_range += f"-{result.end_line}"
                location_parts.append(f"行号：{line_range}")
            location = "".join(f"；{part}" for part in location_parts)
            header = (
                f"[{citation_id}] 文件：{result.filename}；分段：{chunk_label}"
                f"{location}\n"
            )
            available = self.max_context_chars - current_length - len(separator) - len(header)
            if available <= 0:
                truncated = True
                break

            excerpt = window_content[:available].rstrip()
            if not excerpt:
                continue

            block = f"{header}{excerpt}"
            blocks.append(f"{separator}{block}")
            current_length += len(separator) + len(block)
            chunks.append(
                RetrievedChunk(
                    citation_id=citation_id,
                    chunk_id=result.chunk_id,
                    document_path=result.document_path,
                    filename=result.filename,
                    file_type=result.file_type,
                    chunk_index=result.chunk_index,
                    score=result.score,
                    content=excerpt,
                    chunk_indexes=chunk_indexes,
                    heading_path=result.heading_path,
                    symbol_path=result.symbol_path,
                    start_line=result.start_line,
                    end_line=result.end_line,
                    page_number=result.page_number,
                    record_path=result.record_path,
                    slide_number=result.slide_number,
                    shape_index=result.shape_index,
                )
            )
            if len(excerpt) < len(window_content):
                truncated = True
                break

        if len(chunks) < len(search_results):
            truncated = True

        return RetrievalResult(
            chunks=tuple(chunks),
            context="".join(blocks),
            truncated=truncated,
        )


class VectorRetriever(ChunkRetriever):
    """Use query embeddings plus sqlite-vec, with a NumPy fallback."""

    def __init__(
        self,
        knowledge_base: KnowledgeBase,
        embedding_backend: EmbeddingBackend,
        *,
        top_k: int = 5,
        max_context_chars: int = 12_000,
        code: bool = False,
    ) -> None:
        super().__init__(
            knowledge_base,
            top_k=top_k,
            max_context_chars=max_context_chars,
        )
        self.vector_index = VectorIndex(knowledge_base, embedding_backend)
        self.code = code

    def _search(self, question: str) -> list[SearchResult]:
        return self.vector_index.search(
            question, top_k=self.top_k, code=self.code
        )


# Compatibility for callers written before question retrieval was separated
# from the jieba-backed keyword search path.
KeywordRetriever = ChunkRetriever
