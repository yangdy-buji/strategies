# 三指数均线止盈止损策略Triple-Exponential-Moving-Average-Profit-Taking-and-Stop-Loss-Strategy · 保守修复候选

原研究名单 #353 / SID 1187。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/a70e49f27418.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 使日期输入生效
- 退出不受日期门禁限制

## 未解决／保持原行为

- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 起止内允许入场
- 结束之后不入场且close_all仍执行
- 结束后死叉仍允许平仓
- 结束日之后已有Long遇fastEMA下穿仍退出，窗外交叉不得开仓。
- 仅全文静态复核；未执行原策略、原生编译、回测或券商操作。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`三指数均线止盈止损策略Triple-Exponential-Moving-Average-Profit-Taking-and-Stop-Loss-Strategy.md`

原文件SHA256：`0dc68fad2dd2736a32f863cf55e9521fd66c48448c758a1f77748cf5707a674d`

原代码SHA256：`528014f13e00beef5cbca314f72e80c730265811269392ef0e1d3cf85bc2743b`

候选SHA256：`36f3f20f2c4ac7d68d2c455c967676cc8657eec61896ab7e88d342cba1004251`
