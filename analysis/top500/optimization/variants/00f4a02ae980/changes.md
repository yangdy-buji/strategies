# 动量指标均线交叉策略Momentum-Indicator-Crossover-Strategy · 保守修复候选

原研究名单 #100 / SID 1738。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/00f4a02ae980.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 日期函数恒真绕过开始日期。

## 未解决／保持原行为

- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 开始前不入场
- 日期外退出不受影响
- startP前Long忽略，startP后允许；已持仓Short仍平仓。
- 仅全文静态复核；未执行原策略、原生编译、回测或券商操作。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`动量指标均线交叉策略Momentum-Indicator-Crossover-Strategy.md`

原文件SHA256：`5fb8af3ecaa344b2064039b06e39c91581efc55f664e7bf9b2e90c8eb02b8313`

原代码SHA256：`45fe8ebdca95b811cdf2f156c06b15b834a05ede79eabdb51cb7991da06b1629`

候选SHA256：`48ff4867c41c3e86a289016503e87415a0b1e545f5ccd6e10fdf8141fb35f9fe`
