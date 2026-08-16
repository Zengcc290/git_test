# V3 网页验收记录

## 数据流

```text
浏览器
  ├─ GET /、/app.js、/app.css ───────────────→ 静态文件
  └─ JSON / multipart API
       ├─ /api/upload、/api/index ───────────→ index_paths
       │                                       └→ 抽取/清洗/分段
       │                                           └→ SQLite + FTS5
       ├─ /api/search ───────────────────────→ SQLite FTS5/BM25
       │                                       └→ 高亮结果 → 浏览器
       ├─ /api/ask ──────────────────────────→ FTS5 KeywordRetriever
       │                                       └→ RAG Prompt → LLM
       │                                           └→ 引用校验 → 浏览器
       ├─ /api/documents ────────────────────→ SQLite 元数据
       └─ /api/remove ───────────────────────→ SQLite 级联删除 + FTS5 触发器
```

HTTP 层只负责路由、JSON/multipart 解析、输入边界和错误状态；业务层每个请求使用独立 SQLite 连接，ThreadingHTTPServer 支持并发浏览器请求。V3 不引入向量数据库，检索路径保持 FTS5 + jieba + LIKE 兜底。

## 四个页面验收

以下记录使用临时 SQLite 数据库和临时上传目录；问答用测试客户端返回固定带引用答案，避免验收依赖外部额度。`tests/test_web.py` 覆盖同一组业务断言，HTTP 路由用 `create_server(..., port=0)` 启动真实服务器验证。

| 编号 | 页面/问题 | 操作与预期 | 结果 |
|---:|---|---|---|
| 1 | 搜索页 | 打开 `/`，搜索 `SQLite`；显示匹配文档和 `<mark>` 高亮 | 通过 |
| 2 | 搜索页 | 搜索不存在的 `不存在的术语`；显示空结果，不调用模型 | 通过 |
| 3 | 导入页 | 上传 `sqlite.md`；返回 `indexed=1` 并刷新文档/分段计数 | 通过 |
| 4 | 导入页 | 上传同名文件两次；第二个文件自动保存为 `sqlite-1.md`，不覆盖首个文件 | 通过 |
| 5 | 问答页 | 问“SQLite FTS5 是什么？”；答案含 `[1]`，引用卡片显示实际文件和分段 | 通过 |
| 6 | 问答页 | 问知识库没有的内容；返回“根据当前知识库资料，无法回答该问题。”且 `refused=true` | 通过 |
| 7 | 问答页 | LLM 返回非法 `[99]`；接口显示引用校验错误，不输出伪造答案 | 通过 |
| 8 | 文档页 | 列表显示文件类型、字节大小、分段数和路径 | 通过 |
| 9 | 文档页 | 点击移除；文档、chunks 和两套 FTS5 索引均不再命中 | 通过 |
| 10 | 全流程/错误 | `../secret.md`、`.exe`、超过 512 MiB、非法 JSON 和并发搜索请求均得到明确错误；错误文本不含 `LLM_API_KEY` | 通过 |

## 自动化验收命令

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

重点 Web 测试包括搜索、高亮、问答引用和拒答、上传/重名、类型/路径/大小校验、删除和 multipart 解析。启动手工验收：

```powershell
.\.venv\Scripts\python.exe -m knowledge_search web --port 8000
```

服务绑定本机回环地址；关闭进程后 SQLite WAL 文件可正常回收。V3 的后续 V4 工作是 Embedding、混合检索和召回率对比，不改变本验收的 FTS5 基线。
