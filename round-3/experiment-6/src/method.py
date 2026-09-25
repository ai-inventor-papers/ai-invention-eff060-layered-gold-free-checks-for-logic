#!/usr/bin/env python3
"""Every baseline re-run on the held-out NL->FOL set E (iteration 2, gen_art experiment 6 = plan gen_plan_experiment_2).

Stages (idempotent; every LLM call cached in results/llm_cache.jsonl, every score appended to results/scores/*.jsonl):
  prep        label-blind load of E; parse check (fol.py + z3); nonce disguise (exp D disguise_item) -> data/E_units.json
  prereg      write prereg_baselines.json (models, prompts, sha1s, feature sets, folds, thresholds, B2 spec, caps)
  frame       draw the 300-row frontier frame (ONLY label read before scoring; disclosed) + label-vector sha1s,
              then FREEZE prereg (sha256)
  judges      judge_cheap (flash-lite, rubric A JSON) + judge_cheap2 (gpt-4.1-nano P(YES)), orig + disg   [--limit N]
  sc_gen      SC-5 samples: gpt-4.1-nano, T=0.7, 5 per sentence, dataset-E few-shot prompt              [--limit N]
  verbalise   round-trip API verbaliser (flash-lite, VERBALISE prompt)                                    [--limit N]
  strong      judge_strong (gemini-3.1-pro-preview, effort low) orig + disg on the frontier frame         [--limit N]
  retest      judge_cheap_disg test-retest on 200 sha1-chosen rows (cache-bypass nonce in the key only)
  cpu         parse_fail + the user's pilot structural metrics (adapted documents)
  sc_score    SC-5 scoring: equivalence modulo vocabulary of candidate vs samples (z3, pair cache)
  local_judges / local_strong / local_verb / local_sc   F-KEY local path (Qwen3-8B, Llama-3.1-8B, Qwen3-14B-nf4; GPU)
  nli         NLI (2 checkpoints, both directions) + mpnet cosine for a verbaliser (--which local|api; GPU)
  b2_build    B2 worlds for every formula of every set (CPU, z3)
  b2_read     B2 reader (--which dev,gate,screen,unbatched,rewrites,Eref,E; local Qwen3-8B, frozen prompt in prereg_b2.json)
  b2_gate_report  reader gate + B2 thresholds from the screen (no E label)
  sc_invariance   SC-5 on the shared rewrites from exp C's existing samples
  t2_repro / retest_sibling   local-judge reproducibility vs exp D / test-retest vs the sibling experiment
  b2_think    POST-HOC diagnostic: thinking-mode reader on the screen gate items (not pre-registered)
  s4          feature table E_baseline_features.jsonl + folds_E.json (label-free)
  analysis    S4 fits + all tables (src/analysis_E.py; the only place labels are joined), summary.md, method_out.json
Usage: PYTHONHASHSEED=0 .venv/bin/python method.py --stage NAME [--limit N]
"""
from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import math
import os
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

os.environ.setdefault("PYTHONHASHSEED", "0")
os.environ.setdefault("NLTK_DATA", str(Path(__file__).resolve().parent / "data" / "nltk_data"))
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
sys.setrecursionlimit(10000)

from loguru import logger  # noqa: E402

from src.common import DATA, LOGS, RES, ROOT, detect_cpus, jdump, jload, norm, read_jsonl, sha1, set_ram_limit  # noqa: E402

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(str(LOGS / "run.log"), rotation="30 MB", level="DEBUG")

NUM_CPUS = detect_cpus()
WORKERS = max(1, min(12, NUM_CPUS - 2))
# T1: label-blind pilots write to results/pilot (T1_SCORES_DIR) so that every file in results/scores post-dates the
# prereg_T1 freeze; the LLM cache (results/llm_cache.jsonl) makes the later full sweep reuse the pilot calls for free
SCORES = Path(os.environ["T1_SCORES_DIR"]) if os.environ.get("T1_SCORES_DIR") else RES / "scores"
SCORES.mkdir(parents=True, exist_ok=True)
EXPD = Path("../../../round-1/experiment-4/src")
EXPA = Path("../../../round-1/experiment-1/src")
EXPC = Path("../../../round-1/experiment-3/src")
PREREG = ROOT / "prereg_baselines.json"
PREREG_SHA = ROOT / "prereg_baselines.sha256"
FEWSHOT = json.loads((Path("../../../round-1/dataset-1/src")
                      / "prompts" / "fewshot_v1.txt").read_text())


# ------------------------------------------------------------------ io helpers
def append_jsonl(p: Path, rows: list[dict]) -> None:
    with p.open("a") as f:
        for r in rows:
            f.write(json.dumps({"ts": time.time(), **r}, ensure_ascii=False) + "\n")


def load_scores(name: str) -> dict:
    """{key: last row} of results/scores/<name>.jsonl (append-only; the last line for a key wins)."""
    p = SCORES / f"{name}.jsonl"
    out = {}
    if p.exists():
        for r in read_jsonl(p):
            out[r["key"]] = r
    return out


def units() -> list[dict]:
    return jload(DATA / "E_units.json")


def prereg() -> dict:
    if not PREREG_SHA.exists():
        raise RuntimeError("prereg not frozen: run --stage prereg then --stage frame")
    return jload(PREREG)


def require_frozen() -> dict:
    pre = prereg()
    h = hashlib.sha256(PREREG.read_bytes()).hexdigest()
    if h != PREREG_SHA.read_text().split()[0]:
        raise RuntimeError("prereg_baselines.json changed after freeze")
    return pre


# =====================================================================================================================
def _prep_worker(args):
    iid, text, fol = args
    import sys as _s
    _s.setrecursionlimit(10000)
    ok = strict_parse_ok(fol)
    return iid, ok


def strict_parse_ok(fol) -> bool:
    """labeller.parse_ok AND no atom without a name (fol.py accepts a dangling trailing connective, e.g. 'A(x) ∧', by
    reading an atom named None at end of input; such truncated outputs are unparseable)."""
    from src.labeller.fol import parse
    from src.labeller.labeller import parse_ok
    from src.labeller.repair_census import atoms
    if not fol or not fol.strip() or not parse_ok(fol):
        return False
    try:
        return all(isinstance(a[1], str) and a[1] for a in atoms(parse(fol)))
    except Exception:  # noqa: BLE001
        return False


def _disg_worker(chunk):
    import sys as _s
    _s.setrecursionlimit(10000)
    from src.disguise import disguise_item
    out = []
    for k, text, fol in chunk:
        try:
            d = disguise_item(text, fol or None)
        except Exception as e:  # noqa: BLE001 - counted as a disguise failure, fallback to E's own disguise
            d = {"text_d": None, "fol_d": None, "ok": False, "fail_reasons": [f"exception:{str(e)[:80]}"]}
        out.append((k, {"text_d": d["text_d"], "fol_d": d["fol_d"], "ok": d["ok"], "fail_reasons": d["fail_reasons"],
                        "leak_text": d.get("leak_text"), "leak_formula": d.get("leak_formula")}))
    return out


def stage_prep():
    """Label-blind unit table: item ids, text, candidate, parse flag, disguised pair (+ fallback), strata, system."""
    import multiprocessing as mp
    from concurrent.futures import ProcessPoolExecutor
    from src.e_pool import load_E, pool_of, sysvar, fold_of_sentence
    rows = load_E(blind=True)
    logger.info(f"E blind rows {len(rows)}; pools {Counter(pool_of(r) for r in rows)}")
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=WORKERS, mp_context=mp.get_context("spawn")) as pool:
        pok = dict(pool.map(_prep_worker, [(r["metadata_item_id"], r["text"], r["candidate_fol"]) for r in rows], chunksize=64))
    logger.info(f"parse check {time.time()-t0:.0f}s: parseable {sum(pok.values())}/{len(rows)}")
    # disguise: dedupe identical (text, fol) pairs (the disguise is a deterministic function of both)
    uniq = {}
    for r in rows:
        if pok[r["metadata_item_id"]]:
            uniq.setdefault(sha1(r["text"] + "||" + r["candidate_fol"]), (r["text"], r["candidate_fol"]))
    todo = [(k, t, f) for k, (t, f) in uniq.items()]
    chunks = [todo[i:i + 40] for i in range(0, len(todo), 40)]
    t0 = time.time()
    dres = {}
    with ProcessPoolExecutor(max_workers=WORKERS, mp_context=mp.get_context("spawn")) as pool:
        for res in pool.map(_disg_worker, chunks):
            dres.update(dict(res))
    n_fail = sum(1 for d in dres.values() if not d["ok"])
    fr = n_fail / max(1, len(dres))
    reasons = Counter(x.split(":")[0] for d in dres.values() for x in d["fail_reasons"])
    logger.info(f"disguise {len(dres)} unique pairs in {time.time()-t0:.0f}s; assertion failures {n_fail} ({fr:.2%}) {dict(reasons)}")
    whole_arm_fallback = fr > 0.02  # F-DATA: use E's audited disguise for the whole arm
    out = []
    for r in rows:
        iid = r["metadata_item_id"]
        u = {"item_id": iid, "row_key": r["row_key"], "sentence_id": r["metadata_sentence_id"], "text": r["text"], "candidate_fol": r["candidate_fol"],
             "reference_fol": r["reference_fol"], "system": r["metadata_system"], "sysvar": sysvar(r),
             "slot": r.get("metadata_slot"), "family": r.get("metadata_family"), "system_class": r.get("metadata_system_class"),
             "prompt_variant": r.get("metadata_prompt_variant"), "pool": pool_of(r), "parse_ok": bool(pok[iid]),
             "strata": r["metadata_strata"], "fold_E": fold_of_sentence(r["metadata_sentence_id"])}
        if pok[iid]:
            d = dres[sha1(r["text"] + "||" + r["candidate_fol"])]
            if whole_arm_fallback or not d["ok"] or not d["fol_d"]:
                u.update(text_d=r.get("metadata_disguised_text"), fol_d=r.get("metadata_disguised_fol"),
                         disg_source="E_metadata", disg_fail=d["fail_reasons"])
                if not u["fol_d"]:  # E's own disguise missing too -> keep exp-D disguise even if an assertion failed
                    u.update(text_d=d["text_d"], fol_d=d["fol_d"], disg_source="expD_assert_failed")
            else:
                u.update(text_d=d["text_d"], fol_d=d["fol_d"], disg_source="expD", disg_fail=[])
        out.append(u)
    jdump(out, DATA / "E_units.json", indent=None)
    stats = {"n_rows": len(out), "n_parseable": sum(u["parse_ok"] for u in out), "pools": dict(Counter(u["pool"] for u in out)),
             "disguise_unique_pairs": len(dres), "disguise_assert_failures": n_fail, "disguise_fail_rate": fr,
             "disguise_fail_reasons": dict(reasons), "whole_arm_fallback_to_E": whole_arm_fallback,
             "disg_source": dict(Counter(u.get("disg_source") for u in out if u["parse_ok"])),
             "mean_leak_text": sum((d.get("leak_text") or 0) for d in dres.values()) / max(1, len(dres)),
             "max_leak_formula": max([(d.get("leak_formula") or 0) for d in dres.values()] or [0])}
    jdump(stats, RES / "prep_stats.json")
    lines = []
    for u in [u for u in out if u["parse_ok"]][:30]:
        lines += [f"[{u['item_id']}] {u['sysvar']} src={u['disg_source']}", f"  T : {u['text']}", f"  T': {u['text_d']}",
                  f"  F : {u['candidate_fol']}", f"  F': {u['fol_d']}", ""]
    (RES / "disguise_audit.txt").write_text("\n".join(lines))
    logger.info(f"prep stats {stats}")


# =====================================================================================================================
FEATS = {
    "S1": ["parse_fail", "pilot_joint_conflict", "pilot_arity_incons", "pilot_shape_incons", "pilot_dangling",
           "pilot_undeclared", "pilot_rerun_jacc"],
    "S2": ["rt_nli_min", "rt_nli_fwd", "rt_nli_bwd", "rt_nli_contra", "rt_embed_cos", "rt_nli_min_local", "rt_embed_cos_local"],
    "S3": ["judge_cheap_disg", "judge_cheap_orig", "judge_cheap2_disg", "judge_cheap2_orig"],
    "SC": ["sc5_eq_frac", "sc5_entropy"],
}
FEATS["S4"] = FEATS["S1"] + FEATS["S2"] + FEATS["S3"] + FEATS["SC"]
# bridge to the screen number: exp D's S4 set minus rt_reformalise_eq (closed at 0.513 in iteration 1, not re-run)
FEATS["S4_iter1"] = ["parse_fail", "pilot_joint_conflict", "pilot_arity_incons", "pilot_shape_incons", "pilot_dangling",
                     "pilot_undeclared", "pilot_rerun_jacc", "rt_nli_min", "rt_nli_fwd", "rt_nli_bwd", "rt_nli_contra",
                     "rt_embed_cos", "judge_cheap_disg", "judge_cheap2_disg", "judge_cheap_orig", "judge_cheap2_orig"]
FEATS["S5"] = FEATS["S4"] + ["judge_strong_orig", "judge_strong_disg"]

STRONG = {"model": "google/gemini-3.1-pro-preview", "extra": {"reasoning": {"effort": "low"}}, "max_tokens": 4000}
SC_MODEL = "openai/gpt-4.1-nano"
B2_READER = "google/gemini-2.5-flash-lite"


def stage_prereg():
    """Write prereg_baselines.json (NOT yet frozen: the frame stage adds the frame hash + label-vector hashes, then freezes)."""
    from src import judges as J
    from src.budget import CAP_TOTAL, CAPS, load_prices
    if PREREG_SHA.exists():
        raise RuntimeError("prereg already frozen; refusing to overwrite")
    expd = jload(DATA / "expD_prereg.json")
    assert J.PROMPT_SHA["RUBRIC_A"] == expd["prompts"]["sha1"]["RUBRIC_A"] == "06686913c59b6d9a7daeb5748cb9f53ed2b2e812"
    assert sha1(expd["prompts"]["user_json"]) == J.PROMPT_SHA["USER_JSON_A"]
    prices = load_prices(refresh=True)
    models = dict(expd["models"])
    swaps = []
    for m in (models["judge_cheap"], models["judge_cheap2"], STRONG["model"], SC_MODEL, B2_READER):
        if m not in prices:
            swaps.append(f"{m} NOT LISTED")
    thr_d = jload(DATA / "expD_analysis.json")["thresholds"]
    pre = {
        "title": "All baselines re-run on held-out dataset E (iter 2)",
        "created_iso": time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime()), "created_ts": time.time(),
        "data": {"dataset": "iter_1/gen_art/gen_art_dataset_1 full_data_out.json group heldout_candidates (8507 rows, 700 sentences)",
                 "blind_loader": "src/e_pool.py load_E(blind=True) strips 18 label keys + 4 class-structure keys"},
        "models": {**models, "judge_strong": STRONG["model"], "judge_strong_params": STRONG["extra"],
                   "judge_strong_max_tokens": STRONG["max_tokens"], "sc5": SC_MODEL, "b2_reader": B2_READER,
                   "local_verbaliser": "Qwen/Qwen3-8B (bf16, greedy, same VERBALISE prompt)"},
        "model_swaps": swaps,
        "prices_per_token": {m: {"in": prices[m]["in"], "out": prices[m]["out"]} for m in
                             (models["judge_cheap"], models["judge_cheap2"], STRONG["model"], SC_MODEL) if m in prices},
        "prompts": {**expd["prompts"], "sc5_prompt": "dataset E prompts/fewshot_v1.txt (system + 6 exemplars + 'Sentence: {sentence}')",
                    "sc5_prompt_sha1": sha1(json.dumps(FEWSHOT, sort_keys=True, ensure_ascii=False))},
        "prompt_sha1_check": {"RUBRIC_A": J.PROMPT_SHA["RUBRIC_A"], "USER_JSON_A": J.PROMPT_SHA["USER_JSON_A"],
                              "USER_YESNO": J.PROMPT_SHA["USER_YESNO"], "VERBALISE": J.PROMPT_SHA["VERBALISE"]},
        "max_tokens": {**expd["max_tokens"], "sc5": 300, "b2_reader": 400, "judge_strong": STRONG["max_tokens"]},
        "temperature": {"judges": 0, "verbaliser": 0, "sc5": 0.7, "b2_reader": 0},
        "orientation": "every metric oriented so that higher = more likely UNFAITHFUL (judges: 1-P(faithful))",
        "unparseable_rule": "LLM components are NOT called on unparseable candidates; they receive the pre-declared worst "
                            "oriented score (1.0; SC eq_frac 0) and count as coverage failures in the COVERAGE view",
        "json_fail_rule": "judge_cheap: one retry, then fallback oriented score 0.5 (counted)",
        "pools": {"E_POOL": "system_class=='llm'", "GOLDSYS": "system=='malls_gpt4_gold'", "CCG": "system_class=='symbolic_eventsem' (separate)",
                  "PRIMARY": "candidate_fol non-empty AND parses with labeller/fol.py AND converts to z3"},
        "label_regimes": {"R_AB": "tier in {A,B} & final in {CORRECT,ERROR} & not reading_choice (headline)",
                          "R_A": "tier == 'A' only (A_unaudited_ref excluded)",
                          "COVERAGE": "R_AB ∪ UNPARSEABLE-as-ERROR",
                          "sensitivity": ["CONTESTED_AS_CORRECT", "CONTESTED_AS_ERROR", "ALL_TIERS", "R_AB_L25_NO_TOPUP"]},
        "label_vector_function": "sha1('\\n'.join(sorted(f'{item_id}:{label}')))  (src/e_pool.py label_vector_sha1)",
        "combination_feature_sets": FEATS,
        "combination_model": "L2 logistic regression C=1.0, standardised within training folds, missing -> 0 + missing-indicator "
                             "(src/analysis.py combo_oof logic); folds_E below; for fold k fit on labelled rows of other folds, "
                             "predict ALL rows of fold k",
        "folds_E": "fold(sentence_id) = int(sha1('E_folds_v1|'+sentence_id),16) % 5 over all 700 sentences",
        "thresholds": {"rule": "frozen from the SCREEN (exp D results/analysis.json); judges flag if P(faithful)<0.5",
                       "values_from_expD": thr_d,
                       "new_columns": {"rt_nli_min_local": "exp D rt_nli_min_localverb screen threshold",
                                       "rt_embed_cos_local": "exp D rt_embed_cos screen threshold (no local-verbaliser cosine existed)",
                                       "rt_nli_min_alt": "exp D value", "sc5_eq_frac": "flag if eq_frac < 0.5 (oriented > 0.5)",
                                       "sc5_entropy": "descriptive (no threshold): flag if > median screen value unavailable -> 0.5 nat",
                                       "b2_score": "90th percentile of b2_score on screen track-H CORRECT items (computed in b2_gate before any E label)",
                                       "S4": "nested: within each training fold, the training-fit score quantile giving FA=0.10 on training CORRECT rows"}},
        "bootstrap": {"resamples": 2000, "cluster": "metadata_sentence_id", "seed": 0, "ci": "percentile 95%"},
        "testability": {"rule": ">=50 CORRECT and >=50 ERROR rows and >=25 sentences per side (dataset card §3)",
                        "R_AB": {"L25": True, "L20": True, "EXC": True, "CTRL": True, "L25_topup_only": False},
                        "R_A": {"L25": False, "L20": True, "EXC": True, "CTRL": False, "pooled_L20_EXC_CTRL": True},
                        "untestable_cells": "reported descriptively with sign only, never tested"},
        "frontier_frame_rule": "cells {CORRECT,ERROR} x {L25,L20,EXC,CTRL} within R_AB ∩ PRIMARY ∩ E_POOL; 300 rows: 38 per cell "
                               "(37 in the last 4 cells); order sha1(item_id+'frontier_v1'); <=1 row per sentence per cell and <=2 "
                               "rows per sentence overall; inclusion probability = n_drawn/n_cell (IPW)",
        "analyses": ["(a) AUROC/AUPRC/precision-recall-FA at frozen thresholds, tie rate; R_AB, R_A, COVERAGE, sensitivity; pooled/per stratum/long pool",
                     "(b) paired Δ vs judge_cheap_disg: cluster bootstrap + DeLong",
                     "(c) frontier vs cheap judge on the frame, unweighted + IPW, $ per call vs $0.002 gate",
                     "(d) contamination DiD GOLDSYS vs E_POOL, gold-recognition probe, MDE = 2.8 x bootstrap SE",
                     "(e) judge recall per error type at matched FA 0.10/0.20; error_type field accuracy vs majority chance",
                     "(f) complexity AUROC per bin + GEE (exchangeable, groups = sentence) judge_correct ~ z(words)+C(stratum)",
                     "(g) coverage, $ and seconds per item", "(h) gold-error / correct-not-equivalent rates",
                     "(i) system-level Kendall tau-b over 13 system x variant rows (descriptive)",
                     "(j) invariance on exp D's 282 shared rewrites (B2 new, judges joined)", "(k) B2 report"],
        "b2_spec": {"mutant_ops": ["NEG", "REV", "QUANT", "RESTR", "CONN", "DROP", "SWAP", "SCOPE"], "n_mutants": 6,
                    "max_candidates_tried": 20, "z3_timeout_ms": 2000,
                    "direction": "mutant i even: phi TRUE & psi FALSE world; odd: phi FALSE & psi TRUE; fallback other direction",
                    "domain": "constants + k fresh individuals, k=1..3, |D|<=4 (constants+1 if >3 constants), cap 6",
                    "world_solver": "z3 Optimize minimising #true atoms, smallest SAT domain first",
                    "verbaliser": "fixed template, no LLM", "reader": B2_READER + " T=0, one call per item, text only (never a formula)",
                    "score": "b2_score = (#determined verdicts != phi-truth + 0.5 x #UNDETERMINED) / n_worlds",
                    "gate": "balanced accuracy >= 0.85 on worlds of track-H expert-corrected formulas (40-item dev slice excluded)",
                    "prompt_dev": "<=2 variants on a 40-item screen-H dev slice; frozen in prereg_b2.json",
                    "status_fallback": "non-ok -> oriented score 0.5 (coverage failure)"},
        "budget": {"cap_total": CAP_TOTAL, "caps": CAPS,
                   "note": f"the run-shared OpenRouter key had ${'{'}limit_remaining{'}'} left at freeze (see key_state); F-KEY applies if it dies"},
        "time_fallback_order": ["judge_cheap orig/disg + cheap2 disg", "pilot + parse + API-verbaliser NLI/cosine", "SC-5", "S4 + folds",
                                "frontier 300", "B2 screen + gate", "B2 on E", "local verbaliser", "cheap2 orig", "B2 rewrites"],
        "departures": ["frontier on a 300-row stratified frame (budget)", "frame drawing reads labels (disclosed; nothing tuned on it)",
                       "pilot 'documents' are artificial (system|variant, stratum, sha1 bucket of ~20 sentences) groups",
                       "rerun-Jaccard: zero-shot vs few-shot for Llama-3.3-70B/Qwen3-235B, cross-system for the rest",
                       "rt_reformalise_eq not re-run (closed at 0.513)", "R_ADJ/R_COMP labels do not exist yet: exported feature table + fit_s4_oof",
                       "B2 is new: reader gate before fusion", "judges not run on unparseable rows (worst score)",
                       "matched-FA recall uses per-judge E thresholds (descriptive)", "system-level tau descriptive",
                       "disguise_item called with its default seed (seed = text), as the sibling experiment does"],
    }
    try:
        import requests
        ks = requests.get(os.environ["OPENROUTER_BASE_URL"].rstrip("/") + "/key", headers={"Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}"},
                          timeout=30).json()["data"]
        pre["key_state"] = {k: ks.get(k) for k in ("limit", "limit_reset", "limit_remaining", "usage_daily")}
        pre["budget"]["note"] = pre["budget"]["note"].replace("{limit_remaining}", f"{ks.get('limit_remaining'):.2f}")
    except Exception as e:  # noqa: BLE001
        pre["key_state"] = {"error": str(e)[:100]}
    jdump(pre, PREREG)
    logger.info(f"prereg written (unfrozen) with model swaps {swaps}")


