"""Analysis driver: joins all per-item scores to the frozen labels, computes every table and writes
results/analysis.json, results/tables/*.csv, results/method_out.json, results/judge_label_disagreements.csv, summary.md."""
from __future__ import annotations

import csv
import json
import math
from collections import Counter, defaultdict

import numpy as np
from loguru import logger

from .analysis import (METRICS, NA, FAIL, ClusterBoot, assemble, at_threshold, auc_w, boot_auc, ci, combo_oof, delong,
                       evaluate_set, fill, thresholds)
from .common import DATA, RES, ROOT, TAB, jdump, jload, norm, read_jsonl

from .analysis import SUBSET_METRICS
MAIN_METRICS = [m for m in METRICS if m not in SUBSET_METRICS]
CENSUS_OPS = ["NEG", "REV", "QUANT", "RESTR", "CONN", "MOVE", "DROP", "ADD", "SWAP", "BIND", "SCOPE", "UNGLUE"]


def _load(name):
    p = RES / "scores" / f"{name}.jsonl"
    return {r["key"]: r for r in read_jsonl(p)} if p.exists() else {}


def _clean(o):
    if isinstance(o, dict):
        return {str(k): _clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_clean(v) for v in o]
    if isinstance(o, (np.floating, float)):
        return None if (isinstance(o, float) and (math.isnan(o) or math.isinf(o))) or (isinstance(o, np.floating) and np.isnan(o)) else float(o)
    if isinstance(o, np.integer):
        return int(o)
    if isinstance(o, np.bool_):
        return bool(o)
    return o


def write_csv(path, rows: list[dict]):
    if not rows:
        path.write_text("")
        return
    cols = list(dict.fromkeys(c for r in rows for c in r))
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({c: (json.dumps(v) if isinstance(v, (list, dict)) else v) for c, v in r.items()})


def fmt(a, c=None):
    if a is None:
        return "—"
    return f"{a:.3f}" + (f" [{c[0]:.3f}, {c[1]:.3f}]" if c and c[0] is not None else "")


