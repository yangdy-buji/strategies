# 基于移动平均线的动量策略This-strategy-is-a-momentum-strategy-based-on-moving-average-lines · 保守修复候选

原研究名单 #229 / SID 3553。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/2de06f53b9b6.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 日期函数恒真绕过输入。
- 卖信号用于平多时不能受日期窗口影响。
- 仅反手空入场需要窗口，窗外仍平多。

## 未解决／保持原行为

- 原Short无独立止盈止损，窗外buy被禁也不能反手平Short；需确定Short退出政策。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 原版本编译检查
- 原信号正常且退出分支保持有效
- enableShorts=true且窗外SHORT信号应只平Long不建Short。
- 仅全文静态复核；未执行原策略、原生编译、回测或券商操作。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`基于移动平均线的动量策略This-strategy-is-a-momentum-strategy-based-on-moving-average-lines.md`

原文件SHA256：`096f9468f2a6d1b1d3b204caea93210387c36cdf570973cad81b67a99fecee80`

原代码SHA256：`04421df0ff656522c7c98735a68d9afeea5f285a7c4473b9e2bda557f824c1d5`

候选SHA256：`6aee6c29821dd203f4811b590522aff8f8856d9d9ca224e10ccecfa2467e638c`
