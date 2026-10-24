# 双重确认的优势均线策略A-Dual-Moving-Average-Confirmation-Advantage-Line-Strategy · 保守修复候选

原研究名单 #126 / SID 2324。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/b94c77d91d7f.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 日期恒真绕过输入。
- 退出必须在日期窗外继续。

## 未解决／保持原行为

- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 原信号参数不变
- 相关条件边界及持仓退出验证
- 结束日后longexit可平long，long不可新开。
- 仅全文静态复核；未执行原策略、原生编译、回测或券商操作。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`双重确认的优势均线策略A-Dual-Moving-Average-Confirmation-Advantage-Line-Strategy.md`

原文件SHA256：`cf90d23c8016f22639dc270e04246034d6600ba2562ce42a1b3b7eaf8e153622`

原代码SHA256：`28834e3a4f4b9236bf30f79215582035d59ad59696997ef1765789a0686da4b2`

候选SHA256：`283cb02df6663538129ee6cf437da34571b62635fdc04f38c2865e4bcb5e26dd`
