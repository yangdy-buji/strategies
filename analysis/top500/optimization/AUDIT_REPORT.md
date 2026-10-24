# 剩余489项静态源码审查结果

[优化登记](index.html) · [500项CSV](manifest.csv)

本轮完成489项完整源码静态审查，新增152个修复候选。全部500项状态：{"candidate": 163, "reviewed": 210, "needs_design": 127}。

未确认缺陷不代表没有风险；待设计项保持原代码。修复候选也可能仍有未处理问题，请阅读每张卡的剩余问题。没有原生Pine编译和回测，不声称收益提高。

## 新增修复候选

|原序号 / SID|策略|修改概要|

|---|---|---|

|14 / 3762|[多周期RSI超卖反转策略-Multi-Timeframe-RSI-Oversold-Reversal-Strategy](cards/79a39417ecce.html)|RSI退出覆盖已有额外入场ID，不改变加仓配置。；接入已有收盘止损布尔，并让止盈/止损覆盖两个入场ID。|

|15 / 4962|[相对量价策略Relative-Volume-Price-Strategy](cards/d85890022015.html)|日期输入未生效。；窗外持仓保持跟踪。；窗外已有持仓仍执行退出。；窗外不加仓。|

|21 / 1791|[动量自适应高斯通道多周期策略-Momentum-Adaptive-Gaussian-Channel-Multi-Period-Strategy](cards/34a4b08f72c0.html)|季节逻辑固定OR只支持跨年；起月早于止月时全年均为真，须同时支持非跨年范围。|

|25 / 2462|[均值恢复ATR趋势策略Mean-Reversion-ATR-Trend-Strategy](cards/e61446137522.html)|日期恒真绕过输入。；窗外不应重置已有持仓止损。；恢复日期只门控入场；已有持仓需继续处理退出。；已有持仓窗外不能加仓。|

|27 / 3301|[基于多重指标筛选与动态止损的自动交易策略Auto-Trading-Strategy-Based-on-Multiple-Indicators-and-Dynamic-Stop-Loss](cards/ce472780c958.html)|市价平仓必须调用close，exit缺少价格参数。；对称修复多头市价平仓API。|

|29 / 5419|[趋势跟踪止损策略Trend-Following-Strategy-with-Trailing-Stop-Loss](cards/a7d51c90d23e.html)|把现有正确日期函数接到唯一入场。|

|32 / 4488|[布林带突破动量跟踪交易策略-Bollinger-Bands-Breakout-Momentum-Trading-Strategy](cards/77bafc111633.html)|恢复日期。；出口移出日期窗。|

|36 / 4705|[日内多头突破策略-Intraday-Bullish-Breakout-Strategy](cards/07a7a5392ed8.html)|策略启用开关没有接入订单条件。|

|39 / 373|[Flawless-Victory-DCA-动量与波动率策略Flawless-Victory-DCA-Momentum-and-Volatility-Strategy](cards/979624b1af03.html)|保护退出覆盖两个做多入口ID。|

|44 / 2528|[均线震荡AO指标交易策略Moving-Average-AO-Indicator-Trading-Strategy](cards/ab74e505f295.html)|开始结束时间未用于入场过滤；恢复函数范围，退出已经独立有效。|

|48 / 5054|[移动平均线双轨与趋势跟踪策略Dual-Moving-Average-Channel-with-Trend-Tracking-Strategy](cards/049a3ba24aca.html)|日期函数恒真。；退出不能被日期阻断。|

|55 / 3524|[基于相对成交量和趋势的交易策略Relative-Volume-Trend-Following-Trading-Strategy](cards/aa91859a9fd0.html)|恢复可选结束时间的入场窗口。；不得因日期越界重置已有持仓跟踪止损。；将日期门槛下移至入场，退出控制流始终可达。|

|56 / 2486|[均线交叉长线并量化策略EMA-Crossover-for-Long-Line-Quant-Strategy](cards/949e2f5fb09a.html)|恢复入场日期。；退出移出日期限制。；退出移出日期限制。|

|57 / 5741|[高级斐波那契回调与成交量加权价格行为交易策略-Advanced-Fibonacci-Retracement-and-Volume-Weighted-Price-Action-Trading-Strategy](cards/8cf1a1f1c756.html)|数组每根新建归零，非更新bar比较0导致信号失真；应持久保存水平。另高低重置顺序与pinbar方向需设计确认。|

|62 / 3405|[基于快速移动均线和慢速移动均线的量化交易策略Dual-Moving-Average-Breakout-Strategy](cards/eee00608c188.html)|恢复模式入场时间范围。；单向多仓退出独立。；单向空仓退出独立。；双向模式窗外只平原仓，禁止反向新开。|

|63 / 4573|[形态识别吊颈线交易策略Pattern-Recognition-Pinbar-Trading-Strategy](cards/f8fc04aadb35.html)|恢复开始日期开关。；保留原始多头形态供窗外退出使用。；保留原始空头形态供窗外退出使用。；日期仅限制多头入场。；日期仅限制空头入场。；独立空头退出ID避免修改多头保护。；独立空头退出ID避免修改多头保护。|

|65 / 1882|[双EMA金叉死叉跟踪策略Dual-EMA-Crossover-Strategy](cards/47cf1b6bcb93.html)|恢复可关闭的日期过滤。；退出不依赖入场日期窗。|

|66 / 2199|[双移动均线追踪止损策略Dual-Moving-Average-Tracking-Stop-Loss-Strategy](cards/326f85412de3.html)|时间函数恒真。；状态维护和退出需跨窗继续。|

