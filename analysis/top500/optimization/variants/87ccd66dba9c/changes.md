# 动态供需区间中线反转策略-Dynamic-Supply-Demand-Zone-Midline-Reversal-Strategy · 保守修复候选

原研究名单 #429 / SID 1474。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/87ccd66dba9c.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 合并Long全仓止盈止损，防止退出预留份额冲突。
- 合并Short全仓止盈止损，防止退出预留份额冲突。

## 未解决／保持原行为

- 新信号close_all与entry同次发送、区域被重写仍沿用原逻辑，未验证其成交顺序。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 开Long后先触对应供需区止损，应覆盖全部仓位；先触目标应取消同组止损。
- 开Short后先触对应供需区止损，应覆盖全部仓位；先触目标应取消同组止损。
- 分别Long跌破entryDemandZone、Short突破entrySupplyZone，全部仓位均有止损。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`动态供需区间中线反转策略-Dynamic-Supply-Demand-Zone-Midline-Reversal-Strategy.md`

原文件SHA256：`3b04b4acbf15b48afda7be0cf6a65bb79eee4b39ab7b7b5177cae22d672bbf5b`

原代码SHA256：`d7d24041a7ec3427c86c31590191e8589604358d178ea86357dd2393aef8ed9d`

候选SHA256：`037b5a66001846789aa9b3a552a899387331e1abac9f2a8b210f3245dc1d679f`
