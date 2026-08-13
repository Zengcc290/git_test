# 个人本地知识库搜索工具 V1

这是一个不带聊天机器人的本地文档搜索引擎。它把 `.txt`、`.md`、PDF、`.pptx` 和配置化 `.json` 内容导入 SQLite，清洗并分段后使用 SQLite FTS5 做关键词搜索，命令行返回带高亮的上下文。

## 功能

- 导入 TXT、Markdown、PDF、PPTX 文本和配置化 JSON 记录
- 流式读取、清洗、分段和写入，避免大文件全文同时驻留内存
- 统一换行和空白，保留标题与正文
- 按段落分段，超长段落按标点/空格切分并保留重叠
- SQLite 文档表、分段表和 FTS5 全文索引
- jieba 中文词索引优先检索，原始 FTS5 和参数化 LIKE 分级兜底
- 文件 SHA-256 增量索引，重复运行会跳过未变化文件
- 目录排除规则、最大文件数限制和超大 JSON 大小保护
- 索引过程中显示当前文件和总进度
- 命令行查询、结果排序、路径/分段信息和命中高亮
- 控制台日志、文件日志、单文件异常隔离
- Python `unittest` 回归测试，覆盖正式索引链路和 JSON 流式解析
- 实验过程记录见 [`docs/experiment-log.md`](docs/experiment-log.md)

## 环境准备

所有项目命令都使用项目自己的虚拟环境。在 PowerShell 中运行：

```powershell
cd C:\Users\liang\Desktop\code\git_test\personal_local_knowledge_base_v0
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

如果 `.venv` 已存在，不需要重复创建；依赖安装和后续运行仍使用 `.venv\Scripts\python.exe`。

## 快速使用

先初始化数据库（首次执行 `index` 也会自动初始化）：

```powershell
.\.venv\Scripts\python.exe -m knowledge_search init-db
```

索引少量默认示例文档：

```powershell
.\.venv\Scripts\python.exe -m knowledge_search index `
  .\sample_documents\python-notes.txt `
  .\sample_documents\search-design.md `
  .\sample_documents\redox_reactions_dynamic.pptx `
  --max-files 20
```

索引目录时可用 `--exclude-dir` 重复添加目录名、通配符或相对路径；默认会排除 `.git`、`.venv`、`__pycache__`、`node_modules`、`build` 和 `dist`。`--max-files 0` 表示不限制。JSON 文件大小保护通过 `--max-json-size` 控制；索引默认最多处理 512 MiB，超过上限会跳过并在汇总中报告。

搜索关键词：

```powershell
.\.venv\Scripts\python.exe -m knowledge_search search SQLite
.\.venv\Scripts\python.exe -m knowledge_search search 本地 --limit 5 --no-color
```

不加 `--no-color` 时，终端使用 ANSI 黄色高亮；`--no-color` 会使用 `[[命中词]]` 标记，方便重定向和查看日志。

查看统计信息：

```powershell
.\.venv\Scripts\python.exe -m knowledge_search stats
```

常用选项：

```powershell
.\.venv\Scripts\python.exe -m knowledge_search index .\my-docs `
  --exclude-dir cache --exclude-dir 'generated/*' `
  --max-files 1000 --max-json-size 1GB
.\.venv\Scripts\python.exe -m knowledge_search index .\my-docs --chunk-size 800 --overlap 100 --force
.\.venv\Scripts\python.exe -m knowledge_search search "FTS5 SQLite" --db .\data\knowledge.db --limit 10
```

每个命令都支持 `--db`、`--log-file` 和 `--log-level`。默认数据库为 `data/knowledge.db`，默认日志为 `logs/app.log`。

## 目录结构

```text
knowledge_search/       核心 Python 包
  extractors.py          TXT/Markdown/PDF/PPTX/JSON 抽取入口
  json_parser.py         配置化 JSON 解析和流式结构扫描
  cleaning.py            文本清洗
  chunking.py            文本分段
  database.py            SQLite 与 FTS5
  indexer.py             文件发现和增量索引
  cli.py                 命令行入口
