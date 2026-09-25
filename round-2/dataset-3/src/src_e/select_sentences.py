#!/usr/bin/env python3
"""STEP 1: deterministic held-out sentence selection (sha1 ordering; no randomness).

Outputs work/sentences.json (600 rows), work/fewshot_exemplars.json (6), work/calib_sentences.json (20),
work/exclusion_log.json, prereg_strata.json (frozen here, before any metric runs).
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
import time
from collections import Counter
from pathlib import Path

from loguru import logger

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "labeller"))
sys.setrecursionlimit(10000)
from fol import parse  # noqa: E402
from complexity_counts import depth, nquant, nconds  # noqa: E402
from label_lib import equivalent_modulo_vocab  # noqa: E402

DL, W = ROOT / "data_local", ROOT / "work"
logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(ROOT / "logs" / "select.log", level="DEBUG")

TEXT_COND = re.compile(r"\b(if|when|whenever|who|that|which|whose|unless|provided|only if|as long as|in case)\b", re.I)
EXC_PATS = [("unless", r"\bunless\b"), ("except", r"\bexcept(?:ing)?\b"), ("excluding", r"\bexcluding\b"),
            ("other_than", r"\bother than\b"), ("without", r"\bwithout\b"), ("but_not", r"\bbut not\b")]
XOR_BUTNOT = re.compile(r"but not both|either\b.*\bbut not", re.I)


def norm(s: str) -> str:
    s = s.lower().replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def h(s: str) -> str:
    return hashlib.sha1(norm(s).encode()).hexdigest()


def sid(s: str) -> str:
    return hashlib.sha1(("heldout|" + norm(s)).encode()).hexdigest()[:12]


def split_sents(block: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+|\n+", block)
    return [p.strip() for p in parts if p.strip()]


def exception_type(text: str) -> str | None:
    for name, pat in EXC_PATS:
        if re.search(pat, text, re.I):
            if name == "but_not" and XOR_BUTNOT.search(text):
                continue
            return name
    return None


def load_jsonl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


def build_exclusion() -> tuple[set, dict]:
    ex, src = set(), Counter()

    def add(s, tag):
        for x in [s] + split_sents(s):
            if x.strip():
                ex.add(h(x)); src[tag] += 1
    for r in load_jsonl(ROOT / "raw/hf/tasksource__folio/folio_v2_validation.jsonl"):
        for p in r["premises"].split("\n"):
            add(p, "tasksource_folio_validation")
        add(r["conclusion"], "tasksource_folio_validation")
    for r in csv.DictReader(open(DL / "folio_refined_validation.csv")):
        for p in r["nl premises"].split("\n"):
            add(p, "folio_refined_validation")
        add(r["nl conclusion"], "folio_refined_validation")
    for f, tag in [("DSAVlab-UNIUD_FOLIO_validation-curated__FOLIO_instances.jsonl", "curated_folio"),
                   ("DSAVlab-UNIUD_MALLS_test_subset-CURATED__MALLS_instances.jsonl", "curated_malls")]:
        for r in load_jsonl(DL / f):
            add(r["NL_sentence"], tag)
    for r in json.load(open(DL / "yuan-yang__MALLS-v0__MALLS-v0.1-test.json")):
        add(r["NL"], "malls_test")
    for m in ("gpt-3.5-turbo", "gpt-4", "text-davinci-003"):
        for r in json.load(open(ROOT / f"raw/logiclm/FOLIO_dev_{m}.json")):
            add(r["context"], "logiclm_context")
            q = r["question"].split("?", 1)[-1]
            add(q, "logiclm_question")
    return ex, dict(src)


def malls_pool(ex: set) -> tuple[list, dict]:
    log = Counter()
    seen, pool = set(), []
    for r in json.load(open(DL / "yuan-yang__MALLS-v0__MALLS-v0.1-train.json")):
        log["raw"] += 1
        text, gold = r["NL"].strip(), r["FOL"].strip()
        try:
            e = parse(gold)
        except Exception:  # noqa: BLE001
            log["gold_unparseable"] += 1
            continue
        n = norm(text)
        if n in seen:
            log["dup_text"] += 1
            continue
        seen.add(n)
        if h(text) in ex:
            log["excluded_screen_hash"] += 1
            continue
        pool.append({"text": text, "reference_fol": gold, "sentence_id": sid(text), "source": "MALLS-v0.1-train",
                     "words": len(text.split()), "n_conditions": nconds(e), "n_quant": nquant(e), "depth": depth(e),
                     "text_conditions": len(TEXT_COND.findall(text)), "exception_type": exception_type(text)})
    log["pool"] = len(pool)
    return pool, dict(log)


def pick_exc(pool):
    core = sorted([r for r in pool if r["exception_type"] in ("unless", "except", "excluding", "other_than")],
                  key=lambda r: r["sentence_id"])
    out = core[:100]
    for t in ("without", "but_not"):
        if len(out) >= 100:
            break
        fill = sorted([r for r in pool if r["exception_type"] == t and r["words"] >= 15], key=lambda r: r["sentence_id"])
        out += fill[: 100 - len(out)]
    return out, {"core_available": len(core)}


def pick_binned(pool, bins, quotas):
    order = sorted(pool, key=lambda r: r["sentence_id"])
    by = [[r for r in order if lo <= r["words"] <= hi] for lo, hi in bins]
    take = [min(q, len(b)) for q, b in zip(quotas, by)]
    short = sum(quotas) - sum(take)
    i = 0
    while short > 0 and any(len(b) > t for b, t in zip(by, take)):
        j = i % len(by)
        if len(by[j]) > take[j]:
            take[j] += 1; short -= 1
        i += 1
    out = []
    for b, t in zip(by, take):
        out += b[:t]
    return out, {"bin_supply": [len(b) for b in by], "bin_taken": take, "shortfall": short}


def ctrl_pool(ex: set):
    """FOLIO-train premises paired with folio-refined train, with agreement_type."""
    ts = load_jsonl(ROOT / "raw/hf/tasksource__folio/folio_v2_train.jsonl")
    ref = list(csv.DictReader(open(DL / "yfxiao__folio-refined__train.csv")))
    refmap = {}
    for r in ref:
        nls = [s for s in r["nl premises"].split("\n") if s.strip()]
        refmap.setdefault(tuple(norm(s) for s in nls), (nls, [s for s in r["fol premises"].split("\n") if s.strip()]))
    log, seen, out = Counter(), set(), []
    for r in ts:
        nls = [s for s in r["premises"].split("\n") if s.strip()]
        fols = [s for s in r["premises-FOL"].split("\n") if s.strip()]
        key = tuple(norm(s) for s in nls)
        if key not in refmap:
            log["story_unmatched"] += 1
            continue
        rn, rf = refmap[key]
        if not (len(nls) == len(fols) == len(rn) == len(rf)):
            log["story_linecount_mismatch"] += 1
            continue
        log["story_matched"] += 1
        for t, of, ff in zip(nls, fols, rf):
            n = norm(t)
            if n in seen:
                continue
            seen.add(n)
            if h(t) in ex:
                log["excluded_screen_hash"] += 1
                continue
            if of.strip() == ff.strip():
                at = "IDENTICAL_STRING"
            else:
                try:
                    at = equivalent_modulo_vocab(parse(ff), parse(of))
                except Exception:  # noqa: BLE001
                    at = "UNPARSEABLE"
            try:
                e = parse(ff)
            except Exception:  # noqa: BLE001
                at = "UNPARSEABLE"; e = None
            log[f"agreement_{at}"] += 1
            if e is None:
                continue
            out.append({"text": t.strip(), "reference_fol": ff.strip(), "original_fol": of.strip(),
                        "sentence_id": sid(t), "source": "FOLIO-v2-train", "agreement_type": at,
                        "words": len(t.split()), "n_conditions": nconds(e), "n_quant": nquant(e), "depth": depth(e),
                        "text_conditions": len(TEXT_COND.findall(t)), "exception_type": exception_type(t)})
    return out, dict(log)


def ast_feats(f):
    e = parse(f)
    s = f
    return {"univ_cond": s.lstrip().startswith("∀") and "→" in s, "xor": "⊕" in s, "neg": "¬" in s,
            "const": bool(re.search(r"\(([a-z][a-z0-9]{2,})[,)]", s)) and not s.lstrip().startswith(("∀", "∃")),
            "nconds": nconds(e)}


def pick_fewshot(elig):
    order = sorted(elig, key=lambda r: (r["agreement_type"] == "IDENTICAL_STRING", r["sentence_id"]))
    want = [("universal_conditional", lambda r, f: f["univ_cond"] and f["nconds"] == 1 and " who " not in r["text"]),
            ("relative_clause_restrictor", lambda r, f: f["univ_cond"] and re.search(r"\b(who|that|which)\b", r["text"]) is not None),
            ("either_or_xor", lambda r, f: f["xor"] and "either" in r["text"].lower()),
            ("negation", lambda r, f: f["neg"] and not f["xor"] and re.search(r"\b(not|no|never|n't)\b", r["text"].lower()) is not None),
            ("named_individual", lambda r, f: f["const"] and not f["xor"]),
            ("two_condition_conditional", lambda r, f: f["univ_cond"] and f["nconds"] >= 2 and not f["xor"])]
    used, out = set(), []
    for name, cond in want:
        for r in order:
            if r["sentence_id"] in used or not (8 <= r["words"] <= 22):
                continue
            try:
                f = ast_feats(r["reference_fol"])
            except Exception:  # noqa: BLE001
                continue
            if cond(r, f):
                out.append({**r, "exemplar_role": name}); used.add(r["sentence_id"])
                break
    return out


def main():
    t0 = time.time()
    ex, exsrc = build_exclusion()
    logger.info(f"exclusion hashes: {len(ex)} from {exsrc}")
    pool, mlog = malls_pool(ex)
    logger.info(f"MALLS-train pool: {mlog}")
    exc, exc_log = pick_exc(pool)
    used = {r["sentence_id"] for r in exc}
    rest = [r for r in pool if r["sentence_id"] not in used]
    l25, l25_log = pick_binned([r for r in rest if r["words"] >= 25 and r["n_conditions"] >= 3],
                               [(25, 29), (30, 34), (35, 10 ** 6)], [67, 67, 66])
    used |= {r["sentence_id"] for r in l25}
    l20, l20_log = pick_binned([r for r in rest if 20 <= r["words"] <= 24 and r["n_conditions"] >= 3 and r["sentence_id"] not in used],
                               [(20, 21), (22, 22), (23, 24)], [50, 50, 50])
    for s, lab in ((exc, "EXC"), (l25, "L25"), (l20, "L20")):
        for r in s:
            r["source_stratum"] = lab
    cp, clog = ctrl_pool(ex)
    elig = [r for r in cp if r["agreement_type"] in ("IDENTICAL_STRING", "EQ", "VOCAB", "GRAN")]
    logger.info(f"CTRL pool: {clog}; eligible {len(elig)}")
    fews = pick_fewshot(elig)
    assert len(fews) == 6, [f["exemplar_role"] for f in fews]
    fs_ids = {f["sentence_id"] for f in fews}
    elig = [r for r in elig if r["sentence_id"] not in fs_ids]
    order = sorted(elig, key=lambda r: (r["agreement_type"] == "IDENTICAL_STRING", r["sentence_id"]))
    bins = [(0, 11, 50), (12, 19, 60), (20, 10 ** 6, 40)]
    by = [[r for r in order if lo <= r["words"] <= hi] for lo, hi, _ in bins]
    take = [min(q, len(b)) for (_, _, q), b in zip(bins, by)]
    short = 150 - sum(take)
    for j in (1, 0):
        extra = min(short, len(by[j]) - take[j]); take[j] += extra; short -= extra
    ctrl = []
    for (lo, hi, _), b, t in zip(bins, by, take):
        for r in b[:t]:
            r["source_stratum"] = "CTRL"; r["ctrl_len_bin"] = f"{lo}-{hi if hi < 10**6 else 'inf'}"
            ctrl.append(r)
    ctrl_ids = {r["sentence_id"] for r in ctrl}
    # calibration sentences: CTRL-pool TRUSTED_AGREED premises not used in CTRL or exemplars; 10 with >=15 words
    rem = [r for r in order if r["sentence_id"] not in ctrl_ids and r["agreement_type"] != "IDENTICAL_STRING"]
    rem += [r for r in order if r["sentence_id"] not in ctrl_ids and r["agreement_type"] == "IDENTICAL_STRING"]
    long_ = [r for r in rem if r["words"] >= 15][:10]
    short_ = [r for r in rem if r["words"] < 15 and r["words"] >= 7][:10]
    calib = long_ + short_
    sents = exc + l25 + l20 + ctrl
    ids = [r["sentence_id"] for r in sents]
    assert len(ids) == len(set(ids)) == 600, (len(ids), len(set(ids)))
    for r in sents:
        r["reference_status_initial"] = "MALLS_GPT4_GOLD" if r["source"].startswith("MALLS") else "TRUSTED_AGREED_PENDING_AUDIT"
        r.setdefault("agreement_type", None)
    coll = sum(h(r["text"]) in ex for r in sents + fews + calib)
    W.mkdir(exist_ok=True)
    (W / "sentences.json").write_text(json.dumps(sents, ensure_ascii=False, indent=1))
    (W / "fewshot_exemplars.json").write_text(json.dumps(fews, ensure_ascii=False, indent=1))
    (W / "calib_sentences.json").write_text(json.dumps(calib, ensure_ascii=False, indent=1))
    exlog = {"exclusion_hash_count": len(ex), "exclusion_sources": exsrc, "malls_pool": mlog, "ctrl_pool": clog,
             "ctrl_eligible_after_fewshot": len(elig), "exc": exc_log, "l25": l25_log, "l20": l20_log,
             "ctrl_bins_taken": take, "ctrl_shortfall": short, "hash_collisions_with_screen_after_exclusion": coll,
             "exc_type_counts": dict(Counter(r["exception_type"] for r in exc)),
             "ctrl_agreement_counts": dict(Counter(r["agreement_type"] for r in ctrl))}
    (W / "exclusion_log.json").write_text(json.dumps(exlog, indent=1))
    prereg = {
        "frozen_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "frozen_before": "any candidate generation, labelling or metric run",
        "strata": {
            "EXC": "MALLS-train; all parseable unless/except/excluding/other-than items (sha1-ordered, cap 100), filled with 'without' then non-XOR 'but not' items with >=15 words",
            "L25": ">=25 words and n_conditions>=3 (gold-derived nconds), even over word bins 25-29/30-34/>=35",
            "L20": "20-24 words and n_conditions>=3, even over bins 20-21/22/23-24",
            "CTRL": "FOLIO-v2-train premises where tasksource original gold ≡ folio-refined (IDENTICAL_STRING/EQ/VOCAB/GRAN); reference = refined; bins <12/12-19/>=20 words; non-identical agreement preferred"},
        "counts": {"EXC": len(exc), "L25": len(l25), "L20": len(l20), "CTRL": len(ctrl)},
        "exclusion": {"hash_count": len(ex), "collisions_after_exclusion": coll},
        "testability_rule": "A stratum is TESTABLE only if, using tier A+B final labels only (CONTESTED excluded), it has >=50 ERROR rows AND >=50 CORRECT rows AND >=25 distinct sentences contributing ERROR rows AND >=25 distinct sentences contributing CORRECT rows. Declared per stratum after labelling, before any metric runs.",
        "top_up_rule": "If after Step 3 the tier-A-projected ERROR or CORRECT count of L25 is below 60, generate one more sha1-ordered batch of 100 L25 sentences with the 5 cheapest generator slots, budget permitting.",
        "testability_declaration": None}
    (ROOT / "prereg_strata.json").write_text(json.dumps(prereg, indent=1))
    logger.info(f"done in {time.time()-t0:.0f}s: {prereg['counts']}; fewshot {[f['exemplar_role'] for f in fews]}; calib {len(calib)}; collisions {coll}")
    logger.info(json.dumps(exlog))


if __name__ == "__main__":
    main()
