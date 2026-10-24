import json
import unittest
from tools.strategy_optimization import build


class OptimizationBuildTests(unittest.TestCase):
    def record(self):
        return dict(id='abcdef123456',sid=1,research_index=1,title='危险</script><script>x</script>',filename='source.md',source_sha256='a'*64,original_code_sha256='b'*64,status='needs_review',severity='未定',issues=['尚需源码审查'],remaining=[],verification=dict(native_compile=False,backtest=False),card='cards/abcdef123456.html',variant=None,diff=None,changes=None,category='待分类')

    def test_header_preserves_one_version_and_does_not_inherit_returns(self):
        code='/*backtest\nstart: 2020\n*/\n//@version=4\nstrategy("x")\n'
        text=build.annotated_code(code,self.record())
        self.assertTrue(text.startswith('//@version=4\n'))
        self.assertEqual(text.count('//@version='),1)
        self.assertIn('未回测',text)
        self.assertIn('a'*64,text)
        self.assertIn('strategy("x")',text)
        self.assertNotIn('年化收益50',text)

    def test_multiple_version_directives_rejected(self):
        with self.assertRaises(ValueError):build.annotated_code('//@version=4\n//@version=5',self.record())

    def test_index_embedded_data_cannot_close_script(self):
        text=build.render_index([self.record()])
        self.assertNotIn('危险</script><script>x</script>',text)
        self.assertIn('\\u003c',text)
        self.assertIn('textContent',text)

    def test_unmodified_card_has_no_candidate_download(self):
        text=build.render_card(self.record())
        self.assertNotIn('conservative.pine',text)
        self.assertIn('尚未修改',text)
        self.assertIn('危险&lt;/script&gt;',text)

    def test_candidate_card_has_changes_and_remaining(self):
        r=self.record();r.update(status='candidate',variant='variants/abcdef123456/conservative.pine',changes='variants/abcdef123456/changes.md',diff='variants/abcdef123456/changes.patch',original_variant='variants/abcdef123456/original.pine',remaining=['仍无硬止损'])
        text=build.render_card(r)
        self.assertIn('../variants/abcdef123456/conservative.pine',text)
        self.assertIn('仍无硬止损',text)
        self.assertIn('未回测',text)

    def test_old_findings_are_separate_from_remaining_defects(self):
        r=self.record();r['original_findings']=['原版ID错误，本轮已修']
        text=build.render_card(r)
        self.assertIn('原版审查上下文',text)
        self.assertIn('不表示这些问题在修复版中全部仍然存在',text)
        self.assertIn('原版ID错误，本轮已修',text)

    def test_completed_audit_is_distinct_from_pending_review(self):
        r=self.record();r.update(status='reviewed',audit=dict(synopsis='以EMA交叉入场，反向交叉退出',evidence=[dict(line=120,code='long = crossover(a, b)',reason='交叉信号')],findings=[],verdict='no_confirmed_defect'))
        text=build.render_card(r)
        self.assertIn('已审·未确认缺陷',text)
        self.assertIn('以EMA交叉入场',text)
        self.assertIn('120',text)
        self.assertIn('不代表已证明没有缺陷',text)

    def test_audit_status_uses_approved_patch_not_proposal(self):
        self.assertEqual(build.audit_status(dict(verdict='fix_proposed'),False),'needs_design')
        self.assertEqual(build.audit_status(dict(verdict='fix_proposed'),True),'candidate')
        self.assertEqual(build.audit_status(dict(verdict='no_confirmed_defect'),False),'reviewed')

    def test_deferred_review_reason_remaining_and_cases_are_visible(self):
        r=self.record();approval=dict(status='deferred',review='需要确认锚价',remaining=['首次保护尚无定义'],validation_cases=['跳空后检查保护'])
        build.apply_review_metadata(r,approval)
        text=build.render_card(r)
        self.assertIn('暂缓修改',text);self.assertIn('需要确认锚价',text)
        self.assertIn('首次保护尚无定义',text);self.assertIn('跳空后检查保护',text)

if __name__=='__main__':unittest.main()
