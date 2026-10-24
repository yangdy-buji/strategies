"""Conservative, SHA-bound Pine source patches; no native compilation implied."""
import hashlib

FIXES = {}


def _register(sid, title, source_sha256, code_sha256, patches, remaining, cases):
    FIXES[sid] = dict(title=title, source_sha256=source_sha256,
                      code_sha256=code_sha256, patches=patches,
                      changes=[p[2] for p in patches], remaining=remaining,
                      validation_cases=cases)


def apply_fix(sid: int, code: str, source_sha256: str, registry=None) -> str:
    """Fail closed on unknown SID, source/code drift or non-unique anchors."""
    registry=FIXES if registry is None else registry
    if sid not in registry:
        raise ValueError(f'Unknown fix SID: {sid}')
    fix = registry[sid]
    if source_sha256 != fix['source_sha256']:
        raise ValueError(f'SID {sid}: source SHA mismatch')
    if hashlib.sha256(code.encode('utf-8')).hexdigest() != fix['code_sha256']:
        raise ValueError(f'SID {sid}: code SHA mismatch')
    for number, (old, new, reason, preserved) in enumerate(fix['patches'], 1):
        reason=reason.replace('\r',' ').replace('\n',' ')
        preserved=preserved.replace('\r',' ').replace('\n',' ')
        if code.count(old) != 1:
            raise ValueError(f'SID {sid}: patch {number} anchor must match exactly once')
        # Subexpression patches must not insert comments into an executable line.
        position=code.index(old)
        line_start=code.rfind('\n',0,position)+1
        line=code[line_start:].split('\n',1)[0]
        indent=line[:len(line)-len(line.lstrip(' \t'))]
        note = (f'{indent}// OPT-{sid}-{number:02d}：{reason}\n'
                f'{indent}// OPT-{sid}-{number:02d} 保持：{preserved}\n'
                f'{indent}// OPT-{sid}-{number:02d} 验证：未原生Pine编译/回测；静态/表达式用例不证明收益。\n')
        code=code[:position]+new+code[position+len(old):]
        code=code[:line_start]+note+code[line_start:]
    return code

_register(
    621,
    '反向信号撤销多头限价单',
    'ae4106355ea696bcb1e5c7cc84aebbc283beacd2efe0c211a07706d37be56054',
    'cffceaaa187aad20240ebfaf5618692dacdb3b7516272c9bfdc4b257a10275b6',
    [('if short\n    strategy.close', 'if short\n    strategy.cancel("Long")\n    strategy.close', '原反向信号仅平仓且遗留限价单；先撤Long待成交单再平仓。', '原short条件、Long限价入场、平仓及警报。')],
    ['未原生Pine编译/回测；静态及小范围模型不等于订单成交模拟，旧版收益不适用。'],
    ['反向信号撤单先于平仓；挂单集合清空后不再触价买入。']
)

_register(
    735,
    'RSI平仓ID关联修复',
    'a82e0b961539d2b7d6cb3a9df58a2eadf4c7abbaeb0d0e24229cb16d294bf610',
    'e4bbda59eac55965fc521145f01bf63ad8f7cd47b687ea8987a270d55fb9d548',
    [('    strategy.close("RSICLose", when=bull_cross)', '    strategy.close("RSI", when=bull_cross)', '原平仓ID无对应入场；改为RSI以正确关联。', 'EXIT与bull_cross双重门禁、Buy订单和全部参数。')],
    ['未原生Pine编译/回测；静态及小范围模型不等于订单成交模拟，旧版收益不适用。'],
    ['订单ID关联及EXIT/bull_cross四组合。']
)

_register(
    2458,
    '恢复入场日期门禁',
    'bc5722e8427f767693149c947e9776c5b45e7fdcee8e1b555dc4dac9dfe2195f',
    'b33bbc9842fb275975899b6686adfca7a930962243ab0d410af29bd0a8e41910',
    [('isWithinTradingWindow = true', 'isWithinTradingWindow = time >= startTimeInput and time <= endTimeInput', '原日期门禁恒真；恢复起止参数并包含边界，仅限制入场。', '日期默认值、EMA过滤及独立退出条件。')],
    ['未原生Pine编译/回测；静态及小范围模型不等于订单成交模拟，旧版收益不适用。'],
    ['前/起始/中间/结束/后五点日期边界；独立退出保留。']
)

