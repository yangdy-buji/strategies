# 均线震荡AO指标交易策略Moving-Average-AO-Indicator-Trading-Strategy · 保守修复候选

原研究名单 #44 / SID 2528。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/ab74e505f295.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 开始结束时间未用于入场过滤；恢复函数范围，退出已经独立有效。

## 未解决／保持原行为

- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 窗口前及窗口后构造相同入场信号应被拒绝；窗口内允许原信号，已有仓位的原退出在窗外仍可执行。
- 核对原默认指标参数和数量配置未发生改变。
- startP前和end后拒绝入场，但short条件可关闭已有BUY。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`均线震荡AO指标交易策略Moving-Average-AO-Indicator-Trading-Strategy.md`

原文件SHA256：`33305c9934051da23cd272e815819defc0afc12491b17a56ad4e941f2c37ce03`

原代码SHA256：`0ed82f1ea4aec3af6dc3f125e5d7fc022e0a92f5295a0f5889e8f036f9bbe71a`

候选SHA256：`b8318adf5cb5ff9707a5cff0e0d6143775a29bc512cbbb2adaa6c1cbafff6a9b`
