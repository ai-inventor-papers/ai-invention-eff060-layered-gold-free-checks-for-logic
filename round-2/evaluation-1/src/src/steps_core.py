"""Steps 1-5: bookkeeping, independent re-derivation, label regimes, common-item tables, regime-shift matrix."""
from __future__ import annotations

import hashlib
import itertools
import json
import random
from collections import Counter

import numpy as np
import pandas as pd
from loguru import logger
from scipy import stats as sps
from sklearn.metrics import roc_auc_score

import stats_utils as su
from load import AUDIT, EXP_C, EXP_D

BIN = ("CORRECT", "ERROR")
UNC = ("UNCERTAIN", "UNCERTAIN_COMPOUND", "UNCERTAIN_GRAN")

# headline metrics (oriented, higher = error); order = table order
HEADLINE_L = ["p_fused_H", "bow_uncarried", "l2_bow_Adef", "l3_score", "n_smells", "role_count", "c_score",
              "c_score_peers6", "medoid_depth", "cluster_entropy", "sc5_cheap", "judge_cheap_disg", "judge_cheap_orig",
              "judge_cheap2_disg", "judge_cheap2_orig", "rt_nli_min", "rt_nli_min_localverb", "rt_embed_cos",
              "parse_fail", "pilot_rerun_jacc", "pilot_joint_conflict"]
# LABEL-CONDITIONAL / sparse metrics: they exist only on a label-dependent subset (p_fused_Lcf was cross-fitted on exp A's
# CORRECT/ERROR items, best_baseline_oof = shipped S4 on exp D's CORRECT/ERROR items, rt_reformalise_eq fails to parse on
# ~7% of items). Requiring them would shrink every common set to the A/D-binary items (e.g. R_ADJ_AB 474 -> 154), so they
# are scored on (common set AND non-null) in a separate SUBSET block, with the judge re-scored on the same subset.
SECONDARY_L = ["p_fused_Lcf", "best_baseline_oof", "rt_reformalise_eq"]
# fused_H was fitted on track H (in-sample there) and p_fused_Lcf exists on L only -> excluded from H
HEADLINE_H = [m for m in HEADLINE_L if m not in ("p_fused_H",)]
SECONDARY_H = ["rt_reformalise_eq"]
HOLM_FAMILY = ["p_fused_H", "c_score", "bow_uncarried", "l3_score", "S4_refit_oof", "PT_oof"]
REF = "judge_cheap_disg"
NICE = {"p_fused_H": "fused_H", "p_fused_Lcf": "fused_Lcf", "bow_uncarried": "L2_bow", "l3_score": "L3",
        "n_smells": "L1_smells", "role_count": "L2_role", "best_baseline_oof": "S4_shipped", "PT_oof": "PT",
        "PTJ_oof": "PT_J", "l2_bow_Adef": "L2_bow_Adef(n_unanch+uncarried)", "S4_refit_oof": "S4_refit", "S4PT_oof": "S4_PT", "PTg_oof": "PT_g"}


def nice(m: str) -> str:
    return NICE.get(m, m)


