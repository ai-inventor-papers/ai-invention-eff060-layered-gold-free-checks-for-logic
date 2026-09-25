#!/usr/bin/env python3
"""STEP 3: verify both seals, join scores to labels ONCE, and write the verdict + every pre-registered analysis.

Confirmatory: criterion (c) on P0 (untouched, gated CORRECT vs ERROR). Under FALLBACK B there are 0 CORRECT rows, so
the verdict is NOT_TESTABLE.
PROVISIONAL (addendum prereg, non-confirmatory): ERROR_CERT (y=1) vs MAPPED = UNRESOLVED_GLOSS_GATE_FAILED (y=0), with
identical statistics. The audit-based noise correction and the audit-labelled view run when results/audit_report.json
exists.

Outputs: results/analysis_rcomp.json, results/confirm_verdict_rcomp.json, results/per_item_rcomp_free.jsonl,
results/tables.md.
usage: join_and_test.py [--quick]   (--quick: B=200, fewer permutations; for testing only)
"""
from __future__ import annotations

import argparse
import glob
import json
import sys
import time
from collections import Counter, defaultdict

import numpy as np
import pandas as pd
from scipy.stats import kendalltau

import analysis_lib as AL
from auc_tools import StratAUC
from cc import B, E7, EV2, EV3, LOGS, RES, RUN, SEED, WS, dump, jl, setup_logger, sha256_bytes, sha256_file, vec_sha, wilson

sys.path.append(str(EV2 / "src"))
import consensus_mx as CS  # noqa: E402
import mechanism as MC  # noqa: E402
from stats import SentBoot  # noqa: E402

logger = setup_logger("join_and_test")
METRICS = ["c_score_align", "c_exact", "c_score_hyb", "c_score_nf", "g_align", "g_nf", "judge_cheap_disg", "judge_cheap_orig",
           "judge_local_disg", "judge_local_orig"]
VARIANTS = ["V1_c_pn", "V2_c_rw", "V3_c_pn_rw", "V5_c_v5"]
MAPPED = "UNRESOLVED_GLOSS_GATE_FAILED"
QWEN_SLOT_MODEL = "qwen/qwen3-235b-a22b-2507"


# ================================================================================================ seals
def verify_seals() -> dict:
    labs = jl(RES / "rcomp_free_labels_final.jsonl")
    seal = json.loads((RES / "seal.json").read_text())["seals"][-1]
    lv = lambda rs: sha256_bytes(json.dumps(sorted((r["row_key"], r["label"]) for r in rs), ensure_ascii=False).encode())  # noqa: E731
    out = {"label_all": lv(labs) == seal["label_vector_sha256_all_rows"],
           "label_untouched": lv([r for r in labs if not r["seen_iter3"]]) == seal["label_vector_sha256_untouched"],
           "label_seal_mode": seal["mode"], "label_seal_all": seal["label_vector_sha256_all_rows"],
           "label_seal_untouched": seal["label_vector_sha256_untouched"]}
    ss = json.loads((RES / "score_seal_rcomp.json").read_text())
    sc = jl(RES / "scores_rcomp_free.jsonl")
    out["score_columns_ok"] = {c: (vec_sha([(o["row_key"], o.get(c)) for o in sc]) == v["all"] and
                                   vec_sha([(o["row_key"], o.get(c)) for o in sc if o["untouched"]]) == v["untouched"])
                               for c, v in ss["columns"].items()}
    out["score_file_ok"] = sha256_file(RES / "scores_rcomp_free.jsonl") == ss["scores_file_sha256"]
    out["prereg_ok"] = sha256_file(WS / "prereg_rcomp_confirm.json") == (WS / "prereg_rcomp_confirm.sha256").read_text().split()[0]
    out["addendum_ok"] = sha256_file(WS / "prereg_addendum_fallbackB.json") == (WS / "prereg_addendum_fallbackB.sha256").read_text().split()[0]
    out["ALL_OK"] = bool(out["label_all"] and out["label_untouched"] and all(out["score_columns_ok"].values()) and out["score_file_ok"]
                         and out["prereg_ok"] and out["addendum_ok"])
    return out


