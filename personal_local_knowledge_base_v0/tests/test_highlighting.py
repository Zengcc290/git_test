# 高亮模块的行为测试使用标准库 unittest。
import unittest

# 导入查询转义和高亮函数。
from knowledge_search.highlighting import highlight_text, to_fts_query


class HighlightingTests(unittest.TestCase):
    def test_highlights_case_insensitively(self):
        # 搜索词大小写不同也应命中，并保留原文的 SQLite 大小写。
        self.assertEqual(
            highlight_text("SQLite is fast", "sqlite", "[[", "]]"),
            "[[SQLite]] is fast",
        )

    def test_escapes_fts_syntax(self):
        # 多个普通关键词应转换成安全的 FTS5 AND 查询。
        self.assertEqual(to_fts_query("sqlite search"), '"sqlite" AND "search"')

    def test_rejects_blank_query(self):
        # 空查询不能生成有效的 MATCH 表达式。
        with self.assertRaises(ValueError):
            to_fts_query("  ")


if __name__ == "__main__":
    # 允许直接执行本测试文件。
    unittest.main()
