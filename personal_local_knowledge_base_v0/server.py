"""Uvicorn-compatible entry point for the Qwen embedding service.

Usage::

    python -m uvicorn server:app --host 0.0.0.0 --port 8000 --workers 1

Tune the service through the QWEN_* environment variables. The model is
loaded once when Uvicorn imports this module, and the micro-batch worker starts
on ASGI startup.
"""

from __future__ import annotations

import os
import importlib.util
import sys
from pathlib import Path


def _load_embedding_module():
    """Load the implementation even when this wrapper is one directory above the project."""

    here = Path(__file__).resolve().parent
    candidates = (
        here / "scripts" / "qwen_embedding_server.py",
        here / "personal_local_knowledge_base_v0" / "scripts" / "qwen_embedding_server.py",
    )
    for path in candidates:
        if not path.is_file():
            continue
        spec = importlib.util.spec_from_file_location("qwen_embedding_server", path)
        if spec is None or spec.loader is None:
            continue
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        return module
    searched = "\n".join(str(path) for path in candidates)
    raise RuntimeError(
        "找不到 scripts/qwen_embedding_server.py，请同步该文件。已搜索：\n" + searched
    )


_embedding = _load_embedding_module()
DEFAULT_MODEL = _embedding.DEFAULT_MODEL
EmbeddingEngine = _embedding.EmbeddingEngine
create_app = _embedding.create_app


engine = EmbeddingEngine(
    os.getenv("QWEN_EMBEDDING_MODEL", DEFAULT_MODEL),
    revision=os.getenv("QWEN_EMBEDDING_REVISION"),
    max_batch_size=int(os.getenv("QWEN_MAX_BATCH_SIZE", "16")),
    max_batch_tokens=int(os.getenv("QWEN_MAX_BATCH_TOKENS", "8192")),
    max_length=int(os.getenv("QWEN_MAX_LENGTH", "2048")),
    batch_wait_ms=float(os.getenv("QWEN_BATCH_WAIT_MS", "3")),
)
app = create_app(engine)
