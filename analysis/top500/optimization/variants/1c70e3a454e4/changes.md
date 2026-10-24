# 拓宽均线区间的马丁格尔止损炒股策略Martingale-Strategy-with-Expanded-Moving-Average-Range-for-Stock-Trading · 保守修复候选

原研究名单 #494 / SID 4622。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/1c70e3a454e4.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 恢复入口日期。
- 区分入场EMA1与止盈EMA1 TP；先撤窗外入场单，再提交持仓止盈与原期末平仓，避免撤单误取消止盈。

## 未解决／保持原行为

- 原唯一strategy声明仍是注释，候选有既存原生编译阻断；不擅自启用被注释的10层加仓配置。
- 未原生Pine编译、回测或订单撮合验证；批准仅限所列静态修复。
- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 过期不新增初仓或补仓。
- 窗外仅撤EMA1入场，EMA1 TP保护不被同ID撤单取消。
- 期末close EMA1必须在cancel EMA1之后提交，保持原退出意图。
- 窗外EMA1加仓挂单取消，但独立TP保留并且全平市场单不被撤销。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`拓宽均线区间的马丁格尔止损炒股策略Martingale-Strategy-with-Expanded-Moving-Average-Range-for-Stock-Trading.md`

原文件SHA256：`f14513a007a628910358e583a8c4328c429748cc17f159480bfd4206a53f5e57`

原代码SHA256：`f09cea09c8e1a3b5a49879faac9510469b54b29e17eacd01238432302a2fee1f`

候选SHA256：`1cb572fb2fd8ea433d8b926195f898083ceba68a0a2fe7cfb7a8258135a2c514`
