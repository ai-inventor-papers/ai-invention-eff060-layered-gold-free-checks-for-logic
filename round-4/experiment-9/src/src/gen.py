"""STEP D/E: write the pre-registration (prereg_csc_E.json + sha256) from the pilot, then run the generation sweeps.

usage: gen.py prereg | gen.py mini | gen.py full
Arm sizes (declared in the prereg BEFORE any CSC score is joined to labels): OWN = all 2,686 R_AB rows; K4 = 600
stratified rows from families outside the pool; OTHER-SIG = 900 stratified rows; FORMAT-ONLY = ALL rows (expanded from
900: after dedup by (text, model) it costs ~1,100 calls); PLACEBO = 100; RENAME = ALL R_AB CORRECT rows (expanded from 400
because only ~1/3 of rows admit a WordNet synonym rename)."""
from __future__ import annotations

import asyncio
import hashlib
import json
import sys
import time
from pathlib import Path

from loguru import logger

sys.path.insert(0, str(Path(__file__).resolve().parent))
import arms as A  # noqa: E402
import csc  # noqa: E402
import csc_llm as llm  # noqa: E402

ROOT = A.ROOT
RES = ROOT / "results"
SIZES = {"OWN": None, "K4": 600, "OTHER": 900, "FMT": 10**6, "PLACEBO": 100, "RENAME": 10**6}
ARM_ORDER = ["OWN", "FMT", "OTHER", "K4", "RENAME_SYN", "RENAME_NONCE", "PLACEBO"]
SHRINK = {"PLACEBO": 50, "RENAME": 250, "OTHER": 600, "FMT": 600, "K4": 300}


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def build():
    frame = A.load_frame()
    labels = {r["row_key"]: r["y"] for r in A.jl(A.DATA / "labels_RAB.jsonl")}
    return frame, A.build_arms(frame, labels, sizes=SIZES)


