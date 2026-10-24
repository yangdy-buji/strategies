# 双RSI指标突破策略Dual-RSI-Indicator-Breakout-Strategy · 保守修复候选

原研究名单 #387 / SID 1907。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/cab2e73ee038.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 两个独立持仓用同一止损ID，存在后调用修改前调用的身份冲突；慢RSI使用独立ID。

## 未解决／保持原行为

- 默认FIFO退出分配可能与Fast/Slow独立退出的文字意图不同，未更改close_entries_rule。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 同时存在Fast Enter与Slow Enter时，各自90%均价止损有不同ID；RSI70/68独立市价退出仍有效。
- 核对原默认指标参数和数量配置未发生改变。
- Fast Enter及Slow Enter同时存在时各有stop关联；Slow平仓不修改Fast保护ID。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`双RSI指标突破策略Dual-RSI-Indicator-Breakout-Strategy.md`

原文件SHA256：`4a2c7ef024188cfd0188ff1b61f02633fd1389378e5971535aaa33fcde6fa08b`

原代码SHA256：`9aff45dde7551bd084e6c2ca75f02c871da8d75597a863a9ad867fcf389a282d`

候选SHA256：`4769382c4f54640a0d97ea662dd1fcc8bd4847155faff4ed9be77cb491d85969`
