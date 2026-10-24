# 回测资料身份与卡片字段审计（只读）

核对日期：2026-10-24。输入为 analysis/catalog.json 与 Google Drive「量化回测结果_2026-10-20」。未执行所附源程序；只读取数据与 features.py 的哈希实现。本文件为审计草稿。

## 关键结论

- catalog 5807 条，features.jsonl 5807 条；按 repo_path 的 basename 与 catalog.filename 精确连接，5807/5807 命中，filename 无重复；features.sid 与 all_scored.sid 唯一。
- 全部 5807 个 catalog.code 按 features.py 的 norm_source 重算 MD5，均等于 features.src_hash（无冲突）。这证实规范化源码的一致性，但不能提升为原始源码字节一致或严格回测版本绑定。
- features.py 的 norm_source 去掉 backtest 区块、全部注释，把所有引号字符串替为 S，再压缩空白、小写。该摘要会忽略有交易意义的字符串差异、大小写及回测配置。src_hash 与 source_sha256 算法及输入均不同，不能直接比较。回测 CSV/JSONL 本身没有 source_sha256 / src_hash 字段；只能经 sid → features → path → catalog 的中间证据链连接。
- sid 是当时 strats.json enumerate 下标（features.py 322–332行），并非稳定跨版本身份；打包中没有 strats.json 或 repo 原始快照。不可用 catalog 顺序或模糊标题直接替代连接。
- 唯一 name+'.md' 与 path 不一致的是 sid 707，name=README.md，path=repo/README.md。因此 path优先；name仅辅助核验。
- all_results.csv 5283行的 repo_path basename 均与该sid在all_scored的path相符，零冲突。

## 有效日线集合与重复

all_552_daily.csv：552行；440 ran + passes_filter=True，3 ran但未过筛，109 skipped。top552_daily_ranked_combined.csv为440；final_ranking.csv为434，即前者再排6个重复。excluded.csv为118行。

all_results.csv中 full_universe + status=ok 为268行，与552集合有185交集，新增83。其余stage为screen_50stocks，不应混为全样本日线结果。83条新增均满足trades≥100、exposure≥2%。440+83=523唯一sid；规范化MD5去重后513；按all_scored.representative_sid为508组，直接is_representative=True也508。

508代表策略中，剔除fill_artifact_suspect后只剩499；再剔除包含LEAK_或BUG_的策略后466；仅保留red_flags为空则220。因此可构造至少500个有全样本历史回测的展示候选，但不能声称有500个无严重疑点、经验证的优质策略。保留疑点项时应明确分层和展示红旗；不得用screen_50stocks补足并隐去阶段差异。

features.src_hash有5704个唯一值，92个重复组，合计103条重复冗余；dupes.json另有近重复组（groups / reasons / stats），比分组MD5更宽松，不能称为严格源码相同。所有既有重复与近重复信息应单独保留。

## 中文短评缺口

manual_review.jsonl为485条、485唯一sid，字段sid/delta/comment/auto_at_review；评论均非空，长度29–84字。Top500仅280条reviewed=True，220条False。这批短评主要是机制概述与单个风险提醒，不是500份完整中文入场、退出、仓位、风险说明；文件名manual_review也不能证明由真人完成。

例如sid2411短评：经典唐奇安50日突破做多、12日低点追踪离场+固定金额止损，规则简单、经济逻辑清晰（趋势延续）。此类短评可作为“历史评语”附加证据，不能替代逐项源码验证或自动升级现有review_status。

## 各数据文件与可用字段

