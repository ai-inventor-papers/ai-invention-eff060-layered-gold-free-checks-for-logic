#!/usr/bin/env python3
"""E2-A analyses (plan STEP 4-5). Runs ONLY after both seals verify; joins sealed labels to sealed scores by row_key.

  join       verify score_seal.json (recompute every hash) + e2src verify_seal.py, assert score seal time < join time,
             write per_item_E2A.jsonl (scores + labels + complexity)
  analyse    (a) primary confirmation, (b) S4_E2 nesting, H-MECH (i)-(iv), H-IMPROVE, H-RENAME, complexity, system tau-b,
             coverage, cost, placebos -> results/*.json, tables.md
Statistics: frozen eval-2 stats (auc, strat_auc, WStratAuc); stratified sentence-cluster bootstrap (sentences resampled
WITHIN stratum, B = 2000, seed 0; the prereg'd scheme) with the frozen pooled SentBoot as a sensitivity; S4 via the frozen
T1 s4.fit_s4_oof (C = 1.0, 5 E2 folds).
"""
from __future__ import annotations

import argparse
import glob
import hashlib
import json
import math
import subprocess
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

WS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WS / "frozen" / "eval2" / "src"))
sys.path.insert(0, str(WS / "frozen" / "t1"))
from stats import SentBoot, WStratAuc, auc, ci, strat_auc  # noqa: E402  (frozen eval-2)

RES = WS / "results"
RES.mkdir(exist_ok=True)
E2S = WS / "e2src"
B = 2000
LONG = ("L25", "EXC")
PRIMARY = "c_score_align"
BAR = "judge_cheap_disg"
METRICS = ["c_score_align", "p_peer_text", "c_exact", "g_align", "l2_bow", "l3_z3", "c_pn", "c_rw", "c_pn_rw", "c_two", "c_v5",
           "judge_cheap_disg", "judge_cheap_orig", "judge_cheap2_disg", "judge_cheap2_orig", "judge_local_qwen8b_disg",
           "judge_local_qwen8b_orig", "pilot_joint_conflict", "pilot_arity_incons", "pilot_shape_incons", "pilot_dangling",
           "pilot_rerun_jacc"]
LABEL_OF = {"c_score_align": "V0 c_score_align (frozen consensus)", "p_peer_text": "PT p_peer_text (frozen fusion)",
            "c_exact": "c_exact (no aligner)", "g_align": "ALIGN graded g", "l2_bow": "L2-bow (text side)", "l3_z3": "L3 (text side)",
            "c_pn": "V1 plurality-normalised", "c_rw": "V2 reliability-weighted", "c_pn_rw": "V3 = V1+V2", "c_two": "V4 two-channel",
            "c_v5": "V5 3-pool", "judge_cheap_disg": "flash-lite rubric A, disguised (PRIMARY BAR)",
            "judge_cheap_orig": "flash-lite rubric A, original", "judge_cheap2_disg": "gpt-4.1-nano P(YES), disguised",
            "judge_cheap2_orig": "gpt-4.1-nano P(YES), original", "judge_local_qwen8b_disg": "local Qwen3-8B, disguised",
            "judge_local_qwen8b_orig": "local Qwen3-8B, original", "pilot_joint_conflict": "pilot m1 joint-load conflict (adapted)",
            "pilot_arity_incons": "pilot m2 arity inconsistency", "pilot_shape_incons": "pilot m2 shape inconsistency",
            "pilot_dangling": "pilot m3 dangling symbols", "pilot_rerun_jacc": "pilot m5 1 - rerun Jaccard (cross-system proxy)", "S4_E2": "S4_E2 stack (OOF)", "S4_E2_plus_V0": "S4_E2 + V0 (OOF)"}
S4_FEATS = ["judge_cheap_disg", "judge_cheap_orig", "judge_cheap2_disg", "judge_cheap2_orig", "judge_local_qwen8b_disg",
            "judge_local_qwen8b_orig", "l2_bow", "l3_z3"]