# ================================================================================================= STEP 1
def step1_bookkeeping(df: pd.DataFrame, raw: dict, out_tab) -> dict:
    res = {}
    L = df[df.track == "L"]
    rows = []
    for exp, col, inc in [("A", "lab_A", "in_A"), ("C", "lab_C", "in_C"), ("D", "lab_D", "in_D"), ("E", "E_final_label", "in_E")]:
        for tr in ("L", "H"):
            sub = df[(df.track == tr) & df[inc]]
            cnt = sub[col].value_counts(dropna=False).to_dict()
            rows.append({"experiment": exp, "track": tr, "n": len(sub), "label_counts": json.dumps({str(k): int(v) for k, v in cnt.items()})})
    # label-vector sha1 conventions
    Dscreen = raw["D_screen"]
    lv_file = "\n".join(f"{r['item_id']}:{r['label']}" for r in Dscreen)
    lv_sorted = "\n".join(sorted(f"{r['item_id']}:{r['label']}" for r in Dscreen))
    lv_list = "\n".join(r["label"] for r in Dscreen)
    d_reported = (EXP_D / "data/label_vector.sha1").read_text().strip()
    Cs = json.loads((EXP_C / "results/screen_items.json").read_text())
    c_reported = (EXP_C / "results/screen_label_hash.txt").read_text().strip()
    c_tab = hashlib.sha256("\n".join(sorted(f"{x['item_id']}\t{x['label']}" for x in Cs)).encode()).hexdigest()
    c_sha1_sorted = hashlib.sha1("\n".join(sorted(f"{x['item_id']}:{x['label']}" for x in Cs)).encode()).hexdigest()
    As = raw["A_screen"]
    a_sha1_sorted = hashlib.sha1("\n".join(sorted(f"{x['item_id']}:{x['label']}" for x in As)).encode()).hexdigest()
    a_sha256_tab = hashlib.sha256("\n".join(sorted(f"{x['item_id']}\t{x['label']}" for x in As)).encode()).hexdigest()
    hashes = {
        "D": {"reported": d_reported, "sha1_file_order_id:label": hashlib.sha1(lv_file.encode()).hexdigest(),
              "sha1_sorted_id:label": hashlib.sha1(lv_sorted.encode()).hexdigest(),
              "sha1_label_list_file_order": hashlib.sha1(lv_list.encode()).hexdigest()},
        "C": {"reported": c_reported, "sha256_sorted_id\\tlabel (C screen.py convention)": c_tab,
              "sha1_sorted_id:label": c_sha1_sorted},
        "A": {"sha1_sorted_id:label": a_sha1_sorted, "sha256_sorted_id\\tlabel": a_sha256_tab},
    }
    hashes["D"]["reproduced_by"] = [k for k, v in hashes["D"].items() if k != "reported" and v == d_reported] or ["NONE"]
    hashes["C"]["reproduced_by"] = [k for k, v in hashes["C"].items() if k != "reported" and v == c_reported] or ["NONE"]
    hashes["note"] = ("D's 122d01df... = sha1 over 'item_id:label' lines in file order (file is sorted by item_id, so it "
                      "equals the sorted convention); C's 0e43cbdd... = sha256 over sorted 'item_id<TAB>label' lines "
                      "(C src/screen.py line 319-320). The two hashes use different algorithms AND separators, so they "
                      "could never have been compared directly; the label vectors also differ (see label_disagreements).")
    res["label_hashes"] = hashes
    # set counts
    common = L[L.in_A & L.in_C & L.in_D]
    cons = common[(common.lab_A == common.lab_C) & (common.lab_C == common.lab_D) & common.lab_A.isin(BIN)]
    cons_j = cons[cons[REF].notna()]
    res["sets"] = {"n_L_A": int(L.in_A.sum()), "n_L_C": int(L.in_C.sum()), "n_L_D": int(L.in_D.sum()), "n_L_E": int(L.in_E.sum()),
                   "n_common_ACD": len(common), "n_common_ACDE": int((common.in_E).sum()),
                   "n_label_consistent_binary": len(cons), "n_err_consistent": int((cons.lab_A == "ERROR").sum()),
                   "n_consistent_with_judge_disg": len(cons_j), "n_err_consistent_with_judge": int((cons_j.lab_A == "ERROR").sum()),
                   "n_sentences_consistent_with_judge": int(cons_j.cluster.nunique()),
                   "expected": "588 / ~389-400 / 389 with 160 errors and 151 sentences"}
    triples = Counter(zip(common.lab_A, common.lab_C, common.lab_D))
    res["label_triples_common"] = {f"{a}|{c}|{d}": int(v) for (a, c, d), v in triples.most_common()}
    # disagreement cascade
    drows = []
    for k, r in common.iterrows():
        labs = [r.lab_A, r.lab_C, r.lab_D]
        if len(set(labs)) == 1:
            continue
        acs = {str(r.auto_class_A), str(r.auto_class_C), str(r.auto_class_D)}
        gran = bool(r.D_vocab_borderline is True or r.C_vocab_strict is False or (acs & {"VOCAB", "GRAN"})
                    or r.lab_C == "UNCERTAIN_GRAN")
        fol_all = f"{r.candidate_fol} {r.reference_fol}"
        if all(l in UNC for l in labs):
            reason = "UNCERTAIN_NAMING_ONLY"  # e.g. A/D 'UNCERTAIN' vs C 'UNCERTAIN_COMPOUND': same verdict, different name
        elif any(l in UNC for l in labs) and any(l in BIN for l in labs):
            reason = "UNCERTAIN_vs_BINARY"
        elif gran:
            reason = "GRAN_BORDERLINE"
        elif r.D_subst_only is True:
            reason = "SUBST_ONLY"
        elif any("COMPOUND" in a or "TIMEOUT" in a for a in acs):
            reason = "COMPOUND_TIMEOUT"
        elif any(l == "UNPARSEABLE" for l in labs):
            reason = "UNPARSEABLE_DISAGREE"
        elif "⊕" in fol_all or "xor" in fol_all.lower():
            reason = "XOR_PRECEDENCE"
        else:
            reason = "OTHER"
        drows.append({"item_id": k, "system": r.system, "lab_A": r.lab_A, "lab_C": r.lab_C, "lab_D": r.lab_D,
                      "E_final_label": r.E_final_label, "reason": reason, "gran_tag": gran,
                      "auto_class_A": r.auto_class_A, "auto_class_C": r.auto_class_C, "auto_class_D": r.auto_class_D,
                      "text": r.text[:200], "candidate_fol": r.candidate_fol[:200]})
    ddf = pd.DataFrame(drows)
    out_tab(ddf, "label_disagreements.csv", "exp A screen_items.json labels, exp C analysis_table.jsonl, exp D per_item_scores.jsonl; common track-L ids")
    res["disagreements"] = {"n": len(ddf), "by_reason": ddf.reason.value_counts().to_dict() if len(ddf) else {},
                            "n_gran_tagged": int(ddf.gran_tag.sum()) if len(ddf) else 0,
                            "n_UNCERTAIN_GRAN_in_C": int((ddf.lab_C == "UNCERTAIN_GRAN").sum()) if len(ddf) else 0,
                            "reviewer_16_GRAN_items": None}
    n16 = triples.get(("UNCERTAIN", "UNCERTAIN_GRAN", "CORRECT"), 0)
    res["disagreements"]["reviewer_16_GRAN_items"] = (
        f"CONFIRMED: {n16} common items have labels (A=UNCERTAIN, C=UNCERTAIN_GRAN, D=CORRECT); they fall under "
        f"UNCERTAIN_vs_BINARY in the cascade (first rule) and all carry the GRAN tag" if n16 == 16 else f"REFUTED/DIFFERENT: {n16}")
    # track-H analogue
    H = df[df.track == "H"]
    Hc = H[H.in_A & H.in_C & H.in_D]
    res["trackH"] = {"n_common_ACD": len(Hc), "triples": {f"{a}|{c}|{d}": int(v) for (a, c, d), v in Counter(zip(Hc.lab_A, Hc.lab_C, Hc.lab_D)).most_common(12)},
                     "n_consistent_binary": int(((Hc.lab_A == Hc.lab_C) & (Hc.lab_C == Hc.lab_D) & Hc.lab_A.isin(BIN)).sum())}
    # E vs own transitions (binary own labels, E any label)
    trans = {}
    for exp, col, inc in [("A", "lab_A", "in_A"), ("C", "lab_C", "in_C"), ("D", "lab_D", "in_D")]:
        sub = L[L[inc] & L.in_E & L[col].isin(BIN)]
        trans[exp] = {f"{a}->{b}": int(v) for (a, b), v in Counter(zip(sub[col], sub.E_final_label)).most_common()}
    res["E_vs_own_transitions"] = trans
    res["E_vs_own_expected"] = "D: CORRECT->ERROR 58, ERROR->CORRECT 1; C: 62 / 1"
    for exp, col in [("A", "lab_A"), ("C", "lab_C"), ("D", "lab_D")]:
        rows.append({"experiment": exp, "track": "L", "n": trans[exp].get("CORRECT->ERROR", 0),
                     "label_counts": f"CORRECT->ERROR under E (ERROR->CORRECT: {trans[exp].get('ERROR->CORRECT', 0)})"})
    for k, v in res["sets"].items():
        rows.append({"experiment": "SET", "track": "L", "n": v if isinstance(v, int) else None, "label_counts": k if isinstance(v, int) else f"{k}: {v}"})
    out_tab(pd.DataFrame(rows), "bookkeeping.csv", "exp A/C/D per-item files + dataset E screen_adjudicated_labels.json")
    logger.info(f"step1: common={len(common)} consistent={len(cons)} (+judge {len(cons_j)}, err {res['sets']['n_err_consistent_with_judge']}, sents {res['sets']['n_sentences_consistent_with_judge']}); disagreements={res['disagreements']['by_reason']}")
    logger.info(f"step1: transitions {trans}")
    return res


