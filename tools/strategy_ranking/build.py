"""Build source-linked, external-backtest research rankings, not trade advice."""
from __future__ import annotations
import argparse
import csv
import hashlib
import html
import json
import math
from pathlib import Path
from urllib.parse import quote
from tools.strategy_catalog.build import CSS, page, ul, fence, numbered_code

METRICS=[('cagr','年化收益',True),('sharpe','Sharpe',False),('max_dd','最大回撤',True),('calmar','Calmar',False),('trades','报告交易数',False),('exposure','平均持仓暴露',True),('win_rate','胜率',True),('profit_factor','利润因子',False),('avg_hold_days','平均持有天数',False),('short_trade_frac','空头交易占比',True),('tickers_run','运行股票数',False)]
SECTIONS=[('策略原理','principle'),('信号链与指标解释','signal_explanations'),('入场规则：触发条件与执行顺序','entry_steps'),('出场规则：平仓、反手与保护单','exit_steps'),('仓位与资金管理','sizing_analysis'),('默认参数与敏感点','parameter_notes'),('信号到成交的时间顺序','execution_timeline'),('回测表现逐项解读','performance_findings'),('优点与支持证据','strengths'),('缺点与失效场景','weaknesses'),('下一轮验证清单','validation_plan')]

def fmt(v,percent=False):
    if v is None:return '未提供'
    try:n=float(v)
    except (TypeError,ValueError):return str(v)
    if not math.isfinite(n):return '未提供'
    return f'{n*100:.2f}%' if percent else f'{n:,.2f}'

def format_metrics(metrics):
    return '<div class="table-wrap"><table><thead><tr><th>报告指标</th><th>数值</th></tr></thead><tbody>'+''.join('<tr><td>'+label+'</td><td>'+fmt(metrics.get(key),pct)+'</td></tr>' for key,label,pct in METRICS)+'</tbody></table></div>'

def tier(r):return '同口径日线主榜' if r.get('cohort')=='full_daily' else '补充验证候选（不同证据层）'

def score_rows(r):
    return [('日线表现分',r.get('daily_score'),'70%'),('近三年历史分段分',r.get('recent_score'),'10%'),('已有逻辑合理性分',r.get('current_logic_score'),'20%'),('静态风险扣分',r.get('risk_penalty'),'直接扣除'),('综合研究分',r.get('combined_score'),'用于本证据层内排序')]