def run(prereg: dict, costs_api: list[dict]) -> dict:
    items = jload(DATA / "screen_items.json")
    rws = jload(DATA / "invariance_items.json")
    dmap = jload(DATA / "disguise_map.json")
    pdv = jload(RES / "promptdev_local.json")
    dev_ids = set(pdv["dev_slice_ids"])
    byid = {r["item_id"]: r for r in items}
    rwby = {r["rw_id"]: r for r in rws}
    pilot, rt_llm, rt_nli, rt_eq = _load("pilot"), _load("roundtrip_llm"), _load("roundtrip_nli"), _load("rt_equiv")
    j1, j2, j3 = _load("judge_cheap"), _load("judge_cheap2"), _load("judge_strong")
    recall = _load("recall_probe")
    local = {"judge_local_qwen8b": _load("judge_local_qwen8b"), "judge_local_llama8b": _load("judge_local_llama8b"),
             "judge_local_qwen14b": _load("judge_local_qwen14b"), "rt_nli_local": _load("roundtrip_nli_local"),
             "rt_eq_local": _load("rt_equiv_local")}
    recall_local = _load("recall_probe_local")
    keys_all = [r["item_id"] for r in items] + [r["rw_id"] for r in rws]
    track_of = lambda k: byid[k]["track"] if k in byid else rwby[k]["track"]  # rewrites inherit the base item's track
    sub_of = lambda k: byid[k].get("sub_source") if k in byid else None
    rows = assemble(keys_all, pilot, rt_llm, rt_nli, rt_eq, j1, j2, j3, track_of, sub_of, local=local)
    # table: metric -> key -> value ; cluster ; max
    table = {m: {k: rows[k][m] for k in keys_all} for m in METRICS}
    table["_cluster"] = {k: norm(byid[k]["text"]) if k in byid else norm(rwby[k]["text"]) for k in keys_all}
    table["_max"] = {}
    for m in METRICS:
        vals = [v for v in table[m].values() if v not in (NA, FAIL)]
        table["_max"][m] = max(vals) if vals else 1.0
        if METRICS[m][1] in ("prob", "bin", "cont", "cont_L") and table["_max"][m] < 1.0 and m != "pilot_dangling":
            table["_max"][m] = max(table["_max"][m], 1.0)
    # thresholds from track-H CORRECT (dev slice excluded)
    href = [r["item_id"] for r in items if r["track"] == "H" and r["label"] == "CORRECT" and r["item_id"] not in dev_ids]
    sc_h, msk_h = {}, {}
    for m in METRICS:
        s, app, _ = fill([table[m][k] for k in href], table["_max"][m])
        sc_h[m], msk_h[m] = s, app
    thr = thresholds(sc_h, msk_h)
    A = {"thresholds": thr, "metric_definitions": {m: d for m, (d, _) in METRICS.items()}}

    # ------------------------------------------------------------------ evaluation sets
    L = [r for r in items if r["track"] == "L"]
    H = [r for r in items if r["track"] == "H" and r["item_id"] not in dev_ids]
    sets = {
        "L_primary": [(r["item_id"], 1 if r["label"] == "ERROR" else 0) for r in L if r["label"] in ("CORRECT", "ERROR")],
        "L_borderline_to_uncertain": [(r["item_id"], 1 if r["label"] == "ERROR" else 0) for r in L
                                      if r["label"] in ("CORRECT", "ERROR") and not r["vocab_borderline"]],
        "L_pessimistic_err_or_uncertain": [(r["item_id"], 0 if r["label"] == "CORRECT" else 1) for r in L
                                           if r["label"] in ("CORRECT", "ERROR", "UNCERTAIN")],
        "L_exclude_subst_only": [(r["item_id"], 1 if r["label"] == "ERROR" else 0) for r in L
                                 if r["label"] in ("CORRECT", "ERROR") and not r["subst_only"]],
        "L_unparseable_as_error": [(r["item_id"], 0 if r["label"] == "CORRECT" else 1) for r in L
                                   if r["label"] in ("CORRECT", "ERROR", "UNPARSEABLE")],
        "H_primary": [(r["item_id"], 1 if r["label"] == "ERROR" else 0) for r in H if r["label"] in ("CORRECT", "ERROR")],
        "H_curator_view": [(r["item_id"], 1 if r["label_h_curator"] == "ERROR" else 0) for r in H
                           if r["label_h_curator"] in ("CORRECT", "ERROR")],
        "H_dev_slice": [(r["item_id"], 1 if r["label"] == "ERROR" else 0) for r in items if r["item_id"] in dev_ids],
    }
    sub_ids = set(prereg["strong_subsample"]["L"]) | set(prereg["strong_subsample"]["H"])
    sets["L_strong_subset"] = [(k, y) for k, y in sets["L_primary"] if k in sub_ids]
    sets["H_strong_subset"] = [(k, y) for k, y in sets["H_curator_view"] if k in sub_ids]
    results, boots, cbs = {}, {}, {}
    for sname, ky in sets.items():
        keys = [k for k, _ in ky]
        y = np.array([v for _, v in ky])
        mets = list(METRICS)
        res, cb, bt = evaluate_set(sname, keys, y, table, thr, mets)
        results[sname] = {"n": len(keys), "n_pos": int(y.sum()), "n_neg": int((1 - y).sum()), "metrics": res}
        boots[sname], cbs[sname] = bt, cb
        logger.info(f"set {sname}: n={len(keys)} pos={int(y.sum())}")
    A["sets"] = results
    rows_csv = []
    for sname, R in results.items():
        for m, r in R["metrics"].items():
            rows_csv.append({"set": sname, "metric": m, **{k: v for k, v in r.items()}})
    write_csv(TAB / "auroc_all_sets.csv", rows_csv)

    # ------------------------------------------------------------------ paired deltas vs judge_cheap_disg (+ DeLong)
    def paired(sname, ref="judge_cheap_disg", others=None):
        ky = sets[sname]
        keys = [k for k, _ in ky]
        y = np.array([v for _, v in ky])
        bt = boots[sname]
        out = {}
        s_ref, a_ref, _ = fill([table[ref][k] for k in keys], table["_max"][ref])
        for m in (others or bt):
            if m == ref or m not in bt or ref not in bt:
                continue
            d = bt[m] - bt[ref]
            s_m, a_m, _ = fill([table[m][k] for k in keys], table["_max"][m])
            both = a_ref & a_m
            dl = delong(y[both], s_m[both], s_ref[both]) if both.sum() > 10 else None
            out[m] = {"delta_auroc": results[sname]["metrics"][m]["auroc"] - results[sname]["metrics"][ref]["auroc"],
                      "ci": ci(d), "p_boot_le0": float(np.mean(d[~np.isnan(d)] <= 0)) if np.any(~np.isnan(d)) else None,
                      "delong": None if dl is None else {"auc_m": dl[0], "auc_ref": dl[1], "z": dl[2], "p": dl[3]},
                      "note": "metric applicable only on a subset" if both.sum() < len(keys) else ""}
        return out
    A["paired_vs_judge_cheap_disg"] = {s: paired(s) for s in ("L_primary", "H_primary", "H_curator_view", "L_exclude_subst_only")}
    A["paired_strong_subset"] = {s: {ref: paired(s, ref=ref, others=["judge_strong_orig", "judge_strong_disg"])
                                     for ref in ("judge_cheap_orig", "judge_cheap_disg")} for s in ("L_strong_subset", "H_strong_subset")}

    # ------------------------------------------------------------------ contamination
    cont = {}
    for judge in ("judge_cheap", "judge_cheap2", "judge_strong", "judge_local_qwen8b", "judge_local_llama8b", "judge_local_qwen14b"):
        cj = {}
        subset_j = judge in ("judge_strong", "judge_local_qwen14b")
        for sname in (("L_primary", "H_primary", "H_curator_view") if not subset_j else ("L_strong_subset", "H_strong_subset")):
            bt = boots[sname]
            o, d = f"{judge}_orig", f"{judge}_disg"
            if o not in bt or d not in bt:
                continue
            delta = bt[d] - bt[o]
            cj[sname] = {"auroc_orig": results[sname]["metrics"][o]["auroc"], "auroc_disg": results[sname]["metrics"][d]["auroc"],
                         "delta_disg_minus_orig": results[sname]["metrics"][d]["auroc"] - results[sname]["metrics"][o]["auroc"],
                         "ci": ci(delta), "_boot": delta}
        # DiD: Δ(H) - Δ(L), tracks resampled independently (different cluster draws)
        pairs = [("H_primary", "L_primary"), ("H_curator_view", "L_primary")] if not subset_j else [("H_strong_subset", "L_strong_subset")]
        for h, l in pairs:
            if h in cj and l in cj:
                did = cj[h]["_boot"] - cj[l]["_boot"]
                cj[f"DiD_{h}_minus_{l}"] = {"did": cj[h]["delta_disg_minus_orig"] - cj[l]["delta_disg_minus_orig"], "ci": ci(did),
                                            "contamination_evidence": bool(ci(did)[1] is not None and ci(did)[1] < 0)}
        # mean P(faithful) shift on ERROR items (memorised public gold should push ORIGINAL scores up)
        for tname, ids in (("H_ERROR_curator", [r["item_id"] for r in H if r["label_h_curator"] == "ERROR"]),
                           ("H_CORRECT", [r["item_id"] for r in H if r["label"] == "CORRECT"]),
                           ("L_ERROR", [r["item_id"] for r in L if r["label"] == "ERROR"]),
                           ("L_CORRECT", [r["item_id"] for r in L if r["label"] == "CORRECT"])):
            src = {"judge_cheap": j1, "judge_cheap2": j2, "judge_strong": j3, **{k: v for k, v in local.items() if k.startswith("judge_local")}}[judge]
            po = [src[f"{i}|orig"]["p"] for i in ids if f"{i}|orig" in src and f"{i}|disg" in src
                  and src[f"{i}|orig"].get("p") is not None and src[f"{i}|disg"].get("p") is not None]
            pd_ = [src[f"{i}|disg"]["p"] for i in ids if f"{i}|orig" in src and f"{i}|disg" in src
                   and src[f"{i}|orig"].get("p") is not None and src[f"{i}|disg"].get("p") is not None]
            if po:
                diff = np.array(po) - np.array(pd_)
                rng = np.random.default_rng(0)
                bs = [diff[rng.integers(0, len(diff), len(diff))].mean() for _ in range(2000)]
                cj[f"mean_pfaithful_orig_minus_disg_{tname}"] = {"n": len(po), "mean_orig": float(np.mean(po)),
                                                                 "mean_disg": float(np.mean(pd_)), "diff": float(diff.mean()),
                                                                 "ci": ci(np.array(bs))}
        for v in cj.values():
            if isinstance(v, dict):
                v.pop("_boot", None)
        cont[judge] = cj
    A["contamination"] = cont
    A["recall_probe"] = recall_probe_analysis(items, recall)
    A["recall_probe_local_qwen8b"] = recall_probe_analysis(items, recall_local, tag="_local") if recall_local else None

    # ------------------------------------------------------------------ best baseline combination (cross-fitted)
    fs = prereg["combination_feature_sets"]
    S1, S2, S3 = fs["S1_structural"], fs["S2_roundtrip"], fs["S3_judges"]
    feature_sets = {"S1_structural": S1, "S2_roundtrip": S2, "S3_judges_disg": S3,
                    "S4_all_cheap": S1 + S2 + S3 + ["judge_cheap_orig", "judge_cheap2_orig"],
                    "S6_exploratory_S4_plus_local": S1 + S2 + S3 + ["judge_cheap_orig", "judge_cheap2_orig", "judge_local_qwen8b_orig",
                                                                     "judge_local_qwen8b_disg", "judge_local_llama8b_orig",
                                                                     "judge_local_llama8b_disg", "rt_nli_min_localverb"]}
    combo = {}
    oof_out = {}
    folds_out = {}
    for tname in ("L_primary", "H_curator_view"):
        ky = sets[tname]
        keys = [k for k, _ in ky]
        y = np.array([v for _, v in ky])
        groups = [table["_cluster"][k] for k in keys]
        cb = cbs[tname]
        combo[tname] = {}
        fold_ref = None
        for fname, feats in feature_sets.items():
            feats_ok = [f for f in feats if any(table[f][k] != NA for k in keys)]
            oof, fold, cols = combo_oof(keys, y, groups, table, feats_ok, fold_of=fold_ref)
            if fold_ref is None:
                fold_ref = {k: int(f) for k, f in zip(keys, fold)}
            a = auc_w(y, oof)
            ba = boot_auc(y, oof, cb)
            combo[tname][fname] = {"features": feats_ok, "oof_auroc": float(a), "ci": ci(ba), "_boot": ba}
            if tname == "L_primary":
                for k, v in zip(keys, oof):
                    oof_out.setdefault(k, {})[f"baseline_combo_{fname}_oof"] = float(v)
        best = max(("S1_structural", "S2_roundtrip", "S3_judges_disg", "S4_all_cheap"), key=lambda f: combo[tname][f]["oof_auroc"])
        combo[tname]["best"] = {"set": best, "oof_auroc": combo[tname][best]["oof_auroc"], "ci": combo[tname][best]["ci"],
                                "note": "max over 4 pre-registered feature sets: mildly optimistic"}
        # best vs judge_cheap_disg paired
        bt = boots[tname]
        d = combo[tname][best]["_boot"] - bt["judge_cheap_disg"]
        combo[tname]["best_minus_judge_cheap_disg"] = {"delta": combo[tname][best]["oof_auroc"] - results[tname]["metrics"]["judge_cheap_disg"]["auroc"],
                                                       "ci": ci(d)}
        if tname == "L_primary":
            for k in keys:
                oof_out[k]["best_baseline_oof"] = oof_out[k][f"baseline_combo_{best}_oof"]
            folds_out = fold_ref
        # S5 on the strong subset (fold-split within the subset)
        sk = [k for k in keys if k in sub_ids]
        if len(sk) > 40:
            ys = np.array([dict(ky)[k] for k in sk])
            feats5 = feature_sets["S4_all_cheap"] + ["judge_strong_orig", "judge_strong_disg"]
            feats5 = [f for f in feats5 if any(table[f][k] != NA for k in sk)]
            oof5, _, _ = combo_oof(sk, ys, [table["_cluster"][k] for k in sk], table, feats5)
            oof4, _, _ = combo_oof(sk, ys, [table["_cluster"][k] for k in sk], table,
                                   [f for f in feature_sets["S4_all_cheap"] if any(table[f][k] != NA for k in sk)])
            combo[tname]["S5_strong_subset"] = {"n": len(sk), "oof_auroc_S5": float(auc_w(ys, oof5)),
                                                "oof_auroc_S4_same_items": float(auc_w(ys, oof4))}
        for f in feature_sets:
            combo[tname][f].pop("_boot", None)
    A["baseline_combination"] = combo
    jdump(folds_out, DATA / "folds.json")

    # ------------------------------------------------------------------ per-type sensitivity (track H curator + track L)
    A["per_type"] = per_type(items, H, L, table, thr, j1)

    # ------------------------------------------------------------------ invariance
    A["invariance"] = invariance(rws, table, thr)

    # ------------------------------------------------------------------ complexity strata
    A["complexity"] = complexity(items, sets, table, thr, j1)

    # ------------------------------------------------------------------ system level
    sysl = {}
    for s in sorted({r["system"] for r in L}):
        its = [r for r in L if r["system"] == s]
        ce = [r for r in its if r["label"] in ("CORRECT", "ERROR")]
        row = {"n": len(its), "label_dist": dict(Counter(r["label"] for r in its)),
               "true_error_rate_CE": sum(r["label"] == "ERROR" for r in ce) / max(1, len(ce)),
               "nonCORRECT_rate_all": sum(r["label"] != "CORRECT" for r in its) / len(its), "metrics": {}}
        for m in MAIN_METRICS:
            s_, app, fl = fill([table[m][r["item_id"]] for r in its], table["_max"][m])
            if app.sum() == 0:
                continue
            row["metrics"][m] = {"mean_score": float(np.nanmean(s_[app])), "flag_rate": float(np.mean(s_[app] > thr[m]))}
        sysl[s] = row
    A["system_level"] = {"per_system": sysl, "note": "3 systems only: descriptive, no rank-correlation test"}
    # rank agreement (descriptive)
    order_true = sorted(sysl, key=lambda s: sysl[s]["true_error_rate_CE"])
    A["system_level"]["true_error_order"] = order_true
    A["system_level"]["metric_order_matches"] = {m: [s for s in sorted(sysl, key=lambda s: sysl[s]["metrics"].get(m, {}).get("mean_score", 0))] == order_true
                                                 for m in MAIN_METRICS if all(m in sysl[s]["metrics"] for s in sysl)}

    # ------------------------------------------------------------------ coverage
    cov = {}
    for m in METRICS:
        per = {}
        for grp, its in (("L", L), ("H", [r for r in items if r["track"] == "H"]), ("RW", rws)):
            ks = [r["item_id"] if "item_id" in r and grp != "RW" else r["rw_id"] for r in its]
            vals = [table[m][k] for k in ks]
            app = [v for v in vals if v != NA]
            per[grp] = {"n_applicable": len(app), "n_fail": sum(v == FAIL for v in app),
                        "coverage": (1 - sum(v == FAIL for v in app) / len(app)) if app else None}
        for s in sorted({r["system"] for r in L}):
            vals = [table[m][r["item_id"]] for r in L if r["system"] == s]
            app = [v for v in vals if v != NA]
            per[f"L|{s}"] = {"coverage": (1 - sum(v == FAIL for v in app) / len(app)) if app else None, "n_fail": sum(v == FAIL for v in app)}
        cov[m] = per
    A["coverage"] = {"per_metric": cov,
                     "unparseable_per_system": {s: sum(1 for r in items if r["system"] == s and r["label"] == "UNPARSEABLE")
                                                for s in sorted({r["system"] for r in items})},
                     "label_dist_per_system": {s: dict(Counter(r["label"] for r in items if r["system"] == s))
                                               for s in sorted({r["system"] for r in items})},
                     "vocab_borderline": {t: sum(r["vocab_borderline"] for r in items if r["track"] == t) for t in ("L", "H")},
                     "subst_only_error": {t: sum(r["subst_only"] for r in items if r["track"] == t) for t in ("L", "H")}}
    write_csv(TAB / "coverage.csv", [{"metric": m, **{f"{g}_{k}": v for g, d in per.items() for k, v in d.items()}} for m, per in cov.items()])

    # ------------------------------------------------------------------ cost
    A["cost"] = cost_table(items, rws, pilot, rt_llm, rt_nli, j1, j2, j3, prereg, costs_api)

    # ------------------------------------------------------------------ diagnostics: joint-conflict within FOLIO answer strata; T7 gold round-trip
    diag = {}
    for sname in ("L_primary", "H_curator_view"):
        ky = [(k, y) for k, y in sets[sname] if byid[k]["role"] == "conclusion"]
        d = {}
        for ans in sorted({str(byid[k].get("folio_answer")) for k, _ in ky}):
            sub = [(k, y) for k, y in ky if str(byid[k].get("folio_answer")) == ans]
            y = np.array([t for _, t in sub])
            s, app, _ = fill([table["pilot_joint_conflict"][k] for k, _ in sub], table["_max"]["pilot_joint_conflict"])
            s = np.where(app, s, np.nan)
            d[ans] = {"n": len(sub), "n_pos": int(y.sum()), "auroc": None if len(set(y)) < 2 else float(auc_w(y, s)),
                      "flag_rate_correct": float(np.nanmean(s[y == 0] > 0.5)) if (y == 0).any() else None,
                      "flag_rate_error": float(np.nanmean(s[y == 1] > 0.5)) if (y == 1).any() else None}
        diag[f"pilot_joint_conflict_by_folio_answer_{sname}"] = d
    gold_ok = [r["item_id"] for r in items if r["track"] == "H" and r["auto_class"] == "EQUIV"]
    vals = [rt_eq.get(k, {}).get("rt_reformalise_eq") for k in gold_ok]
    diag["T7_gold_roundtrip_reformalise_equiv_rate"] = {"n": len(vals), "rate": float(np.mean([v == 1 for v in vals])) if vals else None,
                                                         "n_fail": sum(v is None for v in vals)}
    A["diagnostics"] = diag
    # label quality: how often is public gold wrong, how often is a candidate correct-but-not-equivalent
    Hall = [r for r in items if r["track"] == "H"]
    lq = {"track_H_original_gold_vs_corrected": {
              "n": len(Hall), "auto_class": dict(Counter(r["auto_class"] for r in Hall)),
              "label": dict(Counter(r["label"] for r in Hall)),
              "orig_gold_wrong_rate_(ERROR+UNCERTAIN+READING_CHOICE)/parseable": sum(r["label"] in ("ERROR", "UNCERTAIN", "READING_CHOICE") for r in Hall)
              / max(1, sum(r["label"] != "UNPARSEABLE" for r in Hall)),
              "orig_gold_unparseable_rate": sum(r["label"] == "UNPARSEABLE" for r in Hall) / len(Hall),
              "correct_but_not_equivalent_rate_(VOCAB/GRAN among non-EQUIV parseable)":
                  sum(r["auto_class"] in ("VOCAB", "GRAN") for r in Hall) / max(1, sum(r["auto_class"] not in ("EQUIV", "UNPARSEABLE") for r in Hall))},
          "track_L_logiclm": {
              "n": len(L), "auto_class": dict(Counter(r["auto_class"] for r in L)),
              "vocab_or_gran_share_of_CORRECT": sum(r["auto_class"] in ("VOCAB", "GRAN") for r in L if r["label"] == "CORRECT") / max(1, sum(r["label"] == "CORRECT" for r in L)),
              "vocab_borderline_share_of_CORRECT": sum(r["vocab_borderline"] for r in L if r["label"] == "CORRECT") / max(1, sum(r["label"] == "CORRECT" for r in L)),
              "subst_only_share_of_ERROR": sum(r["subst_only"] for r in L if r["label"] == "ERROR") / max(1, sum(r["label"] == "ERROR" for r in L)),
              "uncertain_share_of_parseable": sum(r["label"] == "UNCERTAIN" for r in L) / max(1, sum(r["label"] != "UNPARSEABLE" for r in L))},
          "note": ("subst_only ERROR = the only typed repair is ADD+DROP of an unaligned predicate, i.e. most likely a vocabulary "
                   "mismatch the aligner missed (correct-but-not-equivalent). The parallel run run_qY2a2IS-WLIs measured 43.9% "
                   "of solver-non-equivalent candidates judged faithful by a 3-family panel; iteration 2 re-scores with the "
                   "adjudicated labels of dataset artifact E.")}
    A["label_quality"] = lq

    # ------------------------------------------------------------------ disagreements export
    dis = []
    for r in L:
        if r["label"] not in ("CORRECT", "ERROR"):
            continue
        o = j1.get(f"{r['item_id']}|orig")
        if not o or o.get("p") is None:
            continue
        judge_faithful = o["p"] >= 0.5
        if (r["label"] == "ERROR" and judge_faithful) or (r["label"] == "CORRECT" and not judge_faithful):
            dis.append({"item_id": r["item_id"], "system": r["system"], "label": r["label"], "auto_class": r["auto_class"],
                        "repair_ops": r["repair_ops"], "subst_only": r["subst_only"], "judge_cheap_p_orig": o["p"],
                        "judge_cheap_type": o.get("type"), "judge_reason": o.get("reason"), "text": r["text"],
                        "candidate_fol": r["candidate_fol"], "reference_fol": r["reference_fol"]})
    write_csv(RES / "judge_label_disagreements.csv", dis)
    A["judge_label_disagreements"] = {"n": len(dis), "by_label": dict(Counter(d["label"] for d in dis)),
                                      "ERROR_judged_faithful_subst_only": sum(1 for d in dis if d["label"] == "ERROR" and d["subst_only"])}
    return _clean(A), rows, table, oof_out, folds_out


