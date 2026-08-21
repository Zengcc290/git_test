"""Standard-library HTTP server exposing the knowledge base as a local web app.

The server deliberately uses ``http.server`` rather than a third-party web
framework so the "complete version" runs with only the project's existing
dependencies. It presents a small JSON API consumed by the bundled
single-page interface and reuses the same ``KnowledgeBase``, ``index_paths``,
``VectorRetriever`` and ``RagAnswerer`` objects as the command line.
"""

from __future__ import annotations

import errno
import json
import logging
import mimetypes
import os
import re
import threading
import urllib.parse
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Callable

from ..database import KnowledgeBase
from ..constants import (
    DEFAULT_CHUNK_OVERLAP_CHARS,
    DEFAULT_CORE_CHUNK_CHARS,
    DEFAULT_MAX_SEARCH_LIMIT,
    DEFAULT_SEARCH_LIMIT,
    DEFAULT_UPLOAD_DIR,
    DEFAULT_WEB_HOST,
    DEFAULT_WEB_PORT,
    MAX_CHUNK_SIZE,
    MAX_CONTEXT_CHARS,
    MAX_INDEX_PATHS,
    MAX_JSON_BODY_BYTES,
    MAX_MULTIPART_OVERHEAD,
    MAX_QUESTION_CHARS,
    MAX_UPLOAD_BYTES,
)
from ..embedding import EmbeddingBackend
from ..extractors import SUPPORTED_SUFFIXES
from ..indexer import index_paths
from ..rag.answer import RagAnswerer, RagConfig
from ..rag.llm_client import LLMClient, LLMClientError
from ..rag.retriever import ChunkRetriever, VectorRetriever
from ..rag.prompt import REFUSAL_ANSWER
from ..vector_search import VectorIndex

logger = logging.getLogger(__name__)

# The interface and its assets live beside this module, so the web server is
# self-contained even when the process is launched from another directory.
_STATIC_DIR = Path(__file__).resolve().parent / "static"

# Uploads are written here before being indexed. Keeping them in one directory
# makes document management predictable and lets ``list`` show real paths.
# Accepted extension set mirrors the extractor's supported types.
_UPLOAD_SUFFIXES = SUPPORTED_SUFFIXES

# Keep the limits in one place so both direct callers and HTTP requests use
# the same policy.  The upload limit is deliberately conservative for a local
# browser service; this local tool does not need a large-object store.
_MAX_UPLOAD_BYTES = MAX_UPLOAD_BYTES
_MAX_MULTIPART_OVERHEAD = MAX_MULTIPART_OVERHEAD
_MAX_JSON_BODY_BYTES = MAX_JSON_BODY_BYTES
_MAX_SEARCH_LIMIT = DEFAULT_MAX_SEARCH_LIMIT
_MAX_INDEX_PATHS = MAX_INDEX_PATHS
_MAX_QUESTION_CHARS = MAX_QUESTION_CHARS
_MAX_CHUNK_SIZE = MAX_CHUNK_SIZE
_MAX_CONTEXT_CHARS = MAX_CONTEXT_CHARS


class _ExclusiveThreadingHTTPServer(ThreadingHTTPServer):
    """Bind exclusively so a second server cannot reuse the port on Windows."""

    allow_reuse_address = False


def _search_result_location(result: Any) -> str:
    parts: list[str] = []
    if result.heading_path:
        parts.append(" > ".join(result.heading_path))
    if result.record_path:
        parts.append(f"JSON {result.record_path}")
    if result.page_number is not None:
        parts.append(f"第 {result.page_number} 页")
    if result.slide_number is not None:
        parts.append(f"幻灯片 {result.slide_number}")
    if result.shape_index is not None:
        parts.append(f"形状 {result.shape_index}")
    if result.symbol_path:
        separator = "." if result.file_type == "py" else "::"
        parts.append(separator.join(result.symbol_path))
    if result.start_line is not None:
        line_range = str(result.start_line)
        if result.end_line is not None and result.end_line != result.start_line:
            line_range += f"-{result.end_line}"
        parts.append(f"行 {line_range}")
    return " · ".join(parts)


