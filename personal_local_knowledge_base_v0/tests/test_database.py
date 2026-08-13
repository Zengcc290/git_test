# 使用临时目录隔离数据库文件，测试完成后自动清理。
import tempfile
import unittest
from pathlib import Path

# 导入数据库门面和两个用于构造测试数据的模型。
from knowledge_search.database import KnowledgeBase
from knowledge_search.models import Chunk, ExtractedDocument


class DatabaseTests(unittest.TestCase):
    def test_chunk_window_returns_neighbors_from_same_document(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            document = ExtractedDocument(
                path=(root / "note.md").resolve(),
                file_type="md",
                text="zero one two",
                sha256="window-hash",
                size=12,
                modified_ns=1,
            )
            with KnowledgeBase(root / "knowledge.db") as knowledge_base:
                knowledge_base.replace_document(
                    document,
                    [Chunk(0, "zero"), Chunk(1, "one"), Chunk(2, "two")],
                )
                hit = knowledge_base.search("one")[0]
                window = knowledge_base.chunk_window(hit.chunk_id)

            self.assertEqual([chunk.index for chunk in window], [0, 1, 2])
            self.assertEqual([chunk.content for chunk in window], ["zero", "one", "two"])
    def test_fts5_search_and_replace_document(self):
        # 每次测试创建独立的临时 SQLite 数据库。
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = Path(temp_dir) / "knowledge.db"
            source_path = Path(temp_dir) / "note.md"
            # 创建一个与数据库记录对应的源文件路径。
            source_path.write_text("SQLite note", encoding="utf-8")
            # 手工构造抽取结果，隔离数据库层测试与文件抽取层。
            document = ExtractedDocument(
                path=source_path.resolve(),
                file_type="md",
                text="SQLite note",
                sha256="hash-1",
                size=11,
                modified_ns=1,
            )

            with KnowledgeBase(db_path) as knowledge_base:
                # 写入一个分段后，用 FTS5 搜索它。
                knowledge_base.replace_document(document, [Chunk(0, "SQLite note")])
                results = knowledge_base.search("sqlite")
                self.assertEqual(len(results), 1)
                self.assertIn("<mark>SQLite</mark>", results[0].highlighted_content)
                self.assertEqual(knowledge_base.document_count(), 1)
                self.assertEqual(knowledge_base.chunk_count(), 1)

                # 替换同一路径文档，验证旧内容会从 FTS5 中消失。
                newer = ExtractedDocument(
                    path=document.path,
                    file_type="md",
                    text="FTS5 replacement",
                    sha256="hash-2",
                    size=16,
                    modified_ns=2,
                )
                knowledge_base.replace_document(newer, [Chunk(0, "FTS5 replacement")])
                self.assertEqual(knowledge_base.search("sqlite"), [])
                self.assertEqual(len(knowledge_base.search("FTS5")), 1)

    def test_health_check_reports_orphan_chunks_and_missing_token_rows(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = Path(temp_dir) / "knowledge.db"
            with KnowledgeBase(db_path) as knowledge_base:
                knowledge_base.connection.execute("PRAGMA foreign_keys = OFF")
                knowledge_base.connection.execute(
                    """
                    INSERT INTO chunks(document_id, chunk_index, content, start_offset)
                    VALUES (999, 0, 'orphan content', 0)
                    """
                )
                knowledge_base.connection.commit()

                report = knowledge_base.check_health()

            self.assertFalse(report.healthy)
            self.assertTrue(any("孤立" in issue for issue in report.issues))
            self.assertTrue(any("chunk_tokens" in issue for issue in report.issues))


if __name__ == "__main__":
    # 允许直接执行本测试文件。
    unittest.main()
