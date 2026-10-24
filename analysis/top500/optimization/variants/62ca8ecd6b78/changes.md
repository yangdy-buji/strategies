# 超级趋势策略SuperTrend-Strategy · 保守修复候选

原研究名单 #468 / SID 5343。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/62ca8ecd6b78.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 恢复源码中已存在的策略声明，不更改其参数。
- 恢复日期窗口与原窗外close_all。
- 只多模式反信号平仓不受日期限制。

## 未解决／保持原行为

- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 使用原Pine v4编译，恰好一个活动strategy声明；原数量与信号保持。
- 开始前和结束后有原买信号时不产生新仓，窗口内保持原信号。
- 窗口内成交，越过结束时间后仍按原止损/止盈/反向条件退出。
- LongOnly结束后Sell可退出；Both窗口外取消Long/Short未成交订单并close_all。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`超级趋势策略SuperTrend-Strategy.md`

原文件SHA256：`fdb8eff2c382e106a1c044ee55e02eaf4bcacdd2a974b70a51f7c95ed22839d9`

原代码SHA256：`a1268cf81649d33d97bff2577756427ed82673a34a858e8de68ae2347ee4b1d0`

候选SHA256：`76b72153d1fb4c236b2c30e90cd9497b9212885f720b7caa463bbb9a6b355a60`
