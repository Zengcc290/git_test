"""输入文本清洗。"""

# re 用来压缩连续空格和制表符。
import re
# unicodedata 用来统一 Unicode 字符的等价表示，避免检索时出现重复形式。
import unicodedata
from collections.abc import Iterable, Iterator


def _clean_line(raw_line: str, previous_blank: bool) -> tuple[str, bool]:
    """清洗一行文字，并返回清洗结果和新的空行状态。"""

    # 压缩行内空格，再去除行首尾空白。
    line = re.sub(r"[ \t]+", " ", raw_line).strip()
    if not line:
        # 连续空行只保留第一个；换行符是流式输出中的段落分隔符。
        return ("" if previous_blank else "\n", True)
    # 给普通行补一个换行，方便下游识别段落边界。
    return line + "\n", False


def iter_clean_text(
    text_chunks: Iterable[str],
    *,
    max_pending: int = 64 * 1024,
) -> Iterator[str]:
    """逐块清洗文本，保证待处理缓存不会随文件总大小增长。"""

    # line_buffer 只保存当前尚未遇到换行符的残余内容。
    line_buffer = ""
    # 记录上一行是否为空，用于压缩连续空行。
    previous_blank = False

    for text_chunk in text_chunks:
        if not text_chunk:
            continue

        # 每个输入块独立做 Unicode、BOM、空字节和换行规范化。
        normalized = unicodedata.normalize("NFC", text_chunk)
        normalized = normalized.replace("\ufeff", "").replace("\x00", "")
        normalized = normalized.replace("\r\n", "\n").replace("\r", "\n")
        line_buffer += normalized

        # 处理完整行，最后一个没有换行符的元素留在缓存中。
        lines = line_buffer.split("\n")
        line_buffer = lines.pop()
        for raw_line in lines:
            cleaned_line, previous_blank = _clean_line(raw_line, previous_blank)
            if cleaned_line:
                yield cleaned_line

        # 极端情况下单行可能比整个输入块还大，主动切出一小段防止缓存无限增长。
        while len(line_buffer) > max_pending:
            split_at = line_buffer.rfind(" ", 0, max_pending)
            if split_at <= 0:
                split_at = max_pending
            raw_piece = line_buffer[:split_at]
            line_buffer = line_buffer[split_at:]
            cleaned_piece = re.sub(r"[ \t]+", " ", raw_piece).strip()
            if cleaned_piece:
                # 这里不是自然换行，只补空格，避免把一行误拆成两个段落。
                yield cleaned_piece + " "
                previous_blank = False

    # 文件结尾可能没有换行符，最后的残余也必须清洗并输出。
    if line_buffer:
        cleaned_line, _ = _clean_line(line_buffer, previous_blank)
        if cleaned_line:
            yield cleaned_line


def clean_text(text: str) -> str:
    """规范换行、空白和不可见字符，同时保留 Markdown 标题等语义文字。"""

    # 空输入直接返回空字符串，避免后续无意义的处理。
    if not text:
        return ""

    # 复用流式实现；测试和小文本场景才会在这里把结果拼成一个字符串。
    # 再次 strip 去掉整个文档两端由流式换行产生的空白。
    return "".join(iter_clean_text([text])).strip()
