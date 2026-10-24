# 优化候选本地验证记录

日期：2026-10-24。环境：macOS，本地隔离worktree，`feat/strategy-catalog`。
修改基线：`768b70f`。实现提交：`52255e3de4dbe4d11c1126420d6eb6b01511787a`；本记录后续仅补充验证元数据。

## 已执行

|命令或检查|结果|
|---|---|
|`python3 -m unittest discover -s tests`|112项通过，包含15项源码绑定的修复用例、13项产物验收用例|
|`python3 -m tools.strategy_optimization.build`|500项登记、11候选、20需单独设计、469待源码审查|
|`python3 -m tools.strategy_optimization.verify`|PASS：500源码指纹、11候选完整再生成/补丁/备注，卡片双向链接及6149个本地链接检查通过（含重复遍历）|
|`node tests/test_optimization_ui.cjs`|默认11候选、500项切换、状态筛选、SID搜索、空状态、链接通过|
|`node tests/test_ranking_ui.cjs`|原排名交互回归通过|
|`node tests/test_catalog_ui.cjs`|原分类目录交互回归通过|
|`python3 -m tools.strategy_ranking.verify --source <原回测目录>`|500分数重算一致、16输入指纹、原排名覆盖及3531链接通过|
|根目录策略Markdown相对768b70f差异|0，原资料未改|
|独立规格审查|通过，11项代码符合批准范围；验证文档缺项已关闭|

独立质量复审通过：无blocking/important；复跑112项Python及三个Node测试，500张原HTML卡片在不启用优化链接时与原实现逐字一致。

再次重建的550个文件SHA逐项一致。原源码快照保留既有行尾空格，统一差异补丁含标准空白上下文标记，因此全量`git diff --check`会报告这些归档产物；排除variants归档后，生成器、测试和文档的staged空白检查通过。

## 验证实际含义

修复用例从源码表达式、分支缩进和订单ID提取受影响的局部逻辑，检查日期边界、布尔组合、挂单撤销及保护分支。它们不是Pine解析器、编译器或完整订单执行器。部分用例检查文本结构及范围不变，不代表完成真实成交验证。

所有11候选均**未原生Pine编译、未回测**。本机`pine`/`pinec`命令及可用工具中未找到原生Pine环境；浏览器库存为空，未做真实浏览器视觉检查。DOM测试仅验证页面脚本逻辑。

旧收益只属于原版本。日期恢复、BB顺序和退出保护变动可能降低收益或增加回撤，需另行用相同数据与执行模型逐笔验证。原目录catalog与ranking JSON指纹保存在summary.json，优化构建未改变评分。

未部署、未合入master、未推送、未接券商或真实下单。按用户门禁，可运行变更在缺少部署验证时保持本地。

## 主要产物SHA256

|文件|SHA256|
|---|---|
|manifest.json|`5d6d7fa1ed9020a70aed0b8cd68c3a41a08d57d690f761a3dcad853e0c1ec4ba`|
|manifest.csv|`281f8b7128f067aac3d370633953a95364779ad78539c9956475b8b12a4d6e8a`|
|index.html|`109cbd4aeefb0324b143b20f36584f0f587045c2139abeb8fcc003908f275fff`|
|summary.json|`d811e0e185242f34c5ae6a0b118129b3eed3faf91bdd7f46e0a6335f81fe0b3c`|
