# Bollinger-Bands-Mean-Reversion-Trading-Strategy-with-Dynamic-Support-布林带均值回归交易策略与动态支撑 · 保守修复候选

原研究名单 #359 / SID 146。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/e557875c8bbe.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 持仓期间重复信号虽不能新增持仓，仍覆盖entryDay并错误重启当天退出限制。

## 未解决／保持原行为

- 信号日期仍是发单日期而非下一bar成交日期；未改原同日交易政策。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 持仓重复信号不重置实际入场日期，次日原退出条件仍有效。
- 昨天入场、今天持仓时再次longCondition，不更新entryDay；今天closeCondition可平仓。
- 空仓原longCondition仍可入场；同日dropCondition仍强制退出。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`Bollinger-Bands-Mean-Reversion-Trading-Strategy-with-Dynamic-Support-布林带均值回归交易策略与动态支撑.md`

原文件SHA256：`c0fc4d3f8b29369e0bf21a67529f4c2ad1481a2fb881387bbf979db35ec402f6`

原代码SHA256：`7eaf5e4eabaffacf272b8b47d12a458d1f830451cba2eed0613639484747be84`

候选SHA256：`fef17f3f19a3cb2671a439a86f9cb9fc26ef3c7f385d52d3a2eb7b271c102167`
