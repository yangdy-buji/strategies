# RSI均线交叉趋势策略RSI-Moving-Average-Crossover-Trend-Strategy · 保守修复候选

原研究名单 #137 / SID 799。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/4414ec4b27e7.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 恢复日期窗。
- 退出移出日期入场门禁。

## 未解决／保持原行为

- 未进行原生Pine编译、回测或订单撮合验证；批准仅限所列静态修复。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 开始日前不入场。
- 结束日23:59之后不入场。
- 窗外持仓遇反向信号仍平仓。
- 起止两边及等号边界；窗外emavalue<smavalue仍调用close。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`RSI均线交叉趋势策略RSI-Moving-Average-Crossover-Trend-Strategy.md`

原文件SHA256：`5244f67bbbfd825ef266e0e011b9fc88be589ccc5b2897ebacac26a98037e313`

原代码SHA256：`300b4a9c08c56e9648e92ca0e75a1eb9876013e3b176515679c848b07867aa05`

候选SHA256：`73a32f71cd450ff0eccc8bf832552b140f6ac134ba362f2b4953c288ef52a0aa`
