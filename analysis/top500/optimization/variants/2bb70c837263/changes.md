# 基于动量交易策略Momentum-and-Volume-Trading-Strategy · 保守修复候选

原研究名单 #272 / SID 3079。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/2bb70c837263.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 百分比价差转换为tick并分离方向ID。
- 百分比价差转换为tick并分离方向ID。

## 未解决／保持原行为

- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- close=100、mintick=0.01时0.8%目标为80tick、0.5%止损为50tick；多空各自绑定入场ID。
- close=100、mintick=.01、0.8%目标应为80ticks；多空均校核，mintick=1时数值不变。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`基于动量交易策略Momentum-and-Volume-Trading-Strategy.md`

原文件SHA256：`1a2fedc42d3c1a28b4bfe9be073c19d0086b4f3452f8699abdf00c8804f761ce`

原代码SHA256：`24d900aa394e5a64f4662ace74605e87542d29d0edc9d39e3555c541baaa1d39`

候选SHA256：`2e54cb0e71bd87d8602a877de31c60908a9eb5ab54461029041ea564c660a5c0`
