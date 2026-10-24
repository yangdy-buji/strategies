# 双TEMA叉死叉交易策略Dual-TEMA-Crossover-Trading-Strategy · 保守修复候选

原研究名单 #472 / SID 1915。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/740285e0f0f4.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 恢复入场日期。

## 未解决／保持原行为

- 未进行原生Pine编译、回测或订单撮合验证；批准仅限所列静态修复。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 窗外不新增仓位。
- 已有多仓窗外反向仍退出。
- 窗外xnRes<ynRes继续平多，窗外上涨不进场。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`双TEMA叉死叉交易策略Dual-TEMA-Crossover-Trading-Strategy.md`

原文件SHA256：`9fb49b9aea47dee036223f1e5ec9f814685db0d7614dbf7ade673c3079e4668a`

原代码SHA256：`02f020eb73ce8547b5d76969d2209ff93ec3e03e2ec236f78015cb6eb8de8b44`

候选SHA256：`799f6d612ee4cd7cf0db15449a4d3404b16f49bc009ec9381b0c17f7f717b464`