def stage_frame():
    """Frontier frame (label read disclosed) + label-vector hashes; then freeze prereg (sha256)."""
    from src.e_pool import load_E, regime_labels, label_vector_sha1
    if PREREG_SHA.exists():
        raise RuntimeError("already frozen")
    pre = jload(PREREG)
    U = {u["item_id"]: u for u in units()}
    full = load_E(blind=False, _frame_ok=True)
    # only item_id, final_label, tier, source_stratum, sentence_id are used here
    rab = regime_labels(full, "R_AB")
    ra = regime_labels(full, "R_A")
    cells = defaultdict(list)
    for r in full:
        iid, rk = r["metadata_item_id"], r["row_key"]
        if rk in rab and U[iid]["parse_ok"] and U[iid]["pool"] == "E_POOL" and rk == iid:  # colliding ids never drawn
            cells[("ERROR" if rab[rk] else "CORRECT", r["metadata_strata"]["source_stratum"])].append((iid, r["metadata_sentence_id"]))
    order = [(c, s) for c in ("CORRECT", "ERROR") for s in ("L25", "L20", "EXC", "CTRL")]
    quota = {cell: (38 if i < 4 else 37) for i, cell in enumerate(order)}  # 4*38 + 4*37 = 300
    per_sent = Counter()
    frame, pop = [], {}
    for cell in order:
        cand = sorted(cells[cell], key=lambda x: sha1(x[0] + "frontier_v1"))
        pop["|".join(cell)] = len(cand)
        seen_s, got = set(), 0
        for iid, sid in cand:
            if got >= quota[cell]:
                break
            if sid in seen_s or per_sent[sid] >= 2:
                continue
            frame.append({"item_id": iid, "cell": "|".join(cell)})
            seen_s.add(sid)
            per_sent[sid] += 1
            got += 1
    incl = {}
    for f in frame:
        n_drawn = sum(1 for g in frame if g["cell"] == f["cell"])
        incl[f["item_id"]] = n_drawn / pop[f["cell"]]
    fr = {"rule": pre["frontier_frame_rule"], "cells_population": pop, "n": len(frame),
          "per_cell": dict(Counter(f["cell"] for f in frame)), "rows": [{**f, "incl_prob": incl[f["item_id"]]} for f in frame]}
    jdump(fr, DATA / "frontier_frame.json")
    ids = sorted(rab)
    rk2id = {r["row_key"]: r["metadata_item_id"] for r in full}
    pre["frontier_frame"] = {"file": "data/frontier_frame.json", "sha256": hashlib.sha256((DATA / "frontier_frame.json").read_bytes()).hexdigest(),
                             "n": len(frame), "per_cell": fr["per_cell"], "cells_population": pop}
    pre["label_vectors"] = {"note": "lines 'metadata_item_id:label' over ROWS (the 115 colliding item_ids appear once per row); "
                                    "'_rowkey' variant uses row_key (item_id~variant for colliding rows)"}
    for nm, lab in (("R_AB", rab), ("R_A", ra)):
        ks = sorted(lab)
        labs = ["ERROR" if lab[k] else "CORRECT" for k in ks]
        pre["label_vectors"][nm] = {"n": len(ks), "sha1": label_vector_sha1([rk2id[k] for k in ks], labs),
                                    "sha1_rowkey": label_vector_sha1(ks, labs)}
    pre["freeze_context"] = ("Frozen before ANY score file exists. The only label read before scoring is stage 'frame' "
                             "(draw_frontier_frame logic in method.py), which reads item_id, final_label, tier, reading_choice, "
                             "source_stratum and sentence_id to draw the 300-row frontier frame and hash the R_AB/R_A label vectors; "
                             "no parameter, prompt, threshold or model choice depends on it.")
    pre["frozen_iso"] = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())
    jdump(pre, PREREG)
    PREREG_SHA.write_text(hashlib.sha256(PREREG.read_bytes()).hexdigest() + "  prereg_baselines.json\n")
    logger.info(f"frame {len(frame)} rows {fr['per_cell']}; population {pop}; R_AB n={len(rab)} R_A n={len(ra)}; prereg FROZEN")


# =====================================================================================================================
def _judge_units(limit, pools=("E_POOL", "GOLDSYS", "CCG")):
    """PRIMARY units, R_AB-FIRST (T1 2.1): key = (0 if the row is in R_AB or tier-A decided else 1, sha1(item_id)).
    Only label-regime MEMBERSHIP is read (data/t1_priority.json), never a label value or a score, so a mid-sweep key
    death leaves the analysable rows covered first."""
    U = [u for u in units() if u["parse_ok"] and u["pool"] in pools]
    pr_p = DATA / "t1_priority.json"
    prio = set(jload(pr_p)["priority_item_ids"]) if pr_p.exists() else set()
    U.sort(key=lambda u: (0 if u["item_id"] in prio else 1, sha1(u["item_id"])))
    return U[:limit] if limit else U


def _dedup(pairs):
    """[(key, text, fol)] -> unique [(ukey, text, fol)] and {key: ukey}."""
    m, uq = {}, {}
    for k, t, f in pairs:
        uk = sha1(t + "||" + (f or ""))
        m[k] = uk
        uq.setdefault(uk, (t, f))
    return [(uk, t, f) for uk, (t, f) in uq.items()], m


def stage_judges(limit=None, which=("cheap_disg", "cheap2_disg", "cheap_orig", "cheap2_orig")):
    from src import judges as J
    from src.budget import Budget
    pre = require_frozen()
    rub, ut = pre["prompts"]["rubric"], pre["prompts"]["user_json"]
    U = _judge_units(limit)
    logger.info(f"cheap judges on {len(U)} PRIMARY rows x {which} (limit={limit})")

    async def run():
        async with Budget(concurrency=32) as b:
            for w in which:
                name, cond = w.rsplit("_", 1)
                done = load_scores(f"judge_{name}")
                pairs = [(f"{u['item_id']}|{cond}", u["text"] if cond == "orig" else u["text_d"],
                          u["candidate_fol"] if cond == "orig" else u["fol_d"]) for u in U]
                pairs = [p for p in pairs if p[0] not in done or done[p[0]].get("p") is None]
                uq, m = _dedup(pairs)
                t0 = time.time()
                if name == "cheap":
                    outs = await J.gather_limited([J.judge_json(b, component="judge_cheap", model=pre["models"]["judge_cheap"],
                                                                rubric=rub, text=t, fol=f, item_id=k, user_tmpl=ut) for k, t, f in uq], w)
                else:
                    outs = await J.gather_limited([J.judge_logprob(b, component="judge_cheap2", model=pre["models"]["judge_cheap2"],
                                                                   rubric=rub, text=t, fol=f, item_id=k) for k, t, f in uq], w)
                res = {k: o for (k, _, _), o in zip(uq, outs)}
                secs = time.time() - t0
                rows = []
                for k, _, _ in pairs:
                    o = res[m[k]]
                    rows.append({"key": k, "p": o.get("p"), "type": o.get("type"), "fail": o.get("fail"), "src": o.get("src"),
                                 "cost": o.get("cost"), "seconds": o.get("seconds"), "dedup_key": m[k], "raw": o.get("raw"),
                                 "verdict": o.get("verdict")})
                append_jsonl(SCORES / f"judge_{name}.jsonl", rows)
                nf = sum(r["p"] is None for r in rows)
                logger.info(f"{w}: {len(rows)} rows ({len(uq)} unique calls) in {secs:.0f}s; failures {nf}; "
                            f"spent ${b.spent:.4f} {b.by_comp}; key_dead={b.dead}")
                if b.dead:
                    logger.error("shared key exhausted -> F-KEY")
                    break
    asyncio.run(run())


# =====================================================================================================================
def _sc_messages(text):
    return ([{"role": "system", "content": FEWSHOT["system"]}] + FEWSHOT["exemplars"]
            + [{"role": "user", "content": FEWSHOT["user_template"].format(sentence=text)}])


async def _sc_call(b, J, text, sid, k):
    """One T=0.7 sample; the sample index is part of the cache key (NOT the prompt)."""
    cache = J._load_cache()
    msgs = _sc_messages(text)
    ck = J._ckey("sc5", SC_MODEL, msgs, {"max_tokens": 300, "temperature": 0.7, "sample": k})
    if ck in cache:
        return {**cache[ck]["resp"], "cached": True}
    from src.budget import BudgetExceeded
    try:
        r = await b.call(component="sc5", model=SC_MODEL, messages=msgs, max_tokens=300, item_id=f"{sid}|s{k}", temperature=0.7)
    except BudgetExceeded as e:
        return {"text": None, "fail": f"budget:{e}"}
    except Exception as e:  # noqa: BLE001
        return {"text": None, "fail": f"api:{str(e)[:100]}"}
    rec = {"key": ck, "component": "sc5", "model": SC_MODEL, "item_id": f"{sid}|s{k}",
           "resp": {kk: r[kk] for kk in ("text", "logprobs", "cost", "in_tok", "out_tok", "seconds", "finish")}}
    cache[ck] = rec
    with J.CACHE_P.open("a") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return {**rec["resp"], "cached": False}


def stage_sc_gen(limit=None):
    from src import judges as J
    from src.budget import Budget
    require_frozen()
    sents = {}
    for u in units():
        sents.setdefault(u["sentence_id"], u["text"])
    pr_p = DATA / "t1_priority.json"  # T1: sentences with an R_AB / tier-A row first (membership only)
    prio = set(jload(pr_p)["priority_item_ids"]) if pr_p.exists() else set()
    psent = {u["sentence_id"] for u in units() if u["item_id"] in prio}
    sids = sorted(sents, key=lambda s: (0 if s in psent else 1, sha1(s)))
    if limit:
        sids = sids[:limit]
    done = load_scores("sc5_samples")
    todo = [s for s in sids if s not in done or any(x is None for x in done[s]["samples_raw"])]
    logger.info(f"SC-5 generation: {len(todo)} sentences x 5 samples")

    async def run():
        async with Budget(concurrency=32) as b:
            outs = await J.gather_limited([_sc_call(b, J, sents[s], s, k) for s in todo for k in range(5)], "sc5")
            logger.info(f"spent ${b.spent:.4f} {b.by_comp}; dead={b.dead}")
            return outs
    outs = asyncio.run(run())
    rows = []
    for i, s in enumerate(todo):
        o = outs[5 * i:5 * i + 5]
        raw = [x.get("text") for x in o]
        forms = [J.extract_formula(t) if t else None for t in raw]
        forms = [f[4:].strip() if f and f.upper().startswith("FOL:") else f for f in forms]
        rows.append({"key": s, "samples_raw": raw, "samples": forms, "cost": sum((x.get("cost") or 0) for x in o if not x.get("cached")),
                     "fails": [x.get("fail") for x in o]})
    append_jsonl(SCORES / "sc5_samples.jsonl", rows)
    logger.info(f"SC-5: {len(rows)} sentences; missing samples {sum(x is None for r in rows for x in r['samples'])}")


# =====================================================================================================================
def stage_verbalise(limit=None):
    from src import judges as J
    from src.budget import Budget
    pre = require_frozen()
    U = _judge_units(limit)
    done = load_scores("rt_verbal_api")
    pairs = [(u["item_id"], u["candidate_fol"]) for u in U if u["item_id"] not in done or not done[u["item_id"]].get("verbalisation")]
    uq = {}
    for k, f in pairs:
        uq.setdefault(sha1(f), f)
    logger.info(f"API verbaliser: {len(pairs)} rows, {len(uq)} unique formulas")

    async def run():
        async with Budget(concurrency=32) as b:
            keys = list(uq)
            outs = await J.gather_limited([J.simple_text(b, component="roundtrip", model=pre["models"]["roundtrip_llm"], item_id=k,
                                                         max_tokens=120, prompt=J.VERBALISE.format(fol=uq[k])) for k in keys], "verbalise")
            logger.info(f"spent ${b.spent:.4f} {b.by_comp}; dead={b.dead}")
            return dict(zip(keys, outs))
    res = asyncio.run(run())
    rows, leaks = [], 0
    for k, f in pairs:
        g = res[sha1(f)]
        v, leak = J.clean_verbalisation(g.get("text") or "") if g.get("text") else (None, False)
        leaks += bool(leak)
        rows.append({"key": k, "verbalisation": v, "raw": (g.get("text") or "")[:300], "leak": leak, "fail": g.get("fail"),
                     "cost": g.get("cost"), "seconds": g.get("seconds")})
    append_jsonl(SCORES / "rt_verbal_api.jsonl", rows)
    logger.info(f"verbalise: {len(rows)} rows; failures {sum(1 for r in rows if not r['verbalisation'])}; residual symbols {leaks}")


# =====================================================================================================================
def _strong_params() -> dict:
    """STRONG model/params; prereg_T1 (if frozen) may swap the model or raise max_tokens (pilot rule T1 2.4)."""
    p = dict(STRONG)
    t1 = ROOT / "prereg_T1.json"
    if t1.exists():
        d = jload(t1).get("strong", {})
        p["model"] = d.get("model", p["model"])
        p["max_tokens"] = int(d.get("max_tokens", p["max_tokens"]))
        p["extra"] = d.get("extra", p["extra"])
    return p


def strong_order(which=("orig", "disg")) -> list[tuple[str, str]]:
    """T1 frontier priority (pre-declared): ORIGINAL on every frame row in frame sha1 order, then DISGUISED round-robin
    over the 8 frame cells (cells in sorted order, rows within a cell in frame sha1 order), so a cap stop leaves a
    cell-balanced disguised subset (analysed with IPW)."""
    fr = jload(DATA / "frontier_frame.json")["rows"]
    fr = sorted(fr, key=lambda r: sha1(r["item_id"] + "frontier_v1"))
    out = []
    if "orig" in which:
        out += [(r["item_id"], "orig") for r in fr]
    if "disg" in which:
        cells = defaultdict(list)
        for r in fr:
            cells[r["cell"]].append(r["item_id"])
        ck = sorted(cells)
        i = 0
        while any(cells[c] for c in ck):
            c = ck[i % len(ck)]
            if cells[c]:
                out.append((cells[c].pop(0), "disg"))
            i += 1
    return out


def stage_strong(limit=None, which=("orig", "disg")):
    from src import judges as J
    from src.budget import Budget
    pre = require_frozen()
    SP = _strong_params()
    if which == ("pilot",):  # T1 2.2 label-blind pilot: first 10 frame rows by sha1, 5 orig + 5 disg
        o = strong_order(("orig",))[:10]
        order = [(i, "orig") for i, _ in o[:5]] + [(i, "disg") for i, _ in o[5:10]]
    else:
        order = strong_order(which)
    if limit:
        order = order[:limit]
    U = {u["item_id"]: u for u in units()}
    done = load_scores("judge_strong")
    todo = []
    for i, cond in order:
        u = U[i]
        t, f = (u["text"], u["candidate_fol"]) if cond == "orig" else (u["text_d"], u["fol_d"])
        if f"{i}|{cond}" not in done or done[f"{i}|{cond}"].get("p") is None:
            todo.append((f"{i}|{cond}", t, f))
    logger.info(f"strong judge {SP['model']} (max_tokens {SP['max_tokens']}) on {len(todo)} units")

    reserve = 0.75 if which == ("disg",) else None  # prereg_T1 strong.shared_key_reserve_rule

    async def run():
        outs = []
        async with Budget(concurrency=16) as b:
            step = 40 if reserve is not None else len(todo) or 1
            for i in range(0, len(todo), step):
                if reserve is not None:
                    ks = _key_status()
                    if ks.get("limit_remaining") is None or ks["limit_remaining"] <= reserve:
                        logger.warning(f"strong disg stopped by the shared-key reserve rule: {ks}")
                        outs += [{"p": None, "fail": f"budget:key_reserve {ks.get('limit_remaining')}"}] * (len(todo) - i)
                        break
                outs += await J.gather_limited([J.judge_json(b, component="strong", model=SP["model"], rubric=pre["prompts"]["rubric"],
                                                             text=t, fol=f, item_id=k, max_tokens=SP["max_tokens"], extra=SP["extra"],
                                                             user_tmpl=pre["prompts"]["user_json"]) for k, t, f in todo[i:i + step]], "strong")
            logger.info(f"spent ${b.spent:.4f} {b.by_comp}; dead={b.dead}")
            return outs
    outs = asyncio.run(run())
    rows = [{"key": k, "p": o.get("p"), "type": o.get("type"), "fail": o.get("fail"), "cost": o.get("cost"), "seconds": o.get("seconds"),
             "finish": o.get("finish"), "raw": o.get("raw")}
            for (k, _, _), o in zip(todo, outs)]
    append_jsonl(SCORES / "judge_strong.jsonl", rows)
    costs = [r["cost"] for r in rows if r["cost"]]
    logger.info(f"strong: {len(rows)} rows, failures {sum(r['p'] is None for r in rows)}; mean $/call "
                f"{(sum(costs)/len(costs) if costs else 0):.5f}")


def stage_retest(limit=None):
    """judge_cheap_disg re-called on 200 sha1-chosen rows; identical prompt, cache key carries a nonce only."""
    from src import judges as J
    from src.budget import Budget
    pre = require_frozen()
    U = sorted([u for u in units() if u["parse_ok"] and u["pool"] == "E_POOL"], key=lambda u: sha1(u["item_id"] + "retest_v1"))[:200]
    rub, ut = pre["prompts"]["rubric"], pre["prompts"]["user_json"]

    async def one(b, u):
        msgs = [{"role": "system", "content": rub}, {"role": "user", "content": ut.format(text=u["text_d"], fol=u["fol_d"])}]
        cache = J._load_cache()
        params = {"max_tokens": 150, "response_format": {"type": "json_object"}, "retest_nonce": "retest_v1"}
        ck = J._ckey("retest", pre["models"]["judge_cheap"], msgs, params)
        if ck in cache:
            r = cache[ck]["resp"]
        else:
            try:
                r = await b.call(component="retest", model=pre["models"]["judge_cheap"], messages=msgs, max_tokens=150,
                                 item_id=u["item_id"], extra={"response_format": {"type": "json_object"}})
            except Exception as e:  # noqa: BLE001
                return {"p": None, "fail": str(e)[:100]}
            rec = {"key": ck, "component": "retest", "model": pre["models"]["judge_cheap"], "item_id": u["item_id"],
                   "resp": {kk: r[kk] for kk in ("text", "logprobs", "cost", "in_tok", "out_tok", "seconds", "finish")}}
            cache[ck] = rec
            with J.CACHE_P.open("a") as f:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        o = J.parse_judge_json(r["text"])
        return {"p": None if o is None else o["p"], "fail": None if o else "json_parse"}

    async def run():
        async with Budget(concurrency=32) as b:
            return await J.gather_limited([one(b, u) for u in U], "retest")
    outs = asyncio.run(run())
    append_jsonl(SCORES / "judge_cheap_retest.jsonl", [{"key": f"{u['item_id']}|disg", **o} for u, o in zip(U, outs)])
    logger.info(f"retest: {len(outs)} rows, failures {sum(o['p'] is None for o in outs)}")


# =====================================================================================================================
def _pilot_docs(U):
    """Artificial 'documents' for the pilot metrics (E rows are single sentences): (system|variant, stratum, sha1 bucket of
    ~20 sentences). CTRL has no FOLIO story id in dataset E, so it uses the same bucket rule."""
    n_sent = defaultdict(set)
    for u in U:
        n_sent[u["strata"]["source_stratum"]].add(u["sentence_id"])
    B = {s: max(1, round(len(v) / 20)) for s, v in n_sent.items()}
    docs = defaultdict(list)
    for u in U:
        st = u["strata"]["source_stratum"]
        docs[(u["sysvar"], st, int(sha1(u["sentence_id"]), 16) % B[st])].append(u)
    return docs, B


