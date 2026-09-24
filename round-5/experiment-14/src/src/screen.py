#!/usr/bin/env python3
"""A4/A5 (post-seal label join): AUROC + sentence-cluster CIs per variant and cell, paired Δ vs V0 (frozen), context Δ vs the
cheap API judges, binary e/d (c > 0.5; V4 flag-rate matched to V0) overall / per words tercile / LONG / L25 / CTRL / per T9
class, the key diagnostic (Δd, Δe on T3 and L25), NET Δ(e+d) T3 - T1, post-seal reproduction checks, and the eval-3
R_oracle bound with the oracle-gap share. Writes results/screen_E.json and tables/*.csv."""
from __future__ import annotations

import json
import sys
import time

import numpy as np
import pandas as pd

from common import FREEZE, LONG, RES, ROOT, SEED, TAB, B, jdump, setup_logger
from labels import T9, frame
from stats import SentBoot, WAuc, WStratAuc, auroc, boot_ci, strat_auroc

logger = setup_logger("screen")
VARIANTS = ["V1", "V2", "V3", "V4", "V5"]
SCORES = ["V0_frozen", "V0_rep", "c_exact"] + VARIANTS
JUDGES = ["judge_cheap_disg", "judge_cheap_orig", "judge_cheap2_orig"]
CELLS = {"ALL-strat": (None, "strat"), "pooled": (None, "pooled"), "LONG-strat": (LONG, "strat"),
         "L25": (("L25",), "pooled"), "L20": (("L20",), "pooled"), "EXC": (("EXC",), "pooled"), "CTRL": (("CTRL",), "pooled")}


def flags(df: pd.DataFrame, P: pd.DataFrame) -> dict:
    """Binary flag per score: c > 0.5; V4 at the threshold matching V0's flag rate on Z (ties broken by row order)."""
    out = {s: (P[s].astype(float).values > 0.5) for s in SCORES if s != "V4"}
    rate = out["V0_frozen"].mean()
    v = P["V4"].astype(float).values
    thr = float(np.quantile(v, 1 - rate, method="higher"))
    f4 = v > thr
    if abs(f4.mean() - rate) > 0.01:  # step ties: take the top-k by score (stable by row order)
        k = int(round(rate * len(v)))
        o = np.argsort(-v, kind="stable")
        f4 = np.zeros(len(v), bool)
        f4[o[:k]] = True
    out["V4"] = f4
    out["_V4_threshold"] = thr
    out["_V0_flag_rate"] = float(rate)
    return out


def auc_block(y, s, st, W, stat):
    pt = strat_auroc(y, s, st) if stat == "strat" else auroc(y, s)
    f = WStratAuc(y, s, st) if stat == "strat" else WAuc(y, s)
    bs = np.array([f(w) for w in W])
    return pt, bs


def ed_block(y, fl, W) -> dict:
    y = np.asarray(y, int)
    endorsed = ~fl
    e = float(endorsed[y == 1].mean()) if (y == 1).any() else None
    d = float(fl[y == 0].mean()) if (y == 0).any() else None
    with np.errstate(invalid="ignore", divide="ignore"):
        eb = (W @ (endorsed & (y == 1)).astype(float)) / (W @ (y == 1).astype(float))
        db = (W @ (fl & (y == 0)).astype(float)) / (W @ (y == 0).astype(float))
    return {"e": e, "d": d, "e_ci": boot_ci(eb), "d_ci": boot_ci(db), "n_err": int((y == 1).sum()), "n_cor": int((y == 0).sum()),
            "auroc_b": (1 - (e + d) / 2) if e is not None and d is not None else None, "_eb": eb, "_db": db}


