# 日内多头突破策略-Intraday-Bullish-Breakout-Strategy · 保守修复候选

原研究名单 #36 / SID 4705。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/07a7a5392ed8.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 策略启用开关没有接入订单条件。

## 未解决／保持原行为

- 持仓重复形态仍覆盖entryLongPrice1并移动目标/止损；是否冻结属设计选择。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 关闭开关不入场
- 已持仓退出仍有效
- entryCondition1=false时即使swingLow为真也不能下Long。
- 仅全文静态复核；未执行原策略、原生编译、回测或券商操作。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`日内多头突破策略-Intraday-Bullish-Breakout-Strategy.md`

原文件SHA256：`4d24800b441b063df4a1aedbc8357f3e3c7a9f2c63fce02cf1322f6abe32d0b0`

原代码SHA256：`8c408c699059bf5582c9750e3b3acad129a3560f5eee66746dfa526a41c27799`

候选SHA256：`061bb0891b1b15a142e3479be46135f60a93e259de5cc3d9506027cb37c35dbb`
