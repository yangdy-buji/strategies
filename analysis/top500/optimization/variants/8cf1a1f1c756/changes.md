# 高级斐波那契回调与成交量加权价格行为交易策略-Advanced-Fibonacci-Retracement-and-Volume-Weighted-Price-Action-Trading-Strategy · 保守修复候选

原研究名单 #57 / SID 5741。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/8cf1a1f1c756.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 数组每根新建归零，非更新bar比较0导致信号失真；应持久保存水平。另高低重置顺序与pinbar方向需设计确认。

## 未解决／保持原行为

- 更新bar先把fibHigh/Low重置为本根再计算，未利用区间极值；pinbar多空影线方向与通常语义相反，待设计确认。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 连续两根非fibLength倍数bar，fibonacciLevels应保持最近更新的5个值而非重置0；更新bar继续原计算。
- 核对原默认指标参数和数量配置未发生改变。
- bar_index=20更新后21..39保持相同数组；40仍按原本根高低计算五值。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`高级斐波那契回调与成交量加权价格行为交易策略-Advanced-Fibonacci-Retracement-and-Volume-Weighted-Price-Action-Trading-Strategy.md`

原文件SHA256：`f0dbe549f62a5bc9ee7869dc7b6611bc38d79c9b3a8181923aaf1c7a90a65110`

原代码SHA256：`3a63775c03fa18c7dc4e1ce1904a3a6e5f7be8285830f0bcd05f47d69acc6123`

候选SHA256：`561b67a79798cdd98fceba6bb6edf0735d96936c42077613d0c512e66a6a3720`
