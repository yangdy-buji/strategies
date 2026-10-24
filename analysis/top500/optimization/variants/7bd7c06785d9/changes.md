# Darvas-Box-Breakout-and-Risk-Management-Strategy-Darvas-盒子突破与风险管理策略 · 保守修复候选

原研究名单 #306 / SID 235。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/7bd7c06785d9.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- boxp允许1或2使boxp-2非正，highest长度无效；最小合法长度应为3。

## 未解决／保持原行为

- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- boxp=3时k3长度为1且可计算；UI应拒绝boxp=1或2；默认boxp=5信号完全相同。
- 核对原默认指标参数和数量配置未发生改变。
- boxp=3使k3长度1；拒绝1、2，默认5的箱体和买卖条件不变。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`Darvas-Box-Breakout-and-Risk-Management-Strategy-Darvas-盒子突破与风险管理策略.md`

原文件SHA256：`03fcd4aca60ddd498e52e6e4f8940327b03c73689bb338717572ca7a3c1ea1c5`

原代码SHA256：`e800104fd8a729ba25b3abe106d2b25b5e4766f591c461747738d25ba1f2bda8`

候选SHA256：`370f072c3b27f2d88758c4bcb434cc36075c75e0295b04ac6c447523c2bd5e92`
