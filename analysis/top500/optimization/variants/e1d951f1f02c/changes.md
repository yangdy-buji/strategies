# 多重技术指标协同交易策略系统-Multi-Technical-Indicator-Synergistic-Trading-System · 保守修复候选

原研究名单 #491 / SID 4236。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/e1d951f1f02c.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- BB返回中轨、上轨、下轨，前两项接反使图示及额外卖信号错误。

## 未解决／保持原行为

- Sell ID无入场且qty_percent=1的close无效，但真实sellSignal仍关闭Buy；未猜测做空意图。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 标准差正时upper大于basis
- MA交易条件不变
- basis100、upper110、lower90应分别绑定，附加卖出比较110。
- 仅全文静态复核；未执行原策略、原生编译、回测或券商操作。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`多重技术指标协同交易策略系统-Multi-Technical-Indicator-Synergistic-Trading-System.md`

原文件SHA256：`a044f6ed288113b285b90dbcf9ba0f3aba3dceff866cfd095de9c2540079b437`

原代码SHA256：`77a5c0e31ff308d2b55f32af83c3ce83e8401276707fde8a7436ad0a940d1603`

候选SHA256：`739c579b9701145213c5eda068b961f96c318ddd4345ae828793ca6b1a07660c`
