# 基于ATR和突破的ETF交易策略An-ATR-and-Breakout-based-ETF-Trading-Strategy · 保守修复候选

原研究名单 #141 / SID 2597。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/4a273ddd3263.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 多头枚举遗漏count-3，导致该层未被跟踪退出；连续信号计数也可能超过已成交编号，后者需进一步设计。

## 未解决／保持原行为

- 计数可超过十个，当前退出仅最近十个且计数含被拒信号，超过范围的覆盖需另行设计。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 设count_open_longs=4且持有Long1，触发trailing_SL_long_signal，新增count-3平仓命令必须匹配Long1。
- 核对原默认指标参数和数量配置未发生改变。
- count_open_longs=4时补上Long1退出；其余0..9的现有退出均保留。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`基于ATR和突破的ETF交易策略An-ATR-and-Breakout-based-ETF-Trading-Strategy.md`

原文件SHA256：`ff55f72dfec08b7b8e7b3d2e339bedfd54a1a8ec70038132f990cf956706c044`

原代码SHA256：`a55e9b816dee402e93851b1ad072c9b3ec462b7dc5bd18dca2544a5f83b46a8e`

候选SHA256：`9f74a3b51c4fe63ceecbf26b689d98e915df94e133954773a7d14e1c1a27f2c7`
