"""STEP G: label-joined analyses (after results/scores_labelblind.jsonl is hashed into prereg_csc_E_addendum.json).

Populations (fixed in prereg_csc_E_addendum1.json before scoring): PRIMARY = R_AB rows whose 3 CSC-OWN peer calls
completed (the paid sweep was stopped by the platform's phase budget), GE2 / MINI200 sensitivities, FULL = all 2,686 R_AB
rows for the $0 analyses (FREE-MATCHED exact vs ALIGN, vocabulary decomposition of free-peer divergence).
Every comparison is paired on identical rows; sentence-cluster bootstrap B = 2000, seed 0 (eval 2 SentBoot)."""
from __future__ import annotations

import hashlib
import json
import math
import multiprocessing as mp
import os
import sys
import time
import warnings
from collections import Counter, defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import numpy as np
import pandas as pd
from loguru import logger
from scipy.stats import kendalltau
from sklearn.metrics import average_precision_score

SRC = Path(__file__).resolve().parent
ROOT = SRC.parent
sys.path.insert(0, str(ROOT / "vendor" / "ev2"))
sys.path.insert(0, str(ROOT / "vendor"))
sys.path.insert(0, str(SRC))
from mechanism import ed_decomposition, gee_fit, make_bins, net_test, prereg_cuts, zcols  # noqa: E402
from stats import SentBoot, WAuc, WStratAuc, auc, ci, strat_auc  # noqa: E402

warnings.filterwarnings("ignore")
RES = ROOT / "results"
DATA = ROOT / "data"
RUN = Path("/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop")
B = 2000
MIN_CELL = 50
COMPARATORS = ["c_free_exact", "c_free_align", "c_free_graded", "T1__c_score_align", "T1__p_peer_text", "T1__judge_cheap_disg",
               "T1__judge_cheap_orig", "T1__judge_cheap2_orig", "T1__judge_cheap2_disg", "T1__rt_nli_min", "T1__sc5_eq_frac",
               "T1__S4_full_oof", "T1__l2_bow", "T1__g_score", "T1__nf_c_score"]
VARIANTS = ["c_csc", "c_csc_graded", "c_csc_multi", "HYB_MEAN", "HYB_MAX"]
PRETTY = {"T1__c_score_align": "c_score_align (9 free peers, ALIGN)", "T1__p_peer_text": "p_peer_text", "T1__judge_cheap_disg": "flash-lite judge (disguised)",
          "T1__judge_cheap_orig": "flash-lite judge (original)", "T1__judge_cheap2_orig": "gpt-4.1-nano judge (original)",
          "T1__judge_cheap2_disg": "gpt-4.1-nano judge (disguised)", "T1__rt_nli_min": "round-trip NLI (min)", "T1__sc5_eq_frac": "self-consistency sc5",
          "T1__S4_full_oof": "S4_full stack (OOF)", "T1__l2_bow": "l2_bow", "T1__g_score": "g_score (graded free)", "T1__nf_c_score": "nf_c_score",
          "c_free_exact": "FREE-MATCHED exact (same 3 families, no signature)", "c_free_align": "FREE-MATCHED ALIGN", "c_free_graded": "FREE-MATCHED graded (identity)",
          "c_csc": "CSC c_csc", "c_csc_graded": "CSC c_csc_graded", "c_csc_multi": "CSC c_csc_multi", "HYB_MEAN": "HYB_MEAN", "HYB_MAX": "HYB_MAX",
          "T1__judge_strong_orig": "frontier judge (original)"}


def jl(p: Path) -> list[dict]:
    return [json.loads(l) for l in Path(p).read_text().splitlines() if l.strip()]


def jdump(o, p: Path) -> None:
    def conv(x):
        if isinstance(x, (np.integer,)):
            return int(x)
        if isinstance(x, (np.floating,)):
            return None if np.isnan(x) else float(x)
        if isinstance(x, np.ndarray):
            return x.tolist()
        if isinstance(x, float) and math.isnan(x):
            return None
        return str(x)
    Path(p).write_text(json.dumps(o, indent=1, default=conv, ensure_ascii=False, allow_nan=False) if False else
                       json.dumps(_clean(o), indent=1, default=conv, ensure_ascii=False))


def _clean(o):
    if isinstance(o, dict):
        return {str(k): _clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_clean(v) for v in o]
    if isinstance(o, float) and (math.isnan(o) or math.isinf(o)):
        return None
    if isinstance(o, np.floating):
        v = float(o)
        return None if (math.isnan(v) or math.isinf(v)) else v
    if isinstance(o, np.integer):
        return int(o)
    if isinstance(o, np.bool_):
        return bool(o)
    return o


# =================================================================================================== frame
def guard() -> dict:
    add = json.loads((ROOT / "prereg_csc_E_addendum.json").read_text())
    p = RES / "scores_labelblind.jsonl"
    sha = hashlib.sha256(p.read_bytes()).hexdigest()
    assert sha == add["scores_labelblind_sha256"], "label-blind score table changed after hashing"
    a1 = ROOT / "prereg_csc_E_addendum1.json"
    assert a1.stat().st_mtime < p.stat().st_mtime, "addendum1 must predate the score table"
    return {"scores_sha256": sha, "prereg_sha256": (ROOT / "prereg_csc_E.sha256").read_text().split()[0],
            "addendum1_sha256": (ROOT / "prereg_csc_E_addendum1.sha256").read_text().split()[0],
            "order_ok": (ROOT / "prereg_csc_E.json").stat().st_mtime < a1.stat().st_mtime < p.stat().st_mtime,
            "analysis_start_ts": time.time()}


