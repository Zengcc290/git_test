import json
import http.client
import tempfile
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest.mock import patch

from knowledge_search.database import KnowledgeBase
from knowledge_search.indexer import index_paths
from knowledge_search.rag.answer import RagConfig
from knowledge_search.rag.llm_client import LLMResponse, TokenUsage
from knowledge_search.web.app import (
    KnowledgeWebApp,
    create_server,
    _extract_quoted,
    _parse_multipart,
)


def _indexed_temp_db(text: str = "SQLite FTS5 提供本地全文搜索。"):
    temp_dir = tempfile.TemporaryDirectory()
    root = Path(temp_dir.name)
    source = root / "sqlite.md"
    source.write_text(text, encoding="utf-8")
    db_path = root / "knowledge.db"
    with KnowledgeBase(db_path) as knowledge_base:
        index_paths(knowledge_base, [source])
    return temp_dir, root, db_path


class FakeClient:
    def complete(self, messages, *, temperature=0.0):
        return LLMResponse(
            content="FTS5 是 SQLite 的全文搜索扩展。[1]",
            usage=TokenUsage(prompt_tokens=10, completion_tokens=8, total_tokens=18),
        )


class KnowledgeWebAppTests(unittest.TestCase):
    def test_stats_and_documents_report_indexed_state(self):
        temp_dir, root, db_path = _indexed_temp_db()
        try:
            app = KnowledgeWebApp(
                db_path=db_path,
                upload_dir=root / "uploads",
                client_factory=FakeClient,
            )
            stats = app.stats()
            self.assertEqual(stats["documents"], 1)
            self.assertGreaterEqual(stats["chunks"], 1)

            documents = app.documents()
            self.assertEqual(len(documents), 1)
            self.assertEqual(documents[0]["filename"], "sqlite.md")
            self.assertEqual(documents[0]["file_type"], "md")
        finally:
            temp_dir.cleanup()

    def test_search_returns_highlighted_content(self):
        temp_dir, root, db_path = _indexed_temp_db()
        try:
            app = KnowledgeWebApp(db_path=db_path, upload_dir=root / "uploads")
            results = app.search("FTS5")
            self.assertTrue(results)
            self.assertEqual(results[0]["filename"], "sqlite.md")
            self.assertIn("<mark>", results[0]["highlighted"])
        finally:
            temp_dir.cleanup()

    def test_ask_uses_fake_client_and_returns_citation_sources(self):
        temp_dir, root, db_path = _indexed_temp_db()
        try:
            app = KnowledgeWebApp(
                db_path=db_path,
                upload_dir=root / "uploads",
                client_factory=FakeClient,
            )
            result = app.ask("SQLite FTS5 是什么？", RagConfig())
            self.assertNotIn("error", result)
            self.assertIn("[1]", result["answer"])
            self.assertEqual(result["usage"]["total_tokens"], 18)
            self.assertEqual(result["sources"][0]["filename"], "sqlite.md")
        finally:
            temp_dir.cleanup()

    def test_ask_returns_structured_error_when_client_fails(self):
        temp_dir, root, db_path = _indexed_temp_db()

        def failing_client():
            from knowledge_search.rag.llm_client import LLMClientError

            raise LLMClientError("未配置 LLM_API_KEY。")

        try:
            app = KnowledgeWebApp(
                db_path=db_path,
                upload_dir=root / "uploads",
                client_factory=failing_client,
            )
            result = app.ask("SQLite FTS5 是什么？", RagConfig())
            self.assertIn("error", result)
            self.assertIn("LLM_API_KEY", result["error"])
        finally:
            temp_dir.cleanup()

    def test_save_upload_persists_and_deduplicates_names(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            app = KnowledgeWebApp(db_path=root / "kb.db", upload_dir=root / "uploads")
            first_path, first_name = app.save_upload("note.md", "内容".encode("utf-8"))
            second_path, second_name = app.save_upload("note.md", "另一个".encode("utf-8"))
            self.assertEqual(first_name, "note.md")
            self.assertEqual(second_name, "note-1.md")
            self.assertNotEqual(first_path, second_path)
            self.assertTrue(Path(first_path).is_file())
            self.assertTrue(Path(second_path).is_file())

    def test_save_upload_rejects_unsupported_suffix(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            app = KnowledgeWebApp(db_path=root / "kb.db", upload_dir=root / "uploads")
            with self.assertRaisesRegex(ValueError, "不支持"):
                app.save_upload("evil.exe", b"data")

    def test_save_upload_sanitizes_traversal_name(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            app = KnowledgeWebApp(db_path=root / "kb.db", upload_dir=root / "uploads")
            _, name = app.save_upload("../secret.md", "内容".encode("utf-8"))
            self.assertEqual(name, "secret.md")

    def test_remove_document(self):
        temp_dir, root, db_path = _indexed_temp_db()
        try:
            app = KnowledgeWebApp(db_path=db_path, upload_dir=root / "uploads")
            document_id = app.documents()[0]["id"]
            result = app.remove(document_id)
            self.assertTrue(result["removed"])
            self.assertEqual(app.documents(), [])
        finally:
            temp_dir.cleanup()


class MultipartParsingTests(unittest.TestCase):
    def test_parse_multipart_extracts_filename_and_data(self):
        boundary = "----boundary"
        body = (
            f"--{boundary}\r\n"
            'Content-Disposition: form-data; name="file"; filename="note.md"\r\n'
            "Content-Type: text/markdown\r\n\r\n"
            "hello world\r\n"
            f"--{boundary}--\r\n"
        ).encode("utf-8")
        filename, data = _parse_multipart(
            body, f'multipart/form-data; boundary="{boundary}"'
        )
        self.assertEqual(filename, "note.md")
        self.assertEqual(data, b"hello world")

    def test_parse_multipart_requires_file(self):
        boundary = "----boundary"
        body = (
            f"--{boundary}\r\n"
            'Content-Disposition: form-data; name="note"\r\n\r\n'
            "value\r\n"
            f"--{boundary}--\r\n"
        ).encode("utf-8")
        with self.assertRaisesRegex(ValueError, "没有文件"):
            _parse_multipart(body, f'multipart/form-data; boundary="{boundary}"')

    def test_extract_quoted_handles_quoted_and_bare_values(self):
        self.assertEqual(_extract_quoted('form-data; filename="a b.md"', "filename"), "a b.md")
        self.assertEqual(_extract_quoted("form-data; filename=plain.md", "filename"), "plain.md")
        self.assertEqual(_extract_quoted("form-data", "filename"), "")


class HttpApiTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir, self.root, self.db_path = _indexed_temp_db()
        self.app = KnowledgeWebApp(
            db_path=self.db_path,
            upload_dir=self.root / "uploads",
            client_factory=FakeClient,
        )
        self.server = create_server(self.app, lambda: RagConfig(), port=0)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.host, self.port = self.server.server_address

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)
        self.temp_dir.cleanup()

    def request(self, method, path, body=None, headers=None):
        connection = http.client.HTTPConnection(self.host, self.port, timeout=5)
        try:
            connection.request(method, path, body=body, headers=headers or {})
            response = connection.getresponse()
            raw = response.read()
            try:
                payload = json.loads(raw.decode("utf-8")) if raw else None
            except json.JSONDecodeError:
                payload = raw.decode("utf-8", errors="replace")
            return response.status, payload
        finally:
            connection.close()

    def test_static_stats_search_and_ask_routes(self):
        status, html = self.request("GET", "/")
        self.assertEqual(status, 200)
        self.assertIn("个人知识库", html)

        status, stats = self.request("GET", "/api/stats")
        self.assertEqual(status, 200)
        self.assertEqual(stats["documents"], 1)

        status, search = self.request("GET", "/api/search?q=FTS5")
        self.assertEqual(status, 200)
        self.assertIn("<mark>", search["results"][0]["highlighted"])

        status, answer = self.request(
            "POST",
            "/api/ask",
            json.dumps({"question": "SQLite FTS5 是什么？"}).encode(),
            {"Content-Type": "application/json"},
        )
        self.assertEqual(status, 200)
        self.assertEqual(answer["sources"][0]["filename"], "sqlite.md")

    def test_multipart_upload_and_bad_json_are_rejected_cleanly(self):
        boundary = "----v3-boundary"
        body = (
            f"--{boundary}\r\n"
            'Content-Disposition: form-data; name="file"; filename="../new.md"\r\n'
            "Content-Type: text/markdown\r\n\r\n"
            "new FTS5 content\r\n"
            f"--{boundary}--\r\n"
        ).encode()
        status, uploaded = self.request(
            "POST",
            "/api/upload",
            body,
            {"Content-Type": f'multipart/form-data; boundary="{boundary}"'},
        )
        self.assertEqual(status, 200)
        self.assertEqual(uploaded["filename"], "new.md")
        self.assertTrue(Path(uploaded["path"]).is_relative_to(self.root / "uploads"))

        status, error = self.request(
            "POST", "/api/search", b"[]", {"Content-Type": "application/json"}
        )
        self.assertEqual(status, 400)
        self.assertIn("对象", error["error"])

        status, error = self.request("GET", "/api/search?q=FTS5&limit=0")
        self.assertEqual(status, 400)
        self.assertIn("搜索条数", error["error"])

    def test_concurrent_search_requests_are_independent(self):
        def search_once(_):
            status, payload = self.request("GET", "/api/search?q=FTS5")
            return status, len(payload["results"])

        with ThreadPoolExecutor(max_workers=8) as executor:
            results = list(executor.map(search_once, range(16)))
        self.assertEqual(results, [(200, 1)] * 16)

    def test_error_response_redacts_api_key(self):
        secret = "web-secret-key"

        def failing_client():
            from knowledge_search.rag.llm_client import LLMClientError

            raise LLMClientError(f"remote rejected {secret}")

        self.app.client_factory = failing_client
        with patch.dict("os.environ", {"LLM_API_KEY": secret}, clear=False):
            status, payload = self.request(
                "POST",
                "/api/ask",
                json.dumps({"question": "SQLite FTS5 是什么？"}).encode(),
                {"Content-Type": "application/json"},
            )
        self.assertEqual(status, 200)
        self.assertNotIn(secret, payload["error"])
        self.assertIn("[REDACTED]", payload["error"])


if __name__ == "__main__":
    unittest.main()
