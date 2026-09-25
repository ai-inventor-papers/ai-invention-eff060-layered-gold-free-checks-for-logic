#!/usr/bin/env python3
"""S6 / S8: testability declaration, written BEFORE any score of the condition is computed or joined.

SIG : primary pool = 10 few-shot SIG rows labelled CORRECT or ERROR (results/sig_labels.jsonl).
FREE: primary pool = tiers A+B rows labelled CORRECT or ERROR, excluding CONTESTED / reading_choice / REF_FLAGGED /
      UNRESOLVED (results/free_labels.jsonl); also an A-only count.
Rule (pre-registered): TESTABLE iff >= 50 CORRECT and >= 50 ERROR rows, each over >= 25 distinct sentences.
Per-stratum (word tercile, clause type, template) AUROCs are reported only where >= 30/30 (descriptive).
Writes results/testability_<COND>.json (the guard file every scorer checks) and merges into results/testability.json.

usage: testability.py SIG [--topup]  |  testability.py FREE
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results"
RC = ROOT / "rcomp"
FEW = {"G1", "G1b", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9"}


def jl(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.exists() else []


def word_terciles(sents: dict) -> dict:
    ws = sorted(s["words"] for s in sents.values() if s["batch"] == "main")
    c1, c2 = ws[len(ws) // 3], ws[2 * len(ws) // 3]
    return {"cut_1": c1, "cut_2": c2, "rule": "T1: words < cut_1; T2: cut_1 <= words < cut_2; T3: words >= cut_2 (main sentences)"}


def tercile(w: int, cuts: dict) -> str:
    return "W1" if w < cuts["cut_1"] else ("W2" if w < cuts["cut_2"] else "W3")


def summarise(pool: list[dict], all_rows: list[dict], sents: dict, cuts: dict, label_key: str = "label") -> dict:
    n = Counter(r[label_key] for r in pool)
    sc = {lab: len({r["sentence_id"] for r in pool if r[label_key] == lab}) for lab in ("CORRECT", "ERROR")}
    vec = sorted((r["row_key"], r[label_key]) for r in pool)
    strata = {}
    for name, fn in (("word_tercile", lambda r: tercile(sents[r["sentence_id"]]["words"], cuts)),
                     ("clause_type", lambda r: sents[r["sentence_id"]]["clause_type"]),
                     ("template_id", lambda r: sents[r["sentence_id"]]["template_id"]),
                     ("nconds_weak", lambda r: str(sents[r["sentence_id"]]["nconds_weak"]))):
        d = defaultdict(Counter)
        for r in pool:
            d[fn(r)][r[label_key]] += 1
        strata[name] = {k: {"CORRECT": v["CORRECT"], "ERROR": v["ERROR"], "reportable_30_30": v["CORRECT"] >= 30 and v["ERROR"] >= 30}
                        for k, v in sorted(d.items())}
    return {"n_CORRECT": n["CORRECT"], "n_ERROR": n["ERROR"], "sentences_with_CORRECT": sc["CORRECT"],
            "sentences_with_ERROR": sc["ERROR"], "n_sentences_in_pool": len({r["sentence_id"] for r in pool}),
            "label_counts_all_rows": dict(Counter(r[label_key] for r in all_rows)),
            "per_template_counts": {t: dict(Counter(r[label_key] for r in pool if sents[r["sentence_id"]]["template_id"] == t))
                                    for t in sorted({sents[r["sentence_id"]]["template_id"] for r in pool})},
            "strata": strata, "sha256_label_vector": hashlib.sha256(json.dumps(vec).encode()).hexdigest(),
            "verdict": "TESTABLE" if (n["CORRECT"] >= 50 and n["ERROR"] >= 50 and sc["CORRECT"] >= 25 and sc["ERROR"] >= 25)
            else "NOT_TESTABLE"}


def merge(cond: str, rec: dict) -> None:
    p = RES / "testability.json"
    d = json.loads(p.read_text()) if p.exists() else {}
    d[cond] = rec
    p.write_text(json.dumps(d, indent=1))


def declare_sig(topup: bool) -> dict:
    sents = {s["sentence_id"]: s for s in json.loads((RC / "work" / "rcomp_sentences.json").read_text())}
    cuts = word_terciles(sents)
    rows = [r for r in jl(RES / "sig_labels.jsonl") if r["slot"] in FEW]
    if not topup:
        rows = [r for r in rows if sents[r["sentence_id"]]["batch"] == "main"]
    pool = [r for r in rows if r["label"] in ("CORRECT", "ERROR")]
    rec = {"condition": "SIG", "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "topup": topup,
           "primary_pool_rule": "10 few-shot SIG rows labelled CORRECT or ERROR (pure z3 labels); OFF_SIGNATURE, UNKNOWN, "
                                "READING_CHOICE, UNPARSEABLE excluded and counted",
           "word_terciles": cuts, **summarise(pool, rows, sents, cuts)}
    parse_ok = [r for r in rows if r["parse_ok"]]
    rec["off_signature_share_of_parseable"] = sum(r["off_signature"] for r in parse_ok) / max(1, len(parse_ok))
    rec["F3_triggered"] = rec["off_signature_share_of_parseable"] > 0.5
    rec["loose_view_counts"] = dict(Counter(r["label_loose"] for r in rows))
    return rec


def declare_free() -> dict:
    sents = {s["sentence_id"]: s for s in json.loads((RC / "work" / "rcomp_sentences.json").read_text())}
    cuts = word_terciles(sents)
    rows = [r for r in jl(RES / "free_labels.jsonl")]
    few = [r for r in rows if r["slot"] in FEW and r["prompt_variant"] == "fewshot_v1"]
    ok = lambda r: (r["label"] in ("CORRECT", "ERROR") and r.get("label_tier") in ("A", "B") and not r.get("reading_choice")
                    and not r.get("ref_flagged"))
    pool_all = [r for r in rows if ok(r)]
    pool_few = [r for r in few if ok(r)]
    rec = {"condition": "FREE", "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "primary_pool_rule": "tiers A+B, CORRECT/ERROR, excluding CONTESTED, reading_choice, REF_FLAGGED, UNRESOLVED; "
                                "all FREE candidate rows (few-shot + zero-shot); the few-shot-only pool is reported alongside",
           "word_terciles": cuts, **summarise(pool_all, rows, sents, cuts),
           "few_shot_only": {k: v for k, v in summarise(pool_few, few, sents, cuts).items() if k != "strata"},
           "tier_A_only": {k: v for k, v in summarise([r for r in pool_all if r["label_tier"] == "A"], rows, sents, cuts).items()
                           if k != "strata"},
           "tier_counts": dict(Counter(f"{r['label']}:{r.get('label_tier')}" for r in rows))}
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cond", choices=["SIG", "FREE"])
    ap.add_argument("--topup", action="store_true")
    a = ap.parse_args()
    rec = declare_sig(a.topup) if a.cond == "SIG" else declare_free()
    (RES / f"testability_{a.cond}.json").write_text(json.dumps(rec, indent=1))
    merge(a.cond, rec)
    print(json.dumps({k: rec[k] for k in ("verdict", "n_CORRECT", "n_ERROR", "sentences_with_CORRECT", "sentences_with_ERROR",
                                          "label_counts_all_rows", "sha256_label_vector")}, indent=1))


if __name__ == "__main__":
    sys.exit(main())