class KnowledgeWebApp:
    """Bind a database path to the operations exposed over HTTP."""

    def __init__(
        self,
        *,
        db_path: Path,
        upload_dir: Path = DEFAULT_UPLOAD_DIR,
        client_factory: Callable[[], LLMClient] = LLMClient.from_env,
        embedding_backend: EmbeddingBackend | None = None,
    ) -> None:
        self.db_path = Path(db_path).expanduser().resolve()
        self.upload_dir = Path(upload_dir).expanduser().resolve()
        self.client_factory = client_factory
        self.embedding_backend = embedding_backend
        self._lock = threading.RLock()

    def open(self) -> KnowledgeBase:
        # A new connection per request keeps concurrent browser tabs from
        # sharing a single SQLite connection across threads.
        return KnowledgeBase(self.db_path)

    # ------------------------------------------------------------------ API

    def stats(self) -> dict[str, Any]:
        with self._lock:
            with self.open() as knowledge_base:
                return {
                    "database": str(knowledge_base.db_path),
                    "documents": knowledge_base.document_count(),
                    "chunks": knowledge_base.chunk_count(),
                    "search_mode": (
                        "semantic" if self.embedding_backend is not None else "keyword"
                    ),
                }

    def documents(self) -> list[dict[str, Any]]:
        with self._lock:
            with self.open() as knowledge_base:
                return [
                    {
                        "id": document.document_id,
                        "path": document.path,
                        "filename": document.filename,
                        "file_type": document.file_type,
                        "size": document.size,
                        "chunks": document.chunk_count,
                        "indexed_at": document.indexed_at,
                        "parser": document.parser,
                    }
                    for document in knowledge_base.list_documents()
                ]

    def search(
        self,
        query: str,
        limit: int = DEFAULT_SEARCH_LIMIT,
        *,
        semantic: bool | None = None,
    ) -> list[dict[str, Any]]:
        query = str(query).strip()
        if not query:
            return []
        if limit <= 0 or limit > _MAX_SEARCH_LIMIT:
            raise ValueError(f"搜索条数必须在 1 到 {_MAX_SEARCH_LIMIT} 之间。")
        use_semantic = (
            self.embedding_backend is not None if semantic is None else semantic
        )
        with self._lock:
            with self.open() as knowledge_base:
                if use_semantic:
                    if self.embedding_backend is None:
                        raise ValueError("语义检索未配置 Embedding 服务。")
                    results = VectorIndex(
                        knowledge_base, self.embedding_backend
                    ).search(query, top_k=limit)
                else:
                    results = knowledge_base.search(query, limit=limit)
        return [
            {
                "filename": result.filename,
                "file_type": result.file_type,
                "path": result.document_path,
                "chunk_index": result.chunk_index,
                "score": result.score,
                "content": result.content,
                "highlighted": result.highlighted_content,
                "embedding_content": result.embedding_content,
                "block_id": result.block_id,
                "block_type": result.block_type,
                "language": result.language,
                "heading_path": list(result.heading_path),
                "symbol_path": list(result.symbol_path),
                "start_line": result.start_line,
                "end_line": result.end_line,
                "page_number": result.page_number,
                "record_path": result.record_path,
                "slide_number": result.slide_number,
                "shape_index": result.shape_index,
                "location": _search_result_location(result),
            }
            for result in results
        ]

    def ask(
        self,
        question: str,
        config: RagConfig,
        *,
        semantic: bool | None = None,
    ) -> dict[str, Any]:
        question = str(question).strip()
        if not question:
            raise ValueError("问题不能为空。")
        if len(question) > _MAX_QUESTION_CHARS:
            raise ValueError(f"问题不能超过 {_MAX_QUESTION_CHARS} 个字符。")
        use_semantic = (
            self.embedding_backend is not None if semantic is None else semantic
        )
        with self._lock:
            with self.open() as knowledge_base:
                if use_semantic:
                    if self.embedding_backend is None:
                        raise ValueError("语义检索未配置 Embedding 服务。")
                    retriever = VectorRetriever(
                        knowledge_base,
                        self.embedding_backend,
                        top_k=config.top_k,
                        max_context_chars=config.max_context_chars,
                    )
                else:
                    retriever = ChunkRetriever(
                        knowledge_base,
                        top_k=config.top_k,
                        max_context_chars=config.max_context_chars,
                    )
                answerer = RagAnswerer(
                    retriever,
                    temperature=config.temperature,
                    client_factory=self.client_factory,
                )
                try:
                    result = answerer.answer(question)
                except LLMClientError as exc:
                    # Exposed as a structured error so the interface can show it
                    # without ever leaking credentials in a traceback.
                    return {"error": _redact_error(str(exc))}
        return {
            "question": result.question,
            "answer": result.answer,
            "refused": result.refused,
            "elapsed_ms": round(result.elapsed_ms, 2),
            "context_chars": result.context_chars,
            "usage": {
                "prompt_tokens": result.usage.prompt_tokens,
                "completion_tokens": result.usage.completion_tokens,
                "total_tokens": result.usage.total_tokens,
            },
            "sources": [
                {
                    "citation_id": source.citation_id,
                    "filename": source.filename,
                    "file_type": source.file_type,
                    "path": source.document_path,
                    "chunk_index": source.chunk_index,
                    "chunk_indexes": list(source.chunk_indexes or (source.chunk_index,)),
                    "score": source.score,
                    "heading_path": list(source.heading_path),
                    "symbol_path": list(source.symbol_path),
                    "start_line": source.start_line,
                    "end_line": source.end_line,
                    "page_number": source.page_number,
                    "record_path": source.record_path,
                    "slide_number": source.slide_number,
                    "shape_index": source.shape_index,
                    "location": " · ".join(source.location_parts),
                }
                for source in result.sources
            ],
        }

    def index_paths(
        self,
        paths: list[Path],
        *,
        chunk_size: int = DEFAULT_CORE_CHUNK_CHARS,
        overlap: int = DEFAULT_CHUNK_OVERLAP_CHARS,
    ) -> dict[str, Any]:
        if not paths:
            raise ValueError("没有可索引的路径。")
        if len(paths) > _MAX_INDEX_PATHS:
            raise ValueError(f"一次最多索引 {_MAX_INDEX_PATHS} 个路径。")
        if chunk_size <= 0 or chunk_size > _MAX_CHUNK_SIZE:
            raise ValueError(f"chunk_size 必须在 1 到 {_MAX_CHUNK_SIZE} 之间。")
        if overlap < 0 or overlap >= chunk_size:
            raise ValueError("overlap 必须大于等于 0 且小于 chunk_size。")
        with self._lock:
            with self.open() as knowledge_base:
                stats = index_paths(
                    knowledge_base,
                    paths,
                    chunk_size=chunk_size,
                    overlap=overlap,
                    embedding_backend=self.embedding_backend,
                )
        return {
            "files_found": stats.files_found,
            "indexed": stats.indexed,
            "skipped": stats.skipped,
            "empty": stats.empty,
            "failed": stats.failed,
            "oversized": stats.oversized,
        }

    def remove(self, document_id: int) -> dict[str, Any]:
        if document_id <= 0:
            raise ValueError("文档 ID 必须是正整数。")
        with self._lock:
            with self.open() as knowledge_base:
                path = self._path_for_id(knowledge_base, document_id)
                if path is None:
                    return {"removed": False, "reason": "not_found"}
                removed = knowledge_base.remove_document(Path(path))
        return {"removed": bool(removed), "path": path}

    @staticmethod
    def _path_for_id(knowledge_base: KnowledgeBase, document_id: int) -> str | None:
        for document in knowledge_base.list_documents():
            if document.document_id == document_id:
                return document.path
        return None

    # --------------------------------------------------------------- upload

    def save_upload(self, filename: str, data: bytes) -> tuple[str, str]:
        """Persist an uploaded file and return its real path plus basename."""
        if not isinstance(data, (bytes, bytearray)):
            raise ValueError("上传内容无效。")
        if len(data) == 0:
            raise ValueError("上传文件为空。")
        if len(data) > _MAX_UPLOAD_BYTES:
            raise ValueError("上传文件超过 512MB 上限。")
        if not filename:
            raise ValueError("上传文件缺少文件名。")
        # Normalize both URL-style and Windows separators before taking the
        # basename.  This keeps the upload inside upload_dir on every host.
        filename = str(filename).replace("\\", "/")
        safe_name = Path(filename).name
        if safe_name in {"", ".", ".."} or "\x00" in safe_name:
            raise ValueError("上传文件名无效。")
        suffix = Path(safe_name).suffix.lower()
        if suffix not in _UPLOAD_SUFFIXES:
            raise ValueError(
                "不支持的文件类型；仅支持 TXT、Markdown、PDF、PPTX、JSON、"
                "Python 和 C/C++。"
            )
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        upload_root = self.upload_dir.resolve()
        target = upload_root / safe_name
        # Avoid silently overwriting an existing upload with the same name.
        counter = 1
        while target.exists():
            target = self.upload_dir / f"{target.stem}-{counter}{target.suffix}"
            counter += 1
        # The resolved target check also protects deployments where an upload
        # directory contains a symlink created outside this process.
        if target.resolve().parent != upload_root:
            raise ValueError("上传路径无效。")
        target.write_bytes(data)
        return str(target.resolve()), target.name


