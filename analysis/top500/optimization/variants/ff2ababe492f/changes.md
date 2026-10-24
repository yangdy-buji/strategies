# 均值回归型连续K线反转交易策略-Mean-Reversion-Consecutive-Candle-Reversal-Trading-Strategy · 保守修复候选

原研究名单 #2 / SID 2458。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/ff2ababe492f.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 原日期门禁恒真；恢复起止参数并包含边界，仅限制入场。

## 未解决／保持原行为

- 未原生Pine编译/回测；静态及小范围模型不等于订单成交模拟，旧版收益不适用。
- 保留默认200%权益与无硬止损；逐tick/收盘执行仍需原生验证。

## 验证场景

- 前/起始/中间/结束/后五点日期边界；独立退出保留。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。

- 默认200%权益逆势买入且无硬止损，外部固定单位回测不反映杠杆与保证金风险。
- 日期门禁恒true；实时逐tick及收盘成交与历史OHLC可能不一致。

## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`均值回归型连续K线反转交易策略-Mean-Reversion-Consecutive-Candle-Reversal-Trading-Strategy.md`

原文件SHA256：`bc5722e8427f767693149c947e9776c5b45e7fdcee8e1b555dc4dac9dfe2195f`

原代码SHA256：`b33bbc9842fb275975899b6686adfca7a930962243ab0d410af29bd0a8e41910`

候选SHA256：`fa2b50f05703cc757e7870dbe8859bec36f8a6aa45242d6cf4c239c3f48a41c1`
