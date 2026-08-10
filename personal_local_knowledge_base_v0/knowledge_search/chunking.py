"""按段落和长度切分文档。"""

# re 用于识别由空行分隔的自然段。
import re

# Chunk 是分段结果的数据结构。
from .models import Chunk


def _split_long_paragraph(text: str, chunk_size: int, overlap: int) -> list[str]:
    # 用列表收集最终片段，避免在循环中频繁拼接长字符串。
    parts: list[str] = []
    # start 表示当前窗口在段落中的起始位置。
    start = 0
    # 只有当边界位于窗口后半段时才采用它，避免产生过短片段。
    minimum_boundary = max(1, int(chunk_size * 0.55))

    while start < len(text):
        # 先按最大长度确定硬上限，保证分段不会无限增长。
        hard_end = min(len(text), start + chunk_size)
        end = hard_end
        if hard_end < len(text):
            # 在硬上限之前寻找中英文标点或换行作为更自然的切分点。
            candidates = [
                text.rfind(mark, start + minimum_boundary, hard_end)
                for mark in "。！？.!?；;，,\n"
            ]
            # 选择最靠后的有效标点，这样可以最大化当前片段的信息量。
            boundary = max(candidates, default=-1)
            if boundary >= start + minimum_boundary:
                # +1 让标点留在当前分段末尾，而不是丢失。
                end = boundary + 1
            else:
                # 没找到合适标点时，退化为按空格切分。
                whitespace = text.rfind(" ", start + minimum_boundary, hard_end)
                if whitespace > start:
                    end = whitespace

        # strip 防止边界切分带来首尾空白。
        part = text[start:end].strip()
        if part:
            parts.append(part)
        if end >= len(text):
            # 已经处理到段落末尾，结束窗口循环。
            break

        # 下一段从当前段末尾向前回退 overlap 个字符，保留上下文。
        next_start = max(end - overlap, start + 1)
        # 避免重叠窗口从空白字符中间开始。
        while next_start < len(text) and text[next_start].isspace():
            next_start += 1
        start = next_start

    # 返回纯文本片段，编号由外层统一生成。
    return parts


def chunk_text(text: str, chunk_size: int = 800, overlap: int = 100) -> list[Chunk]:
    """优先按空行分段，超长段落再按边界切分，并保留少量重叠上下文。"""

    # 校验参数，避免出现负长度窗口或无法前进的重叠窗口。
    if chunk_size <= 0:
        raise ValueError("chunk_size 必须大于 0")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap 必须满足 0 <= overlap < chunk_size")
    # 空文档没有可供检索的分段。
    if not text or not text.strip():
        return []

    # 空行是最可靠的段落边界，先用它保留原始结构。
    paragraphs = [
        paragraph.strip()
        for paragraph in re.split(r"\n\s*\n", text.strip())
        if paragraph.strip()
    ]

    # contents 保存最终片段；current 暂存可以合并到同一片段的短段落。
    contents: list[str] = []
    current: list[str] = []
    # current_length 用于判断继续合并是否会超过目标长度。
    current_length = 0

    def flush() -> None:
        # 声明要修改外层闭包中的暂存变量。
        nonlocal current, current_length
        if current:
            # 用两个换行恢复段落之间的视觉分隔。
            contents.append("\n\n".join(current))
            # 清空暂存区，准备收集下一组段落。
            current = []
            current_length = 0

    for paragraph in paragraphs:
        if len(paragraph) > chunk_size:
            # 超长段落不能和其他段落混合，先提交已有短段落。
            flush()
            # 对超长段落执行带重叠的边界切分。
            contents.extend(_split_long_paragraph(paragraph, chunk_size, overlap))
            continue

        # 计算把当前自然段加入暂存区后的长度，2 代表段落分隔的两个换行。
        proposed_length = current_length + len(paragraph) + (2 if current else 0)
        if current and proposed_length > chunk_size:
            # 超过目标长度时，先输出已有内容，再从当前段落重新开始。
            flush()
        current.append(paragraph)
        # 更新暂存区长度；第一个段落不需要额外的分隔长度。
        current_length += len(paragraph) + (2 if len(current) > 1 else 0)

    # 循环结束后不要遗忘最后一组暂存段落。
    flush()
    # 根据输出顺序生成稳定的、从 0 开始的分段编号。
    return [Chunk(index=index, content=content) for index, content in enumerate(contents)]