|74 / 2868|[基于RSI的多头趋势追踪策略RSI-Trend-Tracking-Long-Only-Strategy](cards/be184f47a263.html)|保护单独立于入场信号，在有效持仓均价存在时每根维护。|

|77 / 1990|[双均线交叉RSI动量策略与风险收益优化系统-Dual-Moving-Average-Cross-RSI-Momentum-Strategy-with-Risk-Reward-Optimization-System](cards/a9092b7f70e2.html)|空头目标减去负价差导致目标在入场价上方。|

|91 / 4393|[宽带震荡锁定策略Bollinger-Bands-Consolidation-Strategy](cards/3f21fc821df9.html)|日期输入未生效。；窗外已有持仓不能重置跟踪线。；窗外仍处理持仓退出。；窗外不能继续入场加仓。|

|93 / 2849|[基于RSI指标的双轨突破策略RSI-Dual-track-Breakthrough-Strategy](cards/bcf6975d1373.html)|开始日期输入未用于入场。|

|100 / 1738|[动量指标均线交叉策略Momentum-Indicator-Crossover-Strategy](cards/00f4a02ae980.html)|日期函数恒真绕过开始日期。|

|102 / 2213|[双移动平均线反转策略Dual-Moving-Average-Reversal-Strategy](cards/812e7da5a676.html)|恢复仅入口日期。|

|103 / 4671|[收缩带Bollinger与RSI组合策略Bollinger-Bands-and-RSI-Combination-Strategy](cards/fb7f387aa500.html)|恢复可选截止日期。；窗外持仓继续单向跟踪。；允许持仓窗外执行原退出块。；入口仍严格窗内。|

|106 / 71|[ATR增强型蜡烛反转模式识别与风险管理策略-ATR-Enhanced-Candlestick-Reversal-Pattern-Recognition-and-Risk-Management-Strategy](cards/48c0f5288549.html)|多空退出使用同一exit ID，短侧独立命名以避免同根更新覆盖其他方向退出订单。|

|108 / 2497|[均线反弹吸筹策略Moving-Average-Rebound-Strategy](cards/7306957acd9c.html)|正价格不可能小于自身95%，止损永不触发。|

|110 / 5503|[连续K线反转突破策略Consecutive-Candlestick-Reversal-Breakout-Strategy](cards/4c8d3743f082.html)|恢复日期入场。；窗外原保护退出仍生效。|

|125 / 5084|[移动平均聚合动量云策略-Moving-Average-Convergence-Momentum-Cloud-Strategy](cards/e76d4cf22414.html)|修复展示返回值。|

|126 / 2324|[双重确认的优势均线策略A-Dual-Moving-Average-Confirmation-Advantage-Line-Strategy](cards/b94c77d91d7f.html)|日期恒真绕过输入。；退出必须在日期窗外继续。|

|127 / 1776|[动量突破旗形模式交易策略基于量价确认的日内高频交易系统-Momentum-Breakout-Flag-Pattern-Trading-Strategy-Volume-Price-Confirmed-Intraday-High-Frequency-Trading-System](cards/a14fc77831b6.html)|strategy.close首参必须是入场ID，现与实际入场不匹配。；strategy.close首参必须是入场ID，现与实际入场不匹配。；旗形在本块因回撤或超时失效后，入场须重新确认inFlag，不能继续突破下单。|

|130 / 2209|[双移动平均线交叉MACD趋势跟踪策略Dual-Moving-Average-Crossover-MACD-Trend-Following-Strategy](cards/63539726a65b.html)|恢复日期函数。；接入入口日期门禁。；接入入口日期门禁。；接入入口日期门禁。；接入入口日期门禁。；双向窗外保留反向平空。；双向窗外保留反向平多。|

|131 / 3422|[基于支持位和趋势EMA的多空策略-Support-Level-and-Trend-EMA-Based-Long-Strategy](cards/2c11252bcd5b.html)|第一档50%无止损却预留仓位，第二档止损只能保护剩余部分；给首档补同一止损。|

|135 / 4563|[开盘驱动策略Open-Drive-Strategy](cards/fc7336fda61a.html)|多空共用exit ID，分开命名避免相互修改；限价定时退出和未使用bs/ss保护仍需设计确认。|

|137 / 799|[RSI均线交叉趋势策略RSI-Moving-Average-Crossover-Trend-Strategy](cards/4414ec4b27e7.html)|恢复日期窗。；退出移出日期入场门禁。|

|141 / 2597|[基于ATR和突破的ETF交易策略An-ATR-and-Breakout-based-ETF-Trading-Strategy](cards/4a273ddd3263.html)|多头枚举遗漏count-3，导致该层未被跟踪退出；连续信号计数也可能超过已成交编号，后者需进一步设计。|

|143 / 2168|[双时间轴波动率价差交易策略Dual-Timeframe-Volatility-Spread-Trading-Strategy](cards/a9f40db0eff2.html)|恢复入场窗口。|

|145 / 3115|[基于历史新高突破的买入策略Buying-Strategy-Based-on-Historical-High-Breakout](cards/16deb91b6b45.html)|让既定默认90合法。|

|146 / 2162|[双时间尺度动量策略-Dual-Timeframe-Momentum-Strategy](cards/7f438a53c539.html)|反向失效时取消未成交同ID入口。|

