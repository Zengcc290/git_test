"""Reuse the V1 FTS5 search as the retrieval stage for RAG."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations

from ..database import KnowledgeBase
from ..models import SearchResult
from ..tokenization import tokenize_for_search


_QUESTION_STOPWORDS = {
    "a",
    "an",
    "are",
    "can",
    "could",
    "does",
    "explain",
    "how",
    "is",
    "please",
    "the",
    "what",
    "why",
    "介绍",
    "报道",
    "什么",
    "作用",
    "使用",
    "可以",
    "吗",
    "呢",
    "和",
    "哪些",
    "如何",
    "怎么",
    "怎样",
    "是否",
    "是",
    "有",
    "有什么",
    "的",
    "能否",
    "请",
    "请问",
    "解释",
    "为什么",
    "与",
    "区别",
    "各",
    "各赢",
    "多少",
    "多久",
    "哪个",
    "分别",
    "情况",
    "统计",
    "赛后",
    "最终",
    "比赛",
    "赛季",
    "总结",
    "提前",
    "结束",
    "发生",
    "时候",
    "做",
    "场",
    "类",
    "词",
    "他",
    "又",
}


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

    @property
    def citation(self) -> str:
        indexes = self.chunk_indexes or (self.chunk_index,)
        if len(indexes) == 1:
            chunk_label = str(indexes[0])
        else:
            chunk_label = "、".join(str(index) for index in indexes)
        return f"[{self.citation_id}] {self.filename}，分段 {chunk_label}"


@dataclass(frozen=True)
class RetrievalResult:
    """Retrieved chunks plus the bounded context sent to the model."""

    chunks: tuple[RetrievedChunk, ...]
    context: str
    truncated: bool = False

    @property
    def context_chars(self) -> int:
        return len(self.context)


class KeywordRetriever:
    """Retrieve FTS5 results and fit them into a deterministic char budget."""

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

    @staticmethod
    def _query_tokens(question: str) -> list[str]:
        tokens: list[str] = []
        seen: set[str] = set()
        for token in tokenize_for_search(question):
            normalized = token.casefold()
            if normalized in _QUESTION_STOPWORDS or normalized in seen:
                continue
            if len(normalized) == 1 and not normalized.isdigit():
                continue
            seen.add(normalized)
            tokens.append(token)
        return tokens

    def _search(self, question: str) -> list[SearchResult]:
        tokens = self._query_tokens(question)
        if not tokens:
            return []

        results = self.knowledge_base.search(" ".join(tokens), limit=self.top_k)
        if results or len(tokens) == 1:
            return results

        # V1 uses precise AND matching. A long natural question often contains one
        # unmatched descriptive word. Pair queries preserve entity co-occurrence,
        # which is crucial in a large corpus where single common terms are noisy.
        candidates: dict[int, dict[str, object]] = {}
        search_tokens = tokens[:12]
        pair_queries = combinations(search_tokens, 2)
        for left, right in pair_queries:
            for rank, result in enumerate(
                self.knowledge_base.search(
                    f'"{left}" "{right}"',
                    limit=max(self.top_k, 10),
                ),
                start=1,
            ):
                candidate = candidates.setdefault(
                    result.chunk_id,
                    {"result": result, "pair_hits": 0, "rank_sum": 0},
                )
                candidate["pair_hits"] = int(candidate["pair_hits"]) + 1
                candidate["rank_sum"] = int(candidate["rank_sum"]) + rank

        # If no pair exists (for example a one-keyword question), retain the
        # original single-token fallback behavior.
        if not candidates:
            for token in search_tokens:
                for rank, result in enumerate(
                    self.knowledge_base.search(token, limit=max(self.top_k, 10)),
                    start=1,
                ):
                    candidate = candidates.setdefault(
                        result.chunk_id,
                        {"result": result, "pair_hits": 0, "rank_sum": 0},
                    )
                    candidate["rank_sum"] = int(candidate["rank_sum"]) + rank

        def matched_token_count(candidate: dict[str, object]) -> int:
            content = candidate["result"].content.casefold()
            return sum(token.casefold() in content for token in search_tokens)

        ranked = sorted(
            candidates.values(),
            key=lambda candidate: (
                -matched_token_count(candidate),
                -int(candidate["pair_hits"]),
                int(candidate["rank_sum"]),
                candidate["result"].score,
                candidate["result"].document_path,
                candidate["result"].chunk_index,
            ),
        )
        return [candidate["result"] for candidate in ranked[: self.top_k]]

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
                window_content = "\n\n".join(
                    f"[分段 {chunk.index}]\n{chunk.content}" for chunk in window
                )
            else:
                chunk_indexes = (result.chunk_index,)
                window_content = result.content
            chunk_label = "、".join(str(index) for index in chunk_indexes)
            header = f"[{citation_id}] 文件：{result.filename}；分段：{chunk_label}\n"
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