# ================================================================================================= STEP 2
def _boot_delta(y, s1, s2, clusters, B=2000, seed=0):
    cb = su.ClusterBoot(list(clusters), B=B, seed=seed)
    W = cb.item_W()
    a1, a2 = su.boot_auc_w(y, s1, W), su.boot_auc_w(y, s2, W)
    return a1, a2, a1 - a2


def _reviewer_rng_boot(y, S: dict, ref: str, order: list[str], sent: list[str]) -> dict:
    """Exact replication of the reviewer's paired_boot.py resampling: ONE random.Random(0) stream consumed first by
    c_score's 2000 resamples and then by fused_H's (cluster = text.strip().lower())."""
    us = sorted(set(sent))
    idx = {s: [i for i, t in enumerate(sent) if t == s] for s in us}
    rng = random.Random(0)
    out = {}
    for m in order:
        d = []
        for _ in range(2000):
            ii = [i for s in rng.choices(us, k=len(us)) for i in idx[s]]
            yy = y[ii]
            if yy.all() or (~yy.astype(bool)).all():
                continue
            d.append(roc_auc_score(yy, S[m][ii]) - roc_auc_score(yy, S[ref][ii]))
        d = np.array(d)
        out[m] = (float(np.mean(d)), [float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))])
    return out


def step2_rederive(df: pd.DataFrame, out_tab) -> dict:
    L = df[df.track == "L"]
    rows = []
    rev_pb = json.loads((AUDIT / "paired_boot.json").read_text())
    rev_ra = json.loads((AUDIT / "rescore_adjudicated.json").read_text())
    rev_ja = json.loads((AUDIT / "join_audit.json").read_text())

    def add(src, q, rep, rec, tol):
        diff = None if (rep is None or rec is None) else abs(rep - rec)
        rows.append({"source": src, "quantity": q, "reported": rep, "recomputed": None if rec is None else round(rec, 4),
                     "abs_diff": None if diff is None else round(diff, 4), "tolerance": tol,
                     "status": "MATCH" if (diff is not None and diff <= tol + 1e-9) else "MISMATCH"})

    # --- paired_boot.json (n=389)
    ks = L[L.in_A & L.in_C & L.in_D & (L.lab_A == L.lab_C) & (L.lab_C == L.lab_D) & L.lab_A.isin(BIN) & L[REF].notna()]
    y = (ks.lab_A == "ERROR").astype(int).values
    add("paired_boot.json", "n", rev_pb["n"], len(ks), 0)
    add("paired_boot.json", "n_err", rev_pb["n_err"], int(y.sum()), 0)
    add("paired_boot.json", "n_sent (text.strip().lower())", rev_pb["n_sent"], ks.text.str.strip().str.lower().nunique(), 0)
    S = {"c_score": ks.c_score.values, "fused_H": ks.p_fused_H.values, "judge_disg": ks[REF].values, "sc5_cheap": ks.sc5_cheap.values}
    for m, v in S.items():
        add("paired_boot.json", f"auroc {m}", rev_pb["auroc"][m], su.auroc(y, v), 0.002)
    rep_rng = _reviewer_rng_boot(y, S, "judge_disg", ["c_score", "fused_H"], list(ks.text.str.strip().str.lower()))
    for m in ("c_score", "fused_H"):
        a1, a2, d = _boot_delta(y, S[m], S["judge_disg"], ks.cluster.values)
        rep = rev_pb[f"{m}_minus_judge_disg"]
        ci = su.ci95(d)
        add("paired_boot.json", f"{m}-judge delta (own bootstrap mean, D-norm clusters)", rep["delta"], float(np.nanmean(d)), 0.01)
        add("paired_boot.json", f"{m}-judge CI lo (own bootstrap)", rep["ci95"][0], ci[0], 0.01)
        add("paired_boot.json", f"{m}-judge CI hi (own bootstrap)", rep["ci95"][1], ci[1], 0.01)
        mean_r, ci_r = rep_rng[m]
        add("paired_boot.json", f"{m}-judge delta (reviewer RNG replica)", rep["delta"], mean_r, 0.0005)
        add("paired_boot.json", f"{m}-judge CI lo (reviewer RNG replica)", rep["ci95"][0], ci_r[0], 0.0005)
        add("paired_boot.json", f"{m}-judge CI hi (reviewer RNG replica)", rep["ci95"][1], ci_r[1], 0.0005)
    # --- rescore_adjudicated.json
    rmet = {"fused_H": "p_fused_H", "l3": "l3_score", "l2_bow": "bow_uncarried", "c_score": "c_score", "sc5_cheap": "sc5_cheap",
            "judge_cheap_disg": REF, "rt_nli_min": "rt_nli_min", "pilot_rerun_jacc": "pilot_rerun_jacc"}
    for view, tiers in [("adj_all_tiers", None), ("adj_tierAB", {"A", "B"})]:
        sub = L[L.in_E & L.E_final_label.isin(BIN) & (L.E_reading_choice != True)]  # noqa: E712
        if tiers:
            sub = sub[sub.E_label_tier.isin(tiers)]
        add("rescore_adjudicated.json", f"{view} n_items", rev_ra[view]["n_items"], len(sub), 0)
        com = sub.dropna(subset=list(rmet.values()))
        yy = (com.E_final_label == "ERROR").astype(int).values
        add("rescore_adjudicated.json", f"{view} n_common", rev_ra[view]["n_common"], len(com), 0)
        add("rescore_adjudicated.json", f"{view} n_common_err", rev_ra[view]["n_common_err"], int(yy.sum()), 0)
        for nm, col in rmet.items():
            add("rescore_adjudicated.json", f"{view} auroc {nm}", rev_ra[view]["auroc_common"][nm], su.auroc(yy, com[col].values), 0.002)
    # --- join_audit own-label recomputes
    c = L[L.in_C & L.lab_C.isin(BIN) & L.c_score.notna()]
    add("join_audit.json", "c_score own n", 546, len(c), 0)
    add("join_audit.json", "c_score own auroc", 0.8655, su.auroc((c.lab_C == "ERROR").astype(int).values, c.c_score.values), 0.002)
    a = L[L.in_A & L.lab_A.isin(BIN)]
    add("join_audit.json", "fused own n", 477, len(a), 0)
    add("join_audit.json", "fused own auroc", 0.7589, su.auroc((a.lab_A == "ERROR").astype(int).values, a.p_fused_H.values), 0.002)
    d = L[L.in_D & L.lab_D.isin(BIN)]
    dj = d[d[REF].notna()]
    add("join_audit.json", "judge_disg own n (non-missing)", 513, len(dj), 0)
    add("join_audit.json", "judge_disg own auroc excl JSON fails", 0.7846, su.auroc((dj.lab_D == "ERROR").astype(int).values, dj[REF].values), 0.002)
    mx = np.nanmax(df[REF].values)
    s_fill = d[REF].fillna(mx).values
    add("exp D analysis.json", "judge_disg L_primary auroc with FAIL->max (as shipped)", 0.7774622892635317,
        su.auroc((d.lab_D == "ERROR").astype(int).values, s_fill), 0.002)
    # join_audit common consistent (n=398)
    cc = L[L.in_A & L.in_C & L.in_D & (L.lab_A == L.lab_C) & (L.lab_C == L.lab_D) & L.lab_A.isin(BIN)]
    add("join_audit.json", "n_common_consistent_binary", rev_ja["n_common_consistent_binary"], len(cc), 0)
    ja_map = {"fused_H": "p_fused_H", "l2_bow": "bow_uncarried", "l3": "l3_score", "c_score": "c_score", "sc5_cheap": "sc5_cheap",
              "judge_cheap_disg": REF, "judge_cheap_orig": "judge_cheap_orig", "rt_nli_min": "rt_nli_min"}
    for nm, col in ja_map.items():
        sub = cc[cc[col].notna()]
        add("join_audit.json", f"common-consistent auroc {nm} (n={len(sub)})", rev_ja["auroc_on_common_consistent"][nm]["auroc"],
            su.auroc((sub.lab_A == "ERROR").astype(int).values, sub[col].values), 0.002)
    tab = pd.DataFrame(rows)
    out_tab(tab, "rederivation.csv", "reviewer audit JSONs (iter_1/review_report/review_report/audit) vs independent recompute from per-item files")
    mism = tab[tab.status == "MISMATCH"]
    diag = []
    for _, r in mism.iterrows():
        if "own bootstrap" in r.quantity:
            diag.append(f"{r.quantity}: own ClusterBoot (numpy default_rng(0), D norm() clusters) differs from the reviewer's random.Random(0) "
                        f"draws by {r.abs_diff}; the reviewer-RNG replica row reproduces the reported value exactly, so the gap is Monte-Carlo "
                        f"resampling noise, not an id-set/orientation error.")
        else:
            diag.append(f"{r.quantity}: reported {r.reported} vs recomputed {r.recomputed} -- investigate")
    res = {"n_checks": len(tab), "n_match": int((tab.status == "MATCH").sum()), "n_mismatch": len(mism),
           "mismatch_diagnoses": diag, "orientation_selftest_pass": bool(all(tab[tab.quantity.str.contains("auroc")].recomputed.dropna() > 0.5)),
           "gate_passed": bool(all(("own bootstrap" in q) for q in mism.quantity)) if len(mism) else True}
    logger.info(f"step2: {res['n_match']}/{res['n_checks']} MATCH; mismatches: {list(mism.quantity)}")
    return res


