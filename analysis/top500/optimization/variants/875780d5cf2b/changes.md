# 动态均值回归与动量策略-Dynamic-Mean-Reversion-and-Momentum-Strategy · 保守修复候选

原研究名单 #370 / SID 1494。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/875780d5cf2b.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 多空共享同一exit ID，后调用可能修改前调用订单身份；应为Short单独命名。

## 未解决／保持原行为

- ATR保护随close移动而非锁定，未改锚点设计。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 分别持Long与Short时，两套exit具有不同ID且各自from_entry正确；止盈止损仍按收盘±2ATR。
- 核对原默认指标参数和数量配置未发生改变。
- Long信号同次仍提交limit与stop；Short信号不会改写Long退出。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`动态均值回归与动量策略-Dynamic-Mean-Reversion-and-Momentum-Strategy.md`

原文件SHA256：`644dceb7271d5df2d7e7298eb7822c8b27bc8acfa24a7950b3c9e1b28e20bfbc`

原代码SHA256：`b1bfe6989e7aba875b0649d2b48570c3c925a5c74ce3c036da9160b62f6689d4`

候选SHA256：`1386b2f9787cecfe77618fb1a821098740dd629e592cc0e042a61e12b1d477bc`
