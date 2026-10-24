# 形态识别吊颈线交易策略Pattern-Recognition-Pinbar-Trading-Strategy · 保守修复候选

原研究名单 #63 / SID 4573。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/f8fc04aadb35.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 恢复开始日期开关。
- 保留原始多头形态供窗外退出使用。
- 保留原始空头形态供窗外退出使用。
- 日期仅限制多头入场。
- 日期仅限制空头入场。
- 独立空头退出ID避免修改多头保护。
- 独立空头退出ID避免修改多头保护。

## 未解决／保持原行为

- 追踪分支缺trail_offset，当前仅stop可用，追踪距离设计仍未给出；barsSinceEntry动态历史引用需原生验证。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 开始前和结束后有原买信号时不产生新仓，窗口内保持原信号。
- 窗口内成交，越过结束时间后仍按原止损/止盈/反向条件退出。
- 跟踪开关真/假分别验证Sell保护from_entry为sell，Buy保护不被空头调用覆盖。
- 分别isTrailingStop=true/false检查sell独立ID；窗外相反信号仍可触发close而不新开仓。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。

- 默认trail_price未提供trail_offset，不能认定追踪止损有效。
- 振幅取成交K而非信号K；日期输入未接入。

## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`形态识别吊颈线交易策略Pattern-Recognition-Pinbar-Trading-Strategy.md`

原文件SHA256：`9f67d1c7add16774126c0333cc20665e6dae0bec70161237ab21027ba00f5185`

原代码SHA256：`0db62a6eb9502249ec2b685ad36c6cf00101be4b83b6108c218b8edad83fb188`

候选SHA256：`7c7ff65cd80004df1f93ded0b3141ec2ae3a7efa2564ac498ca20032e0e29461`
