# 基于MACD的复合量化交易策略Compound-Quantitative-Trading-Strategy-Based-on-MACD · 保守修复候选

原研究名单 #259 / SID 2764。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/5f35344289e2.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 恢复用户起止时间。
- 死叉平仓窗外仍生效。

## 未解决／保持原行为

- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 窗口前、起点、终点及窗口后各构造相同入场信号：只允许窗内新仓。
- 窗口结束前已有持仓，结束后出现原退出条件：退出调用仍可执行，不因日期而关闭保护。
- 结束时未退出仓位下一根sell可关闭；默认MACD参数保持。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`基于MACD的复合量化交易策略Compound-Quantitative-Trading-Strategy-Based-on-MACD.md`

原文件SHA256：`98621cd6272d3d3636749fb8263d8dca136a00bdb2e2065a046f152a140fb72a`

原代码SHA256：`d60b7b964292a9d3773abf430060ef7a9063b26863fb8ce2aa9889bdf79cc456`

候选SHA256：`58e27dfba91bdd75bb57fb755b87738e001c4840214442e65be0cd808eecbdea`