sample_documents/        可直接运行的示例文档
data/                    数据库目录（数据库文件被 git 忽略）
docs/experiment-log.md   实验记录
```

## 运行测试

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

测试使用临时目录，不会污染正式数据库；缺少 `pypdf` 或 `python-pptx` 时，对应抽取测试会自动跳过。

索引过程不会调用 `read_bytes()` 读取整个文件。TXT/Markdown 按固定大小读取并增量解码，普通 JSON 记录逐条读取；记录先在 512 MiB 探测窗口内确认完整性，实际读取块仍为固定大小。如果一条记录超过探测窗口，则保持记录边界，改为原始文本分块流式传递，不把整条记录放入内存。若整个 JSON 文件也超过文件大小保护，需显式使用 `--max-json-size 0` 才允许继续扫描。PDF 按页抽取，PPTX 按幻灯片抽取；清洗器、分段器和 SQLite 写入也通过迭代器逐步传递数据。

搜索会优先使用 jieba 生成的中文词索引，再由 FTS5 的 BM25 计算相关性；如果 jieba 词索引没有命中，会回退到原始文本 FTS5，最后才使用参数化 `LIKE`。因此 jieba 负责改善中文词边界和召回，FTS5 负责排序，二者不是互相替代关系。

## 配置化 JSON 索引

JSON 文件通过配置文件解析。配置可以指定记录路径、参与索引的字段、数组拼接方式和过滤条件。`index_mode` 默认为 `record`，表示每条 JSON 记录独立分段；改为 `file` 可将配置选中的所有记录合并为整个文件索引。

示例配置见 [`docs/json-config.example.json`](docs/json-config.example.json)。例如：

```powershell
.\.venv\Scripts\python.exe -m knowledge_search json-preview .\docs\json-data.example.json --json-config .\docs\json-config.example.json --limit 3
.\.venv\Scripts\python.exe -m knowledge_search index .\docs --json-config .\docs\json-config.example.json --max-files 100
```

配置中的 `record_path` 支持 `$` 根节点、点号字段、数组下标和 `[*]`，例如 `$.data.items[*]`；读取器会跳过无关字段，只将命中的一条普通记录解析到内存后立即交给下游。单条记录超过 512 MiB 探测窗口时，会原样分块传递，索引时不再应用字段选择和过滤条件；`json-preview` 和 `json-structure` 需要完整对象，因此遇到这种记录会报错。`fields[].path` 默认相对于每条记录；使用嵌套 `record_path` 时不支持以 `$` 开头从完整根节点读取字段。

### 查看超大 JSON 的字段目录

`json-structure` 会复用正式解析器按块读取 JSON Lines 或顶层数组，只输出字段路径、类型和出现次数，不打印正文，也不会把整个文件载入内存。默认扫描前 100 条记录，且结构扫描默认不设文件大小上限；`--max-records 0` 才会扫描到文件末尾。

```powershell
.\.venv\Scripts\python.exe -m knowledge_search json-structure `
  .\sample_documents\wikipedia-zh-cn-20260501.json `
  --max-records 100
```

你的 `wikipedia-zh-cn-20260501.json` 是 JSON Lines，单条记录的字段可用 `$.id`、`$.title`、`$.tags` 和 `$.text` 读取；后续若要建立索引，可使用 `record_path` 为 `$` 的 JSON 配置，让每条顶层对象独立分段，并根据数据规模设置 `--max-files` 和 `--max-json-size`。

`--max-json-size` 和 `--json-record-probe-size` 都支持人类可读大小：`B`、`KB`、`MB`、`GB`、`TB`（不区分大小写，也支持 `KiB`、`MiB`、`GiB`、`TiB`）；不带单位的纯数字仍按字节处理。例如 `512MB`、`1GB`、`1.5GB`。换算采用 1024 进制。它们分别控制整个文件上限和单条记录探测窗口。要处理总大小超过 512 MiB、但仍希望按记录流式读取的 JSON，可使用：

```powershell
.\.venv\Scripts\python.exe -m knowledge_search index .\large-json `
  --json-config .\docs\json-config.example.json `
  --max-json-size 1GB --json-record-probe-size 512MB
```

输入 `--max-json-size 0` 表示关闭文件大小限制。

## V1 命令与验收

V1 增加了可管理、可验证的知识库操作。所有命令都可以追加 `--db`、`--log-file` 和 `--log-level`。

```powershell
# 列出文档、类型、大小、分段数和索引时间
.\.venv\Scripts\python.exe -m knowledge_search list

# 删除一个已索引文档；路径可以是相对路径或绝对路径
.\.venv\Scripts\python.exe -m knowledge_search remove ".\sample_documents\search-design.md"

# 清理源文件已经不存在的索引记录
.\.venv\Scripts\python.exe -m knowledge_search prune

# 检查 chunks、chunk_tokens 和两套 FTS5 索引的一致性
.\.venv\Scripts\python.exe -m knowledge_search check-db
```

搜索支持组合过滤：

```powershell
.\.venv\Scripts\python.exe -m knowledge_search search SQLite --type md
.\.venv\Scripts\python.exe -m knowledge_search search Python --path .\sample_documents
.\.venv\Scripts\python.exe -m knowledge_search search SQLite --type md --path .\sample_documents
```

`--type` 支持 `txt`、`md`、`pdf`、`pptx` 和 `json`；`--path` 既可以指向单个文件，也可以指向目录。删除后，文档的分段、原始 FTS5 索引和中文 FTS5 索引会通过 SQLite 触发器一起清理。删除不存在的路径会给出提示并返回非零状态；`prune` 没有需要清理的记录时返回 0。

`check-db` 在健康数据库返回 0；发现孤立 chunks、FTS5 数量或 rowid 不一致、缺失 token 行、无分段文档时返回 1 并打印诊断信息。

## V1 范围与限制

V0 只做关键词搜索，不做问答、对话、Embedding、向量数据库和远程 API。PDF 仅支持有文本层的文件，扫描版 PDF 暂不做 OCR；PPTX 目前抽取幻灯片文本框、标题、表格和组合图形文字，不处理图片中的文字、图表内部文字或演讲者备注。JSON 解析支持 JSON Lines 和顶层数组的逐条流式读取；超过探测窗口的单条记录会按原始记录边界分块进入索引，但 `json-preview`/`json-structure` 仍要求记录可以完整解析。jieba 词索引会增加首次建库时间和少量磁盘占用，但可以减少中文查询对低相关 `LIKE` 结果的依赖。
