# 白盒冰山策略Robot-White-Box-Iceberg-Strategy · 保守修复候选

原研究名单 #7 / SID 4941。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/4a401c623419.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 原needtime恒真；按既有日期参数恢复严格起止时间条件（边界不入场）。
- 原窗口外可能遗留入场限价单；在窗口外逐次撤销六个入场ID。

## 未解决／保持原行为

- 原零qty退出、总敞口与边界全平时点未重写。
- 未原生Pine编译/回测；静态及小范围模型不等于订单成交模拟，旧版收益不适用。

## 验证场景

- 窗外六个入场ID撤销；TPL/TPS保留；原期末全平分支不变。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。

- 限价、三层qty/pyramiding、持仓后冻结层级与qty=0反向退出均超出外部固定单位保真范围；Sharpe阈值不排除填单假象。
- 没有真实冰山隐藏量或盘口执行模型，也无硬止损。
- 开始日期失效，needtime恒true，结束时间仅末尾全平撤单。

## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`白盒冰山策略Robot-White-Box-Iceberg-Strategy.md`

原文件SHA256：`2ee97c3e5f0eb56a6bcbbc73e569ab101709ea0d36b30bd61b4cc8f895ae6ae3`

原代码SHA256：`4b9e623bcedc5a8df8fb46bb83bd1aa5d20f40fe41e0c340ce86586095737b7b`

候选SHA256：`3c3b23a446dc62c7f5804abdd89d49da74fbdeb0aa921cbc0abf0c6681a1fe77`