def poll_m1() -> dict:
    hits = glob.glob(str(RUN / "iter_5/gen_art/*/freeze/CONSENSUS_FREEZE_READY.json"))
    rec = {"utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "hits": hits}
    ok = None
    for h in hits:
        try:
            d = json.loads(open(h).read())
            ok = {"path": h, "token_ok": d.get("token") == "aii_iter5_consensus_freeze_v1", "content": d}
        except (OSError, json.JSONDecodeError) as e:
            ok = {"path": h, "error": str(e)[:200]}
    rec["marker"] = ok
    with (LOGS / "poll_M1.log").open("a") as fh:
        fh.write(json.dumps(rec, default=str) + "\n")
    return rec


# ================================================================================================ data
def load_joined() -> pd.DataFrame:
    labs = {r["row_key"]: r for r in jl(RES / "rcomp_free_labels_final.jsonl")}
    sc = jl(RES / "scores_rcomp_free.jsonl")
    rows = []
    for s in sc:
        l = labs[s["row_key"]]
        cert = l.get("nonequiv_certificate_type_counts") or {}
        rows.append({**{k: v for k, v in s.items() if k not in ("s1_detectors",)}, "s1_detectors": ",".join(s["s1_detectors"]),
                     "label": l["label"], "label_binary": l["label_binary"], "matched_reading_search": l.get("matched_reading_search"),
                     "cert_dominant": max(cert, key=cert.get) if cert else None, "cert_counts": json.dumps(cert),
                     "old_label_iter3": l.get("old_label_iter3")})
    D = pd.DataFrame(rows)
    D["y_conf"] = D.label_binary.map({"ERROR": 1.0, "CORRECT": 0.0})
    D["y"] = D.label.map({"ERROR_CERT": 1.0, MAPPED: 0.0})
    D["qwen_slot"] = D.system.str.contains(QWEN_SLOT_MODEL, regex=False)
    sel = WS / "freeze_copy/selection.json"
    if sel.exists():  # M1 frozen V4 coefficients (label-free application to two SEALED columns)
        co = json.loads(sel.read_text())["V4_coefficients_frozen"]
        z = co["intercept"] + co["c_exact"] * D.c_exact + co["c_align"] * D.c_score_align
        D["V4_c_two_channel"] = 1 / (1 + np.exp(-z))
        if "V4_c_two_channel" not in VARIANTS:
            VARIANTS.append("V4_c_two_channel")
    D["not_end_maj_align"] = 1.0 - D.end_maj_align.astype(float)
    D["not_end_maj_exact"] = 1.0 - D.end_maj_exact.astype(float)
    return D


def view_pop(D: pd.DataFrame, judge: str, untouched: bool = True) -> pd.DataFrame:
    m = D.y.notna() & D.c_score_align.notna() & D[judge].notna()
    if untouched:
        m &= D.untouched
    return D[m]


# ================================================================================================ analyses
def confirmatory(D: pd.DataFrame) -> dict:
    out = {}
    for view, j in (("disg", "judge_cheap_disg"), ("orig", "judge_cheap_orig")):
        P = D[D.untouched & D.y_conf.notna() & D.c_score_align.notna() & D[j].notna()]
        n1, n0 = int((P.y_conf == 1).sum()), int((P.y_conf == 0).sum())
        s1, s0 = P[P.y_conf == 1].sentence_id.nunique(), P[P.y_conf == 0].sentence_id.nunique()
        out[view] = {"n_ERROR": n1, "n_CORRECT": n0, "sentences_ERROR": int(s1), "sentences_CORRECT": int(s0),
                     "TESTABLE": bool(n1 >= 50 and n0 >= 50 and s1 >= 25 and s0 >= 25)}
    out["verdict"] = "NOT_TESTABLE" if not (out["disg"]["TESTABLE"] and out["orig"]["TESTABLE"]) else "TESTABLE"
    out["reason"] = ("FALLBACK B: the gloss gate failed twice (gloss_v1 half A, gloss_v2 half B); every MAPPED row is "
                     "UNRESOLVED_GLOSS_GATE_FAILED, so the gated label set has 0 CORRECT rows")
    out["label_counts_all"] = dict(Counter(D.label))
    out["label_counts_untouched"] = dict(Counter(D[D.untouched].label))
    return out


def metric_table(P: pd.DataFrame, boot: AL.Boot, cols: list[str], ycol: str = "y") -> dict:
    out = {}
    for m in cols:
        out[m] = {"within_template": AL.auc_block(P, m, boot, ycol), "pooled": AL.auc_block(P, m, boot, ycol, stratum="pooled")}
    return out


def headline(D: pd.DataFrame, boot: AL.Boot, untouched: bool = True, ycol: str = "y") -> dict:
    o = {}
    for view, j in (("disg", "judge_cheap_disg"), ("orig", "judge_cheap_orig")):
        P = view_pop(D, j, untouched) if ycol == "y" else D[D[ycol].notna() & D.c_score_align.notna() & D[j].notna() & (D.untouched if untouched else True)]
        o[view] = AL.paired_delta(P, "c_score_align", j, boot, ycol)
    o["both_ci_gt_0"] = bool(o["disg"].get("ci_lower_gt_0") and o["orig"].get("ci_lower_gt_0"))
    return o


def mech_i(D: pd.DataFrame, sms: dict, boot: AL.Boot) -> dict:
    """Among MAPPED (provisional-CORRECT) candidates' non-agreeing peers: share of peers labelled ERROR_CERT."""
    lab = dict(zip(D.row_key, D.label))
    res = {}
    for role, yv in (("MAPPED_candidates", 0.0), ("ERROR_candidates", 1.0)):
        C = D[(D.y == yv) & D.untouched & D.in_matrix]
        for rule in ("exact", "align"):
            per = defaultdict(Counter)
            for r in C.itertuples():
                sm_ = sms[r.sentence_id]
                ci_ = sm_.row_node[r.row_key]
                fam = sm_.row_meta[r.row_key]["family"]
                for q, m in sm_.row_meta.items():
                    if not m["is_peer"] or m["family"] == fam or q == r.row_key:
                        continue
                    pj = sm_.row_node[q]
                    ag = sm_.is_exact(ci_, pj) if rule == "exact" else sm_.is_eq(ci_, pj)
                    if not ag:
                        per[r.sentence_id][lab.get(q, "MISSING")] += 1
            sids = sorted(per)
            cl = boot.cl(sids)
            tot = np.array([sum(per[s].values()) for s in sids], float)
            blk = {"n_nonagreeing_peer_slots": int(tot.sum()), "n_sentences": len(sids), "label_counts": dict(sum(per.values(), Counter()))}
            for L in ("ERROR_CERT", MAPPED):
                k = np.array([per[s][L] for s in sids], float)
                Wm = boot.W[:, cl].astype(float)
                with np.errstate(invalid="ignore", divide="ignore"):
                    bs = (Wm @ k) / (Wm @ tot)
                blk[f"share_{L}"] = float(k.sum() / tot.sum()) if tot.sum() else None
                blk[f"share_{L}_ci"] = [float(np.nanpercentile(bs, 2.5)), float(np.nanpercentile(bs, 97.5))] if tot.sum() else [None, None]
            blk["note"] = "unparseable / no-output generations are not in the matrix peer pool, so they never appear here"
            if role == "MAPPED_candidates":
                blk["bar_share_ERROR_ge_0.50"] = bool(blk["share_ERROR_CERT"] is not None and blk["share_ERROR_CERT"] >= 0.5)
            res[f"{role}|{rule}"] = blk
    return res


def ed_table(D: pd.DataFrame, boot: AL.Boot) -> dict:
    """(iv) END_MAJ e/d under exact vs ALIGN, overall and by ERROR_CERT dominant certificate type (untouched provisional)."""
    P = D[D.untouched & D.y.notna() & D.end_maj_align.notna()].copy()
    cl = boot.cl(P.sentence_id)
    W = boot.W[:, cl].astype(float)
    y = P.y.to_numpy()
    out = {"n_err": int(y.sum()), "n_cor": int((1 - y).sum())}

    def ed_boot(mask_err, en):
        e = en[mask_err].mean()
        eb = (W[:, mask_err] @ en[mask_err]) / W[:, mask_err].sum(1)
        return float(e), eb
    cor = y == 0
    cells = {"ALL_ERROR": y == 1}
    for t, n in Counter(P[P.y == 1].cert_dominant.fillna("none")).items():
        if n >= 20 and t != "none":
            cells[f"ERROR_CERT:{t}"] = (y == 1) & (P.cert_dominant.to_numpy() == t)
    for rule in ("align", "exact"):
        en = P[f"end_maj_{rule}"].astype(float).to_numpy()
        dv, db = ed_boot(cor, 1 - en)
        out[f"d_{rule}"] = {"d": dv, "ci": [float(np.percentile(db, 2.5)), float(np.percentile(db, 97.5))]}
        out[f"ed_identity_{rule}"] = MC.ed_decomposition(y.astype(int), en.astype(int))
    en_a, en_x = P.end_maj_align.astype(float).to_numpy(), P.end_maj_exact.astype(float).to_numpy()
    _, dba = ed_boot(cor, 1 - en_a)
    _, dbx = ed_boot(cor, 1 - en_x)
    dd = dba - dbx
    d_diff = {"d_align_minus_d_exact": float((1 - en_a)[cor].mean() - (1 - en_x)[cor].mean()),
              "ci": [float(np.percentile(dd, 2.5)), float(np.percentile(dd, 97.5))]}
    d_diff["prediction_d_lower_under_align"] = ("CONFIRMED" if d_diff["ci"][1] < 0 else "REFUTED" if d_diff["ci"][0] > 0 else "INCONCLUSIVE")
    out["d_contrast"] = d_diff
    out["cells"] = {}
    for c, m in cells.items():
        ea, eba = ed_boot(m, en_a)
        ex, ebx = ed_boot(m, en_x)
        de = eba - ebx
        ci = [float(np.percentile(de, 2.5)), float(np.percentile(de, 97.5))]
        out["cells"][c] = {"n": int(m.sum()), "e_align": ea, "e_exact": ex, "e_align_minus_exact": ea - ex, "ci": ci,
                           "prediction_e_higher_under_align": "CONFIRMED" if ci[0] > 0 else "REFUTED" if ci[1] < 0 else "INCONCLUSIVE"}
    out["note"] = "ERROR_GLOSS (meaning-rename analogue) does not exist under FALLBACK B; MAPPED plays the CORRECT role (provisional)"
    return out


def scatter_and_net(D: pd.DataFrame, sms: dict) -> dict:
    P = D[D.y.notna() & D.in_matrix].copy()
    P["y_AB"] = P.y.astype(int)
    P["family_vendor"] = P.family
    P["stratum"] = P.template_id
    P["n_conditions"] = P.nconds_weak.astype(float)
    P["words"] = P.words.astype(float)
    out = {"population": "all FREE rows with provisional labels (pairs need every labelled row of a sentence)"}
    try:
        sc = MC.scatter_index(P, sms, {"words_tercile_cuts": [29.5, 34.5]})
        s = sc["summary"]
        r = s["overall"].get("ratio_SI_cor_over_SI_err_same_sentences", {})
        out["scatter"] = {"overall": {k: s["overall"][k] for k in ("SI_err", "SI_cor", "SI_mix")}, "ratio": r,
                          "by_words_tercile": {k: v.get("ratio_SI_cor_over_SI_err_same_sentences") for k, v in s["by_words_tercile"].items()},
                          "prediction": s["prediction"], "n_pairs": s["n_pairs"],
                          "bar_ratio_ge_2": bool(r.get("ratio") is not None and r["ratio"] >= 2)}
    except (ValueError, KeyError, ZeroDivisionError) as e:
        out["scatter"] = {"error": str(e)[:300]}
    Pn = P.assign(in_RAB=True, long=True, words_t=P.word_tercile.map({"W1": "T1", "W2": "T2", "W3": "T3"}),
                  ncond_bin=P.nconds_weak.map({4: "0-1", 5: "4+"}), end_MAJ=P.end_maj_align.astype(float).fillna(0).astype(int),
                  end_MAJ_EXACT=P.end_maj_exact.astype(float).fillna(0).astype(int))
    Pn = Pn[P.end_maj_align.notna()].reset_index(drop=True)
    out["net"] = {}
    for rule, col in (("END_MAJ_align", "end_MAJ"), ("MAJ_EXACT", "end_MAJ_EXACT")):
        try:
            r = MC.net_test(Pn, SentBoot(Pn.sentence_id.values, b=200, seed=0), col)
            r["bar_words_delta_gt_0"] = bool(r["words_T3_minus_T1"]["delta_e_plus_d"] > 0)
            out["net"][rule] = r
        except (ValueError, np.linalg.LinAlgError) as e:
            # AME refits need both classes of the endorsement indicator; when a rule never endorses an ERROR (e = 0 in
            # every cell) only the Delta(e+d) part is defined: same formula as net_test, computed here with its weights.
            sb = SentBoot(Pn.sentence_id.values, b=200, seed=0)
            W = sb.W()
            y = Pn.y_AB.to_numpy()
            en = Pn[col].to_numpy().astype(float)

            def ed(Wm, m):
                with np.errstate(invalid="ignore", divide="ignore"):
                    return ((Wm[..., m] @ (en[m] * y[m])) / (Wm[..., m] @ y[m]),
                            (Wm[..., m] @ ((1 - en[m]) * (1 - y[m]))) / (Wm[..., m] @ (1 - y[m])))
            lo, hi = Pn.words_t.to_numpy() == "T1", Pn.words_t.to_numpy() == "T3"
            one = np.ones(len(Pn))
            (el, dl), (eh, dh) = ed(one, lo), ed(one, hi)
            (ebl, dbl), (ebh, dbh) = ed(W, lo), ed(W, hi)
            dB = (ebh + dbh) - (ebl + dbl)
            out["net"][rule] = {"words_T3_minus_T1": {"delta_e_plus_d": float((eh + dh) - (el + dl)),
                                                      "ci": [float(np.nanpercentile(dB, 2.5)), float(np.nanpercentile(dB, 97.5))],
                                                      "e_lo": float(el), "e_hi": float(eh), "d_lo": float(dl), "d_hi": float(dh)},
                                "AME": f"undefined ({str(e)[:120]})"}
            out["net"][rule]["bar_words_delta_gt_0"] = bool(out["net"][rule]["words_T3_minus_T1"]["delta_e_plus_d"] > 0)
    out["net_note"] = "eval-2 net_test unchanged, B = 200 (AME refits); ncond '4+ minus 0-1' = nconds 5 minus 4"
    return out


def sensitivities(D: pd.DataFrame, boot: AL.Boot) -> dict:
    base = headline(D, boot)
    rows = {"primary_provisional": base}
    filt = {
        "s1a_drop_detector_rows": D[~D.s1_flag],
        "s1b_drop_detector_ERROR_CERT_only": D[~(D.s1_flag & (D.y == 1))],
        "s3_all_rows_incl_seen_iter3": None,
        "s5_drop_qwen235b_slot": D[~D.qwen_slot],
        "s7_fewshot_only": D[D.prompt_variant == "fewshot_v1"],
    }
    for k, d in filt.items():
        rows[k] = headline(D, boot, untouched=False) if d is None else headline(d, boot)
    P9 = D[D.judge_cheap_orig_source == "exp7"]
    rows["s9_orig_view_exp7_scored_rows_only"] = {"orig": AL.paired_delta(view_pop(P9, "judge_cheap_orig"), "c_score_align", "judge_cheap_orig", boot)}
    P10 = D[D.judge_cheap_disg.notna() & D.judge_cheap_orig.notna()]
    rows["s10_common_support"] = headline(P10, boot)
    rows["s2_s6_s8"] = "not applicable under FALLBACK B (no gloss verdicts exist)"
    for k, v in rows.items():
        if isinstance(v, dict) and "disg" in v:
            v["flip_vs_primary"] = bool(v["both_ci_gt_0"] != base["both_ci_gt_0"])
    # s4 per template
    s4 = {}
    for t in sorted(D.template_id.unique()):
        s4[t] = headline(D[D.template_id == t], boot)
    rows["s4_per_template"] = s4
    return rows


def exploratory_variants(D: pd.DataFrame, boot: AL.Boot) -> dict:
    P = view_pop(D, "judge_cheap_disg")
    P = P[P[VARIANTS].notna().all(axis=1)]
    out, pv = {}, {}
    for v in VARIANTS:
        for ref in ("c_score_align", "judge_cheap_disg"):
            r = AL.paired_delta(P, v, ref, boot)
            out[f"{v} - {ref}"] = r
            pv[f"{v} - {ref}"] = r["p_two_sided"]
    adj = AL.holm(pv)
    for k in out:
        out[k]["p_holm"] = adj[k]
    out["_note"] = ("V1/V2/V3/V5 scored before the label seal with freeze_copy_prelim/consensus_variants.py, byte-identical (sha 6730a63b) to "
                    "the file the sibling M1 marker froze at 11:20:44Z; V4 = sigmoid of the M1-frozen coefficients (freeze_copy/selection.json, "
                    "frozen before the 11:23:52Z label seal) applied to the sealed c_exact and c_align columns, computed after the label seal "
                    "(flag: 'scored after label seal, code frozen externally'); 2-sided bootstrap sign p, Holm over all V-rows")
    out["_auroc"] = {v: AL.auc_block(P, v, boot) for v in VARIANTS}
    return out


def complexity(D: pd.DataFrame, boot: AL.Boot) -> dict:
    out = {}
    for view, j in (("disg", "judge_cheap_disg"), ("orig", "judge_cheap_orig")):
        P = view_pop(D, j)
        o = {}
        for dim, vals in (("word_tercile", ["W1", "W2", "W3"]), ("nconds_weak", [4, 5])):
            o[dim] = {}
            vecs = {}
            for v in vals:
                sub = P[P[dim] == v]
                r = AL.paired_delta(sub, "c_score_align", j, boot)
                o[dim][str(v)] = r
                if r["delta"] is not None:
                    e, bv = AL.delta_boot_vector(sub, "c_score_align", j, boot)
                    ea, ba = AL.delta_boot_vector(sub.assign(_z=0.5), "c_score_align", "_z", boot)
                    ej, bj = AL.delta_boot_vector(sub.assign(_z=0.5), j, "_z", boot)
                    vecs[v] = (e, bv, ea, ba, ej, bj)
            lo, hi = vals[0], vals[-1]
            if lo in vecs and hi in vecs:
                e = vecs[hi][0] - vecs[lo][0]
                b = vecs[hi][1] - vecs[lo][1]
                sa = vecs[hi][2] - vecs[lo][2]
                sab = vecs[hi][3] - vecs[lo][3]
                sj = vecs[hi][4] - vecs[lo][4]
                sjb = vecs[hi][5] - vecs[lo][5]
                o[dim][f"delta_of_deltas_{hi}_minus_{lo}"] = {"est": e, "ci": [float(np.nanpercentile(b, 2.5)), float(np.nanpercentile(b, 97.5))]}
                o[dim][f"slope_c_align_{hi}_minus_{lo}"] = {"est": sa, "ci": [float(np.nanpercentile(sab, 2.5)), float(np.nanpercentile(sab, 97.5))]}
                o[dim][f"slope_judge_{hi}_minus_{lo}"] = {"est": sj, "ci": [float(np.nanpercentile(sjb, 2.5)), float(np.nanpercentile(sjb, 97.5))]}
        out[view] = o
    return out


def system_level(D: pd.DataFrame, boot: AL.Boot) -> dict:
    P = view_pop(D, "judge_cheap_disg")
    P = P.assign(system_id=P.slot + "|" + P.prompt_variant)
    systems = sorted(P.system_id.unique())
    cl = boot.cl(P.sentence_id)
    out = {"n_systems": len(systems)}
    for m in ("c_score_align", "judge_cheap_disg", "judge_cheap_orig", "c_exact"):
        Q = P[P[m].notna()]
        cq = boot.cl(Q.sentence_id)

        def sys_means(w):
            g = pd.DataFrame({"s": Q.system_id.to_numpy(), "w": w, "x": Q[m].to_numpy() * w, "y": Q.y.to_numpy() * w}).groupby("s").sum()
            return (g.x / g.w).to_numpy(), (g.y / g.w).to_numpy()
        mx, ry = sys_means(np.ones(len(Q)))
        tau = kendalltau(mx, ry).statistic
        bs = []
        for b in range(0, boot.B, 4):  # every 4th replicate (500) for speed; disclosed
            w = boot.W[b, cq].astype(float)
            if (pd.Series(w).groupby(Q.system_id.to_numpy()).sum() == 0).any():
                continue
            a, c = sys_means(w)
            bs.append(kendalltau(a, c).statistic)
        out[m] = {"kendall_tau_b": float(tau), "ci": [float(np.nanpercentile(bs, 2.5)), float(np.nanpercentile(bs, 97.5))], "n_boot": len(bs),
                  "per_system": {s: {"mean_score": float(a), "error_rate": float(e)} for s, a, e in zip(sorted(Q.system_id.unique()), mx, ry)}}
    out["note"] = "descriptive; 12 systems (slot x prompt variant); bootstrap uses 500 of the 2,000 shared replicates"
    return out


def coverage(D: pd.DataFrame, boot: AL.Boot) -> dict:
    n = len(D)
    out = {"n_rows": n, "label_counts": dict(Counter(D.label)), "per_metric": {}}
    for m in METRICS + VARIANTS:
        k = int(D[m].notna().sum())
        out["per_metric"][m] = {"scored": k, "share_of_all_2652": k / n, "unparseable_rows": int((D.label == "UNPARSEABLE").sum()),
                                "no_output_rows": int((D.label == "NO_OUTPUT").sum())}
    # unparseable-as-ERROR convention: UNPARSEABLE rows join the ERROR class with every metric set to its maximum (1.0)
    U = D[D.untouched & ((D.y.notna()) | (D.label == "UNPARSEABLE"))].copy()
    U.loc[U.label == "UNPARSEABLE", "y"] = 1.0
    for m in ("c_score_align", "judge_cheap_disg", "judge_cheap_orig", "c_exact"):
        U.loc[U.label == "UNPARSEABLE", m] = 1.0
    out["unparseable_as_ERROR_untouched"] = {"n_unparseable_added": int((U.label == "UNPARSEABLE").sum()),
                                             **{v: AL.paired_delta(U, "c_score_align", j, boot) for v, j in (("disg", "judge_cheap_disg"), ("orig", "judge_cheap_orig"))}}
    return out


def costs(D: pd.DataFrame, sms: dict) -> dict:
    gen = {}
    for r in jl(E7 / "rcomp/raw/generations.jsonl"):
        gen[(r["sentence_id"], r["slot"], r["prompt_variant"])] = float(r.get("cost_usd") or 0.0)
    rk_meta = {r.row_key: (r.sentence_id, r.slot, r.prompt_variant) for r in D.itertuples()}
    full, amort, secs = [], [], []
    pool_cost = defaultdict(float)
    for (sid, slot, pv), c in gen.items():
        if pv == "fewshot_v1":
            pool_cost[sid] += c
    ncand = Counter(D[D.in_matrix].sentence_id)
    for r in D[D.in_matrix & D.c_score_align.notna()].itertuples():
        sm_ = sms[r.sentence_id]
        fam = sm_.row_meta[r.row_key]["family"]
        peers = [q for q, m in sm_.row_meta.items() if m["is_peer"] and m["family"] != fam and q != r.row_key]
        full.append(sum(gen.get(rk_meta[q], 0.0) for q in peers if q in rk_meta))
        amort.append(pool_cost[r.sentence_id] / max(ncand[r.sentence_id], 1))
        ci_ = sm_.row_node[r.row_key]
        secs.append(sum(sm_.secs.get((ci_, sm_.row_node[q]), 0.0) for q in peers))
    jd = [r for r in jl(E7 / "results/judge_FREE.jsonl") if r.get("p") is not None]
    j5 = [r for r in jl(RES / "judge_orig_iter5_FREE.jsonl") if r.get("p") is not None]
    jcost = [r["cost"] for r in jd + j5 if r.get("cost")]
    jsec = [r["seconds"] for r in jd + j5 if r.get("seconds")]
    led = jl(WS / "labeller/cost_ledger.jsonl")
    lab_phase, metric_phase = defaultdict(float), defaultdict(float)
    for r in led:
        ph = r.get("phase", "?")
        (metric_phase if ph.startswith(("judge_orig_completion", "frontier_judge")) else lab_phase)[ph] += float(r.get("usd", 0.0))
    return {"consensus_full_usd_per_candidate_peer_generations": float(np.mean(full)),
            "consensus_amortised_usd_per_candidate": float(np.mean(amort)),
            "consensus_marginal_z3_cpu_seconds_per_candidate_mean": float(np.mean(secs)),
            "consensus_marginal_z3_cpu_seconds_per_candidate_median": float(np.median(secs)),
            "consensus_marginal_api_usd": 0.0,
            "judge_cheap_usd_per_call_mean": float(np.mean(jcost)) if jcost else None,
            "judge_cheap_seconds_per_call_mean": float(np.mean(jsec)) if jsec else None,
            "judge_cheap_seconds_per_call_median": float(np.median(jsec)) if jsec else None,
            "labelling_cost_by_phase_usd (NOT a metric cost)": dict(lab_phase),
            "metric_scoring_cost_by_phase_usd (judge completion / frontier judge)": dict(metric_phase),
            "note": "FULL = generation cost of the candidate's own peer pool (other-family fewshot rows); amortised = the sentence's fewshot pool cost "
                    "shared by every candidate of that sentence; MARGINAL = z3 CPU on the eqmv matrix (no API)"}


def placebos(D: pd.DataFrame, boot: AL.Boot, n_shuffle: int) -> dict:
    P = view_pop(D, "judge_cheap_disg")
    rng = np.random.default_rng(SEED)
    cover = 0
    res = []
    for i in range(n_shuffle):
        yp = P.y.to_numpy().copy()
        for t in P.template_id.unique():
            m = P.template_id.to_numpy() == t
            yp[m] = rng.permutation(yp[m])
        r = AL.paired_delta(P.assign(_y=yp), "c_score_align", "judge_cheap_disg", boot, "_y")
        cover += int(r["ci"][0] <= 0 <= r["ci"][1])
        res.append({"delta": r["delta"], "ci": r["ci"]})
    rnd = AL.auc_block(P.assign(_r=rng.random(len(P))), "_r", boot)
    sup_cover, sup_n = 0, 0 if n_shuffle < 20 else 100
    for i in range(sup_n):  # post-hoc supplement (D26): coverage of the nominal 95% interval under the null
        yp = P.y.to_numpy().copy()
        for t in P.template_id.unique():
            m = P.template_id.to_numpy() == t
            yp[m] = rng.permutation(yp[m])
        r = AL.paired_delta(P.assign(_y=yp), "c_score_align", "judge_cheap_disg", boot, "_y")
        sup_cover += int(r["ci"][0] <= 0 <= r["ci"][1])
    return {"supplement_100_shuffles": {"n": sup_n, "delta_ci_covers_0": sup_cover,
                                        "coverage": sup_cover / sup_n if sup_n else None, "note": "post-hoc supplement (D26)"},
            "label_shuffle_within_template": {"n": n_shuffle, "delta_ci_covers_0": cover, "pass_ge_90pct": cover >= 0.9 * n_shuffle, "runs": res},
            "random_score": {"auroc": rnd["est"], "ci": rnd["ci"], "covers_0.5": bool(rnd["ci"][0] <= 0.5 <= rnd["ci"][1])}}


def noise_correction(D: pd.DataFrame, boot: AL.Boot, head: dict) -> dict | None:
    p = RES / "audit_report.json"
    if not p.exists():
        return None
    rep = json.loads(p.read_text())
    out = {"assumption": "non-differential contamination (a mislabelled row scores like a typical row of its TRUE class)",
           "formula": "A = (AUROC_obs - a(1-b) - b/2) / ((1-b)(1-2a)); delta_true = delta_obs / ((1-b)(1-2a))", "sources": {}}
    srcs = {k: (v["contamination_a_error_side"], v["contamination_b_mapped_side"]) for k, v in rep["by_auditor"].items()}
    srcs["dataset5_executor_audit"] = (1 - 0.867, 1 - 0.867)
    for name, (a, b) in srcs.items():
        f = (1 - b) * (1 - 2 * a)
        blk = {"a": a, "b": b, "scale": f}
        for view in ("disg", "orig"):
            h = head[view]
            corr = lambda A: (A - a * (1 - b) - b / 2) / f if A is not None and f > 0 else None  # noqa: E731
            blk[view] = {"auroc_c_align_obs": h["auroc_a"], "auroc_c_align_corrected": corr(h["auroc_a"]),
                         "auroc_judge_obs": h["auroc_b"], "auroc_judge_corrected": corr(h["auroc_b"]),
                         "delta_obs": h["delta"], "delta_corrected": h["delta"] / f if f > 0 else None,
                         "delta_ci_corrected": [c / f for c in h["ci"]] if f > 0 else None}
        vals = [blk[v][k] for v in ("disg", "orig") for k in ("auroc_c_align_corrected", "auroc_judge_corrected") if blk[v][k] is not None]
        blk["valid_all_corrected_auroc_in_0_1"] = bool(all(0 <= x <= 1 for x in vals))
        out["sources"][name] = blk
    # differential-contamination check on the audited rows: mean score of contaminants vs their labelled class
    pr = {r["row_key"]: r for r in rep["per_row"]}
    names = [k for k in rep["by_auditor"] if k != "consensus"]
    A = D[D.row_key.isin(pr)].copy()

    def cons(rk):
        v = [pr[rk].get(n) for n in names]
        if len(v) >= 2 and all(x in ("FAITHFUL", "FAITHFUL_DIFFERENT_DECOMPOSITION") for x in v):
            return 0.0
        if len(v) >= 2 and all(x == "UNFAITHFUL" for x in v):
            return 1.0
        return np.nan
    A["y_aud"] = A.row_key.map(cons)
    dif = {}
    for m in ("c_score_align", "judge_cheap_disg", "judge_cheap_orig"):
        g = A[A[m].notna() & A.y_aud.notna()].groupby(["y", "y_aud"])[m].agg(["mean", "count"])
        dif[m] = {f"label={'ERROR_CERT' if k[0] == 1 else 'MAPPED'}|auditors={'UNFAITHFUL' if k[1] == 1 else 'FAITHFUL'}": {"mean": float(v["mean"]), "n": int(v["count"])}
                  for k, v in g.iterrows()}
    out["differential_check_mean_scores"] = dif
    return out


def frontier_view(D: pd.DataFrame, boot: AL.Boot) -> dict | None:
    """STEP F: c_score_align vs the frontier judge (gemini-3.1-pro, original view) on the 150-row stratified sample."""
    p = RES / "judge_frontier_FREE.jsonl"
    if not p.exists():
        return None
    fr = {}
    for r in jl(p):
        if r.get("p") is not None:
            fr[r["row_key"]] = 1 - float(r["p"])
    samp = [r["row_key"] for r in json.loads((RES / "frontier_sample.json").read_text())]
    F = D[D.row_key.isin(samp)].copy()
    F["judge_frontier_orig"] = F.row_key.map(fr)
    out = {"n_sample": len(samp), "n_scored": int(F.judge_frontier_orig.notna().sum()),
           "counts": {k: int(v) for k, v in Counter(F[F.judge_frontier_orig.notna()].label).items()},
           "auroc": {m: AL.auc_block(F, m, boot) for m in ("c_score_align", "judge_frontier_orig", "judge_cheap_orig", "judge_cheap_disg", "c_exact")},
           "c_align_minus_frontier": AL.paired_delta(F, "c_score_align", "judge_frontier_orig", boot),
           "frontier_minus_flashlite_orig": AL.paired_delta(F, "judge_frontier_orig", "judge_cheap_orig", boot),
           "nested_[frontier + c] - [frontier]": AL.nested_block(F, ["judge_frontier_orig"], ["c_score_align"], boot, n_perm=50),
           "nested_[c + frontier] - [c]": AL.nested_block(F, ["c_score_align"], ["judge_frontier_orig"], boot, n_perm=50),
           "status": "PROVISIONAL labels (ERROR_CERT vs MAPPED); 150-row stratified sample of the untouched orig-view population"}
    costs = [r["cost"] for r in jl(p) if r.get("cost")]
    secs = [r["seconds"] for r in jl(p) if r.get("seconds")]
    out["cost_usd_per_call_mean"] = float(np.mean(costs)) if costs else None
    out["seconds_per_call_mean"] = float(np.mean(secs)) if secs else None
    return out


def audit_view(D: pd.DataFrame, boot: AL.Boot) -> dict | None:
    p = RES / "audit_report.json"
    if not p.exists():
        return None
    rep = json.loads(p.read_text())
    names = [k for k in rep["by_auditor"] if k != "consensus"]
    pr = {r["row_key"]: r for r in rep["per_row"]}
    F = ("FAITHFUL", "FAITHFUL_DIFFERENT_DECOMPOSITION")

    def cons(rk):
        v = [pr[rk].get(n) for n in names]
        if len(v) >= 2 and all(x in F for x in v):
            return 0.0
        if len(v) >= 2 and all(x == "UNFAITHFUL" for x in v):
            return 1.0
        return np.nan
    A = D[D.row_key.isin(pr)].copy()
    A["y_aud"] = A.row_key.map(cons)
    A["y_aud_and_label"] = np.where(A.y_aud == A.y, A.y_aud, np.nan)
    out = {"status": "EXPLORATORY: LLM-audited (gold-informed) labels on the 200-row audit sample; not gold"}
    for yc in ("y_aud", "y_aud_and_label"):
        o = {}
        for view, j in (("disg", "judge_cheap_disg"), ("orig", "judge_cheap_orig")):
            P = A[A[yc].notna() & A.c_score_align.notna() & A[j].notna()]
            o[view] = AL.paired_delta(P, "c_score_align", j, boot, yc)
        o["c_exact_minus_judge_disg"] = AL.paired_delta(A[A[yc].notna()], "c_exact", "judge_cheap_disg", boot, yc)
        out[yc] = o
    out["n_y_aud"] = dict(Counter(A.y_aud.dropna()))
    return out


# ================================================================================================ main
@logger.catch(reraise=True)
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    a = ap.parse_args()
    Bn = 200 if a.quick else B
    t0 = time.time()
    seals = verify_seals()
    logger.info(f"seals: {({k: v for k, v in seals.items() if k != 'score_columns_ok'})}")
    assert seals["ALL_OK"], "a seal did not verify: refusing to join"
    m1 = poll_m1()
    D = load_joined()
    sent_t = dict(zip(D.sentence_id, D.template_id))
    boot = AL.Boot(list(sent_t), sent_t, Bn, SEED)
    sms = {r["sentence_id"]: CS.SentenceMatrix(r) for r in jl(EV3 / "pairwise_classes_RCOMP.jsonl") if r["condition"] == "FREE"}
    A = {"generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "B": Bn, "seed": SEED, "seals": seals, "m1_poll": m1,
         "orientation": "higher = more likely ERROR"}
    A["confirmatory"] = confirmatory(D)
    logger.info(f"confirmatory: {A['confirmatory']['verdict']} {A['confirmatory']['disg']}")
    P_d = view_pop(D, "judge_cheap_disg")
    P_o = view_pop(D, "judge_cheap_orig")
    A["provisional_counts"] = {v: {"n": len(P), "n_ERROR_CERT": int((P.y == 1).sum()), "n_MAPPED": int((P.y == 0).sum()),
                                   "n_sent": int(P.sentence_id.nunique()), "n_sent_err": int(P[P.y == 1].sentence_id.nunique()),
                                   "n_sent_mapped": int(P[P.y == 0].sentence_id.nunique())} for v, P in (("disg", P_d), ("orig", P_o))}
    A["provisional_headline"] = headline(D, boot)
    logger.info(f"provisional headline: disg {A['provisional_headline']['disg']['delta']:.3f} {A['provisional_headline']['disg']['ci']}; "
                f"orig {A['provisional_headline']['orig']['delta']:.3f} {A['provisional_headline']['orig']['ci']}")
    P_all = D[D.untouched & D.y.notna()]
    A["metrics_untouched_all_scored"] = metric_table(P_all, boot, METRICS + ["not_end_maj_align", "not_end_maj_exact"])
    A["metrics_on_disg_view_pop"] = metric_table(P_d, boot, METRICS)
    A["secondary_deltas"] = {"c_align - judge_local_disg": AL.paired_delta(P_all, "c_score_align", "judge_local_disg", boot),
                             "c_exact - c_align": AL.paired_delta(P_all, "c_exact", "c_score_align", boot),
                             "c_hyb - judge_cheap_disg": AL.paired_delta(P_d, "c_score_hyb", "judge_cheap_disg", boot),
                             "c_exact - judge_cheap_disg": AL.paired_delta(P_d, "c_exact", "judge_cheap_disg", boot),
                             "c_exact - judge_cheap_orig": AL.paired_delta(P_o, "c_exact", "judge_cheap_orig", boot),
                             "judge_cheap_orig - judge_cheap_disg (contamination view gap)": AL.paired_delta(
                                 D[D.untouched & D.y.notna() & D.judge_cheap_disg.notna()], "judge_cheap_orig", "judge_cheap_disg", boot)}
    logger.info(f"metrics done {time.time() - t0:.0f}s")
    npm = 10 if a.quick else 50
    A["nested"] = {"[judge_disg + c] - [judge_disg]": AL.nested_block(P_d, ["judge_cheap_disg"], ["c_score_align"], boot, n_perm=npm),
                   "[judge_orig + c] - [judge_orig]": AL.nested_block(P_o, ["judge_cheap_orig"], ["c_score_align"], boot, n_perm=npm),
                   "[c + judge_disg] - [c]": AL.nested_block(P_d, ["c_score_align"], ["judge_cheap_disg"], boot, n_perm=npm),
                   "[c + judge_orig] - [c]": AL.nested_block(P_o, ["c_score_align"], ["judge_cheap_orig"], boot, n_perm=npm)}
    logger.info(f"nested done {time.time() - t0:.0f}s")
    A["operating_points"] = {
        "c_align_majority_rule_gt_0.5 (label-free)": AL.op_point(P_d, "c_score_align", 0.5),
        "judge_disg_rubric_p_lt_0.5": AL.op_point(P_d, "judge_cheap_disg", 0.5),
        "judge_orig_rubric_p_lt_0.5": AL.op_point(P_o, "judge_cheap_orig", 0.5)}
    for m, P in (("c_score_align", P_d), ("judge_cheap_disg", P_d), ("judge_cheap_orig", P_o)):
        th = AL.thr_at_fa(P, m, 0.10)
        for side, t in th.items():
            if t is not None:
                A["operating_points"][f"{m}_FA_bracket_0.10_{side} (label-chosen, descriptive)"] = AL.op_point(P, m, t)
    A["h_mech"] = {"i_nonagreeing_peers": mech_i(D, sms, boot), "iv_e_d": ed_table(D, boot)}
    A["h_mech"].update(scatter_and_net(D, sms))
    logger.info(f"h-mech done {time.time() - t0:.0f}s")
    A["sensitivities"] = sensitivities(D, boot)
    A["exploratory_variants"] = exploratory_variants(D, boot)
    A["complexity"] = complexity(D, boot)
    A["system_level"] = system_level(D, boot)
    A["coverage"] = coverage(D, boot)
    A["cost"] = costs(D, sms)
    logger.info(f"sens/variants/complexity/system/coverage/cost done {time.time() - t0:.0f}s")
    A["placebos"] = placebos(D, boot, 5 if a.quick else 20)
    A["noise_correction"] = noise_correction(D, boot, A["provisional_headline"])
    A["audit_labelled_view"] = audit_view(D, boot)
    A["frontier"] = frontier_view(D, boot)
    A["runtime_s"] = time.time() - t0
    dump(RES / ("analysis_rcomp_quick.json" if a.quick else "analysis_rcomp.json"), A)
    if not a.quick:
        cols = ["row_key", "sentence_id", "template_id", "slot", "system", "family", "prompt_variant", "words", "word_tercile", "nconds_weak",
                "clause_type", "label", "label_binary", "y", "seen_iter3", "untouched", "s1_flag", "s1_detectors", "cert_dominant",
                "matched_reading_search", "old_label_iter3", "coverage_status", "judge_cheap_orig_source", "npc", "end_maj_align", "end_maj_exact",
                "candidate_fol"] + METRICS + VARIANTS
        with (RES / "per_item_rcomp_free.jsonl").open("w") as fh:
            for r in D[cols].to_dict("records"):
                r = {k: (None if isinstance(v, float) and np.isnan(v) else v) for k, v in r.items()}
                r["label_haiku_only"] = "NOT_APPLICABLE_GATE_FAILED" if r["label"] == MAPPED else r["label"]
                r["label_provisional"] = {1.0: "ERROR_CERT", 0.0: "MAPPED"}.get(r["y"])
                fh.write(json.dumps(r, ensure_ascii=False, default=lambda x: x.item() if hasattr(x, "item") else str(x)) + "\n")
    logger.info(f"done in {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