|153 / 4851|[海龟交易三日反转策略Turtle-Trading-3-Day-Reversion-Strategy](cards/d7ed73a9b021.html)|恢复日期及原窗外强平。|

|163 / 2687|[基于EMA指标的趋势跟踪策略EMA-Crossover-Trend-Following-Strategy](cards/99b8a5ba4496.html)|恢复时间输入。；解除平仓的日期限制。|

|172 / 1977|[双均线RSI动量突破交易策略-Dual-EMA-RSI-Momentum-Breakout-Trading-Strategy](cards/aa09afaab47f.html)|入场分支把刚记录的止损设为na，持仓保护分支不执行；删除这次清空。|

|176 / 3250|[基于均量线和波动率的趋势追踪策略Trend-Following-Strategy-Based-on-Volume-weighted-Average-Price-and-Volatility](cards/9e6bddfe7f9c.html)|起止日期没有生效；仅恢复入场日期过滤。|

|179 / 3675|[基于量化统计的双标准差动态VWAP震荡突破交易策略-Statistical-Dual-Standard-Deviation-VWAP-Breakout-Trading-Strategy](cards/541a3e0149e7.html)|历史bar全部使用timenow使间隔不随历史行情前进；应使用当前K线time。|

|181 / 379|[G-Channel-Trend-Detection-Strategy-G-Channel趋势检测策略](cards/a5149ca03296.html)|多空保护使用不同ID，避免同ID修改。|

|185 / 2075|[双均线止盈止损趋势交易策略-Dual-Moving-Average-Trend-Trading-Strategy-with-Stop-Loss-and-Take-Profit](cards/02bfc6b39fae.html)|持仓期间持续提交均价保护。|

|186 / 4127|[多空均衡移动平均趋势跟随策略Multi-factor-Moving-Average-Trend-Following-Strategy](cards/4e83b578222c.html)|窗口函数恒真。；保持窗外持仓退出。；只允许窗口内新入场。|

|187 / 3552|[基于移动平均线均回复策略Based-on-the-Moving-Average-Reversion-Strategy](cards/271b0abd9b0e.html)|版本注解格式错误。|

|188 / 2|[10EMA双重交叉趋势追踪策略10EMA-Double-Cross-Trend-Tracking-Strategy](cards/48ce0df7ec53.html)|空头风险距离第二比较使用反向差值，距离大于10.40仍通过。；多空退出使用同一exit ID，短侧独立命名以避免同根更新覆盖其他方向退出订单。|

|189 / 2013|[双均线交叉开仓策略-Dual-Moving-Average-Crossover-Entry-Strategy](cards/e166edd1228c.html)|低于均线时open-ma5为负，不可能大于正阈值。|

|190 / 3379|[基于布林通道和RSI指标的渐进DCA策略Bollinger-Band-and-RSI-Mixing-with-DCA-Strategy](cards/46e19036171f.html)|恢复主仓和追加仓入场时间。；主仓退出不随入场窗口失效。；百分比转价格差再转tick，保留原百分比及动态均价锚点。；最大层限制应为小于而非不等于，避免超限继续加。|

|205 / 3460|[基于月季线均线操作的量化交易策略Quant-Trading-Strategy-Based-on-Monthly-and-Quarterly-Moving-Average-Operation](cards/ad68ab433719.html)|开始日期被if true绕过，直接门控入场且退出保持不变。|

|206 / 5078|[移动平均线金叉交易策略Moving-Average-Crossover-Trading-Strategy](cards/ebfefa24d53a.html)|日期条件恒真。；信号退出不受日期门禁。|

|208 / 5791|[黄金交叉策略Golden-Cross-Strategy](cards/9a86cb046a87.html)|恢复入场日期。；死叉退出移出日期。|

|212 / 3210|[基于均线交叉的长线追涨策略SMA-Crossover-Bullish-Trend-Following-Strategy](cards/01812a28b204.html)|初始金叉时均价为na，成交后若无新金叉便没有退出订单。|

|214 / 4271|[多重指标动量突破趋势交易策略-Multi-Indicator-Momentum-Breakout-Trend-Trading-Strategy](cards/96b3f74d3951.html)|绝对价格传入tick距离参数loss/profit，退出价格失真。；绝对价格传入tick距离参数loss/profit，退出价格失真。；多空退出使用同一exit ID，短侧独立命名以避免同根更新覆盖其他方向退出订单。|

|217 / 5236|[自适应布林通道动态仓位管理策略-Adaptive-Bollinger-Bands-Dynamic-Position-Management-Strategy](cards/21937e06ebd4.html)|time变化为毫秒差，不可能正常等于1，小时分支失效；改为非零变化，只修边界检测不声称持续一小时。|

|225 / 5171|[经典移动平均线交叉策略Moving-Average-Crossover-Strategy](cards/6b274e0d6b7e.html)|恢复日期入口。；退出移出日期。|

|226 / 3594|[基于脉冲MACD和双均线交叉的多时间尺度趋势追踪策略-Multi-timeframe-Trend-Tracking-Strategy-Based-on-Impulse-MACD-and-Dual-Moving-Average-Crossover](cards/d5c67fe3a4a6.html)|孤立缩进块缺失函数定义且引用未定义len，SMA实际调用内置ta.sma。|

|229 / 3553|[基于移动平均线的动量策略This-strategy-is-a-momentum-strategy-based-on-moving-average-lines](cards/2de06f53b9b6.html)|日期函数恒真绕过输入。；卖信号用于平多时不能受日期窗口影响。；仅反手空入场需要窗口，窗外仍平多。|

