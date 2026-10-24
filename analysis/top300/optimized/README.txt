TOP300实施脚本包

本轮新候选·未回测: 56
沿用旧候选·未回测: 59
保留原版·待验证: 60
保留原版·待设计: 125

候选不是上线版。所有文件未原生Pine编译、未重测，不能继承原排名收益。new_patch为本轮新修；carry_existing仅沿用既有候选；unchanged/deferred_design输出原版且文件名带original。

originals保留原版，baselines保留本轮修改起点，scripts为交付版本，changes记录逐处原因、保持行为、差异和未解决问题。局部Python测试不能证明完整Pine、指标时序与订单成交行为。

部分设计建议需要独立行情、原生执行或明确经济假设，具体见每项remaining与validation_plan。验证时先逐笔对齐原/新版订单和仓位，再做同成本、同股票池的后续样本测试。ZIP不包含依赖仓库目录的HTML页面。