_register(
    2943,
    '恢复入场日期且保留原止损限制',
    'f4f2e0e3c7e993f8e619ab1861c9f4f3180b7cfc31b29e625549cd9f8792e852',
    '134de6b56eae2bdeca3cb866b4f742d3fce420d942a851cd9fe76b10db64b835',
    [('inDateRange = true', 'inDateRange = time >= i_startTime and time <= i_endTime', '原日期门禁恒真；恢复包含边界的日期范围，只作用于原入场条件。', '原止损颜色限制、等待收盘配置、退出及默认日期。')],
    ['止损仍受color.green限制，本轮保留。', '未原生Pine编译/回测；静态及小范围模型不等于订单成交模拟，旧版收益不适用。'],
    ['日期五点边界；两条退出文本与颜色门禁不变。']
)

_register(
    3322,
    '持仓期间持续提交保护单',
    '8637e9238b926156759354b8d49f1b3cbeff4a7e9e6ef7fe0aeee08dd75207bf',
    'caa922bf8431b8c5248f98738e1af95fe457c16503c2fe9d7a7541be6e8fd6f3',
    [('if (longCondition )\n    strategy.entry("Long", strategy.long)\n    strategy.exit("Take Profit/Stop Loss", "Long", limit=takeProfit, stop=stopLoss)', 'if (longCondition )\n    strategy.entry("Long", strategy.long)\nif strategy.position_size > 0\n    strategy.exit("Take Profit/Stop Loss", "Long", limit=takeProfit, stop=stopLoss)', '原保护单仅在入场信号为真时提交；改为确认持多仓时持续提交，空仓不提交。', '入场信号、均价锚点与原100%止损默认（止损价为零，仍存在风险）；未增加成交后即时重算。')],
    ['默认100%止损产生零止损价；首次成交到后续计算之间保护覆盖未验证。', 'start_date/end_date仍未接入，本轮未扩大范围。', '未原生Pine编译/回测；静态及小范围模型不等于订单成交模拟，旧版收益不适用。'],
    ['保护单独立于入场信号且仅持多仓提交；100%默认值保留。']
)

_register(
    3330,
    '仅开仓应用起始日期',
    '1b9f9c478c4596263b90f899492771a015cd0a44b3866c392f9a421dc68fb3d1',
    'c59ed9691eef481f276b1242ccbe14d158621ec934a41297ae258a3b8ac1d722',
    [('    buy_condition = touched_lower_bb and MACD > aMACD or expected_rebound', '    buy_condition = (touched_lower_bb and MACD > aMACD) or expected_rebound', '原AND/OR依赖优先级；加括号明确两条原入场路径而不改变逻辑。', 'expected_rebound可独立触发的原语义，未改为另一组AND。'), ('    if strategy.position_size == 0 and buy_condition', '    if strategy.position_size == 0 and buy_condition and time >= backtest_timeframe_start', '原起始时间闲置；只在开仓分支增加包含起始时刻门禁。', '外层true、信号状态更新、持仓计数和所有退出分支，未启用结束日期。')],
    ['未原生Pine编译/回测；静态及小范围模型不等于订单成交模拟，旧版收益不适用。'],
    ['AND/OR八组合真值表；仅开仓加日期且全部退出文本不变。']
)

_register(
    3883,
    '买入警报金额说明修正',
    '02ce2e430748815e7aa1762cb67b30c4f7df0278c3b8358f41cdb19fb24a97b4',
    '1a97aa7aab392c65a14c749c92060ad6799a149b9085550941f4b3271be6bb7b',
    [('alertcondition(buyDip1, title="Dip1 Buy", message="Price dipped 10% from ATH, buying $1000")', 'alertcondition(buyDip1, title="Dip1 Buy", message="Price dipped 10% from ATH; buy amount uses configured buy_amount (Buy Amount ($))")', '原警报固定1000与真实配置不符；常量消息改为明确指向buy_amount参数。', 'alertcondition常量消息要求、原触发条件、真实qty、默认金额及不开启加仓。'), ('alertcondition(buyDip2, title="Dip2 Buy", message="Price dipped 15% from ATH, buying $1000")', 'alertcondition(buyDip2, title="Dip2 Buy", message="Price dipped 15% from ATH; buy amount uses configured buy_amount (Buy Amount ($))")', '原警报固定1000与真实配置不符；常量消息改为明确指向buy_amount参数。', 'alertcondition常量消息要求、原触发条件、真实qty、默认金额及不开启加仓。'), ('alertcondition(buyDip3, title="Dip3 Buy", message="Price dipped 20% from ATH, buying $1000")', 'alertcondition(buyDip3, title="Dip3 Buy", message="Price dipped 20% from ATH; buy amount uses configured buy_amount (Buy Amount ($))")', '原警报固定1000与真实配置不符；常量消息改为明确指向buy_amount参数。', 'alertcondition常量消息要求、原触发条件、真实qty、默认金额及不开启加仓。')],
    ['原层级布尔状态不等同实际成交确认；未开启加仓。', '未原生Pine编译/回测；静态及小范围模型不等于订单成交模拟，旧版收益不适用。'],
    ['三条警报指向配置；常量消息、真实qty和订单不变。']
)

