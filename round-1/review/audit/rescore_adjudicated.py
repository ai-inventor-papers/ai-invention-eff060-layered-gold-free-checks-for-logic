"""Re-score iter-1 metrics on track L under dataset-E adjudicated screen labels (tiers A+B, and all non-CONTESTED)."""
import json
from pathlib import Path
import numpy as np
from sklearn.metrics import roc_auc_score
B=Path(__file__).resolve().parents[3] / 'round-1'
def rj(p): return [json.loads(l) for l in open(p) if l.strip()]
adj=json.load(open(B/'dataset-1/src/screen_adjudicated_labels.json'))
A={r['item_id']:r for r in rj(B/'experiment-1/src/results/per_item.jsonl')}
C={r['item_id']:r for r in rj(B/'experiment-3/src/results/analysis_table.jsonl')}
D={r['item_id']:r for r in rj(B/'experiment-4/src/results/per_item_scores.jsonl')}
metrics=[('fused_H',A,'p_fused_H',1),('l3',A,'l3_score',1),('l2_bow',A,'bow_uncarried',1),
 ('c_score',C,'c_score',1),('sc5_cheap',C,'sc5_eq_frac_cheap',-1),
 ('judge_cheap_disg',D,'judge_cheap_disg',-1),('rt_nli_min',D,'rt_nli_min',-1),('pilot_rerun_jacc',D,'pilot_rerun_jacc',-1)]
out={}
for view,tiers in [('adj_all_tiers',None),('adj_tierAB',{'A','B'})]:
    keys=[k for k,v in adj.items() if v['track']=='L' and v['final_label'] in('CORRECT','ERROR') and not v.get('reading_choice') and (tiers is None or v['label_tier'] in tiers)]
    res={'n_items':len(keys),'n_err':sum(adj[k]['final_label']=='ERROR' for k in keys)}
    common=[k for k in keys if all(k in dct and dct[k].get(f) is not None for _,dct,f,_ in metrics)]
    y=np.array([adj[k]['final_label']=='ERROR' for k in common])
    res['n_common']=len(common); res['n_common_err']=int(y.sum())
    res['auroc_common']={m:round(roc_auc_score(y,[s*dct[k][f] for k in common]),4) for m,dct,f,s in metrics}
    out[view]=res
# agreement of the experiments' own labels with adjudicated final label
agree={}
for nm,dct,labf in [('D',D,'label'),('C',C,'label')]:
    from collections import Counter
    c=Counter()
    for k,v in dct.items():
        if v.get('track')=='L' and k in adj and v.get(labf) in('CORRECT','ERROR'):
            c[(v[labf],adj[k]['final_label'])]+=1
    agree[nm]={str(k):n for k,n in c.most_common()}
out['own_vs_adjudicated']=agree
print(json.dumps(out,indent=1)); json.dump(out,open('rescore_adjudicated.json','w'),indent=1)
