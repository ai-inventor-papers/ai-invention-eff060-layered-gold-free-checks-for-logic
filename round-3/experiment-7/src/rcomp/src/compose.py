#!/usr/bin/env python3
"""STEP 3: deterministic composition (sha1-seeded) of R_COMP candidate sentences from lexicon.json.

Over-generates K per template, then applies the pre-registered filters IN ORDER, logging each count:
  words >= 25 -> nconds(weak) >= 3 -> >= 2 non-sortal restrictor atoms -> z3 non-trivial (weak neither valid nor
  unsat; weak not equivalent to strong; no VACUOUS atom in weak or strong) -> no screen hash collision -> no string dup.
Composition constraints (per sentence): conditions from >= 2 distinct source rules; Q, E/P from rules different from each
other; no predicate twice; unique (sorted conditions, Q, E/P). The per-entry usage cap (<= 4 sentences) is enforced at
selection time (select.py) on the chosen set.
Output: work/rcomp_pool.json (all survivors with provenance) and work/compose_log.json.
"""
from __future__ import annotations

import argparse
import json
import multiprocessing as mp
import random
from collections import Counter
from concurrent.futures import ProcessPoolExecutor

from common import ROOT, W, dump, sha1, setup_logger

K_PER_TEMPLATE = 600


def slot(e: dict, neg: bool = False) -> dict:
    return {"atom": e["atom_final"], "pred": e["pred_final"], "vp": e["vp_sg_pos"], "neg_vp": e["vp_sg_neg"],
            "neg": neg, "lexicon_id": e["lexicon_id"], "rule_id": e["rule_id"]}


STOPW = set("a an the is are be been has have had does do can cannot not no of in on at to for from by with as and or its their".split())


def content_stems(vp: str) -> set:
    import re
    from nltk.stem import PorterStemmer
    ps = PorterStemmer()
    return {ps.stem(w) for w in re.findall(r"[a-z]+", vp.lower()) if w not in STOPW}


def overlap(a: set, b: set) -> bool:
    """Guard against semantically dependent atoms inside one sentence: subset or Jaccard >= 0.5 of content stems."""
    if not a or not b:
        return False
    return a <= b or b <= a or len(a & b) / len(a | b) >= 0.5


def compose_one(t: str, i: int, lex: dict, groups: list[str], byid: dict):
    from templates import fill, USES_E
    rng = random.Random(int(sha1(f"rcomp|{t}|{i}"), 16))
    g = "person" if t == "T7" else rng.choices(groups, weights=[len(lex[s]["nonsortal"]) for s in groups])[0]
    ns = lex[g]["nonsortal"]
    noun_e = rng.choice(lex[g]["sortal"]) if t != "T7" else None
    used_preds = {noun_e["pred_final"]} if noun_e else set()
    pick = []
    used_stems = [content_stems(noun_e["vp_sg_pos"])] if noun_e else []
    for _ in range(60):
        e = rng.choice(ns)
        if e["pred_final"] in used_preds or any(e["vp_sg_pos"] == p["vp_sg_pos"] for p in pick):
            continue
        st = content_stems(e["vp_sg_pos"])
        if any(overlap(st, u) for u in used_stems):
            continue  # near-duplicate meanings (attends the conference / attends the conference remotely)
        used_stems.append(st)
        pick.append(e); used_preds.add(e["pred_final"])
        if len(pick) == 5:
            break
    if len(pick) < 5:
        return None, "pick_fail"
    conds, Qe, Xe = pick[:3], pick[3], pick[4]
    if any(e.get("audit") == "WRONG" for e in pick + ([noun_e] if noun_e else [])):
        return None, "lexicon_audit_wrong"  # rejection (not removal) keeps every other sentence identical
    if len({c["rule_id"] for c in conds}) < 2:
        return None, "conds_one_rule"
    if Qe["rule_id"] == Xe["rule_id"]:
        return None, "QX_same_rule"
    neg_pos = rng.randrange(3) if rng.random() < 0.45 else None
    C = [slot(c, neg=(k == neg_pos)) for k, c in enumerate(conds)]
    v = rng.randrange(2)
    N = noun_e["noun"] if noun_e else None
    S = noun_e["atom_final"] if noun_e else None
    r = fill(t, v, N, S, C, slot(Qe), slot(Xe), person=(g == "person"))
    if r is None:
        return None, "plural_fail"
    r.update({"sort_group": g, "sentence_seed": sha1(f"rcomp|{t}|{i}"), "compose_index": i,
              "noun_lexicon_id": noun_e["lexicon_id"] if noun_e else None,
              "condition_lexicon_ids": [c["lexicon_id"] for c in C], "negated_condition": neg_pos,
              "Q_lexicon_id": Qe["lexicon_id"], ("E_lexicon_id" if t in USES_E else "P_lexicon_id"): Xe["lexicon_id"],
              "lexicon_ids": ([noun_e["lexicon_id"]] if noun_e else []) + [c["lexicon_id"] for c in C] + [Qe["lexicon_id"], Xe["lexicon_id"]],
              "source_rule_ids": sorted({byid[x]["rule_id"] for x in ([noun_e["lexicon_id"]] if noun_e else []) + [c["lexicon_id"] for c in C] + [Qe["lexicon_id"], Xe["lexicon_id"]]}),
              "combo_key": "|".join(sorted(c["atom"] for c in C)) + "#" + Qe["atom_final"] + "#" + Xe["atom_final"]})
    return r, "ok"


