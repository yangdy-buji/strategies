# 双移动均线与RSI反转交易策略Dual-Moving-Average-and-RSI-Reversal-Trading-Strategy · 保守修复候选

原研究名单 #357 / SID 2185。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/f8944ae554c1.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- v4使用命名空间颜色。
- v4颜色命名空间和布尔绘图类型修复，将long显式映射为1/0，仅改变展示类型。
- v4颜色命名空间和布尔绘图类型修复，将short显式映射为1/0，仅改变展示类型。
- 移除变量声明尾随逗号，避免等待另一条声明。

## 未解决／保持原行为

- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 以Pine v4编译，活动颜色引用均有color前缀；交易布尔表达式不变。
- 多头绘图为绿色，long条件和订单不变。
- 空头绘图为红色，short条件和订单不变。
- 以v4编译源码，src声明后RSI段正常解析。
- 两条件true/false分别画1/0；颜色均用color.*；entry when仍使用原布尔条件。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`双移动均线与RSI反转交易策略Dual-Moving-Average-and-RSI-Reversal-Trading-Strategy.md`

原文件SHA256：`3388736a425b4acbd2d169812ec2ebb6981a1e411583ae6f19f9ca9de94e5186`

原代码SHA256：`17dee389ceeee070ef2ed93e95819a196bf40e8c4870ed2cb53c2c7398ef931e`

候选SHA256：`177f4c27e3c317fccb14ee4040b4f3a1d8d454d84ba5c46a2558b107aa6da58a`
