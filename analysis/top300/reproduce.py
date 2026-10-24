# -*- coding: utf-8 -*-
"""Reproduce a user-data analysis snapshot; does not execute any strategy."""
import csv
import hashlib
import html
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'analysis/top300'
OUT.mkdir(exist_ok=True)
inputs = ['analysis/top500/ranking.json', 'analysis/top500/optimization/manifest.json',
          'analysis/top500/optimization/summary.json']
hashes = {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in inputs}
ranking = json.loads((ROOT / inputs[0]).read_text())
audits = {r['sid']: r for r in json.loads((ROOT / inputs[1]).read_text())}
hard_flags = {'LEAK_lookahead', 'fill_artifact_suspect', 'not_a_strategy', 'not_backtested',
              'grid_or_avg_down_no_stop', 'martingale', 'repaint_warning', 'htf_security_repaints_live'}
status_labels = {'reviewed': '已审未确认缺陷', 'needs_design': '待设计/验证', 'candidate': '已有修复候选但未重测'}
tiers = {'A': 'A 严格指标优选', 'B': 'B 次优研究候选', 'C': 'C 条件候选，不能认定双优'}
records, excluded = [], []
for r in ranking:
    d, recent, a = r['reported_daily'], r['reported_recent'], audits[r['sid']]
    assert r['id'] == a['id'] and r['source_sha256'] == a['source_sha256']
    reasons = []
    if r['cohort'] != 'full_daily': reasons.append('仅50票初筛，不与全量日线混排')
    if not (d.get('cagr') is not None and d['cagr'] > 0 and d.get('sharpe') is not None and d['sharpe'] > 0): reasons.append('全期年化或夏普非正/缺失')
    if not (recent.get('cagr') is not None and recent['cagr'] > 0): reasons.append('历史末3年年化非正/缺失')
    if hard_flags.intersection(r['red_flags']): reasons.append('保守排除高风险标记：' + '、'.join(sorted(hard_flags.intersection(r['red_flags']))))
    if r['features'].get('leak_hard'): reasons.append('静态硬前视疑点')
    if reasons:
        excluded.append({'sid': r['sid'], 'title': r['title'], 'reasons': reasons})
        continue
    clean = a['status'] == 'reviewed'
    basic = clean and r['current_logic_score'] >= 44 and d['cagr'] >= .1
    tier = 'A' if basic and d['sharpe'] >= 1 and d['max_dd'] >= -.3 else ('B' if basic and d['sharpe'] >= .8 and d['max_dd'] >= -.4 else 'C')
    complex_engine = [x['feature'] for x in r['details']['engine_compatibility'] if x['feature'] not in ('基础信号与成交', 'qty与仓位规模')]
    penalties = {'原有静态风险扣分': r['risk_penalty'],
                 '本轮审查扣分': {'reviewed': 0, 'needs_design': 10, 'candidate': 20}[a['status']],
                 '复杂订单保真未验证': 6 if complex_engine else 0,
                 '全期回撤超过50%': 10 if d['max_dd'] < -.5 else 0}
    score = .55 * r['daily_score'] + .30 * r['current_logic_score'] + .15 * (r['recent_score'] or 0) - sum(penalties.values())
    gaps = []
    if not clean: gaps.append('源码审查存在待处理问题；修复版不能继承旧绩效')
    if r['current_logic_score'] < 44: gaps.append('逻辑可审查性初评分低于44')
    if d['cagr'] < .1: gaps.append('全期年化低于10%')
    if d['sharpe'] < 1: gaps.append('全期夏普低于1')
    if d['max_dd'] < -.3: gaps.append('全期回撤超过30%')
    risks = [f"原版最大回撤{abs(d['max_dd'])*100:.2f}%"]
    if not r['features'].get('stop_loss_explicit'): risks.append('静态特征未确认独立硬止损，信号退出不等于损失上限')
    if complex_engine: risks.append('复杂订单引擎差异：' + '、'.join(complex_engine))
    if any(x['feature'] == 'qty与仓位规模' for x in r['details']['engine_compatibility']): risks.append('外部引擎统一仓位，不忠实复现源码数量配置')
    if r['red_flags']: risks.append('原静态标记（不均为已确认缺陷）：' + '、'.join(r['red_flags']))
    if any(x.get('cagr') is not None and x['cagr'] < 0 for x in r['intraday']): risks.append('已有其他周期负年化记录；股票池/时段不同，不能直接外推日线稳定性')
    if a['status'] != 'reviewed': risks.extend(a['issues']); risks.extend(a['remaining'])
    risks.extend(r.get('critical_findings', []))
    if r['sid'] == 2351: risks.append('BullPower使用绝对价格阈值，跨股票尺度及方向状态持久化需额外核验')
    synopsis = a.get('audit', {}).get('synopsis') or r['details']['principle']
    record = dict(sid=r['sid'], id=r['id'], title=r['title'], category=r['category'], tier=tier,
                  tier_label=tiers[tier], score=score, logic_score=r['current_logic_score'],
                  daily_score=r['daily_score'], recent_score=r['recent_score'], penalties=penalties,
                  cagr=d['cagr'], sharpe=d['sharpe'], max_dd=d['max_dd'], calmar=d['calmar'],
                  recent_cagr=recent['cagr'], recent_sharpe=recent.get('sharpe'),
                  profit_factor=d['profit_factor'], trades=d['trades'], tickers=d['tickers_run'],
                  audit_status=a['status'], audit_label=status_labels[a['status']],
                  original_rank=r['research_index'], synopsis=synopsis,
                  strengths=[f"全量日线年化{d['cagr']*100:.2f}%，夏普{d['sharpe']:.3f}",
                             f"历史末3年年化{recent['cagr']*100:.2f}%，并非独立样本外",
                             '完整源码审查未确认可修复缺陷' if clean else '问题与修复范围已有逐项审查记录'],
                  risks=list(dict.fromkeys(risks)), strict_gaps=gaps,
                  detail_card='../top500/cards/'+r['id']+'.html',
                  audit_card='../top500/optimization/cards/'+r['id']+'.html',
                  source_sha256=r['source_sha256'], daily_source=r['daily_source'])
    records.append(record)