# ================================================================================================= STEP 3
def step3_regimes(df: pd.DataFrame) -> dict:
    """Declare every label regime (item set + binary label) BEFORE any AUROC beyond step 2."""
    L = df[df.track == "L"]
    H = df[df.track == "H"]
    # exp D chose its judge rubric on 60 track-H items (prompt_dev.dev_slice_ids) and excluded them from every H headline
    dev = set(json.loads((EXP_D / "results/analysis.json").read_text())["prompt_dev"]["dev_slice_ids"])
    H = H[~H.index.isin(list(dev))]
    R = {}
    cons = L[L.in_A & L.in_C & L.in_D & (L.lab_A == L.lab_C) & (L.lab_C == L.lab_D) & L.lab_A.isin(BIN)]
    R["R_SOLVER_CONS"] = {"track": "L", "y": (cons.lab_A == "ERROR").astype(int), "desc": "A=C=D label-consistent CORRECT/ERROR (solver labels)"}
    for exp, col, inc in [("A", "lab_A", "in_A"), ("C", "lab_C", "in_C"), ("D", "lab_D", "in_D")]:
        s = L[L[inc] & L[col].isin(BIN)]
        R[f"R_SOLVER_OWN_{exp}"] = {"track": "L", "y": (s[col] == "ERROR").astype(int), "desc": f"exp {exp}'s own solver labels (sensitivity)"}
    e = L[L.in_E & (L.E_reading_choice != True)]  # noqa: E712
    ab = e[e.E_label_tier.isin(["A", "B"])]
    s = ab[ab.E_final_label.isin(BIN)]
    R["R_ADJ_AB"] = {"track": "L", "y": (s.E_final_label == "ERROR").astype(int), "desc": "E final CORRECT/ERROR, tier A or B, not reading_choice (screen analogue of R_AB)"}
    s = e[e.E_label_tier.isin(["A"]) & e.E_final_label.isin(BIN)]
    R["R_ADJ_A"] = {"track": "L", "y": (s.E_final_label == "ERROR").astype(int), "desc": "E tier A only (solver vs audited reference; screen analogue of R_A)"}
    s = e[e.E_label_tier.isin(["A", "B", "auto_only"]) & e.E_final_label.isin(BIN)]
    R["R_ADJ_ALL"] = {"track": "L", "y": (s.E_final_label == "ERROR").astype(int), "desc": "E all decided tiers incl. auto_only"}
    s = ab[ab.E_final_label.isin(BIN + ("CONTESTED",))]
    R["R_ADJ_AB_CONT_C"] = {"track": "L", "y": (s.E_final_label == "ERROR").astype(int), "desc": "R_ADJ_AB with CONTESTED counted CORRECT"}
    R["R_ADJ_AB_CONT_E"] = {"track": "L", "y": s.E_final_label.isin(["ERROR", "CONTESTED"]).astype(int), "desc": "R_ADJ_AB with CONTESTED counted ERROR"}
    un = L[L.in_A & L.in_C & L.in_D & (L.lab_A == "UNPARSEABLE") & (L.lab_C == "UNPARSEABLE") & (L.lab_D == "UNPARSEABLE")]
    yu = pd.concat([(cons.lab_A == "ERROR").astype(int), pd.Series(1, index=un.index)])
    R["L_UNPARSEABLE_AS_ERROR"] = {"track": "L", "y": yu, "unparse_ids": set(un.index),
                                   "desc": "R_SOLVER_CONS + items all three experiments call UNPARSEABLE, as ERROR; metrics that cannot score them get the regime max"}
    s = H[H.in_D & H.lab_D.isin(BIN)]
    R["H_SOLVER"] = {"track": "H", "y": (s.lab_D == "ERROR").astype(int), "desc": "track H, exp D solver labels"}
    s = H[H.in_E & H.E_label_tier.isin(["A", "B"]) & H.E_final_label.isin(BIN) & (H.E_reading_choice != True)]  # noqa: E712
    R["H_ADJ_AB"] = {"track": "H", "y": (s.E_final_label == "ERROR").astype(int), "desc": "track H, E tiers A/B"}
    s = H[H.in_D & H.lab_D_hcur.isin(BIN)]
    R["H_CURATOR"] = {"track": "H", "y": (s.lab_D_hcur == "ERROR").astype(int), "desc": "track H, D's H_curator_view (curated original->corrected pair is the ground truth)"}
    return R


