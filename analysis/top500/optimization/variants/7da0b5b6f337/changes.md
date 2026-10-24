# EMA反向买卖策略EMA-Reverse-Buy-Sell-Strategy · 保守修复候选

原研究名单 #396 / SID 325。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/7da0b5b6f337.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 多空共用同一exit ID可能互相修改退出订单，短侧必须独立命名。

## 未解决／保持原行为

- 信号消失后限价entry未撤销，反向挂单也未设互斥；需要明确信号有效期。
- 均价na与反手旧方向均价的首次保护空窗/价位仍需原生验证。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 同时计算多空保护时各exit ID独立，对应from_entry保持Long/Short。
- Long Stop Loss/TP与Short Stop Loss/TP各自只关联对应入场；ATR倍数不变。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`EMA反向买卖策略EMA-Reverse-Buy-Sell-Strategy.md`

原文件SHA256：`bc9726f8efaa6d728be8886b88d759c11ffc58cbb87e4ad47191328066694a53`

原代码SHA256：`d672a7d11c2c29bf158fb67605352858eff95fd8b03910658c6460ba035877b7`

候选SHA256：`9e8b94e4a70322c22d9a63d25626825c031d79bc8c8ec09c07116a734a05d91c`
