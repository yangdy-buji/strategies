import unittest
from tools.strategy_ranking.build import fmt, format_metrics, ranked_card_html, ranking_index

class RankingRenderTests(unittest.TestCase):
    def test_missing_is_not_zero(self):
        self.assertEqual(fmt(None),'未提供')
        self.assertEqual(fmt(0),'0.00')
        self.assertEqual(fmt(.12,True),'12.00%')
    def test_nonfinite_is_not_rendered_as_fact(self):
        self.assertEqual(fmt(float('nan')),'未提供')
    def test_metric_table_labels_reported_not_verified(self):
        t=format_metrics({'cagr':.1,'max_dd':-.25})
        self.assertIn('10.00%',t);self.assertIn('-25.00%',t);self.assertIn('未提供',t)
    def test_empty_ranking_is_safe(self):
        out=ranking_index([],{'primary_count':0,'supplement_count':0})
        self.assertIn('application/json',out)
        self.assertIn('textContent',out)
        self.assertIn('非严格样本外',out)
if __name__=='__main__':unittest.main()
