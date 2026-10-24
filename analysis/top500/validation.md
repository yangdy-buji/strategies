# 回测融合排名本地验证记录

实现提交：`f9c9ac2ae8ecbe870807cb52acc64c7027da65f4`。环境：macOS 本地 `feat/strategy-catalog` worktree。
日期：2026-10-24。原资料基线：`4597699`。

## 已执行

|命令/检查|结果|
|---|---|
|`python3 -m unittest discover -s tests`|77项通过|
|`python3 -m tools.strategy_ranking.build --source <回测目录>`|500份；451主榜、49补充；完整初筛补充池2992|
|`python3 -m tools.strategy_ranking.verify --source <回测目录>`|PASS；500份评分重算、500个源码哈希、16个输入文件哈希、1000张HTML/Markdown卡片、3030个链接|
|`node tests/test_ranking_ui.cjs`|搜索、分类、证据层、收益和精读筛选、分页、链接及分层排序通过|
|`node tests/test_catalog_ui.cjs`|原目录交互回归通过|
|`git diff --check` / `git diff --cached --check`|通过|
|根目录策略Markdown相对基线差异|0；原策略未修改|
|独立质量复审|全量失败/超时组回流修复通过；错误数门禁和实际数据名单重算通过|
|独立规格复审|qty/加仓误判、默认条件分支恢复修复通过；Top20全精读、类别与重要疑点展示通过|

源码精读记录共34份，入选31份；主榜前20全部覆盖。其余卡片为自动语义辅助，未宣称逐份源码审计。原逻辑分冻结，新增精读发现展示但未只对局部样本调整排名。

## 未验证项与发布状态

- 外部回测未重新执行；没有原始行情、逐笔订单或权益序列，无法独立验证其收益。源码标准化哈希为有损匹配，不能证明回测版本完全相同。
- 严格主榜只有451份；49份初筛补充独立展示，不能当成同口径Top500。旧的超时回流6份已排除。
- 未做真实浏览器视觉验证；Node DOM harness仅验证脚本行为。
- 未运行策略、未接券商、未真实下单；未部署、未合入master、未推送远端。可运行产物保留本地，遵守部署验证后才允许推送的门禁。
- 生成卡片和大表按gitignore保留本地；生成代码、来源manifest、复核数据与说明已版本化。

## 产物SHA256

|文件|SHA256|
|---|---|
|ranking.json|`b7a5d3f07f30af8786ff121fa05d6a0da1c878c4af986b7d629cc8f8864839c4`|
|ranking.csv|`3471aa2a1f8c5ac785a326a9f4f717a0da19accfed3594944c6de8a45c20a846`|
|index.html|`e7998064ee3e48cb02c4260df4f6ee2399766b439e84df7d82046ca0c2321ed3`|
|summary.json|`ec9e06e11e08f52f6e9be0fc236c4b7e9653312552a6439fe652c59eea3c6f9b`|
|source_manifest.json|`28f58c0e8191a021f8fb0e5a40fb90efb9b0602e6cc9c371f79f498146775ac5`|
