#!/usr/bin/env python3
"""STEP 0 ($0, label-blind, BEFORE any gloss call): the sealed score table for R_COMP FREE.

Inputs, read-only:
- exp 7 rcomp_candidates.jsonl through the WHITELIST loader (cc.load_scores): frozen c_score_align / nf / hyb, g_*, the judges;
- eval 3 pairwise_classes_RCOMP.jsonl (FREE): the label-free exact / ALIGN pair matrix;
- results/judge_orig_iter5_FREE.jsonl (D16, the label-blind completion of the original-view judge).

Derived here (all label-free):
- c_exact, and c_re (the recomputed c_score_align, used for the cross-check), END_MAJ align / exact, from eval 2's
  consensus_mx.row_consensus, imported unchanged;
- V1 c_pn, V2 c_rw, V3 c_pn_rw, V5 c_v5 from the sibling freeze file, copied into freeze_copy_prelim/ (out-of-fold
  family weights, 5 sentence folds);
- the s1a out-of-family syntactic flags (frozen detectors, see S1_DETECTORS).

Writes:
- results/scores_rcomp_free.jsonl (one row per FREE row);
- results/score_seal_rcomp.json (sha256 of each sorted (row_key, score) vector, for all rows and for untouched rows);
- results/score_checks.json.
"""
from __future__ import annotations

import importlib.util
import json
import re
import sys
import time
from collections import Counter

import numpy as np

from cc import EV2, EV3, LAB, RES, WS, dump, fold_of, jl, load_scores, setup_logger, sha256_file, vec_sha

sys.path.append(str(EV2 / "src"))
import consensus_mx as CS  # noqa: E402  (eval-2, unchanged, read-only import)

logger = setup_logger("scores")
_spec = importlib.util.spec_from_file_location("consensus_variants", WS / "freeze_copy_prelim/consensus_variants.py")
CV = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(CV)

# ------------------------------------------------------------------------------------------ s1a detectors (frozen)
ATOM = re.compile(r"([A-Za-z_][A-Za-z0-9_]*)\(([^()]*)\)")
BOUND = re.compile(r"[∀∃]\s*([a-z][A-Za-z0-9_]*)")
EXIST = re.compile(r"∃\s*([a-z][A-Za-z0-9_]*)")
SAME_PRED_DISJ = re.compile(r"(?<![A-Za-z0-9_])([A-Za-z_][A-Za-z0-9_]*)\([^()]*\)\s*\)*\s*∨\s*\(*\s*¬?\s*\1\(")
NEG_TOK = {"not", "non", "no", "never", "lacks", "without", "doesnot"}
S1_DETECTORS = {
    "d1_two_constants_same_slot": "one predicate name with >= 2 distinct constants (non-bound-variable arguments) in the same argument slot",
    "d2_same_pred_disjunction": "regex " + SAME_PRED_DISJ.pattern + " (a disjunction of two atoms of the same predicate)",
    "d3_exists_under_forall_as_argument": "the formula has a universal quantifier and an existential quantifier that introduces a "
                                          "variable used as a NON-FIRST argument of some atom (exists-for-constant)",
    "d4_negation_inside_name": "a CamelCase / underscore token of a predicate name at a non-first position is one of " + "|".join(sorted(NEG_TOK)),
}


def name_tokens(n: str) -> list[str]:
    return [t.lower() for t in re.findall(r"[A-Z]?[a-z]+|[A-Z]+(?![a-z])|\d+", n.replace("_", " "))]


def s1_flags(fol: str | None) -> dict:
    """Label-free syntactic detectors of the out-of-family faithful forms seen in the dataset-5 executor audit."""
    if not fol or not fol.strip():
        return {k: False for k in S1_DETECTORS}
    bound = set(BOUND.findall(fol))
    atoms = [(p, [a.strip() for a in args.split(",") if a.strip()]) for p, args in ATOM.findall(fol)]
    slots = {}
    for p, args in atoms:
        for i, a in enumerate(args):
            if a not in bound:
                slots.setdefault((p, i), set()).add(a)
    d1 = any(len(v) >= 2 for v in slots.values())
    d2 = bool(SAME_PRED_DISJ.search(fol))
    ex = set(EXIST.findall(fol))
    d3 = bool("∀" in fol and ex and any(a in ex for _, args in atoms for a in args[1:]))
    d4 = any(t in NEG_TOK for p, _ in atoms for t in name_tokens(p)[1:])
    return {"d1_two_constants_same_slot": d1, "d2_same_pred_disjunction": d2, "d3_exists_under_forall_as_argument": d3,
            "d4_negation_inside_name": d4}


