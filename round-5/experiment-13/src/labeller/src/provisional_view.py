#!/usr/bin/env python3
"""Provisional search-level view for iteration 5 while the gloss step is pending (D9): ERROR (= ERROR_CERT, final) vs
MAPPED (z3-equivalent under some family map; not gloss-checked). Adds block 'search_provisional_view' to
results/testability_FREE_v2.json with the testability rule applied to ERROR vs MAPPED and the audited contamination of
both classes. NOT a replacement for the pre-registered CORRECT class."""
from __future__ import annotations

import json

from assemble_labels import testability
from common import RES, dump, load_jsonl


def main() -> None:
    rows = load_jsonl(RES / "free_labels_v2.jsonl")
    view = []
    for r in rows:
        r2 = dict(r)
        r2["label_binary"] = {"ERROR_CERT": "ERROR", "UNRESOLVED_GLOSS_NOT_RUN": "CORRECT"}.get(r["label"], "EXCLUDED")
        view.append(r2)
    sa = json.loads((RES / "soundness_audit.json").read_text())
    ea = sa["ii_executor_audit"]
    rep = sa["i_sig_replay"]
    t = json.loads((RES / "testability_FREE_v2.json").read_text())
    t["search_provisional_view"] = {
        "definition": "class 'CORRECT' in this block = MAPPED (search-level, NOT gloss-checked); ERROR = ERROR_CERT",
        "all_rows": testability(view, "all FREE rows, provisional ERROR_CERT vs MAPPED"),
        "untouched_subset": testability([r for r in view if not r.get("seen_iter3")], "untouched subset, provisional"),
        "contamination": {
            "MAPPED_share_faithful_executor_audit": [ea["MAPPED"]["share_faithful (upper bound of CORRECT precision if the gloss check accepted every MAPPED row)"], ea["MAPPED"]["ci"]],
            "ERROR_CERT_share_not_faithful_executor_audit": [ea["ERROR_CERT"]["implied_precision_not_rated_faithful"], ea["ERROR_CERT"]["ci"]],
            "SIG_known_error_rescue_rate_nonce": rep["nonce"]["rescue_rate_on_SIG_ERROR (non-identity equivalent map exists)"],
            "note": "executor audit is non-blind (D9); the SIG rescue rate is exact but on SIG-distribution errors"},
    }
    dump(RES / "testability_FREE_v2.json", t)
    p = t["search_provisional_view"]
    print({k: {x: p[k][x] for x in ("n_ERROR", "n_CORRECT", "sentences_with_ERROR", "sentences_with_CORRECT", "TESTABLE")}
           for k in ("all_rows", "untouched_subset")})


if __name__ == "__main__":
    main()
