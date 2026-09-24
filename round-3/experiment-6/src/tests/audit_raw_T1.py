#!/usr/bin/env python3
"""Raw-file re-derivation of the T1 headline numbers (TODO 5), on a code path disjoint from src/ and tests/audit_T1.py.

Reads ONLY raw inputs, never the joined or aggregated outputs:
- labels from dataset E itself (iter_1 full_data_out.json, heldout_candidates);
- pool and parse_ok from data/E_units.json;
- consensus scores from exp 5's frozen per_item_E.jsonl (exp 5 imputation value read from data/exp5/prereg.json);
- API judge scores straight from results/scores/judge_cheap.jsonl and judge_strong.jsonl
  (oriented = 1 - P(faithful); a JSON failure = 0.5, the pre-registered rule);
- frame rows from data/frontier_frame.json.

AUROC is computed with the Mann-Whitney rank-sum formula (scipy rankdata, midranks for ties). This differs from the
sklearn roc_auc_score used by src/api_bar.py and from the pairwise count used by audit_T1.py. The bootstrap is its own
loop (B = 1000, seed 2024).

Placebos: the same bootstrap test is re-run on
(1) labels permuted within stratum, and
(2) a random-score challenger.
Neither should pass, i.e. the CI must not lie above 0.
Output: results/audit_raw_T1.json.
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy.stats import rankdata

ROOT = Path(__file__).resolve().parent.parent
E_FULL = Path("/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_dataset_1/full_data_out.json")


def auc_rank(y: np.ndarray, s: np.ndarray) -> float:
    n1, n0 = int(y.sum()), int(len(y) - y.sum())
    if n1 == 0 or n0 == 0:
        return float("nan")
    r = rankdata(s)
    return float((r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def strat_auc(y, s, h) -> float:
    num = den = 0.0
    for g in np.unique(h):
        m = h == g
        n1, n0 = int(y[m].sum()), int((~y[m].astype(bool)).sum())
        if n1 and n0:
            num += auc_rank(y[m], s[m]) * n1 * n0
            den += n1 * n0
    return num / den


def cluster_boot(sid, f, B=1000, seed=2024):
    groups = defaultdict(list)
    for i, s in enumerate(sid):
        groups[s].append(i)
    gl = [np.array(v) for _, v in sorted(groups.items())]
    rng = np.random.default_rng(seed)
    vals = []
    for _ in range(B):
        pick = rng.integers(0, len(gl), len(gl))
        vals.append(f(np.concatenate([gl[j] for j in pick])))
    vals = np.array(vals)
    return [float(np.nanpercentile(vals, 2.5)), float(np.nanpercentile(vals, 97.5))]


def last_scores(path: Path) -> dict:
    out = {}
    for line in path.read_text().splitlines():
        if line.strip():
            r = json.loads(line)
            if r.get("p") is not None or r["key"] not in out:
                out[r["key"]] = r
    return out


def main() -> int:
    # ---- labels from dataset E (R_AB: tiers A/B, final CORRECT/ERROR, no reading_choice)
    E = json.loads(E_FULL.read_text())
    cand = next(d for d in E["datasets"] if d["dataset"] == "heldout_candidates")["examples"]
    units = {u["item_id"] + "|" + u["prompt_variant"]: u for u in json.loads((ROOT / "data" / "E_units.json").read_text())}
    lab = {}
    for r in cand:
        inp = json.loads(r["input"])
        k = r["metadata_item_id"] + "|" + inp.get("prompt_variant")
        if (r["metadata_label_tier"] in ("A", "B") and r["metadata_final_label"] in ("CORRECT", "ERROR")
                and not r.get("metadata_reading_choice")):
            u = units[k]
            if u["pool"] == "E_POOL" and u["parse_ok"] in (True, "True"):
                lab[k] = (1 if r["metadata_final_label"] == "ERROR" else 0, r["metadata_sentence_id"],
                          r["metadata_strata"]["source_stratum"], r["metadata_item_id"])
    # ---- frozen consensus (exp 5) with exp 5's parseable-missing neutral value
    neutral = json.loads((ROOT / "data" / "exp5" / "prereg.json").read_text())["imputation"]["neutral"]["c_score_align"]
    e5 = {}
    for line in (ROOT / "data" / "exp5" / "per_item_E.jsonl").read_text().splitlines():
        r = json.loads(line)
        e5[r["row_key"]] = neutral if r["c_score_align"] is None else r["c_score_align"]
    # ---- raw API judge scores
    jc = last_scores(ROOT / "results" / "scores" / "judge_cheap.jsonl")
    js = last_scores(ROOT / "results" / "scores" / "judge_strong.jsonl")

    def judge(d, iid, view):
        r = d.get(f"{iid}|{view}")
        if r is None:
            return np.nan
        return 0.5 if r.get("p") is None else 1.0 - float(r["p"])

    K = sorted(lab)
    y = np.array([lab[k][0] for k in K])
    sid = np.array([lab[k][1] for k in K])
    h = np.array([lab[k][2] for k in K])
    c = np.array([e5[k] for k in K], float)
    jd = np.array([judge(jc, lab[k][3], "disg") for k in K])
    out = {"population": {"n": len(K), "n_error": int(y.sum()), "n_correct": int(len(y) - y.sum()), "n_sentences": len(set(sid)),
                          "judge_missing": int(np.isnan(jd).sum())}}
    out["pooled_auroc"] = {"c_score_align": auc_rank(y, c), "judge_cheap_disg": auc_rank(y, jd)}
    out["strat_auroc"] = {"c_score_align": strat_auc(y, c, h), "judge_cheap_disg": strat_auc(y, jd, h)}

    def dtest(yy, a, b, hh, ss, mask=None):
        m = np.ones(len(yy), bool) if mask is None else mask
        yy, a, b, hh, ss = yy[m], a[m], b[m], hh[m], ss[m]
        d = strat_auc(yy, a, hh) - strat_auc(yy, b, hh)
        ci = cluster_boot(ss, lambda ix: strat_auc(yy[ix], a[ix], hh[ix]) - strat_auc(yy[ix], b[ix], hh[ix]))
        return {"delta": d, "ci": ci, "passes_CI_gt0": ci[0] > 0, "n": int(m.sum())}
    out["confirmatory_strat_delta"] = dtest(y, c, jd, h, sid)
    out["long_pool_strat_delta"] = dtest(y, c, jd, h, sid, mask=np.isin(h, ["L25", "L20", "EXC"]))
    # ---- placebos: the same test must FAIL
    rng = np.random.default_rng(7)
    yp = y.copy()
    for g in np.unique(h):
        m = np.where(h == g)[0]
        yp[m] = rng.permutation(yp[m])
    out["placebo_permuted_labels"] = dtest(yp, c, jd, h, sid)
    out["placebo_random_challenger"] = dtest(y, rng.random(len(y)), jd, h, sid)
    # ---- frame ratio (frontier original view)
    fr = json.loads((ROOT / "data" / "frontier_frame.json").read_text())["rows"]
    by_item = defaultdict(list)
    for k in K:
        by_item[lab[k][3]].append(k)
    Fk = [sorted(by_item[r["item_id"]])[0] for r in fr if by_item.get(r["item_id"])]
    fy = np.array([lab[k][0] for k in Fk])
    fc = np.array([e5[k] for k in Fk], float)
    fs = np.array([judge(js, lab[k][3], "orig") for k in Fk])
    out["frame"] = {"n": len(Fk), "auroc_c": auc_rank(fy, fc), "auroc_strong_orig": auc_rank(fy, fs),
                    "ratio": auc_rank(fy, fc) / auc_rank(fy, fs)}
    # ---- compare with the analysis (read only for the comparison; nothing above uses it)
    A = json.loads((ROOT / "results" / "analysis_T1.json").read_text())
    ref = {"confirmatory": A["a_head_on"]["R_AB pooled"]["deltas"]["c_score_align - judge_cheap_disg [strat]"]["delta"],
           "long": A["a_head_on"]["R_AB long (L25+L20+EXC)"]["deltas"]["c_score_align - judge_cheap_disg [strat]"]["delta"],
           "ratio": A["d_frontier"]["ratio"]["ratio"]}
    out["checks"] = {
        "population_2686": out["population"]["n"] == 2686,
        "confirmatory_match_1e-3": abs(out["confirmatory_strat_delta"]["delta"] - ref["confirmatory"]) < 1e-3,
        "long_match_1e-3": abs(out["long_pool_strat_delta"]["delta"] - ref["long"]) < 1e-3,
        "ratio_match_1e-3": abs(out["frame"]["ratio"] - ref["ratio"]) < 1e-3,
        "placebo_permuted_fails": not out["placebo_permuted_labels"]["passes_CI_gt0"],
        "placebo_random_fails": not out["placebo_random_challenger"]["passes_CI_gt0"]}
    out["analysis_reference"] = ref
    out["all_ok"] = all(out["checks"].values())
    (ROOT / "results" / "audit_raw_T1.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))
    return 0 if out["all_ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
