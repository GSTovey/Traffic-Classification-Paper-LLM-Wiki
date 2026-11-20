"""Validate evidence and the references that authorize its use in a synthesis."""
from __future__ import annotations

import json
import re
from datetime import date
from hashlib import sha256
from pathlib import Path
from typing import Any

LEDGER = Path('09-claims/evidence-ledger.jsonl')
SCHEMA = LEDGER.with_name('evidence-ledger.schema.json')
CLAIMS = LEDGER.with_name('proposition-index.md')
MIGRATION = LEDGER.with_name('claim-migration-map.md')
FRONTS = Path('12-research-fronts')
FRONT_INDEX = FRONTS / 'index.md'
ARCHIVE_START = '<!-- evidence-governance:archive:start -->\n'
ARCHIVE_END = '<!-- evidence-governance:archive:end -->'
CLAIM_ID = re.compile(r'(?<![\w-])CLM-[0-9]{4,}(?![\w-])')
EVIDENCE_ID = re.compile(r'(?<![\w-])EV-[A-Za-z0-9-]+')
CLAIM_STATES = {'supported', 'contested', 'insufficient_evidence', 'superseded'}
SIGNED_FRONT_STATES = {'converging', 'diverging', 'stale', 'conditional_support',
                       'insufficient_evidence', 'scope_unclear'}


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if value in ('null', '~'):
        return None
    if value.startswith(('[', '{')):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
        return value[1:-1]
    return value


def frontmatter(path: Path) -> dict[str, Any]:
    lines = path.read_text(encoding='utf-8').splitlines()
    if not lines or lines[0].strip() != '---':
        return {}
    result: dict[str, Any] = {}
    for line in lines[1:]:
        if line.strip() == '---':
            break
        name, sep, value = line.partition(':')
        if sep and re.fullmatch(r'[a-zA-Z_][\w-]*', name):
            result[name] = parse_scalar(value)
    return result


def add_issue(issues: list[dict[str, str]], severity: str, location: str, message: str) -> None:
    issues.append({'severity': severity, 'location': location, 'message': message})


def section(text: str, title: str) -> str:
    match = re.search(rf'^## {re.escape(title)}[ \t]*\n(.*?)(?=^## |\Z)', text, re.M | re.S)
    return match[1] if match else ''


def table_rows(text: str) -> list[list[str]]:
    rows = [re.split(r'(?<!\\)\|', line)[1:-1] for line in text.splitlines()
            if line.startswith('|') and line.endswith('|')]
    return [[cell.strip().strip('`') for cell in row] for row in rows[2:]]


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and value.strip().lower() not in ('', 'unknown', '—', 'null', 'not_applicable')


def date_is_valid(value: Any) -> bool:
    try:
        return isinstance(value, str) and date.fromisoformat(value).isoformat() == value
    except ValueError:
        return False


def local_file(root: Path, value: str) -> bool:
    path = Path(value)
    if path.is_absolute() or '..' in path.parts:
        return False
    return (root / path).is_file() and (root / path).resolve().is_relative_to(root.resolve())


def schema_validator(root: Path):
    # Load only for commands that inspect records. The statistics entry point is standalone.
    from jsonschema import Draft202012Validator, FormatChecker

    schema = json.loads((root / SCHEMA).read_text(encoding='utf-8'))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def parse_records(root: Path, text: str, location: str, issues: list[dict[str, str]], validator) -> list[dict[str, Any]]:
    records = []
    for line_no, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            continue
        at = f'{location}:{line_no}'
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            add_issue(issues, 'blocking', at, f'JSONL 无法解析：{exc}')
            continue
        errors = list(validator.iter_errors(record))
        for error in errors:
            field = '.'.join(map(str, error.absolute_path)) or 'record'
            add_issue(issues, 'blocking', at, f'Schema {field}：{error.message}')
        if errors:
            continue
        records.append(record)
        note = record['source_note']
        if not local_file(root, note) and not local_file(root, f'{note}.md'):
            add_issue(issues, 'blocking', at, f'来源笔记不存在：{note}')
        if record.get('schema_version') == 2:
            document = record['source_document']
            original = (document.startswith(('00-inbox/PDFs/', '02-parsed-markdown/', '01-mineru-output/'))
                        and local_file(root, document))
            if not original:
                severity = 'blocking' if record['status'] == 'verified' else 'important'
                add_issue(issues, severity, at, f'原文文件无法解析：{document}')
    return records


