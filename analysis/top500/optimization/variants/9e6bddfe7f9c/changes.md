# 基于均量线和波动率的趋势追踪策略Trend-Following-Strategy-Based-on-Volume-weighted-Average-Price-and-Volatility · 保守修复候选

原研究名单 #176 / SID 3250。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/9e6bddfe7f9c.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 起止日期没有生效；仅恢复入场日期过滤。

## 未解决／保持原行为

- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 窗口前及窗口后构造相同入场信号应被拒绝；窗口内允许原信号，已有仓位的原退出在窗外仍可执行。
- 核对原默认指标参数和数量配置未发生改变。
- 开始日00:00与结束日23:59边界内允许，之后下降条件仍可退出。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`基于均量线和波动率的趋势追踪策略Trend-Following-Strategy-Based-on-Volume-weighted-Average-Price-and-Volatility.md`

原文件SHA256：`5c27f153c7b7532186456f3a20e911698e61cca89f1371265015393c5b19a97a`

原代码SHA256：`b41cfe13e26d892b82b3fa4fb38533de033f59ae7eb4808dc1b9a490bb6dfb5e`

候选SHA256：`248f90c9f1aaa1c272cec718e145b7616d9548584c2e6b0e1c8e4589f5ce2541`
