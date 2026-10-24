# 策略表现与逻辑融合研究名单

[交互排名目录](index.html) · [CSV总表](ranking.csv) · [评分方法](methodology.md) · [排除记录](excluded.csv) · [输入指纹](source_manifest.json)

共 **500** 份详细卡片：**451** 份同口径日线主榜，**49** 份小股票池初筛补充候选。不是500个同等证据或已验证可实盘的策略。补充不占主榜名次；其分数只在初筛候选池内比较。

主榜中报告年化收益为正 423 份、非正 28 份。当前集合是相对研究排序，不保证每份都有正收益或经济优势。

所有入选策略已有规则、参数、表现与执行差异解读；其中 **31** 份完成本轮完整源码精读，**31** 份列出精读发现的重要疑点。其余是自动语义辅助，不冒充逐份源码审计。原先已有的复核继续保留。

## 主榜前20（必须同时阅读重要疑点）

|名次|策略|综合研究分|逻辑分|日线年化|Sharpe|最大回撤|本轮重要疑点|
|---:|---|---:|---:|---:|---:|---:|---|
|1|[多级移势均线交易策略Multi-level-Shift-Moving-Average-Trading-Strategy](cards/623db80e698a.html)|79.52|48.00|50.68%|2.78|-14.97%|限价成交疑点：三层qty/pyramiding及反向entry qty=0退出不被外部固定单位引擎忠实支持。；无硬止损；跨方向层级条件可能反手，单层默认100%权益名义敞口。；日线与1h绩效明显相反，日线Sharpe未超3不能排除填单假象。|
|2|[均值回归型连续K线反转交易策略-Mean-Reversion-Consecutive-Candle-Reversal-Trading-Strategy](cards/ff2ababe492f.html)|78.33|48.00|35.25%|1.14|-38.93%|默认200%权益逆势买入且无硬止损，外部固定单位回测不反映杠杆与保证金风险。；日期门禁恒true；实时逐tick及收盘成交与历史OHLC可能不一致。|
|3|[拉里威廉姆斯三周期动态均线交易策略-Larry-Williams-Three-Period-Dynamic-Moving-Average-Trading-Strategy](cards/3973c7947db0.html)|77.82|44.00|39.32%|1.14|-38.91%|日期门禁恒true；na(time_close)不构成正常交易日收盘强平。；没有硬止损，退出也需要连续三次同向收盘条件。|
|4|[N-Bars-Breakout-Strategy-N-Bars-突破策略](cards/4c8e539e9fcf.html)|76.55|48.00|23.14%|1.47|-18.73%|突破确认后挂信号K的open限价，不能回填该K已经发生的开盘或触价；存在限价填单保真疑点。；无挂单失效/取消管理，反向信号只close持仓不保证撤掉未成交买单。|
|5|[基于Vix修复线性回归的低点捕捉策略Vix-Fix-Linear-Regression-Bottom-Fishing-Strategy](cards/796b8b9f4242.html)|76.39|48.00|20.66%|1.04|-29.46%|默认止损仅在回归正值且上升的green状态生效，不是全天候ATR保护。；日期门禁恒true，KC参数未参与交易。|
|6|[基于动量指标的短期交易策略Short-term-Trading-Strategy-Based-on-Momentum-Indicator](cards/52a2f2cf7c44.html)|76.09|36.00|19.90%|1.03|-25.13%|Mass Index衡量波幅而非价格方向，27线不参与交易；无止损仅反手。|
|7|[白盒冰山策略Robot-White-Box-Iceberg-Strategy](cards/4a401c623419.html)|74.89|48.00|43.02%|2.35|-29.62%|限价、三层qty/pyramiding、持仓后冻结层级与qty=0反向退出均超出外部固定单位保真范围；Sharpe阈值不排除填单假象。；没有真实冰山隐藏量或盘口执行模型，也无硬止损。；开始日期失效，needtime恒true，结束时间仅末尾全平撤单。|
|8|[双项式动量突破反转策略Binomial-Momentum-Breakout-Reversal-Strategy](cards/1a02062fdf96.html)|74.88|44.00|16.46%|1.09|-26.55%|BullPower绝对价格阈值与两个子模块的持久状态不能简化为当前阈值信号；无硬止损。|
|9|[三均线交叉趋势跟踪策略结合RSI和成交量确认系统-Triple-EMA-Crossover-Trend-Following-Strategy-with-RSI-and-Volume-Confirmation-System](cards/b2709f45760a.html)|74.74|44.00|14.10%|1.06|-21.35%|止损和目标每根以当前low/close重算，止损可放宽，不是固定3R。；标题三均线实为两根EMA，RSI70/30输入未使用。|
|10|[动态阈值价格变化突破策略-Dynamic-Threshold-Price-Change-Breakout-Strategy](cards/96056a60c81a.html)|74.59|39.00|23.03%|1.14|-34.84%|所谓动态阈值实为固定10%；只平多不做空。；low触六根低点只发市价close，无止损挂单，手工状态未追踪成交。|
|11|[基于布林带和MACD的量化交易策略Trading-Strategy-Based-on-Bollinger-Bands-and-MACD](cards/93c4ed6e7b91.html)|74.09|44.00|19.22%|1.00|-25.53%|expected_rebound的or分支绕过布林下轨过滤。；追踪保护是close条件市价退出，不是盘中stop挂单；日期门禁恒true。|
|12|[动量突破策略Momentum-Breakout-Strategy](cards/5babe1e11c16.html)|72.92|48.00|24.89%|0.96|-36.39%|15美元风险仓位只计算未传entry；stop/profit输入未用于订单。；逐tick实时计算与历史OHLC不等价，追踪参数为tick单位。|
|13|[基于熊力量指标的量化交易策略Bear-Power-Strategy](cards/88851838289b.html)|72.82|31.00|18.59%|1.08|-29.68%|十字星分支中close>open的true侧不可达；指标不是常见low-EMA Bear Power。；绝对价格阈值10/1跨标的失真，无止损。|
|14|[多周期RSI超卖反转策略-Multi-Timeframe-RSI-Oversold-Reversal-Strategy](cards/79a39417ecce.html)|71.27|48.00|25.36%|1.10|-41.52%|stopLossHit未引用：1.4%止损仅计算，不执行。；add more入场ID没有匹配退出；qty=3与默认未开启加仓存在执行差异。；EMA只绘图，无多周期；锚价在每根超卖信号被覆盖。|
|15|[相对量价策略Relative-Volume-Price-Strategy](cards/d85890022015.html)|71.20|48.00|29.16%|0.84|-27.28%|low触追踪线仅发市价close，不能按stop价即时成交。；空仓尾部清零初始止损，同根可能同时发close与entry；时间门禁恒true。|
|16|[关键反转信号回测策略Key-Reversal-Backtest-Strategy](cards/77e011e75ccd.html)|70.84|44.00|22.15%|1.04|-37.74%|止盈止损只在订单之后清状态，通常下一根才平仓；新信号可覆盖退出。；源码仅做多，pip参数实际是绝对价差。|
|17|[双超趋势策略Dual-SuperTrend-Strategy](cards/90effa222c51.html)|70.79|36.00|23.27%|1.08|-38.99%|所谓双超趋势实际单套自定义ATR通道；多空状态可同时true，多头分支优先。；无硬止损，轨线不是保护挂单。|
|18|[RSI50_EMA长仓策略-RSI50_EMA-Long-Only-Strategy](cards/97d16dd4e91c.html)|70.56|48.00|19.69%|1.05|-36.27%|strategy.close("RSICLose")无匹配入场ID，RSI订单缺失有效退出。；主Buy入场不要求RSI过滤；100%权益仓位不是百分比止损。|
|19|[三内下反转策略Three-Inside-Down-Reversal-Strategy](cards/0164824bb810.html)|70.29|39.00|24.61%|1.05|-40.19%|看跌三内下形态实际开Long，不能按名称解释为做空。；40/20触价只在订单之后清状态，退出延迟且新信号可覆盖。|
|20|[多指标交叉动量趋势跟踪策略基于Supertrend与ADX双重确认的量化交易系统-Multi-Indicator-Momentum-Trend-Following-Strategy-Quantitative-Trading-System-Based-on-Supertrend-and-ADX-Dual-Confirmation](cards/3584e3b6e286.html)|70.28|44.00|16.45%|1.02|-27.10%|只有Supertrend反向才平仓，ADX或RSI过滤失效不退出；图线不是止损挂单。；注释称变绿退出，但源码方向1为红色，必须以实际方向语义为准。|

