"""Local scalar counterexamples; not a Pine compiler or broker emulator."""
import ast
import json
import math
import operator
import os
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


def code_for(sid):
    manifest = json.loads((ROOT / 'analysis/top300/pinescript/manifest.json').read_text())
    item = next(x for x in manifest if x['sid'] == sid)
    original = (ROOT / 'analysis/top300/pinescript' / item['file']).read_text()
    if os.environ.get('TOP300_TEST_ORIGINAL') == '1':
        return original
    from tools.strategy_top300.core import resolve_base, apply_record
    records = json.loads((ROOT / 'analysis/top300/execution/batch_1.json').read_text())
    record = next(x for x in records if x['sid'] == sid)
    return apply_record(resolve_base(ROOT, record), record)


def rhs(code, variable):
    return re.search(r'^\s*' + re.escape(variable) + r'\s*:?=\s*(.+)$', code, re.M)[1].split('//')[0].strip()


def scalar(expression, values, reject_zero=False):
    """Only whitelisted arithmetic/comparison AST nodes and lazy Pine ternary.

    Precomputed series calls/history are explicit inputs, so no untrusted code
    executes. Zero division models Pine undefined numeric output as NaN.
    """
    for key in sorted(values, key=len, reverse=True):
        if '(' in key or '[' in key:
            expression = expression.replace(key, str(values[key]))
    depth = 0
    q = None
    nesting = 0
    for i, ch in enumerate(expression):
        if ch == '(':
            depth += 1
        elif ch == ')':
            depth -= 1
        elif depth == 0 and ch == '?':
            if q is None:
                q = i
            else:
                nesting += 1
        elif depth == 0 and ch == ':' and q is not None:
            if nesting:
                nesting -= 1
            else:
                condition = scalar(expression[:q], values, reject_zero)
                branch = expression[q+1:i] if condition and not (isinstance(condition, float) and math.isnan(condition)) else expression[i+1:]
                return scalar(branch.strip(), values, reject_zero)
    binary = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul}
    compare = {ast.Eq: operator.eq, ast.NotEq: operator.ne, ast.Gt: operator.gt, ast.Lt: operator.lt, ast.GtE: operator.ge, ast.LtE: operator.le}
    def visit(node):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.Name):
            return float('nan') if node.id in ('na', 'nan') else values[node.id]
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            return -visit(node.operand)
        if isinstance(node, ast.BinOp):
            a, b = visit(node.left), visit(node.right)
            if isinstance(node.op, ast.Div):
                if reject_zero and b == 0:
                    raise AssertionError('Undefined division reached')
                return a / b if b else float('nan')
            return binary[type(node.op)](a, b)
        if isinstance(node, ast.Compare) and len(node.ops) == 1:
            a, b = visit(node.left), visit(node.comparators[0])
            if math.isnan(a) or math.isnan(b):
                return False
            return compare[type(node.ops[0])](a, b)
        if isinstance(node, ast.Call):
            name = ast.unparse(node.func)
            args = [visit(a) for a in node.args]
            if name == 'ta.sma' and '__series_call__' in values:
                return values['__series_call__'](ast.unparse(node.args[0]), *args)
            if name in ('abs', 'math.abs'):
                return abs(args[0])
            if name == 'na':
                return math.isnan(args[0])
        raise AssertionError('Unsupported scalar syntax: ' + ast.dump(node))
    return visit(ast.parse(expression.strip(), mode='eval').body)


