# 策略分类与分析目录

[打开本地交互目录](index.html) · [CSV表格](catalog.csv) · [JSON完整数据](catalog.json) · [评分与分类方法](methodology.md)

覆盖 **5807** 份原始资料；**24** 份已逐份源码复核，**5783** 份为自动初审。历史表现验证 **0** 份。

## 如何使用

打开 index.html，默认显示已源码复核的交易策略，按合理性排序。切换“自动初审”查看全量研究线索；点击名称阅读卡片。CSV可用表格软件筛选。卡片同时提供HTML和Markdown。

合理性高不代表收益好。自动初评分依据代码特征，不能替代语义分析。未复核卡片包含作者说明、订单上下文和完整源码，其规则解释仍可能不完整。美股是目标市场，原市场配置并不等于美股适配通过。

## 类别覆盖

|类别|资料数|
|---|---:|
|做市／网格|1|
|动量／突破|772|
|均值回归|656|
|待分类|1641|
|混合策略|2|
|相对价值／配对|1|
|趋势跟随|2589|
|辅助资料|143|
|配置／定投|2|

## 已源码复核卡片

|策略|类别|合理性分|
|---|---|---:|
|[Heikin-Ashi非重绘趋势确认策略-Heikin-Ashi-Non-Repainting-Trend-Confirmation-Strategy](cards/15affc3b0e28.md)|趋势跟随|68|
|[MACD和EMA金叉死叉策略MACD-and-EMA-Crossover-Strategy](cards/010c60466cf6.md)|趋势跟随|67|
|[布林带与日内强度指数均值回归策略Bollinger-Band-Mean-Reversion-Strategy-with-Intraday-Intensity-Index](cards/34085a4ae810.md)|均值回归|66|
|[布林带反转趋势策略Bollinger-Bands-Reversal-Trend-Strategy](cards/5a9c7a457850.md)|混合策略|62|
|[海龟突破回撤自适应交易策略Turtle-Breakout-Drawdown-Adaptive-Trading-Strategy](cards/5ef47daa0a94.md)|动量／突破|61|
|[基于两个移动平均线的交叉策略Moving-Average-Crossover-Strategy](cards/23a71b1eb86e.md)|趋势跟随|58|
|[Ichimoku云图量化交易策略A-Quantitative-Ichimoku-Cloud-Trading-Strategy](cards/7dfe079f8297.md)|趋势跟随|57|
|[MACD机器人交易策略MACD-Robot-Trading-Strategy](cards/5130cb589dd5.md)|趋势跟随|57|
|[StochRSI反转交易策略StochRSI-Reversal-Trading-Strategy](cards/5819e697269a.md)|均值回归|57|
|[基于一目均衡表的趋势追踪策略Ichimoku-Balance-Line-Trend-Tracking-Strategy](cards/e778e94faea8.md)|动量／突破|56|
|[基于EMA均线和MACD指标的趋势跟踪策略EMA-Crossover-and-MACD-Signals-Trend-Following-Strategy](cards/ddfb4f138b33.md)|趋势跟随|55|
|[EMA背离均值回归策略-EMA-Divergence-Mean-Reversion-Strategy](cards/c8750b01e731.md)|均值回归|54|
|[RSI统计套利策略](cards/c622ccb3feb1.md)|混合策略|53|
|[相对强弱RSI反转策略RSI-Reversal-Trading-Strategy](cards/7c1725092064.md)|均值回归|53|
|[穿越限价单双向跨期交易策略Cross-Limit-Order-Cross-Period-Trading-Strategy](cards/9b0a60acee52.md)|趋势跟随|51|
|[MACD-TEMA-交叉策略-MACD-TEMA-Crossover-Strategy](cards/5cfa877d1e24.md)|趋势跟随|50|
|[双均线SuperTrend量化交易策略Dual-Moving-Average-Supertrend-Quantitative-Trading-Strategy](cards/050aa1424f6a.md)|趋势跟随|50|
|[基础网格交易策略](cards/06fca4671779.md)|做市／网格|50|
|[超级趋势策略SuperTrend-Strategy](cards/62ca8ecd6b78.md)|趋势跟随|48|
|[趋势强度确认策略Trend-Strength-Confirm-Bars-Strategy](cards/148e98c1270f.md)|趋势跟随|48|
|[均值回归型布林带美元成本平均投资策略-Mean-Reversion-Bollinger-Band-Dollar-Cost-Averaging-Investment-Strategy](cards/52863e516d34.md)|配置／定投|47|
|[高频跨期套利策略](cards/40ab585c7423.md)|相对价值／配对|43|
|[一种定期购买加密货币的策略Simple-Holder-Strategy](cards/2612b59fe65a.md)|配置／定投|39|
|[套利图表](cards/6c3ce34f346f.md)|辅助资料|不评分|

## 更新与验证

在工作分支根目录运行：

```sh
python3 -m unittest discover -s tests -v
python3 -m tools.strategy_catalog.build --workers 8
python3 -m tools.strategy_catalog.verify
```

复核覆盖文件在 reviews/，绑定源文件SHA256；源码改变后拒绝使用旧复核。代码相同组只代表完整提取源码字节相同（忽略首尾空白），不把同一家族当成重复。
