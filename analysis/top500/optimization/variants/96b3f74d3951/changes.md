# 多重指标动量突破趋势交易策略-Multi-Indicator-Momentum-Breakout-Trend-Trading-Strategy · 保守修复候选

原研究名单 #214 / SID 4271。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/96b3f74d3951.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 绝对价格传入tick距离参数loss/profit，退出价格失真。
- 绝对价格传入tick距离参数loss/profit，退出价格失真。
- 多空退出使用同一exit ID，短侧独立命名以避免同根更新覆盖其他方向退出订单。

## 未解决／保持原行为

- 首笔均价na空窗及反手时旧均价引用仍需原生验证。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 均价100多头止损98目标103
- 空头止损102目标97
- 同根执行两方向exit时使用不同ID，from_entry与止损止盈价格表达式均保持原值。
- 均价100、SL2%/RR1.5时Long stop98 limit103、Short stop102 limit97。
- 仅全文静态复核；未执行原策略、原生编译、回测或券商操作。
- 两方向exit拥有不同ID且各自from_entry仍为Long/Short。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`多重指标动量突破趋势交易策略-Multi-Indicator-Momentum-Breakout-Trend-Trading-Strategy.md`

原文件SHA256：`cc1f358fd5ba5521b6c66de74ab85a10964d687f188b8cf130142c81501a012a`

原代码SHA256：`0b0f19b9c0dee9d91406156a08b1ea796f98c451deeff0e4ec9baf67d3e34d5a`

候选SHA256：`6143aa480ac300cfacaa828161178830a76799402916de3186eb55f36cbeae0f`