@logger.catch(reraise=True)
def main():
    t0 = time.time()
    df = frame()
    P = df[df.Z].reset_index(drop=True)
    P["V0_frozen"] = P.V0_frozen.astype(float)
    y = P.y.values.astype(int)
    st = P.stratum.values
    boot = SentBoot(P.sentence_id.values, b=B, seed=SEED)
    Wf = boot.W()
    A = {"population": {"Z": {"n": len(P), "n_error": int(y.sum()), "n_correct": int((1 - y).sum()), "n_sentences": int(P.sentence_id.nunique())},
                        "R_AB": {"n": int(df.R_AB.sum()), "n_error": int(df[df.R_AB].y.sum()), "n_sentences": int(df[df.R_AB].sentence_id.nunique())},
                        "R_AB_not_in_Z": df[df.R_AB & ~df.Z][["row_key", "stratum", "n_peers", "coverage_status"]].to_dict("records")},
         "B": B, "seed": SEED}
    assert len(P) == 2672, len(P)
    # ---------------- post-seal reproduction checks
    A["repro"] = {"c_exact_pooled_auroc_Z": auroc(y, P.c_exact.values), "target_c_exact": 0.748,
                  "c3_plain_pooled_auroc_Z": auroc(y, P.c3_plain.values), "target_c3_eval2_c_k3_best_oof": 0.784520131776288,
                  "V0_frozen_pooled_Z": auroc(y, P.V0_frozen.values), "V0_rep_pooled_Z": auroc(y, P.V0_rep.values),
                  "V0_frozen_strat_full_RAB_2686": strat_auroc(df[df.R_AB].y.values.astype(int), df[df.R_AB].V0_frozen.astype(float).values, df[df.R_AB].stratum.values),
                  "n_V5_imputed_neutral_in_Z": int(P.V5_imputed.fillna(False).sum())}
    A["repro"]["c_exact_pass"] = abs(A["repro"]["c_exact_pooled_auroc_Z"] - 0.748) < 0.0015
    A["repro"]["c3_pass"] = abs(A["repro"]["c3_plain_pooled_auroc_Z"] - 0.784520131776288) < 0.0015
    logger.info(f"repro {json.dumps(A['repro'])}")
    # ---------------- AUROC per cell
    A["auroc"], A["delta_vs_V0"], A["delta_vs_judges"] = {}, {}, {}
    rows_auc, rows_d = [], []
    for cname, (strata, stat) in CELLS.items():
        m = np.ones(len(P), bool) if strata is None else np.isin(st, strata)
        W = Wf[:, m]
        ser = {}
        for s in SCORES + JUDGES:
            v = P[s].astype(float).values[m]
            if np.isnan(v).any():
                logger.warning(f"{s} has {np.isnan(v).sum()} NaN in {cname}")
                continue
            ser[s] = auc_block(y[m], v, st[m], W, stat)
        A["auroc"][cname] = {s: {"auroc": pt, "ci": boot_ci(bs), "n": int(m.sum()), "n_err": int(y[m].sum()), "n_cor": int((1 - y[m]).sum()),
                                 "n_sent": int(P.sentence_id[m].nunique())} for s, (pt, bs) in ser.items()}
        A["delta_vs_V0"][cname] = {}
        for s in ["V0_rep", "c_exact"] + VARIANTS:
            d = ser[s][1] - ser["V0_frozen"][1]
            A["delta_vs_V0"][cname][s] = {"delta": ser[s][0] - ser["V0_frozen"][0], "ci": boot_ci(d), "se": float(np.nanstd(d)),
                                          "p_one_sided_le0": float(np.nanmean(d <= 0))}
            rows_d.append({"cell": cname, "variant": s, **A["delta_vs_V0"][cname][s]})
        A["delta_vs_judges"][cname] = {}
        for s in ["V0_frozen"] + VARIANTS:
            for j in JUDGES:
                d = ser[s][1] - ser[j][1]
                A["delta_vs_judges"][cname][f"{s} - {j}"] = {"delta": ser[s][0] - ser[j][0], "ci": boot_ci(d)}
        for s, (pt, bs) in ser.items():
            rows_auc.append({"cell": cname, "stat": stat, "score": s, "auroc": pt, "ci_lo": boot_ci(bs)[0], "ci_hi": boot_ci(bs)[1], "n": int(m.sum())})
        logger.info(f"{cname}: " + " ".join(f"{s}={ser[s][0]:.4f}" for s in SCORES))
    # ---------------- e/d
    FL = flags(df, P)
    A["binary"] = {"V4_threshold_flag_rate_matched": FL["_V4_threshold"], "V0_flag_rate": FL["_V0_flag_rate"],
                   "flag_rates": {s: float(FL[s].mean()) for s in SCORES}}
    cuts = {"ALL": np.ones(len(P), bool), "LONG": P.long.values, "L25": st == "L25", "L20": st == "L20", "EXC": st == "EXC", "CTRL": st == "CTRL",
            "words_T1": P.words_t.values == "T1", "words_T2": P.words_t.values == "T2", "words_T3": P.words_t.values == "T3"}
    ED, rows_ed = {}, []
    for c, m in cuts.items():
        ED[c] = {}
        for s in SCORES:
            r = ed_block(y[m], FL[s][m], Wf[:, m])
            ED[c][s] = r
            rows_ed.append({"cut": c, "score": s, **{k: v for k, v in r.items() if not k.startswith("_")}})
    # key diagnostic: Δd, Δe vs V0 on T3 and L25 (+ LONG, ALL)
    A["key_diagnostic"] = {}
    for c in ("words_T3", "L25", "LONG", "ALL", "CTRL"):
        A["key_diagnostic"][c] = {}
        for s in ["c_exact"] + VARIANTS:
            a, b = ED[c][s], ED[c]["V0_frozen"]
            A["key_diagnostic"][c][s] = {"d": a["d"], "e": a["e"], "d_V0": b["d"], "e_V0": b["e"],
                                         "delta_d": a["d"] - b["d"], "delta_d_ci": boot_ci(a["_db"] - b["_db"]),
                                         "delta_e": a["e"] - b["e"], "delta_e_ci": boot_ci(a["_eb"] - b["_eb"]),
                                         "d_falls_without_e_rising": bool(boot_ci(a["_db"] - b["_db"])[1] < 0 and boot_ci(a["_eb"] - b["_eb"])[0] <= 0)}
    # NET Δ(e+d) T3 - T1 (eval-2 definition)
    A["NET_T3_minus_T1"] = {}
    for s in SCORES:
        t3, t1 = ED["words_T3"][s], ED["words_T1"][s]
        net = (t3["e"] + t3["d"]) - (t1["e"] + t1["d"])
        nb = (t3["_eb"] + t3["_db"]) - (t1["_eb"] + t1["_db"])
        A["NET_T3_minus_T1"][s] = {"net": net, "ci": boot_ci(nb), "delta_e": t3["e"] - t1["e"], "delta_d": t3["d"] - t1["d"]}
    # per T9 class e (ERROR rows of the class) and d reference
    A["t9_e"] = {}
    rows_t9 = []
    for cl in T9:
        m = np.array([cl in x for x in P.t9])
        A["t9_e"][cl] = {"n": int(m.sum())}
        for s in SCORES:
            if m.sum() == 0:
                continue
            en = ~FL[s][m]
            eb = (Wf[:, m] @ en.astype(float)) / Wf[:, m].sum(1)
            A["t9_e"][cl][s] = {"e": float(en.mean()), "e_ci": boot_ci(eb)}
            rows_t9.append({"class": cl, "score": s, "n": int(m.sum()), "e": float(en.mean()), "e_ci_lo": boot_ci(eb)[0], "e_ci_hi": boot_ci(eb)[1]})
    A["ed"] = {c: {s: {k: v for k, v in r.items() if not k.startswith("_")} for s, r in d.items()} for c, d in ED.items()}
    # ---------------- oracle bound (A5)
    A["oracle"] = oracle(df, P, FL, Wf)
    A["runtime_s"] = time.time() - t0
    jdump(A, RES / "screen_E.json")
    for name, rows in (("screen_auroc", rows_auc), ("screen_delta_vs_V0", rows_d), ("screen_ed", rows_ed), ("screen_t9_e", rows_t9)):
        _csv(pd.DataFrame(rows), TAB / f"{name}.csv", f"results/screen_E.json :: src/screen.py main() [{name}]")
    logger.info(f"screen done {time.time() - t0:.0f}s")


