# 双均线趋势交叉量化交易策略研究与优化-Dual-Moving-Average-Trend-Crossover-Quantitative-Trading-Strategy-Analysis-and-Optimization · 保守修复候选

原研究名单 #490 / SID 2094。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/37f7a0ea56a3.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 每根持仓K线计一笔，累计利润正负被误当单笔胜负。

## 未解决／保持原行为

- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 持仓十根只计一笔
- 先赢后亏分别记一次赢亏
- 零盈亏不计胜负
- 持仓10根只计一笔；先赚100后亏20应胜1负1。
- 仅全文静态复核；未执行原策略、原生编译、回测或券商操作。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`双均线趋势交叉量化交易策略研究与优化-Dual-Moving-Average-Trend-Crossover-Quantitative-Trading-Strategy-Analysis-and-Optimization.md`

原文件SHA256：`9385f47a1a35562c24b2ea74b238bcfde1bf69a17de3b07b509bc37183e96cca`

原代码SHA256：`0536631d0c6e27eba6a83a9ca0355b086d1389540ce5274d6a0ce426ccac3a01`

候选SHA256：`a89f3f60786ad0c34604014d4ec382675b86091af75018abb492fe25bc9ae003`
