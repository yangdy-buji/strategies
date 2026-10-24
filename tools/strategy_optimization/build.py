"""Build annotated repair candidates; never run strategies or inherit old returns."""
from __future__ import annotations
import argparse
from collections import Counter
import difflib
import hashlib
import html
import json
from pathlib import Path
import re
from urllib.parse import quote
from tools.strategy_catalog.analyzer import _source
from tools.strategy_catalog.build import page, ul
from tools.strategy_ranking.build import write_csv

LABELS={'candidate':'修复候选·未回测','needs_design':'已审·待设计/验证','needs_review':'待源码审查','reviewed':'已审·未确认缺陷'}
DESIGN_SIDS={3762,1180,1371,5507,1169,4573,1779,4962,1588,2240}
REMAINING={735:['RSI退出仍需EXIT与bull_cross同时成立；主Buy不受RSI过滤，无独立硬止损。'],5369:['VWMA动量仍未接入信号；没有硬止损，正确上轨过滤可能减少交易。'],621:['仍用信号K的open限价，不能回填已发生的触价；未增加硬止损或挂单超时。'],2458:['保留默认200%权益与无硬止损；逐tick/收盘执行仍需原生验证。'],4621:['na(time_close)不构成普通交易日的收盘强平；无独立硬止损。'],3330:['expected_rebound仍为不要求触及下轨的独立路径；保护仍为条件市价退出。']}
DATE='2026-10-24'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def normalized(code):
    return code.rstrip('\n')+'\n'


def audit_status(audit,has_fix):
    if has_fix:return 'candidate'
    if not audit:return 'needs_review'
    return 'reviewed' if audit['verdict']=='no_confirmed_defect' else 'needs_design'


def apply_review_metadata(record,approval):
    record['patch_review']=approval
    for field in ('remaining','validation_cases'):
        record[field]=list(dict.fromkeys(record.get(field,[])+approval.get(field,[])))
    if approval['status']=='deferred':record['issues']+=['独立复核暂缓修改：'+approval['review']]


def annotated_code(code, record):
    versions=re.findall(r'^\s*//@version=\d+\s*$',code,re.M)
    if len(versions)>1:raise ValueError('多个Pine版本指令')
    version=versions[0].strip()+'\n' if versions else ''
    rest=re.sub(r'^\s*//@version=\d+\s*\n?', '',code,count=1,flags=re.M) if versions else code
    header=[f'优化候选 conservative-v1 · {DATE}',f'原文件：{record["filename"]}',f'原文件SHA256：{record["source_sha256"]}',f'SID：{record["sid"]}；原研究名单序号：{record["research_index"]}',
            '状态：未原生编译，未回测。原排名和旧绩效不适用于本版本。',
            '范围：只修复下方OPT备注列出的缺陷；剩余问题见changes.md。',
            '原backtest区块为原始资料配置，不代表本版本完成过回测。']
    return version+'\n'.join('// '+x.replace('\n',' ') for x in header)+'\n\n'+normalized(rest)


