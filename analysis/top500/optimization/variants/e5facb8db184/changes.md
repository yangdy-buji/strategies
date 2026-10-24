# 动态K线大阳线交易策略Dynamic-Candlestick-Big-Yang-Line-Trading-Strategy · 保守修复候选

原研究名单 #270 / SID 1434。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/e5facb8db184.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 移除信号分支na均价保护。
- 保护单独立于入场信号，在有效持仓均价存在时每根维护。

## 未解决／保持原行为

- 空头原公式以target_points作止损距离、stop_loss_points作获利距离，参数语义疑似对调待确认；首次保护要等成交后计算。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 单根阳线信号成交后没有第二信号，仍应建立Sell保护。
- 入场信号只出现一根，成交后信号消失，仍须有非na止盈和止损。
- 多仓均价100时止损在下方目标在上方；如有空仓则止损在上方目标在下方。
- 仅单根Marubozu信号后Buy仍获得保护；空头Cover使用原上方take_profit及下方stop_loss。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`动态K线大阳线交易策略Dynamic-Candlestick-Big-Yang-Line-Trading-Strategy.md`

原文件SHA256：`b0162d8ae03c089cba7cadde27b650b24accde002da50e1d252e0d2edd59ae90`

原代码SHA256：`77ffee056200190497e79c899da386f99a4e80268bc5ebc46f721b5e32221244`

候选SHA256：`870d5dd0ae5e2ee0e7165b96d9fd3b8921eccd11392c6bc2e875f04ceba121dc`
