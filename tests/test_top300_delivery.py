import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile
from tests.test_top300_core import fixture
from tools.strategy_top300.build import script_payload, archive_bytes, reviewed_remaining
from tools.strategy_top300.build import build
from tools.strategy_top300.verify import compare_outputs


class Top300DeliveryTests(unittest.TestCase):
    def test_independent_review_risks_are_preserved_without_mutating_proposal(self):
        r=fixture();extra={'remaining':['复核补充风险','未原生编译']}
        self.assertEqual(reviewed_remaining(r,extra),['未原生编译','复核补充风险'])
        self.assertEqual(r['remaining'],['未原生编译'])

    def test_retained_original_is_not_relabelled_as_optimized(self):
        r=fixture();r.update(action='unchanged',change_type='none',patches=[])
        self.assertEqual(script_payload('value = close\n',r),'value = close\n')

    def test_candidate_keeps_first_version_directive_and_disclaims_returns(self):
        code='//@version=5\nvalue = close\n';r=fixture(code)
        output=script_payload(code,r)
        self.assertTrue(output.startswith('//@version=5\n'))
        for text in ('未原生Pine编译','未回测','2351',r['source_sha256'],'OPT-T300'):
            self.assertIn(text,output)

    def test_new_patch_cannot_silently_migrate_pine_version(self):
        code='//@version=5\nvalue = close\n';r=fixture(code)
        r['patches'][0].update(old='//@version=5',new='//@version=6')
        with self.assertRaises(ValueError):script_payload(code,r)

    def test_archive_is_deterministic_and_does_not_require_external_html(self):
        outputs={'scripts/a.pine':b'abc','manifest.json':b'[]','index.html':b'<html>'}
        first=archive_bytes(outputs)
        self.assertEqual(first,archive_bytes(outputs))
        with zipfile.ZipFile(io.BytesIO(first)) as z:
            self.assertEqual(z.read('scripts/a.pine'),b'abc')
            self.assertNotIn('index.html',z.namelist())
            self.assertIsNone(z.testzip())

    def test_verification_rejects_changed_or_extra_script(self):
        with tempfile.TemporaryDirectory() as directory:
            p=Path(directory);(p/'a.pine').write_bytes(b'abc')
            compare_outputs(p,{'a.pine':b'abc'})
            (p/'a.pine').write_bytes(b'wrong')
            with self.assertRaises(ValueError):compare_outputs(p,{'a.pine':b'abc'})
            (p/'a.pine').write_bytes(b'abc');(p/'extra.pine').touch()
            with self.assertRaises(ValueError):compare_outputs(p,{'a.pine':b'abc'})

    def test_build_refuses_symlink_before_any_output_is_written(self):
        for ancestor in (False,True):
            with self.subTest(ancestor=ancestor),tempfile.TemporaryDirectory() as directory:
                root=Path(directory);source=root/'original.md';source.write_bytes(b'ORIGINAL')
                out=root/'analysis/top300/optimized'
                if ancestor:
                    target=root/'other';target.mkdir();(root/'analysis').mkdir()
                    (root/'analysis/top300').symlink_to(target,target_is_directory=True)
                else:
                    out.mkdir(parents=True);(out/'manifest.json').symlink_to(source)
                with patch('tools.strategy_top300.build.load_records',return_value=([],{})),patch('tools.strategy_top300.build.prepare_outputs',return_value=({'new.txt':b'new','manifest.json':b'changed'},{})):
                    with self.assertRaises(ValueError):build(root)
                self.assertEqual(source.read_bytes(),b'ORIGINAL')
                self.assertFalse((out/'new.txt').exists())


if __name__=='__main__':unittest.main()
