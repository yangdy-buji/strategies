# 多个EMA周期动态交易策略Multi-Timeframe-Dynamic-EMA-Trading-Strategy · 保守修复候选

原研究名单 #455 / SID 3740。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/5fc844f39d65.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 恢复日期。

## 未解决／保持原行为

- count可为0或负数导致Amount无效；平台pyramiding未设置；保留原样。
- 未进行原生Pine编译、回测或订单撮合验证；批准仅限所列静态修复。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 结束后不再出现入场和当柱到期退出冲突。
- 结束后七个ID分别执行原close，任何金叉不再进场。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`多个EMA周期动态交易策略Multi-Timeframe-Dynamic-EMA-Trading-Strategy.md`

原文件SHA256：`6196137c8ea2ff7796a78071c5cfe9d208cc6ab345081c3dda8a85b6d2f3e8de`

原代码SHA256：`43efbc0e3413b9ba5ceb426169e84cbdb20876b9e0863d21230f2d152e1e3205`

候选SHA256：`2214ad07226cfee0fc998650e7658dc61d8f9ebd38e26832eaf6eb2a25213a4a`
