"""Paired sentence-clustered bootstrap of candidate - judge_cheap_disg on the common, label-consistent track-L items of exp A/C/D."""
import json, random
from pathlib import Path
import numpy as np
from sklearn.metrics import roc_auc_score
B = Path(__file__).resolve().parents[3] / 'round-1'
def rj(p): return [json.loads(l) for l in open(p) if l.strip()]
A={r['item_id']:r for r in rj(B/'experiment-1/src/results/per_item.jsonl')}
C={r['item_id']:r for r in rj(B/'experiment-3/src/results/analysis_table.jsonl')}
D={r['item_id']:r for r in rj(B/'experiment-4/src/results/per_item_scores.jsonl')}
sa=json.load(open(B/'experiment-1/src/screen_items.json')); sa=sa['items'] if isinstance(sa,dict) else sa
labA={r['item_id']:r.get('label') for r in sa}
ks=[k for k in A if A[k]['track']=='L' and k in C and k in D and labA.get(k)==C[k]['label']==D[k]['label'] and labA[k] in('CORRECT','ERROR') and D[k].get('judge_cheap_disg') is not None]
y=np.array([labA[k]=='ERROR' for k in ks])
S={'c_score':np.array([C[k]['c_score'] for k in ks]),'fused_H':np.array([A[k]['p_fused_H'] for k in ks]),
   'judge_disg':-np.array([D[k]['judge_cheap_disg'] for k in ks]),'sc5_cheap':-np.array([C[k]['sc5_eq_frac_cheap'] for k in ks])}
sent=[A[k]['text'].strip().lower() for k in ks]; us=sorted(set(sent)); idx={s:[i for i,t in enumerate(sent) if t==s] for s in us}
rng=random.Random(0); out={'n':len(ks),'n_err':int(y.sum()),'n_sent':len(us),'auroc':{m:round(roc_auc_score(y,v),4) for m,v in S.items()}}
for m in ['c_score','fused_H']:
    d=[]
    for _ in range(2000):
        ii=[i for s in rng.choices(us,k=len(us)) for i in idx[s]]
        yy=y[ii]
        if yy.all() or (~yy).all(): continue
        d.append(roc_auc_score(yy,S[m][ii])-roc_auc_score(yy,S['judge_disg'][ii]))
    out[f'{m}_minus_judge_disg']={'delta':round(float(np.mean(d)),4),'ci95':[round(float(np.percentile(d,2.5)),4),round(float(np.percentile(d,97.5)),4)]}
print(json.dumps(out,indent=1)); json.dump(out,open('paired_boot.json','w'),indent=1)
