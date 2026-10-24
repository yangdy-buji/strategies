# 基于自适应移动平均线的趋势跟踪策略Trend-Following-Strategy-Based-on-Adaptive-Moving-Average · 保守修复候选

原研究名单 #482 / SID 3599。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/055045ca7d7d.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 版本注解格式错误。

## 未解决／保持原行为

- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 原版本编译检查
- 原信号正常且退出分支保持有效
- 同一KAMA序列生成相同long/longClose布尔表达式。
- 仅全文静态复核；未执行原策略、原生编译、回测或券商操作。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`基于自适应移动平均线的趋势跟踪策略Trend-Following-Strategy-Based-on-Adaptive-Moving-Average.md`

原文件SHA256：`762776eb6d85b19be17830018a042cca00d4c94c2958b60bae8761528531aec4`

原代码SHA256：`30097c104435777e8031106e36a51a23972807327e50d77d33d0ef49cbf8c286`

候选SHA256：`2b9ba89f7bc4706a7b765652cf97f4833ea033f2a4554f8d803a3ab5cc76e890`