def stage_cpu():
    """parse_fail + the user's pilot structural metrics (adapted) + rerun-Jaccard proxy."""
    from src.pilot_metrics import compute_pilot
    U = units()
    docs, B = _pilot_docs(U)
    rows = []
    seen = set()
    for key, us in docs.items():
        for u in us:
            if u["item_id"] in seen:
                continue
            seen.add(u["item_id"])
            story = [v["candidate_fol"] for v in us if v["item_id"] != u["item_id"] and v["parse_ok"]]
            rows.append({"key": u["item_id"], "candidate_fol": u["candidate_fol"] if u["parse_ok"] else None,
                         "story_premises_fol": story, "declared_predicates": None, "has_story": True})
    res = compute_pilot(rows, workers=WORKERS)
    # rerun-Jaccard: zero-shot vs few-shot where both exist (Llama-3.3-70B, Qwen3-235B), else cross-system
    by_sent = defaultdict(list)
    for u in U:
        by_sent[u["sentence_id"]].append(u)

    def jac(a, b):
        return len(set(a) & set(b)) / max(1, len(set(a) | set(b)))
    out = []
    for u in U:
        if u["item_id"] in {o["key"] for o in out}:
            continue
        p = dict(res.get(u["item_id"], {"key": u["item_id"]}))
        mine = p.get("pred_tokens")
        flag, rj = None, None
        if mine is not None:
            twin = [v for v in by_sent[u["sentence_id"]] if v["system"] == u["system"] and v["prompt_variant"] != u["prompt_variant"]
                    and v["pool"] == "E_POOL"]
            twin_t = [res.get(v["item_id"], {}).get("pred_tokens") for v in twin]
            twin_t = [t for t in twin_t if t is not None]
            if twin_t:
                rj, flag = sum(jac(mine, t) for t in twin_t) / len(twin_t), "zeroshot_vs_fewshot"
            else:
                others = [res.get(v["item_id"], {}).get("pred_tokens") for v in by_sent[u["sentence_id"]]
                          if v["pool"] == "E_POOL" and v["sysvar"] != u["sysvar"]]
                others = [t for t in others if t is not None]
                if others:
                    rj, flag = sum(jac(mine, t) for t in others) / len(others), "cross_system"
        p["pilot_rerun_jacc"] = rj
        p["rerun_flag"] = flag
        p["parse_fail"] = 0 if u["parse_ok"] else 1
        p["pilot_undeclared"] = None  # no declared-predicate list in dataset E (not applicable)
        p["key"] = u["item_id"]
        out.append(p)
    (SCORES / "pilot.jsonl").write_text("")
    append_jsonl(SCORES / "pilot.jsonl", out)
    (RES / "pilot_mapping_E.md").write_text(
        "# Pilot metrics on dataset E: adaptation\n\n"
        "Dataset E rows are single sentences, so the pilot's 'document' (a set of formulas loaded together) is an artificial group:\n"
        f"(system|variant, source_stratum, int(sha1(sentence_id),16) % B) with B per stratum {B} (about 20 sentences per document).\n"
        "CTRL (FOLIO) rows have no story id in dataset E and use the same bucket rule.\n\n"
        "- pilot_joint_conflict: story = the other parseable formulas of the same document; 1 if story ∪ {cand} is UNSAT (z3, 5 s).\n"
        "- pilot_arity_incons / pilot_shape_incons: arity / argument-kind clashes of cand against the rest of the document.\n"
        "- pilot_dangling: fraction of cand predicates+constants that appear nowhere else in the document.\n"
        "- pilot_undeclared: NOT APPLICABLE (dataset E generators output no predicate declarations).\n"
        "- pilot_rerun_jacc: 1 - predicate-token Jaccard; zero-shot vs few-shot output of the same system for Llama-3.3-70B and "
        "Qwen3-235B (the only slots with two prompt variants), otherwise the mean Jaccard with the other LLM slots on the same "
        "sentence (cross-system proxy); column rerun_flag says which.\n"
        "The joint-load conflict metric therefore has a different meaning from the user's pilot (documents are not coherent stories); "
        "it is reported as 'adapted'.\n")
    logger.info(f"pilot: {len(out)} rows; parse_fail {sum(r['parse_fail'] for r in out)}; joint_conflict=1 "
                f"{sum(1 for r in out if r.get('pilot_joint_conflict') == 1)}; rerun flags {Counter(r['rerun_flag'] for r in out)}")


# =====================================================================================================================
def _sc_pair_worker(chunk):
    import sys as _s
    _s.setrecursionlimit(10000)
    from src.labeller.labeller import equivalent_modulo_vocab
    out = []
    for a, b in chunk:
        t0 = time.time()
        try:
            r = equivalent_modulo_vocab(a, b, ms=2000, do_search=False)
            cls = r["cls"]
        except Exception as e:  # noqa: BLE001
            cls = f"EXC:{type(e).__name__}"
        out.append({"a": a, "b": b, "cls": cls, "eq": cls in ("EQUIV", "VOCAB", "GRAN"), "secs": round(time.time() - t0, 3)})
    return out


def stage_sc_score(which=("sc5_local_samples",)):
    for w in which:
        _sc_score(w)


def _sc_score(samples_name="sc5_samples"):
    """SC-5: eq_frac = #samples equivalent modulo vocabulary to the candidate / 5 (unparseable/missing sample = not
    equivalent), entropy of the equivalence classes of {candidate} ∪ samples (missing samples = singletons)."""
    import math
    import multiprocessing as mp
    from src.labeller.labeller import parse_ok
    S = load_scores(samples_name)
    if not S:
        logger.error(f"no SC samples in {samples_name}")
        return
    U = [u for u in units() if u["parse_ok"]]
    pc_p = RES / f"sc_pair_cache_{samples_name}.jsonl"
    cache = {}
    if pc_p.exists():
        for r in read_jsonl(pc_p):
            cache[(sha1(r["a"]), sha1(r["b"]))] = r["eq"]
    samp_ok = {}
    for s, r in S.items():
        samp_ok[s] = [f if (f and parse_ok(f)) else None for f in r["samples"]]
    pairs = set()
    for u in U:
        smp = samp_ok.get(u["sentence_id"])
        if smp is None:
            continue
        for f in smp:
            if f and f != u["candidate_fol"]:
                pairs.add((u["candidate_fol"], f))
    for smp in samp_ok.values():
        fs = [f for f in smp if f]
        for i, a in enumerate(fs):
            for b in fs[i + 1:]:
                if a != b:
                    pairs.add((a, b))
    todo = sorted(p for p in pairs if (sha1(p[0]), sha1(p[1])) not in cache)
    logger.info(f"SC pairs: {len(pairs)} total, {len(todo)} to compute")
    t0 = time.time()
    if todo:
        chunks = [todo[i:i + 25] for i in range(0, len(todo), 25)]
        with mp.get_context("spawn").Pool(WORKERS) as pool, pc_p.open("a") as f:
            for i, res in enumerate(pool.imap_unordered(_sc_pair_worker, chunks)):
                for r in res:
                    cache[(sha1(r["a"]), sha1(r["b"]))] = r["eq"]
                    f.write(json.dumps(r, ensure_ascii=False) + "\n")
                if (i + 1) % 100 == 0:
                    logger.info(f"SC pairs {i+1}/{len(chunks)} chunks {time.time()-t0:.0f}s")
    secs_pair = (time.time() - t0) / max(1, len(todo))

    def eq(a, b):
        if a == b:
            return True  # identical strings are trivially equivalent (the iter-1 cache bug)
        return bool(cache.get((sha1(a), sha1(b)), cache.get((sha1(b), sha1(a)), False)))
    from src.consensus_min import sc_scores_one
    rows = []
    for u in U:
        smp = samp_ok.get(u["sentence_id"])
        if smp is None:
            continue
        rows.append({"key": u["item_id"], **sc_scores_one(u["candidate_fol"], smp, eq), "n_samples_parsed": sum(1 for f in smp if f)})
    name = samples_name.replace("_samples", "")
    (SCORES / f"{name}.jsonl").write_text("")
    append_jsonl(SCORES / f"{name}.jsonl", rows)
    jdump({"pairs": len(pairs), "computed": len(todo), "secs_per_pair": secs_pair,
           "sample_parse_rate": sum(1 for v in samp_ok.values() for f in v if f) / max(1, 5 * len(samp_ok))},
          RES / f"{name}_score_meta.json")
    logger.info(f"SC scored {len(rows)} rows; {secs_pair:.3f}s/pair")


# =====================================================================================================================
# F-KEY LOCAL PATH: the shared OpenRouter key was exhausted by other runs at freeze time (limit_remaining 0 at 18:02 UTC,
# daily reset 00:00 UTC = after this module's deadline). Local open-weight models from exp D's prereg_local.json.
LOCAL_Q8 = "Qwen/Qwen3-8B"
LOCAL_L8 = "meta-llama/Llama-3.1-8B-Instruct"
LOCAL_Q14 = ("Qwen/Qwen3-14B", "nf4")


def _prereg_local():
    return jload(EXPD / "prereg_local.json")


def _msgs_json(rub, ut, text, fol):
    return [{"role": "system", "content": rub},
            {"role": "user", "content": ut.format(text=text, fol=fol if (fol and fol.strip()) else "(empty)")}]


def _local_json_judge(lm, units_, rub, ut, tag, max_new_tokens=150, bs=64):
    """exp D _local_json_judge verbatim (one 'Return ONLY the JSON object.' retry), batch size 32 on the RTX 4090."""
    from src import judges as J
    msgs = [_msgs_json(rub, ut, t, f) for _, t, f in units_]
    gen = lm.generate(msgs, max_new_tokens=max_new_tokens, tag=tag, bs=bs)
    outs, retry = [], []
    for i, g in enumerate(gen):
        o = J.parse_judge_json(g["text"])
        outs.append({**(o or {"p": None}), "fail": None if o else "json_parse", "seconds": g["seconds"], "raw": g["text"][:300]})
        if o is None:
            retry.append(i)
    if retry:
        m2 = [msgs[i] + [{"role": "assistant", "content": gen[i]["text"]}, {"role": "user", "content": "Return ONLY the JSON object."}]
              for i in retry]
        g2 = lm.generate(m2, max_new_tokens=max_new_tokens, tag=tag + "_retry", bs=bs)
        for i, g in zip(retry, g2):
            o = J.parse_judge_json(g["text"])
            if o:
                outs[i] = {**o, "fail": None, "seconds": outs[i]["seconds"] + g["seconds"], "raw": g["text"][:300], "retried": True}
    return outs


def stage_local_judges(limit=None, which=("qwen8b_disg", "qwen8b_orig", "llama8b_disg", "llama8b_orig")):
    from src import judges as J
    from src.common import disable_triton_overrides
    from src.local_llm import LocalLM
    disable_triton_overrides()
    require_frozen()
    pl = _prereg_local()
    rub, ut = pl["prompts"]["rubric"], pl["prompts"]["user_json"]
    U = _judge_units(limit)
    lm, cur = None, None
    for w in which:
        name, cond = w.rsplit("_", 1)
        model = LOCAL_Q8 if name == "qwen8b" else LOCAL_L8
        if cur != model:
            if lm is not None:
                lm.unload()
            lm, cur = LocalLM(model), model
        pairs = [(f"{u['item_id']}|{cond}", u["text"] if cond == "orig" else u["text_d"],
                  u["candidate_fol"] if cond == "orig" else u["fol_d"]) for u in U]
        uq, m = _dedup(pairs)
        t0 = time.time()
        if name == "qwen8b":
            outs = _local_json_judge(lm, uq, rub, ut, f"judge_local_{w}")
        else:
            msgs = [[{"role": "system", "content": rub},
                     {"role": "user", "content": J.USER_YESNO.format(text=t, fol=f if (f and f.strip()) else "(empty)")}] for _, t, f in uq]
            outs = [{"p": o["p"], "mass_yes_no": o.get("mass_yes_no"), "seconds": o["seconds"],
                     "fail": None if o["p"] is not None else "no_mass", "src": "logprobs"} for o in lm.p_yes(msgs, tag=f"judge_local_{w}", bs=32)]
        res = {k: o for (k, _, _), o in zip(uq, outs)}
        rows = [{"key": k, **{kk: vv for kk, vv in res[m[k]].items() if kk != "raw"}, "dedup_key": m[k]} for k, _, _ in pairs]
        append_jsonl(SCORES / f"judge_local_{name}.jsonl", rows)
        logger.info(f"local {w}: {len(rows)} rows ({len(uq)} unique) in {time.time()-t0:.0f}s; failures {sum(r['p'] is None for r in rows)}")
    if lm is not None:
        lm.unload()


def stage_local_strong(limit=None):
    """Qwen3-14B nf4 (exp D's largest local judge; NOT a frontier model) orig + disg on the frontier frame."""
    from src.common import disable_triton_overrides
    from src.local_llm import LocalLM
    disable_triton_overrides()
    require_frozen()
    pl = _prereg_local()
    fr = jload(DATA / "frontier_frame.json")["rows"]
    ids = [r["item_id"] for r in fr][:limit] if limit else [r["item_id"] for r in fr]
    U = {u["item_id"]: u for u in units()}
    su = []
    for i in ids:
        u = U[i]
        su += [(f"{i}|orig", u["text"], u["candidate_fol"]), (f"{i}|disg", u["text_d"], u["fol_d"])]
    lm = LocalLM(LOCAL_Q14[0], quant=LOCAL_Q14[1])
    t0 = time.time()
    outs = _local_json_judge(lm, su, pl["prompts"]["rubric"], pl["prompts"]["user_json"], "judge_local_qwen14b", bs=16)
    append_jsonl(SCORES / "judge_local_qwen14b.jsonl", [{"key": k, **{kk: vv for kk, vv in o.items() if kk != "raw"}}
                                                        for (k, _, _), o in zip(su, outs)])
    logger.info(f"local strong: {len(su)} units in {time.time()-t0:.0f}s, failures {sum(o['p'] is None for o in outs)}")
    lm.unload()


def stage_local_verb(limit=None):
    """Local Qwen3-8B verbaliser (same VERBALISE prompt, greedy) + clean_verbalisation()."""
    from src import judges as J
    from src.common import disable_triton_overrides
    from src.local_llm import LocalLM
    disable_triton_overrides()
    require_frozen()
    U = _judge_units(limit)
    uq = {}
    for u in U:
        uq.setdefault(sha1(u["candidate_fol"]), u["candidate_fol"])
    keys = list(uq)
    lm = LocalLM(LOCAL_Q8)
    t0 = time.time()
    gen = lm.generate([[{"role": "user", "content": J.VERBALISE.format(fol=uq[k])}] for k in keys], 120, tag="verbalise_local", bs=64)
    lm.unload()
    res = dict(zip(keys, gen))
    rows, leaks = [], 0
    for u in U:
        g = res[sha1(u["candidate_fol"])]
        v, leak = J.clean_verbalisation(g["text"])
        leaks += bool(leak)
        rows.append({"key": u["item_id"], "verbalisation": v or None, "raw": g["text"][:300], "leak": leak, "seconds": g["seconds"]})
    append_jsonl(SCORES / "rt_verbal_local.jsonl", rows)
    logger.info(f"local verbaliser: {len(rows)} rows ({len(keys)} unique) in {time.time()-t0:.0f}s; residual symbols {leaks}")


def stage_local_sc(limit=None):
    """F-KEY fallback for SC-5: Qwen3-8B sampling at T=0.7, 5 samples per sentence, dataset-E few-shot prompt (sc5_local)."""
    from src import judges as J
    from src.common import disable_triton_overrides
    from src.local_llm import LocalLM, sample_many
    disable_triton_overrides()
    require_frozen()
    sents = {}
    for u in units():
        sents.setdefault(u["sentence_id"], u["text"])
    sids = sorted(sents, key=lambda s: sha1(s))
    if limit:
        sids = sids[:limit]
    lm = LocalLM(LOCAL_Q8)
    t0 = time.time()
    outs = sample_many(lm, [_sc_messages(sents[s]) for s in sids], n=5, max_new_tokens=300, temperature=0.7, bs=16, tag="sc5_local")
    lm.unload()
    rows = []
    for s, texts in zip(sids, outs):
        forms = [J.extract_formula(t) if t else None for t in texts]
        forms = [f[4:].strip() if f and f.upper().startswith("FOL:") else f for f in forms]
        rows.append({"key": s, "samples_raw": [t[:400] for t in texts], "samples": forms})
    (SCORES / "sc5_local_samples.jsonl").write_text("")
    append_jsonl(SCORES / "sc5_local_samples.jsonl", rows)
    logger.info(f"local SC-5: {len(rows)} sentences in {time.time()-t0:.0f}s")


# =====================================================================================================================
# B2 world_probe
B2_DEV_N = 40


def b2_sets() -> dict[str, list[dict]]:
    """{set: [{key, text, fol}]} — screen (exp A ids), href (expert-corrected refs: gate), rewrites (exp D shared set),
    E (PRIMARY rows, one per item_id), Eref (E references, secondary gate: reference_status is a reference audit)."""
    A = jload(DATA / "expA_screen_items.json")
    H = jload(DATA / "expA_href_items.json")
    D = {r["item_id"]: r for r in jload(DATA / "expD_screen_items.json")}
    rw = jload(DATA / "invariance_items.json")
    out = {"screen": [{"key": r["item_id"], "text": r["text"], "fol": r["candidate_fol"]} for r in A if r.get("candidate_fol")],
           "href": [{"key": r["item_id"], "text": r["text"], "fol": r["candidate_fol"]} for r in H if r.get("candidate_fol")],
           "rewrites": ([{"key": r["rw_id"], "text": r["text"], "fol": r["candidate_fol"]} for r in rw]
                        + [{"key": b, "text": D[b]["text"], "fol": D[b]["candidate_fol"]} for b in sorted({r["base_item_id"] for r in rw})])}
    seen, E = set(), []
    for u in units():
        if u["parse_ok"] and u["item_id"] not in seen:
            seen.add(u["item_id"])
            E.append({"key": u["item_id"], "text": u["text"], "fol": u["candidate_fol"]})
    out["E"] = sorted(E, key=lambda x: sha1(x["key"]))
    from src.e_pool import load_sentences
    ref = []
    for srow in load_sentences(blind=False):
        st = srow.get("output")
        inp = json.loads(srow["input"])
        if st in ("GOLD_PANEL_OK", "TRUSTED_AGREED", "PANEL_REPAIRED") and inp.get("reference_fol"):
            ref.append({"key": "ref:" + srow["metadata_sentence_id"], "text": inp["text"], "fol": inp["reference_fol"],
                        "stratum": srow["metadata_strata"]["source_stratum"], "ref_status": st})
    out["Eref"] = ref
    return out


def _b2_build_worker(chunk):
    import sys as _s
    _s.setrecursionlimit(10000)
    os.environ["PYTHONHASHSEED"] = "0"
    from src.b2_world_probe import build_worlds
    out = []
    for fol in chunk:
        try:
            b = build_worlds(fol, sha1(fol))
        except Exception as e:  # noqa: BLE001 - counted as z3_fail
            b = {"status": "z3_fail", "worlds": [], "why": f"exc:{str(e)[:80]}"}
        out.append((sha1(fol), b))
    return out


def stage_b2_build():
    """World construction (CPU, deterministic, label-free) for every formula of every B2 set."""
    import multiprocessing as mp
    from src.labeller.fol import parse  # noqa: F401
    sets = b2_sets()
    wp = DATA / "b2_worlds.jsonl"
    have = {r["key"] for r in read_jsonl(wp)} if wp.exists() else set()
    fols = []
    for name in ("href", "screen", "rewrites", "Eref", "E"):
        for x in sets[name]:
            if sha1(x["fol"]) not in have and strict_parse_ok(x["fol"]):
                have.add(sha1(x["fol"]))
                fols.append(x["fol"])
    logger.info(f"B2 worlds to build: {len(fols)} formulas; sets {({k: len(v) for k, v in sets.items()})}")
    t0 = time.time()
    chunks = [fols[i:i + 10] for i in range(0, len(fols), 10)]
    n = 0
    with mp.get_context("spawn").Pool(WORKERS) as pool, wp.open("a") as f:
        for res in pool.imap(_b2_build_worker, chunks):
            for k, b in res:
                f.write(json.dumps({"key": k, **b}, ensure_ascii=False) + "\n")
                n += 1
            if n % 1000 < 10:
                logger.info(f"B2 build {n}/{len(fols)} {time.time()-t0:.0f}s")
    W = {r["key"]: r for r in read_jsonl(wp)}
    st = Counter(r["status"] for r in W.values())
    nw = [len(r["worlds"]) for r in W.values() if r["status"] == "ok"]
    tf = [w["phi_truth"] for r in W.values() for w in r["worlds"]]
    meta = {"n_formulas": len(W), "status": dict(st), "mean_worlds_ok": sum(nw) / max(1, len(nw)),
            "share_ge4_worlds": sum(1 for x in nw if x >= 4) / max(1, len(W)), "phi_true_share": sum(tf) / max(1, len(tf)),
            "ops": dict(Counter(w["mutant_op"] for r in W.values() for w in r["worlds"])), "seconds": time.time() - t0}
    jdump(meta, RES / "b2_build_meta.json")
    logger.info(f"B2 build done: {meta}")


def _b2_units(name, sets=None, limit=None):
    sets = sets or b2_sets()
    W = {r["key"]: r for r in read_jsonl(DATA / "b2_worlds.jsonl")}
    out = []
    for x in sets[name]:
        b = W.get(sha1(x["fol"]))
        out.append({**x, "build": b})
    return out[:limit] if limit else out


def b2_dev_keys():
    H = jload(DATA / "expA_href_items.json")
    return set(sorted([r["item_id"] for r in H], key=lambda k: sha1(k + "b2dev"))[:B2_DEV_N])


