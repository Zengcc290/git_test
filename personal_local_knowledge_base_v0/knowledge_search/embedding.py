"""Qwen3 document/query embeddings with deterministic inputs and validation."""

from __future__ import annotations

import hashlib
import json
import logging
import math
import os
import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol, Sequence
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import numpy as np


logger = logging.getLogger(__name__)


DEFAULT_EMBEDDING_MODEL = "Qwen/Qwen3-Embedding-0.6B"
DEFAULT_QUERY_INSTRUCTION = (
    "根据用户问题，从知识库中检索能够直接回答问题的相关文档片段"
)
CODE_QUERY_INSTRUCTION = (
    "根据用户问题，从代码库中检索相关的实现、函数、类或调用逻辑"
)
DOCUMENT_INPUT_TEMPLATE_VERSION = "qwen3-document-v2-strict-length"


@dataclass(frozen=True)
class EmbeddingSettings:
    """All values that affect generated vectors or cache identity."""

    model_name: str = DEFAULT_EMBEDDING_MODEL
    model_revision: str | None = None
    dimension: int = 1024
    normalize: bool = True
    batch_size: int = 8
    query_instruction: str = DEFAULT_QUERY_INSTRUCTION

    def __post_init__(self) -> None:
        if not self.model_name.strip():
            raise ValueError("embedding_model 不能为空")
        if not 0 < self.dimension <= 1024:
            raise ValueError("embedding_dimension 必须在 1 到 1024 之间")
        if not self.normalize:
            raise ValueError("当前向量链路要求 normalize_embeddings=true")
        if self.batch_size <= 0:
            raise ValueError("batch_size 必须大于 0")
        if not self.query_instruction.strip():
            raise ValueError("query_instruction 不能为空")

    @property
    def input_fingerprint(self) -> str:
        payload = {
            "document_template": DOCUMENT_INPUT_TEMPLATE_VERSION,
            "query_instruction": self.query_instruction,
        }
        encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()


class EmbeddingBackend(Protocol):
    """Small injectable surface used by chunking, indexing, and retrieval."""

    settings: EmbeddingSettings

    @property
    def model_revision(self) -> str: ...

    def embed_documents(self, texts: Sequence[str]) -> np.ndarray: ...

    def embed_query(self, query: str, *, code: bool = False) -> np.ndarray: ...

    def token_count(self, text: str) -> int: ...


