# 基于支撑位和阻力位的技术分析交易策略-Trading-Strategy-Based-on-Support-and-Resistance-Levels-Using-Technical-Analysis · 保守修复候选

原研究名单 #385 / SID 3425。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/66d766d430c0.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 函数返回先高枢轴再低枢轴，支撑阻力接收顺序倒置。

## 未解决／保持原行为

- pivot值未持久化，常为na且exit同时要求两值有效；日线数据在图表周期上求pivot的设计尚未修改。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 保持正常入场信号
- 无新信号持仓和窗外退出仍有效
- 确认高点120低点100时long比较120，short比较100。
- 仅全文静态复核；未执行原策略、原生编译、回测或券商操作。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`基于支撑位和阻力位的技术分析交易策略-Trading-Strategy-Based-on-Support-and-Resistance-Levels-Using-Technical-Analysis.md`

原文件SHA256：`903dd6c57f61adc398988c379fc2407545f88bd4fec4fd3694362f65036ebf1d`

原代码SHA256：`605cb8c6129e1fdde2675762dad62fa1a8721e0066106ac467ca88162fd641e9`

候选SHA256：`5ef3dfa05289a1ea1e7526f602e6cfa4301ff7237f284bc7f1bba2c93ed4d8df`