def ranked_card_html(r,base,details):
    e=html.escape;rank=r.get('primary_rank');cohort=tier(r)
    body='<main class="card"><nav><a href="../index.html">← 排名目录</a> · <a href="../../cards/'+r['id']+'.html">原逻辑卡片</a> · <a href="../../../'+quote(r['filename'])+'">原始策略</a> · <a href="'+r['id']+'.md">Markdown版</a></nav>'
    body+='<h1>'+e(r['title'])+'</h1><p class="notice">研究名单 #'+str(r['research_index'])+' · '+cohort+' · '+('主榜第 '+str(rank)+' 名' if rank else '不占用同口径主榜名次')+'<br>外部历史回测，尚未独立复现；规范化源码匹配不等于严格版本绑定。近三年为历史末段，非严格样本外。</p>'
    body+='<div class="meta">'+''.join('<span class="badge">'+e(str(v))+'</span>' for v in [r['category'],details.get('detail_level','自动精细分析'),r.get('current_logic_review','未知'),r.get('cohort','')])+'</div>'
    body+='<h2>先读结论</h2><p class="prose">'+e(details.get('overview',''))+'</p><p class="prose">'+e(details.get('verdict',''))+'</p>'
    body+='<h2>排名为何在这里</h2><div class="table-wrap"><table><thead><tr><th>项目</th><th>分数</th><th>权重／用途</th></tr></thead><tbody>'+''.join('<tr><td>'+a+'</td><td>'+fmt(b)+'</td><td>'+c+'</td></tr>' for a,b,c in score_rows(r))+'</tbody></table></div>'
    body+=ul(r.get('penalty_reasons',[]),'没有触发本版静态风险扣分；不代表没有风险。')
    body+='<p>同证据层权重敏感性：偏绩效方案名次 '+str(r.get('sensitivity_perf_rank','不适用'))+'；偏逻辑方案名次 '+str(r.get('sensitivity_logic_rank','不适用'))+'。这是评分规则敏感性，不是交易参数稳健性测试。</p>'
    body+='<h2>报告日线表现</h2><p>2016-01-04—2026-10-16；当期成分股回看历史；固定单位信号组合；单边成本0.1%。'+('50股票初筛，不能与全市场主榜直接比较。' if r.get('cohort')!='full_daily' else '全市场样本，实际运行股票数如下。')+'</p>'+format_metrics(r.get('reported_daily',{}))
    recent=r.get('reported_recent',{})
    body+='<h2>近三年历史末段</h2><p>同一回测后756个日频观测，非严格样本外；未按新数据重新执行。</p>'+format_metrics(recent)
    for title,key in SECTIONS:
        body+='<h2>'+title+'</h2>';value=details.get(key)
        body+=('<p class="prose">'+e(value)+'</p>') if isinstance(value,str) else ul(value or [],'资料不足，需结合源码复核。')
    body+='<h2>原策略与回测引擎差异</h2><div class="table-wrap"><table><thead><tr><th>项目及源码</th><th>回测行为</th><th>影响与验证</th></tr></thead><tbody>'
    for x in details.get('engine_compatibility',[]):
        body+='<tr><td>'+e(str(x.get('feature','')))+'<br>'+e(str(x.get('source_evidence','')))+'</td><td>'+e(str(x.get('backtest_behavior','')))+'</td><td>'+e(str(x.get('impact','')))+'<br>'+e(str(x.get('verification','')))+'</td></tr>'
    body+='</tbody></table></div><h2>日内／跨周期交叉证据</h2><p>日内回测允许隔夜；5/10/15分钟为近2年，30分钟/1小时为近5年，股票池为200只。各周期样本相关，不能合计交易数当作独立样本。四周期仅保存Top100，未出现不表示失败。</p>'
    body+=intraday_table(r.get('intraday',[]))
    body+='<h2>已有逻辑分与证据</h2><div class="table-wrap"><table><thead><tr><th>维度</th><th>分数</th><th>依据</th></tr></thead><tbody>'
    for x in base.get('scores',[]):body+='<tr><td>'+e(x['dimension'])+'</td><td>'+str(x['score'])+'/'+str(x['max'])+'</td><td>'+e(x['reason'])+'</td></tr>'
    body+='</tbody></table></div><p>排名沿用之前逻辑分，未因看到高收益反向抬分。本轮精读若发现问题，在规则、风险和差异矩阵说明。</p>'
    if r.get('prior_comment'):body+='<details><summary>外部历史短评（不是本轮精读）</summary><p>'+e(r['prior_comment'])+'</p></details>'
    body+='<h2>源代码依据</h2>'+ul([f'第{x["line"]}行：{x["claim"]}' for x in base.get('review_evidence',[])],'以下提供订单切片与完整源码，自动分析不证明所有分支均正确。')
    for name,label in [('entry_rules','入场'),('exit_rules','出场')]:
        for x in base.get(name,[]):body+='<details><summary>'+label+' · 原文件第'+str(x['line'])+'行</summary><p>'+e(x['explanation'])+'</p><pre>'+e(x['code'])+'</pre></details>'
    body+='<details><summary>完整源码（原文件行号）</summary><pre>'+e(numbered_code(base))+'</pre></details><h2>数据溯源与限制</h2><pre>'+e(json.dumps({'sid':r['sid'],'filename':r['filename'],'source_sha256':base['source_sha256'],'daily_source':r.get('daily_source'),'source_match':r.get('source_match'),'duplicates':r.get('duplicate_members'), 'eligibility_notes':r.get('eligibility_notes')},ensure_ascii=False,indent=2))+'</pre><p><a href="../methodology.md">完整方法</a> · <a href="../source_manifest.json">输入文件指纹</a></p></main>'
    return page(r['title'],body).replace('</style>','\n.card li{white-space:pre-wrap}</style>',1)

