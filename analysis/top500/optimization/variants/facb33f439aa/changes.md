# 双轨跟踪震荡分型策略Dual-track-Oscillator-Pattern-Strategy · 保守修复候选

原研究名单 #458 / SID 2251。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/facb33f439aa.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 日期函数恒真。
- 平仓不应被日期阻断。

## 未解决／保持原行为

- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 窗口外入场关闭
- 窗外Sell仍退出
- 窗外Buy无订单，窗外Sell关闭既有多头。
- 仅全文静态复核；未执行原策略、原生编译、回测或券商操作。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`双轨跟踪震荡分型策略Dual-track-Oscillator-Pattern-Strategy.md`

原文件SHA256：`a7fe714e6bc988900036e5fb39624b9bbe8df475c445edf22efc87eefb7e5bb5`

原代码SHA256：`e4d9b092e9adacf9841d8a76c202bb0c5cf578074dd02abd3a9e6a6be16365e9`

候选SHA256：`20a659bbee24c07730118b4fb14e08413ee8b865710ce344e4681ac8bf37fb12`