def _b2_read_local(lm, jobs, variant, max_new_tokens=160):
    from src.b2_world_probe import parse_answers, reader_prompt
    msgs = [[{"role": "user", "content": reader_prompt(t, ws, variant)}] for t, ws in jobs]
    gen = lm.generate(msgs, max_new_tokens=max_new_tokens, tag=f"b2_reader_{variant}", bs=48)
    return [(parse_answers(g["text"], len(ws)), g["text"][:300], g["seconds"]) for g, (t, ws) in zip(gen, jobs)]


def stage_b2_read(limit=None, which=("dev",)):
    """B2 reader over one or more sets: 'dev' (prompt dev, 2 variants, 40 track-H corrected), 'gate', 'screen', 'unbatched',
    'rewrites', 'Eref', 'E'. Backend: local Qwen3-8B (F-KEY), frozen variant in prereg_b2.json (except for 'dev')."""
    from src.b2_world_probe import score
    from src.common import disable_triton_overrides
    from src.local_llm import LocalLM
    disable_triton_overrides()
    require_frozen()
    sets = b2_sets()
    lm = LocalLM(LOCAL_Q8)
    pb2_p = ROOT / "prereg_b2.json"
    for w in which:
        t0 = time.time()
        if w == "dev":
            dev = b2_dev_keys()
            U = [u for u in _b2_units("href", sets) if u["key"] in dev and u["build"] and u["build"]["status"] == "ok"]
            res = {}
            for var in ("v1", "v2"):
                outs = _b2_read_local(lm, [(u["text"], u["build"]["worlds"]) for u in U], var)
                res[var] = _gate_metrics(U, outs)
            chosen = max(("v1", "v2"), key=lambda v: (res[v]["bal_acc"] or 0, v == "v1"))
            rec = {"created_iso": time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime()), "backend": f"local {LOCAL_Q8} greedy",
                   "dev_slice": sorted(dev), "dev_results": res, "chosen_variant": chosen,
                   "rule": "higher balanced accuracy on the 40-item track-H dev slice (tie -> v1); dev items excluded from the gate",
                   "reason_local": "F-KEY: OpenRouter key exhausted; the planned API reader cannot be called"}
            jdump(rec, pb2_p)
            (ROOT / "prereg_b2.sha256").write_text(hashlib.sha256(pb2_p.read_bytes()).hexdigest() + "  prereg_b2.json\n")
            logger.info(f"B2 prompt dev: {res} -> {chosen} (frozen)")
            continue
        var = jload(pb2_p)["chosen_variant"]
        if w == "unbatched":
            U = [u for u in _b2_units("screen", sets) if u["build"] and u["build"]["status"] == "ok"]
            U = sorted(U, key=lambda u: sha1(u["key"] + "unbatched"))[:200]
            jobs, idx = [], []
            for i, u in enumerate(U):
                for j, wd in enumerate(u["build"]["worlds"]):
                    jobs.append((u["text"], [wd]))
                    idx.append((i, j))
            outs = _b2_read_local(lm, jobs, var)
            rows = [{"key": U[i]["key"], "world": j, "verdict": (o[0][0] if o[0] else None)} for (i, j), o in zip(idx, outs)]
            (SCORES / "b2_unbatched.jsonl").write_text("")
            append_jsonl(SCORES / "b2_unbatched.jsonl", rows)
            logger.info(f"B2 unbatched: {len(rows)} single-world calls in {time.time()-t0:.0f}s")
            continue
        name = {"gate": "href", "screen": "screen", "rewrites": "rewrites", "Eref": "Eref", "E": "E"}[w]
        U = _b2_units(name, sets, limit)
        ok = [u for u in U if u["build"] and u["build"]["status"] == "ok"]
        # dedupe identical (text, formula) jobs
        uq = {}
        for u in ok:
            uq.setdefault(sha1(u["text"] + "||" + u["fol"]), (u["text"], u["build"]["worlds"]))
        keys = list(uq)
        outs = dict(zip(keys, _b2_read_local(lm, [uq[k] for k in keys], var)))
        rows = []
        for u in U:
            b = u["build"]
            if not b or b["status"] != "ok":
                rows.append({"key": u["key"], "status": (b or {}).get("status", "parse_fail"), "b2_score": None, "n_worlds": 0})
                continue
            v, raw, secs = outs[sha1(u["text"] + "||" + u["fol"])]
            sc = score(b["worlds"], v)
            rows.append({"key": u["key"], "status": "ok" if v else "reader_fail", **sc, "n_worlds": len(b["worlds"]),
                         "verdicts": v, "phi_truth": [x["phi_truth"] for x in b["worlds"]], "ops": [x["mutant_op"] for x in b["worlds"]],
                         "seconds": secs, "raw": None if v else raw, "variant": var})
        (SCORES / f"b2_{w}.jsonl").write_text("")
        append_jsonl(SCORES / f"b2_{w}.jsonl", rows)
        logger.info(f"B2 {w}: {len(rows)} rows ({len(keys)} reader calls) in {time.time()-t0:.0f}s; status "
                    f"{Counter(r['status'] for r in rows)}")
    lm.unload()


def _gate_metrics(U, outs):
    tp = tn = nt = nf = und = 0
    for u, (v, _, _) in zip(U, outs):
        if v is None:
            continue
        for wd, x in zip(u["build"]["worlds"], v):
            if wd["phi_truth"]:
                nt += 1
                tp += x == "TRUE"
            else:
                nf += 1
                tn += x == "FALSE"
            und += x == "UNDETERMINED"
    return {"n_items": len(U), "n_reader_fail": sum(1 for o in outs if o[0] is None), "n_true_worlds": nt, "n_false_worlds": nf,
            "acc_true": tp / nt if nt else None, "acc_false": tn / nf if nf else None,
            "bal_acc": ((tp / nt) + (tn / nf)) / 2 if nt and nf else None, "undet_share": und / max(1, nt + nf)}


# =====================================================================================================================
def stage_nli(limit=None, which=("local", "api")):
    """NLI both directions (main + alt checkpoint) and mpnet cosine between the text and each verbaliser's output (GPU).
    Columns: rt_nli_{fwd,bwd,min,contra}[_alt] for the API verbaliser, rt_*_local for the local Qwen3-8B verbaliser."""
    from src.common import disable_triton_overrides
    from src.roundtrip import NLI_ALT, NLI_MAIN, embed_cos, nli_probs
    disable_triton_overrides()
    require_frozen()
    text = {u["item_id"]: u["text"] for u in units()}
    for w in which:
        V = load_scores("rt_verbal_" + w)
        keys = [k for k, v in V.items() if v.get("verbalisation")]
        if limit:
            keys = keys[:limit]
        if not keys:
            logger.warning(f"no verbalisations for {w}")
            continue
        sfx = "" if w == "api" else "_local"
        # dedupe (text, verbalisation) pairs
        pk = {k: (text[k], V[k]["verbalisation"]) for k in keys}
        uq = sorted(set(pk.values()))
        fwd = [(t, v) for t, v in uq]
        bwd = [(v, t) for t, v in uq]
        san, _ = nli_probs([(t, t) for t, _ in uq[:20]], NLI_MAIN)
        res = {p: {} for p in uq}
        secs = {}
        for name, model in (("", NLI_MAIN), ("_alt", NLI_ALT)):
            f, s1 = nli_probs(fwd, model)
            b, s2 = nli_probs(bwd, model)
            secs[name or "main"] = s1 + s2
            for p_, x, y in zip(uq, f, b):
                res[p_][f"rt_nli_fwd{name}{sfx}"] = x["entail"]
                res[p_][f"rt_nli_bwd{name}{sfx}"] = y["entail"]
                res[p_][f"rt_nli_min{name}{sfx}"] = min(x["entail"], y["entail"])
                res[p_][f"rt_nli_contra{name}{sfx}"] = max(x["contra"], y["contra"])
        cos, s3 = embed_cos(fwd)
        for p_, c in zip(uq, cos):
            res[p_][f"rt_embed_cos{sfx}"] = c
        n = max(1, len(uq))
        rows = [{"key": k, **res[pk[k]], "nli_seconds": secs["main"] / n, "embed_seconds": s3 / n} for k in keys]
        (SCORES / f"rt_nli_{w}.jsonl").write_text("")
        append_jsonl(SCORES / f"rt_nli_{w}.jsonl", rows)
        jdump({"t7_nli_self_entail_mean": sum(x["entail"] for x in san) / max(1, len(san)), "seconds": secs | {"embed": s3},
               "n_pairs": len(uq), "n_rows": len(rows)}, RES / f"roundtrip_meta_{w}.json")
        logger.info(f"NLI {w}: {len(rows)} rows / {len(uq)} unique pairs; secs {secs}, embed {s3:.0f}")


# =====================================================================================================================
# COLUMN ASSEMBLY (label-free) -> E_baseline_features.jsonl, folds_E.json
BOUNDED = 1.0


def _judge_cols(name, fname, conds=("orig", "disg"), subset=None):
    """-> {col: {item_id: v}}, {col: {item_id: status}} ; None if the component never produced a score."""
    J = load_scores(fname)
    if not any(r.get("p") is not None for r in J.values()):
        return None
    cols, st = {}, {}
    for cond in conds:
        c = f"{name}_{cond}"
        cols[c], st[c] = {}, {}
        for u in units():
            iid = u["item_id"]
            if subset is not None and iid not in subset:
                continue
            if not u["parse_ok"]:
                cols[c][iid], st[c][iid] = BOUNDED, "fail"
                continue
            r = J.get(f"{iid}|{cond}")
            if r is None:
                st[c][iid] = "missing"
                continue
            if r.get("p") is None:
                cols[c][iid], st[c][iid] = 0.5, "fallback"  # pre-declared JSON/no-verdict fallback
            else:
                cols[c][iid], st[c][iid] = 1.0 - float(r["p"]), "ok"
    return cols, st


def build_columns():
    """All oriented baseline columns (label-free). Returns cols, status, fail_fill, thresholds, missing_components, types."""
    U = units()
    ids = list(dict.fromkeys(u["item_id"] for u in U))
    Ub = {u["item_id"]: u for u in U}
    cols, st, missing = {}, {}, []
    thr_d = jload(DATA / "expD_analysis.json")["thresholds"]

    def put(c, iid, v, s_):
        cols.setdefault(c, {})
        st.setdefault(c, {})
        cols[c][iid] = v
        st[c][iid] = s_
    # parse + pilot
    P = load_scores("pilot")
    for iid in ids:
        u = Ub[iid]
        put("parse_fail", iid, 0.0 if u["parse_ok"] else 1.0, "ok")
        p = P.get(iid, {})
        for c in ("pilot_joint_conflict", "pilot_arity_incons", "pilot_shape_incons", "pilot_dangling", "pilot_rerun_jacc"):
            if not u["parse_ok"]:
                put(c, iid, None, "fail")
                continue
            v = p.get(c)
            if c == "pilot_rerun_jacc":
                put(c, iid, None if v is None else 1.0 - v, "na" if v is None else "ok")
            elif c == "pilot_joint_conflict":
                put(c, iid, None if v is None else float(v), "fail" if v is None else "ok")
            else:
                put(c, iid, None if v is None else float(v), "na" if v is None else "ok")
    # round trip
    for w, sfx in (("api", ""), ("local", "_local")):
        R = load_scores(f"rt_nli_{w}")
        if not R:
            missing.append(f"roundtrip_{w}")
            continue
        for base in ("rt_nli_min", "rt_nli_fwd", "rt_nli_bwd", "rt_nli_contra", "rt_nli_min_alt", "rt_embed_cos"):
            c = base + sfx
            for iid in ids:
                if not Ub[iid]["parse_ok"]:
                    put(c, iid, None, "fail")
                    continue
                r = R.get(iid)
                key = f"{base}{sfx}" if base != "rt_nli_min_alt" else f"rt_nli_min_alt{sfx}"
                if r is None or r.get(key) is None:
                    put(c, iid, None, "fail")
                    continue
                v = r[key]
                put(c, iid, v if base == "rt_nli_contra" else 1.0 - v, "ok")
    # judges
    frame_ids = {r["item_id"] for r in jload(DATA / "frontier_frame.json")["rows"]}
    for name, fname, subset in (("judge_cheap", "judge_cheap", None), ("judge_cheap2", "judge_cheap2", None),
                                ("judge_strong", "judge_strong", frame_ids), ("judge_local_qwen8b", "judge_local_qwen8b", None),
                                ("judge_local_llama8b", "judge_local_llama8b", None), ("judge_local_qwen14b", "judge_local_qwen14b", frame_ids)):
        r = _judge_cols(name, fname, subset=subset)
        if r is None:
            missing.append(name)
            continue
        for c in r[0]:
            cols[c], st[c] = r[0][c], r[1][c]
            if subset is None and sum(1 for v in st[c].values() if v == "missing") > 0.5 * len(ids):
                missing.append(f"{c}(partial)")
    # SC-5
    for nm in ("sc5", "sc5_local"):
        S = load_scores(nm)
        if not S:
            missing.append(nm)
            continue
        for iid in ids:
            if not Ub[iid]["parse_ok"]:
                put(f"{nm}_eq_frac", iid, None, "fail")
                put(f"{nm}_entropy", iid, None, "fail")
                continue
            r = S.get(iid)
            if r is None:
                put(f"{nm}_eq_frac", iid, None, "fail")
                put(f"{nm}_entropy", iid, None, "fail")
                continue
            put(f"{nm}_eq_frac", iid, 1.0 - r["sc5_eq_frac"], "ok")
            put(f"{nm}_entropy", iid, r["sc5_entropy"], "ok")
    # B2
    B = load_scores("b2_E")
    if not B:
        missing.append("b2")
    else:
        for iid in ids:
            for c in ("b2_score", "b2_mismatch_det", "b2_undet_share"):
                if not Ub[iid]["parse_ok"]:
                    put(c, iid, None, "fail")
                    continue
                r = B.get(iid)
                if r is None:
                    put(c, iid, None, "missing")
                elif r["status"] != "ok" or r.get(c) is None:
                    put(c, iid, 0.5, "fallback")
                else:
                    put(c, iid, float(r[c]), "ok")
    B = load_scores("b2api_E")
    if B:
        thr_api = jload(RES / "b2api_threshold.json") if (RES / "b2api_threshold.json").exists() else {}
        for iid in ids:
            for c in ("b2_score", "b2_mismatch_det", "b2_undet_share"):
                ca = c.replace("b2_", "b2api_")
                if not Ub[iid]["parse_ok"]:
                    put(ca, iid, None, "fail")
                    continue
                r = B.get(iid)
                if r is None:
                    put(ca, iid, None, "missing")
                elif r["status"] != "ok" or r.get(c) is None:
                    put(ca, iid, 0.5, "fallback")
                else:
                    put(ca, iid, float(r[c]), "ok")
    fail_fill = {}
    for c, vals in cols.items():
        if c in ("pilot_arity_incons", "pilot_shape_incons"):
            fail_fill[c] = max([v for v in vals.values() if v is not None] or [1.0])
        elif c.endswith("_entropy"):
            fail_fill[c] = math.log(6)
        else:
            fail_fill[c] = BOUNDED
    # thresholds frozen from the screen (prereg)
    thr = {}
    for c in cols:
        if c in thr_d:
            thr[c] = thr_d[c]
        elif c.startswith("judge_"):
            thr[c] = 0.5
        elif c == "rt_nli_min_local":
            thr[c] = thr_d["rt_nli_min_localverb"]
        elif c.endswith("_local") and c.replace("_local", "") in thr_d:
            thr[c] = thr_d[c.replace("_local", "")]
        elif c.startswith("sc5"):
            thr[c] = 0.5
        elif c.startswith("b2_"):
            g = RES / "b2_threshold.json"
            thr[c] = jload(g)[c] if g.exists() else 0.5
        elif c.startswith("b2api_"):
            g = RES / "b2api_threshold.json"
            thr[c] = jload(g)[c.replace("b2api_", "b2_")] if g.exists() else 0.5
        else:
            thr[c] = 0.5
    return cols, st, fail_fill, thr, missing


def stage_s4():
    """Label-free: E_baseline_features.jsonl (every oriented column + status per E row) and folds_E.json."""
    from src.s4 import build_feature_table, write_table
    cols, st, fail_fill, thr, missing = build_columns()
    U = units()
    table = build_feature_table(U, cols, {c: {k: ("ok" if v == "ok" else ("fail" if v in ("fail", "fallback") else "na"))
                                              for k, v in st[c].items()} for c in st})
    # fallback values (0.5) are real values -> keep them; 'fail' rows get the worst value in fit_s4_oof
    for r in table:
        for c in cols:
            if st[c].get(r["item_id"]) == "fallback":
                r[c + "__status"] = "fallback"
    write_table(table, ROOT / "E_baseline_features.jsonl")
    folds = {"rule": "int(sha1('E_folds_v1|'+sentence_id),16) % 5",
             "sentence_fold": {u["sentence_id"]: u["fold_E"] for u in U},
             "item_fold": {u["item_id"]: u["fold_E"] for u in U}, "row_fold": {u["row_key"]: u["fold_E"] for u in U}}
    jdump(folds, ROOT / "folds_E.json")
    jdump({"columns": sorted(cols), "fail_fill": fail_fill, "thresholds": thr, "missing_components": missing}, RES / "feature_meta.json")
    logger.info(f"feature table: {len(table)} rows x {len(cols)} columns; missing components {missing}; "
                f"folds {Counter(u['fold_E'] for u in U)}")


# =====================================================================================================================
def stage_b2_gate_report(which=("b2",)):
    for prefix in which:
        _b2_gate_report(prefix)


def _b2_gate_report(prefix="b2"):
    """Reader gate (track-H expert-corrected formulas, dev slice excluded; E trusted references per stratum) and the B2
    thresholds (90th percentile on screen track-H CORRECT items) — screen data only, no E label."""
    import numpy as np
    dev = b2_dev_keys()
    G = load_scores(f"{prefix}_gate")
    H = {r["item_id"]: r for r in jload(DATA / "expA_href_items.json")}

    def gm(rows):
        tp = tn = nt = nf = und = 0
        for r in rows:
            if r.get("status") != "ok":
                continue
            for v, t in zip(r["verdicts"], r["phi_truth"]):
                if t:
                    nt += 1
                    tp += v == "TRUE"
                else:
                    nf += 1
                    tn += v == "FALSE"
                und += v == "UNDETERMINED"
        return {"n_items": len(rows), "n_ok": sum(1 for r in rows if r.get("status") == "ok"), "n_true_worlds": nt, "n_false_worlds": nf,
                "acc_true": tp / nt if nt else None, "acc_false": tn / nf if nf else None,
                "bal_acc": ((tp / nt) + (tn / nf)) / 2 if nt and nf else None, "undet_share": und / max(1, nt + nf)}
    prim = [r for k, r in G.items() if k not in dev]
    out = {"primary_gate_trackH_corrected": gm(prim)}
    by_src = defaultdict(list)
    for k, r in G.items():
        if k not in dev:
            by_src[H.get(k, {}).get("role", "?")].append(r)
    out["primary_by_source"] = {k: gm(v) for k, v in by_src.items()}
    ER = load_scores(f"{prefix}_Eref")
    if ER:
        sets = {x["key"]: x for x in b2_sets()["Eref"]}
        by = defaultdict(list)
        for k, r in ER.items():
            by[sets[k]["stratum"]].append(r)
        out["secondary_E_references"] = {st: gm(v) for st, v in sorted(by.items())}
        out["secondary_E_references"]["ALL"] = gm(list(ER.values()))
    ba = out["primary_gate_trackH_corrected"]["bal_acc"]
    out["gate_threshold"] = 0.85
    out["passed"] = bool(ba is not None and ba >= 0.85)
    out["eligibility"] = "ELIGIBLE_FOR_FUSION" if out["passed"] else "NOT_ELIGIBLE_FOR_FUSION"
    # thresholds from screen track-H CORRECT (exp A labels; screen data)
    A = {r["item_id"]: r for r in jload(DATA / "expA_screen_items.json")}
    S = load_scores(f"{prefix}_screen")
    thr = {}
    for c in ("b2_score", "b2_mismatch_det", "b2_undet_share"):
        v = [r[c] for k, r in S.items() if A.get(k, {}).get("track") == "H" and A[k]["label"] == "CORRECT" and r.get("status") == "ok"
             and r.get(c) is not None]
        thr[c] = float(np.percentile(v, 90)) if v else 0.5
    thr["n_ref_items"] = len([1 for k, r in S.items() if A.get(k, {}).get("track") == "H" and A[k]["label"] == "CORRECT" and r.get("status") == "ok"])
    jdump(thr, RES / f"{prefix}_threshold.json")
    # T2 sanity on the screen (labels allowed: screen data): AUROC on track L CORRECT vs ERROR, and track H
    from src.analysis import auc_w
    san = {}
    for tr in ("L", "H"):
        ks = [k for k, r in S.items() if A.get(k, {}).get("track") == tr and A[k]["label"] in ("CORRECT", "ERROR")]
        y = np.array([1 if A[k]["label"] == "ERROR" else 0 for k in ks])
        for c in ("b2_score", "b2_mismatch_det", "b2_undet_share"):
            sc = np.array([S[k][c] if (S[k].get("status") == "ok" and S[k].get(c) is not None) else 0.5 for k in ks], dtype=float)
            san[f"{tr}|{c}"] = {"auroc": auc_w(y, sc) if len(set(y)) == 2 else None, "n_pos": int(y.sum()), "n_neg": int(len(y) - y.sum()),
                                "n_status_ok": sum(1 for k in ks if S[k].get("status") == "ok")}
    out["screen_sanity_auroc"] = san
    out["thresholds"] = thr
    jdump(out, RES / f"{prefix}_gate.json")
    logger.info(f"{prefix} gate: {out['primary_gate_trackH_corrected']} -> {out['eligibility']}; thr {thr}; screen {san}")


