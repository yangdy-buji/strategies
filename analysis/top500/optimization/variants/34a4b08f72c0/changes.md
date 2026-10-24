# 动量自适应高斯通道多周期策略-Momentum-Adaptive-Gaussian-Channel-Multi-Period-Strategy · 保守修复候选

原研究名单 #21 / SID 1791。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/34a4b08f72c0.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 季节逻辑固定OR只支持跨年；起月早于止月时全年均为真，须同时支持非跨年范围。

## 未解决／保持原行为

- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 起月9止月2时9/12/1/2月为真、6月为假；起月3止月8时4月为真、1/12月为假。
- 核对原默认指标参数和数量配置未发生改变。
- 测试3月至8月只含3..8；9月至2月含9..12和1..2；相同月份只包含该月。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`动量自适应高斯通道多周期策略-Momentum-Adaptive-Gaussian-Channel-Multi-Period-Strategy.md`

原文件SHA256：`c90e3feed6725cae827031f7564f22d6632b3777c2e8204f0879c334468295a8`

原代码SHA256：`c695c3b877fb0df44c12eb40f33623e088f16d88b8cc5e31cb7e027686498f55`

候选SHA256：`ba43fe5b121ebfe2ce141a80a21e036663e9e5fdc0bbf80b2e1f7e48da4dc54a`
