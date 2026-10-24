# 基于移动平均线均回复策略Based-on-the-Moving-Average-Reversion-Strategy · 保守修复候选

原研究名单 #187 / SID 3552。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/271b0abd9b0e.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 版本注解格式错误。

## 未解决／保持原行为

- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 原版本编译检查
- 原信号正常且退出分支保持有效
- shortMA下穿buyMA买入，上穿bigMA平仓。
- 仅全文静态复核；未执行原策略、原生编译、回测或券商操作。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`基于移动平均线均回复策略Based-on-the-Moving-Average-Reversion-Strategy.md`

原文件SHA256：`5d52c84c20f80928990d437199a9169f7e6eace40c07752ef9f22bd9dd9da856`

原代码SHA256：`774c66455af92c5509b54a96736a6b6a460207fb4ec56855d56b52459826208a`

候选SHA256：`3f33bee407168ebc4914347e0fda3e97dec1c4b4fc1246c699d19100c704e441`
