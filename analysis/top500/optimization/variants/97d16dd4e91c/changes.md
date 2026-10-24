# RSI50_EMA长仓策略-RSI50_EMA-Long-Only-Strategy · 保守修复候选

原研究名单 #18 / SID 735。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/97d16dd4e91c.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 原平仓ID无对应入场；改为RSI以正确关联。

## 未解决／保持原行为

- 未原生Pine编译/回测；静态及小范围模型不等于订单成交模拟，旧版收益不适用。
- RSI退出仍需EXIT与bull_cross同时成立；主Buy不受RSI过滤，无独立硬止损。

## 验证场景

- 订单ID关联及EXIT/bull_cross四组合。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。

- strategy.close("RSICLose")无匹配入场ID，RSI订单缺失有效退出。
- 主Buy入场不要求RSI过滤；100%权益仓位不是百分比止损。

## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`RSI50_EMA长仓策略-RSI50_EMA-Long-Only-Strategy.md`

原文件SHA256：`a82e0b961539d2b7d6cb3a9df58a2eadf4c7abbaeb0d0e24229cb16d294bf610`

原代码SHA256：`e4bbda59eac55965fc521145f01bf63ad8f7cd47b687ea8987a270d55fb9d548`

候选SHA256：`51396140ebab90265c1d307dc80a845c4d20cb36ccdd7fa278cf0735e7fedeae`
