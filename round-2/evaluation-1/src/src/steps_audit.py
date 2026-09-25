"""Steps 8-13: MUST-FIX transcription with recompute flags, judge matched-FA recall + contamination MDE, invariance
same-set cross-check, Candidate B status, coverage-vs-request + function inventory, complexity (descriptive)."""
from __future__ import annotations

import ast
import json
import os
import re
import subprocess
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as smapi
from loguru import logger
from scipy import stats as sps

import stats_utils as su
import steps_core as sc
from load import DS_E, EXP_A, EXP_C, EXP_D, GA, IT1, rj

BIN = ("CORRECT", "ERROR")
RUN = IT1.parent.parent


# ================================================================================================= STEP 8
class Transcriber:
    def __init__(self):
        self.rows = []

    def add(self, table_id, quantity, value, source, key, ci=None, n=None, recomputed=None, tol=0.005):
        if recomputed is None:
            flag = "TRANSCRIBED_ONLY"
        elif value is None:
            flag = "RECOMPUTED_ONLY"
        else:
            try:
                flag = "MATCH" if abs(float(value) - float(recomputed)) <= tol else "MISMATCH"
            except (TypeError, ValueError):
                flag = "MATCH" if str(value) == str(recomputed) else "MISMATCH"
        self.rows.append({"table_id": table_id, "quantity": quantity, "value": value, "CI": None if ci is None else json.dumps(ci),
                          "n": n, "source_path": str(source), "json_key_path": key, "recomputed_value": recomputed, "match_flag": flag})

    def df(self, prefix=None):
        d = pd.DataFrame(self.rows)
        return d if prefix is None else d[d.table_id.str.startswith(prefix)]


_DEV = None


def _dev_ids() -> set:
    global _DEV
    if _DEV is None:
        _DEV = set(json.loads((EXP_D / "results/analysis.json").read_text())["prompt_dev"]["dev_slice_ids"])
    return _DEV


def _d_block_items(df: pd.DataFrame, block: str) -> tuple[pd.DataFrame, np.ndarray] | None:
    L, H = df[(df.track == "L") & df.in_D], df[(df.track == "H") & df.in_D]
    H = H[~H.index.isin(list(_dev_ids()))]  # D's prompt-dev slice is excluded from every H headline
    if block == "L_primary":
        s = L[L.lab_D.isin(BIN)]
        return s, (s.lab_D == "ERROR").astype(int).values
    if block == "L_borderline_to_uncertain":
        s = L[L.lab_D.isin(BIN) & (L.D_vocab_borderline != True)]  # noqa: E712
        return s, (s.lab_D == "ERROR").astype(int).values
    if block == "L_pessimistic_err_or_uncertain":
        s = L[L.lab_D.isin(BIN + ("UNCERTAIN",))]
        return s, (s.lab_D != "CORRECT").astype(int).values
    if block == "L_exclude_subst_only":
        s = L[L.lab_D.isin(BIN) & (L.D_subst_only != True)]  # noqa: E712
        return s, (s.lab_D == "ERROR").astype(int).values
    if block == "L_unparseable_as_error":
        s = L[L.lab_D.isin(BIN + ("UNPARSEABLE",))]
        return s, (s.lab_D != "CORRECT").astype(int).values
    if block == "H_primary":
        s = H[H.lab_D.isin(BIN)]
        return s, (s.lab_D == "ERROR").astype(int).values
    if block == "H_curator_view":
        s = H[H.lab_D_hcur.isin(BIN)]
        return s, (s.lab_D_hcur == "ERROR").astype(int).values
    return None


def _d_recompute_auroc(df, sub, y, m, n_app):
    """Exp D conventions: FAIL -> metric max over the screen; NA (not applicable) excluded. The oriented_scores dict
    stores both as None, so try both and keep the variant whose n matches the reported n_applicable."""
    s = sub[m].values.astype(float)
    mx = np.nanmax(df[m].values.astype(float)) if df[m].notna().any() else np.nan
    ok = ~np.isnan(s)
    variants = {"fail_to_max": (len(s), su.auroc(y, np.where(np.isnan(s), mx, s)) if len(np.unique(y)) > 1 else None),
                "exclude_missing": (int(ok.sum()), su.auroc(y[ok], s[ok]) if ok.sum() and len(np.unique(y[ok])) > 1 else None)}
    for k, (n, a) in variants.items():
        if n == n_app:
            return a, k
    return variants["exclude_missing"][1], "exclude_missing(n differs)"