def eq_worker(args):
    """(key, formula, reference) -> (key, True | False | None): equivalence modulo vocabulary (no repair search)."""
    import sys as _s
    _s.setrecursionlimit(10000)
    from .labeller.labeller import equivalent_modulo_vocab
    key, f, ref = args
    try:
        c = equivalent_modulo_vocab(f, ref, do_search=False)["cls"]
    except Exception:  # noqa: BLE001
        return key, None
    return key, (True if c in ("EQUIV", "VOCAB", "GRAN") else (None if c in ("UNPARSEABLE", "REF_UNPARSEABLE") else False))


def recall_probe_analysis(items, recall, tag=""):
    """Gold-recall probe: does the model reproduce the PUBLIC original gold (names / logic) more than chance?"""
    import multiprocessing as mp
    from concurrent.futures import ProcessPoolExecutor
    from .labeller.fol import parse
    from .pilot_metrics import CAMEL
    H = [r for r in items if r["track"] == "H"]
    gpt4 = {}
    for r in items:
        if r["track"] == "L" and r["system"] == "gpt-4" and r["role"] == "conclusion":
            gpt4[norm(r["text"])] = r["candidate_fol"]

    def names(f):
        try:
            e = parse(f)
        except Exception:  # noqa: BLE001
            return None
        from .labeller.repair_census import symbols
        P, C = symbols(e)
        return {p[0].lower() for p in P}
    args, rows = [], []
    for r in H:
        rc = recall.get(r["item_id"])
        if not rc:
            continue
        f = rc.get("formula")
        n_p, n_o, n_c = names(f) if f else None, names(r["orig_gold"]), names(r["reference_fol"])
        g4 = gpt4.get(norm(r["text"]))
        n_g4 = names(g4) if g4 else None
        J = lambda a, b: (len(a & b) / max(1, len(a | b))) if (a is not None and b is not None) else None
        rows.append({"item_id": r["item_id"], "sub": r["sub_source"], "parsed": n_p is not None,
                     "J_probe_orig": J(n_p, n_o), "J_probe_corr": J(n_p, n_c), "J_probe_gpt4": J(n_p, n_g4),
                     "J_gpt4_orig": J(n_g4, n_o), "orig_eq_corr": r["auto_class"] == "EQUIV"})
        if f:
            args.append((r["item_id"] + "|orig", f, r["orig_gold"]))
            args.append((r["item_id"] + "|corr", f, r["reference_fol"]))
    with ProcessPoolExecutor(max_workers=6, mp_context=mp.get_context("spawn")) as pool:
        eqs = dict(pool.map(eq_worker, args, chunksize=4))
    out = {"n_items": len(rows), "parse_rate": float(np.mean([r["parsed"] for r in rows])) if rows else None}
    for sub in ("FOLIO-concl", "MALLS", "ALL"):
        rs = [r for r in rows if sub == "ALL" or r["sub"] == sub]
        d = {"n": len(rs)}
        for kname in ("J_probe_orig", "J_probe_corr", "J_probe_gpt4", "J_gpt4_orig"):
            v = [r[kname] for r in rs if r[kname] is not None]
            d[kname] = {"mean": float(np.mean(v)) if v else None, "n": len(v)}
        # non-equivalent (orig != corrected) items: equivalence of probe to orig vs corrected gold
        ne = [r for r in rs if not r["orig_eq_corr"]]
        eo = [eqs.get(r["item_id"] + "|orig") for r in ne]
        ec = [eqs.get(r["item_id"] + "|corr") for r in ne]
        d["noneq_items"] = len(ne)
        d["probe_equiv_to_ORIGINAL_gold_rate"] = float(np.mean([e is True for e in eo])) if ne else None
        d["probe_equiv_to_CORRECTED_gold_rate"] = float(np.mean([e is True for e in ec])) if ne else None
        allr = [eqs.get(r["item_id"] + "|orig") for r in rs]
        d["probe_equiv_to_original_gold_rate_all"] = float(np.mean([e is True for e in allr])) if rs else None
        # paired test J_probe_orig - J_probe_gpt4 on items with both
        pr = [(r["J_probe_orig"], r["J_probe_gpt4"]) for r in rs if r["J_probe_orig"] is not None and r["J_probe_gpt4"] is not None]
        if len(pr) > 5:
            diff = np.array([a - b for a, b in pr])
            rng = np.random.default_rng(0)
            bs = np.array([diff[rng.integers(0, len(diff), len(diff))].mean() for _ in range(2000)])
            d["J_probe_orig_minus_J_probe_gpt4"] = {"n": len(pr), "mean": float(diff.mean()), "ci": ci(bs)}
            pr2 = [(r["J_probe_orig"], r["J_gpt4_orig"]) for r in rs if r["J_probe_orig"] is not None and r["J_gpt4_orig"] is not None]
            diff2 = np.array([a - b for a, b in pr2])
            bs2 = np.array([diff2[rng.integers(0, len(diff2), len(diff2))].mean() for _ in range(2000)])
            d["J_probe_orig_minus_J_gpt4_orig"] = {"n": len(pr2), "mean": float(diff2.mean()), "ci": ci(bs2)}
        out[sub] = d
    write_csv(TAB / f"recall_probe_items{tag}.csv", rows)
    return out


