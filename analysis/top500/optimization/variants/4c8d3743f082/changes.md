# 连续K线反转突破策略Consecutive-Candlestick-Reversal-Breakout-Strategy · 保守修复候选

原研究名单 #110 / SID 5503。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/4c8d3743f082.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 恢复日期入场。
- 窗外原保护退出仍生效。

## 未解决／保持原行为

- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 窗口前、起点、终点及窗口后各构造相同入场信号：只允许窗内新仓。
- 窗口结束前已有持仓，结束后出现原退出条件：退出调用仍可执行，不因日期而关闭保护。
- 末根入场后越界，满足原ATR或stop_loss条件仍平仓并清active。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`连续K线反转突破策略Consecutive-Candlestick-Reversal-Breakout-Strategy.md`

原文件SHA256：`9c8ad76d55119ad4beb89997efd34d179f15a1d1c5fef8a6e617f3b4973d1a38`

原代码SHA256：`10a75f95fded5124a0ff9c3543d23e5b73776ad1a11c4a2b9f145af6d6d22bee`

候选SHA256：`fff8c17e9eec3d2f0b3456a706b76f641910b5c0589cfdb874fb8bfb236000af`
