"""RAG configuration and end-to-end answer orchestration."""

from __future__ import annotations

import json
import logging
import os
import re
import time
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from .llm_client import LLMClient, LLMClientError, TokenUsage
from .prompt import REFUSAL_ANSWER, REFUSAL_PREFIX, build_messages
from .retriever import KeywordRetriever, RetrievedChunk


logger = logging.getLogger(__name__)
CITATION_PATTERN = re.compile(r"\[(\d+)\]")


class CitationValidationError(LLMClientError):
    """The model response did not use only citations from this retrieval."""


@dataclass(frozen=True)
class RagConfig:
    top_k: int = 5
    max_context_chars: int = 12_000
    temperature: float = 0.0

    def __post_init__(self) -> None:
        if self.top_k <= 0:
            raise ValueError("top_k 必须大于 0")
        if self.max_context_chars <= 0:
            raise ValueError("max_context_chars 必须大于 0")
        if not 0 <= self.temperature <= 2:
            raise ValueError("temperature 必须在 0 到 2 之间")

    @classmethod
    def from_file(cls, path: Path) -> "RagConfig":
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except FileNotFoundError as exc:
            raise ValueError(f"RAG 配置文件不存在：{path}") from exc
        except json.JSONDecodeError as exc:
            raise ValueError(f"RAG 配置不是有效 JSON：{path}") from exc
        if not isinstance(data, dict):
            raise ValueError("RAG 配置顶层必须是 JSON 对象")

        allowed = {"top_k", "max_context_chars", "temperature"}
        unknown = sorted(set(data) - allowed)
        if unknown:
            raise ValueError(f"RAG 配置包含未知字段：{', '.join(unknown)}")
        try:
            return cls(
                top_k=int(data.get("top_k", 5)),
                max_context_chars=int(data.get("max_context_chars", 12_000)),
                temperature=float(data.get("temperature", 0)),
            )
        except (TypeError, ValueError) as exc:
            raise ValueError("RAG 配置字段类型无效") from exc


@dataclass(frozen=True)
class AnswerResult:
    question: str
    answer: str
    sources: tuple[RetrievedChunk, ...]
    context_chars: int
    context_truncated: bool
    elapsed_ms: float
    usage: TokenUsage = TokenUsage()
    refused: bool = False


class RagAnswerer:
    """Run retrieval first and create the LLM client only when it is needed."""

    def __init__(
        self,
        retriever: KeywordRetriever,
        *,
        temperature: float = 0.0,
        client_factory: Callable[[], LLMClient] = LLMClient.from_env,
    ) -> None:
        self.retriever = retriever
        self.temperature = temperature
        self.client_factory = client_factory

    def answer(self, question: str) -> AnswerResult:
        started = time.perf_counter()
        retrieval = self.retriever.retrieve(question)

        if not retrieval.chunks:
            result = AnswerResult(
                question=question,
                answer=REFUSAL_ANSWER,
                sources=(),
                context_chars=0,
                context_truncated=retrieval.truncated,
                elapsed_ms=(time.perf_counter() - started) * 1000,
                refused=True,
            )
            self._log_result(result)
            return result

        usage: TokenUsage | None = None
        try:
            response = self.client_factory().complete(
                build_messages(question, retrieval.context),
                temperature=self.temperature,
            )
            usage = response.usage
            refused = response.content.startswith(REFUSAL_PREFIX)
            self._validate_citations(
                response.content,
                retrieval.chunks,
                refused=refused,
            )
        except LLMClientError as exc:
            elapsed_ms = (time.perf_counter() - started) * 1000
            self._log_failure(
                question,
                retrieval.chunks,
                elapsed_ms,
                exc,
                usage=usage,
            )
            raise

        result = AnswerResult(
            question=question,
            answer=response.content,
            sources=retrieval.chunks,
            context_chars=retrieval.context_chars,
            context_truncated=retrieval.truncated,
            elapsed_ms=(time.perf_counter() - started) * 1000,
            usage=response.usage,
            refused=refused,
        )
        self._log_result(result)
        return result

    @staticmethod
    def _validate_citations(
        answer: str,
        sources: tuple[RetrievedChunk, ...],
        *,
        refused: bool,
    ) -> None:
        """Reject missing or invented citations before a response becomes successful."""

        citation_ids = [int(value) for value in CITATION_PATTERN.findall(answer)]
        available_ids = {source.citation_id for source in sources}
        invalid_ids = sorted(set(citation_ids) - available_ids)
        if invalid_ids:
            invalid_text = "、".join(f"[{value}]" for value in invalid_ids)
            available_text = "、".join(f"[{value}]" for value in sorted(available_ids))
            raise CitationValidationError(
                "大模型回答引用校验失败："
                f"引用 {invalid_text} 不属于本次检索结果；"
                f"可用引用为 {available_text}。请重试。"
            )
        if not refused and not citation_ids:
            raise CitationValidationError(
                "大模型回答引用校验失败：非拒答答案没有提供 [n] 格式的引用。"
                "本次回答未被接受，请重试。"
            )

    def _source_records(self, sources: tuple[RetrievedChunk, ...]) -> list[dict[str, object]]:
        return [
            {
                "citation_id": source.citation_id,
                "chunk_id": source.chunk_id,
                "path": self._redact(source.document_path),
                "filename": self._redact(source.filename),
                "chunk_index": source.chunk_index,
                "chunk_indexes": source.chunk_indexes or (source.chunk_index,),
                "score": source.score,
                "content": self._redact(source.content),
            }
            for source in sources
        ]

    @staticmethod
    def _redact(value: str) -> str:
        """Keep configured credentials out of audit records if a model echoes one."""

        # No-hit refusals intentionally do not construct an LLM client, so load
        # dotenv here as well before deciding which value must be removed.
        LLMClient.load_dotenv()
        api_key = os.environ.get("LLM_API_KEY", "")
        if api_key:
            return value.replace(api_key, "[REDACTED]")
        return value

    def _log_result(self, result: AnswerResult) -> None:
        record = {
            "event": "rag_answer",
            "question": self._redact(result.question),
            "retrieval_results": self._source_records(result.sources),
            "context_chars": result.context_chars,
            "context_truncated": result.context_truncated,
            "answer": self._redact(result.answer),
            "refused": result.refused,
            "elapsed_ms": round(result.elapsed_ms, 3),
            "token_usage": {
                "prompt_tokens": result.usage.prompt_tokens,
                "completion_tokens": result.usage.completion_tokens,
                "total_tokens": result.usage.total_tokens,
            },
        }
        logger.info("RAG_RECORD %s", json.dumps(record, ensure_ascii=False))

    def _log_failure(
        self,
        question: str,
        sources: tuple[RetrievedChunk, ...],
        elapsed_ms: float,
        error: LLMClientError,
        *,
        usage: TokenUsage | None = None,
    ) -> None:
        record = {
            "event": "rag_error",
            "question": self._redact(question),
            "retrieval_results": self._source_records(sources),
            "answer": None,
            "elapsed_ms": round(elapsed_ms, 3),
            "token_usage": (
                {
                    "prompt_tokens": usage.prompt_tokens,
                    "completion_tokens": usage.completion_tokens,
                    "total_tokens": usage.total_tokens,
                }
                if usage is not None
                else None
            ),
            "error_type": type(error).__name__,
            "error": self._redact(str(error)),
        }
        logger.error("RAG_RECORD %s", json.dumps(record, ensure_ascii=False))
