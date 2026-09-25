"""STAGE 7: the ONLY place labels are joined to scores.

Primary: track L, label in {CORRECT, ERROR}. Secondary: ERROR u UNCERTAIN(COMPOUND) vs CORRECT; ERROR minus pure ADD+DROP
(atom substitution, the dominant vocabulary artefact) vs CORRECT; track H (OOF) separately; READING_CHOICE never pooled.
Item-level AUROC / AUPRC with sentence-clustered bootstrap (B=2000), paired ΔAUROC on the same resamples, binary-layer
TPR/FPR/precision (+ re-weighted to 10%/25% prevalence), tie-aware pairwise accuracy acc_eq with tie calibration
(Deutsch, Foster & Freitag 2023; ε chosen on track H), L1 per system × length false alarms, per-operator sensitivity,
error-type readout, invariance, coverage, complexity strata, cost, and the strategy's gates.
"""
from __future__ import annotations

import json
import math
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from loguru import logger
from sklearn.metrics import average_precision_score, roc_auc_score

OPS = ["NEG", "REV", "QUANT", "RESTR", "CONN", "MOVE", "DROP", "ADD", "SWAP", "BIND", "SCOPE", "UNGLUE", "COMPOUND"]
SCORES = ["l1_any", "n_smells", "l2_bow", "l2_role", "l3_score", "p_fused_H", "p_fused_Hall", "p_fused_Lcf",
          "cascade_llmformula", "l3_score_llmformula", "l3_score_local"]
PARTIAL = {"cascade_llmformula", "l3_score_llmformula", "l3_score_local"}  # decomposed-judge ablation: may cover only a subset
BINARY = {"l1_any": "l1_any", "l2_bow_flag": "bow_flag", "l2_role_flag": "role_flag", "l3_flag": "l3_flag",
          "fused_flag": "fused_flag", "l1_or_l2": None}


def _norm(t):
    import re
    t = t.lower().replace("’", "'")
    t = re.sub(r"(\w)'(\w)", r"\1\2", t)
    t = re.sub(r"[^\w\s]", " ", t)
    return " ".join(t.split())


def wilson(k, n, z=1.96):
    if n == 0:
        return [None, None]
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [round(max(0.0, c - h), 4), round(min(1.0, c + h), 4)]


def score_value(s: dict, name: str):
    if not (s.get("parse_ok") and s.get("cpu_status") == "OK"):
        return None
    if name == "l2_bow":
        return (s.get("bow_n_unanch") or 0) + (s.get("bow_uncarried") or 0.0)
    if name == "l2_role":
        return s.get("role_count")
    if name == "cascade_llmformula":
        return s.get("p_cascade_llmformula")
    if name == "p_fused_Lcf":
        return s.get("p_fused_Lcf")
    if name == "l3_score_llmformula":
        return s.get("l3_score_llmformula") if s.get("dj_status") == "OK" else None
    if name == "l3_score":
        return s.get("l3_score") if s.get("l3_ok") else s.get("l3_score")
    return s.get(name)


def auc_safe(y, x):
    y = np.asarray(y); x = np.asarray(x, float)
    if len(set(y.tolist())) < 2:
        return None
    return float(roc_auc_score(y, x))


def boot_auc(rows, names, B=2000, seed=0):
    """Cluster bootstrap by normalised sentence. rows: [{'y', 'cl', name: value}] (all names present)."""
    rng = np.random.default_rng(seed)
    cl = sorted({r["cl"] for r in rows})
    idx_of = defaultdict(list)
    for i, r in enumerate(rows):
        idx_of[r["cl"]].append(i)
    y = np.array([r["y"] for r in rows])
    X = {n: np.array([r[n] for r in rows], float) for n in names}
    out = {n: [] for n in names}
    for _ in range(B):
        pick = rng.integers(0, len(cl), len(cl))
        ii = np.concatenate([idx_of[cl[j]] for j in pick])
        yy = y[ii]
        if yy.min() == yy.max():
            continue
        for n in names:
            out[n].append(roc_auc_score(yy, X[n][ii]))
    return {n: np.array(v) for n, v in out.items()}


def ci(a):
    if a is None or len(a) == 0:
        return [None, None]
    return [round(float(np.quantile(a, 0.025)), 4), round(float(np.quantile(a, 0.975)), 4)]


