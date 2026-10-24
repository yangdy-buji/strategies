import json
import unittest
from tools.strategy_ranking.details import build_details


class DetailTests(unittest.TestCase):
    def base(self):
        code = 'fast = ta.ema(close, 9)\nslow = ta.sma(close, 21)\nif ta.crossover(fast, slow) and close > close[1]\n    strategy.entry("L", strategy.long, qty=5, limit=open, stop=high)\nstrategy.exit("X", "L", stop=close-ta.atr(14), limit=close+2*ta.atr(14))\nstrategy.risk.max_drawdown(20, strategy.percent_of_equity)'
        return dict(title='测试均线', code=code, entry_rules=[dict(line=4, code=code.split('strategy.exit')[0])], exit_rules=[dict(line=5, code=code.splitlines()[4])], parameters=['length = input.int(21)'])

    def test_conditions_and_chinese_meaning_are_preserved(self):
        detail = build_details(self.base(), {}, {})
        joined = '\n'.join(detail['entry_steps'] + detail['signal_explanations'])
        for term in ['向上穿越', '指数移动平均', '简单移动平均', '前1根', 'ta.crossover(fast, slow) and close > close[1]']:
            self.assertIn(term, joined)
        self.assertGreaterEqual(len(detail), 18)
        self.assertIn('语义辅助', detail['detail_level'])

    def test_missing_and_nonfinite_never_become_performance(self):
        result = build_details({}, dict(reported_daily=dict(cagr=float('nan'), sharpe=float('inf'))), {})
        text = json.dumps(result, ensure_ascii=False, allow_nan=False)
        self.assertNotIn('nan', '\n'.join(result['performance_findings']).lower())
        self.assertNotIn('inf', '\n'.join(result['performance_findings']).lower())
        self.assertIn('缺失', text)

    def test_existing_review_has_priority(self):
        base = self.base()
        base.update(entry_explanation=['人工完整复核：条件A且条件B'], parameter_explanation=['21是固定窗口'], review_status='源码复核')
        result = build_details(base, {}, {})
        self.assertEqual(result['entry_steps'][0], base['entry_explanation'][0])
        self.assertIn('21是固定窗口', result['parameter_notes'])

    def test_engine_matrix_distinguishes_stop_limit_and_ignored_risk(self):
        result = build_details(self.base(), dict(features=dict(risk_rules=True, entry_limit_orders=True, entry_stop_orders=True)), {})
        rows = result['engine_compatibility']
        text = json.dumps(rows, ensure_ascii=False)
        for term in ['limit', 'stop', '忽略', 'qty', '未验证']:
            self.assertIn(term, text)
        self.assertTrue(all(set(['feature','source_evidence','backtest_behavior','impact','verification']) <= set(x) for x in rows))

    def test_recent_is_not_oos_and_timeframes_are_not_independent(self):
        result = build_details(self.base(), dict(cohort='full_daily', reported_daily=dict(cagr=.1, exposure=.99,trades=8,tickers_run=8,avg_hold_days=300), reported_recent=dict(oos3_cagr=.2), intraday=[dict(tf='5m',cagr=.15,trades=5,exposure=.99,tickers_run=5)]), dict(cagr=.08))
        text = '\n'.join(result['performance_findings'])
        for term in ['百分点', '历史末段', '不是独立样本外', '不合计', '持有型']:
            self.assertIn(term, text)
        self.assertNotIn('alpha', text.lower())
        self.assertNotIn('100,000', text)

    def test_capital_exposure_does_not_imply_holding_duration(self):
        for trades, hold in [(20000, 2), (10, None), (10, 1)]:
            result = build_details({}, dict(reported_daily=dict(exposure=.99, trades=trades, tickers_run=1019, avg_hold_days=hold)), {})
            text = '\n'.join(result['performance_findings'])
            self.assertIn('组合平均资金暴露', text)
            self.assertIn('min(n_active, 20) / 20', text)
            self.assertNotIn('持仓时间占比', text)
            self.assertNotIn('可能是持有型', text)
            self.assertIn('高资金利用不等于频繁交易或持有型', text)

    def test_hold_inference_needs_low_turnover_and_long_holding(self):
        result = build_details({}, dict(reported_daily=dict(exposure=.99, trades=1019, tickers_run=1019, avg_hold_days=365)), {})
        text = '\n'.join(result['performance_findings'])
        self.assertIn('可能是持有型', text)
        self.assertIn('365', text)

    def test_benchmark_difference_requires_matching_full_daily_cohort(self):
        for cohort in ['screening50', None]:
            result = build_details({}, dict(cohort=cohort, reported_daily=dict(cagr=.1)), dict(cagr=.08))
            text = '\n'.join(result['performance_findings'])
            self.assertNotIn('+2.00个百分点', text)
            self.assertIn('不可直接比较', text)
        result = build_details({}, dict(cohort='full_daily', reported_daily=dict(cagr=.1)), dict(cagr=.08))
        self.assertIn('+2.00个百分点', '\n'.join(result['performance_findings']))

    def test_plain_qty_and_zero_pyramiding_are_not_layered_positions(self):
        for declaration in ['', 'strategy("test", pyramiding=0)\n']:
            base = dict(code=declaration + 'strategy.entry("L", strategy.long, qty=contracts)')
            result = build_details(base, dict(features=dict(pyramiding=0)), {})
            self.assertNotIn('加仓/网格/摊薄', [r['feature'] for r in result['engine_compatibility']])
            self.assertIn('qty与仓位规模', [r['feature'] for r in result['engine_compatibility']])

    def test_positive_and_unknown_pyramiding_distinguish_evidence(self):
        result = build_details(dict(code='strategy("test", pyramiding=3)'), {}, {})
        self.assertIn('加仓/网格/摊薄', [r['feature'] for r in result['engine_compatibility']])
        result = build_details(dict(code='strategy("test", pyramiding=layers)'), {}, {})
        rows = [r for r in result['engine_compatibility'] if r['feature'] == '加仓/网格/摊薄']
        self.assertEqual(len(rows), 1)
        self.assertIn('可能配置', rows[0]['impact'])
        self.assertIn('未确认', rows[0]['impact'])

    def test_critical_review_findings_are_prominent_without_score_change(self):
        finding = '退出逻辑只在盈利时平仓，亏损仓位可能无限持有。'
        result = build_details(dict(critical_findings=[finding]), dict(combined_score=61), {})
        self.assertIn(finding, result['overview'])
        self.assertIn(finding, result['verdict'])
        self.assertIn(finding, result['weaknesses'][0])
        self.assertIn('综合分61.00', result['score_interpretation'])

    def test_automatic_rules_recover_disabled_filter_with_nested_context(self):
        code = '\n'.join(['//@version=5', 'strategy("test")', 'useEmaFilter = input.bool(false)', 'ema200 = ta.ema(close, 200)', 'go = close > open', 'if useEmaFilter', '    go := go and close > ema200', 'if go', '    strategy.entry("L", strategy.long)'])
        base = dict(code=code, code_start_line=10, language='PineScript', entry_rules=[dict(line=18, code='L18:     strategy.entry("L", strategy.long)')])
        result = build_details(base, {}, {})
        text = result['entry_steps'][0]
        for evidence in ['useEmaFilter = input.bool(false)', 'L15: if useEmaFilter', 'L16:     go := go and close > ema200', 'L17: if go', '默认关闭', '带控制条件的源码证据切片（非完整执行证明）', '不可顺序执行']:
            self.assertIn(evidence, text)
        self.assertIn('    go :=', text)
        base['entry_explanation'] = ['已精读：默认关闭均线过滤。']
        self.assertEqual(build_details(base, {}, {})['entry_steps'], base['entry_explanation'])

    def test_final_equity_only_when_reported(self):
        result = build_details({}, dict(reported_daily=dict(finalEquity=123456)), {})
        text = '\n'.join(result['performance_findings'])
        self.assertIn('123,456', text)
        self.assertIn('100,000', text)

if __name__ == '__main__':
    unittest.main()
