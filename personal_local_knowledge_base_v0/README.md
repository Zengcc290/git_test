# 个人本地知识库搜索工具 V0

这是一个不带聊天机器人的本地文档搜索引擎。它把 `.txt`、`.md`、PDF 和 `.pptx` 文本导入 SQLite，清洗并分段后使用 SQLite FTS5 做关键词搜索，命令行返回带高亮的上下文。

## 功能

- 导入 TXT、Markdown、PDF 和 PPTX 文本
- 流式读取、清洗、分段和写入，避免大文件全文同时驻留内存
- 统一换行和空白，保留标题与正文
- 按段落分段，超长段落按标点/空格切分并保留重叠
- SQLite 文档表、分段表和 FTS5 全文索引
- jieba 中文词索引优先检索，原始 FTS5 和参数化 LIKE 分级兜底
- 文件 SHA-256 增量索引，重复运行会跳过未变化文件
- 命令行查询、结果排序、路径/分段信息和命中高亮
- 控制台日志、文件日志、单文件异常隔离
- Python `unittest` 单元测试
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

索引示例文档：

```powershell
.\.venv\Scripts\python.exe -m knowledge_search index .\sample_documents
```

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
.\.venv\Scripts\python.exe -m knowledge_search index .\my-docs --chunk-size 800 --overlap 100 --force
.\.venv\Scripts\python.exe -m knowledge_search search "FTS5 SQLite" --db .\data\knowledge.db --limit 10
```

每个命令都支持 `--db`、`--log-file` 和 `--log-level`。默认数据库为 `data/knowledge.db`，默认日志为 `logs/app.log`。

## 目录结构

```text
knowledge_search/       核心 Python 包
  extractors.py          TXT/Markdown/PDF/PPTX 抽取
  cleaning.py            文本清洗
  chunking.py            文本分段
  database.py            SQLite 与 FTS5
  indexer.py             文件发现和增量索引
  cli.py                 命令行入口
tests/                   单元测试
sample_documents/        可直接运行的示例文档
data/                    数据库目录（数据库文件被 git 忽略）
docs/experiment-log.md   实验记录
```

## 运行测试

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

测试只使用临时目录，不会污染正式数据库。SQLite FTS5 需要当前 Python 自带的 SQLite 编译时启用；本项目已在开发环境中验证。

索引过程不会调用 `read_bytes()` 读取整个文件。TXT/Markdown 按固定大小读取并增量解码，PDF 按页抽取，PPTX 按幻灯片抽取；清洗器、分段器和 SQLite 写入也通过迭代器逐步传递数据。内存占用主要取决于单个读取块、当前分段和底层 PDF/PPTX 库的页面/演示文稿对象，而不是整个文档的文本总量。

搜索会优先使用 jieba 生成的中文词索引，再由 FTS5 的 BM25 计算相关性；如果 jieba 词索引没有命中，会回退到原始文本 FTS5，最后才使用参数化 `LIKE`。因此 jieba 负责改善中文词边界和召回，FTS5 负责排序，二者不是互相替代关系。

## V0 范围与限制

V0 只做关键词搜索，不做问答、对话、Embedding、向量数据库和远程 API。PDF 仅支持有文本层的文件，扫描版 PDF 暂不做 OCR；PPTX 目前抽取幻灯片文本框、标题、表格和组合图形文字，不处理图片中的文字、图表内部文字或演讲者备注。jieba 词索引会增加首次建库时间和少量磁盘占用，但可以减少中文查询对低相关 `LIKE` 结果的依赖。
