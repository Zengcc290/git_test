import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from knowledge_search.database import KnowledgeBase
from knowledge_search.indexer import index_paths
from knowledge_search.json_parser import (
    JsonRecordTooLargeError,
    JsonSizeLimitError,
    JsonField,
    JsonFilter,
    JsonProfile,
    inspect_json_structure,
    iter_json_text,
    parse_size,
    parse_json_preview,
)


class JsonParserTests(unittest.TestCase):
    def test_parse_human_readable_sizes(self):
        self.assertEqual(parse_size("512MB"), 512 * 1024**2)
        self.assertEqual(parse_size("1GB"), 1024**3)
        self.assertEqual(parse_size("1.5 GiB"), 1536 * 1024**2)
        self.assertEqual(parse_size("4096"), 4096)
        self.assertEqual(parse_size("0"), 0)

    def test_parse_size_rejects_invalid_values(self):
        for value in ("", "-1MB", "1XB", "1.1B"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                parse_size(value)

    def _profile(
        self,
        *,
        index_mode: str = "record",
        record_path: str = "$",
        filters: tuple[JsonFilter, ...] | None = None,
    ) -> JsonProfile:
        return JsonProfile(
            name="items",
            record_path=record_path,
            index_mode=index_mode,
            fields=(
                JsonField(path="id", name="ID"),
                JsonField(path="title", name="标题"),
                JsonField(path="tags[*]", name="标签", join="、"),
                JsonField(path="text", name="正文"),
            ),
            separator="\n",
            filters=(
                (JsonFilter(path="status", operator="equals", expected="published"),)
                if filters is None
                else filters
            ),
            fingerprint="test",
        )

    def _write_json_lines(self, root: Path) -> Path:
        path = root / "items.json"
        records = [
            {
                "id": "1",
                "title": "SQLite 教程",
                "tags": ["数据库", "搜索"],
                "text": "SQLite FTS5",
                "status": "published",
            },
            {
                "id": "2",
                "title": "草稿",
                "tags": ["草稿"],
                "text": "不应进入索引",
                "status": "draft",
            },
        ]
        path.write_text(
            "\n".join(json.dumps(record, ensure_ascii=False) for record in records),
            encoding="utf-8",
        )
        return path

    def test_json_lines_are_parsed_across_small_read_chunks(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = self._write_json_lines(Path(temp_dir))

            records = list(iter_json_text(path, self._profile(), read_size=3))

            self.assertEqual(len(records), 1)
            self.assertIn("标题: SQLite 教程", records[0])
            self.assertIn("标签: 数据库、搜索", records[0])
            self.assertNotIn("草稿", records[0])

    def test_top_level_array_is_streamed_one_record_at_a_time(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "items.json"
            path.write_text(
                json.dumps(
                    [
                        {"id": 1, "title": "one", "tags": [], "text": "a", "status": "published"},
                        {"id": 2, "title": "two", "tags": [], "text": "b", "status": "published"},
                    ],
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            profile = self._profile()
            records = list(iter_json_text(path, profile, read_size=4))

            self.assertEqual(len(records), 2)
            self.assertIn("标题: one", records[0])
            self.assertIn("标题: two", records[1])

    def test_nested_record_path_yields_before_later_record_is_parsed(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "nested-items.json"
            # 第二条记录故意损坏；第一条仍应先被交给下游，而不是等待
            # 整个顶层对象解析完成后才开始产出。
            path.write_text(
                '{"data":{"items":['
                '{"id":1,"title":"first","tags":[],"text":"one",'
                '"status":"published"},'
                '{"id":2,"title":"broken",'
                '"status":"published"',
                encoding="utf-8",
            )
            profile = self._profile(
                record_path="$.data.items[*]",
                filters=(),
            )

            records = iter_json_text(path, profile, read_size=3)
            try:
                first = next(records)
                self.assertIn("标题: first", first)
                with self.assertRaises(ValueError):
                    next(records)
            finally:
                records.close()

    def test_nested_record_path_indexes_each_array_item(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            path = root / "nested-items.json"
            path.write_text(
                json.dumps(
                    {
                        "data": {
                            "items": [
                                {"title": "first", "status": "published"},
                                {"title": "second", "status": "published"},
                            ]
                        }
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            profile = JsonProfile(
                name="nested",
                record_path="$.data.items[*]",
                index_mode="record",
                fields=(JsonField(path="title"),),
                separator="\n",
                filters=(JsonFilter(path="status", operator="equals", expected="published"),),
                fingerprint="nested",
            )

            records = list(iter_json_text(path, profile, read_size=2))

            self.assertEqual(records, ["first", "second"])

    def test_record_larger_than_probe_is_streamed_without_merging_records(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "large-records.json"
            first = {"id": 1, "title": "large", "payload": "x" * 300}
            second = {"id": 2, "title": "small", "payload": "tail"}
            first_text = json.dumps(first, ensure_ascii=False)
            path.write_text(
                first_text + "\n" + json.dumps(second, ensure_ascii=False),
                encoding="utf-8",
            )
            profile = JsonProfile(
                name="raw-large",
                record_path="$",
                index_mode="record",
                fields=(JsonField(path="title"),),
                separator="\n",
                filters=(),
                fingerprint="raw-large",
            )

            blocks = list(
                iter_json_text(
                    path,
                    profile,
                    read_size=17,
                    record_probe_size=64,
                )
            )

            self.assertGreater(len(blocks), 2)
            self.assertTrue(all(len(block) <= 17 for block in blocks if block))
            first_blocks = []
            second_blocks = []
            current = first_blocks
            for block in blocks:
                if getattr(block, "record_start", True) and current is first_blocks and first_blocks:
                    current = second_blocks
                current.append(str(block))
            self.assertEqual("".join(first_blocks), first_text)
            self.assertEqual("".join(second_blocks), "small")

    def test_nested_large_record_keeps_record_boundary(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "nested-large-records.json"
            first = {"id": 1, "title": "large", "payload": "x" * 300}
            second = {"id": 2, "title": "small", "payload": "tail"}
            path.write_text(
                json.dumps(
                    {"data": {"items": [first, second]}},
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            profile = JsonProfile(
                name="nested-raw-large",
                record_path="$.data.items[*]",
                index_mode="record",
                fields=(JsonField(path="title"),),
                separator="\n",
                filters=(),
                fingerprint="nested-raw-large",
            )

            blocks = list(
                iter_json_text(
                    path,
                    profile,
                    read_size=17,
                    record_probe_size=64,
                )
            )

            first_blocks = []
            second_blocks = []
            current = first_blocks
            for block in blocks:
                if getattr(block, "record_start", True) and current is first_blocks and first_blocks:
                    current = second_blocks
                current.append(str(block))
            self.assertEqual("".join(first_blocks), json.dumps(first, ensure_ascii=False))
            self.assertEqual("".join(second_blocks), "small")

    def test_preview_rejects_a_record_that_cannot_be_materialized(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "large-record.json"
            path.write_text(
                json.dumps({"title": "x" * 100}, ensure_ascii=False),
                encoding="utf-8",
            )
            profile = JsonProfile(
                name="raw-large",
                record_path="$",
                index_mode="record",
                fields=(JsonField(path="title"),),
                separator="\n",
                filters=(),
                fingerprint="raw-large",
            )

            with self.assertRaises(JsonRecordTooLargeError):
                parse_json_preview(
                    path,
                    profile,
                    limit=1,
                    record_probe_size=32,
                )

    def test_file_mode_keeps_streaming_blocks_but_combines_downstream(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = self._write_json_lines(Path(temp_dir))
            profile = self._profile(index_mode="file")

            blocks = list(iter_json_text(path, profile, read_size=5))

            self.assertEqual("".join(blocks).count("标题:"), 1)
            self.assertIn("SQLite 教程", "".join(blocks))

    def test_preview_only_consumes_requested_records(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = self._write_json_lines(Path(temp_dir))

            previews = parse_json_preview(path, self._profile(), limit=1)

            self.assertEqual(len(previews), 1)
            self.assertIn("SQLite 教程", previews[0])

    def test_json_size_limit_is_checked_before_streaming(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = self._write_json_lines(Path(temp_dir))

            with self.assertRaises(JsonSizeLimitError):
                list(iter_json_text(path, self._profile(), max_size=1))

    def test_structure_scan_does_not_use_index_size_limit_by_default(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = self._write_json_lines(Path(temp_dir))

            with patch("knowledge_search.json_parser.ensure_json_size") as check_size:
                inspect_json_structure(path, max_records=1, read_size=3)

            check_size.assert_called_once_with(path.resolve(), 0)

    def test_structure_report_summarizes_nested_paths(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "nested.json"
            path.write_text(
                json.dumps(
                    [
                        {"id": 1, "meta": {"kind": "a"}, "labels": ["x", "y"]},
                        {"id": 2, "meta": {"kind": "b"}, "labels": []},
                    ],
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            report = inspect_json_structure(
                path,
                max_records=1,
                read_size=3,
                max_depth=5,
            )
            entries = {entry.path: entry for entry in report.entries}

            self.assertFalse(report.complete)
            self.assertEqual(report.records_scanned, 1)
            self.assertEqual(entries["$"].types, (("object", 1),))
            self.assertEqual(entries["$.meta.kind"].types, (("string", 1),))
            self.assertEqual(entries["$.labels[*]"].count, 2)

    def test_json_lines_can_go_through_the_indexer(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            path = self._write_json_lines(root)
            with KnowledgeBase(root / "knowledge.db") as knowledge_base:
                stats = index_paths(
                    knowledge_base,
                    [path],
                    json_profile=self._profile(),
                )

                self.assertEqual(stats.indexed, 1)
                self.assertEqual(knowledge_base.chunk_count(), 1)
                self.assertTrue(knowledge_base.search("SQLite"))
                self.assertFalse(knowledge_base.search("草稿"))


if __name__ == "__main__":
    unittest.main()
