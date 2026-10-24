# 双均线RSI动量突破交易策略-Dual-EMA-RSI-Momentum-Breakout-Trading-Strategy · 保守修复候选

原研究名单 #172 / SID 1977。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/aa09afaab47f.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 入场分支把刚记录的止损设为na，持仓保护分支不执行；删除这次清空。

## 未解决／保持原行为

- 同一绿带内止损后再入会继续用该绿带交叉价，这是原状态锚点，未改为每笔成交价。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- EMA金叉时stopLoss已设为emaB，入场成交后下一根没有金叉时该值仍非na并生成Stop Loss。
- 核对原默认指标参数和数量配置未发生改变。
- 绿色交叉记录emaB后入场不能清掉；后续无新交叉持仓仍有有效stopLoss。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`双均线RSI动量突破交易策略-Dual-EMA-RSI-Momentum-Breakout-Trading-Strategy.md`

原文件SHA256：`8d47af2d26a0c55eb4cafbf995da3857d6caf746a58a6454c5693d731bce62da`

原代码SHA256：`4a13e51691e5aef5ffd800bf8abd134a90f42977cef0049bb413cb0cfa7bb224`

候选SHA256：`ea50b8e4c3706dcd2cce0eda5144cdf351874a90f3334cd05ec6c2052f952291`
