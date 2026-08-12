import tempfile
import unittest
from pathlib import Path

from knowledge_search.database import KnowledgeBase
from knowledge_search.indexer import index_paths


class SearchValidationTests(unittest.TestCase):
    def test_expected_document_is_returned_for_each_keyword(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "python.md").write_text(
                "Python virtualenv creates an isolated environment.",
                encoding="utf-8",
            )
            (root / "sqlite.md").write_text(
                "SQLite FTS5 provides local full-text search.",
                encoding="utf-8",
            )

            with KnowledgeBase(root / "knowledge.db") as knowledge_base:
                stats = index_paths(knowledge_base, [root])

                self.assertEqual(stats.indexed, 2)
                self.assertEqual(knowledge_base.search("virtualenv")[0].filename, "python.md")
                self.assertEqual(knowledge_base.search("FTS5")[0].filename, "sqlite.md")


if __name__ == "__main__":
    unittest.main()
