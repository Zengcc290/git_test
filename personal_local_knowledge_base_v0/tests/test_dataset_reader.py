import gzip
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from knowledge_search.dataset_reader import (
    DATASET_RECORD_KEYS,
    DatasetReaderError,
    available_adapters,
    infer_local_format,
    infer_dataset_name,
    iter_dataset_blocks,
    iter_dataset,
    iter_huggingface,
    iter_local_dataset,
    iter_local_dureader,
    normalize,
    register_adapter,
)


HAS_DATASETS = (
    importlib.util.find_spec("datasets") is not None
    and importlib.util.find_spec("pyarrow") is not None
)


class DatasetNormalizationTests(unittest.TestCase):
    def assert_record_shape(self, record):
        self.assertEqual(tuple(record), DATASET_RECORD_KEYS)
        self.assertIsInstance(record["id"], str)
        self.assertIsInstance(record["answers"], list)
        self.assertIsInstance(record["meta"], dict)

    def test_normalizes_dureader_and_collects_negatives(self):
        record = normalize(
            "dureader",
            {
                "anchor": "问题",
                "positive": "正确正文",
                "negative_1": "负例一",
                "negative_2": None,
                "negative_15": "负例十五",
            },
            7,
        )

        self.assert_record_shape(record)
        self.assertEqual(record["id"], "7")
        self.assertEqual(record["query"], "问题")
        self.assertEqual(record["text"], "正确正文")
        self.assertEqual(record["meta"]["negatives"], ["负例一", "负例十五"])

    def test_normalizes_code_datasets(self):
        github = normalize(
            "github_code",
            {
                "repo_name": "org/repo",
                "path": "src/main.py",
                "code": "def main(): pass",
                "language": "Python",
                "license": "MIT",
            },
            0,
        )
        codesearchnet = normalize(
            "codesearchnet",
            {
                "url": "https://example.test/function",
                "func_name": "search",
                "whole_func_string": "def search(query): pass",
                "docstring": "Search documents.",
                "repository_name": "org/search",
                "func_path_in_repository": "search.py",
            },
            1,
        )

        self.assert_record_shape(github)
        self.assertEqual(github["id"], "org/repo:src/main.py")
        self.assertEqual(github["meta"]["language"], "Python")
        self.assert_record_shape(codesearchnet)
        self.assertEqual(codesearchnet["title"], "search")
        self.assertEqual(codesearchnet["query"], "Search documents.")

    def test_normalizes_qa_datasets_and_removes_nq_html_tokens(self):
        narrative = normalize(
            "narrativeqa",
            {
                "document": {
                    "id": "doc-1",
                    "summary": {"title": "Story"},
                    "text": "Long story text",
                },
                "question": {"text": "What happened?"},
                "answers": [{"text": "An event."}, {"text": "A result."}],
            },
            0,
        )
        natural = normalize(
            "natural_questions",
            {
                "id": 42,
                "document": {
                    "title": "Article",
                    "tokens": {
                        "token": ["<P>", "searchable", "text", "</P>"],
                        "is_html": [True, False, False, True],
                    },
                },
                "question": {"text": "What is searchable?"},
                "annotations": [{"yes_no_answer": "NONE"}],
            },
            0,
        )

        self.assertEqual(narrative["answers"], ["An event.", "A result."])
        self.assertEqual(natural["text"], "searchable text")
        self.assertNotIn("<P>", natural["text"])
        self.assertEqual(natural["meta"]["annotations"][0]["yes_no_answer"], "NONE")

    def test_normalizes_msmarco_and_rejects_unknown_adapter(self):
        record = normalize(
            "msmarco",
            {"_id": "passage-1", "title": "Passage", "text": "Body"},
            3,
        )
        self.assert_record_shape(record)
        self.assertEqual(record["id"], "passage-1")
        with self.assertRaisesRegex(ValueError, "Unsupported dataset"):
            normalize("unknown", {}, 0)

    def test_infers_adapter_from_one_row_schema(self):
        self.assertEqual(
            infer_dataset_name({"anchor": "q", "positive": "p"}),
            "dureader",
        )
        self.assertEqual(
            infer_dataset_name({"repo_name": "org/repo", "path": "a.py", "code": "pass"}),
            "github_code",
        )
        self.assertEqual(
            infer_dataset_name({"_id": "p1", "title": "Title", "text": "Body"}),
            "hotpotqa",
        )
        with self.assertRaisesRegex(DatasetReaderError, "无法自动识别数据集字段"):
            infer_dataset_name({"unknown": "value"})

    def test_registers_custom_adapter_without_new_physical_parser(self):
        def custom_adapter(row, index):
            return {
                "id": row["key"],
                "title": None,
                "text": row["body"],
                "query": None,
                "answers": [],
                "meta": {"index": index},
            }

        register_adapter("custom_test", custom_adapter, replace=True)
        record = normalize("CUSTOM_TEST", {"key": 9, "body": "custom text"}, 4)

        self.assertIn("custom_test", available_adapters())
        self.assertEqual(record["id"], "9")
        self.assertEqual(record["text"], "custom text")
        self.assertEqual(record["meta"]["index"], 4)


