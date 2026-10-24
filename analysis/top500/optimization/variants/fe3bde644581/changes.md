# 黄金分割移动平均线交易策略Golden-Ratio-Moving-Average-Trading-Strategy · 保守修复候选

原研究名单 #304 / SID 5796。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/fe3bde644581.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 恢复仅入口日期。

## 未解决／保持原行为

- profit参数未接入，原止盈规则不扩展。
- 未进行原生Pine编译、回测或订单撮合验证；批准仅限所列静态修复。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 窗口外不入场，已有仓位继续止损与信号退出。
- 窗外持多仍按均价80%止损，回到短均线上且跌破前低仍close。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`黄金分割移动平均线交易策略Golden-Ratio-Moving-Average-Trading-Strategy.md`

原文件SHA256：`4b222c06bcf66a72f949dc86f274598e713d646033aa0779e89ecfbc7bcd0d3c`

原代码SHA256：`24269f972357a3f2616895291a373f25b9c6f8b2e907912c8ad66a2052277987`

候选SHA256：`72b1c5585d3c5afc62c1951375f86dd47dce315d04fd054face3d22b459ee893`
