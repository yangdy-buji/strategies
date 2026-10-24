# 双均线交叉RSI动量策略与风险收益优化系统-Dual-Moving-Average-Cross-RSI-Momentum-Strategy-with-Risk-Reward-Optimization-System · 保守修复候选

原研究名单 #77 / SID 1990。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/a9092b7f70e2.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 空头目标减去负价差导致目标在入场价上方。

## 未解决／保持原行为

- 180按bar计数而非时钟小时，尾部TP调用绕过最短持仓；未擅自选择时长语义。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 入场100、ATR2、倍数1.5、RR2得94
- 多头目标保持106
- entry100、ATR2、mult1.5、RR2时空头目标94，多头仍106。
- 仅全文静态复核；未执行原策略、原生编译、回测或券商操作。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`双均线交叉RSI动量策略与风险收益优化系统-Dual-Moving-Average-Cross-RSI-Momentum-Strategy-with-Risk-Reward-Optimization-System.md`

原文件SHA256：`34abbec1ee8d464637d268b290af97354f789ba875dc5f76b6d56d91a0f43961`

原代码SHA256：`d9052530cb74ec91846689a6319d5b597e697a59434207ede88d41d38caca20a`

候选SHA256：`6f2f88d7214160da973ffd79d27c8174b48231bb8ad9342e443cf4f2bce6c463`