class DatasetStreamingTests(unittest.TestCase):
    def test_infers_parquet_jsonl_and_gzip_formats(self):
        self.assertEqual(infer_local_format(Path("train.parquet")), "parquet")
        self.assertEqual(infer_local_format(Path("train.jsonl")), "json")
        self.assertEqual(infer_local_format(Path("train.jsonl.gz")), "json")
        with self.assertRaisesRegex(ValueError, "无法从文件后缀"):
            infer_local_format(Path("train.zip"))

    def test_unknown_suffix_is_content_probed_and_streamed(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            json_path = root / "records.data"
            json_path.write_text(
                '{"_id":"one","text":"first"}\n'
                '{"_id":"two","text":"second"}\n',
                encoding="utf-8",
            )
            text_path = root / "notes.bin"
            text_path.write_text("first line\nsecond line\n", encoding="utf-8")

            json_records = list(iter_local_dataset(json_path, "hotpotqa"))
            text_records = list(iter_local_dataset(text_path, "hotpotqa"))

        self.assertEqual([record["id"] for record in json_records], ["one", "two"])
        self.assertEqual([record["text"] for record in text_records], ["first line", "second line"])

    def test_unknown_suffix_can_use_explicit_datasets_builder(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "records.payload"
            path.write_text("body one\nbody two\n", encoding="utf-8")
            with patch(
                "knowledge_search.dataset_reader._load_dataset",
                return_value=iter([{"text": "body one"}, {"text": "body two"}]),
            ) as mocked:
                records = list(
                    iter_local_dataset(path, "hotpotqa", file_format="text")
                )

        self.assertEqual([record["text"] for record in records], ["body one", "body two"])
        mocked.assert_called_once_with(
            "text",
            data_files={"train": str(path.resolve())},
            split="train",
            streaming=True,
        )

    def test_local_reader_auto_selects_adapter_after_one_row_probe(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "records.parquet"
            path.touch()
            rows = iter(
                [
                    {"anchor": "q1", "positive": "p1"},
                    {"anchor": "q2", "positive": "p2"},
                ]
            )
            with patch(
                "knowledge_search.dataset_reader._load_dataset",
                return_value=rows,
            ) as mocked:
                records = list(iter_local_dataset(path))

        self.assertEqual([record["query"] for record in records], ["q1", "q2"])
        self.assertEqual([record["text"] for record in records], ["p1", "p2"])
        mocked.assert_called_once_with(
            "parquet",
            data_files={"train": str(path.resolve())},
            split="train",
            streaming=True,
        )

    def test_unified_entry_treats_dataset_file_names_as_local(self):
        with self.assertRaisesRegex(FileNotFoundError, "数据集文件不存在"):
            next(iter_dataset("missing.parquet", "dureader"))

    def test_local_reader_streams_rows_through_one_adapter(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "train.parquet"
            path.touch()
            rows = [
                {"anchor": "q1", "positive": "p1"},
                {"anchor": "q2", "positive": "p2"},
            ]
            with patch(
                "knowledge_search.dataset_reader._load_dataset",
                return_value=iter(rows),
            ) as mocked:
                records = list(iter_local_dataset(path, "dureader"))

        self.assertEqual([record["text"] for record in records], ["p1", "p2"])
        mocked.assert_called_once_with(
            "parquet",
            data_files={"train": str(path.resolve())},
            split="train",
            streaming=True,
        )

    def test_dureader_convenience_reader_and_huggingface_config(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "part.parquet"
            path.touch()
            with patch(
                "knowledge_search.dataset_reader._load_dataset",
                return_value=iter([{"anchor": "q", "positive": "p"}]),
            ):
                self.assertEqual(next(iter_local_dureader(path))["text"], "p")

        with patch(
            "knowledge_search.dataset_reader._load_dataset",
            return_value=iter(
                [
                    {
                        "url": "u",
                        "func_name": "f",
                        "whole_func_string": "def f(): pass",
                    }
                ]
            ),
        ) as mocked:
            record = next(
                iter_huggingface(
                    "code-search-net/code_search_net",
                    "all",
                    "train",
                    "codesearchnet",
                )
            )

        self.assertEqual(record["title"], "f")
        mocked.assert_called_once_with(
            "code-search-net/code_search_net",
            split="train",
            streaming=True,
            name="all",
        )

    def test_dataset_blocks_keep_text_canonical_and_records_independent(self):
        records = [
            {
                "id": "a",
                "title": "First",
                "text": "canonical one",
                "query": "q1",
                "answers": [],
                "meta": {"language": "Python"},
            },
            {
                "id": "b",
                "title": None,
                "text": "canonical two",
                "query": None,
                "answers": [],
                "meta": {},
            },
        ]

        blocks = list(iter_dataset_blocks(records, source_name="sample"))

        self.assertEqual([block.content for block in blocks], ["canonical one", "canonical two"])
        self.assertEqual([block.record_path for block in blocks], ["sample[a]", "sample[b]"])
        self.assertEqual(blocks[0].heading_path, ("First",))
        self.assertEqual(blocks[0].language, "Python")
        self.assertTrue(all(block.hard_boundary_before for block in blocks))
        self.assertTrue(all(block.hard_boundary_after for block in blocks))

    def test_reader_wraps_backend_failures(self):
        with patch(
            "knowledge_search.dataset_reader._load_dataset",
            side_effect=OSError("backend failed"),
        ):
            with self.assertRaisesRegex(DatasetReaderError, "读取 Hugging Face"):
                next(iter_huggingface("repo", None, "train", "dureader"))

    @unittest.skipUnless(HAS_DATASETS, "datasets/pyarrow 未安装")
    def test_real_parquet_and_gzipped_jsonl_are_streamed(self):
        import pyarrow as pa
        import pyarrow.parquet as parquet

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            parquet_path = root / "dureader.parquet"
            parquet.write_table(
                pa.table(
                    {
                        "anchor": ["question one", "question two"],
                        "positive": ["positive one", "positive two"],
                    }
                ),
                parquet_path,
            )
            parquet_records = list(iter_local_dureader(parquet_path))

            jsonl_path = root / "passages.jsonl.gz"
            with gzip.open(jsonl_path, "wt", encoding="utf-8") as stream:
                stream.write(
                    json.dumps(
                        {"_id": "p1", "title": "One", "text": "gzip body"}
                    )
                    + "\n"
                )
            jsonl_records = list(iter_local_dataset(jsonl_path, "hotpotqa"))

        self.assertEqual(
            [record["text"] for record in parquet_records],
            ["positive one", "positive two"],
        )
        self.assertEqual(jsonl_records[0]["id"], "p1")
        self.assertEqual(jsonl_records[0]["text"], "gzip body")


if __name__ == "__main__":
    unittest.main()