|231 / 2529|[均线震荡突破HODL策略Moving-Average-Oscillation-HODL-Strategy](cards/ffd9f19cf1f3.html)|恢复日期。；保留窗外退出。|

|233 / 4224|[多重均线黄金交叉分批止盈策略-Multi-EMA-Golden-Cross-Strategy-with-Tiered-Take-Profit](cards/26c2428a4c8d.html)|Buy1未覆盖stop_loss条件，只有Buy2有止损；给Buy1增加同一止损触发，保留份额与默认加仓配置。|

|234 / 3755|[多周期EMA交叉量化交易策略Multi-Period-EMA-Crossover-Quantitative-Trading-Strategy](cards/7099010b6332.html)|日期函数恒真使用户范围及窗外平仓无效；恢复用户日期即可，已有窗外平仓分支。|

|254 / 2526|[均线金叉死叉策略-Moving-Average-Crossover-Strategy](cards/6b8c9f45435d.html)|修正空头价格方向和ID。|

|258 / 4001|[多指标趋势跟踪期权交易EMA交叉策略-Multi-Indicator-Trend-Following-Options-Trading-EMA-Cross-Strategy](cards/b969cfc64d26.html)|空头目标也向上5%，会立即满足退出，修为按持仓方向计算。；使用真实空仓判断多头入场，防止伪状态复位后持仓中重写锚价。；使用真实空仓判断空头入场，避免状态尾部清零造成持仓误入场。；真实持仓期间启用止盈检查，不依赖发单当根被清零的布尔状态。|

|259 / 2764|[基于MACD的复合量化交易策略Compound-Quantitative-Trading-Strategy-Based-on-MACD](cards/5f35344289e2.html)|恢复用户起止时间。；死叉平仓窗外仍生效。|

|261 / 2611|[基于ATR的均值回复策略Mean-Reversion-Strategy-Based-on-ATR](cards/88b174294f89.html)|开始时间被恒真绕过；恢复开始时间限定，止损分支在持仓时仍独立。|

|267 / 3103|[基于动量顺势策略Momentum-Trend-Following-Strategy](cards/0bb9b9971857.html)|开始日期输入被常量true绕过。；退出不应受日期门控。；退出不应受日期门控。|

|268 / 3704|[基于风险回报比和技术分析的牛旗突破策略-Risk-Reward-Ratio-and-Technical-Analysis-Based-Bull-Flag-Breakout-Strategy](cards/567468cb4961.html)|将同仓位止盈止损合为一组保护。|

|270 / 1434|[动态K线大阳线交易策略Dynamic-Candlestick-Big-Yang-Line-Trading-Strategy](cards/e5facb8db184.html)|移除信号分支na均价保护。；保护单独立于入场信号，在有效持仓均价存在时每根维护。|

|272 / 3079|[基于动量交易策略Momentum-and-Volume-Trading-Strategy](cards/2bb70c837263.html)|百分比价差转换为tick并分离方向ID。；百分比价差转换为tick并分离方向ID。|

|275 / 3756|[多周期EMA交叉高胜率趋势跟踪策略进阶版-Multi-Timeframe-EMA-Cross-High-Win-Rate-Trend-Following-Strategy-Advanced](cards/bcd99caa81c2.html)|把后续连续三行均价赋值放在持仓分支。；仅对已成交持仓提交保护，防止空仓新入场沿用上一笔保留的价格。|

|276 / 5519|[追踪趋势获利策略Take-Profit-on-Trend-Strategy](cards/5d1575b51739.html)|日期输入失效；只恢复入场时间过滤，退出独立。|

|277 / 5753|[高级量化趋势追踪与云图反转复合交易策略-Advanced-Quantitative-Trend-Following-and-Cloud-Reversal-Composite-Trading-Strategy](cards/2c1b99697677.html)|拆分空头保护ID，保持原动态价格公式。|

|278 / 5678|[顿希安通道突破策略Donchian-Channel-Breakout-Strategy](cards/3d1103f22fd6.html)|结束时间错误引用起始年月日。；日期函数恒真。；日期函数未接入场。|

|279 / 3549|[基于移动平均线和相对强弱指标的动量反转策略Momentum-Reversal-Strategy](cards/8ea92f9916b4.html)|平仓错误引用退出ID而非Buy入场ID；另takeProfit与quantityRemainder每根重置且profit单位tick，需设计分批状态。|

|281 / 4134|[多策略自适应趋势跟踪与突破交易系统-Multi-Strategy-Adaptive-Trend-Following-and-Breakout-Trading-System](cards/2c08e80d68e1.html)|均价退出仅在信号分支导致首次na且无新信号不保护；无from_entry还跨模型占用仓位。；仅对应方向实仓时持续提交，不依赖入场信号重现。；均价退出仅在信号分支导致首次na且无新信号不保护；无from_entry还跨模型占用仓位。；仅对应方向实仓时持续提交，不依赖入场信号重现。；均价退出仅在信号分支导致首次na且无新信号不保护；无from_entry还跨模型占用仓位。；仅对应方向实仓时持续提交，不依赖入场信号重现。；均价退出仅在信号分支导致首次na且无新信号不保护；无from_entry还跨模型占用仓位。；仅对应方向实仓时持续提交，不依赖入场信号重现。|

|284 / 3984|[多指标趋势动量ATR目标价交易策略-Multi-Indicator-Trend-Momentum-ATR-Target-Trading-Strategy](cards/9a6f7abdc541.html)|修正标准返回值对应关系。|

