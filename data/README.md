# RAG 数据区

数据按处理阶段流转，不同阶段不要混放：

- `raw/`：原始文档，仅作为输入，不直接修改
- `processed/`：解析后的纯文本或结构化文档
- `chunks/`：切分后的文本块及 Metadata
- `indexes/`：向量索引、关键词索引和本地数据库
- `sample/`：少量可公开、可复现的样例数据

`raw/` 到 `indexes/` 的内容通常由 `scripts/` 生成，并已在 `.gitignore` 中排除；目录骨架通过 `.gitkeep` 保留。
