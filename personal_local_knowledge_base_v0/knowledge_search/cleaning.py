"""输入文本清洗。"""

# re 用来压缩连续空格和制表符。
import re
# unicodedata 用来统一 Unicode 字符的等价表示，避免检索时出现重复形式。
import unicodedata


def clean_text(text: str) -> str:
    """规范换行、空白和不可见字符，同时保留 Markdown 标题等语义文字。"""

    # 空输入直接返回空字符串，避免后续无意义的处理。
    if not text:
        return ""

    # NFC 会把视觉上相同但编码不同的字符组合成统一形式。
    normalized = unicodedata.normalize("NFC", text)
    # 去掉 UTF-8 BOM 和 SQLite 不适合存储的空字节。
    normalized = normalized.replace("\ufeff", "").replace("\x00", "")
    # 将 Windows、旧 Mac 和 Unix 的换行格式统一为 \n。
    normalized = normalized.replace("\r\n", "\n").replace("\r", "\n")

    # 逐行处理，便于同时压缩行内空格和连续空行。
    cleaned_lines: list[str] = []
    # 记录上一行是否为空，最多保留一个空行作为段落分隔。
    previous_blank = False
    for raw_line in normalized.split("\n"):
        # 连续空格/制表符合并成一个空格，并去除行首尾空白。
        line = re.sub(r"[ \t]+", " ", raw_line).strip()
        if not line:
            # 只有前一行不是空行时，才保存本次空行。
            if not previous_blank:
                cleaned_lines.append("")
            previous_blank = True
            continue
        # 非空行保留清洗后的内容，并重置连续空行状态。
        cleaned_lines.append(line)
        previous_blank = False

    # 再次去除整个文档两端的空白，避免产生空分段。
    return "\n".join(cleaned_lines).strip()
