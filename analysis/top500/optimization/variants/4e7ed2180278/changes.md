# 多重均线交叉动量趋势跟踪策略-Multi-EMA-Crossover-Momentum-Trend-Following-Strategy · 保守修复候选

原研究名单 #361 / SID 4197。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/4e7ed2180278.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 多空退出复用同一ID，拆分空头退出ID避免修改已有多单保护。

## 未解决／保持原行为

- 固定入场价还是动态收盘价保护需要设计确认。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- Buy和Sell先后出现时退出ID不同；空仓保护仍计算原收盘动态比例，不覆盖多头订单身份。
- 核对原默认指标参数和数量配置未发生改变。
- Buy和Sell反转时from_entry仍对应，任何一侧退出不能被另一侧同ID覆盖。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`多重均线交叉动量趋势跟踪策略-Multi-EMA-Crossover-Momentum-Trend-Following-Strategy.md`

原文件SHA256：`c3f6205c90397d8dfe45ae30436d005fbafd99a5bd91d836b768a9def1debbe1`

原代码SHA256：`ee5136aeeff1f9719fc7309ec094673fd855fa049ccf89fbb360c2a46d4b7e40`

候选SHA256：`456854af7a89cbc15f7e0088faf10c3938822e203170504d215537d329f0a5c5`