def content_sha256(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def fingerprint_payload(payload: dict[str, object]) -> str:
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def build_document_embedding_input(
    *,
    content: str,
    path: str,
    block_type: str,
    language: str | None = None,
    heading_path: tuple[str, ...] = (),
    symbol_path: tuple[str, ...] = (),
    start_line: int | None = None,
    end_line: int | None = None,
    page_number: int | None = None,
    record_path: str | None = None,
    slide_number: int | None = None,
) -> str:
    """Build the one stable natural-text representation embedded for a chunk."""

    document_type = language or Path(path).suffix.lstrip(".").upper() or block_type
    metadata = [f"文档类型：{document_type}", f"文件：{Path(path).name}"]
    if language:
        metadata.append(f"语言：{language}")
    structure = symbol_path or heading_path
    if structure:
        metadata.append(f"结构：{' > '.join(structure)}")
    if start_line is not None:
        line_range = str(start_line)
        if end_line is not None and end_line != start_line:
            line_range += f"-{end_line}"
        metadata.append(f"行号：{line_range}")
    if page_number is not None:
        metadata.append(f"页码：{page_number}")
    if slide_number is not None:
        metadata.append(f"幻灯片：{slide_number}")
    if record_path:
        metadata.append(f"JSON 路径：{record_path}")
    metadata_text = "\n".join(metadata)
    return f"{metadata_text}\n\n原文内容：\n{content}"


def build_query_embedding_input(
    query: str,
    instruction: str = DEFAULT_QUERY_INSTRUCTION,
) -> str:
    query = query.strip()
    if not query:
        raise ValueError("查询不能为空")
    return f"Instruct: {instruction}\nQuery: {query}"


def validate_vectors(
    vectors: object,
    *,
    expected_count: int,
    dimension: int,
    normalized: bool,
) -> np.ndarray:
    """Return contiguous float32 vectors after enforcing storage invariants."""

    array = np.asarray(vectors, dtype=np.float32)
    if array.shape != (expected_count, dimension):
        raise ValueError(
            "Embedding dimension mismatch: "
            f"expected {(expected_count, dimension)}, got {array.shape}"
        )
    if not np.isfinite(array).all():
        raise ValueError("Embedding 包含 NaN 或 Inf")
    if normalized and expected_count:
        norms = np.linalg.norm(array, axis=1)
        if not np.allclose(norms, 1.0, rtol=1e-4, atol=1e-5):
            raise ValueError("归一化 Embedding 的范数不接近 1.0")
    return np.ascontiguousarray(array, dtype=np.float32)


class RemoteEmbeddingError(RuntimeError):
    """The SSH-forwarded embedding service could not satisfy a request."""

    def __init__(
        self,
        message: str,
        *,
        retryable: bool = False,
        status_code: int | None = None,
    ) -> None:
        super().__init__(message)
        self.retryable = retryable
        self.status_code = status_code


class RemoteQwen3EmbeddingModel:
    """Batch Qwen3 requests through an OpenAI/vLLM-compatible HTTP service."""

    def __init__(
        self,
        settings: EmbeddingSettings | None = None,
        *,
        base_url: str = "http://127.0.0.1:8000",
        api_key: str | None = None,
        timeout: float = 120.0,
        protocol: str = "auto",
        max_retries: int = 5,
        retry_delay: float = 1.0,
    ) -> None:
        self.settings = settings or EmbeddingSettings()
        if not base_url.strip():
            raise ValueError("embedding_base_url 不能为空")
        if timeout <= 0:
            raise ValueError("embedding_timeout 必须大于 0")
        if protocol not in {"auto", "openai", "simple"}:
            raise ValueError("embedding_protocol 必须是 auto、openai 或 simple")
        if max_retries < 0:
            raise ValueError("embedding_max_retries 不能小于 0")
        if retry_delay < 0:
            raise ValueError("embedding_retry_delay 不能小于 0")
        root = base_url.strip().rstrip("/")
        self.base_url = root[:-3] if root.endswith("/v1") else root
        self.api_key = api_key or os.getenv("EMBEDDING_API_KEY", "")
        self.timeout = timeout
        self.protocol = protocol
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self._resolved_protocol: str | None = None
        self._resolved_revision: str | None = None

    def _service_protocol(self) -> str:
        if self._resolved_protocol:
            return self._resolved_protocol
        if self.protocol != "auto":
            self._resolved_protocol = self.protocol
            return self._resolved_protocol
        try:
            openapi = self._request_json("/openapi.json")
            paths = openapi.get("paths")
            if isinstance(paths, dict) and "/embed" in paths:
                self._resolved_protocol = "simple"
                return self._resolved_protocol
        except RemoteEmbeddingError:
            pass
        self._resolved_protocol = "openai"
        return self._resolved_protocol

    def _request_json(
        self,
        path: str,
        *,
        payload: dict[str, object] | None = None,
    ) -> dict[str, object]:
        headers = {"Accept": "application/json"}
        data = None
        if payload is not None:
            headers["Content-Type"] = "application/json"
            data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        request = Request(
            f"{self.base_url}{path}",
            data=data,
            headers=headers,
            method="POST" if payload is not None else "GET",
        )
        for attempt in range(self.max_retries + 1):
            cause: BaseException | None = None
            try:
                with urlopen(request, timeout=self.timeout) as response:
                    raw_bytes = response.read()
            except HTTPError as exc:
                cause = exc
                detail = exc.read().decode("utf-8", errors="replace")[:500]
                if self.api_key:
                    detail = detail.replace(self.api_key, "[REDACTED]")
                retryable = exc.code in {408, 429, 500, 502, 503, 504}
                error = RemoteEmbeddingError(
                    f"Embedding 服务返回 HTTP {exc.code}：{detail}",
                    retryable=retryable,
                    status_code=exc.code,
                )
            except (URLError, OSError, TimeoutError) as exc:
                cause = exc
                error = RemoteEmbeddingError(
                    f"无法连接 Embedding 服务 {self.base_url}：{exc}",
                    retryable=True,
                )
            else:
                try:
                    raw = raw_bytes.decode("utf-8")
                except UnicodeDecodeError as exc:
                    raise RemoteEmbeddingError(
                        "Embedding 服务返回了非 UTF-8 JSON"
                    ) from exc
                try:
                    parsed = json.loads(raw)
                except json.JSONDecodeError as exc:
                    raise RemoteEmbeddingError(
                        "Embedding 服务返回了无效 JSON"
                    ) from exc
                if not isinstance(parsed, dict):
                    raise RemoteEmbeddingError(
                        "Embedding 服务响应必须是 JSON 对象"
                    )
                return parsed

            if not error.retryable or attempt >= self.max_retries:
                raise error from cause
            logger.warning(
                "Embedding 请求临时失败（第 %s/%s 次重试）：%s；%s 秒后重试",
                attempt + 1,
                self.max_retries,
                error,
                self.retry_delay,
            )
            if self.retry_delay:
                time.sleep(self.retry_delay)
        raise AssertionError("unreachable")

    @property
    def model_revision(self) -> str:
        if self._resolved_revision:
            return self._resolved_revision
        if self.settings.model_revision:
            self._resolved_revision = self.settings.model_revision
            return self._resolved_revision
        # A service may expose the lightweight /embed endpoint while also
        # publishing standard model metadata. Use that metadata when present;
        # only legacy simple servers need an explicit revision override.
        try:
            payload = self._request_json("/v1/models")
        except RemoteEmbeddingError:
            if self._service_protocol() == "simple":
                raise RemoteEmbeddingError(
                    "远端 /embed 服务不报告模型 revision；请通过 "
                    "--embedding-revision 或 EMBEDDING_MODEL_REVISION 传入实际 commit hash"
                )
            raise
        models = payload.get("data", [])
        if isinstance(models, list):
            for item in models:
                if not isinstance(item, dict):
                    continue
                if item.get("id") != self.settings.model_name:
                    continue
                for key in ("model_revision", "revision", "commit_hash", "sha"):
                    revision = item.get(key)
                    if isinstance(revision, str) and revision.strip():
                        self._resolved_revision = revision.strip()
                        return self._resolved_revision
                root = str(item.get("root", ""))
                match = re.search(r"[/\\]snapshots[/\\]([0-9a-f]{7,64})", root)
                if match:
                    self._resolved_revision = match.group(1)
                    return self._resolved_revision
        raise RemoteEmbeddingError(
            "远端 /v1/models 未提供模型 commit hash；"
            "请通过 --embedding-revision 显式传入远端实际 revision"
        )

    @staticmethod
    def _normalize(vectors: object) -> np.ndarray:
        array = np.asarray(vectors, dtype=np.float32)
        if array.ndim != 2:
            return array
        norms = np.linalg.norm(array, axis=1, keepdims=True)
        nonzero = norms[:, 0] > 0
        array[nonzero] /= norms[nonzero]
        return array

    def embed_documents(self, texts: Sequence[str]) -> np.ndarray:
        if not texts:
            return np.empty((0, self.settings.dimension), dtype=np.float32)
        batches: list[np.ndarray] = []
        protocol = self._service_protocol()
        for start in range(0, len(texts), self.settings.batch_size):
            batch = list(texts[start : start + self.settings.batch_size])
            if protocol == "simple":
                response = self._request_json(
                    "/embed", payload={"texts": batch}
                )
                vectors = response.get("embeddings")
                if not isinstance(vectors, list) or len(vectors) != len(batch):
                    raise RemoteEmbeddingError(
                        "Embedding 服务返回的向量数量不匹配"
                    )
            else:
                response = self._request_json(
                    "/v1/embeddings",
                    payload={
                        "model": self.settings.model_name,
                        "input": batch,
                        "encoding_format": "float",
                        "dimensions": self.settings.dimension,
                    },
                )
                data = response.get("data")
                if not isinstance(data, list) or len(data) != len(batch):
                    raise RemoteEmbeddingError(
                        "Embedding 服务返回的向量数量不匹配"
                    )
                indices = [
                    item.get("index") if isinstance(item, dict) else None
                    for item in data
                ]
                if not all(isinstance(index, int) for index in indices) or sorted(
                    indices
                ) != list(range(len(batch))):
                    raise RemoteEmbeddingError(
                        "Embedding 服务返回了无效的向量 index"
                    )
                ordered = sorted(data, key=lambda item: int(item["index"]))
                vectors = [item.get("embedding") for item in ordered]
            if not all(isinstance(vector, list) for vector in vectors):
                raise RemoteEmbeddingError("Embedding 服务未返回 float 数组")
            batches.append(self._normalize(vectors))
        combined = np.vstack(batches)
        return validate_vectors(
            combined,
            expected_count=len(texts),
            dimension=self.settings.dimension,
            normalized=self.settings.normalize,
        )

    def embed_query(self, query: str, *, code: bool = False) -> np.ndarray:
        instruction = CODE_QUERY_INSTRUCTION if code else self.settings.query_instruction
        return self.embed_documents(
            [build_query_embedding_input(query, instruction)]
        )[0]

    def token_count(self, text: str) -> int:
        """Use vLLM's tokenizer endpoint when an exact count is required."""

        errors: list[Exception] = []
        for path in ("/tokenize", "/v1/tokenize"):
            try:
                response = self._request_json(
                    path,
                    payload={"model": self.settings.model_name, "prompt": text},
                )
                count = response.get("count")
                if isinstance(count, int):
                    return count
                tokens = response.get("tokens")
                if isinstance(tokens, list):
                    return len(tokens)
            except RemoteEmbeddingError as exc:
                errors.append(exc)
        raise RemoteEmbeddingError(
            "远端服务未提供 /tokenize 或 /v1/tokenize，无法执行精确 Token 检查"
        ) from (errors[-1] if errors else None)

    def fits_token_limit(self, text: str, max_tokens: int) -> bool:
        # Qwen 的 byte-level fallback 不会产生多于 UTF-8 字节数的正文 token。
        # 明显低于上限时使用这个严格上界，接近上限时再请求远端 tokenizer。
        if len(text.encode("utf-8")) + 8 <= max_tokens:
            return True
        return self.token_count(text) <= max_tokens


def cosine_similarity(left: np.ndarray, right: np.ndarray) -> float:
    denominator = float(np.linalg.norm(left) * np.linalg.norm(right))
    if denominator == 0 or not math.isfinite(denominator):
        return 0.0
    return float(np.dot(left, right) / denominator)
