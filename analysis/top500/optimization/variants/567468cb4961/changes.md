# 基于风险回报比和技术分析的牛旗突破策略-Risk-Reward-Ratio-and-Technical-Analysis-Based-Bull-Flag-Breakout-Strategy · 保守修复候选

原研究名单 #268 / SID 3704。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/567468cb4961.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 将同仓位止盈止损合为一组保护。

## 未解决／保持原行为

- 信号重复时重新计算保护价，原行为未调整。
- 未进行原生Pine编译、回测或订单撮合验证；批准仅限所列静态修复。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 先跌至止损时全仓可止损。
- 先触目标时全仓止盈，另一保护自动取消。
- 持仓10单位同时具有全量止损和止盈，任一成交另一取消。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`基于风险回报比和技术分析的牛旗突破策略-Risk-Reward-Ratio-and-Technical-Analysis-Based-Bull-Flag-Breakout-Strategy.md`

原文件SHA256：`17acaa568c9afce5c51a5c5ef22393c64ee4d2f744df8ea2879bcb95ae209c19`

原代码SHA256：`20f93a75d162ccd499636fded52fb9296c0dbb745cacf5b33bb064d71be82fd5`

候选SHA256：`ccea4298a145bb9afa62a2a382335de8359de024aaa14349c3fc71f9bfec00ab`
