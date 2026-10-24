# 趋势价格简单移动平均量化策略Simple-Moving-Average-Trend-Price-Quantitative-Strategy · 保守修复候选

原研究名单 #28 / SID 5369。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/433e2d506419.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 原上轨误接中轨；按bb返回中、上、下轨顺序接收。

## 未解决／保持原行为

- 未原生Pine编译/回测；静态及小范围模型不等于订单成交模拟，旧版收益不适用。
- VWMA动量仍未接入信号；没有硬止损，正确上轨过滤可能减少交易。

## 验证场景

- 已知中轨100、上轨120、下轨80；买入边界110/120/121。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。

- bb返回顺序错配，upperBB变量实际中轨，多空过滤不对称。
- VWMA动量计算未接交易；无硬止损。

## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`趋势价格简单移动平均量化策略Simple-Moving-Average-Trend-Price-Quantitative-Strategy.md`

原文件SHA256：`96452178fd848ba9d71492ab33871aa3cde502ed5bae4bcbbc25ed6fb864ed40`

原代码SHA256：`078af8ca93a9d8e1584b28917a7858255a983474fba92e72ad43ee6dec117440`

候选SHA256：`e0bf51bcb001f57680ed47040752b91d51aca31dc71fbb6f1d33de0225ea598a`
