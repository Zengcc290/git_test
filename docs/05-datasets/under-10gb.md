# 10 GB 以内的可用数据集

本清单针对当前项目的能力：本地文档搜索、中文分词、SQLite FTS5，以及 TXT/Markdown/PDF/PPTX 文本导入。

核验日期：2026-08-11。这里区分两种情况：

- **固定数据集不超过 10 GB**：下载整个候选集即可满足限制。
- **大数据集的可控子集**：原始数据超过 10 GB，但可以按快照、语言、站点或分片取不超过 10 GB 的部分。

## 最推荐的组合

| 组合 | 内容 | 原始数据量（约） | 适合用途 |
| --- | --- | ---: | --- |
| 中文知识库 | 中文 Wikipedia 单个快照 + THUCNews | 2.39 GB + 2.19 GB = **4.58 GB** | 通用中文百科、新闻全文搜索 |
| 中文知识库 + 代码 | 上一组合 + CodeSearchNet | **约 5.1 GB**（Hugging Face 版本） | 中文知识与代码/注释混合搜索 |
| 中文知识库 + 代码小样本 | 上一组合 + The Stack Smol | **约 7.5 GB** | 30 种编程语言的代码文档搜索 |

注意：这里是源数据体积。解压、转换成 TXT/Markdown、SQLite 数据库、FTS5 索引和日志会额外占用空间；建议至少预留源数据体积的 2–4 倍磁盘空间。

## 固定数据集：不超过 10 GB

### 1. 中文 Wikipedia 单个快照：2.12–2.39 GB

