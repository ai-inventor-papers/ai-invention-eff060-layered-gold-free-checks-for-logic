#!/usr/bin/env python3
"""Label-free descriptive analyses of E2-B (valid without any label; computed from sealed scores only, under the same
open() guard as the scorers). They do NOT test faithfulness; they describe coverage, cost, agreement structure and the
invariance of the frozen metric, which the user asked for per metric.

  (1) coverage per system: parse rate, V0 scorable (>= 2 other-family parseable peers), judge coverage;
  (2) score distributions per word bin and per system (V0, PT, flash-lite disguised), flag rates at 0.5;
  (3) concordance V0 vs flash-lite disguised on rows scored by both (Spearman, flag agreement, Cohen kappa of flags);
  (4) system-level rankings by mean V0 vs by mean flash-lite disguised (Kendall tau-b between the two label-free rankings);
  (5) pairwise agreement structure (eval-2 matrix): classes per sentence, largest-class share, share of cross-family pairs
      agreeing, share of sentences with no agreeing cross-family pair, pair timeouts;
  (6) label-free rename invariance of V0: RENAME_SYN / RENAME_NONCE controls of a hash sample of parseable candidates
      (any label): paired flip (control flagged at c > 0.5 while its parent is not), reverse flip, mean shift, exact-equal
      share, with Wilson CIs; V0 of the parent recomputed and checked against the sealed score.
-> analysis/descriptive_nolabels_E2B.json"""
from __future__ import annotations

import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

WS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WS / "src"))
import score_e2b as S  # noqa: E402  (guard + helpers)

SC, AN = WS / "scores", WS / "analysis"
AN.mkdir(exist_ok=True)


def wilson(k, n, z=1.96):
    if n == 0:
        return [None, None]
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return [c - h, c + h]


def desc(v):
    v = np.array([x for x in v if x is not None], float)
    if len(v) == 0:
        return {"n": 0}
    return {"n": int(len(v)), "mean": float(v.mean()), "median": float(np.median(v)), "share_gt_0.5": float((v > 0.5).mean()),
            "share_eq_0": float((v == 0).mean()), "share_eq_1": float((v == 1).mean()), "n_distinct": int(len(np.unique(v)))}


