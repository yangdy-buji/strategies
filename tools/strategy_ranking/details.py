"""Evidence-bound, deterministic explanations of existing strategy/backtest records.

No backtest is executed here. Lexical explanations deliberately do not assert
control-flow, fill, or interpreter fidelity that the input cannot establish.
"""
import math
import re

from .context import enrich_rule


def _number(value):
    try:
        result = float(value)
        return result if math.isfinite(result) else None
    except (ValueError, TypeError, OverflowError):
        return None


def _items(value):
    if not value:
        return []
    return value if isinstance(value, list) else [value]


def _meaning(expression):
    text = str(expression)
    names = {
        'ta.crossover': '向上穿越（上一根未高于、本根高于）',
        'crossover': '向上穿越（上一根未高于、本根高于）',
        'ta.crossunder': '向下穿越（上一根未低于、本根低于）',
        'crossunder': '向下穿越（上一根未低于、本根低于）',
        'ta.ema': '指数移动平均', 'ema': '指数移动平均',
        'ta.sma': '简单移动平均', 'sma': '简单移动平均',
        'ta.rsi': '相对强弱指标RSI', 'rsi': '相对强弱指标RSI',
        'ta.atr': '平均真实波幅ATR', 'atr': '平均真实波幅ATR',
        'ta.highest': '窗口最高值', 'highest': '窗口最高值',
        'ta.lowest': '窗口最低值', 'lowest': '窗口最低值',
        'ta.macd': '快慢均线差及其信号线MACD',
        'strategy.position_avg_price': '当前持仓平均开仓价',
        'strategy.position_size': '持仓数量（正为多、负为空、零为空仓）',
        'strategy.opentrades': '当前未平仓交易数',
        'strategy.openprofit': '当前浮动盈亏（账户货币）',
        'close': '收盘价', 'open': '开盘价', 'high': '最高价', 'low': '最低价',
        'volume': '成交量', 'and': '并且', 'or': '或者', 'not': '不满足',
        'true': '真', 'false': '假', 'if': '当', 'when': '执行条件',
    }
    pattern = r'(?<![\w.])(' + '|'.join(re.escape(k) for k in sorted(names, key=len, reverse=True)) + r')(?![\w.])'
    text = re.sub(pattern, lambda m: names[m.group()], text)
    text = re.sub(r'\[(\d+)\]', lambda m: '（前' + m.group(1) + '根的值）', text)
    text = re.sub(r'>=|<=|==|!=|>|<', lambda m: {'>=':' 大于等于 ', '<=':' 小于等于 ', '==':' 等于 ', '!=':' 不等于 ', '>':' 大于 ', '<':' 小于 '}[m.group()], text)
    return text


def _rules(base, kind):
    reviewed = _items(base.get(kind + '_explanation'))
    if reviewed:
        return list(reviewed)
    result = []
    for index, rule in enumerate(_items(base.get(kind + '_rules')), 1):
        if not isinstance(rule, dict):
            result.append('规则%d：%s；语义辅助：%s' % (index, rule, _meaning(rule)))
            continue
        code = enrich_rule(base, rule)
        # Preserve the recovered control structure in both evidence and gloss;
        # definitions guarded by an ancestor if must never become plain steps.
        prose = []
        default_notes = []
        for raw in code.splitlines():
            source = re.sub(r'^\s*L\d+: ?', '', raw)
            line = source.strip()
            indent = source[:len(source) - len(source.lstrip())]
            if not re.match(r'^\s*L\d+:', raw) and not re.search(r'strategy\.|^if\b|=', line):
                continue
            if not line or line.startswith('//'):
                continue
            if re.search(r'input(?:\.bool)?\s*\(\s*(?:defval\s*=\s*)?false\b', line):
                variable = line.split('=', 1)[0].strip()
                default_notes.append('%s默认关闭；只有对应if门控启用时，受控条件才会参与规则，不能把该过滤器当作无条件开启。' % variable)
            if 'strategy.entry' in line or 'strategy.order' in line:
                direction = '申请做空' if 'strategy.short' in line else ('申请做多' if 'strategy.long' in line else '申请下单（方向需追踪变量）')
                prose.append(indent + direction + '：' + line)
            elif re.search(r'strategy\.(exit|close|close_all)\s*\(', line):
                prose.append(indent + '申请退出持仓：' + line)
            else:
                prose.append(indent + _meaning(line))
        result.append('规则%d（原文第%s行）：语义辅助逐行对照，保留缩进和条件层级；以下不是可独立顺序执行的步骤。\n%s\n%s\n带控制条件的源码证据切片（非完整执行证明）：\n%s\n边界：以上为语义辅助，变量赋值顺序、嵌套控制流及实际成交未证明。' % (index, rule.get('line', '未知'), '\n'.join(default_notes), '\n'.join(prose), code))
    return result or ['未提取到%s规则；不能据此断言源码没有该规则，需阅读完整源码与自定义函数。' % ('入场' if kind == 'entry' else '退出')]


