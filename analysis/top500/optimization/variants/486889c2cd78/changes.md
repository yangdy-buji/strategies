# 多层级跌幅ATH动态追踪三段买入策略-Multi-level-ATH-Dynamic-Tracking-Triple-Entry-Strategy · 保守修复候选

原研究名单 #43 / SID 3883。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/486889c2cd78.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 原警报固定1000与真实配置不符；常量消息改为明确指向buy_amount参数。
- 原警报固定1000与真实配置不符；常量消息改为明确指向buy_amount参数。
- 原警报固定1000与真实配置不符；常量消息改为明确指向buy_amount参数。

## 未解决／保持原行为

- 原层级布尔状态不等同实际成交确认；未开启加仓。
- 未原生Pine编译/回测；静态及小范围模型不等于订单成交模拟，旧版收益不适用。

## 验证场景

- 三条警报指向配置；常量消息、真实qty和订单不变。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。

- 三层显式qty但未配置pyramiding；发单即更新买过标记，拒单也可能消耗层级。
- 默认每层50000而警报称1000；无止损，平仓不重置层标记。

## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`多层级跌幅ATH动态追踪三段买入策略-Multi-level-ATH-Dynamic-Tracking-Triple-Entry-Strategy.md`

原文件SHA256：`02ce2e430748815e7aa1762cb67b30c4f7df0278c3b8358f41cdb19fb24a97b4`

原代码SHA256：`1a97aa7aab392c65a14c749c92060ad6799a149b9085550941f4b3271be6bb7b`

候选SHA256：`b88d00efc3463e0971937bea1901d66c2cefc31c79876fc7ca633cf0b9f68875`
