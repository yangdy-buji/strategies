# 基于布林通道和RSI指标的渐进DCA策略Bollinger-Band-and-RSI-Mixing-with-DCA-Strategy · 保守修复候选

原研究名单 #190 / SID 3379。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/46e19036171f.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 恢复主仓和追加仓入场时间。
- 主仓退出不随入场窗口失效。
- 百分比转价格差再转tick，保留原百分比及动态均价锚点。
- 最大层限制应为小于而非不等于，避免超限继续加。

## 未解决／保持原行为

- entry_price会被未成交信号更新，且无持仓也可能触发consec_LE；是否允许独立加仓需确认。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 窗口前、起点、终点及窗口后各构造相同入场信号：只允许窗内新仓。
- 窗口结束前已有持仓，结束后出现原退出条件：退出调用仍可执行，不因日期而关闭保护。
- 均价100、D_sl=10、mintick=0.01时loss应为1000tick即10元，不是1000tick偶然依赖品种；mintick=0.25时为40tick。
- 设置A=5且opentrades=6时追加信号必须拒绝；opentrades=4时仍沿用原追加数量。
- opentrades=A或>A不再加仓；均价100、10%、mintick=.01时退出距离1000ticks；窗外主仓退出有效。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`基于布林通道和RSI指标的渐进DCA策略Bollinger-Band-and-RSI-Mixing-with-DCA-Strategy.md`

原文件SHA256：`cbdd603103e3ef199a0d970aca10f7c90d1feb1d024b9358b5ab97916d98b2ff`

原代码SHA256：`09407b896af12f41cd77022eb6e6fc7740724a0116e07a66a4a448887ad24c16`

候选SHA256：`0ff1f964a7b0524384f0514dded3dfcde913f58e96f0dbf69cb8ac7e6237b129`
