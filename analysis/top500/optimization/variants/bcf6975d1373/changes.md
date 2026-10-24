# 基于RSI指标的双轨突破策略RSI-Dual-track-Breakthrough-Strategy · 保守修复候选

原研究名单 #93 / SID 2849。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/bcf6975d1373.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 开始日期输入未用于入场。

## 未解决／保持原行为

- RSI退出额外要求take_profit_long，是否应无条件RSI退出属于设计选择。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 起始日前不入场
- 持仓退出不因日期失效
- 开始日前RSI低不买，开始后低RSI允许；已有仓位止损不受日期阻挡。
- 仅全文静态复核；未执行原策略、原生编译、回测或券商操作。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`基于RSI指标的双轨突破策略RSI-Dual-track-Breakthrough-Strategy.md`

原文件SHA256：`ad575d81b1f8cf7df489ed842ddf0958913add339736ba541814c0332c2c4856`

原代码SHA256：`736a1db7302096f9cd7ea3da62b15bf2ff08cb8b3209b5725247f91b09e5c5a7`

候选SHA256：`0e9bd114977852e6a38a714ca185b959f45b5560a003c99b80a5fd862dcbc097`
