# RSI趋势动量交易策略结合双均线和成交量确认-RSI-Trend-Momentum-Trading-Strategy-with-Dual-MA-and-Volume-Confirmation · 保守修复候选

原研究名单 #384 / SID 834。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/8e7fbde9affd.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 拒绝零长度。

## 未解决／保持原行为

- SMA长度输入仍无正数约束。
- 未进行原生Pine编译、回测或订单撮合验证；批准仅限所列静态修复。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 默认长度10结果不变。
- 输入0被参数边界拒绝。
- 长度0应不可配置，1与默认10合法。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`RSI趋势动量交易策略结合双均线和成交量确认-RSI-Trend-Momentum-Trading-Strategy-with-Dual-MA-and-Volume-Confirmation.md`

原文件SHA256：`412c001d91fe431bcec53e0680efe5adb36db118e52b504d3f44a116c9f9995f`

原代码SHA256：`830d5403205e13c4272f6eecc3a085d70e38cec007e27e3298285aaaaf402acc`

候选SHA256：`14bb4e46305233e55ced78e4169edb53c57a6b3860b394d781afbd89ee94d3e0`