def step8_mustfix(df: pd.DataFrame, out_tab) -> dict:
    T = Transcriber()
    # -------------------------------------------------------------------- EXP D
    pA = EXP_D / "results/analysis.json"
    aD = json.loads(pA.read_text())
    for block in ["L_primary", "H_primary", "H_curator_view", "L_exclude_subst_only", "L_unparseable_as_error",
                  "L_borderline_to_uncertain", "L_pessimistic_err_or_uncertain"]:
        blk = aD["sets"].get(block)
        if not blk:
            continue
        items = _d_block_items(df, block)
        T.add(f"D.sets.{block}", "n", blk.get("n"), pA, f"sets.{block}.n", recomputed=len(items[1]) if items else None, tol=0)
        for m, r in blk["metrics"].items():
            rec, how = (None, None)
            if items is not None and m in df.columns:
                rec, how = _d_recompute_auroc(df, items[0], items[1], m, r.get("n_applicable"))
            T.add(f"D.sets.{block}", f"AUROC {m} [{how}]" if how else f"AUROC {m}", r.get("auroc"), pA, f"sets.{block}.metrics.{m}.auroc",
                  ci=r.get("auroc_ci"), n=r.get("n_applicable"), recomputed=rec)
    # paired vs judge (DeLong p): each metric scored with the convention whose n matches the block's n_applicable
    def _var(sub, m, n_app):
        v = sub[m].values.astype(float)
        mx = np.nanmax(df[m].values.astype(float))
        if n_app == len(v):
            return np.where(np.isnan(v), mx, v), np.ones(len(v), bool)
        return v, ~np.isnan(v)
    for block, mets in aD["paired_vs_judge_cheap_disg"].items():
        items = _d_block_items(df, block)
        bm = aD["sets"].get(block, {}).get("metrics", {})
        for m, r in mets.items():
            rec = None
            if items is not None and m in df.columns and m in bm:
                sub, y = items
                sm_, okm = _var(sub, m, bm[m].get("n_applicable"))
                sj, okj = _var(sub, "judge_cheap_disg", bm["judge_cheap_disg"].get("n_applicable"))
                ok = okm & okj
                if ok.sum() and len(np.unique(y[ok])) > 1:
                    rec = su.auroc(y[ok], sm_[ok]) - su.auroc(y[ok], sj[ok])
            T.add(f"D.paired_vs_judge.{block}", f"delta {m} - judge_cheap_disg", r.get("delta_auroc"), pA,
                  f"paired_vs_judge_cheap_disg.{block}.{m}", ci=r.get("ci"), recomputed=rec)
            T.add(f"D.paired_vs_judge.{block}", f"DeLong p {m}", (r.get("delong") or {}).get("p"), pA,
                  f"paired_vs_judge_cheap_disg.{block}.{m}.delong.p")
    # frontier same-item
    for sset, d1 in aD["paired_strong_subset"].items():
        tr = "L" if sset.startswith("L") else "H"
        for cheap, d2 in d1.items():
            for strong, r in d2.items():
                # exp D's H strong subset (n=96) is scored on the H_curator_view labels
                lab = "lab_D" if tr == "L" else "lab_D_hcur"
                sub = df[(df.track == tr) & df.in_D & df[lab].isin(BIN) & df[strong].notna()]
                y = (sub[lab] == "ERROR").astype(int).values
                mxc = np.nanmax(df[cheap].values)
                rec = su.auroc(y, sub[strong].values) - su.auroc(y, sub[cheap].fillna(mxc).values) if len(sub) else None
                T.add(f"D.frontier.{sset}", f"{strong} - {cheap}", r.get("delta_auroc"), pA, f"paired_strong_subset.{sset}.{cheap}.{strong}",
                      ci=r.get("ci"), n=len(sub), recomputed=rec)
                T.add(f"D.frontier.{sset}", f"{strong} - {cheap} DeLong p", (r.get("delong") or {}).get("p"), pA,
                      f"paired_strong_subset.{sset}.{cheap}.{strong}.delong.p")
    # invariance per family (recompute from rewrite_scores.jsonl at D thresholds)
    rw = rj(EXP_D / "results/rewrite_scores.jsonl")
    thr = aD["thresholds"]
    base_sc = {k: r for k, r in zip(df.index, df.to_dict(orient="records"))}
    for m, fams in aD["invariance"]["per_metric"].items():
        for fam, r in fams.items():
            if not isinstance(r, dict) or "fa_rewrite" not in r:
                continue
            # exp D convention: a FAILED score (stored as None) counts as the metric's maximum (flagged)
            rows = [x for x in rw if x["family"] == fam and x["base_item_id"] in base_sc]
            if rows and m in thr and m in df.columns:
                mx = np.nanmax(df[m].values.astype(float))
                sr = np.array([(x.get("oriented_scores") or {}).get(m) for x in rows], dtype=float)
                sb = np.array([base_sc[x["base_item_id"]].get(m) for x in rows], dtype=float)
                sr, sb = np.where(np.isnan(sr), mx, sr), np.where(np.isnan(sb), mx, sb)
                fr, fb = sr > thr[m], sb > thr[m]
                T.add("D.invariance", f"{m}|{fam} fa_rewrite", r["fa_rewrite"], EXP_D / "results/rewrite_scores.jsonl",
                      f"invariance.per_metric.{m}.{fam}.fa_rewrite", n=r.get("n"), recomputed=float(fr.mean()))
                T.add("D.invariance", f"{m}|{fam} fa_base (REPRINT = base-flagged share)", r["fa_base"], pA,
                      f"invariance.per_metric.{m}.{fam}.fa_base", n=r.get("n"), recomputed=float(fb.mean()))
                T.add("D.invariance", f"{m}|{fam} flip_rate", r["flip_rate"], pA, f"invariance.per_metric.{m}.{fam}.flip_rate",
                      n=r.get("n"), recomputed=float((fr != fb).mean()))
    # cost per component (recompute from costs.jsonl)
    costs = pd.DataFrame(rj(EXP_D / "results/costs.jsonl"))
    for comp, g in costs.groupby("component"):
        T.add("D.cost", f"{comp} usd per call", None, EXP_D / "results/costs.jsonl", f"component={comp}", n=len(g),
              recomputed=float(g.cost.mean()))
        T.add("D.cost", f"{comp} seconds per call", None, EXP_D / "results/costs.jsonl", f"component={comp}", n=len(g),
              recomputed=float(g.seconds.mean()))
    for k, v in aD["cost"].items():
        if isinstance(v, dict):
            for kk, vv in v.items():
                if isinstance(vv, (int, float)):
                    T.add("D.cost", f"{k}.{kk}", vv, pA, f"cost.{k}.{kk}")
    for m, v in aD["coverage"]["per_metric"].items():
        for tr in ("L", "H"):
            if tr in v:
                T.add("D.coverage", f"{m}|{tr} coverage", v[tr].get("coverage"), pA, f"coverage.per_metric.{m}.{tr}.coverage", n=v[tr].get("n_applicable"))
    # H complexity table (transcribe)
    for blk, bins in aD["complexity"].items():
        for b, r in bins.items():
            if isinstance(r, dict):
                for m, rr in r.items():
                    if isinstance(rr, dict) and "auroc" in rr:
                        T.add(f"D.complexity.{blk}", f"{b}|{m} AUROC", rr["auroc"], pA, f"complexity.{blk}.{b}.{m}.auroc", n=r.get("n"))
    # -------------------------------------------------------------------- EXP A
    pM = EXP_A / "results/metrics.json"
    mA = json.loads(pM.read_text())
    L = df[(df.track == "L") & df.in_A]
    prim = L[L.lab_A.isin(BIN)]
    yA = (prim.lab_A == "ERROR").astype(int).values
    flagmap = {"l1_any": "l1_any", "l2_bow_flag": "bow_flag", "l2_role_flag": "role_flag", "l3_flag": "l3_flag", "fused_flag": "fused_flag"}
    for setname, layers in mA["binary_layers"].items():
        for lay, r in layers.items():
            if not isinstance(r, dict):
                continue
            rec = {}
            if setname == "primary_L_ERROR_vs_CORRECT" and lay in flagmap:
                st = su.at_flag(yA, prim[flagmap[lay]].values > 0.5)
                rec = {"TPR": st["recall"], "FPR": st["fa"], "precision": st["precision"], "precision_at_prev_0.1": st["prec_at_prev10"],
                       "precision_at_prev_0.25": st["prec_at_prev25"]}
            for q in ("TPR", "FPR", "precision", "precision_at_prev_0.1", "precision_at_prev_0.25"):
                if q in r:
                    T.add(f"A.binary_layers.{setname}", f"{lay} {q}", r[q], pM, f"binary_layers.{setname}.{lay}.{q}", n=r.get("n_pos"),
                          recomputed=rec.get(q))
    for setname, ev in mA["evaluations"].items():
        for m, r in (ev.get("scores") or {}).items():
            rec = None
            if setname == "primary_L_ERROR_vs_CORRECT":
                col = {"l2_bow": "l2_bow_Adef", "l2_role": "role_count"}.get(m, m)
                if col in prim.columns and prim[col].notna().all():
                    rec = su.auroc(yA, prim[col].values)
            T.add(f"A.evaluations.{setname}", f"AUROC {m}", r.get("AUROC"), pM, f"evaluations.{setname}.scores.{m}.AUROC",
                  ci=r.get("AUROC_CI95_cluster"), n=ev.get("n"), recomputed=rec)
    cal = json.loads((EXP_A / "results/calibration.json").read_text())
    for f, r in cal["L3_gate_primary"].items():
        if isinstance(r, dict):
            T.add("A.L3_HREF_gate", f"{f} field accuracy", r["acc"], EXP_A / "results/calibration.json", f"L3_gate_primary.{f}.acc",
                  ci=r.get("wilson95"), n=r.get("n"))
    T.add("A.L3_HREF_gate", "force excluded from L3 score (acc < gate)", "mm_force .69 excluded", EXP_A / "prereg.json", "L3_field_gate")
    pre = json.loads((EXP_A / "prereg.json").read_text())
    T.add("A.fusion", "fusion features", json.dumps(pre["fusion_features"]), EXP_A / "prereg.json", "fusion_features")
    T.add("A.fusion", "fusion model", pre["fusion_model"], EXP_A / "prereg.json", "fusion_model")
    coef_note = "fusion coefficients not stored in prereg.json; results/fusion_H_noleak.pkl not unpickled (sklearn-version-dependent pickle); TRANSCRIBED_ONLY"
    try:
        import pickle
        with open(EXP_A / "results/fusion_H_noleak.pkl", "rb") as fh:
            obj = pickle.load(fh)
        est = obj[-1] if hasattr(obj, "__getitem__") and not isinstance(obj, dict) else obj
        if isinstance(obj, dict):
            est = obj.get("model") or obj.get("clf") or obj
        coefs = getattr(est, "coef_", None)
        if coefs is None and hasattr(est, "steps"):
            coefs = est.steps[-1][1].coef_
        if coefs is not None:
            coef_note = json.dumps(dict(zip(pre["fusion_features"], [round(float(c), 4) for c in np.ravel(coefs)])))
    except Exception as ex:  # noqa: BLE001  pickle can raise many types across sklearn versions
        logger.warning(f"fusion pkl not readable: {type(ex).__name__}: {ex}")
    T.add("A.fusion", "fusion standardised coefficients (noleak model)", coef_note, EXP_A / "results/fusion_H_noleak.pkl", "pickle")
    readme = (EXP_A / "README.md").read_text().splitlines()
    for i, line in enumerate(readme, 1):
        if re.search(r"Test-retest|qwen3-30b-a3b-instruct-2507 on HREF|Local outage model", line):
            T.add("A.robustness_rows", line.strip()[:60], line.strip()[:400], EXP_A / "README.md", f"line {i}")
    for m, r in mA["track_H_paired_same_text_AUROC"].items():
        T.add("A.trackH_paired", f"AUROC {m}", r["auroc"], pM, f"track_H_paired_same_text_AUROC.{m}", n=r["n"])
    dj = su.auroc(yA, prim.l3_score_llmformula.values) - su.auroc(yA, prim.l3_score.values) if prim.l3_score_llmformula.notna().all() else None
    T.add("A.decomposed_judge", "AUROC(l3_llmformula) - AUROC(l3_score)", -0.0589, EXP_A / "README.md", "line ~212 paired vs l3_score", recomputed=dj)
    con = mA["contamination_trackL_l3_AUROC"]
    okd = prim.l3_score_disguised.notna() & prim.l3_score_exact.notna()
    T.add("A.disguise", "L3 AUROC orig exact-align", con["orig_exact_align"], pM, "contamination_trackL_l3_AUROC.orig_exact_align", n=con["n"],
          recomputed=su.auroc(yA[okd.values], prim.l3_score_exact.values[okd.values]) if okd.any() else None)
    T.add("A.disguise", "L3 AUROC disguised", con["disguised"], pM, "contamination_trackL_l3_AUROC.disguised", n=con["n"],
          recomputed=su.auroc(yA[okd.values], prim.l3_score_disguised.values[okd.values]) if okd.any() else None)
    for k, v in mA["label_artefacts"].items():
        if isinstance(v, (int, float)):
            T.add("A.label_sets", k, v, pM, f"label_artefacts.{k}")
    for k, v in mA["gates_fused_primary"].items():
        if isinstance(v, dict):
            T.add("A.gates", k, v.get("value", v.get("worst_family_FA")), pM, f"gates_fused_primary.{k}")
    # -------------------------------------------------------------------- EXP C
    pS = EXP_C / "results/summary.json"
    sC = json.loads(pS.read_text())
    Lc = df[(df.track == "L") & df.in_C]
    for setname, mets in sC["auroc"].items():
        for m, r in mets.items():
            if not isinstance(r, dict) or "auroc" not in r:
                continue
            rec = None
            if setname == "primary" and m in Lc.columns:
                s = Lc[Lc.lab_C.isin(BIN) & Lc.c_score.notna() & Lc[m].notna()]
                if len(s) == r.get("n"):
                    rec = su.auroc((s.lab_C == "ERROR").astype(int).values, s[m].values)
            if setname in ("track_H", "trackH", "H") and m in df.columns:
                s = df[(df.track == "H") & df.lab_C.isin(BIN) & df[m].notna()]
                if len(s) == r.get("n"):
                    rec = su.auroc((s.lab_C == "ERROR").astype(int).values, s[m].values)
            T.add(f"C.auroc.{setname}", f"AUROC {m}", r["auroc"], pS, f"auroc.{setname}.{m}.auroc", ci=r.get("auroc_ci95"), n=r.get("n"), recomputed=rec)
    for k, r in sC["secondary_peer_as_candidate"].get("all_sentences", {}).items():
        T.add("C.multifamily_1686", f"AUROC {k}", r.get("auroc"), pS, f"secondary_peer_as_candidate.all_sentences.{k}.auroc", ci=r.get("auroc_ci95"), n=r.get("n"))
    for k, r in sC["crossfit_logistic"].items():
        T.add("C.crossfit", k, r.get("delta"), pS, f"crossfit_logistic.{k}.delta", ci=r.get("delta_ci95"), n=r.get("n"))
    # RENAME and other families: recompute FA from consensus.json rewrites
    cons = json.loads((EXP_C / "results/consensus.json").read_text())
    rwc = pd.DataFrame([r for r in cons["rewrites"] if r.get("applicable")])
    for fam, r in sC["rewrite_invariance"].items():
        if isinstance(r, dict) and "false_alarm_rate" in r:
            g = rwc[(rwc.family == fam) & (rwc.reparse_ok == True) & rwc.eq_frac_full.notna()]  # noqa: E712
            T.add("C.rewrite_invariance", f"{fam} false_alarm_rate", r["false_alarm_rate"], pS, f"rewrite_invariance.{fam}.false_alarm_rate",
                  ci=r.get("false_alarm_ci95"), n=r.get("n_scored"), recomputed=float(g.flag.astype(bool).mean()) if len(g) else None)
            T.add("C.rewrite_invariance", f"{fam} flip_rate", r["flip_rate"], pS, f"rewrite_invariance.{fam}.flip_rate", n=r.get("n_scored"),
                  recomputed=float((g.flag.astype(bool) != g.base_flag.astype(bool)).mean()) if len(g) else None)
    # system level: Spearman + bootstrap-over-systems CI + Kendall
    sysd = pd.DataFrame(sC["system_level"]["systems"])
    rho = sps.spearmanr(sysd.error_rate, sysd.mean_c_score).correlation
    tau = sps.kendalltau(sysd.error_rate, sysd.mean_c_score).correlation
    rng = np.random.default_rng(0)
    bs_r, bs_t = [], []
    for _ in range(2000):
        ii = rng.integers(0, len(sysd), len(sysd))
        a, b = sysd.error_rate.values[ii], sysd.mean_c_score.values[ii]
        if len(np.unique(a)) < 3 or len(np.unique(b)) < 3:
            continue
        bs_r.append(sps.spearmanr(a, b).correlation)
        bs_t.append(sps.kendalltau(a, b).correlation)
    rep = sC["system_level"].get("spearman_error_rate_vs_mean_c_score", sC["system_level"].get("spearman"))
    T.add("C.system_level", f"Spearman(error_rate, mean c_score) over {len(sysd)} systems", rep if isinstance(rep, (int, float)) else 0.87, pS,
          "system_level (reported 0.87 in C summary text)", ci=su.ci95(np.array(bs_r)), n=len(sysd), recomputed=float(rho), tol=0.01)
    T.add("C.system_level", "Kendall tau (NEW) with bootstrap-over-systems CI; underpowered (<10 systems)", None, pS, "system_level.systems",
          ci=su.ci95(np.array(bs_t)), n=len(sysd), recomputed=float(tau))
    oa = sC["operator_agreement"]
    T.add("C.operator_agreement", "medoid exact operator multiset match", oa["exact_multiset"], pS, "operator_agreement.exact_multiset", ci=oa.get("exact_ci95"), n=oa["n"])
    T.add("C.operator_agreement", "chance (majority exact)", oa["chance_majority_exact"]["freq"], pS, "operator_agreement.chance_majority_exact.freq")
    T.add("C.operator_agreement", "coarse class match", oa["coarse_class"], pS, "operator_agreement.coarse_class", ci=oa.get("coarse_ci95"))
    T.add("C.operator_agreement", "chance (majority coarse)", oa["chance_majority_coarse"]["freq"], pS, "operator_agreement.chance_majority_coarse.freq")
    vc = sC["shared_aligner_confound"]["vocab_clean_subset"]
    for m, r in vc.items():
        if isinstance(r, dict) and "auroc" in r:
            T.add("C.vocab_clean_control", f"AUROC {m}", r["auroc"], pS, f"shared_aligner_confound.vocab_clean_subset.{m}.auroc", ci=r.get("auroc_ci95"), n=r.get("n"))

    def walk(o, path, pat):
        if isinstance(o, dict):
            for k, v in o.items():
                if re.search(pat, str(k), re.I) and isinstance(v, (int, float, dict)):
                    yield f"{path}.{k}", v
                yield from walk(v, f"{path}.{k}", pat)
    for kp, v in walk(sC, "summary", r"partial|interaction|slope"):
        T.add("C.partial_and_length", kp, v if isinstance(v, (int, float)) else json.dumps(v)[:300], pS, kp)
    # -------------------------------------------------------------------- DATASET E (transcribe from dataset_card.md)
    card_p = DS_E / "dataset_card.md"
    card = card_p.read_text().splitlines()
    pats = {"panel accepts expert-corrected formulas": r"accepts only 0\.613", "panel majority accuracy on real errors": r"majority accuracy .* 0\.727|about\s*$|0\.727 of the time",
            "MALLS gold judged unfaithful": r"440/535", "tier counts (screen)": r"Tiers: `", "final labels by system class": r"Final labels by system class",
            "screen track-L auto vs panel": r"Track-L auto label vs panel majority"}
    for q, pat in pats.items():
        for i, line in enumerate(card, 1):
            if re.search(pat, line):
                T.add("E.card", q, line.strip()[:400], card_p, f"dataset_card.md line {i}")
                break
    sec = None
    for i, line in enumerate(card, 1):
        mm = re.match(r"## (\d+)\.", line)
        if mm:
            sec = int(mm.group(1))
        if sec in (3, 4, 5, 11) and line.startswith("|") and not line.startswith("|---"):
            T.add(f"E.card.section{sec}", f"row line {i}", line.strip()[:400], card_p, f"dataset_card.md section {sec} line {i}")
        if sec == 11 and line.startswith("- "):
            T.add("E.card.section11", f"bullet line {i}", line.strip()[:400], card_p, f"dataset_card.md section 11 line {i}")
    T.add("E.card", "heldout tier counts A/B/C/none/UNPARSEABLE (plan-stated 1,044 / 2,157 / 3,891 / 276 / 1,086)",
          "see card sections 2-3; transcribed per plan, not recomputed (firewall)", card_p, "sections 2-3")
    # panel calibration recompute (permitted group)
    pc = json.loads((Path(__file__).resolve().parent.parent / "data/panel_calibration.json").read_text())
    import ast as _ast
    gate = [e for e in pc if e["metadata_subset"] == "synthetic_gate"]
    pairs = [e for e in pc if e["metadata_subset"] == "trackH_real_error_pairs"]
    members = ["P1", "P3", "R1"]
    cal = {}
    for who in members + ["majority"]:
        tf, nf, tu, nu = 0, 0, 0, 0
        for e in gate:
            v = _ast.literal_eval(e["metadata_panel_verdicts_prompt_v2"]) if isinstance(e["metadata_panel_verdicts_prompt_v2"], str) else e["metadata_panel_verdicts_prompt_v2"]
            if who == "majority":
                vs = [v[m]["faithful"] for m in members if m in v and v[m].get("faithful") is not None]
                if not vs:
                    continue
                pred = sum(vs) > len(vs) / 2
            else:
                if who not in v or v[who].get("faithful") is None:
                    continue
                pred = v[who]["faithful"]
            if e["output"] == "FAITHFUL":
                nf += 1
                tf += pred
            else:
                nu += 1
                tu += (not pred)
        rf, ru = tf / nf if nf else None, tu / nu if nu else None
        cal[f"gate_{who}"] = {"n": nf + nu, "faithful_side_acc": rf, "unfaithful_side_acc": ru,
                              "balanced_acc": (rf + ru) / 2 if rf is not None and ru is not None else None}
    for amb_name, amb_filter in [("all96", lambda e: True), ("unambiguous", lambda e: str(e.get("metadata_ambiguous_curated")) == "False")]:
        for who in members + ["majority"]:
            fl, ac, n = 0, 0, 0
            for e in pairs:
                if not amb_filter(e):
                    continue
                v = _ast.literal_eval(e["metadata_panel_votes"]) if isinstance(e["metadata_panel_votes"], str) else e["metadata_panel_votes"]
                if not v:
                    continue
                if who == "majority":
                    o = [v[m]["orig_faithful"] for m in members if m in v and v[m].get("orig_faithful") is not None]
                    c = [v[m]["corr_faithful"] for m in members if m in v and v[m].get("corr_faithful") is not None]
                    if not o or not c:
                        continue
                    of, cf = sum(o) > len(o) / 2, sum(c) > len(c) / 2
                else:
                    if who not in v or v[who].get("orig_faithful") is None:
                        continue
                    of, cf = v[who]["orig_faithful"], v[who]["corr_faithful"]
                n += 1
                fl += (not of)
                ac += bool(cf)
            cal[f"expert_{amb_name}_{who}"] = {"n_pairs": n, "unfaithful_side_acc(original flagged)": fl / n if n else None,
                                                "faithful_side_acc(corrected accepted)": ac / n if n else None,
                                                "balanced_acc": (fl + ac) / (2 * n) if n else None}
    for k, v in cal.items():
        for kk, vv in v.items():
            ref = None
            if k == "expert_unambiguous_majority" and kk.startswith("faithful_side"):
                ref = 0.613
            if k == "expert_unambiguous_majority" and kk.startswith("unfaithful_side"):
                ref = 0.84
            if k == "gate_P1" and kk == "balanced_acc":
                ref = 0.861
            T.add("E.panel_calibration", f"{k}.{kk}", ref, "data/panel_calibration.json (from dataset E full_data_out.json panel_calibration group)",
                  f"{k}.{kk}", recomputed=vv, tol=0.01)
    tab = T.df()
    for src in ["D.", "A.", "C.", "E."]:
        out_tab(tab[tab.table_id.str.startswith(src)], f"mustfix_{src[0]}.csv", "iteration-1 artifacts (see source_path column); recompute from per-item files where possible")
    summ = tab.match_flag.value_counts().to_dict()
    mism = tab[tab.match_flag == "MISMATCH"][["table_id", "quantity", "value", "recomputed_value"]].head(60)
    logger.info(f"step8: {len(tab)} rows; flags {summ}")
    diag = ("All residual MISMATCH rows involve metrics that exp D stores as NOT-APPLICABLE on part of a block (judge_strong_* and "
            "judge_local_qwen14b_* exist only on the 200L/96H strong subset; pilot_rerun_jacc / pilot_dangling are NA where no rerun or "
            "story exists). exp D's oriented_scores stores NA and FAIL identically (None), so the full-block paired deltas and the "
            "pilot_rerun_jacc invariance rows cannot be re-derived exactly; the dedicated same-item frontier rows (D.frontier.*) and every "
            "cheap-judge/round-trip/structural row DO reproduce. No mismatch touches a headline number.")
    return {"n_rows": len(tab), "flags": summ, "mismatches": mism, "mismatch_diagnosis": diag, "panel_calibration_recomputed": cal,
            "panel_gate_reference": "R_ADJ gate: balanced accuracy >= 0.85 and >= 0.80 per side"}