def jl(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.exists() else []


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def dump(name: str, obj) -> None:
    (RES / name).write_text(json.dumps(obj, indent=1, default=lambda o: None if isinstance(o, float) and math.isnan(o) else str(o)))


# ================================================================================================================ join
def stage_join() -> None:
    seal = json.loads((WS / "score_seal.json").read_text())
    bad = [k for k, h in seal["sha256"].items() if not (WS / k).exists() or sha256(WS / k) != h]
    assert not bad, f"score seal broken: {bad[:5]}"
    vs = subprocess.run([str(E2S / ".venv" / "bin" / "python"), str(E2S / "src_e2" / "verify_seal.py")], capture_output=True,
                        text=True, cwd=str(E2S))
    assert vs.returncode == 0 and "seal_intact" in (vs.stdout + vs.stderr), f"label seal verify failed: {vs.stdout[-500:]} {vs.stderr[-500:]}"
    lseal = json.loads((E2S / "seal.json").read_text())
    t_join = time.time()
    assert seal["written_ts"] < t_join, "score seal must predate the join"
    labels = {r["row_key"]: r for r in jl(E2S / "sealed" / "labels_E2.jsonl") if r.get("system_class") == "llm"}
    sents = {s["sentence_id"]: s for s in json.loads((E2S / "work" / "sentences_E2_active.json").read_text())}
    scores = jl(WS / "scores_E2A.jsonl")
    out, miss = [], 0
    for r in scores:
        lab = labels.get(r["row_key"])
        if lab is None:
            miss += 1
        s = sents[r["sentence_id"]]
        r = dict(r)
        r.update({"label": (lab or {}).get("label"), "label_tier": (lab or {}).get("label_tier"),
                  "reading_choice": bool((lab or {}).get("reading_choice")), "vex": (lab or {}).get("vex"),
                  "vex_eq": (lab or {}).get("vex_eq"), "auto_label": (lab or {}).get("auto_label"),
                  "error_ops": (lab or {}).get("error_ops"), "reference_status": (lab or {}).get("reference_status"),
                  "correct_not_equivalent": (lab or {}).get("correct_not_equivalent"),
                  "n_conditions": s.get("n_conditions"), "n_quant": s.get("n_quant"), "depth": s.get("depth")})
        out.append(r)
    p = WS / "per_item_E2A.jsonl"
    p.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in out))
    rec = {"score_seal_utc": seal["written_utc"], "score_seal_ts": seal["written_ts"], "label_seal_utc": lseal.get("sealed_at_utc"),
           "label_seal_verify_stdout_tail": vs.stdout[-400:], "join_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t_join)),
           "join_ts": t_join, "n_rows": len(out), "rows_without_label": miss, "per_item_sha256": sha256(p),
           "score_seal_files_verified": len(seal["sha256"])}
    dump("join_record.json", rec)
    print(json.dumps(rec, indent=1))


# ============================================================================================================ helpers
class Data:
    def __init__(self, rows: list[dict]):
        self.rows = rows
        self.n = len(rows)
        self.col = lambda c: np.array([np.nan if r.get(c) is None else float(r[c]) for r in rows], float)
        self.sid = np.array([r["sentence_id"] for r in rows])
        self.stratum = np.array([r["stratum"] for r in rows])
        lab = np.array([r.get("label") for r in rows])
        tier = np.array([r.get("label_tier") for r in rows])
        rc = np.array([bool(r.get("reading_choice")) for r in rows])
        cls = np.isin(lab, ["CORRECT", "ERROR"]) & ~rc
        self.y = (lab == "ERROR").astype(float)
        self.regime = {"R_AB": cls & np.isin(tier, ["A", "B"]), "R_A": cls & (tier == "A"),
                       "R_VEX": cls & np.isin(tier, ["A", "B"]) & np.array([r.get("vex") is True for r in rows]),
                       "R_AB_nopilot": cls & np.isin(tier, ["A", "B"]) & ~np.array([bool(r.get("pilot")) for r in rows])}
        self.cells = {"LONG (L25+EXC)": np.isin(self.stratum, LONG), "L25": self.stratum == "L25", "EXC": self.stratum == "EXC",
                      "DT": self.stratum == "DT", "ALL": np.ones(self.n, bool)}


def strat_boot_weights(sids, strata, b: int = B, seed: int = 0) -> np.ndarray:
    """Stratified sentence-cluster bootstrap: within each stratum, sentences resampled with replacement.
    -> (B, n_rows) multiplicity weights."""
    sids, strata = np.asarray(sids), np.asarray(strata)
    rng = np.random.default_rng(seed)
    W = np.zeros((b, len(sids)))
    for st in sorted(set(strata)):
        m = strata == st
        keys, inv = np.unique(sids[m], return_inverse=True)
        S = len(keys)
        C = np.stack([np.bincount(rng.integers(0, S, S), minlength=S) for _ in range(b)]).astype(float)
        W[:, np.where(m)[0]] = C[:, inv]
    return W


