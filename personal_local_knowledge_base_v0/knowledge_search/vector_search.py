"""SQLite vector retrieval with sqlite-vec and a NumPy compatibility fallback."""

from __future__ import annotations

import logging
import sqlite3
from pathlib import Path
from threading import RLock

import numpy as np

from .constants import DEFAULT_RAG_TOP_K

from .database import KnowledgeBase
from .embedding import EmbeddingBackend, validate_vectors
from .models import SearchResult

logger = logging.getLogger(__name__)


class SqliteVecUnavailable(RuntimeError):
    """The optional sqlite-vec extension cannot be used on this connection."""


def _load_sqlite_vec(connection: sqlite3.Connection):
    """Load sqlite-vec once and return its Python helper module."""

    try:
        import sqlite_vec
    except ImportError as exc:  # pragma: no cover - depends on environment
        raise SqliteVecUnavailable(
            "未安装 sqlite-vec；将回退到 NumPy 向量检索"
        ) from exc

    try:
        # sqlite_vec.load uses SQLite's extension loading API. Disable it again
        # immediately after loading so this connection cannot load arbitrary
        # extensions for the remainder of the request.
        connection.enable_load_extension(True)
        sqlite_vec.load(connection)
        connection.enable_load_extension(False)
    except (AttributeError, OSError, sqlite3.Error) as exc:
        try:
            connection.enable_load_extension(False)
        except (AttributeError, sqlite3.Error):
            pass
        raise SqliteVecUnavailable(
            f"sqlite-vec 扩展加载失败；将回退到 NumPy 向量检索：{exc}"
        ) from exc
    return sqlite_vec


