import copy
import hashlib
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from tools.strategy_top300.core import (
    apply_record, proposal_digest, resolve_base, validate_approvals,
    validate_record_shape,
    load_records, read_json,
)

ROOT=Path(__file__).resolve().parents[1]


def fixture(code='value = close\n'):
    return dict(rank=1,sid=2351,source_sha256='a'*64,base_kind='original',
                base_sha256=hashlib.sha256(code.encode()).hexdigest(),action='new_patch',
                change_type='correctness',summary='修复明确问题',
                patches=[dict(old='close',new='open',reason='使用正确输入',preserved='其他条件不变',validation_cases=['开收盘不同'])],
                resolved=['输入问题'],remaining=['未原生编译'],validation_plan=['原生回放'])


class Top300CoreTests(unittest.TestCase):
    def test_inline_replacement_comments_do_not_split_expression(self):
        r=fixture();candidate=apply_record('value = close\n',r)
        active='\n'.join(x for x in candidate.splitlines() if not x.lstrip().startswith('//'))
        self.assertEqual(active,'value = open')
        self.assertIn('OPT-T300',candidate)

    def test_comment_newlines_cannot_inject_executable_lines(self):
        r=fixture();r['patches'][0]['reason']='原因\nstrategy.entry("bad", strategy.long)'
        code=apply_record('value = close\n',r)
        active=[x for x in code.splitlines() if not x.lstrip().startswith('//')]
        self.assertEqual(active,['value = open'])

    def test_duplicate_patch_match_refused(self):
        r=fixture('value = close + close\n')
        with self.assertRaises(ValueError):apply_record('value = close + close\n',r)

    def test_changed_base_refused(self):
        with self.assertRaises(ValueError):apply_record('value = low\n',fixture())

    def test_unchanged_cannot_hide_patches(self):
        r=fixture();r['action']='unchanged'
        with self.assertRaises(ValueError):validate_record_shape(r)

    def test_unchanged_cannot_use_prior_candidate(self):
        r=fixture();r.update(action='unchanged',change_type='none',patches=[],base_kind='prior_candidate')
        with self.assertRaises(ValueError):validate_record_shape(r)

    def test_approval_required_for_every_new_patch(self):
        with self.assertRaises(ValueError):validate_approvals([fixture()],{})

    def test_approval_binds_entire_record(self):
        r=fixture();a={'2351':dict(status='approved',record_sha256=proposal_digest(r),review='独立检查通过')}
        validate_approvals([r],a)
        r['remaining'].append('新增未审风险')
        with self.assertRaises(ValueError):validate_approvals([r],a)

    def test_deferred_is_not_approval(self):
        r=fixture();a={'2351':dict(status='deferred',record_sha256=proposal_digest(r),review='需设计')}
        with self.assertRaises(ValueError):validate_approvals([r],a)

    def test_original_base_is_exact_source_and_bound(self):
        metadata=json.loads((ROOT/'analysis/top300/pinescript/manifest.json').read_text())[0]
        r=fixture();r.update(source_sha256=metadata['source_sha256'],base_sha256=metadata['pine_sha256'])
        self.assertEqual(resolve_base(ROOT,r),(ROOT/'analysis/top300/pinescript'/metadata['file']).read_text())
        r['source_sha256']='0'*64
        with self.assertRaises(ValueError):resolve_base(ROOT,r)

    def test_removing_code_is_supported_but_noop_rejected(self):
        r=fixture();r['patches'][0]['new']=''
        self.assertIn('value = ',apply_record('value = close\n',r))
        r['patches'][0]['new']='close'
        with self.assertRaises(ValueError):apply_record('value = close\n',r)

    def test_ranking_cannot_silently_truncate_record_validation(self):
        ranking=read_json(ROOT/'analysis/top300/ranking.json')
        for invalid in (ranking[:-1],ranking+[ranking[-1]]):
            def altered(path):
                return invalid if Path(path)==ROOT/'analysis/top300/ranking.json' else read_json(path)
            with self.subTest(length=len(invalid)),patch('tools.strategy_top300.core.read_json',side_effect=altered):
                with self.assertRaises(ValueError):load_records(ROOT,require_approvals=False)

    def test_patch_reasons_must_include_chinese_explanation(self):
        r=fixture();r['patches'][0]['reason']='fix input'
        with self.assertRaises(ValueError):validate_record_shape(r)

    def test_generated_notes_do_not_participate_in_later_matches(self):
        r=fixture();r['patches'][0]['reason']='替换为open输入'
        r['patches'].append(dict(old='open',new='high',reason='使用最高价',preserved='范围不变',validation_cases=['顺序匹配']))
        result=apply_record('value = close\n',r)
        active=[x for x in result.splitlines() if not x.lstrip().startswith('//')]
        self.assertEqual(active,['value = high'])
        self.assertIn('OPT-T300-01',result);self.assertIn('OPT-T300-02',result)

    def test_later_patch_cannot_target_only_generated_note(self):
        r=fixture();r['patches'][0]['reason']='新增phantom说明'
        r['patches'].append(dict(old='phantom',new='oops',reason='错误目标',preserved='其他',validation_cases=['应拒绝']))
        with self.assertRaises(ValueError):apply_record('value = close\n',r)

    def test_source_export_cannot_escape_repository(self):
        path=ROOT/'analysis/top300/pinescript/manifest.json';meta=read_json(path)
        r=fixture();r.update(source_sha256=meta[0]['source_sha256'],base_sha256=meta[0]['pine_sha256'])
        altered=copy.deepcopy(meta);altered[0]['source_file']='../outside.md'
        with patch('tools.strategy_top300.core.read_json',side_effect=lambda p:altered if Path(p)==path else read_json(p)):
            with self.assertRaises(ValueError):resolve_base(ROOT,r)


if __name__=='__main__':unittest.main()
