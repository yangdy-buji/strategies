"""Check full inventory, immutable source fingerprints, evidence lines and links."""
from __future__ import annotations
import hashlib
import csv
import re
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.parse import unquote, urlparse
from .build import validate_records

class Links(HTMLParser):
    def __init__(self):
        super().__init__();self.links=[]
    def handle_starttag(self,tag,attrs):
        if tag=='a':
            self.links.extend(v for k,v in attrs if k=='href')

def verify_inventory(root,output):
    records=json.loads((output/'catalog.json').read_text())
    expected={p.name for p in root.glob('*.md')}
    actual=[r['filename'] for r in records]
    if len(set(actual))!=len(actual) or set(actual)!=expected:
        raise ValueError('源文件覆盖不完整或重复')
    validate_records(records)
    card_ids={r['id'] for r in records}
    for ext in ('md','html'):
        if {p.stem for p in (output/'cards').glob('*.'+ext)}!=card_ids:
            raise ValueError('卡片缺失或有过期卡片: '+ext)
    links_checked=0
    for r in records:
        source=root/r['filename'];raw=source.read_bytes()
        if hashlib.sha256(raw).hexdigest()!=r['source_sha256']:raise ValueError('源文件已变: '+r['filename'])
        lines=raw.decode('utf-8').splitlines()
        if r['code']:
            code_lines=r['code'].splitlines();start=r['code_start_line']-1
            if lines[start:start+len(code_lines)]!=code_lines:raise ValueError('提取源码与行号不匹配: '+r['filename'])
        for evidence in r.get('entry_rules',[])+r.get('exit_rules',[])+r.get('review_evidence',[]):
            if not 1<=evidence['line']<=len(lines):raise ValueError('证据行号越界')
        for ext in ('md','html'):
            card=output/'cards'/(r['id']+'.'+ext);content=card.read_text()
            for required in ('入场','出场','策略原理','完整源码','未验证',r['source_sha256']):
                if required not in content:raise ValueError('卡片缺少字段: '+str(card)+' '+required)
            if ext=='html':
                parser=Links();parser.feed(content)
                for link in parser.links:
                    url=urlparse(link)
                    if not url.scheme and url.path:
                        target=card.parent/unquote(url.path)
                        if not target.is_file():raise ValueError('链接不存在: '+str(target))
                        links_checked+=1
    for name in ('index.html','README.md','methodology.md','catalog.csv','summary.json'):
        if not (output/name).is_file():raise ValueError('缺少入口产物: '+name)
    index=(output/'index.html').read_text()
    match=re.search(r'<script id="catalog-data" type="application/json">(.*?)</script>',index,re.S)
    if not match:raise ValueError('交互目录缺少内嵌数据')
    embedded=json.loads(match[1])
    if {r['id'] for r in embedded}!=card_ids or len(embedded)!=len(records):raise ValueError('交互目录覆盖不完整')
    with (output/'catalog.csv').open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
    if {r['id'] for r in rows}!=card_ids or len(rows)!=len(records):raise ValueError('CSV覆盖不完整')
    for row in rows:
        if not (output/row['card']).is_file():raise ValueError('CSV卡片链接不存在')
        links_checked+=1
    parser=Links();parser.feed(index)
    for link in parser.links:
        url=urlparse(link)
        if not url.scheme and url.path:
            if not (output/unquote(url.path)).is_file():raise ValueError('入口链接不存在: '+link)
            links_checked+=1
    for link in re.findall(r'\]\(([^)]+)\)',(output/'README.md').read_text()):
        url=urlparse(link)
        if not url.scheme and url.path:
            if not (output/unquote(url.path)).is_file():raise ValueError('README链接不存在: '+link)
            links_checked+=1
    return {'files':len(records),'cards':len(records)*2,'source_hashes_verified':len(records),'local_links_checked':links_checked,'status':'PASS'}

def main():
    root=Path(__file__).resolve().parents[2]
    print(json.dumps(verify_inventory(root,root/'analysis'),ensure_ascii=False,indent=2))
if __name__=='__main__':main()
