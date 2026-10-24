# 双均线止盈止损趋势交易策略-Dual-Moving-Average-Trend-Trading-Strategy-with-Stop-Loss-and-Take-Profit · 保守修复候选

原研究名单 #185 / SID 2075。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/02bfc6b39fae.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 持仓期间持续提交均价保护。

## 未解决／保持原行为

- 成交到下一次策略计算间保护空档未消除。
- 未进行原生Pine编译、回测或订单撮合验证；批准仅限所列静态修复。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 金叉后下一柱无新信号也提交有效保护。
- 信号仅一柱、下一柱持仓，止损99%止盈101%；空仓不提交。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`双均线止盈止损趋势交易策略-Dual-Moving-Average-Trend-Trading-Strategy-with-Stop-Loss-and-Take-Profit.md`

原文件SHA256：`8a99e018699760e4ed67caf7650bc646f6e76e60f7be22a13405c5c16514d08b`

原代码SHA256：`08cb30cc799efe1399226e1ae16d725cc7d20e5a44f4424fdd213f44de924695`

候选SHA256：`b1dca7e2505e06ed21acb85f42291a940f5a9f6313cc01a9e1cb2b9772618306`