def intraday_table(rows):
    if not rows:return '<p>本地保存的表中未找到该策略的逐周期数据；不补中性成绩，不推断为零收益。</p>'
    headers=['周期','年化收益','Sharpe','最大回撤','交易数','来源范围']
    out='<div class="table-wrap"><table><thead><tr>'+''.join('<th>'+x+'</th>' for x in headers)+'</tr></thead><tbody>'
    for x in rows:
        out+='<tr>'+''.join('<td>'+html.escape(str(v))+'</td>' for v in [x.get('tf',''),fmt(x.get('cagr'),True),fmt(x.get('sharpe')),fmt(x.get('max_dd'),True),fmt(x.get('trades')),x.get('scope','')])+'</tr>'
    return out+'</tbody></table></div>'

def ranked_card_md(r,base,details):
    out=[f'# 研究名单 {r["research_index"]} · {r["title"]}',f'[排名目录](../index.html) · [原逻辑卡片](../../cards/{r["id"]}.md) · [原始文件](../../../{quote(r["filename"])})',
         f'> {tier(r)}；主榜名次：{r.get("primary_rank") or "不适用"}。外部报告未独立复现；近三年是历史末段，不是严格样本外。',
         '## 先读结论',details.get('overview',''),details.get('verdict',''),'## 排名构成',
         '|项目|分数|权重／用途|\n|---|---:|---|\n'+'\n'.join(f'|{a}|{fmt(b)}|{c}|' for a,b,c in score_rows(r)),
         '\n'.join('- '+x for x in r.get('penalty_reasons',[])),
         f'权重敏感性：偏绩效名次 {r.get("sensitivity_perf_rank","不适用")}，偏逻辑名次 {r.get("sensitivity_logic_rank","不适用")}；不代表交易参数测试。',
         '## 报告日线表现（未经独立复现）',
         '|指标|全历史|近三年历史末段|\n|---|---:|---:|\n'+'\n'.join(f'|{label}|{fmt(r.get("reported_daily",{}).get(k),pct)}|{fmt(r.get("reported_recent",{}).get(k),pct)}|' for k,label,pct in METRICS),
         '日线窗口2016-01-04至2026-10-16。现成分股回看历史，单边0.1%成本。近三年为末756个观测，不是严格样本外。']
    for title,key in SECTIONS:
        v=details.get(key,[]);out+=['## '+title,v if isinstance(v,str) else '\n'.join('- '+str(x) for x in v)]
    out.append('## 原策略与回测引擎差异')
    for x in details.get('engine_compatibility',[]):
        out+=['### '+str(x.get('feature',''))]+[f'- {label}：{x.get(k,"")}' for k,label in [('source_evidence','源码依据'),('backtest_behavior','引擎行为'),('impact','影响'),('verification','验证')]]
    out+=['## 日内／跨周期证据','不同窗口和股票池，允许隔夜。未出现不代表失败；各周期交易不可合并为独立样本。',
          '|周期|年化收益|Sharpe|回撤|来源范围|\n|---|---:|---:|---:|---|\n'+'\n'.join(f'|{x.get("tf")}|{fmt(x.get("cagr"),True)}|{fmt(x.get("sharpe"))}|{fmt(x.get("max_dd"),True)}|{x.get("scope","")}|' for x in r.get('intraday',[])),
          '## 外部历史短评',r.get('prior_comment') or '未提供；不等于本轮源码精读。',
          '## 源码证据','\n'.join(f'- 第{x["line"]}行：{x["claim"]}' for x in base.get('review_evidence',[]))]
    for name,label in [('entry_rules','入场'),('exit_rules','出场')]:
        for x in base.get(name,[]):out+=[f'### {label}：原文件第{x["line"]}行',x['explanation'],fence(x['code'])]
    out+=['## 完整源码',fence(numbered_code(base)),'## 溯源',fence(json.dumps({'sid':r['sid'],'source_sha256':base['source_sha256'],'daily_source':r.get('daily_source'),'source_match':r.get('source_match'),'eligibility_notes':r.get('eligibility_notes')},ensure_ascii=False,indent=2),'json')]
    return '\n\n'.join(out)+'\n'

