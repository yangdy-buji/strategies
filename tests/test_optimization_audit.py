import copy
import hashlib
import unittest
from tools.strategy_optimization.audit import validate_audits, approved_registry, patch_digest


class AuditTests(unittest.TestCase):
    def sample(self):
        code='//@version=5\nx = true\nif x\n    strategy.entry("L", strategy.long)'
        source=dict(sid=1,id='a'*12,filename='a.md',source_sha256='b'*64,code=code,code_start_line=10)
        audit=dict(sid=1,id=source['id'],filename='a.md',source_sha256='b'*64,code_sha256=hashlib.sha256(code.encode()).hexdigest(),code_lines=4,review_scope='full_source_static',synopsis='恒真x触发Long订单，无退出。',evidence=[dict(line=11,code='x = true',reason='门禁恒真')],findings=[],verdict='no_confirmed_defect',patches=[])
        return source,audit

    def test_full_coverage_and_source_evidence(self):
        source,audit=self.sample();self.assertTrue(validate_audits([audit],[source]))
        with self.assertRaises(ValueError):validate_audits([], [source])
        with self.assertRaises(ValueError):validate_audits([audit,audit],[source])
        audit['evidence'][0]['code']='x = false'
        with self.assertRaises(ValueError):validate_audits([audit],[source])

    def test_drift_and_invalid_review_claim_rejected(self):
        source,audit=self.sample()
        for key,value in [('source_sha256','c'*64),('code_sha256','d'*64),('code_lines',9),('review_scope','regex_only'),('synopsis','')]:
            bad=copy.deepcopy(audit);bad[key]=value
            with self.assertRaises(ValueError):validate_audits([bad],[source])

    def test_patch_must_have_evidence_and_validation(self):
        source,audit=self.sample();audit.update(verdict='fix_proposed',patches=[dict(old='x = true',new='x = time >= start',reason='接入已有日期',preserved='其他条件',validation_cases=['开始前不可入场'])])
        self.assertTrue(validate_audits([audit],[source]))
        bad=copy.deepcopy(audit);bad['patches'][0]['old']='missing'
        with self.assertRaises(ValueError):validate_audits([bad],[source])

    def test_explicit_line_deletion_is_supported(self):
        source,audit=self.sample();audit.update(verdict='fix_proposed',patches=[dict(old='x = true',new='',reason='删除错误重置',preserved='其他状态',validation_cases=['下根保护价不为na'])])
        self.assertTrue(validate_audits([audit],[source]))
        bad=copy.deepcopy(audit);bad['patches'][0]['validation_cases']=[]
        with self.assertRaises(ValueError):validate_audits([bad],[source])

    def test_unapproved_patch_never_applied(self):
        _,audit=self.sample();audit.update(verdict='fix_proposed',patches=[dict(old='x = true',new='x = false',reason='reason',preserved='keep',validation_cases=['case'])])
        with self.assertRaises(ValueError):approved_registry([audit],{})
        approval={'1':dict(status='approved',patch_sha256=patch_digest(audit),review='独立复核通过')}
        result=approved_registry([audit],approval)
        self.assertEqual(result[1]['patches'][0][:2],('x = true','x = false'))
        audit['patches'][0]['new']='x = 1'
        with self.assertRaises(ValueError):approved_registry([audit],approval)

    def test_deferred_fix_requires_explanation(self):
        _,audit=self.sample();audit.update(verdict='fix_proposed',patches=[dict(old='x',new='y',reason='r',preserved='k',validation_cases=['case'])])
        approval={'1':dict(status='deferred',patch_sha256=patch_digest(audit),review='交易方向需要单独设计')}
        self.assertEqual(approved_registry([audit],approval),{})
        approval['1']['review']=''
        with self.assertRaises(ValueError):approved_registry([audit],approval)

    def test_extended_registry_keeps_legacy_registry_unchanged(self):
        from tools.strategy_optimization.fixes import apply_fix,FIXES
        source,audit=self.sample();audit.update(verdict='fix_proposed',patches=[dict(old='x = true',new='x = false',reason='修复条件',preserved='保持其他代码',validation_cases=['false不入场'])])
        registry=approved_registry([audit],{'1':dict(status='approved',patch_sha256=patch_digest(audit),review='已复核')})
        output=apply_fix(1,source['code'],source['source_sha256'],registry=registry)
        self.assertIn('x = false',output);self.assertIn('OPT-1-',output)
        self.assertNotIn(1,FIXES)
        with self.assertRaises(ValueError):apply_fix(1,source['code']+'x',source['source_sha256'],registry=registry)

    def test_partial_expression_note_is_before_line_not_inside_expression(self):
        from tools.strategy_optimization.fixes import apply_fix
        code='if allowed and (low - high) <= 10\n    strategy.entry("S", strategy.short)'
        registry={1:dict(source_sha256='a'*64,code_sha256=hashlib.sha256(code.encode()).hexdigest(),patches=[('(low - high)','(high - low)','修复距离符号','保持条件')])}
        result=apply_fix(1,code,'a'*64,registry=registry)
        self.assertIn('if allowed and (high - low) <= 10\n',result)
        self.assertNotIn('if allowed and //',result)
        clean='\n'.join(l for l in result.splitlines() if not l.lstrip().startswith('// OPT-'))
        self.assertEqual(clean,code.replace('(low - high)','(high - low)'))

    def test_newlines_in_notes_cannot_insert_executable_statements(self):
        from tools.strategy_optimization.fixes import apply_fix
        code='x = true';registry={1:dict(source_sha256='a'*64,code_sha256=hashlib.sha256(code.encode()).hexdigest(),patches=[('true','false','reason\nstrategy.entry("BAD",strategy.long)','keep\runsafe()')])}
        output=apply_fix(1,code,'a'*64,registry=registry)
        executable=[l for l in output.splitlines() if not l.lstrip().startswith('//')]
        self.assertEqual(executable,['x = false'])

if __name__=='__main__':unittest.main()
