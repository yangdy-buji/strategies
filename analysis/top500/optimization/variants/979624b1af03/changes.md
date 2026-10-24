# Flawless-Victory-DCA-动量与波动率策略Flawless-Victory-DCA-Momentum-and-Volatility-Strategy · 保守修复候选

原研究名单 #39 / SID 373。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/979624b1af03.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 保护退出覆盖两个做多入口ID。

## 未解决／保持原行为

- sell_condition限制保护提交及pyramiding=0仍保留；dca_interval未限制正数。
- 未进行原生Pine编译、回测或订单撮合验证；批准仅限所列静态修复。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- DCA关闭的Long仍匹配退出。
- DCA开启时DCA Long满足原卖出条件也受退出保护。
- 分别以Long/DCA Long持仓且卖出条件真/假检查退出匹配。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`Flawless-Victory-DCA-动量与波动率策略Flawless-Victory-DCA-Momentum-and-Volatility-Strategy.md`

原文件SHA256：`f0e4e066be0e1ba014303fa69cb23444e6649d7c81e0565e47cd0d4a8da0344e`

原代码SHA256：`68acb9fe4ab73de3e161e4f71b1e730908965c8a62126eb1e0e40e01a93108fb`

候选SHA256：`0157d129f9044fd1e693b1ef6ca937be0ee6eecf71bb089e00ee33901908beb2`