def _metrics(data):
    return {str(k).removeprefix('oos3_'): v for k, v in (data or {}).items()}


def build_details(base, ranked, benchmark):
    """Return extended Chinese card text without inventing absent observations."""
    code = str(base.get('code') or '')
    features = ranked.get('features') or {}
    daily = _metrics(ranked.get('reported_daily'))
    recent = _metrics(ranked.get('reported_recent'))
    findings, strengths, weaknesses = [], [], []
    signals = []
    # Concrete indicator and condition assignments complement order slices.
    for raw in code.splitlines():
        line = raw.strip()
        if not line.startswith('//') and re.search(r'\b(?:ta\.)?(?:ema|sma|rsi|atr|highest|lowest|crossover|crossunder|macd)\s*\(|\[\d+\]', line) and not line.startswith(('plot', 'strategy.')):
            signals.append('计算/条件：%s；含义：%s。' % (line, _meaning(line)))
    if not signals:
        signals = ['信号线索：%s；未提取到可直接解释的常见指标，完整条件见入场与退出证据。' % base.get('family', '未分类')]
    parameters = list(_items(base.get('parameter_explanation')))
    for item in _items(base.get('parameters')):
        text = str(item)
        parameters.append('参数原值：%s；含义：%s。周期值按K线根数理解，不自动等于天数；是否参与订单条件须沿变量依赖核对。' % (text, _meaning(text)))
    if not parameters:
        parameters = ['未提取到输入参数；应从上述指标调用中的常数及完整源码核对默认窗口、阈值和开关，不能解释为无参数。']
    sizing = list(_items(base.get('position_explanation')))
    sizing += ['仓位声明/调用：%s。数量、现金额或权益比例以该调用的参数类型为准，不能相互替代。' % x for x in _items(base.get('position_rules'))]
    if not sizing:
        sizing = ['未提取到独立仓位声明；需核对strategy声明、entry/order的qty和权益变化，不推算每笔风险金额。']
    matrix = []

    def add(feature, pattern, flag, behavior, impact, verification):
        evidence = [line.strip() for line in code.splitlines() if re.search(pattern, line) and not line.strip().startswith('//')]
        if evidence or features.get(flag):
            matrix.append(dict(feature=feature, source_evidence='\n'.join(evidence) or '特征扫描标记 %s=%s；具体调用需回查完整源码' % (flag, features.get(flag)), backtest_behavior=behavior, impact=impact, verification='保真未验证：' + verification))

    add('qty与仓位规模', r'\bqty\s*=|default_qty_', 'explicit_qty', '现有解释器忽略原策略qty，采用引擎统一仓位规则。', '收益及回撤对应统一仓位，不代表源码固定数量、现金或权益比例。', '逐笔对齐数量、开仓权益和成交金额。')
    pyramid_values = re.findall(r'\bpyramiding\s*=\s*([^,)\n]+)', '\n'.join(line for line in code.splitlines() if not line.strip().startswith('//')))
    pyramid_positive = any(_number(v.strip()) is not None and _number(v.strip()) > 0 for v in pyramid_values)
    pyramid_unknown = any(_number(v.strip()) is None for v in pyramid_values)
    feature_pyramid = _number(features.get('pyramiding'))
    if pyramid_positive or pyramid_unknown or (feature_pyramid is not None and feature_pyramid > 0):
        impact = ('源码可能配置加仓，但表达式取值未确认，不能确认存在多层持仓；若启用，统一单仓会改变均价与风险路径。' if pyramid_unknown and not pyramid_positive else '正值配置允许同向多次入场，不证明实际发生加仓；若发生，多层持仓和均价变化可能被压成单仓，风险与利润路径不同。')
        add('加仓/网格/摊薄', r'\bpyramiding\s*=', 'pyramiding', '现有解释器不复现完整加仓管理。', impact, '求值pyramiding配置并对齐实际增仓、均价与最大投入。')
    for flag in ['martingale', 'grid_dca', 'averaging_down']:
        if features.get(flag):
            add(flag, r'(?!)', flag, '原策略动态加仓/摊薄机制未被完整执行。', '扫描提示该机制，尚非控制流证明；统一仓位结果不足以检验尾部风险。', '检查亏损时规模是否递增及累计敞口上限。')
    add('部分退出', r'qty_percent\s*=|strategy\.(?:exit|close)\([^\n]*qty\s*=', 'partial_exits', '现有解释器不按原策略数量复现部分退出。', '剩余仓位和后续止盈止损可能不同。', '逐笔核对平仓数量、剩余数量和订单关联ID。')
    add('strategy.risk风控', r'strategy\.risk\.', 'risk_rules', 'strategy.risk.* 在现有解释器中为no-op，忽略风控调用。', '触发最大回撤或日亏损限制后，回测可能继续交易；不能把该结果当受保护的真实策略。', '用触发阈值的路径验证停单、撤单与强平。')
    add('交易时段过滤', r'input\.session|time\([^\n]*[Ss]ession|\b(?:hour|minute|dayofweek)\b', 'session_time_logic', '现有解释器未执行完整session时段语义。', '盘前盘后、时区、午休和收盘前平仓行为可能不同。', '按交易所时区检查边界K线与夏令时。')
    add('入场limit限价', r'strategy\.(?:entry|order)\([^\n]*limit\s*=', 'entry_limit_orders', '现有结果不足以证明待成交限价单、撤单与跨K线保留得到忠实模拟。', '买入限价限制最高买价、卖出限价限制最低卖价；挂单价不保证成交，open限价也不必然更便宜。', '对齐挂单时刻、触价、跳空、撤单和成交价。')
    add('入场stop触发单', r'strategy\.(?:entry|order)\([^\n]*stop\s*=', 'entry_stop_orders', '现有结果不足以证明stop触发顺序和stop-limit联动保真。', '入场stop是突破触发价，不等于持仓止损；同有stop与limit时为触发后限价，可能不成交。', '分别验证触发价格与限价成交，包含跳空未成交路径。')
    add('退出价格与点数', r'strategy\.exit|syminfo\.mintick', 'exit_orders', '现有退出模拟不等同于交易所逐笔路径；同根触及多个价位的先后需核验。', 'stop/limit通常是绝对价格；profit/loss及追踪点数需按minTick换算，不能假设所有股票固定0.01。平均开仓价也不能替换为当前收盘价。', '核对平均开仓价、止盈价、止损价、minTick和同根优先顺序。')
    if not matrix:
        matrix.append(dict(feature='基础信号与成交', source_evidence='已提供源码%d字符；入场切片%d条、退出切片%d条。' % (len(code),len(base.get('entry_rules') or []),len(base.get('exit_rules') or [])), backtest_behavior='排名引用现有解释器结果；未逐笔与原平台对照。', impact='未检出特殊特征不等于语义保真。', verification='保真未验证：对齐信号时间、成交价、持仓及费用。'))
    metric_labels = [('cagr','复合年增长率',True),('sharpe','夏普比率',False),('max_dd','最大回撤',True),('calmar','卡玛比率',False),('trades','交易数',False),('exposure','组合平均资金暴露',True),('win_rate','胜率',True),('profit_factor','盈利因子',False),('avg_hold_days','平均持仓天数',False),('short_trade_frac','空头交易占比',True),('tickers_run','股票数',False)]
    blocks = [('日线',daily),('近三年历史末段',recent)]
    blocks += [(str(row.get('tf','未知周期')), _metrics(row)) for row in ranked.get('intraday',[]) if isinstance(row,dict)]
    for label, data in blocks:
        parts = []
        for key, name, percent in metric_labels:
            value = _number(data.get(key))
            if value is not None:
                parts.append('%s%s' % (name, ('%.2f%%' % (value*100)) if percent else ('%.3g' % value)))
        findings.append('%s已有记录：%s。' % (label, '；'.join(parts) if parts else '可用有限数值缺失，不补造收益、胜率或交易次数'))
        equity = _number(data.get('finalEquity',data.get('final_equity')))
        if equity is not None:
            findings.append('%s已有finalEquity为%s；这是100,000初始模拟本金口径的期末值，非实际账户收益，未由年化收益反推。' % (label, format(equity,',.2f')))
        exp, trades, tickers = (_number(data.get(key)) for key in ['exposure','trades','tickers_run'])
        if exp is not None:
            findings.append('%s exposure按每时点min(n_active, 20) / 20再取均值，表示组合平均资金暴露；同时持有20只股票即可达到上限，不表示每只股票的持有时间。' % label)
        if exp is not None and exp > .95:
            density = trades / tickers if trades is not None and tickers is not None and tickers > 0 else None
            hold = _number(data.get('avg_hold_days'))
            if density is not None and density <= 2 and hold is not None and hold >= 90:
                findings.append('%s组合平均资金暴露%.2f%%，交易数/股票数%.2f且平均持仓%.1f天；结合低交易密度及长持仓，这可能是持有型结果，仍需核对逐股分布。' % (label, exp * 100, density, hold))
            else:
                findings.append('%s组合平均资金暴露%.2f%%；高资金利用不等于频繁交易或持有型。缺少低交易密度与长持仓的联合支持，不能推断每股持有特征；5分钟数据频率也不证明日内频繁交易。' % (label, exp * 100))
        if trades is not None and trades <= 20:
            weaknesses.append('事实：%s只报告%.0f笔交易；推断：少量事件可能主导汇总表现，需查看逐股逐笔分布。' % (label,trades))
    findings.append('近三年指标是已有历史末段切片，不是独立样本外（OOS）检验；筛选与参数选择是否接触该时段未证明。')
    findings.append('跨周期使用不同股票池和窗口，是相关证据；不合计交易数充当独立样本，周期分数也不是同一组合的收益。')
    dc, bc = _number(daily.get('cagr')), _number((benchmark or {}).get('cagr'))
    if dc is not None and bc is not None:
        if ranked.get('cohort') == 'full_daily':
            findings.append('同一全市场日线窗口下，与提供基准的复合年增长率差为%+.2f个百分点，仅作同口径参考；该差未调整风险和仓位，不是超额收益归因。' % ((dc-bc)*100))
        else:
            findings.append('提供的基准属于全市场日线窗口；本记录为%s，异股票池或口径未确认，不可直接比较CAGR差，不据此计算百分点差。' % ('50股初筛' if ranked.get('cohort') == 'screening50' else '未确认队列'))
    if dc is not None:
        (strengths if dc>0 else weaknesses).append('事实：日线记录复合年增长率%.2f%%；仅描述该回测口径，不证明未来可持续。' % (dc*100))
    if _number(daily.get('max_dd')) is not None:
        weaknesses.append('事实：日线最大回撤%.2f%%；回撤恢复期、年度收益和最差单笔未在该汇总字段提供，不能据此推算。' % (float(daily['max_dd'])*100))
    if base.get('entry_explanation'):
        strengths += ['已有源码复核意见：' + str(s) for s in _items(base.get('strengths'))]
        weaknesses += ['已有源码复核风险：' + str(s) for s in _items(base.get('weaknesses'))]
    strengths += ['事实：有%d条入场证据、%d条退出证据可回查；可审查性不等于获利能力。' % (len(base.get('entry_rules') or []),len(base.get('exit_rules') or []))]
    weaknesses += ['执行差异：%s。%s' % (r['feature'], r['impact']) for r in matrix if r['feature'] != '基础信号与成交']
    critical = [str(item) for item in _items(base.get('critical_findings'))]
    if critical:
        weaknesses = ['本轮源码精读关键发现：' + item for item in critical] + weaknesses
    critical_summary = ('本轮关键发现：' + '；'.join(critical) + ' ') if critical else ''
    title = base.get('title','未命名策略')
    scores = []
    for key, label in [('current_logic_score','当前逻辑分'),('daily_score','日线表现分'),('recent_score','历史末段分'),('risk_penalty','风险扣分'),('combined_score','综合分')]:
        value = _number(ranked.get(key))
        if value is not None:
            scores.append('%s%.2f' % (label,value))
    validation = [r['verification'] for r in matrix]
    validation += ['逐条核对上述完整入场/退出条件及自定义函数；先固定默认参数，再做参数邻域敏感度，避免用排名反向挑参数。', '在同股票池、同窗口、同费用和同仓位下与持有基准比较；另保留未参与挑选的后续窗口。', '检查逐股分布、逐笔成交和交易集中度；当前任务只解释既有记录，以上是待验证计划，没有重跑回测。']
    return dict(
        overview=critical_summary + '%s：%s；%s。现有回测来自解释器，不能视为原策略真实交易。' % (title,base.get('family',base.get('category','未分类')), '、'.join(scores) or '评分数据缺失'),
        principle=('已有源码复核原理：' if base.get('entry_explanation') else '原目录原理摘要（需对照源码，作者描述不等于事实）：') + str(base.get('principle') or base.get('category_evidence') or '未提供独立原理说明，以以下具体信号及订单规则为依据。'),
        signal_explanations=signals, entry_steps=_rules(base,'entry'), exit_steps=_rules(base,'exit'), sizing_analysis=sizing,
        execution_timeline=['数据周期：%s；源码市场：%s。该配置不自动代表美股适用性。' % (base.get('period','未提供'),base.get('market','未提供')), '先计算上述指标及历史引用，再判断完整条件并申请订单；信号出现、挂单与成交是不同事件。', '成交时间需核对process_orders_on_close、calc_on_every_tick与挂单类型；静态切片不能证明本根收盘或下一根开盘实际成交。', '持仓后按退出规则处理；反向订单、部分退出与同根止盈止损的顺序须逐笔验证。'],
        parameter_notes=parameters, performance_findings=findings, strengths=strengths, weaknesses=weaknesses,
        engine_compatibility=matrix, validation_plan=validation,
        verdict=critical_summary + '研究优先级：%s。该排序综合现有表现与逻辑审查；%d项执行语义需核验，尚不能推出原策略的可交易收益。' % ('、'.join(scores) or '无有效分数',len(matrix)),
        detail_level='沿用已有逐份源码复核并补充回测解释' if base.get('entry_explanation') else '自动语义辅助解释；不是逐份人工源码复核',
        evidence_provenance=['完整源码保留于卡片code字段；原文文件：%s；源内容校验：%s。' % (base.get('filename','未提供'),base.get('source_sha256','未提供')), '所有表现引用已有回测文件；本轮没有重跑回测，也没有验证真实成交保真。'],
        prior_review_context=('外部历史短评，仅供追溯，非本轮复核：' + str(ranked['prior_comment'])) if ranked.get('prior_comment') else '未提供外部历史短评。',
        score_interpretation=scores or ['无有效评分字段；不估计缺失分数。'],
        unresolved_questions=['自定义函数、递归、request.security及嵌套控制流是否完整执行需原平台逐笔对照；词法解释不能证明这些语义。', '股票池、时间窗口和费用变化对结果的影响需要同口径实验，现有跨周期汇总不能隔离这些因素。'])