def acc_eq(y, s, eps):
    """Tie-aware pairwise accuracy (Deutsch et al. 2023): over all item pairs, agreement of sign(y_i-y_j) with
    sign_eps(s_i-s_j), where |s_i-s_j| <= eps counts as a metric tie."""
    y = np.asarray(y, float); s = np.asarray(s, float)
    dy = np.sign(y[:, None] - y[None, :])
    ds = s[:, None] - s[None, :]
    sg = np.where(np.abs(ds) <= eps, 0.0, np.sign(ds))
    iu = np.triu_indices(len(y), 1)
    return float((dy[iu] == sg[iu]).mean())


def tie_calibrate(y, s):
    s = np.asarray(s, float)
    diffs = np.unique(np.abs(s[:, None] - s[None, :]))
    cands = np.unique(np.concatenate([[0.0], np.quantile(diffs, np.linspace(0, 1, 41))]))
    best = max(cands, key=lambda e: acc_eq(y, s, e))
    return float(best), acc_eq(y, s, best)


def binary_stats(y, f):
    y = np.asarray(y, int); f = np.asarray(f, int)
    tp = int(((f == 1) & (y == 1)).sum()); fp = int(((f == 1) & (y == 0)).sum())
    P = int((y == 1).sum()); N = int((y == 0).sum())
    tpr = tp / P if P else None
    fpr = fp / N if N else None
    prec = tp / (tp + fp) if tp + fp else None
    out = {"TPR": tpr, "FPR": fpr, "precision": prec, "prevalence": P / len(y) if len(y) else None, "n_pos": P,
           "n_neg": N, "TPR_wilson": wilson(tp, P), "FPR_wilson": wilson(fp, N)}
    for pi in (0.10, 0.25):
        if tpr is not None and fpr is not None and (tpr * pi + fpr * (1 - pi)) > 0:
            out[f"precision_at_prev_{pi}"] = tpr * pi / (tpr * pi + fpr * (1 - pi))
        else:
            out[f"precision_at_prev_{pi}"] = None
    return out


def rnd(x, k=4):
    if isinstance(x, float):
        return round(x, k)
    if isinstance(x, dict):
        return {a: rnd(b, k) for a, b in x.items()}
    if isinstance(x, list):
        return [rnd(b, k) for b in x]
    return x


def evaluate_set(rows, names, B, label_name):
    """rows have y, cl and score values (None allowed -> item excluded for that score, counted)."""
    res = {"set": label_name, "n": len(rows), "n_pos": int(sum(r["y"] for r in rows)), "scores": {}}
    res["prevalence"] = res["n_pos"] / res["n"] if res["n"] else None
    core = [n for n in names if n not in PARTIAL and all(r.get(n) is not None for r in rows)]
    common = [r for r in rows if all(r.get(n) is not None for n in core)]
    boots = boot_auc(common, core, B) if common and len({r["y"] for r in common}) == 2 else {}
    for n in names:
        if n not in core:
            sub = [r for r in rows if r.get(n) is not None and all(r.get(c) is not None for c in core)]
            if len(sub) >= 20 and len({r["y"] for r in sub}) == 2:
                bb = boot_auc(sub, core + [n], B, seed=1)
                res.setdefault("partial_subset_boots", {})[n] = {
                    "n": len(sub), "n_pos": int(sum(r["y"] for r in sub)),
                    "AUROC_on_subset": {c: auc_safe([r["y"] for r in sub], [r[c] for r in sub]) for c in core + [n]},
                    "paired_vs_l3_score": paired(bb, n, "l3_score") if "l3_score" in bb else None,
                    "paired_vs_p_fused_H": paired(bb, n, "p_fused_H") if "p_fused_H" in bb else None}
                boots_n = bb[n]
                res["scores_ci_partial"] = res.get("scores_ci_partial", {}); res["scores_ci_partial"][n] = ci(boots_n)
    for n in names:
        rr = [r for r in rows if r.get(n) is not None]
        y = [r["y"] for r in rr]; x = [r[n] for r in rr]
        a = auc_safe(y, x)
        res["scores"][n] = {"AUROC": a, "AUROC_CI95_cluster": ci(boots.get(n)) if n in core else
                            res.get("scores_ci_partial", {}).get(n, [None, None]), "n_scored": len(rr),
                            "n_missing": len(rows) - len(rr),
                            "AUPRC": float(average_precision_score(y, x)) if a is not None else None,
                            "prevalence": float(np.mean(y)) if y else None}
    res["n_common"] = len(common)
    res["_boots"] = boots
    return res


