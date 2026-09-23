#!/usr/bin/env python3
"""PEER+TEXT on held-out dataset E: end-to-end driver (method AND baselines side by side, one pipeline).

Method (ours): PEER+TEXT = graded cross-family consensus (peer formalisations aligned into the candidate's vocabulary,
claim-unit entailment by finite-model refutation + z3; support / coverage / g_score, unit error codes) fused with the
solver-exact text checks of iteration 1 (L2-bow content accounting, L3 text questionnaire vs z3 role profile) by a
logistic frozen on the iteration-1 screen (fit only where the solver label and the adjudicated label agree).
Baselines on the SAME rows: the disguised and original cheap LLM judge (exp D rubric-A prompt, gemini-2.5-flash-lite;
pre-registered bar), the local Qwen3-8B judge (exp D local bar; labelled secondary because the shared OpenRouter key
ran out), the iteration-1 binary consensus c_score_align, the name-free (NF-anchored) consensus, L2-bow alone, L3 alone,
L1 lint and L2-role (columns only).

Stages (each is resumable and cached; `uv run method.py all` reruns everything that is missing):
  views     src/data_views.py             E blind view (allowlist) + label view + API row order
  api       src/run_api_E.py               L3 questionnaires + flash-lite judges on E (needs the shared key)
  local     src/local_judge_E.py           local Qwen3-8B judge on E (GPU; .venv_gpu)
  screen    src/screen_fit.py compute|fit|freeze   screen features, variant selection, fusion fit, prereg freeze
  score     src/score_E.py run --stage mini|100|all ; assemble
  analyse   src/analyse_E.py               the only label join (guarded by the prereg hash + mtimes)
  outputs   build method_out.json (exp_gen_sol_out) + full/mini/preview variants
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from loguru import logger

ROOT = Path(__file__).resolve().parent
PY = str(ROOT / ".venv" / "bin" / "python")
PY_GPU = str(ROOT / ".venv_gpu" / "bin" / "python")

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(ROOT / "logs" / "method.log", rotation="30 MB", level="DEBUG")


def sh(args: list[str]) -> None:
    logger.info("$ " + " ".join(args))
    r = subprocess.run(args, cwd=ROOT)
    if r.returncode != 0:
        raise RuntimeError(f"stage failed ({r.returncode}): {' '.join(args)}")


def jl(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.exists() else []


def s(x) -> str:
    if x is None:
        return "NA"
    if isinstance(x, float):
        return f"{x:.6f}"
    return str(x)


def build_outputs() -> None:
    """method_out.json in the exp_gen_sol_out schema: one example per E row (input = blind-view JSON, output = the E
    final label joined AFTER the analysis), predict_* = every metric's score (higher = more likely an error)."""
    items = jl(ROOT / "results" / "per_item_E.jsonl")
    labels = {r["row_key"]: r for r in jl(ROOT / "data" / "E_labels.jsonl")}
    blind = {r["row_key"]: r for r in jl(ROOT / "data" / "E_blind.jsonl")}
    analysis = json.loads((ROOT / "results" / "analysis.json").read_text())
    pre = json.loads((ROOT / "results" / "prereg.json").read_text())
    ex = []
    for r in items:
        b = blind[r["row_key"]]
        L = labels[r["row_key"]]
        inp = {"text": b["text"], "candidate_fol": b["candidate_fol"], "system": b["system"], "prompt_variant": b["prompt_variant"],
               "row_key": r["row_key"], "item_id": b["item_id"], "sentence_id": b["sentence_id"]}
        e = {"input": json.dumps(inp, ensure_ascii=False), "output": L["final_label"],
             "predict_peer_text": s(r.get("p_peer_text")), "predict_peer_text_flag": s(r.get("flag")),
             "predict_peer": s(r.get("peer_only")), "predict_text": s(r.get("p_text")),
             "predict_g_score": s(r.get("g_score")), "predict_c_score_nf": s(r.get("c_score_nf")),
             "predict_c_score_align": s(r.get("c_score_align")), "predict_nf_g_score": s(r.get("nf_g_score")),
             "predict_nf_c_score": s(r.get("nf_c_score")), "predict_l2_bow": s(r.get("l2_bow")), "predict_l3": s(r.get("l3_z3")),
             "predict_l1_any": s(r.get("l1_any")), "predict_l2_role": s(r.get("l2_role")),
             "predict_judge_cheap_disg": s(r.get("judge_cheap_disg")), "predict_judge_cheap_orig": s(r.get("judge_cheap_orig")),
             "predict_judge_local_qwen8b_disg": s(r.get("judge_local_qwen8b_disg")),
             "predict_judge_local_qwen8b_orig": s(r.get("judge_local_qwen8b_orig")),
             "metadata_row_key": r["row_key"], "metadata_item_id": r["item_id"], "metadata_sentence_id": r["sentence_id"],
             "metadata_system": r["system"], "metadata_system_class": r["system_class"], "metadata_family_vendor": r["family_vendor"],
             "metadata_stratum": r["stratum"], "metadata_strata": r["strata"], "metadata_fold_E": r["fold_E"],
             "metadata_label_tier": L["label_tier"], "metadata_repair_ops": L["repair_ops"], "metadata_error_ops": L["error_ops"],
             "metadata_reading_choice": L["reading_choice"], "metadata_coverage_status": r["coverage_status"],
             "metadata_unit_codes": [c["code"] + ":" + c.get("unit", "")[:120] for c in (r.get("unit_codes") or [])][:12],
             "metadata_top_code": r.get("top_code"), "metadata_fired_signal": r.get("fired_signal"),
             "metadata_model_used": r.get("model_used"), "metadata_n_unknown": r.get("n_unknown"),
             "metadata_n_peers_used": r.get("n_peers_used"), "metadata_peer_unavailable": r.get("peer_unavailable"),
             "metadata_support": r.get("support"), "metadata_coverage": r.get("coverage"),
             "metadata_medoid_ops": r.get("medoid_ops"), "metadata_judge_local_type": r.get("judge_local_qwen8b_disg_type"),
             "metadata_cost_usd": (r.get("cost_usd_peer_text") or 0.0), "metadata_judge_cost_usd": r.get("judge_cost_usd"),
             "metadata_secs": (r.get("secs_pairs") or 0.0) + (r.get("secs_text") or 0.0),
             "metadata_prereg_sha256": r["prereg_sha256"]}
        ex.append(e)
    heads = {k: {kk: vv for kk, vv in v.items() if kk in ("n", "n_error", "n_correct", "metrics")} for k, v in analysis["a_tables"].items()}
    out = {"metadata": {
        "method_name": "PEER+TEXT (graded cross-family consensus fused with solver-exact text checks), frozen on the screen, scored once on E",
        "prereg_sha256": (ROOT / "results" / "prereg.sha256").read_text().split()[0],
        "peer_variant": pre["variant"], "F1_failed_on_screen": pre["selection_evidence"]["F1_failed"],
        "fusion": pre["frozen"]["fusion"], "text_only": pre["frozen"]["text_only"],
        "orientation": "every predict_* is oriented so that higher = more likely an error; NA = not available",
        "headline_auroc_tables": heads, "criteria": analysis["criteria"],
        "p_tests": json.loads((ROOT / "results" / "p_tests.json").read_text()),
        "workspace": str(ROOT)},
        "datasets": [{"dataset": "E_heldout_candidates", "examples": ex}]}
    (ROOT / "method_out.json").write_text(json.dumps(out, ensure_ascii=False))
    logger.info(f"method_out.json: {len(ex)} examples, {(ROOT / 'method_out.json').stat().st_size / 1e6:.1f} MB")


@logger.catch(reraise=True)
def main():
    stage = sys.argv[1] if len(sys.argv) > 1 else "all"
    if stage in ("views", "all"):
        sh([PY, "src/data_views.py"])
    if stage in ("api", "all"):
        sh([PY, "src/run_api_E.py"])
    if stage in ("local", "all") and Path(PY_GPU).exists():
        sh([PY_GPU, "src/local_judge_E.py"])
    if stage in ("screen", "all"):
        if not (ROOT / "results" / "prereg.json").exists():
            sh([PY, "src/screen_fit.py", "compute"])
            sh([PY, "src/screen_fit.py", "fit"])
            sh([PY, "src/screen_fit.py", "freeze"])
    if stage in ("score", "all"):
        for st in ("mini", "100", "all"):
            sh([PY, "src/score_E.py", "run", "--stage", st])
        sh([PY, "src/score_E.py", "assemble"])
    if stage in ("analyse", "all"):
        sh([PY, "src/analyse_E.py"])
    if stage in ("outputs", "all"):
        build_outputs()


if __name__ == "__main__":
    main()