def build_frame() -> tuple[pd.DataFrame, dict]:
    F = pd.DataFrame(jl(DATA / "frame_blind.jsonl"))
    L = pd.DataFrame(jl(DATA / "labels_RAB.jsonl"))
    P = F.merge(L, on="row_key", how="left", validate="1:1")
    S = defaultdict(dict)
    for r in jl(RES / "scores_labelblind.jsonl"):
        S[r["arm"]][r["row_key"]] = r
    sal = json.loads((RES / "salvage_rows.json").read_text())

    def col(arm, key, default=np.nan):
        return [S[arm].get(rk, {}).get(key, default) if S[arm].get(rk, {}).get(key) is not None else default for rk in P.row_key]
    for key in ("c_csc", "c_csc_graded", "c_csc_multi", "n_usable", "n_unknown", "z3_cpu_s", "peer_pair_agree", "n_missing_calls"):
        P[("" if key.startswith("c_csc") else "own_") + key] = col("OWN", key)
    P["own_status"] = col("OWN", "status", "NA")
    P["own_majority"] = col("OWN", "peer_majority_fol", None)
    P["c_free_exact"] = col("FREE", "c_csc")
    P["c_free_graded"] = col("FREE", "c_csc_graded")
    P["c_free_multi"] = col("FREE", "c_csc_multi")
    P["c_free_align"] = col("FREE", "c_free_align")
    P["free_status"] = col("FREE", "status", "NA")
    P["free_align_status"] = col("FREE", "free_align_status", "NA")
    P["free_n_usable"] = col("FREE", "n_usable")
    P["free_ppa"] = col("FREE", "peer_pair_agree")
    P["free_majority"] = col("FREE", "peer_majority_fol", None)
    for arm, pre in (("K4", "c_k4"), ("OTHER", "c_other")):
        P[pre] = col(arm, "c_csc")
        P[pre + "_graded"] = col(arm, "c_csc_graded")
        P[pre + "_missing"] = col(arm, "n_missing_calls")
    P["c_other_align"] = col("OTHER", "c_align")
    P["c_align9_base"] = col("ALIGN9_BASE", "c_align9")
    P["c_align9_syn"] = col("ALIGN9_SYN", "c_align9")
    P["HYB_MEAN"] = (P.c_csc + P.T1__c_score_align) / 2
    P["HYB_MAX"] = np.maximum(P.c_csc, P.T1__c_score_align)
    P["y"] = P.y.astype(int)
    P["PRIMARY"] = P.row_key.isin(set(sal["PRIMARY"]))
    P["GE2"] = P.row_key.isin(set(sal["GE2"]))
    P["MINI200"] = P.row_key.isin(set(sal["MINI200"])) & P.PRIMARY
    P["stratum"] = P.stratum.astype(str)
    cuts = prereg_cuts(P)
    P = make_bins(P, cuts)
    P["nq_bin"] = np.where(P.n_quant <= 1, "0-1", np.where(P.n_quant == 2, "2", "3+"))
    P["depth_bin"] = np.where(P.depth <= 1, "0-1", np.where(P.depth == 2, "2", "3+"))
    P["in_RAB"] = True
    P["y_AB"] = P.y
    P["long"] = P.stratum.isin(["L25", "L20", "EXC"])
    # binary endorsement (flag = c > 0.5); END_MAJ-9 follows eval 2 (endorsed iff c_score_align < 0.5)
    for c in ("c_csc", "c_csc_graded", "c_csc_multi", "c_free_exact", "c_free_align", "c_free_graded", "HYB_MEAN", "HYB_MAX", "c_k4", "c_other", "c_other_align"):
        P["en_" + c] = np.where(P[c].isna(), np.nan, (P[c] <= 0.5).astype(float))
    P["en_END_MAJ9"] = (P.T1__c_score_align < 0.5).astype(float)
    return P, cuts


# =================================================================================================== metric helpers
class Cell:
    def __init__(self, name: str, P: pd.DataFrame, mask: np.ndarray, boot: SentBoot):
        self.name = name
        self.mask = np.asarray(mask, bool)
        self.P = P
        self.d = P[self.mask]
        self.y = self.d.y.values.astype(int)
        self.st = self.d.stratum.values
        self.W = boot.W(self.mask)
        self.n_err, self.n_cor = int(self.y.sum()), int((1 - self.y).sum())
        self.read = self.n_err >= MIN_CELL and self.n_cor >= MIN_CELL

    def _s(self, col):
        return self.d[col].values.astype(float)

    def metric(self, col: str, kind: str = "strat") -> dict:
        s = self._s(col)
        ok = ~np.isnan(s)
        y, st, W, s = self.y[ok], self.st[ok], self.W[:, ok], s[ok]
        n1, n0 = int(y.sum()), int((1 - y).sum())
        if n1 == 0 or n0 == 0:
            return {"n": int(ok.sum()), "point": None, "ci": [None, None], "read": False}
        if kind == "strat":
            pt = strat_auc(y, s, st)
            w = WStratAuc(y, s, st)
        else:
            pt = auc(y, s)
            w = WAuc(y, s)
        bs = [w(W[b]) for b in range(W.shape[0])]
        out = {"n": int(ok.sum()), "n_err": n1, "n_cor": n0, "point": pt, "ci": ci(bs), "read": n1 >= MIN_CELL and n0 >= MIN_CELL,
               "auprc": float(average_precision_score(y, s)), "prev": float(y.mean()), "tie_rate": float(1 - len(np.unique(s)) / len(s))}
        return out

    def delta(self, a: str, b: str, kind: str = "strat") -> dict:
        sa, sb = self._s(a), self._s(b)
        ok = ~np.isnan(sa) & ~np.isnan(sb)
        y, st, W = self.y[ok], self.st[ok], self.W[:, ok]
        sa, sb = sa[ok], sb[ok]
        n1, n0 = int(y.sum()), int((1 - y).sum())
        if n1 == 0 or n0 == 0:
            return {"n": int(ok.sum()), "delta": None, "ci": [None, None], "read": False}
        if kind == "strat":
            pa, pb = strat_auc(y, sa, st), strat_auc(y, sb, st)
            wa, wb = WStratAuc(y, sa, st), WStratAuc(y, sb, st)
        else:
            pa, pb = auc(y, sa), auc(y, sb)
            wa, wb = WAuc(y, sa), WAuc(y, sb)
        bs = [wa(W[i]) - wb(W[i]) for i in range(W.shape[0])]
        c = ci(bs)
        return {"n": int(ok.sum()), "n_err": n1, "n_cor": n0, "a": pa, "b": pb, "delta": pa - pb, "ci": c,
                "read": n1 >= MIN_CELL and n0 >= MIN_CELL, "sign": ("+" if c[0] is not None and c[0] > 0 else "-" if c[1] is not None and c[1] < 0 else "0")}

    def ed(self, en_col: str) -> dict:
        en = self.d[en_col].values.astype(float)
        ok = ~np.isnan(en)
        y, W, en = self.y[ok], self.W[:, ok], en[ok]
        if y.sum() == 0 and (1 - y).sum() == 0:
            return {"n": int(ok.sum()), "e": None, "d": None}
        if y.sum() == 0 or (1 - y).sum() == 0:  # one-class cell (e.g. an error class): report the defined half only
            with np.errstate(invalid="ignore", divide="ignore"):
                if y.sum():
                    return {"n": int(ok.sum()), "e": float(en.mean()), "e_ci": ci((W @ en) / W.sum(1)), "d": None, "read_e": int(y.sum()) >= MIN_CELL}
                return {"n": int(ok.sum()), "e": None, "d": float((1 - en).mean()), "d_ci": ci((W @ (1 - en)) / W.sum(1)), "read_d": int(len(y)) >= MIN_CELL}
        r = ed_decomposition(y, en.astype(int))
        with np.errstate(invalid="ignore", divide="ignore"):
            eb = (W @ (en * y)) / (W @ y)
            db = (W @ ((1 - en) * (1 - y))) / (W @ (1 - y))
        r.update({"e_ci": ci(eb), "d_ci": ci(db), "n": int(ok.sum()), "read_e": int(y.sum()) >= MIN_CELL, "read_d": int((1 - y).sum()) >= MIN_CELL})
        return r

    def ed_delta(self, en_a: str, en_b: str) -> dict:
        a, b = self.d[en_a].values.astype(float), self.d[en_b].values.astype(float)
        ok = ~np.isnan(a) & ~np.isnan(b)
        y, W, a, b = self.y[ok], self.W[:, ok], a[ok], b[ok]
        with np.errstate(invalid="ignore", divide="ignore"):
            de = (W @ ((a - b) * y)) / (W @ y)
            dd = (W @ (((1 - a) - (1 - b)) * (1 - y))) / (W @ (1 - y))
        return {"delta_e": float(((a - b) * y).sum() / y.sum()), "delta_e_ci": ci(de),
                "delta_d": float((((1 - a) - (1 - b)) * (1 - y)).sum() / (1 - y).sum()), "delta_d_ci": ci(dd), "n": int(ok.sum())}


