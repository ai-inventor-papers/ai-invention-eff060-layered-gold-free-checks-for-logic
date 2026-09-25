#!/usr/bin/env python3
"""Extract dataset 3's perturb_suite into data/perturb_rows.jsonl (one flat row per mutant/control), check dataset E's
R_AB / R_A label-vector sha1s against exp 6's prereg_baselines.json (stop on mismatch), and log vendored-file sha1s."""
from __future__ import annotations

import glob
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

from loguru import logger

ROOT = Path(__file__).resolve().parent.parent
RUN = Path(__file__).resolve().parents[4]
D3 = RUN / "round-2/dataset-3/src"
DE = RUN / "round-1/dataset-1/src"
E6 = RUN / "iter_2/gen_art/gen_art_experiment_6"

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(ROOT / "logs" / "prep_data.log", rotation="30 MB", level="DEBUG")


def load_groups(d: Path, want: str) -> list[dict]:
    files = sorted(glob.glob(str(d / "full_data_out" / "full_data_out_*.json"))) or [str(d / "full_data_out.json")]
    out = []
    for f in files:
        for g in json.loads(Path(f).read_text())["datasets"]:
            if g["dataset"] == want:
                out.extend(g["examples"])
    return out


@logger.catch(reraise=True)
def main():
    ex = load_groups(D3, "perturb_suite")
    logger.info(f"perturb_suite rows: {len(ex)}")
    rows = []
    for r in ex:
        inp = json.loads(r["input"])
        sysname = r["metadata_system"]
        is_ctrl = r["metadata_fold"] == "PERTURB_CONTROL"
        rows.append({
            "item_id": r["metadata_item_id"], "sentence_id": r["metadata_sentence_id"], "base_item_id": r["metadata_base_item_id"],
            "fold": r["metadata_fold"], "system": sysname, "label": r["output"],
            "operator": None if is_ctrl else r.get("metadata_operator"),
            "control_type": r.get("metadata_subtype") if is_ctrl else None,
            "op_fine": None if is_ctrl else ("ADD_INTERNAL" if r.get("metadata_subtype") == "ADD_INTERNAL" else r.get("metadata_operator")),
            "polarity": r.get("metadata_position_polarity"), "matched_pair_id": r.get("metadata_matched_pair_id"),
            "matched_pair_complete": r.get("metadata_matched_pair_complete"), "subtype": r.get("metadata_subtype"),
            "base_source": r.get("metadata_base_source"), "base_trust": r.get("metadata_base_trust"),
            "strata": r.get("metadata_strata"), "text": inp["text"], "candidate_fol": inp["candidate_fol"],
            "reference_fol": inp.get("reference_fol"), "reference_fol_weak": inp.get("reference_fol_weak"),
            "reference_fol_strong": inp.get("reference_fol_strong"),
            "disguised_text": r.get("metadata_disguised_text"), "disguised_fol": r.get("metadata_disguised_fol"),
            "disguised_reference_fol": r.get("metadata_disguised_reference_fol"),
            "edited_predicate": r.get("metadata_edited_predicate"), "error_ops": r.get("metadata_error_ops"),
        })
    c = Counter((x["fold"], x["op_fine"] or x["control_type"], x["polarity"]) for x in rows)
    logger.info(f"counts: {sorted(c.items())}")
    logger.info(f"base sources: {Counter(x['base_source'] for x in {r['base_item_id']: r for r in rows}.values())}")
    (ROOT / "data" / "perturb_rows.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in rows))
    # ---- label-vector check (dataset E vs exp 6 prereg_baselines)
    pb = json.loads((E6 / "prereg_baselines.json").read_text())
    E = load_groups(DE, "heldout_candidates")
    lv = {}
    for name, pred in (("R_AB", lambda r: r.get("metadata_label_tier") in ("A", "B") and r["output"] in ("CORRECT", "ERROR") and not r.get("metadata_reading_choice")),
                       ("R_A", lambda r: r.get("metadata_label_tier") == "A" and r["output"] in ("CORRECT", "ERROR") and not r.get("metadata_reading_choice"))):
        lines = sorted(f"{r['metadata_item_id']}:{r['output']}" for r in E if pred(r))
        lv[name] = {"n": len(lines), "sha1": hashlib.sha1("\n".join(lines).encode()).hexdigest()}
    exp = pb["label_vectors"]
    res = {k: {"ours": lv[k], "prereg": {"n": exp[k]["n"], "sha1": exp[k]["sha1"]}, "match": lv[k]["sha1"] == exp[k]["sha1"]} for k in lv}
    logger.info(f"label-vector check: {json.dumps(res)}")
    (ROOT / "results").mkdir(exist_ok=True)
    (ROOT / "results" / "label_vector_check.json").write_text(json.dumps(res, indent=1))
    if not all(v["match"] for v in res.values()):
        logger.warning("label-vector sha1 mismatch vs exp 6 prereg_baselines (see results/label_vector_check.json)")
    # ---- vendored-file manifest
    man = {str(p.relative_to(ROOT)): hashlib.sha1(p.read_bytes()).hexdigest() for p in sorted((ROOT / "src").rglob("*.py"))}
    (ROOT / "logs" / "vendor_manifest.json").write_text(json.dumps(man, indent=1))
    logger.info(f"vendor manifest: {len(man)} files")


if __name__ == "__main__":
    main()
