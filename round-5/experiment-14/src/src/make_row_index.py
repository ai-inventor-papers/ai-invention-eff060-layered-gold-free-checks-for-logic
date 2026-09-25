#!/usr/bin/env python3
"""Write results/row_index_labelfree.jsonl: per_item_T1 rows with LABEL fields stripped (whitelist), for the sealed scorer."""
from __future__ import annotations

import json

from common import PER_ITEM, RES, jl, sha256_file

KEEP = ["canonical_key", "exp5_row_key", "sentence_id", "fold_E", "source_stratum", "family", "system", "pool", "parse_ok",
        "prompt_variant", "c_score_align"]
FORBIDDEN = {"final_label", "y_R_AB", "in_R_AB", "in_R_A", "label_tier", "auto_label", "error_ops", "repair_ops", "reading_choice", "vex"}


def main():
    rows = jl(PER_ITEM)
    out = RES / "row_index_labelfree.jsonl"
    with out.open("w") as fh:
        for r in rows:
            d = {k: r[k] for k in KEEP}
            d["words"] = r["strata"]["words"]
            d["n_conditions"] = r["strata"]["n_conditions"]
            assert not (set(d) & FORBIDDEN)
            fh.write(json.dumps(d) + "\n")
    print(len(rows), sha256_file(out))


if __name__ == "__main__":
    main()
