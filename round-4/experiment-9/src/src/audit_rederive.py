"""Independent re-derivation of the headline numbers through a DIFFERENT code path.

Reads raw files only (results/llm_cache.jsonl peer outputs, results/arms_built.json slot keys, results/salvage_rows.json,
data/frame_blind.jsonl, data/labels_RAB.jsonl, data/sentence_peers_free.json). It does not use csc.consensus_score,
_eq_canon, the fingerprint pre-filter, or eval 2 stats/mechanism. Instead it has its own z3 encoding (lowercased names,
arity-suffixed function symbols, a fresh solver per pair, 2 s), sklearn roc_auc_score, its own within-stratum AUROC and
e/d, and its own sentence bootstrap (seed 1, B = 1000). A placebo re-runs the paired test on labels permuted within
stratum; it must NOT give a CI excluding 0. Output: results/audit_rederive.json."""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
import z3
from sklearn.metrics import roc_auc_score

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "vendor" / "e8src"))
sys.setrecursionlimit(20000)
import vendor_e.fol as EF  # noqa: E402  (the dataset-E parser only; the z3 encoding below is independent)

U = z3.DeclareSort("Obj")


def jl(p):
    return [json.loads(l) for l in Path(p).read_text().splitlines() if l.strip()]


def enc(e, env, fns):
    k = e[0]
    if k in ("all", "ex"):
        v = z3.Const("v_" + e[1] + "_" + str(len(env)), U)
        body = enc(e[2], {**env, e[1]: v}, fns)
        return z3.ForAll([v], body) if k == "all" else z3.Exists([v], body)
    if k == "not":
        return z3.Not(enc(e[1], env, fns))
    if k == "atom":
        name, args = e[1].lower(), e[2]
        key = f"P_{name}_{len(args)}"
        if key not in fns:
            fns[key] = z3.Function(key, *([U] * len(args)), z3.BoolSort()) if args else z3.Bool(key)
        zargs = [env[a] if a in env else z3.Const("K_" + a.lower(), U) for a in args]
        return fns[key](*zargs) if args else fns[key]
    a, b = enc(e[1], env, fns), enc(e[2], env, fns)
    return {"and": z3.And, "or": z3.Or, "imp": z3.Implies, "iff": lambda x, y: x == y, "xor": z3.Xor}[k](a, b)


def parse(s):
    if not s or not str(s).strip():
        return None
    try:
        return EF.parse(str(s))
    except Exception:  # noqa: BLE001
        return None


def equiv(a, b) -> bool:
    ea, eb = parse(a), parse(b)
    if ea is None or eb is None:
        return False
    try:
        fns = {}
        s = z3.Solver()
        s.set("timeout", 2000)
        s.add(z3.Not(enc(ea, {}, fns) == enc(eb, {}, fns)))
        return s.check() == z3.unsat
    except Exception:  # noqa: BLE001
        return False


def score(cand, peers):
    usable = [p for p in peers if parse(p) is not None]
    if len(usable) < 2:
        return 0.5
    return 1 - sum(equiv(cand, p) for p in usable) / len(usable)


def strat_auc(y, s, st):
    num = den = 0.0
    for g in set(st):
        m = st == g
        yy, ss = y[m], s[m]
        pos, neg = ss[yy == 1], ss[yy == 0]
        if len(pos) and len(neg):
            w = len(pos) * len(neg)
            num += roc_auc_score(yy, ss) * w
            den += w
    return num / den


