import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from tools.strategy_catalog.verify import verify_inventory

class VerifyTest(unittest.TestCase):
    def fixture(self,root):
        (root/'sample.md').write_text('hello')
        out=root/'analysis';(out/'cards').mkdir(parents=True)
        record=dict(id='a'*12,filename='sample.md',source_sha256=hashlib.sha256(b'hello').hexdigest(),score=None,scores=[],performance_score=None,performance_status='未验证',code='',code_start_line=0)
        (out/'catalog.json').write_text(json.dumps([record]))
        return out,record
    def test_missing_cards_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);out,r=self.fixture(root)
            with self.assertRaises(ValueError):verify_inventory(root,out)
    def test_missing_catalog_entry_files_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);out,r=self.fixture(root)
            content='入场 出场 策略原理 完整源码 未验证 '+r['source_sha256']
            for ext in ('md','html'):
                (out/'cards'/(r['id']+'.'+ext)).write_text(content)
            with self.assertRaises(ValueError):verify_inventory(root,out)
    def test_changed_source_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);out,r=self.fixture(root)
            (root/'sample.md').write_text('changed')
            with self.assertRaises(ValueError):verify_inventory(root,out)
if __name__=='__main__': unittest.main()
