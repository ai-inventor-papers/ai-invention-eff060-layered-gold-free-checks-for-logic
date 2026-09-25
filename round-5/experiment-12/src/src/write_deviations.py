#!/usr/bin/env python3
"""deviations.json (every departure from plan.md / prereg_iter5_E2B.json, with its evidence file) and
cost_ledger_master.jsonl (every paid call of this artifact, one line each, from the four ledgers)."""
from __future__ import annotations

import json
import time
from collections import Counter
from pathlib import Path

WS = Path(__file__).resolve().parents[1]


def jl(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.exists() else []


def main():
    polls = jl(WS / "logs" / "budget_polls.jsonl")
    blocked_from = "2026-09-24T11:39:32Z"
    restored = next((p["ts_utc"] for p in polls if p["ok"]), None)
    prog = jl(WS / "e2b" / "progress.jsonl")
    cm = json.loads((WS / "scores" / "costmatched_decision.json").read_text()) if (WS / "scores" / "costmatched_decision.json").exists() else None
    fl = jl(WS / "scores" / "judge_flashlite.jsonl")
    D = [
        {"id": "D-E2B", "what": "pre-registered replication sample drawn by E2's frozen rule beyond E2's freeze", "reason": "power (eval-3 power_E2.json)", "evidence": "prereg_iter5_E2B.json"},
        {"id": "D-E2B-comp", "what": "E2-B is 93.5% 25-29 words (the >=30 bin is exhausted after E2's surplus)", "evidence": "e2b/census_E2B.json"},
        {"id": "D-E2B-freeze-env", "what": "code freeze verified on 78 files; or_client.py = E2's D0 post-fix sha; pyproject/uv.lock differ from E's only by project name and E2's pyarrow pin", "evidence": "e2bsrc/code_freeze_check_E2B.json"},
        {"id": "D-E2B-drift", "what": "NOT NEEDED: M2 from E2-A (PASS, combined majority agreement 0.955, track-H flag rate 0.827 within E's CI) was present at 11:20 UTC; its pinned providers were applied to P1/P3/R1 (provider.order, allow_fallbacks=false) through e2bsrc/src_e2b/pe.py (request routing only; panel code unchanged)", "evidence": "e2b/drift_decision.json"},
        {"id": "D-E2B-M1", "what": "NOT NEEDED: M1 present at 11:25 UTC; winner 'NONE: V0 stands' -> no carried H-IMPROVE variant (U4/B-IMPROVE not applicable); V1-V5 scored as development-only rows with freeze_copy/consensus_variants.py (sha verified)", "evidence": "e2b/m1_copy_record.json"},
        {"id": "D-E2B-budget-stop", "what": f"the RUN-LEVEL OpenRouter budget for the 'Test idea' phase ($12, shared by all concurrent artifacts) was exhausted at {blocked_from}; every paid call returned HTTP 403 aii_run_budget_exhausted. This artifact had spent $0.82 of its $9.5 cap. Probes every 15 min from 11:41 to 14:41 UTC, all refused (logs/budget_polls.jsonl); polling stopped at 14:47 because a restore after that could not complete the pre-registered 250-sentence floor (5 batches) before the last paid call at 15:38; restored: {restored}",
         "consequence": "the panel stage completed for no batch end to end (batch 1 stage 1 finished for 14/50 sentences before the stop); per the pre-registered rule an incomplete batch is excluded entirely from the panel regime, so E2-B labels are E's final rule WITHOUT panel votes (tier A against the UNAUDITED MALLS gold; non-equivalent classes UNRESOLVED), where E2's pilot already showed that no L25 CORRECT class exists",
         "evidence": "e2b/budget_stop_batches_complete.json, e2bsrc/work/panel_heldout_quarantine_403.jsonl, logs/budget_polls.jsonl", "completed_batches": [p["batch"] for p in prog]},
        {"id": "D-E2B-fallback-population", "what": "with no panel regime, R_AB has no CORRECT class, so the E2-B analyses run on E2's pre-registered no-panel regime R_A_UNAUDITED (testability_E2.py regime; E2 drift stop rule 'tier-A-only confirmation'): LLM rows, tier A_unaudited_ref, CORRECT = z3-equivalent to the UNAUDITED MALLS gold, ERROR = typed-repair error against it; every such number is SECONDARY and is NOT a faithfulness confirmation (E's panel judged 82% of MALLS gold wrong). The switch rule (R_AB if testable, else R_A_UNAUDITED) is coded in analyse_e2b.choose_population and was fixed before any score-label join; the choice was prompted by solver auto-label COUNTS after 101 sentences (19 CORRECT / 123 ERROR), which the plan allows for testability", "evidence": "analysis/analysis_E2B.json :: analysis_population"},
        {"id": "D-E2B-panel-quarantine", "what": "E's frozen panel_run.py records a sentence as done even when some of its calls failed; records with errors are moved to *_quarantine_403.jsonl after every sweep (src_e2b/quarantine_errors.py) so a resume re-asks them from cache", "evidence": "e2bsrc/work/*_quarantine_403.jsonl"},
        {"id": "D-E2B-judge-fallback", "what": "judge replies without a parseable faithful_prob after the one frozen retry get oriented 0.5 (status 'fallback'), exactly exp 6 T1's pre-declared PRIMARY rule; the T1 SENSITIVITY column *_vfb (median P(faithful) of ok rows with the same verdict) is kept", "evidence": "src/score_e2b.py::cmd_assemble"},
        {"id": "D-E2B-judges-partial", "what": f"flash-lite: {sum(r['p'] is not None for r in fl)} answered units of {len(fl)} requested before the stop (disguised view only; the original view and nano never ran); cost-matched deepseek-v3.2: pilot refused (403) -> decision {cm['decision'] if cm else 'NOT RUN'}; frontier: 10-row pilot only ($4.57e-3/item, 0 parse failures)", "evidence": "scores/judge_*.jsonl"},
        {"id": "D-E2B-S4", "what": "S4_E2B is the CPU-feasible stack (parse_fail, pilot_joint_conflict, pilot_arity_incons, l2_bow, l3_z3, flash-lite disg/orig, nano orig/disg); local LLM judges, NLI round trip and SC-5 need a GPU or extra samples and are recorded as substituted (exp-6 rule); pilot_dangling/rerun_jacc not applicable without a story/rerun", "evidence": "src/analyse_e2b.py::S4_SUBSTITUTED"},
        {"id": "D-E2B-pool-params", "what": "exp-5 pool_scoring with auxiliary readouts switched off exactly as E2-A does (variants=['ALIGN'], k6_seeds=0, famfield=False, medoid_budget_s=0); c_score_align / ALIGN:g_score / l2_bow / l3_z3 go through the unchanged code path; the copy reproduces the stored exp-5 c_score_align and p_peer_text on 50/50 dataset-E rows", "evidence": "e2b/exp5_repro_check.json"},
        {"id": "D-E2B-warm-import", "what": "scoring workers pre-import fol_triage/spaCy before scoring (a cold nltk import on this filesystem takes ~17 s and was interrupted by the 30 s pair alarm, leaving a half-initialised module); no computed value changes", "evidence": "src/score_e2b.py::warm_init"},
        {"id": "D-E2B-transport", "what": "vendored clients' hard-coded openrouter.ai URLs replaced at runtime by $OPENROUTER_BASE_URL (vendor_d.budget.URL, vendor_a.llm.URL), the same transport-only fix as E2's D0; the price catalogue is fetched with the key", "evidence": "src/score_e2b.py::_vendor_budget / cmd_l3"},
        {"id": "D-E2B-lf-controls", "what": "ADDED while blocked: label-free rename invariance of V0 on a sha1 sample of 300 PARSEABLE candidates of any label (E2's frozen control generator), because the pre-registered controls need final-CORRECT parents that the no-panel regime does not produce", "evidence": "scores/controls_lf_scores_E2B.jsonl, analysis/descriptive_nolabels_E2B.json"},
        {"id": "D-E2B-local-judge", "what": "no GPU on this machine (4 CPUs by affinity): the local Qwen3-8B judge is not run and is dropped from S4", "evidence": "aii-use-hardware check"},
        {"id": "D-E2B-GG", "what": "GG not scored: the M1 GG gate was PENDING at the last poll and every paid call was refused after 11:39 UTC", "evidence": "freeze_copy/CONSENSUS_FREEZE_READY.copy.json"},
    ]
    (WS / "deviations.json").write_text(json.dumps({"written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "deviations": D}, indent=1))
    led = []
    for r in jl(WS / "e2bsrc" / "cost_ledger.jsonl"):
        led.append({"ts": r["ts"], "source": "e2bsrc/cost_ledger.jsonl", "phase": r.get("phase"), "model": r.get("model"), "cost_usd": r.get("cost_usd"), "provider": r.get("provider")})
    for r in jl(WS / "exp5src" / "results" / "costs.jsonl"):
        led.append({"ts": r["ts"], "source": "exp5src/results/costs.jsonl", "phase": r.get("component"), "model": r.get("model"), "cost_usd": r.get("cost")})
    for r in jl(WS / "exp5src" / "cache" / "l3_cost_ledger.jsonl"):
        led.append({"ts": r["ts"], "source": "exp5src/cache/l3_cost_ledger.jsonl", "phase": "L3_questionnaire", "model": r.get("model"), "cost_usd": r.get("cost_usd")})
    for r in jl(WS / "scores" / "extra_ledger.jsonl"):
        led.append({"ts": r["ts"], "source": "scores/extra_ledger.jsonl", "phase": r.get("phase"), "model": r.get("model"), "cost_usd": r.get("cost_usd")})
    led.sort(key=lambda r: r["ts"])
    (WS / "cost_ledger_master.jsonl").write_text("".join(json.dumps(r) + "\n" for r in led))
    tot = Counter()
    for r in led:
        tot[r["phase"]] += r["cost_usd"] or 0.0
    print(json.dumps({"n_calls": len(led), "total_usd": round(sum(tot.values()), 5), "by_phase": {k: round(v, 5) for k, v in tot.items()}}))


if __name__ == "__main__":
    main()
