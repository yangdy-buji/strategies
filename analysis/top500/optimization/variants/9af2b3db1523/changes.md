# 长期趋势SMA均线交叉量化策略-Long-term-Trend-SMA-Crossover-Quantitative-Strategy · 保守修复候选

原研究名单 #464 / SID 5613。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/9af2b3db1523.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 日期过滤开关和起止输入被恒真绕过。
- 退出不能受日期门禁。

## 未解决／保持原行为

- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 起止窗内信号允许入场
- 窗外不入场且仍可退出
- useDateFilter=false时窗外entry允许；true时禁止，但既有Long Entry仍可退出。
- 仅全文静态复核；未执行原策略、原生编译、回测或券商操作。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`长期趋势SMA均线交叉量化策略-Long-term-Trend-SMA-Crossover-Quantitative-Strategy.md`

原文件SHA256：`efee190d9ed91891e9b2dd7370bde179efb453e8cf85c8857abf3b707fb60661`

原代码SHA256：`f1be2b2a417f676154ed7e87be198d9613a2155c0352c5c99d11786119ec08b6`

候选SHA256：`98752baef8f98dcf99031a774a8c9589813853b4451437caf0766fcd517ecf62`
