# 基于多重指标筛选与动态止损的自动交易策略Auto-Trading-Strategy-Based-on-Multiple-Indicators-and-Dynamic-Stop-Loss · 保守修复候选

原研究名单 #27 / SID 3301。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/ce472780c958.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 市价平仓必须调用close，exit缺少价格参数。
- 对称修复多头市价平仓API。

## 未解决／保持原行为

- close与相反entry同次成交数量行为，以及MAX_LOSS默认0立即止亏的原设计仍需验证。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 存在SELL仓且多头条件触发时，调用close匹配SELL入场ID。
- 存在BUY仓且空头条件触发时，调用close匹配BUY入场ID；原保护价格保持。
- 多头触发时平SELL后发BUY及BUY_STOP；空头路径对称，初始绝对价保护没有新增持仓门槛。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`基于多重指标筛选与动态止损的自动交易策略Auto-Trading-Strategy-Based-on-Multiple-Indicators-and-Dynamic-Stop-Loss.md`

原文件SHA256：`3606420c72ec2e7b8b4e83f7d1698da8a66c33cc1c1d3316c990ebdd6a9da3f8`

原代码SHA256：`5c079169c5d71a62cc85210dafdcbb9f64d18eae2b8179363d45952fb9245945`

候选SHA256：`39879619be5b26f79bb8bed68f3139e066865cbb216040e978efb3fbbfdf0978`