def fmt_ci(x, nd=3):
    if x is None or x.get("point", x.get("delta")) is None:
        return "–"
    v = x.get("point", x.get("delta"))
    c = x.get("ci") or [None, None]
    if c[0] is None:
        return f"{v:.{nd}f}"
    sgn = "+" if "delta" in x and v >= 0 else ""
    return f"{sgn}{v:.{nd}f} [{c[0]:+.{nd}f}, {c[1]:+.{nd}f}]" if "delta" in x else f"{v:.{nd}f} [{c[0]:.{nd}f}, {c[1]:.{nd}f}]"


# =================================================================================================== analyses
def a_ed(P, boot, pop_mask, arms: dict, tag: str) -> dict:
    """(a) e/d per cell + GEE slopes + NET for each binary arm on the population mask."""
    out = {"cells": {}, "gee": {}, "net": {}}
    cells = {"R_AB": np.ones(len(P), bool)}
    for s in ("L25", "L20", "EXC", "CTRL"):
        cells[s] = P.stratum.values == s
    for t in ("T1", "T2", "T3"):
        cells["words_" + t] = P.words_t.values == t
    for b in ("0-1", "2", "3", "4+"):
        cells["ncond_" + b] = P.ncond_bin.values == b
    for e in sorted(P.exc_bin.unique()):
        cells["exc_" + e] = P.exc_bin.values == e
    cells["tierA"] = P.label_tier.values == "A"
    cells["VEX"] = P.vex.values.astype(bool)
    for cn, cm in cells.items():
        c = Cell(cn, P, pop_mask & cm, boot)
        out["cells"][cn] = {a: c.ed(col) for a, col in arms.items()}
        out["cells"][cn]["n_err"], out["cells"][cn]["n_cor"] = c.n_err, c.n_cor
    base = zcols(P[pop_mask].copy())
    for a, col in arms.items():
        d = base[base[col].notna()].copy()
        d["endorsed"] = d[col].astype(int)
        d["flagged"] = 1 - d["endorsed"]
        cor, err = d[d.y == 0], d[d.y == 1]
        out["gee"][a] = {"d_words_ncond": gee_fit(zcols(cor), "flagged ~ zw + zn"),
                         "d_words_ncond_stratum": gee_fit(zcols(cor), "flagged ~ zw + zn + C(stratum)"),
                         "e_words_ncond": gee_fit(zcols(err), "endorsed ~ zw + zn"),
                         "e_words_ncond_stratum": gee_fit(zcols(err), "endorsed ~ zw + zn + C(stratum)")}
    return out


def run_net(P, boot, pop_mask, arms: dict) -> dict:
    out = {}
    Q = P.copy()
    Q["in_RAB"] = pop_mask
    for a, col in arms.items():
        Q["_en"] = Q[col].fillna(0)
        try:
            out[a] = net_test(Q, boot, col="_en")
        except Exception as e:  # noqa: BLE001
            logger.warning(f"net_test {a} failed: {e}")
            out[a] = {"error": str(e)[:200]}
    return out


def b_auroc(P, boot, pop_mask, cols: list, bars: list, tag: str) -> dict:
    cells = {"R_AB [strat]": (np.ones(len(P), bool), "strat"), "R_AB [pooled]": (np.ones(len(P), bool), "pooled"),
             "long L25+L20+EXC [strat]": (P.long.values, "strat"), "L25 [pooled]": (P.stratum.values == "L25", "pooled"),
             "L20 [pooled]": (P.stratum.values == "L20", "pooled"), "EXC [pooled]": (P.stratum.values == "EXC", "pooled"),
             "CTRL [pooled]": (P.stratum.values == "CTRL", "pooled"), "tier A only [strat]": (P.label_tier.values == "A", "strat"),
             "VEX subset [strat]": (P.vex.values.astype(bool), "strat")}
    out = {"metrics": {}, "deltas": {}}
    for cn, (cm, kind) in cells.items():
        c = Cell(cn, P, pop_mask & cm, boot)
        out["metrics"][cn] = {"n_err": c.n_err, "n_cor": c.n_cor, "read": c.read}
        for col in cols + bars:
            if col in P:
                out["metrics"][cn][col] = c.metric(col, kind)
        out["deltas"][cn] = {}
        for a in cols:
            for b in bars:
                if a != b and a in P and b in P:
                    out["deltas"][cn][f"{a} - {b}"] = c.delta(a, b, kind)
        logger.info(f"[{tag}] {cn}: n_err {c.n_err} n_cor {c.n_cor}")
    return out


def s4_nesting(P: pd.DataFrame, pop_mask: np.ndarray, boot: SentBoot) -> dict:
    """(c) fit_s4_oof on folds_E: [S4_full + x] vs S4_full, [S4_full + c_score_align + x] vs [S4_full + c_score_align], fitted
    on the population rows only (labels = R_AB), OOF predictions compared with the paired sentence bootstrap."""
    from s4 import fit_s4_oof
    coefs = json.loads((RUN / "iter_3/gen_art/gen_art_experiment_6/results/s4_full_coefs.json").read_text())
    s4 = coefs["S4_full"]["features_used"]
    T1 = {r["canonical_key"]: r for r in jl(RUN / "iter_3/gen_art/gen_art_experiment_6/results/per_item_T1.jsonl") if r["canonical_key"] in set(P.row_key)}
    bf = {}
    with open(RUN / "iter_2/gen_art/gen_art_experiment_6/E_baseline_features.jsonl") as fh:
        want = {T1[k]["exp6_row_key"] for k in T1}
        for line in fh:
            r = json.loads(line)
            if r["row_key"] in want:
                bf[r["row_key"]] = r
    ff = {f: (math.log(6) if f.endswith("entropy") else 1.0) for f in s4}
    folds = json.loads((RUN / "iter_2/gen_art/gen_art_experiment_6/folds_E.json").read_text())["sentence_fold"]
    d = P[pop_mask]
    table, labels, fold = [], {}, {}
    extra = ["T1__c_score_align", "c_csc", "c_csc_graded", "c_csc_multi", "c_free_exact", "c_free_align"]
    for _, r in d.iterrows():
        t1 = T1[r.row_key]
        b = bf.get(t1["exp6_row_key"], {})
        row = {"row_key": r.row_key, "metadata_fold_E": folds[r.sentence_id]}
        for f in s4:
            if f.startswith("L:"):
                v, st = b.get(f[2:]), b.get(f[2:] + "__status", "na")
            else:
                v, st = t1.get(f), t1.get(f + "__status", "ok")
            row[f] = None if v is None else float(v)
            row[f + "__status"] = "fail" if str(st).startswith("fail") else ("ok" if v is not None else "na")
        for f in extra:
            v = r[f]
            row[f] = None if pd.isna(v) else float(v)
            row[f + "__status"] = "ok" if row[f] is not None else "na"
        table.append(row)
        labels[r.row_key] = int(r.y)
        fold[r.row_key] = folds[r.sentence_id]
    sets = {"S4_full": s4, "S4_full+c_csc": s4 + ["c_csc"], "S4_full+c_csc_graded": s4 + ["c_csc_graded"],
            "S4_full+c_csc_multi": s4 + ["c_csc_multi"], "S4_full+c_free_exact": s4 + ["c_free_exact"],
            "S4_full+c_score_align": s4 + ["T1__c_score_align"], "S4_full+c_score_align+c_csc": s4 + ["T1__c_score_align", "c_csc"],
            "S4_full+c_score_align+c_csc_graded": s4 + ["T1__c_score_align", "c_csc_graded"]}
    Q = P.copy()
    for nm, feats in sets.items():
        oof, info = fit_s4_oof(table, labels, fold, feats, C=1.0, fail_fill=ff)
        Q["oof__" + nm] = [oof.get(k, np.nan) if oof.get(k) is not None else np.nan for k in Q.row_key]
    c = Cell("nest", Q, pop_mask, boot)
    out = {"fits": {nm: {"strat": c.metric("oof__" + nm, "strat"), "pooled": c.metric("oof__" + nm, "pooled")} for nm in sets},
           "reproduction_vs_T1_S4_full_oof": {"corr": float(np.corrcoef(Q.loc[pop_mask, "oof__S4_full"], Q.loc[pop_mask, "T1__S4_full_oof"])[0, 1]),
                                              "T1_S4_full_oof_strat_same_rows": c.metric("T1__S4_full_oof", "strat")},
           "nested": {}}
    for big, small in (("S4_full+c_csc", "S4_full"), ("S4_full+c_csc_graded", "S4_full"), ("S4_full+c_csc_multi", "S4_full"),
                       ("S4_full+c_free_exact", "S4_full"), ("S4_full+c_score_align", "S4_full"),
                       ("S4_full+c_score_align+c_csc", "S4_full+c_score_align"),
                       ("S4_full+c_score_align+c_csc_graded", "S4_full+c_score_align")):
        out["nested"][f"{big} - {small}"] = {k: c.delta("oof__" + big, "oof__" + small, k) for k in ("strat", "pooled")}
    return out