def common_set(df: pd.DataFrame, reg: dict, metrics: list[str]) -> tuple[pd.DataFrame, np.ndarray, list[str], list[str]]:
    """Rows of the regime where ALL headline metrics are non-null (unparseable rows of L_UNPARSEABLE_AS_ERROR get the
    regime max for metrics that cannot score them). Metrics with <50% coverage on the regime are dropped (H only)."""
    ids = reg["y"].index
    sub = df.loc[ids].copy()
    dropped = []
    if reg["track"] == "H":
        keep = []
        for m in metrics:
            cov = sub[m].notna().mean()
            (keep if cov >= 0.5 else dropped).append(m)
        metrics = keep
    un = reg.get("unparse_ids", set())
    if un:
        mask_un = sub.index.isin(list(un))
        for m in metrics:
            mx = np.nanmax(sub[m].values)
            sub.loc[mask_un, m] = sub.loc[mask_un, m].fillna(mx)
        for fl in ("fused_flag", "bow_flag", "l3_flag", "flag_medoid"):
            sub.loc[mask_un, fl] = sub.loc[mask_un, fl].fillna(1.0)
    ok = sub[metrics].notna().all(axis=1)
    sub = sub[ok]
    y = reg["y"].loc[sub.index].values.astype(int)
    return sub, y, metrics, dropped


