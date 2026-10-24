import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from tools.strategy_catalog.build import apply_reviews, render_card, render_card_html, render_index, validate_records


def record():
    return dict(id='a'*12, filename='示例 策略.md', title='<script>alert(1)</script>', source_sha256='b'*64,
        language='PineScript', kind='strategy', category='趋势跟随', family='均线', tags=['仅多'], market='待确认',
        period='1d', description='作者原理描述',code='if buy\n    strategy.entry("L", strategy.long)', code_start_line=20,
        parameters=['length = input(20)'], entry_rules=[{'line':20,'code':'if buy\n    strategy.entry("L", strategy.long)','explanation':'条件需复核'}],
        exit_rules=[], position_rules=[], risks=[], strengths=['规则明确'], weaknesses=['未验证'],
        scores=[{'dimension':'获利机制','score':10,'max':20,'reason':'假设待验证'}], score=10,
        classification_confidence='低', review_status='自动初审',evidence_level='E0',performance_score=None,
        performance_status='未验证',source_url='https://example.com')

class CatalogTest(unittest.TestCase):
    def test_missing_review_leaves_auto_and_performance_unknown(self):
        r=record(); result=apply_reviews([r],[])
        self.assertEqual(result[0]['review_status'],'自动初审')
        self.assertIsNone(result[0]['performance_score'])

    def test_review_must_match_source_hash(self):
        r=record()
        with self.assertRaises(ValueError):
            apply_reviews([r],[dict(filename=r['filename'],source_sha256='changed')])

    def test_duplicate_or_unknown_review_rejected(self):
        r=record(); rev=dict(filename=r['filename'],source_sha256=r['source_sha256'])
        with self.assertRaises(ValueError): apply_reviews([r],[rev,rev])
        with self.assertRaises(ValueError): apply_reviews([r],[dict(filename='no.md',source_sha256='x')])

    def test_review_cannot_inject_performance_or_paths(self):
        r=record(); rev=dict(filename=r['filename'],source_sha256=r['source_sha256'],id='../bad',performance_score=99)
        with self.assertRaises(ValueError): apply_reviews([r],[rev])

    def test_card_preserves_entry_source_and_missing_exit_uncertainty(self):
        out=render_card(record())
        self.assertIn('入场',out); self.assertIn('出场',out)
        self.assertIn('strategy.entry',out); self.assertIn('20',out)
        self.assertIn('未验证',out); self.assertIn('未识别',out)
        self.assertIn('完整源码',out)

    def test_reviewed_rules_display_instead_of_only_author_copy(self):
        r=record();r.update(principle='均线确认趋势',entry_explanation=['收盘上穿后提交买单'],exit_explanation=['下穿后反转'],review_status='源码复核')
        out=render_card(r)
        self.assertIn('收盘上穿后提交买单',out);self.assertIn('下穿后反转',out)

    def test_scored_auxiliary_record_is_rejected(self):
        r=record();r['kind']='tool'
        with self.assertRaisesRegex(ValueError,'非策略'):
            validate_records([r])

    def test_duplicate_dimensions_and_score_above_100_rejected(self):
        r=record()
        r['scores']=[dict(dimension=d,score=m,max=m,reason='test') for d,m in [('获利机制',20),('信号因果性',25),('规则完整性',20),('风险与仓位',20),('美股执行',15)]]
        r['scores'].append(dict(r['scores'][0]));r['score']=120
        with self.assertRaises(ValueError): validate_records([r])

    def test_html_escape_untrusted_content(self):
        out=render_card_html(record())
        self.assertNotIn('<script>alert(1)</script>',out)
        self.assertIn('&lt;script&gt;',out)
        index=render_index([record()])
        self.assertNotIn('<script>alert(1)</script>',index)
        self.assertIn('\\u003cscript',index)
        self.assertIn('textContent',index)

if __name__=='__main__': unittest.main()