def write_prereg() -> dict:
    pilot = json.loads((RES / "pilot.json").read_text())
    frame, built = build()
    usd = {m: v["usd_per_call"] for m, v in pilot["per_model"].items()}
    proj = {}
    for arm in ARM_ORDER:
        uj = A.dedupe(built["jobs"].get(arm, []))
        proj[arm] = {"rows": len(built["arms"].get(arm, {})), "unique_calls": len(uj),
                     "usd_est": round(sum(usd.get(j["model"], max(usd.values())) for j in uj), 4)}
    allj = A.dedupe([j for a in ARM_ORDER for j in built["jobs"].get(a, [])])
    total = sum(usd.get(j["model"], max(usd.values())) for j in allj)
    rows_sha = {a: hashlib.sha1("\n".join(sorted(v)).encode()).hexdigest() for a, v in built["arms"].items()}
    pre = {
        "title": "T6-E Candidate-Signature Consensus on development set E -- pre-registration",
        "status_of_data": "DEVELOPMENT: dataset E was used by earlier rounds to choose consensus; no result here is a confirmation (confirmation = iteration 5 on E2 / R_COMP FREE).",
        "written_before": "any CSC score exists for the full sweep and before any CSC score is joined to labels (only the 30-row pilot peers exist; no pilot score was joined to labels)",
        "prompt": {"file": "iter_1/gen_art/gen_art_dataset_1/prompts/fewshot_v1.txt", "sha256": sha256(csc.PROMPT_PATH),
                   "block_sig": csc.B_SIG, "block_format_only": csc.B_FMT, "temperature": 0, "max_tokens": 600},
        "pool": [m[0] for m in csc.POOL], "pool_params": {m[0]: m[2] for m in csc.POOL},
        "peer_rule": "first k=3 pool members whose vendor family differs from the candidate's; k=4 arm = all 4, only for families outside the pool",
        "equivalence": "z3 validity of a<->b with predicates keyed (lowercased name, arity) and constants by lowercased name; union vocabulary uninterpreted; NO aligner; 2 s z3 timeout (+ 20 s wall cap); UNKNOWN = not equivalent (counted); random-finite-model fingerprint pre-filter (sound)",
        "scores": {"c_csc": "1 - share of usable peers z3-equivalent to the candidate",
                   "c_csc_graded": "exp 5 peer_text.graded_consensus with the identity map (1 - F1(support, coverage))",
                   "c_csc_multi": "peer endorses if eq(cand, p.fol) or (eq(cand, p.alt_fol) and p.alt_fol eq some other peer's fol or alt_fol)",
                   "fallbacks": "<2 usable peers -> 0.5 (csc_insufficient_peers, share reported); unparseable candidate -> 1.0 in the COVERAGE view only (R_AB rows are all parseable)"},
        "binary": "flag = c > 0.5 (k=3: endorsed = at least 2 of 3 usable peers agree; with 2 usable peers both must agree); e = P(endorsed | ERROR), d = P(flagged | CORRECT)",
        "rows": {"population": "the 2,686 parseable R_AB E_POOL rows of T1 (1,822 ERROR / 864 CORRECT, 292 sentences)",
                 "arm_rows_sha1": rows_sha, "selection": {k: v for k, v in built["selection"].items() if k != "RENAME"},
                 "rename_selection": {k: v for k, v in built["selection"].get("RENAME", {}).items() if k != "rows"}},
        "arms": {"OWN": "CSC with the candidate's own signature, k=3 (all rows)",
                 "FREE-MATCHED": "$0: the same 3 family-disjoint pool families' EXISTING dataset-E few-shot outputs (G4/G6/G7/G2-fewshot), scored exactly (c_free_exact) and with the frozen eqmv/ALIGN verdicts of eval 2's pairwise matrix (c_free_align)",
                 "FORMAT-ONLY": "fresh no-signature calls, same peers, same JSON/alt_fol instruction (ALL rows; ADDED control)",
                 "OTHER-SIG": "sham: the signature of the lowest-Jaccard other parseable candidate of the same sentence (900 stratified rows); scored exactly and with eqmv (ALIGN)",
                 "K4": "k=4 for families outside the pool (600 stratified rows)",
                 "RENAME_SYN / RENAME_NONCE": "ALL R_AB CORRECT rows; SYN = dataset-3 control_rename WordNet synonym (only rows that admit one); NONCE = E disguise map on the formula only; peers regenerated from the renamed signature",
                 "PLACEBO": "100 rows; peers get the signature of a random OTHER sentence",
                 "HYB_MEAN / HYB_MAX": "(c_csc + c_score_align)/2 and max(.) ($0)"},
        "metrics": {"primary": "stratified (within source_stratum) AUROC, tie-aware (eval 2 stats.strat_auc)",
                    "secondary": ["pooled AUROC", "AUPRC", "e/d", "per-stratum AUROC"],
                    "bootstrap": "sentence-clustered, B=2000, seed 0 (eval 2 SentBoot), paired on identical rows",
                    "cells": "a cell with < 50 positives or < 50 negatives is NOT_READ"},
        "gates": {"G1": "d(c_csc > 0.5 | R_AB CORRECT) <= 0.35 AND the words slope of GEE d ~ z(words) + z(n_conditions) among CORRECT rows has CI including 0 or entirely < 0",
                  "G2": "stratified AUROC(CSC) >= stratified AUROC(c_score_align) - 0.01 on R_AB AND pooled AUROC(CSC) > AUROC(c_score_align) on L25 (point estimates; the L25 paired CI is reported whatever its sign)",
                  "G3-E": "FA(c > 0.5) on RENAME_SYN CORRECT rows <= base FA (same rows, CSC-OWN) + 0.05 (point estimate; CI reported); NONCE reported as the stress boundary, not gated",
                  "G4": "null here (sibling PERTURB experiment)",
                  "G5": "FULL cost per candidate (sum of its peer calls, dedup-apportioned) <= $0.002",
                  "variants": "{c_csc, c_csc_graded, c_csc_multi} x k {3, 4 on the K4 rows} + HYB_MEAN; graded variants binarised at the same c > 0.5"},
        "analyses": ["(a) e/d per stratum, words tercile, n_conditions bin, exception type; GEE d~zw+zn (CORRECT), e~zw+zn (ERROR); NET words T3-T1 (eval 2 net_test)",
                     "(b) AUROC/AUPRC/strat AUROC overall, L25, long, EXC, CTRL; paired deltas vs judges, c_score_align, FREE-MATCHED, FORMAT-ONLY, p_peer_text, rt_nli_min, sc5_eq_frac; attribution CSC-FMT (signature) and FMT-FREE (format+drift)",
                     "(c) nesting over S4_full and S4_full + c_score_align via fit_s4_oof on folds_E",
                     "(d) where d went: vocabulary-only vs structural free-peer disagreements (pairs_E); 60-row tagging of still-flagged CORRECT rows (rule written first)",
                     "(e) e by error class, CSC vs FREE-MATCHED vs OTHER-SIG",
                     "(f) typing via typed_repair_same_vocab against E repair_ops (R_A errors with 1-2 ops) vs majority, medoid 0.371, chance",
                     "(g) cost per candidate FULL (dedup-apportioned and undeduped) and MARGINAL (z3 CPU s)",
                     "(h) complexity curves + M3 (bootstrap delta-slope and stacked GEE interaction)",
                     "(i) system-level Kendall tau-b over 13 system x variant rows",
                     "(j) placebos: shuffled labels, random-sentence signature",
                     "(k) RENAME FA SYN / NONCE vs base",
                     "sensitivity: tier A only; VEX subset; COVERAGE view; insufficient-peer rows excluded vs 0.5"],
        "pilot": {k: pilot[k] for k in ("n_rows", "per_model", "spent_total")},
        "cost_estimate": {"per_arm": proj, "total_dedup_usd": round(total, 4), "hard_stop_usd": llm.HARD_STOP,
                          "shrink_order_if_projection_exceeds_8.5": SHRINK, "OWN_floor_rows": 1500},
        "pre_declared_deviations": [
            "microsoft/phi-4 pilot parse rate 0.85 (n=27) is below the 0.9 go-criterion but above the 0.8 drop rule; failures are function terms / non-grammar formulas (E-parser UNPARSEABLE), not JSON format; phi-4 KEPT, re-checked on the mini-sweep (drop if < 0.8), unparseable peers leave the denominator",
            "FORMAT-ONLY expanded from 900 rows to all rows and RENAME from 400 to all CORRECT rows (cheap after dedup; declared before any score)",
            "large inputs (> 5 MB) are read in place (sha256 logged in inputs_manifest.json) instead of being copied into ./inputs",
            "rename_syn additionally rejects a synonym whose lowercased name collides with an existing symbol (CSC matches names case-insensitively)"],
        "created_ts": time.time(),
    }
    p = ROOT / "prereg_csc_E.json"
    p.write_text(json.dumps(pre, indent=1, ensure_ascii=False))
    (ROOT / "prereg_csc_E.sha256").write_text(sha256(p) + "  prereg_csc_E.json\n")
    logger.info(f"prereg written sha256 {sha256(p)}; total est ${total:.3f}; per arm {proj}")
    return pre


