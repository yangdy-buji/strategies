# 高级量化趋势追踪与云图反转复合交易策略-Advanced-Quantitative-Trend-Following-and-Cloud-Reversal-Composite-Trading-Strategy · 保守修复候选

原研究名单 #277 / SID 5753。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/2c1b99697677.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 拆分空头保护ID，保持原动态价格公式。

## 未解决／保持原行为

- senkouSpanA是和的两期SMA近双倍价，其他一目线亦非典型定义，模型需确认。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- Sell仓位由独立空头退出ID保护；Buy退出不被第二调用修改。
- Buy首次入场同次仍有保护；Sell反转时独立保护ID，公式保持。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`高级量化趋势追踪与云图反转复合交易策略-Advanced-Quantitative-Trend-Following-and-Cloud-Reversal-Composite-Trading-Strategy.md`

原文件SHA256：`9c250c38316ce0e9333a489f4f5c0785046992c2554ea2ebdef5c3dd1956061a`

原代码SHA256：`c82e2664e82ba87f3ecfe03f55fd1c0ad32ff5ec6008c96e410b80aafc5fdbcf`

候选SHA256：`7e7067cdcea1be16f89f44fe7fe7ca5ad3fcf139342d4c4cd3f5cddc2c562b02`
