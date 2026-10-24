# 双均线交叉开仓策略-Dual-Moving-Average-Crossover-Entry-Strategy · 保守修复候选

原研究名单 #189 / SID 2013。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/e166edd1228c.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 低于均线时open-ma5为负，不可能大于正阈值。

## 未解决／保持原行为

- 场景1仅盈利退出、场景2仅亏损退出属于原有不对称设计，未扩写。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 开盘99、MA100时距离为1可入第二分支
- 开盘高于MA仍由第一分支判断
- open99、ma5100时场景2为真；open99.999、ma5100时不满足距离。
- 仅全文静态复核；未执行原策略、原生编译、回测或券商操作。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`双均线交叉开仓策略-Dual-Moving-Average-Crossover-Entry-Strategy.md`

原文件SHA256：`b92196eabc1ea2d9398d104d6fbdfbd35eeec6a444180e2dfeb15c5940e61cc5`

原代码SHA256：`51a71462dbec687eb9edf1be2122a611f1dae3d64c1f0bf77b5dd542c0a05013`

候选SHA256：`990493e41f0b8afa81073609566216110fee672cfe467f6b9e625e6a35ef1103`
