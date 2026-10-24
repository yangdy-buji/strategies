# 基于支持位和趋势EMA的多空策略-Support-Level-and-Trend-EMA-Based-Long-Strategy · 保守修复候选

原研究名单 #131 / SID 3422。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/2c11252bcd5b.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 第一档50%无止损却预留仓位，第二档止损只能保护剩余部分；给首档补同一止损。

## 未解决／保持原行为

- 动态目标和止损随每根指标变化，未锁定入场。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 持Ultra Long 100份时第一目标预留50份；价格先跌破longStopLoss，两个退出组共覆盖100份。
- 核对原默认指标参数和数量配置未发生改变。
- TP1前先触SL须覆盖两组份额；TP1后剩余数量仍由Full Exit止损保护。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`基于支持位和趋势EMA的多空策略-Support-Level-and-Trend-EMA-Based-Long-Strategy.md`

原文件SHA256：`fd7a3fda84536ac031b14b09b47a4fb186b441eff946a2b0445296fc4ad44555`

原代码SHA256：`8582e8776363035fe83e7579ceeb322e874522eae4781f19ec8079c8ac10d2f4`

候选SHA256：`54d667f9c485690e1b9c33c5c622c83a9b6b175c34952e9cb598e81d2b7227b2`
