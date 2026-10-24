# 海龟交易三日反转策略Turtle-Trading-3-Day-Reversion-Strategy · 保守修复候选

原研究名单 #153 / SID 4851。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/d7ed73a9b021.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 恢复日期及原窗外强平。

## 未解决／保持原行为

- 原版本行// @version = 5需目标编译确认识别；未改写版本。
- 未进行原生Pine编译、回测或订单撮合验证；批准仅限所列静态修复。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 开始前不买；超过结束时间已有close_all生效。
- 窗外持多触close_all，窗内满足三日下降规则仍entry。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`海龟交易三日反转策略Turtle-Trading-3-Day-Reversion-Strategy.md`

原文件SHA256：`55597f291b57661aebb2f3d57d320a632af87f9b9ea8dffb2aebcdd921d45691`

原代码SHA256：`14e5b38f18f9e127522ef8adfc1b1ac74de75d74df7454bddf82ca0944bafcf9`

候选SHA256：`d6d659e77ea239afef4201acc2f683f9ec4d51a7731d599d1d4545558247e6f7`
