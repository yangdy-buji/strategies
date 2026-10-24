# 双均线趋势跟踪与ATR风控自适应交易策略-Dual-Moving-Average-Trend-Following-Strategy-with-ATR-Based-Risk-Management-System · 保守修复候选

原研究名单 #415 / SID 2099。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/ce0ff62415a1.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 模式1空仓检测不读取不存在的交易索引。
- 模式2同样修复不存在交易的空仓判断。
- 分批目标预留份额也必须受相同止损保护。

## 未解决／保持原行为

- S2把部分退出比例同时当目标涨幅，S1追踪允许回落，均属原参数/模型歧义。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 模式1在opentrades=0时SMA金叉，validOpenLongPosition应为true；持仓时应为false。
- 模式2在空仓且金叉和高周期趋势成立时允许开多；已有Long Entry时不重复开仓。
- 模式2持100份、部分目标50%，先触止损时两部分均受保护；先触目标只退出预定份额。
- S1/S2初始空仓可入场；S2部分比例50及100时先触止损均覆盖被预留份额。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`双均线趋势跟踪与ATR风控自适应交易策略-Dual-Moving-Average-Trend-Following-Strategy-with-ATR-Based-Risk-Management-System.md`

原文件SHA256：`a01356ca7c124dace5cea03b42db88d4b639de077ae9968580fbd24db8994215`

原代码SHA256：`a09efb5ba2b02c1937ec396ebc7b5914e1091d1ea255e37268040d21f30268f2`

候选SHA256：`423b34b1ae3fa6406d57f5ea2a066ad75f3c4945b315de200d74520e2f1420f3`
