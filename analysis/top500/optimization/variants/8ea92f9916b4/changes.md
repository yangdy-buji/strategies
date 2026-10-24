# 基于移动平均线和相对强弱指标的动量反转策略Momentum-Reversal-Strategy · 保守修复候选

原研究名单 #279 / SID 3549。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/8ea92f9916b4.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 平仓错误引用退出ID而非Buy入场ID；另takeProfit与quantityRemainder每根重置且profit单位tick，需设计分批状态。

## 未解决／保持原行为

- takeProfit和quantityRemainder每根重置，profit参数tick单位与百分比混用、部分退出状态设计仍未解决。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- closeOverbought=false且RSI>70、已持Buy时close应匹配Buy而非退出IDTake Profit。
- 核对原默认指标参数和数量配置未发生改变。
- closeOverbought=false且RSI>70时关闭Buy；true时原部分退出分支保持。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`基于移动平均线和相对强弱指标的动量反转策略Momentum-Reversal-Strategy.md`

原文件SHA256：`7dbec366748c87e46670e3744dae54b4f7e6979c35829def7bd92329409a3aa2`

原代码SHA256：`a7658764b4e9a3b317f5c591754dd8f6a5c69100779ca081584b1153a526739e`

候选SHA256：`1ad526f230a4a753ce431c80fc7f51d5eae0e17cb0aa0ecc0394999750e5e057`
