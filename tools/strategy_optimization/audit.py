"""Validate source-bound review records and explicitly reviewed repair proposals."""
import hashlib
import json
from pathlib import Path

VERDICTS={'no_confirmed_defect','needs_design','fix_proposed'}


def patch_digest(record):
    payload={k:record[k] for k in ('sid','source_sha256','code_sha256','patches')}
    return hashlib.sha256(json.dumps(payload,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def validate_audits(records, sources):
    expected={s['sid']:s for s in sources}
    if len(records)!=len(expected) or {r['sid'] for r in records}!=set(expected):
        raise ValueError('审查数量/身份不匹配或存在重复')
    for r in records:
        source=expected[r['sid']];code=source['code'];lines=code.splitlines();start=source['code_start_line']
        for key in ('id','filename','source_sha256'):
            if r.get(key)!=source[key]:raise ValueError(f'SID {r["sid"]} 审查来源漂移: {key}')
        if r.get('code_sha256')!=hashlib.sha256(code.encode()).hexdigest() or r.get('code_lines')!=len(lines):raise ValueError('审查代码指纹/行数不符')
        if r.get('review_scope')!='full_source_static' or not r.get('synopsis','').strip():raise ValueError('缺少具体全文静态审查说明')
        if r.get('verdict') not in VERDICTS or not isinstance(r.get('findings'),list):raise ValueError('审查结论或发现格式不符')
        if not r.get('evidence'):raise ValueError('缺少源码证据')
        for item in r['evidence']:
            offset=item['line']-start
            if offset<0 or offset>=len(lines) or item.get('code')!=lines[offset] or not item.get('reason'):raise ValueError(f'SID {r["sid"]} 原始行证据不匹配: {item.get("line")}')
        for item in r['findings']:
            if item.get('severity') not in {'high','medium','low'} or not item.get('kind') or not item.get('detail') or not item.get('resolution'):raise ValueError('发现缺少严重度/问题/处置')
            if not start<=item.get('evidence_line',-1)<start+len(lines):raise ValueError('发现证据行越界')
        if bool(r.get('patches')) != (r['verdict']=='fix_proposed'):raise ValueError('补丁与结论矛盾')
        patched=code
        for p in r.get('patches',[]):
            if not all(isinstance(p.get(k),str) and p[k].strip() for k in ('old','reason','preserved')) or not isinstance(p.get('new'),str) or not p.get('validation_cases'):raise ValueError('补丁缺少内容/原因/保持项/用例')
            if p['old']==p['new'] or patched.count(p['old'])!=1:raise ValueError(f'SID {r["sid"]} 补丁不唯一或没有变化')
            patched=patched.replace(p['old'],p['new'],1)
    return True


def approved_registry(records, approvals):
    registry={};proposed={str(r['sid']) for r in records if r['patches']}
    if set(approvals)!=proposed:raise ValueError('新增补丁必须逐项独立复核，审批数量不一致')
    for r in records:
        if not r['patches']:continue
        approval=approvals[str(r['sid'])]
        if approval.get('status') not in {'approved','deferred'} or not approval.get('review','').strip() or approval.get('patch_sha256')!=patch_digest(r):raise ValueError(f'SID {r["sid"]} 补丁复核无效或过期')
        if approval['status']=='deferred':continue
        registry[r['sid']]=dict(title=r['synopsis'],source_sha256=r['source_sha256'],code_sha256=r['code_sha256'],
            patches=[(p['old'],p['new'],p['reason'],p['preserved']) for p in r['patches']],
            changes=[p['reason'] for p in r['patches']],remaining=approval.get('remaining',[])+['修复候选未原生编译/回测；旧排名收益不适用。'],
            validation_cases=[case for p in r['patches'] for case in p['validation_cases']])
    return registry


def load_audit(root, ranking, catalog):
    from .fixes import FIXES
    directory=Path(root)/'analysis/top500/optimization/audit'
    if not (directory/'assignments.json').exists():return {},dict(FIXES),{}
    assignments=json.loads((directory/'assignments.json').read_text())
    remaining=[r for r in ranking if r['sid'] not in FIXES]
    assigned=[sid for group in assignments.values() for sid in group]
    if len(assigned)!=489 or len(set(assigned))!=489 or set(assigned)!={r['sid'] for r in remaining}:raise ValueError('489审查清单必须完整且无重复')
    records=[]
    for group,sids in assignments.items():
        batch=json.loads((directory/f'batch_{group}.json').read_text())
        if len(batch)!=len(sids) or {r['sid'] for r in batch}!=set(sids):raise ValueError('审查组范围错误: '+group)
        records.extend(batch)
    sources=[dict(catalog[r['filename']],sid=r['sid']) for r in remaining]
    validate_audits(records,sources)
    approvals=json.loads((directory/'patch_approvals.json').read_text())
    registry=dict(FIXES);registry.update(approved_registry(records,approvals))
    return {r['sid']:r for r in records},registry,approvals
