# 经典移动平均线交叉策略Moving-Average-Crossover-Strategy · 保守修复候选

原研究名单 #225 / SID 5171。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/6b274e0d6b7e.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 恢复日期入口。
- 退出移出日期。

## 未解决／保持原行为

- 未进行原生Pine编译、回测或订单撮合验证；批准仅限所列静态修复。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 开始前不买。
- 结束后死叉仍平多。
- 窗外死叉能close Long；入口嵌套if仍保持两个合法缩进层级。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`经典移动平均线交叉策略Moving-Average-Crossover-Strategy.md`

原文件SHA256：`873c2df6cab88074ed01edd197260e02c0f2a02dff99c4586168d1977973da12`

原代码SHA256：`ab67689be38e7c54dfe32ee4b7fd1b8b95cebe8a80e71d29c1f168464820cfba`

候选SHA256：`68985079cb68fb07c68e113e71bc552caccb858f2d648b6f4b37e9037f24623f`
