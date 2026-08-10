# RAG 学习与实践库

这是一个面向 Retrieval-Augmented Generation（RAG）的学习、实验与工程实践仓库。
目录按“学习资料 → 数据处理 → 检索生成 → 评估上线 → 项目示例”组织，`.git` 目录和 Git 历史保持不变。

## 推荐学习顺序

1. 阅读 `docs/00-roadmap/`，了解整体路线和每阶段产出。
2. 学习 `docs/01-foundations/`：LLM、信息检索、Embedding、向量数据库。
3. 按 `docs/02-rag-pipeline/` 实现数据接入、解析、切分、索引、检索、重排和生成。
4. 使用 `examples/01-minimal-rag/` 到 `examples/03-rag-evaluation/` 完成小项目。
5. 在 `docs/03-evaluation/` 中建立评测集和误差分析流程。
6. 最后阅读 `docs/04-production/`，补齐部署、监控和成本控制。

## 目录结构

```text
docs/              学习资料、笔记、论文和工程文档
src/rag/           RAG 各阶段的可复用实现
src/shared/        配置、日志、模型客户端等公共代码
tests/             单元测试、集成测试、评测和测试夹具
data/              原始资料到索引的 RAG 数据流水线
experiments/       Notebook、基准测试和消融实验
prompts/           系统提示词、检索模板和生成模板
configs/           本地、测试、生产配置模板
scripts/           数据处理、建库、评测和运维脚本
examples/          从最小 RAG 到混合检索的完整示例
```

## 数据流

```text
data/raw
  → data/processed
  → data/chunks
  → data/indexes
  → src/rag/retrieval
  → src/rag/generation
```

生成的文档副本、切片和索引默认被 `.gitignore` 忽略；小型、可公开复现的样例放在 `data/sample/`。
每个空目录中的 `.gitkeep` 用于让 Git 保留目录骨架。

## 约定

- 学习结论放在 `docs/06-notes/`，可复用的正式内容再整理到对应专题目录。
- 一次实验一个目录，放入配置、代码、结果和结论，结果统一放在实验目录的 `outputs/` 下。
- 不把 API Key、真实用户数据、未脱敏业务文档或本地数据库提交到仓库。
- 新增模块时，优先按 RAG 流程阶段归入 `src/rag/`，不要把所有代码堆在单一文件夹。
