"""Hash-bound TOP300 proposals. Never executes strategy source."""
import hashlib
import json
from pathlib import Path
import re
from tools.strategy_catalog.analyzer import _source


def sha(value):
    return hashlib.sha256(value.encode('utf-8') if isinstance(value,str) else value).hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def proposal_digest(record):
    return sha(json.dumps(record,ensure_ascii=False,sort_keys=True,separators=(',',':')))


def validate_record_shape(r):
    if type(r.get('sid')) is not int or type(r.get('rank')) is not int:
        raise ValueError('SID/rank must be integers')
    for key in ('source_sha256','base_sha256'):
        if not re.fullmatch('[0-9a-f]{64}',r.get(key,'')):raise ValueError('Invalid hash: '+key)
    if r.get('base_kind') not in ('original','prior_candidate'):raise ValueError('Invalid base kind')
    action=r.get('action')
    if action not in ('new_patch','carry_existing','unchanged','deferred_design'):raise ValueError('Invalid action')
    if r.get('change_type') not in ('correctness','design_experiment','mixed','none'):raise ValueError('Invalid change type')
    if not isinstance(r.get('summary'),str) or not r['summary'].strip():raise ValueError('Missing individual summary')
    for key in ('resolved','remaining','validation_plan'):
        if not isinstance(r.get(key),list) or any(not isinstance(x,str) or not x.strip() for x in r[key]):raise ValueError('Invalid list: '+key)
    if not r['remaining'] or not r['validation_plan']:raise ValueError('Unverified scope must be explicit')
    patches=r.get('patches')
    if not isinstance(patches,list) or bool(patches)!=(action=='new_patch'):raise ValueError('Action/patch mismatch')
    if action=='new_patch' and (r['change_type']=='none' or not r['resolved']):raise ValueError('Missing change classification')
    if action!='new_patch' and r['change_type']!='none':raise ValueError('Non-patch action must use none')
    if action=='carry_existing' and r['base_kind']!='prior_candidate':raise ValueError('Carry requires prior candidate')
    if action in ('unchanged','deferred_design') and r['base_kind']!='original':raise ValueError('Unmodified action requires original')
    for p in patches:
        for key in ('old','reason','preserved'):
            if not isinstance(p.get(key),str) or not p[key].strip():raise ValueError('Missing patch field: '+key)
        for key in ('reason','preserved'):
            if not re.search(r'[\u4e00-\u9fff]',p[key]):raise ValueError('Chinese explanation required: '+key)
        if not isinstance(p.get('new'),str) or p['old']==p['new']:raise ValueError('Empty/no-op patch')
        cases=p.get('validation_cases')
        if not isinstance(cases,list) or not cases or any(not isinstance(x,str) or not x.strip() for x in cases):raise ValueError('Missing validation cases')
    return True


def resolve_base(root,record):
    root=Path(root).resolve();sid=record['sid']
    selected={r['sid']:r for r in read_json(root/'analysis/top300/ranking.json')}
    meta={r['sid']:r for r in read_json(root/'analysis/top300/pinescript/manifest.json')}[sid]
    if sid not in selected or selected[sid]['rank']!=record['rank'] or selected[sid]['id'] not in meta['file']:
        raise ValueError('Selection identity drift')
    if not re.fullmatch('[0-9a-f]{12}',selected[sid]['id']):raise ValueError('Unsafe strategy ID')
    source_path=(root/meta['source_file']).resolve()
    if source_path.parent!=root or Path(meta['source_file']).name!=meta['source_file'] or source_path.suffix!='.md':raise ValueError('Unsafe original source path')
    raw=source_path.read_bytes()
    if sha(raw)!=record['source_sha256'] or sha(raw)!=selected[sid]['source_sha256'] or sha(raw)!=meta['source_sha256']:
        raise ValueError('Original source drift')
    original,_,_=_source(raw.decode('utf-8'))
    expected_name=f"{record['rank']:03d}_SID{sid}_{selected[sid]['id']}.pine"
    if meta['file']!=expected_name:raise ValueError('Unexpected source export path')
    export=(root/'analysis/top300/pinescript'/expected_name).read_bytes()
    if export!=original.encode('utf-8') or sha(export)!=meta['pine_sha256']:raise ValueError('Original Pine export drift')
    if record['base_kind']=='original':
        code=original
    elif record['base_kind']=='prior_candidate':
        old={r['sid']:r for r in read_json(root/'analysis/top500/optimization/manifest.json')}[sid]
        expected=f"variants/{selected[sid]['id']}/conservative.pine"
        if old['variant']!=expected or old['source_sha256']!=record['source_sha256'] or old['status']!='candidate':raise ValueError('Prior candidate identity mismatch')
        payload=(root/'analysis/top500/optimization'/expected).read_bytes()
        if sha(payload)!=old['variant_sha256']:raise ValueError('Prior candidate drift')
        code=payload.decode('utf-8')
    else:raise ValueError('Unknown base kind')
    if sha(code)!=record['base_sha256']:raise ValueError('Proposal baseline drift')
    return code


