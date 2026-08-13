"""Run fixed RAG cases through the production answer path and emit an audit log."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from knowledge_search.database import KnowledgeBase
from knowledge_search.logging_config import configure_logging
from knowledge_search.rag.answer import RagAnswerer, RagConfig
from knowledge_search.rag.retriever import KeywordRetriever


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cases", type=Path)
    parser.add_argument("--db", required=True, type=Path)
    parser.add_argument("--log-file", required=True, type=Path)
    parser.add_argument("--rag-config", type=Path, default=Path("configs/rag.json"))
    args = parser.parse_args()

    cases = json.loads(args.cases.read_text(encoding="utf-8"))
    if not isinstance(cases, list) or not cases:
        raise ValueError("评估用例必须是非空 JSON 数组")
    questions = [case.get("question") for case in cases]
    if any(not isinstance(question, str) or not question.strip() for question in questions):
        raise ValueError("每个评估用例都必须包含非空 question")
    if len(set(questions)) != len(questions):
        raise ValueError("评估问题不能重复")

    config = RagConfig.from_file(args.rag_config)
    # A fixed evaluation is one immutable run. Overwrite an earlier output so
    # rerunning the README command cannot silently mix old and new records.
    args.log_file.parent.mkdir(parents=True, exist_ok=True)
    args.log_file.write_text("", encoding="utf-8")
    configure_logging("INFO", args.log_file)
    with KnowledgeBase(args.db) as knowledge_base:
        retriever = KeywordRetriever(
            knowledge_base,
            top_k=config.top_k,
            max_context_chars=config.max_context_chars,
        )
        answerer = RagAnswerer(retriever, temperature=config.temperature)
        for index, case in enumerate(cases, start=1):
            print(f"[{index}/{len(cases)}] {case['id']}", flush=True)
            result = answerer.answer(case["question"])
            print(
                f"  refused={result.refused} sources={len(result.sources)} "
                f"elapsed_ms={result.elapsed_ms:.1f} tokens={result.usage.total_tokens}",
                flush=True,
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
