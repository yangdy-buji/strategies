# 三倍标准差布林带突破量化交易策略结合百日均线优化-Triple-Standard-Deviation-Bollinger-Bands-Breakout-Strategy-with-100-Day-Moving-Average-Optimization · 保守修复候选

原研究名单 #475 / SID 1168。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/d314eafdf5c7.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 版本指令含空格无法按标准注解声明v6。

## 未解决／保持原行为

- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 目标Pine版本编译通过
- 检查声明绑定与对应指标输出一致
- 首个有效上轨突破仍只建Trade多头，下轨跌破仍关Trade。
- 仅全文静态复核；未执行原策略、原生编译、回测或券商操作。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`三倍标准差布林带突破量化交易策略结合百日均线优化-Triple-Standard-Deviation-Bollinger-Bands-Breakout-Strategy-with-100-Day-Moving-Average-Optimization.md`

原文件SHA256：`f2126328ccab1d1a1299249c6ce8eb00c8ca3e3766764f0179da11b3d8831cf0`

原代码SHA256：`9e7f0911caa5015c695ab986f30794ff7827dbc3c2b555855efbb561a439d59b`

候选SHA256：`56a4d23923457886faa9d39a83ba91419d5715cdfa3a01ab244199a2bda17a59`
