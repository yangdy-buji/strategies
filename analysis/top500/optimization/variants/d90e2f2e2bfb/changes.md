# MA-SMA-MA-Slope-Trailing-Stop-Loss-Re-Entry-均线简单移动平均线均线斜率追踪止损重新进场 · 保守修复候选

原研究名单 #337 / SID 496。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/d90e2f2e2bfb.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 每根K线重复检测上一次历史平仓会覆盖已复位的止损标记；仅在新平仓产生时检测。

## 未解决／保持原行为

- 止损识别仍用退出价格对比trailStopPrice，均线市价退出可能也满足；止损线可下移，是否改为单向追踪需确认。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 发生一次止损后条件允许再入并将stopLossOccurred清false；随后closedtrades不增加的bar不得再次读取旧成交把标记设true。
- 核对原默认指标参数和数量配置未发生改变。
- 一次止损后复位再入，后续closedtrades不增加时不得重新设置stopLossOccurred。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`MA-SMA-MA-Slope-Trailing-Stop-Loss-Re-Entry-均线简单移动平均线均线斜率追踪止损重新进场.md`

原文件SHA256：`7c6984bc326e0fd4bfd8d6985c2a0456ec62b6ca3055d6502ab482032d51920f`

原代码SHA256：`3f410df38a40500b95f9f3226662800d7f788dff65e0fed76e4888428163cbe7`

候选SHA256：`21b1bd797bdfc4ac59a2c02ef788aae78fcaef3e65bb9d403ec20db1363b4af2`
