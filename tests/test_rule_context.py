import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / 'tools/strategy_ranking/context.py'


class RuleContextTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(MODULE.exists(), 'control-flow enrichment is not implemented')
        spec = importlib.util.spec_from_file_location('rule_context', MODULE)
        self.mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.mod)

    def enrich(self, code, selected, start=1):
        return self.mod.enrich_rule(dict(code=code, code_start_line=start),
                                    dict(code='\n'.join(f'L{i + start}: {code.splitlines()[i]}' for i in selected)))

    def test_real_2458_preserves_optional_ema_default_and_period(self):
        path = next(ROOT.glob('*Mean-Reversion-Consecutive-Candle-Reversal-Trading-Strategy.md'))
        lines = path.read_text().splitlines()
        start = next(i for i, line in enumerate(lines) if line.startswith('``` pinescript')) + 1
        end = next(i for i in range(start, len(lines)) if lines[i].startswith('```'))
        code = '\n'.join(lines[start:end])
        selected = [i for i, line in enumerate(code.splitlines()) if 'longCondition :=' in line or 'strategy.entry(' in line]
        result = self.enrich(code, selected, start + 1)
        for text in ['if useEmaFilter', 'useEmaFilter = input.bool(false', 'emaPeriodInput = input.int(200', 'emaValue = ta.ema(close, emaPeriodInput)', 'if longCondition']:
            self.assertIn(text, result)
        self.assertIn(f'L{start + selected[0] + 1}:     longCondition :=', result)

    def test_nested_else_multiline_tuple_and_balanced_condition(self):
        code = '''//@version=6
useFilter = input.bool(false)
[a,
 b] = ta.macd(close, 12, 26, 9)
if useFilter and (
     a > b)
    if close > open
        signal = true
    else
        signal = false
else
    signal = true
if signal
    strategy.entry("L", strategy.long)'''
        result = self.enrich(code, [9, 13])
        for i, line in enumerate(code.splitlines(), 1):
            if i > 1:
                self.assertIn(f'L{i}: {line}', result)

    def test_simple_unconditional_order(self):
        result = self.enrich('//@version=5\nstrategy.entry("L", strategy.long)', [1])
        self.assertIn('L2: strategy.entry("L", strategy.long)', result)

    def test_unknown_language_or_missing_lines_warns(self):
        result = self.enrich('def run():\n    buy()', [1])
        self.assertIn('片段未恢复完整控制流，不可顺序执行', result)
        result = self.mod.enrich_rule({'code': '//@version=5\nx=1', 'code_start_line': 1}, {'code': 'L300: strategy.entry("L", strategy.long)'})
        self.assertIn('片段未恢复完整控制流，不可顺序执行', result)
        self.assertIn('L300:', result)

    def test_deterministic_explicit_cap(self):
        code = '//@version=5\n' + '\n'.join(f'x{i} = x{i-1}' for i in range(600)) + '\nstrategy.entry("L", strategy.long, qty=x599)'
        first = self.enrich(code, [601])
        self.assertEqual(first, self.enrich(code, [601]))
        self.assertIn('截断', first)
        self.assertIn('片段未恢复完整控制流，不可顺序执行', first)


if __name__ == '__main__':
    unittest.main()
