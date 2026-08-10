# RAG Pipeline

每个目录对应一个可独立验证的流水线阶段：

```text
ingestion → parsing → chunking → embeddings → indexing
                                             ↓
generation ← reranking ← retrieval ← query
```

- `ingestion/`：文件、网页、数据库等数据源接入
- `parsing/`：PDF、Markdown、HTML、Office 等格式解析
- `chunking/`：按长度、语义、标题和结构切分
- `embeddings/`：Embedding 模型、批处理和版本管理
- `indexing/`：向量索引、倒排索引和 Metadata
- `retrieval/`：向量、关键词、混合和过滤检索
- `reranking/`：重排、上下文压缩和去重
- `generation/`：上下文组装、引用、拒答和答案生成
