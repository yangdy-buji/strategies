# 拉里威廉姆斯三周期动态均线交易策略-Larry-Williams-Three-Period-Dynamic-Moving-Average-Trading-Strategy · 保守修复候选

原研究名单 #3 / SID 4621。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/3973c7947db0.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 原日期门禁恒真；恢复包含边界的起止参数。
- 原退出依赖日期门禁；移除该依赖使窗外仍能退出。

## 未解决／保持原行为

- 未原生Pine编译/回测；静态及小范围模型不等于订单成交模拟，旧版收益不适用。
- na(time_close)不构成普通交易日的收盘强平；无独立硬止损。

## 验证场景

- 日期五点边界；退出仍保留连续蜡烛及确认条件。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。

- 日期门禁恒true；na(time_close)不构成正常交易日收盘强平。
- 没有硬止损，退出也需要连续三次同向收盘条件。

## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`拉里威廉姆斯三周期动态均线交易策略-Larry-Williams-Three-Period-Dynamic-Moving-Average-Trading-Strategy.md`

原文件SHA256：`6f52852843a35fa7f885d23aec5ace9399b970fd95485146e3e8f8d01b228c26`

原代码SHA256：`fd9a3fa946122cc32ef8a1d20d672c783ed31042ab5f3e7a7b5d689866c4dc3d`

候选SHA256：`045aa5b4050721b2e5d24530ceb0b26d4043736fa2310a4c9bc73fe7f3dba505`
