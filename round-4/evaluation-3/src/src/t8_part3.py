#!/usr/bin/env python3
"""PART 3: iteration-5 power analysis -> power_E2.json (+ tables/p3_*.csv).

Effect = strat AUROC(c_score_align) - strat AUROC(comparator) on exp-6 R_AB rows (E_POOL PRIMARY, n = 2686). SE(n) from
B = 1000 sentence-subsample bootstraps (sentences drawn with replacement) per cell and n; log SE = a + b log n fit;
MDE80 = 2.80 SE; power = Phi(Delta/SE - 1.96); yield correction from dataset E's built sentence counts."""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from loguru import logger  # noqa: E402
from scipy.stats import norm  # noqa: E402

from t8_paths import DSE, E6T1, E7, RESD, ROOT, jdump, jl, write_csv  # noqa: E402
from stats import WAuc, WStratAuc, auc, strat_auc  # noqa: E402

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(ROOT / "logs" / "part3.log", rotation="30 MB", level="DEBUG")

COMPS = {"flashlite_disg": "judge_cheap_disg", "flashlite_orig": "judge_cheap_orig", "nano_orig": "judge_cheap2_orig"}
NGRID = [40, 60, 80, 100, 125, 150, 200, 250, 300, 400, 500]
BPOW = 1000
Z = norm.ppf(0.975) + norm.ppf(0.80)  # 2.80
Z1 = norm.ppf(0.95) + norm.ppf(0.80)  # 2.49
EFFECTS = [0.05, 0.069, 0.099, 0.10, 0.15]
PLANNED = {"L25": [250, 300, 350, 400], "EXC": [75, 100], "L20": [50], "DT": [100]}


def hm_se(a: float, n1: float, n0: float) -> float:
    q1, q2 = a / (2 - a), 2 * a * a / (1 + a)
    return float(np.sqrt((a * (1 - a) + (n1 - 1) * (q1 - a * a) + (n0 - 1) * (q2 - a * a)) / (n1 * n0)))


def load_rows() -> pd.DataFrame:
    rows = [r for r in jl(E6T1 / "results" / "per_item_T1.jsonl") if r["in_R_AB"] and r["system"] and r.get("pool") == "E_POOL"]
    d = pd.DataFrame([{"sentence_id": r["sentence_id"], "stratum": r["source_stratum"], "y": int(r["y_R_AB"]),
                       "exp5_row_key": r["exp5_row_key"], "c_score_align": r["c_score_align"],
                       **{k: r[v] for k, v in COMPS.items()}} for r in rows])
    return d


def verdict(mde: float, pw069: float) -> str:
    if mde <= 0.10 and pw069 >= 0.5:
        return "ADEQUATE"
    if mde <= 0.15 or pw069 >= 0.3:
        return "MARGINAL"
    return "UNDERPOWERED"


