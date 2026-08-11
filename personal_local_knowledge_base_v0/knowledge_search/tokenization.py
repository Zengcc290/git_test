"""中文搜索词生成和 jieba 相关的 FTS5 查询构造。"""

from __future__ import annotations

import logging
from collections.abc import Iterator

from .highlighting import query_terms


logger = logging.getLogger(__name__)


def _fallback_tokens(text: str) -> Iterator[str]:
    """jieba 不可用时，按英文单词和单个中文字符提供最低限度兜底。"""

    current = []
    for char in text:
        # 连续 ASCII 字母/数字/下划线作为一个词保留。
        if char.isascii() and (char.isalnum() or char == "_"):
            current.append(char)
            continue
        if current:
            yield "".join(current)
            current = []
        # 中文单字虽然不如 jieba 准确，但可以避免整个中文查询完全失效。
        if "\u4e00" <= char <= "\u9fff":
            yield char
    if current:
        yield "".join(current)


def tokenize_for_search(text: str) -> list[str]:
    """优先使用 jieba 搜索模式切词，并去除空白和纯标点词。"""

    if not text or not text.strip():
        return []

    try:
        # cut_for_search 会对长词做更细的切分，适合召回关键词搜索结果。
        import jieba

        candidates = jieba.cut_for_search(text, HMM=True)
    except ImportError:  # pragma: no cover - requirements 会安装 jieba
        logger.warning("jieba 未安装，使用字符级搜索分词兜底")
        candidates = _fallback_tokens(text)

    tokens: list[str] = []
    for candidate in candidates:
        token = candidate.strip()
        if not token:
            continue
        # 过滤纯标点，避免生成无意义的 FTS5 条件。
        if not any(char.isalnum() or "\u4e00" <= char <= "\u9fff" for char in token):
            continue
        if token not in tokens:
            tokens.append(token)
    return tokens


def to_token_fts_query(query: str) -> str:
    """把 jieba 词项转换为安全的 FTS5 AND 查询。"""

    # 先按引号和空格解析用户查询，再对每个查询片段进行中文分词。
    source = " ".join(query_terms(query))
    tokens = tokenize_for_search(source)
    if not tokens:
        return ""
    # 双引号保证标点或特殊字符不会改变 MATCH 语法。
    return " AND ".join(f'"{token.replace(chr(34), chr(34) * 2)}"' for token in tokens)

