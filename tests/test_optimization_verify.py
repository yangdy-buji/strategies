import copy
import csv
import unittest
import tempfile
from pathlib import Path
import difflib
import json

from tools.strategy_optimization.verify import validate_manifest, validate_patch, validate_variant, validate_views, validate_documents, validate_audit_metadata, CSV_FIELDS, _links


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

    def test_additional_candidates_require_explicit_registry(self):
        r=self.row();r['sid']=1
        self.assertTrue(validate_manifest([r],[r],expected_count=1,candidate_sids={1}))
        with self.assertRaises(ValueError):validate_manifest([r],[r],expected_count=1,candidate_sids=set())

    def test_reviewed_requires_completed_no_defect_audit(self):
        r=self.row();r['sid']=9000;r['status']='reviewed'
        for field in ('variant','variant_sha256','original_variant','diff','changes'):r[field]=None
        with self.assertRaises(ValueError):self.check(r,r)
        r['audit']=dict(review_scope='full_source_static',verdict='no_confirmed_defect')
        self.assertTrue(self.check(r,r))

class ArtifactTests(unittest.TestCase):
    def view_fixture(self):
        from tools.strategy_optimization.build import render_index
        from tools.strategy_ranking.build import write_csv
        rows=[OptimizationVerifyTests().row()]
        rows[0].update(title='=中文标题,带逗号',category='趋势',audit_synopsis='完整审查',audit_verdict='fix_proposed',audit_findings=[{'detail':'未解决问题'}],patch_review={'status':'approved','review':'通过'})
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'manifest.csv'
            write_csv(path,rows,CSV_FIELDS)
            with path.open(encoding='utf-8-sig',newline='') as stream:csv_rows=list(csv.DictReader(stream))
        return rows,csv_rows,render_index(rows)

    def test_index_and_csv_cover_manifest_in_order(self):
        rows,csv_rows,html=self.view_fixture()
        self.assertTrue(validate_views(rows,csv_rows,html))
        self.assertEqual(csv_rows[0]['title'],"'=中文标题,带逗号")
        self.assertEqual(csv_rows[0]['audit_findings'],json.dumps(rows[0]['audit_findings'],ensure_ascii=False))
        with self.assertRaises(ValueError):validate_views(rows,[],html)
        with self.assertRaises(ValueError):validate_views(rows,csv_rows,html.replace('cards/','wrong/'))

    def test_csv_all_exported_fields_and_missing_columns_rejected(self):
        rows,csv_rows,html=self.view_fixture()
        for field in CSV_FIELDS:
            with self.subTest(field=field):
                changed=copy.deepcopy(csv_rows);changed[0][field]+='tampered'
                with self.assertRaises(ValueError):validate_views(rows,changed,html)
                missing=copy.deepcopy(csv_rows);del missing[0][field]
                with self.assertRaises(ValueError):validate_views(rows,missing,html)

    def test_index_non_identity_metadata_drift_rejected(self):
        from tools.strategy_optimization.build import render_index
        rows,csv_rows,_=self.view_fixture()
        for field in ('title','category','research_index','severity'):
            changed=copy.deepcopy(rows);changed[0][field]='stale'
            with self.assertRaises(ValueError):validate_views(rows,csv_rows,render_index(changed))

    def test_card_and_changes_reject_stale_review_and_remaining(self):
        from tools.strategy_optimization.build import render_card,changes_md
        row=OptimizationVerifyTests().row()
        row.update(validation_cases=['本地用例'],remaining=['仍有未解决缺陷'],patch_review={'status':'approved','review':'复核结论'})
        card=render_card(row);changes=changes_md(row)
        self.assertTrue(validate_documents(row,card,changes))
        for stale in (card.replace('仍有未解决缺陷','全部解决'),card.replace('复核结论','过期结论')):
            with self.assertRaises(ValueError):validate_documents(row,stale,changes)
        with self.assertRaises(ValueError):validate_documents(row,card,changes.replace('仍有未解决缺陷','全部解决'))
        with self.assertRaises(ValueError):validate_documents(row,card,None)
        row.update(status='needs_design',patch_review={'status':'deferred','review':'需要设计确认'})
        card=render_card(row)
        self.assertTrue(validate_documents(row,card))
        with self.assertRaises(ValueError):validate_documents(row,card.replace('需要设计确认','已批准'))

    def test_audit_export_metadata_matches_authoritative_record(self):
        audit=dict(synopsis='全文静态审查',verdict='needs_design',findings=[{'detail':'待解决缺陷'}])
        row={'audit_'+key:copy.deepcopy(value) for key,value in audit.items()}
        self.assertTrue(validate_audit_metadata(row,audit))
        for field in audit:
            with self.subTest(field=field):
                changed=copy.deepcopy(row);changed['audit_'+field]='过期内容'
                with self.assertRaises(ValueError):validate_audit_metadata(changed,audit)
                missing=copy.deepcopy(row);del missing['audit_'+field]
                with self.assertRaises(ValueError):validate_audit_metadata(missing,audit)

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
