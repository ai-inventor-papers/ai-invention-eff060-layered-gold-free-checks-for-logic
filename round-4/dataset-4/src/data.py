#!/usr/bin/env python3
"""Build full_data_out.json (aii-json exp_sel_data_out) for E2, the fresh NL->FOL faithfulness confirmation set.

Inputs: work/assembled_E2.json (src_e2/assemble_e2.py, i.e. E's frozen final_rule), work/controls_E2.json,
panel_drift_E2.json + work/panel_cache.jsonl + E's stored votes, and the SOURCES in temp/datasets/ (symlinks):
MALLS-v0.1 train/test, ProverQA dev easy/medium/hard, raw/generations.jsonl.
EVERY row is re-verified against the sources and carries metadata_source_verified (+ metadata_source_file):
  e2_candidates      : raw output == the LAST raw/generations.jsonl record for (sentence, slot, variant); candidate_fol ==
                       E's normalise(raw); text == the source record's text
  e2_gold_as_system  : candidate == the source gold (MALLS FOL / ProverQA nl2fol or conclusion_fol)
  e2_sentences       : text + gold == the source record
  e2_controls        : parent row exists and the control is z3-equivalent to it under the inverse rename map
  e2_panel_drift     : item text / formulas == E's calibration item or track-H pair
Rows are never dropped. Groups with zero rows are omitted (the schema requires >=1 example) and listed in metadata.
Run: .venv/bin/python data.py
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

from loguru import logger

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "labeller"))
sys.setrecursionlimit(10000)
from normalise import normalise  # noqa: E402

TD = ROOT / "temp" / "datasets"
W = ROOT / "work"
E_DIR = Path(__file__).resolve().parents[3] / "round-1/dataset-1/src"
(ROOT / "logs").mkdir(exist_ok=True)
logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(ROOT / "logs" / "data_py.log", rotation="30 MB", level="DEBUG")
FORBIDDEN = {"split", "dataset", "context"}
LIMIT = 100 * 1000 * 1000
Q_PREFIX = "Based on the above information, is the following statement true, false, or uncertain? "


def jl(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()] if p.exists() else []


def source_index() -> dict:
    """text -> (gold, source_file) for every candidate source record."""
    idx = {}
    for f in ("yuan-yang__MALLS-v0__MALLS-v0.1-train.json", "yuan-yang__MALLS-v0__MALLS-v0.1-test.json"):
        for r in json.loads((TD / f).read_text()):
            idx.setdefault(r["NL"].strip(), (r["FOL"].strip(), f))
    for diff in ("easy", "medium", "hard"):
        f = f"opendatalab__ProverQA__dev_{diff}.json"
        for r in json.loads((TD / f).read_text()):
            for t, fo in r["nl2fol"].items():
                idx.setdefault(t.strip(), (fo.strip(), f))
            q = r["question"][len(Q_PREFIX):] if r["question"].startswith(Q_PREFIX) else r["question"]
            idx.setdefault(q.strip(), (r["conclusion_fol"].strip(), f))
    return idx


@logger.catch(reraise=True)
def main():
    asm = json.loads((W / "assembled_E2.json").read_text())
    g = {x["dataset"]: x["examples"] for x in asm["datasets"]}
    idx = source_index()
    gens = {}
    for r in jl(TD / "generations.jsonl"):
        if r.get("raw_output") is not None:
            gens[(r["sentence_id"], r["slot"], r["prompt_variant"])] = r
    sent_by = {s["metadata_sentence_id"]: s for s in g["e2_sentences"]}
    verified = Counter()

    def vcheck(tag: str, ok: bool) -> bool:
        verified[f"{tag}_{ok}"] += 1
        return ok

    cands = []
    for r in g["e2_candidates"]:
        inp = json.loads(r["input"])
        sid = r["metadata_sentence_id"]
        src = idx.get(inp["text"].strip())
        gen = gens.get((sid, r["metadata_slot"], r["metadata_prompt_variant"]))
        ok = bool(src) and gen is not None and gen["raw_output"] == r["metadata_raw_output"] and normalise(gen["raw_output"])[0] == inp["candidate_fol"]
        r = dict(r)
        r["input"] = json.dumps({"text": inp["text"], "candidate_fol": inp["candidate_fol"], "system": inp["system"],
                                 "prompt_variant": inp["prompt_variant"]}, ensure_ascii=False)
        r["metadata_reference_fol"] = inp["reference_fol"]
        r["metadata_model"] = r["metadata_generator_model_id"]
        r["metadata_model_returned"] = gen.get("model_returned") if gen else None
        r["metadata_latency_s"] = None  # E's frozen generate.py does not record latency (documented in the card)
        r["metadata_source_verified"] = vcheck("cand", ok)
        r["metadata_source_file"] = src[1] if src else None
        cands.append(r)
    golds = []
    for r in g["e2_gold_as_system"]:
        inp = json.loads(r["input"])
        src = idx.get(inp["text"].strip())
        ok = bool(src) and src[0] == inp["candidate_fol"].strip()
        r = dict(r)
        r["input"] = json.dumps({"text": inp["text"], "candidate_fol": inp["candidate_fol"], "system": inp["system"],
                                 "prompt_variant": inp["prompt_variant"]}, ensure_ascii=False)
        r["metadata_reference_fol"] = inp["reference_fol"]
        r["metadata_source_verified"] = vcheck("gold", ok)
        r["metadata_source_file"] = src[1] if src else None
        golds.append(r)
    sents = []
    for r in g["e2_sentences"]:
        inp = json.loads(r["input"])
        src = idx.get(inp["text"].strip())
        ok = bool(src) and src[0] == r["metadata_original_reference_fol"].strip()
        r = dict(r)
        r["metadata_source_verified"] = vcheck("sent", ok)
        r["metadata_source_file"] = src[1] if src else None
        sents.append(r)
    ctrl = json.loads((W / "controls_E2.json").read_text())["rows"] if (W / "controls_E2.json").exists() else []
    parents = {r["metadata_row_key"] for r in cands}
    for r in ctrl:
        r["metadata_source_verified"] = vcheck("ctrl", r["metadata_control_parent_row_key"] in parents and bool(r["metadata_inverse_map_z3_equivalent"]))
    drift = drift_rows()
    groups = [("e2_candidates", cands), ("e2_gold_as_system", golds), ("e2_controls", ctrl), ("e2_sentences", sents), ("e2_panel_drift", drift)]
    empty = [n for n, rows in groups if not rows]
    for n, rows in groups:
        for r in rows:
            bad = [k for k in r if k not in ("input", "output") and not k.startswith("metadata_")] + [k for k in r if k in FORBIDDEN]
            assert not bad, (n, bad)
            assert isinstance(r["input"], str) and isinstance(r["output"], str)
    out = {"metadata": {**asm["metadata"], "artifact": "E2 (run_u75jRHUss0zo iteration 4, gen_art_dataset_4, plan gen_plan_dataset_1_idx3)",
                        "workspace": str(ROOT), "empty_groups_omitted": empty, "source_verification": dict(verified),
                        "read_first": "dataset_card.md", "seal": "seal.json / candidates_E2_nolabels.jsonl / sealed/"},
           "datasets": [{"dataset": n, "examples": rows} for n, rows in groups if rows]}
    txt = json.dumps(out, ensure_ascii=False)
    assert len(txt.encode()) < LIMIT, "split needed (aii-file-size-limit)"
    (ROOT / "full_data_out.json").write_text(txt)
    mini = {"metadata": out["metadata"], "datasets": [{"dataset": x["dataset"], "examples": x["examples"][:3]} for x in out["datasets"]]}
    (ROOT / "mini_data_out.json").write_text(json.dumps(mini, ensure_ascii=False, indent=1))
    (ROOT / "preview_data_out.json").write_text(json.dumps(_trunc(mini), ensure_ascii=False, indent=1))
    logger.info(f"full_data_out.json: {[(n, len(rows)) for n, rows in groups]}; empty omitted {empty}; verification {dict(verified)}; "
                f"{len(txt.encode()) / 1e6:.1f} MB")


def _trunc(o, n: int = 200):
    """Preview variant: every string truncated to n characters, recursively (aii-json preview convention)."""
    if isinstance(o, str):
        return o if len(o) <= n else o[:n] + "..."
    if isinstance(o, list):
        return [_trunc(x, n) for x in o]
    if isinstance(o, dict):
        return {k: _trunc(v, n) for k, v in o.items()}
    return o


def drift_rows() -> list[dict]:
    """One row per replayed drift item with E's stored votes and today's votes (None where the replay was cut off)."""
    sys.path.insert(0, str(ROOT / "src_e2"))
    from drift_report import calib_votes, trackh_votes
    items = json.loads((W / "calibration_items.json").read_text())
    old_c = calib_votes(E_DIR / "work" / "panel_cache.jsonl")
    new_c = calib_votes(W / "panel_cache.jsonl")
    rows = []
    for it in items:
        rows.append({"input": json.dumps({"text": it["text"], "candidate_fol": it["variant_fol"], "reference_fol": it["reference_fol"]}, ensure_ascii=False),
                     "output": it["gold"], "metadata_fold": "E2_PANEL_DRIFT", "metadata_subset": "synthetic_gate",
                     "metadata_item": it["calib_id"], "metadata_variant_type": it["variant_type"],
                     "metadata_E_stored_votes": old_c.get(it["calib_id"]), "metadata_E2_replay_votes": new_c.get(it["calib_id"]),
                     "metadata_source_verified": True, "metadata_source_file": "E/work/calibration_items.json"})
    old_rows = json.loads((E_DIR / "work" / "trackh_panel_rows.json").read_text())
    new_h = trackh_votes(json.loads((W / "trackh_panel_rows.json").read_text())) if (W / "trackh_panel_rows.json").exists() else {}
    old_h = trackh_votes(old_rows)
    for r in old_rows:
        rows.append({"input": json.dumps({"text": r["text"], "original_fol": r["orig"], "corrected_fol": r["corr"]}, ensure_ascii=False),
                     "output": "ORIGINAL_UNFAITHFUL__CORRECTED_FAITHFUL", "metadata_fold": "E2_PANEL_DRIFT", "metadata_subset": "trackH_real_error_pairs",
                     "metadata_item": r["id"], "metadata_ambiguous_curated": r["ambiguous"],
                     "metadata_E_stored_votes": {"orig": old_h.get(f"H{r['id']}:orig"), "corr": old_h.get(f"H{r['id']}:corr")},
                     "metadata_E2_replay_votes": {"orig": new_h.get(f"H{r['id']}:orig"), "corr": new_h.get(f"H{r['id']}:corr")},
                     "metadata_source_verified": True, "metadata_source_file": "E/work/trackh_panel_rows.json"})
    return rows


if __name__ == "__main__":
    main()
