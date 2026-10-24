# 趋势跟踪止损策略Trend-Following-Strategy-with-Trailing-Stop-Loss · 保守修复候选

原研究名单 #29 / SID 5419。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/a7d51c90d23e.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 把现有正确日期函数接到唯一入场。

## 未解决／保持原行为

- 余下50%没有明确退出及动态目标随close上移，原保护设计待确认。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 窗口前、起点、终点及窗口后各构造相同入场信号：只允许窗内新仓。
- 窗口结束前已有持仓，结束后出现原退出条件：退出调用仍可执行，不因日期而关闭保护。
- 窗前/后不新开Long，已有Long的50%limit仍在窗口外提交。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`趋势跟踪止损策略Trend-Following-Strategy-with-Trailing-Stop-Loss.md`

原文件SHA256：`377dbe055aea9f0e12a32bebb73bfde6fcae19a2e7eff8b80b9f4a76c0a2b45a`

原代码SHA256：`42826c465ba69587c34c1c7f6e3ecda760c74978522d7c4936b6439bf58756ab`

候选SHA256：`10fd9d0c79cc7d913b6a1e1767fed3828713077823ca71acd33c05342ead44d9`