def z3_checks(r: dict) -> dict:
    """Worker: complexity counts + z3 non-triviality + profile (VACUOUS) on weak and strong readings."""
    import common  # noqa: F401 - sets sys.path in the spawned worker
    import z3
    from fol import parse, preds, mkpred, to_z3, valid, equivalent, profile
    from complexity_counts import nconds, nquant, depth
    out = {}
    w, s = parse(r["reference_fol_weak"]), parse(r["reference_fol_strong"])
    out["nconds_weak"], out["nquant"], out["depth_weak"] = nconds(w), nquant(w), depth(w)
    P = {q: mkpred(q, m) for q, m in preds(w).items()}
    zw = to_z3(w, {}, P)
    out["weak_valid"], out["weak_unsat"] = valid(zw), valid(z3.Not(zw))
    out["weak_eq_strong"] = equivalent(w, s)
    pw, ps = profile(w), profile(s)
    out["profile_weak"], out["profile_strong"] = pw, ps
    out["vacuous"] = "VACUOUS" in pw.values() or "VACUOUS" in ps.values() or "UNKNOWN" in pw.values()
    return out


def restrictor_nonsortal(r: dict) -> int:
    """Non-sortal atoms in the restrictor (antecedent) of the weak reading, excluding the sortal atom."""
    from templates import USES_P
    n = 3  # the three conditions are always restrictor literals
    if r["template_id"] == "T3":
        n += 1  # the proviso atom P sits in the antecedent of the weak reading
    return n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--k", type=int, default=K_PER_TEMPLATE)
    a = ap.parse_args()
    logger = setup_logger("compose")
    import select_sentences as ss
    from templates import TEMPLATES
    L = json.loads((ROOT / "lexicon.json").read_text())
    byid = {e["lexicon_id"]: e for e in L["entries"]}
    groups = [g for g, v in L["groups"].items() if v["usable"]]
    lex = {g: {"sortal": sorted([e for e in L["entries"] if e["subject_sort"] == g and e["sortal"]], key=lambda e: e["lexicon_id"]),
               "nonsortal": sorted([e for e in L["entries"] if e["subject_sort"] == g and not e["sortal"]], key=lambda e: e["lexicon_id"])}
           for g in groups}
    logger.info(f"usable groups {groups}: " + ", ".join(f"{g} {len(v['sortal'])}/{len(v['nonsortal'])}" for g, v in lex.items()))
    log = Counter()
    cands = []
    for t in TEMPLATES:
        for i in range(a.k):
            r, why = compose_one(t, i, lex, groups, byid)
            log[f"compose_{why}"] += 1
            if r is not None:
                cands.append(r)
    log["composed"] = len(cands)
    # filter 1: words
    cands = [r for r in cands if len(r["text"].split()) >= 25]
    log["f1_words_ge25"] = len(cands)
    ex, _ = ss.build_exclusion()
    with ProcessPoolExecutor(max_workers=4, mp_context=mp.get_context("spawn")) as pool:
        res = list(pool.map(z3_checks, cands, chunksize=16))
    for r, z in zip(cands, res):
        r.update(z)
    cands = [r for r in cands if r["nconds_weak"] >= 3]
    log["f2_nconds_ge3"] = len(cands)
    cands = [r for r in cands if restrictor_nonsortal(r) >= 2]
    log["f3_restrictor_nonsortal_ge2"] = len(cands)
    cands = [r for r in cands if r["weak_valid"] is False and r["weak_unsat"] is False and r["weak_eq_strong"] is False
             and not r["vacuous"]]
    log["f4_z3_nontrivial"] = len(cands)
    cands = [r for r in cands if ss.h(r["text"]) not in ex]
    log["f5_no_screen_collision"] = len(cands)
    seen_t, seen_c, out = set(), set(), []
    for r in sorted(cands, key=lambda r: r["sentence_seed"]):
        n = ss.norm(r["text"])
        if n in seen_t or r["combo_key"] in seen_c:
            log["dup_dropped"] += 1; continue
        seen_t.add(n); seen_c.add(r["combo_key"])
        r["sentence_id"] = sha1("rcomp|" + n)[:12]
        r["words"] = len(r["text"].split())
        r["word_bin"] = "25-29" if r["words"] <= 29 else ("30-34" if r["words"] <= 34 else ">=35")
        r["exception_type"] = ss.exception_type(r["text"])
        r["text_conditions"] = len(ss.TEXT_COND.findall(r["text"]))
        out.append(r)
    log["f6_no_dup"] = len(out)
    log["per_template"] = dict(Counter(r["template_id"] for r in out))
    log["per_group"] = dict(Counter(r["sort_group"] for r in out))
    log["per_word_bin"] = dict(Counter(r["word_bin"] for r in out))
    dump(W / "rcomp_pool.json", out)
    dump(W / "compose_log.json", dict(log))
    logger.info(json.dumps(dict(log)))


if __name__ == "__main__":
    main()