# ================================================================================================= STEP 9
JUDGES = ["judge_cheap", "judge_cheap2", "judge_strong", "judge_local_qwen8b", "judge_local_llama8b", "judge_local_qwen14b"]


def step9_judges(df, regimes, out_tab, B=2000) -> dict:
    rows = []
    res = {}
    for rn in ("R_SOLVER_CONS", "R_ADJ_AB"):
        reg = regimes[rn]
        sub_all = df.loc[reg["y"].index]
        adj = rn.startswith("R_ADJ")
        for j in JUDGES:
            o, d = f"{j}_orig", f"{j}_disg"
            if o not in df.columns or d not in df.columns:
                continue
            sub = sub_all[sub_all[o].notna() & sub_all[d].notna()]
            y = reg["y"].loc[sub.index].values.astype(int)
            if y.sum() < 10 or (1 - y).sum() < 10:
                continue
            cb = su.ClusterBoot(list(sub.cluster.values), B=B)
            W = cb.item_W()
            ops_col = "E_repair_ops" if adj else "ops_C"
            coarse = np.array(["COMPOUND" if not isinstance(x, list) or not x else su.op_class(x) for x in sub[ops_col]])
            for f in (0.10, 0.20):
                fp = {}
                for cond, col in (("orig", o), ("disg", d)):
                    s = sub[col].values.astype(float)
                    rule = su.matched_fa_rule(s[y == 0], f)
                    fp[cond] = su.flag_prob(s, rule)
                    fp[cond + "_fa"] = rule[2]
                for cell in ["ALL", "POLARITY", "COVERAGE", "STRUCT", "MIXED", "COMPOUND"]:
                    mask = (y == 1) if cell == "ALL" else ((y == 1) & (coarse == cell))
                    n = int(mask.sum())
                    if n == 0:
                        continue
                    Wm = W[:, mask]
                    with np.errstate(invalid="ignore", divide="ignore"):
                        dd = (Wm @ fp["orig"][mask] - Wm @ fp["disg"][mask]) / Wm.sum(1)
                    ci = su.ci95(dd)
                    rows.append({"regime": rn, "judge": j, "fa_target": f, "cell": cell, "n_err": n, "informative": n >= 15,
                                 "recall_orig": float(fp["orig"][mask].mean()), "recall_disg": float(fp["disg"][mask].mean()),
                                 "achieved_fa_orig": fp["orig_fa"], "achieved_fa_disg": fp["disg_fa"],
                                 "diff_orig_minus_disg": float(fp["orig"][mask].mean() - fp["disg"][mask].mean()), "ci_lo": ci[0], "ci_hi": ci[1],
                                 "n_items": len(sub), "auroc_orig": su.auroc(y, sub[o].values), "auroc_disg": su.auroc(y, sub[d].values)})
    J = pd.DataFrame(rows)
    out_tab(J, "judge_matched_fa.csv", "exp D per_item_scores oriented judge scores (orig vs nonce-disguised) under R_SOLVER_CONS and R_ADJ_AB")
    allrow = J[(J.cell == "ALL") & (J.fa_target == 0.10)]
    res["matched_fa_recall_FA010_ALL"] = allrow[["regime", "judge", "recall_orig", "recall_disg", "diff_orig_minus_disg", "ci_lo", "ci_hi"]]
    # contamination DiD with independent bootstraps per track
    crow = []
    for j in JUDGES:
        o, d = f"{j}_orig", f"{j}_disg"
        if o not in df.columns:
            continue
        per = {}
        for tname, rn in (("L", "R_SOLVER_OWN_D"), ("H", "H_SOLVER"), ("H_curator", "H_CURATOR")):
            reg = regimes[rn]
            sub = df.loc[reg["y"].index]
            sub = sub[sub[o].notna() & sub[d].notna()]
            y = reg["y"].loc[sub.index].values.astype(int)
            if y.sum() < 5 or (1 - y).sum() < 5:
                continue
            cb = su.ClusterBoot(list(sub.cluster.values), B=B, seed={"L": 0, "H": 1, "H_curator": 2}[tname])
            W = cb.item_W()
            gap_b = su.boot_auc_w(y, sub[o].values, W) - su.boot_auc_w(y, sub[d].values, W)
            gap = su.auroc(y, sub[o].values) - su.auroc(y, sub[d].values)
            per[tname] = (gap, gap_b, len(sub), int(y.sum()))
            ci = su.ci95(-gap_b)
            crow.append({"judge": j, "quantity": f"disg-orig AUROC on {tname}", "value": -gap, "ci_lo": ci[0], "ci_hi": ci[1], "n": len(sub),
                         "n_err": int(y.sum()), "significant_drop": bool(ci[1] is not None and ci[1] < 0), "se": float(np.nanstd(gap_b)), "mde_80": None,
                         "detects_0.05": None})
        for htr in ("H", "H_curator"):
            if htr in per and "L" in per:
                did = per[htr][0] - per["L"][0]
                bs = per[htr][1] - per["L"][1]
                se = float(np.nanstd(bs))
                ci = su.ci95(bs)
                crow.append({"judge": j, "quantity": f"DiD (orig-disg)_{htr} - (orig-disg)_L", "value": did, "ci_lo": ci[0], "ci_hi": ci[1],
                             "n": per[htr][2] + per["L"][2], "n_err": per[htr][3] + per["L"][3], "significant_drop": None, "se": se,
                             "mde_80": 2.80 * se, "detects_0.05": bool(2.80 * se <= 0.05)})
    C = pd.DataFrame(crow)
    out_tab(C, "contamination.csv", "exp D judges orig vs disguised; DiD with independent H and L sentence bootstraps; MDE = 2.80 x SE (80% power, alpha .05)")
    res["contamination"] = C
    aD = json.loads((EXP_D / "results/analysis.json").read_text())
    c2 = aD["contamination"].get("judge_cheap2", {})
    res["verify_nano_drops"] = {"H_primary_reported": c2.get("H_primary", {}).get("delta_disg_minus_orig"),
                                "H_curator_reported": c2.get("H_curator_view", {}).get("delta_disg_minus_orig"),
                                "H_recomputed": C[(C.judge == "judge_cheap2") & (C.quantity == "disg-orig AUROC on H")].value.tolist(),
                                "H_curator_recomputed": C[(C.judge == "judge_cheap2") & (C.quantity == "disg-orig AUROC on H_curator")].value.tolist()}
    return res


