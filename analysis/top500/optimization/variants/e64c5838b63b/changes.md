# 唐奇安通道趋势跟踪策略Donchian-Channel-Trend-Tracking-Strategy · 保守修复候选

原研究名单 #411 / SID 2421。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/e64c5838b63b.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 恢复日期窗。
- 保留窗口内入场同时提交保护；窗口外撤入场挂单并持续更新持仓保护。

## 未解决／保持原行为

- 末个窗内下单可能于下一柱先成交后撤单，日期过滤约束的是策略计算时点，不能声称绝无窗外成交。
- 未原生Pine编译、回测或订单撮合验证；批准仅限所列静态修复。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 窗外入口禁用。
- 窗口内空仓挂stop入场时同时提交原Long Exit/Short Exit，不能等持仓后才首次保护。
- 窗外有多/空仓时更新对应退出，取消Long/Short入场单但不取消Long Exit/Short Exit。
- 空仓窗内stop入场后同一柱触保护价；窗外撤Long/Short而不撤Long Exit/Short Exit。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`唐奇安通道趋势跟踪策略Donchian-Channel-Trend-Tracking-Strategy.md`

原文件SHA256：`be004131a55b062cdcf4061e36e44626a28ebb46455c38bb6e3a20392cd02f18`

原代码SHA256：`737c4bc5485ab2dedf8e3c0a326560d98920a91f6ad7f2ac35d17372c2c13985`

候选SHA256：`5e624d6cbfec4e448b4e3a6773a74eb106d3c467d69655e12dcec597f84d5f21`