# ------------------------------------------------------------------------------------------ helpers
def seen_iter3_membership() -> dict:
    """Label-free membership flag only: row_key -> seen_iter3 (whitelist hook drops every other key incl. labels)."""
    out = {}
    with (LAB / "results/free_labels_v2.jsonl").open() as fh:
        for line in fh:
            r = json.loads(line, object_pairs_hook=lambda ps: {k: v for k, v in ps if k in ("row_key", "seen_iter3")})
            out[r["row_key"]] = bool(r["seen_iter3"])
    return out


def judge_orig_merged(rows: list[dict]) -> dict:
    new = {}
    for r in jl(RES / "judge_orig_iter5_FREE.jsonl"):
        if r.get("p") is not None:
            new[r["row_key"]] = 1 - float(r["p"])
    out = {}
    for r in rows:
        if r["judge_cheap_orig"] is not None:
            out[r["row_key"]] = (r["judge_cheap_orig"], "exp7")
        elif r["row_key"] in new:
            out[r["row_key"]] = (new[r["row_key"]], "iter5")
        else:
            out[r["row_key"]] = (None, None)
    return out


SEAL_COLS = ["c_score_align", "c_exact", "c_re", "c_score_nf", "c_score_hyb", "g_align", "g_nf", "judge_cheap_disg",
             "judge_cheap_orig", "judge_cheap_orig_exp7", "judge_local_disg", "judge_local_orig", "end_maj_align", "end_maj_exact",
             "V1_c_pn", "V2_c_rw", "V3_c_pn_rw", "V5_c_v5", "npc", "plur_top_share", "s1_flag"]


