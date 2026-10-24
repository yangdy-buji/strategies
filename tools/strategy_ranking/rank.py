"""Rank supplied historical evidence; never execute supplied backtest programs."""
import csv
import hashlib
import io
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path

RESULTS = '0_代码与中间数据/results/'
METRICS = ('cagr','total_return','sharpe','sortino','max_dd','calmar','win_rate','profit_factor','trades','exposure','avg_hold_days','short_trade_frac','final_equity','tickers_run','errs')
WEIGHTS = {'sharpe':.30, 'calmar':.25, 'cagr':.25, 'max_dd':.20}


def number(value):
    try:
        result = float(value)
        return result if math.isfinite(result) else None
    except (TypeError, ValueError):
        return None


def sid_of(row):
    value = str(row.get('sid', ''))
    if not re.fullmatch(r'\d+', value):
        raise ValueError('Invalid sid: ' + value)
    return int(value)


def norm_source(code):
    code = re.sub(r'/\*backtest.*?\*/', ' ', code, flags=re.S)
    code = re.sub(r'/\*.*?\*/', ' ', code, flags=re.S)
    code = '\n'.join(re.sub(r'//.*$', '', line) for line in code.split('\n'))
    code = re.sub(r'"[^"\n]*"|\'[^\'\n]*\'', 'S', code)
    return re.sub(r'\s+', ' ', code).strip().lower()


def percentiles(values):
    """Average tied rank, scaled from zero to one; singleton is 0.5."""
    if len(values) == 1:
        return [.5]
    order = sorted(values)
    positions = defaultdict(list)
    for i, value in enumerate(order):
        positions[value].append(i)
    return [sum(positions[v]) / len(positions[v]) / (len(values)-1) for v in values]


def clean(value):
    if isinstance(value, dict): return {k:clean(v) for k,v in value.items()}
    if isinstance(value, list): return [clean(v) for v in value]
    if isinstance(value, float) and not math.isfinite(value): return None
    return value


