# 双周期ATR波动率突破股票趋势策略Volatility-Bands-and-VWAP-Multi-Timeframe-Stock-Trend-Trading-Strategy · 保守修复候选

原研究名单 #408 / SID 1959。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/963ff671d194.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 恢复日期。
- 退出移出门禁，接回已声明撤单条件。

## 未解决／保持原行为

- 最后窗内下单仍可能于下一柱先成交后执行窗外撤单；不保证撮合时间绝对在窗内。
- 未进行原生Pine编译、回测或订单撮合验证；批准仅限所列静态修复。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 日期窗外禁止新挂单。
- 反向且未成交时撤销long挂单。
- 窗外退出仍执行，挂单取消。
- stop未成交后source跌破ma或超出时间窗，long挂单被取消；已持仓反向信号仍平仓。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`双周期ATR波动率突破股票趋势策略Volatility-Bands-and-VWAP-Multi-Timeframe-Stock-Trend-Trading-Strategy.md`

原文件SHA256：`7c5c2f6959b0af3cb6985002a175b657f151176e905ab1d14ded95ddce36f955`

原代码SHA256：`927cf69d129f4881a0a82d42dc184f19fb3104cce2fa05fac5de7df26ebcf402`

候选SHA256：`bc8e18f93062f79aa1f165922921f5e1b00d7f945e54aeda6bc119c2346a91d7`
