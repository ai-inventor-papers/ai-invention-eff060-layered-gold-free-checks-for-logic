#!/usr/bin/env python3
"""Independent re-derivation of the headline numbers from the RAW result files, through a different code path than
src/analyse.py (no import of analyse.py / auc_tools.py / analysis_rows_*.jsonl / rcomp_candidates.jsonl):

  raw inputs : results/sig_labels.jsonl (labels), results/scores_SIG.jsonl (consensus), results/judge_SIG.jsonl,
               results/judge_frontier_SIG.jsonl, results/judge_local_SIG.jsonl, results/scores_rename_SIG.jsonl,
               results/free_labels.jsonl, results/scores_FREE.jsonl, results/judge_FREE.jsonl, rcomp/work/rcomp_sentences.json
  AUROC      : brute-force O(n_err x n_cor) pair counting per stratum in pure Python (analyse.py uses rank bincounts)
  bootstrap  : Python `random` with a different seed, sentences resampled within template as explicit row lists
  placebos   : the same delta test on (a) labels permuted within sentence and (b) a random score in place of c_score_sig;
               the test must FAIL (CI includes 0 / delta ~ 0) there.
Writes results/rederive_raw.json and prints a comparison with results/analysis.json.
usage: .venv/bin/python tests/rederive_raw.py [--B 400]
"""
import argparse
import json
import random
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "results"
FEW = {"G1", "G1b", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9"}


def jl(p):
    return [json.loads(l) for l in Path(p).read_text().splitlines() if l.strip()]


def judge_map(p):
    d = {}
    for r in jl(p):
        if r.get("p") is not None:
            d[(r["row_key"], r["cond"])] = 1.0 - float(r["p"])
    return d


def score_map(p):
    d = {}
    for r in jl(p):
        d.update(r["rows"])
    return d


def auc_pairs(rows, key, stratum):
    """sum over strata of concordant (+0.5 ties) / pairs, brute force."""
    by = defaultdict(lambda: ([], []))
    for r in rows:
        (by[stratum(r)][0] if r["y"] else by[stratum(r)][1]).append(r[key])
    num = den = 0.0
    for e, c in by.values():
        for a in e:
            for b in c:
                num += 1.0 if a > b else (0.5 if a == b else 0.0)
        den += len(e) * len(c)
    return num / den if den else float("nan")


def boot_delta(rows, k1, k2, stratum, B, seed):
    rng = random.Random(seed)
    by_s = defaultdict(list)
    for r in rows:
        by_s[r["sid"]].append(r)
    by_t = defaultdict(list)
    for s, rs in by_s.items():
        by_t[rs[0]["tmpl"]].append(s)
    ds = []
    for _ in range(B):
        samp = []
        for t, ss in by_t.items():
            for i in range(len(ss)):
                s = rng.choice(ss)
                samp.extend(dict(r, tmpl=t) for r in by_s[s])
        ds.append(auc_pairs(samp, k1, stratum) - auc_pairs(samp, k2, stratum))
    ds.sort()
    return [ds[int(0.025 * B)], ds[int(0.975 * B) - 1]], sum(d <= 0 for d in ds) / B


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--B", type=int, default=400)
    a = ap.parse_args()
    S = {s["sentence_id"]: s for s in json.loads((ROOT / "rcomp" / "work" / "rcomp_sentences.json").read_text())}
    sc = score_map(RES / "scores_SIG.jsonl")
    jc, jf, jlo = judge_map(RES / "judge_SIG.jsonl"), judge_map(RES / "judge_frontier_SIG.jsonl"), judge_map(RES / "judge_local_SIG.jsonl")
    rows = []
    for r in jl(RES / "sig_labels.jsonl"):
        if r["slot"] not in FEW or r["label"] not in ("CORRECT", "ERROR") or S[r["sentence_id"]]["batch"] != "main":
            continue
        x = sc.get(r["row_key"], {})
        k = r["row_key"]
        rows.append({"k": k, "sid": r["sentence_id"], "tmpl": S[r["sentence_id"]]["template_id"], "y": r["label"] == "ERROR",
                     "reading": r.get("matched_reading"), "c_sig": x.get("c_score_sig"), "c_hyb": x.get("c_score_hyb"),
                     "j_disg": jc.get((k, "disg")), "j_orig": jc.get((k, "orig")), "f_orig": jf.get((k, "orig")),
                     "f_disg": jf.get((k, "disg")), "l_disg": jlo.get((k, "disg")), "l_orig": jlo.get((k, "orig"))})
    T = lambda r: r["tmpl"]  # noqa: E731
    both = lambda k1, k2: [r for r in rows if r[k1] is not None and r[k2] is not None]  # noqa: E731
    out = {"n_pool": len(rows), "n_error": sum(r["y"] for r in rows), "n_correct": sum(not r["y"] for r in rows)}

    p = both("c_sig", "j_disg")
    ci, pv = boot_delta(p, "c_sig", "j_disg", T, a.B, 1234)
    out["primary"] = {"n": len(p), "auroc_c_sig": auc_pairs(p, "c_sig", T), "auroc_judge_disg": auc_pairs(p, "j_disg", T)}
    out["primary"]["delta"] = out["primary"]["auroc_c_sig"] - out["primary"]["auroc_judge_disg"]
    out["primary"]["ci"], out["primary"]["p_one_sided"] = ci, pv
    q = both("c_sig", "j_orig")
    out["vs_orig"] = {"n": len(q), "delta": auc_pairs(q, "c_sig", T) - auc_pairs(q, "j_orig", T)}
    out["vs_orig"]["ci"], _ = boot_delta(q, "c_sig", "j_orig", T, a.B, 99)
    for jn in (("j_orig", "j_disg"), ("l_orig", "l_disg")):
        w = both(*jn)
        out[f"disguise_cost_{jn[0][0]}"] = {"n": len(w), "delta": auc_pairs(w, jn[0], T) - auc_pairs(w, jn[1], T)}
    out["pooled_delta"] = auc_pairs(p, "c_sig", lambda r: 0) - auc_pairs(p, "j_disg", lambda r: 0)
    out["within_sentence_delta"] = auc_pairs(p, "c_sig", lambda r: r["sid"]) - auc_pairs(p, "j_disg", lambda r: r["sid"])
    fr = both("c_sig", "f_orig")
    out["frontier"] = {"n": len(fr), "auroc_c_sig_pooled": auc_pairs(fr, "c_sig", lambda r: 0),
                       "auroc_frontier_orig_pooled": auc_pairs(fr, "f_orig", lambda r: 0),
                       "auroc_frontier_disg_pooled": auc_pairs(both("c_sig", "f_disg"), "f_disg", lambda r: 0)}
    lo = both("c_sig", "l_disg")
    out["local"] = {"auroc_disg": auc_pairs(lo, "l_disg", T), "auroc_orig": auc_pairs(both("c_sig", "l_orig"), "l_orig", T)}
    cor = [r for r in rows if not r["y"] and r["c_sig"] is not None]
    out["d_by_reading"] = {rd: sum(r["c_sig"] >= 0.5 for r in cor if r["reading"] == rd) / max(1, sum(r["reading"] == rd for r in cor))
                           for rd in ("weak", "strong")}
    err = [r for r in rows if r["y"] and r["c_sig"] is not None]
    out["e_error_endorsement"] = sum(r["c_sig"] < 0.5 for r in err) / len(err)
    fl = [r for r in rows if r["c_sig"] is not None]
    tp = sum(r["c_sig"] >= 0.5 and r["y"] for r in fl)
    fp = sum(r["c_sig"] >= 0.5 and not r["y"] for r in fl)
    out["op_c_sig"] = {"precision": tp / (tp + fp), "recall": tp / sum(r["y"] for r in fl), "fa": fp / sum(not r["y"] for r in fl)}

    # rename invariance from the raw rename scores
    ren = score_map(RES / "scores_rename_SIG.jsonl")
    ra = {}
    for kind in ("RENAME_NONCE", "RENAME_SYN"):
        for m in ("c_score_nf", "c_score_hyb", "c_score_align"):
            key = "NF-anchored:c_score_nf" if m == "c_score_nf" else m
            v = [x[key] for k, x in ren.items() if k.startswith(f"REN|{kind}|") and x.get(key) is not None]
            ra[f"{kind}:{m}"] = {"n": len(v), "fa": sum(t >= 0.5 for t in v) / len(v) if v else None}
    out["rename_fa"] = ra

    # FREE tier-A deltas (point estimates)
    fsc = score_map(RES / "scores_FREE.jsonl")
    fj = judge_map(RES / "judge_FREE.jsonl")
    frows = []
    for r in jl(RES / "free_labels.jsonl"):
        if r["label"] in ("CORRECT", "ERROR") and r["label_tier"] in ("A", "B") and not r.get("ref_flagged"):
            x = fsc.get(r["row_key"], {})
            frows.append({"sid": r["sentence_id"], "tmpl": S[r["sentence_id"]]["template_id"], "y": r["label"] == "ERROR",
                          "c_align": x.get("c_score_align"), "c_hyb": x.get("c_score_hyb"), "j_disg": fj.get((r["row_key"], "disg"))})
    fa = [r for r in frows if r["c_align"] is not None and r["j_disg"] is not None]
    out["FREE"] = {"n": len(fa), "delta_align_vs_disg": auc_pairs(fa, "c_align", T) - auc_pairs(fa, "j_disg", T),
                   "delta_hyb_vs_disg": auc_pairs([r for r in fa if r["c_hyb"] is not None], "c_hyb", T) - auc_pairs([r for r in fa if r["c_hyb"] is not None], "j_disg", T)}

    # PLACEBOS: the same primary test must FAIL here
    rng = random.Random(777)
    perm = []
    by_s = defaultdict(list)
    for r in p:
        by_s[r["sid"]].append(r)
    for rs in by_s.values():
        ys = [r["y"] for r in rs]
        rng.shuffle(ys)
        perm += [dict(r, y=y) for r, y in zip(rs, ys)]
    ci_p, pv_p = boot_delta(perm, "c_sig", "j_disg", lambda r: r["sid"], a.B, 55)
    out["placebo_within_sentence_label_permutation"] = {
        "delta_within_sentence": auc_pairs(perm, "c_sig", lambda r: r["sid"]) - auc_pairs(perm, "j_disg", lambda r: r["sid"]),
        "ci": ci_p, "p_one_sided": pv_p, "fails_as_expected": ci_p[0] <= 0 <= ci_p[1]}
    rnd = [dict(r, rnd=rng.random()) for r in p]
    ci_r, pv_r = boot_delta(rnd, "rnd", "j_disg", T, a.B, 66)
    out["placebo_random_score_vs_judge"] = {"auroc_random": auc_pairs(rnd, "rnd", T),
                                            "delta_random_minus_judge": auc_pairs(rnd, "rnd", T) - auc_pairs(rnd, "j_disg", T),
                                            "ci": ci_r, "passes_primary_rule": ci_r[0] > 0}
    gshuf = [dict(r, y=y) for r, y in zip(p, rng.sample([r["y"] for r in p], len(p)))]
    ci_g, _ = boot_delta(gshuf, "c_sig", "j_disg", T, a.B, 77)
    out["placebo_global_label_shuffle"] = {"auroc_c_sig": auc_pairs(gshuf, "c_sig", T),
                                           "delta": auc_pairs(gshuf, "c_sig", T) - auc_pairs(gshuf, "j_disg", T),
                                           "ci": ci_g, "fails_as_expected": ci_g[0] <= 0 <= ci_g[1]}

    # comparison with the analysis output
    A = json.loads((RES / "analysis.json").read_text())
    s = A["SIG"]
    cmp = {"primary_delta": (out["primary"]["delta"], s["primary"]["delta"]),
           "primary_ci": (out["primary"]["ci"], s["primary"]["ci"]),
           "vs_orig_delta": (out["vs_orig"]["delta"], s["secondary"]["vs_judge_cheap_orig"]["delta"]),
           "pooled_delta": (out["pooled_delta"], s["secondary"]["pooled"]["delta"]),
           "within_sentence_delta": (out["within_sentence_delta"], s["secondary"]["within_sentence"]["delta"]),
           "disguise_cost_cheap": (out["disguise_cost_j"]["delta"], s["contamination"]["judge_cheap"]["orig_minus_disg_within_template"]["delta"]),
           "disguise_cost_local": (out["disguise_cost_l"]["delta"], s["contamination"]["judge_local"]["orig_minus_disg_within_template"]["delta"]),
           "frontier_c_sig": (out["frontier"]["auroc_c_sig_pooled"], s["frontier"]["c_score_sig"]["pooled"]["auroc"]),
           "frontier_orig": (out["frontier"]["auroc_frontier_orig_pooled"], s["frontier"]["judge_frontier_orig"]["pooled"]["auroc"]),
           "d_strong": (out["d_by_reading"]["strong"], s["mechanism_sig"]["d_by_matched_reading"]["strong"]["d_correct_divergence"]),
           "d_weak": (out["d_by_reading"]["weak"], s["mechanism_sig"]["d_by_matched_reading"]["weak"]["d_correct_divergence"]),
           "rename_nonce_hyb": (out["rename_fa"]["RENAME_NONCE:c_score_hyb"]["fa"], s["rename_invariance"]["RENAME_NONCE"]["c_score_hyb"]["fa_rate_c_ge_0.5"]),
           "FREE_align": (out["FREE"]["delta_align_vs_disg"], A["FREE"]["tier_AB"]["c_score_align_vs_judge_cheap_disg"]["delta"]),
           "FREE_hyb": (out["FREE"]["delta_hyb_vs_disg"], A["FREE"]["tier_AB"]["c_score_hyb_vs_judge_cheap_disg"]["delta"])}
    out["comparison_rederived_vs_analysis"] = {k: {"rederived": v[0], "analysis": v[1],
                                                   "match_1e-9": (abs(v[0] - v[1]) < 1e-9) if isinstance(v[0], float) else None}
                                               for k, v in cmp.items()}
    (RES / "rederive_raw.json").write_text(json.dumps(out, indent=1))
    for k, v in out["comparison_rederived_vs_analysis"].items():
        print(f"{k:24s} rederived={v['rederived']} analysis={v['analysis']} match={v['match_1e-9']}")
    for k in ("placebo_within_sentence_label_permutation", "placebo_random_score_vs_judge", "placebo_global_label_shuffle"):
        print(k, json.dumps(out[k]))


if __name__ == "__main__":
    main()
