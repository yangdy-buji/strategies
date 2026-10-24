# 均线回转反转策略Mean-Reversion-Reverse-Strategy-Based-on-Moving-Average · 保守修复候选

原研究名单 #484 / SID 2501。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/e5113536e9b4.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 恢复入场日期。
- 退出移出日期限制。
- 退出移出日期限制。

## 未解决／保持原行为

- pyramiding输入仅缩放qty，真实加仓行为保持原样。
- 未进行原生Pine编译、回测或订单撮合验证；批准仅限所列静态修复。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 日期外不再开仓。
- 窗口结束仍可按原规则平仓。
- 窗外利润条件不满足仍不平；满足完整退出条件可关闭Buy1至Buy4。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`均线回转反转策略Mean-Reversion-Reverse-Strategy-Based-on-Moving-Average.md`

原文件SHA256：`1e52bf9dd5d1b72e0efe2db63858c66be1d0147a58fcef7a95eb655475c79b09`

原代码SHA256：`94f13b9da684b3aba6af31a2377850c677900c538ad6bb08e88a9057787addc6`

候选SHA256：`320c799b00815984c9a342afbc6fa880c675d702a5259f8aa0ea10b1d52bfa0b`
