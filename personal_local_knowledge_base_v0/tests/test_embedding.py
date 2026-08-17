import json
import tempfile
import threading
import unittest
from dataclasses import replace
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import numpy as np

from knowledge_search.chunking import ChunkingConfig, iter_chunk_blocks
from knowledge_search.database import KnowledgeBase
from knowledge_search.embedding import (
    EmbeddingSettings,
    RemoteQwen3EmbeddingModel,
    build_document_embedding_input,
    build_query_embedding_input,
)
from knowledge_search.extractors import extract_document
from knowledge_search.indexer import index_paths
from knowledge_search.models import DocumentBlock
from knowledge_search.vector_search import NumpyVectorIndex


class FakeEmbeddingBackend:
    def __init__(self, revision="fake-commit"):
        self.revision = revision
        self.settings = EmbeddingSettings(
            model_name="fake/qwen3",
            model_revision=revision,
            dimension=2,
            batch_size=2,
        )
        self.document_calls = []

    @property
    def model_revision(self):
        return self.revision

    def embed_documents(self, texts):
        self.document_calls.append(list(texts))
        vectors = []
        for text in texts:
            vectors.append([0.0, 1.0] if "unrelated" in text else [1.0, 0.0])
        return np.asarray(vectors, dtype=np.float32)

    def embed_query(self, query, *, code=False):
        return np.asarray([1.0, 0.0], dtype=np.float32)

    def token_count(self, text):
        return len(text)


def block(content, *, block_id="b0", hard_before=False, hard_after=False):
    return DocumentBlock(
        block_id=block_id,
        path="sample.md",
        block_type="paragraph",
        language=None,
        heading_path=("Topic",),
        symbol_path=(),
        content=content,
        start_line=1,
        end_line=1,
        page_number=None,
        hard_boundary_before=hard_before,
        hard_boundary_after=hard_after,
    )


class SemanticChunkingTests(unittest.TestCase):
    def test_similarity_uses_non_overlapping_cores_then_embeds_final_text(self):
        backend = FakeEmbeddingBackend()
        chunks = list(
            iter_chunk_blocks(
                [block("abcdefghij" * 3)],
                chunk_size=10,
                overlap=3,
                min_chunk_chars=2,
                max_chunk_chars=20,
                max_chunk_tokens=10_000,
                embedding_backend=backend,
            )
        )

        self.assertEqual(backend.document_calls[0], ["abcdefghij"] * 3)
        self.assertEqual(len(chunks), 2)
        self.assertEqual(chunks[0].content, "abcdefghij" * 2)
        self.assertEqual(chunks[0].content[-3:], chunks[1].content[:3])
        self.assertEqual(backend.document_calls[1], [
            chunk.embedding_content for chunk in chunks
        ])
        self.assertTrue(all(chunk.embedding_vector == (1.0, 0.0) for chunk in chunks))

    def test_hard_boundary_prevents_merge_and_overlap(self):
        backend = FakeEmbeddingBackend()
        left = block("abcdefghij", block_id="left", hard_after=True)
        right = block("klmnopqrst", block_id="right", hard_before=True)
        chunks = list(
            iter_chunk_blocks(
                [left, right],
                chunk_size=10,
                overlap=3,
                min_chunk_chars=2,
                max_chunk_chars=20,
                max_chunk_tokens=10_000,
                embedding_backend=backend,
            )
        )

        self.assertEqual([chunk.content for chunk in chunks], [left.content, right.content])

    def test_different_structure_prevents_merge(self):
        backend = FakeEmbeddingBackend()
        left = block("abcdefghij", block_id="left")
        right = replace(
            block("klmnopqrst", block_id="right"), heading_path=("Other",)
        )
        chunks = list(
            iter_chunk_blocks(
                [left, right],
                chunk_size=10,
                overlap=3,
                min_chunk_chars=2,
                max_chunk_chars=20,
                max_chunk_tokens=10_000,
                embedding_backend=backend,
            )
        )
        self.assertEqual(len(chunks), 2)


