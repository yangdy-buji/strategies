# 多策略自适应趋势跟踪与突破交易系统-Multi-Strategy-Adaptive-Trend-Following-and-Breakout-Trading-System · 保守修复候选

原研究名单 #281 / SID 4134。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/2c08e80d68e1.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 均价退出仅在信号分支导致首次na且无新信号不保护；无from_entry还跨模型占用仓位。；仅对应方向实仓时持续提交，不依赖入场信号重现。
- 均价退出仅在信号分支导致首次na且无新信号不保护；无from_entry还跨模型占用仓位。；仅对应方向实仓时持续提交，不依赖入场信号重现。
- 均价退出仅在信号分支导致首次na且无新信号不保护；无from_entry还跨模型占用仓位。；仅对应方向实仓时持续提交，不依赖入场信号重现。
- 均价退出仅在信号分支导致首次na且无新信号不保护；无from_entry还跨模型占用仓位。；仅对应方向实仓时持续提交，不依赖入场信号重现。

## 未解决／保持原行为

- 首次成交至下一次计算前保护空窗仍存在；ATR随bar变化仍会移动止损/止盈。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 目标版本编译检查
- 边界和持仓退出检查
- 入场仅一根，次根无信号仍给匹配from_entry持仓提交保护；不为反方向待成交新单使用旧均价。
- Koop Range一根信号成交后次根信号为false，仍由Verkoop Range保护，其他from_entry不占其数量。
- Short Range仓仅由空头价差保护，不以旧多仓均价向待成交Short挂单。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`多策略自适应趋势跟踪与突破交易系统-Multi-Strategy-Adaptive-Trend-Following-and-Breakout-Trading-System.md`

原文件SHA256：`f1634cce3905898bb0c40b4dec47ceadcf1e12cb37977a7940ecab5703ef07e5`

原代码SHA256：`f4a662f316dea58538a2ee8179f3897bf01cf614de42bc6cabb4690768fb5630`

候选SHA256：`622bb3a98403cc68492ea7468b508d5b9f42cb656701f2cd947ea2297d2a0c7b`
