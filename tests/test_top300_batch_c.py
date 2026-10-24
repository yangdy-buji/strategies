"""Source-bound local counterexamples; no Pine compiler or fill simulator."""
import hashlib
import json
import re
import unittest
from pathlib import Path
from tests.safe_expression import evaluate
ROOT = Path(__file__).resolve().parents[1]

def candidate(sid):
    path = ROOT / 'analysis/top300/execution/batch_3.json'
    records = json.loads(path.read_text()) if path.exists() else []
    row = next((r for r in records if r['sid'] == sid), None)
    if row:
        from tools.strategy_top300.core import resolve_base, apply_record
        return apply_record(resolve_base(ROOT, row), row)
    manifest = json.loads((ROOT / 'analysis/top300/pinescript/manifest.json').read_text())
    return (ROOT / 'analysis/top300/pinescript' / next(r['file'] for r in manifest if r['sid'] == sid)).read_text()

class BatchC(unittest.TestCase):
    def test_flag_state_machine_contract_and_counterexamples(self):
        code = candidate(1776)
        # Every transition contract is bound to actual candidate text; arithmetic
        # and predicates below are extracted, not eval'ed or independently invented.
        for fragment in ['var float flagImpulseLow=na', 'var float pullbackLow=na',
                         'pullbackLow:=na', 'impulseBarIndex:=bar_index',
                         'if inFlag and sessActive and bar_index>impulseBarIndex',
                         'pullbackLow:=na(pullbackLow)?low:math.min(pullbackLow,low)',
                         'if inFlag and newHigh and breakoutVolOk', 'inFlag:=false',
                         'strategy.close("Long Flag Breakout",comment="PartialVolExit",qty_percent=50)',
                         'strategy.close("Long Flag Breakout",comment="FullVolExit",qty_percent=100)']:
            self.assertIn(fragment, code)
        expr = re.search(r'retracementPct=([^\n]+)', code).group(1)
        invalid = re.search(r'inFlag:=([^?\n]+)\?false:inFlag', code).group(1)
        gate = re.search(r'if inFlag and sessActive and ([^\n]+)', code).group(1)
        self.assertFalse(evaluate(gate,bar_index=4,impulseBarIndex=4))
        self.assertTrue(evaluate(gate,bar_index=5,impulseBarIndex=4))
        low = None
        for bars, price, expected in [(1,107,30),(2,108,30),(3,104,60)]:
            low = price if low is None else min(low,price)
            pct = evaluate(expr,flagImpulseHigh=110,flagImpulseLow=100,pullbackLow=low)
            self.assertEqual(pct,expected)
            self.assertEqual(evaluate(invalid,retracementPct=pct,maxPullbackPct=50,pullbackBars=bars,maxPullbackBars=5),bars==3)
        self.assertTrue(evaluate(invalid,retracementPct=30,maxPullbackPct=50,pullbackBars=6,maxPullbackBars=5))
        # Reinitializing a new impulse discards the previous low and timer.
        self.assertIn('pullbackLow:=na,pullbackBars:=0,impulseBarIndex:=bar_index',code)
        self.assertEqual(evaluate(expr,flagImpulseHigh=210,flagImpulseLow=200,pullbackLow=207),30)
        self.assertIn('target=approxEntry+rrRatio*risk', code)
        entry = re.search(r'if (inFlag and newHigh and breakoutVolOk)',code).group(1)
        for valid, breakout, volume, expected in [(True,True,True,True),(False,True,True,False),(True,False,True,False),(True,True,False,False)]:
            self.assertEqual(evaluate(entry,inFlag=valid,newHigh=breakout,breakoutVolOk=volume),expected)

    def test_flag_confirmed_close_and_no_held_trade_reanchoring(self):
        code=candidate(1776)
        impulse=re.search(r'if (barstate\.[^\n]+isImpulseBar[^\n]+)',code).group(1)
        self.assertNotIn('barstate.isnew',impulse)
        self.assertIn('barstate.isconfirmed',impulse)
        impulse=impulse.replace('barstate.isconfirmed','confirmed').replace('strategy.position_size','position')
        # Historical bars and realtime close share confirmed=True; realtime
        # opening updates are unconfirmed even though isnew would be true.
        for confirmed,position,expected in [(True,0,True),(True,0,True),(False,0,False),(True,1,False)]:
            self.assertEqual(evaluate(impulse,confirmed=confirmed,position=position,isImpulseBar=True,sessActive=True),expected)
        entry=re.search(r'if (inFlag and newHigh and breakoutVolOk[^\n]*)',code).group(1)
        self.assertIn('strategy.position_size==0',entry)
        for position,expected in [(0,True),(1,False),(-1,False)]:
            self.assertEqual(evaluate(entry.replace('strategy.position_size','position'),inFlag=True,newHigh=True,breakoutVolOk=True,position=position),expected)
        # Protect/reanchor and partial-exit reset remain inside that entry gate.
        entry_start=code.index('    if '+entry)
        partial_section=code.index('// (5) PARTIAL EXIT')
        protected=code[entry_start:partial_section]
        self.assertIn('        strategy.exit("StopTargetExit"',protected)
        self.assertIn('        partialExitUsed:=false,maxVolSinceEntry:=volume',protected)

    def test_smma_and_all_offered_ma_branches(self):
        code = candidate(5078)
        self.assertNotIn('(src[1] * (length - 1) + src) / length',code)
        self.assertIn('smoothing == "SMMA"', code)
        self.assertIn('rma(src, length)',code)
        for label in ['DEMA','TEMA','LSMA','HullMA']:
            self.assertIn('smoothing == "'+label+'"',code)
        self.assertIn('linreg(src, length, 0)',code)

    def test_wait_does_not_restart_and_exit_not_contradictory(self):
        code = candidate(5429)
        self.assertNotIn('downtrend and close > sma and ta.crossover',code)
        self.assertEqual(code.count('if (warunek_wejscia and strategy.position_size == 0)'),2)
        self.assertIn('bar_index - indeks_wejscia >= wait_bars',code)

    def test_exit_quantity_reservations(self):
        code = candidate(3878)
        exits = [x for x in code.splitlines() if x.startswith('strategy.exit(')]
        self.assertEqual(len(exits),8)
        self.assertEqual(len(set(re.search(r'strategy.exit\("([^"]+)',x).group(1) for x in exits)),8)
        self.assertTrue(all('qty_percent=25' in x and 'stop=' in x for x in exits))
        code = candidate(5493)
        self.assertIn('limit=close + (profitTarget * syminfo.mintick), stop=close - (trailingStop * syminfo.mintick)',code)
        self.assertNotIn('trail_points=trailingStop)',code)

    def test_break_even_updates_same_bracket_and_latches(self):
        code=candidate(5240)
        self.assertNotIn('"Exit Buy BE"',code)
        self.assertIn('activeSL := math.max(activeSL, strategy.position_avg_price)',code)
        self.assertIn('if strategy.position_size > 0\n',code)

    def test_price_target_quantity_invariance_and_negative_short_quantity(self):
        code=candidate(3958)
        expr=re.search(r'if (close >= strategy.opentrades.entry_price\(trade_num\) \* 1.30)',code).group(1)
        expr=expr.replace('strategy.opentrades.entry_price(trade_num)','entry_price')
        self.assertFalse(evaluate(expr,close=129,entry_price=100))
        self.assertTrue(evaluate(expr,close=130,entry_price=100))
        self.assertNotIn('strategy.opentrades.profit(trade_num)',code)
        code=candidate(2604)
        self.assertNotIn('qty=strategy.position_size *',code)
        self.assertIn('"Short TP1", "Short"',code)
        branches = re.split(r'(?:else )?if \(takeProfitType == "[^"]+"\)',code)[1:]
        self.assertEqual(len(branches),3)
        for block in branches:
            for side,stop in [('Long','rangeLow'),('Short','rangeHigh')]:
                exits=[line for line in block.splitlines() if 'strategy.exit("'+side in line]
                self.assertEqual(sum(int(re.search(r'qty_percent=(\d+)',line).group(1)) for line in exits),100)
                self.assertTrue(all('stop='+stop in line for line in exits))
        for distance,want in [(10,[105,107.5,115]),(-10,[95,92.5,85])]:
            lines=[line for line in branches[2].splitlines() if 'strategy.exit("Long' in line]
            values=[evaluate(re.search(r'limit=([^,]+)',line).group(1),entryAnchor=100,longDistance=distance) for line in lines]
            self.assertEqual(values,want)

    def test_peak_not_reset_while_in_position_and_date_start(self):
        code=candidate(1557)
        expr=re.search(r'enterTrade = ([^\n]+)',code).group(1).replace('strategy.position_size','position_size')
        for time,size,want in [(99,0,False),(100,0,True),(101,1,False),(101,0,True)]:
            self.assertEqual(evaluate(expr,time=time,entryDate=100,position_size=size),want)
        self.assertIn('highestPrice := math.max(highestPrice, high)',code)

    def test_channel_bracket_first_bar_holding_and_reversal_timing(self):
        code=candidate(2604)
        blocks=re.split(r'(?:else )?if \(takeProfitType == "[^"]+"\)',code)[1:]
        single=blocks[0]
        self.assertNotIn('if strategy.position_size',single)
        self.assertNotIn('entryAnchor',single)
        self.assertIn('limit=rangeHigh, stop=rangeLow',single)
        self.assertIn('limit=rangeLow, stop=rangeHigh',single)
        # Default mode executes after both entry branches without waiting for
        # reported fills; each exit is tied to the intended direction's ID.
        self.assertLess(code.index('strategy.entry("Short"'),code.index('if (takeProfitType'))
        for position,new_entry in [(0,'Long'),(100,'Long'),(100,'Short'),(-100,'Long')]:
            self.assertIn('strategy.exit("'+new_entry+' TP1", "'+new_entry+'"',single)
        # The two experimental modes deliberately wait for a valid held side.
        # These source-extracted predicates document the first-fill gap and
        # prevent applying the old long average to the pending short reversal.
        for block in blocks[1:]:
            predicates=re.findall(r'if (strategy.position_size [<>] 0)',block)
            self.assertEqual(len(predicates),2)
            for size,expected in [(0,[False,False]),(100,[True,False]),(-100,[False,True])]:
                self.assertEqual([evaluate(x.replace('strategy.position_size','size'),size=size) for x in predicates],expected)

    def test_ma_constant_and_step_short_sequences(self):
        code=candidate(5078)
        self.assertIn('if smoothing == "RMA" or smoothing == "SMMA"\n        rma(src, length)',code)
        self.assertIn('linreg(src, length, 0)',code)
        formulas={name: re.search(r'else if smoothing == "'+name+r'"\n        ([^\n]+)',code).group(1) for name in ['DEMA','TEMA']}
        # Local numerical contracts of Pine built-ins, not a Pine interpreter.
        # RMA uses SMA seed and alpha=1/n; EMA uses first sample and 2/(n+1).
        for samples in [[10]*5,[10,10,10,16,16]]:
            smma=sum(samples[:3])/3
            outputs=[smma]
            e1=e2=e3=samples[0]
            demas=[];temas=[];lsmas=[]
            for i,value in enumerate(samples):
                if i>=3:
                    smma=(smma*2+value)/3
                    outputs.append(smma)
                e1=e1+0.5*(value-e1);e2=e2+0.5*(e1-e2);e3=e3+0.5*(e2-e3)
                demas.append(evaluate(formulas['DEMA'],e1=e1,e2=e2,e3=e3))
                temas.append(evaluate(formulas['TEMA'],e1=e1,e2=e2,e3=e3))
                if i>=2:
                    window=samples[i-2:i+1]
                    slope=(window[2]-window[0])/2
                    lsmas.append(sum(window)/3+slope)
            if samples[-1]==10:
                self.assertEqual(outputs,[10,10,10]);self.assertEqual(demas,[10]*5);self.assertEqual(temas,[10]*5);self.assertEqual(lsmas,[10]*3)
            else:
                self.assertEqual(outputs[:2],[10,12]);self.assertAlmostEqual(outputs[2],40/3)
                self.assertEqual(demas[3],14.5);self.assertEqual(temas[3],15.25)
                self.assertEqual(lsmas,[10,15,17])

    def test_zero_denominators_and_sell_before_reset(self):
        for sid,name,values,expected in [(2719,'efficiency_ratio',dict(price_change=0,volatility_sum=0),0),
                                         (2719,'efficiency_ratio',dict(price_change=10,volatility_sum=20),0.5),
                                         (3100,'cmo',dict(sumUp=0,sumDown=0),0),
                                         (3100,'cmo',dict(sumUp=10,sumDown=0),100),
                                         (3100,'cmo',dict(sumUp=0,sumDown=10),-100)]:
            expr=re.search(r'^'+name+r' = ([^\n]+)',candidate(sid),re.M).group(1)
            condition,branches=expr.split('?',1);yes,no=branches.split(':',1)
            result=evaluate(yes if evaluate(condition,**values) else no,**values)
            self.assertEqual(result,expected)
        code=candidate(3112)
        assignment=code.index('sell_condition =')
        reset=code.index('crossed_above_70 := false')
        self.assertLess(assignment,reset)
        expr=re.search(r'sell_condition = ([^\n]+)',code).group(1)
        for delta in [20,40]:
            self.assertTrue(evaluate(expr,crossed_above_70=True,delta_sma=delta,below_60_threshold=50))
        self.assertFalse(evaluate(expr,crossed_above_70=False,delta_sma=20,below_60_threshold=50))

    def test_all_100_hashes_and_sequential_unique_patches(self):
        from tools.strategy_top300.core import resolve_base, apply_record
        rows=json.loads((ROOT/'analysis/top300/execution/batch_3.json').read_text())
        self.assertEqual([r['rank'] for r in rows],list(range(201,301)))
        for row in rows:
            base=resolve_base(ROOT,row)
            self.assertEqual(hashlib.sha256(base.encode()).hexdigest(),row['base_sha256'])
            for patch in row['patches']:
                self.assertEqual(base.count(patch['old']),1,(row['sid'],patch['reason']))
                base=base.replace(patch['old'],patch['new'],1)
                self.assertTrue(patch['reason'] and patch['preserved'] and patch['validation_cases'])
            self.assertTrue(apply_record(resolve_base(ROOT,row),row))
            self.assertTrue(row['remaining'] and row['validation_plan'])

if __name__ == '__main__': unittest.main()