class BatchABehaviorTests(unittest.TestCase):
    def test_ad_flat_bar_preserves_accumulator(self):
        code = code_for(4228)
        values = dict(high=10, low=10, close=10, volume=100)
        values['ad[1]'] = 75
        if 'adIncrement =' in code:
            values['adIncrement'] = scalar(rhs(code, 'adIncrement'), values)
        self.assertEqual(scalar(rhs(code, 'ad'), values), 75)

    def test_volume_multiplier_flat_and_regular(self):
        expr = rhs(code_for(4228), 'moneyFlowMultiplier')
        self.assertEqual(scalar(expr, dict(high=10, low=10, close=10)), 0)
        self.assertEqual(scalar(expr, dict(high=12, low=8, close=11)), .5)

    def test_mfi_one_sided_and_no_flow(self):
        expr = rhs(code_for(4228), 'mfi')
        for pos, neg, expected in [(10, 0, 100), (0, 10, 0), (30, 10, 75)]:
            self.assertEqual(scalar(expr, dict(positiveFlow=pos, negativeFlow=neg)), expected)
        self.assertTrue(math.isnan(scalar(expr, dict(positiveFlow=0, negativeFlow=0))))

    def test_cmf_zero_volume_is_neutral_and_warmup_undefined(self):
        expr = rhs(code_for(4228), 'cmf')
        for den, num, expected in [(0, 0, 0), (10, 5, .5)]:
            values = {'ta.sma(volume, lengthCMF)': den, 'ta.sma(moneyFlowVolume, lengthCMF)': num, 'avgVolume': den, 'avgMoneyFlowVolume': num}
            self.assertEqual(scalar(expr, values), expected)
        self.assertTrue(math.isnan(scalar(expr, {'ta.sma(volume, lengthCMF)': float('nan'), 'ta.sma(moneyFlowVolume, lengthCMF)': float('nan'), 'avgVolume': float('nan'), 'avgMoneyFlowVolume': float('nan')})))

    def test_di_dx_flat_and_regular(self):
        for sid, denominator, period in [(1622, 'trur', 'adxLen'), (5389, 'atrValue', 'adxPeriod')]:
            with self.subTest(sid=sid):
                code = code_for(sid)
                for tr, plus, minus in [(0, 0, 0), (4, 2, 1), (float('nan'), 0, 0)]:
                    values = {denominator: tr, f'ta.rma(plusDM, {period})': plus, f'ta.rma(minusDM, {period})': minus}
                    values.update(smoothedPlusDM=plus, smoothedMinusDM=minus)
                    values['plusDI'] = scalar(rhs(code, 'plusDI'), values)
                    values['minusDI'] = scalar(rhs(code, 'minusDI'), values)
                    dx = scalar(rhs(code, 'dx'), values)
                    if math.isnan(tr):
                        self.assertTrue(math.isnan(dx))
                    else:
                        self.assertAlmostEqual(dx, 0 if tr == 0 else 100 / 3)

    def test_cmo_flat_then_directional(self):
        expr = rhs(code_for(3159), 'vCMO')
        for up, down, expected in [(0, 0, 0), (3, 1, .5), (0, 3, -1)]:
            self.assertEqual(scalar(expr, dict(vUD=up, vDD=down)), expected)
        self.assertTrue(math.isnan(scalar(expr, dict(vUD=float('nan'), vDD=float('nan')))))

    def test_er_flat_then_trend(self):
        code = code_for(3458)
        expr = next(l.strip() for l in code.splitlines() if l.strip().endswith('net / total') or 'total == 0 ?' in l)
        self.assertEqual(scalar(expr, dict(net=0, total=0)), 0)
        self.assertEqual(scalar(expr, dict(net=4, total=4)), 1)
        self.assertEqual(scalar(expr, dict(net=2, total=4)), .5)

    def test_macd_normalization_zero_range_is_explicitly_undefined(self):
        code = code_for(1603)
        expr = rhs(code, 'normalizedMacd')
        for low, high, current, expected in [(5, 5, 5, None), (0, 10, 5, 50), (0, 10, 10, 80), (float('nan'), float('nan'), 5, None)]:
            with self.subTest(low=low, high=high):
                values = {'ta.lowest(macdLine, lengthRSI)': low,
                          'ta.highest(macdLine, lengthRSI)': high,
                          'macdLine': current, 'lowestK': 20, 'highestK': 80, 'macdLow': low, 'macdHigh': high}
                if 'macdRange =' in code:
                    values['macdRange'] = scalar(rhs(code, 'macdRange'), values)
                actual = scalar(expr, values, reject_zero=True)
                if expected is None:
                    self.assertTrue(math.isnan(actual))
                else:
                    self.assertEqual(actual, expected)

    def test_history_calls_are_unconditional_before_scalar_guards(self):
        cases = [(4228, ['cmf'], ['ta.sma(moneyFlowVolume, lengthCMF)', 'ta.sma(volume, lengthCMF)']),
                 (1622, ['plusDI', 'minusDI'], ['ta.rma(plusDM, adxLen)', 'ta.rma(minusDM, adxLen)']),
                 (5389, ['plusDI', 'minusDI'], ['ta.rma(plusDM, adxPeriod)', 'ta.rma(minusDM, adxPeriod)']),
                 (1603, ['normalizedMacd'], ['ta.lowest(macdLine, lengthRSI)', 'ta.highest(macdLine, lengthRSI)'])]
        for sid, guards, calls in cases:
            with self.subTest(sid=sid):
                code = code_for(sid)
                for guard in guards:
                    self.assertNotIn('ta.', rhs(code, guard))
                for call in calls:
                    lines = [line for line in code.splitlines() if call in line]
                    self.assertEqual(len(lines), 1)
                    self.assertNotIn('?', lines[0])
                    self.assertEqual(lines[0], lines[0].lstrip())
                    self.assertLess(code.index(lines[0]), min(code.index(g + ' ') for g in guards))

    def test_cmf_zero_window_then_volume_recovery(self):
        code = code_for(4228)
        buffers = {}
        actual = None
        for volume, money in [(100, 100)] * 3 + [(0, 0)] * 5 + [(100, 50)]:
            cache = {}
            def series(source, value, length):
                if source not in cache:
                    history = buffers.setdefault(source, [])
                    history.append(value)
                    cache[source] = sum(history[-length:]) / length if len(history) >= length else float('nan')
                return cache[source]
            values = dict(volume=volume, moneyFlowVolume=money, lengthCMF=3, __series_call__=series)
            for name in ['avgMoneyFlowVolume', 'avgVolume']:
                if name + ' =' in code:
                    values[name] = scalar(rhs(code, name), values)
            actual = scalar(rhs(code, 'cmf'), values)
        self.assertEqual(actual, .5)
        self.assertEqual(len(buffers['moneyFlowVolume']), 9)

    def test_indicator_length_inputs_reject_zero_and_negative(self):
        code = code_for(3900)
        for var in ['diLength', 'adxSmoothing', 'supertrendPeriod', 'rsiLength']:
            expr = rhs(code, var)
            match = re.search(r'minval\s*=\s*(\d+)', expr)
            minimum = int(match[1]) if match else -math.inf
            default = int(re.search(r'input.int\((\d+)', expr)[1])
            for invalid in [-1, 0]:
                self.assertFalse(invalid >= minimum, var)
            self.assertTrue(default >= minimum)


if __name__ == '__main__':
    unittest.main()