def paired(boots, a, b):
    if a not in boots or b not in boots or len(boots[a]) == 0:
        return None
    d = boots[a] - boots[b]
    return {"delta_mean": round(float(d.mean()), 4), "CI95": ci(d), "P(delta<=0)": round(float((d <= 0).mean()), 4)}


def run(root: Path, res_dir: Path | None = None, B: int = 2000):
    res_dir = res_dir or (root / "results")
    items = {x["item_id"]: x for x in json.loads((root / "screen_items.json").read_text())}
    scored = [json.loads(l) for l in (res_dir / "scores_unlabelled.jsonl").read_text().splitlines() if l.strip()]
    inv = json.loads((res_dir / "invariance_scores.json").read_text())
    calib = json.loads((res_dir / "calibration.json").read_text())
    abl = json.loads((res_dir / "ablations.json").read_text())
    for s in scored:  # ---- LABEL JOIN
        if s["track"] in ("L", "H"):
            it = items[s["item_id"]]
            s["label"], s["auto_class"], s["repair_ops"] = it["label"], it["auto_class"], it["repair_ops"]
            s["ref_source"] = it.get("ref_source")
        else:
            s["label"], s["auto_class"], s["repair_ops"] = "CORRECT_REF", "REF", None
    L = [s for s in scored if s["track"] == "L"]
    H = [s for s in scored if s["track"] == "H"]
    HREF = [s for s in scored if s["track"] == "HREF"]
    M = {"labels_sha256": json.loads((root / "screen_meta.json").read_text())["labels_sha256"]}

    # ---- within-L cross-fitted fusion (secondary; GroupKFold by sentence on CORRECT/ERROR)
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import GroupKFold
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    FEATS = json.loads(((res_dir / "prereg.json") if (res_dir / "prereg.json").exists() else (root / "prereg.json")).read_text())["fusion_features"]
    fvec = lambda s: [float(s.get(f, 0.0) or 0.0) for f in FEATS]  # noqa: E731
    Lp = [s for s in L if s["label"] in ("CORRECT", "ERROR") and s.get("parse_ok") and s.get("cpu_status") == "OK"]
    if len(Lp) > 20:
        X = np.array([fvec(s) for s in Lp]); y = np.array([s["label"] == "ERROR" for s in Lp], int)
        g = np.array([_norm(s["text"]) for s in Lp])
        oof = np.zeros(len(y))
        for tr, te in GroupKFold(n_splits=5).split(X, y, g):
            m = make_pipeline(StandardScaler(), LogisticRegression(C=1.0, class_weight="balanced", max_iter=2000))
            m.fit(X[tr], y[tr]); oof[te] = m.predict_proba(X[te])[:, 1]
        for s, p in zip(Lp, oof):
            s["p_fused_Lcf"] = float(p)

    def rows_for(sub, pos_fn, neg_fn):
        out = []
        for s in sub:
            if pos_fn(s):
                y = 1
            elif neg_fn(s):
                y = 0
            else:
                continue
            r = {"y": y, "cl": _norm(s["text"]), "item_id": s["item_id"]}
            for n in SCORES:
                r[n] = score_value(s, n)
            out.append(r)
        return out
    is_c = lambda s: s["label"] == "CORRECT"  # noqa: E731
    sets = {
        "primary_L_ERROR_vs_CORRECT": rows_for(L, lambda s: s["label"] == "ERROR", is_c),
        "secondary_L_ERRORuCOMPOUND_vs_CORRECT": rows_for(
            L, lambda s: s["label"] == "ERROR" or (s["label"] == "UNCERTAIN" and s["auto_class"] == "COMPOUND"), is_c),
        "secondary_L_ERROR_minus_pureADDDROP_vs_CORRECT": rows_for(
            L, lambda s: s["label"] == "ERROR" and s["auto_class"] != "ADD+DROP", is_c),
    }
    names_L = [n for n in SCORES]
    evals = {}
    for k, rows in sets.items():
        names = [n for n in names_L if any(r.get(n) is not None for r in rows)]
        ev = evaluate_set(rows, names, B, k)
        bo = ev.pop("_boots")
        ev["paired_delta_AUROC"] = {
            f"{a} - {b}": paired(bo, a, b) for a, b in [
                ("p_fused_H", "l1_any"), ("p_fused_H", "n_smells"), ("p_fused_H", "l2_bow"), ("p_fused_H", "l2_role"),
                ("p_fused_H", "l3_score"), ("l2_role", "l2_bow"), ("l3_score", "l2_bow"),
                ("p_fused_H", "cascade_llmformula"), ("p_fused_H", "p_fused_Lcf"), ("p_fused_H", "p_fused_Hall")]}
        evals[k] = ev
    # track H (OOF fused), separately
    Hrows = []
    for s in H:
        if s["label"] == "READING_CHOICE":
            continue
        if s["label"] == "ERROR" or (s["label"] == "UNCERTAIN" and s["auto_class"] == "COMPOUND"):
            y = 1
        elif s["label"] == "CORRECT":
            y = 0
        else:
            continue
        r = {"y": y, "cl": _norm(s["text"]), "item_id": s["item_id"]}
        for n in ["l1_any", "n_smells", "l2_bow", "l2_role", "l3_score"]:
            r[n] = score_value(s, n)
        r["p_fused_H_oof"] = s.get("p_fused_H_oof") if s.get("parse_ok") and s.get("cpu_status") == "OK" else None
        Hrows.append(r)
    evH = evaluate_set(Hrows, ["l1_any", "n_smells", "l2_bow", "l2_role", "l3_score", "p_fused_H_oof"], B,
                       "track_H_ERRORuCOMPOUND_vs_CORRECT(OOF)")
    boH = evH.pop("_boots")
    evH["paired_delta_AUROC"] = {"l2_role - l2_bow": paired(boH, "l2_role", "l2_bow"),
                                 "p_fused_H_oof - l2_bow": paired(boH, "p_fused_H_oof", "l2_bow")}
    evals["track_H"] = evH
    # ---- paired (same-text) H AUROC, iter-3 comparability: original vs corrected formula for the same sentence
    href_by = {_norm(s["text"]): s for s in HREF}
    pa = defaultdict(list)
    for s in H:
        if s["label"] in ("ERROR",) or (s["label"] == "UNCERTAIN" and s["auto_class"] == "COMPOUND"):
            h = href_by.get(_norm(s["text"]))
            if not h:
                continue
            for n in ["n_smells", "l2_bow", "l2_role", "l3_score"]:
                a, b = score_value(s, n), score_value(h, n)
                if a is not None and b is not None:
                    pa[n].append(1.0 if a > b else 0.5 if a == b else 0.0)
    M["track_H_paired_same_text_AUROC"] = {n: {"auroc": round(float(np.mean(v)), 4), "n": len(v)} for n, v in pa.items()}

    # ---- binary layers: TPR/FPR/precision, re-weighted precision, acc_eq with tie calibration (eps on H)
    def bflags(s):
        if not (s.get("parse_ok") and s.get("cpu_status") == "OK"):
            return None
        return {"l1_any": s.get("l1_any"), "l2_bow_flag": s.get("bow_flag"), "l2_role_flag": s.get("role_flag"),
                "l3_flag": s.get("l3_flag"), "fused_flag": s.get("fused_flag"),
                "l1_or_l2": int(bool(s.get("l1_any") or s.get("bow_flag") or s.get("role_flag"))),
                "cascade_any": int(s.get("fired_layer") not in ("none", None))}
    bin_res = {}
    Hb = [(r["y"], bflags(next(x for x in H if x["item_id"] == r["item_id"]))) for r in Hrows]
    Hb = [(y, f) for y, f in Hb if f]
    for k in ["primary_L_ERROR_vs_CORRECT", "secondary_L_ERROR_minus_pureADDDROP_vs_CORRECT"]:
        idx = {r["item_id"]: r["y"] for r in sets[k]}
        rows = [(idx[s["item_id"]], bflags(s)) for s in L if s["item_id"] in idx and bflags(s)]
        out = {}
        for b in ["l1_any", "l2_bow_flag", "l2_role_flag", "l3_flag", "fused_flag", "l1_or_l2", "cascade_any"]:
            y = [a for a, _ in rows]; f = [c[b] for _, c in rows]
            st = binary_stats(y, f)
            yh = [a for a, _ in Hb]; fh = [c[b] for _, c in Hb]
            eps, acc_h = tie_calibrate(yh, fh) if len(set(yh)) == 2 else (0.0, None)
            st["acc_eq_L"] = acc_eq(y, f, eps)
            st["tie_eps_from_H"] = eps
            st["acc_eq_H"] = acc_h
            out[b] = st
        # continuous scores acc_eq with eps tuned on H
        for n in ["p_fused_H", "l3_score", "l2_bow"]:
            rr = [(r["y"], r[n]) for r in sets[k] if r.get(n) is not None]
            hn = "p_fused_H_oof" if n == "p_fused_H" else n
            hh = [(r["y"], r[hn]) for r in Hrows if r.get(hn) is not None]
            if len(hh) > 10 and rr:
                eps, acc_h = tie_calibrate([a for a, _ in hh], [b for _, b in hh])
                out[f"{n}(continuous)"] = {"acc_eq_L": acc_eq([a for a, _ in rr], [b for _, b in rr], eps),
                                           "tie_eps_from_H": eps, "acc_eq_H": acc_h}
        bin_res[k] = out
    M["binary_layers"] = bin_res

    # ---- L1 per system x length (FA on CORRECT; precision on ERROR), per-smell FA; smell fails if FA>3% on any system
    l1tab = {}
    smell_fa = defaultdict(dict)
    for sysn in sorted({s["system"] for s in L}):
        sub = [s for s in L if s["system"] == sysn and s.get("parse_ok") and s.get("cpu_status") == "OK"]
        for lb in ("<12", "12-19", ">=20", "all"):
            ss = [s for s in sub if lb == "all" or s["strata"]["len_bin"] == lb]
            cor = [s for s in ss if s["label"] == "CORRECT"]; err = [s for s in ss if s["label"] == "ERROR"]
            fa = sum(s["l1_any"] for s in cor); tp = sum(s["l1_any"] for s in err)
            l1tab[f"{sysn}|{lb}"] = {"n_correct": len(cor), "FA": fa / len(cor) if cor else None,
                                     "FA_wilson": wilson(fa, len(cor)), "n_error": len(err),
                                     "TPR": tp / len(err) if err else None,
                                     "precision": tp / (tp + fa) if tp + fa else None}
        cor = [s for s in sub if s["label"] == "CORRECT"]
        cnt = Counter(c for s in cor for c in s.get("l1_codes", []))
        for c in ["EX_IMP", "ALL_AND", "IFF_RESTR", "GLUE", "FREE", "VACUOUS", "TRIVIAL", "ARITY", "DANGLING"]:
            smell_fa[c][sysn] = {"fires": cnt[c], "n_correct": len(cor), "FA": cnt[c] / len(cor) if cor else None}
    M["L1_by_system_length"] = l1tab
    M["L1_smell_FA_by_system"] = {c: {"per_system": v, "FAILS(>3% on any system)": any((x["FA"] or 0) > 0.03 for x in v.values())}
                                  for c, v in smell_fa.items()}
    M["L1_smell_fires_on_L_errors"] = dict(Counter(c for s in L if s["label"] == "ERROR" for c in s.get("l1_codes", []) or []))

    # ---- per-type sensitivity at operating thresholds (track-L ERROR; track-H census classes)
    def per_type(sub):
        out = {}
        for op in OPS:
            ss = [s for s in sub if (op == "COMPOUND" and s["auto_class"] == "COMPOUND") or
                  (s["repair_ops"] and op in s["repair_ops"])]
            ss = [s for s in ss if s.get("parse_ok") and s.get("cpu_status") == "OK"]
            if not ss:
                continue
            out[op] = {"n": len(ss), **{b: round(float(np.mean([bool(s.get(k)) for s in ss])), 4) for b, k in
                                        [("L1", "l1_any"), ("L2_bow", "bow_flag"), ("L2_role", "role_flag"),
                                         ("L3", "l3_flag"), ("fused", "fused_flag")]},
                       "cascade_any": round(float(np.mean([s.get("fired_layer") not in ("none", None) for s in ss])), 4)}
        return out
    M["per_type_sensitivity"] = {
        "track_L": per_type([s for s in L if s["label"] == "ERROR" or s["auto_class"] == "COMPOUND"]),
        "track_H": per_type([s for s in H if s["label"] in ("ERROR", "UNCERTAIN", "READING_CHOICE")]),
        "FA_on_CORRECT_track_L": {b: round(float(np.mean([bool(s.get(k)) for s in L if s["label"] == "CORRECT"
                                                            and s.get("parse_ok") and s.get("cpu_status") == "OK"])), 4)
                                  for b, k in [("L1", "l1_any"), ("L2_bow", "bow_flag"), ("L2_role", "role_flag"),
                                               ("L3", "l3_flag"), ("fused", "fused_flag")]}}
    # ---- error-type readout on depth-1 errors
    d1 = [s for s in L + H if s["label"] in ("ERROR",) and s["repair_ops"] and len(s["repair_ops"]) == 1]
    M["error_type_readout_depth1"] = {
        "n_depth1": len(d1),
        "P(error_code in true ops | fired)": (round(float(np.mean([s["error_code"] in s["repair_ops"] for s in d1
                                                                    if s.get("error_code") and s["error_code"] != "UNPARSEABLE"])), 4)
                                             if any(s.get("error_code") for s in d1) else None),
        "n_fired": sum(1 for s in d1 if s.get("error_code") and s["error_code"] != "UNPARSEABLE"),
        "by_layer": {lay: {"n": len(v), "hit": round(float(np.mean(v)), 4)} for lay, v in
                     {lay: [s["error_code"] in s["repair_ops"] for s in d1 if s.get("fired_layer") == lay]
                      for lay in ("L1", "L2", "L3")}.items() if v},
        "confusion": dict(Counter(f"{s['repair_ops'][0]}->{s.get('error_code')}" for s in d1).most_common(30))}

    # ---- invariance: FA at operating threshold per family + flip rate vs original
    invres = {}
    for fam in sorted({r["family"] for r in inv}):
        rr = [r for r in inv if r["family"] == fam]
        ap = [r for r in rr if r["applies"] and r.get("parse_ok")]
        d = {"n_items": len(rr), "n_applies": len(ap), "n_na": len(rr) - len(ap)}
        for lay in ["l1_flag", "bow_flag", "role_flag", "l3_flag", "fused_flag"]:
            if not ap:
                continue
            fa = [bool(r.get(lay)) for r in ap]
            fl = [bool(r.get(lay)) != bool(r["orig"].get(lay)) for r in ap]
            d[lay] = {"FA": round(float(np.mean(fa)), 4), "FA_orig": round(float(np.mean([bool(r['orig'].get(lay)) for r in ap])), 4),
                      "flip_rate": round(float(np.mean(fl)), 4), "FA_wilson": wilson(sum(fa), len(fa))}
        if ap:
            d["mean_abs_dp_fused"] = round(float(np.mean([abs(r["p_fused_H"] - r["orig"]["p_fused_H"]) for r in ap])), 4)
            d["L1_flips_examples"] = [{"item_id": r["item_id"], "orig": r["orig_l1_codes"], "rewritten": r["l1_codes"]}
                                      for r in ap if bool(r.get("l1_flag")) != bool(r["orig"].get("l1_flag"))][:5]
        invres[fam] = d
    M["invariance"] = invres

    # ---- coverage (failures in the denominator)
    cov = {}
    for tr, sub in (("L", L), ("H", H), ("HREF", HREF)):
        n = len(sub)
        c = Counter(s.get("coverage_status", "UNPARSEABLE") for s in sub)
        cov[tr] = {"n": n, "status_counts": dict(c), "full_coverage_rate": c.get("OK", 0) / n if n else None,
                   "parse_rate": sum(1 for s in sub if s.get("parse_ok")) / n if n else None,
                   "L3_ok_rate": sum(1 for s in sub if s.get("l3_ok")) / n if n else None,
                   "scored_by_fused_rate(any output incl. unparseable->p=1)": 1.0}
    cov["L_by_system_parse_rate"] = {sy: round(sum(1 for s in L if s["system"] == sy and s.get("parse_ok")) /
                                               max(1, sum(1 for s in L if s["system"] == sy)), 4)
                                     for sy in sorted({s["system"] for s in L})}
    M["coverage"] = cov

    # ---- complexity strata
    strat = {}
    prim = {r["item_id"]: r for r in sets["primary_L_ERROR_vs_CORRECT"]}
    def binner(s, key):
        v = s["strata"].get(key)
        if key == "len_bin":
            return v
        if key == "exception":
            return str(bool(v))
        if v is None:
            return "NA"
        if key == "n_quant":
            return "0" if v == 0 else ("1" if v == 1 else ">=2")
        if key == "depth":
            return "<=1" if v <= 1 else ("2-3" if v <= 3 else ">=4")
        if key == "n_conditions":
            return "0" if v == 0 else ("1-2" if v <= 2 else ">=3")
    for key in ["len_bin", "n_quant", "depth", "n_conditions", "exception"]:
        groups = defaultdict(list)
        for s in L:
            if s["item_id"] in prim:
                groups[binner(s, key)].append((s, prim[s["item_id"]]))
        d = {}
        for b, lst in sorted(groups.items()):
            y = [r["y"] for _, r in lst]
            npos, nneg = sum(y), len(y) - sum(y)
            e = {"n_error": npos, "n_correct": nneg, "UNTESTABLE": npos < 50 or nneg < 50}
            for n in ["p_fused_H", "l1_any", "l2_bow", "l2_role", "l3_score"]:
                vv = [(r["y"], r[n]) for _, r in lst if r.get(n) is not None]
                e[f"AUROC_{n}"] = auc_safe([a for a, _ in vv], [c for _, c in vv]) if vv else None
            for lay, k in [("L1", "l1_any"), ("fused", "fused_flag"), ("L2_role", "role_flag")]:
                cor = [s for s, r in lst if r["y"] == 0 and s.get("parse_ok")]
                e[f"FA_{lay}"] = round(float(np.mean([bool(s.get(k)) for s in cor])), 4) if cor else None
            d[b] = e
        strat[key] = d
    M["complexity_strata_primary_L"] = strat

    # ---- per-system AUROC and system-level (descriptive, 3 systems)
    persys = {}
    for sy in sorted({s["system"] for s in L}):
        rr = [prim[s["item_id"]] for s in L if s["system"] == sy and s["item_id"] in prim]
        persys[sy] = {"n": len(rr), "n_error": sum(r["y"] for r in rr),
                      **{f"AUROC_{n}": auc_safe([r["y"] for r in rr if r.get(n) is not None],
                                                [r[n] for r in rr if r.get(n) is not None]) for n in ["p_fused_H", "l1_any", "l2_bow", "l3_score"]}}
    sysl = {}
    for sy in persys:
        sub = [s for s in L if s["system"] == sy]
        sysl[sy] = {"error_rate(ERROR/(ERROR+CORRECT))": sum(s["label"] == "ERROR" for s in sub) /
                    max(1, sum(s["label"] in ("ERROR", "CORRECT") for s in sub)),
                    "mean_p_fused_H(parseable)": float(np.mean([s["p_fused_H"] for s in sub if s.get("parse_ok") and s.get("cpu_status") == "OK"])),
                    "parse_rate": sum(1 for s in sub if s.get("parse_ok")) / len(sub)}
    from scipy.stats import kendalltau
    ks = sorted(sysl)
    tau = kendalltau([sysl[k]["error_rate(ERROR/(ERROR+CORRECT))"] for k in ks], [sysl[k]["mean_p_fused_H(parseable)"] for k in ks])
    M["per_system_item_AUROC"] = persys
    M["system_level_descriptive"] = {"systems": sysl, "kendall_tau_error_rate_vs_mean_p": float(tau.statistic),
                                     "note": "3 systems: descriptive only, no power"}

    # ---- cost / time
    Lc = [s for s in L]
    M["cost"] = {"L1_usd_per_item": 0.0, "L2_usd_per_item": 0.0,
                 "L3_usd_per_item_mean(track L, text-shared across systems)": float(np.mean([s["cost_usd_l3"] for s in Lc])),
                 "L3_usd_per_1000_items(track L)": 1000 * float(np.mean([s["cost_usd_l3"] for s in Lc])),
                 "L3_usd_per_1000_calls(flash-lite, from cache records)": 1000 * float(np.mean(
                     [r["cost_usd"] for r in (json.loads(l) for l in (root / "cache" / "llm_cache.jsonl").read_text().splitlines() if l.strip())
                      if r["model"] == "google/gemini-2.5-flash-lite" and r["tag"].startswith("L3#")] or [0.0])),
                 "decomposed_judge_usd_per_1000_calls": 1000 * float(np.mean(
                     [r["cost_usd"] for r in (json.loads(l) for l in (root / "cache" / "llm_cache.jsonl").read_text().splitlines() if l.strip())
                      if r["model"] == "google/gemini-2.5-flash-lite" and r["tag"].startswith("DJ#")] or [0.0])),
                 "total_spend_usd(all stages incl. ablations)": abl["spend_usd_total"],
                 "secs_cpu_p50": float(np.quantile([s["secs_cpu"] for s in Lc], 0.5)),
                 "secs_cpu_p95": float(np.quantile([s["secs_cpu"] for s in Lc], 0.95)),
                 "secs_l3_p50": float(np.quantile([s["secs_l3"] for s in Lc], 0.5)),
                 "secs_l3_p95": float(np.quantile([s["secs_l3"] for s in Lc], 0.95))}

    # ---- contamination: l3_score AUROC original(exact align) vs disguised on primary set (paired bootstrap)
    ids = {r["item_id"]: r["y"] for r in sets["primary_L_ERROR_vs_CORRECT"]}
    cr = [{"y": ids[s["item_id"]], "cl": _norm(s["text"]), "orig": s["l3_score_exact"], "disg": s["l3_score_disguised"]}
          for s in L if s["item_id"] in ids and s.get("l3_score_exact") is not None and s.get("l3_score_disguised") is not None]
    if cr and len({r["y"] for r in cr}) == 2:
        bo = boot_auc(cr, ["orig", "disg"], B)
        M["contamination_trackL_l3_AUROC"] = {"n": len(cr), "orig_exact_align": auc_safe([r["y"] for r in cr], [r["orig"] for r in cr]),
                                              "disguised": auc_safe([r["y"] for r in cr], [r["disg"] for r in cr]),
                                              "paired_orig_minus_disguised": paired(bo, "orig", "disg")}
    M["contamination_HREF_field_accuracy"] = abl["contamination"]
    M["formula_reading_accuracy_decomposed_judge"] = abl["formula_reading_accuracy"]

    # ---- label artefact audit (for iteration-2 adjudication)
    M["label_artefacts"] = {
        "track_L_auto_class": dict(Counter(s["auto_class"] for s in L)),
        "ERROR_pure_ADD+DROP_share": sum(s["auto_class"] == "ADD+DROP" for s in L if s["label"] == "ERROR") /
        max(1, sum(s["label"] == "ERROR" for s in L)),
        "note": "ADD+DROP = one atom replaced by another; on inspection mostly predicate-vocabulary/arity choices "
                "(Lunch(james) vs HasLunch(james, company)) that the iter-3 aligner cannot bridge -> likely CORRECT "
                "under panel adjudication; reported as a secondary set."}

    # ---- gates (fused, primary set)
    pe = evals["primary_L_ERROR_vs_CORRECT"]["scores"]
    fus_auc = pe["p_fused_H"]["AUROC"]
    worst_fa = max((v["fused_flag"]["FA"] for v in invres.values() if isinstance(v.get("fused_flag"), dict)), default=None)
    worst_fa_orig = max((v["fused_flag"]["FA_orig"] for v in invres.values() if isinstance(v.get("fused_flag"), dict)), default=None)
    cov_rate = cov["L"]["full_coverage_rate"]
    cpi = M["cost"]["L3_usd_per_1000_calls(flash-lite, from cache records)"] / 1000
    M["gates_fused_primary"] = {
        "AUROC>=0.65": {"value": fus_auc, "pass": bool(fus_auc is not None and fus_auc >= 0.65)},
        "coverage>=0.90": {"value": cov_rate, "pass": bool(cov_rate is not None and cov_rate >= 0.90),
                           "note": "full coverage = parse ok + all layers scored; unparseable outputs count as failures"},
        "rewrite_FA<=0.10_per_family": {"worst_family_FA": worst_fa, "worst_family_FA_on_originals": worst_fa_orig,
                                        "pass": bool(worst_fa is not None and worst_fa <= 0.10),
                                        "worst_family_flip_rate": max((v["fused_flag"]["flip_rate"] for v in invres.values()
                                                                       if isinstance(v.get("fused_flag"), dict)), default=None),
                                        "note": "as pre-registered: share of rewritten CORRECT items flagged; the originals "
                                                "are flagged at the same rate (fused FA on track-L CORRECT ~0.19 vs 0.10 "
                                                "calibrated on H), so the flip rate isolates rewrite sensitivity"},
        "cost<=0.002/item": {"value": cpi, "pass": bool(cpi <= 0.002)},
        "dAUROC_over_disguised_judge": "computed in iteration 2 by joining experiment D on item_id (not in this artifact)"}
    M["evaluations"] = evals
    M["calibration"] = calib
    M = rnd(M)
    (res_dir / "metrics.json").write_text(json.dumps(M, ensure_ascii=False, indent=1))
    with (res_dir / "per_item.jsonl").open("w") as fh:
        for s in scored:
            fh.write(json.dumps(s, ensure_ascii=False) + "\n")
    logger.info("analysis written: " + json.dumps({k: v["scores"]["p_fused_H"]["AUROC"] if "p_fused_H" in v["scores"] else None
                                                   for k, v in evals.items()}))
    import output
    output.write_method_out(root, res_dir, scored, M)
    return M
