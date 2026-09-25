#!/usr/bin/env python3
"""STEP 3 end / 4c: stratified sha1 selection of R_COMP sentences.

  preselect  -> work/rcomp_preselect.json: the set sent to fluency rating + reference audit
               (main pool: 1.15 x the per-template quota, usage cap 4 = the pool capacity ~276; reserve pool: 130 T1/T2/T7,
               separate usage cap 6)
  final      -> work/rcomp_sentences.json (250 main + 100 TOP-UP RESERVE, flagged topup_batch/reserve)
               drops fluency < 3 and REF_FLAGGED sentences and lexicon entries implicated in >= 2 flags;
               sentences whose fluency / audit has not run yet are kept with status PENDING.
Quotas: T8 ('but only if') 25 (<= 10%), T1 29, every other template 28; round-robin over word bins 25-29 / 30-34 / >=35.
Usage cap: every lexicon entry appears in <= 4 main sentences (and, separately, <= 4 reserve sentences:
the lexicon's non-sortal capacity, ~1,636 slots, is below 350 x 5).
"""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict

from common import RAW, W, dump, load_jsonl, setup_logger

QUOTA = {"T1": 29, "T2": 28, "T3": 28, "T4": 28, "T5": 28, "T6": 28, "T7": 28, "T8": 25, "T9": 28}
BINS = ["25-29", "30-34", ">=35"]
RESERVE_T = ("T1", "T2", "T7")


def greedy(pool: list[dict], quota: dict, cap: int, usage: Counter | None = None) -> list[dict]:
    usage = usage if usage is not None else Counter()
    by = {t: {b: sorted([r for r in pool if r["template_id"] == t and r["word_bin"] == b], key=lambda r: r["sentence_id"])
              for b in BINS} for t in quota}
    ptr = {t: {b: 0 for b in BINS} for t in quota}
    taken = {t: Counter() for t in quota}
    out = []
    progress = True
    while progress:
        progress = False
        for t in quota:
            if sum(taken[t].values()) >= quota[t]:
                continue
            for b in sorted(BINS, key=lambda b: (taken[t][b], BINS.index(b))):
                lst = by[t][b]
                got = False
                while ptr[t][b] < len(lst):
                    r = lst[ptr[t][b]]; ptr[t][b] += 1
                    if all(usage[x] < cap for x in r["lexicon_ids"]):
                        for x in r["lexicon_ids"]:
                            usage[x] += 1
                        out.append(r); taken[t][b] += 1; got = True
                        break
                if got:
                    progress = True
                    break
    return out


def status_maps():
    """fluency: sentence_id -> rating; audit: sentence_id -> {flagged, verdicts} (from the LLM phase caches)."""
    flu, aud = {}, {}
    for r in load_jsonl(RAW / "fluency_items.jsonl"):
        flu[r["sentence_id"]] = r
    for r in load_jsonl(RAW / "ref_audit_items.jsonl"):
        aud[r["sentence_id"]] = r
    return flu, aud


def preselect(logger):
    pool = json.loads((W / "rcomp_pool.json").read_text())
    main = greedy(pool, {t: round(q * 1.15) for t, q in QUOTA.items()}, cap=4)
    ids = {r["sentence_id"] for r in main}
    rest = [r for r in pool if r["sentence_id"] not in ids and r["template_id"] in RESERVE_T and not r["nested"]]
    res = greedy(rest, {"T1": 44, "T2": 43, "T7": 43}, cap=6)
    for r in main:
        r["preselect_pool"] = "main"
    for r in res:
        r["preselect_pool"] = "reserve"
    dump(W / "rcomp_preselect.json", main + res)
    logger.info(f"preselect main {len(main)} {dict(Counter(r['template_id'] for r in main))}; reserve {len(res)}")


def final(logger):
    pre = json.loads((W / "rcomp_preselect.json").read_text())
    flu, aud = status_maps()
    log = Counter()
    flag_count = Counter()
    for r in pre:
        f = flu.get(r["sentence_id"])
        r["fluency"] = f["rating"] if f else None
        r["fluency_status"] = "RATED" if f else "PENDING"
        a = aud.get(r["sentence_id"])
        r["audit_status"] = "AUDITED" if a else "PENDING"
        r["ref_flagged"] = bool(a and a["ref_flagged"])
        r["audit_verdicts"] = a["verdicts"] if a else None
        if r["ref_flagged"]:
            for x in r["lexicon_ids"]:
                flag_count[x] += 1
    bad_lex = {x for x, n in flag_count.items() if n >= 2}
    elig = []
    for r in pre:
        if r["fluency"] is not None and r["fluency"] < 3:
            log["drop_fluency_lt3"] += 1; continue
        if r["ref_flagged"]:
            log["drop_ref_flagged"] += 1; continue
        if set(r["lexicon_ids"]) & bad_lex:
            log["drop_lexicon_implicated_2flags"] += 1; continue
        elig.append(r)
    main = greedy([r for r in elig if r["preselect_pool"] == "main"], QUOTA, cap=4)
    mids = {r["sentence_id"] for r in main}
    rest = [r for r in elig if r["sentence_id"] not in mids and r["template_id"] in RESERVE_T and not r["nested"]]
    res = greedy(rest, {"T1": 34, "T2": 33, "T7": 33}, cap=4)
    for r in main:
        r["topup_batch"] = False; r["batch"] = "main"
    for r in res:
        r["topup_batch"] = True; r["batch"] = "reserve"
    out = main + res
    log.update({"main": len(main), "reserve": len(res), "bad_lexicon_entries": len(bad_lex),
                "main_per_template": dict(Counter(r["template_id"] for r in main)),
                "main_per_bin": dict(Counter(r["word_bin"] for r in main)),
                "main_per_group": dict(Counter(r["sort_group"] for r in main)),
                "fluency_pending": sum(r["fluency_status"] == "PENDING" for r in out),
                "audit_pending": sum(r["audit_status"] == "PENDING" for r in out)})
    usage = Counter(x for r in main for x in r["lexicon_ids"])
    log["max_usage_main"] = max(usage.values())
    dump(W / "rcomp_sentences.json", out)
    dump(W / "select_log.json", dict(log))
    logger.info(json.dumps(dict(log)))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["preselect", "final"])
    a = ap.parse_args()
    lg = setup_logger("select")
    preselect(lg) if a.cmd == "preselect" else final(lg)
