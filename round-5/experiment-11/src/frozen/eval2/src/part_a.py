"""PART A driver (mechanism): gates, prereg, matrix readouts, G2, pairwise_classes_E.jsonl, VOCAB_EXACT, the e/d
decomposition cuts, graded trace, M1/M2/NET/SCATTER/M3-local and M4. Writes results/part_a.json + tables/*.csv."""
from __future__ import annotations

import hashlib
import json
import re
import sys
import time
from collections import Counter

import numpy as np
import pandas as pd
from loguru import logger

from paths import DS_E, E5, E6, I1, ROOT, jl, sha256_file

sys.path.insert(0, str(ROOT / "vendor_exp5"))
sys.path.insert(0, str(ROOT / "vendor_exp5" / "vendor_c"))

import consensus_mx as CS  # noqa: E402
import m4 as M4  # noqa: E402
import mechanism as MC  # noqa: E402
from frame import build_frame, gates_G0_G1, regime  # noqa: E402
from stats import SentBoot, auc, ci, strat_auc  # noqa: E402

TAB = ROOT / "tables"
RES = ROOT / "results"


def jdump(p, o):
    p.write_text(json.dumps(o, indent=1, default=lambda x: x.item() if hasattr(x, "item") else str(x)))


def write_csv(df: pd.DataFrame, name: str, sources: list[str]):
    p = TAB / name
    with p.open("w") as fh:
        for s in sources:
            fh.write(f"# source: {s}\n")
        df.to_csv(fh, index=False)


