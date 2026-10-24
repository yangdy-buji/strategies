# 多空均衡移动平均趋势跟随策略Multi-factor-Moving-Average-Trend-Following-Strategy · 保守修复候选

原研究名单 #186 / SID 4127。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/4e83b578222c.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 窗口函数恒真。
- 保持窗外持仓退出。
- 只允许窗口内新入场。

## 未解决／保持原行为

- 手工持仓标志仍假设订单成交；不改变历史撮合行为。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 目标版本编译检查
- 边界和持仓退出检查
- 窗内bPositionOpened为true跨窗后跌破stopLossPrice仍关myPosition。
- 仅全文静态复核；未执行原策略、原生编译、回测或券商操作。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`多空均衡移动平均趋势跟随策略Multi-factor-Moving-Average-Trend-Following-Strategy.md`

原文件SHA256：`e9b78cbf92b9e517377a74354a969957afde377fb456d50c8d7a213bc955fcc7`

原代码SHA256：`56c6fefc42cb42142e8ac1212e4127fc337eafe453add82735cd77ea2f14586c`

候选SHA256：`d0a84040757e2e13d1ba3b4b811e2a596b003cb79dcfaa1b97dca9a4d0b87b18`
