# 多指标趋势跟踪期权交易EMA交叉策略-Multi-Indicator-Trend-Following-Options-Trading-EMA-Cross-Strategy · 保守修复候选

原研究名单 #258 / SID 4001。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/b969cfc64d26.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 空头目标也向上5%，会立即满足退出，修为按持仓方向计算。
- 使用真实空仓判断多头入场，防止伪状态复位后持仓中重写锚价。
- 使用真实空仓判断空头入场，避免状态尾部清零造成持仓误入场。
- 真实持仓期间启用止盈检查，不依赖发单当根被清零的布尔状态。

## 未解决／保持原行为

- 止盈仍在close达到目标后才提交限价单，并非入场预挂；信号close与实际成交价可有滑点。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 正常多头目标保持不变
- 空头或止损触发时正确退出
- 已持多/空仓而callSignal为真，不重新记录entryPrice或反手。
- 已持仓而putSignal为真，不重新记录entryPrice；空仓时原信号仍入场。
- 发单当根position_size=0、尾部positionOpen=false，次根实际持仓后仍执行止盈。
- putSignal信号收盘100，下bar成交后无新信号且close95，仍提交Put止盈95。
- 持多/空期间反向信号不改entryPrice、不反手；平仓后新信号可再次入场。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`多指标趋势跟踪期权交易EMA交叉策略-Multi-Indicator-Trend-Following-Options-Trading-EMA-Cross-Strategy.md`

原文件SHA256：`2d11a87cb432f3580acaaa5fe35f19fc7a5aab0934998dd6ddf9b344b50802dd`

原代码SHA256：`4b6d7be67e9ce6559de60c311d6d6987cdeb3e238368fd2b4f7b0d2e433ffcc7`

候选SHA256：`ee260c174475200b5733ccc7906029ddd265e0f84d9f1e19adf1cfec94f48f2a`
