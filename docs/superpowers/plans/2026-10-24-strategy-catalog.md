# 策略分类与卡片实施计划

> **For agentic workers:** 使用 subagent-driven-development 执行；用户明确授权并行，各任务只写其分配文件。

**Goal:** 为5,807份原始资料生成可检索分类和可追溯合理性初评分、完整阅读卡片，并提供源码复核样本。
**Architecture:** Python标准库提取器生成结构化记录；人工源码复核JSON覆盖记录；渲染器生成Markdown/CSV/内嵌HTML。源文件只读，各代理按独立文件写入。
**Tech Stack:** Python 3标准库、unittest、静态HTML。

## 任务1：提取器与评分
- [ ] 新建 tools/strategy_catalog/analyzer.py 和 tests/test_analyzer.py。API analyze(path:Path)->dict；字段契约通过代理消息固定。
- [ ] 先构造包含跨行strategy.entry、注释伪订单、退出和条件变量的测试，执行 `python3 -m unittest discover -s tests -v` 观察缺失功能，再实现。
- [ ] 实现原文区块、代码区块、订单与依赖、风险证据、分类、评分；输入只扫描根目录md。

## 任务2：源码复核（并行独立JSON）
- [ ] 两个批次各选择12份不同家族策略，读完整源码，输出 analysis/reviews/batch_a.json 和 batch_b.json；所有结论绑定 source_sha256。
- [ ] 用中文解释默认参数、条件、执行顺序、入场、出场、仓位、优缺点；给出五项评分和依据，不伪造回测。

## 任务3：目录与卡片生成
- [ ] 新建 tools/strategy_catalog/build.py 与 tests/test_catalog.py，先验证覆盖、无表现评分、链接和HTML转义。
- [ ] 合并复核记录，源码哈希不一致失败；输出每文件一卡、JSON、CSV、HTML及说明。
- [ ] 执行 `python3 -m tools.strategy_catalog.build --workers 8` 并核对5807份覆盖。

## 任务4：独立审查与交付
- [ ] 分阶段检查规格符合性和代码质量，修复后复核。
- [ ] 执行全部测试、全量生成、链接/数据验证、git diff --check；记录SHA和未验证项。
- [ ] 本地工作分支提交经验证产物；无预发验证环境，不推送、不自动合并master。交付本地入口路径。
