# 布林带突破动量跟踪交易策略-Bollinger-Bands-Breakout-Momentum-Trading-Strategy · 保守修复候选

原研究名单 #32 / SID 4488。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/77bafc111633.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 恢复日期。
- 出口移出日期窗。

## 未解决／保持原行为

- 未进行原生Pine编译、回测或订单撮合验证；批准仅限所列静态修复。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 窗外不新开。
- 日期后下破下轨已有仓位平仓。
- 结束后下破下轨仍平Long，上破上轨不能入场。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`布林带突破动量跟踪交易策略-Bollinger-Bands-Breakout-Momentum-Trading-Strategy.md`

原文件SHA256：`b7568684ae12b9574578bdb492987db71cf5d63e33470fa3512c0bd26f506ce8`

原代码SHA256：`ff0530cb6cbbee7baf875b252cd5c4ab4af3da4f2902956a797edd05ebecad5c`

候选SHA256：`85822b7c921db7be5e2bcddc2486c321aef402f3cb99b12deac693ffca5c92ed`