def render_card(r):
    e=html.escape
    body='<main class="card"><nav><a href="../index.html">← 优化登记</a> · <a href="../../cards/'+r['id']+'.html">原分析卡片与旧回测</a> · <a href="../../../../'+quote(r['filename'])+'">原始策略文件</a></nav><h1>'+e(r['title'])+'</h1>'
    body+='<p class="notice">原研究名单 #'+str(r['research_index'])+' · '+LABELS[r['status']]+'。原榜序号不代表优化版名次。</p>'
    if r['status']=='candidate':
        body+='<p><a href="../'+r['variant']+'" download>下载带中文备注的Pine修复候选</a> · <a href="../'+r['original_variant']+'" download>原始提取代码</a> · <a href="../'+r['diff']+'">查看逐行差异</a> · <a href="../'+r['changes']+'">修改说明</a></p>'
        body+='<p>未原生编译、未回测。局部行为用例不等于完整Pine运行验证，尚不能判断收益是否改善。</p>'
    else:body+='<p>尚未修改；已审未确认缺陷不代表已证明没有缺陷，也不表示绩效已验证。待设计项需要明确交易意图或原生执行验证。</p>'
    audit=r.get('audit')
    if audit:
        body+='<h2>本轮完整源码静态审查</h2><p>'+e(audit['synopsis'])+'</p><p>未执行原生Pine编译或回测。</p><h3>源码证据</h3>'
        for item in audit['evidence']:body+='<p>原文件第'+str(item['line'])+'行：'+e(item['reason'])+'</p><pre>'+e(item['code'])+'</pre>'
        if audit['findings']:body+='<h3>本轮发现与处置</h3><p>下列保留审查时的处置建议；实际应用范围以本轮修改和补丁复核结论为准。</p>'+ul([f'{x["severity"]} · 原第{x["evidence_line"]}行：{x["detail"]}；处置：{x["resolution"]}' for x in audit['findings']])
    if r.get('patch_review'):body+='<h2>补丁独立复核</h2><p>'+('已批准局部修复' if r['patch_review']['status']=='approved' else '暂缓修改')+'：'+e(r['patch_review']['review'])+'</p>'
    body+='<h2>本轮处理／待核验问题</h2>'+ul(r['issues'])+'<h2>仍需关注</h2>'+ul(r['remaining'],'仍需原生编译、逐笔成交及独立回测验证。')
    if r.get('original_findings'):body+='<h2>原版审查上下文</h2><p>以下仅供原版对照，不表示这些问题在修复版中全部仍然存在；已处理部分以本轮修改和差异文件为准。</p>'+ul(r['original_findings'])
    body+='<h2>验证场景</h2>'+ul(r.get('validation_cases',[]),'先确认源码规则和订单生命周期，再制定行为用例。')
    body+='<h2>来源与验证状态</h2><pre>'+e(json.dumps({k:r.get(k) for k in ['sid','filename','source_sha256','original_code_sha256','variant_sha256','verification']},ensure_ascii=False,indent=2))+'</pre><p><a href="../README.md">范围与复现命令</a> · <a href="../manifest.csv">500项登记CSV</a> · <a href="../validation.md">本地验证记录</a></p></main>'
    return page('策略优化 · '+r['title'],body)


def render_index(records):
    small=[{k:r.get(k) for k in ['id','sid','title','category','research_index','status','severity','card']} for r in records]
    data=json.dumps(small,ensure_ascii=False).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
    counts=Counter(r['status'] for r in records)
    body='<main><nav><a href="../index.html">← 原排名与详细卡片</a></nav><h1>策略优化登记</h1><p class="notice">共'+str(len(records))+'项：'+str(counts['candidate'])+'个修复候选，'+str(counts['reviewed'])+'个已审未确认缺陷，'+str(counts['needs_design'])+'个待设计/验证，'+str(counts['needs_review'])+'个待审。所有候选未原生编译、未回测，不能继承旧排名或收益。</p><p><a href="manifest.csv" download>下载500项登记CSV</a> · <a href="README.md">修改范围与复现方式</a></p><div class="filters"><label>搜索<input id="query" type="search" placeholder="名称、类别或SID"></label><label>优化状态<select id="status"><option value="candidate">修复候选·未回测</option><option value="">全部500项</option><option value="reviewed">已审·未确认缺陷</option><option value="needs_design">已审·待设计/验证</option><option value="needs_review">待源码审查</option></select></label></div><p id="summary" role="status" aria-live="polite"></p><div class="table-wrap"><table><thead><tr><th>策略／打开优化卡</th><th>原名单序号</th><th>类别</th><th>状态</th></tr></thead><tbody id="rows"></tbody></table></div><p id="empty" hidden>没有匹配结果，请放宽筛选。</p></main>'
    script='<script id="optimization-data" type="application/json">'+data+'''</script><script>
'use strict';const data=JSON.parse(document.getElementById('optimization-data').textContent),$=id=>document.getElementById(id),labels={candidate:'修复候选·未回测',needs_design:'已审·待设计/验证',needs_review:'待源码审查',reviewed:'已审·未确认缺陷'};
function draw(){const q=$('query').value.toLowerCase().trim(),rows=data.filter(r=>(!$('status').value||r.status===$('status').value)&&(!q||(r.title+' '+r.category+' '+r.sid).toLowerCase().includes(q)));$('rows').replaceChildren();for(const r of rows){const tr=document.createElement('tr');for(const value of [r.title,r.research_index,r.category,labels[r.status]]){const td=document.createElement('td');if(tr.children.length===0){const a=document.createElement('a');a.href=r.card;a.textContent=value;td.append(a)}else td.textContent=value;tr.append(td)}$('rows').append(tr)}$('summary').textContent='显示 '+rows.length+' / '+data.length+' 项；按原名单顺序展示，不是优化后排名。';$('empty').hidden=rows.length>0}
for(const id of ['query','status'])$(id).addEventListener('input',draw);draw();
</script>'''
    return page('500策略优化登记',body,script)


