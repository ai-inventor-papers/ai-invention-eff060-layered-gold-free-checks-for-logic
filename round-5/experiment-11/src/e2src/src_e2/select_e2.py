#!/usr/bin/env python3
"""E2 STEP 1: sentence pools, exclusion, 12-gram filter, census and deterministic E2 selection ($0, no LLM).

Reuses dataset E's frozen selection functions (src/select_sentences.py: build_exclusion, malls_pool, exception_type,
norm, h, sid) byte-identical, and ADDS the E2 rules of the plan:
  * exclusion = E's hash exclusion + E's 700 sentences + E's calibration sentences + every screen text + FOLIO-v2-train
    + E's few-shot exemplars; any candidate sharing a lowercase word 12-gram with an E sentence is dropped; within E2
    only the first (E2 order) of two sentences sharing a 12-gram is kept.
  * E2 order = sha1('E2_v1|' + sentence_id) (sentence_id = E's recipe sha1('heldout|'+norm(text))[:12]).
  * L25: MALLS-train, >=25 words and gold n_conditions >=3; long bin (>=30 words) gets min(supply, 45% of target).
  * EXC: pre-registered ladder (a) MALLS-train core markers, (b) MALLS-test non-curated core markers >=15 words,
    (c) MALLS-train 'without' >=15 words, (d) non-XOR 'but not' >=15 words (train, then test).
  * DT: ProverQA dev (easy/medium/hard) nl2fol + question->conclusion_fol units, deduped by text and by
    entity-abstracted skeleton, inclusion ladder (>=15w,>=2c) -> (>=12w,>=2c) -> (>=15w,>=1c).
Outputs: work/pool_E2.json (ranked pools incl. surplus/reserve), work/sentences.json (ACTIVE set), census_E2.json,
exclusion_log_E2.json.  Usage: select_e2.py [--l25 350] [--exc 100] [--dt 100]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import types
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "labeller"))
sys.setrecursionlimit(10000)
import select_sentences as ss  # noqa: E402  (E's frozen selection code; configures its own loguru sinks)
from fol import parse, equivalent  # noqa: E402
from complexity_counts import depth, nquant, nconds  # noqa: E402
from disguise import emit  # noqa: E402
from loguru import logger  # noqa: E402

W = ROOT / "work"
E_DIR = Path("/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_dataset_1")
SCREEN = Path("/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/screen_items.json")
PQA = ROOT / "raw" / "hf" / "opendatalab__ProverQA" / "dev"
PQA_REV = "e2561beed450272690da658d21ae667570dbbafc"
SEED = "E2_v1|"
CORE = ("unless", "except", "excluding", "other_than")
Q_PREFIX = "Based on the above information, is the following statement true, false, or uncertain? "


def e2key(sentence_id: str) -> str:
    return hashlib.sha1((SEED + sentence_id).encode()).hexdigest()


def grams12(text: str) -> set:
    t = ss.norm(text).split()
    return {" ".join(t[i:i + 12]) for i in range(len(t) - 11)}


def build_exclusion_without_malls_test() -> tuple[set, dict]:
    """E's build_exclusion with the MALLS-test source suppressed (for EXC pool (b) only). Implemented by handing E's
    function a json shim whose load() returns [] for the MALLS-test file; E's code itself is not modified."""
    real = ss.json

    def load(fp, *a, **k):
        if "MALLS-v0.1-test" in getattr(fp, "name", ""):
            return []
        return real.load(fp, *a, **k)
    ss.json = types.SimpleNamespace(load=load, loads=real.loads, dumps=real.dumps, dump=real.dump)
    try:
        return ss.build_exclusion()
    finally:
        ss.json = real


