#!/usr/bin/env python3
"""E calibration units for the 4-bit (nf4) local judges / round-trip on the 16 GB GPU (deviation D-GPU16).
The judges' frozen E scores (exp 6) were produced at bf16 on a 21 GB GPU; this machine has 16 GB, so the 8B judges run
nf4. To keep PRIMARY thresholds (matched FA 0.10 on E R_AB LLM CORRECT rows) on the SAME quantisation as the PERTURB
scores, we re-score: all 864 E R_AB LLM CORRECT rows + 400 sha1-ordered R_AB ERROR rows (the latter only to measure the
nf4-vs-bf16 shift in E AUROC on identical rows). Written after the PREREG_HYB freeze. Output data/E_calib_units.jsonl."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
E6 = Path("/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_6")


def main():
    assert (ROOT / "results/prereg_hyb.sha256").exists(), "labels may be read only after the PREREG_HYB freeze"
    lab = {}
    for l in (ROOT / "data/exp5/E_labels.jsonl").read_text().splitlines():
        r = json.loads(l)
        if r["system_class"] == "llm" and not r.get("reading_choice") and r["final_label"] in ("CORRECT", "ERROR") \
                and r["label_tier"] in ("A", "B"):
            lab[r["item_id"]] = r["final_label"]
    U = json.loads((E6 / "data/E_units.json").read_text())
    rows = [u for u in U if u["item_id"] in lab and u.get("parse_ok") and u.get("fol_d")]
    cor = [u for u in rows if lab[u["item_id"]] == "CORRECT"]
    err = sorted([u for u in rows if lab[u["item_id"]] == "ERROR"], key=lambda u: hashlib.sha1(u["item_id"].encode()).hexdigest())[:400]
    out = [{"key": "EC:" + u["row_key"], "item_id": u["item_id"], "row_key": u["row_key"], "label": lab[u["item_id"]],
            "text": u["text"], "fol": u["candidate_fol"], "text_d": u["text_d"], "fol_d": u["fol_d"],
            "stratum": u["strata"]["source_stratum"], "sentence_id": u["sentence_id"]} for u in cor + err]
    (ROOT / "data/E_calib_units.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in out))
    print(len(cor), len(err), "parseable R_AB LLM rows", len(rows))


if __name__ == "__main__":
    main()