def _redact_error(message: str) -> str:
    """Remove credentials from errors returned through the browser API."""

    # LLMClient already sanitizes its own HTTP errors.  This second boundary is
    # intentional: custom client factories used by tests or local adapters may
    # raise an error containing the configured key directly.
    LLMClient.load_dotenv()
    api_key = os.environ.get("LLM_API_KEY", "")
    if api_key:
        message = message.replace(api_key, "[REDACTED]")
    base_url = os.environ.get("LLM_BASE_URL", "")
    if base_url:
        message = message.replace(base_url, "[REDACTED_URL]")
    return message


class KnowledgeRequestHandler(BaseHTTPRequestHandler):
    """Route HTTP requests to :class:`KnowledgeWebApp`.

    ``server`` carries the app instance and a RAG configuration loader so the
    handler stays independent of any specific database path.
    """

    server_version = "KnowledgeBaseWeb/1.0"

    @property
    def app(self) -> KnowledgeWebApp:
        return self.server.app  # type: ignore[attr-defined]

    @property
    def rag_config(self) -> RagConfig:
        return self.server.rag_config()  # type: ignore[attr-defined]

    def log_message(self, format: str, *args: Any) -> None:
        logger.info("%s - %s", self.address_string(), format % args)

    # ------------------------------------------------------------ plumbing

    def _send_json(self, payload: Any, status: int = HTTPStatus.OK) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self) -> Any:
        try:
            length = int(self.headers.get("Content-Length") or 0)
        except ValueError as exc:
            raise ValueError("请求体长度无效。") from exc
        if length <= 0 or length > _MAX_JSON_BODY_BYTES:
            raise ValueError("请求体无效或过大。")
        raw = self.rfile.read(length)
        try:
            return json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("请求体不是有效 JSON。") from exc

    def _read_json_object(self) -> dict[str, Any]:
        payload = self._read_json()
        if not isinstance(payload, dict):
            raise ValueError("JSON 请求体必须是对象。")
        return payload

    def _static(self, path: str) -> None:
        if path in ("", "/"):
            path = "/index.html"
        relative = urllib.parse.unquote(path.lstrip("/"))
        candidate = (_STATIC_DIR / relative).resolve()
        if candidate != _STATIC_DIR and _STATIC_DIR not in candidate.parents:
            self.send_error(HTTPStatus.FORBIDDEN)
            return
        if not candidate.is_file():
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        content_type = mimetypes.guess_type(str(candidate))[0] or "application/octet-stream"
        body = candidate.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    # -------------------------------------------------------------- routes

    def do_GET(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API
        parsed = urllib.parse.urlsplit(self.path)
        route = parsed.path
        query = urllib.parse.parse_qs(parsed.query)
        try:
            if route in ("/", "/index.html", "/app.css", "/app.js", "/favicon.ico"):
                self._static(route)
                return
            if route == "/api/stats":
                self._send_json(self.app.stats())
                return
            if route == "/api/documents":
                self._send_json({"documents": self.app.documents()})
                return
            if route == "/api/search":
                term = (query.get("q") or [""])[0].strip()
                if not term:
                    self._send_json({"results": []})
                    return
                try:
                    limit = int(
                        (query.get("limit") or [str(DEFAULT_SEARCH_LIMIT)])[0]
                    )
                except (TypeError, ValueError) as exc:
                    raise ValueError("limit 必须是整数。") from exc
                mode = (query.get("mode") or [None])[0]
                self._send_json(
                    {
                        "results": self.app.search(
                            term,
                            limit=limit,
                            semantic=_semantic_option({"mode": mode}),
                        )
                    }
                )
                return
            self.send_error(HTTPStatus.NOT_FOUND)
        except (OSError, ValueError, RuntimeError) as exc:
            logger.warning("GET %s 失败：%s", route, exc)
            self._send_json({"error": str(exc)}, HTTPStatus.BAD_REQUEST)

    def do_POST(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API
        parsed = urllib.parse.urlsplit(self.path)
        route = parsed.path
        try:
            if route == "/api/search":
                payload = self._read_json_object()
                term = str(payload.get("q", "")).strip()
                limit = int(payload.get("limit", DEFAULT_SEARCH_LIMIT))
                self._send_json(
                    {
                        "results": self.app.search(
                            term,
                            limit=limit,
                            semantic=_semantic_option(payload),
                        )
                    }
                )
                return
            if route == "/api/ask":
                payload = self._read_json_object()
                question = str(payload.get("question", "")).strip()
                if not question:
                    raise ValueError("问题不能为空。")
                config = self._config_from(payload, self.rag_config)
                self._send_json(
                    self.app.ask(
                        question,
                        config,
                        semantic=_semantic_option(payload),
                    )
                )
                return
            if route == "/api/index":
                payload = self._read_json_object()
                raw_paths = payload.get("paths", [])
                if not isinstance(raw_paths, list) or not all(
                    isinstance(item, str) and item.strip() for item in raw_paths
                ):
                    raise ValueError("paths 必须是非空字符串数组。")
                paths = [Path(item).expanduser() for item in raw_paths]
                if not paths:
                    raise ValueError("没有可索引的路径。")
                chunk_size = int(payload.get("chunk_size", DEFAULT_CORE_CHUNK_CHARS))
                overlap = int(
                    payload.get("overlap", DEFAULT_CHUNK_OVERLAP_CHARS)
                )
                self._send_json(
                    self.app.index_paths(
                        paths, chunk_size=chunk_size, overlap=overlap
                    )
                )
                return
            if route == "/api/remove":
                payload = self._read_json_object()
                document_id = int(payload.get("id"))
                self._send_json(self.app.remove(document_id))
                return
            if route == "/api/upload":
                filename, data = self._read_upload()
                saved_path, saved_name = self.app.save_upload(filename, data)
                result = self.app.index_paths([Path(saved_path)])
                self._send_json(
                    {
                        "filename": saved_name,
                        "path": saved_path,
                        "index": result,
                    }
                )
                return
            self.send_error(HTTPStatus.NOT_FOUND)
        except ValueError as exc:
            self._send_json({"error": str(exc)}, HTTPStatus.BAD_REQUEST)
        except LLMClientError as exc:
            self._send_json({"error": str(exc)}, HTTPStatus.BAD_GATEWAY)
        except Exception:
            logger.exception("POST %s 失败", route)
            self._send_json({"error": "服务器内部错误。"}, HTTPStatus.INTERNAL_SERVER_ERROR)

    def _config_from(self, payload: dict[str, Any], base: RagConfig) -> RagConfig:
        try:
            top_k = int(payload.get("top_k", base.top_k))
            max_context_chars = int(
                payload.get("max_context_chars", base.max_context_chars)
            )
            temperature = float(payload.get("temperature", base.temperature))
        except (TypeError, ValueError) as exc:
            raise ValueError("问答参数类型无效。") from exc
        if top_k > _MAX_SEARCH_LIMIT:
            raise ValueError(f"top_k 不能超过 {_MAX_SEARCH_LIMIT}。")
        if max_context_chars > _MAX_CONTEXT_CHARS:
            raise ValueError(f"max_context_chars 不能超过 {_MAX_CONTEXT_CHARS}。")
        return RagConfig(
            top_k=top_k,
            max_context_chars=max_context_chars,
            temperature=temperature,
        )

    def _read_upload(self) -> tuple[str, bytes]:
        content_type = self.headers.get("Content-Type", "")
        if not content_type.startswith("multipart/form-data"):
            raise ValueError("上传请求必须是 multipart/form-data。")
        try:
            length = int(self.headers.get("Content-Length") or 0)
        except ValueError as exc:
            raise ValueError("上传请求长度无效。") from exc
        if length <= 0 or length > _MAX_UPLOAD_BYTES + _MAX_MULTIPART_OVERHEAD:
            raise ValueError("上传文件无效或超过大小上限。")
        body = self.rfile.read(length)
        filename, data = _parse_multipart(body, content_type)
        if len(data) > _MAX_UPLOAD_BYTES:
            raise ValueError("上传文件超过 512MB 上限。")
        return filename, data


def _parse_multipart(body: bytes, content_type: str) -> tuple[str, bytes]:
    """Minimal multipart parser for a single file part.

    The standard library has no public multipart parser, so this handles the
    narrow shape produced by the bundled frontend. It extracts the boundary
    from Content-Type and the filename/data from the first file field.
    """
    match = re.search(r"(?:^|;)\s*boundary=(?:\"([^\"]+)\"|([^;\s]+))", content_type, re.I)
    if match is None:
        raise ValueError("multipart 请求缺少 boundary。")
    boundary_text = match.group(1) or match.group(2) or ""
    if not boundary_text or len(boundary_text) > 200:
        raise ValueError("multipart boundary 无效。")
    boundary = boundary_text.encode("utf-8")
    delimiter = b"--" + boundary
    if delimiter not in body:
        raise ValueError("multipart 请求体无效。")

    segments = body.split(delimiter)
    for segment in segments:
        if not segment.strip(b"\r\n"):
            continue
        header_end = segment.find(b"\r\n\r\n")
        if header_end == -1:
            continue
        header_block = segment[:header_end].decode("utf-8", errors="replace")
        headers = {}
        for line in header_block.split("\r\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                headers[key.strip().lower()] = value.strip()
        disposition = headers.get("content-disposition", "")
        if "filename=" not in disposition.lower():
            continue
        filename = _extract_quoted(disposition, "filename")
        data = segment[header_end + 4 :].rstrip(b"\r\n")
        return filename, data
    raise ValueError("multipart 请求中没有文件。")


def _extract_quoted(header: str, key: str) -> str:
    match = re.search(
        rf"(?:^|;)\s*{re.escape(key)}=(?:\"((?:[^\"\\]|\\.)*)\"|([^;]*))",
        header,
        re.I,
    )
    if match is None:
        return ""
    quoted, bare = match.groups()
    if quoted is not None:
        return quoted.replace(r"\"", '"').replace(r"\\", "\\")
    return (bare or "").strip()


def _semantic_option(payload: dict[str, Any]) -> bool | None:
    """Parse the optional retrieval mode without breaking old API clients."""

    mode = payload.get("mode")
    if mode is None or mode == "":
        return None
    if mode in {"semantic", "vector"}:
        return True
    if mode in {"keyword", "fts"}:
        return False
    raise ValueError("mode 必须是 semantic、vector 或 keyword。")


def create_server(
    app: KnowledgeWebApp,
    rag_config: Callable[[], RagConfig],
    host: str = DEFAULT_WEB_HOST,
    port: int = DEFAULT_WEB_PORT,
) -> ThreadingHTTPServer:
    handler = KnowledgeRequestHandler
    server = _ExclusiveThreadingHTTPServer((host, port), handler)
    server.app = app  # type: ignore[attr-defined]
    server.rag_config = rag_config  # type: ignore[attr-defined]
    return server


def run_web(
    *,
    db_path: Path,
    host: str = DEFAULT_WEB_HOST,
    port: int = DEFAULT_WEB_PORT,
    upload_dir: Path = DEFAULT_UPLOAD_DIR,
    embedding_backend: EmbeddingBackend | None = None,
) -> None:
    """Start the blocking web server for CLI use."""
    app = KnowledgeWebApp(
        db_path=db_path,
        upload_dir=upload_dir,
        embedding_backend=embedding_backend,
    )
    rag_config_path = Path("configs/rag.json")
    if not rag_config_path.exists():
        rag_config_path = Path(__file__).resolve().parents[2] / "configs" / "rag.json"

    def load_config() -> RagConfig:
        if rag_config_path.exists():
            return RagConfig.from_file(rag_config_path)
        return RagConfig()

    try:
        server = create_server(app, load_config, host=host, port=port)
    except OSError as exc:
        if exc.errno == errno.EADDRINUSE or getattr(exc, "winerror", None) == 10048:
            raise RuntimeError(f"端口 {port} 已被占用，Web 服务未启动。") from None
        raise
    logger.info("知识库网页已启动：http://%s:%s/", host, port)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
