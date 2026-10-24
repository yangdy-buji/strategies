# Top500 注释修复实施计划

> **For agentic workers:** 使用 subagent-driven-development；用户授权并行，独立文件所有权避免冲突。

**Goal:** 交付11个注明变化和验证边界的保守修复候选，以及500项优化登记。
**Architecture:** fixes.py定义绑定原指纹的精准补丁；build.py生成独立Pine、差异、变更卡片和登记页；verify.py核对指纹、覆盖、备注及链接。原排名生成器仅增加可选优化状态链接。
**Tech Stack:** Python标准库、unittest、现有HTML样式与Node DOM检查。没有原生Pine环境时明确标记未编译/未回测。

- [x] 确认设计，检查隔离分支与基线77项测试，查找原生Pine环境。
- [x] 修复模块：SID735/5369/621/4143/3883/3322/2458/4621/2943/3330/4941。先写原缺陷失败用例和指纹拒绝测试，再实现精准补丁；保留Pine版本与交易默认值。中文备注说明原/新行为、保持项及待原生验证。
- [x] 输出模块：先测试500项状态覆盖、未修复不生成Pine、差异可还原、HTML转义；再实现manifest、11个variants及500张状态卡。
- [x] 原卡片关联：先测试缺少optimization时兼容旧目录、存在时正确链接；再添加链接生成。
- [x] 生成器验收：`python3 -m tools.strategy_optimization.build`；校验原文件SHA、输出源码SHA、完整差异、所有状态链接和无继承新收益。
- [x] 独立规格审查通过后进行质量审查；修复发现并重跑受影响测试。
- [x] 全套Python与Node回归、输出验证；记录实现SHA、环境、命令、结果、未验证项，保留本地不推送。

接口约定：`fixes.py`导出`FIXES`（sid为键，含source_sha256、title、changes、remaining、validation_cases）与`apply_fix(sid, code, source_sha256)->str`。补丁不加文件头（构建器负责），在变化附近插入中文注释；指纹或唯一匹配失败抛ValueError。未支持sid拒绝处理。`build.py`读取原catalog与ranking，调用上述接口，不执行原策略。

验证边界：行为用例只覆盖已修改的局部语义，不等于完整Pine执行器；不运行外部回测脚本、不接券商、不写原策略。
