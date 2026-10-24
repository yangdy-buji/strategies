# 双均线交叉与随机指标结合的自适应追踪止损策略-Dual-Moving-Average-Crossover-with-Stochastic-Filter-and-Adaptive-Trailing-Stop-Strategy · 保守修复候选

原研究名单 #378 / SID 1994。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/cecdd28451f4.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 只在对应方向已有实际持仓时持续提交均价保护，避免反向待成交订单使用旧方向均价。
- 只在对应方向已有实际持仓时持续提交均价保护，避免反向待成交订单使用旧方向均价。

## 未解决／保持原行为

- 首次成交/反手成交后至下一次策略计算前仍无该方向保护；不承诺入场bar内止损。
- 保本条件仍按当前close计算，回落后可退回原SL；未擅改为单向追踪。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 持仓后即使没有新信号也更新本方向保护。
- 反手信号当根不使用旧方向均价提交新方向保护；新方向成交后下一计算才创建保护，首次成交到该计算仍有空窗。
- Long实仓无buySignal仍更新Long Exit；Short待成交时不以Long均价挂Short Exit。
- 新Short成交且下一计算均价100时挂shortSL102、shortTP96。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`双均线交叉与随机指标结合的自适应追踪止损策略-Dual-Moving-Average-Crossover-with-Stochastic-Filter-and-Adaptive-Trailing-Stop-Strategy.md`

原文件SHA256：`d72478c14f89f54b020e77c75e7b5aa055bd2a827b311a85edecd5aca5fe3bb6`

原代码SHA256：`8c7b32e6ac2d458a89e2d43efc6c5425d49d472380b532dc6941b5f172db5866`

候选SHA256：`f799e704c88b11cde0e3f182b8599fa0a324429e8a50e55cb32055a7d58f633f`
