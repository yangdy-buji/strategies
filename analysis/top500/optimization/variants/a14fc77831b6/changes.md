# 动量突破旗形模式交易策略基于量价确认的日内高频交易系统-Momentum-Breakout-Flag-Pattern-Trading-Strategy-Volume-Price-Confirmed-Intraday-High-Frequency-Trading-System · 保守修复候选

原研究名单 #127 / SID 1776。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/a14fc77831b6.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- strategy.close首参必须是入场ID，现与实际入场不匹配。
- strategy.close首参必须是入场ID，现与实际入场不匹配。
- 旗形在本块因回撤或超时失效后，入场须重新确认inFlag，不能继续突破下单。

## 未解决／保持原行为

- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 持仓时首次高量阴线平50%
- 第二次高量阴线平剩余
- 回撤超限且同根新高放量，inFlag=false后不得入场；有效旗形仍按原突破入场。
- 回撤51%且newHigh与breakoutVolOk均真时不下单。
- 有效旗形突破可下单；首次最高量红K关50%，第二次关余量。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`动量突破旗形模式交易策略基于量价确认的日内高频交易系统-Momentum-Breakout-Flag-Pattern-Trading-Strategy-Volume-Price-Confirmed-Intraday-High-Frequency-Trading-System.md`

原文件SHA256：`97aeb38dab11c43d2fd5e39c0745cb9954f4c6be136351421008c3dd82ea2910`

原代码SHA256：`72c76c8dc2d44514c449e1447fd5f200e79ed406f4f8f398289900b90fcef74e`

候选SHA256：`5fa90140e6ec89dbf636236d1fe01aaf34b3043d1590089fe62aa33597815a0e`
