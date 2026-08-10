# 使用临时目录生成一次性 PDF，避免在项目中留下测试产物。
import tempfile
import unittest
from pathlib import Path

# 用 pypdf 组装带文本层的最小 PDF。
from pypdf import PdfWriter
from pypdf.generic import DecodedStreamObject, DictionaryObject, NameObject

# 被测函数：根据扩展名抽取文档并返回元数据。
from knowledge_search.extractors import extract_document


class ExtractorTests(unittest.TestCase):
    def test_extracts_text_from_pdf_text_layer(self):
        # 这个测试只验证文本层抽取，不涉及 OCR。
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "note.pdf"
            # 创建一个空白页面，再手动附加 Helvetica 字体和内容流。
            writer = PdfWriter()
            page = writer.add_blank_page(width=612, height=792)
            font = DictionaryObject(
                {
                    NameObject("/Type"): NameObject("/Font"),
                    NameObject("/Subtype"): NameObject("/Type1"),
                    NameObject("/BaseFont"): NameObject("/Helvetica"),
                }
            )
            page[NameObject("/Resources")] = DictionaryObject(
                {NameObject("/Font"): DictionaryObject({NameObject("/F1"): font})}
            )
            stream = DecodedStreamObject()
            stream.set_data(b"BT /F1 12 Tf 72 720 Td (PDF search works) Tj ET")
            page[NameObject("/Contents")] = stream
            # 将构造好的 PDF 写入临时路径。
            with path.open("wb") as handle:
                writer.write(handle)

            # 抽取后应识别 PDF 类型并得到内容流中的文本。
            document = extract_document(path)
            self.assertEqual(document.file_type, "pdf")
            self.assertIn("PDF search works", document.text)


if __name__ == "__main__":
    # 允许直接执行本测试文件。
    unittest.main()