|292 / 3172|[基于双移动平均线交叉的回调入场策略EintSimple-Pullback-Strategy](cards/21b4c90411d4.html)|恢复入场时间窗。|

|296 / 2196|[双移动均线趋势跟踪交易系统结合风险收益比优化策略-Dual-Moving-Average-Trend-Following-Trading-System-with-Risk-Reward-Ratio-Optimization-Strategy](cards/7f7ef78245b5.html)|保护单独立于入场信号，在有效持仓均价存在时每根维护。|

|297 / 2105|[双均线趋势跟踪策略与RSI过滤器-Dual-Moving-Average-Trend-Following-Strategy-with-RSI-Filter](cards/0ccf02320146.html)|先清理空仓旧锚价，再记录本次入场信号收盘价，防止新记录立即被空仓复位抹掉。；删除发单同根的尾部再次清零，保留刚记录的新信号价格。|

|298 / 5391|[趋势突破交易系统移动平均线突破策略-Trend-Breakout-Trading-System-with-Moving-Average-TBMA-Strategy](cards/f95b65084864.html)|全仓目标先预留仓位，后止损没有可用数量。；以止损而非入价加2倍风险，实际只有1R。|

|303 / 1644|[动态达瓦斯箱体突破与均线趋势确认交易系统-Dynamic-Darvas-Box-Breakout-with-Moving-Average-Trend-Confirmation-Trading-System](cards/339219da52fb.html)|保证三个highest窗口均为正。|

|304 / 5796|[黄金分割移动平均线交易策略Golden-Ratio-Moving-Average-Trading-Strategy](cards/fe3bde644581.html)|恢复仅入口日期。|

|306 / 235|[Darvas-Box-Breakout-and-Risk-Management-Strategy-Darvas-盒子突破与风险管理策略](cards/7bd7c06785d9.html)|boxp允许1或2使boxp-2非正，highest长度无效；最小合法长度应为3。|

|310 / 4707|[日内锤子反转形态多头策略Intraday-Hammer-Reversal-Pattern-Long-Strategy](cards/5a6725d76968.html)|对阴锤子使用实体底部到低点距离。|

|311 / 4500|[布林带结合超级趋势的智能波动区间交易策略-Intelligent-Volatility-Range-Trading-Strategy-Combining-Bollinger-Bands-and-SuperTrend](cards/6deabcb408ef.html)|按中轨上轨下轨解构。|

|312 / 5335|[超级趋势反转策略Super-Trend-Reverse-Strategy](cards/ba41cdf1648b.html)|TrendDown重置错误使用下方UP而非上方DOWN。；平多不应被日期窗阻断。|

|316 / 2680|[基于EMA平均线交叉的趋势追踪策略Trend-Following-Strategy-Based-on-EMA-Crossover](cards/008ca5a0bd81.html)|日期恒真绕过输入。；平仓不能受日期门禁。|

|327 / 4877|[渔夫指标移动止损策略Fisher-Yurik-Trailing-Stop-Strategy](cards/c5544c33f3ce.html)|日期输入恒真失效；恢复入场时间窗，退出独立。|

|331 / 2188|[双移动均线交叉反转策略Dual-Moving-Average-Reversal-Strategy](cards/64941c33a4a8.html)|恢复限价入场日期范围。；窗外撤销未成交限价买单，已有持仓仍可按xsell退出。|

|336 / 3634|[基于趋势确认的多重指标动态止损策略-Trend-Confirmation-Multi-Indicator-Dynamic-Stop-Loss-Strategy](cards/8f958fc7b956.html)|对齐延迟事件与摆动低点历史索引。|

|337 / 496|[MA-SMA-MA-Slope-Trailing-Stop-Loss-Re-Entry-均线简单移动平均线均线斜率追踪止损重新进场](cards/d90e2f2e2bfb.html)|每根K线重复检测上一次历史平仓会覆盖已复位的止损标记；仅在新平仓产生时检测。|

|338 / 5607|[金叉死叉长线多因子策略Golden-Cross-Death-Cross-Long-term-Multi-factor-Strategy](cards/20e73fb43a48.html)|合并同仓止盈止损。|

|341 / 3848|[多均线交叉趋势跟踪RSI波动策略-Multi-Moving-Average-Cross-Trend-Following-RSI-Oscillation-Strategy](cards/0e4e17ba6338.html)|先提交全仓限价退出会预留全部数量，独立止损无可用仓位。|

|342 / 1023|[Trend-Following-with-Breakout-and-Frequency-Filter-Long-Only-基于突破和频率过滤的趋势跟踪策略只做多](cards/2b6b4c1644e2.html)|使用bar_index保存最近入场信号K线索引，消除毫秒与根数混算。；入场间隔按K线根数。；记录索引而非毫秒时间戳。；趋势退出持有门槛按K线根数。|

|348 / 1688|[动量反转短线交易策略-Momentum-Reversal-Trading-Strategy](cards/f19bad41da52.html)|恢复仅入场日期窗。|

|350 / 3251|[基于复合突破策略The-Compound-Breakout-Strategy](cards/cdc6f46f3a17.html)|日期函数恒真。；持仓退出跨窗口继续，入场仅窗口内。；窗外不得再次入场。|

|353 / 1187|[三指数均线止盈止损策略Triple-Exponential-Moving-Average-Profit-Taking-and-Stop-Loss-Strategy](cards/a70e49f27418.html)|使日期输入生效；退出不受日期门禁限制|