@logger.catch(reraise=True)
def main() -> None:
    R = load_rows()
    logger.info(f"exp-6 R_AB rows {len(R)} ({R.y.sum()}/{(1 - R.y).sum()}), sentences {R.sentence_id.nunique()}")
    if len(R) != 2686:
        # fall back: exclude non-llm pools exactly as the exp-6 table population
        logger.warning(f"R_AB row count {len(R)} != 2686")
    out = {"population": {"n": len(R), "n_err": int(R.y.sum()), "n_cor": int((1 - R.y).sum()), "n_sent": int(R.sentence_id.nunique()),
                          "source": f"{E6T1}/results/per_item_T1.jsonl :: in_R_AB & pool == E_POOL"},
           "comparators": COMPS, "z_two_sided": Z, "z_one_sided": Z1, "B": BPOW, "cells": {}}
    # ---------------- yield (dataset E built counts)
    E = json.loads((DSE / "full_data_out.json").read_text())
    built = defaultdict(set)
    for ds in E["datasets"]:
        if ds["dataset"] != "heldout_candidates":
            continue
        for ex in ds["examples"]:
            sid = ex.get("metadata_sentence_id")
            st = (ex.get("metadata_strata") or {}).get("source_stratum")
            if sid and st:
                built[st].add(sid)
    n_built = {k: len(v) for k, v in built.items()}
    logger.info(f"dataset E built sentences per stratum: {n_built}")
    rng = np.random.default_rng(0)
    yl = {}
    for st in ("L25", "L20", "EXC", "CTRL"):
        used = R[R.stratum == st].sentence_id.nunique()
        nb = n_built.get(st, 0)
        if nb == 0:
            continue
        yb = rng.binomial(nb, used / nb, 2000) / nb
        sub = R[R.stratum == st]
        yl[st] = {"n_built": nb, "n_usable": int(used), "yield": used / nb, "yield_ci": [float(np.percentile(yb, 2.5)), float(np.percentile(yb, 97.5))],
                  "rows_per_usable_sentence": len(sub) / max(used, 1), "correct_share": float(1 - sub.y.mean())}
    out["yield"] = yl
    out["yield_note"] = "yield = #built sentences of the stratum contributing >= 1 R_AB row / #built (dataset E); CI = binomial parametric bootstrap"
    # ---------------- SE(n) per cell
    cells = {"L25": R.stratum == "L25", "L20": R.stratum == "L20", "EXC": R.stratum == "EXC", "CTRL": R.stratum == "CTRL",
             "long": R.stratum.isin(["L25", "L20", "EXC"]), "all": np.ones(len(R), bool)}
    se_rows = []
    for cell, m in cells.items():
        d = R[np.asarray(m)].reset_index(drop=True)
        sids, sidx = np.unique(d.sentence_id.values, return_inverse=True)
        S = len(sids)
        y = d.y.values
        st = d.stratum.values
        f_c = WStratAuc(y, d.c_score_align.values, st)
        f_k = {k: WStratAuc(y, d[k].values, st) for k in COMPS}
        obs = {k: strat_auc(y, d.c_score_align.values, st) - strat_auc(y, d[k].values, st) for k in COMPS}
        rec = {"n_rows": len(d), "n_err": int(y.sum()), "n_cor": int((1 - y).sum()), "n_sent": S, "observed_delta": obs, "se": {}}
        for n in NGRID:
            rs = np.random.default_rng(1000 + n)
            vals = {k: [] for k in COMPS}
            skipped = 0
            for _ in range(BPOW):
                cnt = np.bincount(rs.integers(0, S, n), minlength=S).astype(float)
                w = cnt[sidx]
                if (w * y).sum() == 0 or (w * (1 - y)).sum() == 0:
                    skipped += 1
                    continue
                a = f_c(w)
                for k in COMPS:
                    vals[k].append(a - f_k[k](w))
            for k in COMPS:
                v = np.array(vals[k])
                v = v[np.isfinite(v)]
                se_rows.append({"cell": cell, "comparator": k, "n_sent": n, "se": float(v.std(ddof=1)), "mean_delta": float(v.mean()),
                                "n_boot": len(v), "n_skipped_one_class": skipped})
        out["cells"][cell] = rec
        logger.info(f"cell {cell}: {rec['n_rows']} rows, {S} sent, obs Δ {obs['flashlite_disg']:.3f}")
    SE = pd.DataFrame(se_rows)
    fits = {}
    for (cell, k), g in SE.groupby(["cell", "comparator"]):
        b, a = np.polyfit(np.log(g.n_sent), np.log(g.se), 1)
        fits[f"{cell}|{k}"] = {"a": float(a), "b": float(b)}
        for mde in (0.069, 0.10):
            fits[f"{cell}|{k}"][f"n_for_mde_{mde}"] = float((mde / Z / np.exp(a)) ** (1 / b))
    out["se_fit"] = fits
    SE["mde80"] = Z * SE.se
    SE["mde80_one_sided"] = Z1 * SE.se
    for eff in EFFECTS:
        SE[f"power_at_{eff}"] = norm.cdf(eff / SE.se - norm.ppf(0.975))
    write_csv(SE, "p3_se_grid.csv", [f"{E6T1}/results/per_item_T1.jsonl :: c_score_align, judge_cheap_disg, judge_cheap_orig, judge_cheap2_orig, y_R_AB"])

    def se_at(cell, k, n):
        f = fits[f"{cell}|{k}"]
        return float(np.exp(f["a"]) * n ** f["b"])
    # ---------------- planned E2 cells
    plan = []
    for cell, ns in PLANNED.items():
        yields = ([("CTRL_yield", yl["CTRL"]["yield"], yl["CTRL"]["yield_ci"])] + [(f"y{v}", v, [v, v]) for v in (0.3, 0.5, 0.8)]) \
            if cell == "DT" else [("E_yield", yl[cell]["yield"], yl[cell]["yield_ci"])]
        se_cell = "all" if cell == "DT" else cell
        for n_plan in ns:
            for ylab, yv, yci in yields:
                for k in COMPS:
                    nu = n_plan * yv
                    se = se_at(se_cell, k, nu)
                    se_lo, se_hi = se_at(se_cell, k, n_plan * yci[1]), se_at(se_cell, k, n_plan * yci[0])
                    rec = {"cell": cell, "planned_sentences": n_plan, "yield_scenario": ylab, "yield": yv, "n_usable": nu,
                           "comparator": k, "se_model_cell": se_cell, "se": se, "mde80": Z * se, "mde80_yield_band": [Z * se_lo, Z * se_hi],
                           "mde80_one_sided": Z1 * se, **{f"power_at_{e}": float(norm.cdf(e / se - norm.ppf(0.975))) for e in EFFECTS}}
                    # label-mix sensitivity (Hanley-McNeil SE ratio, CORRECT share x0.5 / x1.5)
                    if se_cell in yl or se_cell == "all":
                        base = yl.get(se_cell) or {"rows_per_usable_sentence": len(R) / R.sentence_id.nunique(), "correct_share": float(1 - R.y.mean())}
                        nr = nu * base["rows_per_usable_sentence"]
                        a0 = out["cells"][se_cell]["observed_delta"]
                        acc = auc(R[np.asarray(cells[se_cell])].y, R[np.asarray(cells[se_cell])].c_score_align)
                        cs = base["correct_share"]
                        s0 = hm_se(acc, nr * (1 - cs), nr * cs)
                        for lab, f in (("cor_x0.5", 0.5), ("cor_x1.5", 1.5)):
                            c2 = min(0.95, cs * f)
                            rec[f"mde80_labelmix_{lab}"] = Z * se * hm_se(acc, nr * (1 - c2), nr * c2) / s0
                    rec["verdict"] = verdict(rec["mde80"], rec["power_at_0.069"])
                    plan.append(rec)
    PL = pd.DataFrame(plan)
    PL["mde80_yield_lo"] = PL.mde80_yield_band.apply(lambda v: v[0])
    PL["mde80_yield_hi"] = PL.mde80_yield_band.apply(lambda v: v[1])
    write_csv(PL.drop(columns=["mde80_yield_band"]), "p3_planned_E2.csv",
              [f"{E6T1}/results/per_item_T1.jsonl :: SE(n) fit", f"{DSE}/full_data_out.json :: built sentences per stratum (yield)"])
    out["planned_E2"] = plan
    # n needed for the observed L25 effect
    out["n_needed"] = {cell: {k: {"usable_for_mde_0.069": fits[f"{cell}|{k}"]["n_for_mde_0.069"],
                                  "usable_for_mde_0.10": fits[f"{cell}|{k}"]["n_for_mde_0.1"],
                                  "planned_for_mde_0.069": fits[f"{cell}|{k}"]["n_for_mde_0.069"] / yl[cell]["yield"] if cell in yl else None,
                                  "planned_for_mde_0.10": fits[f"{cell}|{k}"]["n_for_mde_0.1"] / yl[cell]["yield"] if cell in yl else None}
                             for k in COMPS} for cell in ("L25", "L20", "EXC", "long")}
    # ---------------- criterion (c) effect assumptions
    p1 = json.loads((RESD / "part1.json").read_text()) if (RESD / "part1.json").exists() else None
    eff = {"conservative": {"value": 0.069, "what": "observed E L25 pooled Delta c_score_align - flash-lite disguised (exp 6 tables_T1.md)"}}
    if p1 is not None:
        P = pd.read_pickle(RESD / "part1_rows.pkl")
        j = P[P.stratum == "L25"].merge(R[["exp5_row_key", "flashlite_disg"]], left_on="row_key", right_on="exp5_row_key", how="inner")
        ok = j.c_vres_9fam.notna() & j.flashlite_disg.notna()
        j = j[ok]
        eff["optimistic"] = {"value": float(auc(j.y_AB, j.c_vres_9fam) - auc(j.y_AB, j.flashlite_disg)),
                             "value_3pool": float(auc(j.y_AB, j.c_vres_3pool.fillna(0.5)) - auc(j.y_AB, j.flashlite_disg)),
                             "n": int(len(j)), "what": "Part-1 graded c_vres (label-free liberal-vocabulary counterfactual) - flash-lite disguised on E L25 consensus-scorable rows"}
    out["criterion_c_effects"] = eff
    # ---------------- R_COMP FREE scenarios
    rc = [r for r in jl(E7 / "results" / "rcomp_candidates.jsonl")]
    free = pd.DataFrame([r for r in rc if r["condition"] == "FREE" and r["label"] in ("CORRECT", "ERROR")])
    sig = pd.DataFrame([r for r in rc if r["condition"] == "SIG" and r["label"] in ("CORRECT", "ERROR")])
    free["y"] = (free.label == "ERROR").astype(int)
    sig["y"] = (sig.label == "ERROR").astype(int)
    fz = free.dropna(subset=["c_score_align", "judge_cheap_disg"])
    r_scores = float(np.corrcoef(fz.c_score_align, fz.judge_cheap_disg)[0, 1])
    sz = sig.dropna(subset=["c_score_align"])
    res = sz.c_score_align - sz.groupby("y").c_score_align.transform("mean")
    g = pd.DataFrame({"s": sz.sentence_id.values, "r": res.values})
    k_ = g.groupby("s").r.agg(["mean", "count", "var"])
    msb = (k_["count"] * (k_["mean"] - g.r.mean()) ** 2).sum() / (len(k_) - 1)
    msw = (k_["var"].fillna(0) * (k_["count"] - 1)).sum() / (len(g) - len(k_))
    m0 = k_["count"].mean()
    icc = float(max(0.0, (msb - msw) / (msb + (m0 - 1) * msw)))
    scen = []
    sig_ok = sig.dropna(subset=["c_score_align", "judge_cheap_disg"]).reset_index(drop=True)
    sids = sig_ok.sentence_id.unique()
    rs = np.random.default_rng(7)
    for ne in (420, 600, 900):
        for nc in (34, 100, 200, 400, 800):
            m = (ne + nc) / 221
            deff = 1 + (m - 1) * icc
            v1, v2 = hm_se(0.80, ne, nc) ** 2, hm_se(0.58, ne, nc) ** 2
            var_d = (v1 + v2 - 2 * r_scores * np.sqrt(v1 * v2)) * deff
            # empirical: sentence-cluster resampling of SIG rows, then class-count resampling to the target counts
            ds = []
            for _ in range(300):
                pick = rs.choice(sids, len(sids), replace=True)
                sub = sig_ok.set_index("sentence_id").loc[pick].reset_index()
                e_ = sub[sub.y == 1].sample(ne, replace=True, random_state=int(rs.integers(1 << 30)))
                c_ = sub[sub.y == 0].sample(nc, replace=True, random_state=int(rs.integers(1 << 30)))
                s = pd.concat([e_, c_])
                ds.append(auc(s.y, s.c_score_align) - auc(s.y, s.judge_cheap_disg))
            scen.append({"n_err": ne, "n_cor": nc, "n_sent": 221, "rows_per_sentence": m, "design_effect": deff,
                         "mde80_analytic": float(Z * np.sqrt(var_d)), "mde80_empirical_SIG": float(Z * np.std(ds, ddof=1)),
                         "sig_delta_mean": float(np.mean(ds))})
    SC = pd.DataFrame(scen)
    write_csv(SC, "p3_rcomp_free_scenarios.csv", [f"{E7}/results/rcomp_candidates.jsonl :: FREE tier-A (454 rows) correlation, SIG c_score_align residual ICC, SIG resampling"])
    out["rcomp_free"] = {"score_correlation_FREE_tierA": r_scores, "n_FREE_tierA": int(len(fz)), "icc_SIG_residual": icc,
                         "auroc_assumed": {"c_align_FREE_tierA": 0.80, "judge": 0.58},
                         "observed_FREE_tierA": {"auroc_c_align": auc(fz.y, fz.c_score_align), "auroc_judge_cheap_disg": auc(fz.y, fz.judge_cheap_disg)},
                         "scenarios": scen,
                         "caveat": "order-of-magnitude guide only: analytic Hanley-McNeil + SIG-row resampling as an upper-variance proxy; no FREE-labelled data at these counts exist"}
    # ---------------- recommendation
    L = PL[(PL.cell == "L25") & (PL.comparator == "flashlite_disg")]
    rec_txt = []
    for _, r in L.iterrows():
        rec_txt.append(f"L25 planned {r.planned_sentences} -> ~{r.n_usable:.0f} usable: MDE80 {r.mde80:.3f}, power@0.069 {r['power_at_0.069']:.2f} => {r.verdict}")
    nn = out["n_needed"]["L25"]["flashlite_disg"]
    rec_txt.append(f"To detect +0.069 on L25 at 80% power: ~{nn['usable_for_mde_0.069']:.0f} usable sentences = ~{nn['planned_for_mde_0.069']:.0f} planned at E's yield; "
                   f"for MDE 0.10: ~{nn['usable_for_mde_0.10']:.0f} usable = ~{nn['planned_for_mde_0.10']:.0f} planned.")
    lp = out["n_needed"]["long"]["flashlite_disg"]
    rec_txt.append(f"Long pool (L25+L20+EXC) needs ~{lp['usable_for_mde_0.069']:.0f} usable sentences for MDE 0.069: pre-declaring the long pool as criterion (c)'s primary cell is the cheaper route.")
    out["recommendation"] = rec_txt
    jdump(ROOT / "power_E2.json", out)
    for t in rec_txt:
        logger.info(t)


if __name__ == "__main__":
    main()