def d_went(P: pd.DataFrame, pop_mask: np.ndarray, free_flag_col: str, csc_flag_col: str | None) -> dict:
    """(d) vocabulary-only vs structural free-peer disagreements for CORRECT rows (pairs_E: align / nf / hyb verdicts).
    csc_flag_col None -> the $0 FULL-population version (all CORRECT rows flagged by FREE-MATCHED)."""
    free = json.loads((DATA / "sentence_peers_free.json").read_text())
    import csc as C
    cor = P[pop_mask & (P.y.values == 0)]
    if csc_flag_col is None:
        rows = cor[cor[free_flag_col] == 0]
    else:
        rows = cor[(cor[free_flag_col] == 0) & (cor[csc_flag_col] == 1)]
    need = {}
    for _, r in rows.iterrows():
        fams = [m[1] for m in C.peers_for(r.family, 3)]
        sp = free.get(r.sentence_id, {})
        for f in fams:
            if f in sp:
                need[(r.row_key, sp[f]["row_key"])] = None
    with open(RUN / "iter_3/gen_art/gen_art_experiment_8/results/pairs_E.jsonl") as fh:
        for line in fh:
            q = json.loads(line)
            k = (q["cand"], q["peer"])
            if k in need:
                need[k] = q
    cls = Counter()
    per_row = []
    for (rk, pk), q in need.items():
        if q is None:
            cls["pair_missing_or_peer_unparseable"] += 1
            continue
        if q["align_eq"]:
            c = "align_equivalent (vocabulary/granularity resolved by the aligner)"
        elif q["nf_eq"] or q["hyb_eq"]:
            c = "vocabulary-only (NF/HYB name-free equivalent, ALIGN not)"
        else:
            c = "structural (no vocabulary map makes them equivalent)"
        cls[c] += 1
        per_row.append((rk, c))
    tot = sum(v for k, v in cls.items() if not k.startswith("pair_missing"))
    rowcls = defaultdict(set)
    for rk, c in per_row:
        rowcls[rk].add(c)
    n_rows_vocab_only = sum(1 for s in rowcls.values() if all(not c.startswith("structural") for c in s))
    return {"n_rows": int(len(rows)), "pair_classes": dict(cls), "pair_shares": {k: v / tot for k, v in cls.items() if tot and not k.startswith("pair_missing")},
            "rows_all_disagreements_vocabulary_resolvable": n_rows_vocab_only,
            "share_rows_vocab_resolvable": n_rows_vocab_only / max(1, len(rowcls))}


TAG_RULE = """Automated tagging rule for CORRECT rows still flagged by CSC (written before tagging; applied mechanically):
 1 READING_CHOICE  : the candidate is z3-equivalent (same vocabulary) to some peer's alt_fol (a second legitimate reading was produced)
 2 PEER_SCATTER    : no two peers agree with each other (no peer majority) -> peers diverge among themselves
 3 GRANULARITY     : the candidate and the peer-majority formula are eqmv-equivalent (ALIGN/granularity bridge) but not same-vocabulary equivalent
 4 SINGLE_OP_DIFF  : the typed same-vocabulary repair from candidate to peer majority is one op (peer error OR label error; not separable without a human)
 5 MULTI_OP_DIFF   : otherwise (compound structural difference)"""


def tag_rows(rows: list[dict]) -> list[dict]:
    import consensus_lib as CL  # noqa: F401
    import csc as C
    out = []
    for r in rows:
        peers = r["peers"]
        cand = r["cand"]
        tag = None
        if any(p.get("alt_fol") and C.exact_equiv(cand, p["alt_fol"]) is True for p in peers):
            tag = "READING_CHOICE"
        maj = C.majority_formula(peers)
        if tag is None and maj is None:
            tag = "PEER_SCATTER"
        if tag is None:
            try:
                v, how = CL.equivalent_modulo_vocab(cand, maj, ms=3000)
            except Exception:  # noqa: BLE001
                v = None
            if v is True:
                tag = "GRANULARITY"
        rep = None
        if tag is None:
            rep = C.typed_repair_same_vocab(cand, maj, budget_s=4.0)
            tag = "SINGLE_OP_DIFF" if len(rep.get("ops") or []) == 1 else "MULTI_OP_DIFF"
        out.append({**r, "tag": tag, "repair": rep})
    return out


def typing_task(rows: list[dict]) -> list[dict]:
    sys.path.insert(0, str(SRC))
    import csc as C
    out = []
    for r in rows:
        res = {}
        for which in ("own_majority", "free_majority"):
            t = r.get(which)
            res[which] = C.typed_repair_same_vocab(r["cand"], t, budget_s=4.0) if t else {"cls": "NO_MAJORITY", "ops": []}
        out.append({**r, **{"pred_" + k: v for k, v in res.items()}})
    return out


def _init_worker():
    sys.path.insert(0, str(SRC))
    sys.setrecursionlimit(20000)


