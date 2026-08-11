# 使用标准库 unittest 验证 jieba 词索引查询的基本行为。
import unittest

# 导入文本分词和 FTS5 查询构造函数。
from knowledge_search.tokenization import tokenize_for_search, to_token_fts_query


class TokenizationTests(unittest.TestCase):
    def test_tokenizes_chinese_query_for_search(self):
        # 这个查询应被拆成多个有意义的中文词，而不是一个连续长字符串。
        query = "氧化还原反应"
        tokens = tokenize_for_search(query)
        self.assertIn("氧化", tokens)
        self.assertIn("还原", tokens)
        self.assertIn("反应", tokens)

    def test_builds_and_fts_query(self):
        # 词项之间使用 AND，避免只命中一个词时返回过多无关内容。
        query = "氧化还原反应"
        fts_query = to_token_fts_query(query)
        self.assertEqual(fts_query, '"氧化" AND "还原" AND "反应"')

    def test_blank_query_returns_empty_token_query(self):
        # 纯空白没有有效词项，交给原始查询层处理错误或兜底。
        self.assertEqual(to_token_fts_query("  "), "")


if __name__ == "__main__":
    # 允许直接执行本测试文件。
    unittest.main()
