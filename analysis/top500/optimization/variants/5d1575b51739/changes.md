# 追踪趋势获利策略Take-Profit-on-Trend-Strategy · 保守修复候选

原研究名单 #276 / SID 5519。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/5d1575b51739.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 日期输入失效；只恢复入场时间过滤，退出独立。

## 未解决／保持原行为

- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 开始前及结束后ENTRY_CONDITIONS真也不入场；已有entry仓在窗外达到BHD止盈止损仍平仓。
- 核对原默认指标参数和数量配置未发生改变。
- 结束后无新entry；已有仓位满足2/3倍bhd_unit条件仍close。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`追踪趋势获利策略Take-Profit-on-Trend-Strategy.md`

原文件SHA256：`f15e83093392f33f5b96dfe4c1ddce9b55e1384bd1ab07d062b4ee9360d666c7`

原代码SHA256：`2bdca15bfff7df5dc84d64d4f751f9a0b5a895ed0f60ce2911c6e750ee09a879`

候选SHA256：`7d00b4aa79fd45bd0ffd44bec37fda78e6493e609a1ed6e9ae4a9d6e3dcbc3b5`
