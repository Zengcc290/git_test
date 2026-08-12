# V1 基础搜索结果验证

这是一次历史性的基础搜索结果记录。原来的临时验证夹具已按当前项目需求移除；每个查询使用 `limit=5`，当时的实际返回文档按结果顺序记录如下。

| 查询词 | 预期命中文档 | 实际返回文档（Top-5） | Top-1 | Top-5 包含 |
| --- | --- | --- | --- | --- |
| `virtualenv` | `python.md` | `python.md` | 是 | 是 |
| `FTS5` | `sqlite.md` | `sqlite.md` | 是 | 是 |
| `中文搜索` | `chinese-search.md` | `chinese-search.md` | 是 | 是 |
| `OCR` | `pdf.md` | `pdf.md` | 是 | 是 |
| `grouped shapes` | `pptx.md` | `pptx.md` | 是 | 是 |
| `overlap` | `chunking.md` | `chunking.md` | 是 | 是 |
| `SHA-256` | `incremental-index.md` | `incremental-index.md` | 是 | 是 |
| `health checks` | `cli.md` | `cli.md` | 是 | 是 |
| `database records` | `prune.md` | `prune.md` | 是 | 是 |
| `subprocess` | `testing.md` | `testing.md` | 是 | 是 |

结果：10/10 个查询 Top-1 正确，10/10 个查询的 Top-5 包含预期文档。本记录只验证基础关键词召回，不代表语义检索或 RAG 生成质量。