def ranking_index(records,summary):
    cols=['id','title','category','research_index','primary_rank','cohort','combined_score','daily_score','recent_score','current_logic_score','current_logic_review','risk_penalty','red_flags','detail_level','critical_findings']
    small=[]
    for r in records:
        x={k:r.get(k) for k in cols};x.update({k:r.get('reported_daily',{}).get(k) for k in ('cagr','sharpe','max_dd','trades','exposure')});small.append(x)
    data=json.dumps(small,ensure_ascii=False,allow_nan=False,separators=(',',':')).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
    n=len(records);main_count=summary.get('primary_count',0);supp=summary.get('supplement_count',0)
    body=f'''<main><nav><a href="../index.html">← 原逻辑目录</a></nav><h1>策略表现与逻辑融合研究名单 · {n}份</h1><p class="muted">{main_count}份同口径日线主榜 · {supp}份补充候选 · 每份附详细规则、表现解读及引擎差异</p><p class="notice">依据用户提供的历史回测重新排名，未独立复现。近三年是历史末段，非严格样本外。补充候选有独立证据层，不与主榜分数横向比较；名单不是500个已验证可实盘策略。</p><p><a href="REPORT.md">结果说明</a> · <a href="methodology.md">评分与限制</a> · <a href="ranking.csv" download>下载CSV</a> · <a href="excluded.csv" download>排除记录</a></p><div class="filters">
<label>搜索<input id="query" type="search" placeholder="策略名或类别"></label><label>类别<select id="category"><option value="">全部类别</option></select></label>
<label>证据层<select id="cohort"><option value="">全部（分层显示）</option><option value="full_daily">同口径主榜</option><option value="screening50">50股初筛补充</option></select></label>
<label>收益筛选<select id="positive"><option value="">全部</option><option value="yes">年化收益大于0</option></select></label>
<label>源码复核<select id="detail"><option value="">全部</option><option value="reviewed">本轮源码精读</option></select></label>
<label>排序<select id="sort"><option value="rank">名单顺序</option><option value="combined_score">综合分</option><option value="cagr">年化收益</option><option value="sharpe">Sharpe</option><option value="max_dd">回撤更小</option></select></label></div>
<p id="summary" role="status" aria-live="polite"></p><div class="table-wrap"><table><thead><tr><th>策略 · 打开详细卡片</th><th>名单 / 主榜</th><th>类别 / 证据层</th><th>综合 / 逻辑</th><th>年化 / Sharpe</th><th>回撤 / 风险扣分</th></tr></thead><tbody id="rows"></tbody></table><div id="empty" class="empty" hidden>没有匹配结果，请放宽筛选。</div></div><div class="pager"><button id="prev">上一页</button><span id="page"></span><button id="next">下一页</button></div></main>'''
    script='<script id="ranking-data" type="application/json">'+data+'''</script><script>
'use strict';const data=JSON.parse(document.getElementById('ranking-data').textContent);const $=id=>document.getElementById(id);let pn=0;const size=50;
for(const cat of [...new Set(data.map(r=>r.category))].sort()){const o=document.createElement('option');o.value=cat;o.textContent=cat;$('category').append(o)}
function number(v,pct=false){return v===null||v===undefined?'未提供':(v*(pct?100:1)).toFixed(2)+(pct?'%':'')}
function selected(){const q=$('query').value.trim().toLowerCase();const rows=data.filter(r=>(!q||(r.title+' '+r.category).toLowerCase().includes(q))&&(!$('category').value||r.category===$('category').value)&&(!$('cohort').value||r.cohort===$('cohort').value)&&(!$('positive').value||r.cagr>0)&&(!$('detail').value||(r.detail_level||'').includes('源码精读')));const sort=$('sort').value;rows.sort((a,b)=>(b.cohort==='full_daily')-(a.cohort==='full_daily')||(sort==='rank'?a.research_index-b.research_index:((b[sort]??-Infinity)-(a[sort]??-Infinity)))||a.research_index-b.research_index);return rows}
function cell(tr,text){const td=document.createElement('td');td.textContent=text;tr.append(td);return td}
function draw(){const rows=selected(),pages=Math.max(1,Math.ceil(rows.length/size));pn=Math.min(pn,pages-1);$('rows').replaceChildren();for(const r of rows.slice(pn*size,(pn+1)*size)){const tr=document.createElement('tr'),td=cell(tr,'');const a=document.createElement('a');a.href='cards/'+r.id+'.html';a.textContent=r.title;td.append(a);const sub=document.createElement('div');sub.className='muted';sub.textContent=r.detail_level;td.append(sub);cell(tr,r.research_index+' / '+(r.primary_rank??'补充'));cell(tr,r.category+' / '+(r.cohort==='full_daily'?'全市场日线':'补充验证'));cell(tr,number(r.combined_score)+' / '+number(r.current_logic_score));cell(tr,number(r.cagr,true)+' / '+number(r.sharpe));cell(tr,number(r.max_dd,true)+' / '+number(r.risk_penalty)+((r.critical_findings||[]).length?' · 源码重要疑点'+r.critical_findings.length+'项':''));$('rows').append(tr)}$('summary').textContent='匹配 '+rows.length+' / '+data.length+' 份；同证据层内排序，补充候选始终单列。';$('empty').hidden=!!rows.length;$('page').textContent=(pn+1)+' / '+pages;$('prev').disabled=pn===0;$('next').disabled=pn>=pages-1}
for(const id of ['query','category','cohort','positive','detail','sort'])$(id).addEventListener('input',()=>{pn=0;draw()});$('prev').addEventListener('click',()=>{pn--;draw()});$('next').addEventListener('click',()=>{pn++;draw()});draw();
</script>'''
    return page('策略表现与逻辑融合研究名单',body,script)

