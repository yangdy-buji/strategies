# 均线震荡突破HODL策略Moving-Average-Oscillation-HODL-Strategy · 保守修复候选

原研究名单 #231 / SID 2529。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/ffd9f19cf1f3.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 恢复日期。
- 保留窗外退出。

## 未解决／保持原行为

- 未进行原生Pine编译、回测或订单撮合验证；批准仅限所列静态修复。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 窗前不入场。
- 窗后跌破均线平仓。
- 结束后收盘跌破均线可close HODL，升破均线不再entry。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`均线震荡突破HODL策略Moving-Average-Oscillation-HODL-Strategy.md`

原文件SHA256：`583711766c4cd6e7a9ed7dc703be188fd53ceacb0d8f1d56d7d3e7fdaa76a592`

原代码SHA256：`094f1654fa122decb75621c8b03bfc1d6c2ffaf115cfa450db277c2ba775e152`

候选SHA256：`bc3ffcf154c6c6c2817587ed3ab960961af866795b633413321e0b698b014616`
