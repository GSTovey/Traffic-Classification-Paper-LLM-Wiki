#!/usr/bin/env python3
"""Low-intrusion audit for cross-paper research capability.

The script reads the pilot manifest and evidence ledger, reports issues, and
optionally writes two durable reports. It never edits paper notes, claims,
research fronts, methods, or personal research pages.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PILOT = ROOT / "00-dashboard" / "research-capability-pilot.json"
DEFAULT_REPORT = ROOT / "00-dashboard" / "research-capability-audit.md"
DEFAULT_QUEUE = ROOT / "00-dashboard" / "research-review-queue.md"
VALID_STATUSES = {"auto_extracted", "pending_review", "verified", "contested", "retired"}
VALID_EVIDENCE_TYPES = {
    "author_claim",
    "direct_experiment",
    "ablation",
    "independent_replication",
    "cross_paper_synthesis",
}
VALID_POLARITIES = {"supports", "challenges", "neutral"}


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if not value:
        return ""
    if value.startswith(("[", "{")):
        try:
            return json.loads(value.replace("'", '"'))
        except json.JSONDecodeError:
            return value
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    return value


def frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    result: dict[str, Any] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        result[key.strip()] = parse_scalar(value)
    return result


def add_issue(issues: list[dict[str, str]], severity: str, location: str, message: str) -> None:
    issues.append({"severity": severity, "location": location, "message": message})


def exists_note(root: Path, value: str) -> bool:
    if not value:
        return False
    candidate = root / value
    if candidate.exists():
        return True
    if value.endswith(".md"):
        return (root / value).exists()
    return (root / f"{value}.md").exists()


def link_exists(root: Path, target: str, stems: set[str]) -> bool:
    target = target.split("#", 1)[0].strip()
    if not target or target.startswith(("http:", "https:", "mailto:")):
        return True
    target = target.replace("\\", "/")
    if (root / target).exists() or (root / f"{target}.md").exists():
        return True
    base = Path(target).name
    return base in stems or Path(base).stem in stems


def check_links(root: Path, paths: list[str], issues: list[dict[str, str]]) -> None:
    stems = {p.stem for p in root.rglob("*.md")}
    pattern = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")
    for rel in paths:
        path = root / rel
        if not path.exists() or path.suffix != ".md":
            continue
        text = path.read_text(encoding="utf-8")
        for raw_target in pattern.findall(text):
            if not link_exists(root, raw_target, stems):
                add_issue(issues, "important", rel, f"内部链接无法解析：[[{raw_target}]]")


def read_ledger(root: Path, issues: list[dict[str, str]]) -> list[dict[str, Any]]:
    path = root / "09-claims" / "evidence-ledger.jsonl"
    records: list[dict[str, Any]] = []
    if not path.exists():
        add_issue(issues, "blocking", str(path.relative_to(root)), "证据账本不存在")
        return records
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        location = f"09-claims/evidence-ledger.jsonl:{line_no}"
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            add_issue(issues, "blocking", location, f"JSONL 无法解析：{exc}")
            continue
        records.append(record)
        required = {
            "record_id",
            "claim_id",
            "source_note",
            "source_locator",
            "evidence_type",
            "polarity",
            "conditions",
            "counterevidence_ids",
            "status",
        }
        missing = sorted(required - set(record))
        if missing:
            add_issue(issues, "blocking", location, f"缺少字段：{', '.join(missing)}")
        if record.get("status") not in VALID_STATUSES:
            add_issue(issues, "blocking", location, f"未知证据状态：{record.get('status')}")
        if record.get("evidence_type") not in VALID_EVIDENCE_TYPES:
            add_issue(issues, "important", location, f"未知证据类型：{record.get('evidence_type')}")
        if record.get("polarity") not in VALID_POLARITIES:
            add_issue(issues, "important", location, f"未知证据方向：{record.get('polarity')}")
        source_note = record.get("source_note", "")
        if not exists_note(root, source_note):
            add_issue(issues, "blocking", location, f"来源笔记不存在：{source_note}")
        locator = record.get("source_locator")
        if record.get("status") == "verified" and not isinstance(locator, dict):
            add_issue(issues, "blocking", location, "verified 记录必须有结构化 source_locator")
        elif record.get("status") == "verified" and not any(str(v).strip() for v in locator.values()):
            add_issue(issues, "blocking", location, "verified 记录的 source_locator 不能为空")
    return records


def audit(root: Path, pilot_path: Path) -> dict[str, Any]:
    issues: list[dict[str, str]] = []
    if not pilot_path.exists():
        add_issue(issues, "blocking", str(pilot_path), "试点清单不存在")
        return {"pilot_id": "unknown", "issues": issues, "records": []}
    pilot = json.loads(pilot_path.read_text(encoding="utf-8"))
    pilot_notes = pilot.get("notes", [])
    checked_paths = pilot.get("fronts", []) + pilot.get("methods", [])

    for rel in pilot_notes:
        path = root / rel
        if not path.exists():
            add_issue(issues, "blocking", rel, "试点论文笔记不存在")
            continue
        fm = frontmatter(path)
        if fm.get("type") != "paper":
            add_issue(issues, "important", rel, "论文笔记 type 不是 paper")
        deep_note = str(fm.get("reading_level", "")).strip() in {"L3", "L4"}
        for field in ("pdf", "mineru_md"):
            value = fm.get(field, "")
            if not value:
                add_issue(issues, "important" if deep_note else "advisory", rel, f"缺少 {field} 字段")
            elif not exists_note(root, value):
                add_issue(issues, "blocking", rel, f"{field} 指向的文件不存在：{value}")
        text = path.read_text(encoding="utf-8")
        if deep_note:
            for heading in ("## 3.4 问题发现路径", "## 3.5 科学假设形成", "## 6.7 局限性", "## 10. 证据记录"):
                if heading not in text:
                    add_issue(issues, "important", rel, f"缺少关键分析段落：{heading}")

    for rel in pilot.get("fronts", []):
        path = root / rel
        if not path.exists():
            add_issue(issues, "blocking", rel, "研究前沿页面不存在")
            continue
        fm = frontmatter(path)
        for field in ("status", "problem_state", "evidence_state"):
            if not fm.get(field):
                add_issue(issues, "important", rel, f"缺少研究前沿状态字段：{field}")
        text = path.read_text(encoding="utf-8")
        for heading in ("## 问题定义", "## 现有解释与共同前提", "## 支持证据与反证", "## 候选科学问题与可证伪假设", "## 统一验证方案"):
            if heading not in text:
                add_issue(issues, "important", rel, f"缺少研究问题分析段落：{heading}")

    for rel in pilot.get("methods", []):
        path = root / rel
        if not path.exists():
            add_issue(issues, "blocking", rel, "试点方法页不存在")
            continue
        text = path.read_text(encoding="utf-8")
        for heading in ("成立前提", "失效条件", "迁移边界", "证据状态"):
            if heading not in text:
                add_issue(issues, "important", rel, f"方法页缺少边界信息：{heading}")

    records = read_ledger(root, issues)
    record_claims = {r.get("claim_id") for r in records}
    for claim_id in pilot.get("claim_ids", []):
        if claim_id not in record_claims:
            add_issue(issues, "important", "09-claims/evidence-ledger.jsonl", f"试点关键主张未登记：{claim_id}")

    check_links(root, checked_paths, issues)
    counts = {
        "pilot_notes": len(pilot_notes),
        "fronts": len(pilot.get("fronts", [])),
        "methods": len(pilot.get("methods", [])),
        "ledger_records": len(records),
        "blocking": sum(i["severity"] == "blocking" for i in issues),
        "important": sum(i["severity"] == "important" for i in issues),
        "advisory": sum(i["severity"] == "advisory" for i in issues),
    }
    return {
        "generated_on": str(date.today()),
        "pilot_id": pilot.get("pilot_id", "unknown"),
        "question": pilot.get("question", ""),
        "counts": counts,
        "issues": issues,
        "records": records,
    }


def markdown_report(result: dict[str, Any]) -> str:
    counts = result["counts"]
    lines = [
        "# 研究能力审计报告",
        "",
        f"- 生成日期：{result.get('generated_on', 'unknown')}",
        f"- 试点：`{result.get('pilot_id', 'unknown')}`",
        f"- 研究问题：{result.get('question', '')}",
        "",
        "## 审计范围",
        "",
        f"论文笔记 {counts.get('pilot_notes', 0)} 篇，研究前沿 {counts.get('fronts', 0)} 个，方法页 {counts.get('methods', 0)} 个，关键证据记录 {counts.get('ledger_records', 0)} 条。",
        "",
        "## 结果",
        "",
        f"- 阻断性错误：{counts.get('blocking', 0)}",
        f"- 重要质量问题：{counts.get('important', 0)}",
        f"- 非阻断性建议：{counts.get('advisory', 0)}",
        "",
        "## 问题清单",
        "",
        "| 严重程度 | 位置 | 问题 |",
        "|---|---|---|",
    ]
    if result["issues"]:
        lines.extend(f"| {i['severity']} | `{i['location']}` | {i['message']} |" for i in result["issues"])
    else:
        lines.append("| — | — | 未发现问题 |")
    lines += [
        "",
        "## 解释",
        "",
        "本报告只记录影响论文证据、跨论文综合、创新点挖掘和研究决策的缺陷；普通历史格式差异不会阻断论文入库。证据账本中的 pending_review 和 contested 记录不得自动升级为正式共识。",
        "",
    ]
    return "\n".join(lines)


def queue_report(result: dict[str, Any]) -> str:
    lines = [
        "# 研究审核队列",
        "",
        f"试点：`{result.get('pilot_id', 'unknown')}`；生成日期：{result.get('generated_on', 'unknown')}",
        "",
        "| 优先级 | 位置 | 待处理事项 |",
        "|---|---|---|",
    ]
    issues = result["issues"]
    if issues:
        for issue in issues:
            priority = "P0" if issue["severity"] == "blocking" else "P1" if issue["severity"] == "important" else "P2"
            lines.append(f"| {priority} | `{issue['location']}` | {issue['message']} |")
    else:
        lines.append("| — | — | 当前没有待处理事项 |")
    lines += [
        "",
        "处理规则：先修复来源和定位问题，再审核证据方向；未经审核的记录不得进入正式共识。",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("audit", "validate", "queue"))
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--pilot", type=Path, default=None)
    parser.add_argument("--write", action="store_true", help="写入两个审计报告，不修改知识内容")
    parser.add_argument("--strict", action="store_true", help="将重要质量问题也作为失败返回")
    args = parser.parse_args()
    root = args.root.resolve()
    pilot = (args.pilot or (root / DEFAULT_PILOT.relative_to(ROOT))).resolve()
    result = audit(root, pilot)
    if args.write or args.command == "queue":
        (root / DEFAULT_REPORT.relative_to(ROOT)).write_text(markdown_report(result), encoding="utf-8")
        (root / DEFAULT_QUEUE.relative_to(ROOT)).write_text(queue_report(result), encoding="utf-8")
    if args.command == "queue":
        print(queue_report(result))
    else:
        print(markdown_report(result))
    if result["counts"]["blocking"]:
        return 1
    if args.strict and result["counts"]["important"]:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
