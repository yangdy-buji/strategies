# 双移动平均线反转策略Dual-Moving-Average-Reversal-Strategy · 保守修复候选

原研究名单 #102 / SID 2213。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/812e7da5a676.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 恢复仅入口日期。

## 未解决／保持原行为

- stopDistance按当前close作分母，与按买价止损比例不完全等价；原设计未改。
- 未进行原生Pine编译、回测或订单撮合验证；批准仅限所列静态修复。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 窗外无新仓，退出仍执行。
- 窗外两个买入分支都为假，但sellCondition/stopCondition仍可平仓。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`双移动平均线反转策略Dual-Moving-Average-Reversal-Strategy.md`

原文件SHA256：`081aa85507ac20e4aa555c71470350d78f93515543812e1af429200aae0560d0`

原代码SHA256：`381d83331471287e157c48c285551fb5d8020029f4e0112ce5d3f1bf274a2205`

候选SHA256：`85de2ead10de75145f50ecc4b2ab69fb484ea7229f524afd1994f22f037a7c7a`
