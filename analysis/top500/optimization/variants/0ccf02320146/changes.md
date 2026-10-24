# 双均线趋势跟踪策略与RSI过滤器-Dual-Moving-Average-Trend-Following-Strategy-with-RSI-Filter · 保守修复候选

原研究名单 #297 / SID 2105。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/0ccf02320146.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 先清理空仓旧锚价，再记录本次入场信号收盘价，防止新记录立即被空仓复位抹掉。
- 删除发单同根的尾部再次清零，保留刚记录的新信号价格。

## 未解决／保持原行为

- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 信号当根空仓，entryPrice记录close并保留；次根成交且信号消失，锚价仍为信号收盘而不是改为均价。
- 交易结束后无新信号锚价清空；若同时有新信号只留下新信号收盘价。
- 空仓信号发单后本根position_size仍为0，尾部不得清除新entryPrice。
- 信号close=100而次根跳空105成交，止盈止损必须仍按100；平仓后无新信号清空，第二笔不得复用100。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`双均线趋势跟踪策略与RSI过滤器-Dual-Moving-Average-Trend-Following-Strategy-with-RSI-Filter.md`

原文件SHA256：`b4c33f9381894310fd5b8e16f50ffd2119ce2f6e4312027e5bd4b6e0b92f984c`

原代码SHA256：`b790a3dae7239c82b79f82a2ea38de4ede64a0bbd2cd89c7b75e8e662e19e53a`

候选SHA256：`3be997f6430009c0af97352465552b6256015dd119f5e03e521015fca219e652`
