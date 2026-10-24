# 动态趋势线突破反转交易策略-Dynamic-Trendline-Breakout-Reversal-Trading-Strategy · 保守修复候选

原研究名单 #391 / SID 1620。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/c353ad7e1d49.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 反向入场ID为Long Reverse/Short Reverse，原exit只匹配Long/Short，反向仓位失去括号保护；统一入场ID。
- 反向空仓沿用Short入场ID以匹配ShortExit。

## 未解决／保持原行为

- 通过收盘越过止损判断反手可能因止损先成交失去触发，是否要求真实止损后反手需设计确认。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 分别触发多头与空头反手，新的入场ID必须被LongExit或ShortExit匹配，数量乘数保持。
- 核对原默认指标参数和数量配置未发生改变。
- 多仓收盘跌破止损触发反手后，ShortExit必须匹配反向空仓；反向多仓亦检查LongExit。
- 多转空以及空转多均沿用Short/Long ID并由对应均价保护覆盖。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`动态趋势线突破反转交易策略-Dynamic-Trendline-Breakout-Reversal-Trading-Strategy.md`

原文件SHA256：`095c6ab82784f978db47966fe56589e188e72488aede5e3b7ec8b4f95a760292`

原代码SHA256：`b4aff37fca95db53a97eb32f979ec7901ec90fd1831a6d4d1b57db7129442454`

候选SHA256：`c5b8adfa10d93d0153e95ea7a007798b5b4cd2ac343d1bb6e4f935978ff62c6b`
