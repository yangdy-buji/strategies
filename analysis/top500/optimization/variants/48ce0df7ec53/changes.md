# 10EMA双重交叉趋势追踪策略10EMA-Double-Cross-Trend-Tracking-Strategy · 保守修复候选

原研究名单 #188 / SID 2。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/48ce0df7ec53.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 空头风险距离第二比较使用反向差值，距离大于10.40仍通过。
- 多空退出使用同一exit ID，短侧独立命名以避免同根更新覆盖其他方向退出订单。

## 未解决／保持原行为

- trail_points=low仍混合价格与tick；stop-limit入场意图需原生订单验证。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 空头风险距离11应返回na
- 空头风险距离5应返回bearentryhigh
- 距离0.5仍走最小1.00分支
- 同根执行两方向exit时使用不同ID，from_entry与止损止盈价格表达式均保持原值。
- 入场100、保护高点111时拒绝；高点105时止损105。
- 仅全文静态复核；未执行原策略、原生编译、回测或券商操作。
- 同根执行多空exit时，exit仅绑定buy、Short exit仅绑定sell，不覆盖对方订单。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`10EMA双重交叉趋势追踪策略10EMA-Double-Cross-Trend-Tracking-Strategy.md`

原文件SHA256：`58a34de7648ae6ca4abb5c795d4e52e9b1188da5004def801fb5bc97116ce745`

原代码SHA256：`a80b4048278f2966afea36d9b32ea9052eb06bb8306875ac0214333e0e2b8174`

候选SHA256：`3bc04c2c1f6a19d49d2b09afed201b6123a226d5d8736a38d7e6f80975378740`
