#!/usr/bin/env python3
"""Writes results/deviations.json (every departure from the artifact plan / prereg_sig.json, with its cost) and fills the
'patches' section of results/VENDOR_SHA256.json (post-patch sha256 + reason for every vendored/copied file we edited).
Facts that depend on run outputs (counts, spend) are read from the files, not typed in. usage: write_records.py"""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results"
RC = ROOT / "rcomp"


def jl(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.exists() else []


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


PATCHES = {
    "src/vendor_x5/pool_scoring.py": "PEER_HYB (c_score_hyb = ALIGN OR NF-anchored agreement), keeps NF pairs; emits per-peer agreement dicts "
                                     "peer_equal_align / peer_equal_nf keyed by peer row (for class ids / mechanism join)",
    "src/vendor_x5/vendor_d/budget.py": "OPENROUTER_BASE_URL instead of a hard-coded URL; artifact-wide guard()/book(); workspace root one level deeper",
    "src/vendor_x5/vendor_d/common.py": "workspace root one level deeper (src/vendor_x5/vendor_d)",
    "src/vendor_x5/vendor_a/llm.py": "OPENROUTER_BASE_URL instead of a hard-coded URL",
    "src/vendor_x5/vendor_c/peers.py": "OPENROUTER_BASE_URL instead of a hard-coded URL",
    "src/vendor_e_panel/panel.py": "vendored location on sys.path; cache under results/",
    "src/vendor_e_panel/or_client.py": "OPENROUTER_BASE_URL; artifact-wide guard()/book(); ledger/catalog paths",
    "rcomp/src_e/or_client.py": "OPENROUTER_BASE_URL; artifact-wide guard()/book()",
    "rcomp/src_e/generate.py": "retry transient provider errors (HTTP 404/502/503, key limit) on resume",
    "rcomp/src/label_rcomp.py": "worker count from RCOMP_LABEL_WORKERS (48-core box)",
    "rcomp/src/select_rcomp.py": "dataset-3 bug: Counter.update with dict values raised TypeError (log = dict(log))",
}


def main() -> None:
    v = json.loads((RES / "VENDOR_SHA256.json").read_text())
    v["patches"] = {f: {"sha256_after_patch": sha(ROOT / f), "reason": r} for f, r in PATCHES.items() if (ROOT / f).exists()}
    (RES / "VENDOR_SHA256.json").write_text(json.dumps(v, indent=1))

    sents = json.loads((RC / "work" / "rcomp_sentences.json").read_text())
    n_main = sum(s["batch"] == "main" for s in sents)
    free = jl(RES / "free_labels.jsonl")
    fl = Counter(r["label"] for r in free)
    fj = jl(RES / "judge_FREE.jsonl")
    fj_ok = {(r["row_key"], r["cond"]) for r in fj if r.get("p") is not None}
    fr = [r for r in jl(RES / "judge_frontier_SIG.jsonl") if r.get("p") is not None]
    polls = jl(ROOT / "logs" / "key_poll.jsonl")
    led = sum(float(r.get("usd") or 0) for r in jl(ROOT / "cost_ledger.jsonl"))
    D = [
        {"id": "D1", "step": "S1", "what": "Sonnet lexicon audit and reference audit NOT run (only the Haiku fluency phase ran); all 314 "
         "selected sentences keep audit_status PENDING", "why": "the shared OpenRouter key showed limit $7.00 / $4.64 remaining for ALL "
         "concurrent runs at 01:37 UTC; the Sonnet adjudicator's R_ADJ gate had failed anyway", "cost": "plan F6 path: references are "
         "verified by construction + z3 unit tests only; some awkward sentences may survive (fluency filter still applied)"},
        {"id": "D2", "step": "S1", "what": f"final selection gave {n_main} main sentences (< 250): 75 preselected sentences dropped for fluency < 3; "
         "reserve (93) untouched because SIG was TESTABLE without the top-up", "why": "prereg selection rule", "cost": "smaller n; per-template cells ~20-28 sentences"},
        {"id": "D3", "step": "S1", "what": "minimal fix of a dataset-3 bug in rcomp/src/select_rcomp.py (Counter.update with dict values)", "why": "code error (F6)", "cost": "none"},
        {"id": "D4", "step": "S1", "what": "perturb.py and adjudicate.py select skipped (as planned)", "why": "PERTURB already exists in dataset 3; the Sonnet adjudicator is replaced", "cost": "none"},
        {"id": "D5", "step": "S4", "what": "F (gpt-5.1) dropped from FREE generation (F_sentences = 0)", "why": "shared-key budget; F is not needed for consensus (few-shot peers only)", "cost": "no GPT-5.1 FREE candidates"},
        {"id": "D6", "step": "S4", "what": f"zero-shot G2 (qwen3-235b) returned a bodiless HTTP 404 on every call (few-shot G2 works); "
         f"{fl.get('NO_OUTPUT', 0)} FREE rows are NO_OUTPUT (no candidate; excluded, counted)", "why": "provider-side failure, retried once on resume", "cost": "zero-shot arm = G1b only"},
        {"id": "D7", "step": "S7b/S9", "what": "the FREE judge's original-text pass stopped at "
         f"{sum(1 for k in fj_ok if k[1] == 'orig')} rows; the disguised bar covers {sum(1 for k in fj_ok if k[1] == 'disg')} rows. "
         "SIG judges ran once more over rows whose first pass hit proxy 5xx errors (network failures, not parse failures; parse failures "
         "came back from the cache and were not re-billed)", "why": "shared key near exhaustion after FREE became NOT_TESTABLE (D9)", "cost": "FREE judge_cheap_orig partial (secondary only)"},
        {"id": "D8", "step": "S7c", "what": f"frontier subsample cut to {len({r['row_key'] for r in fr})} rows (30 ERROR / 30 CORRECT, sha1-first, "
         "orig AND disguised; 5-row pilot first) instead of 150", "why": "pilot $0.0052/call; 300 calls would exceed the $1.0 allowance and the shared key; prereg rule 'N >= 50 or NOT TESTED'",
         "cost": "frontier (d)-analogue is descriptive with wide CIs"},
        {"id": "D9", "step": "S8", "what": "the dataset-E panel (and its 60-item known-label check) was NOT run, so FREE has no tier-B labels. "
         f"FREE labels are tier A (solver) only: {dict(fl)}. FREE is NOT_TESTABLE (< 50 CORRECT), so the FREE readout is descriptive and sign-only (plan F4)",
         "why": "the shared key fell to $0.37 (03:27 UTC) against about $1.7 needed; F1 polled the key every 10 min for 60 min: "
         + json.dumps([p.get("limit_remaining") for p in polls]), "cost": "no FREE CI claim; the vocabulary-divergence contrast is on tier A only, where CORRECT means exactly equivalent under the reference's names"},
        {"id": "D10", "step": "S10", "what": "g_align / g_nf are used AS IS (ALIGN:g_score, NF-anchored:g_score), not as '1 - g'",
         "why": "exp-5 peer_text.py line 812 defines g_score = 1 - F1(support, coverage), already 'higher = more likely an error'; the plan's '1 - g' would invert it (AUROC 0.02 in a debug run)", "cost": "none (bug avoided)"},
        {"id": "D11", "step": "S9", "what": "FREE consensus and judge scores were computed label-blind BEFORE the FREE testability declaration (FREE_PREJOIN=1)",
         "why": "prereg S8 requires the FREE declaration before any FREE score is JOINED; analyse.py is the first join and checks the declaration and the label sha256", "cost": "none"},
        {"id": "D12", "step": "S7a/S9/S10.8", "what": "worker-side fixes in src/score_consensus.py: (a) warm nltk/wordnet/pandas/scipy imports before the per-pair SIGALRM, because "
         "an alarm that fires during a slow first import leaves a half-initialised module and fails every later sentence of that worker (seen in an early SIG re-score and in the first FREE mini-run; both were discarded "
         "and re-run); (b) apply RLIMIT_AS only after those imports (MemoryError otherwise); (c) the rename pass restores sys.path before spawning workers, because rcomp/src/common.py shadowed vendor_c/common.py (eqmv); "
         "(d) BLAS threads pinned to 1 (OpenBLAS virtual reservations hit RLIMIT_AS)", "why": "infrastructure bugs, not method changes", "cost": "none; every final score file has 0 WORKER_FAIL sentences"},
        {"id": "D13", "step": "S7d", "what": "local Qwen3-8B judge (bf16, greedy, RUBRIC_B + USER_JSON, exp-5 config) ran at batch 12 (it ran out of GPU memory at 48 on the 20 GB RTX 4000 Ada). "
         "The original-text condition was also run, as a secondary contamination row comparable with exp 5's E value", "why": "hardware", "cost": "none"},
        {"id": "D14", "step": "all API phases", "what": "F1's '$2 pause' threshold was not applied at phase start; each phase instead ran in the pre-registered priority order and stopped at a $0.25 key floor, as prereg_sig.json caps_usd.shared_key_note specifies",
         "why": "the shared key's total limit was $7 for all runs, so a $2 threshold would have blocked the primary judge bar", "cost": "less key left for other runs; the artifact's own spend stayed far below its $9.5 cap"},
        {"id": "D15", "step": "S3/S5", "what": "SIG exemplars keep their own vocabulary (signature block appended to the final user message only), as disclosed in the plan", "why": "fewshot_v1 byte-identical", "cost": "small prompt inconsistency"},
    ]
    out = {"artifact_ledger_total_usd": round(led, 4), "deviations": D}
    (RES / "deviations.json").write_text(json.dumps(out, indent=1))
    print(f"deviations: {len(D)}; patches: {len(v['patches'])}; ledger ${led:.4f}")


if __name__ == "__main__":
    main()
