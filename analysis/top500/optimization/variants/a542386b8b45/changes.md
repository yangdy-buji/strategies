# 多重均线趋势跟踪与动态止损策略-Multi-EMA-Trend-Following-Strategy-with-Dynamic-Stop-Loss · 保守修复候选

原研究名单 #394 / SID 4215。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/a542386b8b45.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 未偏移日线表达式配lookahead_on将日末值提前注入历史日内。
- 未偏移日线表达式配lookahead_on将日末值提前注入历史日内。
- 未偏移日线表达式配lookahead_on将日末值提前注入历史日内。

## 未解决／保持原行为

- lookahead_off实时仍使用未确认日线EMA，不能承诺不重绘；重复bullishEntry会重置目标/最高价。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 目标版本编译检查
- 边界和持仓退出检查
- 日内首小时不得取得本日最终EMA；到日线收盘才有历史确认值。
- 仅全文静态复核；未执行原策略、原生编译、回测或券商操作。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`多重均线趋势跟踪与动态止损策略-Multi-EMA-Trend-Following-Strategy-with-Dynamic-Stop-Loss.md`

原文件SHA256：`8b6a15cbaa06366bb7257d1e213b2e6c4d881098809737b1fec7815fd2f795d8`

原代码SHA256：`501003990c5a198adb718d308fc249ae8d3a4eb935d9832bf580cea90cdaed86`

候选SHA256：`49d539afbb465b7f5d104ce880b17842735fe62dd2b6b629075361d5b414b848`
