# 基于真实波幅的加权移动平均跨期策略True-Range-Based-Weighted-Moving-Average-Cross-Period-Strategy · 保守修复候选

原研究名单 #470 / SID 3526。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/e03e16b81471.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 日期失效且声明无pyramiding，第二至五层加仓不可达；日期可修但加仓需确认杠杆。

## 未解决／保持原行为

- 声明未设置支持五档的pyramiding，加仓计划是否需要启用需确认。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 起止时间外同样的long拐点不允许BUY1至BUY5新入场；short且盈利全平在窗外仍有效。
- 核对原默认指标参数和数量配置未发生改变。
- 窗外BUY1..BUY5均禁开，short且盈利仍close_all。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`基于真实波幅的加权移动平均跨期策略True-Range-Based-Weighted-Moving-Average-Cross-Period-Strategy.md`

原文件SHA256：`5809658207be7409bb68bb8b8cbd627b9c3d05871f0daf9b6ad2237ef47495ec`

原代码SHA256：`3d8768fff0f772b85781c4eea34fc749ddfa98500cb534a99abbf73011a9225e`

候选SHA256：`32f6b1af508b35607ef0ff916dda4e0169dc36810abf881bf1214a4fb6f2ef26`
