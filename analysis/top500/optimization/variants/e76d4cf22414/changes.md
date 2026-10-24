# 移动平均聚合动量云策略-Moving-Average-Convergence-Momentum-Cloud-Strategy · 保守修复候选

原研究名单 #125 / SID 5084。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/e76d4cf22414.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 修复展示返回值。

## 未解决／保持原行为

- 未进行原生Pine编译、回测或订单撮合验证；批准仅限所列静态修复。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- BB Middle显示SMA20，BB Upper显示SMA20+2标准差。
- 返回100/120/80时三条图分别正确；交易条件文本不变。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`移动平均聚合动量云策略-Moving-Average-Convergence-Momentum-Cloud-Strategy.md`

原文件SHA256：`0ee7eb419b44cf843a3b3d42563fef0ccc1d314a7c6bd9e5de982f6a00feb688`

原代码SHA256：`044da6b37d256fab18e160b4bf5afd0f01cdbfad5341cddf052c2f8751dc6d07`

候选SHA256：`f4cb6899b783baff9dcefcf9c85f569d8f07278048ca270283f72b17b5351c9e`
