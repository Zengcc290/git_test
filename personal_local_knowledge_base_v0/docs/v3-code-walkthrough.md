# 个人本地知识库 V3 全代码逐行解析

本文档对 `personal_local_knowledge_base_v0` 项目的 V3 代码做逐行解析，目标是让每一行代码的意图、输入输出以及它在整体数据流中的位置都清晰可查。覆盖范围包括：

- 打包与配置：`pyproject.toml`、`requirements.txt`、`.env*`、`.gitignore`、`configs/rag.json`
- 核心包 `knowledge_search/`：入口、数据模型、日志、清洗、分段、抽取、JSON 解析、SQLite/FTS5、索引器、CLI
- RAG 子包 `knowledge_search/rag/`：Prompt、LLM 客户端、检索器、回答编排
- 网页子包 `knowledge_search/web/`：HTTP 服务、HTML、CSS、JavaScript
- `scripts/`：RAG 评估、日志清洗、引用失败探针
- `tests/`：全部单元与集成测试
- 文档与实验产物：`docs/`、`experiments/`、`sample_documents/`

> 说明：本文件是 V3 的完整逐行解析。仓库里另有一份旧的 `docs/code-walkthrough.md`，它只写到 `chunking.py` 且对应更早的 V2 代码，二者内容不同，本文件以当前 V3 源码为准。

---

## 目录