def typing_analysis(P: pd.DataFrame, pop_mask: np.ndarray, boot: SentBoot) -> dict:
    d = P[pop_mask & (P.y.values == 1) & (P.label_tier.values == "A")]
    d = d[d.repair_ops.apply(lambda x: isinstance(x, list) and 1 <= len(x) <= 2)]
    rows = [{"row_key": r.row_key, "cand": r.candidate_fol, "own_majority": r.own_majority, "free_majority": r.free_majority,
             "true_ops": sorted(r.repair_ops), "sentence_id": r.sentence_id} for _, r in d.iterrows()]
    chunks = [rows[i:i + 4] for i in range(0, len(rows), 4)]
    res = []
    with ProcessPoolExecutor(max_workers=4, mp_context=mp.get_context("spawn"), initializer=_init_worker) as ex:
        for f in as_completed([ex.submit(typing_task, c) for c in chunks]):
            try:
                res += f.result()
            except Exception as e:  # noqa: BLE001
                logger.error(f"typing chunk failed {e}")
    coarse = {"ADD": "COVERAGE", "DROP": "COVERAGE", "NEG": "POLARITY", "REV": "POLARITY", "QUANT": "POLARITY"}

    def cc(ops):
        return sorted({coarse.get(o, "STRUCT") for o in ops})
    maj = Counter(tuple(r["true_ops"]) for r in res).most_common(1)[0] if res else (None, 0)
    out = {"n": len(res), "true_class_counts": {"+".join(k): v for k, v in Counter(tuple(r["true_ops"]) for r in res).items()},
           "majority_class": "+".join(maj[0]) if maj[0] else None, "majority_acc": maj[1] / len(res) if res else None,
           "chance": 1 / max(1, len({tuple(r["true_ops"]) for r in res})), "iter2_medoid_ref": 0.371, "per_row": res}
    sid = [r["sentence_id"] for r in res]
    sb = SentBoot(sid, B, 0) if res else None
    for which in ("own_majority", "free_majority"):
        acc = np.array([sorted(r["pred_" + which].get("ops") or []) == r["true_ops"] for r in res], float)
        acc_c = np.array([bool(r["pred_" + which].get("ops")) and cc(r["pred_" + which]["ops"]) == cc(r["true_ops"]) for r in res], float)
        cov = np.array([bool(r["pred_" + which].get("ops")) for r in res], float)
        W = sb.W() if sb else None
        out[which] = {"acc_exact_opset": float(acc.mean()) if len(acc) else None,
                      "acc_exact_ci": ci((W @ acc) / W.sum(1)) if len(acc) else [None, None],
                      "acc_coarse_class": float(acc_c.mean()) if len(acc) else None,
                      "coverage_typed": float(cov.mean()) if len(acc) else None,
                      "pred_class_counts": dict(Counter(r["pred_" + which].get("cls") for r in res).most_common(12))}
    return out


def cost_analysis(P: pd.DataFrame, pop_mask: np.ndarray) -> dict:
    S = [r for r in jl(RES / "scores_labelblind.jsonl") if r["arm"] == "OWN"]
    share = Counter()
    for r in S:
        for p in r["peers"]:
            share[p["key"]] += 1
    pr = {}
    for r in S:
        full_undedup = sum(p.get("usd") or 0 for p in r["peers"])
        full_app = sum((p.get("usd") or 0) / share[p["key"]] for p in r["peers"])
        pr[r["row_key"]] = (full_undedup, full_app, r.get("z3_cpu_s") or 0.0)
    d = P[pop_mask]
    u = np.array([pr[k][0] for k in d.row_key if k in pr])
    a = np.array([pr[k][1] for k in d.row_key if k in pr])
    z = np.array([pr[k][2] for k in d.row_key if k in pr])
    led = jl(RES / "api_cost_ledger.jsonl")
    by_model = defaultdict(list)
    for r in led:
        if r.get("usd"):
            by_model[r["model"]].append(r["usd"])
    return {"n": int(len(u)), "FULL_usd_per_candidate_undeduped_mean": float(u.mean()), "FULL_usd_per_candidate_undeduped_p95": float(np.percentile(u, 95)),
            "FULL_usd_per_candidate_dedup_apportioned_mean": float(a.mean()),
            "MARGINAL_z3_cpu_s_per_candidate_mean": float(z.mean()), "MARGINAL_z3_cpu_s_p95": float(np.percentile(z, 95)),
            "usd_per_call_by_model": {m: float(np.mean(v)) for m, v in by_model.items()},
            "reference_flash_lite_usd_per_item": 4.88e-05, "reference_free_9peer_pool_usd_per_item_FULL": 1.21e-04,
            "G5_threshold": 0.002, "G5_pass": bool(u.mean() <= 0.002),
            "ledger_total_usd": float(sum(r.get("usd") or 0 for r in led)), "n_ledger_rows": len(led)}


def complexity(P, boot, pop_mask, cols) -> dict:
    out = {}
    for var, bins in (("words_t", ("T1", "T2", "T3")), ("nq_bin", ("0-1", "2", "3+")), ("depth_bin", ("0-1", "2", "3+")),
                      ("ncond_bin", ("0-1", "2", "3", "4+")), ("exc_bin", tuple(sorted(P.exc_bin.unique())))):
        out[var] = {}
        for b in bins:
            c = Cell(f"{var}={b}", P, pop_mask & (P[var].values == b), boot)
            out[var][b] = {"n_err": c.n_err, "n_cor": c.n_cor, "read": c.read, **{col: c.metric(col, "strat") for col in cols}}
    return out


def m3_both(P, boot, pop_mask, en_col: str, judge_col: str, tag: str) -> dict:
    """M3 under both specifications: (1) bootstrap delta of the logistic slope of row-level decision correctness on z(words)
    (consensus binary vs judge binarised at the consensus flag rate, eval 2 m3_local logic); (2) stacked GEE with a
    method x z(words) interaction."""
    from sklearn.linear_model import LogisticRegression
    d = zcols(P[pop_mask & P[en_col].notna().values & P[judge_col].notna().values].copy())
    y = d.y.values.astype(int)
    b_c = 1 - d[en_col].values.astype(int)
    rate = b_c.mean()
    js = d[judge_col].values.astype(float)
    tb = np.array([int(hashlib.sha1(f"M3|{rk}".encode()).hexdigest()[:12], 16) / 16 ** 12 for rk in d.row_key])
    order = np.lexsort((tb, js))[::-1]
    b_j = np.zeros(len(js), int)
    b_j[order[:int(round(rate * len(js)))]] = 1
    d["correct_c"] = (b_c == y).astype(int)
    d["correct_j"] = (b_j == y).astype(int)
    gc, gj = gee_fit(d, "correct_c ~ zw"), gee_fit(d, "correct_j ~ zw")
    st = pd.concat([d.assign(correct=d.correct_c, method="consensus"), d.assign(correct=d.correct_j, method="judge")])
    gs = gee_fit(st, "correct ~ zw * C(method, Treatment('judge'))")
    mask = pop_mask & P[en_col].notna().values & P[judge_col].notna().values
    W = boot.W(mask)
    X = d[["zw"]].values
    diffs = []
    for b in range(W.shape[0]):
        try:
            s1 = LogisticRegression(C=1e6, max_iter=500).fit(X, d.correct_c.values, sample_weight=W[b] + 1e-12).coef_[0][0]
            s2 = LogisticRegression(C=1e6, max_iter=500).fit(X, d.correct_j.values, sample_weight=W[b] + 1e-12).coef_[0][0]
            diffs.append(s1 - s2)
        except ValueError:
            continue
    sc = gc["coef"]["zw"]["b"] if gc["coef"] else None
    sj = gj["coef"]["zw"]["b"] if gj["coef"] else None
    inter = [k for k in (gs["coef"] or {}) if k.startswith("zw:")]
    return {"tag": tag, "n": int(len(d)), "flag_rate": float(rate), "acc_consensus": float(d.correct_c.mean()), "acc_judge": float(d.correct_j.mean()),
            "spec1_bootstrap_delta_slope": {"delta": (sc - sj) if (sc is not None and sj is not None) else None, "ci": ci(diffs), "n_boot": len(diffs),
                                            "slope_consensus": sc, "slope_judge": sj},
            "spec2_stacked_gee_interaction": (gs["coef"] or {}).get(inter[0]) if inter else None,
            "joint_label": "consensus degrades LESS with length than the judge iff both specifications give a positive delta with CI > 0"}


