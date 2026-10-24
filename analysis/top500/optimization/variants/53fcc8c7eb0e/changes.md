# 多重均线趋势追踪与风控优化量化交易策略-Multi-Moving-Average-Trend-Following-and-Risk-Management-Quantitative-Trading-Strategy · 保守修复候选

原研究名单 #430 / SID 4221。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/53fcc8c7eb0e.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- trail_points和trail_offset以tick计，ATR为价格距离须除最小跳动。

## 未解决／保持原行为

- longStopLoss计算未用于硬止损，激活前无硬保护；positionSize风险假设不等于实得亏损上限。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 目标版本编译检查
- 边界和持仓退出检查
- ATR2、mintick0.01时两个参数为300tick即价格3；mintick1时为3。
- 仅全文静态复核；未执行原策略、原生编译、回测或券商操作。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`多重均线趋势追踪与风控优化量化交易策略-Multi-Moving-Average-Trend-Following-and-Risk-Management-Quantitative-Trading-Strategy.md`

原文件SHA256：`72ed5de493675aff81e055a1daa54d72ebbf3ff3942c5c4617a536f5bbf726ae`

原代码SHA256：`5ba05778a6539acab5b13b5a2df2bd71a5a4d88ca8d53a96f5d61c64d63da53f`

候选SHA256：`a06712fffba80672ce3e9ae881e1c7c3bb658cad1d841470367b45b6bc876bae`
