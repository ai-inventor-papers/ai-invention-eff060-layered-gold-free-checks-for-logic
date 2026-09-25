#!/usr/bin/env python3
"""E2-B Step 6: UNION with E2-A and the inverse-variance meta-analysis cross-check.

  uv run / exp5src/.venv/bin/python src/union.py --e2a <E2-A per-row file> [--e2a-marker <E2A_FINAL_READY.json>]

Harmonises E2-A's per-row file to E2-B's column names (a column-name map with fallbacks; any analysis whose columns are
missing is NOT_COMPUTED and says which column), applies the duplicate rule (a sentence labelled by both samples counts
once, taking E2-B's copy; test-retest kappa of final labels on the duplicates), then:
  U1 union LONG POOL (L25_E2A + L25_E2B + EXC_E2A): strat delta V0 - flashlite_disg, CI > 0, + point > 0 vs orig / nano
  U2 union L25; U3 nested [S4 + V0] - S4 (per-sample cross-fitted S4 columns); U4 carried variant (none: V0 stands)
  fixed sequence at alpha 0.05 (each tested only if the previous is confirmed);
  heterogeneity Delta_A - Delta_B (SE = sqrt(SE_A^2 + SE_B^2)), Cochran's Q, I^2; within-25-29-bin recheck;
  fixed-effect inverse-variance meta-analysis (L25_E2A, L25_E2B, EXC_E2A) vs the pooled bootstrap (|diff| > 0.02 reported).
Strata = {L25_E2A, L25_E2B, EXC_E2A} x word bin; sentence-cluster bootstrap B=2000 (exp-6 api_bar), seed 0.
Outputs: analysis/union_longpool.json."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
import time
from collections import Counter
from pathlib import Path

import numpy as np

WS = Path(__file__).resolve().parents[1]
AN = WS / "analysis"
sys.path.insert(0, str(WS / "exp6src"))
from src import api_bar as AB  # noqa: E402

ALIASES = {  # E2-B name -> candidate E2-A names (first found wins)
    "row_key": ["row_key", "canonical_key", "metadata_row_key", "item_key"],
    "sentence_id": ["sentence_id", "metadata_sentence_id", "sid"],
    "stratum": ["stratum", "source_stratum", "metadata_stratum"],
    "label": ["label", "final_label", "output"],
    "tier": ["tier", "label_tier", "metadata_label_tier"],
    "reading_choice": ["reading_choice", "metadata_reading_choice"],
    "V0": ["V0", "c_score_align", "c_align"],
    "flashlite_disg": ["flashlite_disg", "judge_cheap_disg", "judge_flashlite_disg"],
    "flashlite_orig": ["flashlite_orig", "judge_cheap_orig", "judge_flashlite_orig"],
    "nano_orig": ["nano_orig", "judge_cheap2_orig", "judge_nano_orig"],
    "S4": ["S4_E2B", "S4_E2_oof", "S4_E2", "S4_full_oof", "S4_oof"],
    "S4_plus_V0": ["S4_E2B_plus_V0", "S4_E2_plus_c_score_align_oof", "S4_E2_plus_V0", "S4_full_plus_c_score_align_oof", "S4_plus_c_oof"],
    "words": ["words", "n_words"],
    "word_bin": ["word_bin"],
    "system_class": ["system_class", "metadata_system_class"],
    "in_R_AB": ["in_R_AB", "in_RAB", "R_AB"],
}


def jl(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()]


def pick(r: dict, name: str):
    for a in ALIASES[name]:
        if a in r:
            return r[a], a
        if isinstance(r.get("strata"), dict) and a in r["strata"]:
            return r["strata"][a], "strata." + a
        if isinstance(r.get("metadata_strata"), dict) and a in r["metadata_strata"]:
            return r["metadata_strata"][a], "metadata_strata." + a
    return None, None


def harmonise(rows: list[dict], sample: str) -> tuple[list[dict], dict]:
    out, used = [], Counter()
    for r in rows:
        h = {"sample": sample}
        for n in ALIASES:
            v, src = pick(r, n)
            h[n] = v
            if src:
                used[f"{n}<-{src}"] += 1
        st = str(h["stratum"] or "")
        if sample == "E2B":
            h["stratum"] = "L25_E2B"
        elif st.startswith("L25"):
            h["stratum"] = "L25_E2A"
        elif st.startswith("EXC"):
            h["stratum"] = "EXC_E2A"
        elif st.startswith("DT"):
            h["stratum"] = "DT_E2A"
        if h["word_bin"] is None and h["words"] is not None:
            h["word_bin"] = "30-34" if h["words"] >= 30 else ("25-29" if h["words"] >= 25 else "<25")
        if h["in_R_AB"] is None:
            h["in_R_AB"] = (h["label"] in ("CORRECT", "ERROR") and h["tier"] in ("A", "B") and not h["reading_choice"]
                            and (h["system_class"] in (None, "llm")))
        h["y"] = 1 if h["label"] == "ERROR" else (0 if h["label"] == "CORRECT" else None)
        out.append(h)
    return out, dict(used)


def cell_delta(rows: list[dict], a: str, b: str, B: int, strat_key=lambda r: f"{r['stratum']}|{r['word_bin']}") -> dict:
    R = [r for r in rows if r["in_R_AB"] and r.get(a) is not None and r.get(b) is not None and r["y"] is not None]
    if len(R) < 20 or len({r["y"] for r in R}) < 2:
        return {"n": len(R), "delta": None, "status": "NOT_TESTABLE"}
    y = np.array([r["y"] for r in R])
    sa = np.array([float(r[a]) for r in R])
    sb = np.array([float(r[b]) for r in R])
    h = np.array([strat_key(r) for r in R])
    cb = AB.ClusterBoot([f"{r['sample']}|{r['sentence_id']}" for r in R], b=B, seed=0)
    d = AB.paired_boot(y, sa, sb, cb, "strat", h)
    sids = np.array([r["sentence_id"] for r in R])
    return {"a": a, "b": b, "strat_a": d["a"], "strat_b": d["b"], "delta": d["delta"], "ci": d["ci"], "se": d["se"],
            "ci_gt_0": bool(d["ci"][0] is not None and d["ci"][0] > 0), "n": len(R), "n_error": int(y.sum()), "n_correct": int(len(y) - y.sum()),
            "n_sentences": len(set(sids)), "sentences_with_both_classes": len(set(sids[y == 1]) & set(sids[y == 0]))}


def kappa(a: list, b: list) -> float | None:
    if not a:
        return None
    cats = sorted(set(a) | set(b))
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    pe = sum((a.count(c) / n) * (b.count(c) / n) for c in cats)
    return (po - pe) / (1 - pe) if pe < 1 else None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--e2a", required=True)
    ap.add_argument("--e2a-marker", default="")
    ap.add_argument("--e2b", default=str(AN / "per_item_E2B.jsonl"))
    ap.add_argument("--B", type=int, default=2000)
    ap.add_argument("--out", default=str(AN / "union_longpool.json"))
    a = ap.parse_args()
    OUT = Path(a.out)
    pa, pb = Path(a.e2a), Path(a.e2b)
    out = {"inputs": {"e2a": str(pa), "e2a_sha256": hashlib.sha256(pa.read_bytes()).hexdigest(), "e2b": str(pb),
                      "e2b_sha256": hashlib.sha256(pb.read_bytes()).hexdigest()}, "B": a.B, "computed_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    if a.e2a_marker:
        m = json.loads(Path(a.e2a_marker).read_text())
        want = m.get("sha256") or m.get("per_row_sha256")
        out["inputs"]["e2a_marker"] = a.e2a_marker
        out["inputs"]["e2a_sha_matches_marker"] = (want == out["inputs"]["e2a_sha256"]) if want else "marker has no sha256 field"
        out["e2a_label_regime"] = m.get("label_regime")
    A, ua = harmonise(jl(pa), "E2A")
    Bb, ub = harmonise(jl(pb), "E2B")
    out["column_map_used"] = {"E2A": ua, "E2B": ub}
    missing = [n for n in ("sentence_id", "stratum", "label", "tier", "V0", "flashlite_disg") if not any(r[n] is not None for r in A)]
    if missing:
        out["status"] = f"NOT_COMPUTED: E2-A file lacks columns {missing}"
        OUT.write_text(json.dumps(out, indent=1))
        print(out["status"])
        return 1
    A = [r for r in A if r["stratum"] in ("L25_E2A", "EXC_E2A")]
    # duplicate rule: a sentence labelled by both counts once, E2-B's copy
    dup = sorted({r["sentence_id"] for r in A} & {r["sentence_id"] for r in Bb})
    if dup:
        key = lambda r: (r["sentence_id"], str(r["row_key"]).split("|")[-1])  # noqa: E731
        la = {key(r): r["label"] for r in A if r["sentence_id"] in dup}
        lb = {key(r): r["label"] for r in Bb if r["sentence_id"] in dup}
        common = sorted(set(la) & set(lb))
        out["duplicates"] = {"n_sentences": len(dup), "n_rows_matched": len(common),
                             "kappa_final_labels": kappa([la[k] for k in common], [lb[k] for k in common]),
                             "agreement": (sum(la[k] == lb[k] for k in common) / len(common)) if common else None}
        A = [r for r in A if r["sentence_id"] not in set(dup)]
    else:
        out["duplicates"] = {"n_sentences": 0}
    U = A + Bb
    long_pool = [r for r in U if r["stratum"] in ("L25_E2A", "L25_E2B", "EXC_E2A")]
    l25 = [r for r in U if r["stratum"] in ("L25_E2A", "L25_E2B")]
    seq = {}
    seq["U1_long_pool_V0_minus_flashlite_disg"] = cell_delta(long_pool, "V0", "flashlite_disg", a.B)
    seq["U1_aux_vs_flashlite_orig"] = cell_delta(long_pool, "V0", "flashlite_orig", a.B)
    seq["U1_aux_vs_nano_orig"] = cell_delta(long_pool, "V0", "nano_orig", a.B)
    seq["U2_L25_V0_minus_flashlite_disg"] = cell_delta(l25, "V0", "flashlite_disg", a.B)
    seq["U3_nested_S4_plus_V0_minus_S4_long_pool"] = cell_delta(long_pool, "S4_plus_V0", "S4", a.B)
    seq["U4_carried_variant_minus_V0"] = {"status": "NOT_APPLICABLE: M1 winner = 'NONE: V0 stands'"}
    # fixed-sequence verdicts
    alive = True
    fs = {}
    for k in ("U1_long_pool_V0_minus_flashlite_disg", "U2_L25_V0_minus_flashlite_disg", "U3_nested_S4_plus_V0_minus_S4_long_pool", "U4_carried_variant_minus_V0"):
        d = seq[k]
        if str(d.get("status", "")).startswith("NOT_APPLICABLE"):
            fs[k] = d["status"]
            continue
        if not alive:
            fs[k] = "DESCRIPTIVE (an earlier hypothesis in the fixed sequence was not confirmed)"
            continue
        if d.get("delta") is None:
            fs[k] = d.get("status", "NOT_COMPUTED")
            alive = False
            continue
        extra_ok = True
        if k.startswith("U1"):
            extra_ok = all((seq[x].get("delta") or -1) > 0 for x in ("U1_aux_vs_flashlite_orig", "U1_aux_vs_nano_orig"))
        ok = d["ci_gt_0"] and extra_ok
        fs[k] = "CONFIRMED (CI > 0)" if ok else ("NOT CONFIRMED: " + ("CI includes 0" if d["delta"] > 0 else "point <= 0"))
        alive = ok
    u1 = seq["U1_long_pool_V0_minus_flashlite_disg"]
    wording = ("confirmed on untouched long sentences" if u1.get("ci_gt_0") else
               ("direction replicated, not significant at MDE ~0.057" if (u1.get("delta") or 0) > 0 else
                "DISCONFIRM: E result was development-set optimism"))
    out["fixed_sequence"] = {"results": seq, "verdicts": fs, "U1_wording": wording}
    # heterogeneity A vs B on L25 (+ within 25-29 bin)
    het = {}
    for nm, filt in (("L25_all_bins", lambda r: True), ("L25_bin_25-29", lambda r: r["word_bin"] == "25-29")):
        dA = cell_delta([r for r in U if r["stratum"] == "L25_E2A" and filt(r)], "V0", "flashlite_disg", a.B)
        dB = cell_delta([r for r in U if r["stratum"] == "L25_E2B" and filt(r)], "V0", "flashlite_disg", a.B)
        if dA.get("delta") is None or dB.get("delta") is None:
            het[nm] = {"status": "NOT_COMPUTED", "A": dA, "B": dB}
            continue
        diff = dA["delta"] - dB["delta"]
        se = math.sqrt(dA["se"] ** 2 + dB["se"] ** 2)
        wA, wB = 1 / dA["se"] ** 2, 1 / dB["se"] ** 2
        pooled = (wA * dA["delta"] + wB * dB["delta"]) / (wA + wB)
        Q = wA * (dA["delta"] - pooled) ** 2 + wB * (dB["delta"] - pooled) ** 2
        from scipy.stats import chi2
        het[nm] = {"delta_E2A": dA["delta"], "se_E2A": dA["se"], "delta_E2B": dB["delta"], "se_E2B": dB["se"], "diff_A_minus_B": diff,
                   "diff_ci": [diff - 1.96 * se, diff + 1.96 * se], "Q": Q, "Q_p": float(1 - chi2.cdf(Q, 1)),
                   "I2": max(0.0, (Q - 1) / Q) if Q > 0 else 0.0,
                   "differs": bool(abs(diff) > 1.96 * se)}
    out["heterogeneity"] = het
    # fixed-effect inverse-variance meta-analysis
    comps = {}
    for st in ("L25_E2A", "L25_E2B", "EXC_E2A"):
        comps[st] = cell_delta([r for r in U if r["stratum"] == st], "V0", "flashlite_disg", a.B)
    ok = {k: v for k, v in comps.items() if v.get("delta") is not None and v.get("se")}
    if ok:
        w = {k: 1 / v["se"] ** 2 for k, v in ok.items()}
        est = sum(w[k] * ok[k]["delta"] for k in ok) / sum(w.values())
        se = math.sqrt(1 / sum(w.values()))
        l25k = [k for k in ok if k.startswith("L25")]
        wl = {k: w[k] for k in l25k}
        est_l25 = sum(wl[k] * ok[k]["delta"] for k in l25k) / sum(wl.values()) if wl else None
        out["meta_analysis_fixed_effect"] = {
            "components": {k: {"delta": v["delta"], "se": v["se"], "n": v["n"]} for k, v in comps.items()},
            "long_pool": {"estimate": est, "ci": [est - 1.96 * se, est + 1.96 * se],
                          "pooled_bootstrap": u1.get("delta"), "abs_diff": abs(est - (u1.get("delta") or est)),
                          "disagreement_gt_0.02": bool(abs(est - (u1.get("delta") or est)) > 0.02)},
            "L25": {"estimate": est_l25, "ci": ([est_l25 - 1.96 * math.sqrt(1 / sum(wl.values())), est_l25 + 1.96 * math.sqrt(1 / sum(wl.values()))] if wl else None),
                    "pooled_bootstrap": seq["U2_L25_V0_minus_flashlite_disg"].get("delta")}}
    regime_b = next((json.loads(l).get("label_regime") for l in pb.read_text().splitlines() if l.strip()), None)
    out["label_regimes"] = {"E2A": out.get("e2a_label_regime"), "E2B": regime_b,
                            "union_status": ("SECONDARY (label regimes differ)" if out.get("e2a_label_regime") and regime_b and
                                             str(out.get("e2a_label_regime")).upper() != str(regime_b).upper() else "PRIMARY")}
    out["residual_risk"] = ("E2-A and E2-B share the label instrument (the panel): the union adds SAMPLING power, not label-regime "
                            "independence; instrument-disjoint confirmation is R_COMP FREE's role")
    out["status"] = "COMPUTED"
    OUT.write_text(json.dumps(out, indent=1, default=str))
    print(json.dumps({"U": fs, "wording": wording, "het": {k: v.get("diff_A_minus_B") for k, v in het.items()}}, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
