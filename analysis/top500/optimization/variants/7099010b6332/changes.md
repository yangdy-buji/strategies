# 多周期EMA交叉量化交易策略Multi-Period-EMA-Crossover-Quantitative-Trading-Strategy · 保守修复候选

原研究名单 #234 / SID 3755。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/7099010b6332.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 日期函数恒真使用户范围及窗外平仓无效；恢复用户日期即可，已有窗外平仓分支。

## 未解决／保持原行为

- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 用户Hasta结束日期后持Compra，FechaValida为false且原Venta x fin分支可达。
- 核对原默认指标参数和数量配置未发生改变。
- 越界已有Compra执行Venta x fin；窗口内原cantidad和alcista条件不变。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`多周期EMA交叉量化交易策略Multi-Period-EMA-Crossover-Quantitative-Trading-Strategy.md`

原文件SHA256：`ac96502c40214248bcd9b8c5e65170cae90dc157a4a9201998b069733d5b389e`

原代码SHA256：`6f8f0a5c7e0d3dfc5309b1290cfa812106c341782e87169c2a6bc80ea227c331`

候选SHA256：`f1161b34ad4347d16b8d7d100be03cf5a9748d7c1f591a4a03f1a8b6813f297c`
