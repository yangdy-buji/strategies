# 移动平均线双轨与趋势跟踪策略Dual-Moving-Average-Channel-with-Trend-Tracking-Strategy · 保守修复候选

原研究名单 #48 / SID 5054。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/049a3ba24aca.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 日期函数恒真。
- 退出不能被日期阻断。

## 未解决／保持原行为

- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 日期前后不新入场
- 日期外已有持仓退出仍执行
- finish后sell_time为真仍关闭L，buy_time不建L。
- 仅全文静态复核；未执行原策略、原生编译、回测或券商操作。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`移动平均线双轨与趋势跟踪策略Dual-Moving-Average-Channel-with-Trend-Tracking-Strategy.md`

原文件SHA256：`fa3c6caaa8090973f8d96ba4c4da0ee27de1fc38d705d098c88d28036a13a8dc`

原代码SHA256：`55e1237248b20048712bac892fecc2cab425b27c71c4b0a201d866bf1ee140b0`

候选SHA256：`20fbd527ec1e94a5794923fc9b269245fa9f8f2e238a3f567a68fc99fbd00b8a`