|355 / 2178|[双波带突破策略Double-Bollinger-Bands-Breakout-Strategy](cards/ce43f33d5e13.html)|日期参数未参与入场。；窗外持仓不可重置跟踪线。；原日期包住退出，恢复门禁必须只门控入场。|

|356 / 1223|[三重均线趋势追踪多指标组合量化交易策略-Triple-EMA-Trend-Following-Multi-Indicator-Quantitative-Trading-Strategy](cards/c14168333c6d.html)|ta.dmi依次返回+DI、-DI、ADX，现把+DI当ADX门槛。|

|357 / 2185|[双移动均线与RSI反转交易策略Dual-Moving-Average-and-RSI-Reversal-Trading-Strategy](cards/f8944ae554c1.html)|v4使用命名空间颜色。；v4颜色命名空间和布尔绘图类型修复，将long显式映射为1/0，仅改变展示类型。；v4颜色命名空间和布尔绘图类型修复，将short显式映射为1/0，仅改变展示类型。；移除变量声明尾随逗号，避免等待另一条声明。|

|358 / 1861|[双7日突破策略Double-7-Days-Breakout-Strategy](cards/7bfe4c1aa59c.html)|恢复已有起止日期计算。；把退出移到日期入场门槛之外。|

|359 / 146|[Bollinger-Bands-Mean-Reversion-Trading-Strategy-with-Dynamic-Support-布林带均值回归交易策略与动态支撑](cards/e557875c8bbe.html)|持仓期间重复信号虽不能新增持仓，仍覆盖entryDay并错误重启当天退出限制。|

|361 / 4197|[多重均线交叉动量趋势跟踪策略-Multi-EMA-Crossover-Momentum-Trend-Following-Strategy](cards/4e7ed2180278.html)|多空退出复用同一ID，拆分空头退出ID避免修改已有多单保护。|

|370 / 1494|[动态均值回归与动量策略-Dynamic-Mean-Reversion-and-Momentum-Strategy](cards/875780d5cf2b.html)|多空共享同一exit ID，后调用可能修改前调用订单身份；应为Short单独命名。|

|376 / 65|[ATR动态趋势跟踪与重入场交易策略-ATR-Dynamic-Trend-Following-with-Re-entry-Trading-Strategy](cards/a6990d119a2b.html)|保护单可能盘中成交但收盘回到区间，inTrade不会复位，后续多头信号被永久阻塞。按已平仓交易计数同步复位。|

|378 / 1994|[双均线交叉与随机指标结合的自适应追踪止损策略-Dual-Moving-Average-Crossover-with-Stochastic-Filter-and-Adaptive-Trailing-Stop-Strategy](cards/cecdd28451f4.html)|只在对应方向已有实际持仓时持续提交均价保护，避免反向待成交订单使用旧方向均价。；只在对应方向已有实际持仓时持续提交均价保护，避免反向待成交订单使用旧方向均价。|

|379 / 3295|[基于多重技术指标的高频交易动态优化策略-Multi-Technical-Indicator-Based-High-Frequency-Dynamic-Optimization-Strategy](cards/67e97551bff6.html)|DMI返回顺序为+DI、-DI、ADX。|

|384 / 834|[RSI趋势动量交易策略结合双均线和成交量确认-RSI-Trend-Momentum-Trading-Strategy-with-Dual-MA-and-Volume-Confirmation](cards/8e7fbde9affd.html)|拒绝零长度。|

|385 / 3425|[基于支撑位和阻力位的技术分析交易策略-Trading-Strategy-Based-on-Support-and-Resistance-Levels-Using-Technical-Analysis](cards/66d766d430c0.html)|函数返回先高枢轴再低枢轴，支撑阻力接收顺序倒置。|

|387 / 1907|[双RSI指标突破策略Dual-RSI-Indicator-Breakout-Strategy](cards/cab2e73ee038.html)|两个独立持仓用同一止损ID，存在后调用修改前调用的身份冲突；慢RSI使用独立ID。|

|391 / 1620|[动态趋势线突破反转交易策略-Dynamic-Trendline-Breakout-Reversal-Trading-Strategy](cards/c353ad7e1d49.html)|反向入场ID为Long Reverse/Short Reverse，原exit只匹配Long/Short，反向仓位失去括号保护；统一入场ID。；反向空仓沿用Short入场ID以匹配ShortExit。|

|394 / 4215|[多重均线趋势跟踪与动态止损策略-Multi-EMA-Trend-Following-Strategy-with-Dynamic-Stop-Loss](cards/a542386b8b45.html)|未偏移日线表达式配lookahead_on将日末值提前注入历史日内。；未偏移日线表达式配lookahead_on将日末值提前注入历史日内。；未偏移日线表达式配lookahead_on将日末值提前注入历史日内。|

|396 / 325|[EMA反向买卖策略EMA-Reverse-Buy-Sell-Strategy](cards/7da0b5b6f337.html)|多空共用同一exit ID可能互相修改退出订单，短侧必须独立命名。|

|408 / 1959|[双周期ATR波动率突破股票趋势策略Volatility-Bands-and-VWAP-Multi-Timeframe-Stock-Trend-Trading-Strategy](cards/963ff671d194.html)|恢复日期。；退出移出门禁，接回已声明撤单条件。|

|411 / 2421|[唐奇安通道趋势跟踪策略Donchian-Channel-Trend-Tracking-Strategy](cards/e64c5838b63b.html)|恢复日期窗。；保留窗口内入场同时提交保护；窗口外撤入场挂单并持续更新持仓保护。|

