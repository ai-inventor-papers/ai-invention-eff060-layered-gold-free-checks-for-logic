"""Reviewer audit: is c_align operator-sensitive on PERTURB, or does it just flag any departure from an endorsed base?
Reads gen_art_experiment_8/results/perturb_scores.jsonl (read-only)."""
import json, collections
P=str(__import__("pathlib").Path(__file__).resolve().parents[3] / 'round-3/experiment-8/src/results/perturb_scores.jsonl')
rows=[json.loads(l) for l in open(P)]
out={}
by=collections.defaultdict(list)
for r in rows:
    if r.get('is_rcomp') or r.get('c_align__status')!='ok': continue
    k=r['operator'] if r['y']==1 else ('CONTROL:'+str(r.get('control_type')) if r.get('control_type') else 'BASE')
    by[k].append(r['c_align'])
for k,v in sorted(by.items()):
    out[k]={'n':len(v),'share_c_eq_1':round(sum(x>=0.999999 for x in v)/len(v),4),'mean':round(sum(v)/len(v),4)}
    print(k,out[k])
# within-base AUROC predicted from base score alone: mutant c=1 always -> AUROC = P(ctrl<1)+0.5*P(ctrl==1)
ctrl=[x for k,v in by.items() if k=='BASE' or (k.startswith('CONTROL') and 'RENAME' not in k) for x in v]
p1=sum(x>=0.999999 for x in ctrl)/len(ctrl)
print('non-rename controls+BASE n',len(ctrl),'share c=1',round(p1,4),'predicted AUROC if every mutant has c=1:',round((1-p1)+0.5*p1,4))
out['predicted_auroc_if_all_mutants_c1']=round((1-p1)+0.5*p1,4)
json.dump(out,open(str(__import__("pathlib").Path(__file__).resolve().parents[3] / 'round-3/review/audit/perturb_c_align_constant.json'),'w'),indent=1)
