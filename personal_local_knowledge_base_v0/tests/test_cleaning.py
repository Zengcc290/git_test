# 使用 Python 标准库 unittest，避免测试依赖额外测试框架。
import unittest

# 被测函数：负责统一文本中的换行和空白。
from knowledge_search.cleaning import clean_text, iter_clean_text


class CleaningTests(unittest.TestCase):
    def test_normalizes_whitespace_and_newlines(self):
        # 构造同时包含 BOM、不同换行、制表符、连续空行和空字节的输入。
        source = "\ufeff标题\r\n\r\n\r\n  第一行\t\t内容  \r\n\x00"
        # 期望结果保留一个段落空行，并压缩行内空白。
        self.assertEqual(clean_text(source), "标题\n\n第一行 内容")

    def test_empty_text(self):
        # 只有空白的文本最终应被视为空文档。
        self.assertEqual(clean_text("   \n\n  "), "")

    def test_streaming_cleaner_accepts_multiple_chunks(self):
        # 模拟文件被分成多个读取块，验证块边界不会改变清洗结果。
        chunks = iter(["  第一", "行\t内容\n\n", "\n第二行  "])
        cleaned = "".join(iter_clean_text(chunks)).strip()
        self.assertEqual(cleaned, "第一行 内容\n\n第二行")


if __name__ == "__main__":
    # 允许直接执行本测试文件。
    unittest.main()
