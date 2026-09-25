#!/usr/bin/env python3
"""STEP H (post-seal only): join exp 7's iteration-3 FREE labels through a WHITELIST loader (row_key, label, label_tier,
label_source; every other key is dropped at parse time, so no score ever enters memory), define seen_iter3, declare
testability on the untouched subset, and write the old-vs-new agreement table (audit iii) + 20 disagreements for hand
classification. Refuses to run unless results/seal.json holds a seal.
"""
from __future__ import annotations

import json
import random
import time
from collections import Counter

from assemble_labels import label_vector_sha, testability
from common import OLD_CANDIDATES, RES, dump, load_jsonl, setup_logger

logger = setup_logger("post_seal_join")
WHITELIST = ("row_key", "label", "label_tier", "label_source")


def whitelist_hook(pairs):
    return {k: v for k, v in pairs if k in WHITELIST}


def load_old() -> dict:
    out = {}
    with OLD_CANDIDATES.open() as fh:
        for line in fh:
            if not line.strip():
                continue
            r = json.loads(line, object_pairs_hook=whitelist_hook)
            if "|FREE|" in r.get("row_key", ""):
                out[r["row_key"]] = r
    return out


def kappa(pairs) -> float | None:
    n = len(pairs)
    if not n:
        return None
    po = sum(a == b for a, b in pairs) / n
    ca, cb = Counter(a for a, _ in pairs), Counter(b for _, b in pairs)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / (n * n)
    return round((po - pe) / (1 - pe), 3) if pe < 1 else None


def main() -> None:
    seal = json.loads((RES / "seal.json").read_text())["seals"]
    assert seal, "no seal: run assemble_labels.py first"
    last = seal[-1]
    rows = load_jsonl(RES / "free_labels_v2.jsonl")
    assert label_vector_sha(rows) == last["label_vector_sha256_all_rows"], "labels changed after the seal"
    old = load_old()
    logger.info(f"old FREE rows (whitelisted keys only): {len(old)}; tiers {dict(Counter((o.get('label'), o.get('label_tier')) for o in old.values()))}")
    missing = [r["row_key"] for r in rows if r["row_key"] not in old]
    for r in rows:
        o = old.get(r["row_key"], {})
        r["seen_iter3"] = bool(o.get("label") in ("CORRECT", "ERROR") and o.get("label_tier") == "A")
        r["old_label_iter3"] = o.get("label")
        r["old_label_tier_iter3"] = o.get("label_tier")
    with (RES / "free_labels_v2.jsonl").open("w") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    untouched = [r for r in rows if not r["seen_iter3"]]
    t = json.loads((RES / "testability_FREE_v2.json").read_text())
    t["untouched_subset"] = testability(untouched, "untouched subset (not tier-A labelled in iteration 3) - PRIMARY")
    t["seen_iter3_subset"] = testability([r for r in rows if r["seen_iter3"]], "seen_iter3 subset")
    dump(RES / "testability_FREE_v2.json", t)
    last2 = dict(last)
    last2.update(utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), stage="post_seal_untouched_declaration",
                 label_vector_sha256_untouched=label_vector_sha(untouched), n_untouched=len(untouched),
                 old_labels_joined=True, note="labels unchanged (all-row hash re-verified before the join)")
    seal_all = json.loads((RES / "seal.json").read_text())
    seal_all["seals"].append(last2)
    dump(RES / "seal.json", seal_all)
    # agreement: old tier-A binary vs new search-level view (ERROR_CERT vs MAPPED) and vs final binary
    tab = Counter()
    pairs = []
    dis = []
    for r in rows:
        if not r["seen_iter3"]:
            continue
        new_view = {"ERROR_CERT": "ERROR", "UNRESOLVED_GLOSS_NOT_RUN": "MAPPED", "CORRECT": "CORRECT",
                    "ERROR_GLOSS": "ERROR"}.get(r["label"], r["label"])
        tab[(r["old_label_iter3"], new_view)] += 1
        nv = "ERROR" if new_view == "ERROR" else "CORRECT_OR_MAPPED"
        ov = "ERROR" if r["old_label_iter3"] == "ERROR" else "CORRECT_OR_MAPPED"
        pairs.append((ov, nv))
        if ov != nv:
            dis.append(r)
    rng = random.Random(0)
    sample = rng.sample(dis, min(20, len(dis)))
    rep = {"utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "old_rows_found": len(old), "new_rows": len(rows), "new_row_keys_missing_in_old": len(missing),
           "missing_examples": missing[:10],
           "seen_iter3": sum(r["seen_iter3"] for r in rows), "untouched": len(untouched),
           "old_label_counts_on_new_rows": dict(Counter(r["old_label_iter3"] for r in rows)),
           "agreement_table_old_tierA_vs_new": {f"{a}|{b}": v for (a, b), v in sorted(tab.items())},
           "kappa_old_vs_new_search_view": kappa(pairs),
           "note": ("search-only mode: the new side is ERROR (ERROR_CERT) vs MAPPED (z3-equivalent under some family map, not yet "
                    "gloss-checked); MAPPED is an upper bound of CORRECT"),
           "disagreement_sample_for_hand_classification": [
               {k: r.get(k) for k in ("row_key", "sentence_id", "template_id", "text", "candidate_fol", "old_label_iter3",
                                      "label", "search_status", "map_certificate", "nonequiv_certificate_type_counts")}
               for r in sample]}
    dump(RES / "old_label_agreement.json", rep)
    logger.info(f"agreement: {rep['agreement_table_old_tierA_vs_new']} kappa={rep['kappa_old_vs_new_search_view']}; "
                f"untouched {len(untouched)}; missing keys {len(missing)}")


if __name__ == "__main__":
    main()
