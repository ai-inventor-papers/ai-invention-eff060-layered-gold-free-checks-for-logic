#!/usr/bin/env python3
# NOTE (published copy): this file names server paths this repository
# does not publish (a stage it does not ship, or another run's workspace),
# so the steps that read them will not run from a clone as written:
#   /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_dataset_1
"""STEP 1 data views for dataset E (held-out) and the iteration-1 screen.

make_blind_view(rows)  -> data/E_blind.jsonl : ALLOWLIST of label-free fields only (asserted); sha256 written next to it.
make_label_view(rows)  -> data/E_labels.jsonl: item_id + every label field. Read ONLY by analyse_E.py after the prereg check.
api_priority           -> data/api_priority.json: ordered item_ids for the API jobs (judge / L3). The ORDER uses only
                          label AVAILABILITY (is the row in the analysable R_AB pool: llm, tier A/B, decided,
                          not reading_choice) so the shared-key budget is spent on rows that can be analysed first; the
                          label VALUE is never exposed to any scorer. Documented as a deviation-free budget measure.
"""
from __future__ import annotations

import glob
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

from loguru import logger

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
E_DIR = Path("/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_dataset_1")

ALLOW_META = ["item_id", "sentence_id", "system", "slot", "family", "system_class", "generator_model_id", "prompt_variant"]
STRATA_KEYS = ["words", "n_quant", "depth", "n_conditions", "text_conditions", "exception_type", "source_stratum",
               "ctrl_len_bin", "l25_topup_batch"]
FORBIDDEN = ["output", "reference_fol", "auto_label", "equiv_status", "repair_ops", "repair_status", "convention_flags",
             "panel_votes", "panel_item", "panel_ambiguous", "panel_scope", "final_label", "error_ops", "label_tier",
             "label_source", "addrop_only_suspect", "solver_lenient_label", "correct_not_equivalent", "reading_choice",
             "gold_audit_flag", "reference_status", "class_id", "class_size"]
LABEL_FIELDS = ["final_label", "label_tier", "auto_label", "equiv_status", "repair_ops", "repair_status", "error_ops",
                "label_source", "addrop_only_suspect", "solver_lenient_label", "correct_not_equivalent", "reading_choice",
                "gold_audit_flag", "reference_status", "class_id", "class_size", "panel_votes", "panel_scope",
                "convention_flags"]
STRATUM_ORDER = {"CTRL": 0, "EXC": 1, "L20": 2, "L25": 3}


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load_E() -> list[dict]:
    """Glob both layouts (single file or directory of parts); return heldout_candidates examples."""
    files = sorted(glob.glob(str(E_DIR / "full_data_out" / "full_data_out_*.json")))
    if not files:
        files = [str(E_DIR / "full_data_out.json")]
    rows = []
    for f in files:
        d = json.loads(Path(f).read_text())
        for g in d["datasets"]:
            if g["dataset"] == "heldout_candidates":
                rows.extend(g["examples"])
    logger.info(f"E heldout_candidates: {len(rows)} rows from {len(files)} file(s)")
    return rows


def make_blind_view(rows: list[dict]) -> list[dict]:
    out = []
    for r in rows:
        inp = json.loads(r["input"])
        b = {k: r.get(f"metadata_{k}") for k in ALLOW_META}
        b["row_key"] = f"{b['item_id']}|{b['prompt_variant']}"  # item_id is sha1(system|text|fol): zero/few-shot twins collide
        b["text"] = inp["text"]
        b["candidate_fol"] = inp.get("candidate_fol") or ""
        st = r.get("metadata_strata") or {}
        b["strata"] = {k: st.get(k) for k in STRATA_KEYS}
        for k in FORBIDDEN:
            assert k not in b and k not in b["strata"], f"forbidden key {k} in blind view"
        out.append(b)
    return out


def make_label_view(rows: list[dict]) -> list[dict]:
    out = []
    for r in rows:
        inp = json.loads(r["input"])
        x = {"row_key": f"{r['metadata_item_id']}|{r['metadata_prompt_variant']}", "item_id": r["metadata_item_id"], "sentence_id": r["metadata_sentence_id"], "system": r["metadata_system"],
             "system_class": r["metadata_system_class"], "prompt_variant": r["metadata_prompt_variant"],
             "family": r["metadata_family"], "output": r["output"], "reference_fol": inp.get("reference_fol"),
             "strata": r.get("metadata_strata")}
        for k in LABEL_FIELDS:
            x[k] = r.get(f"metadata_{k}")
        out.append(x)
    return out


def analysable(x: dict) -> bool:
    return (x["system_class"] == "llm" and x["label_tier"] in ("A", "B") and x["final_label"] in ("CORRECT", "ERROR")
            and not x["reading_choice"])


def api_priority(blind: list[dict], labels: list[dict]) -> list[str]:
    """Order: (0) analysable R_AB LLM rows, (1) malls_gpt4_gold rows, (2) everything else; within: stratum CTRL, EXC,
    L20, L25 then sha1(item_id)."""
    lab = {x["row_key"]: x for x in labels}

    def key(b):
        x = lab[b["row_key"]]
        grp = 0 if analysable(x) else (1 if b["system_class"] == "reference_gold_as_system" else 2)
        return (grp, STRATUM_ORDER.get(b["strata"]["source_stratum"], 9), hashlib.sha1(b["row_key"].encode()).hexdigest())
    return [b["row_key"] for b in sorted(blind, key=key)]


@logger.catch(reraise=True)
def main():
    logger.remove()
    logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
    logger.add(ROOT / "logs" / "data_views.log", rotation="30 MB", level="DEBUG")
    rows = load_E()
    blind = make_blind_view(rows)
    ids = [b["row_key"] for b in blind]
    assert len(set(ids)) == len(ids), "E row_key not unique"
    logger.info(f"item_id duplicates (zero/few-shot identical outputs): {len(ids) - len({b['item_id'] for b in blind})}")
    p = DATA / "E_blind.jsonl"
    p.write_text("".join(json.dumps(b, ensure_ascii=False) + "\n" for b in blind))
    txt = p.read_text()
    for k in FORBIDDEN:
        assert f'"{k}":' not in txt, f"forbidden key {k} leaked into E_blind.jsonl"
    (DATA / "E_blind.sha256").write_text(sha256_file(p) + "\n")
    labels = make_label_view(rows)
    (DATA / "E_labels.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in labels))
    pr = api_priority(blind, labels)
    n_an = sum(analysable(x) for x in labels)
    (DATA / "api_priority.json").write_text(json.dumps({"order": pr, "n_analysable_first": n_an}))
    logger.info(f"E_blind {len(blind)} rows sha256 {sha256_file(p)[:12]}; analysable R_AB rows {n_an}")
    logger.info(f"system_class {Counter(b['system_class'] for b in blind)}; strata {Counter(b['strata']['source_stratum'] for b in blind)}")
    logger.info(f"families {Counter(b['family'] for b in blind)}; slots {Counter(b['slot'] for b in blind)}")


if __name__ == "__main__":
    main()
