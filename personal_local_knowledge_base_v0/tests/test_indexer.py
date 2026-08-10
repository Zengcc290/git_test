# 使用临时目录模拟用户提供的文档目录。
import tempfile
import unittest
from pathlib import Path

# 导入数据库和完整索引流水线。
from knowledge_search.database import KnowledgeBase
from knowledge_search.indexer import index_paths


class IndexerTests(unittest.TestCase):
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
            # JSON 文件不在 SUPPORTED_SUFFIXES 中，应被忽略。
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