- 入口：[Hugging Face 中文 Wikipedia JSONL 快照](https://huggingface.co/datasets/fjcanyue/wikipedia-zh-cn)
- 官方来源：[Wikimedia zhwiki dump](https://dumps.wikimedia.org/zhwiki/latest/)
- 最新可选快照：`wikipedia-zh-cn-20260501.json`，页面列出的大小约 **2.39 GB**。
- 内容：中文百科条目，JSON Lines，每行包含 `text` 等字段。
- 许可：数据卡提示以 Wikipedia 的 GFDL 1.3、CC BY-SA 4.0 等原始协议为准。
- 适配方式：抽取 `text` 字段为 `.txt` 或 `.md` 后即可进入现有索引器；官方 XML dump 则需要先用 WikiExtractor 类工具转换。

这是最适合当前项目的首个数据集。不要把该 Hugging Face 仓库的所有日期快照一起下载，页面显示全部快照合计约 13.4 GB；只下载一个日期即可满足 10 GB 限制。

### 2. THUCNews：2.19 GB

- 入口：[清华大学 THUCTC 官方 GitHub](https://github.com/thunlp/THUCTC)
- 内容：约 74 万篇中文新闻文档，14 个类别，UTF-8 纯文本。
- 体积：官方 README 明确写明 **2.19 GB**。
- 适配方式：基本可以直接放入 `data/raw` 后索引，不需要 JSON/Parquet 转换。
- 注意：代码仓库是 MIT；数据下载需要在项目 README 指向的站点填写信息，数据本身应按下载站点条款使用。

它比训练用网页语料更适合作为搜索项目的真实文档集，新闻标题、分类目录和长文本都能检验分段与高亮效果。

### 3. The Stack Smol：2.95 GB

- 入口：[Hugging Face `bigcode/the-stack-smol`](https://huggingface.co/datasets/bigcode/the-stack-smol)
- 内容：The Stack 的约 0.1% 小样本，30 种编程语言，每种语言约 10,000 个样本，约 300,000 行/文件记录。
- 体积：数据卡显示 **2.95 GB**。
- 格式：Parquet/Hugging Face Dataset，字段包括 `content`、`lang`、`path`、`licenses`。
- 适配方式：把每条记录的 `content` 写成 Markdown 或 TXT；建议把语言、仓库路径和许可证写入文件头。
- 注意：需要接受 The Stack 使用条款；代码来源的原始许可证仍然有效，不能把它当成统一 MIT/Apache 数据集。

### 4. TinyStories：7.62 GB

- 入口：[Hugging Face `roneneldan/TinyStories`](https://huggingface.co/datasets/roneneldan/TinyStories)
- 内容：GPT-3.5/GPT-4 生成的英文短故事，合成数据，适合压力测试和分段测试。
- 体积：数据卡显示 **7.62 GB**。
- 许可：数据卡标记为 CDLA-Sharing-1.0。
- 适配方式：TXT 版本可直接索引。
- 限制：不是真实知识库，不建议作为生产知识来源；适合验证大目录、长时间索引、重复查询和内存占用。

### 5. ChineseWebText 2.0 的毒性标注子集：3.16 GB

- 入口：[Hugging Face `CASIA-LM/ChineseWebText2.0`](https://huggingface.co/datasets/CASIA-LM/ChineseWebText2.0)
- 内容：约 1,632,620 条中文网页文本，包含毒性分数/标签；数据卡称该子集约 **3.16 GB**。
- 许可：数据卡标记 Apache-2.0；使用时仍应保留数据来源和论文信息。
- 适合用途：中文安全搜索、敏感内容过滤、误召回分析和评测。
- 限制：ChineseWebText 2.0 全量约 3.8 TB，3.16 GB 是毒性子集，不是通用中文知识库；不建议把它作为第一个主数据源。

## 可控子集：从大库取 10 GB 以内

### 6. FineWeb2 中文子集的 10 GB 采样

- 入口：[Hugging Face `HuggingFaceFW/fineweb-2`](https://huggingface.co/datasets/HuggingFaceFW/fineweb-2)
- 全量：约 20.2 TB；普通话 `cmn_Hani` 子集约 1.48 TB。
- 许可：ODC-By 1.0，并受 Common Crawl 条款约束。
- 做法：只流式读取 `cmn_Hani`，累计输出到 10 GB 就停止；不要下载完整子集。
- 适合用途：生成大规模网页语料的可控样本，验证流式处理和高吞吐索引。

### 7. arXiv PDF 分片：0.5–10 GB

- 入口：[arXiv 官方 S3 bulk data 说明](https://info.arxiv.org/help/bulk_data_s3.html)
- 官方说明：PDF 按约 500 MB 的 tar 包分片；可选 1–20 个分片，把下载量控制在约 0.5–10 GB。
- 适配方式：解包后直接使用项目现有 PDF 抽取器；扫描版/图片型 PDF 仍需 OCR。
- 注意：S3 是 requester-pays，下载会产生云端流量费用；论文版权和再分发权按每篇论文的许可处理。建议只选定一个 arXiv 分类或时间段，不要全量下载。

### 8. Stack Exchange 单站点 dump

- 入口：[Internet Archive Stack Exchange Data Dump](https://archive.org/details/stackexchange)
- 全网 dump：页面显示约 92.3 GB；每个站点是单独的 7z/XML 压缩包。
- 适合用途：技术问答、故障排查、编程问答搜索。
- 许可：CC BY-SA 4.0，需要保留来源和作者链接要求。
- 做法：只选择一个中小站点或少数站点，并在下载页核对当前文件大小；不要下载全网包。
- 适配方式：XML 需要先转换为 Markdown/TXT；提取标题、问题正文、答案正文和标签，最好每个问题保存为一个 Markdown 文件。

## 代码数据的补充选项

### CodeSearchNet：约 3.5 GB 原始压缩包；Hugging Face 衍生版 492 MB

- 原始项目：[GitHub `github/CodeSearchNet`](https://github.com/github/CodeSearchNet)
- 可直接读取的衍生版：[Hugging Face `sentence-transformers/codesearchnet`](https://huggingface.co/datasets/sentence-transformers/codesearchnet)
- Hugging Face 数据卡显示：约 1.38M 条 comment-code 对，约 **492 MB**。
- 原始项目的下载脚本会获取多个语言子集，搜索结果和项目说明显示压缩数据合计约 **3.5 GB**。
- 适合用途：代码注释搜索、自然语言到代码检索、验证 `lang`/路径元数据设计。
- 适配方式：每条记录写成 Markdown，文件头放 comment、语言和代码路径，正文放 code。

## 不建议在 10 GB 限制下整库下载的项目

| 数据集 | 已核验规模 | 10 GB 内的用法 |
| --- | ---: | --- |
| SkyPile-150B | 约 665 GB | 取指定 JSON 文件/流式抽样，不能整库下载 |
| FineWeb | 约 54.8 TB | 按单个快照或字节上限采样 |
| Dolma v1.7 | 4.5 TB gzip | 使用样本或流式抽样；官方 v1.6 sample 也约 16.4 GB，仍超过限制 |
| CulturaX | 约 17.5 TB | 按语言和分片抽取 |
| OSCAR 中文 | 约 1.4 TB | 只取部分分片；数据卡当前还提示访问暂时暂停 |
| CLUECorpusSmall | 约 14 GB | 需要再裁剪，整库超过限制 |
| ChineseWebText 2.0 | 约 3.8 TB | 只能使用 3.16 GB 毒性标注子集或自行抽样 |

## 给当前项目的落地顺序

1. 先下载中文 Wikipedia 的单个 JSONL 快照和 THUCNews，原始数据约 4.58 GB。
2. 将 Wikipedia JSONL 的 `text` 字段导出为 TXT/Markdown；THUCNews 直接索引。
3. 运行现有命令：

   ```powershell
   .\.venv\Scripts\python.exe -m knowledge_search index ..\data\raw\external --chunk-size 800 --overlap 100
   ```

4. 如果要验证代码搜索，再加入 CodeSearchNet（约 492 MB）或 The Stack Smol（2.95 GB）。
5. 如果要压测流式处理，再从 FineWeb2 或 arXiv 取不超过 10 GB 的受控样本。

当前项目原生识别 TXT、Markdown、PDF、PPTX；JSONL、Parquet、XML 需要在索引前转换成 TXT/Markdown。所有大数据源都不建议直接写入 Git 仓库，放到 `data/raw/external` 并保留下载清单和许可证信息即可。

