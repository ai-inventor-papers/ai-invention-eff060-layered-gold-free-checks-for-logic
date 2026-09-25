#!/usr/bin/env python3
"""STEP 6: the ONLY code that joins dataset-E labels to scores. Refuses to run unless results/prereg.sha256 exists, matches
sha256(results/prereg.json) and is OLDER than results/per_item_E.jsonl. Every analysis follows prereg.json.

Outputs: results/analysis.json, results/tables.md, results/p_tests.json, results/deviations.json
"""
from __future__ import annotations

import hashlib
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from loguru import logger
from scipy.stats import kendalltau, rankdata, spearmanr

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "results"
SD = ROOT / "data" / "screen"
B = 2000
SEED = 20260923

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(ROOT / "logs" / "analyse_E.log", rotation="30 MB", level="DEBUG")


def jl(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.exists() else []


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def guard() -> dict:
    ps, pj, pi = RES / "prereg.sha256", RES / "prereg.json", RES / "per_item_E.jsonl"
    if not ps.exists():
        raise SystemExit("REFUSED: results/prereg.sha256 missing")
    if ps.read_text().split()[0] != sha256_file(pj):
        raise SystemExit("REFUSED: prereg.json does not match prereg.sha256")
    if not pi.exists() or ps.stat().st_mtime >= pi.stat().st_mtime:
        raise SystemExit("REFUSED: per_item_E.jsonl missing or not newer than the prereg")
    return json.loads(pj.read_text())


# =================================================================================================== statistics
def auc_fast(y: np.ndarray, s: np.ndarray) -> float:
    n1 = int(y.sum())
    n0 = len(y) - n1
    if n1 == 0 or n0 == 0:
        return float("nan")
    r = rankdata(s)
    return float((r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def auprc(y, s):
    from sklearn.metrics import average_precision_score
    return float(average_precision_score(y, s)) if 0 < y.sum() < len(y) else float("nan")


def matched_fa(neg_vals, fa: float):
    """(t, lam) such that flagging s > t fully and s == t with weight lam gives EXACTLY the target FA on the negatives
    (fractional tie-breaking = expectation of randomized tie-breaking; needed when many CORRECT rows tie at the max)."""
    v = np.asarray(neg_vals, float)
    for t in sorted(set(v.tolist()), reverse=True):
        gt, ge = float(np.mean(v > t)), float(np.mean(v >= t))
        if gt <= fa <= ge:
            return float(t), ((fa - gt) / (ge - gt) if ge > gt else 0.0)
    return float(v.min()), 1.0


def flagp(x: float, t: float, lam: float) -> float:
    return 1.0 if x > t else (lam if x == t else 0.0)


class Boot:
    """Sentence-clustered bootstrap index sets (fixed seed; identical resamples for every metric on a subset)."""

    def __init__(self, sids: list[str], b: int = B, seed: int = SEED):
        self.by = defaultdict(list)
        for i, s in enumerate(sids):
            self.by[s].append(i)
        keys = sorted(self.by)
        rng = np.random.default_rng(seed)
        arr = [np.array(self.by[k]) for k in keys]
        self.idx = []
        for _ in range(b):
            pick = rng.integers(0, len(keys), len(keys))
            self.idx.append(np.concatenate([arr[j] for j in pick]))


def ci(vals):
    v = np.asarray([x for x in vals if not (isinstance(x, float) and math.isnan(x))])
    if len(v) == 0:
        return [None, None]
    return [float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))]


def delong(y, s1, s2):
    """DeLong test for paired AUROCs (secondary). Returns (delta, z, p)."""
    from scipy.stats import norm
    y = np.asarray(y)
    pos, neg = np.where(y == 1)[0], np.where(y == 0)[0]
    m, n = len(pos), len(neg)

    def comps(s):
        s = np.asarray(s, float)
        V10 = np.array([np.mean((s[i] > s[neg]) + 0.5 * (s[i] == s[neg])) for i in pos])
        V01 = np.array([np.mean((s[pos] > s[j]) + 0.5 * (s[pos] == s[j])) for j in neg])
        return V10, V01
    a10, a01 = comps(s1)
    b10, b01 = comps(s2)
    d = a10.mean() - b10.mean()
    S10 = np.cov(np.vstack([a10, b10]))
    S01 = np.cov(np.vstack([a01, b01]))
    var = (S10[0, 0] + S10[1, 1] - 2 * S10[0, 1]) / m + (S01[0, 0] + S01[1, 1] - 2 * S01[0, 1]) / n
    z = d / math.sqrt(var) if var > 0 else float("nan")
    return float(d), float(z), float(2 * (1 - norm.cdf(abs(z)))) if not math.isnan(z) else float("nan")


def evaluate(rows: list[dict], metrics: list[str], y_key: str = "y", pairs: list[tuple] = (), b: int = B) -> dict:
    """AUROC (+CI), AUPRC, prevalence for each metric and paired ΔAUROC (+CI) on the IDENTICAL row set."""
    for m in metrics:
        assert all(r.get(m) is not None for r in rows), f"missing values for {m} on the evaluation set"
    y = np.array([r[y_key] for r in rows])
    out = {"n": len(rows), "n_error": int(y.sum()), "n_correct": int(len(y) - y.sum()),
           "n_sentences": len({r["sentence_id"] for r in rows}), "metrics": {}, "paired": {}}
    if len(rows) == 0 or y.sum() == 0 or y.sum() == len(y):
        return out
    S = {m: np.array([float(r[m]) for r in rows]) for m in metrics}
    bt = Boot([r["sentence_id"] for r in rows], b=b)
    boots = {m: [] for m in metrics}
    for idx in bt.idx:
        yy = y[idx]
        for m in metrics:
            boots[m].append(auc_fast(yy, S[m][idx]))
    for m in metrics:
        out["metrics"][m] = {"auroc": auc_fast(y, S[m]), "ci": ci(boots[m]), "auprc": auprc(y, S[m]),
                             "prevalence": float(y.mean())}
    for a, c in pairs:
        if a in S and c in S:
            d = [x - z for x, z in zip(boots[a], boots[c])]
            dl = delong(y, S[a], S[c]) if len(rows) <= 6000 else (None, None, None)
            out["paired"][f"{a} - {c}"] = {"delta": auc_fast(y, S[a]) - auc_fast(y, S[c]), "ci": ci(d),
                                            "p_boot_le0": float(np.mean(np.array(d) <= 0)), "delong_z": dl[1], "delong_p": dl[2]}
    return out


# =================================================================================================== main
@logger.catch(reraise=True)
def main():
    pre = guard()
    labels = {r["row_key"]: r for r in jl(ROOT / "data" / "E_labels.jsonl")}
    items = jl(RES / "per_item_E.jsonl")
    for r in items:
        L = labels[r["row_key"]]
        r.update({"final_label": L["final_label"], "label_tier": L["label_tier"], "reading_choice": L["reading_choice"],
                  "repair_ops": L["repair_ops"], "error_ops": L["error_ops"], "gold_audit_flag": L["gold_audit_flag"],
                  "correct_not_equivalent": L["correct_not_equivalent"], "addrop_only_suspect": L["addrop_only_suspect"]})
    neutral = pre["imputation"]["neutral"]
    thr = {"fused": pre["frozen"]["fusion"]["threshold"], "text": pre["frozen"]["text_only"]["threshold"]}
    # ------------------------------------------------ metric columns (oriented: higher = error), imputation per prereg
    IMPUTE = {"peer_only": neutral.get("ALIGN:g_score"), "g_score": neutral.get("ALIGN:g_score"),
              "c_score_nf": neutral.get("ALIGN:c_score_nf"), "c_score_align": neutral.get("c_score_align"),
              "nf_g_score": neutral.get("NF-anchored:g_score"), "nf_c_score": neutral.get("NF-anchored:c_score_nf"),
              "l2_bow": neutral.get("l2_bow"), "l3_z3": neutral.get("l3_z3"), "g_score_k6": neutral.get("ALIGN:g_score"),
              "g_score_famfield": neutral.get("ALIGN:g_score"), "l1_any": 0.0, "l2_role": 0.0}
    n_imputed = Counter()
    for r in items:
        unp = r["coverage_status"] == "UNPARSEABLE"
        for c, nv in IMPUTE.items():
            if unp:
                r[c] = 1.0 if c not in ("l1_any", "l2_role") else r.get(c, 1.0) or 1.0
            elif r.get(c) is None:
                r[c] = nv
                n_imputed[c] += 1
        for c in ("p_peer_text", "p_text", "p_sensitivity"):
            if r.get(c) is None:
                r[c] = 1.0 if unp else neutral.get("fallback", 0.5)
                n_imputed[c] += 1
    CORE = ["p_peer_text", "peer_only", "p_text", "g_score", "c_score_nf", "c_score_align", "l2_bow", "l3_z3",
            "nf_g_score", "nf_c_score", "p_sensitivity", "g_score_k6", "g_score_famfield", "l1_any", "l2_role"]
    JUDGES = ["judge_local_qwen8b_disg", "judge_local_qwen8b_orig", "judge_cheap_disg", "judge_cheap_orig"]

    def regime(r, which, contested=None, topup=True):
        if r["system_class"] != "llm" or r.get("reading_choice"):
            return None
        if not topup and r["strata"].get("l25_topup_batch"):
            return None
        fl = r["final_label"]
        if fl == "CONTESTED" and contested:
            fl = contested
        if fl not in ("CORRECT", "ERROR"):
            return None
        if fl == "CONTESTED" or (r["label_tier"] not in ("A", "B") and r["final_label"] != "CONTESTED"):
            return None
        if which == "R_A" and r["label_tier"] != "A":
            return None
        return 1 if fl == "ERROR" else 0
    for r in items:
        r["y_AB"] = regime(r, "R_AB")
        r["y_A"] = regime(r, "R_A")
    A = {}
    A["coverage_imputation"] = {"n_imputed_parseable_missing": dict(n_imputed)}

    def subset(ykey, strata=None, cond=None):
        rs = [r for r in items if r.get(ykey) is not None and (strata is None or r["stratum"] in strata)]
        if cond:
            rs = [r for r in rs if cond(r)]
        return [dict(r, y=r[ykey]) for r in rs]
    long_ = ("L25", "L20", "EXC")
    SUBSETS = {"R_AB pooled": ("y_AB", None), "R_AB L25": ("y_AB", ("L25",)), "R_AB L20": ("y_AB", ("L20",)),
               "R_AB EXC": ("y_AB", ("EXC",)), "R_AB CTRL": ("y_AB", ("CTRL",)), "R_AB long (L25+L20+EXC)": ("y_AB", long_),
               "R_A pooled L20+EXC": ("y_A", ("L20", "EXC")), "R_A L20": ("y_A", ("L20",)), "R_A EXC": ("y_A", ("EXC",)),
               "R_A all strata (sign only)": ("y_A", None), "R_A L25 (sign only)": ("y_A", ("L25",)),
               "R_A CTRL (sign only)": ("y_A", ("CTRL",))}
    # ------------------------------------------------ (a) headline tables
    A["a_tables"] = {}
    for name, (yk, st) in SUBSETS.items():
        rs = subset(yk, st)
        # all core metrics on all rows of the subset
        ev = evaluate(rs, CORE, pairs=[("p_peer_text", "p_text"), ("p_peer_text", "peer_only"), ("p_peer_text", "c_score_align"),
                                       ("c_score_align", "nf_c_score"), ("g_score", "c_score_nf")])
        # judge comparisons on rows where the judge exists (identical rows for both sides)
        for j in JUDGES:
            rj = [r for r in rs if r.get(j) is not None]
            if len(rj) >= 20 and 0 < sum(r["y"] for r in rj) < len(rj):
                ej = evaluate(rj, ["p_peer_text", "p_text", "peer_only", "c_score_align", j],
                              pairs=[("p_peer_text", j), ("p_text", j), ("c_score_align", j), ("peer_only", j)])
                ev[f"vs_{j}"] = ej
            else:
                ev[f"vs_{j}"] = {"n": len(rj), "untestable": True}
        A["a_tables"][name] = ev
        logger.info(f"(a) {name}: n={ev['n']} err={ev['n_error']} fused={ev['metrics'].get('p_peer_text', {}).get('auroc')}")
    # sensitivities
    sens = {}
    for nm, kw in (("CONTESTED->CORRECT", {"contested": "CORRECT"}), ("CONTESTED->ERROR", {"contested": "ERROR"}),
                   ("without L25 top-up", {"topup": False})):
        rs = [dict(r, y=regime(r, "R_AB", **kw)) for r in items]
        rs = [r for r in rs if r["y"] is not None]
        sens[nm] = evaluate(rs, ["p_peer_text", "p_text", "peer_only", "c_score_align"], b=500)
        rj = [r for r in rs if r.get("judge_local_qwen8b_disg") is not None]
        sens[nm]["vs_local_judge"] = evaluate(rj, ["p_peer_text", "judge_local_qwen8b_disg"],
                                              pairs=[("p_peer_text", "judge_local_qwen8b_disg")], b=500)
    A["a_sensitivity"] = sens

    def crit(tab, j):
        e = tab.get(f"vs_{j}", {})
        pr = e.get("paired", {}).get(f"p_peer_text - {j}")
        return pr
    A["criteria"] = {}
    for j in ("judge_cheap_disg", "judge_local_qwen8b_disg"):
        ab = crit(A["a_tables"]["R_AB pooled"], j)
        ra = crit(A["a_tables"]["R_A pooled L20+EXC"], j)
        lg = crit(A["a_tables"]["R_AB long (L25+L20+EXC)"], j)
        n_ab = A["a_tables"]["R_AB pooled"].get(f"vs_{j}", {})
        testable = bool(ab) and min(n_ab.get("n_error", 0), n_ab.get("n_correct", 0)) >= 300
        A["criteria"][j] = {
            "testable_pooled_R_AB (>=300/class)": testable,
            "a_R_AB_CI_gt_0": bool(ab and ab["ci"][0] is not None and ab["ci"][0] > 0),
            "a_R_A_sign_gt_0": bool(ra and ra["delta"] > 0),
            "criterion_a_this_artifact": bool(testable and ab and ab["ci"][0] > 0 and ra and ra["delta"] > 0),
            "criterion_c_long_CI_gt_0": bool(lg and lg["ci"][0] is not None and lg["ci"][0] > 0),
            "delta_R_AB": ab, "delta_R_A": ra, "delta_long": lg}
    # ------------------------------------------------ (b) P1 crossover
    def err_groups(r):
        ops = r.get("error_ops") or r.get("repair_ops") or []
        g = []
        if r["label_tier"] == "A" and ops and len(ops) <= 2 and set(ops) <= {"QUANT", "SCOPE", "BIND", "SWAP", "NEG", "REV", "RESTR"}:
            g.append("STRUCT")
        if ops and set(ops) <= {"ADD", "DROP"}:
            g.append("COVERAGE")
        if r["label_tier"] == "B" and "MEANING_RENAME" in ops:
            g.append("MEANING_RENAME")
        if r.get("eqmv_medoid_eq") is True:
            g.append("PEER_ENDORSED")
        if r.get("nf_eq_medoid_nf") is True:
            g.append("PEER_ENDORSED_NF")
        return g
    P1 = {}
    for yk, nm in (("y_AB", "R_AB"), ("y_A", "R_A")):
        rs = subset(yk)
        neg = [r for r in rs if r["y"] == 0]
        res = {}
        for fa in (0.10, 0.20):
            th = {}
            for m in ("peer_only", "p_text", "p_peer_text", "c_score_align", "judge_local_qwen8b_disg"):
                vals = sorted([r[m] for r in neg if r.get(m) is not None])
                if not vals:
                    continue
                cand = sorted(set(vals))
                t = next((c for c in cand if np.mean(np.array(vals) >= c) <= fa), cand[-1] + 1e-9)
                th[m] = float(t)
            groups = defaultdict(list)
            for r in rs:
                if r["y"] == 1:
                    for g in err_groups(r):
                        groups[g].append(r)
            gres = {}
            for g, gr in groups.items():
                rec = {m: float(np.mean([r[m] >= th[m] for r in gr if r.get(m) is not None])) if th.get(m) is not None else None
                       for m in th}
                bt = Boot([r["sentence_id"] for r in gr], b=1000)
                d = [np.mean([gr[i]["peer_only"] >= th["peer_only"] for i in idx]) - np.mean([gr[i]["p_text"] >= th["p_text"] for i in idx])
                     for idx in bt.idx]
                gres[g] = {"n": len(gr), "recall": rec, "peer_minus_text": rec["peer_only"] - rec["p_text"], "ci": ci(d)}
            res[f"FA{fa:.2f}"] = {"thresholds": th, "groups": gres,
                                  "achieved_FA": {m: float(np.mean([r[m] >= th[m] for r in neg if r.get(m) is not None])) for m in th}}
        # fractional matched-FA readout (exact FA via tie weights); the verdict uses it because the deterministic
        # thresholds are degenerate for tied scores (recall 0 by construction when >FA of CORRECT rows tie at the max)
        for fa in (0.10, 0.20):
            tl = {}
            for m in ("peer_only", "p_text", "p_peer_text", "c_score_align", "judge_local_qwen8b_disg"):
                vals = [r[m] for r in neg if r.get(m) is not None]
                if vals:
                    tl[m] = matched_fa(vals, fa)
            groups = defaultdict(list)
            for r in rs:
                if r["y"] == 1:
                    for gg in err_groups(r):
                        groups[gg].append(r)
            gres = {}
            for gname, gr in groups.items():
                rec = {m: float(np.mean([flagp(r[m], *tl[m]) for r in gr if r.get(m) is not None])) for m in tl}
                fp_ = np.array([flagp(r["peer_only"], *tl["peer_only"]) for r in gr])
                ft_ = np.array([flagp(r["p_text"], *tl["p_text"]) for r in gr])
                bt = Boot([r["sentence_id"] for r in gr], b=1000)
                d = [float(fp_[idx].mean() - ft_[idx].mean()) for idx in bt.idx]
                gres[gname] = {"n": len(gr), "recall": rec, "peer_minus_text": rec["peer_only"] - rec["p_text"], "ci": ci(d)}
            res[f"FA{fa:.2f}_fractional"] = {"thresholds_lambda": tl, "groups": gres}
        res["verdict_basis"] = "FA0.10_fractional"
        g = res["FA0.10_fractional"]["groups"]
        st = g.get("STRUCT")
        txt_groups = [x for x in ("MEANING_RENAME", "PEER_ENDORSED") if x in g]
        conf = []
        rev = []
        if st:
            if st["peer_minus_text"] > 0 and st["ci"][0] is not None and st["ci"][0] > 0:
                conf.append("STRUCT")
            if st["ci"][1] is not None and st["ci"][1] < 0:
                rev.append("STRUCT")
        for x in txt_groups:
            if g[x]["ci"][1] is not None and g[x]["ci"][1] < 0:
                conf.append(x)
            if g[x]["ci"][0] is not None and g[x]["ci"][0] > 0:
                rev.append(x)
        signs_ok = bool(st and st["peer_minus_text"] > 0 and all(g[x]["peer_minus_text"] < 0 for x in txt_groups))
        verdict = "REFUTED" if rev else ("CONFIRMED" if (signs_ok and conf) else "INCONCLUSIVE")
        res["verdict"] = verdict
        gd = res["FA0.10"]["groups"]
        res["verdict_deterministic_thresholds"] = ("REFUTED" if any((gd[x]["ci"][0] or 0) > 0 for x in txt_groups if x in gd)
                                                   or (gd.get("STRUCT") and (gd["STRUCT"]["ci"][1] or 0) < 0) else "INCONCLUSIVE")
        res["ci_excluding_0_in_predicted_direction"] = conf
        res["reversals_with_ci"] = rev
        P1[nm] = res
    A["b_P1"] = P1
    # ------------------------------------------------ (c) P2
    rs = subset("y_AB")
    errs = [r for r in rs if r["y"] == 1]
    rho = spearmanr([r["peer_only"] for r in errs], [r["p_text"] for r in errs])[0]
    bt = Boot([r["sentence_id"] for r in errs], b=1000)
    rb = [spearmanr([errs[i]["peer_only"] for i in idx], [errs[i]["p_text"] for i in idx])[0] for idx in bt.idx]
    y = np.array([r["y"] for r in rs])
    corr = [r for r in rs if r["y"] == 0]

    def grp_auc(gr, m):
        sub = gr + corr
        return auc_fast(np.array([r["y"] for r in sub]), np.array([r[m] for r in sub]))
    pe = [r for r in errs if r.get("eqmv_medoid_eq") is True]
    npe = [r for r in errs if r.get("eqmv_medoid_eq") is not True]
    au = {m: auc_fast(y, np.array([r[m] for r in rs])) for m in ("p_peer_text", "peer_only", "p_text")}
    best = max(("peer_only", "p_text"), key=lambda m: au[m])
    gain = au["p_peer_text"] - au[best]
    share_pe = ((len(pe) / len(errs)) * (grp_auc(pe, "p_peer_text") - grp_auc(pe, best)) / gain) if (gain and pe) else None
    A["c_P2"] = {"spearman_peer_text_errors": float(rho), "ci": ci(rb), "auroc": au, "best_single": best, "gain": gain,
                 "n_peer_endorsed": len(pe), "n_non_endorsed": len(npe),
                 "auroc_groups": {"peer_endorsed": {m: grp_auc(pe, m) for m in au} if pe else None,
                                  "non_endorsed": {m: grp_auc(npe, m) for m in au} if npe else None},
                 "share_of_gain_from_peer_endorsed": share_pe,
                 "verdict": "CONFIRMED" if (rho < 0.4 and share_pe is not None and share_pe >= 0.5) else
                            ("REFUTED" if (rho >= 0.4 or (share_pe is not None and share_pe < 0.5)) else "INCONCLUSIVE")}
    # ------------------------------------------------ (d) P3 complexity interaction
    import statsmodels.api as sm

    def inter(rs, m, b=400):
        yv = np.array([r["y"] for r in rs], float)
        s = np.array([r[m] for r in rs], float)
        w = np.array([r["strata"]["words"] for r in rs], float)

        def fit(ix):
            zs = (s[ix] - s[ix].mean()) / (s[ix].std() or 1)
            zw = (w[ix] - w[ix].mean()) / (w[ix].std() or 1)
            X = sm.add_constant(np.column_stack([zs, zw, zs * zw]))
            try:
                return float(sm.Logit(yv[ix], X).fit(disp=0, maxiter=200).params[3])
            except Exception:  # noqa: BLE001 - separation / singular fits are skipped in the bootstrap
                return float("nan")
        full = fit(np.arange(len(rs)))
        bt = Boot([r["sentence_id"] for r in rs], b=b)
        return {"interaction": full, "ci": ci([fit(ix) for ix in bt.idx]), "B": b}
    rs = subset("y_AB")
    P3 = {"note": "B reduced to 400 for the logistic interaction bootstraps (runtime); all other CIs B=2000"}
    for m in ("c_score_align", "g_score", "nf_c_score", "nf_g_score", "p_peer_text", "p_text", "judge_local_qwen8b_disg"):
        rr = [r for r in rs if r.get(m) is not None]
        P3[m] = inter(rr, m)
    bins = [(0, 15), (15, 20), (20, 25), (25, 30), (30, 999)]
    P3["auroc_by_word_bin"] = {}
    for lo, hi in bins:
        rr = [r for r in rs if lo <= r["strata"]["words"] < hi and r.get("judge_local_qwen8b_disg") is not None]
        ny = sum(r["y"] for r in rr)
        key = f"{lo}-{hi if hi < 999 else 'inf'}"
        if ny >= 30 and len(rr) - ny >= 30:
            P3["auroc_by_word_bin"][key] = evaluate(rr, ["p_peer_text", "p_text", "peer_only", "c_score_align", "judge_local_qwen8b_disg"],
                                                    pairs=[("p_peer_text", "judge_local_qwen8b_disg")], b=500)
        else:
            P3["auroc_by_word_bin"][key] = {"n": len(rr), "n_error": ny, "untestable": True}
    # diff-in-Δ long pool minus CTRL (fused - local judge)
    rj = [r for r in rs if r.get("judge_local_qwen8b_disg") is not None]
    bt = Boot([r["sentence_id"] for r in rj], b=B)
    yj = np.array([r["y"] for r in rj])
    f_ = np.array([r["p_peer_text"] for r in rj])
    j_ = np.array([r["judge_local_qwen8b_disg"] for r in rj])
    lg = np.array([r["stratum"] in long_ for r in rj])

    def did(ix):
        ix = np.asarray(ix)
        a = ix[lg[ix]]
        c = ix[~lg[ix]]
        return (auc_fast(yj[a], f_[a]) - auc_fast(yj[a], j_[a])) - (auc_fast(yj[c], f_[c]) - auc_fast(yj[c], j_[c]))
    P3["did_long_minus_ctrl_fused_vs_local_judge"] = {"did": did(np.arange(len(rj))), "ci": ci([did(ix) for ix in bt.idx])}
    cs = P3["c_score_align"]
    P3["verdict"] = ("CONFIRMED" if (cs["ci"][1] is not None and cs["ci"][1] < 0 and abs(P3["g_score"]["interaction"]) <= 0.5 * abs(cs["interaction"])
                                     and P3["did_long_minus_ctrl_fused_vs_local_judge"]["did"] > 0) else
                     ("REFUTED" if (cs["ci"][0] is not None and cs["ci"][0] > 0) else "INCONCLUSIVE"))
    P3["verdict_note"] = "F1 failed: the rule is applied to the aligner c_score (c_score_align) and ALIGN g; NF columns descriptive"
    A["d_P3"] = P3
    # ------------------------------------------------ (e) P4 invariance on the shared rewrite set (screen pools)
    A["e_P4"] = p4_invariance(pre)
    # ------------------------------------------------ (f) error types
    A["f_error_types"] = error_types(items)
    # ------------------------------------------------ (g) system level
    A["g_system"] = system_level(items)
    # ------------------------------------------------ (h) complexity bins
    A["h_complexity"] = complexity(items, thr)
    # ------------------------------------------------ (i) contamination
    A["i_contamination"] = contamination(items)
    # ------------------------------------------------ (j) coverage & cost
    A["j_coverage_cost"] = coverage_cost(items)
    # ------------------------------------------------ (k) misc
    A["k_misc"] = misc(items, thr)
    # ------------------------------------------------ placebo
    rs = subset("y_AB")
    rng = np.random.default_rng(SEED)
    pl = defaultdict(list)
    strata_idx = defaultdict(list)
    for i, r in enumerate(rs):
        strata_idx[r["stratum"]].append(i)
    y0 = np.array([r["y"] for r in rs])
    for _ in range(200):
        yy = y0.copy()
        for ix in strata_idx.values():
            yy[ix] = rng.permutation(yy[ix])
        for m in ("p_peer_text", "p_text", "peer_only", "c_score_align"):
            pl[m].append(auc_fast(yy, np.array([r[m] for r in rs])))
    A["placebo_within_stratum"] = {m: {"mean": float(np.mean(v)), "p97.5": float(np.percentile(v, 97.5))} for m, v in pl.items()}
    A["placebo_within_stratum"]["note"] = ("labels permuted WITHIN stratum keep the stratum-prevalence x stratum-score-level association, "
                                          "so the mean is the between-stratum (composition) part of the pooled AUROC, not 0.5")
    gl = defaultdict(list)
    for _ in range(200):
        yy = rng.permutation(y0)
        for m in ("p_peer_text", "p_text", "peer_only", "judge_local_qwen8b_disg"):
            gl[m].append(auc_fast(yy, np.array([r[m] for r in rs])))
    A["placebo_global_shuffle"] = {m: {"mean": float(np.mean(v)), "p97.5": float(np.percentile(v, 97.5))} for m, v in gl.items()}
    # stratified AUROC: only within-stratum (error, correct) pairs count; removes the composition confound of pooled AUROC
    def strat_auc(rr, m):
        num = den = 0.0
        for st in ("L25", "L20", "EXC", "CTRL"):
            sub = [r for r in rr if r["stratum"] == st]
            yv = np.array([r["y"] for r in sub])
            n1, n0 = int(yv.sum()), int(len(yv) - yv.sum())
            if n1 and n0:
                num += auc_fast(yv, np.array([r[m] for r in sub])) * n1 * n0
                den += n1 * n0
        return num / den if den else float("nan")
    A["a_stratified"] = {}
    for name, (yk, stt) in (("R_AB pooled", ("y_AB", None)), ("R_AB long (L25+L20+EXC)", ("y_AB", long_)),
                            ("R_A pooled L20+EXC", ("y_A", ("L20", "EXC")))):
        rr = [r for r in subset(yk, stt) if r.get("judge_local_qwen8b_disg") is not None]
        bt = Boot([r["sentence_id"] for r in rr], b=1000)
        mets = ["p_peer_text", "p_text", "peer_only", "c_score_align", "nf_c_score", "l2_bow", "l3_z3", "judge_local_qwen8b_disg"]
        full = {m: strat_auc(rr, m) for m in mets}
        bs = {m: [] for m in mets}
        for ix in bt.idx:
            sub = [rr[i] for i in ix]
            for m in mets:
                bs[m].append(strat_auc(sub, m))
        A["a_stratified"][name] = {"n": len(rr), "stratified_auroc": {m: {"auroc": full[m], "ci": ci(bs[m])} for m in mets},
                                   "delta_fused_minus_local_judge": {"delta": full["p_peer_text"] - full["judge_local_qwen8b_disg"],
                                                                     "ci": ci([a - b for a, b in zip(bs["p_peer_text"], bs["judge_local_qwen8b_disg"])])},
                                   "delta_text_minus_local_judge": {"delta": full["p_text"] - full["judge_local_qwen8b_disg"],
                                                                    "ci": ci([a - b for a, b in zip(bs["p_text"], bs["judge_local_qwen8b_disg"])])},
                                   "delta_fused_minus_c_score_align": {"delta": full["p_peer_text"] - full["c_score_align"],
                                                                       "ci": ci([a - b for a, b in zip(bs["p_peer_text"], bs["c_score_align"])])},
                                   "note": "B=1000; within-stratum pairs only (strata L25/L20/EXC/CTRL), weights n_err x n_cor"}
    (RES / "analysis.json").write_text(json.dumps(A, indent=1, default=float))
    p_tests = {"P1_R_AB": A["b_P1"]["R_AB"]["verdict"], "P1_R_A": A["b_P1"]["R_A"]["verdict"], "P2": A["c_P2"]["verdict"],
               "P3": A["d_P3"]["verdict"], "P4": A["e_P4"]["verdict"], "criteria": {k: {kk: vv for kk, vv in v.items() if not kk.startswith("delta")}
                                                                                   for k, v in A["criteria"].items()}}
    (RES / "p_tests.json").write_text(json.dumps(p_tests, indent=1, default=float))
    write_tables(A, pre)
    logger.info(f"P-tests {json.dumps(p_tests, default=float)}")


# =================================================================================================== helpers
def p4_invariance(pre):
    rows = {r["key"]: r for r in jl(RES / "rewrite_scores_pt.jsonl")}
    labs = json.loads((SD / "screen_adjudicated_labels.json").read_text())
    inv = {r["rw_id"]: r for r in json.loads((ROOT / "data" / "invariance_items.json").read_text())}
    # per-metric thresholds at FA 0.10 on the screen AGREE track-L CORRECT items (same rule as the selection rule)
    sys.path.insert(0, str(ROOT / "src"))
    from screen_fit import adj_label, solver_label, thr_at_fa
    items = {x["item_id"]: x for x in json.loads((SD / "screen_items.json").read_text())}
    agree_L_c = [i for i, v in labs.items() if i in rows and v["track"] == "L" and adj_label(v) == "CORRECT"
                 and solver_label(v["auto_label"]) == "CORRECT"]
    mets = {"g_score": "g_score", "c_score_align": "c_score_align", "nf_g": "NF-anchored:g_score", "l2_bow": "l2_bow",
            "l3_z3": "l3_z3", "fused": "p_peer_text"}
    th = {}
    for m, c in mets.items():
        vals = [rows[i][c] for i in agree_L_c if rows[i].get(c) is not None]
        th[m] = thr_at_fa(vals, 0.10) if vals else None
    th["fused"] = pre["frozen"]["fusion"]["threshold"]
    tl = {}
    for m, c in mets.items():
        vals = [rows[i][c] for i in agree_L_c if rows[i].get(c) is not None]
        tl[m] = matched_fa(vals, 0.10) if vals else None
    tl["fused"] = (th["fused"], 1.0)

    def flag(r, m):  # fractional matched-FA flag (exact screen FA 0.10; the frozen fusion threshold for 'fused')
        v = r.get(mets[m])
        return 1.0 if v is None else flagp(v, *tl[m])
    jd = {r["rw_id"]: r for r in jl(SD / "expD_rewrite_scores.jsonl")}
    jb = {r["item_id"]: r for r in jl(SD / "expD_per_item_scores.jsonl")}
    fam = defaultdict(lambda: defaultdict(list))
    for k, r in rows.items():
        if not k.startswith("RW:"):
            continue
        rw = inv.get(k[3:])
        if not rw or labs.get(rw["base_item_id"], {}).get("final_label") != "CORRECT" or rw["base_item_id"] not in rows:
            continue
        base = rows[rw["base_item_id"]]
        for m in mets:
            fam[rw["family"]][m].append((flag(r, m), flag(base, m)))
        j = jd.get(k[3:])
        b = jb.get(rw["base_item_id"])
        if j and j.get("judge_cheap_disg") is not None and b and b.get("oriented_scores", {}).get("judge_cheap_disg") is not None:
            fam[rw["family"]]["judge_cheap_disg"].append(((1 - j["judge_cheap_disg"]) >= 0.5, b["oriented_scores"]["judge_cheap_disg"] >= 0.5))
        if j and j.get("judge_local_qwen8b_disg") is not None and b and b.get("oriented_scores", {}).get("judge_local_qwen8b_disg") is not None:
            fam[rw["family"]]["judge_local_qwen8b_disg"].append(((1 - j["judge_local_qwen8b_disg"]) >= 0.5,
                                                                 b["oriented_scores"]["judge_local_qwen8b_disg"] >= 0.5))
    table = {f: {m: {"n": len(v), "FA": float(np.mean([a for a, _ in v])), "flip": float(np.mean([abs(float(a) - float(c)) for a, c in v])),
                     "base_flag_rate": float(np.mean([c for _, c in v]))} for m, v in d.items()} for f, d in fam.items()}
    probes = defaultdict(lambda: defaultdict(list))
    for k, r in rows.items():
        if k.startswith("PR:"):
            p = k.split(":")[1]
            for m in mets:
                probes[p][m].append(flag(r, m))
    ptab = {p: {m: {"n": len(v), "recall": float(np.mean(v))} for m, v in d.items()} for p, d in probes.items()}
    fused_ok = all(t.get("fused", {}).get("FA", 1) <= 0.10 for t in table.values())
    judge_bad = any(max(t.get("judge_cheap_disg", {}).get("FA", 0), t.get("judge_local_qwen8b_disg", {}).get("FA", 0)) >= 0.25
                    for t in table.values())
    return {"thresholds": th, "thresholds_fractional": tl, "flag_rule": "fractional matched FA 0.10 on screen AGREE track-L CORRECT (fused: frozen threshold)", "families": table, "probes": ptab, "fused_FA_le_0.10_every_family": fused_ok,
            "a_judge_FA_ge_0.25_somewhere": judge_bad,
            "verdict": "CONFIRMED" if (fused_ok and judge_bad) else ("REFUTED" if not fused_ok else "INCONCLUSIVE")}


def error_types(items):
    rs = [r for r in items if r.get("y_A") == 1 and r.get("repair_ops") and 1 <= len(r["repair_ops"]) <= 2]
    codable = {"NEG", "QUANT", "SWAP", "DROP", "ADD"}
    acc = [r["top_code"] in r["repair_ops"] if r.get("top_code") else False for r in rs]
    rc = [r for r in rs if set(r["repair_ops"]) <= codable]
    acc_c = [r["top_code"] in r["repair_ops"] for r in rc]
    pred = Counter(r.get("top_code") for r in rs)
    tot = sum(pred.values())
    chance = float(np.mean([sum(pred[c] / tot for c in set(r["repair_ops"]) if c in pred) for r in rs])) if rs else None
    conf = defaultdict(Counter)
    for r in rs:
        conf["+".join(sorted(r["repair_ops"]))][r.get("top_code")] += 1
    med = [set(r.get("medoid_ops") or []) == set(r["repair_ops"]) for r in rs if r.get("medoid_ops") is not None]
    judge = {}
    for j in ("judge_local_qwen8b_disg_type", "judge_cheap_disg_type"):
        v = [r[j] in r["repair_ops"] for r in rs if r.get(j)]
        judge[j] = {"n": len(v), "acc": float(np.mean(v)) if v else None}
    nf = [r.get("nf_top_code") in r["repair_ops"] for r in rs if r.get("nf_top_code")]
    alle = [r for r in items if r.get("y_A") == 1 and r.get("repair_ops")]
    ops = Counter(o for r in alle for o in r["repair_ops"])
    pol = sum(ops[o] for o in ("NEG", "REV", "QUANT"))
    cov = sum(ops[o] for o in ("ADD", "DROP"))
    return {"n": len(rs), "top_code_accuracy": float(np.mean(acc)) if acc else None,
            "n_codable": len(rc), "top_code_accuracy_codable": float(np.mean(acc_c)) if acc_c else None,
            "chance_marginal": chance, "pred_code_distribution": dict(pred),
            "confusion": {k: dict(v) for k, v in conf.items()}, "medoid_ops_exact_agreement": float(np.mean(med)) if med else None,
            "judge_error_type_agreement": judge, "nf_top_code_accuracy": float(np.mean(nf)) if nf else None,
            "census_R_A_ops": dict(ops), "share_polarity_ops": pol / max(1, sum(ops.values())),
            "share_coverage_ops": cov / max(1, sum(ops.values()))}


def system_level(items):
    rs = [r for r in items if r.get("y_AB") is not None]
    out = {}
    for level in ("system_variant", "family"):
        key = (lambda r: f"{r['system']}|{r['prompt_variant']}") if level == "system_variant" else (lambda r: r["family_vendor"])
        groups = defaultdict(list)
        for r in rs:
            groups[key(r)].append(r)
        names = sorted(groups)
        mets = ["p_peer_text", "p_text", "peer_only", "judge_local_qwen8b_disg", "judge_cheap_disg"]

        def taus(rows_by):
            er = [np.mean([r["y_AB"] for r in rows_by[n]]) for n in names]
            res = {}
            for m in mets:
                mv = [np.mean([r[m] for r in rows_by[n] if r.get(m) is not None]) if any(r.get(m) is not None for r in rows_by[n]) else np.nan
                      for n in names]
                ok = [(a, b) for a, b in zip(er, mv) if not np.isnan(b)]
                res[m] = kendalltau([a for a, _ in ok], [b for _, b in ok])[0] if len(ok) >= 4 else np.nan
            return res, er
        full, er = taus(groups)
        sids = sorted({r["sentence_id"] for r in rs})
        rng = np.random.default_rng(SEED)
        by_s = defaultdict(list)
        for r in rs:
            by_s[r["sentence_id"]].append(r)
        boots = defaultdict(list)
        for _ in range(500):
            pick = rng.choice(len(sids), len(sids))
            g2 = defaultdict(list)
            for j in pick:
                for r in by_s[sids[j]]:
                    g2[key(r)].append(r)
            if set(g2) != set(names):
                continue
            t, _ = taus(g2)
            for m, v in t.items():
                boots[m].append(v)
        out[level] = {"n_groups": len(names), "groups": {n: {"n": len(groups[n]), "error_rate": float(e)} for n, e in zip(names, er)},
                      "kendall_tau_b": {m: {"tau": float(v), "ci": ci(boots[m])} for m, v in full.items()},
                      "note": "descriptive only (13 system x variant rows / 9 families)"}
    return out


def complexity(items, thr):
    rs = [r for r in items if r.get("y_AB") is not None]
    out = {}
    specs = {"words": [(0, 12), (12, 20), (20, 25), (25, 30), (30, 999)], "n_quant": [(0, 1), (1, 2), (2, 3), (3, 99)],
             "depth": [(0, 4), (4, 6), (6, 8), (8, 99)], "n_conditions": [(0, 2), (2, 3), (3, 4), (4, 99)]}
    mets = ["p_peer_text", "peer_only", "p_text", "judge_local_qwen8b_disg", "judge_cheap_disg"]
    for var, bins in list(specs.items()) + [("exception_type", None)]:
        res = {}
        keys = bins if bins else sorted({str(r["strata"].get("exception_type")) for r in rs})
        for b in keys:
            if bins:
                rr = [r for r in rs if r["strata"].get(var) is not None and b[0] <= r["strata"][var] < b[1]]
                name = f"{b[0]}-{b[1] if b[1] < 99 else 'inf'}"
            else:
                rr = [r for r in rs if str(r["strata"].get("exception_type")) == b]
                name = b
            ny = sum(r["y_AB"] for r in rr)
            if ny < 30 or len(rr) - ny < 30:
                res[name] = {"n": len(rr), "n_error": ny, "untestable": True}
                continue
            y = np.array([r["y_AB"] for r in rr])
            d = {"n": len(rr), "n_error": int(ny)}
            for m in mets:
                sub = [r for r in rr if r.get(m) is not None]
                if len(sub) >= 30 and 0 < sum(r["y_AB"] for r in sub) < len(sub):
                    ys = np.array([r["y_AB"] for r in sub])
                    d[m] = {"auroc": auc_fast(ys, np.array([r[m] for r in sub])), "n": len(sub)}
            d["FA_fused_at_frozen_thr"] = float(np.mean([r["p_peer_text"] >= thr["fused"] for r in rr if r["y_AB"] == 0]))
            d["recall_fused_at_frozen_thr"] = float(np.mean([r["p_peer_text"] >= thr["fused"] for r in rr if r["y_AB"] == 1]))
            res[name] = d
        out[var] = res
    return out


def contamination(items):
    rs = [r for r in items if r.get("y_AB") is not None]
    out = {}
    for base in ("judge_local_qwen8b", "judge_cheap"):
        rr = [dict(r, y=r["y_AB"]) for r in rs if r.get(f"{base}_orig") is not None and r.get(f"{base}_disg") is not None]
        if len(rr) < 50:
            out[base] = {"n": len(rr), "untestable": True}
            continue
        ev = evaluate(rr, [f"{base}_orig", f"{base}_disg"], pairs=[(f"{base}_orig", f"{base}_disg")])
        pr = ev["paired"][f"{base}_orig - {base}_disg"]
        se = (pr["ci"][1] - pr["ci"][0]) / (2 * 1.96)
        out[base] = {"n": ev["n"], "auroc_orig": ev["metrics"][f"{base}_orig"], "auroc_disg": ev["metrics"][f"{base}_disg"],
                     "orig_minus_disg": pr, "MDE_2.8SE": 2.8 * se}
    rr = [dict(r, y=r["y_AB"]) for r in rs if r.get("l3_z3_disg") is not None and r["coverage_status"] != "UNPARSEABLE"]
    out["l3"] = {"n": len(rr), "untestable": True, "reason": "disguised L3 questionnaires need the OpenRouter key"} if len(rr) < 50 else \
        evaluate(rr, ["l3_z3", "l3_z3_disg"], pairs=[("l3_z3", "l3_z3_disg")])
    out["note"] = "PEER signals never see text or names from the benchmark prompt, so they have no contamination channel; the fused " \
                  "score's only LLM component is the L3 questionnaire (text only)."
    return out


def coverage_cost(items):
    out = {"n_rows": len(items), "coverage_status": dict(Counter(r["coverage_status"] for r in items)),
           "peer_unavailable": sum(bool(r.get("peer_unavailable")) for r in items),
           "n_unknown_gt0_share": float(np.mean([(r.get("n_unknown") or 0) > 0 for r in items if r["coverage_status"] == "OK"])),
           "l3_missing": sum(r.get("l3_z3") is None and r["coverage_status"] == "OK" for r in items),
           "judge_cheap_disg_present": sum(r.get("judge_cheap_disg") is not None for r in items),
           "judge_local_disg_present": sum(r.get("judge_local_qwen8b_disg") is not None for r in items)}
    by = defaultdict(list)
    for r in items:
        by[r["stratum"]].append(r)
    out["per_stratum"] = {}
    for s, rr in by.items():
        ok = [r for r in rr if r["coverage_status"] == "OK"]
        out["per_stratum"][s] = {"n": len(rr), "unparseable": sum(r["coverage_status"] == "UNPARSEABLE" for r in rr),
                                 "median_secs_pairs": float(np.median([r["secs_pairs"] or 0 for r in ok])) if ok else None,
                                 "median_secs_text": float(np.median([r["secs_text"] or 0 for r in ok])) if ok else None,
                                 "median_sentence_secs": float(np.median([r["secs_sentence_total"] or 0 for r in ok])) if ok else None,
                                 "mean_cost_usd_peer_text": float(np.mean([r["cost_usd_peer_text"] for r in rr])),
                                 "mean_judge_cost_usd": float(np.mean([r["judge_cost_usd"] for r in rr]))}
    ok = [r for r in items if r["coverage_status"] == "OK"]
    out["mean_cpu_secs_per_row"] = {"peer_pairs": float(np.mean([r["secs_pairs"] or 0 for r in ok])),
                                    "nf_pairs": float(np.mean([r.get("nf_secs_pairs") or 0 for r in ok])),
                                    "text": float(np.mean([r["secs_text"] or 0 for r in ok]))}
    out["mean_usd_per_row"] = {"peer_text_L3_share": float(np.mean([r["cost_usd_peer_text"] for r in items])),
                               "judge_cheap_orig+disg": float(np.mean([r["judge_cost_usd"] for r in items if r["judge_cost_usd"]]))
                               if any(r["judge_cost_usd"] for r in items) else None}
    return out


def misc(items, thr):
    gold = [r for r in items if r["system_class"] == "reference_gold_as_system" and r["final_label"] in ("CORRECT", "ERROR")]
    out = {}
    if gold:
        y = np.array([1 if r["final_label"] == "ERROR" else 0 for r in gold])
        out["gold_as_system"] = {"n": len(gold), "panel_reject_rate": float(y.mean()),
                                 "fused_flag_rate": float(np.mean([r["p_peer_text"] >= thr["fused"] for r in gold])),
                                 "auroc_vs_panel_gold_audit": {m: auc_fast(y, np.array([r[m] for r in gold]))
                                                               for m in ("p_peer_text", "p_text", "peer_only", "c_score_align")}}
        gj = [r for r in gold if r.get("judge_local_qwen8b_disg") is not None]
        if gj:
            yj = np.array([1 if r["final_label"] == "ERROR" else 0 for r in gj])
            out["gold_as_system"]["auroc_vs_panel_gold_audit"]["judge_local_qwen8b_disg"] = auc_fast(yj, np.array([r["judge_local_qwen8b_disg"] for r in gj]))
    for tier in ("A", "B"):
        c = [r for r in items if r.get("y_AB") == 0 and r["label_tier"] == tier]
        out[f"FA_fused_tier_{tier}_CORRECT"] = {"n": len(c), "FA": float(np.mean([r["p_peer_text"] >= thr["fused"] for r in c])) if c else None,
                                                "FA_text": float(np.mean([r["p_text"] >= thr["text"] for r in c])) if c else None,
                                                "mean_p": float(np.mean([r["p_peer_text"] for r in c])) if c else None}
    err = [r for r in items if r.get("y_AB") == 1]
    out["recall_fused_at_frozen_thr_R_AB"] = float(np.mean([r["p_peer_text"] >= thr["fused"] for r in err])) if err else None
    cr = [r for r in items if r.get("y_AB") == 0]
    out["FA_fused_at_frozen_thr_R_AB"] = float(np.mean([r["p_peer_text"] >= thr["fused"] for r in cr])) if cr else None
    prev = len(err) / max(1, len(err) + len(cr))
    tp, fp = out["recall_fused_at_frozen_thr_R_AB"] or 0, out["FA_fused_at_frozen_thr_R_AB"] or 0
    out["precision_fused_at_frozen_thr_R_AB"] = (tp * prev) / (tp * prev + fp * (1 - prev)) if (tp or fp) else None
    out["note"] = "threshold-based numbers carry the screen->E scale shift (frozen on short screen sentences)"
    return out


def fmt(x, d=3):
    return "—" if x is None or (isinstance(x, float) and math.isnan(x)) else f"{x:.{d}f}"


def write_tables(A, pre):
    L = ["# Dataset E results (PEER+TEXT, frozen on the screen; prereg sha256 " + (RES / "prereg.sha256").read_text().split()[0][:12] + ")", ""]
    L.append("## (a) Item-level AUROC [95% sentence-cluster bootstrap CI], identical rows per table")
    L.append("")
    L.append("| subset | n (err/cor) | PEER+TEXT | TEXT | PEER (ALIGN g) | c_score_align | NF c_score | NF g | L2-bow | L3 |")
    L.append("|---|---|---|---|---|---|---|---|---|---|")
    for name, ev in A["a_tables"].items():
        m = ev.get("metrics", {})
        cell = lambda k: (f"{fmt(m[k]['auroc'])} [{fmt(m[k]['ci'][0], 2)}, {fmt(m[k]['ci'][1], 2)}]" if k in m else "—")
        L.append(f"| {name} | {ev['n']} ({ev['n_error']}/{ev['n_correct']}) | {cell('p_peer_text')} | {cell('p_text')} | {cell('peer_only')} | "
                 f"{cell('c_score_align')} | {cell('nf_c_score')} | {cell('nf_g_score')} | {cell('l2_bow')} | {cell('l3_z3')} |")
    L.append("")
    L.append("## (a) Paired ΔAUROC vs the judges (rows where the judge score exists)")
    L.append("")
    L.append("| subset | judge | n (err/cor) | judge AUROC | Δ PEER+TEXT − judge [CI] | Δ TEXT − judge [CI] | DeLong p |")
    L.append("|---|---|---|---|---|---|---|")
    for name, ev in A["a_tables"].items():
        for j in ("judge_local_qwen8b_disg", "judge_cheap_disg"):
            e = ev.get(f"vs_{j}", {})
            if e.get("untestable") or "paired" not in e:
                L.append(f"| {name} | {j} | {e.get('n', 0)} | untestable | | | |")
                continue
            p1 = e["paired"].get(f"p_peer_text - {j}")
            p2 = e["paired"].get(f"p_text - {j}")
            L.append(f"| {name} | {j} | {e['n']} ({e['n_error']}/{e['n_correct']}) | {fmt(e['metrics'][j]['auroc'])} | "
                     f"{fmt(p1['delta'])} [{fmt(p1['ci'][0])}, {fmt(p1['ci'][1])}] | {fmt(p2['delta'])} [{fmt(p2['ci'][0])}, {fmt(p2['ci'][1])}] | "
                     f"{fmt(p1.get('delong_p'), 4)} |")
    L.append("")
    L.append("## (a') Stratified AUROC (within-stratum pairs only; removes the stratum-composition confound) [B=1000 CI]")
    L.append("")
    L.append("| subset | n | PEER+TEXT | TEXT | PEER | c_score_align | NF c_score | local judge | Δ PEER+TEXT − judge [CI] | Δ PEER+TEXT − c_score_align [CI] |")
    L.append("|---|---|---|---|---|---|---|---|---|---|")
    for name, d in A["a_stratified"].items():
        sa = d["stratified_auroc"]
        c1 = d["delta_fused_minus_local_judge"]
        c2 = d["delta_fused_minus_c_score_align"]
        L.append(f"| {name} | {d['n']} | " + " | ".join(fmt(sa[m]["auroc"]) for m in ("p_peer_text", "p_text", "peer_only", "c_score_align", "nf_c_score", "judge_local_qwen8b_disg")) +
                 f" | {fmt(c1['delta'])} [{fmt(c1['ci'][0])}, {fmt(c1['ci'][1])}] | {fmt(c2['delta'])} [{fmt(c2['ci'][0])}, {fmt(c2['ci'][1])}] |")
    L.append("")
    L.append("Placebos: within-stratum label permutation " + json.dumps({k: round(v["mean"], 3) for k, v in A["placebo_within_stratum"].items() if isinstance(v, dict)}) +
             " (composition part of pooled AUROC); global shuffle " + json.dumps({k: round(v["mean"], 3) for k, v in A["placebo_global_shuffle"].items()}))
    L.append("")
    L.append("## Criteria")
    L.append("```")
    L.append(json.dumps({k: {kk: vv for kk, vv in v.items() if not kk.startswith("delta")} for k, v in A["criteria"].items()}, indent=1, default=float))
    L.append("```")
    L.append("")
    L.append("## P-tests")
    for k, v in (("P1 R_AB", A["b_P1"]["R_AB"]["verdict"]), ("P1 R_A", A["b_P1"]["R_A"]["verdict"]), ("P2", A["c_P2"]["verdict"]),
                 ("P3", A["d_P3"]["verdict"]), ("P4", A["e_P4"]["verdict"])):
        L.append(f"- **{k}**: {v}")
    L.append("")
    L.append("### P1 recall by error group at matched FA 0.10 (R_AB; fractional tie-breaking = exact FA; deterministic thresholds are degenerate for tied scores)")
    L.append("")
    L.append("| group | n | PEER | TEXT | PEER+TEXT | c_score_align | local judge | PEER−TEXT [CI] |")
    L.append("|---|---|---|---|---|---|---|---|")
    for g, d in A["b_P1"]["R_AB"]["FA0.10_fractional"]["groups"].items():
        r = d["recall"]
        L.append(f"| {g} | {d['n']} | {fmt(r.get('peer_only'))} | {fmt(r.get('p_text'))} | {fmt(r.get('p_peer_text'))} | "
                 f"{fmt(r.get('c_score_align'))} | {fmt(r.get('judge_local_qwen8b_disg'))} | {fmt(d['peer_minus_text'])} [{fmt(d['ci'][0])}, {fmt(d['ci'][1])}] |")
    L.append("")
    c = A["c_P2"]
    L.append(f"### P2: Spearman(PEER, TEXT) among errors = {fmt(c['spearman_peer_text_errors'])} [{fmt(c['ci'][0])}, {fmt(c['ci'][1])}]; "
             f"gain over best single ({c['best_single']}) = {fmt(c['gain'])}; share from peer-endorsed = {fmt(c['share_of_gain_from_peer_endorsed'])}")
    L.append("")
    L.append("### P3: complexity interaction z(score)·z(words) (logistic, cluster bootstrap)")
    for m in ("c_score_align", "g_score", "nf_c_score", "nf_g_score", "p_peer_text", "p_text", "judge_local_qwen8b_disg"):
        d = A["d_P3"][m]
        L.append(f"- {m}: {fmt(d['interaction'])} [{fmt(d['ci'][0])}, {fmt(d['ci'][1])}]")
    dd = A["d_P3"]["did_long_minus_ctrl_fused_vs_local_judge"]
    L.append(f"- diff-in-Δ (long − CTRL) of PEER+TEXT − local judge: {fmt(dd['did'])} [{fmt(dd['ci'][0])}, {fmt(dd['ci'][1])}]")
    L.append("")
    L.append("### P4: rewrite false alarms on CORRECT bases (screen pools)")
    L.append("")
    fams = A["e_P4"]["families"]
    ms = ["fused", "g_score", "c_score_align", "nf_g", "l2_bow", "l3_z3", "judge_cheap_disg", "judge_local_qwen8b_disg"]
    L.append("| family | n | " + " | ".join(ms) + " |")
    L.append("|---|---|" + "---|" * len(ms))
    for f, d in fams.items():
        n = max(v["n"] for v in d.values())
        L.append(f"| {f} | {n} | " + " | ".join(fmt(d.get(m, {}).get("FA")) for m in ms) + " |")
    L.append("")
    L.append("Probe recall (synthetic, descriptive): " + json.dumps({p: {m: round(v["recall"], 3) for m, v in d.items()} for p, d in A["e_P4"]["probes"].items()}))
    L.append("")
    f = A["f_error_types"]
    L.append(f"### (f) Error typing on R_A errors with 1-2 ops (n={f['n']}): top-code accuracy {fmt(f['top_code_accuracy'])} "
             f"(codable-only {fmt(f['top_code_accuracy_codable'])}, n={f['n_codable']}); chance {fmt(f['chance_marginal'])}; "
             f"medoid_ops exact {fmt(f['medoid_ops_exact_agreement'])}; judge types {json.dumps(f['judge_error_type_agreement'])}")
    L.append("")
    g = A["g_system"]["system_variant"]["kendall_tau_b"]
    L.append("### (g) System level (13 system × variant rows, descriptive): Kendall τ-b vs R_AB error rate: " +
             ", ".join(f"{m} {fmt(v['tau'])} [{fmt(v['ci'][0])}, {fmt(v['ci'][1])}]" for m, v in g.items()))
    L.append("")
    L.append("### (i) Contamination")
    L.append("```")
    L.append(json.dumps(A["i_contamination"], indent=1, default=float)[:3000])
    L.append("```")
    L.append("### (j) Coverage and cost")
    L.append("```")
    L.append(json.dumps(A["j_coverage_cost"], indent=1, default=float)[:3000])
    L.append("```")
    L.append("### (k) Misc")
    L.append("```")
    L.append(json.dumps(A["k_misc"], indent=1, default=float)[:3000])
    L.append("```")
    (RES / "tables.md").write_text("\n".join(L))


if __name__ == "__main__":
    main()
