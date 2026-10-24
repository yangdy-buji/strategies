# -*- coding: utf-8 -*-
"""Assemble static review evidence. Never execute or modify strategies."""
from pathlib import Path
from collections import Counter
import csv, hashlib, html, json

root=Path.cwd();out=root/'analysis/top300'
ranked=json.loads((out/'ranking.json').read_text())
ranking={r['sid']:r for r in ranked}
pine={r['sid']:r for r in json.loads((out/'pinescript/manifest.json').read_text())}
old={r['sid']:r for r in json.loads((root/'analysis/top500/optimization/manifest.json').read_text())}
original={r['sid']:r for r in json.loads((root/'analysis/top500/ranking.json').read_text())}
benchmark=json.loads((root/'analysis/top500/summary.json').read_text())['benchmark']
rows=[];inputs={}
for batch in (1,2,3):
    path=out/f'review_batch_{batch}.json'
    inputs[path.name]=hashlib.sha256(path.read_bytes()).hexdigest()
    data=json.loads(path.read_text())
    assert len(data)==100
    assert {r['rank'] for r in data}==set(range(100*(batch-1)+1,100*batch+1))
    rows.extend(data)
assert len({r['sid'] for r in rows})==300
for r in rows:
    sid=r['sid'];ref=ranking[sid];p=pine[sid]
    assert r['rank']==ref['rank'] and r['source_sha256']==ref['source_sha256']
    assert hashlib.sha256((root/p['source_file']).read_bytes()).hexdigest()==r['source_sha256']
    payload=(out/'pinescript'/p['file']).read_bytes()
    assert hashlib.sha256(payload).hexdigest()==p['pine_sha256']
    lines=payload.decode().splitlines()
    assert r['priority'] in ('P0','P1','P2') and r['assessment'] and r['findings']
    for f in r['findings']:
        assert f['kind'] in ('confirmed_defect','design_risk','validation_gap'),f
        assert f['severity'] in ('high','medium','low'),f
        for key in ('severity','detail','suggestion','tradeoff','validation'):assert f.get(key),(sid,key)
        assert f['evidence']
        for ev in f['evidence']:
            assert 1<=ev['line']<=len(lines),(sid,ev)
            assert ev['code']==lines[ev['line']-1],(sid,ev,lines[ev['line']-1])
    r.update(title=ref['title'],category=ref['category'],old_tier=ref['tier'],
             old_audit_status=old[sid]['status'],cagr=ref['cagr'],sharpe=ref['sharpe'],max_dd=ref['max_dd'],
             old_issues=old[sid]['issues'],old_remaining=old[sid]['remaining'],
             existing_variant='../top500/optimization/'+old[sid]['variant'] if old[sid]['variant'] else None,
             old_card='../top500/optimization/'+old[sid]['card'],
             details_card=ref['detail_card'],pine_file='pinescript/'+p['file'],pine_sha256=p['pine_sha256'])