def run_arms(arms_sel: list[str], max_rows: int | None = None, stop_at: float = 9.0) -> dict:
    frame, built = build()
    jobs = []
    for a in arms_sel:
        rk = list(built["arms"].get(a, {}))
        if max_rows is not None:
            rks = set(rk)
            keep = {r["row_key"] for r in A.stratified([r for r in frame if r["row_key"] in rks], max_rows, "MINI")}
            ks = {s["key"] for r in keep for s in built["arms"][a][r]["slots"]}
            jobs += [j for j in built["jobs"][a] if j["key"] in ks]
        else:
            jobs += built["jobs"][a]
    jobs = A.dedupe(jobs)
    res = asyncio.run(llm.run_jobs(jobs, concurrency=32, stop_at=stop_at))
    (RES / "arms_built.json").write_text(json.dumps({"arms": built["arms"], "selection": built["selection"]}, ensure_ascii=False))
    return {k: v for k, v in res.items() if k != "records"}


if __name__ == "__main__":
    logger.remove()
    logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
    logger.add(ROOT / "logs" / "gen.log", rotation="30 MB", level="DEBUG")
    cmd = sys.argv[1]
    if cmd == "prereg":
        write_prereg()
    elif cmd == "mini":
        logger.info(run_arms(["OWN", "FMT"], max_rows=200))
        logger.info(run_arms(["PLACEBO"], max_rows=20))
    elif cmd == "full":
        logger.info(run_arms(ARM_ORDER))
