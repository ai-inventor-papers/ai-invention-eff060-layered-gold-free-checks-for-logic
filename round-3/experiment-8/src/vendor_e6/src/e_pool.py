"""Dataset E (held-out, iter-1 gen_art_dataset_1) loader with a LABEL-BLIND default, pool / label-regime definitions,
deterministic sentence folds and the label-vector hash shared with the sibling PEER+TEXT experiment.

load_E(blind=True)  -> rows WITHOUT any label-bearing field (every scoring stage uses only this).
load_E(blind=False) -> full rows; raises unless prereg_baselines.sha256 exists and predates every score file
                       (exception: the frontier-frame drawing script, which passes _frame_ok=True and is disclosed).
"""
from __future__ import annotations

import glob
import json
import os
from pathlib import Path

from .common import ROOT, sha1

E_DIR = Path("/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_dataset_1")
PREREG = ROOT / "prereg_baselines.json"
PREREG_SHA = ROOT / "prereg_baselines.sha256"
SCORES = ROOT / "results" / "scores"

# the 18 label keys of the plan + 4 keys that encode the panel/solver class structure (class c0 = reference class)
LABEL_KEYS = ["output", "metadata_final_label", "metadata_auto_label", "metadata_label_tier", "metadata_label_source",
              "metadata_panel_votes", "metadata_error_ops", "metadata_repair_ops", "metadata_repair_status",
              "metadata_equiv_status", "metadata_correct_not_equivalent", "metadata_reading_choice",
              "metadata_gold_audit_flag", "metadata_reference_status", "metadata_convention_flags",
              "metadata_addrop_only_suspect", "metadata_solver_lenient_label", "metadata_panel_ambiguous"]
EXTRA_BLIND_KEYS = ["metadata_class_id", "metadata_class_size", "metadata_panel_item", "metadata_panel_scope"]
EXPECTED_ROWS, EXPECTED_SENTS = 8507, 700


def _raw_groups() -> dict[str, list[dict]]:
    parts = sorted(glob.glob(str(E_DIR / "full_data_out" / "full_data_out_*.json")))
    files = parts if parts else [str(E_DIR / "full_data_out.json")]
    groups: dict[str, list[dict]] = {}
    for f in files:
        d = json.loads(Path(f).read_text())
        for g in d["datasets"]:
            groups.setdefault(g["dataset"], []).extend(g["examples"])
    return groups


_CACHE: dict = {}


def _prereg_ok() -> bool:
    if not PREREG_SHA.exists() or not PREREG.exists():
        return False
    import hashlib
    if hashlib.sha256(PREREG.read_bytes()).hexdigest() != PREREG_SHA.read_text().split()[0]:
        raise RuntimeError("prereg_baselines.json was modified after freezing (sha256 mismatch)")
    t_pre = PREREG_SHA.stat().st_mtime
    for p in SCORES.glob("*.jsonl"):
        first = p.open().readline()
        if not first.strip():
            continue
        ts = json.loads(first).get("ts")
        if ts is not None and ts < t_pre:
            raise RuntimeError(f"score file {p.name} has a first-line timestamp before the prereg freeze")
    return True


def load_E(blind: bool = True, _frame_ok: bool = False) -> list[dict]:
    """Rows of heldout_candidates with the input JSON unpacked (text, candidate_fol, reference_fol, system, variant)."""
    if not blind and not _frame_ok and not _prereg_ok():
        raise PermissionError("label load refused: prereg_baselines.sha256 missing (freeze the prereg first)")
    key = "blind" if blind else "full"
    if key in _CACHE:
        return _CACHE[key]
    g = _raw_groups()
    rows = g["heldout_candidates"]
    if len(rows) != EXPECTED_ROWS or len({r["metadata_sentence_id"] for r in rows}) != EXPECTED_SENTS:
        raise RuntimeError(f"F-DATA: E has {len(rows)} rows / {len({r['metadata_sentence_id'] for r in rows})} sentences")
    out = []
    cnt: dict = {}
    for r in rows:
        cnt[r["metadata_item_id"]] = cnt.get(r["metadata_item_id"], 0) + 1
    for r in rows:
        inp = json.loads(r["input"])
        x = {k: v for k, v in r.items() if k != "input"}
        x.update({"text": inp["text"], "candidate_fol": inp.get("candidate_fol") or "", "reference_fol": inp.get("reference_fol"),
                  "system": inp.get("system"), "prompt_variant": inp.get("prompt_variant"),
                  # 115 item_ids collide (zero-shot == few-shot output of the same system): row_key disambiguates rows
                  "row_key": r["metadata_item_id"] if cnt[r["metadata_item_id"]] == 1
                  else f"{r['metadata_item_id']}~{r.get('metadata_prompt_variant')}"})
        if blind:
            for k in LABEL_KEYS + EXTRA_BLIND_KEYS:
                x.pop(k, None)
        out.append(x)
    _CACHE[key] = out
    return out


