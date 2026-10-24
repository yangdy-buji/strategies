"""Build an offline, evidence-linked strategy research catalog. No trading execution."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from concurrent.futures import ProcessPoolExecutor
import csv
import hashlib
import html
import json
from pathlib import Path
from urllib.parse import quote, urlparse

REVIEW_FIELDS = {'filename','source_sha256','category','family','tags','principle',
    'entry_explanation','exit_explanation','position_explanation','parameter_explanation',
    'strengths','weaknesses','verification_notes','scores','score','review_status',
    'classification_confidence','review_evidence','kind'}
WEIGHTS = {'获利机制':20,'信号因果性':25,'规则完整性':20,'风险与仓位':20,'美股执行':15}
CSS = """
:root{--bg:#f3f5f7;--paper:#fff;--text:#172c3b;--muted:#526575;--accent:#006d70;--border:#d9e1e6;--warn:#825800;--space:1rem;--radius:.6rem;--small:.87rem;--body:1rem;--title:1.85rem;--max:95rem;--control:2.8rem}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:var(--body)/1.65 system-ui,-apple-system,'PingFang SC',sans-serif}main{max-width:var(--max);margin:auto;padding:calc(var(--space)*2)}h1{font-size:var(--title);line-height:1.35;overflow-wrap:anywhere}h2{font-size:1.25rem;margin-top:calc(var(--space)*2)}a{color:var(--accent);overflow-wrap:anywhere}p,li{overflow-wrap:anywhere}.muted,small{color:var(--muted)}.notice{border-left:.25rem solid var(--warn);background:var(--paper);padding:var(--space)}.filters{display:flex;flex-wrap:wrap;gap:var(--space);margin:var(--space) 0}.filters label{display:grid;gap:.25rem;min-width:10rem}input,select,button{font:inherit;min-height:var(--control);padding:.5rem;border:1px solid var(--border);border-radius:var(--radius);background:var(--paper);color:var(--text)}button{cursor:pointer}button:disabled{opacity:.45;cursor:default}input:focus,select:focus,button:focus,a:focus{outline:2px solid var(--accent);outline-offset:2px}.table-wrap{overflow:auto;background:var(--paper);border:1px solid var(--border);border-radius:var(--radius)}table{border-collapse:collapse;width:100%}th,td{text-align:left;vertical-align:top;padding:.75rem;border-bottom:1px solid var(--border)}th{background:var(--bg);white-space:nowrap}td:first-child{min-width:20rem;max-width:40rem}.badge{display:inline-block;background:var(--bg);border:1px solid var(--border);border-radius:var(--radius);padding:.1rem .45rem;margin:.15rem;font-size:var(--small)}pre{overflow:auto;white-space:pre-wrap;overflow-wrap:anywhere;padding:var(--space);background:#eaf0f3;border-radius:var(--radius);font-size:var(--small)}code{font-family:ui-monospace,monospace}details{margin:var(--space) 0}summary{cursor:pointer;color:var(--accent);padding:.4rem 0}.pager{display:flex;align-items:center;gap:var(--space);margin:var(--space) 0}.card{max-width:70rem}.prose{white-space:pre-wrap}.meta{display:flex;flex-wrap:wrap;gap:.5rem}.score{font-weight:700}.empty{padding:calc(var(--space)*2)}@media(max-width:40rem){main{padding:var(--space)}.filters label{width:100%}h1{font-size:1.45rem}td:first-child{min-width:16rem}}
"""


def apply_reviews(records, reviews):
    by_name = {r['filename']: dict(r) for r in records}
    seen = set()
    for review in reviews:
        name = review['filename']
        if name in seen or name not in by_name:
            raise ValueError('重复或未知的复核文件: '+name)
        seen.add(name)
        if review['source_sha256'] != by_name[name]['source_sha256']:
            raise ValueError('复核源码哈希已失效: '+name)
        if set(review) - REVIEW_FIELDS:
            raise ValueError('复核包含未授权字段: '+str(set(review)-REVIEW_FIELDS))
        by_name[name].update(review)
    return list(by_name.values())


def bullets(items, fallback='未识别；需要结合完整源码复核，不能据此断定不存在。'):
    return '\n'.join('- '+str(x).replace('\n','\n  ') for x in items) if items else '- '+fallback


def fence(code, language='text'):
    marker='`'*max(3, max((len(s) for s in __import__('re').findall(r'`+',code)),default=0)+1)
    return marker+language+'\n'+code+'\n'+marker


def source_link(r):
    return '../../'+quote(r['filename'])


def numbered_code(r):
    return '\n'.join(f'{r["code_start_line"]+i:>5} | {s}' for i,s in enumerate(r['code'].splitlines()))


def score_label(r):
    if r['score'] is None: return '不评分'
    return f'{r["score"]}/100（'+('源码复核分' if r['review_status']=='源码复核' else '自动初评分')+'）'


def rule_markdown(r, name):
    key = name+'_explanation'
    out=bullets(r.get(key,[])) if r.get(key) else '以下是静态抽取的订单上下文，条件及依赖仍需复核；不是经过执行验证的完整自然语言规则。'
    rules=r.get(name+'_rules',[])
    if not rules:
        return out if r.get(key) else out+'\n\n未识别到独立订单规则。反向入场、外部函数或平台设置也可能控制退出，请检查完整源码。'
    for rule in rules:
        out+=f'\n\n**原文件第 {rule["line"]} 行附近**：{rule.get("explanation", "需复核")}\n\n'+fence(rule['code'])
    return out


def render_card(r):
    reviewed=r['review_status']=='源码复核'
    out=[f'# {r["title"]}',
        f'[返回分类目录](../README.md) · [交互目录](../index.html) · [原始文件]({source_link(r)})',
        f'> {r["review_status"]}｜分类置信度：{r["classification_confidence"]}｜证据 E0（源码层面）｜表现未验证。合理性评分不是收益预测。',
        f'**合理性：{score_label(r)}**',
        f'**类别：** {r["category"]} → {r["family"]}  \n**类型：** {r["kind"]}  \n**源码语言：** {r["language"]}  \n**原配置市场：** {r["market"]}  \n**原配置周期：** {r["period"]}  \n**标签：** {"、".join(r["tags"]) or "待确认"}',
        '## 策略原理',r.get('principle','自动初审尚未完成逐分支语义复核。下方作者说明帮助理解原意，交易实现以带行号的源码和订单上下文为准。'),
        '## 入场规则',rule_markdown(r,'entry'),
        '## 出场规则',rule_markdown(r,'exit'),
        '## 仓位与风险控制',bullets(r.get('position_explanation',r.get('position_rules',[]))),
        '## 参数与默认值',bullets(r.get('parameter_explanation',r.get('parameters',[]))),
        '## 优点',bullets(r.get('strengths',[]),'暂无经源码确认的独立优势。'),
        '## 缺点与失效场景',bullets(r.get('weaknesses',[])),
        '## 合理性评分依据','|维度|得分|上限|依据|\n|---|---:|---:|---|']
    for s in r['scores']:
        out[-1]+='\n|'+ '|'.join(str(s[k]).replace('|','／').replace('\n',' ') for k in ['dimension','score','max','reason'])+'|'
    if not r['scores']: out.append('辅助资料或无法判断为策略的文件不参与策略评分。')
    out.extend(['','评分版本：rubric-v1。自动初评是保守的规则筛查，源码复核是静态研究判断；两者均未验证盈利能力。',
        '## 风险证据与待验证项'])
    for risk in r.get('risks',[]):
        location=f'第 {risk["line"]} 行' if risk['line'] else '全源码静态扫描'
        out.append(f'- **自动扫描线索 · {risk["severity"]} · {risk["title"]}**：{location}；{risk["evidence"]}')
    out.append(bullets(r.get('verification_notes',[]),'未进行编译、历史回测和模拟成交；美股时段、跳空、成本与做空条件待验证。'))
    if reviewed:
        out.extend(['## 源码复核依据',bullets([f'原文件第 {e["line"]} 行：{e["claim"]}' for e in r.get('review_evidence',[])])])
    out.extend(['## 表现与验证状态','表现分：未验证。收益、回撤、胜率、Sharpe 等均无独立验证数据，不以合理性分替代。',
        '## 作者原始说明（未经独立验证）',r['description'] or '没有提取到说明，请打开原文件。',
        '## 完整源码（原文件行号）',fence(numbered_code(r)),
        '## 溯源',f'- 文件 ID：`{r["id"]}`\n- 源文件 SHA256：`{r["source_sha256"]}`\n- 代码相同组：`{(r.get("duplicate_group") or "无")}`\n- 家族仅是逻辑分组，不代表代码相同。'])
    if urlparse(r.get('source_url','')).scheme in ('http','https'):
        out.append(f'- [原始发布页]({r["source_url"]})')
    return '\n\n'.join(out)+'\n'


def page(title,body,script=''):
    return '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+html.escape(title)+'</title><style>'+CSS+'</style></head><body>'+body+script+'</body></html>'


def ul(items, fallback='未识别；需结合完整源码复核，不能据此断定不存在。'):
    return '<ul>'+''.join('<li>'+html.escape(str(x))+'</li>' for x in (items or [fallback]))+'</ul>'


def render_card_html(r):
    e=html.escape
    body='<main class="card"><nav><a href="../index.html">← 分类目录</a> · <a href="'+source_link(r)+'">原始文件</a> · <a href="'+r['id']+'.md">Markdown 卡片</a></nav>'
    body+='<h1>'+e(r['title'])+'</h1><p class="notice">'+e(r['review_status'])+' · 分类置信度 '+e(r['classification_confidence'])+' · E0 源码证据 · 表现未验证。合理性评分不是收益预测。</p>'
    body+='<p class="score">合理性 '+e(score_label(r))+'</p><div class="meta">'+''.join('<span class="badge">'+e(str(x))+'</span>' for x in [r['category'],r['family'],r['language'],r['market'],r['period']]+r['tags'])+'</div>'
    body+='<h2>策略原理</h2><p class="prose">'+e(r.get('principle','自动初审尚未完成逐分支语义复核。作者原始说明和带行号源码见下方；提取结果可能不完整。'))+'</p>'
    for name,title in [('entry','入场规则'),('exit','出场规则')]:
        body+='<h2>'+title+'</h2>'
        if r.get(name+'_explanation'): body+=ul(r[name+'_explanation'])
        else: body+='<p class="muted">以下为静态抽取的订单上下文及依赖；不能代替完整语义复核。</p>'
        rules=r.get(name+'_rules',[])
        if not rules and not r.get(name+'_explanation'): body+='<p>未识别到独立订单规则；反向入场、外部函数或平台设置可能参与控制，请核对完整源码。</p>'
        for rule in rules:
            body+='<details'+(' open' if not r.get(name+'_explanation') else '')+'><summary>原文件第 '+str(rule['line'])+' 行附近 · '+e(rule.get('explanation','需复核'))+'</summary><pre>'+e(rule['code'])+'</pre></details>'
    for title,items in [('仓位与风险控制',r.get('position_explanation',r.get('position_rules',[]))),('参数与默认值',r.get('parameter_explanation',r.get('parameters',[]))),('优点',r.get('strengths',[])),('缺点与失效场景',r.get('weaknesses',[]))]:
        body+='<h2>'+title+'</h2>'+ul(items)
    body+='<h2>合理性评分依据</h2><div class="table-wrap"><table><thead><tr><th>维度</th><th>得分／上限</th><th>依据</th></tr></thead><tbody>'
    for s in r['scores']:
        body+='<tr><td>'+e(s['dimension'])+'</td><td>'+str(s['score'])+' / '+str(s['max'])+'</td><td>'+e(s['reason'])+'</td></tr>'
    body+='</tbody></table></div><p class="muted">rubric-v1；自动初评与源码复核分开比较。未回测不等于低表现，合理性高也不证明盈利。</p><h2>风险证据与待验证项</h2>'
    body+=ul([f'自动扫描线索 · {x["severity"]} · {x["title"]}（'+(f'第{x["line"]}行' if x['line'] else '全源码静态扫描')+f'）：{x["evidence"]}' for x in r.get('risks',[])]+r.get('verification_notes',[]),'未进行编译、回测或模拟成交；美股适配尚未验证。')
    if r.get('review_evidence'):
        body+='<h2>源码复核依据</h2>'+ul([f'原文件第{x["line"]}行：{x["claim"]}' for x in r['review_evidence']])
    body+='<h2>表现与验证状态</h2><p>表现分：未验证。收益、回撤、胜率及Sharpe均无独立验证数据。</p><details><summary>作者原始说明（未经独立验证）</summary><pre>'+e(r['description'])+'</pre></details><details><summary>完整源码（原文件行号）</summary><pre>'+e(numbered_code(r))+'</pre></details><h2>溯源</h2><p>ID：'+r['id']+'<br>SHA256：'+r['source_sha256']+'<br>代码相同组：'+e((r.get('duplicate_group') or '无'))+'</p></main>'
    return page(r['title'],body)


def compact_record(r):
    keys=['id','title','category','family','kind','score','review_status','classification_confidence','market','period','tags','filename','duplicate_group']
    return {k:r.get(k) for k in keys}


def render_index(records):
    data=json.dumps([compact_record(r) for r in records],ensure_ascii=False,separators=(',',':')).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
    body='''<main><h1>策略分类与研究目录</h1><p class="muted">美股优先 · 按实际交易机制分类 · 所有历史表现均待验证</p><p class="notice">自动初评分用于安排研究顺序；源码复核分有具体规则解释。两者分开筛选。高分不代表收益好，原配置多为加密货币，尚未证明适用于美股。</p><p><a href="README.md">使用说明</a> · <a href="methodology.md">评分方法</a> · <a href="catalog.csv" download>下载 CSV</a></p><div class="filters">
<label>搜索策略 / 标签<input id="query" type="search" placeholder="名称、关键词、家族"></label>
<label>类别<select id="category"><option value="">全部类别</option></select></label>
<label>复核状态<select id="review"><option value="源码复核">源码复核</option><option value="自动初审">自动初审</option><option value="">全部（按复核状态分组）</option></select></label>
<label>资料类型<select id="kind"><option value="strategy">交易策略</option><option value="">全部资料</option><option value="indicator">指标</option><option value="tool">工具 / 教程</option><option value="unknown">待判定</option></select></label>
<label>最低合理性分<input id="minimum" type="number" min="0" max="100" value="0"></label>
<label>排序<select id="sort"><option value="score">合理性分从高到低</option><option value="name">名称</option></select></label>
<label>代码重复<select id="dedup"><option value="yes">相同代码只显示一份</option><option value="no">显示全部文件</option></select></label></div>
<p id="summary" role="status" aria-live="polite"></p><div class="table-wrap"><table><thead><tr><th>策略 · 打开分析卡片</th><th>类别 / 家族</th><th>合理性</th><th>复核 / 置信度</th><th>原配置市场 / 周期</th></tr></thead><tbody id="rows"></tbody></table><div id="empty" class="empty" hidden>没有匹配结果。可清除关键词或放宽类别、复核状态和分数条件。</div></div><div class="pager"><button id="prev">上一页</button><span id="page"></span><button id="next">下一页</button></div><noscript>请启用 JavaScript 使用筛选，或下载 CSV 并查看 cards 下的独立卡片。</noscript></main>'''
    script='''<script id="catalog-data" type="application/json">'''+data+'''</script><script>
'use strict';
const data=JSON.parse(document.getElementById('catalog-data').textContent);
const $=id=>document.getElementById(id);let pageNumber=0;const pageSize=50;
const categories=[...new Set(data.map(r=>r.category))].sort((a,b)=>a.localeCompare(b,'zh-CN'));
for(const category of categories){const o=document.createElement('option');o.value=category;o.textContent=category;$('category').append(o)}
function selected(){const q=$('query').value.trim().toLowerCase(),min=Number($('minimum').value)||0;
let rows=data.filter(r=>(!q||[r.title,r.family,...r.tags].join(' ').toLowerCase().includes(q))&&(!$('category').value||r.category===$('category').value)&&(!$('review').value||r.review_status===$('review').value)&&(!$('kind').value||r.kind===$('kind').value)&&(min===0||r.score!==null&&r.score>=min));
rows.sort((a,b)=>{const reviewRank=(b.review_status==='源码复核')-(a.review_status==='源码复核');return reviewRank||($('sort').value==='score'?((b.score??-1)-(a.score??-1)):0)||a.title.localeCompare(b.title,'zh-CN')});
if($('dedup').value==='yes'){const seen=new Set();rows=rows.filter(r=>{const key=r.duplicate_group||r.id;if(seen.has(key))return false;seen.add(key);return true})}return rows}
function cell(row,text){const td=document.createElement('td');td.textContent=text;row.append(td);return td}
function draw(){const rows=selected(),pages=Math.max(1,Math.ceil(rows.length/pageSize));pageNumber=Math.min(pageNumber,pages-1);$('rows').replaceChildren();
for(const r of rows.slice(pageNumber*pageSize,(pageNumber+1)*pageSize)){const tr=document.createElement('tr'),td=cell(tr,'');const a=document.createElement('a');a.href='cards/'+r.id+'.html';a.textContent=r.title;td.append(a);const tags=document.createElement('div');tags.className='muted';tags.textContent=r.tags.join(' · ');td.append(tags);cell(tr,r.category+' / '+r.family);cell(tr,r.score===null?'不评分':r.score+' / 100');cell(tr,r.review_status+' / '+r.classification_confidence);cell(tr,r.market+' / '+r.period);$('rows').append(tr)}
$('summary').textContent='总计 '+data.length+' 份资料 · 匹配 '+rows.length+' 份（表现均未验证）';$('empty').hidden=rows.length!==0;$('page').textContent=(pageNumber+1)+' / '+pages;$('prev').disabled=pageNumber===0;$('next').disabled=pageNumber>=pages-1}
for(const id of ['query','category','review','kind','minimum','sort','dedup'])$(id).addEventListener('input',()=>{pageNumber=0;draw()});$('prev').addEventListener('click',()=>{pageNumber--;draw()});$('next').addEventListener('click',()=>{pageNumber++;draw()});draw();
</script>'''
    return page('策略分类与研究目录',body,script)


def validate_records(records):
    ids=set()
    for r in records:
        if r['id'] in ids: raise ValueError('ID重复: '+r['id'])
        ids.add(r['id'])
        if r.get('performance_score') is not None or r.get('performance_status')!='未验证':
            raise ValueError('没有行情不能生成表现结论')
        if r['score'] is not None:
            if r['kind']!='strategy': raise ValueError('非策略资料不可评分: '+r['filename'])
            if len(r['scores'])!=len(WEIGHTS) or not 0<=r['score']<=100: raise ValueError('评分维度数量或总分无效')
            if {x['dimension']:x['max'] for x in r['scores']}!=WEIGHTS: raise ValueError('评分维度无效: '+r['filename'])
            if any(not 0<=x['score']<=x['max'] for x in r['scores']): raise ValueError('分项越界')
            if sum(x['score'] for x in r['scores'])!=r['score']: raise ValueError('总分不等于分项')
        elif r['scores']: raise ValueError('无总分但存在分项')


def build(root,output,workers):
    from .analyzer import analyze
    paths=sorted(root.glob('*.md'))
    if workers==1: records=[analyze(p) for p in paths]
    else:
        with ProcessPoolExecutor(max_workers=workers) as pool: records=list(pool.map(analyze,paths,chunksize=25))
    reviews=[]
    for path in sorted((output/'reviews').glob('*.json')): reviews.extend(json.loads(path.read_text()))
    records=apply_reviews(records,reviews)
    duplicates=defaultdict(list)
    for r in records:
        if r['code'].strip(): duplicates[hashlib.sha256(r['code'].strip().encode()).hexdigest()].append(r)
    for digest,group in duplicates.items():
        for r in group:r['duplicate_group']=digest[:16] if len(group)>1 else ''
    validate_records(records)
    output.mkdir(parents=True,exist_ok=True);(output/'cards').mkdir(exist_ok=True)
    for r in records:
        (output/'cards'/f'{r["id"]}.md').write_text(render_card(r),encoding='utf-8')
        (output/'cards'/f'{r["id"]}.html').write_text(render_card_html(r),encoding='utf-8')
    (output/'catalog.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    columns=['id','title','category','family','kind','score','review_status','classification_confidence','market','period','tags','performance_status','evidence_level','duplicate_group','filename','source_sha256','card']
    with (output/'catalog.csv').open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=columns);writer.writeheader()
        for r in records:
            row={k:r.get(k,'') for k in columns};row['tags']=' | '.join(r['tags']);row['card']='cards/'+r['id']+'.html'
            # Avoid spreadsheet formula execution from untrusted source titles.
            row={k:("'"+v if isinstance(v,str) and v.startswith(('=','+','-','@','\t','\r')) else v) for k,v in row.items()}
            writer.writerow(row)
    (output/'index.html').write_text(render_index(records),encoding='utf-8')
    counts=Counter(r['category'] for r in records);review_count=sum(r['review_status']=='源码复核' for r in records)
    summary={'files':len(records),'reviewed':review_count,'automatic':len(records)-review_count,'categories':dict(counts),'kinds':dict(Counter(r['kind'] for r in records)),'exact_code_groups':sum(len(g)>1 for g in duplicates.values()),'performance_verified':0,'rubric':'rubric-v1'}
    (output/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    text='# 策略分类与分析目录\n\n[打开本地交互目录](index.html) · [CSV表格](catalog.csv) · [JSON完整数据](catalog.json) · [评分与分类方法](methodology.md)\n\n'
    text+=f'覆盖 **{len(records)}** 份原始资料；**{review_count}** 份已逐份源码复核，**{len(records)-review_count}** 份为自动初审。历史表现验证 **0** 份。\n\n'
    text+='## 如何使用\n\n打开 index.html，默认显示已源码复核的交易策略，按合理性排序。切换“自动初审”查看全量研究线索；点击名称阅读卡片。CSV可用表格软件筛选。卡片同时提供HTML和Markdown。\n\n合理性高不代表收益好。自动初评分依据代码特征，不能替代语义分析。未复核卡片包含作者说明、订单上下文和完整源码，其规则解释仍可能不完整。美股是目标市场，原市场配置并不等于美股适配通过。\n\n## 类别覆盖\n\n|类别|资料数|\n|---|---:|\n'
    text+='\n'.join(f'|{k}|{v}|' for k,v in sorted(counts.items()))
    text+='\n\n## 已源码复核卡片\n\n|策略|类别|合理性分|\n|---|---|---:|\n'
    for r in sorted([r for r in records if r['review_status']=='源码复核'],key=lambda r:-(r['score'] if r['score'] is not None else -1)):
        text+=f'|[{r["title"].replace("|","／")}]'+f'(cards/{r["id"]}.md)|{r["category"]}|{r["score"] if r["score"] is not None else "不评分"}|\n'
    text+='\n## 更新与验证\n\n在工作分支根目录运行：\n\n```sh\npython3 -m unittest discover -s tests -v\npython3 -m tools.strategy_catalog.build --workers 8\npython3 -m tools.strategy_catalog.verify\n```\n\n复核覆盖文件在 reviews/，绑定源文件SHA256；源码改变后拒绝使用旧复核。代码相同组只代表完整提取源码字节相同（忽略首尾空白），不把同一家族当成重复。\n'
    (output/'README.md').write_text(text,encoding='utf-8')
    return summary


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--workers',type=int,default=8)
    args=parser.parse_args()
    if not 1<=args.workers<=32: parser.error('--workers must be 1..32')
    root=Path(__file__).resolve().parents[2]
    print(json.dumps(build(root,root/'analysis',args.workers),ensure_ascii=False,indent=2))

if __name__=='__main__':main()
