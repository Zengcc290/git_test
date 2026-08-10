"""FTS 查询转义和搜索结果高亮。"""

# re 同时用于拆分查询词和构造安全的高亮正则表达式。
import re


def query_terms(query: str) -> list[str]:
    """提取用于高亮的查询词，支持简单的双引号短语。"""

    # 使用列表而不是 set，保证高亮和兜底 LIKE 查询保持用户输入顺序。
    terms: list[str] = []
    # 双引号内容作为一个短语，其余内容按空白拆成普通关键词。
    for quoted, bare in re.findall(r'"([^"]+)"|(\S+)', query.strip()):
        term = quoted or bare
        # 去掉残留引号，并过滤空字符串。
        term = term.strip().strip('"')
        if term and term not in terms:
            # 去重可以避免重复生成相同的 FTS 条件和高亮结果。
            terms.append(term)
    return terms


def to_fts_query(query: str) -> str:
    """将普通关键词转换成安全的 FTS5 AND 查询，避免用户输入破坏 MATCH 语法。"""

    # 先复用统一的查询词解析逻辑，保证搜索与高亮使用相同词项。
    terms = query_terms(query)
    if not terms:
        raise ValueError("搜索关键词不能为空")
    # FTS5 的双引号可以把每个词作为字面量处理；内部引号需要重复转义。
    return " AND ".join(f'"{term.replace(chr(34), chr(34) * 2)}"' for term in terms)


def highlight_text(
    text: str,
    query: str,
    prefix: str = "<mark>",
    suffix: str = "</mark>",
) -> str:
    """高亮文本中命中的词；最长的词优先，避免短词切断长词。"""

    # 长词优先匹配，避免先匹配短词后破坏长短语的完整高亮。
    terms = sorted(query_terms(query), key=len, reverse=True)
    if not terms:
        # 空查询不应该改变原文。
        return text
    # re.escape 防止关键词中的特殊字符被当作正则表达式语法。
    pattern = re.compile("|".join(re.escape(term) for term in terms), re.IGNORECASE)
    # 用回调保留原始命中文本的大小写，只在两侧增加标记。
    return pattern.sub(lambda match: f"{prefix}{match.group(0)}{suffix}", text)