def load_sentences(blind: bool = True) -> list[dict]:
    rows = _raw_groups()["heldout_sentences"]
    if blind:
        return [{k: v for k, v in r.items() if k in ("input", "metadata_sentence_id", "metadata_strata")} for r in rows]
    return rows


def load_screen_audit() -> list[dict]:
    """Screen rows (labels allowed: screen data, not held-out)."""
    return _raw_groups()["screen_audit"]


# ------------------------------------------------------------------ pools (label-free)
def pool_of(r: dict) -> str:
    if r.get("metadata_system_class") == "llm":
        return "E_POOL"
    if r.get("metadata_system") == "malls_gpt4_gold":
        return "GOLDSYS"
    if r.get("metadata_system_class") == "symbolic_eventsem":
        return "CCG"
    return "OTHER"


def sysvar(r: dict) -> str:
    return f"{r['metadata_system']}|{r.get('metadata_prompt_variant') or r.get('prompt_variant')}"


def fold_of_sentence(sid: str) -> int:
    return int(sha1("E_folds_v1|" + sid), 16) % 5


# ------------------------------------------------------------------ label regimes (need load_E(blind=False))
def y_of(label: str) -> int | None:
    return {"ERROR": 1, "CORRECT": 0}.get(label)


def regime_labels(rows_full: list[dict], regime: str) -> dict[str, int]:
    """{row_key: y} (1 = ERROR/unfaithful) for one label regime. Rows outside the regime are absent."""
    out = {}
    for r in rows_full:
        lab, tier = r["metadata_final_label"], r["metadata_label_tier"]
        rc = bool(r.get("metadata_reading_choice"))
        iid = r["row_key"]
        if regime == "R_AB":
            if tier in ("A", "B") and lab in ("CORRECT", "ERROR") and not rc:
                out[iid] = y_of(lab)
        elif regime == "R_A":
            if tier == "A" and lab in ("CORRECT", "ERROR") and not rc:
                out[iid] = y_of(lab)
        elif regime == "COVERAGE":
            if tier in ("A", "B") and lab in ("CORRECT", "ERROR") and not rc:
                out[iid] = y_of(lab)
            elif lab == "UNPARSEABLE":
                out[iid] = 1
        elif regime in ("CONTESTED_AS_CORRECT", "CONTESTED_AS_ERROR"):
            if tier in ("A", "B") and lab in ("CORRECT", "ERROR") and not rc:
                out[iid] = y_of(lab)
            elif lab == "CONTESTED" and not rc:
                out[iid] = 0 if regime == "CONTESTED_AS_CORRECT" else 1
        elif regime == "ALL_TIERS":
            if lab in ("CORRECT", "ERROR") and not rc:
                out[iid] = y_of(lab)
        elif regime == "R_AB_L25_NO_TOPUP":
            st = r["metadata_strata"]
            if tier in ("A", "B") and lab in ("CORRECT", "ERROR") and not rc and not (
                    st.get("source_stratum") == "L25" and st.get("l25_topup_batch")):
                out[iid] = y_of(lab)
        else:
            raise ValueError(regime)
    return out


def label_vector_sha1(ids, labels) -> str:
    """sha1 of the sorted 'item_id:label' lines (identical to the sibling PEER+TEXT experiment's function)."""
    return sha1("\n".join(sorted(f"{i}:{l}" for i, l in zip(ids, labels))))


def env_hashseed_ok() -> None:
    if os.environ.get("PYTHONHASHSEED") != "0":
        raise RuntimeError("PYTHONHASHSEED must be 0 (repair_census.fp uses hash())")
