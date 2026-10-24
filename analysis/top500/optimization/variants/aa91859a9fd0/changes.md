# 基于相对成交量和趋势的交易策略Relative-Volume-Trend-Following-Trading-Strategy · 保守修复候选

原研究名单 #55 / SID 3524。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/aa91859a9fd0.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 恢复可选结束时间的入场窗口。
- 不得因日期越界重置已有持仓跟踪止损。
- 将日期门槛下移至入场，退出控制流始终可达。

## 未解决／保持原行为

- 空仓尾部会清零原entry_price/stop_loss_price，原统计与追踪初始化仍有语义疑点。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 开始前和结束后有原买信号时不产生新仓，窗口内保持原信号。
- 窗口内成交，越过结束时间后仍按原止损/止盈/反向条件退出。
- 跨结束日期既有stop_loss_price只能max上移；窗外触TSL或吞没熊条件仍关闭Long。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`基于相对成交量和趋势的交易策略Relative-Volume-Trend-Following-Trading-Strategy.md`

原文件SHA256：`781a5390eac0d386576256d87fe959e19adc449fc5b814c1666fdacd80bf57b0`

原代码SHA256：`f20c223934cc5bf7d7fb0ab9f107ac8688fb053bcf50652db934b5de1fe63831`

候选SHA256：`f03d593616365ea3fcc31e5473170114c888f9f2c04d63eec5f32ecdfe4ec5cb`