def main():
    S.install_guard()
    from scipy.stats import spearmanr, kendalltau
    rows = S.jl(SC / "scores_E2B.jsonl")
    out = {"n_rows": len(rows), "n_sentences": len({r["sentence_id"] for r in rows}), "note": "label-free; no faithfulness claim"}
    by_slot = defaultdict(list)
    for r in rows:
        by_slot[r["slot"]].append(r)
    cov = {}
    for s, rs in sorted(by_slot.items()):
        n = len(rs)
        cov[s] = {"system": rs[0]["system"], "family": rs[0]["family"], "n": n, "parse_rate": sum(r["parse_ok"] for r in rs) / n,
                  "V0_scorable": sum(r["parse_ok"] and r["V0"] is not None for r in rs) / n,
                  "flashlite_disg_ok": sum(r.get("flashlite_disg_status") in ("ok", "fallback") for r in rs) / n,
                  "V0": desc([r["V0"] for r in rs if r["parse_ok"]]), "flashlite_disg": desc([r.get("flashlite_disg") for r in rs if r["parse_ok"]])}
    out["coverage_per_system"] = cov
    out["coverage_all"] = {"parse_rate": sum(r["parse_ok"] for r in rows) / len(rows),
                           "V0_scorable": sum(r["parse_ok"] and r["V0"] is not None for r in rows) / len(rows),
                           "V0_missing_reason": dict(Counter(r.get("V0_missing_reason") for r in rows if r["parse_ok"] and r["V0"] is None)),
                           "judge_status": {j: dict(Counter(r.get(j + "_status") for r in rows)) for j in
                                            ("flashlite_disg", "flashlite_orig", "nano_orig", "nano_disg", "costmatched_disg", "costmatched_orig", "frontier_orig")}}
    out["distribution_by_word_bin"] = {b: {m: desc([r.get(m) for r in rows if r["word_bin"] == b and r["parse_ok"]])
                                           for m in ("V0", "p_peer_text", "flashlite_disg", "V1", "V2", "c_exact")}
                                       for b in sorted({r["word_bin"] for r in rows})}
    both = [r for r in rows if r["parse_ok"] and r["V0"] is not None and r.get("flashlite_disg_status") == "ok"]
    if both:
        a = np.array([r["V0"] for r in both])
        b = np.array([r["flashlite_disg"] for r in both])
        fa, fb = a > 0.5, b > 0.5
        po = float((fa == fb).mean())
        pe = float(fa.mean() * fb.mean() + (1 - fa.mean()) * (1 - fb.mean()))
        out["concordance_V0_vs_flashlite_disg"] = {"n": len(both), "spearman": float(spearmanr(a, b).statistic),
                                                    "flag_agreement": po, "flag_kappa": (po - pe) / (1 - pe) if pe < 1 else None,
                                                    "V0_flag_rate": float(fa.mean()), "judge_flag_rate": float(fb.mean())}
    # system-level label-free rankings
    sys_v0 = {s: np.mean([r["V0"] for r in rs if r["parse_ok"] and r["V0"] is not None]) for s, rs in by_slot.items()}
    sys_fl = {s: np.mean([r["flashlite_disg"] for r in rs if r.get("flashlite_disg_status") == "ok"] or [np.nan]) for s, rs in by_slot.items()}
    ks = [s for s in sorted(by_slot) if not np.isnan(sys_fl[s])]
    out["system_rankings"] = {"mean_V0": {s: float(sys_v0[s]) for s in sorted(by_slot)}, "mean_flashlite_disg": {s: float(sys_fl[s]) for s in ks},
                              "parse_rate": {s: cov[s]["parse_rate"] for s in sorted(by_slot)},
                              "tau_b_V0_vs_flashlite": float(kendalltau([sys_v0[s] for s in ks], [sys_fl[s] for s in ks], variant="b").statistic) if len(ks) > 3 else None}
    # pairwise structure
    mx = S.jl(SC / "pairwise_classes_E2B.jsonl")
    if mx:
        ncls, top, agree_pairs, none_agree, to = [], [], [], 0, 0
        for m in mx:
            rows_n = sum(len(nd["rows"]) for nd in m["nodes"])
            if rows_n == 0:
                continue
            size = [sum(len(m["nodes"][i]["rows"]) for i in cl) for cl in m["cliques"]]
            ncls.append(len(m["cliques"]))
            top.append(max(size) / rows_n)
            fam = {r["row_key"]: r["family"] for nd in m["nodes"] for r in nd["rows"]}
            node = {r["row_key"]: nd["node_id"] for nd in m["nodes"] for r in nd["rows"]}
            eq = {}
            for i, j, e, _k, _s in m["pairs"]:
                eq[(i, j)] = eq[(j, i)] = e
                to += e is None
            keys = sorted(fam)
            cnt = ag = 0
            for x in range(len(keys)):
                for y in range(x + 1, len(keys)):
                    if fam[keys[x]] == fam[keys[y]]:
                        continue
                    cnt += 1
                    ag += (node[keys[x]] == node[keys[y]]) or eq.get((node[keys[x]], node[keys[y]])) is True
            if cnt:
                agree_pairs.append(ag / cnt)
                none_agree += ag == 0
        out["agreement_structure"] = {"n_sentences": len(ncls), "mean_classes_per_sentence": float(np.mean(ncls)),
                                      "mean_largest_class_share": float(np.mean(top)), "mean_cross_family_agreement": float(np.mean(agree_pairs)),
                                      "share_sentences_no_cross_family_agreement": none_agree / max(1, len(agree_pairs)),
                                      "pair_timeouts_unknown": int(to), "n_pairs_total": int(sum(len(m["pairs"]) for m in mx))}
    # label-free rename invariance
    cs = S.jl(SC / "controls_lf_scores_E2B.jsonl")
    if cs:
        sc = {r["row_key"]: r for r in rows}
        rn = {}
        for t in ("RENAME_SYN", "RENAME_NONCE"):
            cc = [c for c in cs if c["control_type"] == t and c["V0_control"] is not None and sc[c["parent_row_key"]]["V0"] is not None]
            n = len(cc)
            par = np.array([sc[c["parent_row_key"]]["V0"] for c in cc])
            con = np.array([c["V0_control"] for c in cc])
            flip = int(((con > 0.5) & ~(par > 0.5)).sum())
            rev = int((~(con > 0.5) & (par > 0.5)).sum())
            rn[t] = {"n_pairs": n, "paired_flip": flip / n if n else None, "paired_flip_ci": wilson(flip, n),
                     "reverse_flip": rev / n if n else None, "reverse_flip_ci": wilson(rev, n),
                     "flag_rate_parent": float((par > 0.5).mean()) if n else None, "flag_rate_control": float((con > 0.5).mean()) if n else None,
                     "mean_shift_control_minus_parent": float((con - par).mean()) if n else None,
                     "share_score_unchanged": float((np.abs(con - par) < 1e-12).mean()) if n else None,
                     "parent_recomputed_matches_sealed": int(sum(abs((c["V0_parent_recomputed"] if c["V0_parent_recomputed"] is not None else -9) - sc[c["parent_row_key"]]["V0"]) < 1e-9 for c in cc))}
        rn["sample"] = "sha1('E2B_lfctrl|'+row_key) first 300 PARSEABLE candidates, any label; controls from E2's frozen generator (dataset-3 perturb.control_rename), z3-verified under the inverse map"
        out["rename_invariance_any_label"] = rn
    (AN / "descriptive_nolabels_E2B.json").write_text(json.dumps(out, indent=1, default=float))
    print(json.dumps({k: out[k] for k in out if k in ("concordance_V0_vs_flashlite_disg", "agreement_structure", "coverage_all")}, default=float)[:1500])


if __name__ == "__main__":
    main()