|415 / 2099|[双均线趋势跟踪与ATR风控自适应交易策略-Dual-Moving-Average-Trend-Following-Strategy-with-ATR-Based-Risk-Management-System](cards/ce0ff62415a1.html)|模式1空仓检测不读取不存在的交易索引。；模式2同样修复不存在交易的空仓判断。；分批目标预留份额也必须受相同止损保护。|

|423 / 3418|[基于拉里康诺斯的经典策略Oscillation-Breakthrough-Strategy](cards/10b5e5861d87.html)|日期函数恒真。；均价止损只在信号内设置可能一直na，且恢复日期需不阻断退出。|

|429 / 1474|[动态供需区间中线反转策略-Dynamic-Supply-Demand-Zone-Midline-Reversal-Strategy](cards/87ccd66dba9c.html)|合并Long全仓止盈止损，防止退出预留份额冲突。；合并Short全仓止盈止损，防止退出预留份额冲突。|

|430 / 4221|[多重均线趋势追踪与风控优化量化交易策略-Multi-Moving-Average-Trend-Following-and-Risk-Management-Quantitative-Trading-Strategy](cards/53fcc8c7eb0e.html)|trail_points和trail_offset以tick计，ATR为价格距离须除最小跳动。|

|439 / 1221|[三重均线动量趋势交易策略-Triple-Moving-Average-Momentum-Trend-Trading-Strategy](cards/f37249ddf235.html)|移除入场当根均价na的无效保护调用。；保护单独立于入场信号，在有效持仓均价存在时每根维护。|

|440 / 1496|[动态均线与布林带交叉策略结合固定止损优化模型-Dynamic-Moving-Average-and-Bollinger-Bands-Cross-Strategy-with-Fixed-Stop-Loss-Optimization-Model](cards/0ff09f1096f7.html)|持多时更新有效均价止损。；持空时更新有效均价止损。|

|444 / 4815|[波动率动量突破交易策略结合趋势和动量过滤-Volatility-Momentum-Breakout-Strategy-with-Trend-and-Momentum-Filters](cards/4f5f2aeb93ea.html)|反手没有空仓根时旧同方向入价未清空，下一轮反手复用旧价；用当前真实均价持续同步。；反手没有空仓根时旧同方向入价未清空，下一轮反手复用旧价；用当前真实均价持续同步。|

|445 / 4868|[混沌交易规则止损策略Chaotic-Trading-Rules-Stop-Loss-Strategy](cards/16eeb24adb53.html)|日期函数恒真。；恢复窗口时退出需继续处理已有持仓。；窗口外不得反手入场。；窗口外不得反手入场。；价格和方向时间锚点仅在允许入场的窗口信号更新，避免窗外无新仓却重写存量仓位保护基准。；价格和方向时间锚点仅在允许入场的窗口信号更新，避免窗外无新仓却重写存量仓位保护基准。；价格和方向时间锚点仅在允许入场的窗口信号更新，避免窗外无新仓却重写存量仓位保护基准。；价格和方向时间锚点仅在允许入场的窗口信号更新，避免窗外无新仓却重写存量仓位保护基准。|

|448 / 977|[Swing-Highs-Lows-Candle-Patterns](cards/20f66db952db.html)|study声明与strategy.entry并存不能作为有效策略编译；替换策略声明。|

|451 / 804|[RSI多区间交易策略-Multi-Zone-RSI-Trading-Strategy](cards/dae395cfdca1.html)|同一分档的止盈止损合为一组，防止全量止盈预留阻塞止损。；同一分档的止盈止损合为一组，防止全量止盈预留阻塞止损。；同一分档的止盈止损合为一组，防止全量止盈预留阻塞止损。；同一分档的止盈止损合为一组，防止全量止盈预留阻塞止损。|

|453 / 5218|[自适应价格交叉均线交易策略-Adaptive-Price-Crossing-Moving-Average-Trading-Strategy](cards/dad03d9df088.html)|手工方向标志只在空仓重置，连续反手可同时为true并屏蔽后续方向。；以真实持仓方向替代残留标志。|

|454 / 3713|[基于高斯通道和随机RSI的市场趋势捕捉策略-Gaussian-Channel-and-Stochastic-RSI-Based-Market-Trend-Capture-Strategy](cards/65f8f252b249.html)|恢复日期。；退出脱离窗口。|

|455 / 3740|[多个EMA周期动态交易策略Multi-Timeframe-Dynamic-EMA-Trading-Strategy](cards/5fc844f39d65.html)|恢复日期。|

|458 / 2251|[双轨跟踪震荡分型策略Dual-track-Oscillator-Pattern-Strategy](cards/facb33f439aa.html)|日期函数恒真。；平仓不应被日期阻断。|

|459 / 4332|[多重趋势交叉策略Multi-Trend-Crossover-Strategy](cards/6e22a5f357e4.html)|版本注解格式错误。；日期范围常量true使输入与窗外平仓失效。；信号退出不受日期限制。；信号退出不受日期限制。；慢速VMA极值回看错误使用快周期。；慢速VMA极值回看错误使用快周期。|

|461 / 3387|[基于平均真实波幅的趋势跟踪策略ATR-Based-Trend-Tracking-Strategy](cards/cfcc8d8350a1.html)|恢复日期。；退出脱离日期门禁。；退出脱离日期门禁。；入场窗失效或趋势反向撤销未成交限价单。|

