"""Local web interface for the knowledge base.

The web layer reuses the existing CLI-era pipeline (SQLite FTS5 search,
keyword retrieval and citation-checked RAG) behind a small standard-library
HTTP server, so no extra runtime dependency is required to open it.
"""

from .app import KnowledgeWebApp, create_server, run_web

__all__ = ["KnowledgeWebApp", "create_server", "run_web"]


