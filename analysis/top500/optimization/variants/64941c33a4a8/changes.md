# 双移动均线交叉反转策略Dual-Moving-Average-Reversal-Strategy · 保守修复候选

原研究名单 #331 / SID 2188。未原生编译、未回测；原排名收益不适用于本版本。

[优化卡](../../cards/64941c33a4a8.html) · [原提取代码](original.pine) · [带备注修复版](conservative.pine) · [逐行差异](changes.patch)

## 已修改

- 恢复限价入场日期范围。
- 窗外撤销未成交限价买单，已有持仓仍可按xsell退出。

## 未解决／保持原行为

- 修复候选未原生编译/回测；旧排名收益不适用。

## 验证场景

- 窗口前、起点、终点及窗口后各构造相同入场信号：只允许窗内新仓。
- 窗口结束前已有持仓，结束后出现原退出条件：退出调用仍可执行，不因日期而关闭保护。
- 窗内最后一根生成低于市场的buy限价单，越界且未成交时应取消，不能在窗外迟到成交。
- 末根窗口内limit未成交后越界取消buy；已有buy持仓在窗外xsell仍退出。

## 原版审查上下文

以下仅供对照，不表示这些问题在修复版中全部仍然存在。



## 验证边界

源码前置条件和指纹已检查。局部行为用例结果见[本地验证记录](../../validation.md)；不是Pine编译或完整回测。未使用新行情验证收益。

## 指纹

原文件：`双移动均线交叉反转策略Dual-Moving-Average-Reversal-Strategy.md`

原文件SHA256：`03289a00b8ff657955f704cf0417fdbfe1b0ed40c3fd6929f72c77bd6dd217b2`

原代码SHA256：`8a9d17dfdaef80693fa130e4ae7cd8e714c9cd6f4fe50996ad407b084527dfe2`

候选SHA256：`f9d6f65e39bd2ffcbe94447e42ac0a5eeccda53e63e2f205d9fac5adb8bd3382`
