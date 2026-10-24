"""Independently check optimization provenance; never compile or execute Pine."""
from __future__ import annotations
import argparse
import csv
import difflib
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlparse

from tools.strategy_catalog.analyzer import _source
from tools.strategy_catalog.verify import Links

CSV_FIELDS = ('research_index','sid','id','title','category','status','severity','issues','remaining','audit_synopsis','audit_verdict','audit_findings','patch_review','verification','filename','source_sha256','original_code_sha256','variant_sha256','card','variant','changes','diff')
INDEX_FIELDS = ('id','sid','title','category','research_index','status','severity','card')

CANDIDATE_SIDS = {735, 5369, 621, 4143, 3883, 3322, 2458, 4621, 2943, 3330, 4941}


def _sha(data):
    return hashlib.sha256(data).hexdigest()


def _no_performance(value):
    if isinstance(value, dict):
        for key, child in value.items():
            if re.search(r'optimized.*(?:return|sharpe|profit|cagr|calmar|drawdown)|backtest_results|优化后.*(?:收益|绩效)', key, re.I):
                raise ValueError('禁止未经回测的优化收益字段: '+key)
            _no_performance(child)
    elif isinstance(value, list):
        for child in value: _no_performance(child)


def validate_manifest(records, ranking, expected_count=500, candidate_sids=None):
    candidate_sids=CANDIDATE_SIDS if candidate_sids is None else candidate_sids
    if len(records)!=expected_count or len(ranking)!=expected_count:
        raise ValueError('登记数量必须对应全部研究名单')
    if len({r['id'] for r in records})!=len(records) or len({r['sid'] for r in records})!=len(records):
        raise ValueError('重复身份')
    _no_performance(records)
    for r, original in zip(records, ranking):
        for field in ('id','sid','research_index','filename','source_sha256'):
            if r.get(field)!=original.get(field):raise ValueError('排名身份或顺序不一致: '+field)
        for field in ('source_sha256','original_code_sha256'):
            if not re.fullmatch('[0-9a-f]{64}',r.get(field,'')):raise ValueError('无效SHA: '+field)
        if r.get('status') not in ('candidate','needs_design','needs_review','reviewed'):raise ValueError('无效状态')
        if r['status']=='reviewed' and (r.get('audit',{}).get('review_scope')!='full_source_static' or r['audit'].get('verdict')!='no_confirmed_defect'):raise ValueError('未审查不得标记已审')
        if not isinstance(r.get('issues'),list) or not isinstance(r.get('remaining'),list):raise ValueError('缺少问题/待验证列表')
        verification=r.get('verification',{})
        if verification.get('native_compile') is not False or verification.get('backtest') is not False or not verification.get('local_checks'):
            raise ValueError('不得宣称已原生编译或回测')
        if r.get('card')!='cards/'+r['id']+'.html':raise ValueError('卡片路径不正确')
        candidate=r['status']=='candidate'
        if candidate != (r['sid'] in candidate_sids):raise ValueError('候选修复名单不一致')
        paths={'variant':'conservative.pine','original_variant':'original.pine','diff':'changes.patch','changes':'changes.md'}
        for field, name in paths.items():
            expected='variants/'+r['id']+'/'+name if candidate else None
            if r.get(field)!=expected:raise ValueError('产物路径不正确: '+field)
        if candidate:
            if not re.fullmatch('[0-9a-f]{64}',r.get('variant_sha256') or ''):raise ValueError('候选SHA不正确')
        elif r.get('variant_sha256') is not None:raise ValueError('无候选不得登记候选SHA')
    return True


def validate_views(records, csv_rows, index):
    match=re.search(r'<script id="optimization-data" type="application/json">(.*?)</script>',index,re.S)
    if not match:raise ValueError('入口缺少登记数据')
    embedded=json.loads(match[1])
    if len(csv_rows)!=len(records) or len(embedded)!=len(records):raise ValueError('CSV/入口登记数量不符')
    for row, record in zip(csv_rows,records):
        if set(row)!=set(CSV_FIELDS):raise ValueError('CSV字段缺失或不匹配')
        for key in CSV_FIELDS:
            value=record.get(key,'')
            if isinstance(value,(dict,list)):value=json.dumps(value,ensure_ascii=False)
            if isinstance(value,str) and value.startswith(('=','+','-','@','\t','\r')):value="'"+value
            expected='' if value is None else str(value)
            if row[key]!=expected:raise ValueError('CSV数据不一致: '+key)
    for row, record in zip(embedded,records):
        if row!={key:record.get(key) for key in INDEX_FIELDS}:raise ValueError('入口数据不一致')
    return True



def validate_audit_metadata(record, audit):
    for field in ('synopsis','verdict','findings'):
        if record.get('audit_'+field)!=audit[field]:raise ValueError('审查导出字段与原记录不一致: '+field)
    return True


def validate_documents(record, card, changes=None):
    from .build import render_card, changes_md
    if card!=render_card(record):raise ValueError('状态卡与登记内容不一致')
    if record['status']=='candidate' and changes!=changes_md(record):raise ValueError('修改说明与登记内容不一致')
    return True


def validate_variant(original, candidate, record, registry=None):
    from .fixes import apply_fix
    from .build import annotated_code
    expected=annotated_code(apply_fix(record['sid'],original,record['source_sha256'],registry=registry),record)
    if candidate!=expected:raise ValueError('候选与批准修复规则重新生成结果不一致')
    return True