def main():
    fr = {r["row_key"]: r for r in jl(ROOT / "data/frame_blind.jsonl")}
    lab = {r["row_key"]: r["y"] for r in jl(ROOT / "data/labels_RAB.jsonl")}
    pri = json.loads((ROOT / "results/salvage_rows.json").read_text())["PRIMARY"]
    own = json.loads((ROOT / "results/arms_built.json").read_text())["arms"]["OWN"]
    cache = {r["key"]: r for r in jl(ROOT / "results/llm_cache.jsonl")}
    free = json.loads((ROOT / "data/sentence_peers_free.json").read_text())
    order = ["deepseek", "microsoft", "openai", "qwen"]
    rows = []
    for rk in pri:
        r = fr[rk]
        peers = [cache[s["key"]]["fol"] for s in own[rk]["slots"]]
        fams = [f for f in order if f != r["family"]][:3]
        fpeers = [free[r["sentence_id"]][f]["fol"] for f in fams if f in free.get(r["sentence_id"], {})]
        rows.append((rk, r["sentence_id"], r["stratum"], lab[rk], score(r["candidate_fol"], peers), score(r["candidate_fol"], fpeers),
                     r["T1__c_score_align"]))
    sid = np.array([x[1] for x in rows])
    st = np.array([x[2] for x in rows])
    y = np.array([x[3] for x in rows])
    c = np.array([x[4] for x in rows])
    f = np.array([x[5] for x in rows])
    a = np.array([x[6] for x in rows])
    ed = lambda s: {"e": float(np.mean(s[y == 1] <= 0.5)), "d": float(np.mean(s[y == 0] > 0.5))}  # noqa: E731
    by = defaultdict(list)
    for i, s_ in enumerate(sid):
        by[s_].append(i)
    keys = sorted(by)
    rng = np.random.default_rng(1)

    def boot_delta(yv, s1, s2, B=1000):
        out = []
        for _ in range(B):
            ix = np.concatenate([by[keys[j]] for j in rng.integers(0, len(keys), len(keys))])
            try:
                out.append(strat_auc(yv[ix], s1[ix], st[ix]) - strat_auc(yv[ix], s2[ix], st[ix]))
            except ValueError:
                continue
        return [float(np.percentile(out, 2.5)), float(np.percentile(out, 97.5))]
    res = {"n": len(rows), "n_err": int(y.sum()), "n_cor": int((1 - y).sum()),
           "strat_auroc": {"c_csc": strat_auc(y, c, st), "c_free_exact": strat_auc(y, f, st), "c_score_align": strat_auc(y, a, st)},
           "pooled_auroc": {"c_csc": roc_auc_score(y, c), "c_free_exact": roc_auc_score(y, f)},
           "ed": {"c_csc": ed(c), "c_free_exact": ed(f)},
           "delta_strat_csc_minus_free_exact": strat_auc(y, c, st) - strat_auc(y, f, st),
           "delta_ci_seed1_B1000": boot_delta(y, c, f)}
    # placebo: labels permuted within stratum (seed 7)
    prng = np.random.default_rng(7)
    yp = y.copy()
    for g in set(st):
        m = np.where(st == g)[0]
        yp[m] = prng.permutation(yp[m])
    res["placebo_permuted_labels"] = {"strat_auroc_c_csc": strat_auc(yp, c, st), "delta_strat": strat_auc(yp, c, st) - strat_auc(yp, f, st),
                                      "delta_ci": boot_delta(yp, c, f)}
    res["placebo_permuted_labels"]["ci_excludes_0 (must be False)"] = bool(res["placebo_permuted_labels"]["delta_ci"][0] > 0 or res["placebo_permuted_labels"]["delta_ci"][1] < 0)
    # compare against the pipeline's per-row values
    pipe = {r["row_key"]: r for r in jl(ROOT / "results/per_item_csc_E.jsonl")}
    res["row_agreement_with_pipeline"] = {"c_csc_exact_match_share": float(np.mean([abs(pipe[x[0]]["c_csc"] - x[4]) < 1e-9 for x in rows])),
                                          "c_free_exact_match_share": float(np.mean([abs(pipe[x[0]]["c_free_exact"] - x[5]) < 1e-9 for x in rows]))}
    (ROOT / "results/audit_rederive.json").write_text(json.dumps(res, indent=1))
    print(json.dumps(res, indent=1))


if __name__ == "__main__" and len(sys.argv) == 1:
    main()


def extra():
    """Second audit block: FULL-population FREE-MATCHED exact e/d (own z3 path), CSC d-vs-words slope (statsmodels Logit
    with sentence-clustered SEs instead of GEE), and cost per candidate straight from the raw call ledger."""
    import statsmodels.api as sm
    fr = {r["row_key"]: r for r in jl(ROOT / "data/frame_blind.jsonl")}
    lab = {r["row_key"]: r["y"] for r in jl(ROOT / "data/labels_RAB.jsonl")}
    free = json.loads((ROOT / "data/sentence_peers_free.json").read_text())
    order = ["deepseek", "microsoft", "openai", "qwen"]
    y, s = [], []
    for rk, r in fr.items():
        fams = [f for f in order if f != r["family"]][:3]
        fp = [free[r["sentence_id"]][f]["fol"] for f in fams if f in free.get(r["sentence_id"], {})]
        y.append(lab[rk])
        s.append(score(r["candidate_fol"], fp))
    y, s = np.array(y), np.array(s)
    out = {"FULL_free_exact": {"n": len(y), "e": float(np.mean(s[y == 1] <= 0.5)), "d": float(np.mean(s[y == 0] > 0.5))}}
    pri = set(json.loads((ROOT / "results/salvage_rows.json").read_text())["PRIMARY"])
    pipe = {r["row_key"]: r for r in jl(ROOT / "results/per_item_csc_E.jsonl")}
    cor = [(fr[k]["words"], fr[k]["n_conditions"], int(pipe[k]["c_csc"] > 0.5), fr[k]["sentence_id"]) for k in pri if lab[k] == 0]
    w = np.array([c[0] for c in cor], float)
    n = np.array([c[1] for c in cor], float)
    X = sm.add_constant(np.column_stack([(w - w.mean()) / w.std(ddof=1), (n - n.mean()) / n.std(ddof=1)]))
    g = np.unique([c[3] for c in cor], return_inverse=True)[1]
    m = sm.Logit(np.array([c[2] for c in cor]), X).fit(disp=0, cov_type="cluster", cov_kwds={"groups": g})
    out["CSC_d_words_slope_logit_clusterSE"] = {"b": float(m.params[1]), "ci": [float(v) for v in m.conf_int()[1]]}
    # cost per candidate from the raw ledger (keys -> usd), summed over each PRIMARY row's 3 OWN slots
    usd = {}
    for r in jl(ROOT / "results/api_cost_ledger.jsonl"):
        if r.get("usd"):
            usd[r["key"]] = r["usd"]
    own = json.loads((ROOT / "results/arms_built.json").read_text())["arms"]["OWN"]
    per = [sum(usd.get(sl["key"], 0.0) for sl in own[k]["slots"]) for k in pri]
    out["cost_per_candidate_undeduped_mean"] = float(np.mean(per))
    out["ledger_total_usd"] = float(sum(r.get("usd") or 0 for r in jl(ROOT / "results/api_cost_ledger.jsonl")))
    p = ROOT / "results/audit_rederive.json"
    d = json.loads(p.read_text())
    d["extra"] = out
    p.write_text(json.dumps(d, indent=1))
    print(json.dumps(out, indent=1))


if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "extra":
    extra()
