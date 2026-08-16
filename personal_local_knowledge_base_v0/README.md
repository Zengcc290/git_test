# 个人本地知识库搜索工具 V3

这是一个本地文档搜索和基础 RAG 问答工具。它把 `.txt`、`.md`、PDF、`.pptx` 和配置化 `.json` 内容导入 SQLite，使用 SQLite FTS5 检索相关分段，再把有长度限制的上下文交给 OpenAI 兼容的大模型生成带引用的答案。

## V3 网页界面

V3 在现有 FTS5 + RAG 链路上增加了无需第三方 Web 框架的本地网页服务。先安装依赖，再启动：

```powershell
.\.venv\Scripts\python.exe -m knowledge_search web
```

浏览器打开 <http://127.0.0.1:8000/>。页面包含搜索、问答、导入和文档管理四个视图：

- 搜索：关键词检索、FTS5 排序和命中高亮。
- 问答：复用关键词 RAG，展示答案、耗时、token 和实际引用来源；无资料时拒答。
- 导入：上传 TXT/Markdown/PDF/PPTX/JSON，或提交本机目录批量索引。
- 文档：查看元数据并删除文档及其 FTS5 分段。

网页默认监听 `127.0.0.1:8000`，可以通过 `--db`、`--host`、`--port` 和 `--upload-dir` 调整。上传服务限制文件类型、文件名路径、请求体和 512 MiB 文件大小；API 错误会以 JSON 返回，LLM API Key 会脱敏。

```powershell
.\.venv\Scripts\python.exe -m knowledge_search web --port 9000 --db .\data\knowledge.db --upload-dir .\uploads
```

浏览器到 API 再到 SQLite/RAG 的数据流、逐模块代码讲解见 [`docs/v3-code-walkthrough.md`](docs/v3-code-walkthrough.md)，十条网页问答验收记录见 [`docs/v3-web-acceptance.md`](docs/v3-web-acceptance.md)。

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
- 基于现有 FTS5 的 Top-K 关键词 RAG 问答
- 严格上下文 Prompt、无资料拒答、文件与分段引用
- OpenAI 兼容 API、响应时间及 token 使用量记录
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

复制示例文件并在项目根目录创建 `.env`：

```powershell
Copy-Item .env.example .env
```

编辑 `.env`：

```dotenv
LLM_API_KEY=你的密钥
LLM_BASE_URL=https://api.example.com/v1
LLM_MODEL=模型名称
```

然后直接进行文档问答：

```powershell

.\.venv\Scripts\python.exe -m knowledge_search ask "SQLite FTS5 是什么？"
```

程序会自动读取当前项目的 `.env`。已有的系统环境变量优先级更高，不会被 `.env` 覆盖。`.env` 已加入 Git 忽略规则，只提交不含真实密钥的 [`.env.example`](.env.example)。`LLM_BASE_URL` 填 OpenAI 兼容 API 的版本根地址（通常以 `/v1` 结尾），程序会调用其 `/chat/completions`；也可以直接填写完整的 `/chat/completions` 地址。三个大模型参数不会写入普通 RAG 配置或日志。

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
  rag/                    检索、Prompt、模型客户端和回答编排
  cli.py                 命令行入口
configs/rag.json         不含密钥的 RAG 配置
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

## V2 基础 RAG 问答

`ask` 复用 V1 的 SQLite FTS5 检索，不使用向量数据库或 Agent。默认读取 [`configs/rag.json`](configs/rag.json)：

```json
{
  "top_k": 5,
  "max_context_chars": 12000,
  "temperature": 0
}
```

可使用另一份非敏感配置，或为单次命令覆盖参数：

```powershell
.\.venv\Scripts\python.exe -m knowledge_search ask "如何使用 FTS5？" `
  --rag-config .\configs\rag.json `
  --top-k 3 --max-context-chars 8000 --temperature 0
```

命令输出答案、引用文件、分段编号、响应时间、上下文字符数和 API 返回的 token 使用量。完整的问题、检索来源、回答、耗时和 token 指标以 `RAG_RECORD` JSON 记录到日志；日志不会记录 API Key、请求头或模型服务地址。无匹配分段时程序不会调用大模型，并直接输出“根据当前知识库资料，无法回答该问题。”；API 配置缺失、网络异常、HTTP 错误或响应格式异常会返回简明错误和非零状态。

