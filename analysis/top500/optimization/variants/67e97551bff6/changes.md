# 基于多重技术指标的高频交易动态优化策略-Multi-Technical-Indicator-Based-High-Frequency-Dynamic-Optimization-Strategy · 保守修复候选

原研究名单 #379 / SID 3295。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/67e97551bff6.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- DMI返回顺序为+DI、-DI、ADX。

## 未解决／保持原行为

- 均价保护只在空仓入场分支计算为na，仍可能没有止盈止损；应独立修复其生命周期。
- 未进行原生Pine编译、回测或订单撮合验证；批准仅限所列静态修复。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 过滤读取第三返回值ADX。
- 给DMI返回10/30/40，adx>20应真而不是以10判断。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`基于多重技术指标的高频交易动态优化策略-Multi-Technical-Indicator-Based-High-Frequency-Dynamic-Optimization-Strategy.md`

原文件SHA256：`adfdaca878fa8230857a5bcbc58285c607d9da4d69f2fd27c69e92b1245b5373`

原代码SHA256：`c2923d1dfb85ceafddf8e570b0db21a4d4ffbb1a1abaa4cff417a06cc83a2465`

候选SHA256：`3f8f057cff6c273cedc9b216ea2c09c35ff3f420af7b6b8f542545d906bc19dc`
