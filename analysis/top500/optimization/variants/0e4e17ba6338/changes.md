# 多均线交叉趋势跟踪RSI波动策略-Multi-Moving-Average-Cross-Trend-Following-RSI-Oscillation-Strategy · 保守修复候选

原研究名单 #341 / SID 3848。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/0e4e17ba6338.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 先提交全仓限价退出会预留全部数量，独立止损无可用仓位。

## 未解决／保持原行为

- 首成交bar尚未到持仓计算前仍无保护，属于原行为。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 正常多头目标保持不变
- 空头或止损触发时正确退出
- 均价100挂125与90，任一成交应关闭全部并取消同组另一单。
- 仅全文静态复核；未执行原策略、原生编译、回测或券商操作。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`多均线交叉趋势跟踪RSI波动策略-Multi-Moving-Average-Cross-Trend-Following-RSI-Oscillation-Strategy.md`

原文件SHA256：`19551c3545f43d259b5d28b4130a30f5a55a6de4362745a3c5f7a8dfe104872e`

原代码SHA256：`85c7918f3dec2e741442352cef92eceac33333a640c32de588d382a3eab4d808`

候选SHA256：`03ccf9d2d377cb7c52bb86e9d25914764535c5fd85daa815c56bf2d3508a6867`