def testability(sub: pd.DataFrame, y: np.ndarray) -> dict:
    ne, nc = int(y.sum()), int((1 - y).sum())
    se, sc = sub.cluster[y == 1].nunique(), sub.cluster[y == 0].nunique()
    return {"n": len(y), "n_err": ne, "n_correct": nc, "sent_err": int(se), "sent_correct": int(sc), "n_sentences": int(sub.cluster.nunique()),
            "testable": bool(ne >= 50 and nc >= 50 and se >= 25 and sc >= 25)}


# ================================================================================================= STEP 4
SHIPPED_FLAG = {"p_fused_H": "fused_flag", "bow_uncarried": "bow_flag", "l3_score": "l3_flag", "c_score": "flag_medoid"}


def eval_table(sub: pd.DataFrame, y: np.ndarray, metrics: list[str], d_thr: dict, holm_family=HOLM_FAMILY, B=2000) -> tuple[pd.DataFrame, dict]:
    cb = su.ClusterBoot(list(sub.cluster.values), B=B)
    W = cb.item_W()
    clusters = sub.cluster.values
    boots = {m: su.boot_auc_w(y, sub[m].values.astype(float), W) for m in metrics}
    n_skipped = int(np.isnan(boots[metrics[0]]).sum())
    rows = []
    ref = boots.get(REF)
    for m in metrics:
        s = sub[m].values.astype(float)
        r = {"metric": nice(m), "col": m, "n": len(y), "n_err": int(y.sum()), "n_correct": int((1 - y).sum()),
             "n_sentences": int(sub.cluster.nunique()), "auroc": su.auroc(y, s)}
        ci = su.ci95(boots[m])
        r["auroc_ci_lo"], r["auroc_ci_hi"] = ci
        r["auprc"] = su.auprc(y, s)
        r["prevalence"] = float(y.mean())
        r["tie_frac"] = su.tie_fraction(y, s)
        flag = None
        if m in SHIPPED_FLAG and sub[SHIPPED_FLAG[m]].notna().all():
            flag = sub[SHIPPED_FLAG[m]].values > 0.5
            r["threshold_source"] = SHIPPED_FLAG[m]
        elif m in d_thr:
            flag = s > d_thr[m]
            r["threshold_source"] = f"exp D threshold {d_thr[m]:.4g}"
        if flag is not None:
            st = su.at_flag(y, flag)
            r.update({"thr_precision": st["precision"], "thr_recall": st["recall"], "thr_fa": st["fa"],
                      "thr_prec_at_prev10": st["prec_at_prev10"], "thr_prec_at_prev25": st["prec_at_prev25"]})
        if ref is not None and m != REF:
            d = boots[m] - ref
            dci = su.ci95(d)
            r["delta_vs_judge"] = r["auroc"] - su.auroc(y, sub[REF].values.astype(float))
            r["delta_boot_mean"] = float(np.nanmean(d))
            r["delta_ci_lo"], r["delta_ci_hi"] = dci
            r["delta_p_boot"] = su.boot_p_two_sided(d)
            dl = su.delong_paired(y, s, sub[REF].values.astype(float))
            r["delong_p"] = dl["p"]
            try:
                r["delong_clustered_p"] = su.delong_clustered_paired(y, s, sub[REF].values.astype(float), clusters)["p"]
            except (ZeroDivisionError, ValueError) as ex:
                logger.warning(f"clustered DeLong failed for {m}: {ex}")
                r["delong_clustered_p"] = None
        rows.append(r)
    tab = pd.DataFrame(rows)
    fam = {m: tab.set_index("col").loc[m, "delta_p_boot"] for m in holm_family if m in tab.col.values}
    hb = su.holm(fam)
    famd = {m: tab.set_index("col").loc[m, "delong_p"] for m in holm_family if m in tab.col.values}
    hd = su.holm(famd)
    tab["holm_p_boot"] = tab.col.map(hb)
    tab["holm_p_delong"] = tab.col.map(hd)
    return tab, {"boots": boots, "n_skipped_single_class": n_skipped, "cb": cb}