@logger.catch(reraise=True)
def main() -> None:
    t0 = time.time()
    rows = load_scores("FREE")
    d5_keys = {r["row_key"] for r in jl(LAB / "work/free_rows.jsonl")}
    keys = {r["row_key"] for r in rows}
    assert len(rows) == 2652 and keys == d5_keys, (len(rows), len(keys ^ d5_keys))
    seen = seen_iter3_membership()
    assert set(seen) == keys
    pcl = [r for r in jl(EV3 / "pairwise_classes_RCOMP.jsonl") if r["condition"] == "FREE"]
    sms = {r["sentence_id"]: CS.SentenceMatrix(r) for r in pcl}
    ixs = {r["sentence_id"]: CV.build_index(r) for r in pcl}
    folds = {sid: fold_of(sid) for sid in ixs}
    wts = {f: CV.family_weights(list(ixs.values()), folds, f) for f in range(5)}
    wts_all = CV.family_weights(list(ixs.values()), folds, None)
    jo = judge_orig_merged(rows)
    out = []
    for r in rows:
        rk, sid = r["row_key"], r["sentence_id"]
        o = {k: r.get(k) for k in ("row_key", "item_id", "sentence_id", "template_id", "slot", "system", "family", "prompt_variant",
                                   "parse_ok", "coverage_status", "words", "word_tercile", "nconds_weak", "nconds_bin", "depth_weak",
                                   "nquant", "nested", "negated_condition", "clause_type", "cost_usd", "candidate_fol",
                                   "c_score_align", "c_score_nf", "c_score_hyb", "g_align", "g_nf", "judge_cheap_disg",
                                   "judge_local_disg", "judge_local_orig")}
        o["judge_cheap_orig_exp7"] = r["judge_cheap_orig"]
        o["judge_cheap_orig"], o["judge_cheap_orig_source"] = jo[rk]
        o["seen_iter3"] = seen[rk]
        o["untouched"] = not seen[rk]
        o["fold"] = fold_of(sid)
        sm = sms.get(sid)
        x = CS.row_consensus(sm, rk) if sm is not None else None
        o["in_matrix"] = x is not None
        o["is_peer"] = bool(sm.row_meta[rk]["is_peer"]) if x is not None else None
        if x is not None:
            o.update(npc=x["npc"], n_eq=x["n_eq"], n_eq_exact=x["n_eq_exact"], c_re=x["c_re"], c_exact=x["c_exact"],
                     end_maj_align=x["end_maj"], plur_top_share=x.get("plur_top_share"),
                     end_maj_exact=(x["n_eq_exact"] > x["npc"] / 2) if x["npc"] >= 2 else None)
            ix = ixs[sid]
            w = wts[folds[sid]]
            o["V1_c_pn"] = CV.c_pn(ix, rk)
            o["V2_c_rw"] = CV.c_rw(ix, rk, w)
            o["V3_c_pn_rw"] = CV.c_pn_rw(ix, rk, w)
            o["V5_c_v5"] = CV.c_v5(ix, rk, w)
            o["c_exact_cv"] = CV.c_exact(ix, rk)
        else:
            o.update(npc=None, n_eq=None, n_eq_exact=None, c_re=None, c_exact=None, end_maj_align=None, end_maj_exact=None,
                     plur_top_share=None, V1_c_pn=None, V2_c_rw=None, V3_c_pn_rw=None, V5_c_v5=None, c_exact_cv=None)
        fl = s1_flags(r.get("candidate_fol")) if r["parse_ok"] else {k: False for k in S1_DETECTORS}
        o["s1_detectors"] = [k for k, v in fl.items() if v]
        o["s1_flag"] = bool(o["s1_detectors"])
        out.append(o)
    # ---------------- checks
    def agree(a, b):
        both = [(o[a], o[b]) for o in out if o[a] is not None and o[b] is not None]
        mis = sum(abs(x - y) > 1e-9 for x, y in both)
        nd = sum((o[a] is None) != (o[b] is None) for o in out if o["parse_ok"])
        return {"n_compared": len(both), "n_mismatch": mis, "match_rate": 1 - mis / max(len(both), 1), "n_none_disagree_parsed": nd}
    checks = {"n_rows": len(out), "row_key_set_equals_dataset5": True, "n_untouched": sum(o["untouched"] for o in out),
              "c_score_sig_on_FREE_non_null": sum(r["c_score_sig"] is not None for r in rows),
              "c_re_vs_c_score_align": agree("c_re", "c_score_align"),
              "c_exact_eval2_vs_c_exact_variants_file": agree("c_exact", "c_exact_cv"),
              "judge_cheap_orig_sources": dict(Counter(o["judge_cheap_orig_source"] for o in out)),
              "family_weights_all_sentences": wts_all, "family_weights_by_heldout_fold": wts,
              "s1_flag_rate_parsed": float(np.mean([o["s1_flag"] for o in out if o["parse_ok"]])),
              "s1_detector_counts": dict(Counter(d for o in out for d in o["s1_detectors"])),
              "coverage_counts": dict(Counter(o["coverage_status"] for o in out)),
              "non_null": {c: sum(o.get(c) is not None for o in out) for c in SEAL_COLS}}
    checks["c_re_vs_c_score_align"]["pass_ge_0.99"] = checks["c_re_vs_c_score_align"]["match_rate"] >= 0.99
    dump(RES / "score_checks.json", checks)
    with (RES / "scores_rcomp_free.jsonl").open("w") as fh:
        for o in out:
            fh.write(json.dumps(o, ensure_ascii=False) + "\n")
    seal = {"utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "n_rows": len(out), "n_untouched": checks["n_untouched"],
            "columns": {}, "untouched_row_keys_sha256": vec_sha([(o["row_key"], True) for o in out if o["untouched"]]),
            "scores_file_sha256": sha256_file(RES / "scores_rcomp_free.jsonl"),
            "inputs_sha256": {"rcomp_candidates.jsonl": sha256_file(__import__("cc").E7_CAND),
                              "pairwise_classes_RCOMP.jsonl": sha256_file(EV3 / "pairwise_classes_RCOMP.jsonl"),
                              "judge_orig_iter5_FREE.jsonl": sha256_file(RES / "judge_orig_iter5_FREE.jsonl"),
                              "consensus_variants.py (prelim copy)": sha256_file(WS / "freeze_copy_prelim/consensus_variants.py")},
            "code_sha256": {p: sha256_file(WS / p) for p in ("confirm/scores.py", "confirm/cc.py", "confirm/judge_orig_complete.py")},
            "note": "sealed BEFORE the first gloss call; labels are joined only after this seal and the label seal both verify"}
    for c in SEAL_COLS:
        seal["columns"][c] = {"all": vec_sha([(o["row_key"], o.get(c)) for o in out]),
                              "untouched": vec_sha([(o["row_key"], o.get(c)) for o in out if o["untouched"]])}
    dump(RES / "score_seal_rcomp.json", seal)
    logger.info(f"checks: c_re vs c_align {checks['c_re_vs_c_score_align']}; orig sources {checks['judge_cheap_orig_sources']}; "
                f"s1 {checks['s1_detector_counts']}; {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