def per_type(items, H, L, table, thr, j1):
    out = {}
    for tname, errs in (("H_curator_ERROR", [r for r in H if r["label_h_curator"] == "ERROR"]),
                        ("L_ERROR", [r for r in L if r["label"] == "ERROR"])):
        groups = defaultdict(list)
        for r in errs:
            if r["census_class"] == "COMPOUND":
                groups["COMPOUND"].append(r)
            elif r["repair_ops"]:
                for op in set(r["repair_ops"]):
                    groups[op].append(r)
                groups[f"{len(r['repair_ops'])}-op"].append(r)
        sens = {}
        for g, rs in sorted(groups.items()):
            sens[g] = {"n": len(rs)}
            for m in MAIN_METRICS:
                s, app, _ = fill([table[m][r["item_id"]] for r in rs], table["_max"][m])
                if app.sum():
                    sens[g][m] = float(np.mean(s[app] > thr[m]))
        # judge type-label accuracy
        conf = defaultdict(Counter)
        acc = {"1-op": [0, 0], "2-op": [0, 0]}
        for r in errs:
            if not r["repair_ops"]:
                continue
            o = j1.get(f"{r['item_id']}|orig")
            if not o or o.get("p") is None:
                continue
            t = o.get("type") or "NONE"
            d = f"{len(r['repair_ops'])}-op"
            if d in acc:
                acc[d][0] += int(t in r["repair_ops"])
                acc[d][1] += 1
            if len(r["repair_ops"]) == 1:
                conf[r["repair_ops"][0]][t] += 1
        out[tname] = {"sensitivity_at_threshold": sens,
                      "judge_cheap_type_accuracy": {k: {"correct": v[0], "n": v[1], "acc": v[0] / v[1] if v[1] else None} for k, v in acc.items()},
                      "judge_cheap_type_confusion_single_op": {k: dict(v) for k, v in conf.items()}}
        rows = [{"group": g, **v} for g, v in sens.items()]
        write_csv(TAB / f"per_type_{tname}.csv", rows)
    return out


