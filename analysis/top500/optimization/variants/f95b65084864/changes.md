# 趋势突破交易系统移动平均线突破策略-Trend-Breakout-Trading-System-with-Moving-Average-TBMA-Strategy · 保守修复候选

原研究名单 #298 / SID 5391。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/f95b65084864.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 全仓目标先预留仓位，后止损没有可用数量。
- 以止损而非入价加2倍风险，实际只有1R。

## 未解决／保持原行为

- 重复longSignal仍重设SL/TP；length输入未使用而最低点固定7。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 同一仓位目标止损均有效
- 先触发任一后取消另一
- 收盘100、止损95目标110
- 2R系数不变
- close100、SL95时TP110且SL95共同保护同一Long全部数量。
- 仅全文静态复核；未执行原策略、原生编译、回测或券商操作。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`趋势突破交易系统移动平均线突破策略-Trend-Breakout-Trading-System-with-Moving-Average-TBMA-Strategy.md`

原文件SHA256：`12b74884ad6d19079d6c3ac5e400dfd9850dd3d1a1a68a72d63f4a501e84fd50`

原代码SHA256：`71c7957f1c8a69184d1fd2e106e316ad992b6b34900e2adbf768266e006088fb`

候选SHA256：`08ab2282f5e6ad87bc79bfd5ea45c42978913af39b166bf9119a3b3e190b5df9`