def cell_eval(D: Data, mask: np.ndarray, metrics: dict[str, np.ndarray], pairs: list[tuple[str, str]], seed: int = 0) -> dict:
    """strat AUROC (+ pooled) with stratified cluster-bootstrap CIs for each metric on rows of `mask` where it is present;
    paired deltas on rows where both are present."""
    idx = np.where(mask)[0]
    y, st, sid = D.y[idx], D.stratum[idx], D.sid[idx]
    out = {"n_rows": int(len(idx)), "n_error": int(y.sum()), "n_correct": int(len(idx) - y.sum()),
           "n_sentences": int(len(set(sid))), "n_err_sent": int(len(set(sid[y == 1]))), "n_cor_sent": int(len(set(sid[y == 0]))),
           "metrics": {}, "deltas": {}}
    out["testable"] = bool(out["n_error"] >= 50 and out["n_correct"] >= 50 and out["n_err_sent"] >= 25 and out["n_cor_sent"] >= 25)
    if len(idx) == 0 or y.sum() == 0 or y.sum() == len(y):
        return out
    W = strat_boot_weights(sid, st, B, seed)
    for name, v in metrics.items():
        s = v[idx]
        m = ~np.isnan(s)
        if m.sum() < 10 or len(set(y[m])) < 2:
            out["metrics"][name] = {"n": int(m.sum()), "strat": None}
            continue
        f = WStratAuc(y[m], s[m], st[m])
        vals = np.array([f(W[b][m]) for b in range(B)])
        out["metrics"][name] = {"n": int(m.sum()), "strat": float(strat_auc(y[m], s[m], st[m])), "strat_ci": ci(vals),
                                "pooled": float(auc(y[m], s[m])), "coverage": float(m.mean())}
    for a, c in pairs:
        if a not in metrics or c not in metrics:
            continue
        sa, sc = metrics[a][idx], metrics[c][idx]
        m = ~np.isnan(sa) & ~np.isnan(sc)
        if m.sum() < 10 or len(set(y[m])) < 2:
            continue
        fa, fc = WStratAuc(y[m], sa[m], st[m]), WStratAuc(y[m], sc[m], st[m])
        d = np.array([fa(W[b][m]) - fc(W[b][m]) for b in range(B)])
        pt = strat_auc(y[m], sa[m], st[m]) - strat_auc(y[m], sc[m], st[m])
        c95 = ci(d)
        ym, sm_ = y[m], sid[m]
        ne, nc = int(ym.sum()), int(len(ym) - ym.sum())
        out["deltas"][f"{a} - {c}"] = {"n": int(m.sum()), "n_error": ne, "n_correct": nc,
                                       "testable": bool(ne >= 50 and nc >= 50 and len(set(sm_[ym == 1])) >= 25 and len(set(sm_[ym == 0])) >= 25),
                                       "delta": float(pt), "ci": c95, "p_le0": float(np.mean(d <= 0)),
                                       "ci_gt0": bool(c95[0] is not None and c95[0] > 0),
                                       "pooled_delta": float(auc(y[m], sa[m]) - auc(y[m], sc[m]))}
        # sensitivity: frozen pooled sentence-cluster bootstrap (eval-2 SentBoot)
        sb = SentBoot(sid[m], B, 0)
        Wp = sb.W()
        dp = np.array([fa(Wp[b]) - fc(Wp[b]) for b in range(B)])
        out["deltas"][f"{a} - {c}"]["ci_pooled_cluster_boot"] = ci(dp)
    return out


def mde80(se: float) -> float:
    return (1.959964 + 0.841621) * se


# ================================================================================================================ S4
def s4(D: Data, reg: np.ndarray) -> dict:
    from src.s4 import fit_s4_oof
    idx = np.where(reg)[0]
    table = []
    for i in idx:
        r = D.rows[i]
        t = {"row_key": r["row_key"]}
        for f in S4_FEATS + [PRIMARY]:
            t[f] = r.get(f)
            t[f + "__status"] = "ok" if r.get(f) is not None else "na"
        table.append(t)
    labels = {D.rows[i]["row_key"]: int(D.y[i]) for i in idx}
    folds = {D.rows[i]["row_key"]: int(D.rows[i]["fold_E2"]) for i in idx}
    feats_avail = [f for f in S4_FEATS if np.mean([t[f] is not None for t in table]) >= 0.95]
    small, info_s = fit_s4_oof(table, labels, folds, feats_avail, C=1.0)
    big, info_b = fit_s4_oof(table, labels, folds, feats_avail + [PRIMARY], C=1.0)
    return {"S4_E2": small, "S4_E2_plus_V0": big, "features": feats_avail,
            "features_dropped_lt95pct": [f for f in S4_FEATS if f not in feats_avail],
            "coefs_small": info_s["coefs"], "coefs_big": info_b["coefs"]}


# ================================================================================================================ H-MECH
def load_pairwise() -> dict:
    sys.path.insert(0, str(WS / "freeze_copy"))
    import consensus_variants as CV
    return {r["sentence_id"]: CV.build_index(r) for r in jl(WS / "cache" / "pairwise_E2.jsonl") if "error" not in r}, CV


