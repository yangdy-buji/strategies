# 基于量化统计的双标准差动态VWAP震荡突破交易策略-Statistical-Dual-Standard-Deviation-VWAP-Breakout-Trading-Strategy · 保守修复候选

原研究名单 #179 / SID 3675。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/541a3e0149e7.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 历史bar全部使用timenow使间隔不随历史行情前进；应使用当前K线time。

## 未解决／保持原行为

- 被pyramiding拒绝的重复信号仍更新lastEntryPrice/Time；gap按开仓而非平仓计时的设计未变。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 回放两根历史K线时间相隔15分钟、lastEntryTime非na：间隔判定应随bar time推进，不依赖执行时timenow。
- 核对原默认指标参数和数量配置未发生改变。
- 两历史信号相隔14与15分钟分别不通过/通过默认15分钟条件，不随运行时钟变化。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`基于量化统计的双标准差动态VWAP震荡突破交易策略-Statistical-Dual-Standard-Deviation-VWAP-Breakout-Trading-Strategy.md`

原文件SHA256：`c8291078cd6e0e6a58fe98da7018c6caa0619f2a4484cdc6fd074bb223749342`

原代码SHA256：`23286672d43e72b9ab9507680cc29980050eb2bb7b9252a39cdf2e66d1405c18`

候选SHA256：`5e81da99e5c137a1dff182694e499d6836d3e9b90c61234496a829073f4ff87e`
