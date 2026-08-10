# 使用 unittest 编写可直接运行的分段测试。
import unittest

# 被测函数：负责按段落和长度切分文本。
from knowledge_search.chunking import chunk_text


class ChunkingTests(unittest.TestCase):
    def test_keeps_short_paragraphs_together(self):
        # 两个短段落加上分隔符没有超过目标长度，因此应该合并。
        chunks = chunk_text("第一段\n\n第二段", chunk_size=20, overlap=3)
        self.assertEqual(len(chunks), 1)
        self.assertIn("第一段", chunks[0].content)
        self.assertIn("第二段", chunks[0].content)

    def test_splits_long_text(self):
        # 重复长句应被切成多个非空分段。
        chunks = chunk_text("这是一个很长的句子。" * 20, chunk_size=30, overlap=5)
        self.assertGreater(len(chunks), 1)
        self.assertTrue(all(chunk.content for chunk in chunks))
        self.assertEqual([chunk.index for chunk in chunks], list(range(len(chunks))))

    def test_rejects_invalid_options(self):
        # 目标长度为 0 会导致无法建立有效窗口。
        with self.assertRaises(ValueError):
            chunk_text("text", chunk_size=0)
        # overlap 不能大于等于 chunk_size，否则窗口无法向前推进。
        with self.assertRaises(ValueError):
            chunk_text("text", chunk_size=10, overlap=10)


if __name__ == "__main__":
    # 允许直接执行本测试文件。
    unittest.main()