def stage_sc_invariance():
    """SC-5 on the SAME shared rewrite set as exp D (rw_ids), from exp C's existing gpt-4.1-nano samples (no new calls)."""
    from src.labeller.labeller import parse_ok
    rw = jload(DATA / "invariance_items.json")
    D = {r["item_id"]: r for r in jload(DATA / "expD_screen_items.json")}
    smp = defaultdict(dict)
    for r in read_jsonl(EXPC / "results" / "sc_samples.jsonl"):
        if r.get("arm") == "sc_cheap":
            smp[r["sentence_norm"]][r["sample"]] = r.get("fol") if r.get("parse_ok") else None
    items = [(r["rw_id"], r["text"], r["candidate_fol"]) for r in rw] + [(b, D[b]["text"], D[b]["candidate_fol"]) for b in sorted({r["base_item_id"] for r in rw})]
    pairs, have = [], 0
    for k, t, f in items:
        ss = smp.get(norm(t))
        if not ss:
            continue
        have += 1
        for x in ss.values():
            if x and f and x != f:
                pairs.append((f, x))
    logger.info(f"SC invariance: {have}/{len(items)} items have exp C samples; {len(pairs)} pairs")
    res = {}
    chunks = [pairs[i:i + 20] for i in range(0, len(pairs), 20)]
    import multiprocessing as mp
    with mp.get_context("spawn").Pool(WORKERS) as pool:
        for out in pool.imap_unordered(_sc_pair_worker, chunks):
            for r in out:
                res[(r["a"], r["b"])] = r["eq"]
    rows = []
    for k, t, f in items:
        ss = smp.get(norm(t))
        if not ss or not f or not parse_ok(f):
            rows.append({"key": k, "sc5_eq_frac": None})
            continue
        vals = [ss.get(i) for i in range(5)]
        eqs = [(x == f) or bool(res.get((f, x))) if x else False for x in vals]
        rows.append({"key": k, "sc5_eq_frac": sum(eqs) / 5, "n_samples": sum(1 for x in vals if x)})
    (SCORES / "sc5_rewrites_expC.jsonl").write_text("")
    append_jsonl(SCORES / "sc5_rewrites_expC.jsonl", rows)
    logger.info(f"SC invariance rows {len(rows)}; with score {sum(1 for r in rows if r['sc5_eq_frac'] is not None)}")


# =====================================================================================================================
S1_E = ["parse_fail", "pilot_joint_conflict", "pilot_arity_incons", "pilot_shape_incons", "pilot_dangling", "pilot_rerun_jacc"]
S2_API = ["rt_nli_min", "rt_nli_fwd", "rt_nli_bwd", "rt_nli_contra", "rt_embed_cos"]
S2_LOCAL = ["rt_nli_min_local", "rt_nli_fwd_local", "rt_nli_bwd_local", "rt_nli_contra_local", "rt_embed_cos_local"]
S3_API = ["judge_cheap_disg", "judge_cheap_orig", "judge_cheap2_disg", "judge_cheap2_orig"]
S3_LOCAL = ["judge_local_qwen8b_disg", "judge_local_qwen8b_orig", "judge_local_llama8b_disg", "judge_local_llama8b_orig"]
SC_API = ["sc5_eq_frac", "sc5_entropy"]
SC_LOCAL = ["sc5_local_eq_frac", "sc5_local_entropy"]


def stage_analysis():
    import numpy as np
    from src import analysis_E as AE
    from src.analysis import ClusterBoot, auc_w, boot_auc, ci
    from src.e_pool import load_E, load_sentences, regime_labels, label_vector_sha1
    from src.s4 import fit_s4_oof, read_table
    pre = require_frozen()
    full = load_E(blind=False)  # raises unless the prereg predates every score file
    fr_by = {r["row_key"]: r for r in full}
    U = units()
    Ur = {u["row_key"]: u for u in U}
    clusters = {u["row_key"]: u["sentence_id"] for u in U}
    strata = {u["row_key"]: {**u["strata"]} for u in U}
    cols, st, fail_fill, thr, missing = build_columns()
    have = set(cols)
    A: dict = {"prereg_sha256": PREREG_SHA.read_text().split()[0], "missing_components": missing, "thresholds": thr,
               "fail_fill": fail_fill}
    regimes = {r: regime_labels(full, r) for r in ("R_AB", "R_A", "COVERAGE", "CONTESTED_AS_CORRECT", "CONTESTED_AS_ERROR",
                                                   "ALL_TIERS", "R_AB_L25_NO_TOPUP")}
    A["label_vectors"] = {r: {"n": len(v), "sha1": label_vector_sha1([fr_by[k]["metadata_item_id"] for k in sorted(v)],
                                                                     ["ERROR" if v[k] else "CORRECT" for k in sorted(v)]),
                              "sha1_rowkey": label_vector_sha1(sorted(v), ["ERROR" if v[k] else "CORRECT" for k in sorted(v)])}
                          for r, v in regimes.items() if r in ("R_AB", "R_A")}
    A["label_vectors_match_prereg"] = all(A["label_vectors"][r]["sha1"] == pre["label_vectors"][r]["sha1"] for r in ("R_AB", "R_A"))
    # ---------------- S4 fits (labels used here only, cross-fitted on folds_E)
    table = read_table(ROOT / "E_baseline_features.jsonl")
    folds = {r["row_key"]: r["metadata_fold_E"] for r in table}
    api_ok = all(c in have for c in ("judge_cheap_disg", "judge_cheap_orig"))
    fsets = {}
    if api_ok:
        fsets["S4"] = [f for f in S1_E + S2_API + S2_LOCAL + S3_API + SC_API if f in have]
        fsets["S4_iter1"] = [f for f in S1_E + S2_API + S3_API if f in have]
    fsets["S4_local"] = [f for f in S1_E + S2_LOCAL + S3_LOCAL + SC_LOCAL if f in have]
    fsets["S4_local_iter1set"] = [f for f in S1_E + S2_LOCAL + S3_LOCAL if f in have]
    fsets["S4_local_noLLMjudge"] = [f for f in S1_E + S2_LOCAL + SC_LOCAL if f in have]
    if "b2_score" in have:
        fsets["S4_local_plus_B2"] = fsets["S4_local"] + ["b2_score", "b2_undet_share"]
    train_pool = [r for r in table if r["pool"] == "E_POOL"]
    lab_rab = {k: v for k, v in regimes["R_AB"].items() if Ur[k]["pool"] == "E_POOL"}
    lab_all = {k: v for k, v in regimes["ALL_TIERS"].items() if Ur[k]["pool"] == "E_POOL"}
    s4cols, s4info = {}, {}
    for nm, feats in fsets.items():
        for reg, lab in (("RAB", lab_rab), ("ALLTIERS", lab_all)):
            if reg == "ALLTIERS" and nm not in ("S4", "S4_local"):
                continue
            oof, info = fit_s4_oof(train_pool, lab, folds, feats, C=1.0, fail_fill=fail_fill)
            c = f"{nm}_oof_{reg}"
            s4cols[c] = oof
            s4info[c] = {"features": feats, "features_used": info["features_used"], "fold_thresholds": info["thresholds"],
                         "n_train_per_fold": info["n_train_per_fold"], "coefs": info["coefs"]}
            if reg == "RAB":
                s4cols[f"{nm}_flag"] = {k: float(v) for k, v in info["flags"].items()}
        # shuffled-label self-check (should be ~0.5)
    rng = np.random.default_rng(0)
    ks = sorted(lab_rab)
    perm = dict(zip(ks, rng.permutation([lab_rab[k] for k in ks]).tolist()))
    oof_sh, _ = fit_s4_oof(train_pool, perm, folds, fsets["S4_local"], C=1.0, fail_fill=fail_fill)
    yk = [k for k in ks if Ur[k]["parse_ok"]]
    A["S4_shuffled_label_check"] = {
        "oof_auroc_vs_shuffled_labels": float(auc_w(np.array([perm[k] for k in yk]), np.array([oof_sh[k] for k in yk]))),
        "oof_auroc_of_shuffled_fit_vs_true_labels": float(auc_w(np.array([lab_rab[k] for k in yk]), np.array([oof_sh[k] for k in yk]))),
        "note": "S4_local refit on permuted R_AB labels. The placebo (AUROC against the permuted labels) must be ~0.5. The second "
                "number is NOT a placebo: a noise-fitted linear model still ranks items by a random direction in an informative "
                "feature space (AUROC is scale-free), so it can sit far from 0.5 in either direction."}
    jdump(s4info, RES / "s4_coefs.json")
    # ---------------- analysis table
    rows_all = [u for u in U]
    T = AE.make_table(rows_all, cols, {c: {k: ("fail" if v == "fail" else ("na" if v in ("na", "missing") else "ok")) for k, v in st[c].items()}
                                       for c in st}, fail_fill, clusters)
    for c, vals in s4cols.items():
        T[c] = {u["row_key"]: (AE.NA if vals.get(u["row_key"]) is None else float(vals[u["row_key"]])) for u in rows_all}
        T["_max"][c] = 1.0
        thr[c] = 0.5 if c.endswith("_flag") else float(np.median(s4info.get(c, {}).get("fold_thresholds") or [0.5]))
    metrics = [c for c in list(cols) + list(s4cols) if c in T]
    full_cov = [m for m in metrics if not m.startswith(("judge_strong", "judge_local_qwen14b"))]
    bar = "judge_cheap_disg" if "judge_cheap_disg" in have else "judge_local_qwen8b_disg"
    A["bar"] = bar
    A["bar_note"] = ("pre-registered API bar" if bar == "judge_cheap_disg" else
                     "F-KEY: API judges could not be called (shared key exhausted); the bar is the LOCAL Qwen3-8B disguised judge "
                     "(exp D prereg_local rubric B) — a secondary judge, NOT the pre-registered flash-lite bar")

    def keys_for(pool, regime, primary=True, strat=None, extra=None):
        lab = regimes[regime]
        out = []
        for u in U:
            k = u["row_key"]
            if k not in lab or u["pool"] != pool:
                continue
            if primary and not u["parse_ok"]:
                continue
            if strat and u["strata"]["source_stratum"] not in strat:
                continue
            if extra and not extra(u):
                continue
            out.append(k)
        return out, np.array([lab[k] for k in out])
    # (a)+(b) main blocks
    blocks = {}
    spec = [("R_AB|pooled", "E_POOL", "R_AB", True, None, None), ("R_A|pooled_L20_EXC_CTRL", "E_POOL", "R_A", True, ["L20", "EXC", "CTRL"], None),
            ("R_A|pooled_all", "E_POOL", "R_A", True, None, None),
            ("COVERAGE|pooled", "E_POOL", "COVERAGE", False, None, None),
            ("R_AB|long_L25_L20_EXC", "E_POOL", "R_AB", True, ["L25", "L20", "EXC"], None),
            ("R_AB|L25_no_topup", "E_POOL", "R_AB", True, ["L25"], lambda u: not u["strata"].get("l25_topup_batch")),
            ("CONTESTED_AS_CORRECT|pooled", "E_POOL", "CONTESTED_AS_CORRECT", True, None, None),
            ("CONTESTED_AS_ERROR|pooled", "E_POOL", "CONTESTED_AS_ERROR", True, None, None),
            ("ALL_TIERS|pooled", "E_POOL", "ALL_TIERS", True, None, None),
            ("GOLDSYS|R_AB", "GOLDSYS", "R_AB", True, None, None), ("CCG|ALL_TIERS", "CCG", "ALL_TIERS", False, None, None)]
    for st_ in AE.STRATA:
        spec.append((f"R_AB|{st_}", "E_POOL", "R_AB", True, [st_], None))
        spec.append((f"R_A|{st_}", "E_POOL", "R_A", True, [st_], None))
    for name, pool, reg, prim, strat, extra in spec:
        ks_, y_ = keys_for(pool, reg, prim, strat, extra)
        if len(ks_) == 0 or len(set(y_.tolist())) < 2:
            blocks[name] = {"n": len(ks_), "note": "single class / empty"}
            continue
        b, _, _ = AE.eval_block(name, ks_, y_, T, thr, metrics, bar, compute_delta=True)
        b["regime"], b["pool"] = reg, pool
        if not b["testable"]:
            b["note"] = "UNTESTABLE cell (<50/50 rows or <25 sentences per side): descriptive / sign only"
        blocks[name] = b
        logger.info(f"block {name}: n={b['n']} pos={b['n_pos']} testable={b['testable']} bar AUROC "
                    f"{b['metrics'].get(bar, {}).get('auroc')}")
    A["sets"] = blocks
    # (c) frontier / larger judge on the frame
    frame = jload(DATA / "frontier_frame.json")["rows"]
    frows = [{"row_key": r["item_id"], "incl_prob": r["incl_prob"]} for r in frame]
    pairs = [("judge_strong_orig", "judge_cheap_orig"), ("judge_strong_disg", "judge_cheap_disg"), ("judge_strong_orig", "judge_cheap_disg"),
             ("judge_local_qwen14b_orig", "judge_local_qwen8b_orig"), ("judge_local_qwen14b_disg", "judge_local_qwen8b_disg"),
             ("judge_local_qwen14b_orig", "judge_local_qwen8b_disg"), ("judge_strong_orig", "judge_local_qwen8b_disg")]
    A["frontier_frame"] = AE.frame_analysis(frows, regimes["R_AB"], T, [p_ for p_ in pairs if p_[0] in T and p_[1] in T], clusters)
    A["frontier_frame"]["note"] = ("judge_strong = " + ("gemini-3.1-pro-preview (API)" if "judge_strong_orig" in have else
                                   "NOT RUN (F-KEY); the local Qwen3-14B-nf4 larger judge is reported instead (NOT a frontier model)"))
    # cost per call
    costs = read_jsonl(RES / "costs.jsonl") if (RES / "costs.jsonl").exists() else []
    by_c = defaultdict(list)
    for c_ in costs:
        by_c[c_["component"]].append(c_["cost"])
    A["api_cost"] = {k: {"calls": len(v), "usd": round(sum(v), 5), "usd_per_call": round(sum(v) / len(v), 7)} for k, v in by_c.items()}
    A["api_spend_total_usd"] = round(sum(c_["cost"] for c_ in costs), 5)
    sp = A["api_cost"].get("strong", {}).get("usd_per_call")
    A["frontier_frame"]["cost_gate"] = {"gate_usd_per_item": 0.002, "strong_usd_per_call": sp,
                                        "passes": None if sp is None else bool(2 * sp <= 0.002)}
    # (d) contamination
    kE, _ = keys_for("E_POOL", "R_AB", True)
    kG, _ = keys_for("GOLDSYS", "R_AB", True)
    comp = {"judge_cheap": ("judge_cheap_orig", "judge_cheap_disg"), "judge_cheap2": ("judge_cheap2_orig", "judge_cheap2_disg"),
            "judge_local_qwen8b": ("judge_local_qwen8b_orig", "judge_local_qwen8b_disg"),
            "judge_local_llama8b": ("judge_local_llama8b_orig", "judge_local_llama8b_disg")}
    A["contamination"] = AE.contamination({k: v for k, v in comp.items() if v[0] in T}, kE, kG, regimes["R_AB"], T, clusters)
    A["contamination"]["not_applicable"] = {"judge_strong / judge_local_qwen14b": "frame rows are E_POOL only (no GOLDSYS arm)",
                                            "b2_reader": "text-only reader never sees a formula or gold (no disguise contrast)",
                                            "rt_api_verbaliser_disg": "not run (F-KEY / budget)"}
    # (e) recall per error type at matched FA + error_type field accuracy
    kP, yP = keys_for("E_POOL", "R_AB", True)
    types = [AE.error_type_of(fr_by[k]) if yP[i] == 1 else "CORRECT" for i, k in enumerate(kP)]
    cbP = ClusterBoot([clusters[k] for k in kP])
    judges_e = [m for m in ("judge_cheap_orig", "judge_cheap_disg", "judge_cheap2_orig", "judge_cheap2_disg", "judge_local_qwen8b_orig",
                            "judge_local_qwen8b_disg", "judge_local_llama8b_orig", "judge_local_llama8b_disg", "b2_score", "sc5_local_eq_frac",
                            "rt_nli_min_local", "S4_local_oof_RAB") if m in T]
    A["recall_by_type"] = AE.recall_by_type(kP, yP, types, T, judges_e, cbP)
    A["error_type_distribution"] = dict(Counter(t for t in types if t != "CORRECT"))
    jt = {}
    for nm, fname in (("judge_cheap_orig", ("judge_cheap", "orig")), ("judge_cheap_disg", ("judge_cheap", "disg")),
                      ("judge_local_qwen8b_orig", ("judge_local_qwen8b", "orig")), ("judge_local_qwen8b_disg", ("judge_local_qwen8b", "disg"))):
        J = load_scores(fname[0])
        if J:
            jt[nm] = {k: (J.get(f"{Ur[k]['item_id']}|{fname[1]}") or {}).get("type") for k in kP}
    A["error_type_field_accuracy"] = AE.error_type_accuracy(kP, types, jt, yP)
    # frame recall per type for the larger judges (descriptive)
    kF = [r["row_key"] for r in frows if r["row_key"] in regimes["R_AB"]]
    yF = np.array([regimes["R_AB"][k] for k in kF])
    tF = [AE.error_type_of(fr_by[k]) if yF[i] == 1 else "CORRECT" for i, k in enumerate(kF)]
    A["recall_by_type_frame"] = AE.recall_by_type(kF, yF, tF, T, [m for m in ("judge_strong_orig", "judge_strong_disg", "judge_local_qwen14b_orig",
                                                                            "judge_local_qwen14b_disg", "judge_local_qwen8b_disg") if m in T],
                                                  ClusterBoot([clusters[k] for k in kF]))
    # (f) complexity
    main_m = [m for m in full_cov if not m.endswith("_flag")]
    A["complexity"] = AE.complexity(kP, yP, strata, T, main_m)
    gee_m = [m for m in ("judge_cheap_disg", "judge_cheap_orig", "judge_cheap2_disg", "judge_local_qwen8b_disg", "judge_local_qwen8b_orig",
                         "judge_local_llama8b_disg", "S4_local_oof_RAB", "S4_oof_RAB", "sc5_local_eq_frac", "sc5_eq_frac", "rt_nli_min_local",
                         "rt_nli_min", "b2_score") if m in T]
    A["complexity_gee"] = AE.gee_slopes(kP, yP, strata, clusters, T, thr, gee_m)
    # (g) coverage, $ and seconds per item
    cov = {}
    Epool = [u for u in U if u["pool"] == "E_POOL"]
    for c in cols:
        stc = Counter(st[c].get(u["item_id"], "na") for u in Epool)
        cov[c] = {"n_rows": len(Epool), "usable_share": round(stc.get("ok", 0) / len(Epool), 4), "status": dict(stc)}
    A["coverage"] = cov
    secs = {}
    for fname in ("judge_local_qwen8b", "judge_local_llama8b", "judge_local_qwen14b", "rt_verbal_local", "b2_E", "judge_cheap", "judge_strong"):
        R = load_scores(fname)
        v = [r.get("seconds") for r in R.values() if r.get("seconds")]
        if v:
            secs[fname] = {"n": len(v), "mean_seconds_per_unit": round(float(np.mean(v)), 4)}
    A["seconds_per_item"] = secs
    A["gpu_cost_equivalent"] = {"note": "local GPU seconds are amortised batch seconds per item (RTX 4090); API cost 0",
                                "usd_per_gpu_hour_assumed": 0.34}
    # (h) label quality
    A["label_quality"] = AE.label_quality(full, load_sentences(blind=False))
    # (i) system level
    kS = [k for k in kP if Ur[k]["pool"] == "E_POOL"]
    A["system_level"] = AE.system_level(kS, np.array([regimes["R_AB"][k] for k in kS]), [Ur[k]["sysvar"] for k in kS], clusters, T,
                                        [m for m in main_m if m in T])
    # (j) invariance on the shared rewrite set (same rw_ids as exp D)
    A["invariance"] = invariance_table(thr)
    # (k) B2 report
    A["b2"] = b2_report(kP, yP, types, T, thr, [AE.dropped_condition(fr_by[k]) if yP[i] == 1 else False for i, k in enumerate(kP)])
    jdump(A, RES / "analysis_E.json")
    write_tables(A)
    write_summary(A)
    write_method_out(T, s4cols, regimes, full)
    logger.info("analysis written")


def invariance_table(thr):
    rw = jload(DATA / "invariance_items.json")
    fam_of = {r["rw_id"]: r["family"] for r in rw}
    base_of = {r["rw_id"]: r["base_item_id"] for r in rw}
    out = {"note": "same 282 rewrite ids + 150 base items as exp D (track-L CORRECT bases); FA = flagged share at the frozen "
                   "screen threshold; flip = share of (base, rewrite) pairs whose flag differs"}
    srcs = {}
    B = load_scores("b2_rewrites")
    if B:
        srcs["b2_score"] = ({k: (r["b2_score"] if r.get("status") == "ok" else 0.5) for k, r in B.items()}, thr.get("b2_score", 0.5))
        srcs["b2_undet_share"] = ({k: (r["b2_undet_share"] if r.get("status") == "ok" else 0.5) for k, r in B.items()}, thr.get("b2_undet_share", 0.5))
    S = load_scores("sc5_rewrites_expC")
    if S:
        srcs["sc5_cheap_expC_samples"] = ({k: (None if r["sc5_eq_frac"] is None else 1 - r["sc5_eq_frac"]) for k, r in S.items()}, 0.5)
    for m, (vals, t) in srcs.items():
        fam = defaultdict(lambda: {"n": 0, "fa_rw": 0, "fa_base": 0, "flip": 0})
        for rid, f in fam_of.items():
            a, b = vals.get(rid), vals.get(base_of[rid])
            if a is None or b is None:
                continue
            x = fam[f]
            x["n"] += 1
            x["fa_rw"] += a > t
            x["fa_base"] += b > t
            x["flip"] += (a > t) != (b > t)
        out[m] = {f: {"n": x["n"], "fa_base": round(x["fa_base"] / x["n"], 3), "fa_rewrite": round(x["fa_rw"] / x["n"], 3),
                      "flip_rate": round(x["flip"] / x["n"], 3)} for f, x in sorted(fam.items()) if x["n"]}
    out["expD_judges_same_rw_ids"] = jload(DATA / "expD_analysis.json").get("invariance")
    return out


