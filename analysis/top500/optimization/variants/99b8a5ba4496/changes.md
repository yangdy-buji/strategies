# 基于EMA指标的趋势跟踪策略EMA-Crossover-Trend-Following-Strategy · 保守修复候选

原研究名单 #163 / SID 2687。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/99b8a5ba4496.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 恢复时间输入。
- 解除平仓的日期限制。

## 未解决／保持原行为

- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 窗口前、起点、终点及窗口后各构造相同入场信号：只允许窗内新仓。
- 窗口结束前已有持仓，结束后出现原退出条件：退出调用仍可执行，不因日期而关闭保护。
- 区间内金叉开Buy，区间外死叉仍close Buy。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`基于EMA指标的趋势跟踪策略EMA-Crossover-Trend-Following-Strategy.md`

原文件SHA256：`2bc4ac72d2bd702f1bd450c7d23900c0e403b4341af5d4530a5262663f59468a`

原代码SHA256：`c8675e31847ad2da61dc7af02e2eca7ac9c72cd53c5d6d42c0ac717cd651ffc6`

候选SHA256：`c71080ed9ca9eb4d64bb102207ab3ca33692a31c1353fc948acdde973520c808`