# ================================================================================================= STEP 10
def _nf(s: str) -> str:
    return re.sub(r"\s+", "", str(s or ""))


def step10_invariance(df, commons, out_tab) -> dict:
    A_set = json.loads((EXP_A / "invariance_set.json").read_text())
    A_sc = json.loads((EXP_A / "results/invariance_scores.json").read_text())
    D_set = json.loads((EXP_D / "data/invariance_items.json").read_text())
    D_sc = {r["rw_id"]: r for r in rj(EXP_D / "results/rewrite_scores.jsonl")}
    cons = json.loads((EXP_C / "results/consensus.json").read_text())
    C_set = [r for r in cons["rewrites"]]
    sets = {"A": {(r["item_id"], r["family"]): _nf(r["rewritten_fol"]) for r in A_set if r.get("rewritten_fol")},
            "D": {(r["base_item_id"], r["family"]): _nf(r["candidate_fol"]) for r in D_set},
            "C": {(r["item_id"], r["family"]): _nf(r["fol"]) for r in C_set if r.get("fol") and str(r.get("applicable")) == "True"}}
    fams = sorted({f for s in sets.values() for (_, f) in s})
    orow = []
    for fam in fams:
        r = {"family": fam}
        for k, s in sets.items():
            r[f"n_{k}"] = sum(1 for (_, f) in s if f == fam)
        for a, b in (("A", "D"), ("A", "C"), ("C", "D")):
            ka = {i for (i, f) in sets[a] if f == fam}
            kb = {i for (i, f) in sets[b] if f == fam}
            shared = ka & kb
            ident = sum(1 for i in shared if sets[a][(i, fam)] == sets[b][(i, fam)])
            r[f"shared_base_{a}{b}"] = len(shared)
            r[f"identical_rewrites_{a}{b}"] = ident
            r[f"SAME_REWRITE_SET_{a}{b}"] = "YES" if shared and ident == len(shared) == len(ka) == len(kb) else ("PARTIAL" if ident else "NO")
        orow.append(r)
    O = pd.DataFrame(orow)
    out_tab(O, "invariance_set_overlap.csv", "exp A invariance_set.json, exp D data/invariance_items.json, exp C consensus.json rewrites; FOL compared after whitespace removal")
    # per-family, per-metric FA on CORRECT bases (each experiment's own label) at shipped threshold and matched FA 0.10
    sub, y = commons["R_SOLVER_CONS"]
    aD = json.loads((EXP_D / "results/analysis.json").read_text())
    thr = aD["thresholds"]

    def mrule(m):
        s = sub[m].values.astype(float)
        return su.matched_fa_rule(s[y == 0], 0.10)
    rows = []
    # A: fused (score p_fused_H + shipped fused_flag), bow_flag, l3_flag
    lab = df.lab_A.to_dict()
    Asc = pd.DataFrame([r for r in A_sc if r.get("applies") and r.get("parse_ok")])
    Asc = Asc[Asc.item_id.map(lambda k: lab.get(k) == "CORRECT")]
    rule_f = mrule("p_fused_H")
    for fam, g in Asc.groupby("family"):
        for m, fcol in (("fused", "fused_flag"), ("bow", "bow_flag"), ("l3", "l3_flag")):
            fr = g[fcol].astype(float).values > 0.5
            fb = g["orig"].map(lambda o: o.get(fcol)).astype(float).values > 0.5
            r = {"experiment": "A", "family": fam, "metric": m, "n": len(g), "threshold": "shipped", "base_fa(REPRINT)": fb.mean(),
                 "rewrite_fa": fr.mean(), "flip_rate": (fr != fb).mean()}
            rows.append(r)
        pr = su.flag_prob(g.p_fused_H.astype(float).values, rule_f)
        pb = su.flag_prob(g["orig"].map(lambda o: o.get("p_fused_H")).astype(float).values, rule_f)
        rows.append({"experiment": "A", "family": fam, "metric": "fused", "n": len(g), "threshold": "matched_FA0.10(R_SOLVER_CONS)",
                     "base_fa(REPRINT)": pb.mean(), "rewrite_fa": pr.mean(), "flip_rate": float(np.mean(np.abs(pr - pb)))})
    # D: judges orig/disg
    labD = df.lab_D.to_dict()
    for fam in sorted({r["family"] for r in D_set}):
        g = [r for r in D_set if r["family"] == fam and labD.get(r["base_item_id"]) == "CORRECT"]
        for m in ("judge_cheap_orig", "judge_cheap_disg", "judge_cheap2_orig", "judge_cheap2_disg"):
            pairs = [(D_sc[r["rw_id"]]["oriented_scores"].get(m), df.loc[r["base_item_id"], m]) for r in g if r["rw_id"] in D_sc]
            pairs = [(a, b) for a, b in pairs if a is not None and b is not None and not np.isnan(b)]
            if not pairs:
                continue
            a = np.array([p[0] for p in pairs], float)
            b = np.array([p[1] for p in pairs], float)
            rows.append({"experiment": "D", "family": fam, "metric": m, "n": len(pairs), "threshold": "shipped(0.5)",
                         "base_fa(REPRINT)": (b > thr[m]).mean(), "rewrite_fa": (a > thr[m]).mean(), "flip_rate": ((a > thr[m]) != (b > thr[m])).mean()})
            rl = mrule(m)
            pa, pb = su.flag_prob(a, rl), su.flag_prob(b, rl)
            rows.append({"experiment": "D", "family": fam, "metric": m, "n": len(pairs), "threshold": "matched_FA0.10(R_SOLVER_CONS)",
                         "base_fa(REPRINT)": pb.mean(), "rewrite_fa": pa.mean(), "flip_rate": float(np.mean(np.abs(pa - pb)))})
    # C: c_score = 1 - eq_frac_full
    labC = df.lab_C.to_dict()
    rwc = pd.DataFrame([r for r in C_set if str(r.get("applicable")) == "True" and r.get("reparse_ok") in (True, "True")])
    rwc = rwc[rwc.item_id.map(lambda k: labC.get(k) == "CORRECT") & rwc.eq_frac_full.notna()]
    rule_c = mrule("c_score")
    for fam, g in rwc.groupby("family"):
        fr, fb = g.flag.astype(bool).values, g.base_flag.astype(bool).values
        rows.append({"experiment": "C", "family": fam, "metric": "c_score(flag_medoid)", "n": len(g), "threshold": "shipped",
                     "base_fa(REPRINT)": fb.mean(), "rewrite_fa": fr.mean(), "flip_rate": (fr != fb).mean()})
        pa = su.flag_prob(1 - g.eq_frac_full.astype(float).values, rule_c)
        pb = su.flag_prob(1 - g.base_eq_frac_full.astype(float).values, rule_c)
        rows.append({"experiment": "C", "family": fam, "metric": "c_score", "n": len(g), "threshold": "matched_FA0.10(R_SOLVER_CONS)",
                     "base_fa(REPRINT)": pb.mean(), "rewrite_fa": pa.mean(), "flip_rate": float(np.mean(np.abs(pa - pb)))})
    I = pd.DataFrame(rows)
    ov = O.set_index("family")
    I["SAME_REWRITE_SET_as_other_experiments"] = I.family.map(lambda f: ", ".join(f"{k[-2:]}={ov.loc[f, k]}" for k in ov.columns if k.startswith("SAME_REWRITE_SET")) if f in ov.index else "NA")
    out_tab(I, "invariance_crosscheck.csv", "per-family rewrite FA on CORRECT bases, each experiment's own rewrite set and labels; SAME_REWRITE_SET from invariance_set_overlap.csv")
    # paired McNemar where >= 30 identical rewrites exist between A and D in a family
    mc = []
    for fam in fams:
        ids = [i for (i, f) in sets["A"] if f == fam and (i, f) in sets["D"] and sets["A"][(i, f)] == sets["D"][(i, f)] and labD.get(i) == "CORRECT"]
        if len(ids) < 30:
            mc.append({"family": fam, "n_identical_A_D_on_CORRECT": len(ids), "test": "not run (<30 identical rewrites)"})
            continue
        amap = {(r["item_id"], r["family"]): r for r in A_sc}
        dmap = {(r["base_item_id"], r["family"]): r for r in D_set}
        f1, f2 = [], []
        for i in ids:
            ra, rd = amap.get((i, fam)), dmap.get((i, fam))
            if ra is None or rd is None or rd["rw_id"] not in D_sc:
                continue
            j = D_sc[rd["rw_id"]]["oriented_scores"].get("judge_cheap_disg")
            if j is None or ra.get("fused_flag") is None:
                continue
            f1.append(bool(ra["fused_flag"]))
            f2.append(j > 0.5)
        f1, f2 = np.array(f1), np.array(f2)
        b_, c_ = int((f1 & ~f2).sum()), int((~f1 & f2).sum())
        p = sps.binomtest(b_, b_ + c_, 0.5).pvalue if b_ + c_ else 1.0
        mc.append({"family": fam, "n_identical_A_D_on_CORRECT": len(f1), "fa_fused": float(f1.mean()), "fa_judge_cheap_disg": float(f2.mean()),
                   "discordant_fused_only": b_, "discordant_judge_only": c_, "mcnemar_exact_p": float(p)})
    out_tab(pd.DataFrame(mc), "invariance_paired_mcnemar.csv", "identical rewrites shared by exp A and exp D (CORRECT bases): fused_flag vs judge_cheap_disg")
    statement = ("Iteration-1 invariance comparisons across experiments (A fused FA 0.275 on CONTRAPOSITIVE, D judge FA on contrapositive/"
                 "De Morgan/rename, C RENAME 96%) were computed on DIFFERENT rewrite sets: see invariance_set_overlap.csv for the families "
                 "where the rewritten strings coincide; all other cross-experiment FA comparisons are NOT_SAME_SET (descriptive only).")
    return {"overlap": O, "paired_mcnemar": mc, "statement": statement}