# =================================================================================================== prereg
def write_prereg(cut: dict) -> dict:
    pre = {
        "title": "Consensus mechanism audit (T4 on dataset E) - pre-registration of every analysis choice",
        "note": ("Written after the LABEL-FREE pairwise matrix was computed and before any label-joined analysis. Dataset E labels "
                 "were already seen by earlier iterations: this prereg guards against analysis-choice drift, NOT against label peeking."),
        "seed": 0, "B": 2000, "bootstrap": "sentence-cluster, numpy default_rng(0), sentence_ids resampled with replacement",
        "population": "R_AB rows (analyse_E.regime) that are parseable with |P_c|>=2 (consensus-scorable)",
        "endorsement_rules": {
            "END_MAJ (PRIMARY)": "endorsed iff n_eq > |P_c|/2 <=> FROZEN c_score_align < 0.5; exact tie at half NOT endorsed",
            "END_PLUR": "endorsed iff candidate eqmv-equivalent to a node of the UNIQUE largest peer class (components of the True graph "
                        "induced on P_c's nodes, size in peer rows); ties -> not endorsed",
            "END_FAM2": ">=2 distinct other vendor families have >=1 row equivalent to the candidate",
            "END_FAMMAJ": "each other family votes once (any equivalent row); endorsed iff > half of available families endorse",
            "END_MAJ_EXACT (diagnostic)": "END_MAJ counting only reason=='exact' (or identical string) endorsements (aligner-free)"},
        "unknown": "UNKNOWN (None) = not equivalent", "binary_score": "b = 1 - endorsed (1 = predicted error)",
        "identity": "AUROC_b = 1 - (e+d)/2 asserted to 1e-12; e = P(endorsed|ERROR), d = P(not endorsed|CORRECT)",
        "stratified": "sum_s w_s (1-(e_s+d_s)/2), w_s = n_err,s * n_cor,s",
        "cuts": cut, "min_cell": {"rows_of_relevant_class": 30, "sentences": 10, "else": "descriptive, no CI"},
        "vocab_exact": {"trusted_reference_status": ["GOLD_PANEL_OK", "PANEL_REPAIRED", "TRUSTED_AGREED"],
                        "normalise": "re.sub(r'[^a-z0-9]', '', name.lower())",
                        "match": "Counter of normalised (predicate name, arity) over distinct predicate keys AND set of normalised constants equal to the reference's",
                        "y_exact": "1 iff NOT pure-z3 equivalent (common._eq, fingerprint prefilter + z3, ms=3000, no align) to the reference; UNKNOWN excluded",
                        "testable_iff": ">=50 ERROR and >=50 CORRECT"},
        "gee": {"family": "Binomial(logit)", "cov_struct": "Exchangeable (fallback Independence, logged)", "groups": "sentence_id",
                "se": "robust sandwich", "predictors": "z-scored on the analysis population"},
        "M1": {"model": "endorsed(END_MAJ) ~ z(n_conditions) + z(words) + C(source_stratum) among R_AB ERROR rows",
               "confirm": "n_conditions coef < 0 with 95% CI excluding 0", "refute": "coef > 0 with CI excluding 0",
               "rival": "N-version programming (Eckhardt-Lee 1985; Knight-Leveson 1986): coincident failures concentrate on difficult inputs -> positive slope",
               "sensitivities": ["END_FAM2", "END_FAMMAJ", "END_PLUR", "END_MAJ_EXACT", "long pool only", "+C(vendor family)", "R_A only", "no stratum dummies"]},
        "M2": {"model": "divergent = 1-endorsed ~ z(words) + z(n_conditions) + C(source_stratum) among R_AB CORRECT rows",
               "confirm": "words coef > 0 with CI excluding 0", "extra": "split by correct_not_equivalent"},
        "NET": {"primary": "Delta(e+d) = (e+d)[words T3] - (e+d)[words T1], cluster bootstrap B=2000",
                "secondary": "AME_e + AME_d per SD of words from plain logistic refits in every replicate",
                "repeat": ["n_conditions 4+ vs 0-1", "long pool only"],
                "interpretation": "CI upper < 0 -> AUROC_b improves with length (scatter dominates); CI lower > 0 -> degrades (legitimate divergence dominates); else balanced/undetermined"},
        "SCATTER": {"unit": "sentence with >=2 labelled LLM rows of the class from >=2 families; CROSS-FAMILY pairs only",
                    "quantities": ["SI_err", "SI_cor", "SI_mix", "joint failure rate", "classes per output"],
                    "prediction": "SI_err low and falling with n_conditions; SI_cor high", "pair_gee": "eq ~ C(pair_type) * z(n_conditions)"},
        "M3_local": "correct_c = 1[b==y] (END_MAJ) ~ z(words) vs local judge thresholded at END_MAJ's flag rate (no frozen judge threshold); SECONDARY",
        "M4": {"family_unit": "prereg family_map_vendor (8 LLM vendor families -> K_max = 7)", "draws": 50,
               "draw_seed": "sha1('M4|'+row_key+'|'+k+'|'+j)", "k95": "smallest k with mean AUROC(k) >= 0.95 AUROC(K_max)",
               "confirm": "k95 <= 5", "fixed_pools": "all C(8,3)=56; cross-fit on exp 6 folds_E (fold_E = sha1('E_folds_v1|'+sid)%5); also k=2,4",
               "lofo_rule": "no single family carries the effect iff every LOFO dAUROC CI lower > -0.03 AND every LOFO AUROC > 0.712",
               "M4_subset_score": "c_k = 1 - eq rows / all pool rows of the chosen families (no |P|>=2 minimum inside subsets)"},
        "deviations": {
            "D1": "eqmv timeout 3000 ms (not the direction's 2 s): exact reproduction of the frozen score requires identical settings",
            "D2": "k = 1..7 (8 vendor families), not 1..9",
            "D3": "G2: 0.33% rows differ from the frozen score; eqmv's align/fingerprint use Python str hash (PYTHONHASHSEED-dependent) and exp 5 workers ran with random hash seeds",
            "D4": "T4 runs on dataset E only (R_COMP has no candidates yet; T2 experiment owns them)",
            "D5": "prereg written after the label-free matrix was computed (before any label join)"}}
    p = ROOT / "prereg_mech.json"
    jdump(p, pre)
    (ROOT / "prereg_mech.sha256").write_text(f"{sha256_file(p)}  prereg_mech.json\n")
    return pre


