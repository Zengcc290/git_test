# 使用临时目录模拟用户提供的文档目录。
import tempfile
import unittest
from pathlib import Path

# 导入数据库和完整索引流水线。
from knowledge_search.database import KnowledgeBase
from knowledge_search.indexer import discover_files, index_paths
from knowledge_search.json_parser import JsonField, JsonProfile


class IndexerTests(unittest.TestCase):
    def test_excludes_directories_deduplicates_inputs_and_limits_files(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "keep.txt").write_text("keep", encoding="utf-8")
            (root / "nested").mkdir()
            (root / "nested" / "also.txt").write_text("also", encoding="utf-8")
            (root / "skip").mkdir()
            (root / "skip" / "hidden.txt").write_text("hidden", encoding="utf-8")
            (root / "generated").mkdir()
            (root / "generated" / "ignored.txt").write_text("ignored", encoding="utf-8")

            discovered = list(
                discover_files(
                    [root, root / "nested"],
                    exclude_dirs=["skip", "generated/*"],
                    max_files=2,
                )
            )

            self.assertEqual(
                discovered,
                sorted((root / "keep.txt", root / "nested" / "also.txt")),
            )

    def test_json_config_is_not_indexed_when_inside_input_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            data_path = root / "items.json"
            config_path = root / "json-config.json"
            data_path.write_text(
                '{"title": "searchable", "status": "published"}',
                encoding="utf-8",
            )
            config_path.write_text(
                '{"name": "items", "record_path": "$", "fields": ["title"]}',
                encoding="utf-8",
            )
            profile = JsonProfile.from_file(config_path)

            with KnowledgeBase(root / "knowledge.db") as knowledge_base:
                stats = index_paths(
                    knowledge_base,
                    [root, data_path],
                    json_profile=profile,
                )

                self.assertEqual(stats.files_found, 1)
                self.assertEqual(stats.indexed, 1)
                self.assertEqual(knowledge_base.document_count(), 1)
                self.assertEqual(knowledge_base.list_documents()[0].filename, "items.json")

    def test_oversized_json_is_rejected_before_parsing(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            data_path = root / "items.json"
            config_path = root / "config.json"
            data_path.write_text('{"title": "too large"}', encoding="utf-8")
            config_path.write_text(
                '{"name": "items", "record_path": "$", "fields": ["title"]}',
                encoding="utf-8",
            )
            profile = JsonProfile.from_file(config_path)

            with KnowledgeBase(root / "knowledge.db") as knowledge_base:
                stats = index_paths(
                    knowledge_base,
                    [data_path],
                    json_profile=profile,
                    max_json_size=1,
                )

                self.assertEqual(stats.oversized, 1)
                self.assertEqual(stats.failed, 0)
                self.assertEqual(knowledge_base.document_count(), 0)

    def test_reports_single_file_progress_events(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "one.txt").write_text("one", encoding="utf-8")
            (root / "two.txt").write_text("two", encoding="utf-8")
            events = []

            with KnowledgeBase(root / "knowledge.db") as knowledge_base:
                index_paths(
                    knowledge_base,
                    [root],
                    progress_callback=events.append,
                )

            self.assertEqual([event.status for event in events], [
                "processing",
                "indexed",
                "processing",
                "indexed",
            ])
            self.assertEqual({event.total for event in events}, {2})

    def test_large_json_record_is_chunked_without_merging_next_record(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            data_path = root / "large.json"
            data_path.write_text(
                '{"id":1,"title":"large","payload":"'
                + ("x" * 300)
                + '"}\n{"id":2,"title":"small","payload":"tail"}',
                encoding="utf-8",
            )
            profile = JsonProfile(
                name="large",
                record_path="$",
                index_mode="record",
                fields=(JsonField(path="title"),),
                separator="\n",
                filters=(),
                fingerprint="large",
            )

            with KnowledgeBase(root / "knowledge.db") as knowledge_base:
                stats = index_paths(
                    knowledge_base,
                    [data_path],
                    json_profile=profile,
                    chunk_size=80,
                    overlap=10,
                    json_record_probe_size=64,
                )
                rows = knowledge_base.connection.execute(
                    "SELECT content FROM chunks ORDER BY chunk_index"
                ).fetchall()

            self.assertEqual(stats.indexed, 1)
            self.assertGreater(len(rows), 2)
            contents = [row["content"] for row in rows]
            large_contents = [content for content in contents if '"large"' in content]
            small_contents = [content for content in contents if content == "small"]
            self.assertTrue(large_contents)
            self.assertEqual(small_contents, ["small"])

    def test_indexes_txt_and_markdown_incrementally(self):
        # 测试 TXT、Markdown、增量跳过和空文件清理。
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            # 两个支持类型文件应被发现并写入索引。
            (root / "python.txt").write_text(
                "Python 项目使用 SQLite FTS5 做关键词搜索。", encoding="utf-8"
            )
            (root / "readme.md").write_text(
                "# 本地知识库\n\nMarkdown 文档也可以被索引。", encoding="utf-8"
            )
            # 未提供 JSON 配置时，JSON 文件应被忽略。
            (root / "ignore.json").write_text("not indexed", encoding="utf-8")

            with KnowledgeBase(root / "knowledge.db") as knowledge_base:
                # 第一次索引应新增两个文档且不产生失败。
                first = index_paths(knowledge_base, [root])
                self.assertEqual(first.files_found, 2)
                self.assertEqual(first.indexed, 2)
                self.assertEqual(first.failed, 0)
                # 搜索两个不同文件中的关键词，验证 FTS5 已可用。
                self.assertTrue(knowledge_base.search("SQLite"))
                self.assertTrue(knowledge_base.search("Markdown"))
                self.assertTrue(knowledge_base.search("本地"))

                # 第二次索引使用相同哈希，应全部跳过。
                second = index_paths(knowledge_base, [root])
                self.assertEqual(second.skipped, 2)
                self.assertEqual(knowledge_base.document_count(), 2)

                # 文件变为空后重新索引，应删除其过期分段。
                (root / "python.txt").write_text("\n\n", encoding="utf-8")
                third = index_paths(knowledge_base, [root / "python.txt"])
                self.assertEqual(third.empty, 1)
                self.assertEqual(knowledge_base.search("SQLite"), [])
                self.assertEqual(knowledge_base.document_count(), 1)


if __name__ == "__main__":
    # 允许直接执行本测试文件。
    unittest.main()
