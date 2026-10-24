"""Small source-derived arithmetic/branch checks, not a Pine compiler or broker."""
import hashlib
import json
from pathlib import Path
import re
import unittest
from tests.safe_expression import evaluate as safe_eval
from tools.strategy_optimization.fixes import apply_fix

ROOT=Path(__file__).resolve().parents[1]


class NewRepairBehaviors(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        catalog={r['id']:r for r in json.loads((ROOT/'analysis/catalog.json').read_text())}
        ranking=json.loads((ROOT/'analysis/top500/ranking.json').read_text())
        cls.sources={r['sid']:catalog[r['id']] for r in ranking}
        cls.audits={r['sid']:r for p in (ROOT/'analysis/top500/optimization/audit').glob('batch_*.json') for r in json.loads(p.read_text())}

    def code(self,sid,fixed=True):
        source=self.sources[sid]
        if not fixed:return source['code']
        r=self.audits[sid]
        registry={sid:dict(source_sha256=r['source_sha256'],code_sha256=r['code_sha256'],patches=[(p['old'],p['new'],p['reason'],p['preserved']) for p in r['patches']])}
        return apply_fix(sid,source['code'],source['source_sha256'],registry=registry)

    def test_short_distance_upper_bound_rejects_oversized_risk(self):
        def accepts(code,distance):
            expression=re.search(r'\((bearentryh(?:igh)? - bearentryh(?:igh)?)\) <= 10\.40',code)[1]
            values={'bearentryh':100,'bearentryhigh':100+distance}
            left,right=expression.split(' - ')
            return values[left]-values[right]<=10.40
        self.assertTrue(accepts(self.code(2,False),20))
        self.assertFalse(accepts(self.code(2),20))
        self.assertTrue(accepts(self.code(2),10))

    def test_dmi_third_output_is_adx(self):
        for sid in [1223,3295,3984]:
            code=self.code(sid)
            names=[x.strip() for x in re.search(r'\[([^]]+)\]\s*=\s*ta.dmi',code)[1].split(',')]
            values=dict(zip(names,[30,12,18]))
            self.assertEqual(values['adx'],18)
            self.assertFalse(values['adx']>25)
            old=[x.strip() for x in re.search(r'\[([^]]+)\]\s*=\s*ta.dmi',self.code(sid,False))[1].split(',')]
            self.assertEqual(dict(zip(old,[30,12,18]))['adx'],30)

    def test_short_target_below_entry(self):
        def target(code):
            code='\n'.join(l for l in code.splitlines() if not l.lstrip().startswith('// OPT-'))
            expression=re.search(r'if \(shortCondition[^\n]*\n\s*entryPrice := close\n\s*takeProfit := (.+)',code)[1]
            # Controlled arithmetic expression from the reviewed, hash-bound source.
            return safe_eval(expression,entryPrice=100,atr=2,atrMultiplier=2,riskRewardRatio=3)
        self.assertGreater(target(self.code(1990,False)),100)
        self.assertEqual(target(self.code(1990)),88)

    def test_bearish_lower_wick_excludes_body(self):
        def wick(code):
            expression=re.search(r'^\s*lowerWickSize = (.+)$',code,re.M)[1]
            return safe_eval(expression,open=[0,105],close=[0,101],low=[0,100])
        self.assertEqual(wick(self.code(4707,False)),5)
        self.assertEqual(wick(self.code(4707)),1)

    def test_season_handles_all_month_ranges(self):
        expr=re.search(r'^inSeason = (.+)$',self.code(1791),re.M)[1]
        condition,arms=expr.split('?',1);yes,no=arms.split(':',1)
        for start in range(1,13):
            for end in range(1,13):
                for month in range(1,13):
                    values=dict(startMonth=start,endMonth=end,currentMonth=month)
                    chosen=yes if safe_eval(condition,**values) else no
                    actual=safe_eval(chosen.strip(),**values)
                    expected=start<=month<=end if start<=end else month>=start or month<=end
                    self.assertEqual(actual,expected)

    def test_darvas_lengths_are_positive_at_minimum(self):
        for sid in [235,1644]:
            line=next(l for l in self.code(sid).splitlines() if l.startswith('boxp = input.int'))
            minimum=int(re.search(r'minval\s*=\s*(\d+)',line)[1])
            self.assertGreater(minimum-2,0)

    def test_grid_fifteenth_entry_and_atr_parameter(self):
        code=self.code(1506)
        block=re.search(r'if \(longCondition15\).*?\n\s*strategy.entry\("([^"]+)"',code,re.S)
        self.assertEqual(block[1],'Long15')
        self.assertIn('strategy.close("Long15"',code)
        self.assertIn('atr = ta.atr(atr_len)',code)

    def test_event_based_state_reset_ignores_old_closed_trade(self):
        for sid in [65,496]:
            code=self.code(sid)
            condition=next(l.strip()[3:] for l in code.splitlines() if l.lstrip().startswith('if ') and 'ta.change(strategy.closedtrades)' in l)
            condition=condition.replace('ta.change(strategy.closedtrades)','delta')
            for delta in [0,1]:
                self.assertEqual(bool(safe_eval(condition,delta=delta,inTrade=True)),delta>0)

    def test_donchian_keeps_entry_bar_absolute_protection(self):
        code=self.code(2421)
        code='\n'.join(l for l in code.splitlines() if not l.lstrip().startswith('// OPT-'))
        for direction in ['Long','Short']:
            block=re.search(r'if canEnter'+direction+r'[^\n]*\n((?:[ \t]+[^\n]*\n?)+)',code)[1]
            self.assertIn('strategy.entry("'+direction+'"',block)
            self.assertIn('strategy.exit("'+direction+' Exit"',block)
        self.assertIn('if not window()\n    strategy.cancel("Long")',code)

    def test_window_cancel_does_not_cancel_profit_exit_or_new_close(self):
        code=self.code(4622)
        canceled=set(re.findall(r'strategy.cancel\("([^"]+)"',code))
        profit_ids=set(re.findall(r'strategy.exit\("([^"]+)"',code))
        self.assertFalse(canceled & profit_ids)
        self.assertLess(code.index('strategy.cancel("EMA1")'),code.index('strategy.close("EMA1"'))
        self.assertIn('when = strategy.opentrades > 0',code)

    def test_second_entry_cannot_receive_previous_trade_bracket(self):
        code=self.code(3756)
        code='\n'.join(l for l in code.splitlines() if not l.lstrip().startswith('// OPT-'))
        self.assertRegex(code,r'if strategy.position_size > 0\n\s+strategy.exit\("Take Profit/Stop Loss"')
        target_expr=re.search(r'longTakeProfit := (.+?)\s*//',code)[1].replace('strategy.position_avg_price','average')
        stop_expr=re.search(r'longStopLoss := (.+?)\s*//',code)[1].replace('strategy.position_avg_price','average')
        for position,average,expected in [(1,100,(110,95)),(0,None,None),(1,200,(220,190))]:
            actual=None if position==0 else (round(safe_eval(target_expr,average=average),8),round(safe_eval(stop_expr,average=average),8))
            self.assertEqual(actual,expected)

if __name__=='__main__':unittest.main()
