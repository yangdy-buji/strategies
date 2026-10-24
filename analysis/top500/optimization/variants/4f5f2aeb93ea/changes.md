# 波动率动量突破交易策略结合趋势和动量过滤-Volatility-Momentum-Breakout-Strategy-with-Trend-and-Momentum-Filters · 保守修复候选

原研究名单 #444 / SID 4815。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/4f5f2aeb93ea.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 反手没有空仓根时旧同方向入价未清空，下一轮反手复用旧价；用当前真实均价持续同步。
- 反手没有空仓根时旧同方向入价未清空，下一轮反手复用旧价；用当前真实均价持续同步。

## 未解决／保持原行为

- 首次成交至下一次收盘计算仍有保护空窗；ATR继续随bar变化。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 多100→空90→多80无空仓根时多锚应80
- 正常同向持仓均价保持
- Long100→Short90→Long120无空仓bar时最后longEntryPrice为120。
- 仅全文静态复核；未执行原策略、原生编译、回测或券商操作。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`波动率动量突破交易策略结合趋势和动量过滤-Volatility-Momentum-Breakout-Strategy-with-Trend-and-Momentum-Filters.md`

原文件SHA256：`524abeb8ea609bbc197e1348759f2fff042a3b42ca86f143f3f2378cb6d0b06e`

原代码SHA256：`f454cef687230def986d7146a5d97b78bba26d1991e1be822958f62a6330e824`

候选SHA256：`bacb2d1d2257a738d79fe196b627bac422159abbc202e42a61b2803613f3e489`
