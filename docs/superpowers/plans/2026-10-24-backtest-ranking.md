# 外部回测融合排名实施计划

> **For agentic workers:** 使用 subagent-driven-development，用户授权并行，各代理文件所有权独立。

**Goal:** 把既有逻辑卡片与本地历史回测严格匹配，生成可追溯排名及详细卡片。
**Architecture:** rank.py负责数据读取、身份、过滤和排序；details.py负责具体交易与表现解释；build.py输出独立本地目录。源码精读JSON覆盖自动解释，不倒推修改原评分。
**Tech Stack:** Python标准库、CSV/JSON、HTML/CSS/JS、unittest、Node DOM测试。

- [x] 并行审计回测引擎/数据覆盖与身份匹配，记录实际限制。
- [x] rank.py及test_ranking.py：先测失败，合并全市场结果、独立补充池、风险过滤、逐项评分、数据manifest。
- [x] details.py及test_details.py：先测失败，基于每个策略的具体条件、参数和结果生成解释及差异矩阵。
- [x] priority20.json与new_top20.json：34项完整源码精读（31项入选，覆盖新榜前20），绑定哈希和行号。
- [x] build.py及test_ranking_render.py：页面、表格、卡片、报告、有限数值和安全链接。
- [x] 全量重建、权重敏感性、覆盖与链接、排序验算、源数据不变检查。
- [x] 独立规格/质量审查，修复后复核，记录SHA及本地验证，保留分支不推送。
