"""Reviewer audit: join exp5 (PEER+TEXT) and exp6 (baselines, S4_local) on E R_AB rows.
Recompute headline AUROCs and the never-computed paired delta PT - S4_local, plus a
cross-fitted nested stack [S4_local, PT] vs S4_local on exp6's fold_E."""
import json, numpy as np
from pathlib import Path
from sklearn.metrics import roc_auc_score
from sklearn.linear_model import LogisticRegression
G = Path(__file__).resolve().parents[3] / 'round-2'
OUT = Path(__file__).parent / 'pt_vs_s4.json'
e6 = json.load(open(G/'experiment-6/src/full_method_out.json'))
rows6 = {}
for ds in e6['datasets']:
    if ds['dataset'] != 'E_heldout': continue
    for ex in ds['examples']:
        inp = json.loads(ex['input'])
        k = (ex['metadata_item_id'], inp.get('prompt_variant'))
        rows6.setdefault(k, []).append(ex)
rows5 = {}
for l in open(G/'experiment-5/src/results/per_item_E.jsonl'):
    d = json.loads(l); rows5.setdefault((d['item_id'], d['prompt_variant']), []).append(d)
def f(x):
    try: return float(x)
    except: return None
recs = []
for k, L6 in rows6.items():
    if len(L6) != 1 or k not in rows5 or len(rows5[k]) != 1: continue
    ex = L6[0]; d = rows5[k][0]
    if not ex.get('metadata_in_R_AB'): continue
    y = {'ERROR': 1, 'CORRECT': 0}.get(ex['output'])
    if y is None: continue
    rec = dict(y=y, sid=ex['metadata_sentence_id'], fold=ex['metadata_fold_E'],
               stratum=ex['metadata_strata']['source_stratum'], tier=ex.get('metadata_label_tier'),
               pt=f(d['p_peer_text']), cal=f(d['c_score_align']), s4=f(ex['predict_S4_local_oof_RAB']),
               s4nj=f(ex['predict_S4_local_noLLMjudge_oof_RAB']), jl=f(ex['predict_judge_local_qwen8b_disg']))
    recs.append(rec)
n_before = len(recs); recs = [r for r in recs if None not in (r['pt'], r['s4'], r['jl'], r['cal'], r['s4nj'])]; print('R_AB rows joined', n_before, 'complete', len(recs))
y = np.array([r['y'] for r in recs]); sid = np.array([r['sid'] for r in recs])
X = {k: np.array([r[k] if r[k] is not None else np.nan for r in recs]) for k in ['pt','cal','s4','s4nj','jl']}
fold = np.array([r['fold'] for r in recs])
# nested cross-fit stack
def stack(cols):
    Z = np.column_stack([X[c] for c in cols]); oof = np.zeros(len(y))
    for k in np.unique(fold):
        tr, te = fold != k, fold == k
        mu, sd = Z[tr].mean(0), Z[tr].std(0) + 1e-9
        m = LogisticRegression(C=1.0, max_iter=2000).fit((Z[tr]-mu)/sd, y[tr])
        oof[te] = m.predict_proba((Z[te]-mu)/sd)[:, 1]
    return oof
X['s4_plus_pt'] = stack(['s4', 'pt'])
X['s4_refit'] = stack(['s4'])
usids = np.unique(sid); idx = {s: np.where(sid == s)[0] for s in usids}
rng = np.random.default_rng(0)
def boot(a, b, B=2000):
    base = roc_auc_score(y, X[a]) - (roc_auc_score(y, X[b]) if b else 0)
    ds = []
    for _ in range(B):
        ii = np.concatenate([idx[s] for s in rng.choice(usids, len(usids))])
        if len(np.unique(y[ii])) < 2: continue
        ds.append(roc_auc_score(y[ii], X[a][ii]) - (roc_auc_score(y[ii], X[b][ii]) if b else 0))
    return [round(base, 4), [round(float(np.percentile(ds, 2.5)), 4), round(float(np.percentile(ds, 97.5)), 4)]]
out = {'n': int(len(y)), 'n_err': int(y.sum()), 'n_sent': int(len(usids)),
       'auroc': {k: round(float(roc_auc_score(y, X[k])), 4) for k in ['pt','cal','s4','s4nj','jl','s4_plus_pt','s4_refit']},
       'delta_pt_minus_s4local': boot('pt', 's4'),
       'delta_cal_minus_s4local': boot('cal', 's4'),
       'delta_pt_minus_s4_noLLMjudge': boot('pt', 's4nj'),
       'delta_pt_minus_judge_local': boot('pt', 'jl'),
       'nested_s4pt_minus_s4refit': boot('s4_plus_pt', 's4_refit')}
long = np.isin(np.array([r['stratum'] for r in recs]), ['L25','L20','EXC'])
yl = y[long]
out['long_pool'] = {'n': int(long.sum()), **{k: round(float(roc_auc_score(yl, X[k][long])), 4) for k in ['pt','s4','jl','cal']}}
json.dump(out, open(OUT, 'w'), indent=1); print(json.dumps(out, indent=1))
