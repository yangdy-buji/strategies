# 均线交叉长线并量化策略EMA-Crossover-for-Long-Line-Quant-Strategy · 保守修复候选

原研究名单 #56 / SID 2486。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/949e2f5fb09a.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 恢复入场日期。
- 退出移出日期限制。
- 退出移出日期限制。

## 未解决／保持原行为

- pyramiding变量只是数量乘数，未设置平台加仓参数。
- 未进行原生Pine编译、回测或订单撮合验证；批准仅限所列静态修复。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 日期外不再开仓。
- 窗口结束仍可按原规则平仓。
- 结束后四个Buy ID均可由同一exit条件关闭，但不可新增买单。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`均线交叉长线并量化策略EMA-Crossover-for-Long-Line-Quant-Strategy.md`

原文件SHA256：`897516abaf09ff804f046c6f914742063fa6766a2667031529e346522eada76c`

原代码SHA256：`5fa64f9bd60330ee02933ceaad66ef09b8dff15418b0ac9f915ee31a280489fb`

候选SHA256：`e7a5a6638d8d1fd2128bb31f5d72c56f7037e6e32aa1fcb41d429454f57a9211`
