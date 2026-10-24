# 金叉死叉长线多因子策略Golden-Cross-Death-Cross-Long-term-Multi-factor-Strategy · 保守修复候选

原研究名单 #338 / SID 5607。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/20e73fb43a48.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 合并同仓止盈止损。

## 未解决／保持原行为

- 未进行原生Pine编译、回测或订单撮合验证；批准仅限所列静态修复。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 先触目标可止盈，先触止损可止损且取消另一腿。
- 先触tpLong应全量止盈，先触slLong应全量止损，不再因另一exit预留失败。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`金叉死叉长线多因子策略Golden-Cross-Death-Cross-Long-term-Multi-factor-Strategy.md`

原文件SHA256：`708cd6367de0471f9b867c3292b9d2d2b303ff7782f2a0f2b7bbc4e9fa6b33bc`

原代码SHA256：`4589e354388bd818efad47d9db96e34646a006371910f483783602afa0b3f4d0`

候选SHA256：`f4d29cbf2247cccf8ca3d937a6ce73cdb6c2d138965e9dc9ef7cd2b622d54eed`
