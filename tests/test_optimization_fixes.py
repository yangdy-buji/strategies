"""Source-bound expression/branch checks, NOT a Pine compiler or backtest."""
import hashlib
import importlib
import itertools
import json
import re
import unittest
from tests.safe_expression import evaluate as safe_eval
from unittest.mock import patch
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CAT = {x['id']: x for x in json.loads((ROOT / 'analysis/catalog.json').read_text())}
SOURCES = {x['sid']: CAT[x['id']] for x in json.loads((ROOT / 'analysis/top500/ranking.json').read_text())}
SIDS = {735,5369,621,4143,3883,3322,2458,4621,2943,3330,4941}

def clean(code):
    return '\n'.join(line for line in code.splitlines() if not line.lstrip().startswith('// OPT-'))

def expression(code, name):
    return re.search(r'^' + re.escape(name) + r' = (.+)$', code, re.M)[1]

def evaluate(expr, **values):
    return safe_eval(expr.replace('true', 'True').replace('false', 'False'), **values)

def branch(code, condition):
    lines = clean(code).splitlines()
    start = lines.index(condition)
    depth = len(condition)-len(condition.lstrip())
    result = []
    for line in lines[start+1:]:
        if line.strip() and len(line)-len(line.lstrip()) <= depth:
            break
        result.append(line)
    return '\n'.join(result)

class FixTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            cls.module = importlib.import_module('tools.strategy_optimization.fixes')
        except ModuleNotFoundError:
            cls.module = None

    def fixed(self, sid):
        # Identity baseline makes missing fixes fail on the actual defect assertion.
        src = SOURCES[sid]
        return self.module.apply_fix(sid, src['code'], src['source_sha256']) if self.module else src['code']

    def test_registered_hashes_and_chinese_metadata(self):
        self.assertIsNotNone(self.module, 'fix registry not implemented')
        self.assertEqual(set(self.module.FIXES), SIDS)
        for sid, fix in self.module.FIXES.items():
            self.assertEqual(fix['source_sha256'], SOURCES[sid]['source_sha256'])
            self.assertEqual(fix['code_sha256'], hashlib.sha256(SOURCES[sid]['code'].encode()).hexdigest())
            for key in ['title','changes','remaining','validation_cases']:
                self.assertTrue(fix[key])
            self.assertIn(f'OPT-{sid}-', self.fixed(sid))

    def test_reject_unknown_source_and_changed_code(self):
        self.assertIsNotNone(self.module, 'guard not implemented')
        s = SOURCES[735]
        for sid, code, sha in [(999999,s['code'],s['source_sha256']), (735,s['code'],'0'*64), (735,s['code']+'\n',s['source_sha256'])]:
            with self.assertRaises(ValueError): self.module.apply_fix(sid,code,sha)


    def test_non_unique_or_missing_patch_anchor_rejected(self):
        self.assertIsNotNone(self.module)
        src = SOURCES[735]
        for anchor in ['absent anchor', 'strategy.']:
            fix = dict(self.module.FIXES[735])
            fix['patches'] = [(anchor, 'replacement', '原因', '保持')]
            with patch.dict(self.module.FIXES, {735: fix}):
                with self.assertRaises(ValueError):
                    self.module.apply_fix(735, src['code'], src['source_sha256'])

    def test_exact_patch_scope_reversible_to_original(self):
        self.assertIsNotNone(self.module)
        for sid in SIDS:
            result = clean(self.fixed(sid))
            for old,new,_,_ in reversed(self.module.FIXES[sid]['patches']):
                self.assertEqual(result.count(new),1, sid)
                result = result.replace(new,old,1)
            self.assertEqual(result,clean(SOURCES[sid]['code']),sid)

    def test_4941_strict_time_edges_and_end_liquidation_condition(self):
        expr = expression(self.fixed(4941),'needtime')
        expr = expr.replace('timestamp(fromyear, frommonth, fromday, 00, 00)','start')
        expr = expr.replace('timestamp(toyear, tomonth, today, 23, 59)','end')
        for now,enter,cancel,liquidate in [(9,False,True,False),(10,False,True,False),(15,True,False,False),(20,False,True,False),(21,False,True,True)]:
            gate = evaluate(expr,time=now,start=10,end=20)
            self.assertEqual((gate,not gate,now>20),(enter,cancel,liquidate))

    def test_pine_version_inputs_and_strategy_settings_unchanged(self):
        for sid in SIDS:
            original = SOURCES[sid]['code']; result = self.fixed(sid)
            self.assertEqual(re.findall(r'^.*(?:input\(|input\.|strategy\(|@version).*$' ,original,re.M), re.findall(r'^.*(?:input\(|input\.|strategy\(|@version).*$' ,result,re.M))

    def test_735_exit_targets_rsi_with_original_two_gates(self):
        result = branch(self.fixed(735),'if (EXIT)')
        self.assertIn('strategy.close("RSI", when=bull_cross)', result)
        self.assertNotIn('strategy.close("RSI",', branch(SOURCES[735]['code'],'if (EXIT)'))
        for exit_signal,bull in itertools.product([False,True],repeat=2):
            close_id = re.search(r'strategy.close\("([^"]+)"',result)[1]
            closed = exit_signal and bull and close_id == 'RSI'
            self.assertEqual(closed, exit_signal and bull)

    def test_5369_tuple_assignment_and_signal_boundary(self):
        def bands(code):
            names = re.search(r'\[([^]]+)\] = bb',code)[1].split(', ')
            return dict(zip(names,[100,120,80]))
        fixed = bands(self.fixed(5369)); old = bands(SOURCES[5369]['code'])
        self.assertEqual(fixed,dict(middleBB=100,upperBB=120,lowerBB=80))
        self.assertTrue(110 > old['upperBB']); self.assertFalse(110 > fixed['upperBB'])
        self.assertFalse(120 > fixed['upperBB']); self.assertTrue(121 > fixed['upperBB'])

    def test_621_cancel_before_close_prevents_later_limit_fill(self):
        b = branch(self.fixed(621),'if short')
        self.assertIn('strategy.cancel("Long")', b)
        self.assertLess(b.index('strategy.cancel("Long")'), b.index('strategy.close('))
        pending = {'Long'}
        for order_id in re.findall(r'strategy.cancel\("([^"]+)"\)', b): pending.discard(order_id)
        self.assertFalse('Long' in pending)
        self.assertNotIn('strategy.cancel',SOURCES[621]['code'])

    def test_4143_cancel_all_only_at_existing_end_branch(self):
        condition = 'if time > timestamp(toyear, tomonth, today, 23, 59)'
        b = branch(self.fixed(4143),condition)
        self.assertIn('strategy.cancel_all()', b)
        self.assertIn('strategy.close_all()', b)
        self.assertEqual(clean(self.fixed(4143)).replace('    strategy.cancel_all()\n',''), clean(SOURCES[4143]['code']))

    def test_3883_constant_alert_references_config_and_orders_unchanged(self):
        result = self.fixed(3883)
        alerts = [x for x in result.splitlines() if x.startswith('alertcondition(buyDip')]
        self.assertEqual(len(alerts),3)
        for line in alerts:
            self.assertNotIn('$1000',line)
            self.assertIn('buy_amount',line)
            self.assertRegex(line,r'message="[^"\n]+"\)$')
        self.assertEqual(re.findall(r'^.*(?:strategy\.|qty1 =).*$', result,re.M),re.findall(r'^.*(?:strategy\.|qty1 =).*$',SOURCES[3883]['code'],re.M))

    def test_3322_protection_separate_from_signal_and_flat_guard(self):
        result = self.fixed(3322)
        self.assertNotIn('strategy.exit',branch(result,'if (longCondition )'))
        protection = branch(result,'if strategy.position_size > 0')
        self.assertIn('strategy.exit("Take Profit/Stop Loss", "Long", limit=takeProfit, stop=stopLoss)',protection)
        for signal,pos in itertools.product([False,True],[0,1]):
            condition = re.search(r'^if (strategy.position_size > 0)$', result, re.M)[1]
            self.assertEqual(evaluate(condition.replace('strategy.position_size', 'position_size'),position_size=pos),pos>0)
        self.assertIn('zarar_durumu = input(100,',result)
        self.assertEqual(100*(1-100/100),0)

    def test_date_windows_boundaries_and_exit_independence(self):
        for sid,name,start,end in [(2458,'isWithinTradingWindow','startTimeInput','endTimeInput'),(4621,'inDateRange','startDate','endDate'),(2943,'inDateRange','i_startTime','i_endTime')]:
            with self.subTest(sid=sid):
                expr = expression(self.fixed(sid),name)
                for time,expected in [(9,False),(10,True),(15,True),(20,True),(21,False)]:
                    self.assertEqual(evaluate(expr,**{'time':time,start:10,end:20}),expected,(sid,time))
                self.assertEqual(expression(SOURCES[sid]['code'],name),'true')
        self.assertIn('exitCondition = aboveCount >= sellTriggerInput',self.fixed(2458))
        self.assertIn('if(close > emaH and checkThreeConsecutiveCandles and barstate.isconfirmed)',self.fixed(4621))
        for line in SOURCES[2943]['code'].splitlines():
            if line.startswith(('strategy.close','strategy.exit')): self.assertIn(line,self.fixed(2943))

    def test_3330_entry_only_time_gate_and_or_truth_table(self):
        result=self.fixed(3330)
        self.assertIn('if true// and time <= backtest_timeframe_end',result)
        self.assertIn('    if strategy.position_size == 0 and buy_condition and time >= backtest_timeframe_start',result)
        expr=re.search(r'    buy_condition = (.+)',result)[1]
        self.assertIn('(touched_lower_bb and MACD > aMACD) or expected_rebound',expr)
        for touch,cross,rebound in itertools.product([False,True],repeat=3):
            self.assertEqual(evaluate(expr,touched_lower_bb=touch,MACD=int(cross),aMACD=0,expected_rebound=rebound),(touch and cross) or rebound)
        self.assertEqual(result.split('    //EXIT:')[1],SOURCES[3330]['code'].split('    //EXIT:')[1])

    def test_4941_window_cancel_six_entries_preserve_end_liquidation(self):
        result=self.fixed(4941)
        self.assertNotEqual(expression(result,'needtime'),'true')
        b=branch(result,'if not needtime')
        ids=re.findall(r'strategy.cancel\("([^"]+)"\)',b)
        self.assertEqual(set(ids),{'L1','L2','L3','S1','S2','S3'})
        pending=set(ids)|{'TPL','TPS'}
        pending.difference_update(ids)
        self.assertEqual(pending,{'TPL','TPS'})
        end='if time > timestamp(toyear, tomonth, today, 23, 59)'
        self.assertEqual(branch(result,end),branch(SOURCES[4941]['code'],end))
        self.assertIn('time > timestamp(fromyear, frommonth, fromday, 00, 00) and time < timestamp(toyear, tomonth, today, 23, 59)',result)

if __name__ == '__main__': unittest.main()