def hmech(D: Data, reg: np.ndarray) -> dict:
    ix, CV = load_pairwise()
    lab = {D.rows[i]["row_key"]: int(D.y[i]) for i in np.where(reg)[0]}
    rows_by_sid = defaultdict(list)
    for i in np.where(reg)[0]:
        rows_by_sid[D.rows[i]["sentence_id"]].append(i)
    out = {}
    # (i) non-agreeing peers of CORRECT candidates: share labelled ERROR (peer label must be in R_AB)
    for pool_nm, fams in (("all_families", None), ("pool3_deepseek_microsoft_openai", CV.POOL3)):
        per_sent = defaultdict(lambda: [0, 0])
        for i in np.where(reg & (D.y == 0))[0]:
            r = D.rows[i]
            I = ix.get(r["sentence_id"])
            if I is None or r["row_key"] not in I["node_of"]:
                continue
            P = CV.peers_lofo(I, r["row_key"], families=fams)
            c = I["node_of"][r["row_key"]]
            for p in P:
                if CV.agree(I, c, I["node_of"][p]) or p not in lab:
                    continue
                per_sent[r["sentence_id"]][0] += lab[p]
                per_sent[r["sentence_id"]][1] += 1
        sids = sorted(per_sent)
        num = np.array([per_sent[s][0] for s in sids], float)
        den = np.array([per_sent[s][1] for s in sids], float)
        rng = np.random.default_rng(0)
        bs = []
        for _ in range(B):
            k = rng.integers(0, len(sids), len(sids))
            bs.append(num[k].sum() / den[k].sum() if den[k].sum() else np.nan)
        share = num.sum() / den.sum() if den.sum() else None
        c95 = ci(bs)
        out[f"i_{pool_nm}"] = {"share_nonagreeing_peers_labelled_ERROR": share, "ci": c95, "n_peer_judgements": int(den.sum()),
                               "n_sentences": len(sids),
                               "verdict": ("NOT_READ" if den.sum() < 50 else "CONFIRMED" if share >= 0.5 else "REFUTED")}
    # (ii) SCATTER: SI_err / SI_cor over cross-family labelled pairs (eqmv-equivalent share), same sentences
    si = []
    for sid, ii in rows_by_sid.items():
        I = ix.get(sid)
        if I is None:
            continue
        rs = [(D.rows[i]["row_key"], D.rows[i]["family"], int(D.y[i])) for i in ii if D.rows[i]["row_key"] in I["node_of"]]
        cnt = defaultdict(list)
        for a in range(len(rs)):
            for b in range(a + 1, len(rs)):
                if rs[a][1] == rs[b][1]:
                    continue
                t = "EE" if rs[a][2] + rs[b][2] == 2 else ("CC" if rs[a][2] + rs[b][2] == 0 else "EC")
                cnt[t].append(int(CV.agree(I, I["node_of"][rs[a][0]], I["node_of"][rs[b][0]])))
        if cnt["EE"] and cnt["CC"]:
            si.append((np.mean(cnt["EE"]), np.mean(cnt["CC"])))
    if si:
        a = np.array(si)
        rng = np.random.default_rng(0)
        rb = []
        for _ in range(B):
            k = rng.integers(0, len(a), len(a))
            e_, c_ = a[k, 0].mean(), a[k, 1].mean()
            rb.append(c_ / e_ if e_ > 0 else np.nan)
        ratio = a[:, 1].mean() / a[:, 0].mean() if a[:, 0].mean() > 0 else float("inf")
        out["ii_scatter"] = {"SI_err": float(a[:, 0].mean()), "SI_cor": float(a[:, 1].mean()), "ratio": float(ratio),
                             "ci": ci([x for x in rb if np.isfinite(x)]), "n_sentences": len(si),
                             "verdict": "NOT_READ" if len(si) < 25 else ("CONFIRMED" if ratio >= 2 else "REFUTED")}
    else:
        out["ii_scatter"] = {"verdict": "NOT_READ", "n_sentences": 0}
    # (iii) NET: Delta(e+d) words T3 - T1 of the binary rule flag = c > 0.5 (endorsed = c <= 0.5)
    m = reg & ~np.isnan(D.col(PRIMARY))
    idx = np.where(m)[0]
    words = np.array([D.rows[i]["words"] for i in idx], float)
    q1, q2 = np.quantile(words, [1 / 3, 2 / 3])
    wt = np.where(words <= q1, 1, np.where(words <= q2, 2, 3))
    endorsed = (D.col(PRIMARY)[idx] <= 0.5).astype(float)
    y = D.y[idx]
    sb = SentBoot(D.sid[idx], B, 0)
    Wm = sb.W()

    def ed(w, sel):
        e = (w[..., sel] @ (endorsed[sel] * y[sel])) / (w[..., sel] @ y[sel])
        d = (w[..., sel] @ ((1 - endorsed[sel]) * (1 - y[sel]))) / (w[..., sel] @ (1 - y[sel]))
        return e, d
    one = np.ones(len(idx))
    e1, d1 = ed(one, wt == 1)
    e3, d3 = ed(one, wt == 3)
    eb1, db1 = ed(Wm, wt == 1)
    eb3, db3 = ed(Wm, wt == 3)
    delta = (e3 + d3) - (e1 + d1)
    c95 = ci((eb3 + db3) - (eb1 + db1))
    out["iii_net"] = {"delta_e_plus_d_T3_minus_T1": float(delta), "ci": c95, "e_T1": float(e1), "d_T1": float(d1), "e_T3": float(e3),
                      "d_T3": float(d3), "tercile_cuts_words": [float(q1), float(q2)], "n_T1": int((wt == 1).sum()), "n_T3": int((wt == 3).sum()),
                      "verdict": "CONFIRMED" if delta > 0 else "REFUTED"}
    # (iv) exact vs ALIGN: e and d of the binary rule (> 0.5) per error class
    ce, ca = D.col("c_exact"), D.col(PRIMARY)
    rows = {}

    def cls_of(r):
        ops = r.get("error_ops") or []
        if r.get("label") != "ERROR":
            return "CORRECT"
        if r.get("auto_label") == "VOCAB_GRAN" or (r.get("label_tier") == "B" and not ops):
            return "MEANING_RENAME_type (tier-B VOCAB_GRAN->ERROR)"
        if set(ops) & {"ADD", "DROP"}:
            return "ADD/DROP"
        return "OTHER_ERROR"
    classes = np.array([cls_of(D.rows[i]) for i in range(D.n)])
    ok = reg & ~np.isnan(ce) & ~np.isnan(ca)
    for cl in ("CORRECT", "MEANING_RENAME_type (tier-B VOCAB_GRAN->ERROR)", "ADD/DROP", "OTHER_ERROR"):
        mm = ok & (classes == cl)
        if mm.sum() == 0:
            rows[cl] = {"n": 0}
            continue
        fe, fa = (ce[mm] > 0.5).astype(float), (ca[mm] > 0.5).astype(float)
        sbc = SentBoot(D.sid[mm], B, 0)
        Wc = sbc.W()
        if cl == "CORRECT":  # d = false-alarm share on CORRECT rows
            ex, al = fe, fa
            nm = "d"
        else:  # e = share of ERROR rows endorsed (not flagged)
            ex, al = 1 - fe, 1 - fa
            nm = "e"
        diff_b = (Wc @ (al - ex)) / Wc.sum(1)
        rows[cl] = {"n": int(mm.sum()), "stat": nm, "exact": float(ex.mean()), "ALIGN": float(al.mean()),
                    "ALIGN_minus_exact": float((al - ex).mean()), "ci": ci(diff_b)}
    lower_d = rows.get("CORRECT", {}).get("ALIGN_minus_exact", 0) < 0
    higher_e = [rows.get(k, {}).get("ALIGN_minus_exact", 0) > 0 for k in ("MEANING_RENAME_type (tier-B VOCAB_GRAN->ERROR)", "ADD/DROP")
                if rows.get(k, {}).get("n", 0) > 0]
    rd = rows.get("CORRECT", {}).get("n", 0) >= 50
    out["iv_exact_vs_align"] = {"by_class": rows, "ALIGN_lower_d": lower_d, "ALIGN_higher_e_on_rename_and_adddrop": all(higher_e) if higher_e else None,
                                "verdict": "NOT_READ" if not rd or not higher_e else ("CONFIRMED" if lower_d and all(higher_e) else "REFUTED")}
    return out


