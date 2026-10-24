# G-Channel-Trend-Detection-Strategy-G-Channel趋势检测策略 · 保守修复候选

原研究名单 #181 / SID 379。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/a5149ca03296.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 多空保护使用不同ID，避免同ID修改。

## 未解决／保持原行为

- 止盈止损随每根close移动，是否固定锚点属于设计选择。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 先持Buy后反转Sell，两套保护from_entry各对应本方向，限价止损数值公式不变。
- Buy入场同次可创建多头保护；Sell反转时独立空头ID不会改写多头订单。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`G-Channel-Trend-Detection-Strategy-G-Channel趋势检测策略.md`

原文件SHA256：`018f1de11ff1981b34306924918efed8f7cda007401605e5913955469029d757`

原代码SHA256：`b913693edec60dea2c677ee91a98859b8b1782d00875d0f38db43f4b6ea5f07b`

候选SHA256：`022874343306239a74c0b05e84b972bd70b3d0824eecfc7cf552ea2acb79caea`
