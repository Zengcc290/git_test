"""In-memory NumPy retrieval over float32 vectors stored in SQLite."""

from __future__ import annotations

from pathlib import Path
from threading import RLock

import numpy as np

from .database import KnowledgeBase
from .embedding import EmbeddingBackend, validate_vectors
from .models import SearchResult


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
        top_k: int = 5,
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
