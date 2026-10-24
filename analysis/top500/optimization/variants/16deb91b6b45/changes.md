# 基于历史新高突破的买入策略Buying-Strategy-Based-on-Historical-High-Breakout · 保守修复候选

原研究名单 #145 / SID 3115。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/16deb91b6b45.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 让既定默认90合法。

## 未解决／保持原行为

- strategy overlay=1的旧隐式类型兼容性仍需原生检查。
- 未进行原生Pine编译、回测或订单撮合验证；批准仅限所列静态修复。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 默认90通过输入约束。
- 100以上原允许输入不变。
- 90与400可选，89被约束；默认EMA仍90。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`基于历史新高突破的买入策略Buying-Strategy-Based-on-Historical-High-Breakout.md`

原文件SHA256：`01041d963cc1f8c127c544a1ee2c54ea19d84d9fb19776549f63d80e73654b97`

原代码SHA256：`7d307a32ee75ee4bf50a28c489a2b7e3d811ea4fbc5c8a037ad9e8aef2e1189e`

候选SHA256：`37778e14ef8b9f39afcf6da29dfb01cc4961cbb3d35ecf6ee0e0cda442aeaf58`
