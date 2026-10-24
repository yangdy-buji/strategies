# 基于快速移动均线和慢速移动均线的量化交易策略Dual-Moving-Average-Breakout-Strategy · 保守修复候选

原研究名单 #62 / SID 3405。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/eee00608c188.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 恢复模式入场时间范围。
- 单向多仓退出独立。
- 单向空仓退出独立。
- 双向模式窗外只平原仓，禁止反向新开。

## 未解决／保持原行为

- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 窗口前、起点、终点及窗口后各构造相同入场信号：只允许窗内新仓。
- 窗口结束前已有持仓，结束后出现原退出条件：退出调用仍可执行，不因日期而关闭保护。
- Both在结束后Sell仅平L不建S，Buy仅平S不建L；Long only及Short only窗外退出对称。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`基于快速移动均线和慢速移动均线的量化交易策略Dual-Moving-Average-Breakout-Strategy.md`

原文件SHA256：`d24e89fe877202bb18c21cd8f6fa241ea7ef8d083794beddc547dba5e874d32d`

原代码SHA256：`836a5ae1a42bf75bff5056b3ff397fbdce0c3ad5e28e8d7b8a0297faea5cfad6`

候选SHA256：`ae837364ebe972b2f973c9f9759df312837dbb14ee952ece61e9b80a4f6014f4`