def rule_verdict(tab: pd.DataFrame, cand: str, shipped: dict, testable: bool) -> dict:
    r = tab.set_index("col").loc[cand]
    sh = shipped[cand]
    clauses = {"AUROC>=0.65": bool(r.auroc >= 0.65), "coverage>=0.90": bool(sh["coverage"] >= 0.90),
               "cost<=0.002/item": bool(sh["cost"] <= 0.002), "max_rewrite_FA<=0.10": bool(sh["max_rewrite_fa"] <= 0.10),
               "delta_vs_judge_disg_CI>0": bool(r.delta_ci_lo is not None and r.delta_ci_lo > 0)}
    passA = all(clauses.values())
    passS = passA and bool(r.delta_vs_judge >= 0.03)
    return {"clauses": clauses, "shipped_values": sh, "delta": float(r.delta_vs_judge), "delta_ci": [r.delta_ci_lo, r.delta_ci_hi],
            "verdict_expA_prereg_plus_delta": "PASS" if passA else "FAIL",
            "verdict_strategy_with_tie_margin_0.03": "PASS" if passS else "FAIL",
            "testable": testable, "failing_clauses": [k for k, v in clauses.items() if not v],
            "delta_clause_sign_only": None if testable else ("+" if r.delta_vs_judge > 0 else "-")}


# ================================================================================================= STEP 5
def step5_regime_shift(df, regimes, commons, metrics_by_regime, out_tab, B_tau=500) -> dict:
    Lreg = [k for k, v in regimes.items() if v["track"] == "L"]
    all_m = [m for m in HEADLINE_L]
    # matrix of common-set AUROCs
    mat = {}
    for rn in regimes:
        sub, y = commons[rn]
        mat[rn] = {m: su.auroc(y, sub[m].values.astype(float))
                   if m in sub.columns and (m in metrics_by_regime[rn] or m in ("PT_oof", "PTJ_oof")) and sub[m].notna().all() and len(np.unique(y)) > 1
                   else np.nan for m in all_m + ["PT_oof", "PTJ_oof"]}
    M = pd.DataFrame(mat)
    M.index.name = "metric"
    out_tab(M.reset_index().assign(metric=lambda x: x.metric.map(nice)), "regime_auroc_matrix.csv", "common-set AUROC per regime (steps 3-4)")
    # shifts: full + label-only for L regime pairs
    rows = []
    base_pairs = [(a, b) for a, b in itertools.permutations(Lreg, 2)]
    ci_pairs = set([("R_SOLVER_CONS", b) for b in Lreg if b != "R_SOLVER_CONS"] + [("R_ADJ_AB", "R_ADJ_A"), ("R_ADJ_AB", "R_ADJ_ALL"),
                    ("R_SOLVER_OWN_D", "R_ADJ_AB"), ("R_SOLVER_OWN_C", "R_ADJ_AB"), ("R_SOLVER_OWN_A", "R_ADJ_AB"), ("R_ADJ_AB_CONT_C", "R_ADJ_AB_CONT_E")])
    for r1, r2 in base_pairs:
        if (r1, r2) not in ci_pairs:
            continue
        s1, y1 = commons[r1]
        s2, y2 = commons[r2]
        shared = s1.index.intersection(s2.index)
        if len(shared) < 20:
            continue
        ya = regimes[r1]["y"].loc[shared].values.astype(int)
        yb = regimes[r2]["y"].loc[shared].values.astype(int)
        sub = df.loc[shared]
        cb = su.ClusterBoot(list(sub.cluster.values), B=2000)
        W = cb.item_W()
        for m in all_m:
            if m not in metrics_by_regime[r1] or m not in metrics_by_regime[r2]:
                continue
            s = sub[m].values.astype(float)
            if np.isnan(s).any():
                continue
            full = M.loc[m, r2] - M.loc[m, r1]
            lo = su.auroc(yb, s) - su.auroc(ya, s)
            d = su.boot_auc_w(yb, s, W) - su.boot_auc_w(ya, s, W)
            ci = su.ci95(d)
            direction = "UP" if ci[0] is not None and ci[0] > 0 else ("DOWN" if ci[1] is not None and ci[1] < 0 else "INSIDE_CI")
            rows.append({"metric": nice(m), "from": r1, "to": r2, "n_shared": len(shared), "n_label_changes": int((ya != yb).sum()),
                         "full_shift": full, "label_only_shift": lo, "label_only_ci_lo": ci[0], "label_only_ci_hi": ci[1], "direction": direction})
    SH = pd.DataFrame(rows)
    out_tab(SH, "regime_shift.csv", "label-only shift on items shared by both regimes' common sets; same bootstrap indices for both labelings")
    # Kendall tau-b between metric rankings across L regimes with sentence-bootstrap CI (500)
    Lm = [m for m in all_m if all(m in metrics_by_regime[r] for r in Lreg)]
    allL = df[df.track == "L"]
    gcb = su.ClusterBoot(list(allL.cluster.values), B=B_tau, seed=0)
    pos = {k: i for i, k in enumerate(allL.index)}
    bootA = {}
    for rn in Lreg:
        sub, y = commons[rn]
        Wi = gcb.W[:, gcb.cid[[pos[k] for k in sub.index]]]
        bootA[rn] = np.vstack([su.boot_auc_w(y, sub[m].values.astype(float), Wi) for m in Lm])  # metrics x B
    taus = []
    for r1, r2 in itertools.combinations(Lreg, 2):
        t = sps.kendalltau(M.loc[Lm, r1].values, M.loc[Lm, r2].values).correlation
        tb = [sps.kendalltau(bootA[r1][:, b], bootA[r2][:, b]).correlation for b in range(B_tau)]
        ci = su.ci95(np.array(tb))
        taus.append({"regime_1": r1, "regime_2": r2, "kendall_tau_b": t, "ci_lo": ci[0], "ci_hi": ci[1], "n_metrics": len(Lm)})
    TT = pd.DataFrame(taus)
    out_tab(TT, "rank_kendall_tau.csv", "Kendall tau-b of headline-metric AUROC rankings between regimes; 500 sentence resamples (global)")
    return {"matrix": M, "shift": SH, "tau": TT, "tau_metrics": [nice(m) for m in Lm]}