_register(
    4143,
    '日期结束撤单',
    '1860e3e1e6e6bf80db9253ffbf308535ddc7a8b95017058556a2fdeab2f11bcd',
    '7bb845f51df11c513ea7e60ec725f229eb3234fa5147435c6a6d6b54d79b3cf9',
    [('if time > timestamp(toyear, tomonth, today, 23, 59)\n    strategy.close_all()', 'if time > timestamp(toyear, tomonth, today, 23, 59)\n    strategy.cancel_all()\n    strategy.close_all()', '原结束日期分支仅全平；增加撤销未成交订单以避免后续触价成交。', '既有严格晚于结束时刻条件、needtime、分层入场及零qty退出。')],
    ['原零qty反向entry退出语义与多层挂单敞口未修复。', '未原生Pine编译/回测；静态及小范围模型不等于订单成交模拟，旧版收益不适用。'],
    ['仅原日期结束分支增加撤单，其他可执行文本保持。']
)

_register(
    4621,
    '恢复入场日期并解除退出日期限制',
    '6f52852843a35fa7f885d23aec5ace9399b970fd95485146e3e8f8d01b228c26',
    'fd9a3fa946122cc32ef8a1d20d672c783ed31042ab5f3e7a7b5d689866c4dc3d',
    [('inDateRange = true', 'inDateRange = time >= startDate and time <= endDate', '原日期门禁恒真；恢复包含边界的起止参数。', '原2020年默认窗口与信号，恢复窗口会改变交易覆盖期。'), ('if(close > emaH and inDateRange and checkThreeConsecutiveCandles and barstate.isconfirmed)', 'if(close > emaH and checkThreeConsecutiveCandles and barstate.isconfirmed)', '原退出依赖日期门禁；移除该依赖使窗外仍能退出。', 'EMA、连续蜡烛和barstate确认条件及另一路退出。')],
    ['未原生Pine编译/回测；静态及小范围模型不等于订单成交模拟，旧版收益不适用。'],
    ['日期五点边界；退出仍保留连续蜡烛及确认条件。']
)

_register(
    4941,
    '恢复时间门禁并撤销窗外入场单',
    '2ee97c3e5f0eb56a6bcbbc73e569ab101709ea0d36b30bd61b4cc8f895ae6ae3',
    '4b9e623bcedc5a8df8fb46bb83bd1aa5d20f40fe41e0c340ce86586095737b7b',
    [('needtime = true', 'needtime = time > timestamp(fromyear, frommonth, fromday, 00, 00) and time < timestamp(toyear, tomonth, today, 23, 59)', '原needtime恒真；按既有日期参数恢复严格起止时间条件（边界不入场）。', '默认日期、层级、仓位、零qty退出；与既有严格晚于结束时间全平条件一致，恰好结束时仅撤入场单。'), ('if ma > 0\n    lots := round(size / lot)', 'if not needtime\n    strategy.cancel("L1")\n    strategy.cancel("L2")\n    strategy.cancel("L3")\n    strategy.cancel("S1")\n    strategy.cancel("S2")\n    strategy.cancel("S3")\nif ma > 0\n    lots := round(size / lot)', '原窗口外可能遗留入场限价单；在窗口外逐次撤销六个入场ID。', 'TPL/TPS不在此撤销；原期末全平及八单撤销分支完整保留。')],
    ['原零qty退出、总敞口与边界全平时点未重写。', '未原生Pine编译/回测；静态及小范围模型不等于订单成交模拟，旧版收益不适用。'],
    ['窗外六个入场ID撤销；TPL/TPS保留；原期末全平分支不变。']
)

_register(
    5369,
    '布林带元组顺序修复',
    '96452178fd848ba9d71492ab33871aa3cde502ed5bae4bcbbc25ed6fb864ed40',
    '078af8ca93a9d8e1584b28917a7858255a983474fba92e72ad43ee6dec117440',
    [('[upperBB, middleBB, lowerBB] = bb(close, bbPeriod, bbDeviation)', '[middleBB, upperBB, lowerBB] = bb(close, bbPeriod, bbDeviation)', '原上轨误接中轨；按bb返回中、上、下轨顺序接收。', '原指标参数、穿越条件及双向交易规则。')],
    ['未原生Pine编译/回测；静态及小范围模型不等于订单成交模拟，旧版收益不适用。'],
    ['已知中轨100、上轨120、下轨80；买入边界110/120/121。']
)