def extra_exclusion_texts() -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    e_sents = json.loads((E_DIR / "work" / "sentences.json").read_text())
    e_top = json.loads((E_DIR / "work" / "sentences_topup.json").read_text())
    out["E_700_sentences"] = [s["text"] for s in e_sents] + [s["text"] for s in e_top]
    out["E_calib_sentences"] = [s["text"] for s in json.loads((E_DIR / "work" / "calib_sentences.json").read_text())]
    out["E_fewshot_exemplars"] = [s["text"] for s in json.loads((E_DIR / "work" / "fewshot_exemplars.json").read_text())]
    out["screen_items"] = [it["text"] for it in json.loads(SCREEN.read_text())]
    fol_tr = []
    for r in ss.load_jsonl(ROOT / "raw/hf/tasksource__folio/folio_v2_train.jsonl"):
        fol_tr += [p for p in r["premises"].split("\n") if p.strip()] + [r["conclusion"]]
    out["folio_v2_train"] = fol_tr
    return out


def crosscheck_E_heldout(e_texts: set) -> dict:
    """Cross-check E's 700 against the heldout_sentences group of E/full_data_out.json (27.7 MB)."""
    d = json.loads((E_DIR / "full_data_out.json").read_text())
    grp = next(g for g in d["datasets"] if g["dataset"] == "heldout_sentences")
    fdo = {ss.norm(json.loads(x["input"])["text"]) for x in grp["examples"]}
    return {"n_full_data_out_heldout_sentences": len(fdo), "n_work_sentences": len(e_texts),
            "identical_sets": fdo == e_texts, "only_in_full_data_out": len(fdo - e_texts), "only_in_work": len(e_texts - fdo)}


def feats(text: str, fol: str, e) -> dict:
    return {"words": len(text.split()), "n_conditions": nconds(e), "n_quant": nquant(e), "depth": depth(e),
            "text_conditions": len(ss.TEXT_COND.findall(text)), "exception_type": ss.exception_type(text)}


def malls_test_pool(ex_nomt: set) -> tuple[list, dict]:
    log, seen, pool = Counter(), set(), []
    for r in json.load(open(ROOT / "data_local" / "yuan-yang__MALLS-v0__MALLS-v0.1-test.json")):
        log["raw"] += 1
        text, gold = r["NL"].strip(), r["FOL"].strip()
        try:
            e = parse(gold)
        except Exception:  # noqa: BLE001
            log["gold_unparseable"] += 1
            continue
        n = ss.norm(text)
        if n in seen:
            log["dup_text"] += 1
            continue
        seen.add(n)
        if ss.h(text) in ex_nomt:
            log["excluded_hash_noncurated_rule"] += 1
            continue
        pool.append({"text": text, "reference_fol": gold, "sentence_id": ss.sid(text), "source": "MALLS-v0.1-test", **feats(text, gold, e)})
    log["pool"] = len(pool)
    return pool, dict(log)


def constants(e, bound=frozenset()) -> set:
    k = e[0]
    if k == "atom":
        return {a for a in e[2] if a not in bound}
    if k in ("all", "ex"):
        return constants(e[2], bound | {e[1]})
    if k == "not":
        return constants(e[1], bound)
    return constants(e[1], bound) | constants(e[2], bound)


