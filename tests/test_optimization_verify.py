import copy
import unittest
import tempfile
from pathlib import Path
import difflib
import json

from tools.strategy_optimization.verify import validate_manifest, validate_patch, validate_variant, validate_views, _links


class OptimizationVerifyTests(unittest.TestCase):
    def row(self):
        return dict(id='a'*12, sid=735, research_index=1, filename='a.md', title='A',
                    source_sha256='a'*64, original_code_sha256='b'*64,
                    status='candidate', severity='high', issues=['issue'], remaining=['native'],
                    verification=dict(native_compile=False, backtest=False, local_checks='static only'),
                    card='cards/'+'a'*12+'.html', variant='variants/'+'a'*12+'/conservative.pine',
                    variant_sha256='c'*64, original_variant='variants/'+'a'*12+'/original.pine',
                    diff='variants/'+'a'*12+'/changes.patch', changes='variants/'+'a'*12+'/changes.md')

    def check(self, row, ranking=None):
        return validate_manifest([row], [ranking or self.row()], expected_count=1)

    def test_valid_manifest(self):
        self.assertTrue(self.check(self.row()))

    def test_unverified_claims_rejected(self):
        for field in ('native_compile', 'backtest'):
            with self.subTest(field=field):
                r=self.row(); r['verification'][field]=True
                with self.assertRaises(ValueError): self.check(r)

    def test_ranking_identity_and_order_locked(self):
        for field, value in [('id','z'*12),('sid',5369),('research_index',2),('filename','other.md'),('source_sha256','d'*64)]:
            with self.subTest(field=field):
                r=self.row(); baseline=copy.deepcopy(r); r[field]=value
                with self.assertRaises(ValueError): self.check(r,baseline)

    def test_unknown_candidate_rejected(self):
        r=self.row();r['sid']=99999
        with self.assertRaises(ValueError): self.check(r)

    def test_missing_or_unsafe_candidate_paths_rejected(self):
        for field,value in [('variant',None),('variant','../../outside.pine'),('diff',None),('changes',None),('original_variant',None),('variant_sha256','bad')]:
            with self.subTest(field=field):
                r=self.row();r[field]=value
                with self.assertRaises(ValueError):self.check(r)

    def test_non_candidate_cannot_have_artifact(self):
        r=self.row();r['status']='needs_design';r['sid']=9000
        with self.assertRaises(ValueError):self.check(r)

    def test_performance_claim_fields_rejected_recursively(self):
        for field in ('optimized_return','optimized_sharpe','backtest_results'):
            r=self.row();r['extra']={field:1.2}
            with self.assertRaises(ValueError):self.check(r)

    def test_missing_records_and_duplicates_rejected(self):
        with self.assertRaises(ValueError):validate_manifest([],[],expected_count=1)
        r=self.row()
        with self.assertRaises(ValueError):validate_manifest([r,r],[r,r],expected_count=2)

    def test_non_candidate_valid_without_variant(self):
        r=self.row();r['sid']=9000;r['status']='needs_review'
        for field in ('variant','variant_sha256','original_variant','diff','changes'):r[field]=None
        self.assertTrue(self.check(r,r))

class ArtifactTests(unittest.TestCase):
    def test_index_and_csv_cover_manifest_in_order(self):
        rows=[dict(id='first',sid=1,card='cards/first.html',status='needs_review'),dict(id='second',sid=2,card='cards/second.html',status='needs_design')]
        html='<script id="optimization-data" type="application/json">'+json.dumps(rows)+'</script>'
        self.assertTrue(validate_views(rows,rows,html))
        with self.assertRaises(ValueError):validate_views(rows,list(reversed(rows)),html)
        with self.assertRaises(ValueError):validate_views(rows,rows,html.replace('cards/first.html','wrong.html'))

    def test_patch_matches_original_and_candidate(self):
        original='//@version=5\nstrategy("a")\n'
        candidate=original+'// OPT fix\n'
        patch=''.join(difflib.unified_diff(original.splitlines(keepends=True), candidate.splitlines(keepends=True), fromfile='original.pine', tofile='conservative.pine'))
        self.assertTrue(validate_patch(original, candidate, patch))
        with self.assertRaises(ValueError):validate_patch(original, candidate+'// tampered\n', patch)
        with self.assertRaises(ValueError):validate_patch(original+'// tampered\n', candidate, patch)

    def test_variant_reproduces_approved_fix_exactly(self):
        from tools.strategy_catalog.analyzer import _source
        from tools.strategy_optimization.fixes import apply_fix
        from tools.strategy_optimization.build import annotated_code
        root=Path(__file__).resolve().parents[1]
        row=next(r for r in json.loads((root/'analysis/top500/ranking.json').read_text()) if r['sid']==735)
        code,_,_=_source((root/row['filename']).read_text())
        candidate=annotated_code(apply_fix(row['sid'],code,row['source_sha256']),row)
        self.assertTrue(validate_variant(code,candidate,row))
        with self.assertRaises(ValueError):validate_variant(code,candidate+'// unrelated mutation\n',row)

    def test_local_links_decode_chinese_and_reject_missing_or_escape(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);card=root/'card.html';source=root/'原文件.md';source.write_text('source')
            card.write_text('<a href="%E5%8E%9F%E6%96%87%E4%BB%B6.md">source</a>')
            self.assertEqual(_links(card,root),{source.resolve()})
            for link in ('missing.pine','../outside.pine'):
                card.write_text('<a href="'+link+'">bad</a>')
                with self.assertRaises(ValueError):_links(card,root)

if __name__=='__main__':unittest.main()
