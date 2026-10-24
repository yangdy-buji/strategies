# 基于EMA平均线交叉的趋势追踪策略Trend-Following-Strategy-Based-on-EMA-Crossover · 保守修复候选

原研究名单 #316 / SID 2680。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/008ca5a0bd81.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 日期恒真绕过输入。
- 平仓不能受日期门禁。

## 未解决／保持原行为

- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 原信号参数不变
- 相关条件边界及持仓退出验证
- 结束后close低于短EMA仍关long；窗外不创建新entry。
- 仅全文静态复核；未执行原策略、原生编译、回测或券商操作。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`基于EMA平均线交叉的趋势追踪策略Trend-Following-Strategy-Based-on-EMA-Crossover.md`

原文件SHA256：`54a7897c89d6939efce1fa9b7dbd1dc69a44d1d093a6cfa1607e57279da90107`

原代码SHA256：`0b1c8d86c951cc21581fd882b666730f4faeb7e543febff5afc92fbdcefdeb85`

候选SHA256：`0f04d5192cdf86caee495eacb704071b1cad91f5a5501dc781f869f8244cb7f6`