records.sort(key=lambda x: (x['tier'], -x['score'], x['sid']))
for i, r in enumerate(records, 1): r['rank'] = i
selected = records[:300]
assert len(selected) == 300 and len({r['sid'] for r in selected}) == 300
for r in records[300:]: excluded.append({'sid': r['sid'], 'title': r['title'], 'reasons': ['通过基础筛选，但按本次排序位于300名之后']})
assert len(excluded) + len(selected) == 500
assert len({r['sid'] for r in selected + excluded}) == 500

method = '''本名单从已有500项中筛选，优先美股全量日线证据；并非全仓库重新回测。
“实际表现”在此仅指用户提供的外部历史回测，不是实盘。外部解释器并非原生Pine，源码仅有规范化匹配而非严格版本绑定，所有候选均未独立复现。
基础门槛：full_daily；全期CAGR与Sharpe均为正；历史末3年CAGR为正；排除50票初筛及明确列出的高风险静态标记。高风险标记采取保守排除，未声称全部已证实。
排除标记完整列表：LEAK_lookahead、fill_artifact_suspect、not_a_strategy、not_backtested、grid_or_avg_down_no_stop、martingale、repaint_warning、htf_security_repaints_live；另排除features.leak_hard非空项。其他BUG标记依原risk_penalty与本轮审查扣分，不一概排除。
A：本轮已审未确认缺陷、逻辑初评分>=44、全期CAGR>=10%、Sharpe>=1、最大回撤不超过30%。
B：同样无确认缺陷、逻辑>=44、CAGR>=10%，放宽Sharpe>=0.8、最大回撤不超过40%，且不属于A。
C：通过基础门槛但未达到A/B；可能有待修缺陷、较低逻辑分或较弱表现，不能称为双优。
先A、再B、再C；层内排序分=0.55*原日线表现分+0.30*原逻辑分+0.15*原历史末段分-扣分。分数仅决定研究顺序，不是成功概率。
原日线/末段分沿用原451项日线池的百分位：30%夏普+25%卡玛+25%年化+20%回撤；未在入围子集重新拟合。
扣分=原risk_penalty + 本轮candidate扣20/needs_design扣10/reviewed扣0 + 存在除基础信号与数量以外的引擎差异扣6 + 全期回撤超过50%扣10。
审查扣分针对原版已知问题，不给未回测修复版加分。原risk_penalty与本轮审查可能涉及相同问题，刻意保守惩罚，不解释为独立风险概率。
上述阈值及权重为本次透明研究偏好，不是经样本外校准的标准；44分也不表示高质量经济逻辑。静态未确认缺陷不等于无缺陷。
历史末3年与全期重叠，非独立样本外；日内不同股票池/窗口只展示反例，不直接计分。未做相关性去重，原排名仅按已有代表组去重，300个策略不等于300种独立优势。
排名不提供下单、仓位或上线建议。原版缺陷、引擎差异及缺少独立验证使本名单只能用于下一轮原生复测。
'''
(OUT/'methodology.txt').write_text(method, encoding='utf-8')
(OUT/'ranking.json').write_text(json.dumps(selected, ensure_ascii=False, indent=2)+'\n')
(OUT/'excluded.json').write_text(json.dumps(excluded, ensure_ascii=False, indent=2)+'\n')
fields = ['rank','sid','title','category','tier_label','score','logic_score','cagr','sharpe','max_dd','calmar','recent_cagr','recent_sharpe','audit_label','synopsis','strict_gaps','strengths','risks','original_rank','detail_card','audit_card']
with (OUT/'top300.csv').open('w', encoding='utf-8-sig', newline='') as f:
    w = csv.DictWriter(f, fieldnames=fields); w.writeheader()
    for r in selected:
        row = {k: json.dumps(r[k], ensure_ascii=False) if isinstance(r[k],list) else r[k] for k in fields}
        # Formula-like text is escaped, numeric metrics remain numeric.
        row = {k: "'"+v if isinstance(v,str) and v.startswith(('=','+','-','@')) else v for k,v in row.items()}
        w.writerow(row)
