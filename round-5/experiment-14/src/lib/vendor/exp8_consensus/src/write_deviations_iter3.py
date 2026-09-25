#!/usr/bin/env python3
"""Writes results/deviations.json for THIS artifact (iteration 3, T3+T5): every departure from the artifact plan, when it
was decided relative to the two freezes / the label joins, and its consequence. (src/write_deviations.py is exp 5's
vendored file and is not used.)"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
R = ROOT / "results"


def load(p):
    p = R / p
    return json.loads(p.read_text()) if p.exists() else {}


sel = load("selection.json")
gate = load("regression_gate.json")
ap = load("analysis_perturb.json")
dev = [
    {"id": "D-RESTART", "when": "02:05-02:56 UTC (between Part A scoring and the freeze)",
     "what": "The container was migrated mid-run: .venv and the shared HF cache were wiped, the GPU changed from a 21 GB card to a "
             "16 GB RTX 2000 Ada, and a first GPU job (bf16, 20 rows) died with the old machine.",
     "consequence": ".venv rebuilt from requirements.txt; models re-downloaded (scripts/download_models.sh); the 20 bf16 pilot rows "
                    "are archived in results/perturb_scores/_bf16_pilot_prev_machine/ and not used."},
    {"id": "D-GPU16", "when": "before freeze_b", "what": "Qwen3-8B and Llama-3.1-8B do not fit in 16 GB at bf16; both run bitsandbytes nf4 "
     "(4-bit, bf16 compute). exp 6's E scores for these judges were bf16.",
     "consequence": "PRIMARY thresholds for the local judges and round-trip metrics are fixed on nf4 scores of 864 E R_AB LLM CORRECT "
                    "rows (EC:, data/E_calib_units.jsonl) with the frozen rule, so thresholds and PERTURB scores share one quantisation. "
                    "400 E ERROR rows were also scored to measure the nf4 vs bf16 shift."},
    {"id": "D-JUDGE-E", "when": "before freeze_b", "what": "Frozen judge_cheap_disg covers only 1,106 E rows (exp 5's key died). The flash-lite "
     "threshold uses the same 864 EC CORRECT rows scored here (exp 6's exp-D disguise of E).", "consequence": "~$0.06 extra API spend."},
    {"id": "D-S4FULL", "when": "before freeze_b (plan-declared)", "what": "S4_local on PERTURB = ONE full-E fit (no OOF folds exist for PERTURB rows); "
     "features = exp 6 S4_local minus pilot_rerun_jacc (no rerun analogue) and minus the *_orig judges (the PERTURB judge arm is disguised-only).",
     "consequence": "S4_local PERTURB numbers are a labelled deviation; inputs on PERTURB are nf4 while the fit used bf16 E features."},
    {"id": "D-ORIG", "when": "plan", "what": "Local judges' ORIGINAL-text condition not run on PERTURB (time); disguised only, as the plan specifies.",
     "consequence": "No contamination (orig vs disguised) contrast on PERTURB."},
    {"id": "D-L3-RCOMP", "when": "Part B", "what": "L3 (l3_z3) on the 100 R_COMP bases would need ~100 new flash-lite questionnaires; not run "
     "(the shared key is also serving sibling artifacts).", "consequence": "l3_z3 = NA on R_COMP rows (counted in coverage_perturb.csv); "
     "p_peer_text / p_text on R_COMP use z = 0 for the missing L3 feature (exp 5 frozen rule)."},
    {"id": "D-PILOT-DOCS", "when": "Part B", "what": "Pilot metrics on PERTURB use artificial documents (same system x sha1 bucket of ~20 bases; the "
     "bucket key did not separate E and R_COMP bases because base_source is 'RCOMP', not 'R_COMP'). pilot_rerun_jacc has no analogue.",
     "consequence": "Pilot metrics are REFERENCE rows only (user asked for them 'for reference'), as pre-registered."},
    {"id": "D-GATE", "when": "Step 2c", "what": "Regression gate PASSED (c_align 99.81%, c_nf 99.91% of 8,507 rows within 1e-9).",
     "consequence": "Frozen exp 5 columns remain the headline for ALIGN and NF; HYB uses the re-derived pair verdicts.",
     "evidence": {k: v for k, v in gate.items() if not isinstance(v, dict)}},
    {"id": "D-SELECTION", "when": "after freeze_a (pre-registered outcome)", "what": "Neither HYB nor NF-anchored is eligible: both exceed RENAME FA "
     "0.10 on PERTURB RENAME_SYN / RENAME_NONCE at the screen-derived thresholds (they pass on exp D RENAME).",
     "consequence": "Per the prereg, nothing is frozen and the sibling's R_COMP read uses ALIGN. The failing FA is dominated by the "
                    "unmutated references themselves being flagged (base FA ~ rename FA for NF; NF flip rate ~0.005), i.e. a threshold-"
                    "transfer / reference-endorsement problem rather than rename sensitivity for NF; HYB additionally has a real rename "
                    "flip rate (~0.15). This interpretation is POST HOC and does not change the selection.",
     "evidence": sel.get("evidence")},
    {"id": "D-TYPING-MEDOID", "when": "Part C", "what": "No variant frozen -> the peer medoid is the ALIGN (eqmv) medoid of the full peer pool (prereg: "
     "'R_COMP read uses ALIGN'); the HYB medoid is reported as a secondary typer.", "consequence": "none"},
    {"id": "D-BOOT", "when": "analysis", "what": "stats.cluster_boot_mean vectorised (per-cluster sums, one B x K draw from default_rng(0)); "
     "Part A numbers computed with the earlier per-call Boot implementation (same estimator, different random stream).",
     "consequence": "Monte-Carlo differences in CI endpoints only (<0.01)."},
    {"id": "D-FRONTIER", "when": "plan-declared", "what": "Frontier / API SC and round-trip arms not run on PERTURB (budget belongs to T1); flash-lite "
     "is the only API judge.", "consequence": "API-judge row = flash-lite (disguised)."},
]
if ap.get("available"):
    dev.append({"id": "D-GPU-COVERAGE", "when": "Part B", "what": f"GPU arm availability at analysis time: {ap['available']}",
                "consequence": "metrics not available are listed as 'not run' in coverage_perturb.csv"})
(R / "deviations.json").write_text(json.dumps(dev, indent=1, ensure_ascii=False, default=str))
print(len(dev))
