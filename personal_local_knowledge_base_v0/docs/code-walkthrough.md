# 项目代码逐行解析（Code Walkthrough）

本文档对 `personal_local_knowledge_base_v0` 项目的全部 Python 代码做逐行解析，覆盖核心包 `knowledge_search/`、RAG 子包、命令行入口、`scripts/` 脚本以及 `tests/` 测试。目标是让每一行代码的意图、输入输出和它在整体数据流中的位置都清晰可查。

## 目录

- [整体架构与数据流](#整体架构与数据流)
- [第一部分：包入口](#第一部分包入口)
- [第二部分：数据模型 `models.py`](#第二部分数据模型-modelspy)
- [第三部分：日志配置 `logging_config.py`](#第三部分日志配置-logging_configpy)
- [第四部分：查询转义与高亮 `highlighting.py`](#第四部分查询转义与高亮-highlightingpy)
- [第五部分：中文分词 `tokenization.py`](#第五部分中文分词-tokenizationpy)
- [第六部分：文本清洗 `cleaning.py`](#第六部分文本清洗-cleaningpy)
- [第七部分：文本分段 `chunking.py`](#第七部分文本分段-chunkingpy)
- [第八部分：SQLite 与 FTS5 `database.py`](#第八部分sqlite-与-fts5-databasepy)
- [第九部分：文件发现与增量索引 `indexer.py`](#第九部分文件发现与增量索引-indexerpy)
- [第十部分：文档抽取 `extractors.py`](#第十部分文档抽取-extractorspy)
- [第十一部分：JSON 流式解析 `json_parser.py`](#第十一部分json-流式解析-json_parserpy)
- [第十二部分：RAG Prompt `rag/prompt.py`](#第十二部分rag-prompt-ragpromptpy)
- [第十三部分：LLM 客户端 `rag/llm_client.py`](#第十三部分llm-客户端-ragllm_clientpy)
- [第十四部分：检索器 `rag/retriever.py`](#第十四部分检索器-ragretrieverpy)
- [第十五部分：回答编排 `rag/answer.py` 与 `rag/__init__.py`](#第十五部分回答编排-raganswerpy-与-rag__init__py)
- [第十六部分：命令行入口 `cli.py`](#第十六部分命令行入口-clipy)
- [第十七部分：scripts 脚本](#第十七部分scripts-脚本)
- [第十八部分：tests 测试](#第十八部分tests-测试)

## 整体架构与数据流

项目是一个本地知识库工具，核心链路分两条：

**索引链路（写入）**

```text
文件/目录输入
  → discover_files() 发现候选文件（排除、去重、数量上限）
  → extract_document() 计算 SHA-256 与元数据
  → iter_document_text() 流式抽取正文（TXT/MD 分块、PDF 分页、PPTX 分片、JSON 逐记录）
  → iter_clean_text() 流式清洗（Unicode 规范化、换行统一、空白压缩）
  → iter_chunk_text() 流式分段（段落优先，超长按标点切分 + 重叠）
  → KnowledgeBase.replace_document() 写入 SQLite + 两套 FTS5 索引
```

**检索链路（读取）**

```text
查询字符串
  → to_token_fts_query()（jieba 中文词索引）优先
  → to_fts_query()（原始文本 FTS5）兜底
  → 参数化 LIKE 最后兜底（仅中文）
  → 结果按 bm25 排序 + 程序侧高亮
```

**RAG 链路（问答）**

```text
问题
  → KeywordRetriever.retrieve()（关键词检索 + 相邻分段窗口 + 字符预算）
  → build_messages()（严格 Prompt）
  → LLMClient.complete()（[OI] 兼容 HTTP 调用）
  → _validate_citations()（引用越界/缺失校验）
  → AnswerResult + RAG_RECORD 日志
```

分层职责：`models.py` 只定义数据结构；`database.py` 负责持久化与搜索；`indexer.py` 编排文件发现与流水线；`extractors.py` / `json_parser.py` 负责把各种文件变成文本块；`cleaning.py` / `chunking.py` 负责文本规范化与切分；`rag/` 负责检索增强问答；`cli.py` 负责参数与输出。

---

## 第一部分：包入口

### `knowledge_search/__init__.py`

```python
"""个人本地知识库搜索工具 V2。"""
```

**第 1 行**：模块级 docstring。包被导入时可通过 `knowledge_search.__doc__` 读取，描述包的用途。这也是一个空模块能被识别为「文档化包」的惯例。

```python
# 统一维护项目版本号，便于 README、打包配置和运行时读取。
__version__ = "0.2.0"
```

**第 2 行**：注释，说明 `__version__` 存在的目的——单一事实来源，避免 README、`pyproject.toml`、代码各处版本号不一致。

**第 3 行**：定义包的公开版本号字符串。`import knowledge_search` 后可用 `knowledge_search.__version__` 获取。注意 `pyproject.toml` 中 `version = "0.2.0"` 与此一致，但二者是**手动**保持同步的，当前没有从包读取版本的自动机制（可改进点）。

**作用**：把 `knowledge_search/` 目录标识为可导入的 Python 包，并暴露版本号。

### `knowledge_search/__main__.py`

```python
# 从 CLI 模块导入真正的命令行处理函数。
from .cli import main
```

**第 1 行**：注释，说明导入 `main` 的原因——CLI 逻辑集中在 `cli.py`，这里只是入口转发，避免逻辑散落。

**第 2 行**：相对导入（`.` 代表当前包 `knowledge_search`），从 `cli.py` 引入 `main` 函数。

```python
# 只有使用 ``python -m knowledge_search`` 运行包时，才执行 CLI。
if __name__ == "__main__":
```

**第 3 行**：注释，解释入口守卫的语义。

**第 4 行**：Python 入口守卫。用 `python -m knowledge_search` 运行时，Python 把本模块当作「主模块」，`__name__` 被设为 `"__main__"`，条件成立；若包被 `import knowledge_search` 导入，`__name__` 是 `"knowledge_search.__main__"`，条件不成立，不执行 CLI。这样既能作为模块导入，又能作为命令运行。

```python
    # 将 main 返回的状态码交给操作系统，方便脚本判断命令是否成功。
    raise SystemExit(main())
```

**第 5 行**：注释，说明 `SystemExit` 的用途。

**第 6 行**：调用 `main()` 得到整数退出码，用 `SystemExit` 异常把退出码传给操作系统。等价于 `sys.exit(main())`，但免去额外 `import sys`。退出码 0 表示成功，非 0 表示失败，供 shell `$?` / PowerShell `$LASTEXITCODE` 判断。

**作用**：让 `python -m knowledge_search ...` 真正可运行，并把状态码返回给调用者。

---

## 第二部分：数据模型 `models.py`

```python
# dataclass 用来定义轻量的数据对象，避免手写初始化和比较逻辑。
from dataclasses import dataclass
# Path 用于表达源文件路径，并提供跨平台的路径操作。
from pathlib import Path
```

**第 1 行**：注释，说明 `dataclass` 的引入理由。

**第 2 行**：从标准库导入 `dataclass` 装饰器。用它声明类后，会自动生成 `__init__`、`__repr__`、`__eq__` 等方法，减少样板代码。

**第 3 行**：注释。

**第 4 行**：导入 `pathlib.Path`，用于以面向对象方式表达文件路径。

### `ExtractedDocument`（第 7-24 行）

```python
@dataclass(frozen=True)
class ExtractedDocument:
    """已从文件中读取出的原始文档及其文件元数据。"""
```

**第 7 行**：`@dataclass(frozen=True)` 使实例不可变（字段不能重新赋值），适合作为贯穿索引链路的「只读数据载体」，避免意外修改。

**第 8 行**：类定义。

**第 9 行**：类 docstring。

```python
    path: Path
    file_type: str
    text: str | None
    sha256: str
    size: int
    modified_ns: int
    parser_fingerprint: str = ""
```

**第 11 行**：`path` 字段，规范化的绝对源文件路径，也是数据库 `documents.path` 的唯一标识。

**第 12 行**：`file_type`，如 `txt`、`md`、`pdf`、`pptx`、`json`。

**第 13 行**：`text`，兼容旧接口的全文字段。实际文件抽取时为 `None`（正文由流式迭代器延迟读取），测试中手工构造对象时可直接填字符串。类型 `str | None` 是 Python 3.10+ 语法。

**第 14 行**：`sha256`，原始文件内容的 SHA-256 十六进制串，用于增量索引判断「文件是否变化」。

**第 15 行**：`size`，文件字节大小。

**第 16 行**：`modified_ns`，文件最后修改时间的纳秒表示（`st_mtime_ns`）。

**第 17 行**：`parser_fingerprint`，解析配置指纹，默认空字符串。普通文档为空；JSON 配置变化时此值改变，用于触发重新索引。

### `Chunk`（第 27-36 行）

```python
@dataclass(frozen=True)
class Chunk:
    """文档被切分后的一个可检索片段。"""
    index: int
    content: str
    start_offset: int = 0
```

**第 29 行**：`index`，文档内连续分段编号，从 0 开始。

**第 30 行**：`content`，写入 SQLite 和 FTS5 的实际文本。

**第 31 行**：`start_offset`，分段在原文中的起始偏移，默认 0。当前版本保留字段但未真正使用（见 docstring 注释「V0 暂时保留字段」）。

### `SearchResult`（第 39-58 行）

```python
@dataclass(frozen=True)
class SearchResult:
    """一条搜索命中。score 使用 SQLite FTS5 的 bm25 分数。"""
    chunk_id: int
    document_path: str
    filename: str
    file_type: str
    chunk_index: int
    content: str
    score: float
    highlighted_content: str
```

**第 42 行**：`chunk_id`，`chunks` 表主键。

**第 43 行**：`document_path`，命中文档绝对路径（字符串）。

**第 44 行**：`filename`，不含目录的显示名。

**第 45 行**：`file_type`，扩展名类型。

**第 46 行**：`chunk_index`，分段编号。

**第 47 行**：`content`，未加高亮标记的原始分段文本。

**第 48 行**：`score`，FTS5 `bm25()` 分数，越小通常越相关（本项目排序用 `ORDER BY score ASC`）。

**第 49 行**：`highlighted_content`，加了 `<mark>`/`[[...]]`/ANSI 标记后的文本，供程序或测试使用。

### `DocumentInfo`（第 61-71 行）

```python
@dataclass(frozen=True)
class DocumentInfo:
    """已索引文档及其可管理的统计信息。"""
    document_id: int
    path: str
    filename: str
    file_type: str
    size: int
    chunk_count: int
    indexed_at: str
```

这是 `list` / `prune` 命令展示文档元数据的载体。各字段含义：`document_id`（数据库主键）、`path`（绝对路径字符串）、`filename`、`file_type`、`size`（字节）、`chunk_count`（分段数）、`indexed_at`（索引时间戳字符串）。

### `DatabaseHealth`（第 74-87 行）

```python
@dataclass(frozen=True)
class DatabaseHealth:
    """数据库一致性检查结果。"""
    document_count: int
    chunk_count: int
    chunks_fts_count: int
    chunk_tokens_count: int
    chunks_fts_jieba_count: int
    issues: tuple[str, ...] = ()

    @property
    def healthy(self) -> bool:
        return not self.issues
```

**第 78-83 行**：五个计数 + `issues` 元组。`issues` 默认为空元组。

**第 85-87 行**：`healthy` 是只读属性，`not self.issues` 表示「没有发现问题」即为健康。空元组为假值，所以有 `issues` 时返回 `False`。

### `IndexProgress`（第 90-101 行）

```python
@dataclass(frozen=True)
class IndexProgress:
    """索引器发出的单文件进度事件。"""
    current: int
    total: int
    path: Path
    status: str
```

**第 94 行**：`current`，本次任务中的文件序号，从 1 开始。

**第 95 行**：`total`，本次纳入处理的文件总数。

**第 96 行**：`path`，正在处理/刚处理完的文件路径。

**第 97 行**：`status`，取值 `processing` / `indexed` / `skipped` / `empty` / `oversized` / `failed`。

### `IndexStats`（第 104-117 行）

```python
@dataclass
class IndexStats:
    files_found: int = 0
    indexed: int = 0
    skipped: int = 0
    empty: int = 0
    failed: int = 0
    oversized: int = 0
```

注意这里**没有** `frozen=True`，因为它需要被索引器逐步累加（可变）。各字段是本次索引的汇总计数：发现数、新增/更新数、跳过数、空文本数、失败数、超大 JSON 数。

---

## 第三部分：日志配置 `logging_config.py`

```python
"""统一日志配置。"""
from __future__ import annotations

import logging
import sys
from pathlib import Path
```

**第 1 行**：模块 docstring。

**第 2 行**：`from __future__ import annotations`，让所有类型注解惰性求值（以字符串形式存储），使 `Path | None` 等 3.10+ 语法在注解位置也能向前兼容。

**第 4 行**：导入标准库 `logging`。

**第 5 行**：导入 `sys`，用于访问 `sys.stderr`。

**第 6 行**：导入 `Path`。

```python
def configure_logging(level: str = "INFO", log_file: Path | None = None) -> None:
    # 控制台日志使用 stderr，避免污染 CLI 的正常结果输出。
    handlers: list[logging.Handler] = [logging.StreamHandler(sys.stderr)]
```

**第 10 行**：函数定义。`level` 默认 `"INFO"`，`log_file` 可选。

**第 11 行**：注释，解释为何日志走 `stderr` 而非 `stdout`：CLI 的正常结果（搜索结果、统计等）走 stdout，日志若混入会污染脚本重定向输出。

**第 12 行**：初始化 handler 列表，第一个是 `StreamHandler(sys.stderr)`，把日志写到标准错误流。

```python
    if log_file is not None:
        # 日志目录可能还不存在，因此先创建父目录。
        log_file.parent.mkdir(parents=True, exist_ok=True)
        # 使用 UTF-8 写入文件，保证中文日志可读。
        handlers.append(logging.FileHandler(log_file, encoding="utf-8"))
```

**第 13-16 行**：若指定了日志文件，先 `mkdir(parents=True, exist_ok=True)` 创建父目录（幂等，不存在才创建），再追加一个 `FileHandler`，用 UTF-8 编码写文件，保证中文不乱码。

```python
    # force=True 可以覆盖 unittest 或重复调用遗留的旧日志配置。
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=handlers,
        force=True,
    )
```

**第 18 行**：注释。

**第 19-24 行**：`logging.basicConfig(...)` 做全局根日志配置：

- `level`：`getattr(logging, level.upper(), logging.INFO)` 把字符串 `"INFO"` 转成整数常量 `logging.INFO`；若传入未知级别字符串，`getattr` 的第三个参数 `logging.INFO` 作为默认值兜底（`logging.INFO` 也是整数 20，与 `getattr` 默认参数逻辑一致，此处默认值恰好是 INFO 级别）。
- `format`：每条日志含时间、级别、模块名（logger name）、消息正文。
- `handlers`：使用上面构造的 handler 列表，替代默认 stderr handler。
- `force=True`：强制移除 root logger 上已有的 handler 再重新配置，避免 unittest 或重复调用时残留旧 handler 导致日志重复或级别错乱。

**作用**：统一配置日志的输出位置、级别和格式。CLI 的 `_run` 会在命令开始时先调用它。

---

## 第四部分：查询转义与高亮 `highlighting.py`

```python
"""FTS 查询转义和搜索结果高亮。"""
import re
```

**第 1 行**：docstring。

**第 2 行**：导入 `re`，用于拆分查询词和构造高亮正则。

### `query_terms`（第 7-20 行）

```python
def query_terms(query: str) -> list[str]:
    """提取用于高亮的查询词，支持简单的双引号短语。"""
    terms: list[str] = []
    for quoted, bare in re.findall(r'"([^"]+)"|(\S+)', query.strip()):
        term = quoted or bare
        term = term.strip().strip('"')
        if term and term not in terms:
            terms.append(term)
    return terms
```

**第 9 行**：初始化结果列表（用 list 而非 set，保证顺序稳定，与用户输入顺序一致）。

**第 11 行**：正则 `r'"([^"]+)"|(\S+)'` 用 `re.findall` 同时匹配「双引号包裹的短语」和「非空白字符组成的词」。`findall` 对有两个捕获组时返回元组列表，每个元组 `(quoted, bare)` 中恰好一个非空。`query.strip()` 先去掉首尾空白。

**第 12 行**：`quoted or bare` 取非空的那一个。

**第 13 行**：`strip()` 去掉首尾空白，再 `.strip('"')` 去掉残留引号。

**第 14-15 行**：过滤空字符串并去重（`term not in terms` 才追加），保持首次出现顺序。

**第 16 行**：返回词项列表。

### `to_fts_query`（第 23-31 行）

```python
def to_fts_query(query: str) -> str:
    """将普通关键词转换成安全的 FTS5 AND 查询，避免用户输入破坏 MATCH 语法。"""
    terms = query_terms(query)
    if not terms:
        raise ValueError("搜索关键词不能为空")
    return " AND ".join(f'"{term.replace(chr(34), chr(34) * 2)}"' for term in terms)
```

**第 25 行**：复用 `query_terms` 提取词项。

**第 26-27 行**：无词项（空查询）抛 `ValueError`。

**第 28 行**：把每个词用双引号包裹，词项之间用 ` AND ` 连接。这是 FTS5 的「短语 + AND」语法：

- 双引号 `"..."` 表示该词作为字面短语匹配（phrase query）。
- 内部引号需要转义：FTS5 中字符串字面量里的 `"` 要写成 `""`。`chr(34)` 是双引号 `"`，`chr(34) * 2` 是 `""`，即把一个 `"` 替换成两个 `"`。

**作用**：把用户输入安全转成 FTS5 MATCH 表达式，避免用户输入 `OR`、`*`、括号等破坏查询语法（注入防御）。

### `highlight_text`（第 34-49 行）

```python
def highlight_text(
    text: str,
    query: str,
    prefix: str = "<mark>",
    suffix: str = "</mark>",
) -> str:
    """高亮文本中命中的词；最长的词优先，避免短词切断长词。"""
    terms = sorted(query_terms(query), key=len, reverse=True)
    if not terms:
        return text
    pattern = re.compile("|".join(re.escape(term) for term in terms), re.IGNORECASE)
    return pattern.sub(lambda match: f"{prefix}{match.group(0)}{suffix}", text)
```

**第 38 行**：`prefix` / `suffix` 默认 `<mark>` / `</mark>`，调用方可换成 `[[` / `]]` 或 ANSI 颜色码。

**第 41 行**：按词长度降序排序。因为正则用 `|` 交替，长的先出现可避免短词先命中截断长词（例如「SQLite」先于「SQL」匹配）。

**第 42-43 行**：空查询直接返回原文。

**第 44 行**：`re.escape(term)` 转义每个词里的正则特殊字符，再用 `|` 连接成一个大交替正则，`re.IGNORECASE` 忽略大小写。

**第 45 行**：`pattern.sub` 用回调把每个命中包裹上前缀后缀。`match.group(0)` 是命中的原始文本（保留原文大小写），所以高亮不改变原文大小写。

**作用**：程序侧高亮，与 SQLite 的 `highlight()` 辅助函数不同，这里在 Python 里完成，便于 CLI 灵活切换高亮样式。

---

## 第五部分：中文分词 `tokenization.py`

```python
"""中文搜索词生成和 jieba 相关的 FTS5 查询构造。"""
from __future__ import annotations

import logging
from collections.abc import Iterator

from .highlighting import query_terms
```

**第 5 行**：导入 `logging` 用于 jieba 不可用时的警告。

**第 6 行**：导入 `Iterator` 类型。

**第 8 行**：相对导入 `query_terms`，复用查询词解析。

```python
logger = logging.getLogger(__name__)
```

**第 11 行**：创建模块级 logger，名字是 `knowledge_search.tokenization`。

### `_fallback_tokens`（第 14-30 行）

```python
def _fallback_tokens(text: str) -> Iterator[str]:
    """jieba 不可用时，按英文单词和单个中文字符提供最低限度兜底。"""
    current = []
    for char in text:
        if char.isascii() and (char.isalnum() or char == "_"):
            current.append(char)
            continue
        if current:
            yield "".join(current)
            current = []
        if "\u4e00" <= char <= "\u9fff":
            yield char
    if current:
        yield "".join(current)
```

**第 16 行**：`current` 累积连续的 ASCII 字母数字下划线。

**第 17-24 行**：遍历每个字符：

- 若是 ASCII 且是字母/数字/下划线（`isalnum()` 或 `_`），追加到 `current`，`continue` 跳到下一字符。
- 否则（遇到非英文词字符），若 `current` 有累积内容，先 `yield` 出这个英文单词，并清空 `current`。

**第 25-26 行**：若字符是中文字符（Unicode 码位 `\u4e00`-`\u9fff`），`yield` 单个汉字。这是「字符级」兜底：中文没法分词时按单字处理，避免整个中文查询完全失效。

**第 28-29 行**：循环结束后，若 `current` 还有未输出的英文单词，输出它。

**作用**：jieba 缺失时的降级分词，保证程序仍能运行。

### `tokenize_for_search`（第 33-58 行）

```python
def tokenize_for_search(text: str) -> list[str]:
    """优先使用 jieba 搜索模式切词，并去除空白和纯标点词。"""
    if not text or not text.strip():
        return []

    try:
        import jieba
        candidates = jieba.cut_for_search(text, HMM=True)
    except ImportError:
        logger.warning("jieba 未安装，使用字符级搜索分词兜底")
        candidates = _fallback_tokens(text)
```

**第 36-37 行**：空/纯空白输入直接返回空列表。

**第 39-45 行**：`try` 里延迟导入 jieba（`cut_for_search` 是搜索模式，对长词做更细切分，利于召回）。若 `ImportError`，记录警告并改用字符级兜底。

```python
    tokens: list[str] = []
    for candidate in candidates:
        token = candidate.strip()
        if not token:
            continue
        if not any(char.isalnum() or "\u4e00" <= char <= "\u9fff" for char in token):
            continue
        if token not in tokens:
            tokens.append(token)
    return tokens
```

**第 47-55 行**：遍历分词候选，`strip()` 去空白；过滤空词；过滤「纯标点词」（不含字母数字或中文字符的词）；去重（保持顺序）。返回去重后的词列表。

### `to_token_fts_query`（第 61-70 行）

```python
def to_token_fts_query(query: str) -> str:
    """把 jieba 词项转换为安全的 FTS5 AND 查询。"""
    source = " ".join(query_terms(query))
    tokens = tokenize_for_search(source)
    if not tokens:
        return ""
    return " AND ".join(f'"{token.replace(chr(34), chr(34) * 2)}"' for token in tokens)
```

**第 63 行**：先用 `query_terms` 按引号/空格拆出片段，再 `" ".join` 拼回，这样「引号短语」语义被规范化。

**第 64 行**：对拼回后的字符串做 jieba 分词。

**第 65-66 行**：无词项返回空字符串（由调用方 `search` 判断是否走兜底）。

**第 67 行**：与 `to_fts_query` 相同，把每个 jieba 词转成带双引号的 AND 短语查询，引号转义。

**作用**：把用户查询转成针对 `chunks_fts_jieba`（中文词索引表）的 FTS5 查询。

---

## 第六部分：文本清洗 `cleaning.py`

```python
"""输入文本清洗。"""
import re
import unicodedata
from collections.abc import Iterable, Iterator
```

**第 2 行**：`re` 用于压缩连续空格和制表符。

**第 3 行**：`unicodedata` 用于 Unicode 规范化，把等价字符（如全角/组合字符）统一成标准形式，避免检索时出现重复形式。

**第 4 行**：导入 `Iterable`、`Iterator` 类型。

### `_clean_line`（第 10-19 行）

```python
def _clean_line(raw_line: str, previous_blank: bool) -> tuple[str, bool]:
    """清洗一行文字，并返回清洗结果和新的空行状态。"""
    line = re.sub(r"[ \t]+", " ", raw_line).strip()
    if not line:
        return ("" if previous_blank else "\n", True)
    return line + "\n", False
```

**第 12 行**：`re.sub(r"[ \t]+", " ", raw_line)` 把一行内连续的一个或多个空格/制表符压缩成单个空格；`.strip()` 去掉行首尾空白。

**第 13-14 行**：若清洗后是空行：

- 返回 `("" if previous_blank else "\n", True)`——连续空行只保留第一个（用 `previous_blank` 状态判断），否则输出一个换行符 `\n`。`\n` 是流式输出中的段落分隔符。第二个返回值 `True` 表示「当前行是空行」，供下一行判断。

**第 15 行**：非空行返回 `line + "\n"`（补换行，方便下游识别段落边界），第二个返回值 `False` 表示当前非空。

**作用**：单行清洗 + 空行去重的核心单元。

### `iter_clean_text`（第 22-69 行）

```python
def iter_clean_text(
    text_chunks: Iterable[str],
    *,
    max_pending: int = 64 * 1024,
) -> Iterator[str]:
    """逐块清洗文本，保证待处理缓存不会随文件总大小增长。"""
    line_buffer = ""
    previous_blank = False
```

**第 29 行**：`line_buffer` 只保存当前尚未遇到换行符的残余内容（半行）。

**第 30 行**：`previous_blank` 记录上一行是否为空，用于压缩连续空行。

```python
    for text_chunk in text_chunks:
        if not text_chunk:
            continue

        normalized = unicodedata.normalize("NFC", text_chunk)
        normalized = normalized.replace("\ufeff", "").replace("\x00", "")
        normalized = normalized.replace("\r\n", "\n").replace("\r", "\n")
        line_buffer += normalized
```

**第 34-36 行**：跳过空块。

**第 38 行**：`unicodedata.normalize("NFC", ...)` 用 NFC 组合形式统一 Unicode 等价字符。

**第 39 行**：`.replace("\ufeff", "")` 去掉 UTF-8 BOM 字符；`.replace("\x00", "")` 去掉空字节（常见于二进制或损坏文本）。

**第 40 行**：把 Windows 换行 `\r\n` 和 Mac 换行 `\r` 统一成 `\n`。

**第 41 行**：把规范化后的块追加到 `line_buffer`。

```python
        lines = line_buffer.split("\n")
        line_buffer = lines.pop()
        for raw_line in lines:
            cleaned_line, previous_blank = _clean_line(raw_line, previous_blank)
            if cleaned_line:
                yield cleaned_line
```

**第 43 行**：按 `\n` 切分。

**第 44 行**：`lines.pop()` 取出最后一个元素（可能是没有换行符结尾的「半行」），保留在 `line_buffer` 等待下一块拼接。

**第 45-48 行**：遍历完整行，逐行清洗；若清洗结果非空，`yield` 出去（生成器惰性输出，不累积整文件）。

```python
        while len(line_buffer) > max_pending:
            split_at = line_buffer.rfind(" ", 0, max_pending)
            if split_at <= 0:
                split_at = max_pending
            raw_piece = line_buffer[:split_at]
            line_buffer = line_buffer[split_at:]
            cleaned_piece = re.sub(r"[ \t]+", " ", raw_piece).strip()
            if cleaned_piece:
                yield cleaned_piece + " "
                previous_blank = False
```

**第 52-63 行**：极端情况处理——如果某一行（没有换行符）比整个输入块还大，`line_buffer` 会无限增长。当 `len(line_buffer) > max_pending`（默认 64KB）时：

- `rfind(" ", 0, max_pending)` 在 `max_pending` 之前找最后一个空格作为切分点；找不到（`<= 0`）就用 `max_pending` 硬切。
- 切出 `raw_piece` 并更新 `line_buffer` 为剩余部分。
- 清洗切出的片段；若非空，`yield cleaned_piece + " "`（补一个空格而非换行，避免把一行误拆成两个段落），并置 `previous_blank = False`。

```python
    if line_buffer:
        cleaned_line, _ = _clean_line(line_buffer, previous_blank)
        if cleaned_line:
            yield cleaned_line
```

**第 65-69 行**：文件结尾可能没有换行符，最后的残余也必须清洗并输出。忽略返回的 `previous_blank` 状态（用 `_` 接住），因为后面没有更多行。

### `clean_text`（第 72-81 行）

```python
def clean_text(text: str) -> str:
    """规范换行、空白和不可见字符，同时保留 Markdown 标题等语义文字。"""
    if not text:
        return ""
    return "".join(iter_clean_text([text])).strip()
```

**第 74-75 行**：空输入直接返回空串。

**第 81 行**：复用流式实现——把单段文本包成列表传入 `iter_clean_text`，`"".join` 拼接结果，再 `.strip()` 去掉文档两端的流式换行空白。仅测试和小文本场景使用；大文件走流式 `iter_clean_text` 不拼接。

---

## 第七部分：文本分段 `chunking.py`

```python
"""按段落和长度切分文档。"""
from collections.abc import Iterable, Iterator

from .models import Chunk
```

**第 5 行**：导入 `Chunk` 数据模型。

### `_find_stream_split_end`（第 9-28 行）

```python
def _find_stream_split_end(text: str, chunk_size: int) -> int:
    """在流式缓存的前 chunk_size 个字符中寻找较自然的切分点。"""
    hard_end = min(len(text), chunk_size)
    if hard_end == len(text):
        return hard_end

    minimum_boundary = max(1, int(chunk_size * 0.55))
    candidates = [
        text.rfind(mark, minimum_boundary, hard_end)
        for mark in "。！？.!?；;，,\n"
    ]
    boundary = max(candidates, default=-1)
    if boundary >= minimum_boundary:
        return boundary + 1

    whitespace = text.rfind(" ", minimum_boundary, hard_end)
    return whitespace if whitespace > 0 else hard_end
```

**第 11 行**：`hard_end = min(len(text), chunk_size)`——目标长度不超过 `chunk_size`。

**第 12-13 行**：若剩余文本长度不足 `chunk_size`（`hard_end == len(text)`），直接返回 `hard_end`，即全部作为一段，无需切分。

**第 15 行**：`minimum_boundary = max(1, int(chunk_size * 0.55))`——只允许在窗口后半段（55% 之后）寻找边界，避免产生过短分段。

**第 16-19 行**：在 `[minimum_boundary, hard_end)` 范围内，对每个标点字符（中英文句号、问号、感叹号、分号、逗号、换行）用 `rfind` 找最后出现位置（从右往左，即最靠近 `hard_end` 的自然边界）。

**第 20 行**：`max(candidates, default=-1)` 取这些标点位置里最大的（最靠右），没有则 `-1`。

**第 21-22 行**：若找到的边界 `>= minimum_boundary`，返回 `boundary + 1`（+1 是为了把标点本身包含进当前段）。

**第 24-25 行**：没有合适标点时，在 `[minimum_boundary, hard_end)` 找最后一个空格作为切分点；`whitespace > 0` 才用，否则返回 `hard_end` 硬切（中文连续文本会退化为硬切分）。

### `iter_chunk_text`（第 31-66 行）

```python
def iter_chunk_text(
    text_chunks: Iterable[str],
    chunk_size: int = 800,
    overlap: int = 100,
) -> Iterator[Chunk]:
    """把文本块流式切分为 Chunk，内存中最多保留一个窗口及其重叠部分。"""
    if chunk_size <= 0:
        raise ValueError("chunk_size 必须大于 0")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap 必须满足 0 <= overlap < chunk_size")

    buffer = ""
    chunk_index = 0
```

**第 38-42 行**：参数校验。`chunk_size` 必须 >0；`overlap` 必须 `0 <= overlap < chunk_size`（否则窗口无法向前推进）。

**第 44 行**：`buffer` 是唯一文本缓存，不会随文件总大小无限增长。

**第 45 行**：`chunk_index` 从 0 开始的连续编号。

```python
    for text_chunk in text_chunks:
        if not text_chunk:
            continue
        buffer += text_chunk

        while len(buffer) > chunk_size:
            end = _find_stream_split_end(buffer, chunk_size)
            content = buffer[:end].strip()
            if content:
                yield Chunk(index=chunk_index, content=content)
                chunk_index += 1

            next_start = max(end - overlap, 1)
            buffer = buffer[next_start:]
```

**第 47-50 行**：跳过空块，把块追加到 `buffer`。

**第 52 行**：只要 `buffer` 超过 `chunk_size`，就持续切分（`while` 保证一个超长块可切出多段）。

**第 53 行**：找切分点。

**第 54 行**：取 `buffer[:end]` 并 `.strip()` 去首尾空白。

**第 55-57 行**：若非空，`yield` 一个 `Chunk`，`chunk_index` 递增。

**第 59-60 行**：`next_start = max(end - overlap, 1)`——保留尾部 `overlap` 个字符作为下一段开头（重叠），`max(..., 1)` 保证至少前进 1 个字符避免死循环。`buffer = buffer[next_start:]` 更新剩余缓存。

```python
    if buffer.strip():
        yield Chunk(index=chunk_index, content=buffer.strip())
```

**第 65-66 行**：文件结束后，输出最后一个不足目标长度的分段（若还有内容）。

### `chunk_text`（第 69-73 行）

```python
def chunk_text(text: str, chunk_size: int = 800, overlap: int = 100) -> list[Chunk]:
    """兼容小文本调用，并复用流式实现保证相邻分段始终保留重叠。"""
    return list(iter_chunk_text([text], chunk_size=chunk_size, overlap=overlap))
```

**第 72 行**：`[text]` 只包装调用者已提供的这段文本，调用流式实现，`list(...)` 收集结果。大文件索引路径用 `iter_chunk_text` 直接流式消费，避免在这里物化列表。