|文件|行数|主要用途/字段|
|---|---:|---|
|2_合理性Top500/all_scored.csv|5807|sid/name/repo_path/language/author/fmz_id；archetype/direction/category；rationality_score/auto_score/manual_delta；s_logic/s_no_leak/s_risk/s_simplicity/s_empirical；red_flags/leak_detail/comment_cn/reviewed；is_representative/duplicate_ids/representative_sid；s1与s2历史统计|
|2_合理性Top500/top500.csv|500|上述选集及rank；不可将文件名视为500条回测通过|
|2_合理性Top500/universe_500_plus_top100.csv|552|source/rationality_rank/perf_rank，用于解释候选由来|
|0_代码与中间数据/results/rationality/features.jsonl|5807|src_hash、作者、fmz_id、last_modified；方向与订单次数、止损/止盈/追踪、限价止价、pyramiding/qty/risk_sizing；impl_bugs、leak_hard/leak_soft/leak_detail；指标/参数数量、奇数参数、日期及交易时段线索|
|0_代码与中间数据/results/all_results.csv|5283|status/stage/tickers_run/errs，完整绩效与末三年oos3；须严格区分full_universe与screen_50stocks|
|0_代码与中间数据/results/stage2/stage2.jsonl|268|全样本结果；只有sid，无path或hash|
|0_代码与中间数据/results/stage1/stage1.jsonl|5283|初筛结果；不可与全样本日线混排|
|3_552策略日线重跑/all_552_daily.csv|552|run_status/skip_reason/passes_filter/source_run/fill_artifact_suspect；cagr/total_return/sharpe/sortino/max_dd/calmar/win_rate/profit_factor/trades/exposure/avg_hold_days/short_trade_frac/final_equity/oos3指标/tickers_run|
|3_552策略日线重跑/top552_daily_ranked_combined.csv|440|daily_rank/composite以及日线表现|
|3_552策略日线重跑/top500_daily_ranked.csv|388|合理性500中实际通过的排名子集|
|4_综合排名/final_ranking.csv|434|final_score/score_raw/rationality_pct/perf_percentile/intraday_5tf_mean_percentile/intraday_n_tf/flags|
|4_综合排名/excluded.csv|118|exclude_reason等，须与候选展示一起解释|
|5_日内回测_set552/top100_5m、10m、15m、30m、1h.csv|各100|各周期排名、收益/风险/成交次数/样本起止/flags/last1y_sharpe；非全量日内数据|
|5_日内回测_set552/top50_overall.csv|50|跨周期排名及各周期rank/sharpe|
|0_代码与中间数据/results/intraday/set552/ranked_1h.csv|378|较完整1h列表、last1y表现、duplicate_sids及daily上下文|

## 详细卡片的建议字段边界

身份区：catalog.id、filename、source_sha256、fmz链接，加external_sid、规范化MD5匹配状态、资料相对路径与源文件SHA256（后者需导入时生成）。必须写“规范化源码匹配”，不可写“源码哈希完全一致”。

规则区：优先使用catalog已有源码行号、entry_rules/exit_rules/position_rules、parameters、作者principle；引入历史comment_cn作独立“历史评语”。features可补方向、订单类型、风险管理线索、日期与时段限定，但其正则布尔特征不能证明执行覆盖、准确仓位上限或回测实现忠实。

风险区：保留catalog自身静态风险与外部red_flags/impl_bugs/leak_hard/leak_soft，说明证据来源而非相互覆盖。历史rationality_score与本地source可审查性分数应独立展示，两者口径不同。score_meta权重为logic .35、leak .20、risk .15、simple .15、emp .15；历史合理性分数包含回测经验项，并非纯源码评分。

绩效区：以source_run/stage、样本区间、标的数、trades、exposure、收益风险指标、末三年表现及异常成交标签构成；百分数与小数单位需统一，missing不得填0。现有文件有汇总指标但不能单独证明原生Pine执行等价性，也没有逐笔成交审计/独立留出期设计的充分证据。

缺口：至少220份Top500缺历史评语；所有卡片仍需要明确中文参数解释、准确入场/退出状态逻辑、仓位与持仓边界、局限性。不能通过复制泛化模板自动宣布规则已完整分析。CSV中运行错误、fill suspect、重绘/前视、固定日期、零风险规则、近重复与阶段差异都应作为可见证据。
