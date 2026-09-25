#!/usr/bin/env python3
"""Recompute both label-vector hashes from rcomp_free_labels_final.jsonl and compare with the last entry of seal.json:
sha256 of json.dumps(sorted((row_key, label))), for all rows and for untouched rows (seen_iter3 False).
usage: python results/verify_seal.py   (stdlib only)"""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def lv(rows):
    return hashlib.sha256(json.dumps(sorted((r["row_key"], r["label"]) for r in rows), ensure_ascii=False).encode()).hexdigest()


def main():
    rows = [json.loads(l) for l in (HERE / "rcomp_free_labels_final.jsonl").read_text().splitlines() if l.strip()]
    seal = json.loads((HERE / "seal.json").read_text())["seals"][-1]
    a, u = lv(rows), lv([r for r in rows if not r["seen_iter3"]])
    ok = a == seal["label_vector_sha256_all_rows"] and u == seal["label_vector_sha256_untouched"]
    print(json.dumps({"all": a, "untouched": u, "n": len(rows), "match": ok}, indent=1))
    assert ok, "label seal mismatch"


if __name__ == "__main__":
    main()
