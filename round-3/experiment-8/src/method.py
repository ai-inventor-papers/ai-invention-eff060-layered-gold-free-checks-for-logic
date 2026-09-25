#!/usr/bin/env python3
"""Rename-invariant cross-family consensus (PEER_HYB) and per-error-type sensitivity of every gold-free NL->FOL metric.

METHOD (ours):  PEER_HYB consensus -- a candidate formula agrees with a peer formula of the same sentence (another model
                family) if the iteration-1 name-similarity ALIGN map (eqmv) OR the exp-5 name-free NF-anchored map gives a
                z3-verified equivalence; c_score_hyb = 1 - share of agreeing peers (leave-one-family-out), g_score_hyb =
                graded claim-unit consensus under the composite map. Library: src/consensus_lib.py.
BASELINES (same rows, same pipeline): ALIGN consensus (c_score_align, the iteration-2 survivor), NF-anchored consensus,
                graded g, PEER+TEXT fusion, TEXT-only (L2-bow, L3), SC-5 local self-consistency, local round-trip NLI/embedding,
                local LLM judges (Qwen3-8B, Llama-3.1-8B; disguised), flash-lite judge (disguised), S4 stack, parse rate and
                the user's pilot structural metrics (reference rows).

Stages (each resumable; outputs under results/):
  score      src/run_scoring.py screen|E        pair engine on the screen and on dataset E (+ PERTURB E-base rows)   [CPU]
  gate       src/gate_check.py                  regression gate vs exp 5 frozen columns
  freeze_a   src/freeze_prereg_hyb.py           PREREG_HYB (before any label join)
  part_a     src/analyse_hyb.py                 screen thresholds, rename FA, over-alignment, SELECTION, E AUROCs, audit
  calib      src/prep_calib.py                  E calibration rows for the nf4 local judges / flash-lite threshold
  api        src/run_api_perturb.py             flash-lite judge on PERTURB + calibration rows (OpenRouter, ~$0.35)
  cpu_b      src/perturb_cpu.py                 parse / pilot / L2 / L3 / PEER+TEXT / SC-5 on PERTURB
  gpu_b      src/perturb_gpu.py                 local judges + round trip (nf4) on PERTURB + calibration rows    [GPU]
  s4         src/fit_s4_perturb.py              S4_local full-E fit (before PERTURB labels)
  freeze_b   src/freeze_prereg_perturb.py       PREREG_PERTURB (thresholds, statistics, predictions)
  part_b     src/analyse_perturb.py             per operator x polarity sensitivity, DOWN/UP, invariance, trade-off
  part_c     src/typing_perturb.py              error-type identification (peer medoid vs oracle vs judges)
  tests      pytest tests/                      library unit tests (20 known pairs)
  output     method.py output                   -> method_out.json (exp_gen_sol_out)
usage: .venv/bin/python method.py run [--from STAGE]   |   .venv/bin/python method.py output
"""
from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
from pathlib import Path

from loguru import logger

ROOT = Path(__file__).resolve().parent
RES = ROOT / "results"
PY = str(ROOT / ".venv" / "bin" / "python")
sys.path.insert(0, str(ROOT / "src"))

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(ROOT / "logs" / "method.log", rotation="30 MB", level="DEBUG")

STAGES = [
    ("score", [[PY, "src/run_scoring.py", "E", "--stage", "all"], [PY, "src/run_scoring.py", "screen", "--stage", "all"]]),
    ("gate", [[PY, "src/gate_check.py"]]),
    ("freeze_a", [[PY, "src/freeze_prereg_hyb.py"]]),
    ("part_a", [[PY, "src/analyse_hyb.py"]]),
    ("calib", [[PY, "src/prep_calib.py"]]),
    ("api", [[PY, "src/run_api_perturb.py"]]),
    ("cpu_b", [[PY, "src/perturb_cpu.py"]]),
    ("gpu_b", [[PY, "src/perturb_gpu.py", "--which", "judges_disg,verb,nli"]]),
    ("s4", [[PY, "src/fit_s4_perturb.py"]]),
    ("freeze_b", [[PY, "src/freeze_prereg_perturb.py"]]),
    ("part_b", [[PY, "src/analyse_perturb.py"]]),
    ("part_c", [[PY, "src/typing_perturb.py"]]),
    ("tests", [[PY, "-m", "pytest", "-q", "-c", "pytest.ini", "tests"]]),
]
DONE_MARK = {"freeze_a": RES / "prereg_hyb.sha256", "freeze_b": RES / "prereg_perturb.sha256", "calib": ROOT / "data" / "E_calib_units.jsonl",
             "s4": RES / "s4_perturb_coefs.json"}