def dt_units() -> tuple[list, dict]:
    log, seen, units = Counter(), set(), []
    for diff in ("easy", "medium", "hard"):
        for r in json.load(open(PQA / f"{diff}.json")):
            pairs = [(t, f, "context") for t, f in r["nl2fol"].items()]
            q = r["question"]
            if q.startswith(Q_PREFIX):
                q = q[len(Q_PREFIX):]
            pairs.append((q, r["conclusion_fol"], "conclusion"))
            for text, fol, role in pairs:
                log[f"units_{diff}"] += 1
                text, fol = text.strip(), fol.strip()
                n = ss.norm(text)
                if n in seen:
                    log["dup_text"] += 1
                    continue
                seen.add(n)
                try:
                    e = parse(fol)
                    e2 = parse(emit(e))
                    if equivalent(e, e2) is not True:
                        raise ValueError("round-trip not z3-equivalent")
                except Exception as ex:  # noqa: BLE001
                    log["gold_parse_or_roundtrip_fail"] += 1
                    logger.debug(f"DT drop {text[:60]!r}: {ex}")
                    continue
                consts = sorted(constants(e))
                sk = text
                for c in consts:
                    sk = re.sub(rf"\b{re.escape(c)}\b", "ENT", sk)
                    sk = re.sub(rf"\b{re.escape(c.replace('_', ' '))}\b", "ENT", sk)
                sk = ss.norm(sk)
                either = "either" in text.lower()
                notboth = re.search(r"not both|but not", text, re.I) is not None
                flag = None
                if either and "⊕" in fol and not notboth:
                    flag = "XOR_OR_source"
                elif either and notboth and "⊕" not in fol:
                    flag = "XOR_OR_source"
                units.append({"text": text, "reference_fol": fol, "sentence_id": ss.sid(text), "source": f"ProverQA-dev-{diff}",
                              "proverqa_problem_id": r["id"], "proverqa_role": role, "skeleton": sk, "constants": consts,
                              "convention_flag": flag, **feats(text, fol, e)})
    log["units_parseable_unique"] = len(units)
    return units, dict(log)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--l25", type=int, default=350)
    ap.add_argument("--l25-max", type=int, default=450)
    ap.add_argument("--exc", type=int, default=100)
    ap.add_argument("--dt", type=int, default=100)
    a = ap.parse_args()

    # ---- exclusion ----
    ex_all, exsrc = ss.build_exclusion()
    ex_nomt, exsrc_nomt = build_exclusion_without_malls_test()
    extra = extra_exclusion_texts()
    extra_counts = {}
    for tag, texts in extra.items():
        hs = {ss.h(t) for t in texts}
        ex_all |= hs
        ex_nomt |= hs
        extra_counts[tag] = len(hs)
    e_norm = {ss.norm(t) for t in extra["E_700_sentences"]}
    xcheck = crosscheck_E_heldout(e_norm)
    e_grams = set()
    for t in extra["E_700_sentences"]:
        e_grams |= grams12(t)

    # ---- pools ----
    train_pool, tlog = ss.malls_pool(ex_all)
    test_pool, mlog = malls_test_pool(ex_nomt)
    train_ids = {r["sentence_id"] for r in train_pool}
    test_pool = [r for r in test_pool if r["sentence_id"] not in train_ids]
    dt_pool, dlog = dt_units()
    dt_pool = [r for r in dt_pool if ss.h(r["text"]) not in ex_all]
    drop12 = Counter()

    def ok12(r, tag):
        if grams12(r["text"]) & e_grams:
            drop12[tag] += 1
            return False
        return True
    train_pool = [r for r in train_pool if ok12(r, "malls_train")]
    test_pool = [r for r in test_pool if ok12(r, "malls_test")]
    dt_pool = [r for r in dt_pool if ok12(r, "proverqa")]
    for r in train_pool + test_pool + dt_pool:
        r["e2_key"] = e2key(r["sentence_id"])
    srt = lambda xs: sorted(xs, key=lambda r: r["e2_key"])  # noqa: E731

    accepted_grams: set = set()
    within12 = Counter()

    def take(rows, n, tag, used):
        out = []
        for r in rows:
            if len(out) >= n:
                break
            if r["sentence_id"] in used:
                continue
            g = grams12(r["text"])
            if g & accepted_grams:
                within12[tag] += 1
                continue
            accepted_grams.update(g)
            used.add(r["sentence_id"])
            out.append(r)
        return out

    used: set = set()
    # ---- EXC ladder ----
    exc_pools = {
        "a_malls_train_core": srt([r for r in train_pool if r["exception_type"] in CORE]),
        "b_malls_test_noncurated_core": srt([r for r in test_pool if r["exception_type"] in CORE and r["words"] >= 15]),
        "c_malls_train_without": srt([r for r in train_pool if r["exception_type"] == "without" and r["words"] >= 15]),
        "d_but_not_nonxor": srt([r for r in train_pool if r["exception_type"] == "but_not" and r["words"] >= 15])
        + srt([r for r in test_pool if r["exception_type"] == "but_not" and r["words"] >= 15]),
    }
    exc = []
    exc_taken = {}
    for name, rows in exc_pools.items():
        got = take(rows, a.exc - len(exc), f"EXC_{name}", used)
        for r in got:
            r["exc_pool"] = name
        exc_taken[name] = len(got)
        exc += got
    for i, r in enumerate(exc):
        r["source_stratum"] = "EXC"; r["e2_rank"] = i

    # ---- L25 (from MALLS-train minus EXC) ----
    l25_all = srt([r for r in train_pool if r["words"] >= 25 and r["n_conditions"] >= 3 and r["sentence_id"] not in used])
    short = [r for r in l25_all if r["words"] <= 29]
    long_ = [r for r in l25_all if r["words"] >= 30]

    def l25_for(target):
        nl = min(len(long_), round(0.45 * target))
        return nl, target - nl
    nl_base, ns_base = l25_for(a.l25)
    nl_max, ns_max = l25_for(a.l25_max)
    base = take(long_, nl_base, "L25", used) + take(short, ns_base, "L25", used)
    surplus = take(long_, nl_max - nl_base, "L25", used) + take(short, ns_max - ns_base, "L25", used)
    base, surplus = srt(base), srt(surplus)
    for i, r in enumerate(base + surplus):
        r["source_stratum"] = "L25"; r["e2_rank"] = i; r["l25_tier"] = "base" if i < len(base) else "surplus"
        r["word_bin"] = "30-34" if r["words"] >= 30 else "25-29"

    # ---- DT ladder (one sentence per skeleton) ----
    rungs = [("r1_ge15w_ge2c", lambda r: r["words"] >= 15 and r["n_conditions"] >= 2),
             ("r2_ge12w_ge2c", lambda r: r["words"] >= 12 and r["n_conditions"] >= 2),
             ("r3_ge15w_ge1c", lambda r: r["words"] >= 15 and r["n_conditions"] >= 1)]
    census_dt = {}
    for diff in ("easy", "medium", "hard"):
        sub = [r for r in dt_pool if r["source"].endswith(diff)]
        census_dt[diff] = {name: {"units": sum(f(r) for r in sub), "skeletons": len({r["skeleton"] for r in sub if f(r)})} for name, f in rungs}
    need = int(a.dt * 1.1)  # +10% reserve
    dt, skel_used, rung_taken = [], set(), {}
    for name, f in rungs:
        cnt = 0
        for r in srt([r for r in dt_pool if f(r)]):
            if len(dt) >= need:
                break
            if r["skeleton"] in skel_used:
                continue
            got = take([r], 1, "DT", used)
            if got:
                skel_used.add(r["skeleton"]); got[0]["dt_rung"] = name; dt.append(got[0]); cnt += 1
        rung_taken[name] = cnt
        if len(dt) >= need:
            break
    for i, r in enumerate(dt):
        r["source_stratum"] = "DT"; r["e2_rank"] = i; r["dt_tier"] = "base" if i < a.dt else "reserve"

    allrows = exc + base + surplus + dt
    for r in allrows:
        r["source_dataset"] = "ProverQA" if r["source"].startswith("ProverQA") else r["source"]
        r["reference_status_initial"] = "PROVERQA_PROVER_GOLD" if r["source"].startswith("ProverQA") else "MALLS_GPT4_GOLD"
        r.setdefault("agreement_type", None)
        r.setdefault("convention_flag", None)
    ids = [r["sentence_id"] for r in allrows]
    assert len(ids) == len(set(ids))
    assert not ({r["sentence_id"] for r in allrows} & {ss.sid(t) for t in extra["E_700_sentences"]})
    coll_E = sum(ss.norm(r["text"]) in e_norm for r in allrows)
    coll_12 = sum(bool(grams12(r["text"]) & e_grams) for r in allrows)
    assert coll_E == 0 and coll_12 == 0

    active = exc + base + [r for r in dt if r["dt_tier"] == "base"]
    W.mkdir(exist_ok=True)
    (W / "pool_E2.json").write_text(json.dumps({"EXC": exc, "L25": base + surplus, "DT": dt}, ensure_ascii=False, indent=1))
    (W / "sentences.json").write_text(json.dumps(active, ensure_ascii=False, indent=1))
    exlog = {"E_build_exclusion_hashes": len(ss.build_exclusion()[0]), "E_build_exclusion_sources": exsrc,
             "noncurated_rule_sources (MALLS-test suppressed, for EXC pool b)": exsrc_nomt,
             "added_exclusion_texts": extra_counts, "E_heldout_crosscheck": xcheck,
             "twelvegram_dropped_vs_E": dict(drop12), "twelvegram_dropped_within_E2": dict(within12),
             "malls_train_pool": tlog, "malls_test_pool": mlog, "proverqa_units": dlog,
             "final_collisions_with_E_text": coll_E, "final_12gram_collisions_with_E": coll_12}
    (ROOT / "exclusion_log_E2.json").write_text(json.dumps(exlog, indent=1))
    census = {
        "seed_string": SEED, "order": "sha1('E2_v1|' + sentence_id)",
        "malls": {"L25_supply_after_filters": {"25-29": len(short), ">=30": len(long_), ">=35": sum(r["words"] >= 35 for r in long_)},
                  "L25_targets": {"base": a.l25, "max_with_surplus": a.l25_max, "base_long_short": [nl_base, ns_base], "max_long_short": [nl_max, ns_max]},
                  "L25_selected": {"base": len(base), "surplus_reserve": len(surplus)},
                  "EXC_pool_supply": {k: len(v) for k, v in exc_pools.items()}, "EXC_taken_per_pool": exc_taken,
                  "EXC_type_counts": dict(Counter(r["exception_type"] for r in exc)),
                  "EXC_core_marker_share": round(sum(r["exception_type"] in CORE for r in exc) / max(1, len(exc)), 3)},
        "dt": {"primary_source": "opendatalab/ProverQA (dev easy/medium/hard)", "hf_revision": PQA_REV,
               "construction": "ProverGen: LLM-verbalised text over Prover9-validated FOL; nl2fol maps every context sentence to FOL",
               "controlled_templates": "yes", "license": "not stated on the HF card (the ProverGen GitHub repo is the reference; treat as research-use)",
               "train_split": "train/provergen-5000.json is instruction-tuning format (system/instruction/input/output) with no nl2fol dict; not used",
               "census_per_difficulty": census_dt, "rung_taken": rung_taken, "selected": len(dt),
               "selected_base": sum(r["dt_tier"] == "base" for r in dt), "reserve": sum(r["dt_tier"] == "reserve" for r in dt),
               "distinct_skeletons_selected": len({r["skeleton"] for r in dt}),
               "convention_flag_XOR_OR_source": sum(r["convention_flag"] == "XOR_OR_source" for r in dt),
               "difficulty_counts": dict(Counter(r["source"] for r in dt)),
               "secondary_census": {"hitachi-nlp/FLD.v2": "not needed (ProverQA rung 1 alone exceeds 100 skeletons); abstract predicate symbols would make tier A impossible",
                                    "tasksource/LogicNLI": "no FOL shipped (premise/hypothesis/label only) -> rejected",
                                    "rejected_unverified_llm_gold": ["ProofFOL (GPT-4o on ProofWriter)", "NL2FOL (Lalwani 2024)", "jhkim64/NL2FOL_sentence (7 downloads, FOLIO-overlapping LLM FOL)", "MALLS-like corpora"],
                                    "reason": "gold must be trusted by construction or audited"}},
        "active_counts": dict(Counter(r["source_stratum"] for r in active)),
        "licences": {"MALLS-v0.1": "CC-BY-NC-4.0 (yuan-yang/MALLS-v0)", "ProverQA": "as stated on opendatalab/ProverQA (no licence field on the card)"}}
    (ROOT / "census_E2.json").write_text(json.dumps(census, indent=1))
    logger.info(f"E2 selection: active {census['active_counts']}; L25 supply {census['malls']['L25_supply_after_filters']}; "
                f"EXC {exc_taken}; DT rungs {rung_taken}; 12-gram drops {dict(drop12)} within {dict(within12)}; xcheck {xcheck}")


if __name__ == "__main__":
    main()