def apply_priority(base,reviews):
    by_name={r['filename']:r for r in reviews};review=by_name.get(base['filename'])
    if not review:return dict(base)
    if review['source_sha256']!=base['source_sha256']:raise ValueError('本轮精读源码哈希过期')
    merged=dict(base);merged.update(review);return merged

def sensitivity(records):
    for field,w in [('sensitivity_perf_rank',(.8,.1,.1)),('sensitivity_logic_rank',(.55,.1,.35))]:
        ordered=sorted(records,key=lambda r:(-(w[0]*(r.get('daily_score') or 0)+w[1]*(r.get('recent_score') or 0)+w[2]*(r.get('current_logic_score') or 0)-(r.get('risk_penalty') or 0)),r['sid']))
        for i,r in enumerate(ordered,1):r[field]=i

def write_csv(path,rows,columns):
    with path.open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=columns);writer.writeheader()
        for r in rows:
            vals={k:r.get(k,'') for k in columns}
            for k,v in vals.items():
                if isinstance(v,(dict,list)):vals[k]=json.dumps(v,ensure_ascii=False)
                if isinstance(vals[k],str) and vals[k].startswith(('=','+','-','@','\t','\r')):vals[k]="'"+vals[k]
            writer.writerow(vals)

def write_report(out,records,summary):
    primary=[r for r in records if r['cohort']=='full_daily']
    supplemental=[r for r in records if r['cohort']!='full_daily']
    reviewed=sum('源码精读' in r['detail_level'] for r in records)
    critical=sum(bool(r.get('critical_findings')) for r in records)
    positive=sum(r['reported_daily']['cagr']>0 for r in primary)
    sections=['# 策略表现与逻辑融合研究名单',
        '[交互排名目录](index.html) · [CSV总表](ranking.csv) · [评分方法](methodology.md) · [排除记录](excluded.csv) · [输入指纹](source_manifest.json)',
        f'共 **{len(records)}** 份详细卡片：**{len(primary)}** 份同口径日线主榜，**{len(supplemental)}** 份小股票池初筛补充候选。不是500个同等证据或已验证可实盘的策略。补充不占主榜名次；其分数只在初筛候选池内比较。',
        f'主榜中报告年化收益为正 {positive} 份、非正 {len(primary)-positive} 份。当前集合是相对研究排序，不保证每份都有正收益或经济优势。',
        f'所有入选策略已有规则、参数、表现与执行差异解读；其中 **{reviewed}** 份完成本轮完整源码精读，**{critical}** 份列出精读发现的重要疑点。其余是自动语义辅助，不冒充逐份源码审计。原先已有的复核继续保留。',
        '## 主榜前20（必须同时阅读重要疑点）',
        '|名次|策略|综合研究分|逻辑分|日线年化|Sharpe|最大回撤|本轮重要疑点|\n|---:|---|---:|---:|---:|---:|---:|---|']
    rows=[]
    for r in primary[:20]:
        d=r['reported_daily'];flag='；'.join(r.get('critical_findings',[])) or '未列出；不等于已证明无风险'
        rows.append(f'|{r["primary_rank"]}|[{r["title"].replace("|","／")}](cards/{r["id"]}.html)|{fmt(r["combined_score"])}|{fmt(r["current_logic_score"])}|{fmt(d["cagr"],True)}|{fmt(d["sharpe"])}|{fmt(d["max_dd"],True)}|{flag.replace("|","／").replace(chr(10)," ")}|')
    sections[-1]+='\n'+'\n'.join(rows)
    sections+=['## 为什么不沿用原综合榜',
        '合并了原初筛后全市场结果与552日线重跑，扩大同口径覆盖；同时查原始运行错误数、固定代表去重并隔离已保存异常标记。旧榜把缺失日内结果补50的做法未沿用。',
        '主分为70%日线表现、10%历史末3年分段、20%已有逻辑分，再减明确静态风险扣分。旧合理性分含绩效，不重复混入。日内结果因四周期完整榜缺失只作交叉证据。',
        '## 数据漏斗',fence(json.dumps(summary.get('funnel',{}),ensure_ascii=False,indent=2),'json'),
        '## 全市场排除原因（原因可能重叠，不能相加当策略数）',fence(json.dumps(summary.get('full_daily_exclusion_counts',{}),ensure_ascii=False,indent=2),'json'),
        '## 阅读顺序',
        '先看证据层和本轮重要疑点，再看年化/回撤及逻辑分；点开卡片核对完整入场出场、数量、风险控制和解释器差异。高分仅说明报告指标与既定权重下的研究位置，不证明原策略可交易。',
        '## 不能由现有数据推出的结论',
        '没有原平台逐笔对照，未独立复现；原仓库快照缺失，规范化哈希不是严格版本绑定。当前成分股回看历史有幸存者偏差。近三年仅历史末段，非严格样本外。没有每日收益序列，未生成年度收益、恢复期、相关矩阵或新净值图。',
        '## 本地更新',
        fence('python3 -m unittest discover -s tests -v\npython3 -m tools.strategy_ranking.build --source "<回测目录>"\npython3 -m tools.strategy_ranking.verify --source "<回测目录>"\nnode tests/test_ranking_ui.cjs','sh'),
        '原始策略和回测文件只读。生成器与精读记录纳入工作分支；生成目录、CSV、JSON和卡片保留本地，可由同版本输入重建。未部署、未推送。']
    (out/'REPORT.md').write_text('\n\n'.join(sections)+'\n',encoding='utf-8')