## 为什么不沿用原综合榜

合并了原初筛后全市场结果与552日线重跑，扩大同口径覆盖；同时查原始运行错误数、固定代表去重并隔离已保存异常标记。旧榜把缺失日内结果补50的做法未沿用。

主分为70%日线表现、10%历史末3年分段、20%已有逻辑分，再减明确静态风险扣分。旧合理性分含绩效，不重复混入。日内结果因四周期完整榜缺失只作交叉证据。

## 数据漏斗

```json
{
  "input_screen_50stocks": 4762,
  "eligible_before_dedup_screen_50stocks": 3187,
  "input_full_universe": 526,
  "eligible_before_dedup_full_universe": 465,
  "ranked_full_universe": 451,
  "ranked_screen_50stocks": 2992
}
```

## 全市场排除原因（原因可能重叠，不能相加当策略数）

```json
{
  "insufficient_trades": 3,
  "execution_errors": 49,
  "daily_sharpe_gt_3": 6,
  "fill_artifact_suspect": 6,
  "prior_fill_artifact_suspect": 7,
  "saved_intraday_sharpe_gt_3": 6,
  "invalid_max_dd": 2,
  "duplicate_group": 14
}
```

## 阅读顺序

先看证据层和本轮重要疑点，再看年化/回撤及逻辑分；点开卡片核对完整入场出场、数量、风险控制和解释器差异。高分仅说明报告指标与既定权重下的研究位置，不证明原策略可交易。

## 不能由现有数据推出的结论

没有原平台逐笔对照，未独立复现；原仓库快照缺失，规范化哈希不是严格版本绑定。当前成分股回看历史有幸存者偏差。近三年仅历史末段，非严格样本外。没有每日收益序列，未生成年度收益、恢复期、相关矩阵或新净值图。

## 本地更新

```sh
python3 -m unittest discover -s tests -v
python3 -m tools.strategy_ranking.build --source "<回测目录>"
python3 -m tools.strategy_ranking.verify --source "<回测目录>"
node tests/test_ranking_ui.cjs
```

原始策略和回测文件只读。生成器与精读记录纳入工作分支；生成目录、CSV、JSON和卡片保留本地，可由同版本输入重建。未部署、未推送。