# ================================================================================================= STEP 11
def step11_candidate_B() -> dict:
    ga2 = GA / "gen_art_experiment_2"
    gp2 = IT1 / "gen_plan" / "gen_plan_experiment_2"
    res = {"gen_art_experiment_2_exists": ga2.exists(), "gen_art_experiment_2_files": [], "plan_dir_exists": gp2.exists()}
    if ga2.exists():
        res["gen_art_experiment_2_subdirs"] = sorted(str(Path(r, d).relative_to(ga2)) for r, ds, _ in os.walk(ga2) for d in ds)
        res["sibling_workspace_mtimes"] = {p.name: __import__("datetime").datetime.fromtimestamp(p.stat().st_mtime).isoformat()
                                           for p in sorted(GA.iterdir()) if p.is_dir()}
        for root, dirs, files in os.walk(ga2):
            for f in files:
                res["gen_art_experiment_2_files"].append(str(Path(root, f).relative_to(ga2)))
    if gp2.exists():
        res["plan_dir_files"] = sorted(str(Path(r, f).relative_to(gp2)) for r, _, fs in os.walk(gp2) for f in fs)
        so = gp2 / ".terminal_claude_agent_struct_out.json"
        if so.exists():
            try:
                j = json.loads(so.read_text())
                flat = json.dumps(j)
                res["plan_title"] = re.search(r'"title":\s*"([^"]+)"', flat).group(1) if re.search(r'"title":\s*"([^"]+)"', flat) else None
                res["plan_compute_profile"] = re.search(r'"runpod_compute_profile":\s*"([^"]+)"', flat).group(1) if re.search(r'"runpod_compute_profile":\s*"([^"]+)"', flat) else None
                res["plan_id"] = re.search(r'"id":\s*"([^"]+)"', flat).group(1) if re.search(r'"id":\s*"([^"]+)"', flat) else None
            except (json.JSONDecodeError, AttributeError) as ex:
                res["plan_parse_error"] = str(ex)
        me = gp2 / ".aii" / "module_end.json"
        if me.exists():
            res["plan_module_end"] = json.loads(me.read_text())
    # grep orchestration + iter_1 for mentions
    hits = []
    roots = [IT1, RUN]
    seen = set()
    for root in roots:
        depth_limit = 6 if root == IT1 else 1
        for r, dirs, files in os.walk(root):
            if Path(r).relative_to(root).parts.__len__() >= depth_limit:
                dirs[:] = []
            dirs[:] = [d for d in dirs if d not in (".venv", "hf_cache", ".shared_cache", "node_modules", "__pycache__", "cache", "data_local", "peer_raw")]
            for f in files:
                p = Path(r, f)
                if p in seen or not re.search(r"\.(json|md|log|ptylog|yaml|txt)$", f):
                    continue
                seen.add(p)
                try:
                    if p.stat().st_size > 50e6:
                        continue
                    with open(p, errors="ignore") as fh:
                        for i, line in enumerate(fh, 1):
                            if "gen_art_experiment_2" in line or "experiment_2" in line:
                                clean = re.sub(r"\x1b\[[0-9;?]*[A-Za-z]", "", line).strip()
                                hits.append({"path": str(p), "line": i, "text": clean[:240]})
                                if len([h for h in hits if h["path"] == str(p)]) >= 5:
                                    break
                except OSError:
                    continue
    res["n_grep_hits"] = len(hits)
    res["grep_hits_sample"] = hits[:60]
    res["files_produced"] = len(res["gen_art_experiment_2_files"])
    res["dir_mtime"] = (__import__("datetime").datetime.fromtimestamp(ga2.stat().st_mtime).isoformat() if ga2.exists() else None)
    # an executor that starts always writes .repl_agent.ptylog (every sibling gen_art_* has one); an empty dir means it never ran
    res["planned"] = bool(res["plan_dir_exists"] and (res.get("plan_module_end") or {}).get("passed"))
    res["launched"] = res["files_produced"] > 0
    orch = [h for h in hits if "review_report" not in h["path"] and "upd_hypo" not in h["path"] and "gen_report_text" not in h["path"]]
    res["n_hits_outside_reviewer_and_updhypo_logs"] = len(orch)
    res["last_logged_status"] = orch[-1] if orch else "no orchestration/executor log mentions gen_art_experiment_2; every hit is a later reviewer/upd_hypo agent listing the empty directory"
    if not res["gen_art_experiment_2_exists"]:
        res["finding"] = "planned (gen_plan_experiment_2 passed module_end) but gen_art_experiment_2 was never created: the executor was not launched"
    elif res["files_produced"] == 0:
        res["finding"] = ("planned (gen_plan_experiment_2: 'Checking logic by reading it back and testing worlds', gpu_basic, module_end passed) "
                          "but gen_art_experiment_2 holds only an EMPTY .aii/ directory created with the other workspaces (no .repl_agent.ptylog, "
                          "no .aii/module_end.json, no outputs): "
                          "the executor never started (or its whole workspace was wiped); Candidate B produced no evidence in iteration 1")
    else:
        res["finding"] = f"planned; gen_art_experiment_2 holds {res['files_produced']} files (see listing)"
    logger.info(f"step11: {res['finding']}")
    return res


