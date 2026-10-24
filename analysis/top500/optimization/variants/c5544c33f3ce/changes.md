# 渔夫指标移动止损策略Fisher-Yurik-Trailing-Stop-Strategy · 保守修复候选

原研究名单 #327 / SID 4877。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/c5544c33f3ce.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 日期输入恒真失效；恢复入场时间窗，退出独立。

## 未解决／保持原行为

- entryPrice/stopPrice随Fisher变化而重写，trail_offset=.08为ticks，保护激活设计待确认。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- start前不接受Fisher正区增强入场；窗内买入后finish之后原跟踪exit仍可执行。
- 核对原默认指标参数和数量配置未发生改变。
- 窗口外不入Buy但已建退出继续维护；原追踪价格与偏移不改变。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`渔夫指标移动止损策略Fisher-Yurik-Trailing-Stop-Strategy.md`

原文件SHA256：`b93813632f392a21fbd72d0a73275d26bd0f9900801563da28caf7a44fe2526c`

原代码SHA256：`87da241ca1a3beeab6eabfce26492a250a0edcbc4baa2c950a54e5497e99807a`

候选SHA256：`03d9fe280c7d369890fc28d68c3a9cab44534434a1e75248a0017538a9a74c9e`
