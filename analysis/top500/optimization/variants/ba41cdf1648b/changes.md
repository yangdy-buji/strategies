# 超级趋势反转策略Super-Trend-Reverse-Strategy · 保守修复候选

原研究名单 #312 / SID 5335。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/ba41cdf1648b.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- TrendDown重置错误使用下方UP而非上方DOWN。
- 平多不应被日期窗阻断。

## 未解决／保持原行为

- 入场日期仍为年/月/日独立比较，跨年范围语义非连续时间窗，需单独设计确认。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 重置空头趋势线为hlc3加ATR
- TrendUp保持不变
- 窗口外反向信号仍平多
- 入场日期条件不变
- 上根价格高于TrendDown时新TrendDown=hlc3+FactorATR；窗外shortCond平BUY。
- 仅全文静态复核；未执行原策略、原生编译、回测或券商操作。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`超级趋势反转策略Super-Trend-Reverse-Strategy.md`

原文件SHA256：`2af06eb599b93e3ba810322f9d0974860b6070cda03ee0a54371fe57e0b34a32`

原代码SHA256：`0feb98ec14215c268ebdf8d13f6f0dbd3b67c382592a9bb25a6c7a34b3b0eb49`

候选SHA256：`a2f45dd21570b410765eb0ad4e108c87839797476894a1b6a48f4a37565ca9e6`
