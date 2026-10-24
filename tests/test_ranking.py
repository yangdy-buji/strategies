import csv
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

MODULE = Path(__file__).resolve().parents[1] / 'tools/strategy_ranking/rank.py'

class RankingTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(MODULE.exists(), 'ranking module must implement build_dataset')
        spec = importlib.util.spec_from_file_location('ranking_under_test', MODULE)
        self.mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.mod)
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.catalog = []
        self.features = []
        self.scored = []
        self.rows = []

    def csv(self, name, rows):
        if not rows: return
        p = self.root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open('w') as f:
            w = csv.DictWriter(f, fieldnames=sorted(set().union(*(r.keys() for r in rows))))
            w.writeheader(); w.writerows(rows)

    def add(self, sid, **kw):
        code = f'x = {sid}'
        self.catalog.append(dict(id=str(sid), filename=f'{sid}.md', title=str(sid), code=code, score=50))
        self.features.append(dict(sid=sid,repo_path=f'repo/{sid}.md',src_hash=hashlib.md5(code.encode()).hexdigest()))
        self.scored.append(dict(sid=sid,repo_path=f'repo/{sid}.md',representative_sid=sid))
        row=dict(sid=sid,repo_path=f'repo/{sid}.md',status='ok',stage='full_universe',tickers_run=1019,errs=0,trades=200,exposure=.5,cagr=.1,sharpe=1,calmar=.5,max_dd=-.2)
        row.update(kw);self.rows.append(row)

    def build(self):
        p=self.root/'catalog.json';p.write_text(json.dumps(self.catalog))
        f=self.root/'0_代码与中间数据/results/rationality/features.jsonl';f.parent.mkdir(parents=True,exist_ok=True)
        f.write_text('\n'.join(json.dumps(x) for x in self.features))
        self.csv('2_合理性Top500/all_scored.csv',self.scored)
        self.csv('0_代码与中间数据/results/all_results.csv',self.rows)
        return self.mod.build_dataset(self.root,p)

    def test_failure_and_timeout_excluded(self):
        self.add(1,status='error');self.add(2,status='timeout');self.add(3)
        d=self.build();self.assertEqual([r['sid'] for r in d['primary']],[3])

    def test_representative_stable_not_best_performance(self):
        self.add(1,sharpe=.2);self.add(2,sharpe=2)
        self.scored[1]['representative_sid']=1
        d=self.build();self.assertEqual([r['sid'] for r in d['primary']],[1]);self.assertEqual(d['primary'][0]['duplicate_members'],[1,2])

    def test_missing_recent_is_not_neutral_and_json_finite(self):
        self.add(1,profit_factor='Infinity')
        row=self.build()['primary'][0]
        self.assertIsNone(row['recent_score']);self.assertEqual(row['daily_score'],50)
        self.assertEqual(row['combined_score'],45);self.assertIsNone(row['reported_daily']['profit_factor'])
        json.dumps(row,allow_nan=False)

    def test_different_cohorts_do_not_mix_percentiles(self):
        self.add(1);self.add(2,stage='screen_50stocks',tickers_run=50,sharpe=2)
        d=self.build();self.assertEqual(len(d['primary']),1);self.assertEqual(len(d['supplement_pool']),1)
        self.assertEqual(d['primary'][0]['daily_score'],50)

    def test_anomaly_and_hash_mismatch_rejected(self):
        self.add(1,sharpe=3.1);self.add(2);self.add(3,errs=1)
        self.features[1]['src_hash']='incorrect'
        self.assertEqual(self.build()['primary'],[])

    def test_saved_intraday_anomaly_excluded(self):
        self.add(1)
        self.csv('5_日内回测_set552/top100_5m.csv',[dict(sid=1,sharpe=4)])
        self.assertEqual(self.build()['primary'],[])

    def test_screening_missing_ticker_count_remains_unknown(self):
        self.add(1,stage='screen_50stocks',tickers_run='')
        d=self.build()
        self.assertEqual(len(d['supplement_pool']),1)
        self.assertIsNone(d['supplement_pool'][0]['reported_daily']['tickers_run'])
        self.assertEqual(d['supplement_pool'][0]['cohort'],'screening50')
        self.assertFalse(d['supplement_pool'][0]['source_match']['version_verified'])
        self.assertEqual(d['summary']['supplement_pool_count'],1)
        self.assertTrue(d['source_manifest'][0]['path'])

    def test_supplement_cannot_duplicate_primary_group(self):
        self.add(1)
        self.add(2,stage='screen_50stocks',tickers_run=50)
        self.scored[1]['representative_sid']=1
        self.assertEqual(self.build()['supplement_pool'],[])

    def test_ineligible_representative_not_replaced_with_better_duplicate(self):
        self.add(1,sharpe=4)
        self.add(2,sharpe=1)
        self.scored[1]['representative_sid']=1
        self.assertEqual(self.build()['primary'],[])

    def test_raw_errors_disqualify_daily_rerun(self):
        self.add(1)
        self.csv('3_552策略日线重跑/all_552_daily.csv',[dict(self.rows[0],run_status='ran',source_run='daily500')])
        p=self.root/'0_代码与中间数据/results/rationality/daily/daily.jsonl'
        p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text(json.dumps(dict(sid=1,status='ok',errs=1)))
        self.assertEqual(self.build()['primary'],[])

    def test_supplement_cannot_reintroduce_rejected_full_group(self):
        self.add(1,sharpe=4)
        self.add(2,stage='screen_50stocks',tickers_run=50)
        self.scored[1]['representative_sid']=1
        self.assertEqual(self.build()['supplement_pool'],[])

    def test_review_label_is_string(self):
        self.add(1)
        self.catalog[0]['review_status']='自动初审'
        r=self.build()['primary'][0]
        self.assertEqual(r['current_logic_review'],'自动初审')
        self.assertIsInstance(r['current_logic_review_details'],dict)

    def test_stage2_reused_checks_original_raw_errors(self):
        self.add(1)
        self.csv('3_552策略日线重跑/all_552_daily.csv',[dict(self.rows[0],run_status='ran',source_run='stage2_reused')])
        p=self.root/'0_代码与中间数据/results/stage2/stage2.jsonl'
        p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text(json.dumps(dict(sid=1,status='ok',errs=1)))
        self.assertEqual(self.build()['primary'],[])

    def test_unknown_full_errors_excluded(self):
        self.add(1,errs='')
        self.assertEqual(self.build()['primary'],[])

    def test_intraday_prefers_full_scope_but_preserves_alternate_anomaly(self):
        self.add(1)
        self.csv('0_代码与中间数据/results/intraday/set552/ranked_1h.csv',[dict(sid=1,sharpe=1)])
        self.csv('5_日内回测_set552/top100_1h.csv',[dict(sid=1,sharpe=4)])
        d=self.build()
        self.assertEqual(d['primary'],[])
        row=d['excluded'][0]
        self.assertEqual(len(row['intraday']),1)
        self.assertEqual(row['intraday'][0]['scope'],'全榜')
        self.assertEqual(row['intraday'][0]['source_alternates'][0]['sharpe'],4)

    def test_failed_full_group_cannot_fall_back_to_screen_duplicate(self):
        self.add(1,status='error',cagr='')
        self.add(2,stage='screen_50stocks',tickers_run='')
        self.scored[1]['representative_sid']=1
        self.assertEqual(self.build()['supplement_pool'],[])

    def test_runtime_skips_cannot_fall_back_to_screening(self):
        ids=[3515,4443,3239,800,2923,2799]
        for sid in ids: self.add(sid,stage='screen_50stocks',tickers_run='')
        self.csv('3_552策略日线重跑/all_552_daily.csv',[
            dict(sid=sid,repo_path=f'repo/{sid}.md',run_status='skipped',skip_reason='runtime:slow(>3000s, 123 tickers done)') for sid in ids])
        self.assertEqual(self.build()['supplement_pool'],[])

    def test_compile_prescreen_skip_remains_visible(self):
        self.add(1,stage='screen_50stocks',tickers_run='')
        self.csv('3_552策略日线重跑/all_552_daily.csv',[
            dict(sid=1,repo_path='repo/1.md',run_status='skipped',skip_reason='compile:unsupported syntax')])
        d=self.build()
        self.assertEqual(len(d['supplement_pool']),1)
        self.assertIn('compile:unsupported syntax',' '.join(d['supplement_pool'][0]['eligibility_notes']))

    def test_negative_errors_not_accepted(self):
        self.add(1,errs=-1)
        self.assertEqual(self.build()['primary'],[])

    def test_ties_average(self):
        self.assertEqual(self.mod.percentiles([1,1,3]),[.25,.25,1])

if __name__ == '__main__': unittest.main()