# ================================================================================================= STEP 12
def step12_inventory(out_tab) -> dict:
    files = [EXP_A / "src/fol_triage.py", EXP_C / "src/consensus.py", EXP_C / "src/repair_census.py", EXP_A / "src/repair_census.py",
             EXP_D / "src/labeller/repair_census.py"]
    rows = []
    for f in files:
        if not f.exists():
            rows.append({"file": str(f), "function": None, "note": "FILE MISSING"})
            continue
        tree = ast.parse(f.read_text())
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and not node.name.startswith("_"):
                args = [a.arg for a in node.args.args]
                doc = ast.get_docstring(node) or ""
                first = re.split(r"(?<=\.)\s", doc.strip())[0] if doc else ""
                takes_tf = ("text" in args and any(a in args for a in ("fol", "cand", "candidate", "formula", "candidate_fol")))
                n_lines = (node.end_lineno or node.lineno) - node.lineno + 1
                returns = sorted({type(n.value).__name__ for n in ast.walk(node) if isinstance(n, ast.Return) and n.value is not None})
                own = None
                if not doc or len(first) < 25:
                    own = (f"[written from code] {node.name}({', '.join(args)}): {n_lines}-line function returning "
                           f"{'/'.join(returns) or 'None'}; docstring missing or too short -> FLAGGED")
                rows.append({"file": str(f.relative_to(GA)), "function": node.name, "signature": f"{node.name}({', '.join(args)})",
                             "has_docstring": bool(doc), "docstring_first_sentence": first[:200], "takes_text_fol": takes_tf,
                             "own_definition_if_missing": own, "flag_vague_or_missing": own is not None, "lineno": node.lineno})
    FI = pd.DataFrame(rows)
    out_tab(FI, "function_inventory.csv", "ast parse of iteration-1 released source files (no import)")
    shas = {str(f.relative_to(GA)): su_sha(f) for f in files if "repair_census" in f.name and f.exists()}
    dup = {"repair_census_sha256": shas, "n_distinct_versions": len(set(shas.values())),
           "note": "copies differ" if len(set(shas.values())) > 1 else "all copies identical"}
    # coverage vs request
    req = [
        ("item-level correlation with correctness", "this artifact tables/common_items_*.csv; exp A/C/D analysis", "ANSWERED", "screen only; long sentences untestable"),
        ("system-level correlation", "exp C summary.system_level (9 systems) + tables/mustfix_C.csv (NEW bootstrap CI, Kendall)", "PARTIAL", "<10 systems: descriptive, CI very wide"),
        ("per-error-type sensitivity", "tables/p1_crossover_*.csv (matched FA), exp D per_type", "SCREEN_ONLY", "many cells <15 errors (UNINFORMATIVE)"),
        ("invariance (renaming, reordering, equivalent restatement)", "tables/invariance_crosscheck.csv, invariance_set_overlap.csv", "PARTIAL", "rewrite sets differ across experiments; RENAME FA 96% (C), fused FA 0.275 (A)"),
        ("coverage with unparseables counted", "common_items_L_UNPARSEABLE_AS_ERROR.csv; exp A/C/D coverage blocks", "ANSWERED", ""),
        ("cost", "tables/mustfix_D.csv cost rows; exp A cost; exp C cost", "ANSWERED", ""),
        ("baselines: parse rate, round-trip, judge, SC, pilot structural", "common_items tables (parse_fail, rt_*, judge_*, sc5_cheap, pilot_*)", "ANSWERED", "SC only in cheap-model form on all items"),
        ("complexity curves (words, quantifiers, depth, conditions, exceptions)", "tables/complexity_*.csv, exp D complexity", "SCREEN_ONLY", "long/conditioned strata untestable on the screen; dataset E held-out needed"),
        ("contamination", "tables/contamination.csv (DiD + MDE)", "PARTIAL", "null DiD with MDE > 0.05 for most judges"),
        ("gold-error rate", "dataset E card section 4 (transcribed), exp D label_quality", "PARTIAL", "panel is strict (accepts 0.613 of expert-corrected formulas)"),
        ("correct-but-not-equivalent rate", "dataset E card section 5 (transcribed)", "PARTIAL", "panel-dependent"),
        ("error-type identification", "exp C operator_agreement (81% vs 46% chance); exp A error_type_readout", "PARTIAL", "labeller-dependent; screen only"),
        ("reusable (text, fol) functions with docstrings", "tables/function_inventory.csv", "PARTIAL", "several functions lack docstrings / do not take (text, fol)"),
        ("dataset with labels", "dataset E full_data_out.json (held-out) + screen labels", "ANSWERED", "held-out labels not analysed here (firewall)"),
        ("negative results", "L1 0.508, L2-role 0.557, pilot structural 0.50-0.53, rt_reformalise_eq 0.513 (common_items tables)", "ANSWERED", ""),
        ("Candidate B (template NLI + z3 distinguishing worlds)", "eval_out.json candidate_B", "MISSING", "never executed in iteration 1"),
    ]
    CV = pd.DataFrame(req, columns=["requirement", "where_answered", "status", "gap"])
    out_tab(CV, "coverage_vs_request.csv", "user request requirements vs iteration-1 artifacts + this evaluation")
    return {"function_inventory_summary": {"n_functions": len(FI), "n_with_docstring": int(FI.has_docstring.sum()) if len(FI) else 0,
                                           "n_take_text_fol": int(FI.takes_text_fol.sum()) if len(FI) else 0,
                                           "n_flagged": int(FI.flag_vague_or_missing.sum()) if len(FI) else 0},
            "repair_census_copies": dup, "coverage_vs_request": CV}


