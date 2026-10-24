# 基于高斯通道和随机RSI的市场趋势捕捉策略-Gaussian-Channel-and-Stochastic-RSI-Based-Market-Trend-Capture-Strategy · 保守修复候选

原研究名单 #454 / SID 3713。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/65f8f252b249.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 恢复日期。
- 退出脱离窗口。

## 未解决／保持原行为

- StochRSI最高最低相等时除零和上下轨命名混淆保持。
- 未进行原生Pine编译、回测或订单撮合验证；批准仅限所列静态修复。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 窗外不新开仓。
- 窗后越上轨仍退出。
- 窗外priceAboveUpper仍平Long，priceBelowUpper且stochUp不再开仓。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`基于高斯通道和随机RSI的市场趋势捕捉策略-Gaussian-Channel-and-Stochastic-RSI-Based-Market-Trend-Capture-Strategy.md`

原文件SHA256：`67cd2a5231cf2bb0cdeab8fd78b2d4f1f0cbfb00723fd95ee1f427abd19413c8`

原代码SHA256：`ac6346a27bb01a4a5690c7dc49538be170a7aa01c8f1e65e807615d72989d113`

候选SHA256：`a1c00c963ebc4013c71fae636cce2fb5a6aea5a34ab4296c72af6236a0df13cf`
