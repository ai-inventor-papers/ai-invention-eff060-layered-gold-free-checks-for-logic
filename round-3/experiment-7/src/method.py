#!/usr/bin/env python3
"""R_COMP: cross-family model agreement (consensus) vs LLM judges on long, heavily conditioned rule sentences.

Entry point of the artifact. The heavy stages live in src/ and run resumably (each writes to results/ or rcomp/):

  S1  rcomp/src/{lexicon,compose,select_rcomp,llm_phases}.py   dataset-3 pre-generation phases (fluency only; D1)
  S2  src/sig_prompt.py + results/prereg_sig.json(.sha256)    SIG pre-registration, git-committed before any SIG call
  S3  src/gen_sig.py pilot|full                               SIG generation (10 few-shot slots, signature block)
  S4  rcomp/src/gen_rcomp.py pilot|full                        FREE generation (dataset 3, unchanged prompt)
  S5  src/label_sig.py label|repair                           SIG labels: pure z3 equivalence to weak/strong readings
  S6  src/testability.py SIG                                  testability + label sha256, committed before any score
  S7a src/score_consensus.py run --cond SIG                    c_score_sig / c_score_align / c_score_nf / c_score_hyb / g
  S7b src/run_judges.py cheap --cond SIG                       flash-lite rubric A, disguised (the bar) + original
  S7c src/run_judges.py frontier [--pilot] --n-rows N          gemini-3.1-pro-preview on a stratified SIG subsample
  S7d src/local_judge_rcomp.py --cond SIG --orig               local Qwen3-8B judge (GPU env .venv_gpu)
  S8  rcomp/src/label_rcomp.py; src/panel_rcomp.py assemble; src/testability.py FREE   FREE solver labels (+ panel, D9)
  S9  src/score_consensus.py run --cond FREE; src/run_judges.py cheap --cond FREE
  S10 src/score_consensus.py rename; src/analyse.py; tests/audit_rederive.py
  S11 method.py build   -> method_out.json (exp_gen_sol_out) from results/rcomp_candidates.jsonl

usage: method.py stages            print the stage list above
       method.py analyse [--B N]   S10 + audit + records + S11 (CPU, $0)
       method.py build             S11 only
The reusable metric functions are in src/consensus_rcomp.py (consensus_exact, consensus_scores).
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from loguru import logger

ROOT = Path(__file__).resolve().parent
RES = ROOT / "results"
RC = ROOT / "rcomp"

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(ROOT / "logs" / "method.log", rotation="30 MB", level="DEBUG")

PRED = ["c_score_sig", "c_score_align", "c_score_nf", "c_score_hyb", "g_align", "g_nf", "judge_cheap_disg", "judge_cheap_orig",
        "judge_frontier_orig", "judge_frontier_disg", "judge_local_disg", "judge_local_orig"]
META = ["row_key", "item_id", "sentence_id", "template_id", "slot", "system", "family", "prompt_variant", "parse_ok",
        "label_source", "label_tier", "matched_reading", "off_signature", "sig_status", "repair_ops", "repair_status",
        "sig_class_id", "sig_class_id_size", "sig_class_id_n_peers", "sig_class_id_n_peers_same_class",
        "sig_class_id_peer_majority_class", "sig_class_id_is_peer_majority", "free_solver_class_id", "free_align_class_id",
        "free_hyb_class_id", "free_align_class_id_size", "free_align_class_id_is_peer_majority", "free_hyb_class_id_size",
        "free_hyb_class_id_is_peer_majority", "n_peers_sig", "n_peers_equal_sig", "n_unknown_sig", "n_peers_hyb",
        "correct_not_equivalent", "ref_flagged", "tier_B_provisional", "cost_usd", "secs_sig", "coverage_status"]


def run(cmd: list[str]) -> None:
    logger.info("$ " + " ".join(cmd))
    subprocess.run(cmd, cwd=ROOT, check=True)


def fmt_pred(v) -> str:
    return "None" if v is None else f"{float(v):.6f}"


@logger.catch(reraise=True)
def build() -> None:
    sents = {s["sentence_id"]: s for s in json.loads((RC / "work" / "rcomp_sentences.json").read_text())}
    rows = [json.loads(l) for l in (RES / "rcomp_candidates.jsonl").read_text().splitlines() if l.strip()]
    A = json.loads((RES / "analysis.json").read_text())
    ds = {"SIG": [], "FREE": []}
    for r in rows:
        s = sents[r["sentence_id"]]
        ex = {"input": json.dumps({"text": s["text"], "candidate_fol": r.get("candidate_fol") or "", "condition": r["condition"]}, ensure_ascii=False),
              "output": str(r["label"])}
        for m in PRED:
            ex[f"predict_{m}"] = fmt_pred(r.get(m))
        for k in META:
            v = r.get(k)
            ex[f"metadata_{k}"] = v
        for k, v in (r.get("strata") or {}).items():
            ex[f"metadata_{k}"] = v
        ex["metadata_condition"] = r["condition"]
        ds[r["condition"]].append(ex)
    sig = A["SIG"]
    meta = {"method_name": "cross-family consensus (SIG-exact, ALIGN, NF-anchored, HYB, graded) vs LLM judges on R_COMP",
            "orientation": "every predict_* score: higher = more likely ERROR; 'None' = not computed (see metadata)",
            "labels": {"SIG": "pure z3 equivalence to the weak or strong template reading (CORRECT / ERROR / READING_CHOICE / OFF_SIGNATURE / UNPARSEABLE)",
                       "FREE": "dataset-3 solver-modulo-alignment rule, tier A only (panel not run, deviation D9): CORRECT / ERROR / UNRESOLVED / UNPARSEABLE / NO_OUTPUT"},
            "primary_test": {k: sig["primary"].get(k) for k in ("n", "n_error", "n_correct", "n_sentences", "auroc_metric", "auroc_comparator",
                                                              "delta", "ci", "p_one_sided", "PASS")},
            "testability": {"SIG": json.loads((RES / "testability_SIG.json").read_text())["verdict"],
                            "FREE": json.loads((RES / "testability_FREE.json").read_text())["verdict"] if (RES / "testability_FREE.json").exists() else None},
            "frozen_params": "exp-5 prereg scoring_params (variants ALIGN + NF-anchored, k=5, tau 0.5, timeout 2000 ms, pair cap 30 s); no tuning on R_COMP",
            "results_files": ["results/analysis.json", "results/tables.md", "results/rcomp_candidates.jsonl", "results/deviations.json"]}
    out = {"metadata": meta, "datasets": [{"dataset": "R_COMP_SIG", "examples": ds["SIG"]}]}
    if ds["FREE"]:
        out["datasets"].append({"dataset": "R_COMP_FREE", "examples": ds["FREE"]})
    (ROOT / "method_out.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
    logger.info(f"method_out.json: SIG {len(ds['SIG'])} rows, FREE {len(ds['FREE'])} rows")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["stages", "analyse", "build"])
    ap.add_argument("--B", type=int, default=2000)
    a = ap.parse_args()
    py = sys.executable
    if a.cmd == "stages":
        print(__doc__)
    elif a.cmd == "analyse":
        run([py, "src/analyse.py", "--B", str(a.B)])
        run([py, "tests/audit_rederive.py"])
        run([py, "src/write_records.py"])
        build()
    else:
        build()


if __name__ == "__main__":
    main()
