# ATR动态趋势跟踪与重入场交易策略-ATR-Dynamic-Trend-Following-with-Re-entry-Trading-Strategy · 保守修复候选

原研究名单 #376 / SID 65。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/a6990d119a2b.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 保护单可能盘中成交但收盘回到区间，inTrade不会复位，后续多头信号被永久阻塞。按已平仓交易计数同步复位。

## 未解决／保持原行为

- Re-Long分支在平仓时entryPrice已置na，原同价重入逻辑仍不可达，需要明确重入设计。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 构造盘中low触发stopLoss但收盘返回区间的成交bar：closedtrades增加后inTrade应清空，下一次signal_up可重新入场。
- 核对原默认指标参数和数量配置未发生改变。
- 盘中止损而收盘反弹时状态清空；后续新signal_up允许入场，保护仍与入场同次提交。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`ATR动态趋势跟踪与重入场交易策略-ATR-Dynamic-Trend-Following-with-Re-entry-Trading-Strategy.md`

原文件SHA256：`1317d7b2bfdb7b5ee4138cb5ccf5938c35718ca5eb8f5e8f67f3ade2f8263d2e`

原代码SHA256：`af86c5b4b4c99eb5c33c1660081796e22b0b884640346a1a6be9a1a8ca733e3c`

候选SHA256：`67ad8d39c7a9ce3ba9baa3828b94cbfc641bc4235b4e3c9ee2208718e5ba0089`
