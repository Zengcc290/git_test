import contextlib
import io
import json
import logging
import os
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import patch

from knowledge_search.cli import main
from knowledge_search.database import KnowledgeBase
from knowledge_search.indexer import index_paths
from knowledge_search.models import Chunk, ExtractedDocument
from knowledge_search.rag.answer import CitationValidationError, RagAnswerer, RagConfig
from knowledge_search.rag.llm_client import (
    LLMClient,
    LLMClientError,
    LLMResponse,
    TokenUsage,
)
from knowledge_search.rag.prompt import REFUSAL_ANSWER, SYSTEM_PROMPT, build_messages
from knowledge_search.rag.retriever import ChunkRetriever, KeywordRetriever


def _document(path: Path, content: str, sha256: str) -> ExtractedDocument:
    path.write_text(content, encoding="utf-8")
    return ExtractedDocument(
        path=path.resolve(),
        file_type="md",
        text=content,
        sha256=sha256,
        size=len(content.encode("utf-8")),
        modified_ns=1,
    )


def _reset_logging_handlers() -> None:
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
        handler.close()


class FakeClient:
    def __init__(self, content: str = "FTS5 是 SQLite 的全文搜索扩展。[1]") -> None:
        self.content = content
        self.messages = None
        self.temperature = None

    def complete(self, messages, *, temperature=0.0):
        self.messages = messages
        self.temperature = temperature
        return LLMResponse(
            content=self.content,
            usage=TokenUsage(
                prompt_tokens=120,
                completion_tokens=18,
                total_tokens=138,
            ),
        )


