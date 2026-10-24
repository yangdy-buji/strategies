# 动态均线网格交易策略Grid-Strategy-with-Moving-Average-Lines · 保守修复候选

原研究名单 #469 / SID 1506。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/cf5a70f0d348.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 修复第15格入退ID配对
- 使用ATR长度参数

## 未解决／保持原行为

- 15格与pyramiding=10及手工order标志可能失配；默认FIFO平仓需原生验证。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 仅第15格触发时生成Long15并由shortCondition15平仓
- 第14格仍使用Long14
- 默认数值结果不变
- 仅改ATR长度会改变ATR网格而非MA
- 只触发15格后仅Long15开平；MA100/ATR14时ATR按14计算。
- 仅全文静态复核；未执行原策略、原生编译、回测或券商操作。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`动态均线网格交易策略Grid-Strategy-with-Moving-Average-Lines.md`

原文件SHA256：`84305489e4204600422f2125034dec31a47b79598b31796e218375c01608010b`

原代码SHA256：`433cb1d4fc701fa25a85dc8639b0a8cc641d04bcaccb28f02ce7355e44988e71`

候选SHA256：`869cc91b19fb9f32455d5743292cf6c83c4d2a17358379c7a2ad98c54ba7ca21`
