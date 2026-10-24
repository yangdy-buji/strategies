# TAM日内RSI交易策略TAM-Intraday-RSI-Trading-Strategy · 保守修复候选

原研究名单 #486 / SID 983。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/4b1f1925230c.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 日期过滤开关和开始时间无效；恢复入场时间过滤并保持退出窗外有效。
- 日期只能限制入场，退出不依赖日期。

## 未解决／保持原行为

- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 窗口前及窗口后构造相同入场信号应被拒绝；窗口内允许原信号，已有仓位的原退出在窗外仍可执行。
- 核对原默认指标参数和数量配置未发生改变。
- 开启日期过滤，起点之前不买入；人为已有Buy持仓时，窗外closeCondition仍调用平仓。
- useDateFilter=false仍全部日期允许；开启后起点前禁止entry而closeCondition仍可平仓。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`TAM日内RSI交易策略TAM-Intraday-RSI-Trading-Strategy.md`

原文件SHA256：`9e57e128d721eff222b32649f43c9cf62a0e7683bbcf4ab46b72c2e25b5b20d4`

原代码SHA256：`f0ec8552f53d1b2495e4e84489c0872d45cfd181aa69206d7d96f2a97f465ae2`

候选SHA256：`232e18faedac28635a89a024e5b68a428ef8425e1c463c9a9ec0ba7edde141b0`
