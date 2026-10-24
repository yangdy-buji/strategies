# 基于双移动平均线交叉的回调入场策略EintSimple-Pullback-Strategy · 保守修复候选

原研究名单 #292 / SID 3172。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/21b4c90411d4.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 恢复入场时间窗。

## 未解决／保持原行为

- 原版本行是// @version=5，需在目标Pine确认编译器识别；stopDistance分母及信号后open估价保持。
- 未进行原生Pine编译、回测或订单撮合验证；批准仅限所列静态修复。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 窗前窗后不入场，已有仓位退出不受限。
- 起点相等允许开仓；窗外stopCondition仍可close Long。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`基于双移动平均线交叉的回调入场策略EintSimple-Pullback-Strategy.md`

原文件SHA256：`256e60aced2641ca55fa0a1b2aeda968117d15fed543982af4e68c0afaf9b6b8`

原代码SHA256：`b4d83ee54703a552fc21457ef7cd6e47b055dc699dcfc9efb1563d0d4be00c53`

候选SHA256：`e4b4081bf0a54659813a52e45f0a2533be4f27c5df72bd59d562542bd717bc14`
