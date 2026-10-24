# 日内锤子反转形态多头策略Intraday-Hammer-Reversal-Pattern-Long-Strategy · 保守修复候选

原研究名单 #310 / SID 4707。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/5a6725d76968.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 对阴锤子使用实体底部到低点距离。

## 未解决／保持原行为

- 未进行原生Pine编译、回测或订单撮合验证；批准仅限所列静态修复。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 阴线open100 close98 low95，下影为3而非5，不误满足2倍实体。
- 前柱open100 close98 low95：下影3不是5；body2不应满足下影>=4。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`日内锤子反转形态多头策略Intraday-Hammer-Reversal-Pattern-Long-Strategy.md`

原文件SHA256：`843ab41928e3486c3660ce2f7d77f3a6ee15e4de8c60c769f084f426ceea6f0d`

原代码SHA256：`8d66e45daaa695c0cae48629bd7972c80daec4aa757de7cb91bc63a0f0fa239a`

候选SHA256：`96a6b0ff95f0d4a8450a470a1afffca1b6335247c28efc9ad27a182610a00cf6`
