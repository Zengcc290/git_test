"""按段落和长度切分文档。"""

from collections.abc import Iterable, Iterator

# Chunk 是分段结果的数据结构。
from .models import Chunk


def _find_stream_split_end(text: str, chunk_size: int) -> int:
    """在流式缓存的前 chunk_size 个字符中寻找较自然的切分点。"""

    hard_end = min(len(text), chunk_size)
    if hard_end == len(text):
        return hard_end

    # 只在窗口后半段寻找边界，避免产生过短的分段。
    minimum_boundary = max(1, int(chunk_size * 0.55))
    candidates = [
        text.rfind(mark, minimum_boundary, hard_end)
        for mark in "。！？.!?；;，,\n"
    ]
    boundary = max(candidates, default=-1)
    if boundary >= minimum_boundary:
        return boundary + 1

    # 没有标点时，尽量在空格处切开；中文连续文本会退化为硬切分。
    whitespace = text.rfind(" ", minimum_boundary, hard_end)
    return whitespace if whitespace > 0 else hard_end


def iter_chunk_text(
    text_chunks: Iterable[str],
    chunk_size: int = 800,
    overlap: int = 100,
) -> Iterator[Chunk]:
    """把文本块流式切分为 Chunk，内存中最多保留一个窗口及其重叠部分。"""

    # 与 chunk_text 保持相同的参数约束，避免两套实现行为不一致。
    if chunk_size <= 0:
        raise ValueError("chunk_size 必须大于 0")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap 必须满足 0 <= overlap < chunk_size")

    # buffer 是唯一的文本缓存，不会随着整个文件大小无限增长。
    buffer = ""
    chunk_index = 0
    for text_chunk in text_chunks:
        if not text_chunk:
            continue
        buffer += text_chunk

        # 输入块到达后尽快产出完整分段，避免继续累积。
        while len(buffer) > chunk_size:
            end = _find_stream_split_end(buffer, chunk_size)
            content = buffer[:end].strip()
            if content:
                yield Chunk(index=chunk_index, content=content)
                chunk_index += 1

            # 保留尾部 overlap 个字符，让相邻分段共享少量上下文。
            next_start = max(end - overlap, 1)
            buffer = buffer[next_start:]

    # 文件结束后输出最后一个不足目标长度的分段。
    if buffer.strip():
        yield Chunk(index=chunk_index, content=buffer.strip())


def chunk_text(text: str, chunk_size: int = 800, overlap: int = 100) -> list[Chunk]:
    """兼容小文本调用，并复用流式实现保证相邻分段始终保留重叠。"""

    # [text] 只包装调用者已经提供的这段文本；大文件索引路径使用 iter_chunk_text。
    return list(iter_chunk_text([text], chunk_size=chunk_size, overlap=overlap))