def build_dataset(source_root: Path, catalog_path: Path) -> dict:
    source_root, catalog_path = Path(source_root), Path(catalog_path)
    manifest = []

    def read(path, required=False):
        path = Path(path)
        if not path.exists():
            if required: raise FileNotFoundError(path)
            return []
        data = path.read_bytes()
        try: name = str(path.relative_to(source_root))
        except ValueError: name = str(path)
        sha = hashlib.sha256(data).hexdigest()
        manifest.append(dict(path=name,source_file=name,sha256=sha,bytes=len(data)))
        text = data.decode('utf-8-sig')
        if path.suffix == '.csv': rows = list(csv.DictReader(io.StringIO(text))); offset=2
        elif path.suffix == '.jsonl': rows=[json.loads(x) for x in text.splitlines() if x.strip()];offset=1
        else: return json.loads(text)
        for n,row in enumerate(rows,offset):
            row['_source'] = dict(source_file=name,source_row=n,sha256=sha)
        return rows

    def indexed(rows):
        result={}
        for row in rows:
            sid=sid_of(row)
            if sid in result: raise ValueError('Duplicate sid in input: '+str(sid))
            result[sid]=row
        return result

    catalog=read(catalog_path,True)
    by_name={c['filename']:c for c in catalog}
    if len(by_name)!=len(catalog): raise ValueError('Duplicate catalog filenames')
    features=indexed(read(source_root/(RESULTS+'rationality/features.jsonl'),True))
    scored=indexed(read(source_root/'2_合理性Top500/all_scored.csv',True))
    all_results=indexed(read(source_root/(RESULTS+'all_results.csv'),True))
    daily=indexed(read(source_root/'3_552策略日线重跑/all_552_daily.csv'))
    prior=indexed(read(source_root/'4_综合排名/final_ranking.csv'))
    raws={}
    for kind,path in [('stage1','stage1/stage1.jsonl'),('stage2','stage2/stage2.jsonl'),('daily500','rationality/daily/daily.jsonl')]:
        raws[kind]=indexed(read(source_root/(RESULTS+path)))
    intraday=defaultdict(list)
    sources=[(RESULTS+'intraday/set552/ranked_1h.csv','1h','全榜')]
    sources += [(f'5_日内回测_set552/top100_{tf}.csv',tf,'Top100截断') for tf in ['5m','10m','15m','30m','1h']]
    for path,tf,scope in sources:
        for row in read(source_root/path):
            intraday[sid_of(row)].append(dict(tf=tf,scope=scope,**row['_source'],**{m:number(row.get(m)) for m in METRICS},last1y_sharpe=number(row.get('last1y_sharpe')),start=row.get('start'),end=row.get('end'),flags=row.get('flags','')))
    # Full 1h evidence takes precedence over its rounded, truncated Top100 copy.
    # Keep alternates for audit and anomaly screening without double display.
    for sid,records in intraday.items():
        by_tf={}
        for record in records:
            if record['tf'] not in by_tf:
                record['source_alternates']=[]
                by_tf[record['tf']]=record
            else:
                by_tf[record['tf']]['source_alternates'].append(record)
        intraday[sid]=list(by_tf.values())
    summary_source=read(source_root/(RESULTS+'summary.json'))
    benchmark=summary_source.get('bench') if isinstance(summary_source,dict) else None
    candidates=[];excluded=[];funnel=Counter()
    group_members=defaultdict(list)
    for sid,s in scored.items():
        rep=s.get('representative_sid')
        if rep in (None,''): rep=sid
        rep=sid_of({'sid':rep})
        group_members[rep].append(sid)
    # Track attempts independently of metric availability/success. A timed-out
    # full run must never acquire a second chance via its small-pool result.
    attempted_full_groups=set()
    for sid in set(all_results)|set(daily)|set(raws['stage2']):
        a=all_results.get(sid,{})
        d=daily.get(sid,{})
        skip=str(d.get('skip_reason','')).lower()
        attempted=(a.get('stage')=='full_universe' or sid in raws['stage2']
                   or d.get('run_status')=='ran'
                   or any(token in skip for token in ('runtime:', 'timeout', 'slow(')))
        if attempted:
            attempted_full_groups.add(sid_of({'sid':scored.get(sid,{}).get('representative_sid') or sid}))
    for sid in sorted(set(all_results)|set(daily)):
        a=all_results.get(sid,{})
        d=daily.get(sid,{})
        if d.get('run_status')=='ran': row=d;cohort='full_universe';stage=d.get('source_run','daily500')
        elif a.get('stage')=='full_universe': row=a;cohort='full_universe';stage='stage2'
        else: row=a or d;cohort='screen_50stocks';stage='stage1'
        funnel['input_'+cohort]+=1
        s=scored.get(sid,{});f=features.get(sid,{})
        filename=Path(s.get('repo_path') or f.get('repo_path') or '').name
        c=by_name.get(filename,{})
        reasons=[]
        if not s or not f or not c: reasons.append('identity_missing')
        for evidence in [s,f,row]:
            path=evidence.get('repo_path')
            if path and Path(path).name!=filename: reasons.append('path_sid_mismatch')
        digest=hashlib.md5(norm_source(c.get('code','')).encode()).hexdigest()
        match=bool(c and f.get('src_hash')==digest)
        if not match: reasons.append('normalized_source_hash_mismatch')
        if row is d:
            if d.get('run_status')!='ran': reasons.append('run_not_successful')
        elif row.get('status')!='ok': reasons.append('run_not_successful')
        metrics={m:number(row.get(m)) for m in METRICS}
        raw=raws.get('stage2' if stage=='stage2_reused' else stage,{}).get(sid)
        if raw:
            metrics['errs']=number(raw.get('errs'))
            if raw.get('status')!='ok': reasons.append('raw_run_not_successful')
        if cohort=='full_universe' and metrics['errs'] is None: reasons.append('unknown_execution_errors')
        if metrics['errs'] is not None and metrics['errs']!=0: reasons.append('execution_errors')
        for m in WEIGHTS:
            if metrics[m] is None: reasons.append('missing_finite_'+m)
        if metrics['max_dd'] is not None and not -1<=metrics['max_dd']<=0: reasons.append('invalid_max_dd')
        for field,threshold in [('trades',100),('exposure',.02),('tickers_run',1000 if cohort=='full_universe' else None)]:
            if threshold is not None and (metrics[field] is None or metrics[field]<threshold): reasons.append('insufficient_'+field)
        if str(row.get('fill_artifact_suspect','')).lower()=='true': reasons.append('fill_artifact_suspect')
        if metrics['sharpe'] is not None and metrics['sharpe']>3: reasons.append('daily_sharpe_gt_3')
        if 'FILL_ARTIFACT_SUSPECT' in prior.get(sid,{}).get('flags',''): reasons.append('prior_fill_artifact_suspect')
        if any(x['sharpe'] is not None and x['sharpe']>3 for main in intraday[sid] for x in [main]+main.get('source_alternates',[])): reasons.append('saved_intraday_sharpe_gt_3')
        logic=number(c.get('score'))
        if logic is None: reasons.append('missing_current_logic_score')
        flags=[x for x in re.split(r'[;|,]',s.get('red_flags','')) if x]
        penalty_reasons=[];penalty=0
        if f.get('leak_hard') or any('LEAK_' in x for x in flags): penalty+=15;penalty_reasons.append('静态前视疑点（未确认作弊）：-15')
        if f.get('impl_bugs') or any('BUG_' in x for x in flags): penalty+=10;penalty_reasons.append('静态实现疑点（未确认错误执行）：-10')
        recent={m:number(row.get('oos3_'+m)) for m in ['cagr','total_return','sharpe','max_dd','calmar','trades']}
        recent['label']='历史末3年子区间（非独立样本外）'
        rep=sid_of({'sid':s.get('representative_sid') or sid})
        record=dict(sid=sid,id=c.get('id'),filename=filename,title=c.get('title') or s.get('name'),category=c.get('category'),current_logic_score=logic,current_logic_review=c.get('review_status') or '',current_logic_review_details={k:c.get(k) for k in ['review_status','score_label','scores','strengths','weaknesses','risks','evidence_level']},reported_daily=metrics,daily_source=dict(**row.get('_source',{}),stage=stage,cohort=cohort,raw_verification=raw.get('_source') if raw else None),reported_recent=recent,intraday=intraday[sid],prior_rationality_score=number(s.get('rationality_score')),prior_comment=s.get('comment_cn') or '',red_flags=flags,features={k:v for k,v in f.items() if not k.startswith('_')},source_match=dict(lossy_match=match,version_verified=False,status='normalized_match' if match else 'rejected',normalized_md5=digest,expected_md5=f.get('src_hash'),method='lossy normalized MD5; not exact source version binding',catalog_source_sha256=c.get('source_sha256'),feature_source=f.get('_source'),scored_source=s.get('_source')),duplicate_members=sorted(group_members.get(rep,[sid])),representative_sid=rep,daily_score=None,recent_score=None,combined_score=None,risk_penalty=min(25,penalty),penalty_reasons=penalty_reasons,cohort=cohort,primary_rank=None,eligibility_notes=sorted(set(reasons)))
        if d.get('run_status')=='skipped':
            record['eligibility_notes'].append('全量日线被跳过：'+str(d.get('skip_reason') or '原因未记录'))
            record['full_daily_skip']={'run_status':d['run_status'],'skip_reason':d.get('skip_reason'),**d.get('_source',{})}
        if cohort=='screen_50stocks' and metrics['tickers_run'] is None: record['eligibility_notes'].append('初筛50票配置；实际运行票数缺失，未补50')
        if metrics['errs'] is None: record['eligibility_notes'].append('运行错误数未知；未补零')
        if reasons: record['exclusion_reasons']=sorted(set(reasons));excluded.append(record)
        else: candidates.append(record);funnel['eligible_before_dedup_'+cohort]+=1
    # Freeze group identity before quality filtering; never cherry-pick a passing
    # duplicate when its data-bearing representative has a disqualifying result.
    data_members=defaultdict(list)
    for r in candidates+excluded:
        if r['reported_daily']['cagr'] is not None and 'run_not_successful' not in r.get('exclusion_reasons',[]):
            data_members[(r['cohort'],r['representative_sid'])].append(r['sid'])
    fixed={key:min(ids,key=lambda sid:(sid!=key[1],sid)) for key,ids in data_members.items()}
    pools={}
    for cohort in ['full_universe','screen_50stocks']:
        groups=defaultdict(list)
        for row in candidates:
            if row['cohort']==cohort: groups[row['representative_sid']].append(row)
        pool=[]
        for rep,members in groups.items():
            if cohort=='screen_50stocks' and rep in attempted_full_groups:
                for r in members:
                    r['exclusion_reasons']=['duplicate_full_daily_group'];r['eligibility_notes'].append('duplicate_full_daily_group');excluded.append(r)
                continue
            chosen_sid=fixed.get((cohort,rep))
            chosen=next((r for r in members if r['sid']==chosen_sid),None)
            if chosen is None:
                for r in members:
                    r['exclusion_reasons']=['fixed_representative_ineligible'];r['eligibility_notes'].append('fixed_representative_ineligible');excluded.append(r)
                continue
            pool.append(chosen)
            for r in members:
                if r is not chosen:
                    r['exclusion_reasons']=['duplicate_group'];r['eligibility_notes'].append('duplicate_group');excluded.append(r)
        for field in ['reported_daily','reported_recent']:
            valid=[r for r in pool if all(r[field].get(m) is not None for m in WEIGHTS)]
            target='daily_score' if field=='reported_daily' else 'recent_score'
            for r in valid: r[target]=0.
            for m,weight in WEIGHTS.items():
                for r,pct in zip(valid,percentiles([r[field][m] for r in valid])): r[target]+=100*weight*pct
        for r in pool:
            r['combined_score']=.7*r['daily_score']+.1*(r['recent_score'] if r['recent_score'] is not None else 0)+.2*r['current_logic_score']-r['risk_penalty']
            if r['recent_score'] is None: r['eligibility_notes'].append('近3年指标缺失：该项不获分（最高损失10分），不是0收益')
        pool.sort(key=lambda r:(-r['combined_score'],r['sid']))
        for n,r in enumerate(pool,1):
            if cohort=='full_universe': r['primary_rank']=n
            else: r['supplement_rank']=n
        pools[cohort]=pool
        funnel['ranked_'+cohort]=len(pool)
    for r in pools['full_universe'] + pools['screen_50stocks'] + excluded:
        r['cohort']='full_daily' if r['cohort']=='full_universe' else 'screening50'
        r['daily_source']['cohort']=r['cohort']
    full_exclusions=Counter(x for r in excluded if r['cohort']=='full_daily' for x in r['exclusion_reasons'])
    reasons=Counter(x for r in excluded for x in r['exclusion_reasons'])
    return clean(dict(primary=pools['full_universe'],supplement_pool=pools['screen_50stocks'],excluded=excluded,summary=dict(funnel=dict(funnel),exclusion_counts=dict(reasons),full_daily_exclusion_counts=dict(full_exclusions),primary_count=len(pools['full_universe']),supplement_count=len(pools['screen_50stocks']),supplement_pool_count=len(pools['screen_50stocks']),benchmark=benchmark,benchmark_source=RESULTS+'summary.json',score_formula='0.70*daily_score + 0.10*recent_score + 0.20*current_logic_score - risk_penalty',performance_formula='100*(0.30*pct(sharpe)+0.25*pct(calmar)+0.25*pct(cagr)+0.20*pct(max_dd))',percentile_method='within eligible deduplicated cohort; ties average; singleton 50',intraday_role='display and cross-evidence anomaly gate (Sharpe > 3); no score contribution; absent Top100 records mean unavailable, not failed',recent_label='历史末3年子区间（非独立样本外）'),source_manifest=manifest))
