"""Independent recompute of exp-9 (T6-E, CSC) headline numbers from results/per_item_csc_E.jsonl."""
import json, random
from collections import defaultdict
P=str(__import__("pathlib").Path(__file__).resolve().parents[3] / "round-4/experiment-9/src/results/per_item_csc_E.jsonl")
rows=[json.loads(l) for l in open(P)]
prim=[r for r in rows if r['in_PRIMARY']]
def auc(ys,ss):
    pos=[s for y,s in zip(ys,ss) if y==1]; neg=[s for y,s in zip(ys,ss) if y==0]
    if not pos or not neg: return None
    w=0.0
    for p in pos:
        for n in neg: w+= 1.0 if p>n else 0.5 if p==n else 0.0
    return w/(len(pos)*len(neg))
def strat(rs,key):
    # within-stratum AUROC: pairs only within same stratum
    num=0.0; den=0
    by=defaultdict(list)
    for r in rs: by[r['stratum']].append(r)
    for st,g in by.items():
        pos=[r[key] for r in g if r['y_R_AB']==1]; neg=[r[key] for r in g if r['y_R_AB']==0]
        for p in pos:
            for n in neg: num+= 1.0 if p>n else 0.5 if p==n else 0.0
        den+=len(pos)*len(neg)
    return num/den
def boot(rs,key,B=300,seed=0):
    rnd=random.Random(seed); sents=defaultdict(list)
    for r in rs: sents[r['sentence_id']].append(r)
    ids=list(sents); vals=[]
    for _ in range(B):
        samp=[x for i in (rnd.choice(ids) for _ in ids) for x in sents[i]]
        try: vals.append(strat(samp,key))
        except ZeroDivisionError: pass
    vals.sort(); return vals[int(0.025*len(vals))], vals[int(0.975*len(vals))-1]
out={}
out['n_primary']=len(prim); out['n_err']=sum(r['y_R_AB'] for r in prim)
for k in ['c_csc','c_free_exact','c_score_align']:
    rs=[r for r in prim if r[k] is not None]
    out[k]={'n':len(rs),'strat':round(strat(rs,k),4),'ci_B300':[round(x,3) for x in boot(rs,k)]}
err=[r for r in prim if r['y_R_AB']==1]; cor=[r for r in prim if r['y_R_AB']==0]
for k in ['c_csc','c_free_exact']:
    out[k]['e']=round(sum(1 for r in err if r[k] is not None and r[k]<=0.5)/len(err),3)
    out[k]['d']=round(sum(1 for r in cor if r[k] is not None and r[k]>0.5)/len(cor),3)
out['primary_stratum_counts']={s:[sum(1 for r in prim if r['stratum']==s and r['y_R_AB']==1),sum(1 for r in prim if r['stratum']==s and r['y_R_AB']==0)] for s in ['L25','L20','EXC','CTRL']}
full_cor=[r for r in rows if r['y_R_AB']==0]; out['full_CTRL_share_of_CORRECT']=round(sum(1 for r in full_cor if r['stratum']=='CTRL')/len(full_cor),3)
out['primary_CTRL_share_of_CORRECT']=round(sum(1 for r in cor if r['stratum']=='CTRL')/len(cor),3)
print(json.dumps(out,indent=1))
json.dump(out,open(str(__import__("pathlib").Path(__file__).resolve().parents[3] / "round-4/review/audit/recompute_csc.json"),"w"),indent=1)
