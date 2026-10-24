# 基于布林带和MACD的量化交易策略Trading-Strategy-Based-on-Bollinger-Bands-and-MACD · 保守修复候选

原研究名单 #11 / SID 3330。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/93c4ed6e7b91.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 原AND/OR依赖优先级；加括号明确两条原入场路径而不改变逻辑。
- 原起始时间闲置；只在开仓分支增加包含起始时刻门禁。

## 未解决／保持原行为

- 未原生Pine编译/回测；静态及小范围模型不等于订单成交模拟，旧版收益不适用。
- expected_rebound仍为不要求触及下轨的独立路径；保护仍为条件市价退出。

## 验证场景

- AND/OR八组合真值表；仅开仓加日期且全部退出文本不变。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。

- expected_rebound的or分支绕过布林下轨过滤。
- 追踪保护是close条件市价退出，不是盘中stop挂单；日期门禁恒true。

## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`基于布林带和MACD的量化交易策略Trading-Strategy-Based-on-Bollinger-Bands-and-MACD.md`

原文件SHA256：`1b9f9c478c4596263b90f899492771a015cd0a44b3866c392f9a421dc68fb3d1`

原代码SHA256：`c59ed9691eef481f276b1242ccbe14d158621ec934a41297ae258a3b8ac1d722`

候选SHA256：`bb6b9f59cf74d243ce6de62fcb88e1480f373992dfbca210e21955e2ecabbf78`