def build(root,source,include_supplement=True):
    from .rank import build_dataset
    from .details import build_details
    out=root/'analysis/top500';out.mkdir(parents=True,exist_ok=True);(out/'cards').mkdir(exist_ok=True)
    dataset=build_dataset(source,root/'analysis/catalog.json')
    primary=dataset['primary'][:500];supp=dataset['supplement_pool'][:max(0,500-len(primary))] if include_supplement else []
    selected=primary+supp
    catalog={r['filename']:r for r in json.loads((root/'analysis/catalog.json').read_text())}
    reviews=[]
    for p in sorted((out/'reviews').glob('*.json')):reviews.extend(json.loads(p.read_text()))
    if len({r['filename'] for r in reviews})!=len(reviews):raise ValueError('重复本轮精读记录')
    sensitivity(dataset['primary']);sensitivity(dataset['supplement_pool'])
    summary=dict(dataset['summary']);summary.update(primary_count=len(primary),supplement_count=len(supp),selected_count=len(selected))
    benchmark=summary.get('benchmark',{})
    for i,r in enumerate(selected,1):
        r['research_index']=i;base=apply_priority(catalog[r['filename']],reviews)
        r['category']=base.get('category',r['category']);r['critical_findings']=base.get('critical_findings',[])
        details=build_details(base,r,benchmark);r['detail_level']=details.get('detail_level','自动精细分析')
        if base.get('review_status')=='本轮源码精读':r['detail_level']='源码精读+外部回测解读';details['detail_level']=r['detail_level']
        r['details']=details;r['source_sha256']=base['source_sha256']
        (out/'cards'/(r['id']+'.html')).write_text(ranked_card_html(r,base,details),encoding='utf-8')
        (out/'cards'/(r['id']+'.md')).write_text(ranked_card_md(r,base,details),encoding='utf-8')
    # Only remove obsolete generated cards identified by stable generated ID.
    valid={r['id'] for r in selected}
    for p in (out/'cards').iterdir():
        if p.suffix in ('.md','.html') and len(p.stem)==12 and all(c in '0123456789abcdef' for c in p.stem) and p.stem not in valid:p.unlink()
    summary['priority_reviewed_in_selection']=sum('源码精读' in r['detail_level'] for r in selected)
    (out/'ranking.json').write_text(json.dumps(selected,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    (out/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    (out/'source_manifest.json').write_text(json.dumps(dataset['source_manifest'],ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    flat=[]
    for r in selected:
        x={k:v for k,v in r.items() if k not in ('details','features','intraday','reported_daily','reported_recent')};x.update(r.get('reported_daily',{}));x['card']='cards/'+r['id']+'.html';flat.append(x)
    columns=['research_index','primary_rank','cohort','sid','id','title','category','combined_score','daily_score','recent_score','current_logic_score','current_logic_review','risk_penalty','penalty_reasons','critical_findings','cagr','sharpe','max_dd','calmar','trades','exposure','tickers_run','detail_level','sensitivity_perf_rank','sensitivity_logic_rank','daily_source','source_sha256','filename','card']
    write_csv(out/'ranking.csv',flat,columns)
    ex=dataset['excluded'];cols=sorted({k for r in ex for k in r}) if ex else ['sid','reason'];write_csv(out/'excluded.csv',ex,cols)
    (out/'index.html').write_text(ranking_index(selected,summary),encoding='utf-8')
    write_report(out,selected,summary)
    return summary

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--source',type=Path,required=True);parser.add_argument('--strict-only',action='store_true');args=parser.parse_args()
    root=Path(__file__).resolve().parents[2];print(json.dumps(build(root,args.source,not args.strict_only),ensure_ascii=False,indent=2))
if __name__=='__main__':main()
