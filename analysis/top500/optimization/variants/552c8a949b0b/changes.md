# 基于布林带B指标的长线交易策略Long-Term-Trading-Strategy-Based-on-Bollinger-Bands-B-Indicator · 保守修复候选

原研究名单 #46 / SID 3322。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/552c8a949b0b.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 原保护单仅在入场信号为真时提交；改为确认持多仓时持续提交，空仓不提交。

## 未解决／保持原行为

- 默认100%止损产生零止损价；首次成交到后续计算之间保护覆盖未验证。
- start_date/end_date仍未接入，本轮未扩大范围。
- 未原生Pine编译/回测；静态及小范围模型不等于订单成交模拟，旧版收益不适用。

## 验证场景

- 保护单独立于入场信号且仅持多仓提交；100%默认值保留。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。

- 默认Stop Loss=100%，止损价为0，与介绍5%止损不符。
- exit仅在入场条件成立时提交，初始均价不可用可能留下无有效退出仓位。
- 日期输入闲置，未设置pyramiding却称动态加仓。

## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`基于布林带B指标的长线交易策略Long-Term-Trading-Strategy-Based-on-Bollinger-Bands-B-Indicator.md`

原文件SHA256：`8637e9238b926156759354b8d49f1b3cbeff4a7e9e6ef7fe0aeee08dd75207bf`

原代码SHA256：`caa922bf8431b8c5248f98738e1af95fe457c16503c2fe9d7a7541be6e8fd6f3`

候选SHA256：`1763265e8c7cc25e1047475f62d04fe919db2fd853686f5be02f4f6f707d328f`
