# 移动平均线金叉交易策略Moving-Average-Crossover-Trading-Strategy · 保守修复候选

原研究名单 #206 / SID 5078。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/ebfefa24d53a.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 日期条件恒真。
- 信号退出不受日期门禁。

## 未解决／保持原行为

- DEMA/TEMA/LSMA在选项中但ma函数未实现，选择后返回na；不应宣称全部选项可用。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 日期前后不新入场
- 日期外已有持仓退出仍执行
- 窗外exit信号关long，且无新buy订单。
- 仅全文静态复核；未执行原策略、原生编译、回测或券商操作。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`移动平均线金叉交易策略Moving-Average-Crossover-Trading-Strategy.md`

原文件SHA256：`ede224e98e2f0a7873a3774bc58b918baba20120655f25124ff478422c127d68`

原代码SHA256：`159076076182f239f44282130e4ecdd319e56d7766f2d2a84f3475c5d235fcb2`

候选SHA256：`b2c8f38a9bb15bb7f2f72d643fa0aa203bb34c02c3dab6e9fbadd278d222a476`
