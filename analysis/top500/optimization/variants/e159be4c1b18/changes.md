# 金叉死叉趋势追踪策略Golden-Dead-Cross-Trend-Tracking-Strategy · 保守修复候选

原研究名单 #499 / SID 5605。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/e159be4c1b18.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 恢复可关闭日期。
- 退出不受入场日期限制。

## 未解决／保持原行为

- 未进行原生Pine编译、回测或订单撮合验证；批准仅限所列静态修复。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 过滤关闭不限制日期；开启到期撤单强平。
- 窗外死叉盈利退出仍允许。
- date开关false全时段；true窗口结束原强平不受最低利润限制。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`金叉死叉趋势追踪策略Golden-Dead-Cross-Trend-Tracking-Strategy.md`

原文件SHA256：`5b0869c40fcacc8c564e7657580cea40f5bc25144322703aa7317b44f64acf35`

原代码SHA256：`a7dbde119dd8856b8f3d29b99e72c8735e2a74fd03db1f56f444b683f96ce24a`

候选SHA256：`adf9557a89710f007644c2145d773e1c31055e5d105f88f0fb021c3d595b205f`