class EmbeddingStorageTests(unittest.TestCase):
    def test_vectors_are_cached_validated_and_retrieved_with_numpy(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            path = root / "note.md"
            path.write_text("# Topic\n\n" + "abcdefghij" * 3, encoding="utf-8")
            backend = FakeEmbeddingBackend()
            config = ChunkingConfig(
                core_chunk_chars=10,
                overlap_chars=3,
                min_chunk_chars=2,
                max_chunk_chars=20,
                max_chunk_tokens=10_000,
            )
            with KnowledgeBase(root / "knowledge.db") as knowledge_base:
                first = index_paths(
                    knowledge_base,
                    [path],
                    chunk_size=10,
                    overlap=3,
                    min_chunk_chars=2,
                    max_chunk_chars=20,
                    max_chunk_tokens=10_000,
                    embedding_backend=backend,
                )
                vector_count = knowledge_base.connection.execute(
                    "SELECT COUNT(*) FROM embeddings"
                ).fetchone()[0]
                model = knowledge_base.connection.execute(
                    "SELECT * FROM embedding_models"
                ).fetchone()
                second = index_paths(
                    knowledge_base,
                    [path],
                    chunk_size=10,
                    overlap=3,
                    min_chunk_chars=2,
                    max_chunk_chars=20,
                    max_chunk_tokens=10_000,
                    embedding_backend=backend,
                )
                knowledge_base.connection.execute(
                    "UPDATE embeddings SET vector = ? WHERE chunk_id = "
                    "(SELECT MIN(chunk_id) FROM embeddings)",
                    (b"invalid",),
                )
                repaired = knowledge_base.ensure_document_embeddings(
                    path,
                    backend,
                    chunker_fingerprint=config.fingerprint_for(backend),
                )
                results = NumpyVectorIndex(knowledge_base, backend).search(
                    "Topic", top_k=1
                )
                blobs = knowledge_base.connection.execute(
                    "SELECT vector, vector_dtype FROM embeddings"
                ).fetchall()

            self.assertEqual(first.embeddings_generated, 2)
            self.assertEqual(second.embeddings_generated, 0)
            self.assertEqual(repaired, 1)
            self.assertEqual(vector_count, 2)
            self.assertEqual(model["model_revision"], "fake-commit")
            self.assertEqual(model["dimension"], 2)
            self.assertEqual(results[0].filename, "note.md")
            self.assertAlmostEqual(results[0].score, 1.0)
            self.assertTrue(all(row["vector_dtype"] == "float32" for row in blobs))
            self.assertTrue(all(len(row["vector"]) == 8 for row in blobs))


class EmbeddingInputTests(unittest.TestCase):
    def test_document_and_query_templates_are_stable_natural_text(self):
        document = build_document_embedding_input(
            content="return path",
            path="database.py",
            block_type="function",
            language="Python",
            symbol_path=("KnowledgeBase", "replace_document"),
            start_line=175,
            end_line=230,
        )
        self.assertIn("结构：KnowledgeBase > replace_document", document)
        self.assertIn("原文内容：\nreturn path", document)
        self.assertNotIn("jieba", document)
        self.assertEqual(
            build_query_embedding_input("如何替换文档？"),
            "Instruct: 根据用户问题，从知识库中检索能够直接回答问题的相关文档片段\n"
            "Query: 如何替换文档？",
        )


class _EmbeddingHandler(BaseHTTPRequestHandler):
    embedding_inputs = []

    def log_message(self, format, *args):
        return

    def _send(self, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/v1/models":
            self._send(
                {
                    "data": [
                        {
                            "id": "Qwen/Qwen3-Embedding-0.6B",
                            "model_revision": "abc1234",
                        }
                    ]
                }
            )
            return
        self.send_error(404)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0"))
        payload = json.loads(self.rfile.read(length))
        if self.path == "/v1/embeddings":
            inputs = payload["input"]
            self.embedding_inputs.extend(inputs)
            self._send(
                {
                    "data": [
                        {"index": index, "embedding": [3.0, 4.0]}
                        for index, _ in enumerate(inputs)
                    ]
                }
            )
            return
        if self.path in {"/tokenize", "/v1/tokenize"}:
            self._send({"count": len(payload["prompt"])})
            return
        self.send_error(404)


class RemoteEmbeddingTests(unittest.TestCase):
    def test_openai_compatible_remote_service_is_batched_and_normalized(self):
        _EmbeddingHandler.embedding_inputs = []
        server = ThreadingHTTPServer(("127.0.0.1", 0), _EmbeddingHandler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            backend = RemoteQwen3EmbeddingModel(
                EmbeddingSettings(dimension=2, batch_size=1),
                base_url=f"http://127.0.0.1:{server.server_port}",
                timeout=5,
            )
            self.assertEqual(backend.model_revision, "abc1234")
            vectors = backend.embed_documents(["one", "two"])
            query = backend.embed_query("如何替换文档？")
            self.assertEqual(vectors.shape, (2, 2))
            self.assertTrue(np.allclose(vectors, [[0.6, 0.8], [0.6, 0.8]]))
            self.assertTrue(np.allclose(query, [0.6, 0.8]))
            self.assertTrue(
                _EmbeddingHandler.embedding_inputs[-1].startswith("Instruct: ")
            )
            self.assertTrue(backend.fits_token_limit("abc", 10))
            self.assertFalse(backend.fits_token_limit("abcdefghij", 5))
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)

    def test_auto_detects_simple_embed_protocol(self):
        class SimpleHandler(_EmbeddingHandler):
            def do_GET(self):
                if self.path == "/openapi.json":
                    self._send({"paths": {"/embed": {"post": {}}}})
                    return
                self.send_error(404)

            def do_POST(self):
                length = int(self.headers.get("Content-Length", "0"))
                payload = json.loads(self.rfile.read(length))
                if self.path == "/embed":
                    self._send(
                        {
                            "embeddings": [
                                [3.0, 4.0] for _ in payload["texts"]
                            ]
                        }
                    )
                    return
                self.send_error(404)

        server = ThreadingHTTPServer(("127.0.0.1", 0), SimpleHandler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            backend = RemoteQwen3EmbeddingModel(
                EmbeddingSettings(
                    model_revision="abc1234", dimension=2, batch_size=2
                ),
                base_url=f"http://127.0.0.1:{server.server_port}",
                timeout=5,
            )
            vectors = backend.embed_documents(["one", "two"])
            self.assertTrue(np.allclose(vectors, [[0.6, 0.8], [0.6, 0.8]]))
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)


if __name__ == "__main__":
    unittest.main()
