# 剩余489项策略审查与修复实施计划

> **For agentic workers:** 用户已确认全量审查、确认缺陷修复后统一推送。使用subagent-driven-development，在既有隔离worktree并行审查；不部署，不运行真实策略或下单。推送仍需满足用户原有明确门禁，不能把不部署视作自动豁免。

**Goal:** 完成剩余489项逐项静态源码审查，对原意明确的缺陷生成带中文备注的可追溯修复候选，并全量验证。
**Architecture:** 三组独立JSON记录源码审查结论及精确补丁建议；统一加载器绑定原文件/代码指纹，执行补丁前置检查和保守修复。沿用原卡片、差异、登记和本地验证管道，新增已审无确认缺陷/待设计等状态。
**Tech Stack:** Python标准库、JSON、原版Pine代码、unittest、Node DOM harness。

- [x] 从当前500项名单排除11个已修改项，按代码量分成三组，锁定489 SID清单。
- [x] 审查组1/2/3：阅读每份完整源码，记录具体信号/退出摘要、至少一个有效源码证据位置、发现和结论；不得把关键词扫描等同逐行审计。
- [x] 对明确缺陷提出最小补丁及验证场景；不根据标题改变交易方向，不批量加止损/调仓位/调参数。
- [x] 先测试审查覆盖、指纹漂移拒绝、补丁唯一匹配、状态分层，再扩展修复加载器与页面。
- [x] 独立复审全部新增补丁，验证前后执行分支/表达式，并进行失败→通过回归；无法确定交易意图的发现保留未修原因。
- [x] 重建500登记与所有实际修复候选；核验逐项覆盖、原源文件不变、Pine版本保留、注释与diff、旧绩效不混入新版本。
- [x] 独立规格及质量复审；完成本地测试后合并master并重新验证，依实际部署门禁决定是否可推送，明确记录阻塞。

## 审查记录接口

`analysis/top500/optimization/audit/batch_N.json`为list；每项含sid、id、filename、source_sha256、code_sha256、code_lines、review_scope="full_source_static"、synopsis、evidence=[{line,code,reason}]（line为原Markdown行号）、findings=[{severity,kind,evidence_line,detail,resolution}]、verdict（no_confirmed_defect / needs_design / fix_proposed）、patches=[{old,new,reason,preserved,validation_cases}]。无缺陷不代表性能已验证；无补丁也必须有具体源码摘要，不能使用统一模板填满。

补丁old唯一匹配；new不含OPT备注，由统一加载器插入；方案不明确不能伪造已修。运行验证仍分静态/局部表达式与原生Pine编译、回测，不混称。
