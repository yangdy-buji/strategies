"""Export reviewed TOP300 candidates, without claiming native execution."""
import argparse
from collections import Counter
import csv
import difflib
import html
import io
import json
import os
from pathlib import Path
import re
import uuid
import zipfile
from .core import apply_record, load_records, read_json, resolve_base, sha

LABELS={'new_patch':'本轮新候选·未回测','carry_existing':'沿用旧候选·未回测',
        'unchanged':'保留原版·待验证','deferred_design':'保留原版·待设计'}


def script_payload(base,record):
    code=apply_record(base,record)
    versions=lambda text:re.findall(r'^\s*//@version\s*=\s*(\d+)',text,re.M)
    if versions(base)!=versions(code):raise ValueError('New patch cannot migrate baseline Pine version')
    if record['action'] in ('unchanged','deferred_design'):return code
    prefix=f"// OPT-T300 SID {record['sid']}：{LABELS[record['action']]}\n// 原文件SHA256：{record['source_sha256']}\n// 未原生Pine编译、未回测；旧排名与收益不适用于本候选。\n"
    if code.startswith('//@version='):
        line,separator,rest=code.partition('\n');return line+'\n'+prefix+rest
    return prefix+code


def json_bytes(value):
    return (json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode('utf-8')


def reviewed_remaining(record,approval):
    return list(dict.fromkeys(record['remaining']+(approval or {}).get('remaining',[])))


def archive_bytes(outputs):
    stream=io.BytesIO()
    with zipfile.ZipFile(stream,'w',compression=zipfile.ZIP_DEFLATED) as archive:
        for name,data in sorted(outputs.items()):
            if name.endswith('.html') or name.endswith('.zip'):continue
            if name.startswith('/') or '..' in Path(name).parts:raise ValueError('Unsafe archive path')
            info=zipfile.ZipInfo(name,date_time=(1980,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=0o100644<<16
            archive.writestr(info,data)
    return stream.getvalue()


CSS='body{font:16px/1.65 system-ui;max-width:1300px;margin:30px auto;padding:0 20px;background:#f7f9fc;color:#19283d}a{color:#175da5}table{border-collapse:collapse;width:100%;background:white;font-size:14px}th,td{padding:10px;border-bottom:1px solid #dde4ee;text-align:left}th{background:#e8eef8}section{background:white;padding:18px;margin:14px 0;border-radius:8px}pre{white-space:pre-wrap;overflow:auto;background:#eef2f8;padding:12px}.notice{padding:18px;background:#fff0cb}.scroll{overflow:auto}'


def page(title,body):
    return ('<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+html.escape(title)+'</title><style>'+CSS+'</style>'+body+'</html>').encode('utf-8')


def ul(items):
    return '<ul>'+''.join('<li>'+html.escape(str(x))+'</li>' for x in items)+'</ul>'


def render_card(r):
    e=html.escape
    body='<nav><a href="../index.html">全部300项实施结果</a> · <a href="../../logic_review.html#s'+str(r['sid'])+'">本轮审查</a></nav><h1>'+e(r['title'])+'</h1><p class="notice">原排名 #'+str(r['rank'])+' / SID '+str(r['sid'])+' · '+LABELS[r['action']]+'。原排名不是本候选的新排名。</p>'
    body+='<p>'+e(r['summary'])+'</p><p><a href="../'+r['script']+'" download>下载本项脚本（'+('原版' if r['action'] in ('unchanged','deferred_design') else '候选')+'）</a> · <a href="../'+r['original']+'">原版快照</a> · <a href="../'+r['baseline']+'">修改基线</a> · <a href="../'+r['changes']+'">完整处置说明</a></p>'
    if r['diff']:body+='<p><a href="../'+r['diff']+'">相对本轮基线的差异</a> · <a href="../'+r['original_diff']+'">相对原版的累计差异</a></p>'
    body+='<section><h2>已处理范围</h2>'+ul(r['resolved'] or ['本项未修改交易逻辑。'])+'<h2>剩余问题／设计取舍</h2>'+ul(r['remaining'])+'<h2>下一步验证</h2>'+ul(r['validation_plan'])+'</section>'
    if r['patches']:
        body+='<section><h2>每处修改的原因与保持项</h2>'
        for p in r['patches']:body+='<p>'+e(p['reason'])+'</p><p>保持：'+e(p['preserved'])+'</p>'+ul(p['validation_cases'])
        body+='</section>'
    if r['review']:body+='<section><h2>独立复核</h2><p>'+e(r['review']['review'])+'</p></section>'
    body+='<p>所有脚本均未原生Pine编译、未重测。Python测试仅覆盖源码约束、局部表达式与部分状态边界，不等于真实成交。此处不填写优化后收益。</p><p><a href="../../../top500/cards/'+r['id']+'.html">原规则与历史绩效卡</a> · <a href="../../../top500/optimization/cards/'+r['id']+'.html">旧候选与此前审查</a> · <a href="../validation.json">本地检查范围</a></p>'
    body+='<pre>'+e(json.dumps({k:r[k] for k in ('source_sha256','base_sha256','script_sha256','base_kind','change_type')},ensure_ascii=False,indent=2))+'</pre>'
    return page(r['title'],body)


def render_index(records,summary):
    body='<h1>TOP300 实施结果与独立候选</h1><p class="notice">'+ '；'.join(LABELS[k]+' '+str(summary['actions'].get(k,0))+'项' for k in LABELS)+'。没有新回测，不能把旧排名当成候选绩效。</p>'
    body+='<p><a href="top300_candidates.zip" download>下载300项脚本包</a> · <a href="manifest.csv" download>下载状态清单</a> · <a href="README.txt">使用说明</a> · <a href="../logic_review.html">完整源码审查</a> · <a href="validation.json">本地验证边界</a></p><p>包内包含候选和明确标记的原版，文件名区分candidate/original。待设计项未强行调整交易规则。点击名称查看处置、剩余问题及验证步骤。</p><div class="scroll"><table><thead><tr><th>原排名/SID</th><th>策略</th><th>动作</th><th>变更类型</th><th>本轮处置</th></tr></thead><tbody>'
    for r in records:body+='<tr><td>'+str(r['rank'])+' / '+str(r['sid'])+'</td><td><a href="'+r['card']+'">'+html.escape(r['title'])+'</a></td><td>'+LABELS[r['action']]+'</td><td>'+html.escape(r['change_type'])+'</td><td>'+html.escape(r['summary'])+'</td></tr>'
    return page('TOP300实施结果',body+'</tbody></table></div>')


def prepare_outputs(root,records,approvals):
    root=Path(root);out=root/'analysis/top300/optimized';outputs={};entries=[]
    selected={r['sid']:r for r in read_json(root/'analysis/top300/ranking.json')}
    exports={r['sid']:r for r in read_json(root/'analysis/top300/pinescript/manifest.json')}
    review={r['sid']:r for r in read_json(root/'analysis/top300/logic_review.json')}
    for r in records:
        source=selected[r['sid']]
        if not re.fullmatch('[0-9a-f]{12}',source['id']):raise ValueError('Unsafe strategy ID')
        stem=f"{r['rank']:03d}_SID{r['sid']}_{source['id']}"
        base=resolve_base(root,r);code=script_payload(base,r)
        original=(root/'analysis/top300/pinescript'/exports[r['sid']]['file']).read_bytes()
        changed=r['action'] in ('new_patch','carry_existing')
        entry=dict(r,id=source['id'],title=source['title'],category=source['category'],priority=review[r['sid']]['priority'],
                   remaining=reviewed_remaining(r,approvals.get(str(r['sid']))),
                   script='scripts/'+stem+('_candidate.pine' if changed else '_original.pine'),
                   original='originals/'+stem+'.pine',baseline='baselines/'+stem+'.pine',changes='changes/'+stem+'.txt',
                   card='cards/'+source['id']+'.html',diff='changes/'+stem+'.patch' if changed else None,
                   original_diff='changes/'+stem+'.original.patch' if changed else None,
                   script_sha256=sha(code),native_compile=False,backtest=False,review=approvals.get(str(r['sid'])))
        entries.append(entry)
        outputs[entry['script']]=code.encode();outputs[entry['original']]=original;outputs[entry['baseline']]=base.encode()
        outputs[entry['changes']]=json_bytes(entry)
        outputs[entry['card']]=render_card(entry)
        if changed:
            for key,old,name in [('diff',base,'baseline.pine'),('original_diff',original.decode(),'original.pine')]:
                outputs[entry[key]]=''.join(difflib.unified_diff(old.splitlines(keepends=True),code.splitlines(keepends=True),fromfile=name,tofile='candidate.pine')).encode()
    summary=dict(total=len(entries),actions=dict(Counter(r['action'] for r in entries)),
                 change_types=dict(Counter(r['change_type'] for r in entries)),native_compile=False,backtest=False,
                 input_hashes={str(p.relative_to(root)):sha(p.read_bytes()) for p in [root/'analysis/top300/ranking.json',root/'analysis/top300/logic_review.json',root/'analysis/top300/pinescript/manifest.json',root/'analysis/top500/optimization/manifest.json']+sorted((root/'analysis/top300/execution').glob('*.json'))})
    outputs['manifest.json']=json_bytes(entries);outputs['summary.json']=json_bytes(summary)
    stream=io.StringIO(newline='');fields=['rank','sid','title','priority','action','change_type','base_kind','summary','resolved','remaining','validation_plan','script','original','baseline','changes','source_sha256','script_sha256']
    writer=csv.DictWriter(stream,fieldnames=fields);writer.writeheader()
    for entry in entries:
        row={k:json.dumps(entry[k],ensure_ascii=False) if isinstance(entry[k],list) else entry[k] for k in fields}
        writer.writerow({k:"'"+v if isinstance(v,str) and v.startswith(('=','+','-','@')) else v for k,v in row.items()})
    outputs['manifest.csv']=stream.getvalue().encode('utf-8-sig')
    outputs['index.html']=render_index(entries,summary)
    outputs['README.txt']=('TOP300实施脚本包\n\n'+ '\n'.join(LABELS[k]+': '+str(summary['actions'].get(k,0)) for k in LABELS)+'\n\n候选不是上线版。所有文件未原生Pine编译、未重测，不能继承原排名收益。new_patch为本轮新修；carry_existing仅沿用既有候选；unchanged/deferred_design输出原版且文件名带original。\n\noriginals保留原版，baselines保留本轮修改起点，scripts为交付版本，changes记录逐处原因、保持行为、差异和未解决问题。局部Python测试不能证明完整Pine、指标时序与订单成交行为。\n\n部分设计建议需要独立行情、原生执行或明确经济假设，具体见每项remaining与validation_plan。验证时先逐笔对齐原/新版订单和仓位，再做同成本、同股票池的后续样本测试。ZIP不包含依赖仓库目录的HTML页面。\n').encode()
    outputs['validation.json']=json_bytes(dict(scope='source-bound patches, independent review, local Python cases and output consistency only',native_compile=False,backtest=False,live_orders=False,commands=['python3 -m unittest discover -s tests -q','python3 -m tools.strategy_top300.verify'],limitations=['Local tests are not a Pine compiler or full execution engine','No measured performance improvement','Design experiments require native replay and out-of-sample validation']))
    outputs['top300_candidates.zip']=archive_bytes(outputs)
    return outputs,summary


def check_output_paths(root,out,names):
    root=Path(root).resolve();out=Path(out)
    for name in names:
        if Path(name).is_absolute() or '..' in Path(name).parts:raise ValueError('Unsafe output path')
        path=out/name
        for candidate in (path,*path.parents):
            if candidate==root:break
            if candidate.is_symlink():raise ValueError('Output symlink refused: '+str(candidate))
            if root not in candidate.parents:raise ValueError('Output escapes repository')
        if path.exists() and not path.is_file():raise ValueError('Output must be a regular file')
        if root not in path.resolve().parents:raise ValueError('Resolved output escapes repository')


def atomic_write(root,path,data):
    """Walk anchored directories without following links; replace rather than truncate."""
    parts=path.relative_to(root).parts
    directory=os.open(root,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
    temporary=None
    try:
        for part in parts[:-1]:
            try:os.mkdir(part,dir_fd=directory)
            except FileExistsError:pass
            next_directory=os.open(part,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=directory)
            os.close(directory);directory=next_directory
        temporary='.top300-'+uuid.uuid4().hex+'.tmp'
        descriptor=os.open(temporary,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644,dir_fd=directory)
        with os.fdopen(descriptor,'wb') as stream:stream.write(data)
        os.replace(temporary,parts[-1],src_dir_fd=directory,dst_dir_fd=directory)
        temporary=None
    finally:
        if temporary is not None:
            try:os.unlink(temporary,dir_fd=directory)
            except FileNotFoundError:pass
        os.close(directory)


def build(root):
    root=Path(root).resolve();records,approvals=load_records(root)
    outputs,summary=prepare_outputs(root,records,approvals);out=root/'analysis/top300/optimized'
    check_output_paths(root,out,outputs)
    existing={str(p.relative_to(out)) for p in out.rglob('*') if p.is_file()} if out.exists() else set()
    if existing-set(outputs):raise ValueError('Unexpected existing output files; inspect before removing: '+str(sorted(existing-set(outputs))))
    for name,data in outputs.items():
        atomic_write(root,out/name,data)
    return summary


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[2]);args=parser.parse_args()
    print(json.dumps(build(args.root),ensure_ascii=False,indent=2))


if __name__=='__main__':main()