|463 / 4534|[平滑海坚线买卖策略Heikin-Ashi-Smoothed-Buy-and-Sell-Strategy](cards/00702b798dcb.html)|HA低点应包含开收较小值，max可令低点高于开或收。|

|464 / 5613|[长期趋势SMA均线交叉量化策略-Long-term-Trend-SMA-Crossover-Quantitative-Strategy](cards/9af2b3db1523.html)|日期过滤开关和起止输入被恒真绕过。；退出不能受日期门禁。|

|465 / 3121|[基于双EMA交叉的量化交易策略Quantitative-Trading-Strategy-Based-on-Double-EMA-Crossover](cards/888b5fc2d522.html)|启用开始时间开关。；只将时间门槛保留在entry，退出独立。|

|467 / 3583|[基于线性回归分析和均线指标的短线交易策略Linear-Regression-Channel-Strategy](cards/f406ae09bba5.html)|日期输入失效；入场恢复起止范围，退出已独立。|

|468 / 5343|[超级趋势策略SuperTrend-Strategy](cards/62ca8ecd6b78.html)|恢复源码中已存在的策略声明，不更改其参数。；恢复日期窗口与原窗外close_all。；只多模式反信号平仓不受日期限制。|

|469 / 1506|[动态均线网格交易策略Grid-Strategy-with-Moving-Average-Lines](cards/cf5a70f0d348.html)|修复第15格入退ID配对；使用ATR长度参数|

|470 / 3526|[基于真实波幅的加权移动平均跨期策略True-Range-Based-Weighted-Moving-Average-Cross-Period-Strategy](cards/e03e16b81471.html)|日期失效且声明无pyramiding，第二至五层加仓不可达；日期可修但加仓需确认杠杆。|

|472 / 1915|[双TEMA叉死叉交易策略Dual-TEMA-Crossover-Trading-Strategy](cards/740285e0f0f4.html)|恢复入场日期。|

|473 / 5062|[移动平均线回抽策略Snap-Back-Moving-Average-Counter-trend-Strategy](cards/3f86549d6b08.html)|恢复源码中已存在的策略声明，不更改其参数。；恢复用户设定的交易窗口。；所有持仓保护脱离日期入场窗口。|

|475 / 1168|[三倍标准差布林带突破量化交易策略结合百日均线优化-Triple-Standard-Deviation-Bollinger-Bands-Breakout-Strategy-with-100-Day-Moving-Average-Optimization](cards/d314eafdf5c7.html)|版本指令含空格无法按标准注解声明v6。|

|480 / 1343|[低价买入-高价止盈策略Low-High-Trend-Strategy](cards/41e1a35e9580.html)|日期输入失效；恢复时间范围并解除普通退出对日期范围的限制，保留窗外close_all行为。；普通利润退出不得依赖日期窗口。；高点下穿退出保留窗外执行。|

|482 / 3599|[基于自适应移动平均线的趋势跟踪策略Trend-Following-Strategy-Based-on-Adaptive-Moving-Average](cards/055045ca7d7d.html)|版本注解格式错误。|

|484 / 2501|[均线回转反转策略Mean-Reversion-Reverse-Strategy-Based-on-Moving-Average](cards/e5113536e9b4.html)|恢复入场日期。；退出移出日期限制。；退出移出日期限制。|

|486 / 983|[TAM日内RSI交易策略TAM-Intraday-RSI-Trading-Strategy](cards/4b1f1925230c.html)|日期过滤开关和开始时间无效；恢复入场时间过滤并保持退出窗外有效。；日期只能限制入场，退出不依赖日期。|

|490 / 2094|[双均线趋势交叉量化交易策略研究与优化-Dual-Moving-Average-Trend-Crossover-Quantitative-Trading-Strategy-Analysis-and-Optimization](cards/37f7a0ea56a3.html)|每根持仓K线计一笔，累计利润正负被误当单笔胜负。|

|491 / 4236|[多重技术指标协同交易策略系统-Multi-Technical-Indicator-Synergistic-Trading-System](cards/e1d951f1f02c.html)|BB返回中轨、上轨、下轨，前两项接反使图示及额外卖信号错误。|

|492 / 5583|[量化策略之MA强弱趋势追踪Quantitative-Strategy-of-MA-Strength-Trend-Tracking](cards/f8c111025ed5.html)|日期输入失效；恢复入场范围，独立平仓继续有效。|

|494 / 4622|[拓宽均线区间的马丁格尔止损炒股策略Martingale-Strategy-with-Expanded-Moving-Average-Range-for-Stock-Trading](cards/1c70e3a454e4.html)|恢复入口日期。；区分入场EMA1与止盈EMA1 TP；先撤窗外入场单，再提交持仓止盈与原期末平仓，避免撤单误取消止盈。|

|499 / 5605|[金叉死叉趋势追踪策略Golden-Dead-Cross-Trend-Tracking-Strategy](cards/e159be4c1b18.html)|恢复可关闭日期。；退出不受入场日期限制。|

## 审查证据

逐项摘要、原始行号及发现保存在audit/batch_1.json至batch_3.json；补丁独立复核保存在audit/review_1.json至review_3.json，最终批准记录在audit/patch_approvals.json。所有文件与原代码指纹一起校验。

## 验证边界

[本地验证记录](validation.md)。本次只做静态/局部行为核验，不部署、不执行策略、不接券商。推送门禁另按用户已有约定执行。