Prompt 明确要求模型只依据检索上下文回答，把文档片段视为不可信数据，并要求逐句使用 `[1]`、`[2]` 引用。正式回答链路还会强制校验模型文本：非拒答答案必须至少包含一个属于本次检索结果的 `[n]`，只要出现任一不存在的引用（包括合法与非法引用混合）就整次失败。无引用或错误引用不会被自动补写、不会修改模型原文，也不会记录成 `rag_answer`；CLI 返回非零状态并写入脱敏的 `rag_error`，其中保留已产生的响应时间和 token 使用量。拒答答案可以不带引用，但若带了非法引用同样失败。

CLI 会独立列出实际传给模型的来源，便于人工核对。10 条实际问答和逐事实验收结果见 [`docs/v2-qa-samples.md`](docs/v2-qa-samples.md)。

可用本地假模型端到端复现“无引用答案必须失败”，不消耗真实模型额度：

```powershell
.\.venv\Scripts\python.exe -m scripts.probe_citation_failure `
  --log-output experiments\rag-grounding-eval\citation-failure-probe.log `
  --result-output experiments\rag-grounding-eval\citation-failure-probe-result.json
```

探针会启动真实 `ask` 子进程，并断言退出码为 1、日志只有 `rag_error` 而没有 `rag_answer`、token 用量得到保留、API Key 已脱敏。

大语料 grounding 评估可复现运行（先确保两份受控记录已索引）：

```powershell
.\.venv\Scripts\python.exe -m knowledge_search index `
  experiments\rag-grounding-eval\controlled-facts.md `
  experiments\rag-grounding-eval\controlled-facts-secondary.md `
  --db data\knowledge.db

.\.venv\Scripts\python.exe -m scripts.run_rag_eval `
  experiments\rag-grounding-eval\eval-cases.json `
  --db data\knowledge.db `
  --log-file experiments\rag-grounding-eval\citation-validated-eval-20260813.log

.\.venv\Scripts\python.exe scripts\clean_rag_log.py `
  experiments\rag-grounding-eval\citation-validated-eval-20260813.log `
  experiments\rag-grounding-eval\eval-cases.json `
  --db data\knowledge.db `
  --ablation-result experiments\rag-grounding-eval\ablation-no-context-result.json `
  --jsonl-output experiments\rag-grounding-eval\citation-validated-cleaned.jsonl `
  --report-output experiments\rag-grounding-eval\citation-validated-cleaned-report.md
```

固定评估运行器每次会覆盖指定日志，避免混入旧记录；清洗后若任一用例不通过，清洗命令返回非零状态。

本次评估使用 16,901 篇文档、29,522 个分段，包含 THUCNews 真实新闻细节、两组随机受控事实、资料缺失拒答和跨文档引用。清洗报告见 [`experiments/rag-grounding-eval/citation-validated-cleaned-report.md`](experiments/rag-grounding-eval/citation-validated-cleaned-report.md)，固定用例见 [`eval-cases.json`](experiments/rag-grounding-eval/eval-cases.json)：10/10 条通过，55/55 个事实同时出现在模型答案和答案实际引用的分段中。不提供检索上下文的消融脚本见 [`ablation_no_context.py`](experiments/rag-grounding-eval/ablation_no_context.py)：同一模型对第一组随机事实回答“不知道”，而带 RAG 时精确回答 8/8。

## 当前范围与限制

V3 仍是无会话的关键词 RAG，不做 Agent、Embedding、向量数据库、重排模型或流式输出。程序能保证回答至少引用本次检索来源且不含越界引用，但引用格式合法不等于每句话在语义上都被来源支持，因此仍需结合逐事实评估检查幻觉。PDF 仅支持有文本层的文件，扫描版 PDF 暂不做 OCR；PPTX 目前抽取幻灯片文本框、标题、表格和组合图形文字，不处理图片中的文字、图表内部文字或演讲者备注。Embedding、混合检索和召回率对比留到 V4。
