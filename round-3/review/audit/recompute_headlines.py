"""Reviewer recomputation of iteration-3 headline numbers from raw per-item files (read-only inputs).
T1: gen_art_experiment_6/results/per_item_T1.jsonl ; T2: gen_art_experiment_7/results/analysis_rows_SIG.jsonl"""
import json, numpy as np, collections
R=str(__import__("pathlib").Path(__file__).resolve().parents[3] / 'round-3/')
OUT=str(__import__("pathlib").Path(__file__).resolve().parents[3] / 'round-3/review/audit/recompute_headlines.json')
from scipy.stats import rankdata
def auc(y,s):
    y=np.asarray(y); s=np.asarray(s,float); pos=y==1; n1=pos.sum(); n0=(~pos).sum()
    if n1==0 or n0==0: return np.nan
    r=rankdata(s); return (r[pos].sum()-n1*(n1+1)/2)/(n1*n0)
def strat_auc(y,s,g):
    y=np.asarray(y); s=np.asarray(s,float); g=np.asarray(g); num=0; den=0
    for k in np.unique(g):
        m=g==k; n1=(y[m]==1).sum(); n0=(y[m]==0).sum()
        if n1 and n0: num+=auc(y[m],s[m])*n1*n0; den+=n1*n0
    return num/den
def boot(rows,fn,B=1000,seed=0):
    rng=np.random.default_rng(seed); by=collections.defaultdict(list)
    for r in rows: by[r['_c']].append(r)
    keys=list(by); vals=[]
    for _ in range(B):
        samp=[x for k in rng.choice(keys,len(keys)) for x in by[k]]
        vals.append(fn(samp))
    return [float(np.percentile(vals,2.5)),float(np.percentile(vals,97.5))]
out={}
rows=[json.loads(l) for l in open(R+'experiment-6/src/results/per_item_T1.jsonl')]
rab=[r for r in rows if r.get('in_R_AB') and r.get('pool')=='E_POOL']
for r in rab: r['_c']=r['sentence_id']
y=[r['y_R_AB'] for r in rab]; print('T1 R_AB n',len(rab),'err',sum(y),'sent',len({r['sentence_id'] for r in rab}))
def d_strat(rs,a='c_score_align',b='judge_cheap_disg'):
    yy=[r['y_R_AB'] for r in rs]; g=[r['source_stratum'] for r in rs]
    return strat_auc(yy,[r[a] for r in rs],g)-strat_auc(yy,[r[b] for r in rs],g)
t1={'n':len(rab),'n_err':int(sum(y))}
for m in ['c_score_align','p_peer_text','judge_cheap_disg','judge_cheap2_orig','S4_full_oof']:
    t1[m]={'pooled':round(auc(y,[r[m] for r in rab]),4),'strat':round(strat_auc(y,[r[m] for r in rab],[r['source_stratum'] for r in rab]),4)}
t1['delta_strat_c_minus_flashlite_disg']=round(d_strat(rab),4)
t1['delta_strat_c_minus_flashlite_disg_ci_B1000']=boot(rab,d_strat)
l25=[r for r in rab if r['source_stratum']=='L25']
t1['L25_pooled_c_minus_flashlite']=round(auc([r['y_R_AB'] for r in l25],[r['c_score_align'] for r in l25])-auc([r['y_R_AB'] for r in l25],[r['judge_cheap_disg'] for r in l25]),4)
t1['L25_ci_B1000']=boot(l25,lambda rs: auc([r['y_R_AB'] for r in rs],[r['c_score_align'] for r in rs])-auc([r['y_R_AB'] for r in rs],[r['judge_cheap_disg'] for r in rs]))
out['T1']=t1; print(json.dumps(t1,indent=1))
rows=[json.loads(l) for l in open(R+'experiment-7/src/results/analysis_rows_SIG.jsonl')]
rs=[r for r in rows if r['label'] in ('ERROR','CORRECT') and r['judge_cheap_disg'] is not None and r['c_score_sig'] is not None]
yy=[1 if r['label']=='ERROR' else 0 for r in rs]; g=[r['template_id'] for r in rs]
t2={'n':len(rs),'n_err':sum(yy),'c_sig_within_template':round(strat_auc(yy,[r['c_score_sig'] for r in rs],g),4),
    'judge_cheap_disg_within_template':round(strat_auc(yy,[r['judge_cheap_disg'] for r in rs],g),4)}
allr=[r for r in rows if r['label'] in ('ERROR','CORRECT')]
t2['n_all']=len(allr)
# endorsement e: share of ERROR rows with c<0.5 ; divergence d: CORRECT rows with c>=0.5
e=[r for r in allr if r['label']=='ERROR']; c=[r for r in allr if r['label']=='CORRECT']
t2['e']=round(np.mean([r['c_score_sig']<0.5 for r in e]),4); t2['d']=round(np.mean([r['c_score_sig']>=0.5 for r in c]),4)
out['T2_SIG']=t2; print(json.dumps(t2,indent=1))
json.dump(out,open(OUT,'w'),indent=1)
