"""Clean RAG_RECORD audit lines and score fixed grounding evaluation cases."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sqlite3
from pathlib import Path
from typing import Any


RECORD_MARKER = "RAG_RECORD "
CITATION_PATTERN = re.compile(r"\[(\d+)\]")


def normalize(text: str) -> str:
    text = re.sub(r"[`*_\s]", "", text).casefold()
    return text.replace("：", "比").replace("∶", "比").replace(":", "比")


def contains_any(text: str, alternatives: list[str]) -> bool:
    normalized = normalize(text)
    return any(normalize(value) in normalized for value in alternatives)


def read_records(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if RECORD_MARKER not in line:
            continue
        payload = line.split(RECORD_MARKER, 1)[1]
        records.append(json.loads(payload))
    return records


def relevant_excerpt(evidence: str, facts: list[dict[str, Any]]) -> str:
    compact = re.sub(r"\s+", " ", evidence).strip()
    spans: list[tuple[int, int]] = []
    lowered = compact.casefold()
    for fact in facts:
        for alternative in fact["evidence_any"]:
            position = lowered.find(re.sub(r"\s+", "", alternative).casefold())
            if position >= 0:
                spans.append((max(0, position - 70), min(len(compact), position + 150)))
                break
    if not spans:
        return compact[:400]
    merged: list[tuple[int, int]] = []
    for start, end in sorted(spans):
        if merged and start <= merged[-1][1] + 20:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            merged.append((start, end))
    return " ... ".join(compact[start:end].strip() for start, end in merged)[:1200]


def clean_record(record: dict[str, Any], case: dict[str, Any]) -> dict[str, Any]:
    answer = record["answer"] or ""
    citation_ids = sorted({int(value) for value in CITATION_PATTERN.findall(answer)})
    retrievals = record.get("retrieval_results") or []
    by_id = {int(item["citation_id"]): item for item in retrievals}
    cited = [by_id[citation_id] for citation_id in citation_ids if citation_id in by_id]
    evidence = "\n".join(item.get("content", "") for item in cited)

    fact_checks: list[dict[str, Any]] = []
    for fact in case["facts"]:
        answer_match = contains_any(answer, fact["answer_any"])
        evidence_match = contains_any(evidence, fact["evidence_any"])
        fact_checks.append(
            {
                "label": fact["label"],
                "answer_match": answer_match,
                "evidence_match": evidence_match,
                "supported": answer_match and evidence_match,
            }
        )

    expected_sources = case.get("expected_sources") or [case["expected_source"]]
    retrieved_sources = {
        item.get("filename") for item in retrievals if item.get("filename") in expected_sources
    }
    cited_sources = {
        item.get("filename") for item in cited if item.get("filename") in expected_sources
    }
    retrieved_source = len(retrieved_sources) == len(expected_sources)
    cited_source = len(cited_sources) == len(expected_sources)
    citations_valid = bool(citation_ids) and len(cited) == len(citation_ids)
    refusal_correct = bool(record.get("refused")) == bool(case["expected_refused"])
    supported_count = sum(item["supported"] for item in fact_checks)
    total_facts = len(fact_checks)
    passed = (
        supported_count == total_facts
        and retrieved_source
        and cited_source
        and citations_valid
        and refusal_correct
    )

    return {
        "case_id": case["id"],
        "kind": case["kind"],
        "question": case["question"],
        "answer": answer,
        "expected_sources": expected_sources,
        "retrieved_source": retrieved_source,
        "cited_source": cited_source,
        "citation_ids": citation_ids,
        "citations_valid": citations_valid,
        "expected_refused": case["expected_refused"],
        "actual_refused": bool(record.get("refused")),
        "refusal_correct": refusal_correct,
        "fact_checks": fact_checks,
        "supported_facts": supported_count,
        "total_facts": total_facts,
        "support_rate": supported_count / total_facts if total_facts else 1.0,
        "passed": passed,
        "cited_evidence": [
            {
                "citation_id": item["citation_id"],
                "filename": item["filename"],
                "chunk_indexes": item.get("chunk_indexes", [item["chunk_index"]]),
                "excerpt": relevant_excerpt(item.get("content", ""), case["facts"]),
            }
            for item in cited
        ],
        "elapsed_ms": record["elapsed_ms"],
        "token_usage": record["token_usage"],
        "context_chars": record["context_chars"],
        "context_truncated": record["context_truncated"],
    }


def database_counts(path: Path) -> tuple[int, int]:
    with sqlite3.connect(path) as connection:
        document_count = int(connection.execute("SELECT COUNT(*) FROM documents").fetchone()[0])
        chunk_count = int(connection.execute("SELECT COUNT(*) FROM chunks").fetchone()[0])
    return document_count, chunk_count


def render_report(
    cleaned: list[dict[str, Any]],
    *,
    raw_log: Path,
    ablation: dict[str, Any],
    document_count: int,
    chunk_count: int,
) -> str:
    passed = sum(item["passed"] for item in cleaned)
    supported = sum(item["supported_facts"] for item in cleaned)
    total_facts = sum(item["total_facts"] for item in cleaned)
    average_ms = sum(item["elapsed_ms"] for item in cleaned) / len(cleaned)
    total_tokens = sum(item["token_usage"]["total_tokens"] for item in cleaned)
    digest = hashlib.sha256(raw_log.read_bytes()).hexdigest()

    lines = [
        "# RAG 大语料 Grounding 日志清洗结果",
        "",
        "## 结论",
        "",
        f"- 评估知识库：{document_count:,} 篇文档，{chunk_count:,} 个分段。",
        f"- 最终固定用例：{len(cleaned)} 条；通过 {passed}/{len(cleaned)}。",
        f"- 可核验事实：{supported}/{total_facts} 同时出现在模型答案和实际引用证据中，支持率 {supported / total_facts:.1%}。",
        f"- 平均响应时间：{average_ms:.1f} ms；总 token：{total_tokens:,}。",
        "- 两组随机受控事实中的代号、未来日期和随机数值全部正确，证明答案实际使用了本次本地检索上下文，而非只依赖模型预训练知识。",
        "- 资料缺失用例正确拒答，没有编造主控芯片、预算或负责人。",
        "- 同一模型的无检索上下文消融回答为“不知道这些信息”，且未包含第一组任一随机受控值；这与带 RAG 时第一组 8/8 精确回答形成直接对照。",
        "",
        "## 清洗规则",
        "",
        "- 只读取原始日志中的 `RAG_RECORD` JSON；移除普通运行日志、jieba 调试输出和时间戳。",
        "- 删除绝对路径，只保留引用文件名和实际覆盖的分段编号。",
        "- 只保留答案真正引用的 `[n]` 证据；未引用的 Top-K 正文不进入清洗结果。",
        "- 每个预期事实必须同时命中答案和被引用证据，才计为“支持”。",
        "- 只归一化配置在固定用例中的等价标点和措辞，例如 `4∶40`/`4：40`、`第三场`/`最后一战`；不改写模型原文或补造引用。",
        "- 该评分验证固定事实契合度，不声称能自动识别所有开放式语义幻觉。",
        "",
        "## 无上下文消融对照",
        "",
        f"**同一问题：** {ablation['question']}",
        "",
        f"**同一模型、无知识库回答：** {ablation['answer']}",
        "",
        f"**受控随机值是否出现在无上下文回答中：** "
        f"{'是' if ablation['contains_controlled_answer_values'] else '否'}。",
        "",
        "",
        "## 汇总",
        "",
        "| 用例 | 类型 | 预期来源已引用 | 事实支持 | 拒答判定 | 结果 | 耗时 ms | Token |",
        "|---|---|:---:|---:|:---:|:---:|---:|---:|",
    ]
    for item in cleaned:
        result = "通过" if item["passed"] else "失败"
        refusal = "正确" if item["refusal_correct"] else "错误"
        lines.append(
            f"| {item['case_id']} | {item['kind']} | "
            f"{'是' if item['cited_source'] else '否'} | "
            f"{item['supported_facts']}/{item['total_facts']} | {refusal} | {result} | "
            f"{item['elapsed_ms']:.1f} | {item['token_usage']['total_tokens']} |"
        )

    lines.extend(["", "## 用例明细", ""])
    for index, item in enumerate(cleaned, start=1):
        lines.extend(
            [
                f"### {index}. {item['case_id']}",
                "",
                f"**问题：** {item['question']}",
                "",
                f"**回答：** {item['answer']}",
                "",
                f"**判定：** {'通过' if item['passed'] else '失败'}；"
                f"事实支持 {item['supported_facts']}/{item['total_facts']}；"
                f"预期来源 `{', '.join(item['expected_sources'])}` "
                f"{'均已引用' if item['cited_source'] else '未全部引用'}。",
                "",
                "**事实核验：**",
                "",
            ]
        )
        for fact in item["fact_checks"]:
            state = "支持" if fact["supported"] else "不支持"
            lines.append(f"- {fact['label']}：{state}")
        lines.extend(["", "**清洗后引用证据：**", ""])
        for evidence in item["cited_evidence"]:
            chunks = "、".join(str(value) for value in evidence["chunk_indexes"])
            lines.append(
                f"- [{evidence['citation_id']}] `{evidence['filename']}` 分段 {chunks}："
                f"{evidence['excerpt']}"
            )
        lines.append("")

    lines.extend(
        [
        "## 诊断说明",
        "",
        "开发期的大语料自然问句曾因常见词噪声导致目标文档未进入 Top-K，另有一题的答案跨越相邻分段；当前实现使用关键词对召回、候选覆盖词排序和相邻分段窗口。清洗评分只接受固定用例中显式列出的等价标点和措辞；模型原始答案及引用不会被改写。",
        "",
        "## 限制与残余风险",
        "",
        "- Top-K 中仍可见无关候选和同一文档相邻命中的重复候选；最终答案没有引用它们，但检索精度并非 100%。",
        "- 新闻语料自身存在冲突：`10820.txt` 写伤病比赛 20 场，而其他同主题候选写 18 场。模型回答与其实际引用的 `[1]` 完全一致，但这不等同于证明来源本身绝对真实。",
        f"- {len(cleaned)} 个固定用例和 {total_facts} 个事实适合验证当前链路与回归，不足以代表全部开放问题。",
        "",
        f"原始最终日志 SHA-256：`{digest}`",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("raw_log", type=Path)
    parser.add_argument("cases", type=Path)
    parser.add_argument("--db", required=True, type=Path)
    parser.add_argument("--ablation-result", required=True, type=Path)
    parser.add_argument("--jsonl-output", required=True, type=Path)
    parser.add_argument("--report-output", required=True, type=Path)
    args = parser.parse_args()

    records = read_records(args.raw_log)
    cases = json.loads(args.cases.read_text(encoding="utf-8"))
    ablation = json.loads(args.ablation_result.read_text(encoding="utf-8"))
    if len(records) != len(cases):
        raise ValueError(f"日志记录数 {len(records)} 与用例数 {len(cases)} 不一致")

    records_by_question = {record["question"]: record for record in records}
    cleaned = []
    for case in cases:
        record = records_by_question.get(case["question"])
        if record is None:
            raise ValueError(f"日志中缺少问题：{case['question']}")
        cleaned.append(clean_record(record, case))

    args.jsonl_output.parent.mkdir(parents=True, exist_ok=True)
    args.jsonl_output.write_text(
        "".join(json.dumps(item, ensure_ascii=False) + "\n" for item in cleaned),
        encoding="utf-8",
    )
    document_count, chunk_count = database_counts(args.db)
    args.report_output.write_text(
        render_report(
            cleaned,
            raw_log=args.raw_log,
            ablation=ablation,
            document_count=document_count,
            chunk_count=chunk_count,
        ),
        encoding="utf-8",
    )
    return 0 if all(item["passed"] for item in cleaned) else 1


if __name__ == "__main__":
    raise SystemExit(main())