class SqliteVecVectorIndex:
    """Persistent sqlite-vec KNN retrieval for one embedding configuration."""

    _META_TABLE = "embedding_vec_meta"

    def __init__(self, knowledge_base: KnowledgeBase, backend: EmbeddingBackend) -> None:
        self.knowledge_base = knowledge_base
        self.backend = backend
        self._lock = RLock()
        try:
            self._sqlite_vec = _load_sqlite_vec(knowledge_base.connection)
            self._model_id = knowledge_base.embedding_model_id(backend)
            self._dimension = backend.settings.dimension
            self._table = f"embeddings_vec_{self._model_id}"
            self._ensure_schema()
        except sqlite3.Error as exc:
            raise SqliteVecUnavailable(
                f"sqlite-vec 虚拟表不可用；将回退到 NumPy 向量检索：{exc}"
            ) from exc

    def _ensure_schema(self) -> None:
        connection = self.knowledge_base.connection
        connection.execute(
            f"CREATE VIRTUAL TABLE IF NOT EXISTS {self._table} "
            f"USING vec0(embedding float[{self._dimension}])"
        )
        connection.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {self._META_TABLE} (
                embedding_model_id INTEGER PRIMARY KEY,
                dimension INTEGER NOT NULL,
                vector_count INTEGER NOT NULL,
                latest_updated_at TEXT NOT NULL
            )
            """
        )

    def _sync_if_needed(self) -> int:
        """Rebuild the derived vec table only after the source cache changes."""

        knowledge_base = self.knowledge_base
        signature = knowledge_base.embedding_cache_signature(self.backend)
        connection = knowledge_base.connection
        state = connection.execute(
            f"SELECT dimension, vector_count, latest_updated_at "
            f"FROM {self._META_TABLE} WHERE embedding_model_id = ?",
            (self._model_id,),
        ).fetchone()
        table_count = int(
            connection.execute(f"SELECT count(*) FROM {self._table}").fetchone()[0]
        )
        if (
            state is not None
            and int(state[0]) == self._dimension
            and int(state[1]) == signature[1]
            and str(state[2]) == signature[2]
            and table_count == signature[1]
        ):
            return signature[1]

        rows = connection.execute(
            """
            SELECT chunk_id, vector, vector_dtype
            FROM embeddings
            WHERE embedding_model_id = ?
            ORDER BY chunk_id
            """,
            (self._model_id,),
        ).fetchall()
        for row in rows:
            if row["vector_dtype"] != "float32" or not knowledge_base._valid_vector_blob(
                row["vector"], self.backend
            ):
                raise ValueError(f"Chunk {row['chunk_id']} 的 Embedding 数据无效")

        with connection:
            connection.execute(f"DELETE FROM {self._table}")
            connection.executemany(
                f"INSERT INTO {self._table}(rowid, embedding) VALUES (?, ?)",
                (
                    (int(row["chunk_id"]), sqlite3.Binary(row["vector"]))
                    for row in rows
                ),
            )
            connection.execute(
                f"""
                INSERT INTO {self._META_TABLE}(
                    embedding_model_id, dimension, vector_count, latest_updated_at
                ) VALUES (?, ?, ?, ?)
                ON CONFLICT(embedding_model_id) DO UPDATE SET
                    dimension = excluded.dimension,
                    vector_count = excluded.vector_count,
                    latest_updated_at = excluded.latest_updated_at
                """,
                (self._model_id, self._dimension, signature[1], signature[2]),
            )
        return signature[1]

    def _knn(self, query_blob: bytes, limit: int) -> list[sqlite3.Row]:
        return self.knowledge_base.connection.execute(
            f"""
            SELECT rowid, distance
            FROM {self._table}
            WHERE embedding MATCH ? AND k = ?
            ORDER BY distance ASC
            """,
            (query_blob, limit),
        ).fetchall()

    @staticmethod
    def _score(distance: float) -> float:
        # sqlite-vec's default metric is Euclidean distance. Unit-normalized
        # vectors satisfy cosine = 1 - (L2 distance squared / 2).
        return 1.0 - (float(distance) ** 2) / 2.0

    def search(
        self,
        query: str,
        *,
        top_k: int = DEFAULT_RAG_TOP_K,
        code: bool = False,
        file_type: str | None = None,
        path: Path | None = None,
    ) -> list[SearchResult]:
        if top_k <= 0:
            raise ValueError("top_k 必须大于 0")
        if not query.strip():
            raise ValueError("查询不能为空")

        with self._lock:
            vector_count = self._sync_if_needed()
            if vector_count == 0:
                return []
            query_vector = validate_vectors(
                [self.backend.embed_query(query, code=code)],
                expected_count=1,
                dimension=self.backend.settings.dimension,
                normalized=self.backend.settings.normalize,
            )[0]
            query_blob = self._sqlite_vec.serialize_float32(query_vector.tolist())
            allowed = self.knowledge_base.vector_candidate_chunk_ids(
                file_type=file_type, path=path
            )
            target = min(top_k, len(allowed)) if allowed is not None else top_k
            if target <= 0:
                return []

            # A filtered KNN query may need more than top_k candidates before
            # enough rows survive the document/path filter. Widen progressively
            # and stop at the complete vector table when necessary.
            requested = min(vector_count, max(target, top_k * 8))
            selected: list[tuple[int, float]] = []
            while True:
                rows = self._knn(query_blob, requested)
                selected = [
                    (int(row["rowid"]), self._score(row["distance"]))
                    for row in rows
                    if allowed is None or int(row["rowid"]) in allowed
                ][:target]
                if len(selected) >= target or requested >= vector_count:
                    break
                requested = min(vector_count, requested * 2)

            chunk_ids = [chunk_id for chunk_id, _score in selected]
            scores = [score for _chunk_id, score in selected]
        return self.knowledge_base.results_for_vector_scores(chunk_ids, scores, query)


class VectorIndex:
    """Prefer sqlite-vec and keep NumPy as a transparent compatibility fallback."""

    def __init__(
        self,
        knowledge_base: KnowledgeBase,
        backend: EmbeddingBackend,
        *,
        prefer_sqlite_vec: bool = True,
    ) -> None:
        if prefer_sqlite_vec:
            try:
                self._index = SqliteVecVectorIndex(knowledge_base, backend)
                self.backend_name = "sqlite-vec"
                return
            except SqliteVecUnavailable as exc:
                logger.info("%s", exc)
        self._index = NumpyVectorIndex(knowledge_base, backend)
        self.backend_name = "numpy"

    def search(self, *args, **kwargs) -> list[SearchResult]:
        return self._index.search(*args, **kwargs)


class NumpyVectorIndex:
    """Cache one exact embedding configuration and invalidate on DB changes."""

    def __init__(self, knowledge_base: KnowledgeBase, backend: EmbeddingBackend) -> None:
        self.knowledge_base = knowledge_base
        self.backend = backend
        self._signature: tuple[int, int, str] | None = None
        self._chunk_ids = np.empty(0, dtype=np.int64)
        self._vectors = np.empty(
            (0, backend.settings.dimension), dtype=np.float32
        )
        self._lock = RLock()

    def _refresh_if_needed(self) -> None:
        signature = self.knowledge_base.embedding_cache_signature(self.backend)
        if signature == self._signature:
            return
        chunk_ids, vectors = self.knowledge_base.load_embedding_matrix(self.backend)
        self._chunk_ids = chunk_ids
        self._vectors = vectors
        self._signature = signature

    def search(
        self,
        query: str,
        *,
        top_k: int = DEFAULT_RAG_TOP_K,
        code: bool = False,
        file_type: str | None = None,
        path: Path | None = None,
    ) -> list[SearchResult]:
        if top_k <= 0:
            raise ValueError("top_k 必须大于 0")
        if not query.strip():
            raise ValueError("查询不能为空")
        with self._lock:
            self._refresh_if_needed()
            if self._vectors.shape[0] == 0:
                return []
            query_vector = validate_vectors(
                [self.backend.embed_query(query, code=code)],
                expected_count=1,
                dimension=self.backend.settings.dimension,
                normalized=self.backend.settings.normalize,
            )[0]
            allowed = self.knowledge_base.vector_candidate_chunk_ids(
                file_type=file_type, path=path
            )
            if allowed is None:
                candidate_indices = np.arange(self._chunk_ids.size)
            else:
                candidate_indices = np.flatnonzero(
                    np.isin(self._chunk_ids, np.fromiter(allowed, dtype=np.int64))
                )
            if candidate_indices.size == 0:
                return []
            candidate_vectors = self._vectors[candidate_indices]
            scores = candidate_vectors @ query_vector
            count = min(top_k, scores.shape[0])
            if count == scores.shape[0]:
                top_indices = np.argsort(scores)[::-1]
            else:
                top_indices = np.argpartition(scores, -count)[-count:]
                top_indices = top_indices[np.argsort(scores[top_indices])[::-1]]
            selected = candidate_indices[top_indices]
            chunk_ids = self._chunk_ids[selected].astype(int).tolist()
            top_scores = scores[top_indices].astype(float).tolist()
        return self.knowledge_base.results_for_vector_scores(
            chunk_ids, top_scores, query
        )
