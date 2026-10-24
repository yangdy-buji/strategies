# 收缩带Bollinger与RSI组合策略Bollinger-Bands-and-RSI-Combination-Strategy · 保守修复候选

原研究名单 #103 / SID 4671。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/fb7f387aa500.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 恢复可选截止日期。
- 窗外持仓继续单向跟踪。
- 允许持仓窗外执行原退出块。
- 入口仍严格窗内。

## 未解决／保持原行为

- 源码混合tab与空格缩进，未原生编译确认；stop_loss_price为手动收盘判定非真实止损挂单。
- 未进行原生Pine编译、回测或订单撮合验证；批准仅限所列静态修复。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 关闭截止仅限制开始。
- 过期持仓止损不被重置放宽。
- 日期外超买或触线仍平仓。
- 窗外即使挤压信号成立也不买入。
- USE_ENDTIME false结束后仍允许，true结束后仅持仓管理；窗外止损不得因重置降低。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`收缩带Bollinger与RSI组合策略Bollinger-Bands-and-RSI-Combination-Strategy.md`

原文件SHA256：`287e6b6ddabc9a362f69d2e9b034938a97a45b79de5df9639c38ad8b575244a0`

原代码SHA256：`37352d1dc85306099e8068e570dd8994478dd456ddeca17e38d34366b7c3e68b`

候选SHA256：`c17eb75d787d590835f689f5518a79b04429689942dd2b8949556d1e50672725`
