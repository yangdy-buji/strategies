# 本地验证记录

实现提交：`1a207f5de7115e87f64a4520c006a10ac9434b05`
原始资料基线：`866a77c`（策略内容继承原始 `7853bb2`）。
环境：macOS 本地工作分支 `feat/strategy-catalog`，Python 3.9.6，Node 26.7.0。

## 执行与结果

|命令／检查|结果|
|---|---|
|`python3 -m unittest discover -s tests -v`|30项通过|
|`python3 -m tools.strategy_catalog.build --workers 8`|5807份资料全部生成，24份源码复核覆盖|
|`python3 -m tools.strategy_catalog.build --workers 1`|与8进程生成的11618个数据／卡片产物SHA256逐一一致|
|`python3 -m tools.strategy_catalog.verify`|5807个源哈希、11614张HTML/Markdown卡片、23259个本地链接通过|
|`node tests/test_catalog_ui.cjs`|默认复核列表、搜索、类别/分数/类型筛选、分页、空状态及卡片链接通过|
|`git diff --check` 与 staged diff check|通过|
|根目录原始Markdown相对866a77c差异|0，原始文件未修改|

## 覆盖与边界

- 总资料 5807；自动初审 5783；源码复核 24（23策略＋1工具）。
- 待分类 1641，统一低置信度；不可视为已准确判定主类别。
- 自动初评是可解释启发式，不能代表逐份完整语义复核；源码复核分也不是历史表现分。
- 独立规格审查交叉核对7份复核卡片；代码质量复审无遗留blocking/important。
- 无可用浏览器provider，因此未做真实浏览器视觉检查。Node DOM harness只验证交互脚本逻辑。
- 未编译或运行原始交易策略；无美股历史数据，未回测、未做样本外验证、未接券商、未下单。
- 未部署预发或生产；未推送远端，未合入master。按照用户门禁，可运行产物在缺少部署验证时不得推送。
- 生成产物留在当前worktree本地，已gitignore；生成器、复核记录、测试与说明已提交，可重建。

## 主要产物指纹

|产物|SHA256|
|---|---|
|catalog.json|`1bdbbebc132c07478528016955b3b29489d7a58ebdef89ad669832f4b0d4e5ed`|
|catalog.csv|`e72ac48b85211ca42e8595be7e81fad2a3967a9d9fa557373fac837ff40c97cc`|
|index.html|`a78d3a5130a95a0a68beee52aab5d6e6a2ddcb8c4adc4cbb8a4f9ad4849b19ba`|
|summary.json|`6c2e781ec65661e206aba99fa23e9855aa5bce2b750696ee0aa9bc4bd38423a5`|
