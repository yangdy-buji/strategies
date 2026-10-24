# 顿希安通道突破策略Donchian-Channel-Breakout-Strategy · 保守修复候选

原研究名单 #278 / SID 5678。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/3d1103f22fd6.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 结束时间错误引用起始年月日。
- 日期函数恒真。
- 日期函数未接入场。

## 未解决／保持原行为

- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 起止窗内信号允许入场
- 窗外不入场且仍可退出
- Start2000/End2018时2010允许买，2019不得买且可按dcAverage退出。
- 仅全文静态复核；未执行原策略、原生编译、回测或券商操作。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`顿希安通道突破策略Donchian-Channel-Breakout-Strategy.md`

原文件SHA256：`bc12d7274819f403622bdfeadcf997dd0ed672bb4d81973fae07ef696c75c17e`

原代码SHA256：`4dfff33fdfa1fc1451c29c766f9f231c3de1de83ff683aa46019a7ec1dfcf9d3`

候选SHA256：`2e6293e12ed01cca38ccbc0f0c2490220447e7e542c7aebb1f04c276749f3271`
