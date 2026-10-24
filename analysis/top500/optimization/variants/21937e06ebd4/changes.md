# 自适应布林通道动态仓位管理策略-Adaptive-Bollinger-Bands-Dynamic-Position-Management-Strategy · 保守修复候选

原研究名单 #217 / SID 5236。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/21937e06ebd4.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- time变化为毫秒差，不可能正常等于1，小时分支失效；改为非零变化，只修边界检测不声称持续一小时。

## 未解决／保持原行为

- 小时边界close>upper不等于持续一小时在上轨，卖出qty也不等于注释百分比；设计歧义未改。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- time("60")从整点递增3600000毫秒时hour_breakout可为真；同小时time不变时为假。
- 核对原默认指标参数和数量配置未发生改变。
- time60从一个时间戳增3600000时hour_breakout生效；同小时不生效。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`自适应布林通道动态仓位管理策略-Adaptive-Bollinger-Bands-Dynamic-Position-Management-Strategy.md`

原文件SHA256：`a5b034a74625838d1c9dc87f34e4c1b275c5e38043139248fdc36a841bf8bb6a`

原代码SHA256：`8e6cc55048f449308b402052b65fe9807099202fb3899cd0f0aaadc114a95714`

候选SHA256：`e1a020699da01b0dd6c843984c7fd74dd4a4a10bc00fb7bb3f2e4d831adf3624`