def system_level(P, pop_mask, cols) -> dict:
    d = P[pop_mask]
    g = d.groupby("sysvar")
    err = g.y.mean()
    out = {"n_systems": int(len(err)), "rows_per_system": g.size().to_dict()}
    for c in cols:
        m = g[c].mean()
        ok = m.notna() & err.notna()
        if ok.sum() >= 4:
            t = kendalltau(m[ok], err[ok], variant="b")
            out[c] = {"tau_b": float(t.statistic), "p": float(t.pvalue), "n": int(ok.sum())}
    return out


def md_table(title: str, source: str, header: list, rows: list) -> str:
    s = f"\n## {title}\n# source: {source}\n\n| " + " | ".join(header) + " |\n|" + "---|" * len(header) + "\n"
    for r in rows:
        s += "| " + " | ".join(str(x) for x in r) + " |\n"
    return s


# =================================================================================================== main
@logger.catch(reraise=True)
def main() -> dict:
    t0 = time.time()
    G = guard()
    logger.info(f"guard ok: {G}")
    P, cuts = build_frame()
    boot = SentBoot(P.sentence_id.values, B, 0)
    PRI = P.PRIMARY.values
    FULL = np.ones(len(P), bool)
    A = {"guard": G, "cuts": cuts, "populations": {k: {"n": int(P[k].sum()), "n_err": int(P.loc[P[k], "y"].sum()),
                                                          "n_cor": int((1 - P.loc[P[k], "y"]).sum()), "n_sent": int(P.loc[P[k], "sentence_id"].nunique())}
                                                      for k in ("PRIMARY", "GE2", "MINI200")}}
    A["populations"]["FULL"] = {"n": len(P), "n_err": int(P.y.sum()), "n_cor": int((1 - P.y).sum()), "n_sent": int(P.sentence_id.nunique())}
    A["populations"]["PRIMARY_by_stratum"] = {s: {"n_err": int(P.loc[PRI & (P.stratum == s), "y"].sum()),
                                                  "n_cor": int((1 - P.loc[PRI & (P.stratum == s), "y"]).sum())} for s in ("L25", "L20", "EXC", "CTRL")}
    A["populations"]["PRIMARY_by_family"] = P.loc[PRI, "family"].value_counts().to_dict()
    # coverage / status
    A["status"] = {"own_status_PRIMARY": P.loc[PRI, "own_status"].value_counts().to_dict(),
                   "own_status_GE2": P.loc[P.GE2, "own_status"].value_counts().to_dict(),
                   "free_status_FULL": P.free_status.value_counts().to_dict(), "free_align_status_FULL": P.free_align_status.value_counts().to_dict(),
                   "own_unknown_pairs_PRIMARY": int(np.nansum(P.loc[PRI, "own_n_unknown"])),
                   "own_insufficient_share_PRIMARY": float((P.loc[PRI, "own_status"] == "csc_insufficient_peers").mean()),
                   "free_insufficient_share_FULL": float((P.free_status == "csc_insufficient_peers").mean()),
                   "peer_pair_agree_exact": {"CSC_OWN_PRIMARY": float(np.nanmean(P.loc[PRI, "own_peer_pair_agree"])),
                                             "FREE_MATCHED_same_rows": float(np.nanmean(P.loc[PRI, "free_ppa"])),
                                             "FREE_MATCHED_FULL": float(np.nanmean(P.free_ppa))}}
    logger.info(f"status: {A['status']}")
    # ---------------- (a) e / d
    arms_pri = {"CSC": "en_c_csc", "CSC_graded": "en_c_csc_graded", "CSC_multi": "en_c_csc_multi", "FREE_exact": "en_c_free_exact",
                "FREE_align": "en_c_free_align", "END_MAJ9": "en_END_MAJ9", "HYB_MEAN": "en_HYB_MEAN"}
    A["a_ed_PRIMARY"] = a_ed(P, boot, PRI, arms_pri, "PRIMARY")
    c = Cell("PRIMARY", P, PRI, boot)
    A["a_ed_PRIMARY"]["paired_CSC_minus"] = {b: c.ed_delta("en_c_csc", col) for b, col in arms_pri.items() if b != "CSC"}
    arms_full = {"FREE_exact": "en_c_free_exact", "FREE_align": "en_c_free_align", "FREE_graded": "en_c_free_graded", "END_MAJ9": "en_END_MAJ9"}
    A["a_ed_FULL"] = a_ed(P, boot, FULL, arms_full, "FULL")
    cf = Cell("FULL", P, FULL, boot)
    A["a_ed_FULL"]["paired_exact_minus_align"] = cf.ed_delta("en_c_free_exact", "en_c_free_align")
    for pop in ("GE2", "MINI200"):
        cc_ = Cell(pop, P, P[pop].values, boot)
        A[f"a_ed_{pop}"] = {a: cc_.ed(col) for a, col in arms_pri.items()}
    logger.info(f"(a) done {time.time()-t0:.0f}s")
    # write d FIRST, then read the sibling prediction (read-only)
    dres = {"d_CSC_PRIMARY": A["a_ed_PRIMARY"]["cells"]["R_AB"]["CSC"], "d_FREE_align_PRIMARY": A["a_ed_PRIMARY"]["cells"]["R_AB"]["FREE_align"],
            "d_FREE_exact_PRIMARY": A["a_ed_PRIMARY"]["cells"]["R_AB"]["FREE_exact"], "d_END_MAJ9_PRIMARY": A["a_ed_PRIMARY"]["cells"]["R_AB"]["END_MAJ9"],
            "d_FREE_exact_FULL": A["a_ed_FULL"]["cells"]["R_AB"]["FREE_exact"], "d_FREE_align_FULL": A["a_ed_FULL"]["cells"]["R_AB"]["FREE_align"],
            "d_END_MAJ9_FULL": A["a_ed_FULL"]["cells"]["R_AB"]["END_MAJ9"], "written_ts": time.time()}
    jdump(dres, RES / "d_measured.json")
    sib = RUN / "iter_4/gen_art/gen_art_evaluation_3/prereg_d_split.json"
    A["d_vs_sibling_prediction"] = {"sibling_file": str(sib), "exists": sib.exists(), "read_after_d_written_ts": time.time()}
    if sib.exists():
        A["d_vs_sibling_prediction"]["sibling_prereg_sha256"] = hashlib.sha256(sib.read_bytes()).hexdigest()
    p1 = RUN / "iter_4/gen_art/gen_art_evaluation_3/results/part1.json"
    if p1.exists():
        pools = json.loads(p1.read_text()).get("pools", {})
        A["d_vs_sibling_prediction"]["sibling_part1_predictions"] = {k: {kk: pools[k].get(kk) for kk in ("d_floor_pred", "d_floor_pred_ci", "e_ceiling_pred")}
                                                                     for k in ("3pool", "9fam") if k in pools}
        A["d_vs_sibling_prediction"]["note"] = ("sibling predictions are for the FULL R_AB population; CSC was measured on PRIMARY, where the matched free peers "
                                                "scored exactly already have d = %.3f (FULL: %.3f), so compare RATIOS d_CSC / d_FREE_exact, not levels"
                                                % (dres["d_FREE_exact_PRIMARY"]["d"], dres["d_FREE_exact_FULL"]["d"]))
        A["d_vs_sibling_prediction"]["measured"] = {"d_CSC_PRIMARY": dres["d_CSC_PRIMARY"]["d"], "e_CSC_PRIMARY": dres["d_CSC_PRIMARY"]["e"],
                                                    "ratio_d_CSC_over_d_FREE_exact_PRIMARY": dres["d_CSC_PRIMARY"]["d"] / dres["d_FREE_exact_PRIMARY"]["d"],
                                                    "sibling_ratio_d_floor_3pool_over_d_FREE_exact_FULL": (pools.get("3pool", {}).get("d_floor_pred") or float("nan")) / dres["d_FREE_exact_FULL"]["d"]}
    A["net"] = {"PRIMARY": run_net(P, boot, PRI, {"CSC": "en_c_csc", "FREE_align": "en_c_free_align", "END_MAJ9": "en_END_MAJ9"}),
                "FULL": run_net(P, boot, FULL, {"FREE_exact": "en_c_free_exact", "FREE_align": "en_c_free_align", "END_MAJ9": "en_END_MAJ9"})}
    logger.info(f"NET done {time.time()-t0:.0f}s")
    # ---------------- (b) AUROC
    A["b_PRIMARY"] = b_auroc(P, boot, PRI, VARIANTS, COMPARATORS, "PRIMARY")
    A["b_GE2"] = b_auroc(P, boot, P.GE2.values, ["c_csc"], ["c_free_exact", "c_free_align", "T1__c_score_align", "T1__judge_cheap_disg"], "GE2")
    A["b_MINI200"] = b_auroc(P, boot, P.MINI200.values, ["c_csc"], ["c_free_exact", "c_free_align", "T1__c_score_align", "T1__judge_cheap_disg"], "MINI200")
    A["b_FULL_free"] = b_auroc(P, boot, FULL, ["c_free_exact", "c_free_align", "c_free_graded"], ["T1__c_score_align", "T1__judge_cheap_disg", "T1__p_peer_text"], "FULL")
    strong = PRI & P.T1__judge_strong_orig.notna().values
    cs_ = Cell("PRIMARY frontier frame", P, strong, boot)
    A["b_frontier_frame"] = {"n_err": cs_.n_err, "n_cor": cs_.n_cor, "c_csc": cs_.metric("c_csc", "pooled"),
                             "judge_strong_orig": cs_.metric("T1__judge_strong_orig", "pooled"),
                             "delta": cs_.delta("c_csc", "T1__judge_strong_orig", "pooled")}
    # sensitivity: insufficient-peer rows excluded
    ex = PRI & (P.own_status.values == "OK")
    A["b_PRIMARY_excl_insufficient"] = b_auroc(P, boot, ex, ["c_csc"], ["c_free_exact", "c_free_align", "T1__c_score_align"], "PRI_excl")
    # K4 / OTHER exploratory (incidental coverage)
    for arm, colc in (("K4", "c_k4"), ("OTHER", "c_other")):
        m = P[colc].notna().values & (P[colc + "_missing"].fillna(9).values == 0)
        ce = Cell(arm, P, m, boot)
        A[f"exploratory_{arm}"] = {"n_err": ce.n_err, "n_cor": ce.n_cor, "read": ce.read, colc: ce.metric(colc, "strat"),
                                   "c_csc_same_rows": ce.metric("c_csc", "strat"), "ed_" + arm: ce.ed("en_" + colc), "ed_CSC_same_rows": ce.ed("en_c_csc")}
    logger.info(f"(b) done {time.time()-t0:.0f}s")
    # ---------------- (c) nesting
    try:
        A["c_nesting_PRIMARY"] = s4_nesting(P, PRI, boot)
    except Exception as e:  # noqa: BLE001
        logger.exception("nesting failed")
        A["c_nesting_PRIMARY"] = {"error": str(e)[:300]}
    logger.info(f"(c) done {time.time()-t0:.0f}s")
    # ---------------- (d) where d went
    A["d_where_FULL_free_align_flagged_CORRECT"] = d_went(P, FULL, "en_c_free_align", None)
    A["d_where_FULL_free_exact_flagged_CORRECT"] = d_went(P, FULL, "en_c_free_exact", None)
    A["d_where_PRIMARY_free_flagged_csc_endorsed"] = d_went(P, PRI, "en_c_free_align", "en_c_csc")
    # tagging of still-flagged CORRECT rows (60-row stratified sample, automated rule)
    S_own = {r["row_key"]: r for r in jl(RES / "scores_labelblind.jsonl") if r["arm"] == "OWN"}
    still = P[PRI & (P.y.values == 0) & (P.en_c_csc.values == 0)]
    import arms as AR
    samp = AR.stratified([{"row_key": r.row_key, "stratum": r.stratum} for _, r in still.iterrows()], 60, "TAG")
    rows = [{"row_key": s["row_key"], "text": P.loc[P.row_key == s["row_key"], "text"].iloc[0],
             "cand": P.loc[P.row_key == s["row_key"], "candidate_fol"].iloc[0], "stratum": s["stratum"],
             "peers": [{"model": p["model"], "fol": p["fol"], "alt_fol": p["alt_fol"]} for p in S_own[s["row_key"]]["peers"]]} for s in samp]
    tagged = tag_rows(rows)
    A["d_tagging"] = {"rule": TAG_RULE, "n_still_flagged_CORRECT": int(len(still)), "n_tagged": len(tagged),
                      "tag_counts": dict(Counter(t["tag"] for t in tagged))}
    jdump(tagged, RES / "d_tagging_rows.json")
    logger.info(f"(d) done {time.time()-t0:.0f}s")
    # ---------------- (e) anchoring on real errors: e by error class
    def classes(r):
        ops = set(r.error_ops or [])
        out = []
        if "ADD" in ops: out.append("ADD")
        if "DROP" in ops: out.append("DROP")
        if "COMPOUND" in ops: out.append("COMPOUND")
        if ops & {"NEG", "REV", "QUANT"}: out.append("polarity(NEG/REV/QUANT)")
        if ops & {"CONN", "RESTR", "BIND", "MOVE", "SWAP", "SCOPE", "UNGLUE"}: out.append("structural(CONN/RESTR/BIND/MOVE/SWAP/SCOPE/UNGLUE)")
        if "MEANING_RENAME" in ops or r.auto_label == "VOCAB_GRAN": out.append("MEANING_RENAME-type (MEANING_RENAME op or tier-B VOCAB_GRAN)")
        return out
    P["err_classes"] = [classes(r) if r.y == 1 else [] for r in P.itertuples()]
    E = {}
    for pop, pm in (("PRIMARY", PRI), ("FULL", FULL)):
        E[pop] = {}
        allc = sorted({c for cl in P.err_classes for c in cl})
        for cl in allc:
            m = pm & P.err_classes.apply(lambda x: cl in x).values
            ce = Cell(cl, P, m, boot)
            arms_e = arms_pri if pop == "PRIMARY" else arms_full
            E[pop][cl] = {"n": int(m.sum()), **{a: ce.ed(col) for a, col in arms_e.items()}}
            if pop == "PRIMARY":
                E[pop][cl]["paired_CSC_minus_FREE_exact"] = ce.ed_delta("en_c_csc", "en_c_free_exact") if m.sum() else None
                E[pop][cl]["paired_CSC_minus_FREE_align"] = ce.ed_delta("en_c_csc", "en_c_free_align") if m.sum() else None
    A["e_anchoring_by_error_class"] = E
    logger.info(f"(e) done {time.time()-t0:.0f}s")
    # ---------------- (f) typing
    try:
        A["f_typing_PRIMARY"] = typing_analysis(P, PRI, boot)
        jdump(A["f_typing_PRIMARY"].pop("per_row"), RES / "typing_rows.json")
    except Exception as e:  # noqa: BLE001
        logger.exception("typing failed")
        A["f_typing_PRIMARY"] = {"error": str(e)[:300]}
    logger.info(f"(f) done {time.time()-t0:.0f}s")
    # ---------------- (g) cost
    A["g_cost"] = cost_analysis(P, PRI)
    # ---------------- (h) complexity + M3
    A["h_complexity_PRIMARY"] = complexity(P, boot, PRI, ["c_csc", "c_free_exact", "c_free_align", "T1__c_score_align", "T1__judge_cheap_disg"])
    A["h_complexity_FULL"] = complexity(P, boot, FULL, ["c_free_exact", "c_free_align", "T1__c_score_align", "T1__judge_cheap_disg"])
    A["h_M3"] = {"CSC_vs_flashlite_disg_PRIMARY": m3_both(P, boot, PRI, "en_c_csc", "T1__judge_cheap_disg", "CSC"),
                 "FREEalign_vs_flashlite_disg_PRIMARY": m3_both(P, boot, PRI, "en_c_free_align", "T1__judge_cheap_disg", "FREE_align"),
                 "END_MAJ9_vs_flashlite_disg_PRIMARY": m3_both(P, boot, PRI, "en_END_MAJ9", "T1__judge_cheap_disg", "END_MAJ9")}
    logger.info(f"(h) done {time.time()-t0:.0f}s")
    # ---------------- (i) system level
    A["i_system_level_PRIMARY"] = system_level(P, PRI, ["c_csc", "c_csc_graded", "c_free_exact", "c_free_align", "T1__c_score_align", "T1__judge_cheap_disg"])
    A["i_system_level_FULL"] = system_level(P, FULL, ["c_free_exact", "c_free_align", "T1__c_score_align", "T1__judge_cheap_disg"])
    # ---------------- (j) placebos
    rng = np.random.default_rng(0)
    d = P[PRI]
    ys = rng.permutation(d.y.values)
    A["j_placebo"] = {"shuffled_labels_auroc_c_csc": auc(ys, d.c_csc.values), "shuffled_labels_strat_auroc_c_csc": strat_auc(ys, d.c_csc.values, d.stratum.values),
                      "random_sentence_signature_arm": "NOT_RUN (platform budget refusal; 0 peer calls)"}
    # ---------------- (k) rename: CSC NOT_RUN; $0 incumbent side: c_score_align re-derived (9-peer eqmv) on SYN-renamed CORRECT rows
    m = P.c_align9_base.notna().values & P.c_align9_syn.notna().values
    ck = Cell("RENAME_SYN rows", P, m, boot)
    fa_b = (P.loc[m, "c_align9_base"] >= 0.5).astype(float).values
    fa_s = (P.loc[m, "c_align9_syn"] >= 0.5).astype(float).values
    W = ck.W
    A["k_rename"] = {"CSC_RENAME_SYN": "NOT_RUN", "CSC_RENAME_NONCE": "NOT_RUN",
                     "c_score_align_rederived_on_SYN_rows": {"n": int(m.sum()), "FA_base (c >= 0.5 = not END_MAJ endorsed)": float(fa_b.mean()) if m.sum() else None,
                                                             "FA_syn": float(fa_s.mean()) if m.sum() else None,
                                                             "delta_FA": float(fa_s.mean() - fa_b.mean()) if m.sum() else None,
                                                             "delta_FA_ci": ci((W @ (fa_s - fa_b)) / W.sum(1)) if m.sum() else [None, None],
                                                             "rederived_base_vs_frozen_c_score_align_corr": float(np.corrcoef(P.loc[m, "c_align9_base"], P.loc[m, "T1__c_score_align"])[0, 1]) if m.sum() > 2 else None}}
    # ---------------- gates
    A["gates"] = gates(P, A, boot)
    A["runtime_s"] = time.time() - t0
    jdump(A, RES / "analysis.json")
    logger.info(f"analysis written, {time.time()-t0:.0f}s")
    return A