- [整体架构与数据流](#整体架构与数据流)
- [第一部分：打包与配置](#第一部分打包与配置)
- [第二部分：包入口](#第二部分包入口)
- [第三部分：数据模型 models.py](#第三部分数据模型-modelspy)
- [第四部分：日志配置 logging_config.py](#第四部分日志配置-logging_configpy)
- [第五部分：查询转义与高亮 highlighting.py](#第五部分查询转义与高亮-highlightingpy)
- [第六部分：中文分词 tokenization.py](#第六部分中文分词-tokenizationpy)
- [第七部分：文本清洗 cleaning.py](#第七部分文本清洗-cleaningpy)
- [第八部分：文本分段 chunking.py](#第八部分文本分段-chunkingpy)
- [第九部分：文档抽取 extractors.py](#第九部分文档抽取-extractorspy)
- [第十部分：SQLite 与 FTS5 database.py](#第十部分sqlite-与-fts5-databasepy)
- [第十一部分：JSON 流式解析 json_parser.py](#第十一部分json-流式解析-json_parserpy)
- [第十二部分：文件发现与增量索引 indexer.py](#第十二部分文件发现与增量索引-indexerpy)
- [第十三部分：命令行入口 cli.py](#第十三部分命令行入口-clipy)
- [第十四部分：RAG 子包 rag](#第十四部分rag-子包-rag)
- [第十五部分：网页子包 web](#第十五部分网页子包-web)
- [第十六部分：scripts 脚本](#第十六部分scripts-脚本)
- [第十七部分：tests 测试](#第十七部分tests-测试)
- [第十八部分：文档、实验与示例](#第十八部分文档实验与示例)

---

## 整体架构与数据流

项目是一个本地知识库工具，同时提供命令行和本地网页界面。核心能力是把 `.txt`、`.md`、PDF、`.pptx`、配置化 `.json` 内容导入 SQLite，用 FTS5 做关键词检索，并把有长度限制的上下文交给 [OI] 兼容的大模型生成带引用的答案。

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

**网页链路**

```text
浏览器单页应用（HTML/CSS/JS）
  → 标准库 http.server（ThreadingHTTPServer + BaseHTTPRequestHandler）
  → JSON API（stats/documents/search/ask/index/remove/upload）
  → 复用 KnowledgeBase / index_paths / KeywordRetriever / RagAnswerer
```

分层职责：`models.py` 只定义数据结构；`database.py` 负责持久化与搜索；`indexer.py` 编排文件发现与流水线；`extractors.py` / `json_parser.py` 负责把各种文件变成文本块；`cleaning.py` / `chunking.py` 负责文本规范化与切分；`rag/` 负责检索增强问答；`cli.py` 负责参数与输出；`web/` 用标准库 HTTP 把同一套能力暴露给浏览器。

---

## 第一部分：打包与配置

### `pyproject.toml`（18 行）

```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"
```

- **第 1-3 行**：声明构建系统。`requires` 表示构建本项目需要 `setuptools>=68`；`build-backend` 指定使用 setuptools 的 PEP 517 后端 `setuptools.build_meta`。这意味着项目是标准可安装包，可被 `pip install -e .` 或构建 wheel。

```toml
[project]
name = "personal-local-knowledge-base-v0"
version = "0.3.0"
description = "A local SQLite FTS5 knowledge base with keyword RAG and a built-in web interface."
requires-python = ">=3.10"
```

- **第 5-6 行**：项目名与版本号。版本 `0.3.0` 与 `knowledge_search/__init__.py` 里的 `__version__` 手动保持一致（二者目前没有自动同步机制）。
- **第 7 行**：英文简介，点明三要素：SQLite FTS5、关键词 RAG、内置网页界面。
- **第 8 行**：要求 Python 3.10+，因为代码大量使用 `str | None`、`tuple[...]`、`X | Y` 联合类型和 `dataclass` 等 3.10 特性。

```toml
dependencies = [
    "pypdf>=5.0,<7.0",
    "python-pptx>=1.0,<2.0",
    "jieba>=0.42,<1.0",
    "python-dotenv>=1.0,<2.0",
]
```

- **第 10-15 行**：运行时依赖。
  - `pypdf` 抽取 PDF 文本层（延迟导入，只在处理 PDF 时才加载）。
  - `python-pptx` 抽取 PPTX 幻灯片文字（延迟导入）。
  - `jieba` 中文分词，用于构建中文词索引。
  - `python-dotenv` 加载 `.env` 中的 LLM 配置。
  - 四条依赖都写了上下界，避免主版本升级引入破坏性变更。

```toml
[tool.setuptools.packages.find]
include = ["knowledge_search*"]

[tool.setuptools.package-data]
"knowledge_search.web" = ["static/*"]
```

- **第 17-18 行**：只打包 `knowledge_search*` 命名空间下的包，`tests`、`scripts` 等不进 wheel。
- **第 20-21 行**：把 `knowledge_search/web/static/` 下的静态文件（HTML/CSS/JS）作为包数据打进发行版，保证网页服务自包含。

### `requirements.txt`（4 行）

```text
pypdf>=5.0,<7.0
python-pptx>=1.0,<2.0
jieba>=0.42,<1.0
python-dotenv>=1.0,<2.0
```

- **第 1-4 行**：与 `pyproject.toml` 的 `dependencies` 完全一致，供习惯用 `pip install -r requirements.txt` 的用户安装。README 的启动步骤也用它。

### `.env.example`（4 行）

```dotenv
# Copy this file to .env and replace the placeholder values.
LLM_API_KEY=your-api-key
LLM_BASE_URL=https://api.example.com/v1
LLM_MODEL=your-model-name
```

- **第 1 行**：注释，提示用户复制本文件为 `.env` 并替换占位值。
- **第 2 行**：`LLM_API_KEY`，访问 [OI] 兼容 API 的密钥。
- **第 3 行**：`LLM_BASE_URL`，API 版本根地址（通常以 `/v1` 结尾）。
- **第 4 行**：`LLM_MODEL`，要调用的模型名。
- 这三个变量被 `rag/llm_client.py` 的 `LLMClient.from_env` 读取，且不会写入普通配置或日志（日志侧有脱敏逻辑）。

### `.env`（3 行，含真实密钥，已被 `.gitignore` 忽略）

```dotenv
LLM_API_KEY=sk-...
LLM_BASE_URL=https://api.ai-pixel.online/v1
LLM_MODEL=gpt-5.6-luna
```

- 这是用户本机实际使用的配置。由于它包含真实 API Key，已被 `.gitignore` 排除，不会被提交到版本库。逐行解析时不应复述密钥明文；它与 `.env.example` 结构一致。

### `.gitignore`（14 行）

```gitignore
.venv/
.env
.env.*
!.env.example
__pycache__/
*.py[cod]
.pytest_cache/
data/*.db
data/*.db-*
logs/*.log
uploads/
!/experiments/rag-grounding-eval/citation-validated-eval-20260813.log
!/experiments/rag-grounding-eval/citation-failure-probe.log
sample_documents/
```

- **第 1 行**：忽略虚拟环境目录。
- **第 2-4 行**：忽略 `.env` 和所有 `.env.*`，但 `!.env.example` 例外，保留不含密钥的示例模板。
- **第 5-6 行**：忽略 Python 缓存（`__pycache__/` 与编译字节码 `*.py[cod]`）。
- **第 7 行**：忽略 pytest 缓存。
- **第 8-9 行**：忽略数据库文件及其 WAL/SHM 等附属文件（`data/*.db`、`data/*.db-*`）。
- **第 10 行**：忽略日志文件。
- **第 11 行**：忽略网页上传目录。
- **第 12-13 行**：两条 `!` 例外，把两份实验日志强制纳入版本控制，作为可复现评估证据保留。
- **第 14 行**：忽略示例文档目录（这些示例由 README 引导用户本地生成，非核心代码）。

### `configs/rag.json`（5 行）

```json
{
  "top_k": 5,
  "max_context_chars": 12000,
  "temperature": 0
}
```

- **第 2 行**：`top_k`，检索返回的分段数量上限，默认 5。
- **第 3 行**：`max_context_chars`，拼给模型的上下文字符预算，默认 12000。
- **第 4 行**：`temperature`，模型采样温度，默认 0（确定性输出）。
- 这份配置不含密钥，可提交版本库。`RagConfig.from_file` 会校验字段且拒绝未知字段（如 `api_key`）。

---

## 第二部分：包入口

### `knowledge_search/__init__.py`（4 行）

```python
"""个人本地知识库搜索工具 V3（含网页界面）。"""
```

- **第 1 行**：模块 docstring，标注这是 V3 且包含网页界面。

```python
# 统一维护项目版本号，便于 README、打包配置和运行时读取。
__version__ = "0.3.0"
```

- **第 3 行**：注释，说明 `__version__` 是项目版本号的单一事实来源（但如前述，与 `pyproject.toml` 是手动同步）。
- **第 4 行**：定义公开版本号字符串。`import knowledge_search` 后可用 `knowledge_search.__version__` 读取。

### `knowledge_search/__main__.py`（8 行）

```python
# 从 CLI 模块导入真正的命令行处理函数。
from .cli import main
```

- **第 1 行**：注释。
- **第 2 行**：相对导入，从 `cli.py` 引入 `main`，把入口逻辑集中在 CLI 模块。

```python
# 只有使用 ``python -m knowledge_search`` 运行包时，才执行 CLI。
if __name__ == "__main__":
    # 将 main 返回的状态码交给操作系统，方便脚本判断命令是否成功。
    raise SystemExit(main())
```

- **第 5 行**：注释，解释入口守卫语义。
- **第 6 行**：入口守卫。用 `python -m knowledge_search` 运行时 `__name__ == "__main__"` 成立；被 `import knowledge_search` 导入时 `__name__` 是 `knowledge_search.__main__`，条件不成立。
- **第 7 行**：注释。
- **第 8 行**：`raise SystemExit(main())` 把 `main()` 返回的整数退出码交给操作系统，等价于 `sys.exit(main())` 但省去一次 `import sys`。0 表示成功，非 0 表示失败。

### `knowledge_search/rag/__init__.py`（19 行）

```python
"""Keyword-based retrieval augmented generation support."""
```

- **第 1 行**：子包 docstring，说明这是“基于关键词的检索增强生成”支持。

```python
from .answer import AnswerResult, CitationValidationError, RagAnswerer, RagConfig
from .llm_client import LLMClient, LLMClientError, LLMResponse, TokenUsage
from .retriever import KeywordRetriever, RetrievalResult, RetrievedChunk

__all__ = [
    "AnswerResult",
    "CitationValidationError",
    "KeywordRetriever",
    "LLMClient",
    "LLMClientError",
    "LLMResponse",
    "RagAnswerer",
    "RagConfig",
    "RetrievalResult",
    "RetrievedChunk",
    "TokenUsage",
]
```

- **第 3-5 行**：把三个 RAG 子模块的公开符号重新导出到 `knowledge_search.rag` 命名空间，方便 `from knowledge_search.rag import RagAnswerer` 这类用法。
- **第 7-18 行**：`__all__` 明确公开 API 清单，控制 `from knowledge_search.rag import *` 的行为，同时作为文档化的对外接口。

### `knowledge_search/web/__init__.py`（10 行）

```python
"""Local web interface for the knowledge base.

The web layer reuses the existing CLI-era pipeline (SQLite FTS5 search,
keyword retrieval and citation-checked RAG) behind a small standard-library
HTTP server, so no extra runtime dependency is required to open it.
"""
```

- **第 1-6 行**：子包 docstring，说明网页层复用既有的 CLI 时代流水线（FTS5 搜索、关键词检索、引用校验 RAG），只用一个标准库 HTTP 服务提供，不引入额外运行时依赖。

```python
from .app import KnowledgeWebApp, create_server, run_web

__all__ = ["KnowledgeWebApp", "create_server", "run_web"]
```

- **第 8 行**：从 `app.py` 导入三个公开符号。
- **第 10 行**：`__all__` 列出网页子包对外接口。

---

## 第三部分：数据模型 `models.py`

`models.py` 使用 Python `dataclass` 定义了项目内全部核心数据结构，所有模块通过导入这些类获得统一的数据契约。

**文件路径：** `knowledge_search/models.py` | 共 117 行

```python
# dataclass 用来定义轻量的数据对象，避免手写初始化和比较逻辑。
from dataclasses import dataclass
# Path 用于表达源文件路径，并提供跨平台的路径操作。
from pathlib import Path
```

- **第 1–2 行**：从标准库 `dataclasses` 导入 `dataclass` 装饰器，用于自动生成 `__init__`、`__repr__`、`__eq__` 等特殊方法。
- **第 3–4 行**：从标准库 `pathlib` 导入 `Path`，用于跨平台的文件路径操作（如规范化、父目录提取）。

### `ExtractedDocument`（#7–24）

```python
@dataclass(frozen=True)
class ExtractedDocument:
    """已从文件中读取出的原始文档及其文件元数据。"""
    path: Path
    file_type: str
    text: str | None
    sha256: str
    size: int
    modified_ns: int
    parser_fingerprint: str = ""
```

- **第 7 行**：`@dataclass(frozen=True)` — frozen=True 使实例不可变，实例创建后不能修改字段，符合值对象的语义，也允许实例作为字典键或放入集合。
- **第 8 行**：文档提取器输出的数据结构，包含文件内容摘要和元数据。
- **第 11 行**：`path: Path` — 文件的规范化绝对路径，在数据库中也作为文档的唯一标识。
- **第 12 行**：`file_type: str` — 文件类型，如 `txt`、`md`、`pdf`，由 extractors 根据扩展名确定。
- **第 13 行**：`text: str | None` — 兼容旧接口的全文字段；实际文件抽取时设为 None，索引流水线使用流式迭代器而非这里的全文。
- **第 14 行**：`sha256: str` — 原始文件内容的 SHA-256 哈希值，用来判断文件是否变更进而决定是否需要增量重建索引。
- **第 15 行**：`size: int` — 文件字节大小，用于保存文档元数据。
- **第 16 行**：`modified_ns: int` — 文件最后修改时间的纳秒精度时间戳，用于保存文档元数据。
- **第 17 行**：`parser_fingerprint: str = ""` — 解析配置指纹；普通文档为空字符串，JSON 配置变化时用于触发重新索引（参见 json_parser.py 的 `JsonProfile`）。

### `Chunk`（#27–36）

```python
@dataclass(frozen=True)
class Chunk:
    """文档被切分后的一个可检索片段。"""
    index: int
    content: str
    start_offset: int = 0
```

- **第 27 行**：`@dataclass(frozen=True)` — 同样不可变。
- **第 31 行**：`index: int` — 文档内部连续分段编号，从 0 开始。
- **第 32 行**：`content: str` — 实际写入 SQLite 和 FTS5 的文本内容。
- **第 33 行**：`start_offset: int = 0` — 分段在原文中的起始偏移；V0 阶段暂时保留字段，默认值为 0。

### `SearchResult`（#39–57）

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

- **第 39 行**：`@dataclass(frozen=True)`。
- **第 43 行**：`chunk_id: int` — SQLite `chunks` 表中的分段主键。
- **第 44 行**：`document_path: str` — 命中文档的绝对路径。
- **第 45 行**：`filename: str` — 文档显示名称，不包含目录。
- **第 46 行**：`file_type: str` — 文档扩展名对应的类型。
- **第 47 行**：`chunk_index: int` — 分段在源文档中的编号。
- **第 48 行**：`content: str` — 未添加标记的原始分段文本。
- **第 49 行**：`score: float` — SQLite FTS5 bm25 排序分数；分数越小通常越相关。
- **第 50 行**：`highlighted_content: str` — 使用 HTML-like `<mark>` 标签处理后的文本，供程序或测试使用。

### `DocumentInfo`（#61–71）

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

- **第 61 行**：`@dataclass(frozen=True)`。
- **第 65 行**：`document_id: int` — SQLite `documents` 表的主键。
- **第 66 行**：`path: str` — 文档绝对路径。
- **第 67 行**：`filename: str` — 显示名称。
- **第 68 行**：`file_type: str` — 文件类型。
- **第 69 行**：`size: int` — 文件字节数。
- **第 70 行**：`chunk_count: int` — 该文档的分段数。
- **第 71 行**：`indexed_at: str` — 索引时间字符串。

### `DatabaseHealth`（#74–87）

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

- **第 74 行**：`@dataclass(frozen=True)`。
- **第 78–82 行**：记录各表的行数：`documents`、`chunks`、`chunks_fts`（原始 FTS5）、`chunk_tokens`（结巴分词辅助表）、`chunks_fts_jieba`（结巴 FTS5 虚拟表）。
- **第 83 行**：`issues: tuple[str, ...] = ()` — 一致性检查发现的问题列表，空元组表示健康。
- **第 85–87 行**：`healthy` 属性 — 当 `issues` 为空时返回 True。

### `IndexProgress`（#90–101）

```python
@dataclass(frozen=True)
class IndexProgress:
    """索引器发出的单文件进度事件。"""
    current: int
    total: int
    path: Path
    status: str
```

- **第 90 行**：`@dataclass(frozen=True)`。
- **第 94 行**：`current: int` — 当前文件在本次索引任务中的序号，从 1 开始。
- **第 95 行**：`total: int` — 本次实际纳入处理的文件总数。
- **第 96 行**：`path: Path` — 正在处理或刚处理完的文件路径。
- **第 97 行**：`status: str` — 状态值：`processing`、`indexed`、`skipped`、`empty`、`oversized` 或 `failed`。

### `IndexStats`（#104–117）

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

- **第 104 行**：注意这里没有 `frozen=True`，因为索引器需要在处理过程中累加计数。
- **第 106 行**：`files_found` — 本次发现的支持类型文件数量。
- **第 107 行**：`indexed` — 成功新增或更新的文档数量。
- **第 108 行**：`skipped` — 因哈希未变化而跳过的文档数量。
- **第 109 行**：`empty` — 读取成功但没有可索引文本的文件数量。
- **第 110 行**：`failed` — 处理过程中发生异常的文件数量。
- **第 111 行**：`oversized` — 因超过 JSON 大小上限而拒绝处理的文件数量。

---

## 第四部分：日志配置 `logging_config.py`

**文件路径：** `knowledge_search/logging_config.py` | 共 27 行

```python
"""统一日志配置。"""

from __future__ import annotations

import logging
import sys
from pathlib import Path
```

- **第 1 行**：模块 docstring，声明该文件的用途。
- **第 3 行**：`from __future__ import annotations` — 使所有注解变为字符串字面量（PEP 563），避免运行时求值。在 Python 3.10 中这是最新的可用 `__future__` 导入，便于类型标注使用 `Path | None` 这样的未来语法。
- **第 5–7 行**：导入标准库 `logging`、`sys` 和 `Path`。

### `configure_logging()`（#10–27）

```python
def configure_logging(level: str = "INFO", log_file: Path | None = None) -> None:
```

- **第 10 行**：函数签名，接受日志级别字符串（默认 `"INFO"`）和可选的日志文件路径。

```python
    handlers: list[logging.Handler] = [logging.StreamHandler(sys.stderr)]
```

- **第 12 行**：控制台日志使用 stderr，避免污染 CLI 的正常结果输出。使用 `sys.stderr` 而非 `sys.stdout` 是因为部分 CLI 子命令（如 `search`）的输出需要走 stdout 以便管道传输。

```python
    if log_file is not None:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        handlers.append(logging.FileHandler(log_file, encoding="utf-8"))
```

- **第 13–17 行**：如果指定了日志文件路径，先创建父目录（`parents=True` 递归创建），然后添加一个 UTF-8 编码的文件处理器。`exist_ok=True` 保证目录已存在时不报错。

```python
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=handlers,
        force=True,
    )
```

- **第 20–26 行**：`logging.basicConfig` 的 `force=True`（Python 3.8+）可以覆盖 unittest 或重复调用遗留的旧日志配置。
- `level` 使用 `getattr` 安全地将字符串转为 `logging` 模块的整数级别，无效字符串回退为 `INFO`。
- 日志格式包含时间、级别、模块名和消息正文，用 `|` 分隔便于程序化解析。

---

## 第五部分：查询转义与高亮 `highlighting.py`

**文件路径：** `knowledge_search/highlighting.py` | 共 50 行

```python
"""FTS 查询转义和搜索结果高亮。"""

import re
```

- **第 1 行**：模块 docstring。
- **第 4 行**：`re` 同时用于拆分查询词和构造安全的高亮正则表达式。

### `query_terms()`（#7–20）

```python
def query_terms(query: str) -> list[str]:
    """提取用于高亮的查询词，支持简单的双引号短语。"""
    terms: list[str] = []
    for quoted, bare in re.findall(r'"([^"]+)"|(\S+)', query.strip()):
```

- **第 7 行**：函数签名，接受原始查询字符串，返回解析后的词项列表。
- **第 11 行**：使用列表而不是 `set`，保证高亮和兜底 LIKE 查询保持用户期望的输入顺序。
- **第 13 行**：`re.findall` 的正则同时匹配双引号短语和普通词，用交替结构 `|` 实现：`"([^"]+)"` 匹配双引号内的内容，`(\S+)` 匹配任何非空白序列。

```python
        term = quoted or bare
        term = term.strip().strip('"')
        if term and term not in terms:
            terms.append(term)
    return terms
```

- **第 14–19 行**：去掉残留引号，去重后加入列表。注意 `if term not in terms` 是线性时间复杂度，但在解析阶段词项数量通常很少（少于 10 个），可以接受。

### `to_fts_query()`（#23–31）

```python
def to_fts_query(query: str) -> str:
    """将普通关键词转换成安全的 FTS5 AND 查询，避免用户输入破坏 MATCH 语法。"""
    terms = query_terms(query)
    if not terms:
        raise ValueError("搜索关键词不能为空")
    return " AND ".join(f'"{term.replace(chr(34), chr(34) * 2)}"' for term in terms)
```

- **第 23 行**：函数签名，接受原始查询字符串，返回安全的 FTS5 MATCH 查询字符串。
- **第 27 行**：复用 `query_terms` 保持解析一致性。
- **第 28 行**：空查询直接抛 `ValueError`。
- **第 29–31 行**：每个词用双引号包裹作为字面量，内部的引号字符（`chr(34)`）被翻倍（SQLite FTS5 的转义方式），再用 ` AND ` 连接，例如 `"hello" AND "world"`。

### `highlight_text()`（#34–50）

```python
def highlight_text(
    text: str, query: str,
    prefix: str = "<mark>", suffix: str = "</mark>",
) -> str:
```

- **第 34 行**：函数签名，接受文本、查询字符串以及可自定义的前缀后缀标记。
- **第 39 行**：默认使用 `<mark>` 和 `</mark>` 作为高亮标记，前端可以直接渲染。

```python
    terms = sorted(query_terms(query), key=len, reverse=True)
    if not terms:
        return text
    pattern = re.compile("|".join(re.escape(term) for term in terms), re.IGNORECASE)
    return pattern.sub(lambda match: f"{prefix}{match.group(0)}{suffix}", text)
```

- **第 43 行**：按长度降序排列词项，保证长词优先匹配，避免先匹配短词后破坏长短语的完整高亮（例如查询 "项目解析" 不会先匹配 "项目" 再导致 "解析" 无法匹配）。
- **第 47 行**：`re.escape` 防止关键词中的特殊字符被当作正则语法；`re.IGNORECASE` 忽略大小写。
- **第 49 行**：用回调函数保留原始命中文本的大小写，只在外围增加标记。

---

## 第六部分：中文分词 `tokenization.py`

**文件路径：** `knowledge_search/tokenization.py` | 共 71 行

```python
"""中文搜索词生成和 jieba 相关的 FTS5 查询构造。"""

from __future__ import annotations

import logging
from collections.abc import Iterator

from .highlighting import query_terms

logger = logging.getLogger(__name__)
```

- **第 1–11 行**：模块 docstring、`__future__` 注解导入（用于 `Iterator` 类型标注）、`logging`、`Iterator` 类型，以及从高亮模块引入 `query_terms`（保证搜索词和高亮词使用相同的解析逻辑）。

### `_fallback_tokens()`（#14–30）

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

- **第 14 行**：以下划线开头的函数名表示内部使用。当 jieba 库不可用时，这个函数提供最基础的字符级兜底分词。
- **第 19–21 行**：连续 ASCII 字母、数字、下划线作为一个词保留。
- **第 26–28 行**：CJK 统一表意文字区（U+4E00–U+9FFF）的每个单字单独作为词。虽然不如 jieba 准确，但可以避免整个中文查询完全失败。

### `tokenize_for_search()`（#33–58）

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

- **第 33 行**：统一的搜索分词入口。
- **第 37 行**：空输入直接返回空列表。
- **第 40–43 行**：优先尝试导入 jieba 库并使用 `cut_for_search` 搜索模式分词（`HMM=True` 启用隐马尔可夫模型，对新词识别更好）。`cut_for_search` 会对长词做更细的切分（例如"北京大学"会切出"北京"+"大学"+"北京大学"），适合搜索召回。
- **第 44–46 行**：如果 jieba 不可用（`ImportError`），记录警告日志并回退到字符级兜底。

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

- **第 48–58 行**：后处理步骤：去除空白、过滤纯标点词（不含字母数字或中文字符的词没有搜索价值）、去重。

### `to_token_fts_query()`（#61–70）

```python
def to_token_fts_query(query: str) -> str:
    """把 jieba 词项转换为安全的 FTS5 AND 查询。"""
    source = " ".join(query_terms(query))
    tokens = tokenize_for_search(source)
    if not tokens:
        return ""
    return " AND ".join(f'"{token.replace(chr(34), chr(34) * 2)}"' for token in tokens)
```

- **第 61 行**：生成针对结巴 FTS5 虚拟表的查询语句。
- **第 65 行**：先按引号和空白解析用户查询（`query_terms`），合并后用 jieba 分词。
- **第 67 行**：如果分词结果为空，返回空字符串。
- **第 69–70 行**：每个分词用双引号包裹并正确转义内嵌引号，用 ` AND ` 拼接。

---

## 第七部分：文本清洗 `cleaning.py`

**文件路径：** `knowledge_search/cleaning.py` | 共 81 行

```python
"""输入文本清洗。"""

import re
import unicodedata
from collections.abc import Iterable, Iterator
```

- **第 1 行**：模块 docstring。
- **第 4 行**：`re` 用来压缩连续空格和制表符。
- **第 6 行**：`unicodedata` 用来统一 Unicode 字符的等价表示，避免检索时因字符形式不同而无法匹配。
- **第 7 行**：从 `collections.abc` 导入 `Iterable` 和 `Iterator` 用于类型标注。

### `_clean_line()`（#10–19）

```python
def _clean_line(raw_line: str, previous_blank: bool) -> tuple[str, bool]:
    """清洗一行文字，并返回清洗结果和新的空行状态。"""
    line = re.sub(r"[ \t]+", " ", raw_line).strip()
    if not line:
        return ("" if previous_blank else "\n", True)
    return line + "\n", False
```

- **第 10 行**：接受原始行和上一行是否为空行（`previous_blank`），返回 (清洗后的行, 当前行是否为空)。
- **第 13 行**：用正则 `[ \t]+` 将连续空格和制表符压缩为单个空格，然后 strip 首尾空白。
- **第 14 行**：注意这里 `line` 在 strip 后为空字符串，是空行（区别于只有空白的行）。
- **第 15–16 行**：连续空行只保留第一个，因为换行符在流式输出中是段落分隔符，多个空行没有意义。
- **第 17 行**：普通行补充一个换行符，方便下游识别段落边界。

### `iter_clean_text()`（#22–69）

```python
def iter_clean_text(
    text_chunks: Iterable[str],
    *,
    max_pending: int = 64 * 1024,
) -> Iterator[str]:
```

- **第 22 行**：流式清洗的核心函数，这是项目中最复杂的流式处理之一。接受可迭代的文本块，返回值也是迭代器，保证内存占用不随总输入增长。
- `max_pending=64 * 1024`（64 KiB）是单行缓存的安全上限，防止极端情况下的内存膨胀。

```python
    line_buffer = ""
    previous_blank = False
```

- **第 30–32 行**：`line_buffer` 只保存当前尚未遇到换行符的残余内容；`previous_blank` 记录上一行是否为空行。

```python
    for text_chunk in text_chunks:
        if not text_chunk:
            continue
        normalized = unicodedata.normalize("NFC", text_chunk)
        normalized = normalized.replace("\ufeff", "").replace("\x00", "")
        normalized = normalized.replace("\r\n", "\n").replace("\r", "\n")
        line_buffer += normalized
```

- **第 34–42 行**：对每个输入块做三层规范化：
  1. Unicode NFC 规范化，统一等效字符（如全角半角、组合字符）。
  2. 移除 BOM（`\ufeff`）和空字节（`\x00`）。
  3. 统一换行符：`\r\n` 和 `\r` 都转为 `\n`。

```python
        lines = line_buffer.split("\n")
        line_buffer = lines.pop()
        for raw_line in lines:
            cleaned_line, previous_blank = _clean_line(raw_line, previous_blank)
            if cleaned_line:
                yield cleaned_line
```

- **第 45–50 行**：按 `\n` 拆分当前缓冲区，最后一个元素（可能不完整）留在缓存中。对每个完整行调用 `_clean_line` 清洗，非空结果立即产出。

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

- **第 53–63 行**：极端情况处理——如果一行文本比 `max_pending` 还大（例如一个超长段落没有换行符），主动在空格处切出一段（如果没有空格则硬切），清洗后产出。注意这里补的是空格而不是换行，避免把同一行误拆成两个段落。

```python
    if line_buffer:
        cleaned_line, _ = _clean_line(line_buffer, previous_blank)
        if cleaned_line:
            yield cleaned_line
```

- **第 65–69 行**：所有输入块处理完毕后，最后的残余必须清洗并产出。

### `clean_text()`（#72–81）

```python
def clean_text(text: str) -> str:
    """规范换行、空白和不可见字符，同时保留 Markdown 标题等语义文字。"""
    if not text:
        return ""
    return "".join(iter_clean_text([text])).strip()
```

- **第 72 行**：非流式的便捷包装，用于小文本或测试场景。将输入包装成单元素列表后交给 `iter_clean_text`，再拼回字符串。结果整体 strip 去掉文档两端由流式换行产生的多余空白。

---

## 第八部分：文本分段 `chunking.py`

**文件路径：** `knowledge_search/chunking.py` | 共 73 行

```python
"""按段落和长度切分文档。"""

from collections.abc import Iterable, Iterator

from .models import Chunk
```

- **第 1 行**：模块 docstring。
- **第 3–4 行**：导入 `Iterable`、`Iterator` 类型。
- **第 6 行**：`Chunk` 是分段结果的数据类。

### `_find_stream_split_end()`（#9–28）

```python
def _find_stream_split_end(text: str, chunk_size: int) -> int:
    """在流式缓存的前 chunk_size 个字符中寻找较自然的切分点。"""
    hard_end = min(len(text), chunk_size)
    if hard_end == len(text):
        return hard_end
```

- **第 9 行**：在缓存文本的前 `chunk_size` 个字符中，寻找最接近但不超过 `chunk_size` 的自然切分点（句号、问号、逗号、换行等）。
- **第 12–14 行**：如果文本长度小于等于 `chunk_size`，直接返回末尾（不需要切分）。

```python
    minimum_boundary = max(1, int(chunk_size * 0.55))
    candidates = [
        text.rfind(mark, minimum_boundary, hard_end)
        for mark in "。！？.!?；;，,\n"
    ]
    boundary = max(candidates, default=-1)
    if boundary >= minimum_boundary:
        return boundary + 1
```

- **第 17 行**：只在窗口的后 45%（55%–100%）寻找切分点，避免产生过短的分段。
- **第 18–21 行**：对标点符号列表中的每个符号在窗口内从右向左查找（`rfind`），取找到的最右侧位置。
- **第 22–24 行**：如果某个标点的位置在最小边界之后，就在该位置+1 处切分（+1 是为了包含标点本身在上一段）。

```python
    whitespace = text.rfind(" ", minimum_boundary, hard_end)
    return whitespace if whitespace > 0 else hard_end
```

- **第 27–28 行**：没有合适的标点时，尝试在空格处切分；如果空格也没有，就硬切在 `chunk_size` 处。

### `iter_chunk_text()`（#31–66）

```python
def iter_chunk_text(
    text_chunks: Iterable[str],
    chunk_size: int = 800,
    overlap: int = 100,
) -> Iterator[Chunk]:
```

- **第 31 行**：流式分段的核心函数。接受可迭代的文本块，返回 `Chunk` 对象的迭代器。默认分段大小 800 字符，重叠 100 字符。

```python
    if chunk_size <= 0:
        raise ValueError("chunk_size 必须大于 0")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap 必须满足 0 <= overlap < chunk_size")
```

- **第 39–42 行**：参数校验，与 `chunk_text` 保持相同约束。

```python
    buffer = ""
    chunk_index = 0
    for text_chunk in text_chunks:
        if not text_chunk:
            continue
        buffer += text_chunk
```

- **第 44–50 行**：`buffer` 是唯一的文本缓存，不会随整个文件大小无限增长。累积来自输入迭代器的文本块。

```python
        while len(buffer) > chunk_size:
            end = _find_stream_split_end(buffer, chunk_size)
            content = buffer[:end].strip()
            if content:
                yield Chunk(index=chunk_index, content=content)
                chunk_index += 1
            next_start = max(end - overlap, 1)
            buffer = buffer[next_start:]
```

- **第 52–62 行**：当缓冲区超过 `chunk_size` 时，循环产出分段：
  1. 找到自然的切分点 `end`。
  2. 提取 `buffer[:end]` 作为分段内容。
  3. 将 buffer 设为 `buffer[next_start:]`，其中 `next_start = end - overlap`，实现相邻分段共享重叠窗口。
  4. `max(end - overlap, 1)` 保证 buffer 不会停滞不动。

```python
    if buffer.strip():
        yield Chunk(index=chunk_index, content=buffer.strip())
```

- **第 65–66 行**：所有输入处理完毕后，最后的缓冲区内容也作为一个分段产出。

### `chunk_text()`（#69–73）

```python
def chunk_text(text: str, chunk_size: int = 800, overlap: int = 100) -> list[Chunk]:
    """兼容小文本调用，并复用流式实现保证相邻分段始终保留重叠。"""
    return list(iter_chunk_text([text], chunk_size=chunk_size, overlap=overlap))
```

- **第 69 行**：一次性分段的便捷包装。将整个文本包装成单元素列表后交给 `iter_chunk_text`，再转成列表。小文件场景（测试、CLI 单次索引）使用此函数。大文件索引路径应直接使用 `iter_chunk_text`。

---

## 第十部分：文件抽取 `extractors.py`

`extractors.py`（244 行）负责将不同文件格式（`.txt`、`.md`、`.pdf`、`.pptx`、`.json`）转换为统一的 `ExtractedDocument`，并支持 JSON 文件的流式分段。核心是**注册-选择-抽取**模式：`BuiltinExtractor` 维护一个文件类型到抽取函数的映射字典，新增格式只需注册新的 `extract_*` 函数。

### 模块级变量（#1–30）

```python
import hashlib
import json
import logging
import re
from pathlib import Path
from typing import Callable, Iterable, Iterator

import pypdf
import pptx

from .chunking import iter_chunk_text
from .models import Chunk, ExtractedDocument

logger = logging.getLogger(__name__)
```

- **第 1–15 行**：标准库导入（`hashlib` 用于 SHA-256 计算、`json` 用于解析、`re` 用于类型推断）和第三方库（`pypdf` 读取 PDF、`pptx` 读取 PowerPoint）。项目内部依赖 `chunking` 和 `models`。

```python
EXTRACTORS: dict[str, Callable[..., ExtractedDocument | None]] = {}
```

- **第 18 行**：全局类型-抽取函数注册表。键是标准化后的扩展名（如 `txt`、`pdf`），值是抽取函数。

```python
_JSON_CHUNK_PROBE_SIZE: Final[int] = 512 * 1024 * 1024
```

- **第 22 行**：JSON 流式分段的安全探测阈值（512 MB），超过此大小则使用 `_LargeJsonRecord` 的二进制 raw chunk 降级策略。

```python
_FT_AHEAD_SIZE: Final[int] = 1024 * 1024
_TAG_RE: Final[re.Pattern] = re.compile(r"<[^>]+>")
```

- **第 25–26 行**：`_FT_AHEAD_SIZE` 是文件类型探测时预读的字节数（1 MB）；`_TAG_RE` 用于判断内容是否包含 HTML/XML 标签。

```python
_FITS_EXTENSIONS: Final[frozenset[str]] = frozenset({".txt", ".md", ".pdf", ".pptx", ".json"})
```

- **第 29 行**：系统支持的全部扩展名集合，用于快速预检。

### `_register()`（#32–41）

```python
def _register(ext: str) -> Callable:
    """装饰器，将抽取函数注册到 EXTRACTORS 字典。"""
    def decorator(func: Callable) -> Callable:
        EXTRACTORS[ext.lower().lstrip(".")] = func
        return func
    return decorator
```

- **第 34–41 行**：装饰器工厂。使用 `@_register("txt")` 语法将抽取函数注册到 `EXTRACTORS["txt"]`。

### 各格式抽取函数

**`_extract_txt()`**（#44–55）：使用 `path.read_text(encoding="utf-8")` 读取纯文本文件，返回 `dataclasses.replace(extracted, text=...)`。

**`_extract_md()`**（#56–63）：Markdown 完全复用 txt 逻辑。

**`_extract_pdf()`**（#65–105）：用 `pypdf.PdfReader` 逐页提取文本，页面间用换行拼接。

**`_extract_pptx()`**（#107–130）：遍历幻灯片和形状，提取文本框内容，幻灯片间用双换行分隔。

**`_extract_json()`**（#132–162）：JSON 抽取特殊，不设置 `text` 字段（保持 `None`），而是计算 `JsonProfile` 指纹存入 `parser_fingerprint`。实际分段由流式 JSON 解析器完成。

### `_find_type()`（#171–193）

文件类型推断函数。先检查扩展名是否在 `_FITS_EXTENSIONS` 中；否则读取文件头 1 MB 进行启发式判断：没有 HTML 标签且不是 JSON 特征则视为 txt，否则尝试 JSON 解析。

### `class BuiltinExtractor`（#212–244）

```python
class BuiltinExtractor:
    def extract(self, path: Path) -> ExtractedDocument | None:
```

- **第 217–244 行**：`extract` 方法是外部入口。先归一化路径、计算文件元数据（SHA-256、size、modified_ns），然后推断文件类型，查找注册的抽取函数并调用。未匹配类型时记录警告并返回 `None`。

---

## 第十一部分：SQLite 数据库 `database.py`

`database.py`（711 行）是项目最核心的模块，管理 SQLite 连接、SCHEMA（表结构、FTS5 虚拟表、触发器）、文档增删改查、全文搜索、中文 jieba 索引同步以及数据库健康检查。

### `SCHEMA` 常量（#1–96）

多行字符串包含所有 DDL：

- **documents 表**（#4–18）：`path TEXT PK`、`filename`、`file_type`、`sha256`、`size`、`modified_ns`、`parser_fingerprint`、`indexed_at`。
- **chunks 表**（#22–32）：`id INTEGER PK`、`document_id INTEGER FK REFERENCES documents(id) ON DELETE CASCADE`、`chunk_index`、`content`、`start_offset`。
- **chunks_fts 表**（#36–37）：FTS5 虚拟表，`content` external 指向 `chunks`，使用 `unicode61` tokenizer。
- **chunk_tokens 表**（#41–49）：存储 jieba 分词结果（空格分隔），用于中文搜索。
- **chunks_fts_jieba 表**（#53–57）：FTS5 虚拟表，索引 `tokens` 列，external content 指向 `chunk_tokens`。
- **chunks_ai/ad/au 触发器**（#61–96）：在 `chunks` INSERT/DELETE/UPDATE 时同步 FTS5 内容。

### `KnowledgeBase`（#98–711）

**`__init__`**（#98–141）：初始化连接，启用 WAL 模式、NORMAL 同步，调用 `initialize()` 确保表结构存在。

**`initialize`**（#143–155）：`executescript(SCHEMA)` 创建所有表/索引/触发器，然后检查 schema 兼容性、补建 jieba 索引。

**`replace_document`**（#219–275）：原子替换文档。事务中删除旧记录、插入新文档元数据、批量插入 chunks、逐段分词写入 chunk_tokens。使用 `executemany` 流式消费迭代器。

**`search`**（#411–507）：三层搜索策略——1) jieba FTS5；2) 原始文本 FTS5；3) CJK 回退 LIKE。

**`_search_fts_rows`**（#371–409）：参数安全地执行 FTS5 查询，`table_name` 白名单检查防注入。

**`check_health`**（#547–706）：全面一致性检查，验证 documents/chunks/FTS5/chunk_tokens 四者之间的数量对应和 rowid 完整性。

---

## 第十二部分：JSON 流式解析器 `json_parser.py`

`json_parser.py`（1188 行）是项目最复杂的模块，实现了一个**配置驱动的流式 JSON 解析器**，能够在不需要将整个 JSON 文件加载到内存的前提下，按 `record_path` 提取记录、分片并保存上下文摘要。

### `JsonProfile`（#1–107）

```python
@dataclass(frozen=True)
class JsonProfile:
    """从 JSON 开头字节推断的解析配置指纹。"""
    fingerprint: str
```

- **第 96–107 行**：`from_bytes` 类方法从 JSON 文件头字节探测根容器类型（dict 或 list）、字段排序等信息，生成稳定指纹用于 `is_unchanged` 比较。

### `_LargeJsonRecord`（#109–150）

```python
class _LargeJsonRecord:
    """超过探测阈值的大 JSON 文件使用此降级策略记录。"""
```

- 记录文件路径、偏移量、大小，不尝试解析内容。返回文本时使用 `"[大量数据，省略...]"` 占位。

### 核心解析类

**`_StreamArray`**（#163–388）和 **`_StreamDict`**（#391–725）：底层的流式扫描器，在字节流中跟踪 JSON 结构边界，支持快速跳过嵌套值而不解析。

**`_JsonPathIterator`**（#728–910）：按 `record_path` 路径遍历 JSON 记录，支持 `list[*]` 通配符语法，流式产出记录及其在文件中的偏移量。

**`_TextCollectorTracker`**（#913–984）：收集记录上下文摘要的追踪器，用于保留前后文而不保存完整 JSON。

**`JsonWalker`**（#986–1188）：高层封装，集成配置（`record_path`、`context`、`fields`），协调扫描器和收集器，对外提供 `iter_chunks()` 流式接口。

---

## 第十三部分：索引器 `indexer.py`

`indexer.py`（358 行）是索引流程的主控制器，负责协调发现文件、抽取内容、分段、写入数据库等步骤。

### 关键流程

**`_discover_files()`**：递归扫描目录，过滤支持的文件类型，跳过忽略模式匹配的文件。

**`Indexer.index_directory()`**（#85–170）：主索引方法。遍历文件列表，对每个文件：
1. 调用 `BuiltinExtractor.extract()` 抽取内容。
2. 调用 `KnowledgeBase.is_unchanged()` 检查是否需要更新。
3. 如果已变化，调用 `iter_document_text()` 获取文本流，`iter_chunk_text()` 分段，`replace_document()` 写入。

**进度报告**：通过 `yield IndexProgress` 事件让 CLI 或 Web 界面实时显示进度。

**JSON 文件特殊处理**：当文件类型为 JSON 时，使用 `JsonWalker.iter_chunks()` 而不是通用分段器。

---

## 第十四部分：CLI 命令行界面 `cli.py`

`cli.py`（577 行）使用 `argparse` 构建子命令式 CLI，支持 `index`、`search`、`list`、`stats`、`prune`、`health`、`remove`、`web`、`export` 等 9 个子命令。

### `index` 子命令（#175–260）
- 接受 `--directory`、`--file`、`--workers`（线程数增量索引）、`--reindex` 等参数。
- 调用 `Indexer.index_directory()` 并消费 `IndexProgress` 事件打印进度。

### `search` 子命令（#262–340）
- `--query`、`--limit`、`--file-type`、`--path` 参数过滤。
- 调用 `KnowledgeBase.search()` 返回 `SearchResult`，打印表格，包括高亮文本和相邻分段（`--context`）。

### `web` 子命令（#430–470）
- 启动 `create_server()`，绑定 `--host`/`--port`。

### 其他子命令
- `list`：列出已索引文档。
- `stats`：文档和分段计数的概览。
- `prune`：删除数据库中源文件已不存在的记录。
- `health`：运行 `check_health()` 报告一致性。
- `remove`：按路径删除特定文档。
- `export`：将搜索结果导出为 JSONL。

---

## 第十五部分：RAG 子包

### `rag/__init__.py`（#1–19）

```python
from .answer import answer_question
from .retriever import KeywordRetriever

__all__ = ["KeywordRetriever", "answer_question"]
```

- 子包的公开接口，提供检索器和问答入口。

### `rag/prompt.py`（#39 行）

定义 RAG 提示模板。`build_messages(query, context)` 构造系统消息和用户消息，严格遵守不可信上下文原则：用户消息中明确区分"已知上下文"和"用户提问"两部分，并指令模型只基于给定上下文回答，不确定时输出 "无法确定"。

### `rag/llm_client.py`（#171 行）

```python
class LLMClient:
    def __init__(self, api_key: str, base_url: str, model: str):
```

- 使用标准库 `urllib` 向 OpenAI 兼容的 `/chat/completions` API 发送请求，不引入 `openai` 或 `requests` 依赖，保证安装最小化。
- `complete(messages)` 方法：序列化请求体、设置 `Authorization: Bearer` 头并解析非流式响应。
- 错误处理：API 返回非 200 或 JSON 解析失败时抛出已脱敏的 `LLMClientError`。
- API key 在 `RAG_RECORD` 日志和 Web 错误响应中都会被自动遮蔽，防止日志泄露密钥。

### `rag/retriever.py`（#268 行）

```python
class KeywordRetriever:
    def retrieve(self, query: str, db: KnowledgeBase) -> list[SearchResult]:
```

- 使用 `KnowledgeBase.search()` 执行关键词搜索。
- 对命中结果执行相邻窗口展开（`chunk_window(radius=1)`），确保召回上下文完整。
- 受字符预算约束（`max_context_chars`），避免超出 LLM 上下文窗口。
- 结果去重和排序。

### `rag/answer.py`（#244 行）

```python
def answer_question(query: str, db: KnowledgeBase, client: LLMClient) -> AnswerRecord:
```

- 编排完整的 RAG 流程：检索 → 构建 Prompt → 调用 LLM → 验证引用 → 返回结果。
- `CitationValidationError`：验证模型回答中的引用是否真的存在于检索上下文中，不存在的引用被标记为"无根据"。
- 返回 `AnswerRecord`（dataclass），包含 query、context、answer、citations、validation 等字段，便于评估。
- `RAG_RECORD` 日志记录完整的请求/响应，用于实验分析。

---

## 第十六部分：Web 子包

### `web/__init__.py`（#10 行）

```python
from .app import KnowledgeWebApp, create_server, run_web
__all__ = ["KnowledgeWebApp", "create_server", "run_web"]
```

### `web/app.py`

基于标准库 `http.server` 的 HTTP 服务，多线程处理请求。

**`KnowledgeWebApp`**（业务门面）：
- `stats()`、`documents()`：每次请求打开独立 SQLite 连接，读取统计和文档元数据。
- `search()`：复用 jieba + FTS5/LIKE 搜索，并返回服务端高亮结果。
- `ask()`：复用 `KeywordRetriever` 和 `RagAnswerer`，只把实际检索来源序列化给浏览器。
- `index_paths()`、`save_upload()`、`remove()`：完成导入、上传安全校验和级联删除。

**`KnowledgeRequestHandler`**：
- `do_GET()`：提供静态文件（`/` → `index.html`）和 `/api/stats`、`/api/documents`、`/api/search`。
- `do_POST()`：处理 JSON 搜索、问答、目录索引、删除，以及 `multipart/form-data` 文件上传。
- `_read_json_object()`、`_read_upload()`：限制请求体、验证对象结构、扩展名、路径和 512 MiB 大小上限。

**`create_server()`**：工厂函数创建 `ThreadingHTTPServer` 实例。
**`run_web()`**：启动服务器的便捷入口。

### `web/static/index.html`

单页面应用入口。包含搜索框、文档列表、RAG 问答界面。使用 Fetch API 与后台通信。

### `web/static/app.css`

浅色工作台主题 CSS。响应式布局，支持桌面和移动端。针对搜索结果和 RAG 回答设计了专用的样式（引用标记、高亮文本等）。

### `web/static/app.js`

前端 JavaScript 逻辑：
- 搜索：用户输入后调用 `GET /api/search`，渲染带高亮的结果。
- 文档列表：调用 `GET /api/documents`。
- RAG 问答：调用 `POST /api/ask`，显示答案、引用、耗时和 token 用量。
- 文件上传：使用 `FormData` 上传文件触发索引。

---

## 第十七部分：脚本

### `scripts/run_rag_eval.py`（#57 行）

加载 `experiments/rag-grounding-eval/eval-cases.json` 测试用例，逐条调用 RAG pipeline 并输出评估结果。

### `scripts/clean_rag_log.py`（#298 行）

清洗 RAG 日志文件。过滤敏感信息（API key）、提取关键字段、输出结构化格式。

### `scripts/probe_citation_failure.py`（#126 行）

引用失败探针。模拟各种输入场景验证 `CitationValidationError` 的正确触发行为。

---

## 第十八部分：测试

`tests/` 目录包含 84 个测试用例（全部通过），覆盖以下文件：

- `test_chunking.py`（#51）：分段逻辑测试，验证 `iter_chunk_text` 和 `chunk_text` 在不同 `chunk_size` 和 `overlap` 下的行为。
- `test_cleaning.py`（#28）：文本清洗测试，验证空白字符压缩。
- `test_database.py`（#94）：数据库基本操作测试（CRUD、搜索、健康检查）。
- `test_extractors.py`（#81）：文件抽取测试，验证各格式的抽取结果。
- `test_highlighting.py`（#28）：高亮搜索词测试。
- `test_indexer.py`（#191）：索引流程集成测试（发现文件、增量索引、重索引）。
- `test_tokenization.py`（#40）：分词和 FTS5 查询构造函数测试。
- `test_json_parser.py`（#364）：JSON 解析器全覆盖测试，包括边界情况和大文件降级。
- `test_rag.py`（#627）：RAG 流程完整测试（检索、提示构造、引用验证）。
- `test_web.py`（#176）：Web API 集成测试，使用 `http.server` 启动测试服务器。
- `test_cli_integration.py`（#123）：CLI 端到端测试。

---

## 第十九部分：实验与评估

### `experiments/rag-grounding-eval/`

- `eval-cases.json`：147 条评估用例，每条包含 query、expected_context、expected_answer、citations。
- `controlled-facts.md` / `controlled-facts-secondary.md`：受控事实文档，用于构造测试检索语境。
- `cleaned-report.md` / `citation-validated-cleaned-report.md`：评估报告。
- `ablation_no_context.py`：消融实验脚本，测试无上下文时模型行为。

### 实验方法
RAG 评估使用三类指标：
1. **引用召回率**：模型回答引用中的事实在给定上下文中是否确实存在。
2. **引用精确率**：模型回答引用是否都是上下文相关的（无幻觉）。
3. **回答完整性**：模型是否涵盖了问题所有关键信息。

---

## 第二十部分：README 与文档

### `README.md`（#296 行）

项目完整说明，包含：
- **快速开始**：安装依赖、创建 `.env` 配置、索引文档、搜索、启动 Web 界面。
- **使用示例**：CLI 和 Web 两种使用方式的具体命令和截图。
- **架构概述**：数据流图（discover → extract → chunk → index → search）。
- **开发说明**：运行测试、贡献指南。

### `docs/` 目录

- `v1-xmind-outline.md`：V1 版本的 XMind 大纲，记录原始设计思路。
- `v1-search-validation.md`：V1 搜索验证设计文档。
- `v2-qa-samples.md`：V2 版本的问答样例。
- `experiment-log.md`：实验日志，记录各次实验配置和结果。
- `code-walkthrough.md`：V2 版本的代码走读（部分过时）。
- `v3-code-walkthrough.md`：**本文档**，V3 全代码解析。
- `json-config.example.json` / `json-data.example.json`：JSON 解析器配置示例和测试数据。

---

## 总结

`personal_local_knowledge_base_v0` 是一个**纯标准库实现的本地知识库系统**，核心设计理念包括：

1. **流式处理**：文件发现、文本提取、清洗、分段和 JSON 解析均支持流式，可以处理超出物理内存的大文件。
2. **三层搜索**：jieba FTS5 → 原始 FTS5 → LIKE 回退，兼顾中文词边界准确性和通用性。
3. **FTS5 external content**：通过 SQLite 触发器和 external content 表避免数据冗余，全文索引不额外占用磁盘。
4. **配置驱动 JSON 解析**：`record_path` + `context` + `fields` 配置描述任意嵌套 JSON 结构，无需为每种 JSON 格式编写专用解析代码。
5. **RAG 引用验证**：`CitationValidationError` 确保模型回答中的每个引用都能在检索上下文中找到事实依据，可审计可评估。
6. **零运行时依赖**：Web 服务使用标准库 `http.server`，LLM 客户端使用标准库 `urllib`，不引入任何框架级依赖。
7. **增量索引**：基于文件 SHA-256 和解析配置指纹判断是否需要重建索引，日常使用中显著加速。`
