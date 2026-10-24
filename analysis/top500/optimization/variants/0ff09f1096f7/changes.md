# 动态均线与布林带交叉策略结合固定止损优化模型-Dynamic-Moving-Average-and-Bollinger-Bands-Cross-Strategy-with-Fixed-Stop-Loss-Optimization-Model · 保守修复候选

原研究名单 #440 / SID 1496。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/0ff09f1096f7.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 持多时更新有效均价止损。
- 持空时更新有效均价止损。

## 未解决／保持原行为

- 首次成交至首次持仓计算间仍无保证保护，反转成交时序未原生验证。
- 未进行原生Pine编译、回测或订单撮合验证；批准仅限所列静态修复。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 空仓信号后成交，下一次计算提交多头止损。
- 反转为空后按新均价设置止损。
- 空仓单次信号后信号消失，持多/持空时仍分别提交均价97%/103%止损。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`动态均线与布林带交叉策略结合固定止损优化模型-Dynamic-Moving-Average-and-Bollinger-Bands-Cross-Strategy-with-Fixed-Stop-Loss-Optimization-Model.md`

原文件SHA256：`208cdc01d670a137fb1e8b26d4127e6aaf04308b62695170b90174691c76ef91`

原代码SHA256：`56d33b83adf4d53cc81eb5246634a6d099929f700a3b75bfa2470b9570a14902`

候选SHA256：`7f910b1be3c122f662797b4d2145241895d2e4cadb4cc5b371667ce88e9ee90a`