def su_sha(p: Path) -> str:
    import hashlib
    return hashlib.sha256(p.read_bytes()).hexdigest()


# ================================================================================================= STEP 13
def _bins(col, v):
    if np.isnan(v):
        return None
    if col == "words":
        return "<12" if v < 12 else ("12-19" if v < 20 else ">=20")
    if col == "n_quant":
        return "0-1" if v <= 1 else ("2" if v == 2 else ">=3")
    if col == "depth":
        return "0-1" if v <= 1 else ("2-3" if v <= 3 else ">=4")
    if col == "n_conditions":
        return "0" if v == 0 else ("1-2" if v <= 2 else ">=3")
    if col == "exception":
        return "yes" if v else "no"
    return None


def step13_complexity(df, commons, out_tab, metrics) -> dict:
    rows, grows = [], []
    for rn in ("R_SOLVER_CONS", "R_ADJ_AB"):
        sub, y = commons[rn]
        for col in ("words", "n_quant", "depth", "n_conditions", "exception"):
            b = sub[col].map(lambda v: _bins(col, v))
            for bv in sorted(b.dropna().unique()):
                mask = (b == bv).values
                ne, nc = int(y[mask].sum()), int((1 - y[mask]).sum())
                for m in metrics:
                    if m not in sub.columns:
                        continue
                    a = su.auroc(y[mask], sub[m].values[mask]) if ne and nc else None
                    rows.append({"regime": rn, "stratum": col, "bin": bv, "n_err": ne, "n_correct": nc, "metric": sc.nice(m), "auroc": a,
                                 "descriptive_only": not (ne >= 50 and nc >= 50)})
        # GEE interaction y ~ z(score) * z(words), exchangeable within sentence
        ok = sub.words.notna().values
        for m in metrics:
            if m not in sub.columns:
                continue
            s = sub[m].values[ok].astype(float)
            w = sub.words.values[ok].astype(float)
            if np.std(s) == 0:
                continue
            zs, zw = (s - s.mean()) / s.std(), (w - w.mean()) / w.std()
            X = smapi.add_constant(np.column_stack([zs, zw, zs * zw]))
            groups = pd.factorize(sub.cluster.values[ok])[0]
            try:
                gee = smapi.GEE(y[ok], X, groups=groups, family=smapi.families.Binomial(), cov_struct=smapi.cov_struct.Exchangeable()).fit()
                grows.append({"regime": rn, "metric": sc.nice(m), "n": int(ok.sum()), "coef_score": float(gee.params[1]), "coef_words": float(gee.params[2]),
                              "coef_interaction": float(gee.params[3]), "se_interaction": float(gee.bse[3]), "p_interaction": float(gee.pvalues[3])})
            except (np.linalg.LinAlgError, ValueError) as ex:
                logger.warning(f"GEE failed {rn} {m}: {ex}")
    CT = pd.DataFrame(rows)
    out_tab(CT, "complexity_bins.csv", "binned AUROC by complexity stratum on the common sets of R_SOLVER_CONS and R_ADJ_AB (bins <50/50 descriptive)")
    G = pd.DataFrame(grows)
    out_tab(G, "complexity_gee.csv", "GEE logistic y ~ z(score)*z(words), exchangeable within sentence; interaction = screen preview of P3")
    sC = json.loads((EXP_C / "results/summary.json").read_text())
    ref = sC.get("complexity", {}).get("logistic_score_x_words", {})
    # exact reproduction of exp C's definition: plain logistic y ~ score(raw) + z(words) + score(raw) x z(words), C's own labels
    L = df[(df.track == "L") & df.lab_C.isin(BIN) & df.c_score.notna() & df.words.notna()]
    yC = (L.lab_C == "ERROR").astype(int).values
    wz = (L.words.values - L.words.values.mean()) / L.words.values.std()
    repro = {}
    for m in ("c_score", "sc5_cheap", "judge_cheap_disg", "bow_uncarried", "l3_score", "p_fused_H"):
        ok = L[m].notna().values
        s_ = L[m].values[ok].astype(float)
        X = smapi.add_constant(np.column_stack([s_, wz[ok], s_ * wz[ok]]))
        try:
            fit = smapi.Logit(yC[ok], X).fit(disp=0)
            repro[m] = {"n": int(ok.sum()), "coef_score": float(fit.params[1]), "coef_words_z": float(fit.params[2]),
                        "coef_score_x_words": float(fit.params[3]), "p": float(fit.pvalues[3]),
                        "reported": (ref.get(m) or {}).get("coef_score_x_words")}
        except (np.linalg.LinAlgError, ValueError) as ex:
            logger.warning(f"C-definition logistic failed for {m}: {ex}")
    return {"gee": G, "reference_values_C_summary_complexity_logistic_score_x_words": ref,
            "reproduction_C_definition_own_labels": repro,
            "definition_note": ("iteration-1 c_score -0.94/SD = exp C summary.complexity.logistic_score_x_words (plain logistic, RAW score x "
                                "z(words), C's own labels, n=546) -- reproduced in reproduction_C_definition_own_labels. The 'judge -0.48/SD' "
                                "figure named in the plan was not found in any iteration-1 artifact (grep of exp D README/summary/analysis); "
                                "the judge row here uses exp C's definition on C's labels instead. complexity_gee.csv uses a different, "
                                "sentence-clustered GEE with BOTH score and words standardised, on each regime's common set.")}


# ================================================================================================= driver
def run_all(OUT, df, raw, regimes, commons, metrics_by_regime, decl, out_tab, B=2000, ws=None, quick=False):
    OUT["mustfix"] = step8_mustfix(df, out_tab)
    OUT["judge_matched_fa_and_contamination"] = step9_judges(df, regimes, out_tab, B=B)
    OUT["invariance_crosscheck"] = step10_invariance(df, commons, out_tab)
    OUT["candidate_B"] = step11_candidate_B()
    OUT["coverage_and_inventory"] = step12_inventory(out_tab)
    OUT["complexity"] = step13_complexity(df, commons, out_tab, ["p_fused_H", "bow_uncarried", "l3_score", "c_score", "judge_cheap_disg",
                                                                 "sc5_cheap", "rt_nli_min", "PT_oof", "PTJ_oof"])