def b2_report(kP, yP, types, T, thr, dropped):
    import numpy as np
    from src.analysis import auc_w
    rep = {"gate": jload(RES / "b2_gate.json") if (RES / "b2_gate.json").exists() else None,
           "build": jload(RES / "b2_build_meta.json") if (RES / "b2_build_meta.json").exists() else None,
           "prereg_b2": jload(ROOT / "prereg_b2.json") if (ROOT / "prereg_b2.json").exists() else None}
    B = load_scores("b2_E")
    U = {u["row_key"]: u for u in units()}
    if not B:
        rep["status"] = "b2_E not run"
        return rep
    rep["status_counts_E"] = dict(Counter(r["status"] for r in B.values()))
    # per-op mismatch among CORRECT vs ERROR rows
    per = defaultdict(lambda: {0: [], 1: []})
    for k, y in zip(kP, yP):
        r = B.get(U[k]["item_id"])
        if not r or r.get("status") != "ok":
            continue
        for op, v in (r.get("per_op") or {}).items():
            per[op][int(y)].append(v)
    rep["per_op_mismatch"] = {op: {"CORRECT_mean": round(float(np.mean(d[0])), 4) if d[0] else None,
                                   "ERROR_mean": round(float(np.mean(d[1])), 4) if d[1] else None, "n": [len(d[0]), len(d[1])]}
                              for op, d in sorted(per.items())}
    # dropped-condition hypothesis: b2_undet_share for DROP-typed errors vs CORRECT
    drop = [i for i, d in enumerate(dropped) if d]
    cor = [i for i, y in enumerate(yP) if y == 0]
    s = np.array([(B.get(U[kP[i]]["item_id"]) or {}).get("b2_undet_share") for i in drop + cor], dtype=float)
    yy = np.array([1] * len(drop) + [0] * len(cor))
    rep["undet_share_DROP_vs_CORRECT"] = {"auroc": round(float(auc_w(yy, s)), 4) if len(drop) and len(cor) else None,
                                          "n_drop": len(drop), "n_correct": len(cor),
                                          "types_used": "dropped-condition errors: tier-A repair ops contain ADD, or tier-B panel error_ops contain DROP"}
    s2 = np.array([(B.get(U[kP[i]]["item_id"]) or {}).get("b2_score") for i in drop + cor], dtype=float)
    rep["b2_score_DROP_vs_CORRECT_auroc"] = round(float(auc_w(yy, s2)), 4) if len(drop) and len(cor) else None
    # batching check
    UB = read_jsonl(SCORES / "b2_unbatched.jsonl") if (SCORES / "b2_unbatched.jsonl").exists() else []
    S = load_scores("b2_screen")
    if UB:
        agree = n = 0
        for r in UB:
            b = S.get(r["key"])
            if b and b.get("verdicts") and r.get("verdict") and r["world"] < len(b["verdicts"]):
                n += 1
                agree += b["verdicts"][r["world"]] == r["verdict"]
        rep["batching_check"] = {"n_worlds": n, "agreement": round(agree / n, 4) if n else None}
    rep["covered_subset"] = {"n_E_rows_scored": sum(1 for r in B.values()), "reader_backend": "local Qwen3-8B (F-KEY)"}
    if (RES / "b2_think_diagnostic.json").exists():
        rep["post_hoc_thinking_reader_diagnostic"] = jload(RES / "b2_think_diagnostic.json")
    rep["rewrite_invariance"] = "see analysis_E.json invariance.b2_score"
    return rep