def changes_md(r):
    sections=[f'# {r["title"]} · 保守修复候选',f'原研究名单 #{r["research_index"]} / SID {r["sid"]}。未原生编译、未回测；原排名收益不适用于本版本。',
              '[优化卡](../../cards/'+r['id']+'.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)',
              '## 已修改','\n'.join('- '+x for x in r['issues']),'## 未解决／保持原行为','\n'.join('- '+x for x in r['remaining']),
              '## 验证场景','\n'.join('- '+x for x in r['validation_cases']),
              '## 原版审查上下文','以下仅供对照，不表示这些问题在修复版中全部仍然存在。\n\n'+'\n'.join('- '+x for x in r.get('original_findings',[])),
              '## 验证边界','源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。',
              '## 指纹',f'原文件：`{r["filename"]}`\n\n原文件SHA256：`{r["source_sha256"]}`\n\n原代码SHA256：`{r["original_code_sha256"]}`\n\n候选SHA256：`{r["variant_sha256"]}`']
    return '\n\n'.join(sections)+'\n'


def audit_report(records,summary):
    rows=[r for r in records if r.get('audit')]
    lines=['# 剩余489项静态源码审查结果','[优化登记](index.html) · [500项CSV](manifest.csv)',
           f'本轮完成{len(rows)}项完整源码静态审查，新增{summary["new_candidates"]}个修复候选。全部500项状态：'+json.dumps(summary['counts'],ensure_ascii=False)+'。',
           '未确认缺陷不代表没有风险；待设计项保持原代码。修复候选也可能仍有未处理问题，请阅读每张卡的剩余问题。没有原生Pine编译和回测，不声称收益提高。',
           '## 新增修复候选','|原序号 / SID|策略|修改概要|','|---|---|---|']
    for r in rows:
        if r['status']=='candidate':
            title=r['title'].replace('|','\\|');issues='；'.join(r['issues']).replace('|','\\|').replace('\n',' ')
            lines.append(f'|{r["research_index"]} / {r["sid"]}|[{title}]({r["card"]})|{issues}|')
    lines+=['## 审查证据','逐项摘要、原始行号及发现保存在audit/batch_1.json至batch_3.json；补丁独立复核保存在audit/review_1.json至review_3.json，最终批准记录在audit/patch_approvals.json。所有文件与原代码指纹一起校验。',
            '## 验证边界','[本地验证记录](validation.md)。本次只做静态/局部行为核验，不部署、不执行策略、不接券商。推送门禁另按用户已有约定执行。']
    return '\n\n'.join(lines)+'\n'


def link_ranking_cards(root, ranking, catalog, records):
    # Display-only augmentation: ranking.json and all numerical scores remain unchanged.
    from tools.strategy_ranking.build import apply_priority,ranked_card_html,ranked_card_md,ranking_index
    out=root/'analysis/top500';reviews=[]
    for p in sorted((out/'reviews').glob('*.json')):reviews.extend(json.loads(p.read_text()))
    states={r['id']:r for r in records}
    for old in ranking:
        r=dict(old);r['_optimization']=states[r['id']]
        base=apply_priority(catalog[r['filename']],reviews)
        (out/'cards'/(r['id']+'.html')).write_text(ranked_card_html(r,base,r['details']),encoding='utf-8')
        (out/'cards'/(r['id']+'.md')).write_text(ranked_card_md(r,base,r['details']),encoding='utf-8')
    (out/'index.html').write_text(ranking_index(ranking,json.loads((out/'summary.json').read_text()),optimization=True),encoding='utf-8')