def invariance(rws, table, thr):
    out = {}
    fams = sorted({r["family"] for r in rws})
    rows = []
    for m in MAIN_METRICS:
        per = {}
        for fam in fams + ["ALL_meaning_preserving"]:
            rs = [r for r in rws if (r["family"] == fam if fam != "ALL_meaning_preserving" else r["family"] != "REPRINT")]
            if not rs:
                continue
            s_rw, app_rw, _ = fill([table[m][r["rw_id"]] for r in rs], table["_max"][m])
            s_b, app_b, _ = fill([table[m][r["base_item_id"]] for r in rs], table["_max"][m])
            ok = app_rw & app_b
            if ok.sum() == 0:
                continue
            f_rw, f_b = s_rw[ok] > thr[m], s_b[ok] > thr[m]
            per[fam] = {"n": int(ok.sum()), "fa_rewrite": float(f_rw.mean()), "fa_base": float(f_b.mean()),
                        "flip_rate": float(np.mean(f_rw != f_b)), "mean_abs_delta": float(np.mean(np.abs(s_rw[ok] - s_b[ok])))}
            rows.append({"metric": m, "family": fam, **per[fam]})
        out[m] = per
    write_csv(TAB / "invariance.csv", rows)
    return {"per_metric": out, "family_counts": dict(Counter(r["family"] for r in rws)),
            "note": "bases = first 150 track-L CORRECT items by item_id; REPRINT = formatting-only control"}


