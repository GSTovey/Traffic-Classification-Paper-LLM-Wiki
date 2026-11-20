#!/usr/bin/env python3
"""Low-intrusion audit for cross-paper research capability.

Audits structure, sources and the written review record. Report writing updates
only generated sections. The candidate command appends pending evidence.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any

from evidence_governance import (
    CLAIMS,
    MIGRATION,
    add_candidates,
    add_issue,
    audit_ledger,
    check_migration,
    frontmatter,
    inspect_fronts,
    registry_stats,
)


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PILOT = ROOT / "00-dashboard" / "research-capability-pilot.json"
DEFAULT_REPORT = ROOT / "00-dashboard" / "research-capability-audit.md"
DEFAULT_QUEUE = ROOT / "00-dashboard" / "research-review-queue.md"


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


def audit(root: Path, pilot_path: Path, *, all_fronts: bool = False) -> dict[str, Any]:
    issues: list[dict[str, str]] = []
    if not pilot_path.exists():
        add_issue(issues, "blocking", str(pilot_path), "试点清单不存在")
        return {"pilot_id": "unknown", "issues": issues, "records": [], "counts": {"blocking": 1}}
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
                if not re.search(rf"^#{{2,6}} {re.escape(heading[3:])}(?:$|[（(])", text, re.M):
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

    records, claims = audit_ledger(root, issues)
    fronts = pilot.get("fronts", [])
    mapped = 0
    if all_fronts:
        fronts = inspect_fronts(root, claims, issues)
        mapped = check_migration(root, records, claims, issues)
        checked_paths = sorted(set(checked_paths + fronts + [str(CLAIMS), str(MIGRATION)]))
    record_claims = {r.get("claim_id") for r in records}
    for claim_id in pilot.get("claim_ids", []):
        if claim_id not in record_claims:
            add_issue(issues, "important", "09-claims/evidence-ledger.jsonl", f"试点关键主张未登记：{claim_id}")

    check_links(root, checked_paths, issues)
    counts = {
        "pilot_notes": len(pilot_notes),
        "fronts": len(fronts),
        "legacy_mapped": mapped,
        "v2_records": sum(r.get("schema_version") == 2 for r in records),
        "pending_records": sum(
            r.get("schema_version") == 2 and r["status"] in {"auto_extracted", "pending_review", "contested"}
            for r in records
        ),
        "signed_claims": sum(c["signed"] for c in claims.values()),
        "draft_claims": sum(not c["signed"] for c in claims.values()),
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
        f"论文笔记 {counts.get('pilot_notes', 0)} 篇，研究前沿 {counts.get('fronts', 0)} 个，方法页 {counts.get('methods', 0)} 个，证据 {counts.get('ledger_records', 0)} 条。",
        f"v2 证据 {counts.get('v2_records', 0)} 条，其中待处理 {counts.get('pending_records', 0)} 条。"
        f"旧账本映射 {counts.get('legacy_mapped', 0)} 条，命题草案 {counts.get('draft_claims', 0)} 条，"
        f"已签审命题 {counts.get('signed_claims', 0)} 条。",
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
        "本报告验证结构、来源路径与审核记录。人工逐条确认原文含义、适用范围、可比性和独立性，维护者另行签审正式判断。",
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
    candidates = [r for r in result["records"] if r.get("schema_version") == 2
                  and r["status"] in {"auto_extracted", "pending_review", "contested"}]
    if candidates:
        lines += ["", "## v2 候选证据", "", "| 证据 | 命题 | 初判方向 | 状态 |", "| --- | --- | --- | --- |"]
        for record in candidates:
            lines.append(
                f"| {record['record_id']} | {record['claim_id']} | {record['polarity']} | {record['status']} |"
            )
    lines += [
        "",
        "处理规则：先修复来源和定位问题，再审核证据方向；未经审核的记录不得进入正式共识。",
        "",
    ]
    return "\n".join(lines)


def write_generated_report(path: Path, report: str) -> None:
    start = "<!-- evidence-audit:generated:start -->"
    end = "<!-- evidence-audit:generated:end -->"
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    block = f"{start}\n{report.rstrip()}\n{end}"
    if start not in text and end not in text:
        history = f"\n## 历史人工记录\n\n{text}" if text else ""
        path.write_text(f"{block}\n{history}", encoding="utf-8")
        return
    if text.count(start) != 1 or text.count(end) != 1 or text.index(start) >= text.index(end):
        raise ValueError(f"生成区标记损坏：{path}")
    before, _, remainder = text.partition(start)
    _, _, after = remainder.partition(end)
    path.write_text(f"{before}{block}{after}", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("audit", "validate", "queue", "stats", "add-candidates"))
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--pilot", type=Path, default=None)
    parser.add_argument("--write", action="store_true", help="更新两个审计报告的生成区")
    parser.add_argument("--strict", action="store_true", help="将重要质量问题也作为失败返回")
    parser.add_argument("--all-fronts", action="store_true", help="校验全部前沿、快照和旧账本迁移映射")
    parser.add_argument("--input", type=Path, help="add-candidates 的 v2 JSONL 输入")
    args = parser.parse_args()
    root = args.root.resolve()
    if args.command == "stats":
        print(json.dumps(registry_stats(root), ensure_ascii=False, indent=2))
        return 0
    if args.command == "add-candidates" and args.input is None:
        parser.error("add-candidates requires --input")
    try:
        if args.command == "add-candidates":
            added, issues = add_candidates(root, args.input)
            for issue in issues:
                print(f"{issue['severity']} {issue['location']} {issue['message']}", file=sys.stderr)
            print(f"新增候选证据 {added} 条")
            return int(any(issue["severity"] == "blocking" for issue in issues))
        pilot = (args.pilot or (root / DEFAULT_PILOT.relative_to(ROOT))).resolve()
        result = audit(root, pilot, all_fronts=args.all_fronts)
        if args.write or args.command == "queue":
            write_generated_report(root / DEFAULT_REPORT.relative_to(ROOT), markdown_report(result))
            write_generated_report(root / DEFAULT_QUEUE.relative_to(ROOT), queue_report(result))
    except ModuleNotFoundError as exc:
        if exc.name != "jsonschema":
            raise
        parser.error("Install the dependencies in scripts/requirements.txt (including jsonschema).")
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    print(queue_report(result) if args.command == "queue" else markdown_report(result))
    counts = result["counts"]
    if counts.get("blocking") or any(i["severity"] == "blocking" for i in result["issues"]):
        return 1
    if args.strict and counts.get("important"):
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
