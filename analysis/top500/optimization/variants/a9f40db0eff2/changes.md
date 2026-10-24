# 双时间轴波动率价差交易策略Dual-Timeframe-Volatility-Spread-Trading-Strategy · 保守修复候选

原研究名单 #143 / SID 2168。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/a9f40db0eff2.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 恢复入场窗口。

## 未解决／保持原行为

- 两个Trade开关皆false时count=0导致Amount无效，未修。
- 未进行原生Pine编译、回测或订单撮合验证；批准仅限所列静态修复。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 到期后不再新入场，已有仓位按原条件退出。
- 结束后两入口均禁用且两个ID仍可被close。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`双时间轴波动率价差交易策略Dual-Timeframe-Volatility-Spread-Trading-Strategy.md`

原文件SHA256：`c2726e23faacfcacebbfab3b610b661f783fa781271fe6dba58ef2d99d558f97`

原代码SHA256：`e05c4cb547bb49b32c864ad8f4637514443eda52774c70ca7b0dca95b13f81fc`

候选SHA256：`4eb561c2df58d8ce59da757c70a9834647185b453f2289b119754b9efdd46345`
