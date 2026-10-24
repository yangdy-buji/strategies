# 布林带结合超级趋势的智能波动区间交易策略-Intelligent-Volatility-Range-Trading-Strategy-Combining-Bollinger-Bands-and-SuperTrend · 保守修复候选

原研究名单 #311 / SID 4500。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/6deabcb408ef.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 按中轨上轨下轨解构。

## 未解决／保持原行为

- Supertrend direction正负与图色含义、shape_triangle_up等字符串合法性仍需目标平台核实。
- 未进行原生Pine编译、回测或订单撮合验证；批准仅限所列静态修复。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 中轨等于SMA，卖出比较真正上轨。
- 给BB返回100/120/80时bb_basis=100，bb_upper=120，median_lower=90。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`布林带结合超级趋势的智能波动区间交易策略-Intelligent-Volatility-Range-Trading-Strategy-Combining-Bollinger-Bands-and-SuperTrend.md`

原文件SHA256：`0756bd6229bfcafb887e02fe5a98ac36a81cab6e24b2dc04b36672982a96f7bd`

原代码SHA256：`5c481bf6181a1651b092a15b3ac043f3e0751b244b1efda3a56b58e97a03b600`

候选SHA256：`f84565a18cb09e104db25097b6eea102d161f91720afb539f8b792b8b25a2398`
