# Swing-Highs-Lows-Candle-Patterns · 保守修复候选

原研究名单 #448 / SID 977。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/20f66db952db.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- study声明与strategy.entry并存不能作为有效策略编译；替换策略声明。

## 未解决／保持原行为

- beareng复制bulleng公式，但当前只用于未使用的展示文本；ph做多/pl做空方向是否符合策略意图需确认。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 用Pine v4编译时存在一个strategy声明并允许已有strategy.entry；高低枢轴信号和方向保持。
- 核对原默认指标参数和数量配置未发生改变。
- 保留ph优先、pl次选的两方向entry；声明只出现一次且仍为v4。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`Swing-Highs-Lows-Candle-Patterns.md`

原文件SHA256：`36600c57d79789d7a911b8619ba0fe64ec8c3a871b9340cb6c1846b81fa92f49`

原代码SHA256：`ec508428624c573ed20dc0905170ff56cef2f42519d9d54fb97c0dc198defab8`

候选SHA256：`510eb151b84c91308b9ecd03afe72f46d297e6dbf89ba9b814be53eac7675fad`