def read_claim_index(root: Path, issues: list[dict[str, str]]) -> dict[str, dict[str, Any]]:
    path = root / CLAIMS
    if not path.is_file():
        add_issue(issues, 'blocking', str(CLAIMS), '命题索引不存在')
        return {}
    text = path.read_text(encoding='utf-8')
    result = {}
    for heading, signed in (('正式命题', True), ('待签审命题', False)):
        body = section(text, heading)
        if not body:
            add_issue(issues, 'blocking', str(CLAIMS), f'缺少区段：{heading}')
        for row in table_rows(body):
            claim_id = row[0]
            if len(row) != (6 if signed else 3) or not CLAIM_ID.fullmatch(claim_id) or claim_id in result:
                add_issue(issues, 'blocking', str(CLAIMS), f'命题行格式错误或 ID 重复：{claim_id}')
                continue
            if not nonempty(row[1]):
                add_issue(issues, 'blocking', str(CLAIMS), f'{claim_id} 缺少命题与条件')
            claim: dict[str, Any] = {'signed': signed}
            if signed:
                _, _, state, refs, reviewer, reviewed_on = row
                ids = EVIDENCE_ID.findall(refs)
                if state not in CLAIM_STATES or not nonempty(reviewer) or not date_is_valid(reviewed_on):
                    add_issue(issues, 'blocking', str(CLAIMS), f'{claim_id} 缺有效的命题状态或签审记录')
                if refs != '—' and (not ids or len(set(ids)) != len(ids)):
                    add_issue(issues, 'blocking', str(CLAIMS), f'{claim_id} 关键证据 ID 格式错误或重复')
                claim.update(state=state, evidence_ids=ids, reviewed_on=reviewed_on)
            result[claim_id] = claim
    return result


def check_record_links(records: list[dict[str, Any]], claims: dict[str, Any], issues: list[dict[str, str]]) -> dict[str, dict[str, Any]]:
    by_id = {}
    for record in records:
        key = record['record_id']
        if key in by_id:
            add_issue(issues, 'blocking', str(LEDGER), f'证据 ID 重复：{key}')
        by_id[key] = record
    for key, record in by_id.items():
        for ref in record['counterevidence_ids'] + record.get('legacy_record_ids', []):
            if ref == key or ref not in by_id:
                add_issue(issues, 'blocking', str(LEDGER), f'{key} 引用无效证据：{ref}')
        if record.get('schema_version') == 2 and record['claim_id'] not in claims:
            add_issue(issues, 'blocking', str(LEDGER), f"{key} 引用无效命题：{record['claim_id']}")
    return by_id


