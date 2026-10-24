# 基于Vix修复线性回归的低点捕捉策略Vix-Fix-Linear-Regression-Bottom-Fishing-Strategy · 保守修复候选

原研究名单 #5 / SID 2943。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/796b8b9f4242.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 原日期门禁恒真；恢复包含边界的日期范围，只作用于原入场条件。

## 未解决／保持原行为

- 止损仍受color.green限制，本轮保留。
- 未原生Pine编译/回测；静态及小范围模型不等于订单成交模拟，旧版收益不适用。

## 验证场景

- 日期五点边界；两条退出文本与颜色门禁不变。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。

- 默认止损仅在回归正值且上升的green状态生效，不是全天候ATR保护。
- 日期门禁恒true，KC参数未参与交易。

## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`基于Vix修复线性回归的低点捕捉策略Vix-Fix-Linear-Regression-Bottom-Fishing-Strategy.md`

原文件SHA256：`f4f2e0e3c7e993f8e619ab1861c9f4f3180b7cfc31b29e625549cd9f8792e852`

原代码SHA256：`134de6b56eae2bdeca3cb866b4f742d3fce420d942a851cd9fe76b10db64b835`

候选SHA256：`ecc446c29df342b99533562e1024a2828c6982dd36295a3cfd92f0f813518fff`
