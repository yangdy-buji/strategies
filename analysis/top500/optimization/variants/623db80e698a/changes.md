# 多级移势均线交易策略Multi-level-Shift-Moving-Average-Trading-Strategy · 保守修复候选

原研究名单 #1 / SID 4143。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/623db80e698a.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 原结束日期分支仅全平；增加撤销未成交订单以避免后续触价成交。

## 未解决／保持原行为

- 原零qty反向entry退出语义与多层挂单敞口未修复。
- 未原生Pine编译/回测；静态及小范围模型不等于订单成交模拟，旧版收益不适用。

## 验证场景

- 仅原日期结束分支增加撤单，其他可执行文本保持。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。

- 限价成交疑点：三层qty/pyramiding及反向entry qty=0退出不被外部固定单位引擎忠实支持。
- 无硬止损；跨方向层级条件可能反手，单层默认100%权益名义敞口。
- 日线与1h绩效明显相反，日线Sharpe未超3不能排除填单假象。

## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`多级移势均线交易策略Multi-level-Shift-Moving-Average-Trading-Strategy.md`

原文件SHA256：`1860e3e1e6e6bf80db9253ffbf308535ddc7a8b95017058556a2fdeab2f11bcd`

原代码SHA256：`7bb845f51df11c513ea7e60ec725f229eb3234fa5147435c6a6d6b54d79b3cf9`

候选SHA256：`3827fc31817e8ac01802cff4866068c7301105f9f72e233a29bedf75cf523244`
