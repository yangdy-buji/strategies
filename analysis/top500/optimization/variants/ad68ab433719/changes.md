# 基于月季线均线操作的量化交易策略Quant-Trading-Strategy-Based-on-Monthly-and-Quarterly-Moving-Average-Operation · 保守修复候选

原研究名单 #205 / SID 3460。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/ad68ab433719.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 开始日期被if true绕过，直接门控入场且退出保持不变。

## 未解决／保持原行为

- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 保持正常入场信号
- 无新信号持仓和窗外退出仍有效
- 开始日前to_long为真不买，之后允许；已持仓10%亏损仍平。
- 仅全文静态复核；未执行原策略、原生编译、回测或券商操作。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`基于月季线均线操作的量化交易策略Quant-Trading-Strategy-Based-on-Monthly-and-Quarterly-Moving-Average-Operation.md`

原文件SHA256：`90b70e59d2e49a64ed246def2cd6d93452ff7d22648bb12ea33080affe074b91`

原代码SHA256：`ee26424a87ced61d48bc7de6ee82c338f4cd4131a2f1b99fd3a7ca16b5fb8a9a`

候选SHA256：`27d76047e6935ed5f0a0fb243d21cb96cbc63084f7817c7acefd31c16a764c47`