rows.sort(key=lambda r:r['rank'])
summary={
    'reviewed':len(rows),'priority_counts':dict(Counter(r['priority'] for r in rows)),
    'old_status_counts':dict(Counter(r['old_audit_status'] for r in rows)),
    'confirmed_defect_strategies':sum(any(f['kind']=='confirmed_defect' for f in r['findings']) for r in rows),
    'p0_without_confirmed_defect':sum(r['priority']=='P0' and not any(f['kind']=='confirmed_defect' for f in r['findings']) for r in rows),
    'previously_reviewed_now_confirmed':[{'rank':r['rank'],'sid':r['sid'],'title':r['title']} for r in rows if r['old_audit_status']=='reviewed' and any(f['kind']=='confirmed_defect' for f in r['findings'])],
    'priority_by_old_tier':{tier:dict(Counter(r['priority'] for r in rows if r['old_tier']==tier)) for tier in ('A','B','C')},
    'categories':dict(Counter(r['category'] for r in rows)),
    'prior_no_stop_flags':sum('no_stop_loss' in original[r['sid']]['red_flags'] for r in rows),
    'drawdown_over_40':sum(r['max_dd']<-.4 for r in rows),
    'benchmark':benchmark,
    'below_benchmark_cagr':sum(r['cagr']<benchmark['cagr'] for r in rows),
    'all_three_better_than_benchmark':sum(r['cagr']>benchmark['cagr'] and r['sharpe']>benchmark['sharpe'] and r['max_dd']>benchmark['max_dd'] for r in rows),
    'native_compile':False,'new_backtest':False,'strategy_files_modified':False,'audit_input_sha256':inputs,
    'ranking_sha256':hashlib.sha256((out/'ranking.json').read_bytes()).hexdigest(),
}
# Fixed narrative below belongs to this frozen ranking snapshot; reject drift.
assert summary['old_status_counts']=={'reviewed':162,'needs_design':70,'candidate':68}
assert summary['prior_no_stop_flags']==140 and summary['drawdown_over_40']==68
assert summary['below_benchmark_cagr']==100 and summary['all_three_better_than_benchmark']==50
(out/'logic_review.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
(out/'logic_review_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
fields=['rank','sid','title','priority','old_tier','old_audit_status','assessment','cagr','sharpe','max_dd','findings','pine_file','details_card','old_card','existing_variant']
with (out/'logic_review.csv').open('w',encoding='utf-8-sig',newline='') as stream:
    writer=csv.DictWriter(stream,fieldnames=fields);writer.writeheader()
    for r in rows:
        flat={k:json.dumps(r[k],ensure_ascii=False) if isinstance(r[k],(list,dict)) else r[k] for k in fields}
        writer.writerow({k:"'"+v if isinstance(v,str) and v.startswith(('=','+','-','@')) else v for k,v in flat.items()})
e=html.escape
def txt(value):return e(str(value))
labels={'P0':'优先纠正／核验阻断性问题','P1':'重要设计或执行风险','P2':'核心可保留，先做稳健性验证'}
body='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>TOP300源码合理性复核与优化清单</title><style>body{font:16px/1.65 system-ui;max-width:1400px;margin:30px auto;padding:0 20px;background:#f6f8fb;color:#1b2637}a{color:#1559a5}table{border-collapse:collapse;width:100%;font-size:14px;background:white}td,th{padding:10px;border-bottom:1px solid #dce2ec;text-align:left}th{background:#e7edf6;position:sticky;top:0}section,details{background:white;border:1px solid #dbe2ed;border-radius:8px;margin:14px 0;padding:18px}summary{font-weight:650;cursor:pointer}pre{overflow:auto;background:#f0f3f7;padding:12px}li{margin:5px 0}.notice{background:#fff0ce;padding:18px}.scroll{overflow:auto}</style><h1>TOP300源码合理性复核与优化清单</h1>'''
body+='<p class="notice">本次完整静态复核300份原版脚本。未执行原生Pine编译或新回测，未修改交易代码。原TOP300排名与A/B/C层级是历史筛选结果；本次发现可推翻“此前未确认缺陷”的状态，不能继续仅凭旧名次认定可用。</p>'
body+='<p><a href="logic_review.csv" download>下载逐项审查CSV</a> · <a href="logic_review.json">完整证据JSON</a> · <a href="logic_review_summary.json">统计与输入指纹</a> · <a href="review_counterexamples.json">三个局部反例（非原生执行）</a> · <a href="index.html">原TOP300名单</a></p><ul>'
for key in ('P0','P1','P2'):body+='<li>'+key+' '+labels[key]+'：'+str(summary['priority_counts'].get(key,0))+'项</li>'
body+='</ul><p>P0/P1/P2是处理优先级，不是收益评分。每条发现分别标记确定实现缺陷、设计风险或验证缺口；优化建议不代表保证收益提高。</p>'
body+='<p>有确定实现问题的策略共'+str(summary['confirmed_defect_strategies'])+'项，包含此前已知问题及非默认选项问题，不是全部新发现；P0另包含'+str(summary['p0_without_confirmed_defect'])+'项需先澄清保护覆盖等高风险设计的策略，不能将P0数量当成新增致命错误数量。</p>'
body+='<section><h2>建议保留核心逻辑、优先做验证的基线</h2><p><a href="#s334">334 EMA±ATR通道</a>、<a href="#s5123">5123 前柱唐奇安突破</a>、<a href="#s4392">4392 布林突破</a>、<a href="#s2143">2143 EMA＋RSI</a>、<a href="#s1395">1395 分离唐奇安通道</a>：规则相对清晰，可优先保留核心信号，核验成本、仓位、参数邻域和独立后续窗口。这不是收益或实盘可用性确认。</p><p>旧榜第1和第2（2351、3900）也有状态记忆、尺度或过滤条件的设计问题，严格历史数值门槛不等于逻辑免审。</p></section>'
body+='<section><h2>应先做什么</h2><ol><li>先处理不可能触发的条件、错误返回值、退出ID、失效状态与数量量纲，建立有边界反例的回归；不要先搜索参数。</li><li>把入场过滤与持仓保护分开评估。仅在成交或明确的新仓位生命周期更新保护锚；是否改为挂单止损、状态退出或增加灾难止损，需要单独对照验证。</li><li>统一美股回测的数量、费用、滑点、交易时段、借券及拆股处理，再比较原版与候选版。解释器统一仓位不能证明源码200%权益或多层加仓的风险。</li><li>按时间留出未参与筛选的后续样本，检查参数邻域、逐股贡献和最差年份；现有历史末3年不是独立样本外。</li><li>按收益相关性及信号重合度缩减策略。类别集中不等于已证明相关性，但300个名字不代表300个独立优势。</li></ol><p>止损缺失不自动等于算法错误，统一加固定百分比止损也未必改善趋势策略。修改必须说明退出语义及成本变化。</p></section>'
body+='<section><h2>需要特别注意的现有修复候选</h2><p>SID1776原版冲击柱初始化后，同根回撤计算为100%，超过默认50%阈值；仅在入场条件加inFlag的已有局部修复不能解决状态机问题，可能阻断默认入场。应先区分冲击、冲击后回撤与突破阶段，并重新定义冲击后的回撤低点。不要把现有修复候选当成已验证版本。</p></section>'
body+='<section><h2>全体数据背景</h2><p>此前状态：162项未确认缺陷、70项待设计、68项已有未回测修复候选。原有静态标记中140项标记无止损；68项历史回撤超过40%。这些只是已存数据统计，不是新增回测。类别分布：'+txt(json.dumps(summary['categories'],ensure_ascii=False))+'。</p></section>'
body+='<section><h2>表现不能只看正收益</h2><p>提供的同口径基准年化约14.73%、夏普0.859、最大回撤34.60%。名单中100项年化低于这个基准，只有50项在年化、夏普和回撤三个指标上同时更好。不同仓位和风险暴露尚未归因，不能把这种直接比较当成已验证alpha，也不能仅凭年化低于基准否定低风险策略。</p></section>'
body+='<p>点击名称定位逐项结论；可用浏览器查找SID。表格先按处理优先级、再按原排名排列。</p><div class="scroll"><table><thead><tr><th>原排名 / SID</th><th>策略</th><th>处理优先级</th><th>合理性结论</th><th>原日线年化 / 夏普 / 回撤幅度</th></tr></thead><tbody>'
ordered=sorted(rows,key=lambda r:(r['priority'],r['rank']))
for r in ordered:
    body+='<tr><td>'+str(r['rank'])+' / '+str(r['sid'])+'</td><td><a href="#s'+str(r['sid'])+'">'+txt(r['title'])+'</a></td><td>'+r['priority']+'</td><td>'+txt(r['assessment'])+'</td><td>'+f"{r['cagr']:.2%} / {r['sharpe']:.3f} / {abs(r['max_dd']):.2%}"+'</td></tr>'
body+='</tbody></table></div><h2>逐项源码证据与优化取舍</h2>'
for r in ordered:
    body+='<details id="s'+str(r['sid'])+'"><summary>'+r['priority']+' · 原#'+str(r['rank'])+' / SID '+str(r['sid'])+' '+txt(r['title'])+'</summary><p>'+txt(r['assessment'])+'</p><p>旧审查状态：'+txt(r['old_audit_status'])+'；旧筛选层级：'+r['old_tier']+'。此处旧状态仅供对照，不表示本轮仍认可。</p><p><a href="'+r['pine_file']+'">原版Pine</a> · <a href="'+r['details_card']+'">原完整规则与绩效卡</a> · <a href="'+r['old_card']+'">此前审查及修复说明</a></p>'
    if r['existing_variant']:body+='<p><a href="'+r['existing_variant']+'">已有局部修复候选（未回测，未必覆盖本轮问题）</a></p>'
    for f in r['findings']:
        kind={'confirmed_defect':'确定实现问题','design_risk':'设计风险','validation_gap':'验证缺口'}[f['kind']]
        body+='<h3>'+kind+' · '+txt(f['severity'])+'</h3><p>'+txt(f['detail'])+'</p><h4>源码证据（导出.pine行号）</h4>'
        for ev in f['evidence']:body+='<pre>L'+str(ev['line'])+': '+txt(ev['code'])+'</pre>'
        body+='<p><strong>建议：</strong>'+txt(f['suggestion'])+'</p><p><strong>代价与取舍：</strong>'+txt(f['tradeoff'])+'</p><p><strong>验证方式：</strong>'+txt(f['validation'])+'</p>'
    body+='</details>'
body+='<section><h2>语义核对依据与边界</h2><p>Pine默认订单成交时点与信号计算时点不同；多次退出还涉及订单数量预留。实际费用和滑点会改变结果。参见<a href="https://www.tradingview.com/pine-script-docs/concepts/strategies/">TradingView策略文档</a>。</p><p>实时逐tick、跨周期请求或向过去绘图需要分别核验，不应把所有重绘都等同前视。参见<a href="https://www.tradingview.com/pine-script-docs/concepts/repainting/">重绘说明</a>。</p><p>本次仅阅读与静态推演，未进行原生编译、逐笔回放、原生/外部引擎对齐或新收益测试。新增优化方向必须先验证后决定是否实施。</p></section></html>'
(out/'logic_review.html').write_text(body,encoding='utf-8')
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
class Links(HTMLParser):
    def __init__(self):super().__init__();self.links=[];self.ids=set()
    def handle_starttag(self,t,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.add(a['id'])
        if t=='a' and 'href' in a:self.links.append(a['href'])
links=Links();links.feed(body)
for href in links.links:
    u=urlsplit(href)
    if u.scheme:continue
    if u.path:assert (out/unquote(u.path)).is_file(),href
    else:assert u.fragment in links.ids,href
print(json.dumps(summary,ensure_ascii=False,indent=2))
print('PASS: exact source evidence, 300 unique identities, hashes, links and artifacts')
