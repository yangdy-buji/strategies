# ATR增强型蜡烛反转模式识别与风险管理策略-ATR-Enhanced-Candlestick-Reversal-Pattern-Recognition-and-Risk-Management-Strategy · 保守修复候选

原研究名单 #106 / SID 71。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/48c0f5288549.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 多空退出使用同一exit ID，短侧独立命名以避免同根更新覆盖其他方向退出订单。

## 未解决／保持原行为

- 退出价格仍随每根low/high/close/ATR变化，未固定到成交价；属于原动态设计。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 同根执行两方向exit时使用不同ID，from_entry与止损止盈价格表达式均保持原值。
- Hammer Buy对应Take Profit / Stop Loss，ShootingStar Sell对应Short Take Profit / Stop Loss；同根调用不复用ID。
- close100、ATR2、low98/high102时多头stop95/limit105，空头stop105/limit95保持不变。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`ATR增强型蜡烛反转模式识别与风险管理策略-ATR-Enhanced-Candlestick-Reversal-Pattern-Recognition-and-Risk-Management-Strategy.md`

原文件SHA256：`d93a7f991540c18901ba9c8e94b554e0700d4eeaafa2f687465c05b64fda146a`

原代码SHA256：`26c581ba0b858ecea480675620fcc0ada375cc79efcba245fcec57dbe72ddff3`

候选SHA256：`8437a3ac68ed68b1b34aa2c49cf08d917bba4f5c79ee5d351b354515a88e6639`