def gates(P, A, boot) -> dict:
    PRI = P.PRIMARY.values
    out = {"population": "PRIMARY_CSC_SUBSET (see prereg_csc_E_addendum1.json); PROVISIONAL: not the pre-registered population",
           "G4": None, "variants": {}}
    cost = A["g_cost"]
    bP = A["b_PRIMARY"]
    for v, en in (("c_csc", "en_c_csc"), ("c_csc_graded", "en_c_csc_graded"), ("c_csc_multi", "en_c_csc_multi"), ("HYB_MEAN", "en_HYB_MEAN")):
        c = Cell("g", P, PRI, boot)
        edr = c.ed(en)
        cor = zcols(P[PRI & (P.y.values == 0) & P[en].notna().values].copy())
        cor["flagged"] = 1 - cor[en].astype(int)
        g = gee_fit(cor, "flagged ~ zw + zn")
        slope = (g["coef"] or {}).get("zw")
        g1 = {"d": edr["d"], "d_ci": edr["d_ci"], "words_slope": slope, "d_le_0.35": edr["d"] is not None and edr["d"] <= 0.35,
              "slope_ok": bool(slope and (slope["ci"][0] <= 0 <= slope["ci"][1] or slope["ci"][1] < 0))}
        g1["pass"] = bool(g1["d_le_0.35"] and g1["slope_ok"])
        rab = bP["metrics"]["R_AB [strat]"]
        l25 = bP["metrics"]["L25 [pooled]"]
        dl25 = bP["deltas"]["L25 [pooled]"].get(f"{v} - T1__c_score_align")
        g2a = rab[v]["point"] >= rab["T1__c_score_align"]["point"] - 0.01
        g2 = {"strat_auroc": rab[v], "c_score_align_strat": rab["T1__c_score_align"], "R_AB_part_pass": bool(g2a),
              "L25_read": bool(l25["read"]), "L25_delta_vs_c_score_align": dl25,
              "L25_part": ("NOT_READ (cell < 50/50)" if not l25["read"] else bool(dl25["delta"] > 0))}
        g2["pass"] = "NOT_READ" if not l25["read"] else bool(g2a and dl25["delta"] > 0)
        full = cost["FULL_usd_per_candidate_undeduped_mean"] + (1.21e-4 if v == "HYB_MEAN" else 0.0)
        g5 = {"FULL_usd_per_candidate": full, "threshold": 0.002, "pass": bool(full <= 0.002)}
        out["variants"][v] = {"k": 3, "G1": g1, "G2": g2, "G3_E": "NOT_RUN", "G4": None, "G5": g5,
                              "strat_auroc_R_AB": rab[v], "E_side_status": "PROVISIONAL (subset; G3-E NOT_RUN)"}
    k4 = A.get("exploratory_K4", {})
    out["variants"]["c_csc_k4"] = {"k": 4, "G1": "NOT_READ (incidental coverage only)", "G2": "NOT_READ", "G3_E": "NOT_RUN", "G5": "NOT_READ",
                                   "exploratory": {kk: k4.get(kk) for kk in ("n_err", "n_cor", "c_k4", "c_csc_same_rows")}}
    out["iteration5_rule_note"] = ("ELIGIBLE requires G1, G3 (E and PERTURB), G4 and G5. G3-E is NOT_RUN here, so no variant can be ELIGIBLE "
                                   "from this file alone; the E-side numbers are PROVISIONAL (354-row subset, platform budget refusal).")
    return out


if __name__ == "__main__":
    logger.remove()
    logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
    logger.add(ROOT / "logs" / "analyse.log", rotation="30 MB", level="DEBUG")
    main()
