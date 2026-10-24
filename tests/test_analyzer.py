import hashlib
import importlib
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]

class AnalyzerTests(unittest.TestCase):
    def analyze(self, source, language='PineScript', title='RSI均值回归', description='中文原理\n```\nfake example\n```\n||\nEnglish'):
        module_path = ROOT / 'tools/strategy_catalog/analyzer.py'
        self.assertTrue(module_path.exists(), 'analyzer implementation is missing')
        analyze = importlib.import_module('tools.strategy_catalog.analyzer').analyze
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/'sample.md'
            p.write_text(f'> Name\n\n{title}\n\n> Strategy Description\n\n{description}\n\n> Source ({language})\n\n``` {language}\n{source}\n```\n\n> Detail\n\nhttps://www.fmz.com/strategy/123\n')
            result=analyze(p)
            self.assertEqual(result['source_sha256'],hashlib.sha256(p.read_bytes()).hexdigest())
            self.assertEqual(result['id'],hashlib.sha256(p.name.encode()).hexdigest()[:12])
            self.assertEqual(p.read_text().splitlines()[result['code_start_line']-1],source.splitlines()[0])
            json.dumps(result,ensure_ascii=False)
            return result

    def test_source_section_is_authoritative_and_complete(self):
        code='//@version=5\nstrategy("test")\nfast = ta.ema(close, 10)\nslow = ta.ema(close, 30)\nsignal = ta.crossover(fast, slow)\nif signal\n    strategy.entry("Long", strategy.long)'
        r=self.analyze(code)
        self.assertEqual(r['code'],code)
        self.assertEqual(r['kind'],'strategy')
        self.assertIn('均线',r['family'])
        self.assertEqual(r['category'],'趋势跟随')
        self.assertNotIn('English',r['description'])
        self.assertIn('中文原理',r['description'])
        self.assertEqual(r['source_url'],'https://www.fmz.com/strategy/123')

    def test_multiline_order_outer_conditions_dependencies_absolute_lines(self):
        code='strategy("test")\nfast = ta.ema(close, 10)\nslow = ta.ema(close, 30)\nsignal = ta.crossover(fast, slow)\nallowed = time > 0\nif allowed\n    if signal\n        strategy.entry(\n            "Long",\n            strategy.long,\n            when=signal)'
        r=self.analyze(code); rule=r['entry_rules'][0]
        for expected in ['if allowed','if signal','fast =','slow =','signal =','when=signal)']:
            self.assertIn(expected,rule['code'])
        self.assertEqual(rule['line'],r['code_start_line']+7)
        self.assertIn('未确认',rule['explanation'])

    def test_comments_strings_do_not_create_orders(self):
        r=self.analyze('indicator("test")\n// strategy.entry("a", strategy.long)\n/* strategy.exit("b") */\nlabel = "strategy.entry(fake)"\nplot(close)')
        self.assertEqual(r['kind'],'indicator'); self.assertEqual(r['entry_rules'],[])
        self.assertEqual(r['exit_rules'],[]); self.assertIsNone(r['score'])

    def test_lookahead_is_review_flag_not_cheating_verdict(self):
        r=self.analyze('strategy("test")\nv = request.security(syminfo.tickerid, "D", close[1], lookahead=barmerge.lookahead_on)\nstrategy.entry("a", strategy.long, when=close > v)')
        risk=next(x for x in r['risks'] if 'lookahead' in x['evidence'])
        self.assertIn('核查',risk['title']); self.assertNotIn('作弊',risk['title'])
        self.assertTrue(any('[1]' in x['evidence'] for x in r['risks']))

    def test_score_is_conservative_and_never_performance(self):
        r=self.analyze('strategy("test")\nstrategy.entry("a", strategy.long)\nstrategy.entry("b", strategy.short)')
        self.assertEqual([x['dimension'] for x in r['scores']],['获利机制','信号因果性','规则完整性','风险与仓位','美股执行'])
        self.assertEqual([x['max'] for x in r['scores']],[20,25,20,20,15])
        self.assertEqual(r['score'],sum(x['score'] for x in r['scores']))
        self.assertEqual(r['evidence_level'],'E0'); self.assertIsNone(r['performance_score'])
        self.assertEqual(r['performance_status'],'未验证')
        self.assertTrue(any('反转' in x for x in r['weaknesses']))
        self.assertTrue(any('未识别' in x for x in r['weaknesses']))
        self.assertLess(r['scores'][2]['score'],r['scores'][2]['max'])

    def test_unknown_not_inferred_from_title(self):
        r=self.analyze('hello world',language='unknown',title='神奇均线买卖策略')
        self.assertEqual(r['kind'],'unknown'); self.assertIsNone(r['score'])

    def test_python_comments_do_not_create_orders(self):
        r=self.analyze('"""exchange.Buy(1, 2)"""\n# exchange.Sell(1,2)\ndef main():\n    return 1',language='python')
        self.assertEqual(r['entry_rules'],[])
        self.assertEqual(r['kind'],'unknown')

    def test_unused_indicator_does_not_override_signal_family(self):
        r=self.analyze('strategy("test")\nunused = ta.rsi(close, 14)\nfast = ta.ema(close, 10)\nslow = ta.ema(close, 30)\ngo = ta.crossover(fast, slow)\nstrategy.entry("a", strategy.long, when=go)')
        self.assertEqual(r['family'],'均线信号')
        self.assertNotIn('RSI/Stochastic',r['tags'])

    def test_missing_source_remains_unknown(self):
        analyze=importlib.import_module('tools.strategy_catalog.analyzer').analyze
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/'notes.md';p.write_text('# RSI高收益交易策略\n```\nstrategy("example")\n```')
            r=analyze(p)
            self.assertEqual(r['kind'],'unknown')
            self.assertEqual(r['code'],'')
            self.assertEqual(r['code_start_line'],0)
            self.assertIsNone(r['score'])

    def test_candidate_category_uses_description_and_code(self):
        r=self.analyze('strategy("test")\nr = ta.rsi(close, 14)\nif r < 30\n    strategy.entry("Long", strategy.long, qty=5)\nstrategy.exit("Take", "Long", profit=10, loss=5)',description='## 策略原理\nRSI超卖时买入，等待均值回归。')
        self.assertEqual(r['category'],'均值回归')
        self.assertIn('作者陈述',r['principle'])
        self.assertIn('做多',r['entry_rules'][0]['explanation'])
        self.assertIn('r < 30',r['entry_rules'][0]['explanation'])
        self.assertIn('qty=5',r['entry_rules'][0]['explanation'])
        self.assertIn('profit=10',r['exit_rules'][0]['explanation'])
        self.assertIn('loss=5',r['exit_rules'][0]['explanation'])

    def test_principle_keeps_nested_headings(self):
        r=self.analyze('strategy("test")',description='### 策略原理\n#### 123反转策略\n先检测反转。\n#### STARC通道\n再确认通道。\n### 策略优势\n这段不属于原理。')
        self.assertIn('先检测反转',r['principle'])
        self.assertIn('再确认通道',r['principle'])
        self.assertNotIn('这段不属于原理',r['principle'])

    def test_empty_principle_falls_back_to_author_description(self):
        r=self.analyze('strategy("test")',description='作者开头说明。\n## 策略原理\n## 总结\n这是作者总结。')
        self.assertIn('作者开头说明',r['principle'])
        self.assertIn('回退',r['principle'])
        self.assertIn('作者',r['principle'])
        self.assertNotIn('未提供',r['principle'])

    def test_unclassified_never_has_medium_confidence(self):
        r=self.analyze('strategy("test")\nstrategy.entry("a", strategy.long)',description='说明')
        self.assertEqual(r['category'],'待分类')
        self.assertEqual(r['classification_confidence'],'低')

    def test_tuple_assignment_dependencies_reveal_macd_family(self):
        r=self.analyze('strategy("test")\nfast = 12\nslow = 26\n[macdLine, signalLine, _] = ta.macd(close, fast, slow, 9)\nlongCondition = ta.crossover(macdLine, signalLine)\nif longCondition\n    strategy.entry("Long", strategy.long)')
        self.assertEqual(r['family'],'MACD趋势动量')
        self.assertIn('[macdLine, signalLine, _] = ta.macd',r['entry_rules'][0]['code'])
        self.assertIn('fast = 12',r['entry_rules'][0]['code'])
        self.assertIn('slow = 26',r['entry_rules'][0]['code'])

    def test_multiline_outer_if_is_complete_in_slice_and_explanation(self):
        r=self.analyze('var limit = 20;\nfunction main() {\n    if (close > 10 &&\n        volume > limit) {\n        exchange.Buy(-1, 1);\n    }\n}',language='javascript')
        rule=r['entry_rules'][0]
        self.assertIn('volume > limit',rule['code'])
        self.assertIn('volume > limit',rule['explanation'])
        self.assertIn('var limit = 20',rule['code'])

    def test_real_tuple_and_multiline_control_regressions(self):
        analyze=importlib.import_module('tools.strategy_catalog.analyzer').analyze
        macd=analyze(ROOT/'Advanced-MACD-Strategy-with-Limited-Martingale-基于有限马丁格尔的高级MACD策略.md')
        self.assertEqual(macd['family'],'MACD趋势动量')
        self.assertIn('L108: [macdLine, signalLine, _]',macd['entry_rules'][0]['code'])
        volatility=analyze(ROOT/'吕神-简易波动率策略.md')
        rule=volatility['entry_rules'][0]
        self.assertIn('vix_arr[vix_arr.length - 2] <= vix_ma_up',rule['code'])
        self.assertIn('vix_arr[vix_arr.length - 2] <= vix_ma_up',rule['explanation'])

    def test_root_readme_is_auxiliary_material(self):
        analyze=importlib.import_module('tools.strategy_catalog.analyzer').analyze
        r=analyze(ROOT/'README.md')
        self.assertEqual(r['kind'],'tool')
        self.assertEqual(r['category'],'辅助资料')
        self.assertIsNone(r['score'])
        self.assertIn('Financial Magic Zone',r['description'])

    def test_real_formats(self):
        module_path=ROOT/'tools/strategy_catalog/analyzer.py'
        self.assertTrue(module_path.exists(),'analyzer implementation is missing')
        analyze=importlib.import_module('tools.strategy_catalog.analyzer').analyze
        for filename,kind in [('超级趋势策略SuperTrend-Strategy.md','strategy'),('仿Promise异步模板.md','tool'),('移植-OKCoin-韭菜收割机-注释python版.md','strategy'),('交易终端插件范例.md','tool')]:
            r=analyze(ROOT/filename)
            self.assertEqual(r['kind'],kind,filename)
            self.assertGreater(len(r['code']),100)
            if kind=='tool': self.assertIsNone(r['score'])

if __name__=='__main__': unittest.main()
