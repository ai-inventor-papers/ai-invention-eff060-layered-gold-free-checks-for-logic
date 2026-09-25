"""Cross-experiment audit: join exp A/C/D per-item scores on item_id, compare labels, recompute AUROCs on common items."""
import json, collections
from pathlib import Path
B = Path(__file__).resolve().parents[3] / 'round-1'
def rj(p): return [json.loads(l) for l in open(p) if l.strip()]
def auroc(s, y):
    pos=[a for a,b in zip(s,y) if b]; neg=[a for a,b in zip(s,y) if not b]
    if not pos or not neg: return None
    w=0.0
    for p in pos:
        for n in neg: w += 1 if p>n else 0.5 if p==n else 0
    return w/(len(pos)*len(neg))
A = {r['item_id']: r for r in rj(B/'experiment-1/src/results/per_item.jsonl')}
C = {r['item_id']: r for r in rj(B/'experiment-3/src/results/analysis_table.jsonl')}
D = {r['item_id']: r for r in rj(B/'experiment-4/src/results/per_item_scores.jsonl')}
# labels for A come from screen_items
sa = json.load(open(B/'experiment-1/src/screen_items.json'))
sa = sa['items'] if isinstance(sa, dict) and 'items' in sa else sa
labA = {r['item_id']: r.get('label') for r in sa}
out = {}
for name, dct in [('A',A),('C',C),('D',D)]:
    L = [k for k,v in dct.items() if v.get('track')=='L']
    out[f'n_{name}_trackL'] = len(L)
    labs = collections.Counter((dct[k].get('label') if name!='A' else labA.get(k)) for k in L)
    out[f'labels_{name}_trackL'] = dict(labs)
def lab(name,k):
    return labA.get(k) if name=='A' else {'C':C,'D':D}[name][k].get('label')
LA={k for k,v in A.items() if v.get('track')=='L'}; LC={k for k,v in C.items() if v.get('track')=='L'}; LD={k for k,v in D.items() if v.get('track')=='L'}
common = LA & LC & LD
out['n_common_trackL_ids'] = len(common)
out['n_LA_only']=len(LA-LC-LD); out['n_LD_minus_LA']=len(LD-LA); out['n_LC_minus_LD']=len(LC-LD)
# label disagreement matrix among common ids
dis = collections.Counter()
for k in common:
    dis[(lab('A',k),lab('C',k),lab('D',k))]+=1
out['label_triples_common_top'] = {str(k):v for k,v in dis.most_common(25)}
# consistent binary set
S=[k for k in common if lab('A',k)==lab('C',k)==lab('D',k) and lab('A',k) in ('CORRECT','ERROR')]
out['n_common_consistent_binary']=len(S)
y=[lab('A',k)=='ERROR' for k in S]
out['n_err_common']=sum(y)
def g(dct,k,f):
    v=dct[k].get(f); return v
res={}
for nm,dct,f,sign in [('fused_H',A,'p_fused_H',1),('l2_bow',A,'bow_uncarried',1),('l3',A,'l3_score',1),
                     ('c_score',C,'c_score',1),('sc5_cheap',C,'sc5_eq_frac_cheap',-1),
                     ('judge_cheap_disg',D,'judge_cheap_disg',-1),('judge_cheap_orig',D,'judge_cheap_orig',-1),('rt_nli_min',D,'rt_nli_min',-1)]:
    ks=[(k,yy) for k,yy in zip(S,y) if dct[k].get(f) is not None]
    s=[sign*dct[k][f] for k,_ in ks]; yy=[b for _,b in ks]
    res[nm]={'n':len(ks),'auroc':round(auroc(s,yy),4) if ks else None}
out['auroc_on_common_consistent']=res
# each experiment's own-label AUROC over its own primary set (recompute)
own={}
yC=[(k,C[k]['label']=='ERROR') for k in LC if C[k]['label'] in('CORRECT','ERROR') and C[k].get('c_score') is not None]
own['c_score_own']=(len(yC),round(auroc([C[k]['c_score'] for k,_ in yC],[b for _,b in yC]),4))
yD=[(k,D[k]['label']=='ERROR') for k in LD if D[k]['label'] in('CORRECT','ERROR')]
sD=[(-D[k]['judge_cheap_disg'] if D[k].get('judge_cheap_disg') is not None else None) for k,_ in yD]
kk=[(s,b) for s,(k,b) in zip(sD,yD) if s is not None]
own['judge_cheap_disg_own_nonmissing']=(len(kk),round(auroc([a for a,_ in kk],[b for _,b in kk]),4))
yA=[(k,labA[k]=='ERROR') for k in LA if labA.get(k) in('CORRECT','ERROR')]
own['fused_own']=(len(yA),round(auroc([A[k]['p_fused_H'] for k,_ in yA],[b for _,b in yA]),4))
out['own_label_recompute']=own
print(json.dumps(out,indent=1))
json.dump(out,open(Path(__file__).parent/'join_audit.json','w'),indent=1)