def audit_ledger(root: Path, issues: list[dict[str, str]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    if not (root / LEDGER).is_file():
        add_issue(issues, 'blocking', str(LEDGER), '证据账本不存在')
        return [], {}
    claims = read_claim_index(root, issues)
    records = parse_records(root, (root / LEDGER).read_text(encoding='utf-8'), str(LEDGER), issues, schema_validator(root))
    by_id = check_record_links(records, claims, issues)
    for claim_id, claim in claims.items():
        if not claim['signed']:
            continue
        directions = set()
        for evid in claim['evidence_ids']:
            record = by_id.get(evid, {})
            if (record.get('schema_version') != 2 or record.get('status') != 'verified'
                    or record.get('claim_id') != claim_id or record['reviewed_on'] > claim['reviewed_on']):
                add_issue(issues, 'blocking', str(CLAIMS), f'{claim_id} 的关键证据缺有效的 v2 核验：{evid}')
                continue
            if record['directness'] == 'direct':
                directions.add(record['polarity'])
        if claim['state'] == 'supported' and 'supports' not in directions:
            add_issue(issues, 'blocking', str(CLAIMS), f'{claim_id} 缺少已核验的直接支持证据')
        if claim['state'] == 'contested' and not {'supports', 'challenges'} <= directions:
            add_issue(issues, 'blocking', str(CLAIMS), f'{claim_id} 缺少已核验的相反方向直接证据')
    return records, claims


def add_candidates(root: Path, input_path: Path) -> tuple[int, list[dict[str, str]]]:
    from fcntl import LOCK_EX, flock

    issues: list[dict[str, str]] = []
    claims = read_claim_index(root, issues)
    validator = schema_validator(root)
    candidates = parse_records(root, input_path.read_text(encoding='utf-8'), str(input_path), issues, validator)
    for record in candidates:
        if (record.get('schema_version') != 2 or record['status'] != 'pending_review'
                or 'reviewed_by' in record or 'reviewed_on' in record):
            add_issue(issues, 'blocking', str(input_path), f"候选入口只接收未签审的 v2 pending_review：{record['record_id']}")
    with (root / LEDGER).open('r+', encoding='utf-8') as ledger:
        flock(ledger, LOCK_EX)
        previous_text = ledger.read()
        previous = parse_records(root, previous_text, str(LEDGER), issues, validator)
        previous_ids = {r['record_id']: r for r in previous}
        # An identical retry adds nothing. A reused ID with different content is a conflict.
        new = [record for record in candidates if previous_ids.get(record['record_id']) != record]
        check_record_links(previous + new, claims, issues)
        if any(issue['severity'] == 'blocking' for issue in issues):
            return 0, issues
        if new:
            if previous_text and not previous_text.endswith('\n'):
                ledger.write('\n')
            ledger.write(''.join(json.dumps(record, ensure_ascii=False) + '\n' for record in new))
    return len(new), issues


def inspect_fronts(root: Path, claims: dict[str, Any], issues: list[dict[str, str]]) -> list[str]:
    fronts = {}
    for path in sorted((root / FRONTS).glob('*.md')):
        fm = frontmatter(path)
        if path.name == 'research-front-template.md' or fm.get('type') != 'research-front':
            continue
        rel = str(path.relative_to(root))
        synth = section(path.read_text(encoding='utf-8'), '当前研究认识')
        status, signed_on = fm.get('status'), fm.get('last_synthesized')
        fronts[path.stem] = (status, signed_on or '—')
        claim_ids = fm.get('synthesis_claim_ids')
        evidence_ids = fm.get('synthesis_evidence_ids')
        if not synth or not all(isinstance(ids, list) and all(isinstance(i, str) for i in ids)
                                for ids in (claim_ids, evidence_ids)):
            add_issue(issues, 'blocking', rel, '缺当前研究认识或快照 ID 列表')
            continue
        if (set(claim_ids) != set(CLAIM_ID.findall(synth)) or set(evidence_ids) != set(EVIDENCE_ID.findall(synth))
                or len(set(claim_ids)) != len(claim_ids) or len(set(evidence_ids)) != len(evidence_ids)):
            add_issue(issues, 'blocking', rel, '快照正文与声明的命题或证据 ID 不一致')
        state = fm.get('synthesis_state')
        if state == 'pending_review':
            if status != 'pending_review' or signed_on or fm.get('synthesized_by') or claim_ids or evidence_ids:
                add_issue(issues, 'blocking', rel, '待签审前沿包含正式状态、签审信息或关键引用')
            continue
        if (state != 'signed' or status not in SIGNED_FRONT_STATES or not date_is_valid(signed_on)
                or not nonempty(fm.get('synthesized_by'))):
            add_issue(issues, 'blocking', rel, '正式前沿缺有效状态、签审日期或签审人')
            continue
        required = set()
        for claim_id in claim_ids:
            claim = claims.get(claim_id, {})
            if not claim.get('signed') or claim['reviewed_on'] > signed_on or claim['state'] == 'superseded':
                add_issue(issues, 'blocking', rel, f'引用失效或未签审的命题：{claim_id}')
            else:
                required.update(claim['evidence_ids'])
        if set(evidence_ids) != required:
            add_issue(issues, 'blocking', rel, '快照关键证据与引用命题的已签审依据不一致')
        if status in {'converging', 'diverging', 'conditional_support'} and not required:
            add_issue(issues, 'blocking', rel, '当前状态须有已签审命题和关键证据')
    expected = {}
    if (root / FRONT_INDEX).is_file():
        body = section((root / FRONT_INDEX).read_text(encoding='utf-8'), '当前前沿')
        for row in table_rows(body):
            match = re.fullmatch(r'\[\[([a-z0-9-]+)(?:\\?\|[^\]]+)?\]\]', row[0])
            if len(row) < 3 or not match or match[1] in expected:
                add_issue(issues, 'blocking', str(FRONT_INDEX), f'前沿索引格式错误或重复：{row[0]}')
                continue
            expected[match[1]] = (row[1], row[2])
    if not fronts or expected != fronts:
        add_issue(issues, 'blocking', str(FRONT_INDEX), '索引与前沿页面的状态或签审日期不一致')
    return [str(FRONTS / f'{stem}.md') for stem in fronts]


def check_migration(root: Path, records: list[dict[str, Any]], claims: dict[str, Any], issues: list[dict[str, str]]) -> int:
    path = root / MIGRATION
    if not path.is_file():
        add_issue(issues, 'blocking', str(MIGRATION), '缺旧账本迁移清单')
        return 0
    text = path.read_text(encoding='utf-8')
    fm = frontmatter(path)
    baseline = {r['record_id'] for r in records if r.get('schema_version', 1) == 1}
    ledger_rows = table_rows(section(text, '旧证据账本'))
    mapped = [row[0] for row in ledger_rows]
    if (set(mapped) != baseline or len(mapped) != len(baseline)
            or any(len(row) != 7 or not nonempty(row[-1]) for row in ledger_rows)):
        add_issue(issues, 'blocking', str(MIGRATION), '旧账本的记录与迁移清单不是一一对应')
    original_lines = (root / LEDGER).read_bytes().splitlines(keepends=True)[:len(baseline)]
    if sha256(b''.join(original_lines)).hexdigest() != fm.get('legacy_ledger_sha256'):
        add_issue(issues, 'blocking', str(LEDGER), '冻结的旧账本原文发生变化')
    for match in CLAIM_ID.finditer(text):
        if match[0] not in claims:
            add_issue(issues, 'blocking', str(MIGRATION), f'迁移映射引用了未登记命题：{match[0]}')
    evidence_ids = {r['record_id'] for r in records}
    for match in EVIDENCE_ID.finditer(text):
        if match[0] not in evidence_ids:
            add_issue(issues, 'blocking', str(MIGRATION), f'迁移映射引用了未登记证据：{match[0]}')
    seen = set()
    actual = {'ledger': len(mapped)}
    for heading, prefix, key in (('历史 Claims', 'LEG-C-', 'claims'), ('历史矛盾', 'LEG-R-', 'relations'),
                                 ('前沿历史判断', 'LEG-F-', 'fronts')):
        rows = table_rows(section(text, heading))
        actual[key] = len(rows)
        for row in rows:
            if len(row) != 6 or not row[0].startswith(prefix) or row[0] in seen or not nonempty(row[-1]):
                add_issue(issues, 'blocking', str(MIGRATION), f'历史条目缺稳定 ID、来源或去向：{row[0]}')
            seen.add(row[0])
    if actual != fm.get('frozen_counts'):
        add_issue(issues, 'blocking', str(MIGRATION), '迁移清单计数与冻结范围不一致')
    archives = fm.get('archive_sha256')
    if not isinstance(archives, dict) or len(archives) != actual['fronts'] + 2:
        add_issue(issues, 'blocking', str(MIGRATION), '缺冻结档案的来源与摘要')
        return len(mapped)
    for location, digest in archives.items():
        if not local_file(root, location):
            add_issue(issues, 'blocking', str(MIGRATION), f'冻结来源不存在：{location}')
            continue
        original = (root / location).read_text(encoding='utf-8')
        _, start, tail = original.partition(ARCHIVE_START)
        archived, end, _ = tail.partition(ARCHIVE_END)
        if not start or not end or sha256(archived.encode()).hexdigest() != digest:
            add_issue(issues, 'blocking', location, '冻结的历史正文发生变化')
    return len(mapped)


def registry_stats(root: Path) -> dict[str, int]:
    registry = (root / '00-dashboard/paper-registry.md').read_text(encoding='utf-8')
    notes = {path.name for path in (root / '03-paper-notes').glob('*.md')}
    registered = set()
    for line in registry.splitlines():
        if not line.startswith('|'):
            continue
        for target in re.findall(r'\[\[([^\]|#]+)', line):
            name = Path(target).name
            registered.add(name if name.endswith('.md') else f'{name}.md')
    stats = dict(papers=0, deep=0, talks=0, concepts=0, methods=0, tasks=0, surveys=0, comparisons=0)
    for name in registered & notes:
        fm = frontmatter(root / '03-paper-notes' / name)
        if fm.get('type') == 'paper':
            stats['papers'] += 1
            stats['deep'] += fm.get('reading_level') in ('L3', 'L4')
        elif fm.get('type') == 'academic-talk':
            stats['talks'] += 1
    for number, key in enumerate(('concepts', 'methods', 'tasks', 'surveys', 'comparisons'), start=4):
        stats[key] = len(list((root / f'{number:02d}-{key}').glob('*.md')))
    return stats
