# 基于趋势确认的多重指标动态止损策略-Trend-Confirmation-Multi-Indicator-Dynamic-Stop-Loss-Strategy · 保守修复候选

原研究名单 #336 / SID 3634。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/8f958fc7b956.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 对齐延迟事件与摆动低点历史索引。

## 未解决／保持原行为

- 空仓时清除摆动记录及仅低于SMA才挂保护单保持原样。
- 未进行原生Pine编译、回测或订单撮合验证；批准仅限所列静态修复。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- t-1识别t-2摆动低点时，t保存low[2]。
- 昨日识别前日低点90，昨日low95时保存90而非95。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`基于趋势确认的多重指标动态止损策略-Trend-Confirmation-Multi-Indicator-Dynamic-Stop-Loss-Strategy.md`

原文件SHA256：`958d375d403b8c5634cd8ec041ea092a336838a6c3eae2e833e01f14db7e80ad`

原代码SHA256：`e78e8c9251e317b0c7138ba0d94904f6db761844e308f326576841928fe55ad1`

候选SHA256：`166980bbd9c5fdd7ab8f1348edba88b5ec04c76688e96de10f87091683dcd7b7`
