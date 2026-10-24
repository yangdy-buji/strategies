# 多指标趋势动量ATR目标价交易策略-Multi-Indicator-Trend-Momentum-ATR-Target-Trading-Strategy · 保守修复候选

原研究名单 #284 / SID 3984。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/9a6f7abdc541.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 修正标准返回值对应关系。

## 未解决／保持原行为

- 持仓重复longEntry可重置目标，目标依然以信号close计算。
- 未进行原生Pine编译、回测或订单撮合验证；批准仅限所列静态修复。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- +DI大于-DI且ADX上升才符合原adxCondition。
- DMI返回30/10/25时趋势应满足ADX>18与plusDI>minusDI。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`多指标趋势动量ATR目标价交易策略-Multi-Indicator-Trend-Momentum-ATR-Target-Trading-Strategy.md`

原文件SHA256：`c70a03c5e8802f8bd351684d1206ceedb4dffd192c311c9835eef8b0af0c048d`

原代码SHA256：`10cb028c689b16c06030a1bf2bba8ff58e6df1aacf07326e803c30f50c4cd077`

候选SHA256：`6c05b1678e0286b8a0f6ea624a3233351d55a3c433734b9e13980c7ff31f1ac3`