def complexity(items, sets, table, thr, j1):
    import statsmodels.api as sm
    byid = {r["item_id"]: r for r in items}
    out = {}
    key_metrics = ["judge_cheap_orig", "judge_cheap_disg", "judge_cheap2_disg", "rt_nli_min", "rt_embed_cos",
                   "rt_reformalise_eq", "pilot_joint_conflict", "parse_fail"]
    rows = []
    for sname in ("L_primary", "H_curator_view"):
        ky = sets[sname]
        d = {}
        for dim in ("words_bin", "n_quant_bin", "depth_bin", "n_cond_bin", "exception"):
            vals = sorted({str(byid[k]["strata"][dim]) for k, _ in ky})
            for v in vals:
                sub = [(k, y) for k, y in ky if str(byid[k]["strata"][dim]) == v]
                y = np.array([t for _, t in sub])
                cell = {"n": len(sub), "n_pos": int(y.sum()), "n_neg": int((1 - y).sum())}
                cell["testable"] = bool(cell["n_pos"] >= 50 and cell["n_neg"] >= 50)
                for m in key_metrics:
                    s, app, _ = fill([table[m][k] for k, _ in sub], table["_max"][m])
                    s = np.where(app, s, np.nan)
                    a = auc_w(y, s) if app.sum() else np.nan
                    fa = float(np.mean(s[(y == 0) & app] > thr[m])) if ((y == 0) & app).sum() else None
                    cell[m] = {"auroc": None if np.isnan(a) else float(a), "fa": fa}
                    rows.append({"set": sname, "dim": dim, "bin": v, "metric": m, "n": len(sub), "n_pos": cell["n_pos"],
                                 "n_neg": cell["n_neg"], "testable": cell["testable"], "auroc": cell[m]["auroc"], "fa": fa})
                d[f"{dim}={v}"] = cell
        # logistic slope: judge_cheap_disg correct at threshold ~ z(words) + label
        ks = [k for k, _ in ky]
        y = np.array([t for _, t in ky])
        s, app, _ = fill([table["judge_cheap_disg"][k] for k in ks], table["_max"]["judge_cheap_disg"])
        correct = ((s > thr["judge_cheap_disg"]).astype(int) == y).astype(int)
        w = np.array([byid[k]["strata"]["words"] for k in ks], dtype=float)
        z = (w - w.mean()) / (w.std() or 1)
        X = sm.add_constant(np.column_stack([z, y]))
        try:
            fit = sm.Logit(correct[app], X[app]).fit(disp=0)
            d["logit_correct_vs_words"] = {"coef_z_words": float(fit.params[1]), "se": float(fit.bse[1]), "p": float(fit.pvalues[1]),
                                           "coef_label": float(fit.params[2])}
        except Exception as e:  # noqa: BLE001
            d["logit_correct_vs_words"] = {"error": str(e)[:100]}
        out[sname] = d
    write_csv(TAB / "complexity.csv", rows)
    return out


