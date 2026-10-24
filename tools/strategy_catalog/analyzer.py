"""Conservative source-only catalogue analysis; never executes trading code.

Rules are lexical evidence slices, not a compiler/control-flow proof. All line
references are one-based Markdown source lines. Scores assess review readiness,
not expected return or deployability.
"""
from __future__ import annotations

from pathlib import Path
import hashlib
import re


def _mask(code, language):
    # Preserve offsets/newlines while excluding comments and quoted literals.
    pattern = r'/\*[\s\S]*?\*/|//[^\n]*|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\''
    if language.lower() == 'python':
        pattern = r'"""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'|\#[^\n]*|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\''
    return re.sub(pattern, lambda m: re.sub(r'[^\n]', ' ', m[0]), code)


def _section(text, name):
    m = re.search(r'^>\s*' + re.escape(name) + r'\s*\n([\s\S]*?)(?=^>\s|\Z)', text, re.M)
    return m[1].strip() if m else ''


def _source(text):
    marker = re.search(r'^>\s*Source\s*\(([^)]+)\)[^\n]*\n', text, re.M)
    if not marker:
        return '', 'unknown', 0
    after = text[marker.end():]
    fence = re.search(r'^\s*(`{3,}|~{3,})[^\n]*\n', after, re.M)
    if not fence:
        return '', marker[1], 0
    start = marker.end() + fence.end()
    closing = re.search(r'^' + re.escape(fence[1]) + r'\s*$', text[start:], re.M)
    end = start + closing.start() if closing else len(text)
    code = text[start:end]
    if code.endswith('\n'):
        code = code[:-1]  # Only the structural newline preceding the fence.
    return code, marker[1], text[:start].count('\n') + 1


def _rules(code, masked, start_line):
    original, clean = code.splitlines(), masked.splitlines()
    definitions = {}
    for i, line in enumerate(clean):
        m = re.match(r'\s*(?:(?:var|let|const|float|int|bool|string)\s+)*(\w+)\s*(?::=|=(?!=))', line)
        if m:
            definitions.setdefault(m[1], []).append(i)
        tuple_assignment = re.match(r'\s*(?:var\s+)?\[([^]\n]+)\]\s*(?::=|=(?!=))', line)
        if tuple_assignment:
            for name in tuple_assignment[1].split(','):
                name = name.strip()
                if name != '_' and re.fullmatch(r'\w+', name):
                    definitions.setdefault(name, []).append(i)
    entry, exits = [], []
    pattern = re.compile(r'\bstrategy\.(entry|order|exit|close_all|close)\s*\(|\b(?:exchange|exchanges\s*\[[^\]]+\]|\$)\.(Buy|Sell)\s*\(')
    for match in pattern.finditer(masked):
        i = masked[:match.start()].count('\n')
        cursor, depth = match.end(), 1
        while cursor < len(masked) and depth:
            depth += (masked[cursor] == '(') - (masked[cursor] == ')')
            cursor += 1
        end = masked[:cursor].count('\n')
        chosen = set(range(i, min(end + 1, len(clean))))
        control_ends = {}
        # Indentation is reliable for Pine/Python. For brace languages retain
        # nearby enclosing controls as evidence, with explicit uncertainty.
        indent = len(clean[i]) - len(clean[i].lstrip())
        for j in range(i-1, -1, -1):
            s = clean[j].strip()
            level = len(clean[j]) - len(clean[j].lstrip())
            if s and level < indent:
                if re.match(r'(if\b|else\b|for\b|while\b)', s):
                    chosen.add(j)
                    balance = clean[j].count('(') + clean[j].count('[') - clean[j].count(')') - clean[j].count(']')
                    k = j
                    while balance > 0 and k+1 < i:
                        k += 1
                        chosen.add(k)
                        balance += clean[k].count('(') + clean[k].count('[') - clean[k].count(')') - clean[k].count(']')
                    control_ends[j] = k
                indent = level
        # Follow only prior definitions, transitively, with a finite review cap.
        pending = set(re.findall(r'\b\w+\b', '\n'.join(clean[k] for k in chosen)))
        seen = set()
        while pending and len(chosen) < 120:
            name = min(pending)
            pending.remove(name)
            if name in seen:
                continue
            seen.add(name)
            for j in definitions.get(name, []):
                if j < i and j not in chosen:
                    chosen.add(j)
                    # Multiline definition continuation up to balanced delimiters.
                    balance = clean[j].count('(') + clean[j].count('[') - clean[j].count(')') - clean[j].count(']')
                    k = j
                    while balance > 0 and k+1 < i:
                        k += 1
                        chosen.add(k)
                        balance += clean[k].count('(') + clean[k].count('[') - clean[k].count(')') - clean[k].count(']')
                    pending.update(re.findall(r'\b\w+\b', '\n'.join(clean[n] for n in range(j,k+1))))
        excerpt = '\n'.join(f'L{start_line+j}: {original[j]}' for j in sorted(chosen))
        action = match[1] or match[2]
        call = code[match.start():cursor]
        # Split arguments at top level, retaining named conditions and prices.
        args, offset, nesting = [], match.end(), 0
        for n in range(match.end(), max(match.end(), cursor-1)):
            char = masked[n]
            nesting += (char in '([{') - (char in ')]}')
            if char == ',' and nesting == 0:
                args.append(code[offset:n].strip())
                offset = n+1
        args.append(code[offset:max(offset,cursor-1)].strip())
        named = [arg for arg in args if re.match(r'\w+\s*=',arg)]
        conditions = [' '.join(original[k].strip() for k in range(j, control_ends.get(j,j)+1)) for j in sorted(chosen) if j <= i and re.match(r'\s*(?:if|else|while|for)\b',clean[j])]
        conditions += [arg for arg in named if re.match(r'when\s*=',arg)]
        direction = '做多' if 'strategy.long' in call else '做空' if 'strategy.short' in call else '买入' if action=='Buy' else '卖出' if action=='Sell' else '退出/平仓' if action in ('exit','close','close_all') else '方向需复核'
        identity = args[0] if args and args[0] else '未显式提供'
        settings = [arg for arg in named if not re.match(r'when\s*=',arg)]
        if action=='exit' and len(args)>1 and not re.match(r'\w+\s*=',args[1]):
            settings.insert(0,'关联入场ID='+args[1])
        operators=[]
        if re.search(r'\bcrossover\s*\(',excerpt): operators.append('crossover 表示上穿')
        if re.search(r'\bcrossunder\s*\(',excerpt): operators.append('crossunder 表示下穿')
        if '<' in ' '.join(conditions): operators.append('< 表示小于（含 <= 时为小于等于）')
        if '>' in ' '.join(conditions): operators.append('> 表示大于（含 >= 时为大于等于）')
        explanation = f'{action}：{direction}；订单ID/首参：{identity}。触发条件：'+ ('；'.join(conditions) if conditions else '调用点未识别额外条件，需查看所处函数及调用路径')+'。'
        if settings: explanation += '订单设置：'+'；'.join(settings)+'。'
        if operators: explanation += '条件含义：'+'；'.join(operators)+'。'
        explanation += '下方源码包含已追溯的前置变量定义；静态切片未确认完整控制流、函数内部依赖与实际成交。'
        rule = {'line': start_line+i, 'code': excerpt,
                'explanation': explanation, 'analysis_complete': False}
        (exits if action in ('exit','close','close_all') else entry).append(rule)
    return entry, exits