# =================================================================================================== VOCAB_EXACT
def vocab_exact(df: pd.DataFrame, trusted: list[str]) -> pd.DataFrame:
    import peer_text as PT
    from common import _eq
    import pairwise as PW
    PW.init_worker(6.0)
    out = []
    t0 = time.time()
    for r in df.itertuples():
        rec = {"row_key": r.row_key, "vocab_exact": False, "y_exact": None}
        if r.reference_status in trusted and r.parseable:
            c = PT.parse_fol(r.candidate_fol)
            f = PT.parse_fol(r.reference_fol)
            if c is not None and f is not None:
                def sig(e):
                    return (Counter((MC.normalise_name(n), a) for (n, a) in PT.pred_keys(e)),
                            {MC.normalise_name(x) for x in PT.constants(e)})
                sc, sf = sig(c), sig(f)
                if sc == sf:
                    rec["vocab_exact"] = True
                    res, to = PW._with_alarm(30, _eq, c, f, 3000)
                    rec["y_exact"] = None if (to or res is None) else int(res is not True)
        out.append(rec)
    logger.info(f"VOCAB_EXACT computed in {time.time() - t0:.0f}s")
    return pd.DataFrame(out)


# =================================================================================================== main
def run(stage: str = "all") -> dict:
    A = {}
    df, info = build_frame()
    A["frame_info"] = info
    A["gates"] = gates_G0_G1(df)
    if not (A["gates"]["G0"]["pass"] and A["gates"]["G1"]["pass"]):
        raise SystemExit("G0/G1 failed: fix the join before anything else")
    # ---------------- matrix readouts
    mats = {r["sentence_id"]: r for r in jl(RES / "pair_matrix_E.jsonl")}
    sms = {s: CS.SentenceMatrix(r) for s, r in mats.items()}
    zver = next(iter(mats.values())).get("z3_version")
    csha = next(iter(mats.values())).get("code_sha")
    rc = []
    for r in df.itertuples():
        sm_ = sms.get(r.sentence_id)
        x = CS.row_consensus(sm_, r.row_key) if sm_ else None
        xf = CS.row_consensus(sm_, r.row_key, "family_field") if sm_ else None
        d = {"row_key": r.row_key, "matrix_present": sm_ is not None}
        if x:
            d.update({k: x.get(k) for k in ("npc", "n_eq", "n_eq_exact", "node", "comp", "c_re", "c_exact", "end_maj", "end_plur",
                                             "end_fam2", "end_fammaj", "n_fam_avail", "n_fam_endorse", "plur_top_share")})
            d["fam_stats"] = x["fam_stats"]
            d["fam_stats_ff"] = xf["fam_stats"]
        rc.append(d)
    df = df.merge(pd.DataFrame(rc), on="row_key", how="left")
    # ---------------- G2
    m = df.parseable & df.matrix_present
    both = m & df.c_frozen_raw.notna() & df.c_re.notna()
    mis = both & ((df.c_re - df.c_frozen_raw).abs() > 1e-9)
    none_mis = m & (df.c_frozen_raw.isna() != df.c_re.isna())
    g2 = {"n_compared": int(both.sum()), "n_mismatch": int(mis.sum()), "mismatch_rate": float(mis.sum() / both.sum()),
          "none_iff_npc_lt2_violations": int(none_mis.sum()), "n_unknown_pairs_in_matrix":
          int(sum(p[2] is None for r in mats.values() for p in r["pairs"])),
          "n_mismatch_in_R_AB": int((mis & df.y_AB.notna()).sum()), "accept": bool(mis.sum() / both.sum() <= 0.005),
          "explanation": ("no UNKNOWN pair exists in the recomputed matrix (max pair 4.5 s < 30 s cap); mismatches are deterministic "
                          "fast pairs. eqmv's align()/fp() iterate sets / hash strings, which depend on PYTHONHASHSEED: exp 5's spawn "
                          "workers set PYTHONHASHSEED inside init_worker (after interpreter start, so ineffective) -> per-worker random "
                          "hash seeds. results/diag/hashseed_test.py re-runs the 7 mismatch sentences under 6 seeds: 3/387 pairs flip.")}
    A["G2"] = g2
    df.loc[mis, ["row_key", "sentence_id", "stratum", "c_re", "c_frozen_raw", "y_AB"]].to_csv(TAB / "g2_mismatches.csv", index=False)
    logger.info(f"G2 {g2}")
    # ---------------- pairwise_classes_E.jsonl + non-transitivity
    nt = []
    with (ROOT / "pairwise_classes_E.jsonl").open("w") as fh:
        for sid in sorted(sms):
            line = CS.pairwise_class_line(sms[sid], zver, csha)
            fh.write(json.dumps(line, ensure_ascii=False) + "\n")
            nt.append({"sentence_id": sid, "stratum": line["source_stratum"], "open": line["n_nontransitive_triples"],
                       "wedges": line["n_wedges"], "in_RAB": sid in set(df[df.y_AB.notna()].sentence_id),
                       "n_nodes": len(line["nodes"]), "n_components": len(line["components"]), "n_cliques": len(line["cliques"])})
    NT = pd.DataFrame(nt)
    ntr = {"overall": {"open": int(NT.open.sum()), "wedges": int(NT.wedges.sum()),
                       "rate": float(NT.open.sum() / max(NT.wedges.sum(), 1))}}
    for st, g in NT.groupby("stratum"):
        ntr[st] = {"open": int(g.open.sum()), "wedges": int(g.wedges.sum()), "rate": float(g.open.sum() / max(g.wedges.sum(), 1))}
    ntr["flag_gt_5pct"] = ntr["overall"]["rate"] > 0.05
    ntr["components_vs_cliques"] = {"mean_nodes": float(NT.n_nodes.mean()), "mean_components": float(NT.n_components.mean()),
                                    "mean_cliques": float(NT.n_cliques.mean())}
    A["nontransitivity"] = ntr
    reasons = Counter(p[3] for r in mats.values() for p in r["pairs"])
    A["matrix_summary"] = {"n_sentences": len(mats), "n_pairs": int(sum(len(r["pairs"]) for r in mats.values())),
                           "reason_counts": dict(reasons), "z3_version": zver, "code_sha": csha,
                           "pair_secs_pctl_50_90_99_max": [float(x) for x in np.percentile(
                               [p[4] for r in mats.values() for p in r["pairs"]], [50, 90, 99, 100])],
                           "wall_s_by_stage": {s: json.loads((RES / f"matrix_stage_{s}.json").read_text()) for s in ("mini", "rab", "rest")
                                               if (RES / f"matrix_stage_{s}.json").exists()}}
    # ---------------- prereg (cut points on R_AB sentences)
    rab_all = df[df.y_AB.notna()]
    cut = MC.prereg_cuts(rab_all)
    pre = write_prereg(cut)
    df = MC.make_bins(df, cut)
    # ---------------- VOCAB_EXACT on R_AB rows
    ve = vocab_exact(df[df.y_AB.notna()], pre["vocab_exact"]["trusted_reference_status"])
    df = df.merge(ve, on="row_key", how="left")
    df["vocab_exact"] = df.vocab_exact.fillna(False).astype(bool)
    # ---------------- consensus-scorable R_AB population
    df["in_RAB"] = df.y_AB.notna()
    P = df[df.in_RAB & df.parseable & df.c_frozen_raw.notna()].copy().reset_index(drop=True)
    P["end_MAJ"] = (P.c_frozen_raw < 0.5).astype(int)
    P["end_PLUR"] = P.end_plur.astype(int)
    P["end_FAM2"] = P.end_fam2.astype(int)
    P["end_FAMMAJ"] = P.end_fammaj.astype(int)
    P["end_MAJ_EXACT"] = (P.c_exact < 0.5).astype(int)
    P["c_score_exact"] = P.c_exact.astype(float)
    RULES = {"MAJ": "end_MAJ", "PLUR": "end_PLUR", "FAM2": "end_FAM2", "FAMMAJ": "end_FAMMAJ", "MAJ_EXACT": "end_MAJ_EXACT"}
    A["population"] = {"R_AB_rows": int(df.in_RAB.sum()), "consensus_scorable": len(P),
                       "excluded_unparseable": int((df.in_RAB & ~df.parseable).sum()),
                       "excluded_npc_lt2": int((df.in_RAB & df.parseable & df.c_frozen_raw.isna()).sum()),
                       "scorable_err": int(P.y_AB.sum()), "scorable_cor": int((P.y_AB == 0).sum()),
                       "n_sent": int(P.sentence_id.nunique())}
    boot = SentBoot(P.sentence_id.values, b=2000, seed=0)
    # VOCAB_EXACT testability (declared before AUROCs on it)
    vx = P[P.vocab_exact & P.y_exact.notna()]
    ve_info = {"n_rows_vocab_exact_R_AB": int(P.vocab_exact.sum()), "n_with_y_exact": len(vx),
               "n_err_exact": int((vx.y_exact == 1).sum()), "n_cor_exact": int((vx.y_exact == 0).sum())}
    ve_info["testable"] = ve_info["n_err_exact"] >= 50 and ve_info["n_cor_exact"] >= 50
    if len(vx):
        from sklearn.metrics import cohen_kappa_score
        ve_info["kappa_vs_dataset_label"] = float(cohen_kappa_score(vx.y_AB.astype(int), vx.y_exact.astype(int)))
        ve_info["crosstab"] = {f"label={a}|exact={b}": int(((vx.y_AB == a) & (vx.y_exact == b)).sum()) for a in (0, 1) for b in (0, 1)}
        ve_info["by_tier"] = {t: int((vx.label_tier == t).sum()) for t in ("A", "B")}
    A["vocab_exact"] = ve_info
    P["y_VX"] = P.y_exact
    vx_cor = set(vx[vx.y_exact == 0].row_key)
    ra_cor = set(P[(P.label_tier == "A") & (P.y_AB == 0)].row_key)
    A["vocab_exact"]["overlap"] = {"VX_CORRECT": len(vx_cor), "R_A_CORRECT": len(ra_cor), "intersection": len(vx_cor & ra_cor),
                                   "note": "tier-A CORRECT rows are (almost) all vocabulary-exact: the label side of tier-A CORRECT needs no alignment"}
    # ---------------- cuts
    regimes = {"R_AB": (np.ones(len(P), bool), "y_AB"), "R_A": ((P.label_tier == "A").values, "y_AB"),
               "VOCAB_EXACT": ((P.vocab_exact & P.y_exact.notna()).values, "y_VX")}
    cuts = MC.run_cuts(P, boot, regimes, RULES)
    cuts_out = cuts.copy()
    for c in ("e_ci", "d_ci", "auroc_b_ci", "auroc_c_ci"):
        cuts_out[c + "_lo"] = cuts_out[c].apply(lambda v: v[0])
        cuts_out[c + "_hi"] = cuts_out[c].apply(lambda v: v[1])
        del cuts_out[c]
    write_csv(cuts_out, "ed_decomposition_cuts.csv", [f"{ROOT}/results/pair_matrix_E.jsonl :: eqmv matrix (this artifact)",
                                                      f"{E5}/results/per_item_E.jsonl :: c_score_align (FROZEN)",
                                                      f"{E5}/data/E_labels.jsonl :: final_label, label_tier"])
    A["cuts_headline"] = cuts[(cuts.dim == "ALL")].to_dict("records")
    # VOCAB_EXACT: c_score_align vs c_score_exact side by side (+ the dataset label)
    if len(vx):
        A["vocab_exact"]["auroc"] = {
            "c_score_align_vs_y_exact": auc(vx.y_exact, vx.c_frozen), "c_score_exact_vs_y_exact": auc(vx.y_exact, vx.c_score_exact),
            "c_score_align_vs_dataset_label": auc(vx.y_AB, vx.c_frozen), "c_score_exact_vs_dataset_label": auc(vx.y_AB, vx.c_score_exact)}
    # stratified AUROC_b (within-stratum pairs) per rule, R_AB
    y = P.y_AB.values.astype(int)
    A["stratified"] = {}
    for rule, col in RULES.items():
        s_b = strat_auc(y, 1 - P[col].values, P.stratum.values)
        wsum = 0
        acc = 0
        for st, g in P.groupby("stratum"):
            dd = MC.ed_decomposition(g.y_AB.values.astype(int), g[col].values)
            w = dd["n_err"] * dd["n_cor"]
            acc += w * dd["auroc_b"]
            wsum += w
        A["stratified"][rule] = {"strat_auroc_b": s_b, "sum_ws_identity": acc / wsum, "match": abs(s_b - acc / wsum) < 1e-12}
    A["stratified"]["c_score_align_strat_auroc"] = strat_auc(y, P.c_frozen.values, P.stratum.values)
    # ---------------- graded vs binary + c_score_exact
    gt = MC.graded_trace(y, P.c_frozen.values)
    gte = MC.graded_trace(y, P.c_score_exact.values)
    W = boot.W()
    from stats import WAuc
    wa_c, wa_b, wa_x = WAuc(y, P.c_frozen.values), WAuc(y, 1 - P.end_MAJ.values), WAuc(y, P.c_score_exact.values)
    d_cb = [wa_c(W[b]) - wa_b(W[b]) for b in range(W.shape[0])]
    d_cx = [wa_c(W[b]) - wa_x(W[b]) for b in range(W.shape[0])]
    A["graded_vs_binary"] = {"auroc_c_score_align": gt["auroc"], "auroc_b_END_MAJ": auc(y, 1 - P.end_MAJ.values),
                             "delta_graded_minus_binary": gt["auroc"] - auc(y, 1 - P.end_MAJ.values), "delta_ci": ci(d_cb),
                             "trapezoid_area_check": gt["trapezoid_area"], "named_points": gt["named_points"],
                             "auroc_c_score_exact": gte["auroc"], "delta_align_minus_exact": gt["auroc"] - gte["auroc"],
                             "delta_align_minus_exact_ci": ci(d_cx), "named_points_exact": gte["named_points"],
                             "share_endorsements_needing_align_or_gran": float(1 - P.n_eq_exact.sum() / max(P.n_eq.sum(), 1)),
                             "share_endorsements_needing_align_or_gran_ERROR": float(1 - P[P.y_AB == 1].n_eq_exact.sum() / max(P[P.y_AB == 1].n_eq.sum(), 1)),
                             "share_endorsements_needing_align_or_gran_CORRECT": float(1 - P[P.y_AB == 0].n_eq_exact.sum() / max(P[P.y_AB == 0].n_eq.sum(), 1))}
    pd.DataFrame(gt["trace"]).to_csv(TAB / "graded_trace_c_score_align.csv", index=False)
    pd.DataFrame(gte["trace"]).to_csv(TAB / "graded_trace_c_score_exact.csv", index=False)
    # system_class cut (tiers A+B, any system incl. GOLD / CCG)
    df["y_ABsys"] = [(1 if r.final_label == "ERROR" else 0) if (r.final_label in ("CORRECT", "ERROR") and r.label_tier in ("A", "B")
                     and not r.reading_choice) else None for r in df.itertuples()]
    Q = df[df.y_ABsys.notna() & df.parseable & df.c_frozen_raw.notna()].copy().reset_index(drop=True)
    Q["end_MAJ"] = (Q.c_frozen_raw < 0.5).astype(int)
    Q["y_ABsys"] = Q.y_ABsys.astype(int)
    bq = SentBoot(Q.sentence_id.values, b=2000, seed=0)
    Wq = bq.W()
    sysrows = []
    for sc, g in Q.groupby("system_class"):
        pos = np.where((Q.system_class == sc).values)[0]
        for rec in MC.cell_stats(g, "y_ABsys", {"MAJ": "end_MAJ"}, bq, Wq, pos):
            sysrows.append({"regime": "tiers A+B any system", "dim": "system_class", "cell": sc, **rec})
    A["system_class_cut"] = sysrows
    # ---------------- mechanism tests
    t0 = time.time()
    A["M1_M2"] = MC.mechanism_M1_M2(P, RULES)
    logger.info(f"M1/M2 done {time.time() - t0:.0f}s")
    A["NET"] = {"R_AB": MC.net_test(P, boot), "long_pool": MC.net_test(P, boot, long_only=True)}
    logger.info(f"NET done {time.time() - t0:.0f}s")
    sc = MC.scatter_index(P, sms, cut)
    A["SCATTER"] = sc["summary"]
    sc["sentence_table"].to_csv(TAB / "scatter_sentence_table.csv", index=False)
    logger.info(f"SCATTER done {time.time() - t0:.0f}s")
    txt = (E6 / "results" / "summary.md").read_text()
    mm = re.search(r"- judge_local_qwen8b_disg: words \{'slope_per_sd': (-?[0-9.]+), 'se': ([0-9.]+).*?'ci': \[(-?[0-9.]+), (-?[0-9.]+)\]", txt)
    js = {"slope_per_sd": float(mm.group(1)), "se": float(mm.group(2)), "ci": [float(mm.group(3)), float(mm.group(4))]} if mm else "NOT_IN_FILES"
    A["M3_local"] = MC.m3_local(P, boot, {"value": js, "source": f"{E6}/results/summary.md :: ## Complexity (GEE slope of judge-correctness per SD of words / n_conditions) :: judge_local_qwen8b_disg words"})
    logger.info(f"M3 done {time.time() - t0:.0f}s")
    # ---------------- M4
    pre5 = json.loads((E5 / "results" / "prereg.json").read_text())
    fam_map = pre5["family_map_vendor"]
    llm_fams = sorted({v for v in fam_map.values() if "never_peer" not in v})
    neutral = pre5["imputation"]["neutral"]["c_score_align"]
    K = len(llm_fams) - 1
    A["M4"] = {"llm_vendor_families": llm_fams, "K_max": K}
    A["M4"]["random_k_primary"] = M4.auroc_k(P, boot, "fam_stats", llm_fams, K, primary=True)
    A["M4"]["random_k_capped"] = M4.auroc_k(P, boot, "fam_stats", llm_fams, K, primary=False, b_ci=500)
    ff = sorted({f for fs in P.fam_stats_ff for f in fs} | set(P.family_field))
    Kf = int(P.fam_stats_ff.apply(len).max())
    A["M4"]["random_k_slot_level_sensitivity"] = M4.auroc_k(P, boot, "fam_stats_ff", ff, Kf, primary=True, b_ci=500)
    logger.info(f"M4 random-k done {time.time() - t0:.0f}s")
    fold = P.fold_E.values
    folds6 = json.loads((E6 / "folds_E.json").read_text())["sentence_fold"]
    assert all(folds6[s] == f for s, f in zip(P.sentence_id, fold)), "fold_E mismatch vs exp 6 folds_E.json"
    pools = {}
    for size in (3, 2, 4):
        fp_ = M4.fixed_pools(P, "fam_stats", llm_fams, neutral, size, fold)
        if size == 3:
            P["c_k3_best_oof"] = fp_["oof_scores"]
        pools[size] = {k: v for k, v in fp_.items() if k != "oof_scores"}
        pd.DataFrame(fp_["table"]).to_csv(TAB / f"m4_fixed_pools_k{size}.csv", index=False)
    A["M4"]["fixed_pools"] = pools
    A["M4"]["LOFO"] = M4.lofo(P, boot, "fam_stats", llm_fams, neutral, 0.712)
    logger.info(f"M4 pools/LOFO done {time.time() - t0:.0f}s")
    x4 = json.loads((I1 / "experiment-4/src" / "results" / "method_out.json").read_text())
    fj = x4["metadata"]["analysis"]["cost"]["judge_strong (API, per condition)"]
    frontier = {"usd_per_call": fj["usd_per_call"], "n_calls": fj["n_calls"],
                "source": f"{I1}/gen_art_experiment_4/results/method_out.json :: metadata.analysis.cost['judge_strong (API, per condition)'].usd_per_call"}
    pair_secs = np.array([p[4] for r in mats.values() for p in r["pairs"]])
    rows_per_fam = float(P.npc.mean() / P.n_fam_avail.mean())
    best3 = [pools[3]["in_sample_best"]["pool"]] + list(pools[3]["crossfit"]["pick_counts"])
    A["M4"]["cost"] = M4.cost_table(DS_E / "raw" / "generations.jsonl", fam_map, pair_secs, rows_per_fam, K, frontier, sorted(set(best3)))
    # AUROC(k) vs cost frontier table
    fr = []
    for k in range(1, K + 1):
        kk = A["M4"]["random_k_primary"]["k"][k]
        ck = A["M4"]["cost"]["by_k"][k - 1]
        fr.append({"k": k, "auroc_mean": kk["auroc_mean"], "band_lo": kk["draw_band"][0], "band_hi": kk["draw_band"][1],
                   "ci_lo": kk["auroc_ci_of_draw_mean"][0], "ci_hi": kk["auroc_ci_of_draw_mean"][1], "strat_auroc_mean": kk["strat_auroc_mean"],
                   "endmaj_auroc_mean": kk["endmaj_auroc_mean"], **{f"auroc_{t}": v for t, v in kk["tercile_auroc_mean"].items()},
                   "usd_per_sentence": ck["usd_per_sentence_expected"], "cpu_s_per_candidate": ck["cpu_s_per_candidate"]})
    write_csv(pd.DataFrame(fr), "m4_auroc_k_cost.csv", [f"{ROOT}/results/pair_matrix_E.jsonl :: per-family eq counts",
                                                        f"{DS_E}/raw/generations.jsonl :: cost_usd (fewshot_v1)"])
    lf = [{"family": f, **{f"{a}_{b}": v[a][b] for a in ("all_rows", "rows_not_from_f") for b in ("n", "auroc_lofo", "auroc_full", "delta")},
           "delta_ci_lo": v["all_rows"]["delta_ci"][0], "delta_ci_hi": v["all_rows"]["delta_ci"][1]}
          for f, v in A["M4"]["LOFO"]["families"].items()]
    pd.DataFrame(lf).to_csv(TAB / "m4_lofo.csv", index=False)
    logger.info(f"M4 done {time.time() - t0:.0f}s")
    # ---------------- persist
    keep = ["row_key", "sentence_id", "item_id", "slot", "family_vendor", "system", "stratum", "words", "n_conditions", "words_t",
            "ncond_bin", "exc_bin", "label_tier", "correct_not_equivalent", "final_label", "y_AB", "c_frozen", "c_score_exact",
            "end_MAJ", "end_PLUR", "end_FAM2", "end_FAMMAJ", "end_MAJ_EXACT", "c_k3_best_oof", "vocab_exact", "y_exact", "npc", "stratum_long",
            "n_eq", "n_eq_exact", "judge_local", "text", "candidate_fol", "fold_E"]
    P["stratum_long"] = P.long
    df[df.in_RAB][["row_key", "sentence_id", "stratum", "words", "n_conditions", "label_tier", "final_label", "y_AB", "c_frozen",
                   "c_frozen_raw", "parseable", "correct_not_equivalent", "text", "candidate_fol", "family_vendor", "fold_E"]].to_pickle(RES / "rab_all.pkl")
    df[["row_key", "stratum", "y_AB", "correct_not_equivalent"]].to_pickle(RES / "frame_min.pkl")
    P[keep].to_pickle(RES / "population_RAB.pkl")
    jdump(RES / "part_a.json", A)
    return A


if __name__ == "__main__":
    run()