# =====================================================================================================================
def write_tables(A):
    """CSV versions of the main tables (results/tables/)."""
    import csv
    TAB = RES / "tables"
    TAB.mkdir(exist_ok=True)
    for name, b in A["sets"].items():
        if "metrics" not in b:
            continue
        fn = TAB / f"set_{name.replace('|', '__')}.csv"
        with fn.open("w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["metric", "n_applicable", "n_pos", "n_neg", "prevalence", "auroc", "ci_lo", "ci_hi", "auprc", "tie_rate",
                        "threshold", "precision", "recall", "fa", "coverage", "delta_vs_bar", "delta_ci_lo", "delta_ci_hi", "delong_p", "testable"])
            dl = b.get("paired_vs_bar", {}).get("deltas", {})
            for m, r in sorted(b["metrics"].items(), key=lambda kv: -(kv[1].get("auroc") or 0)):
                if r.get("auroc") is None:
                    continue
                d = dl.get(m, {})
                c = r.get("auroc_ci") or [None, None]
                dc = d.get("ci") or [None, None]
                w.writerow([m, r.get("n_applicable"), r.get("n_pos"), r.get("n_neg"), r.get("prevalence"), r.get("auroc"), c[0], c[1],
                            r.get("auprc"), r.get("tie_rate"), r.get("threshold"), r.get("precision"), r.get("recall"), r.get("fa"),
                            r.get("coverage"), d.get("delta"), dc[0], dc[1], d.get("delong_p"), b.get("testable")])
    with (TAB / "coverage.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["metric", "n_rows", "usable_share", "status"])
        for m, r in A["coverage"].items():
            w.writerow([m, r["n_rows"], r["usable_share"], json.dumps(r["status"])])
    with (TAB / "system_level.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["metric", "tau_b_13", "ci_lo", "ci_hi", "tau_b_11fam", "ci11_lo", "ci11_hi"])
        for m, r in A["system_level"].items():
            if isinstance(r, dict) and "tau_b_13" in r:
                w.writerow([m, r["tau_b_13"], *r["ci"], r["tau_b_11fam"], *r["ci_11fam"]])
    with (TAB / "complexity_words.csv").open("w", newline="") as f:
        w = csv.writer(f)
        cells = A["complexity"]["words"]
        ms = sorted({m for c in cells.values() for m in c if m not in ("n_pos", "n_neg", "descriptive_only")})
        w.writerow(["bin", "n_pos", "n_neg", "descriptive_only"] + ms)
        for b_, c in cells.items():
            w.writerow([b_, c["n_pos"], c["n_neg"], c["descriptive_only"]] + [c.get(m) for m in ms])
    with (TAB / "recall_by_type_FA0.10.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["metric", "type", "n", "recall", "ci_lo", "ci_hi"])
        for m, r in A["recall_by_type"].items():
            for ty, x in r["FA=0.1"]["per_type"].items():
                w.writerow([m, ty, x["n"], x["recall"], *(x["ci"] or [None, None])])


def write_method_out(T, s4cols, regimes, full):
    """exp_gen_sol_out: E_heldout (all 8,507 rows) + screen_B2 (screen items with B2 scores)."""
    fr_by = {r["row_key"]: r for r in full}
    U = units()
    metric_cols = [m for m in T if not m.startswith("_")]
    ex = []
    for u in U:
        r = fr_by[u["row_key"]]
        e = {"input": json.dumps({"text": u["text"], "candidate_fol": u["candidate_fol"], "system": u["system"],
                                  "prompt_variant": u["prompt_variant"]}, ensure_ascii=False),
             "output": r["metadata_final_label"]}
        for m in metric_cols:
            v = T[m].get(u["row_key"])
            e[f"predict_{m}"] = "NA" if v in (None, "NA") else ("FAIL" if v == "FAIL" else f"{v:.6f}")
        e.update({"metadata_item_id": u["item_id"], "metadata_row_key": u["row_key"], "metadata_sentence_id": u["sentence_id"],
                  "metadata_fold_E": u["fold_E"], "metadata_pool": u["pool"], "metadata_sysvar": u["sysvar"], "metadata_parse_ok": u["parse_ok"],
                  "metadata_label_tier": r["metadata_label_tier"], "metadata_strata": u["strata"],
                  "metadata_in_R_AB": u["row_key"] in regimes["R_AB"], "metadata_in_R_A": u["row_key"] in regimes["R_A"],
                  "metadata_disg_source": u.get("disg_source")})
        ex.append(e)
    A_ = {r["item_id"]: r for r in jload(DATA / "expA_screen_items.json")}
    S = load_scores("b2_screen")
    ex2 = []
    for k, r in S.items():
        a = A_.get(k)
        if not a:
            continue
        ex2.append({"input": json.dumps({"text": a["text"], "candidate_fol": a["candidate_fol"], "system": a["system"]}, ensure_ascii=False),
                    "output": a["label"],
                    "predict_b2_score": "NA" if r.get("b2_score") is None else f"{r['b2_score']:.6f}",
                    "predict_b2_mismatch_det": "NA" if r.get("b2_mismatch_det") is None else f"{r['b2_mismatch_det']:.6f}",
                    "predict_b2_undet_share": "NA" if r.get("b2_undet_share") is None else f"{r['b2_undet_share']:.6f}",
                    "metadata_item_id": k, "metadata_track": a["track"], "metadata_status": r.get("status"),
                    "metadata_n_worlds": r.get("n_worlds"), "metadata_verdicts": r.get("verdicts"), "metadata_phi_truth": r.get("phi_truth"),
                    "metadata_ops": r.get("ops")})
    out = {"metadata": {"method_name": "All baselines re-run on held-out dataset E (+ B2 world_probe)",
                        "description": "Oriented scores (higher = more likely unfaithful) for every baseline on dataset E; output = the "
                                       "dataset-E final label; see results/analysis_E.json and README.md",
                        "prereg_sha256": PREREG_SHA.read_text().split()[0]},
           "datasets": [{"dataset": "E_heldout", "examples": ex}] + ([{"dataset": "screen_B2", "examples": ex2}] if ex2 else [])}
    jdump(out, ROOT / "method_out.json", indent=None)
    logger.info(f"method_out.json: E rows {len(ex)}, screen_B2 rows {len(ex2)}")


# =====================================================================================================================
def stage_t2_repro():
    """T2 (screen, labels allowed): the local Qwen3-8B judge with exp D's prereg_local prompt on 150 exp D track-L items,
    orig + disg, compared with exp D's cached judge_local_qwen8b scores (different GPU/batching -> Spearman, exact-match)."""
    import numpy as np
    from scipy.stats import spearmanr
    from src.common import disable_triton_overrides
    from src.local_llm import LocalLM
    disable_triton_overrides()
    pl = _prereg_local()
    items = [r for r in jload(DATA / "expD_screen_items.json") if r["track"] == "L" and r["label"] in ("CORRECT", "ERROR")]
    items = sorted(items, key=lambda r: sha1(r["item_id"] + "t2"))[:150]
    old = {r["key"]: r for r in read_jsonl(EXPD / "results" / "scores" / "judge_local_qwen8b.jsonl")}
    dmap = jload(EXPD / "data" / "disguise_map.json")
    su = []
    for r in items:
        su.append((f"{r['item_id']}|orig", r["text"], r["candidate_fol"]))
        d = dmap[r["item_id"]]
        su.append((f"{r['item_id']}|disg", d["text_d"], d["fol_d"]))
    lm = LocalLM(LOCAL_Q8)
    outs = _local_json_judge(lm, su, pl["prompts"]["rubric"], pl["prompts"]["user_json"], "t2_repro")
    lm.unload()
    a, b = [], []
    for (k, _, _), o in zip(su, outs):
        if o.get("p") is not None and old.get(k, {}).get("p") is not None:
            a.append(o["p"])
            b.append(old[k]["p"])
    a, b = np.array(a), np.array(b)
    rep = {"n": len(a), "spearman": float(spearmanr(a, b).statistic) if len(a) > 2 else None, "exact_match": float(np.mean(a == b)),
           "mean_abs_diff": float(np.mean(np.abs(a - b))), "note": "exp D ran on an RTX 4000 Ada with batch 16; here RTX 4090 batch 32-64"}
    jdump(rep, RES / "t2_repro_local_judge.json")
    logger.info(f"T2 repro: {rep}")


# =====================================================================================================================
def write_summary(A):
    """results/summary.md: plain-language tables from analysis_E.json."""
    L = ["# Baselines on held-out dataset E: summary", ""]
    L += [f"- Bar: `{A['bar']}` ({A['bar_note']})", f"- Missing components: {', '.join(A['missing_components']) or 'none'}",
          f"- API spend: ${A['api_spend_total_usd']}", f"- R_AB label vector sha1 {A['label_vectors']['R_AB']['sha1']} "
          f"(matches prereg: {A['label_vectors_match_prereg']})", ""]

    def fmt(r):
        c = r.get("auroc_ci") or [None, None]
        return f"{r['auroc']:.3f} [{c[0]:.3f}, {c[1]:.3f}]" if r.get("auroc") is not None and c[0] is not None else str(r.get("auroc"))
    for set_name in ("R_AB|pooled", "R_A|pooled_L20_EXC_CTRL", "COVERAGE|pooled", "R_AB|long_L25_L20_EXC"):
        b = A["sets"].get(set_name, {})
        if "metrics" not in b:
            continue
        L += [f"## {set_name}: n={b['n']} ({b['n_pos']} ERROR / {b['n_neg']} CORRECT, {b['n_sentences']} sentences)", "",
              "| metric | AUROC [95% CI] | Δ vs bar [95% CI] | DeLong p | AUPRC | tie rate | prec / rec / FA at frozen thr |", "|---|---|---|---|---|---|---|"]
        dl = b.get("paired_vs_bar", {}).get("deltas", {})
        for m, r in sorted(b["metrics"].items(), key=lambda kv: -(kv[1].get("auroc") or 0)):
            if r.get("auroc") is None or m.endswith("_flag"):
                continue
            d = dl.get(m, {})
            dc = d.get("ci") or [None, None]
            ds = f"{d['delta']:+.3f} [{dc[0]:+.3f}, {dc[1]:+.3f}]" if d.get("delta") is not None and dc[0] is not None else ""

            def f3(x):
                return "-" if x is None else f"{x:.3f}"
            dp = d.get("delong_p")
            dp = "" if dp is None else ("<1e-6" if dp == 0 else f"{dp:.2g}")
            L.append(f"| {m} | {fmt(r)} | {ds} | {dp} | {f3(r.get('auprc'))} | {f3(r.get('tie_rate'))} | "
                     f"{f3(r.get('precision'))} / {f3(r.get('recall'))} / {f3(r.get('fa'))} |")
        L.append("")
    L += ["## Per stratum (R_AB, AUROC)", "", "| metric | " + " | ".join(AE_STRATA) + " |", "|---|" + "---|" * len(AE_STRATA)]
    ms = [m for m, r in A["sets"]["R_AB|pooled"]["metrics"].items() if r.get("auroc") is not None and not m.endswith("_flag")]
    for m in sorted(ms, key=lambda m: -(A["sets"]["R_AB|pooled"]["metrics"][m]["auroc"])):
        L.append(f"| {m} | " + " | ".join(str(A['sets'].get(f'R_AB|{st}', {}).get('metrics', {}).get(m, {}).get('auroc')) for st in AE_STRATA) + " |")
    L.append("")
    L += ["## Frame (284 rows): larger vs cheap judge", "", "```", json.dumps(A["frontier_frame"].get("contrasts"), indent=1), "```", ""]
    L += ["## Contamination (DiD = Δdisg(GOLDSYS) − Δdisg(E_POOL))", ""]
    for k, v in A["contamination"].items():
        if isinstance(v, dict) and "DiD" in v:
            L.append(f"- {k}: E_POOL Δ={v['E_POOL']['delta_disg']} GOLDSYS Δ={v['GOLDSYS']['delta_disg']} DiD={v['DiD']['point']} "
                     f"CI {v['DiD']['ci']} MDE {v['DiD']['MDE_2.8SE']}; probe {v.get('gold_recognition_probe', {}).get('DiD')}")
    L += ["", "## B2 world_probe", "", "```", json.dumps({k: A["b2"].get(k) for k in ("status_counts_E", "undet_share_DROP_vs_CORRECT",
                                                                                       "b2_score_DROP_vs_CORRECT_auroc", "batching_check")}, indent=1),
          json.dumps((A["b2"].get("gate") or {}).get("primary_gate_trackH_corrected"), indent=1), "```", ""]
    L += ["## Complexity (GEE slope of judge-correctness per SD of words / n_conditions)", ""]
    for m, r in A["complexity_gee"].items():
        L.append(f"- {m}: words {r.get('words')} ; n_conditions {r.get('n_conditions')}")
    L += ["", "## System level (Kendall τ-b, 13 system×variant rows; descriptive)", ""]
    for m, r in A["system_level"].items():
        if isinstance(r, dict) and "tau_b_13" in r:
            L.append(f"- {m}: τ={r['tau_b_13']} {r['ci']} ; 11-family τ={r['tau_b_11fam']} {r['ci_11fam']}")
    (RES / "summary.md").write_text("\n".join(L) + "\n")


AE_STRATA = ["L25", "L20", "EXC", "CTRL"]


# =====================================================================================================================
def stage_b2_think(limit=None, which=("gate", "screen")):
    """POST-HOC DIAGNOSTIC (not pre-registered; screen data only): the same worlds and frozen reader prompt, read by
    Qwen3-8B WITH thinking enabled (greedy, <= 2048 new tokens), to separate reader capacity from world construction after
    the pre-registered non-thinking local reader failed the gate. Nothing on dataset E depends on it."""
    import numpy as np
    from src.analysis import auc_w
    from src.b2_world_probe import parse_answers, reader_prompt, score
    from src.common import disable_triton_overrides
    from src.local_llm import LocalLM
    disable_triton_overrides()
    var = jload(ROOT / "prereg_b2.json")["chosen_variant"]
    sets = b2_sets()
    dev = b2_dev_keys()
    lm = LocalLM(LOCAL_Q8)
    lm.is_qwen3 = False  # render() then leaves Qwen3's default (thinking ON) chat template
    rep = {}
    for w in which:
        name = {"gate": "href", "screen": "screen"}[w]
        U = [u for u in _b2_units(name, sets) if u["build"] and u["build"]["status"] == "ok" and not (w == "gate" and u["key"] in dev)]
        if w == "screen":  # time cap: 300 sha1-ordered track-L CORRECT/ERROR items (thinking decoding ~5 s/item at batch 12 on the RTX 4090)
            A0 = {r["item_id"]: r for r in jload(DATA / "expA_screen_items.json")}
            U = sorted([u for u in U if A0.get(u["key"], {}).get("track") == "L" and A0[u["key"]]["label"] in ("CORRECT", "ERROR")],
                       key=lambda u: sha1(u["key"] + "b2think"))[:300]
        if limit:
            U = U[:limit]
        uq = {}
        for u in U:
            uq.setdefault(sha1(u["text"] + "||" + u["fol"]), (u["text"], u["build"]["worlds"]))
        keys = list(uq)
        t0 = time.time()
        gen = lm.generate([[{"role": "user", "content": reader_prompt(uq[k][0], uq[k][1], var)}] for k in keys], 2048, tag=f"b2_think_{w}", bs=48)
        res = {}
        for k, g in zip(keys, gen):
            txt = g["text"].split("</think>")[-1]
            res[k] = (parse_answers(txt, len(uq[k][1])), g["seconds"])
        rows = []
        for u in U:
            v, secs = res[sha1(u["text"] + "||" + u["fol"])]
            rows.append({"key": u["key"], "status": "ok" if v else "reader_fail", **score(u["build"]["worlds"], v), "verdicts": v,
                         "phi_truth": [x["phi_truth"] for x in u["build"]["worlds"]], "seconds": secs})
        (SCORES / f"b2_think_{w}.jsonl").write_text("")
        append_jsonl(SCORES / f"b2_think_{w}.jsonl", rows)
        logger.info(f"B2-think {w}: {len(rows)} rows in {time.time()-t0:.0f}s; reader_fail {sum(r['status'] != 'ok' for r in rows)}")
        if w == "gate":
            tp = tn = nt = nf = 0
            for r in rows:
                if r["status"] != "ok":
                    continue
                for v, t in zip(r["verdicts"], r["phi_truth"]):
                    nt += t
                    nf += not t
                    tp += t and v == "TRUE"
                    tn += (not t) and v == "FALSE"
            rep["gate"] = {"n_items": len(rows), "n_ok": sum(r["status"] == "ok" for r in rows), "acc_true": tp / max(1, nt),
                           "acc_false": tn / max(1, nf), "bal_acc": (tp / max(1, nt) + tn / max(1, nf)) / 2}
        else:
            A_ = {r["item_id"]: r for r in jload(DATA / "expA_screen_items.json")}
            for tr in ("L", "H"):
                ks = [r for r in rows if A_.get(r["key"], {}).get("track") == tr and A_[r["key"]]["label"] in ("CORRECT", "ERROR")]
                y = np.array([1 if A_[r["key"]]["label"] == "ERROR" else 0 for r in ks])
                sc = np.array([r["b2_score"] if r["status"] == "ok" else 0.5 for r in ks], dtype=float)
                rep[f"screen_{tr}_auroc"] = {"auroc": auc_w(y, sc) if len(set(y)) == 2 else None, "n_pos": int(y.sum()), "n_neg": int(len(y) - y.sum())}
    lm.unload()
    rep["note"] = "POST-HOC diagnostic, not pre-registered; screen data only (the dev slice is excluded from the gate numbers)"
    jdump(rep, RES / "b2_think_diagnostic.json")
    logger.info(f"B2-think diagnostic: {rep}")


# =====================================================================================================================
def stage_retest_sibling():
    """Test-retest of the local Qwen3-8B judge across two INDEPENDENT runs (this artifact vs the sibling PEER+TEXT
    experiment, separate caches/processes/batches), standing in for the API test-retest (4f) that F-KEY made impossible."""
    import numpy as np
    from scipy.stats import spearmanr
    sib_p = ROOT.parent / "gen_art_experiment_5" / "results" / "E_judge_local.jsonl"
    if not sib_p.exists():
        logger.warning("sibling local judge file not found")
        return
    sib = {}
    for r in read_jsonl(sib_p):
        sib[(r["row_key"].split("|")[0], r["cond"])] = r.get("p")
    mine = load_scores("judge_local_qwen8b")
    rep = {"sibling_file": str(sib_p)}
    for cond in ("disg", "orig"):
        a, b = [], []
        for (iid, c), p_ in sib.items():
            if c != cond or p_ is None:
                continue
            m = mine.get(f"{iid}|{cond}")
            if m and m.get("p") is not None:
                a.append(m["p"])
                b.append(p_)
        a, b = np.array(a), np.array(b)
        rep[cond] = {"n": int(len(a)), "spearman": float(spearmanr(a, b).statistic) if len(a) > 2 else None,
                     "exact_match": float(np.mean(a == b)) if len(a) else None, "mean_abs_diff": float(np.mean(np.abs(a - b))) if len(a) else None}
    rep["note"] = ("same model/prompt (exp D prereg_local rubric B), greedy; differences come from batch composition/padding and, "
                   "for disg, from the sibling's disguise call")
    jdump(rep, RES / "retest_vs_sibling.json")
    logger.info(f"retest vs sibling: {rep}")


# =====================================================================================================================
def stage_b2_read_api(limit=None, which=("dev", "gate", "screen", "rewrites", "Eref", "E")):
    """B2 with the PLANNED API reader (gemini-2.5-flash-lite, T=0; plan stage 7), run when the key recovered. Own prompt
    dev (v1 vs v2 on the same 40-item dev slice) frozen in prereg_b2_api.json before the gate; scores -> b2api_*.jsonl."""
    from src import judges as J
    from src.b2_world_probe import parse_answers, reader_prompt, score
    from src.budget import Budget
    require_frozen()
    sets = b2_sets()
    pp = ROOT / "prereg_b2_api.json"

    async def read(jobs, var):
        async with Budget(concurrency=32) as b:
            outs = await J.gather_limited([J.simple_text(b, component="b2_reader", model=B2_READER, item_id=sha1(t)[:12],
                                                         prompt=reader_prompt(t, ws, var), max_tokens=400) for t, ws in jobs], "b2api")
            logger.info(f"b2 api spent ${b.spent:.4f} {b.by_comp}; dead={b.dead}")
        return [(parse_answers(o.get("text"), len(ws)), (o.get("text") or "")[:300], o.get("seconds")) for o, (t, ws) in zip(outs, jobs)]
    for w in which:
        t0 = time.time()
        if w == "dev":
            dev = b2_dev_keys()
            U = [u for u in _b2_units("href", sets) if u["key"] in dev and u["build"] and u["build"]["status"] == "ok"]
            res = {v: _gate_metrics(U, asyncio.run(read([(u["text"], u["build"]["worlds"]) for u in U], v))) for v in ("v1", "v2")}
            chosen = max(("v1", "v2"), key=lambda v: (res[v]["bal_acc"] or 0, v == "v1"))
            jdump({"created_iso": time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime()), "backend": f"API {B2_READER} T=0",
                   "dev_slice": sorted(dev), "dev_results": res, "chosen_variant": chosen,
                   "rule": "higher balanced accuracy on the 40-item track-H dev slice (tie -> v1); dev items excluded from the gate"}, pp)
            (ROOT / "prereg_b2_api.sha256").write_text(hashlib.sha256(pp.read_bytes()).hexdigest() + "  prereg_b2_api.json\n")
            logger.info(f"B2-API prompt dev {res} -> {chosen}")
            continue
        var = jload(pp)["chosen_variant"]
        name = {"gate": "href", "screen": "screen", "rewrites": "rewrites", "Eref": "Eref", "E": "E"}[w]
        U = _b2_units(name, sets, limit)
        uq = {}
        for u in U:
            if u["build"] and u["build"]["status"] == "ok":
                uq.setdefault(sha1(u["text"] + "||" + u["fol"]), (u["text"], u["build"]["worlds"]))
        keys = list(uq)
        outs = dict(zip(keys, asyncio.run(read([uq[k] for k in keys], var))))
        rows = []
        for u in U:
            b = u["build"]
            if not b or b["status"] != "ok":
                rows.append({"key": u["key"], "status": (b or {}).get("status", "parse_fail"), "b2_score": None, "n_worlds": 0})
                continue
            v, raw, secs = outs[sha1(u["text"] + "||" + u["fol"])]
            rows.append({"key": u["key"], "status": "ok" if v else "reader_fail", **score(b["worlds"], v), "n_worlds": len(b["worlds"]),
                         "verdicts": v, "phi_truth": [x["phi_truth"] for x in b["worlds"]], "ops": [x["mutant_op"] for x in b["worlds"]],
                         "seconds": secs, "raw": None if v else raw, "variant": var})
        (SCORES / f"b2api_{w}.jsonl").write_text("")
        append_jsonl(SCORES / f"b2api_{w}.jsonl", rows)
        logger.info(f"B2-API {w}: {len(rows)} rows ({len(keys)} calls) in {time.time()-t0:.0f}s; {Counter(r['status'] for r in rows)}")


# =====================================================================================================================

# =====================================================================================================================
# T1 (iteration 3): head-on API bar. Stages t1_prep (gates, priority, VEX), t1_pilot (label-blind), t1_freeze,
# t1_join, t1_analysis (src/analyse_T1.py). See README.md.
PREREG_T1 = ROOT / "prereg_T1.json"
PREREG_T1_SHA = ROOT / "prereg_T1.sha256"
EXP5_DIR = Path("../../../round-2/experiment-5/src")
EXPC_CONS = EXPC / "src" / "consensus.py"


def _t0_unit_tests() -> dict:
    """T0: no API, no labels."""
    import numpy as np
    from sklearn.metrics import roc_auc_score
    from src import api_bar as AB
    from src import budget as BG
    from src import judges as J
    from src.vocab_exact import norm
    out = {}
    hits = []
    for f in list((ROOT / "src").rglob("*.py")) + list(ROOT.glob("*.sh")):
        if "openrouter" + ".ai" in f.read_text(errors="ignore"):
            hits.append(str(f.relative_to(ROOT)))
    out["no_hardcoded_openrouter_host"] = {"pass": not hits, "hits": hits}
    out["budget_url_from_env"] = {"pass": BG.URL.startswith(os.environ["OPENROUTER_BASE_URL"].rstrip("/")), "url_host_is_env": True}
    exp = {"RUBRIC_A": "06686913c59b6d9a7daeb5748cb9f53ed2b2e812", "USER_JSON_A": "5b3ccfb9d82edbbfb5bd1bb7a4e574da62be38b4",
           "USER_YESNO": "b36e93cb44615e19dcb36e85ad8664dcb2acb458", "VERBALISE": "584f33d03322a050f7cc516c5b22ca05d581e91b"}
    out["prompt_sha1"] = {"pass": all(J.PROMPT_SHA[k] == v for k, v in exp.items()), "got": {k: J.PROMPT_SHA[k] for k in exp}}
    sc_sha = sha1(json.dumps(FEWSHOT, sort_keys=True, ensure_ascii=False))
    out["sc_fewshot_sha1"] = {"value": sc_sha, "prereg_baselines": jload(PREREG)["prompts"].get("sc5_prompt_sha1")}
    # exp C consensus components vs consensus_min
    try:
        import ast
        def fn_src(path, names):
            tree = ast.parse(Path(path).read_text())
            return {n.name: ast.unparse(n) for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names}
        a = fn_src(EXPC_CONS, ("components", "entropy"))
        b = fn_src(ROOT / "src" / "consensus_min.py", ("components", "entropy"))
        out["expC_vs_consensus_min"] = {"pass": a == b and len(a) == 2, "identical_functions": sorted(k for k in a if a.get(k) == b.get(k))}
    except (OSError, SyntaxError) as e:
        out["expC_vs_consensus_min"] = {"pass": None, "error": str(e)[:100]}
    t = {"IsTallPerson": "tall person", "has_children": "child", "Likes": "like", "isRed": "red", "Person": "person"}
    got = {k: norm(k) for k in t}
    out["vex_norm"] = {"pass": got == t, "got": got}
    y = np.array([1, 1, 0, 0, 1, 0, 1, 0])
    sc = np.array([.9, .4, .3, .5, .7, .7, .2, .1])
    h = np.array(["a"] * 4 + ["b"] * 4)
    ha = AB.auroc(y[:4], sc[:4]); hb = AB.auroc(y[4:], sc[4:])
    manual = (ha * 2 * 2 + hb * 2 * 2) / 8
    out["strat_auroc_toy"] = {"pass": abs(AB.strat_auroc(y, sc, h) - manual) < 1e-12 and
                              abs(AB.strat_auroc(y, sc, np.array(["a"] * 8)) - roc_auc_score(y, sc)) < 1e-12}
    cb = AB.ClusterBoot([str(i // 2) for i in range(8)], b=200)
    pb = AB.paired_boot(y, sc, sc, cb)
    out["paired_boot_identical"] = {"pass": pb["delta"] == 0 and pb["ci"] == [0.0, 0.0]}
    out["tie_rate_toy"] = {"pass": abs(AB.tie_rate(np.array([1, 0]), np.array([.5, .5])) - 1.0) < 1e-12}
    # a dry-run Budget refuses a call above a component cap (no network: the refusal happens before any request)
    async def dry():
        async with BG.Budget(concurrency=1) as b:
            b.by_comp["retest"] = BG.CAPS["retest"]
            try:
                await b.call(component="retest", model="google/gemini-2.5-flash-lite",
                             messages=[{"role": "user", "content": "x" * 400}], max_tokens=10)
                return False
            except BG.BudgetExceeded:
                return True
    out["budget_refuses_over_cap"] = {"pass": asyncio.run(dry())}
    out["caps_from_prereg_T1"] = {"caps": BG.CAPS, "cap_total": BG.CAP_TOTAL, "prereg_T1_exists": PREREG_T1.exists()}
    return out


def stage_t1_prep():
    """Step 1 (reproduction gates, key map, label hashes, E_judge reuse check) + R_AB-first priority + VEX declaration.
    Reads labels (membership / reproduction of iteration-2 numbers only); no new score exists yet."""
    import numpy as np
    from src import api_bar as AB
    from src.e_pool import label_vector_sha1, load_E, regime_labels
    from src.join_T1 import base_rows
    from src.s4 import fit_s4_oof
    pre = require_frozen()
    full = load_E(blind=False)
    rows, info = base_rows(full)
    G = {"key_map": info}
    # ---- 1.2 label hashes
    fr_by = {r["row_key"]: r for r in full}
    lv = {}
    for reg in ("R_AB", "R_A"):
        v = regime_labels(full, reg)
        ks = sorted(v)
        lv[reg] = {"n": len(v), "sha1": label_vector_sha1([fr_by[k]["metadata_item_id"] for k in ks], ["ERROR" if v[k] else "CORRECT" for k in ks]),
                   "sha1_rowkey": label_vector_sha1(ks, ["ERROR" if v[k] else "CORRECT" for k in ks])}
        for h in ("sha1", "sha1_rowkey"):
            if lv[reg][h] != pre["label_vectors"][reg][h]:
                jdump({"label_vectors": lv, "STOP": f"{reg} {h} mismatch"}, RES / "repro_gates.json")
                raise SystemExit(f"HARD STOP: label hash mismatch {reg} {h}")
    G["label_vectors"] = {"got": lv, "prereg": {k: pre["label_vectors"][k] for k in ("R_AB", "R_A")}, "match": True}
    rab = regime_labels(full, "R_AB")
    ra = regime_labels(full, "R_A")
    by6 = {x["exp6_row_key"]: x for x in rows}
    P = [x for x in rows if x["pool"] == "E_POOL" and x["parse_ok"] and x["exp6_row_key"] in rab]
    y = np.array([rab[x["exp6_row_key"]] for x in P])
    hh = np.array([x["source_stratum"] for x in P])
    G["population"] = {"n": len(P), "n_error": int(y.sum()), "n_correct": int(len(y) - y.sum()),
                       "n_sentences": len({x["sentence_id"] for x in P}), "target": [2686, 1822, 864, 292]}
    # ---- 1.3 (a) S4_local OOF 0.748
    table = [json.loads(l) for l in (DATA / "exp6_E_baseline_features.jsonl").read_text().splitlines() if l.strip()]
    s4c = jload(DATA / "exp6_results" / "s4_coefs.json")
    fm = jload(DATA / "exp6_results" / "feature_meta.json")
    train_pool = [r for r in table if r["pool"] == "E_POOL"]
    lab = {k: v for k, v in rab.items() if by6[k]["pool"] == "E_POOL"}
    folds = {r["row_key"]: r["metadata_fold_E"] for r in table}
    oof, _ = fit_s4_oof(train_pool, lab, folds, s4c["S4_local_oof_RAB"]["features"], C=1.0, fail_fill=fm["fail_fill"])
    s4 = np.array([oof[x["exp6_row_key"]] for x in P])
    G["a_S4_local_oof"] = {"got": AB.auroc(y, s4), "target": 0.748}
    # ---- (b) pooled, (c) stratified
    tg_pool = {"p_peer_text": 0.790, "c_score_align": 0.782, "nf_c_score": 0.743, "judge_local_qwen8b_disg": 0.711}
    tg_str = {"p_peer_text": 0.753, "c_score_align": 0.741, "judge_local_qwen8b_disg": 0.677}
    G["b_pooled"], G["c_stratified"] = {}, {}
    for m, t in tg_pool.items():
        s = np.array([x[m] for x in P], float)
        G["b_pooled"][m] = {"got": AB.auroc(y, s), "target": t}
    for m, t in tg_str.items():
        s = np.array([x[m] for x in P], float)
        G["c_stratified"][m] = {"got": AB.strat_auroc(y, s, hh), "target": t}
    G["c_stratified"]["S4_local_oof"] = {"got": AB.strat_auroc(y, s4, hh), "target": None}
    rng = np.random.default_rng(0)
    pl, gl = [], []
    idx = {h: np.where(hh == h)[0] for h in np.unique(hh)}
    ca = np.array([x["c_score_align"] for x in P], float)
    for _ in range(200):
        yy = y.copy()
        for ix in idx.values():
            yy[ix] = rng.permutation(yy[ix])
        pl.append(AB.auroc(yy, ca))
        gl.append(AB.auroc(rng.permutation(y), ca))
    G["c_placebo_within_stratum_c_score_align"] = {"got": float(np.mean(pl)), "target": 0.592}
    G["placebo_global_shuffle_c_score_align"] = {"got": float(np.mean(gl)), "target": 0.50}
    # orientation: every predict column higher = unfaithful (AUROC > .5)
    G["orientation_ok"] = all(v["got"] > 0.5 for v in G["b_pooled"].values()) and G["a_S4_local_oof"]["got"] > 0.5
    # reviewer audit
    rev = list(Path("/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2").rglob("pt_vs_s4.py"))
    G["d_reviewer_script"] = {"found": [str(r) for r in rev]}
    if rev:
        G["d_reviewer_script"]["target"] = "+0.042 [0.014, 0.070]"
    ptd = AB.paired_boot(y, np.array([x["p_peer_text"] for x in P], float), s4, AB.ClusterBoot([x["sentence_id"] for x in P], b=2000))
    G["d_PT_minus_S4_local"] = {"got": ptd["delta"], "ci": ptd["ci"], "target": 0.042}
    fails = []
    for sec in ("b_pooled", "c_stratified"):
        for m, v in G[sec].items():
            if v["target"] is not None and abs(v["got"] - v["target"]) > 0.0015:
                fails.append(f"{sec}:{m} {v['got']:.4f} vs {v['target']}")
    if abs(G["a_S4_local_oof"]["got"] - 0.748) > 0.0015:
        fails.append(f"S4_local {G['a_S4_local_oof']['got']:.4f}")
    G["gate_fails"] = fails
    G["gates_pass"] = not fails and G["population"]["n"] == 2686
    # ---- 1.4 E_judge.jsonl reuse check (exp 5 disguise = seed_text=norm(text); exp 6 = default seed)
    dm = {r["row_key"]: r for r in read_jsonl(DATA / "exp5" / "E_disguise_map.jsonl")}
    ej = read_jsonl(DATA / "exp5" / "E_judge.jsonl")
    byc = {x["canonical_key"]: x for x in rows}
    same_all = sum(1 for k, x in byc.items() if x["parse_ok"] and dm.get(k, {}).get("text_d") == x["text_d"] and dm.get(k, {}).get("fol_d") == x["fol_d"])
    same_ej = [k["row_key"] for k in ej if dm.get(k["row_key"], {}).get("text_d") == byc[k["row_key"]]["text_d"]
               and dm.get(k["row_key"], {}).get("fol_d") == byc[k["row_key"]]["fol_d"]]
    G["e_judge_reuse"] = {"exp5_rows": len(ej), "identical_disguise_on_exp5_judge_rows": len(same_ej),
                          "identical_disguise_all_parseable": same_all, "n_parseable": sum(x["parse_ok"] for x in rows),
                          "decision": ("exp 5 disguised with seed_text=norm(text), exp 6 (this artifact) with the default seed; "
                                       "the disguised strings are nevertheless identical on all 20 billed exp-5 rows (and on "
                                       f"{same_all}/{sum(x['parse_ok'] for x in rows)} parseable rows overall). The 20 rows are "
                                       "NOT imported: they are rescored in the full sweep (< $0.002) and exp 5's values serve as "
                                       "the T2 API-determinism reference (fresh T=0 call vs exp 5's call)")}
    jdump({"rows": [dict(r, same_disguise=r["row_key"] in same_ej) for r in ej]}, RES / "pilot" / "exp5_judge_rows.json")
    # ---- 2.1 priority (membership only)
    prio = sorted({r["metadata_item_id"] for r in full if r["row_key"] in rab or
                   (r["metadata_label_tier"] == "A" and r["metadata_final_label"] in ("CORRECT", "ERROR"))})
    jdump({"rule": "item_ids in R_AB or tier-A decided (any pool); membership only", "n": len(prio), "priority_item_ids": prio},
          DATA / "t1_priority.json")
    # ---- VEX declaration (no scores joined)
    from src.vocab_exact import vex_rows
    labref_ok = ("PANEL_REPAIRED", "GOLD_PANEL_OK", "TRUSTED_AGREED")
    vin, ref_diff = [], 0
    for x in P:
        lr = x["labelling_ref_sentence"] if x["sentence_ref_status"] in labref_ok else None
        if lr is not None and lr != x["reference_fol"]:
            ref_diff += 1
        vin.append({"key": x["canonical_key"], "candidate_fol": x["candidate_fol"], "labelling_ref": lr or x["reference_fol"],
                    "label_tier": x["label_tier"], "auto_label": x["auto_label"], "final_label": x["final_label"],
                    "ref_status": x["sentence_ref_status"]})
    V = vex_rows(vin, n_jobs=max(1, NUM_CPUS - 1))
    jdump(V, DATA / "vex_rows.json")
    vdecl = {"definition": "src/vocab_exact.py docstring", "labelling_ref_differs_from_row_reference": ref_diff}
    yb = {x["canonical_key"]: rab[x["exp6_row_key"]] for x in P}
    strat_of = {x["canonical_key"]: x["source_stratum"] for x in P}
    sid_of = {x["canonical_key"]: x["sentence_id"] for x in P}
    ops_of = {x["canonical_key"]: (x["error_ops"] or x["repair_ops"] or []) for x in P}
    tier_of = {x["canonical_key"]: x["label_tier"] for x in P}
    for nm in ("include", "include_strict"):
        ks = [k for k, v in V.items() if v.get(nm)]
        ne = sum(yb[k] for k in ks)
        nc = len(ks) - ne
        se = len({sid_of[k] for k in ks if yb[k] == 1})
        sc_ = len({sid_of[k] for k in ks if yb[k] == 0})
        per = {}
        for h in AE_STRATA:
            kk = [k for k in ks if strat_of[k] == h]
            e_ = sum(yb[k] for k in kk)
            per[h] = {"n_error": e_, "n_correct": len(kk) - e_, "sent_err": len({sid_of[k] for k in kk if yb[k]}),
                      "sent_cor": len({sid_of[k] for k in kk if not yb[k]})}
            per[h]["testable"] = per[h]["n_error"] >= 50 and per[h]["n_correct"] >= 50 and per[h]["sent_err"] >= 25 and per[h]["sent_cor"] >= 25
        mix = Counter(o for k in ks if yb[k] for o in ops_of[k])
        mix_all = Counter(o for k in yb if yb[k] for o in ops_of[k])
        vdecl[nm] = {"n": len(ks), "n_error": ne, "n_correct": nc, "sent_err": se, "sent_cor": sc_,
                     "testable": ne >= 50 and nc >= 50 and se >= 25 and sc_ >= 25, "per_stratum": per,
                     "n_testable_strata": sum(v["testable"] for v in per.values()),
                     "tier_counts": dict(Counter(tier_of[k] for k in ks)),
                     "error_op_mix_vex": dict(mix.most_common()), "error_op_mix_all_RAB": dict(mix_all.most_common())}
    vdecl["exclusions"] = dict(Counter(v.get("include_why", v.get("vex_reason")) for v in V.values()))
    vdecl["vex_reasons"] = dict(Counter(v.get("vex_reason") for v in V.values()))
    jdump(vdecl, RES / "vex_declaration.json")
    G["vex"] = {k: vdecl[k]["n"] if isinstance(vdecl.get(k), dict) and "n" in vdecl[k] else vdecl.get(k) for k in ("include", "include_strict")}
    G["t0_unit_tests"] = _t0_unit_tests()
    jdump(G, RES / "repro_gates.json")
    logger.info(f"t1_prep: gates_pass={G['gates_pass']} fails={fails}; population {G['population']}; "
                f"VEX {vdecl['include']['n']} ({vdecl['include']['n_error']}/{vdecl['include']['n_correct']}) "
                f"testable={vdecl['include']['testable']}; T0 {[(k, v.get('pass')) for k, v in G['t0_unit_tests'].items() if 'pass' in v]}")



def _key_status() -> dict:
    import requests
    base = os.environ["OPENROUTER_BASE_URL"].rstrip("/")
    try:
        d = requests.get(base + "/key", headers={"Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}"}, timeout=30).json()["data"]
        return {"limit": d.get("limit"), "limit_remaining": d.get("limit_remaining"), "usage": d.get("usage"), "ts": time.time()}
    except Exception as e:  # noqa: BLE001
        return {"error": str(e)[:200], "ts": time.time()}


def stage_t1_pilot():
    """Step 0.4 key/model check + step 2.2 label-blind pilots (20 rows per cheap arm, 10 frame rows for the frontier,
    20 verbalisations, 4 SC sentences) into results/pilot/, + T2 determinism check on exp-5's 20 billed rows."""
    import subprocess
    import numpy as np
    from src import budget as BG
    PIL = RES / "pilot"
    PIL.mkdir(exist_ok=True)
    ks = _key_status()
    logger.info(f"key status: {ks}")
    prices = BG.load_prices(refresh=True)
    want = ["google/gemini-2.5-flash-lite", "openai/gpt-4.1-nano", "google/gemini-3.1-pro-preview"]
    mcheck = {m: (m in prices, prices.get(m, {}).get("in"), prices.get(m, {}).get("out"),
                  "logprobs" in prices.get(m, {}).get("params", []), "reasoning" in prices.get(m, {}).get("params", [])) for m in want}
    swaps = []
    if "google/gemini-3.1-pro-preview" not in prices:
        cands = sorted([m for m in prices if m.startswith("google/gemini-") and m.endswith("-pro") or m == "google/gemini-3.1-pro"])
        swaps.append({"from": "google/gemini-3.1-pro-preview", "to": cands[-1] if cands else None})
    jdump({"key": ks, "models": {m: dict(zip(("listed", "in", "out", "logprobs", "reasoning"), v)) for m, v in mcheck.items()},
           "swaps": swaps}, PIL / "key_model_check.json")
    if ks.get("limit_remaining") is not None and ks["limit_remaining"] < 5:
        logger.warning(f"limit_remaining {ks['limit_remaining']} < 5: F-KEY watch (caps still bound spend at 4.60)")
    env = dict(os.environ, T1_SCORES_DIR=str(PIL), PYTHONHASHSEED="0")
    py = str(ROOT / ".venv" / "bin" / "python")
    cmds = [["--stage", "judges", "--limit", "20", "--which", "cheap_disg,cheap_orig,cheap2_disg,cheap2_orig"],
            ["--stage", "strong", "--which", "pilot"],
            ["--stage", "verbalise", "--limit", "20"],
            ["--stage", "sc_gen", "--limit", "4"]]
    for c in cmds:
        t0 = time.time()
        r = subprocess.run([py, str(ROOT / "method.py")] + c, env=env, cwd=ROOT, capture_output=True, text=True, timeout=1800)
        logger.info(f"pilot {' '.join(c)} rc={r.returncode} {time.time()-t0:.0f}s")
        if r.returncode:
            logger.error(r.stderr[-2000:])
    # T2: API determinism on the exp-5 rows whose disguised strings are identical (fresh T=0 call, same prompt)
    from src import judges as J
    ej = jload(PIL / "exp5_judge_rows.json")["rows"]
    dm = {r["row_key"]: r for r in read_jsonl(DATA / "exp5" / "E_disguise_map.jsonl")}
    todo = [r for r in ej if r.get("p") is not None][:10]
    pre = require_frozen()

    async def t2():
        async with BG.Budget(concurrency=10) as b:
            return await J.gather_limited([J.judge_json(b, component="judge_cheap", model=pre["models"]["judge_cheap"], rubric=pre["prompts"]["rubric"],
                                                        text=dm[r["row_key"]]["text_d"], fol=dm[r["row_key"]]["fol_d"], item_id=r["row_key"],
                                                        user_tmpl=pre["prompts"]["user_json"]) for r in todo], "t2")
    outs = asyncio.run(t2())
    agree = [abs((o.get("p") if o.get("p") is not None else -9) - r["p"]) <= 0.05 for r, o in zip(todo, outs)]
    # pilot summary from costs.jsonl + pilot score files
    costs = read_jsonl(RES / "costs.jsonl") if (RES / "costs.jsonl").exists() else []
    summ = {"t2_determinism": {"n": len(todo), "agree_within_0.05": int(sum(agree)), "pass": sum(agree) >= 8,
                               "pairs": [(r["p"], o.get("p")) for r, o in zip(todo, outs)]}}
    for comp in ("judge_cheap", "judge_cheap2", "strong", "roundtrip", "sc5"):
        cc = [c["cost"] for c in costs if c["component"] == comp]
        ss = [c["seconds"] for c in costs if c["component"] == comp]
        summ[comp] = {"calls": len(cc), "usd": float(sum(cc)), "mean_usd_call": float(np.mean(cc)) if cc else None,
                      "p80_usd_call": float(np.percentile(cc, 80)) if cc else None, "mean_s_call": float(np.mean(ss)) if ss else None,
                      "mean_out_tok": float(np.mean([c["out_tok"] for c in costs if c["component"] == comp])) if cc else None}
    for f in ("judge_cheap", "judge_cheap2", "judge_strong"):
        R = read_jsonl(PIL / f"{f}.jsonl") if (PIL / f"{f}.jsonl").exists() else []
        summ[f + "_fail_rate"] = {"n": len(R), "fail": sum(r.get("p") is None for r in R),
                                  "fail_reasons": dict(Counter(str(r.get("fail"))[:40] for r in R if r.get("p") is None)),
                                  "src": dict(Counter(str(r.get("src")) for r in R)),
                                  "finish": dict(Counter(str(r.get("finish")) for r in R))}
    V = read_jsonl(PIL / "rt_verbal_api.jsonl") if (PIL / "rt_verbal_api.jsonl").exists() else []
    summ["verbalise"] = {"n": len(V), "fail": sum(not v.get("verbalisation") for v in V), "leak": sum(bool(v.get("leak")) for v in V)}
    S = read_jsonl(PIL / "sc5_samples.jsonl") if (PIL / "sc5_samples.jsonl").exists() else []
    from src.labeller.labeller import parse_ok
    summ["sc5"] = {"n_sentences": len(S), "sample_parse_rate": float(np.mean([bool(f and parse_ok(f)) for r in S for f in r["samples"]])) if S else None}
    summ["key_after"] = _key_status()
    jdump(summ, PIL / "pilot_summary.json")
    logger.info(f"pilot summary: {json.dumps({k: v for k, v in summ.items() if k in ('judge_cheap','judge_cheap2','strong','roundtrip','sc5')})[:1500]}")


def _unique_pairs(view: str) -> int:
    U = _judge_units(None)
    if view == "orig":
        return len({(u["text"], u["candidate_fol"]) for u in U})
    return len({(u["text_d"], u["fol_d"]) for u in U})


def stage_t1_freeze():
    """Step 3: write prereg_T1.json from the pilot numbers and freeze it (sha256 + frozen_iso). Refuses to overwrite."""
    import datetime
    if PREREG_T1_SHA.exists():
        raise RuntimeError("prereg_T1 already frozen")
    for p_ in (RES / "scores").glob("*.jsonl"):
        if p_.stat().st_size:
            raise RuntimeError(f"results/scores/{p_.name} already has rows: the freeze must precede every score")
    from src import judges as J
    PIL = RES / "pilot"
    ps = jload(PIL / "pilot_summary.json")
    import numpy as np
    cc = [c for c in read_jsonl(RES / "costs.jsonl") if c["component"] == "sc5"]
    ps["sc5_cost"] = {"calls": len(cc), "usd": float(sum(c["cost"] for c in cc)),
                      "mean_usd_call": float(np.mean([c["cost"] for c in cc])) if cc else None}
    km = jload(PIL / "key_model_check.json")
    s4c = jload(DATA / "exp6_results" / "s4_coefs.json")["S4_local_oof_RAB"]["features"]
    n_disg, n_orig = _unique_pairs("disg"), _unique_pairs("orig")
    n_formulas = len({u["candidate_fol"] for u in _judge_units(None)})
    n_sent = len({u["sentence_id"] for u in units()})
    c_strong = ps["strong"]["p80_usd_call"] or 0.012
    fr_fail = ps["judge_strong_fail_rate"]
    len_fail = sum(v for k, v in fr_fail.get("finish", {}).items() if k in ("length", "None")) + fr_fail.get("fail", 0)
    strong_max = 4000
    if len_fail > 2:
        strong_max = 8000
    cap_strong_calls = 2.40
    if 568 * c_strong <= cap_strong_calls:
        strong_rule = "BOTH views on all 284 frame rows"
    elif 284 * c_strong <= cap_strong_calls:
        strong_rule = "ORIGINAL on all 284, then DISGUISED round-robin over the 8 frame cells (frame sha1 order) until the cap"
    else:
        strong_rule = "ORIGINAL round-robin over cells until the cap; no disguised view; criterion (d) on the covered subset with IPW"
    est = {"judge_cheap": (ps["judge_cheap"]["mean_usd_call"] or 4e-5) * (n_disg + n_orig),
           "judge_cheap2": (ps["judge_cheap2"]["mean_usd_call"] or 2.5e-5) * (n_disg + n_orig),
           "strong": c_strong * 568, "roundtrip": (ps["roundtrip"]["mean_usd_call"] or 4e-5) * n_formulas,
           "sc5": (ps["sc5_cost"]["mean_usd_call"] or 1.2e-4) * 5 * n_sent, "retest": (ps["judge_cheap"]["mean_usd_call"] or 4e-5) * 200}
    swaps = km.get("swaps", [])
    strong_model = swaps[0]["to"] if swaps and swaps[0].get("to") else "google/gemini-3.1-pro-preview"
    vex = jload(RES / "vex_declaration.json")
    vex_sha = hashlib.sha256((RES / "vex_declaration.json").read_bytes()).hexdigest()
    vex_rows_sha = hashlib.sha256((DATA / "vex_rows.json").read_bytes()).hexdigest()
    exp5_pre = jload(DATA / "exp5" / "prereg.json")
    D = {
        "title": "T1 head-on API bar on held-out dataset E (iteration 3, experiment 1)",
        "created_iso": datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "hypothesis_T1": "the frozen consensus metric (c_score_align, exp 5) beats the pre-registered cheap API judge "
                         "(gemini-2.5-flash-lite rubric A, disguised) on held-out E and adds signal beyond a stack of every baseline",
        "models": {"judge_cheap": "google/gemini-2.5-flash-lite", "judge_cheap2": "openai/gpt-4.1-nano",
                   "judge_strong": strong_model, "roundtrip_llm": "google/gemini-2.5-flash-lite", "sc5": "openai/gpt-4.1-nano",
                   "nli": "MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli", "nli_alt": "cross-encoder/nli-deberta-v3-large",
                   "embed": "sentence-transformers/all-mpnet-base-v2"},
        "model_swaps": swaps,
        "live_prices": km["models"],
        "prompt_sha1": {k: J.PROMPT_SHA[k] for k in ("RUBRIC_A", "USER_JSON_A", "USER_YESNO", "VERBALISE")} |
                       {"SC_FEWSHOT": jload(PREREG)["prompts"]["sc5_prompt_sha1"]},
        "params": {"judge_cheap": {"T": 0, "max_tokens": 150, "response_format": "json_object"},
                   "judge_cheap2": {"T": 0, "max_tokens": 1, "logprobs": True, "top_logprobs": 5},
                   "verbalise": {"T": 0, "max_tokens": 120}, "sc5": {"T": 0.7, "max_tokens": 300, "k": 5}},
        "strong": {"model": strong_model, "max_tokens": strong_max, "extra": {"reasoning": {"effort": "low"}},
                   "pilot_p80_usd_call": c_strong, "pilot_length_or_fail": len_fail, "rule": strong_rule,
                   "shared_key_reserve_rule": "the run key is shared with sibling artifacts (limit_remaining fell 4.64 -> 4.48 "
                                              "during setup, ~1/3 of it spent by others): the DISGUISED frontier view runs LAST "
                                              "(after cheap judges, frontier-orig, round trip, SC-5, retest) and only while the "
                                              "key's limit_remaining stays above $0.75 (checked before the stage and every 40 "
                                              "calls); ORIGINAL (the stronger screen view, 0.802) always runs first on all 284"},
        "judge_json_failure_sensitivity": "PRIMARY rule (pre-declared in exp 6): one retry, then oriented 0.5. Pilot: 2/40 flash-lite "
                                          "outputs omitted faithful_prob but kept a verdict. SENSITIVITY column judge_cheap_*_vfb: "
                                          "such rows get the median P(faithful) of ok rows with the same verdict (label-free, "
                                          "computed over all scored rows); criterion (a) is re-reported with it as a robustness row",
        "budget": {"cap_total": 4.60, "caps": {"judge_cheap": 0.75, "judge_cheap2": 0.45, "strong": 2.50, "roundtrip": 0.35,
                                               "sc5": 0.50, "retest": 0.05},
                   "pilot_spend_counts_against_caps": True, "estimates_from_pilot": est,
                   "unique_pairs": {"disg": n_disg, "orig": n_orig, "formulas": n_formulas, "sentences": n_sent},
                   "rule": "a component that reaches its cap stops as status=partial; unspent cheap-arm money is NOT moved to strong. "
                           "CHEAP arms: all PRIMARY rows in R_AB-first order, truncated at the cap."},
        "execution_order": ["cheap_disg", "cheap_orig", "cheap2_disg", "cheap2_orig", "strong_orig", "verbalise",
                            "nli(api, GPU)", "sc_gen", "sc_score", "retest", "strong_disg (reserve rule)"],
        "frontier_frame": {"file": "data/frontier_frame.json", "sha256": hashlib.sha256((DATA / "frontier_frame.json").read_bytes()).hexdigest(),
                           "used_as_is": True},
        "comparators_priority": ["judge_cheap_disg (PRIMARY BAR)", "judge_cheap_orig", "judge_cheap2_disg", "judge_cheap2_orig",
                                 "BEST_API_CHEAP (highest pooled R_AB AUROC of the four, post hoc = conservative)",
                                 "judge_strong_orig / judge_strong_disg (frame)", "S4_full"],
        "challengers": ["c_score_align (frozen, exp 5)", "g_score", "nf_c_score", "p_peer_text (frozen PT fusion)", "p_text"],
        "confirmatory_contrast": "stratified dAUROC(c_score_align - judge_cheap_disg), R_AB, E_POOL PRIMARY (n=2,686), "
                                 "sentence-cluster bootstrap B=2000 seed 0 percentile CI",
        "population": {"main": "E_POOL (system_class llm) PRIMARY (parse_ok strict) under R_AB", "n": 2686, "n_error": 1822,
                       "n_correct": 864, "n_sentences": 292},
        "criteria": {
            "a": "CI_low > 0 for stratified dAUROC(c_score_align - judge_cheap_disg) on R_AB pooled AND on the long pool "
                 "(L25+L20+EXC, stratified) AND point estimate > 0 on R_A L20+EXC (intersection-union; no multiplicity correction)",
            "b": "nested [S4_full + c_score_align] - S4_full stratified OOF dAUROC CI_low > 0 AND observed delta > 95th percentile "
                 "of the 100-rep within-fold x stratum label-permutation null (pooled version reported; disagreement flagged)",
            "d": "[AUROC(c_score_align)/AUROC(best frontier view) >= 0.95 (point) AND FULL consensus $/item <= 0.10 x frontier $/item] "
                 "OR nested frame [judge_strong_orig + c_score_align] - [judge_strong_orig] OOF dAUROC CI_low > 0",
            "M3": "GEE slope(c_score_align) - slope(judge_cheap_disg) of P(correct flag at matched FA=0.10 on R_AB CORRECT) per SD of "
                  "words, clustered by sentence, cluster-bootstrap CI_low > 0 => CONFIRMED (n_conditions version reported)",
            "VEX": "on the VEX subset (if testable), c_score_align - judge_cheap_disg has a POSITIVE sign (stratified if >=2 strata "
                   "testable within VEX, else pooled); CI > 0 reported as the strong form",
            "verdict": "CONFIRM needs (a) and (b), plus (d) and VEX from this artifact; PARTIAL = (a) but not (b) (redundant with "
                       "the API judge) or (a)+(b) but VEX fails (aligner confound not excluded); DISCONFIRM = (a) fails against "
                       "judge_cheap_disg. Criteria (c), (e) belong to other artifacts."},
        "bootstrap": {"B": 2000, "cluster": "sentence_id", "seed": 0, "type": "percentile", "B_gee": 1000,
                      "gee_fallback_B": 500, "permutation_null_reps": 100},
        "thresholds": {"judges": "flag if P(faithful) < 0.5 (oriented > 0.5), screen-frozen",
                       "consensus_PT": {"fused": exp5_pre["frozen"]["fusion"]["threshold"], "text": exp5_pre["frozen"]["text_only"]["threshold"]},
                       "M3_operating_point": "FA = 0.10 on E R_AB CORRECT rows (90th percentile), same for every metric"},
        "testability": ">= 50 ERROR and >= 50 CORRECT rows and >= 25 sentences per side",
        "S4_sets": {"S4_local": s4c,
                    "S4_full": s4c + ["judge_cheap_disg", "judge_cheap_orig", "judge_cheap2_disg", "judge_cheap2_orig", "rt_nli_min",
                                      "rt_nli_fwd", "rt_nli_bwd", "rt_nli_contra", "rt_embed_cos", "sc5_eq_frac", "sc5_entropy"],
                    "entry_rule": "an API column enters only if status in {ok, fallback} on >= 95% of R_AB PRIMARY rows; otherwise it "
                                  "is left out, its local counterpart stays, and the substitution is labelled",
                    "secondary": {"S4_API": "exp 6 prereg S4 set (20 features)", "S4_full_noJudge": "S4_full minus every judge column",
                                  "S4_full_strat": "S4_full + one-hot source_stratum", "S5_frame": "S4_full + judge_strong_* (frame, descriptive)"},
                    "C": 1.0, "folds": "data/folds_E.json (sha1 sentence folds)"},
        "vex": {"declaration_file": "results/vex_declaration.json", "declaration_sha256": vex_sha, "rows_sha256": vex_rows_sha,
                "include_n": vex["include"]["n"], "include_testable": vex["include"]["testable"],
                "strict_n": vex["include_strict"]["n"], "strict_testable": vex["include_strict"]["testable"]},
        "local_fallback": "if an API arm is unfunded, the local exp-6 column (judge_local_qwen8b_disg etc.) is reported as a "
                          "LABELLED secondary bar, never substituted silently in the verdict",
        "pilot_summary": ps,
        "repro_gates_sha256": hashlib.sha256((RES / "repro_gates.json").read_bytes()).hexdigest(),
    }
    PREREG_T1.write_text(json.dumps(D, indent=1, ensure_ascii=False))
    h = hashlib.sha256(PREREG_T1.read_bytes()).hexdigest()
    PREREG_T1_SHA.write_text(f"{h}  prereg_T1.json  frozen {datetime.datetime.utcnow().isoformat(timespec='seconds')}Z\n")
    logger.info(f"prereg_T1 frozen sha256 {h}; strong rule: {strong_rule}; estimates {est}")



def stage_t1_analysis(which=("full",)):
    """Step 5-7: join (per_item_T1.jsonl), every T1 analysis (src/analyse_T1.py), tables, verdict, figures,
    method_out.json. --which quick = 10 permutation reps / B_gee 50 (smoke test only)."""
    from src import analyse_T1 as AT
    from src import report_T1 as RT
    quick = "quick" in which
    ks = _key_status()
    jdump({"end_of_sweeps": ks, "start_of_run": jload(RES / "pilot" / "key_model_check.json")["key"]}, RES / "key_usage_log.json")
    A, T, rows, regimes = AT.run(max_perm=10 if quick else 100, gee_B=50 if quick else 1000)
    A["cost_ledger"] = RT.cost_ledger(A)
    RT.per_item(T, rows, regimes, T.api)
    n = RT.method_out(T, rows, regimes, A)
    try:
        A["figures"] = RT.figures(A)
    except Exception as e:  # noqa: BLE001 - figures are secondary; the failure is recorded
        logger.error(f"figures failed: {e}")
        A["figures"] = {"error": str(e)[:300]}
    jdump(A, RES / "analysis_T1.json")
    jdump(A["verdict"], RES / "verdict_T1.json")
    (RES / "tables_T1.md").write_text(RT.tables(A))
    logger.info(f"T1 analysis: {A['verdict']['overall_T1_this_artifact']}; method_out rows {n}; runtime {A['runtime_s']:.0f}s")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", required=True)
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--which", default=None)
    a = ap.parse_args()
    if a.stage not in ("local_judges", "local_strong", "local_verb", "local_sc", "nli", "b2_read", "t2_repro", "b2_think"):
        set_ram_limit(40)  # RLIMIT_AS breaks CUDA's virtual-address reservations: GPU stages rely on the VRAM guard instead
    fn = globals().get(f"stage_{a.stage}")
    if fn is None:
        raise SystemExit(f"unknown stage {a.stage}")
    t0 = time.time()
    logger.info(f"=== stage {a.stage} limit={a.limit} ===")
    kw = {}
    if "limit" in fn.__code__.co_varnames[:fn.__code__.co_argcount]:
        kw["limit"] = a.limit
    if a.which:
        kw["which"] = tuple(a.which.split(","))
    fn(**kw)
    logger.info(f"=== stage {a.stage} done in {time.time()-t0:.0f}s ===")


if __name__ == "__main__":
    logger.catch(reraise=True)(main)()