with (OUT/'top300.csv').open(encoding='utf-8-sig', newline='') as f:
    reader = csv.DictReader(f); columns = reader.fieldnames; csv_rows = list(reader)
with (OUT/'priority73.csv').open('w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=columns); writer.writeheader()
    writer.writerows(row for row in csv_rows if row['tier_label'].startswith(('A ', 'B ')))
counts = dict(Counter(r['tier'] for r in selected))
summary = dict(selected=300, eligible=len(records), excluded=len(excluded), tiers=counts,
               status_counts=dict(Counter(r['audit_status'] for r in selected)), input_sha256=hashes,
               top10_sids=[r['sid'] for r in selected[:10]], source='user supplied historical reports',
               native_compile=False, independent_backtest=False, live_performance=False)
(OUT/'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2)+'\n')
e = html.escape
def bullets(xs): return '<ul>'+''.join('<li>'+e(str(x))+'</li>' for x in xs)+'</ul>'
page = '''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>逻辑与历史表现 TOP300</title><style>body{font:16px/1.6 system-ui;margin:30px auto;padding:0 20px;max-width:1400px;color:#182230;background:#f7f9fc}a{color:#1459a8}table{border-collapse:collapse;width:100%;font-size:14px;background:white}td,th{padding:10px;border-bottom:1px solid #dde3ed;text-align:left}th{position:sticky;top:0;background:#e9eff8}section,details{background:white;padding:16px;border:1px solid #dbe2ec;border-radius:8px;margin:14px 0}.notice{padding:16px;background:#fff3d6}summary{cursor:pointer;font-weight:650}.scroll{overflow-x:auto}.num{white-space:nowrap}li{margin:5px 0}</style><h1>逻辑与历史表现 TOP300 研究名单</h1>'''
page += '<p class="notice">严格指标优选 '+str(counts.get('A',0))+' 项；次优研究候选 '+str(counts.get('B',0))+' 项；条件候选 '+str(counts.get('C',0))+' 项。300项不等于300个已验证双优策略。历史指标来自原版外部回测，非实盘；修复版未重测。</p>'
page += '<p><a href="priority73.csv" download>Priority 73 CSV</a> · <a href="top300.csv" download>下载完整CSV（收益/回撤为小数比例）</a> · <a href="ranking.json">完整数据</a> · <a href="excluded.json">200项未入选原因</a> · <a href="summary.json">数据指纹</a> · <a href="../top500/index.html">原500项</a></p>'
page += '<details><summary>筛选标准与评分方法</summary>'+''.join('<p>'+e(line)+'</p>' for line in method.splitlines())+'</details><p>点击策略名称查看本次摘要，展开查看优缺点；完整入场/出场规则及源码见原分析卡，新增审查结论以审查卡为准。可用浏览器查找名称或SID。</p><div class="scroll"><table><thead><tr>'+''.join('<th>'+x+'</th>' for x in ['名次','SID / 策略','层级','研究分','逻辑初分','日线年化','夏普','回撤幅度','末3年年化','审查状态'])+'</tr></thead><tbody>'
for r in selected:
    page += '<tr><td>'+str(r['rank'])+'</td><td><a href="#s'+str(r['sid'])+'">'+str(r['sid'])+' '+e(r['title'])+'</a></td><td>'+r['tier']+'</td><td>'+f"{r['score']:.2f}"+'</td><td>'+str(r['logic_score'])+'</td><td class="num">'+f"{r['cagr']:.2%}"+'</td><td>'+f"{r['sharpe']:.3f}"+'</td><td class="num">'+f"{abs(r['max_dd']):.2%}"+'</td><td class="num">'+f"{r['recent_cagr']:.2%}"+'</td><td>'+e(r['audit_label'])+'</td></tr>'
page += '</tbody></table></div><h2>逐项摘要与优缺点</h2>'
for r in selected:
    page += '<details id="s'+str(r['sid'])+'"><summary>#'+str(r['rank'])+' / SID '+str(r['sid'])+' '+e(r['title'])+' · '+e(r['tier_label'])+'</summary><p>'+e(r['synopsis'])+'</p><p><a href="'+r['detail_card']+'">完整原理、入场、出场与旧回测卡片</a> · <a href="'+r['audit_card']+'">源码审查、缺陷与修复备注</a></p><h3>支持证据</h3>'+bullets(r['strengths'])+'<h3>缺点与未验证风险</h3>'+bullets(r['risks'])+'<h3>与严格门槛的差距</h3>'+bullets(r['strict_gaps'] or ['通过本次严格数值门槛，但不代表交易优势或实盘可用性已验证'])+'<p>扣分明细：'+e(json.dumps(r['penalties'],ensure_ascii=False))+'</p></details>'
page += '</html>'
(OUT/'index.html').write_text(page,encoding='utf-8')
for r in selected:
    assert (OUT/r['detail_card']).is_file() and (OUT/r['audit_card']).is_file()
assert hashes == {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in inputs}
print(json.dumps(summary, ensure_ascii=False,indent=2))
print('TOP10')
for r in selected[:10]: print(r['rank'],r['sid'],r['title'],r['tier'],round(r['score'],2),round(r['cagr']*100,2),round(r['sharpe'],3),round(abs(r['max_dd'])*100,2))
