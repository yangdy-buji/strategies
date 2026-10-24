# 均线金叉死叉策略-Moving-Average-Crossover-Strategy · 保守修复候选

原研究名单 #254 / SID 2526。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/6b8c9f45435d.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 修正空头价格方向和ID。

## 未解决／保持原行为

- 未进行原生Pine编译、回测或订单撮合验证；批准仅限所列静态修复。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 空头均价100时stop101 limit97。
- 多头stop99 limit103不变。
- 均价100时多头99/103、空头101/97；反转信号仍沿用原entry/close次序。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`均线金叉死叉策略-Moving-Average-Crossover-Strategy.md`

原文件SHA256：`518d5604174a95495ff7c4217b7db4e0abe4cb8d09f39821d40d13ead27587d1`

原代码SHA256：`e3cd96adc22b3c5cdbdb67b32a9b174859c857df6330257d489298ec2372a040`

候选SHA256：`55bafdaca06a09c98890608c73d02e4314c8c65ea0e506a24d073cefd18587a2`
