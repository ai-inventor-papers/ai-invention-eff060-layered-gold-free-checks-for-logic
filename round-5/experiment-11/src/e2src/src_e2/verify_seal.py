#!/usr/bin/env python3
"""Verify the E2 seal: re-hash every sealed file against seal.json, assert the no-label files contain none of the
forbidden keys (at any nesting level) and none of the reference / gold strings.

Exact-string scan: every reference_fol and gold_fol string is searched in every field of every no-label row EXCEPT the
row's own candidate_fol/raw_output. A candidate that is character-identical to its reference is the generator's own
output, not a leak; such rows are counted and reported (candidate_identical_to_reference) rather than failed.
Exit code 0 = seal intact."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def keys_of(o, acc=None):
    acc = set() if acc is None else acc
    if isinstance(o, dict):
        for k, v in o.items():
            acc.add(k)
            keys_of(v, acc)
    elif isinstance(o, list):
        for v in o:
            keys_of(v, acc)
    return acc


def main() -> int:
    seal = json.loads((ROOT / "seal.json").read_text())
    ok = True
    for rel, meta in seal["files"].items():
        h = hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()
        if h != meta["sha256"]:
            print(f"HASH MISMATCH {rel}"); ok = False
    refs = [json.loads(l) for l in open(ROOT / "sealed/references_E2.jsonl", encoding="utf-8") if l.strip()]
    ref_by_sid = {r["sentence_id"]: {x for x in (r["reference_fol"], r["gold_fol"]) if x and len(x.strip()) >= 8} for r in refs}
    all_refs = set().union(*ref_by_sid.values()) if ref_by_sid else set()
    forb = set(seal["forbidden_keys_in_nolabel_files"])
    identical = 0
    for rel in ("candidates_E2_nolabels.jsonl", "controls_E2_nolabels.jsonl"):
        for line in open(ROOT / rel, encoding="utf-8"):
            if not line.strip():
                continue
            r = json.loads(line)
            bad = keys_of(r) & forb
            if bad:
                print(f"FORBIDDEN KEYS {rel} {r.get('row_key')}: {bad}"); ok = False
            if r.get("candidate_fol", "").strip() in ref_by_sid.get(r.get("sentence_id"), set()):
                identical += 1
            rest = json.dumps({k: v for k, v in r.items() if k not in ("candidate_fol", "raw_output")}, ensure_ascii=False)
            for s in all_refs:
                if s in rest:
                    print(f"REFERENCE STRING LEAK {rel} {r.get('row_key')}: {s[:60]}"); ok = False
                    break
    print(json.dumps({"seal_intact": ok, "candidate_identical_to_reference": identical}))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
