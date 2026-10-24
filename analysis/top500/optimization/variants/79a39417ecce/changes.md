# 多周期RSI超卖反转策略-Multi-Timeframe-RSI-Oversold-Reversal-Strategy · 保守修复候选

原研究名单 #14 / SID 3762。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/79a39417ecce.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- RSI退出覆盖已有额外入场ID，不改变加仓配置。
- 接入已有收盘止损布尔，并让止盈/止损覆盖两个入场ID。

## 未解决／保持原行为

- entryPrice在持续超卖时重写、平仓后不清零；buymore可在空仓依旧用旧价开新仓，且默认pyramiding使持仓加仓可能被拒。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 若已有add more仓，RSI>79时同Long一样退出；不提高pyramiding。
- entryPrice=100、默认止损1.4%，close<98.6时两个已有ID均收到close；close>103.5时同样覆盖两个ID。
- 重复买信号重设entryPrice仍保持原设计，本补丁不宣称该锚点已改进。
- Long/add more分别在RSI、TP、SL触发时均有匹配close；必须额外验证平仓后旧morebuy不会造成非预期下一笔。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。

- stopLossHit未引用：1.4%止损仅计算，不执行。
- add more入场ID没有匹配退出；qty=3与默认未开启加仓存在执行差异。
- EMA只绘图，无多周期；锚价在每根超卖信号被覆盖。

## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`多周期RSI超卖反转策略-Multi-Timeframe-RSI-Oversold-Reversal-Strategy.md`

原文件SHA256：`e1aab7e69324f8fc14e28909a498e4a764ada05bb1ed0476479e2f5d2060dc24`

原代码SHA256：`2276539b021dae6de50034ecc5d1cc7604e886dc1c021141d47f7bdd39eda936`

候选SHA256：`9040435c53a6df938e726bbb91b2d51882ced396aa1c631d989ec09fd4265ed2`