def cost_table(items, rws, pilot, rt_llm, rt_nli, j1, j2, j3, prereg, costs_api):
    """$ and seconds per item and metric. API metrics: measured usage.cost per call (costs.jsonl, by component).
    Local metrics: GPU seconds x GPU_USD_PER_HOUR. Round-trip metrics need verbalise (+ re-formalise) calls."""
    from .local_llm import GPU_USD_PER_HOUR
    rate = GPU_USD_PER_HOUR / 3600
    comp = defaultdict(list)
    for c in costs_api:
        comp[c["component"]].append(c)
    def per_call(name):
        v = comp.get(name, [])
        return (float(np.mean([c["cost"] for c in v])) if v else None, float(np.mean([c["seconds"] for c in v])) if v else None, len(v))
    out = {}
    for label, cname in (("judge_cheap (API, per condition)", "judge_cheap_primary"), ("judge_cheap2 (API, per condition)", "judge_cheap_secondary"),
                         ("judge_strong (API, per condition)", "strong"), ("verbalise+reformalise calls (API, per call)", "roundtrip"),
                         ("gold_recall_probe (API, per call)", "gold_recall_probe")):
        usd, sec, n = per_call(cname)
        out[label] = {"usd_per_call": usd, "seconds_per_call": sec, "n_calls": n}
    rt = [r for r in rt_llm.values()]
    v_cost = float(np.mean([r.get("verbalise_cost") or 0 for r in rt])) if rt else None
    r_cost = float(np.mean([r.get("reformalise_cost") or 0 for r in rt])) if rt else None
    sn = [r.get("nli_seconds") for r in rt_nli.values() if r.get("nli_seconds") is not None]
    se = [r.get("embed_seconds") for r in rt_nli.values() if r.get("embed_seconds") is not None]
    out["rt_nli_* (API verbalise + local NLI)"] = {"usd_per_item": (v_cost or 0) + (np.mean(sn) if sn else 0) * rate}
    out["rt_embed_cos (API verbalise + local embed)"] = {"usd_per_item": (v_cost or 0) + (np.mean(se) if se else 0) * rate}
    out["rt_reformalise_eq (API verbalise + reformalise + z3)"] = {"usd_per_item": (v_cost or 0) + (r_cost or 0)}
    for name in ("judge_local_qwen8b", "judge_local_llama8b", "judge_local_qwen14b"):
        src = _load(name)
        v = [r.get("seconds") for r in src.values() if r.get("seconds") is not None]
        out[f"{name} (local GPU, per condition)"] = {"gpu_seconds_per_item": float(np.mean(v)) if v else None,
                                                     "usd_equiv_per_item": float(np.mean(v)) * rate if v else None}
    zs = [r.get("z3_seconds") for r in pilot.values() if r.get("z3_seconds") is not None]
    out["pilot_* (z3, CPU)"] = {"cpu_seconds_per_item": float(np.mean(zs)) if zs else None, "usd_per_item": 0.0}
    out["parse_fail"] = {"cpu_seconds_per_item": 0.001, "usd_per_item": 0.0}
    out["_api_spend_total_usd"] = float(sum(c["cost"] for c in costs_api))
    out["_api_spend_by_component"] = {k: float(sum(c["cost"] for c in v)) for k, v in comp.items()}
    out["_gpu_usd_per_hour"] = GPU_USD_PER_HOUR
    return out
