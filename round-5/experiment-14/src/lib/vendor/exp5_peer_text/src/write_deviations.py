#!/usr/bin/env python3
"""Writes results/deviations.json: every departure from the artifact plan, when it was decided (before/after the prereg
freeze, before/after the E label join) and its consequence. No silent deviations."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
R = ROOT / "results"
fit = json.loads((R / "screen_fit.json").read_text())
ph = json.loads((R / "posthoc_nf_fusion.json").read_text()) if (R / "posthoc_nf_fusion.json").exists() else {}
dev = [
    {"id": "D1", "when": "before freeze (18:00 UTC)", "what": "Shared OpenRouter key hit its $50/day limit (limit_remaining 0) minutes after "
     "launch; only 699/700 E L3 questionnaires and 20 flash-lite judge units completed. A key monitor (src/key_monitor.sh) kept "
     "checking every 5 min and never saw budget return before the analysis. At 19:07 UTC the platform replaced the key; the "
     "replacement key was already at its $50 daily limit at 19:08 (limit_remaining 0, a test call returned 403 'Key limit exceeded'); "
     "the monitor was restarted on the replacement key (every 2 min) to re-launch the resumable flash-lite judge + disguised L3; polled every 2 min 19:10-22:13 UTC, limit_remaining stayed 0, so no further API call was made.",
     "consequence": "The pre-registered bar (flash-lite disguised judge) is UNTESTABLE on E (20 rows). Per fallback 6 (pre-registered "
     "in prereg.json a_judge_fallback) the iteration-1 exp D LOCAL judge (Qwen3-8B, rubric B, greedy; screen AUROC .757 vs .777 "
     "for flash-lite) is the LABELLED SECONDARY BAR on all rows. Criterion (a)/(c) against flash-lite: untestable. The disguised L3 "
     "contamination arm and judge_cheap_orig did not run."},
    {"id": "D2", "when": "screen, before freeze", "what": "F1 FAILED under the pre-registered selection rule: for both NF variants "
     ">10% of AGREE track-L CORRECT items tie at g=1, so the deterministic FA-0.10 threshold flags nothing (ROLE_PERMUTE recall 0).",
     "consequence": "Per fallback 3 the peer signal is graded consensus with the iteration-1 aligner (variant ALIGN) fused with "
     "c_score_align; the shared-aligner confound with the solver labeller stays OPEN. NF-anchored still scored on E as a reported "
     "column.", "evidence": fit.get("variant_evidence")},
    {"id": "D3", "when": "after the E analysis (POST HOC)", "what": "Fractional tie-breaking (exact matched FA) shows the F1 failure "
     "was a threshold-tie artefact: NF-anchored passes both gates on the screen (RENAME FA .074, ROLE_PERMUTE recall .771), NF-pure "
     "fails ROLE_PERMUTE (.186). The NF-based fusion was fitted on the screen with the same procedure and applied to E.",
     "consequence": "Reported ONLY as a labelled post-hoc sensitivity (results/posthoc_nf_fusion.json).",
     "evidence": ph.get("fractional_selection_gates_screen"), "E": ph.get("E")},
    {"id": "D4", "when": "analysis, after first analysis run", "what": "P1 matched-FA recall and P4 rewrite flags: deterministic "
     "thresholds are degenerate for tied scores (recall 0 by construction). Added fractional tie-breaking (expected value of "
     "randomised tie-breaking, FA exactly 0.10/0.20); P1 verdict basis = fractional. Deterministic numbers kept in analysis.json.",
     "consequence": "P1 moves from REFUTED (artefact) to INCONCLUSIVE; P4 stays REFUTED under both."},
    {"id": "D5", "when": "before any scoring (unit tests)", "what": "Name-free signature extended with a semantic clamp profile, exact "
     "Murty k-best, anchored-cost rule, NEG code = literal-polarity toggle, mapping acceptance by finite-model-unrefuted count, "
     "coverage as mean over peers, rows keyed by row_key (item_id not unique: 115 zero/few-shot twins).",
     "consequence": "Listed in prereg_selection.json (sha256-frozen before screen scoring)."},
    {"id": "D6", "when": "screen regression", "what": "c_score_align (all-pool, exp-C pool definition) track-L AUROC .8597 vs exp C .866 "
     "(tolerance +-.005 missed by .0015). Likely cause: the dataset-E parser (fixed <-> / ⊕ handling) replaces exp C's parser and "
     "canonical formula strings replace raw strings. L2-bow and L3 reproduce exp A on 903/903 items exactly.",
     "consequence": "Reported; not corrected."},
    {"id": "D7", "when": "E scoring", "what": "medoid_ops typed-repair budget 2 s (plan: 10 s) to fit the run window.",
     "consequence": "More COMPOUND/TIMEOUT medoid readouts (second readout only)."},
    {"id": "D8", "when": "analysis", "what": "Bootstrap sizes: B=2000 for all AUROC / ΔAUROC CIs; B=1000 for P1 recall-difference and P2 "
     "Spearman CIs; B=400 for the P3 logistic-interaction CIs; B=500 for the system-level tau and sensitivity tables (runtime).",
     "consequence": "Wider Monte-Carlo error on those CIs only."},
    {"id": "D9", "when": "after freeze, before the label join", "what": "score_E.py assemble edited to carry the NF-anchored columns "
     "(no change to any frozen score); analyse_E.py written/extended after the freeze (it reads prereg.json for every rule).",
     "consequence": "prereg.json code_sha1 lists the frozen versions; git history shows the edits."},
    {"id": "D10", "when": "freeze", "what": "Fusion / TEXT thresholds are set in-sample on the screen AGREE track-L CORRECT items; "
     "screen sentences are short, E sentences long.", "consequence": "Threshold-based numbers (FA, precision) on E carry the scale "
     "shift; AUROC is unaffected. See analysis k_misc."},
    {"id": "D11", "when": "plan scope", "what": "Only R_AB and R_A regimes are scored here; R_ADJ / R_COMP, nested cross-fitted Δ over "
     "S4 and the frontier-judge ratio are iteration-3 joins (per_item_E.jsonl carries row_key, item_id and fold_E).",
     "consequence": "Criterion (b) and the R_ADJ/R_COMP halves of (a)/(c) are not tested by this artifact."},
]
(R / "deviations.json").write_text(json.dumps(dev, indent=1, ensure_ascii=False, default=float))
print(len(dev))
