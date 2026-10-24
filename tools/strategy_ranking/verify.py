"""Verify ranking math, cohort separation, provenance, coverage and local links."""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import re
from urllib.parse import unquote,urlparse
from tools.strategy_catalog.verify import Links


def validate_ranked(records):
    for key in ('id','sid','representative_sid'):
        if len({r[key] for r in records})!=len(records):raise ValueError('重复身份或代表组: '+key)
    if [r['research_index'] for r in records]!=list(range(1,len(records)+1)):raise ValueError('名单序号不连续')
    main=[r for r in records if r['cohort']=='full_daily'];supp=[r for r in records if r['cohort']!='full_daily']
    if records!=main+supp:raise ValueError('主榜和补充混排')
    if [r['primary_rank'] for r in main]!=list(range(1,len(main)+1)):raise ValueError('主榜名次不连续')
    for pool in (main,supp):
        if any(a['combined_score']<b['combined_score'] for a,b in zip(pool,pool[1:])):raise ValueError('同层排序不正确')
    for r in records:
        if r['cohort']!='full_daily' and r['primary_rank'] is not None:raise ValueError('补充不得占主榜名次')
        expected=.7*r['daily_score']+.1*(r['recent_score'] or 0)+.2*r['current_logic_score']-r['risk_penalty']
        if abs(expected-r['combined_score'])>1e-8:raise ValueError('综合分错误')
        if not r['source_match']['lossy_match'] or r['source_match']['version_verified']:raise ValueError('身份声明不正确')
        d=r['reported_daily']
        if any(d[k] is None or not math.isfinite(d[k]) for k in ('cagr','sharpe','max_dd','calmar')):raise ValueError('主指标缺失/非有限')
        if d['trades']<100 or d['exposure']<.02 or d['sharpe']>3 or not -1<=d['max_dd']<=0:raise ValueError('准入门槛失败')
        if r['cohort']=='full_daily' and (d['errs']!=0 or d['tickers_run']<1000):raise ValueError('全量运行质量失败')
        if any(x.get('sharpe') is not None and x['sharpe']>3 for x in r.get('intraday',[])):raise ValueError('日内异常未隔离')
    return True


def verify(root,source):
    out=root/'analysis/top500';records=json.loads((out/'ranking.json').read_text());summary=json.loads((out/'summary.json').read_text());validate_ranked(records)
    manifest=json.loads((out/'source_manifest.json').read_text())
    for item in manifest:
        path=Path(item['path']);path=path if path.is_absolute() else source/path
        if path.suffix=='.env':raise ValueError('凭证不应被读取')
        if hashlib.sha256(path.read_bytes()).hexdigest()!=item['sha256']:raise ValueError('输入数据改变: '+str(path))
    from .rank import build_dataset
    dataset=build_dataset(source,root/'analysis/catalog.json')
    expected=dataset['primary'][:summary['primary_count']]+dataset['supplement_pool'][:summary['supplement_count']]
    if [r['sid'] for r in records]!=[r['sid'] for r in expected]:raise ValueError('生成名单与从原始输入重算不一致')
    for a,b in zip(records,expected):
        for field in ('combined_score','daily_score','recent_score','current_logic_score','risk_penalty','cohort','primary_rank'):
            if a[field]!=b[field]:raise ValueError('重算字段不一致: '+field)
    if summary['selected_count']!=len(records):raise ValueError('summary与名单不一致')
    ids={r['id'] for r in records};links=0;reviewed=0
    for ext in ('md','html'):
        if {p.stem for p in (out/'cards').glob('*.'+ext)}!=ids:raise ValueError('卡片覆盖不同于名单')
    for r in records:
        raw=(root/r['filename']).read_bytes()
        if hashlib.sha256(raw).hexdigest()!=r['source_sha256']:raise ValueError('源策略变更')
        for ext in ('md','html'):
            p=out/'cards'/(r['id']+'.'+ext);content=p.read_text()
            for required in ('入场','出场','策略原理','完整源码','回测引擎差异',r['source_sha256']):
                if required not in content:raise ValueError('卡片缺字段: '+required)
            if ext=='html':
                parser=Links();parser.feed(content)
                for link in parser.links:
                    url=urlparse(link)
                    if not url.scheme and url.path:
                        if not (p.parent/unquote(url.path)).is_file():raise ValueError('坏链接: '+link)
                        links+=1
        if '源码精读' in r['detail_level']:reviewed+=1
    with (out/'ranking.csv').open(encoding='utf-8-sig',newline='') as f:csvrows=list(csv.DictReader(f))
    if [r['id'] for r in csvrows]!=[r['id'] for r in records]:raise ValueError('CSV覆盖或顺序不一致')
    for name in ('index.html','REPORT.md','methodology.md','excluded.csv'):
        if not (out/name).is_file():raise ValueError('缺少产物: '+name)
    index=(out/'index.html').read_text();match=re.search(r'<script id="ranking-data" type="application/json">(.*?)</script>',index,re.S)
    if not match or [r['id'] for r in json.loads(match[1])]!=[r['id'] for r in records]:raise ValueError('页面数据不一致')
    parser=Links();parser.feed(index)
    for link in parser.links:
        url=urlparse(link)
        if not url.scheme and url.path:
            if not (out/unquote(url.path)).is_file():raise ValueError('入口链接错误: '+link)
            links+=1
    for link in re.findall(r'\]\(([^)]+)\)',(out/'REPORT.md').read_text()):
        url=urlparse(link)
        if not url.scheme and url.path:
            if not (out/unquote(url.path)).is_file():raise ValueError('报告链接错误: '+link)
            links+=1
    return dict(status='PASS',selected=len(records),primary=summary['primary_count'],supplement=summary['supplement_count'],cards=len(records)*2,source_hashes=len(records),input_files=len(manifest),local_links=links,recomputed_scores=len(records),source_reviewed=reviewed)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--source',type=Path,required=True);args=parser.parse_args()
    print(json.dumps(verify(Path(__file__).resolve().parents[2],args.source),ensure_ascii=False,indent=2))
if __name__=='__main__':main()
