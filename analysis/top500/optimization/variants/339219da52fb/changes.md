# 动态达瓦斯箱体突破与均线趋势确认交易系统-Dynamic-Darvas-Box-Breakout-with-Moving-Average-Trend-Confirmation-Trading-System · 保守修复候选

原研究名单 #303 / SID 1644。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/339219da52fb.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 保证三个highest窗口均为正。

## 未解决／保持原行为

- 未进行原生Pine编译、回测或订单撮合验证；批准仅限所列静态修复。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 输入3时最短窗口为1。
- 输入1或2被拒绝。
- boxp=3时三个窗口3/2/1；1和2被输入约束拒绝。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`动态达瓦斯箱体突破与均线趋势确认交易系统-Dynamic-Darvas-Box-Breakout-with-Moving-Average-Trend-Confirmation-Trading-System.md`

原文件SHA256：`8ffb71f39ea63ac6a2884a896e1ac057a3c2aaa5d147fa994371b342eaf8d032`

原代码SHA256：`9557049db9cb997cc4ecb46303a5e1784a2741b66447c259b77903d96b112695`

候选SHA256：`a11b576c027f210189a5be8694ea5b1fbffe6497681629be05982bf932bfbab0`