def oracle(df: pd.DataFrame, P: pd.DataFrame, FL: dict, Wf) -> dict:
    """eval-3 t8_part1.py endorse_det R_oracle, reimplemented on the matrix: for candidate x and each LOFO peer row p,
    agree = (y_p == 0) if x CORRECT else (y_p == 1 and op_class(p) == op_class(x)); unlabelled peers never agree;
    endorsed iff #agree > n/2. d_oracle = share of CORRECT candidates not endorsed. 9-family = full LOFO pool; 3-pool =
    {deepseek, microsoft, openai} minus own family (rows with >= 1 pool peer)."""
    sys.path.insert(0, str(FREEZE))
    import consensus_variants as CV
    from common import MATRIX, jl
    IX = {r["sentence_id"]: CV.build_index(r) for r in jl(MATRIX)}
    lab = {rk: (int(y) if r else None) for rk, y, r in zip(df.row_key, df.y, df.R_AB)}
    opc = dict(zip(df.row_key, df.opc))
    res = {}
    y = P.y.values.astype(int)
    for pool, fams in (("9fam", None), ("3pool", CV.POOL3)):
        endorsed = np.full(len(P), np.nan)
        for i, (rk, sid) in enumerate(zip(P.row_key, P.sentence_id)):
            ix = IX[sid]
            peers = CV.peers_lofo(ix, rk, families=fams)
            if not peers:
                continue
            k = 0
            for p in peers:
                yp = lab.get(p)
                if y[i] == 0:
                    k += yp == 0
                else:
                    k += (yp == 1) and opc.get(p) == opc.get(rk)
            endorsed[i] = float(k > len(peers) / 2)
        ok = ~np.isnan(endorsed)
        out = {}
        for c, m in (("ALL", ok), ("L25", ok & (P.stratum.values == "L25")), ("LONG", ok & P.long.values), ("words_T3", ok & (P.words_t.values == "T3"))):
            cor = m & (y == 0)
            d_or = float((endorsed[cor] == 0).mean())
            rec = {"n_cor": int(cor.sum()), "d_oracle": d_or}
            # END_MAJ on the same pool (plain c): rows' c on this pool > 0.5 == not endorsed
            col = "V0_rep" if pool == "9fam" else "c3_plain"
            rec[f"d_END_MAJ_{pool}"] = float((P[col].values[cor] >= 0.5).mean())
            rows = {}
            for s in (["V0_frozen", "V1", "V2", "V3", "V4"] if pool == "9fam" else ["V5"]):
                d_v = float(FL[s][cor].mean())
                e_v = float((~FL[s][m & (y == 1)]).mean())
                d_ref = float(FL["V0_frozen"][cor].mean())
                den = d_ref - d_or
                rows[s] = {"d_v": d_v, "e_v": e_v, "d_V0": d_ref, "denominator": den,
                           "gap_closed": ((d_ref - d_v) / den) if den >= 0.05 else "ILL_CONDITIONED"}
            rec["variants"] = rows
            out[c] = rec
        res[pool] = out
    res["targets_eval3"] = {"3pool_ALL_d_oracle": 0.38542890716803757, "3pool_L25_d_oracle": 0.5421686746987953,
                            "3pool_L25_END_MAJ": 0.7349397590361446, "9fam_ALL_d_oracle": 0.58584686774942}
    res["repro_pass"] = bool(abs(res["3pool"]["ALL"]["d_oracle"] - 0.38542890716803757) < 0.002
                             and abs(res["3pool"]["L25"]["d_oracle"] - 0.5421686746987953) < 0.002)
    logger.info(f"oracle 3pool ALL {res['3pool']['ALL']['d_oracle']:.4f} L25 {res['3pool']['L25']['d_oracle']:.4f} "
                f"END_MAJ L25 {res['3pool']['L25']['d_END_MAJ_3pool']:.4f}; 9fam ALL {res['9fam']['ALL']['d_oracle']:.4f}")
    return res


def _csv(d: pd.DataFrame, p, source: str):
    with open(p, "w") as fh:
        fh.write(f"# source: {source}\n")
        d.to_csv(fh, index=False)


if __name__ == "__main__":
    main()