def validate_patch(original, candidate, patch):
    expected=''.join(difflib.unified_diff(original.splitlines(keepends=True),candidate.splitlines(keepends=True),fromfile='original.pine',tofile='conservative.pine'))
    if patch!=expected:raise ValueError('补丁与原代码/候选不匹配')
    return True


def _links(path, root):
    content=path.read_text(encoding='utf-8')
    if path.suffix=='.html':
        parser=Links();parser.feed(content);links=parser.links
    else:links=re.findall(r'\]\(([^)]+)\)',content)
    targets=set()
    for link in links:
        url=urlparse(link)
        if not url.scheme and url.path:
            target=(path.parent/unquote(url.path)).resolve()
            if root.resolve() not in target.parents or not target.is_file():raise ValueError('坏的本地链接: '+str(path)+' '+link)
            targets.add(target)
    return targets


def verify(root):
    root=Path(root).resolve();out=root/'analysis/top500/optimization'
    ranking_path=root/'analysis/top500/ranking.json';catalog_path=root/'analysis/catalog.json'
    records=json.loads((out/'manifest.json').read_text(encoding='utf-8'))
    ranking=json.loads(ranking_path.read_text(encoding='utf-8'))
    from .audit import load_audit
    from .build import audit_status
    catalog={r['filename']:r for r in json.loads(catalog_path.read_text(encoding='utf-8'))}
    audits,registry,approvals=load_audit(root,ranking,catalog)
    validate_manifest(records,ranking,candidate_sids=set(registry))
    if audits:
        for r in records:
            if r['sid'] in audits and (r.get('audit')!=audits[r['sid']] or r['status']!=audit_status(audits[r['sid']],r['sid'] in registry)):raise ValueError('审查记录或状态未准确反映审查结果')
            if r['sid'] in audits:validate_audit_metadata(r,audits[r['sid']])
            if str(r['sid']) in approvals and r.get('patch_review')!=approvals[str(r['sid'])]:raise ValueError('补丁复核状态不符')
    with (out/'manifest.csv').open(encoding='utf-8-sig',newline='') as stream:csv_rows=list(csv.DictReader(stream))
    validate_views(records,csv_rows,(out/'index.html').read_text(encoding='utf-8'))
    summary=json.loads((out/'summary.json').read_text(encoding='utf-8'))
    if summary.get('audited_remaining',0)!=len(audits):raise ValueError('审查覆盖统计不符')
    if audits:
        inputs={p.name:_sha(p.read_bytes()) for p in sorted((out/'audit').glob('*.json'))}
        if summary.get('audit_inputs')!=inputs:raise ValueError('审查输入文件漂移')
    for key,path in [('ranking_sha256',ranking_path),('catalog_sha256',catalog_path)]:
        if summary.get(key)!=_sha(path.read_bytes()):raise ValueError('输入文件SHA不匹配: '+key)
    if {p.stem for p in (out/'cards').glob('*.html')}!={r['id'] for r in records}:raise ValueError('卡片覆盖不一致')
    links=0;variants=0
    for r in records:
        source=root/r['filename'];raw=source.read_bytes()
        if _sha(raw)!=r['source_sha256']:raise ValueError('原文件SHA不匹配: '+r['filename'])
        code,_,_=_source(raw.decode('utf-8'))
        if _sha(code.encode('utf-8'))!=r['original_code_sha256']:raise ValueError('原提取源码SHA不匹配')
        card=out/r['card']
        changes=(out/r['changes']).read_text(encoding='utf-8') if r['status']=='candidate' else None
        validate_documents(r,card.read_text(encoding='utf-8'),changes)
        targets=_links(card,root);links+=len(targets)
        if source.resolve() not in targets:raise ValueError('状态卡缺少原文件链接')
        ranking_card=root/'analysis/top500/cards'/(r['id']+'.html')
        if ranking_card.resolve() not in targets or card.resolve() not in _links(ranking_card,root):
            raise ValueError('原分析卡与优化卡缺少双向链接')
        if r['status']=='candidate':
            variant=out/r['variant'];text=variant.read_text(encoding='utf-8')
            if _sha(variant.read_bytes())!=r['variant_sha256']:raise ValueError('候选SHA不匹配')
            validate_variant(code,text,r,registry=registry)
            original=code.rstrip('\n')+'\n'
            if (out/r['original_variant']).read_text(encoding='utf-8')!=original:raise ValueError('原代码快照不匹配')
            validate_patch(original,text,(out/r['diff']).read_text(encoding='utf-8'))
            for required in ('OPT',r['source_sha256'],str(r['sid']),'未原生编译','未回测'):
                if required not in text:raise ValueError('候选缺少追溯或验证状态: '+required)
            if '//@version=' in text and not text.startswith('//@version='):raise ValueError('Pine版本指令不在首行')
            for key in ('variant','original_variant','diff','changes'):
                if (out/r[key]).resolve() not in targets:raise ValueError('状态卡缺少产物链接: '+key)
            variants+=1
    for path in sorted(out.rglob('*')):
        if path.suffix in ('.html','.md'):
            links+=len(_links(path,root))
    return dict(status='PASS',records=len(records),candidates=variants,source_hashes=len(records),local_links=links,native_compile=False,backtest=False)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[2]);args=parser.parse_args()
    print(json.dumps(verify(args.root),ensure_ascii=False,indent=2))

if __name__=='__main__':main()
