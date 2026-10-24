# 基于双EMA交叉的量化交易策略Quantitative-Trading-Strategy-Based-on-Double-EMA-Crossover · 保守修复候选

原研究名单 #465 / SID 3121。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/888b5fc2d522.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 启用开始时间开关。
- 只将时间门槛保留在entry，退出独立。

## 未解决／保持原行为

- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 窗口前、起点、终点及窗口后各构造相同入场信号：只允许窗内新仓。
- 窗口结束前已有持仓，结束后出现原退出条件：退出调用仍可执行，不因日期而关闭保护。
- 开关false允许开始前入场；true时禁止；buy_exit_condition全时可平已有仓位。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`基于双EMA交叉的量化交易策略Quantitative-Trading-Strategy-Based-on-Double-EMA-Crossover.md`

原文件SHA256：`1a96e5fc1f125dda2635f12247af10d1fcec467871c8cab0345932949c44acc9`

原代码SHA256：`2254ec9843f6f33081dadabd80c8d98665078035288a4cb9d80841bd208d6979`

候选SHA256：`799427554bddf3898d5a65afd239eb5e941fd743c3fe360ed9569a5bf47c75d6`
