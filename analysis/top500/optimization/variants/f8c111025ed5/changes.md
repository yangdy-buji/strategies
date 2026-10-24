# 量化策略之MA强弱趋势追踪Quantitative-Strategy-of-MA-Strength-Trend-Tracking · 保守修复候选

原研究名单 #492 / SID 5583。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/f8c111025ed5.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 日期输入失效；恢复入场范围，独立平仓继续有效。

## 未解决／保持原行为

- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- inDateRange窗外阻止Buy与Sell新仓，原strategy.close两方向退出不被窗口阻止。
- 核对原默认指标参数和数量配置未发生改变。
- Buy/Sell各自窗外退出仍工作；tradeDirection限制保持，窗口内数量配置不变。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`量化策略之MA强弱趋势追踪Quantitative-Strategy-of-MA-Strength-Trend-Tracking.md`

原文件SHA256：`157d570c52c81a5e66cdb301ac43b8932606956c84ed2ef64da7c60995a55c54`

原代码SHA256：`780a4a679c41276ed62efbef2d76d8694592897fd0584b5cec9526e22660fa32`

候选SHA256：`c546dadd809fb3909f55b59367045243981fff1435921e8f64468f0f04553d48`
