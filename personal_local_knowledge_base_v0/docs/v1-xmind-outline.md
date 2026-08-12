# 个人本地知识库搜索工具 V1

## 主流程

### 1. 启动

- 首次使用：创建虚拟环境并安装依赖
- 执行 `init-db` 初始化 SQLite 数据库
- 后续使用：直接复用 `data/knowledge.db`

### 2. 文档索引：`index <文档目录>`

- 扫描支持的文件
  - TXT / Markdown：流式读取文本
  - PDF：按页抽取文本
  - PPTX：按幻灯片抽取文本框、标题、表格和组合图形文字
  - JSON：必须提供 JSON 配置，按记录路径和字段解析
- 单文件异常：记录错误，继续处理其他文件
- 文本清洗
  - 统一换行和空白
  - 保留标题与正文
- 文本分段
  - 按段落切分
  - 超长段落按标点或空格切分
  - 保留 overlap 重叠内容
- 增量判断
  - SHA-256 未变化且解析指纹未变化：跳过索引
  - 文件发生变化：替换该文件的旧索引
- 写入 SQLite
  - `documents`：文件元数据
  - `chunks`：文本分段
  - `chunks_fts`：原始文本 FTS5 索引
  - `chunk_tokens`：jieba 分词结果
  - `chunks_fts_jieba`：中文 FTS5 索引

### 3. 关键词搜索：`search <关键词>`

- 输入查询条件
  - 关键词
  - `--limit` 返回数量
  - `--type` 文件类型过滤
  - `--path` 文件或目录过滤
- 第一优先级：jieba 中文分词 + FTS5 BM25 排序
- 无命中：回退到原始文本 FTS5
- 中文仍无命中：使用参数化 `LIKE` 兜底
- 输出结果
  - 文件路径
  - 文件类型
  - 分段编号
  - 相关性排序
  - 命中内容高亮

### 4. 知识库管理

- `list`：查看文件、类型、大小、分段数和索引时间
- `stats`：查看数据库统计信息
- `remove <路径>`：删除文档、分段和关联的两套 FTS5 索引
- `prune`：清理源文件已经不存在的索引记录
- `check-db`：检查 documents、chunks、token 和两套 FTS5 索引的一致性

### 5. 验收与测试

- `python -m unittest discover -s tests -v`：运行回归测试
- 使用 CLI 验证 index、stats、search、remove、prune、重复索引和过滤条件
- 基础搜索验证
  - 10 个查询全部 Top-1 命中
  - 10 个查询全部在 Top-5 中包含预期文档
- V1 边界
  - 只做关键词搜索
  - 不包含问答、对话、Embedding、向量数据库和远程 API
  - 扫描版 PDF 暂不支持 OCR
