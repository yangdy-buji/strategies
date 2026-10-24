import unittest
from tools.strategy_ranking.verify import validate_ranked

class RankVerifyTests(unittest.TestCase):
    def row(self):
        return dict(id='a'*12,sid=1,representative_sid=1,cohort='full_daily',primary_rank=1,research_index=1,current_logic_score=40,daily_score=50,recent_score=50,risk_penalty=0,combined_score=48,reported_daily=dict(cagr=.1,sharpe=1,calmar=.5,max_dd=-.2,trades=200,exposure=.5,tickers_run=1019,errs=0),source_match=dict(lossy_match=True,version_verified=False),intraday=[])
    def test_valid(self):validate_ranked([self.row()])
    def test_wrong_score(self):
        r=self.row();r['combined_score']=99
        with self.assertRaises(ValueError):validate_ranked([r])
    def test_error_not_zero(self):
        r=self.row();r['reported_daily']['errs']=1
        with self.assertRaises(ValueError):validate_ranked([r])
    def test_supplement_cannot_have_main_rank(self):
        r=self.row();r['cohort']='screening50'
        with self.assertRaises(ValueError):validate_ranked([r])
    def test_duplicate_group(self):
        r=self.row();r2=dict(r,id='b'*12,sid=2,research_index=2,primary_rank=2)
        with self.assertRaises(ValueError):validate_ranked([r,r2])
if __name__=='__main__':unittest.main()
