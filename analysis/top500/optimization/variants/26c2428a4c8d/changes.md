# 多重均线黄金交叉分批止盈策略-Multi-EMA-Golden-Cross-Strategy-with-Tiered-Take-Profit · 保守修复候选

原研究名单 #233 / SID 4224。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/26c2428a4c8d.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- Buy1未覆盖stop_loss条件，只有Buy2有止损；给Buy1增加同一止损触发，保留份额与默认加仓配置。

## 未解决／保持原行为

- 默认pyramiding可能只允许Buy1，两个半份订单是否同时成交需原生验证；入场条件会重写持仓锚点。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 假设Buy1和Buy2均已开仓，close<=stop_loss且未触目标/EMA100时两个ID均退出。
- 核对原默认指标参数和数量配置未发生改变。
- Buy1/Buy2任一持有且close<=stop_loss都发close，TP1/TP2差异保持。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`多重均线黄金交叉分批止盈策略-Multi-EMA-Golden-Cross-Strategy-with-Tiered-Take-Profit.md`

原文件SHA256：`67dcdf7b16b4e8bced24c76853fca11c05e3aa1c3cb336e8bde3ff401457267c`

原代码SHA256：`f66cadcd2034c5960db1da5b97c5b8a2e5a64eee94c5257d3366064484e8a8f3`

候选SHA256：`ab47225164a51340017e8e270206c3dbf323e80bdab70a460659e4ddc3ef3998`