def analyze(path: Path) -> dict:
    path = Path(path)
    raw = path.read_bytes()
    text = raw.decode('utf-8', errors='replace')
    code, language, start = _source(text)
    masked = _mask(code, language)
    entries, exits = _rules(code, masked, start)
    description = _section(text, 'Strategy Description')
    is_index = path.name.lower() == 'readme.md' and not code
    if is_index:
        description = text
    description = re.split(r'^\s*\|\|\s*$', description, maxsplit=1, flags=re.M)[0]
    description = re.sub(r'^\s*\[trans\]\s*', '', description).strip()
    if len(description) > 12000 and not is_index:
        description = description[:12000] + '\n【作者说明超过12000字，已截断；完整内容见源文件。】'
    declaration = bool(re.search(r'\bstrategy\s*\(', masked))
    indicator = bool(re.search(r'\b(?:indicator|study)\s*\(', masked))
    tool = bool(re.search(r'\b(?:class\s+Task|Promise|Thread|HttpQuery|WebSocket|LogStatus)\b', masked)) and not entries
    # A plugin returning a UI table with manual side/count arguments is a tool.
    manual_tool = bool(re.search(r'\breturn\s+tbl\b', masked) and re.search(r'\bTransactionTimes\b', masked))
    my_order = language.lower() == 'mylanguage' and bool(re.search(r'\b(?:BK|SK|BPK|SPK|BP|SP)\s*;', masked, re.I))
    kind = 'tool' if manual_tool or is_index else 'strategy' if declaration or entries or my_order else 'indicator' if indicator else 'tool' if tool else 'unknown'
    # Family is based on referenced source expressions, never marketing titles.
    relevant = '\n'.join(x['code'] for x in entries) or masked
    relevant = _mask(relevant, language)
    families = [
        (r'\b(?:supertrend)\s*\(', '趋势跟随', '超级趋势', 'SuperTrend'),
        (r'\b(?:rsi|stoch|stochrsi)\s*\(', '待分类', '动量振荡指标', 'RSI/Stochastic'),
        (r'\b(?:macd)\s*\(', '趋势跟随', 'MACD趋势动量', 'MACD'),
        (r'\b(?:bb|bbands|stdev)\s*\(', '待分类', '波动率通道', '波动率'),
        (r'\b(?:ema|sma|wma|hma|rma|dema|tema)\s*\(', '趋势跟随', '均线信号', '均线'),
        (r'\b(?:atr)\s*\(', '待分类', 'ATR波动率信号', 'ATR'),
        (r'\b(?:highest|lowest)\s*\(', '动量／突破', '区间突破', '价格通道'),
        (r'\bGetDepth\s*\(', '待分类', '订单簿信号', '订单簿'),
    ]
    matches = [(category, family, tag) for pattern, category, family, tag in families if re.search(pattern, relevant, re.I)]
    category, family = matches[0][:2] if matches else ('待分类','未确认信号家族')
    principle_match = re.search(r'^(#{1,6})[ \t]+(?:策略原理|策略逻辑|交易原理|原理|核心逻辑)[^\n]*\n',description,re.M)
    principle_text = ''
    principle_source = '作者原理章节'
    if principle_match:
        section_body = description[principle_match.end():]
        boundary = re.search(r'^#{1,' + str(len(principle_match[1])) + r'}[ \t]+',section_body,re.M)
        principle_text = section_body[:boundary.start()].strip() if boundary else section_body.strip()
    if not principle_text and description.strip():
        principle_text = description.strip()
        principle_source = '作者说明（原理章节缺失或为空，回退）'
    principle = '作者陈述（未验证；来源：'+principle_source+'）：\n'+principle_text if principle_text else '未提供可识别的作者原理说明；请依据源码人工核查。'
    category_evidence = '依据订单依赖源码中的指标函数作粗分类，未证明实际经济机制。'
    # Author claims only support a candidate when matching source evidence exists.
    # Restrict to the principle section to avoid classifying proposed improvements.
    supported = bool(matches)
    candidate = None
    if supported and re.search(r'均值回归|回归均值|超买超卖|低买高卖|超卖.*(?:买入|做多)|超买.*(?:卖出|做空)',principle_text):
        candidate='均值回归'
    elif supported and re.search(r'突破|动量',principle_text):
        candidate='动量／突破'
    elif supported and re.search(r'趋势|跟踪|顺势',principle_text):
        candidate='趋势跟随'
    if candidate and category=='待分类':
        category=candidate
        category_evidence='作者原理描述与订单依赖中的指标函数相互支持的候选分类，方向与机制仍需人工核查。'
    if category=='待分类' and supported:
        # Do not infer mean reversion from RSI alone; use order direction and
        # an actual comparison linked to the oscillator's assigned variable.
        oscillator_vars=re.findall(r'\b(\w+)\s*=\s*(?:ta\.)?(?:rsi|stoch)\s*\(',masked)
        for rule in entries:
            if 'strategy.long' not in rule['code']:
                continue
            for variable in oscillator_vars:
                if re.search(r'\b'+re.escape(variable)+r'\s*<',rule['code']):
                    category='均值回归'
                    category_evidence='做多订单关联振荡器低于阈值的条件；暂列均值回归候选，阈值及上下文待复核。'
                elif re.search(r'\b'+re.escape(variable)+r'\s*>',rule['code']):
                    category='动量／突破'
                    category_evidence='做多订单关联振荡器高于阈值的条件；暂列动量候选，阈值及上下文待复核。'
    if kind in ('tool','indicator','unknown'):
        category = {'tool':'辅助资料','indicator':'辅助资料','unknown':'待分类'}[kind]
    tags = list(dict.fromkeys(x[2] for x in matches))
    if len(matches)>1: tags.append('多类指标线索')
    params = [line.strip() for line in code.splitlines() if re.search(r'\binput(?:\.\w+)?\s*\(', _mask(line,language))]
    params += [line.strip() for line in _section(text,'Strategy Arguments').splitlines() if line.startswith('|') and not re.match(r'^\|(?:Argument|[-:])',line)]
    positions = [line.strip() for line in code.splitlines() if re.search(r'\b(?:qty|default_qty_value|default_qty_type|pyramiding|strategy\.risk|percent_of_equity)\b', _mask(line,language))]
    risks=[]
    def risk(title, evidence, line=0, severity='待核查'):
        risks.append({'severity':severity,'title':title,'evidence':evidence,'line':line})
    for i,line in enumerate(masked.splitlines()):
        if 'lookahead_on' in line:
            risk('跨周期前视设置需核查', code.splitlines()[i]+'；若表达式使用已完成高周期值（如[1]），可能是合法对齐；不能据此判定前视偏差。',start+i)
        if re.search(r'\b(?:pivothigh|pivotlow)\s*\(',line):
            risk('枢轴确认延迟需核查',code.splitlines()[i]+'；需检查确认时点与绘图回移，未证明存在前视。',start+i)
    weaknesses=['仅完成源码静态初审，未运行、未回测，收益、稳健性和实盘可行性未验证。']
    strengths=[]
    if entries:
        strengths.append('发现明确订单调用，可追溯到原文行号和关联条件。')
    if exits:
        strengths.append('识别到显式退出调用；止损是否有效覆盖所有仓位仍需验证。')
    elif kind=='strategy':
        weaknesses.append('未识别显式退出调用；不代表不存在退出，需核查反向入场、封装函数和平台行为。')
        risk('退出覆盖未确认','静态扫描未识别 strategy.exit/close/close_all；不能据此断言没有退出机制。')
    if 'strategy.long' in masked and 'strategy.short' in masked and entries:
        weaknesses.append('同时出现多空订单方向；反向 strategy.entry 可能触发持仓反转，需验证仓位与成本。')
    if kind=='strategy' and not positions:
        weaknesses.append('未识别明确仓位预算配置，默认仓位及最大风险暴露待核查。')
    cost = bool(re.search(r'\bcommission_(?:value|type)\s*=', masked))
    slip = bool(re.search(r'\bslippage\s*=', masked))
    if kind=='strategy' and not(cost and slip):
        weaknesses.append('交易成本设置识别不完整，手续费、滑点及成交假设需单独验证。')
    if kind=='unknown': weaknesses.append('未识别足以确认程序用途的源码特征，不按标题推定为交易策略。')
    if kind=='strategy':
        weaknesses.append('订单条件为词法切片；函数调用、分支可达性及依赖是否完整尚未确认。')
    scores=[]
    if kind=='strategy':
        values=[('获利机制',10 if entries and matches else 5,20,'仅识别源码关联指标线索；未验证经济逻辑、统计优势及交易收益。'),
                ('信号因果性',7 if any(x['title'].startswith(('跨周期','枢轴')) for x in risks) else 12,25,'未编译或回放；静态未发现疑点也不能证明无重绘、无前视，因果性仅部分确认。'),
                ('规则完整性',12 if entries and exits else 7 if entries else 3,20,'按显式入场及退出调用可追溯性初评；完整控制流、订单成交和分支覆盖未验证。'),
                ('风险与仓位',11 if exits and positions else 7 if exits else 4,20,'仅按退出及仓位配置可见性给分；最大损失、跳空及极端市场暴露未验证。'),
                ('美股执行',6 if cost and slip else 3,15,'仅识别成本配置字段；美股交易时段、公司行动、借券、流动性和券商执行均未验证，非上线评级。')]
        scores=[dict(dimension=d,score=s,max=m,reason=r) for d,s,m,r in values]
    period_match=re.search(r'^period:\s*([^\n]+)',code,re.M)
    market_match=re.search(r'["\']currency["\']\s*:\s*["\']([^"\']+)',code)
    url=re.search(r'https?://\S+',_section(text,'Detail'))
    return dict(id=hashlib.sha256(path.name.encode('utf-8')).hexdigest()[:12], filename=path.name,
                title=_section(text,'Name') or path.stem,source_sha256=hashlib.sha256(raw).hexdigest(),
                language=language,kind=kind,category=category,family=family,tags=tags,
                market=market_match[1]+'（源码回测配置，非适用性结论）' if market_match else '未明确',
                period=period_match[1].strip()+'（源码回测配置）' if period_match else '未明确',
                description=description,principle=principle,category_evidence=category_evidence,code=code,code_start_line=start,parameters=params,
                entry_rules=entries,exit_rules=exits,position_rules=positions,risks=risks,
                strengths=strengths,weaknesses=weaknesses,scores=scores,
                score=sum(x['score'] for x in scores) if scores else None,
                classification_confidence='中' if category != '待分类' and (declaration or indicator or manual_tool) else '低',
                review_status='自动初审',evidence_level='E0',performance_score=None,
                performance_status='未验证',source_url=url[0] if url else '',
                score_label='源码可审查性保守初评（不代表收益或投资建议）',
                analysis_limitations='词法分析，非编译或控制流证明；仅提取常见订单API，未知封装与麦语言订单规则待人工核查；家族表示信号线索，不表示近重复。')
