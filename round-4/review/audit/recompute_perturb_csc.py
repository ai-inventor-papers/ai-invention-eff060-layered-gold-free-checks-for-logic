"""Recompute exp-10 FREE consensus base FA (d on verified bases) vs mutant recall, and LOCAL2 e."""
import json
P=str(__import__("pathlib").Path(__file__).resolve().parents[3] / "round-4/experiment-10/src/results/perturb_csc_scores.jsonl")
rows=[json.loads(l) for l in open(P)]
out={}
for k in ['c_align_exp8','c_free3_exact','c_free3_align','c_proxy','judge_cheap_disg_exp8','c_local']:
    for src in [False,True]:
        base=[r for r in rows if r['op_label']=='BASE' and r['is_rcomp']==src and r.get(k) is not None]
        mut=[r for r in rows if r['y']==1 and r['is_rcomp']==src and r.get(k) is not None]
        if not base and not mut: continue
        out[f"{k}|{'RCOMP' if src else 'E'}"]={
          'n_base':len(base),'base_FA(c>0.5)':round(sum(r[k]>0.5 for r in base)/len(base),3) if base else None,
          'n_mut':len(mut),'mutant_recall(c>0.5)':round(sum(r[k]>0.5 for r in mut)/len(mut),3) if mut else None}
# LOCAL2: e with and without score==0.5 (insufficient peers)
mut=[r for r in rows if r['y']==1 and r.get('c_local') is not None]
out['LOCAL2_e_all']=round(sum(r['c_local']<=0.5 for r in mut)/len(mut),3)
out['LOCAL2_share_exact_0.5']=round(sum(r['c_local']==0.5 for r in mut)/len(mut),3)
print(json.dumps(out,indent=1))
json.dump(out,open(P.replace('round-4/experiment-10/src/results/perturb_csc_scores.jsonl','round-4/review/audit/recompute_perturb_csc.json'),'w'),indent=1)