def build(root):
    from .fixes import FIXES,apply_fix
    from .audit import load_audit
    root=Path(root);top=root/'analysis/top500';out=top/'optimization'
    ranking_path=top/'ranking.json';catalog_path=root/'analysis/catalog.json'
    ranking=json.loads(ranking_path.read_text());catalog={r['filename']:r for r in json.loads(catalog_path.read_text())}
    audits,registry,approvals=load_audit(root,ranking,catalog)
    if len(ranking)!=500 or len({r['id'] for r in ranking})!=500:raise ValueError('要求500份唯一排名记录')
    if not set(registry)<=set(r['sid'] for r in ranking):raise ValueError('修复策略不在500名单内')
    prepared=[]
    # Validate every input before writing any outputs.
    for old in ranking:
        raw=(root/old['filename']).read_bytes();digest=sha(raw);code,_,_= _source(raw.decode('utf-8'))
        if digest!=old['source_sha256'] or digest!=catalog[old['filename']]['source_sha256']:raise ValueError('原策略指纹变化：'+old['filename'])
        if code!=catalog[old['filename']]['code']:raise ValueError('原代码与目录不符')
        sid=old['sid'];fix=registry.get(sid);audit=audits.get(sid)
        status=audit_status(audit,bool(fix)) if audits else ('candidate' if fix else ('needs_design' if sid in DESIGN_SIDS or old.get('critical_findings') else 'needs_review'))
        issues=list(fix['changes']) if fix else list(old.get('critical_findings') or [])
        if audit and not fix:issues=[x['detail']+'；'+x['resolution'] for x in audit['findings']] or ['本轮静态审查未确认可修复缺陷；不等于代码已证明正确。']
        if not issues:issues=['待逐行审查；自动提取的风险线索不能直接当作确认缺陷。']+[x['feature']+'：'+x['impact'] for x in old['details'].get('engine_compatibility',[])]
        remaining=list(dict.fromkeys((list(fix['remaining'])+REMAINING.get(sid,[])) if fix else list(old.get('critical_findings') or [])))
        r={k:old[k] for k in ['id','sid','research_index','filename','title','category','source_sha256']}
        if audit:r['audit']=audit
        if audit:r.update(audit_synopsis=audit['synopsis'],audit_verdict=audit['verdict'],audit_findings=audit['findings'])
        r.update(original_code_sha256=sha(code.encode()),status=status,severity='明确缺陷' if fix else ('需设计确认' if status=='needs_design' else '未定'),issues=issues,remaining=remaining,original_findings=list(old.get('critical_findings') or []),
                 verification=dict(native_compile=False,backtest=False,local_checks='源码指纹与补丁前置条件已核对；局部行为用例结果见validation.md'),
                 card='cards/'+r['id']+'.html',variant=None,variant_sha256=None,diff=None,changes=None,original_variant=None,validation_cases=list(fix['validation_cases']) if fix else old['details'].get('validation_plan',[]))
        if str(sid) in approvals:apply_review_metadata(r,approvals[str(sid)])
        variant=None
        if fix:
            variant=annotated_code(apply_fix(sid,code,digest,registry=registry),r);prefix='variants/'+r['id']+'/'
            r.update(variant=prefix+'conservative.pine',variant_sha256=sha(variant.encode()),diff=prefix+'changes.patch',changes=prefix+'changes.md',original_variant=prefix+'original.pine')
        prepared.append((r,code,variant))
    records=[x[0] for x in prepared];(out/'cards').mkdir(parents=True,exist_ok=True)
    for r,code,variant in prepared:
        (out/r['card']).write_text(render_card(r),encoding='utf-8')
        if variant is not None:
            (out/r['variant']).parent.mkdir(parents=True,exist_ok=True)
            (out/r['variant']).write_text(variant,encoding='utf-8');(out/r['original_variant']).write_text(normalized(code),encoding='utf-8')
            diff=''.join(difflib.unified_diff(normalized(code).splitlines(keepends=True),variant.splitlines(keepends=True),fromfile='original.pine',tofile='conservative.pine'))
            (out/r['diff']).write_text(diff,encoding='utf-8');(out/r['changes']).write_text(changes_md(r),encoding='utf-8')
    (out/'manifest.json').write_text(json.dumps(records,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    write_csv(out/'manifest.csv',records,['research_index','sid','id','title','category','status','severity','issues','remaining','audit_synopsis','audit_verdict','audit_findings','patch_review','verification','filename','source_sha256','original_code_sha256','variant_sha256','card','variant','changes','diff'])
    (out/'index.html').write_text(render_index(records),encoding='utf-8')
    summary=dict(selected=len(records),counts=dict(Counter(r['status'] for r in records)),audited_remaining=len(audits),new_candidates=len(registry)-len(FIXES),ranking_sha256=sha(ranking_path.read_bytes()),catalog_sha256=sha(catalog_path.read_bytes()),native_compile=False,backtest=False)
    if audits:summary['audit_inputs']={p.name:sha(p.read_bytes()) for p in sorted((out/'audit').glob('*.json'))}
    (out/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if audits:(out/'AUDIT_REPORT.md').write_text(audit_report(records,summary),encoding='utf-8')
    link_ranking_cards(root,ranking,catalog,records)
    return summary


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.parse_args()
    print(json.dumps(build(Path(__file__).resolve().parents[2]),ensure_ascii=False,indent=2))

if __name__=='__main__':main()