# ================================================================================================================ analyse
def stage_analyse(prefix: int = 0) -> None:
    rows = jl(WS / "per_item_E2A.jsonl")
    if prefix:  # budget-stop fallback: analyse only the completed random prefix of the frozen sha1 order
        order = json.loads((E2S / "work" / "e2a_order.json").read_text())[:prefix]
        keep = set(order)
        rows = [r for r in rows if r["sentence_id"] in keep]
        dump("prefix_used.json", {"prefix_sentences": prefix, "n_rows": len(rows),
                                  "by_stratum": dict(Counter(r["stratum"] for r in rows if True)),
                                  "sentences_by_stratum": dict(Counter(r["stratum"] for r in {r["sentence_id"]: r for r in rows}.values()))})
    D = Data(rows)
    metrics = {m: D.col(m) for m in METRICS}
    reg = D.regime["R_AB"]
    # ---------------- S4 stack on all R_AB rows (every stratum), OOF by E2 folds
    S4 = s4(D, reg)
    for nm in ("S4_E2", "S4_E2_plus_V0"):
        v = np.full(D.n, np.nan)
        for i in np.where(reg)[0]:
            p = S4[nm].get(D.rows[i]["row_key"])
            v[i] = np.nan if p is None else p
        metrics[nm] = v
    pairs = [(PRIMARY, BAR), (PRIMARY, "judge_cheap_orig"), (PRIMARY, "judge_cheap2_orig"), (PRIMARY, "judge_cheap2_disg"),
             (PRIMARY, "judge_local_qwen8b_disg"), (PRIMARY, "judge_local_qwen8b_orig"), ("p_peer_text", BAR),
             ("p_peer_text", "judge_local_qwen8b_disg"), ("S4_E2_plus_V0", "S4_E2"), ("S4_E2", BAR),
             (PRIMARY, "S4_E2"), (PRIMARY, "c_exact"), (PRIMARY, "p_peer_text")] + \
            [(v, PRIMARY) for v in ("c_pn", "c_rw", "c_pn_rw", "c_two", "c_v5", "c_exact")]
    A = {}
    for rn in ("R_AB", "R_A", "R_VEX", "R_AB_nopilot"):
        A[rn] = {}
        for cn, cm in D.cells.items():
            if rn != "R_AB" and cn == "ALL":
                continue
            A[rn][cn] = cell_eval(D, D.regime[rn] & cm, metrics, pairs if rn == "R_AB" else pairs[:6] + [("S4_E2_plus_V0", "S4_E2")])
            print(f"{rn} {cn}: n={A[rn][cn]['n_rows']} testable={A[rn][cn]['testable']}", flush=True)
    dump("auroc_cells.json", A)
    dump("s4_E2.json", {k: v for k, v in S4.items() if k not in ("S4_E2", "S4_E2_plus_V0")})
    # ---------------- (a) / (b) / verdict
    L = A["R_AB"]["LONG (L25+EXC)"]
    dA = L["deltas"].get(f"{PRIMARY} - {BAR}", {})
    dO = L["deltas"].get(f"{PRIMARY} - judge_cheap_orig", {})
    dN = L["deltas"].get(f"{PRIMARY} - judge_cheap2_orig", {})
    dNd = L["deltas"].get(f"{PRIMARY} - judge_cheap2_disg", {})
    dB = L["deltas"].get("S4_E2_plus_V0 - S4_E2", {})
    a_ok = bool(dA.get("ci_gt0")) and (dO.get("delta", -1) > 0) and (dN.get("delta", -1) > 0)
    b_ok = bool(dB.get("ci_gt0"))
    rc = sorted(glob.glob(str(WS.parent / "*" / "**" / "confirm_verdict_rcomp*.json"), recursive=True))
    c_state = {"status": "PENDING", "source": None}
    if rc:
        try:
            cv = json.loads(Path(rc[0]).read_text())
            c_state = {"status": cv.get("VERDICT", cv.get("criterion_c", cv.get("verdict", "READ"))), "reason": cv.get("reason"), "source": rc[0],
                       "summary": {k: cv[k] for k in list(cv)[:8]}}
        except (json.JSONDecodeError, OSError) as e:
            c_state = {"status": f"UNREADABLE: {e}", "source": rc[0]}
    c_str = json.dumps(c_state["status"]).upper()
    c_holds = ("CONFIRM" in c_str and "NOT" not in c_str and "DIS" not in c_str)
    c_untestable = ("PENDING" in c_str or "UNTESTABLE" in c_str or "NOT_TESTABLE" in c_str or "NOT_READ" in c_str)
    L25 = A["R_AB"]["L25"]
    pt = dA.get("delta")
    if pt is None or not dA.get("testable"):
        overall = "NOT_TESTABLE ((a): too few rows with the pre-registered flash-lite disguised bar; see fallback_substitute_bar)"
    elif pt <= 0:
        overall = "DISCONFIRM"
    elif a_ok and b_ok and c_holds:
        overall = "CONFIRM"
    elif a_ok and (c_untestable or not c_holds):
        overall = "PARTIAL ((a) holds; (c) untestable/pending or n.s.)" + ("" if b_ok else "; (b) NOT met")
    elif (not dA.get("ci_gt0")) and c_holds and pt >= 0.05:
        overall = "PARTIAL (underpowered on E2, confirmed on R_COMP FREE)"
    else:
        overall = "NOT CONFIRMED (point > 0 but (a) CI includes 0; not a DISCONFIRM by the pre-registered rule)"
    L25 = A["R_AB"]["L25"]
    dL = L25["deltas"].get(f"{PRIMARY} - {BAR}", {})
    se_L = (dL["ci"][1] - dL["ci"][0]) / (2 * 1.959964) if dL.get("ci") and dL["ci"][0] is not None else None
    verdict = {
        "criteria_verbatim_source": "prereg_iter5_E2A.json :: hypothesis_criteria_verbatim",
        "a": {"cell": "R_AB LONG (L25+EXC)", "delta_vs_flashlite_disg": dA, "delta_vs_flashlite_orig": dO,
              "delta_vs_nano_orig": dN, "delta_vs_nano_disg": dNd, "holds": a_ok, "n": L["n_rows"], "n_error": L["n_error"],
              "n_correct": L["n_correct"], "n_sentences": L["n_sentences"], "testable": L["testable"]},
        "b": {"nested_S4_E2_plus_V0_minus_S4_E2": dB, "holds": b_ok, "S4_features": S4["features"],
              "S4_features_dropped": S4["features_dropped_lt95pct"], "round_trip": "NOT_RUN (declared: no API/local verbaliser in E2-A)"},
        "c": c_state,
        "fallback_substitute_bar": {"note": "prereg_addendum_budgetstop.json: local Qwen3-8B rubric-A judge, DECLARED SUBSTITUTE, secondary, cannot CONFIRM",
                                    "V0_minus_local_disg": L["deltas"].get(f"{PRIMARY} - judge_local_qwen8b_disg"),
                                    "V0_minus_local_orig": L["deltas"].get(f"{PRIMARY} - judge_local_qwen8b_orig"),
                                    "PT_minus_local_disg": L["deltas"].get("p_peer_text - judge_local_qwen8b_disg"),
                                    "L25_V0_minus_local_disg": L25["deltas"].get(f"{PRIMARY} - judge_local_qwen8b_disg"),
                                    "EXC_V0_minus_local_disg": A["R_AB"]["EXC"]["deltas"].get(f"{PRIMARY} - judge_local_qwen8b_disg"),
                                    "DT_V0_minus_local_disg": A["R_AB"]["DT"]["deltas"].get(f"{PRIMARY} - judge_local_qwen8b_disg")},
        "overall": overall,
        "also_reported": {
            "L25_alone": {"delta": dL, "testable": L25["testable"], "se_from_ci": se_L, "mde80": mde80(se_L) if se_L else None},
            "EXC": A["R_AB"]["EXC"]["deltas"].get(f"{PRIMARY} - {BAR}"),
            "DT_sign": A["R_AB"]["DT"]["deltas"].get(f"{PRIMARY} - {BAR}"),
            "long_without_pilot": A["R_AB_nopilot"]["LONG (L25+EXC)"]["deltas"].get(f"{PRIMARY} - {BAR}"),
            "R_A_long": A["R_A"]["LONG (L25+EXC)"]["deltas"].get(f"{PRIMARY} - {BAR}"),
            "R_VEX_long": A["R_VEX"]["LONG (L25+EXC)"]["deltas"].get(f"{PRIMARY} - {BAR}")}}
    # ---------------- H-MECH, H-IMPROVE, H-RENAME
    HM = hmech(D, reg)
    dump("hmech_E2.json", HM)
    sel = json.loads((WS / "freeze_copy" / "selection.json").read_text())
    imp = {"carried_variant": sel["winner"], "rule": sel["rule_text"],
           "verdict": "V0 STANDS (no variant carried by the freeze; V1-V5 below are DEVELOPMENT-ONLY/exploratory rows)",
           "exploratory_long_pool_deltas_vs_V0": {v: L["deltas"].get(f"{v} - {PRIMARY}") for v in ("c_pn", "c_rw", "c_pn_rw", "c_two", "c_v5", "c_exact")}}
    ps = sorted([(k, v["p_le0"]) for k, v in imp["exploratory_long_pool_deltas_vs_V0"].items() if v], key=lambda t: t[1])
    imp["holm_over_5"] = {k: min(1.0, p * (5 - i)) for i, (k, p) in enumerate(ps)}
    dump("improve_E2.json", imp)
    gg = json.loads((WS / "freeze_copy" / "gg_gate.json").read_text())
    ren = {"GG_dev_gate": gg.get("status"), "verdict": "NOT CONFIRMED (GG failed its pre-registered development gate g3; c_gg not computed on E2)",
           "V0_rename_controls": json.loads((RES / "rename_V0.json").read_text()) if (RES / "rename_V0.json").exists() else "NOT_RUN"}
    dump("rename_E2.json", ren)
    # ---------------- complexity (AUROC by bins, V0 vs bar vs PT) and binary e/d
    comp = {}
    for feat, bins in (("words", None), ("n_conditions", [(0, 1), (2, 2), (3, 3), (4, 99)]), ("n_quant", [(0, 0), (1, 1), (2, 99)]),
                       ("depth", [(0, 2), (3, 3), (4, 4), (5, 99)])):
        v = np.array([np.nan if r.get(feat) is None else float(r[feat]) for r in rows])
        if bins is None:
            q = np.nanquantile(v[reg], [1 / 3, 2 / 3])
            bins = [(-1, q[0]), (q[0] + 1e-9, q[1]), (q[1] + 1e-9, 1e9)]
        comp[feat] = {}
        for lo, hi in bins:
            m = reg & (v >= lo) & (v <= hi)
            ce = cell_eval(D, m, {k: metrics[k] for k in (PRIMARY, BAR, "p_peer_text")}, [(PRIMARY, BAR)])
            ed_ = {}
            for k in (PRIMARY, BAR, "p_peer_text"):
                s = metrics[k][m]
                ok = ~np.isnan(s)
                yy = D.y[m][ok]
                thr = 0.5
                ed_[k] = {"e": float(np.mean(s[ok][yy == 1] <= thr)) if (yy == 1).any() else None,
                          "d": float(np.mean(s[ok][yy == 0] > thr)) if (yy == 0).any() else None}
            comp[feat][f"{lo:g}-{hi:g}"] = {"n": ce["n_rows"], "auroc": {k: ce["metrics"].get(k, {}).get("strat") for k in ce["metrics"]},
                                            "delta_V0_minus_bar": ce["deltas"].get(f"{PRIMARY} - {BAR}"), "binary_e_d_thr0.5": ed_}
    exc_types = sorted({r.get("exception_type") for r in rows if r["stratum"] == "EXC"} - {None})
    comp["exception_type"] = {}
    for et in exc_types:
        m = reg & np.array([r.get("exception_type") == et for r in rows])
        ce = cell_eval(D, m, {k: metrics[k] for k in (PRIMARY, BAR)}, [(PRIMARY, BAR)])
        comp["exception_type"][et] = {"n": ce["n_rows"], "delta": ce["deltas"].get(f"{PRIMARY} - {BAR}")}
    dump("complexity_E2.json", comp)
    # ---------------- system-level Kendall tau-b (10 generator slots): mean score vs error rate on R_AB rows
    from scipy.stats import kendalltau
    sysr = {}
    for k in (PRIMARY, BAR, "p_peer_text", "judge_cheap2_orig"):
        er, ms = [], []
        for slot in sorted({r["slot"] for r in rows}):
            m = reg & np.array([r["slot"] == slot for r in rows]) & ~np.isnan(metrics[k])
            if m.sum() < 10:
                continue
            er.append(D.y[m].mean())
            ms.append(metrics[k][m].mean())
        t = kendalltau(ms, er, variant="b")
        sysr[k] = {"tau_b": float(t.statistic), "p": float(t.pvalue), "n_systems": len(er)}
    dump("system_level_E2.json", sysr)
    # ---------------- coverage (unparseables in the denominator: COVERAGE view, unparseable = ERROR-scored 1.0)
    lab = np.array([r.get("label") for r in rows])
    cov = {"n_rows": D.n, "label_counts": dict(Counter(lab.tolist())), "parse_ok": int(sum(r["parse_ok"] for r in rows)),
           "consensus_imputed_lt2_peers": int(sum(bool(r.get("c_score_align__imputed")) for r in rows)),
           "judge_missing_on_parseable": {k: int(sum(1 for r in rows if r["parse_ok"] and r.get(k) is None)) for k in METRICS if k.startswith("judge")}}
    covm = (reg | (lab == "UNPARSEABLE")) & np.isin(D.stratum, LONG)
    Dc = Data(rows)
    Dc.y = np.where(lab == "UNPARSEABLE", 1.0, D.y)
    cov["COVERAGE_view_long"] = cell_eval(Dc, covm, {k: metrics[k] for k in (PRIMARY, BAR, "p_peer_text")}, [(PRIMARY, BAR)])
    dump("coverage_E2.json", cov)
    # ---------------- placebos
    rng = np.random.default_rng(0)
    m = reg & np.isin(D.stratum, LONG)
    y, s, st = D.y[m], metrics[PRIMARY][m], D.stratum[m]
    sh = [strat_auc(rng.permutation(y), s, st) for _ in range(200)]
    perm = []
    for _ in range(200):
        sp = s.copy()
        for x in np.unique(st):
            k = st == x
            sp[k] = rng.permutation(sp[k])
        perm.append(strat_auc(y, sp, st))
    plac = {"shuffled_labels_mean_auroc": float(np.mean(sh)), "shuffled_labels_p95": float(np.percentile(sh, 95)),
            "within_stratum_score_permutation_mean": float(np.mean(perm)), "pass_0.5pm0.03": bool(abs(np.mean(sh) - 0.5) <= 0.03)}
    dump("placebo_E2.json", plac)
    verdict["placebo"] = plac
    dump("confirm_verdict_E2A.json", verdict)
    print(json.dumps({"overall": overall, "a": {k: dA.get(k) for k in ("delta", "ci", "n")}, "b": {k: dB.get(k) for k in ("delta", "ci")}}, indent=1))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", required=True)
    ap.add_argument("--prefix", type=int, default=0)
    a = ap.parse_args()
    if a.stage == "join":
        stage_join()
    else:
        stage_analyse(a.prefix)


if __name__ == "__main__":
    main()
