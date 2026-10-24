# 开盘驱动策略Open-Drive-Strategy · 保守修复候选

原研究名单 #135 / SID 4563。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/fc7336fda61a.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 多空共用exit ID，分开命名避免相互修改；限价定时退出和未使用bs/ss保护仍需设计确认。

## 未解决／保持原行为

- bs/ss计算未实际用于止损；实际退出为三根后close限价，原意图未改。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- el与es各自距信号超过3根后限价退出ID不同；两个分支同bar执行也不覆盖对应from_entry。
- 核对原默认指标参数和数量配置未发生改变。
- el与es各自等待barssince>3；空退出提交不覆盖多退出，数量2不变。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`开盘驱动策略Open-Drive-Strategy.md`

原文件SHA256：`ab034cdbb6cd80c0ab1123726ed510b2f197c29446bca24a09c14c2f6dcfc495`

原代码SHA256：`e890aa51684b6743d0f391f138ac10bab12bada51cbe02e241f16a89d2cc22e9`

候选SHA256：`6d591eb18848a5b87357aeb2b69c0841860cbb571badd6a4b2b879d6cb8e6b63`
