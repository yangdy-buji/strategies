# 双移动平均线交叉MACD趋势跟踪策略Dual-Moving-Average-Crossover-MACD-Trend-Following-Strategy · 保守修复候选

原研究名单 #130 / SID 2209。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/63539726a65b.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 恢复日期函数。
- 接入入口日期门禁。
- 接入入口日期门禁。
- 接入入口日期门禁。
- 接入入口日期门禁。
- 双向窗外保留反向平空。
- 双向窗外保留反向平多。

## 未解决／保持原行为

- 未进行原生Pine编译、回测或订单撮合验证；批准仅限所列静态修复。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 窗外函数为false。
- 该入口窗外不发新订单。
- 双向窗外绿信号平空不反开。
- 双向窗外红信号平多不反开。
- 三种LSB乘窗内外乘Green/Red核对：Both窗外Green仅close S，Red仅close L。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`双移动平均线交叉MACD趋势跟踪策略Dual-Moving-Average-Crossover-MACD-Trend-Following-Strategy.md`

原文件SHA256：`f4919da828cadb078c7b6613d818a2d09c8f1bb78a9796e999716f391fa84172`

原代码SHA256：`7606237cdb50236316a547662574f61eceb8e7551f061f2e4c5b2d9e22e32983`

候选SHA256：`9ebf4c188974c6664c1108f6fec47b4ebd7f910b70cf993397a1ef5d2cd95126`
