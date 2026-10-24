# 平滑海坚线买卖策略Heikin-Ashi-Smoothed-Buy-and-Sell-Strategy · 保守修复候选

原研究名单 #463 / SID 4534。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/00702b798dcb.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- HA低点应包含开收较小值，max可令低点高于开或收。

## 未解决／保持原行为

- 补丁只影响图形，买卖仍基于HA实体趋势。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- haOpen低于maLow时haLow不得高于haOpen
- 买卖条件不变
- maLow100、haClose105、haOpen95时haLow应95。
- 仅全文静态复核；未执行原策略、原生编译、回测或券商操作。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`平滑海坚线买卖策略Heikin-Ashi-Smoothed-Buy-and-Sell-Strategy.md`

原文件SHA256：`929380fa8c0fa6eed95dbc2cde8e5fb7f7631299f5c79110f2b2827b2069b11d`

原代码SHA256：`61e952a4373d777474fc7261d7e114abca04e517cfe19fa95e983f068ed780f3`

候选SHA256：`024b9d782c7dcd16c22dcbfd25856aa25d2ed69c9e09063fd3c066ca9e174f17`