def apply_record(code,record):
    validate_record_shape(record)
    if sha(code)!=record['base_sha256']:raise ValueError('Proposal baseline drift')
    annotations=[]
    for n,p in enumerate(record['patches'],1):
        if code.count(p['old'])!=1:raise ValueError(f"SID {record['sid']} patch {n}: match must be unique")
        offset=code.index(p['old']);end=offset+len(p['old']);delta=len(p['new'])-len(p['old'])
        for annotation in annotations:
            if annotation[0]>=end:annotation[0]+=delta
            elif annotation[0]>=offset:annotation[0]=offset
        annotations.append([offset,n,p])
        code=code[:offset]+p['new']+code[end:]
    notes={}
    for offset,n,p in annotations:
        start=code.rfind('\n',0,min(offset,len(code)))+1
        indent=re.match(r'[ \t]*',code[start:])[0]
        clean=lambda s:s.replace('\r',' ').replace('\n',' ')
        note=f"{indent}// OPT-T300-{n:02d} 修改原因：{clean(p['reason'])}\n{indent}// OPT-T300-{n:02d} 保持行为：{clean(p['preserved'])}\n"
        notes.setdefault(start,[]).append(note)
    for start in sorted(notes,reverse=True):code=code[:start]+''.join(notes[start])+code[start:]
    return code


def validate_approvals(records,approvals):
    proposed={str(r['sid']):r for r in records if r['action']=='new_patch'}
    if set(approvals)!=set(proposed):raise ValueError('Every new patch requires independent review')
    for sid,r in proposed.items():
        a=approvals[sid]
        if a.get('status')!='approved' or a.get('record_sha256')!=proposal_digest(r) or not a.get('review','').strip():
            raise ValueError('Missing, deferred or stale approval for SID '+sid)
    return True


def load_records(root,require_approvals=True):
    root=Path(root);directory=root/'analysis/top300/execution'
    selected=read_json(root/'analysis/top300/ranking.json');records=[]
    if len(selected)!=300 or len({r['sid'] for r in selected})!=300 or [r['rank'] for r in selected]!=list(range(1,301)):
        raise ValueError('Ranking must contain exactly 300 unique ordered identities')
    for n in (1,2,3):
        group=read_json(directory/f'batch_{n}.json')
        if len(group)!=100 or {r['rank'] for r in group}!=set(range(100*(n-1)+1,100*n+1)):raise ValueError('Batch coverage mismatch')
        records.extend(group)
    if len({r['sid'] for r in records})!=300:raise ValueError('Duplicate or missing SID')
    records.sort(key=lambda r:r['rank'])
    for r,original in zip(records,selected):
        if (r['sid'],r['rank'],r['source_sha256'])!=(original['sid'],original['rank'],original['source_sha256']):raise ValueError('Selection mismatch')
        validate_record_shape(r)
        apply_record(resolve_base(root,r),r)
    approvals=read_json(directory/'approvals.json') if require_approvals else {}
    if require_approvals:validate_approvals(records,approvals)
    return records,approvals