class RagTests(unittest.TestCase):
    def test_client_automatically_loads_dotenv(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / ".env").write_text(
                "LLM_API_KEY=dotenv-secret\n"
                "LLM_BASE_URL=https://dotenv.example/v1\n"
                "LLM_MODEL=dotenv-model\n",
                encoding="utf-8",
            )
            previous_cwd = Path.cwd()
            try:
                os.chdir(root)
                with patch.dict(
                    "os.environ",
                    {
                        "LLM_API_KEY": "",
                        "LLM_BASE_URL": "",
                        "LLM_MODEL": "",
                    },
                    clear=False,
                ):
                    for name in ("LLM_API_KEY", "LLM_BASE_URL", "LLM_MODEL"):
                        os.environ.pop(name, None)
                    client = LLMClient.from_env()
            finally:
                os.chdir(previous_cwd)

            self.assertEqual(client.model, "dotenv-model")
            self.assertEqual(
                client.endpoint,
                "https://dotenv.example/v1/chat/completions",
            )

    def test_environment_variables_override_dotenv(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / ".env").write_text(
                "LLM_API_KEY=file-secret\n"
                "LLM_BASE_URL=https://file.example/v1\n"
                "LLM_MODEL=file-model\n",
                encoding="utf-8",
            )
            previous_cwd = Path.cwd()
            try:
                os.chdir(root)
                with patch.dict(
                    "os.environ",
                    {
                        "LLM_API_KEY": "environment-secret",
                        "LLM_BASE_URL": "https://environment.example/v1",
                        "LLM_MODEL": "environment-model",
                    },
                    clear=False,
                ):
                    client = LLMClient.from_env()
            finally:
                os.chdir(previous_cwd)

            self.assertEqual(client.model, "environment-model")
            self.assertEqual(
                client.endpoint,
                "https://environment.example/v1/chat/completions",
            )

    def test_natural_question_retrieves_relevant_chunk(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            with KnowledgeBase(root / "knowledge.db") as knowledge_base:
                knowledge_base.replace_document(
                    _document(
                        root / "sqlite.md",
                        "SQLite FTS5 是 SQLite 内置的全文搜索扩展。",
                        "hash-sqlite",
                    ),
                    [Chunk(0, "SQLite FTS5 是 SQLite 内置的全文搜索扩展。")],
                )
                retriever = KeywordRetriever(knowledge_base, top_k=5)

                retrieval = retriever.retrieve("SQLite FTS5 是什么？")

            self.assertEqual(retrieval.chunks[0].filename, "sqlite.md")
            self.assertEqual(retrieval.chunks[0].chunk_index, 0)
            self.assertIn("[1] 文件：sqlite.md；分段：0", retrieval.context)

    def test_question_chunk_matching_does_not_use_jieba(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            with KnowledgeBase(root / "knowledge.db") as knowledge_base:
                content = "猫在树下乘凉"
                knowledge_base.replace_document(
                    _document(root / "cat.txt", content, "cat-hash"),
                    [Chunk(0, content)],
                )

                with patch(
                    "knowledge_search.database.tokenize_for_search",
                    side_effect=AssertionError("问答召回不应使用 jieba"),
                ):
                    retrieval = ChunkRetriever(knowledge_base, top_k=1).retrieve(
                        "猫在树下干什么"
                    )

            self.assertEqual(retrieval.chunks[0].filename, "cat.txt")
            self.assertEqual(retrieval.chunks[0].content, content)

    def test_long_natural_question_ranks_shared_phrases_in_large_noisy_corpus(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            with KnowledgeBase(root / "knowledge.db") as knowledge_base:
                for index in range(15):
                    content = f"上海队赛季新闻 {index}，比赛中有球员伤病。"
                    knowledge_base.replace_document(
                        _document(root / f"noise-{index}.md", content, f"noise-{index}"),
                        [Chunk(0, content)],
                    )
                target = (
                    "邓华德总结上海队赛季时说医生。32场比赛中，"
                    "人员齐整12场赢8场，伤病20场赢4场。"
                )
                knowledge_base.replace_document(
                    _document(root / "target.md", target, "target"),
                    [Chunk(0, target)],
                )

                retrieval = KeywordRetriever(knowledge_base, top_k=3).retrieve(
                    "邓华德用哪个词总结上海队那个赛季？按他的统计，"
                    "32场中人员齐整和有伤病的比赛各多少场、各赢多少场？"
                )

            self.assertEqual(retrieval.chunks[0].filename, "target.md")

    def test_model_refusal_is_recorded_as_refused(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            with KnowledgeBase(root / "knowledge.db") as knowledge_base:
                knowledge_base.replace_document(
                    _document(root / "note.md", "项目资料存在但没有答案。", "hash"),
                    [Chunk(0, "项目资料存在但没有答案。")],
                )
                result = RagAnswerer(
                    KeywordRetriever(knowledge_base),
                    client_factory=lambda: FakeClient(REFUSAL_ANSWER),
                ).answer("项目资料答案是什么？")

            self.assertTrue(result.refused)

    def test_model_specific_refusal_is_recorded_as_refused(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            with KnowledgeBase(root / "knowledge.db") as knowledge_base:
                knowledge_base.replace_document(
                    _document(root / "note.md", "项目资料存在。", "hash-specific"),
                    [Chunk(0, "项目资料存在。")],
                )
                result = RagAnswerer(
                    KeywordRetriever(knowledge_base),
                    client_factory=lambda: FakeClient(
                        "根据当前知识库资料，无法回答项目预算；资料未提供。"
                    ),
                ).answer("项目预算是什么？")

            self.assertTrue(result.refused)

    def test_context_never_exceeds_limit_with_multiple_documents(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            with KnowledgeBase(root / "knowledge.db") as knowledge_base:
                for index in range(3):
                    content = f"SQLite 文档 {index}。" + ("全文检索内容" * 80)
                    knowledge_base.replace_document(
                        _document(root / f"doc-{index}.md", content, f"hash-{index}"),
                        [Chunk(0, content)],
                    )

                retrieval = KeywordRetriever(
                    knowledge_base,
                    top_k=3,
                    max_context_chars=180,
                ).retrieve("SQLite")

            self.assertLessEqual(retrieval.context_chars, 180)
            self.assertTrue(retrieval.truncated)
            self.assertGreaterEqual(len(retrieval.chunks), 1)

    def test_retrieval_includes_adjacent_chunk_under_same_citation(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            with KnowledgeBase(root / "knowledge.db") as knowledge_base:
                document = _document(
                    root / "split.md",
                    "比分在前一段，原因在后一段。",
                    "split-hash",
                )
                knowledge_base.replace_document(
                    document,
                    [
                        Chunk(0, "比赛持续7分42秒，比分是4比40。"),
                        Chunk(1, "连续犯规导致比赛提前结束。"),
                    ],
                )
                retrieval = KeywordRetriever(knowledge_base, top_k=1).retrieve(
                    "连续犯规为何导致比赛提前结束？"
                )

            self.assertEqual(retrieval.chunks[0].chunk_indexes, (0, 1))
            self.assertIn("比赛持续7分42秒", retrieval.context)
            self.assertIn("分段：0、1", retrieval.context)

    def test_answer_uses_context_and_reports_sources_usage_and_time(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            with KnowledgeBase(root / "knowledge.db") as knowledge_base:
                knowledge_base.replace_document(
                    _document(root / "sqlite.md", "FTS5 提供全文搜索。", "hash"),
                    [Chunk(7, "FTS5 提供全文搜索。")],
                )
                client = FakeClient()
                result = RagAnswerer(
                    KeywordRetriever(knowledge_base),
                    client_factory=lambda: client,
                ).answer("FTS5 是什么？")

            self.assertIn("[1]", result.answer)
            self.assertEqual(result.sources[0].filename, "sqlite.md")
            self.assertEqual(result.sources[0].chunk_index, 7)
            self.assertEqual(result.usage.total_tokens, 138)
            self.assertGreaterEqual(result.elapsed_ms, 0)
            self.assertIn("只能使用", client.messages[0]["content"])
            self.assertIn("FTS5 提供全文搜索", client.messages[1]["content"])

    def test_valid_model_citation_is_accepted(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            with KnowledgeBase(root / "knowledge.db") as knowledge_base:
                knowledge_base.replace_document(
                    _document(root / "note.md", "项目代号是晨星。", "valid-citation"),
                    [Chunk(0, "项目代号是晨星。")],
                )
                result = RagAnswerer(
                    KeywordRetriever(knowledge_base),
                    client_factory=lambda: FakeClient("项目代号是晨星。[1]"),
                ).answer("项目代号是什么？")

            self.assertFalse(result.refused)
            self.assertEqual(result.answer, "项目代号是晨星。[1]")

    def test_model_answer_without_citation_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            with KnowledgeBase(root / "knowledge.db") as knowledge_base:
                knowledge_base.replace_document(
                    _document(root / "note.md", "项目代号是晨星。", "no-citation"),
                    [Chunk(0, "项目代号是晨星。")],
                )
                with self.assertRaisesRegex(CitationValidationError, "没有提供"):
                    RagAnswerer(
                        KeywordRetriever(knowledge_base),
                        client_factory=lambda: FakeClient("This answer has no citation."),
                    ).answer("项目代号是什么？")

    def test_model_answer_with_only_invalid_citation_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            with KnowledgeBase(root / "knowledge.db") as knowledge_base:
                knowledge_base.replace_document(
                    _document(root / "note.md", "项目代号是晨星。", "invalid-citation"),
                    [Chunk(0, "项目代号是晨星。")],
                )
                with self.assertRaisesRegex(CitationValidationError, r"\[99\]"):
                    RagAnswerer(
                        KeywordRetriever(knowledge_base),
                        client_factory=lambda: FakeClient("项目代号是晨星。[99]"),
                    ).answer("项目代号是什么？")

    def test_model_answer_with_valid_and_invalid_citations_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            with KnowledgeBase(root / "knowledge.db") as knowledge_base:
                knowledge_base.replace_document(
                    _document(root / "note.md", "项目代号是晨星。", "mixed-citations"),
                    [Chunk(0, "项目代号是晨星。")],
                )
                with self.assertRaisesRegex(CitationValidationError, r"\[99\]"):
                    RagAnswerer(
                        KeywordRetriever(knowledge_base),
                        client_factory=lambda: FakeClient(
                            "项目代号是晨星。[1] 负责人是未知。[99]"
                        ),
                    ).answer("项目代号和负责人是什么？")

    def test_model_refusal_without_citation_is_accepted(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            with KnowledgeBase(root / "knowledge.db") as knowledge_base:
                knowledge_base.replace_document(
                    _document(root / "note.md", "项目资料没有预算。", "refusal-no-citation"),
                    [Chunk(0, "项目资料没有预算。")],
                )
                result = RagAnswerer(
                    KeywordRetriever(knowledge_base),
                    client_factory=lambda: FakeClient(REFUSAL_ANSWER),
                ).answer("项目预算是多少？")

            self.assertTrue(result.refused)
            self.assertEqual(result.answer, REFUSAL_ANSWER)

    def test_model_refusal_with_invalid_citation_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            with KnowledgeBase(root / "knowledge.db") as knowledge_base:
                knowledge_base.replace_document(
                    _document(root / "note.md", "项目资料没有预算。", "refusal-invalid"),
                    [Chunk(0, "项目资料没有预算。")],
                )
                with self.assertRaisesRegex(CitationValidationError, r"\[99\]"):
                    RagAnswerer(
                        KeywordRetriever(knowledge_base),
                        client_factory=lambda: FakeClient(f"{REFUSAL_ANSWER}[99]"),
                    ).answer("项目预算是多少？")

    def test_no_results_refuses_without_creating_client(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            created = False

            def create_client():
                nonlocal created
                created = True
                return FakeClient()

            with KnowledgeBase(root / "knowledge.db") as knowledge_base:
                result = RagAnswerer(
                    KeywordRetriever(knowledge_base),
                    client_factory=create_client,
                ).answer("火星天气如何？")

            self.assertTrue(result.refused)
            self.assertEqual(result.answer, REFUSAL_ANSWER)
            self.assertFalse(created)

    def test_prompt_treats_context_as_untrusted_and_requires_refusal(self):
        messages = build_messages("问题", "[1] 文件：note.md；分段：0\n资料")

        self.assertIn("不可信数据", SYSTEM_PROMPT)
        self.assertIn(REFUSAL_ANSWER, SYSTEM_PROMPT)
        self.assertEqual(messages[0]["role"], "system")
        self.assertEqual(messages[1]["role"], "user")

    def test_config_rejects_secret_and_unknown_fields(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "rag.json"
            path.write_text(
                json.dumps({"top_k": 5, "api_key": "must-not-be-here"}),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "未知字段"):
                RagConfig.from_file(path)

    def test_http_error_never_exposes_api_key(self):
        secret = "super-secret-api-key"
        client = LLMClient(
            api_key=secret,
            base_url="https://llm.example/v1",
            model="test-model",
        )
        error_body = json.dumps(
            {"error": {"message": f"invalid credential {secret}"}}
        ).encode("utf-8")
        http_error = urllib.error.HTTPError(
            client.endpoint,
            401,
            "Unauthorized",
            {},
            io.BytesIO(error_body),
        )

        with patch("urllib.request.urlopen", side_effect=http_error):
            with self.assertRaises(LLMClientError) as raised:
                client.complete([{"role": "user", "content": "hello"}])

        self.assertNotIn(secret, str(raised.exception))
        self.assertIn("[REDACTED]", str(raised.exception))

    def test_cli_failure_log_never_contains_api_key(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "sqlite.md"
            source.write_text("SQLite FTS5 提供全文搜索。", encoding="utf-8")
            with KnowledgeBase(root / "knowledge.db") as knowledge_base:
                index_paths(knowledge_base, [source])

            secret = "cli-secret-api-key"
            error_body = json.dumps(
                {"error": {"message": f"invalid credential {secret}"}}
            ).encode("utf-8")
            http_error = urllib.error.HTTPError(
                "https://llm.example/v1/chat/completions",
                401,
                "Unauthorized",
                {},
                io.BytesIO(error_body),
            )
            try:
                with patch.dict(
                    "os.environ",
                    {
                        "LLM_API_KEY": secret,
                        "LLM_BASE_URL": "https://llm.example/v1",
                        "LLM_MODEL": "test-model",
                    },
                    clear=False,
                ):
                    with patch("urllib.request.urlopen", side_effect=http_error):
                        status = main(
                            [
                                "ask",
                                "FTS5 是什么？",
                                "--db",
                                str(root / "knowledge.db"),
                                "--log-file",
                                str(root / "app.log"),
                            ]
                        )
            finally:
                _reset_logging_handlers()

            log_text = (root / "app.log").read_text(encoding="utf-8")
            self.assertEqual(status, 1)
            self.assertNotIn(secret, log_text)
            self.assertIn("[REDACTED]", log_text)

    def test_cli_invalid_model_citation_returns_nonzero_and_logs_only_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            secret = "citation-validation-secret"
            source = root / f"{secret}.md"
            source.write_text("项目代号是晨星。", encoding="utf-8")
            with KnowledgeBase(root / "knowledge.db") as knowledge_base:
                index_paths(knowledge_base, [source])

            try:
                with patch.dict(
                    "os.environ",
                    {"LLM_API_KEY": secret},
                    clear=False,
                ):
                    with patch(
                        "knowledge_search.cli.LLMClient.from_env",
                        return_value=FakeClient(
                            f"项目代号是晨星，但没有引用。{secret}"
                        ),
                    ):
                        status = main(
                            [
                                "ask",
                                "项目代号是什么？",
                                "--db",
                                str(root / "knowledge.db"),
                                "--log-file",
                                str(root / "app.log"),
                            ]
                        )
            finally:
                _reset_logging_handlers()

            log_text = (root / "app.log").read_text(encoding="utf-8")
            self.assertEqual(status, 1)
            self.assertIn('"event": "rag_error"', log_text)
            self.assertIn('"error_type": "CitationValidationError"', log_text)
            self.assertIn('"total_tokens": 138', log_text)
            self.assertNotIn('"event": "rag_answer"', log_text)
            self.assertNotIn(secret, log_text)

    def test_no_result_log_redacts_api_key_loaded_from_dotenv(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            secret = "no-result-dotenv-secret"
            (root / ".env").write_text(
                f"LLM_API_KEY={secret}\n"
                "LLM_BASE_URL=https://dotenv.example/v1\n"
                "LLM_MODEL=dotenv-model\n",
                encoding="utf-8",
            )
            previous_cwd = Path.cwd()
            try:
                os.chdir(root)
                with patch.dict("os.environ", {}, clear=False):
                    for name in ("LLM_API_KEY", "LLM_BASE_URL", "LLM_MODEL"):
                        os.environ.pop(name, None)
                    status = main(
                        [
                            "ask",
                            f"没有资料的问题 {secret}",
                            "--db",
                            str(root / "knowledge.db"),
                            "--log-file",
                            str(root / "app.log"),
                        ]
                    )
            finally:
                os.chdir(previous_cwd)
                _reset_logging_handlers()

            log_text = (root / "app.log").read_text(encoding="utf-8")
            self.assertEqual(status, 0)
            self.assertNotIn(secret, log_text)
            self.assertIn("[REDACTED]", log_text)

    def test_invalid_base_url_has_friendly_error(self):
        with self.assertRaisesRegex(LLMClientError, "HTTP\\(S\\)"):
            LLMClient(
                api_key="secret",
                base_url="not-a-url",
                model="test-model",
            )

    def test_cli_ask_outputs_refusal_without_llm_configuration(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            output = io.StringIO()
            try:
                with contextlib.redirect_stdout(output):
                    status = main(
                        [
                            "ask",
                            "不存在的资料是什么？",
                            "--db",
                            str(root / "knowledge.db"),
                            "--log-file",
                            str(root / "app.log"),
                        ]
                    )
            finally:
                _reset_logging_handlers()

            self.assertEqual(status, 0)
            self.assertIn(REFUSAL_ANSWER, output.getvalue())
            self.assertIn("耗时", output.getvalue())

    def test_cli_ask_outputs_answer_sources_and_token_usage(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "sqlite.md"
            source.write_text("SQLite FTS5 提供本地全文搜索。", encoding="utf-8")
            with KnowledgeBase(root / "knowledge.db") as knowledge_base:
                index_paths(knowledge_base, [source])

            output = io.StringIO()
            client = FakeClient()
            try:
                with patch(
                    "knowledge_search.cli.LLMClient.from_env",
                    return_value=client,
                ):
                    with contextlib.redirect_stdout(output):
                        status = main(
                            [
                                "ask",
                                "SQLite FTS5 是什么？",
                                "--db",
                                str(root / "knowledge.db"),
                                "--log-file",
                                str(root / "app.log"),
                                "--top-k",
                                "3",
                            ]
                        )
            finally:
                _reset_logging_handlers()

            text = output.getvalue()
            self.assertEqual(status, 0)
            self.assertIn("FTS5 是 SQLite", text)
            self.assertIn("sqlite.md，分段 0", text)
            self.assertIn("token 138", text)
            log_text = (root / "app.log").read_text(encoding="utf-8")
            self.assertIn('"event": "rag_answer"', log_text)
            self.assertIn('"total_tokens": 138', log_text)


if __name__ == "__main__":
    unittest.main()
