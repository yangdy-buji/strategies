# 双移动均线趋势跟踪交易系统结合风险收益比优化策略-Dual-Moving-Average-Trend-Following-Trading-System-with-Risk-Reward-Ratio-Optimization-Strategy · 保守修复候选

原研究名单 #296 / SID 2196。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/7f7ef78245b5.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 保护单独立于入场信号，在有效持仓均价存在时每根维护。

## 未解决／保持原行为

- 首次成交到下一次计算之间没有有效均价保护，未改变执行设置。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 入场信号只出现一根，成交后信号消失，仍须有非na止盈和止损。
- 多仓均价100时止损在下方目标在上方；如有空仓则止损在上方目标在下方。
- 首次Compra后无再信号仍有SL/TP；close<ema20才允许复位的原节奏不变。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`双移动均线趋势跟踪交易系统结合风险收益比优化策略-Dual-Moving-Average-Trend-Following-Trading-System-with-Risk-Reward-Ratio-Optimization-Strategy.md`

原文件SHA256：`dd0e877b70cbed06fb6c67f4d094e45d811544b4939e9c04ce97905bc813b45a`

原代码SHA256：`9e82287de35a9c43c7d25fbed08a4d1a6335ddf5065b03c918fb84abfccaab32`

候选SHA256：`806f72121f9e1438119b0b2d8a3d4ff38a8099457fa61cb2be6a28f0694602a9`
