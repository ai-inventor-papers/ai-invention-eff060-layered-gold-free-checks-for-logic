"""Shared loaders for the label-joined analyses (Part A / Part B). Every loader that touches a label calls guard() first:
analyses refuse to run unless results/prereg_hyb.json exists and its sha256 matches results/prereg_hyb.sha256.

Orientation: every metric column is oriented so that HIGHER = more likely ERROR.
"""
from __future__ import annotations

import hashlib
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
import stats as ST  # noqa: E402

RES = ROOT / "results"
DATA = ROOT / "data"
TAB = RES / "tables"
TAB.mkdir(parents=True, exist_ok=True)
STRATA = ["CTRL", "EXC", "L20", "L25"]


def jl(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.exists() else []


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def guard(name: str = "prereg_hyb") -> dict:
    p, s = RES / f"{name}.json", RES / f"{name}.sha256"
    if not p.exists() or not s.exists():
        raise SystemExit(f"{name} not frozen: refusing to join labels")
    want = s.read_text().split()[0]
    if sha256_file(p) != want:
        raise SystemExit(f"{name}.json was modified after the freeze (sha256 mismatch)")
    return json.loads(p.read_text())


def nz(x) -> bool:
    return x is not None and not (isinstance(x, float) and math.isnan(x))


# ------------------------------------------------------------------------------------------------ scores (label-free)
def load_scores(pass_: str) -> dict:
    """key -> row dict from results/scores_{pass_}.jsonl (plus sentence_id / stratum)."""
    out = {}
    for s in jl(RES / f"scores_{pass_}.jsonl"):
        for r in s["rows"]:
            r["sentence_id"] = s["sentence_id"]
            r["stratum"] = s.get("stratum")
            out[r["key"]] = r
    return out


# ------------------------------------------------------------------------------------------------ E
def E_regime(L: dict, which: str) -> int | None:
    """exp 5 R_AB / R_A: llm rows, tier A/B, CORRECT/ERROR, not reading_choice (CONTESTED excluded)."""
    if L["system_class"] != "llm" or L.get("reading_choice"):
        return None
    if L["final_label"] not in ("CORRECT", "ERROR") or L["label_tier"] not in ("A", "B"):
        return None
    if which == "R_A" and L["label_tier"] != "A":
        return None
    return 1 if L["final_label"] == "ERROR" else 0


def load_E(pre5: dict | None = None) -> list[dict]:
    """All 8,507 E rows with frozen exp 5 columns, re-derived HYB columns, labels (after guard()), imputation per exp 5."""
    guard()
    pre5 = pre5 or json.loads((DATA / "exp5" / "prereg.json").read_text())
    neu = pre5["imputation"]["neutral"]
    fz = {r["row_key"]: r for r in jl(DATA / "exp5" / "per_item_E.jsonl")}
    lab = {r["row_key"]: r for r in jl(DATA / "exp5" / "E_labels.jsonl")}
    ours = load_scores("E")
    rows = []
    for k, f in fz.items():
        o = ours.get(k, {})
        L = lab[k]
        unp = f["coverage_status"] == "UNPARSEABLE"
        r = {"row_key": k, "item_id": f["item_id"], "sentence_id": f["sentence_id"], "stratum": f["stratum"],
             "strata": f["strata"], "system": f["system"], "system_class": f["system_class"], "family": f["family_vendor"],
             "prompt_variant": f["prompt_variant"], "fold_E": f["fold_E"], "coverage_status": f["coverage_status"],
             "unparseable": unp, "n_peers": o.get("n_peers"), "peer_unavailable": o.get("peer_unavailable"),
             "n_unknown_hyb": o.get("n_unknown_hyb"), "n_unknown_align": o.get("n_unknown_align"),
             "n_unknown_nf": o.get("n_unknown_nf"),
             "final_label": L["final_label"], "label_tier": L["label_tier"], "error_ops": L.get("error_ops"),
             "repair_ops": L.get("repair_ops"), "reference_status": L.get("reference_status"),
             "y_AB": E_regime(L, "R_AB"), "y_A": E_regime(L, "R_A")}
        # frozen columns (headline) + re-derived columns
        raw = {"c_align": f.get("c_score_align"), "c_nf": f.get("nf_c_score"), "g_align": f.get("g_score"),
               "g_nf": f.get("nf_g_score"), "c_hyb": o.get("c_hyb"), "g_hyb": o.get("g_hyb"),
               "c_align_re": o.get("c_align"), "c_nf_re": o.get("c_nf"), "c_nf_pairs": o.get("c_nf_pairs"),
               "p_peer_text": f.get("p_peer_text"), "p_text": f.get("p_text"), "l2_bow": f.get("l2_bow"), "l3_z3": f.get("l3_z3")}
        neutral = {"c_align": neu["c_score_align"], "c_hyb": neu["c_score_align"], "c_align_re": neu["c_score_align"],
                   "c_nf": neu["NF-anchored:c_score_nf"], "c_nf_re": neu["NF-anchored:c_score_nf"],
                   "c_nf_pairs": neu["NF-anchored:c_score_nf"], "g_align": neu["ALIGN:g_score"], "g_hyb": neu["ALIGN:g_score"],
                   "g_nf": neu["NF-anchored:g_score"], "l2_bow": neu["l2_bow"], "l3_z3": neu["l3_z3"], "p_peer_text": 0.5, "p_text": 0.5}
        for c, v in raw.items():
            if unp:
                r[c] = 1.0
            elif v is None:
                r[c] = neutral[c]
                r[c + "__imputed"] = True
            else:
                r[c] = float(v)
        for j in ("judge_local_qwen8b_disg", "judge_cheap_disg"):
            v = f.get(j)
            r[j] = 1.0 if unp else (None if v is None else float(v))
        rows.append(r)
    return rows


# ------------------------------------------------------------------------------------------------ evaluation helpers
def evaluate(rows: list[dict], metrics: list[str], y_key: str = "y", pairs: list[tuple] = (), b: int = ST.B,
             cluster: str = "sentence_id", strat_key: str = "stratum") -> dict:
    """AUROC, stratified AUROC (+ cluster-bootstrap CIs), AUPRC for each metric on the IDENTICAL row set, and paired
    Delta(AUROC) and Delta(stratified AUROC) with CIs from the same resamples."""
    for m in metrics:
        assert all(nz(r.get(m)) for r in rows), f"missing values for {m}"
    y = np.array([r[y_key] for r in rows], int)
    out = {"n": len(rows), "n_error": int(y.sum()), "n_correct": int(len(y) - y.sum()),
           "n_clusters": len({r[cluster] for r in rows}), "metrics": {}, "paired": {}}
    if len(rows) == 0 or y.sum() == 0 or y.sum() == len(y):
        out["untestable"] = True
        return out
    out["testable"] = bool(out["n_error"] >= 50 and out["n_correct"] >= 50)
    S = {m: np.array([float(r[m]) for r in rows]) for m in metrics}
    st = np.array([r.get(strat_key) or "-" for r in rows])
    bt = ST.Boot([r[cluster] for r in rows], b=b)
    ba, bs = {m: [] for m in metrics}, {m: [] for m in metrics}
    for idx in bt.idx:
        yy, ss = y[idx], st[idx]
        for m in metrics:
            ba[m].append(ST.auc_fast(yy, S[m][idx]))
            bs[m].append(ST.strat_auc(yy, S[m][idx], ss))
    for m in metrics:
        out["metrics"][m] = {"auroc": ST.auc_fast(y, S[m]), "auroc_ci": ST.ci(ba[m]), "strat_auroc": ST.strat_auc(y, S[m], st),
                             "strat_auroc_ci": ST.ci(bs[m]), "auprc": ST.auprc(y, S[m]), "prevalence": float(y.mean())}
    for a, c in pairs:
        if a in S and c in S:
            d = [x - z for x, z in zip(ba[a], ba[c])]
            ds = [x - z for x, z in zip(bs[a], bs[c])]
            out["paired"][f"{a} - {c}"] = {
                "delta_auroc": ST.auc_fast(y, S[a]) - ST.auc_fast(y, S[c]), "ci": ST.ci(d),
                "delta_strat_auroc": ST.strat_auc(y, S[a], st) - ST.strat_auc(y, S[c], st), "ci_strat": ST.ci(ds),
                "p_boot_strat_le0": float(np.mean(np.array([x for x in ds if nz(x)]) <= 0)), "n": len(rows)}
    return out


def fa_rate(vals, thr) -> float:
    """Tie-aware expected share flagged at a fractional threshold thr = (t, lam)."""
    v = np.asarray([x for x in vals], float)
    return float(ST.flag_vec(v, *thr).mean()) if len(v) else float("nan")


def boot_rate(vals, clusters, thr, b: int = ST.B) -> tuple[float, list]:
    f = ST.flag_vec(np.asarray(vals, float), *thr)
    return ST.cluster_boot_mean(f, clusters, b=b)


def fmt(x, d=3) -> str:
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "NA"
    return f"{x:.{d}f}"


def fci(c, d=3) -> str:
    if not c or c[0] is None:
        return "[NA]"
    return f"[{c[0]:.{d}f}, {c[1]:.{d}f}]"


def group(rows, key):
    g = defaultdict(list)
    for r in rows:
        g[key(r)].append(r)
    return g
