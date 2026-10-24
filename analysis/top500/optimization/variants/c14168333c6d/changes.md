# 三重均线趋势追踪多指标组合量化交易策略-Triple-EMA-Trend-Following-Multi-Indicator-Quantitative-Trading-Strategy · 保守修复候选

原研究名单 #356 / SID 1223。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/c14168333c6d.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- ta.dmi依次返回+DI、-DI、ADX，现把+DI当ADX门槛。

## 未解决／保持原行为

- riskAmount计算仍未用于qty，未改变原默认仓位。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 目标Pine版本编译通过
- 检查声明绑定与对应指标输出一致
- DI+=35、DI-=15、ADX=20时不得因35误过25阈值。
- 仅全文静态复核；未执行原策略、原生编译、回测或券商操作。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`三重均线趋势追踪多指标组合量化交易策略-Triple-EMA-Trend-Following-Multi-Indicator-Quantitative-Trading-Strategy.md`

原文件SHA256：`a4b721361c2d7616e6cbfb720b8eab61605ac6e1334dc0a323cd374e0d79a38b`

原代码SHA256：`f54ab3bce4879c7b73fe787c32b5b450fa58587f52dfd5c00b130663ecb84f04`

候选SHA256：`380dcebdb398f5dc6d2104fd2700a795ebff5ae7a2b39315ffb30c4d02b57c47`