def flipped_diagnostic(df, commons, regimes, metrics, out_tab) -> dict:
    """Items whose solver label is CORRECT but whose adjudicated label is ERROR (and the reverse)."""
    L = df[df.track == "L"]
    res = {}
    rows = []
    ref_ok = L[(L.lab_D == "CORRECT") & (L.E_final_label == "CORRECT")]
    for defn, col in [("D_solver", "lab_D"), ("C_solver", "lab_C"), ("consensus_solver", None)]:
        if col is None:
            base = L[(L.lab_A == L.lab_C) & (L.lab_C == L.lab_D)]
            col = "lab_A"
        else:
            base = L
        fl = base[(base[col] == "CORRECT") & (base.E_final_label == "ERROR")]
        rv = base[(base[col] == "ERROR") & (base.E_final_label == "CORRECT")]
        agree_err = base[(base[col] == "ERROR") & (base.E_final_label == "ERROR")]
        res[defn] = {"n_correct_to_error": len(fl), "n_error_to_correct": len(rv)}
        for m in metrics:
            allv = L[m].dropna()
            if len(allv) < 50:
                continue
            pr = allv.rank(pct=True)
            thr_items = ref_ok[m].dropna()
            if len(thr_items) < 20:
                continue
            rule = su.matched_fa_rule(thr_items.values.astype(float), 0.20)
            for grp_name, grp in [("CORRECT->ERROR", fl), ("ERROR->CORRECT", rv), ("agree_ERROR", agree_err), ("agree_CORRECT(ref)", ref_ok)]:
                g = grp[grp[m].notna()]
                if len(g) == 0:
                    continue
                rows.append({"definition": defn, "group": grp_name, "metric": nice(m), "n": len(g),
                             "mean_pct_rank": float(pr.loc[g.index].mean()),
                             "share_flagged_FA0.20": float(su.flag_prob(g[m].values.astype(float), rule).mean())})
            # breakdowns for the main flipped set
            for bname, bcol in [("E_auto_label", "E_auto_label"), ("addrop_only_suspect", "E_addrop_only_suspect")]:
                g = fl[fl[m].notna()]
                for val, gg in g.groupby(g[bcol].astype(str)):
                    rows.append({"definition": defn, "group": f"CORRECT->ERROR|{bname}={val}", "metric": nice(m), "n": len(gg),
                                 "mean_pct_rank": float(pr.loc[gg.index].mean()),
                                 "share_flagged_FA0.20": float(su.flag_prob(gg[m].values.astype(float), rule).mean())})
    T = pd.DataFrame(rows)
    out_tab(T, "flipped_items.csv", "solver CORRECT -> adjudicated ERROR items; percentile rank among all track-L items; matched FA 0.20 on doubly-CORRECT items")
    main = T[(T.definition == "D_solver") & (T.group == "CORRECT->ERROR")].set_index("metric")
    if len(main):
        res["D_solver_flipped_mean_pct_rank"] = main.mean_pct_rank.to_dict()
        res["D_solver_flipped_share_flagged_FA020"] = main["share_flagged_FA0.20"].to_dict()
        bow, cs = main.loc["L2_bow", "share_flagged_FA0.20"] if "L2_bow" in main.index else None, main.loc["c_score", "share_flagged_FA0.20"] if "c_score" in main.index else None
        res["prediction_bow_high_cscore_low"] = {"L2_bow_share_flagged": bow, "c_score_share_flagged": cs,
                                                 "supported": bool(bow is not None and cs is not None and bow > cs)}
    return res