def run(start: str | None):
    go = start is None
    for name, cmds in STAGES:
        go = go or name == start
        if not go:
            continue
        if name in DONE_MARK and DONE_MARK[name].exists():
            logger.info(f"{name}: already done ({DONE_MARK[name].name}); frozen files are never overwritten")
            continue
        for c in cmds:
            logger.info(f"{name}: {' '.join(c[1:])}")
            subprocess.run(c, cwd=ROOT, check=True)


# ================================================================================================ method_out.json
def s(x) -> str:
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "NA"
    if isinstance(x, bool):
        return str(x)
    if isinstance(x, float):
        return f"{x:.6f}"
    return str(x)


def build_output():
    import an_common as C
    sel = json.loads((RES / "selection.json").read_text())
    frozen = sel.get("frozen_score")
    frozen_label = sel.get("frozen_variant") or "NONE_ELIGIBLE"
    blind = {r["row_key"]: r for r in C.jl(C.DATA / "exp5" / "E_blind.jsonl")}
    ds = []
    # ---- dataset E (development for the selection; real generator outputs)
    ex = []
    for r in C.jl(RES / "per_item_hyb_E.jsonl"):
        b = blind[r["row_key"]]
        e = {"input": json.dumps({"text": b["text"], "candidate_fol": b["candidate_fol"], "system": b["system"],
                                  "prompt_variant": b["prompt_variant"]}, ensure_ascii=False),
             "output": r["final_label"], "metadata_fold": "E", "metadata_row_key": r["row_key"], "metadata_sentence_id": r["sentence_id"],
             "metadata_stratum": r["stratum"], "metadata_label_tier": r["label_tier"], "metadata_y_R_AB": r["y_AB"],
             "metadata_system_class": r["system_class"], "metadata_coverage_status": r["coverage_status"], "metadata_n_peers": r["n_peers"],
             "predict_c_score_hyb": s(r["c_hyb"]), "predict_g_score_hyb": s(r["g_hyb"]), "predict_c_score_nf": s(r["c_nf"]),
             "predict_c_score_align": s(r["c_align"]), "predict_g_score_align": s(r["g_align"]), "predict_g_score_nf": s(r["g_nf"]),
             "predict_frozen_invariant": s(r.get(frozen)) if frozen else frozen_label}
        ex.append(e)
    ds.append({"dataset": "E_heldout_candidates", "examples": ex})
    # ---- PERTURB (mutants, controls, bases): every Part B metric
    pb = C.jl(RES / "perturb_scores.jsonl")
    A = json.loads((RES / "analysis_perturb.json").read_text())
    mets = A["metrics"]
    ex = []
    rows = {r["item_id"]: r for r in C.jl(C.DATA / "perturb_rows.jsonl")}
    for u in pb:
        is_base = u["key"].startswith("PB:")
        src = rows.get(u["item_id"]) if not is_base else None
        text = src["text"] if src else next(r["text"] for r in rows.values() if r["base_item_id"] == u["base"])
        e = {"input": json.dumps({"text": text, "candidate_fol": u["fol"]}, ensure_ascii=False),
             "output": "ERROR" if u["y"] == 1 else "CORRECT",
             "metadata_fold": "PERTURB_BASE" if is_base else ("PERTURB" if u["y"] == 1 else "PERTURB_CONTROL"),
             "metadata_key": u["key"], "metadata_base_item_id": u["base"], "metadata_operator": u["operator"],
             "metadata_op_fine": u["op_fine"], "metadata_control_type": u["control_type"], "metadata_polarity": u["polarity"],
             "metadata_matched_pair_id": u["matched_pair_id"], "metadata_subtype": u["subtype"], "metadata_base_status": u["base_status"],
             "metadata_base_endorsed": u.get("base_endorsed"),
             "predict_frozen_invariant": s(u.get(frozen)) if frozen else frozen_label}
        for m in mets:
            e[f"predict_{m}"] = s(u.get(m)) if u.get(m + "__status") != "fail" else ("FAIL(" + s(u.get(m)) + ")")
        e["predict_c_score_hyb"] = e.pop("predict_c_hyb", "NA")
        e["predict_g_score_hyb"] = e.pop("predict_g_hyb", "NA")
        e["predict_c_score_nf"] = e.pop("predict_c_nf", "NA")
        e["predict_c_score_align"] = e.pop("predict_c_align", "NA")
        ex.append(e)
    ds.append({"dataset": "PERTURB_suite", "examples": ex})
    # ---- screen items, exp D rewrites, probes (consensus variants)
    ex_rw, ex_sc = [], []
    labs = json.loads((C.DATA / "screen" / "screen_adjudicated_labels.json").read_text())
    inv = {x["rw_id"]: x for x in json.loads((C.DATA / "invariance_items.json").read_text())}
    items = {x["item_id"]: x for x in json.loads((C.DATA / "screen" / "screen_items.json").read_text())}
    probes = {f"PR:{p['probe']}:{p['base_item_id']}": p for p in json.loads((C.DATA / "exp5" / "screen_probes.json").read_text())}
    for r in C.jl(RES / "per_item_screen_hyb.jsonl"):
        k = r["key"]
        if k.startswith("M:"):
            continue
        if k.startswith("RW:"):
            x = inv[k[3:]]
            text, fol, fold = x["text"], x["candidate_fol"], "REWRITE_EXPD"
            out = labs.get(x["base_item_id"], {}).get("final_label") or "UNLABELLED"  # a meaning-preserving rewrite inherits its base label
            base = x["base_item_id"]
            extra = {"metadata_rewrite_family": x["family"], "metadata_base_item_id": base,
                     "metadata_base_label": labs.get(base, {}).get("final_label")}
        elif k.startswith("PR:"):
            p = probes[k]
            b = items[p["base_item_id"]]
            text, fol, fold, out = b["text"], p["fol"], "SCREEN_PROBE", "ERROR"
            extra = {"metadata_probe": p["probe"], "metadata_base_item_id": p["base_item_id"]}
        else:
            b = items.get(k)
            if b is None:
                continue
            text, fol, fold, out = b["text"], b["candidate_fol"], "SCREEN", r["label"] or "UNLABELLED"
            extra = {"metadata_track": b["track"], "metadata_system": b["system"]}
        e = {"input": json.dumps({"text": text, "candidate_fol": fol}, ensure_ascii=False), "output": out, "metadata_fold": fold,
             "metadata_key": k, "metadata_sentence_id": r["sentence_id"], **{kk: v for kk, v in extra.items() if v is not None},
             "predict_c_score_hyb": s(r["c_hyb"]), "predict_g_score_hyb": s(r["g_hyb"]), "predict_c_score_nf": s(r["c_nf"]),
             "predict_c_score_align": s(r["c_align"]), "predict_frozen_invariant": frozen_label if not frozen else s(r.get(frozen))}
        (ex_rw if fold == "REWRITE_EXPD" else ex_sc).append(e)
    ds.append({"dataset": "expD_rewrites_screen", "examples": ex_rw})
    ds.append({"dataset": "screen_items_and_probes", "examples": ex_sc})
    out = {"metadata": {"method_name": "PEER_HYB rename-invariant cross-family consensus + PERTURB per-error-type sensitivity",
                        "description": "Oriented scores (higher = more likely ERROR). E: real generator outputs with panel/solver labels "
                                       "(development for the HYB/NF selection). PERTURB: synthetic typed mutants/controls (never pooled "
                                       "with E). See README.md and results/.",
                        "selection": {k: sel[k] for k in ("frozen_variant", "note", "E_strat_auroc_R_AB")},
                        "prereg_hyb_sha256": C.sha256_file(RES / "prereg_hyb.json"),
                        "prereg_perturb_sha256": C.sha256_file(RES / "prereg_perturb.json"),
                        "predict_frozen_invariant": "NONE_ELIGIBLE = no rename-invariant variant passed the pre-registered rule; the R_COMP read uses ALIGN (predict_c_score_align)" if not frozen else frozen},
           "datasets": ds}
    (ROOT / "method_out.json").write_text(json.dumps(out, ensure_ascii=False))
    logger.info(f"method_out.json: {[(d['dataset'], len(d['examples'])) for d in ds]}")


@logger.catch(reraise=True)
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["run", "output"])
    ap.add_argument("--from", dest="start", default=None)
    a = ap.parse_args()
    if a.cmd == "run":
        run(a.start)
        build_output()
    else:
        build_output()


if __name__ == "__main__":
    main()
