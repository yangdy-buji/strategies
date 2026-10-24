"""Bounded counterexamples and source contracts; these do NOT execute Pine."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
REVIEWS = json.loads((ROOT / 'analysis/top300/logic_review.json').read_text())

def source(sid, patched=True):
    review = next(r for r in REVIEWS if r['sid'] == sid)
    code = (ROOT / 'analysis/top300' / review['pine_file']).read_text()
    if not patched:
        return code
    records = json.loads((ROOT / 'analysis/top300/execution/batch_2.json').read_text())
    record = next(r for r in records if r['sid'] == sid)
    from tools.strategy_top300.core import resolve_base, apply_record
    return apply_record(resolve_base(ROOT, record), record)

class BatchBCounterexamples(unittest.TestCase):
    def test_803_repeated_cross_preserves_fixed_stop(self):
        old_stop, close = 95, 90
        self.assertFalse(close <= close * .95)  # original reanchor hides breach
        self.assertTrue(close <= old_stop)
        self.assertIn('if (buyCondition and strategy.position_size == 0)', source(803))
        self.assertNotIn('if (buyCondition and strategy.position_size == 0)', source(803, False))

    def test_4000_direction_is_not_a_price(self):
        close, bearish_direction, line = 100, 1, 110
        self.assertTrue(close > bearish_direction)  # original erroneous long
        self.assertFalse(bearish_direction < 0)
        patched = source(4000)
        self.assertIn('ta.supertrend(st_multiplier, st_length)', patched)
        self.assertIn('st_direction < 0', patched)
        self.assertIn('st_direction > 0', patched)

    def test_4632_breakout_quantity_initial_r_and_exit_direction(self):
        close, high, prior_high = 105, 106, 100
        self.assertFalse(close > max(high, prior_high))
        self.assertTrue(close > prior_high)
        budget, entry, stop = 250, 100, 97.5
        qty = budget / (entry-stop)
        self.assertEqual(qty, 100)
        self.assertEqual(qty * (entry-stop), budget)
        profit = 7.5
        self.assertEqual(profit / -profit, -1)
        self.assertEqual(profit / (entry-stop), 3)
        patched = source(4632)
        for fragment in ['ta.highest(high, lookback_support_resistance)[1]', 'amount = position_size_usd', '(close - entry_price) / initial_risk', 'strategy.position_size > 0 and (take_profit_long']:
            self.assertIn(fragment, patched)
        self.assertNotIn('amount = position_size_usd / close', patched)

    def test_3518_rejected_add_does_not_change_average_or_count(self):
        real_average, real_count = 100, 1
        virtual_average = (100 + 80) / 2
        self.assertNotEqual(real_average, virtual_average)
        patched = source(3518)
        self.assertIn('avgEntryPrice = strategy.position_avg_price', patched)
        self.assertIn('entryCount = strategy.opentrades', patched)
        self.assertNotIn('entryCount += 1', patched)
        self.assertNotIn('pyramiding=4', patched)

    def test_374_all_sell_calls_close_existing_long(self):
        patched = source(374)
        self.assertEqual(patched.count('strategy.close("Long", when = Sell_'), 3)
        self.assertNotIn('strategy.entry("Sell", when', patched)

    def test_every_patch_has_unique_applicable_precondition(self):
        records = json.loads((ROOT / 'analysis/top300/execution/batch_2.json').read_text())
        self.assertEqual([r['rank'] for r in records], list(range(101, 201)))
        for r in records:
            self.assertIsInstance(source(r['sid']), str)

class BatchBAdditionalModels(unittest.TestCase):
    def test_volume_threshold_and_zero_mean_cross(self):
        self.assertTrue(bool(161.8))  # old numerical boolean ignores volume=80
        self.assertFalse(80 > 161.8)
        self.assertTrue(200 > 161.8)
        for fragment in ['when=buycond and volume > bigVolume', 'when=buycond2 and volume > bigVolume']:
            self.assertIn(fragment, source(1747))
        previous, current = (-1, 1), (1, -1)
        cross = previous[0] <= previous[1] and current[0] > current[1]
        self.assertTrue(cross)
        self.assertFalse(bool(sum(current) / 2))
        self.assertIn('when=ta.crossover(currMacd, signal) and wasOversold', source(2311))

    def test_signal_event_window_and_ambiguous_outcome(self):
        # Bounded local event model, not order matching or a Pine interpreter.
        def outcome(age, high, low, entry=100, entry_low=95):
            if not 1 <= age <= 7:
                return None
            success, failure = high >= entry * 1.02, low < entry_low
            return 'ambiguous' if success and failure else 'success' if success else 'failure' if failure else 'expired' if age == 7 else None
        self.assertIsNone(outcome(0, 110, 90))
        self.assertEqual(outcome(7, 103, 96), 'success')
        self.assertIsNone(outcome(8, 103, 96))
        self.assertEqual(outcome(1, 103, 94), 'ambiguous')
        self.assertEqual(outcome(7, 101, 96), 'expired')
        patched = source(1289)
        for fragment in ['age >= 1 and age <= 7', 'if success and failure', 'else if success', 'array.remove(signalBars, i)']:
            self.assertIn(fragment, patched)
        self.assertLess(patched.index('for i = array.size'), patched.index('array.push(signalBars'))

    def test_pending_entry_never_runs_fill_exit_and_r_stays_fixed(self):
        # Unfilled limit remains pending; rejection at zero qty must not lock it.
        for qty, expected_pending in [(0, False), (2, True)]:
            pending = qty > 0
            self.assertEqual(pending, expected_pending)
        entry, frozen_r, current_r = 100, .02, .05
        self.assertEqual(entry * (1 - frozen_r), 98)
        self.assertEqual(entry * (1 + 4 * frozen_r), 108)
        self.assertNotEqual(entry * (1 - current_r), 98)
        patched = source(4510)
        for fragment in ['inPosition = strategy.position_size > 0', 'not pendingEntry and R > 0', 'if positionSize > 0', 'entryPrice * (1 - entryR)', 'entryPrice * (1 + 4 * entryR)']:
            self.assertIn(fragment, patched)
        self.assertNotIn('inPosition :=', patched)

    def test_fill_state_and_positive_risk(self):
        self.assertFalse(90 > 95)  # negative initial risk must never open
        self.assertTrue(100 > 95)
        patched = source(267)
        self.assertIn('strategy.position_size == 0 and close > low[1]', patched)
        self.assertIn('inTrade = strategy.position_size > 0', patched)
        self.assertIn('else if high >= takeProfit', patched)
        for sid in [5507, 173]:
            patched = source(sid)
            self.assertIn('strategy.position_avg_price : 0', patched)
            self.assertIn('else if entrySignal', patched)
            self.assertNotIn('Profit pip', patched)

    def test_long_only_loss_and_short_to_long_reversal(self):
        losing_long = 1 > 0 and 95 < 100 and 80 > 70
        self.assertTrue(losing_long)
        self.assertIn('strategy.position_size > 0 and close < strategy.position_avg_price', source(5162))
        self.assertIn('strategy.position_size > 0 and close > strategy.position_avg_price', source(5162))
        self.assertFalse(1 <= 0)  # one open short blocks old opentrades gate
        self.assertTrue(-1 <= 0)  # actual short direction admits long reversal
        self.assertIn('strategy.position_size <= 0 and signal > signal[1]', source(1715))
        self.assertNotIn('if (strategy.opentrades < pyramiding)', source(783))

    def test_clock_and_season_boundaries(self):
        def in_clock(minutes, start, end):
            return start <= minutes <= end if start <= end else minutes >= start or minutes <= end
        self.assertTrue(in_clock(570, 570, 1230))
        self.assertFalse(in_clock(569, 570, 1230))
        self.assertTrue(in_clock(60, 1320, 120))
        self.assertFalse(in_clock(720, 1320, 120))
        self.assertFalse(27 <= 8)  # contradictory original June range
        self.assertEqual([d for d in [8, 9, 26, 27] if d <= 8 or d >= 27], [8, 27])
        patched = source(1588)
        self.assertIn('allowedDay and', patched)
        self.assertIn('(d <= 8 or d >= 27)', patched)

    def test_existing_anchor_retained_and_no_flat_add_more(self):
        self.assertIn('longCondition and strategy.position_size == 0', source(3762))
        self.assertIn('if buymore and strategy.position_size > 0', source(3762))
        self.assertIn('entryCondition1 and strategy.position_size == 0', source(4705))
        self.assertIn('entryPrice := strategy.position_avg_price', source(2867))
        self.assertNotIn('stop_loss_price := float(0)', source(4962))
        self.assertIn('active = strategy.position_size > 0', source(5503))
        self.assertEqual(max(95, 90), 95)  # first fill must retain signal stop

    def test_fib_block_and_broker_ledger_experiments(self):
        high, low = max([120, 110, 100]), min([100, 90, 95])
        self.assertEqual((high, low), (120, 90))
        patched = source(5741)
        self.assertIn('array.set(fibonacciLevels, 4, fibLow)', patched)
        self.assertLess(patched.index('array.set(fibonacciLevels, 4, fibLow)'), patched.index('    fibHigh := na'))
        ledger = source(3362)
        self.assertIn('strategy.position_size == 0 ? strategy.equity : 0.0', ledger)
        self.assertNotIn('usdt_balance +=', ledger)
        self.assertIn('when=sell', source(3133))

class BatchBReviewRegression(unittest.TestCase):
    def test_4632_same_bar_reentry_keeps_new_r(self):
        # Old cleanup-after-entry destroys a newly established signal anchor.
        old_r = None
        old_r = 2.5  # new entry
        old_r = None  # stale previous position cleanup
        self.assertIsNone(old_r)
        new_r = None  # old position cleanup first
        new_r = 2.5
        self.assertEqual(new_r, 2.5)
        patched = source(4632)
        self.assertLess(patched.index('if strategy.position_size == 0 and strategy.position_size[1] != 0'), patched.index('if not breakout_detected'))

    def test_zero_denominator_and_warmup_contracts(self):
        # Undefined ratios are unavailable (NA), not silently neutral or previous.
        def ratio(numerator, denominator):
            return None if numerator is None or denominator is None or denominator <= 0 else numerator / denominator
        self.assertIsNone(ratio(0, 0))
        self.assertIsNone(ratio(None, 1))
        self.assertIsNone(ratio(1, None))
        self.assertEqual(ratio(2, 4), .5)
        fragments = {
            3620: 'SmoothedTrueRange > 0 ?',
            5216: 'gcvMean > 0 ?',
            1819: 'high > low ?',
            4863: 'desvio_padrao_retornos > 0 ?',
            5215: 'sd > 0 ?',
            3528: 'stdev > 0 ?',
            4964: 'double_smoothed_abs_pc > 0 ?',
            1488: 'double_smoothed_abs_pc > 0 ?',
            3829: 'totalWeight != 0 ?',
        }
        for sid, fragment in fragments.items():
            with self.subTest(sid=sid):
                self.assertIn(fragment, source(sid))
                self.assertIn(': na', source(sid))
        self.assertIn('length = input.int(25, title="Volatility Length", minval=1)', source(5216))

    def test_invalid_quantity_is_skipped_not_default_sized(self):
        # NA qty can mean default size in Pine: guard the entry, not just division.
        def allowed(qty):
            return qty is not None and qty > 0
        for qty in [None, 0, -1]:
            self.assertFalse(allowed(qty))
        self.assertTrue(allowed(1))
        for sid, fragment in [(1499, 'enterLong and not na(tradeSize) and tradeSize > 0'), (1791, 'longCondition and not na(positionSize) and positionSize > 0')]:
            self.assertIn(fragment, source(sid))
        self.assertEqual(source(495).count('if strategy.opentrades == 0 and not na(orderSize) and orderSize > 0'), 2)

class BatchBNumericalGuardStructure(unittest.TestCase):
    def test_history_functions_remain_outside_guard_branches(self):
        records = json.loads((ROOT / 'analysis/top300/execution/batch_2.json').read_text())
        guarded_sids = {3620, 5216, 1819, 4863, 5215, 3528, 4964, 1488, 3829, 1499, 1791, 495}
        history_calls = ['ta.rma(', 'ta.sma(', 'ta.ema(', 'ta.dev(', 'ta.stdev(', 'ta.highest(', 'ta.lowest(', 'ta.crossover(', 'rma(', 'sma(', 'ema(']
        for record in records:
            if record['sid'] not in guarded_sids:
                continue
            for patch in record['patches']:
                for line in patch['new'].splitlines():
                    if '?' in line:
                        branch = line.split('?', 1)[1]
                        for call in history_calls:
                            self.assertNotIn(call, branch, (record['sid'], line))
        combined = source(3829)
        self.assertIn('smoothedPlus = ta.rma(plusDM, len)', combined)
        self.assertIn('smoothedMinus = ta.rma(minusDM, len)', combined)
        self.assertIn('cciMean = ta.sma(src, cciLength)', combined)
        self.assertIn('williamsHigh = ta.highest(high, williamsRLength)', combined)
        self.assertIn('validPrices ? sum_gkv', source(5216))
        self.assertIn('buyCross = ta.crossover(p, 0.8)', source(1819))

    def test_4632_new_breakout_is_not_cleared_after_detection(self):
        patched = source(4632)
        cleanup = patched.index('if strategy.position_size == 0 and strategy.position_size[1] != 0')
        detection = patched.index('if final_trend == "up" and close > resistance_level')
        entry = patched.index('if not breakout_detected')
        self.assertLess(cleanup, detection)
        self.assertLess(detection, entry)
        # On a close-fill bar: old latch clears, new breakout sets latch, no new entry.
        breakout = False
        breakout = 105 > 100
        self.assertTrue(breakout)
        self.assertFalse(not breakout)

class BatchB4632BreakoutCooldown(unittest.TestCase):
    def test_each_bar_recomputes_breakout_before_entry(self):
        # Previous candidate's persistent flag never resets after a flat breakout.
        latched = False
        old_allowed = []
        for breakout in [True, False]:
            latched = latched or breakout
            old_allowed.append(not latched)
        self.assertEqual(old_allowed, [False, False])
        current_bar_allowed = [not breakout for breakout in [True, False]]
        self.assertEqual(current_bar_allowed, [False, True])
        self.assertEqual([not breakout for breakout in [True, True]], [False, False])
        patched = source(4632)
        self.assertIn('breakout_detected := false\nif final_trend == "up" and close > resistance_level', patched)
        reset = patched.index('breakout_detected := false\nif final_trend == "up"')
        self.assertLess(reset, patched.index('if not breakout_detected'))

if __name__ == '__main__':
    unittest.main()
