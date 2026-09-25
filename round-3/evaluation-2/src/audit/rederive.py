#!/usr/bin/env python3
"""Independent re-derivation of the headline numbers, through a DIFFERENT code path than src/ (no import of src/).

Reads the raw files directly: exp 5 per_item_E.jsonl + E_labels.jsonl + prereg.json, and this artifact's label-free
pairwise_classes_E.jsonl. It uses sklearn roc_auc_score, pandas groupby, a statsmodels GLM with cluster-robust SE (not GEE)
and its own bootstrap loop. It then runs PLACEBO versions (shuffled labels) of each test and checks that they FAIL.
Writes audit/rederive.json. Usage: uv run audit/rederive.py
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from sklearn.metrics import roc_auc_score

ROOT = Path(__file__).resolve().parent.parent
E5 = Path("/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_5")
A = json.loads((ROOT / "results" / "part_a.json").read_text())  # the values being audited (compared, never reused)


def rd(p):
    return pd.read_json(p, lines=True)


# ------------------------------------------------------------------ raw frame
it = rd(E5 / "results/per_item_E.jsonl")
lab = rd(E5 / "data/E_labels.jsonl")[["row_key", "final_label", "label_tier", "reading_choice", "correct_not_equivalent"]]
df = it.merge(lab, on="row_key", how="inner")
df["stratum"] = df.strata.map(lambda s: s["source_stratum"])
df["words"] = df.strata.map(lambda s: s["words"])
df["ncond"] = df.strata.map(lambda s: s["n_conditions"])
rab = df[(df.system_class == "llm") & (~df.reading_choice.astype(bool)) & df.final_label.isin(["CORRECT", "ERROR"])
         & df.label_tier.isin(["A", "B"])].copy()
rab["y"] = (rab.final_label == "ERROR").astype(int)
neutral = json.loads((E5 / "results/prereg.json").read_text())["imputation"]["neutral"]["c_score_align"]
rab["c_imp"] = np.where(rab.coverage_status == "UNPARSEABLE", 1.0, rab.c_score_align.fillna(neutral))
out = {"G0_n": len(rab), "G0_err": int(rab.y.sum()), "G0_sent": int(rab.sentence_id.nunique()),
       "G1_auroc_frozen_imputed": roc_auc_score(rab.y, rab.c_imp)}
P = rab[(rab.coverage_status != "UNPARSEABLE") & rab.c_score_align.notna()].copy().reset_index(drop=True)
P["endorsed"] = (P.c_score_align < 0.5).astype(int)
e = P.loc[P.y == 1, "endorsed"].mean()
d = 1 - P.loc[P.y == 0, "endorsed"].mean()
out.update({"n_scorable": len(P), "e_MAJ": e, "d_MAJ": d, "auroc_b_MAJ_sklearn": roc_auc_score(P.y, 1 - P.endorsed),
            "auroc_c_graded": roc_auc_score(P.y, P.c_score_align)})
out["delta_graded_minus_binary"] = out["auroc_c_graded"] - out["auroc_b_MAJ_sklearn"]

# ------------------------------------------------------------------ NET (own tercile cut via pd.cut)
sent_words = rab.groupby("sentence_id").words.first()
q1, q2 = sent_words.quantile([1 / 3, 2 / 3]).values
P["terc"] = pd.cut(P.words, [-np.inf, q1, q2, np.inf], labels=["T1", "T2", "T3"])


def ed_sum(frame, ycol="y"):
    return frame.loc[frame[ycol] == 1, "endorsed"].mean() + (1 - frame.loc[frame[ycol] == 0, "endorsed"].mean())


out["NET_words_T3_minus_T1"] = ed_sum(P[P.terc == "T3"]) - ed_sum(P[P.terc == "T1"])

# ------------------------------------------------------------------ own cluster bootstrap (loop over sentence draws)
sids = P.sentence_id.unique()
groups = {s: g.index.values for s, g in P.groupby("sentence_id")}


def cboot(stat, frame_ycol="y", B=1000, seed=7):
    rng = np.random.default_rng(seed)
    vals = []
    for _ in range(B):
        ix = np.concatenate([groups[s] for s in rng.choice(sids, len(sids))])
        vals.append(stat(P.loc[ix], frame_ycol))
    return [float(np.nanpercentile(vals, 2.5)), float(np.nanpercentile(vals, 97.5))]


def net_stat(f, ycol):
    return ed_sum(f[f.terc == "T3"], ycol) - ed_sum(f[f.terc == "T1"], ycol)


out["NET_ci_own_bootstrap_B1000"] = cboot(net_stat)

# ------------------------------------------------------------------ M1 / M2 via GLM + cluster-robust SE (not GEE)
P["zw"] = 0.0
P["zn"] = 0.0


def glm_slope(frame, dep, term):
    f = frame.copy()
    f["zw"] = (f.words - f.words.mean()) / f.words.std()
    f["zn"] = (f.ncond - f.ncond.mean()) / f.ncond.std()
    r = smf.glm(f"{dep} ~ zn + zw + C(stratum)", f, family=sm.families.Binomial()).fit(
        cov_type="cluster", cov_kwds={"groups": pd.factorize(f.sentence_id)[0]})
    ci = r.conf_int().loc[term].tolist()
    return {"b": float(r.params[term]), "ci": [float(ci[0]), float(ci[1])]}


P["divergent"] = 1 - P.endorsed
out["M1_ncond_glm_cluster"] = glm_slope(P[P.y == 1], "endorsed", "zn")
out["M2_words_glm_cluster"] = glm_slope(P[P.y == 0], "divergent", "zw")

# ------------------------------------------------------------------ G2 + SCATTER + M4 pool + LOFO from pairwise_classes_E.jsonl (own code)
fam_of = dict(zip(df.row_key, df.family_vendor))
lines = [json.loads(l) for l in (ROOT / "pairwise_classes_E.jsonl").read_text().splitlines()]
frozen = dict(zip(df.row_key, df.c_score_align))
yP = dict(zip(P.row_key, P.y))
n_cmp = n_mis = 0
si_rows = []
famcounts = {}  # row_key -> {family: [n_rows, n_eq]}
for L in lines:
    node_of, peer_rows = {}, []
    for nd in L["nodes"]:
        for r in nd["rows"]:
            node_of[r["row_key"]] = nd["node_id"]
            if r["is_peer"]:
                peer_rows.append((r["row_key"], r["family"]))
    eq = {(i, j): v for i, j, v, _, _ in L["pairs"]}

    def same(a, b):
        return a == b or eq.get((min(a, b), max(a, b))) is True
    for rk, na in node_of.items():
        own = fam_of[rk]
        pc = [(q, f) for q, f in peer_rows if f != own and q != rk]
        fc = {}
        for q, f in pc:
            v = fc.setdefault(f, [0, 0])
            v[0] += 1
            v[1] += same(na, node_of[q])
        famcounts[rk] = fc
        if frozen.get(rk) is not None and not (isinstance(frozen[rk], float) and np.isnan(frozen[rk])) and len(pc) >= 2:
            c = 1 - sum(v[1] for v in fc.values()) / len(pc)
            n_cmp += 1
            n_mis += abs(c - frozen[rk]) > 1e-9
    # scatter: labelled R_AB scorable rows, cross-family pairs
    rows = [(rk, fam_of[rk], yP[rk], node_of[rk]) for rk in node_of if rk in yP]
    ee, cc = [], []
    for i in range(len(rows)):
        for j in range(i + 1, len(rows)):
            if rows[i][1] == rows[j][1]:
                continue
            s = same(rows[i][3], rows[j][3])
            if rows[i][2] == rows[j][2] == 1:
                ee.append(s)
            elif rows[i][2] == rows[j][2] == 0:
                cc.append(s)
    si_rows.append({"sid": L["sentence_id"], "si_err": np.mean(ee) if ee else np.nan, "si_cor": np.mean(cc) if cc else np.nan})
S = pd.DataFrame(si_rows)
out["G2_mismatch_rate_own"] = n_mis / n_cmp
out["G2_n_compared_own"] = n_cmp
out["SI_err_mean"] = float(S.si_err.mean())
out["SI_cor_mean"] = float(S.si_cor.mean())
both = S.dropna()
out["SI_ratio_same_sentences"] = float(both.si_cor.mean() / both.si_err.mean())


def pool_c(rk, fams, min_rows=1):
    fc = famcounts[rk]
    n = sum(fc[f][0] for f in fams if f in fc)
    return neutral if n < min_rows else 1 - sum(fc[f][1] for f in fams if f in fc) / n


allf = ["cohere", "deepseek", "google", "meta", "microsoft", "mistral", "openai", "qwen"]
full7 = P[P.row_key.map(lambda r: len(famcounts[r]) == 7)]
out["M4_k7_auroc_constant_population"] = roc_auc_score(full7.y, [pool_c(r, allf) for r in full7.row_key])
out["M4_k7_n"] = len(full7)
pool = ["deepseek", "microsoft", "openai"]
out["M4_best3_pool_auroc"] = roc_auc_score(P.y, [pool_c(r, [f for f in pool if f != fam_of[r]]) for r in P.row_key])
full = roc_auc_score(P.y, [pool_c(r, allf, 2) for r in P.row_key])
out["LOFO_delta"] = {f: roc_auc_score(P.y, [pool_c(r, [g for g in allf if g != f], 2) for r in P.row_key]) - full for f in allf}

# ------------------------------------------------------------------ PLACEBOS: the same tests on shuffled labels must FAIL
rng = np.random.default_rng(123)
P["y_shuf"] = rng.permutation(P.y.values)
null = [roc_auc_score(rng.permutation(P.y.values), P.c_score_align) for _ in range(1000)]
out["placebo_auroc_c_shuffled"] = roc_auc_score(P.y_shuf, P.c_score_align)
out["perm_test_auroc_c"] = {"observed": out["auroc_c_graded"], "null_max_of_1000": float(max(null)),
                            "p": float((np.sum(np.array(null) >= out["auroc_c_graded"]) + 1) / 1001)}
out["placebo_NET_shuffled"] = {"delta": net_stat(P, "y_shuf"), "ci": cboot(net_stat, "y_shuf")}
out["placebo_M2_shuffled"] = glm_slope(P[P.y_shuf == 0], "divergent", "zw")
out["placebo_M1_shuffled"] = glm_slope(P[P.y_shuf == 1], "endorsed", "zn")
# scatter placebo: shuffle labels WITHIN sentence (keeps each sentence's error count), recompute SI via the same pairs
P["y_ws"] = P.groupby("sentence_id").y.transform(lambda s: rng.permutation(s.values))
yW = dict(zip(P.row_key, P.y_ws))
pe, pc_ = [], []
for L in lines:
    node_of = {r["row_key"]: nd["node_id"] for nd in L["nodes"] for r in nd["rows"]}
    eq = {(i, j): v for i, j, v, _, _ in L["pairs"]}
    rows = [(rk, fam_of[rk], yW[rk], node_of[rk]) for rk in node_of if rk in yW]
    ee, cc = [], []
    for i in range(len(rows)):
        for j in range(i + 1, len(rows)):
            if rows[i][1] == rows[j][1]:
                continue
            a, b = rows[i][3], rows[j][3]
            s = a == b or eq.get((min(a, b), max(a, b))) is True
            (ee if rows[i][2] == rows[j][2] == 1 else cc if rows[i][2] == rows[j][2] == 0 else []).append(s)
    pe.append(np.mean(ee) if ee else np.nan)
    pc_.append(np.mean(cc) if cc else np.nan)
out["placebo_SI_within_sentence_shuffle"] = {"SI_err": float(np.nanmean(pe)), "SI_cor": float(np.nanmean(pc_))}

# ------------------------------------------------------------------ compare with the artifact's values
hd = {(r["regime"], r["rule"]): r for r in A["cuts_headline"]}[("R_AB", "MAJ")]
cmp = {
    "G1": (out["G1_auroc_frozen_imputed"], A["gates"]["G1"]["auroc_R_AB_pooled"]),
    "e_MAJ": (e, hd["e"]), "d_MAJ": (d, hd["d"]), "auroc_b_MAJ": (out["auroc_b_MAJ_sklearn"], hd["auroc_b"]),
    "auroc_c": (out["auroc_c_graded"], hd["auroc_c"]),
    "NET_words": (out["NET_words_T3_minus_T1"], A["NET"]["R_AB"]["words_T3_minus_T1"]["delta_e_plus_d"]),
    "G2_mismatch": (out["G2_mismatch_rate_own"], A["G2"]["mismatch_rate"]),
    "SI_err": (out["SI_err_mean"], A["SCATTER"]["overall"]["SI_err"]["mean"]),
    "SI_cor": (out["SI_cor_mean"], A["SCATTER"]["overall"]["SI_cor"]["mean"]),
    "SI_ratio": (out["SI_ratio_same_sentences"], A["SCATTER"]["overall"]["ratio_SI_cor_over_SI_err_same_sentences"]["ratio"]),
    "M4_k7": (out["M4_k7_auroc_constant_population"], A["M4"]["random_k_primary"]["k"]["7"]["auroc_mean"]),
    "M4_best3": (out["M4_best3_pool_auroc"], A["M4"]["fixed_pools"]["3"]["in_sample_best"]["auroc"]),
    "LOFO_min": (min(out["LOFO_delta"].values()), A["M4"]["LOFO"]["min_delta"])}
out["comparison"] = {k: {"rederived": float(a), "artifact": float(b), "abs_diff": float(abs(a - b)), "match_1e-9": bool(abs(a - b) < 1e-9)}
                     for k, (a, b) in cmp.items()}
out["placebo_checks_fail_as_expected"] = {
    "auroc_near_0.5": abs(out["placebo_auroc_c_shuffled"] - 0.5) < 0.03,
    "NET_ci_covers_0": out["placebo_NET_shuffled"]["ci"][0] < 0 < out["placebo_NET_shuffled"]["ci"][1],
    "M2_ci_covers_0": out["placebo_M2_shuffled"]["ci"][0] < 0 < out["placebo_M2_shuffled"]["ci"][1],
    "M1_ci_covers_0": out["placebo_M1_shuffled"]["ci"][0] < 0 < out["placebo_M1_shuffled"]["ci"][1],
    "SI_gap_collapses": abs(out["placebo_SI_within_sentence_shuffle"]["SI_cor"] - out["placebo_SI_within_sentence_shuffle"]["SI_err"])
    < 0.5 * (out["SI_cor_mean"] - out["SI_err_mean"])}
(ROOT / "audit" / "rederive.json").write_text(json.dumps(out, indent=1, default=float))
print(json.dumps({k: out[k] for k in ("comparison", "placebo_checks_fail_as_expected", "M1_ncond_glm_cluster", "M2_words_glm_cluster",
                                        "NET_ci_own_bootstrap_B1000", "perm_test_auroc_c", "placebo_SI_within_sentence_shuffle",
                                        "placebo_NET_shuffled", "placebo_M2_shuffled")}, indent=1, default=float))
