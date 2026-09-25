#!/usr/bin/env python3
"""STEP 1: source atom pool (work/source_rules.json). Deterministic, $0.

Sources, in priority order:
  (a) dataset E heldout_sentences with reference_status TRUSTED_AGREED / GOLD_PANEL_OK;
  (b) ctrl_pool(): FOLIO-v2-train premises whose tasksource and folio-refined formulas agree
      (IDENTICAL_STRING / EQ / VOCAB), minus E's 6 few-shot exemplars;
  (c) fallback (flag --malls): MALLS-train sentences with <= 15 words.
Every source text is screened against E's exclusion hashes (build_exclusion); collisions must be 0.
From each formula we keep only atoms over the rule's single universally quantified variable:
unary P(v), or binary P(v, c) / P(c, v) with a lowercase constant c.
"""
from __future__ import annotations

import argparse
import json
import re

from common import E_DIR, W, ROOT, dump, sha1
import select_sentences as ss  # noqa: E402  (E's code, verbatim)
from common import setup_logger
from fol import parse  # noqa: E402

logger = setup_logger("source_pool")
LOWER_CONST = re.compile(r"^[a-z][A-Za-z0-9_]*$")


def top_rule(e):
    """Return (var, body) if e is ∀v body (single outer universal); else None."""
    if e[0] != "all":
        return None
    return e[1], e[2]


def bound_in(e, acc=None):
    acc = set() if acc is None else acc
    if e[0] in ("all", "ex"):
        acc.add(e[1]); bound_in(e[2], acc)
    elif e[0] == "not":
        bound_in(e[1], acc)
    elif e[0] != "atom":
        bound_in(e[1], acc); bound_in(e[2], acc)
    return acc


def collect(e, role, out, pol=True):
    """Walk and record (atom, role, positive?) with role in restrictor/consequent/other."""
    k = e[0]
    if k == "atom":
        out.append((e, role, pol)); return
    if k in ("all", "ex"):
        collect(e[2], "other", out, pol); return
    if k == "not":
        collect(e[1], role, out, not pol); return
    if k == "imp" and role == "top":
        collect(e[1], "restrictor", out, pol); collect(e[2], "consequent", out, pol); return
    if k == "and" and role in ("restrictor", "consequent", "top"):
        r = "consequent" if role == "top" else role
        collect(e[1], r, out, pol); collect(e[2], r, out, pol); return
    collect(e[1], "other", out, pol); collect(e[2], "other", out, pol)


def literal(e):
    return e[0] == "atom" or (e[0] == "not" and e[1][0] == "atom")


def conj(e):
    return conj(e[1]) + conj(e[2]) if e[0] == "and" else [e]


def shaped(body) -> bool:
    """∀x (L1 [∧ L2 [∧ L3]] → L)."""
    return body[0] == "imp" and all(literal(x) for x in conj(body[1])) and len(conj(body[1])) <= 3 and literal(body[2])


def extract(text: str, fol: str, src: str, rid_prefix: str) -> dict | None:
    try:
        e = parse(fol)
    except Exception:  # noqa: BLE001 - parser raises assorted errors on junk
        return None
    tr = top_rule(e)
    if tr is None:
        return None
    v, body = tr
    other_bound = bound_in(body)
    acc = []
    collect(body, "top", acc)
    atoms, seen = [], set()
    for a, role, pol in acc:
        args = a[2]
        if any(x in other_bound for x in args):
            continue
        if len(args) == 1 and args[0] == v:
            key = f"{a[1]}(x)"
            const = None
        elif len(args) == 2 and v in args and sum(x == v for x in args) == 1:
            c = args[1] if args[0] == v else args[0]
            if not LOWER_CONST.match(c) or len(c) < 2:
                continue
            key = f"{a[1]}(x, {c})" if args[0] == v else f"{a[1]}({c}, x)"
            const = c
        else:
            continue
        if key in seen:
            continue
        seen.add(key)
        atoms.append({"atom": key, "pred": a[1], "arity": len(args), "const": const,
                      "const_pos": None if const is None else (1 if args[1] == const else 0),
                      "role": role, "polarity_in_source": "pos" if pol else "neg"})
    if not atoms:
        return None
    return {"rule_id": f"{rid_prefix}_{sha1(src + '|' + ss.norm(text))[:10]}", "source": src, "text": text.strip(),
            "fol": fol.strip(), "var": v, "shaped": shaped(body), "atoms": atoms}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--malls", action="store_true", help="also build the MALLS-train fallback pool")
    a = ap.parse_args()
    ex, exsrc = ss.build_exclusion()
    logger.info(f"exclusion hashes {len(ex)} {exsrc}")
    fews = json.loads((W / "e_fewshot_exemplars.json").read_text())
    few_ids = {ss.norm(f["text"]) for f in fews}
    d = json.loads((E_DIR / "full_data_out.json").read_text())
    hs = [g for g in d["datasets"] if g["dataset"] == "heldout_sentences"][0]["examples"]
    rules, log = [], {"a_rows": 0, "b_rows": 0, "c_rows": 0, "screen_collisions": 0, "fewshot_excluded": 0,
                      "no_atoms_or_not_universal": 0, "dup_text": 0}
    seen = set()

    def add(text, fol, src, pref, extra):
        n = ss.norm(text)
        if n in seen:
            log["dup_text"] += 1; return
        if ss.h(text) in ex:
            log["screen_collisions"] += 1; return
        if n in few_ids:
            log["fewshot_excluded"] += 1; return
        r = extract(text, fol, src, pref)
        if r is None:
            log["no_atoms_or_not_universal"] += 1; return
        seen.add(n)
        r.update(extra)
        rules.append(r)

    for x in hs:
        if x["output"] in ("TRUSTED_AGREED", "GOLD_PANEL_OK"):
            inp = json.loads(x["input"])
            log["a_rows"] += 1
            add(inp["text"], inp["reference_fol"], "E_heldout_" + x["output"], "a",
                {"priority": 0, "e_sentence_id": x["metadata_sentence_id"], "reference_status": x["output"]})
    cp, clog = ss.ctrl_pool(ex)
    logger.info(f"ctrl_pool log {clog}")
    for r in sorted(cp, key=lambda r: r["sentence_id"]):
        if r["agreement_type"] in ("IDENTICAL_STRING", "EQ", "VOCAB"):
            log["b_rows"] += 1
            add(r["text"], r["reference_fol"], "FOLIO-v2-train_agreed", "b",
                {"priority": 1, "agreement_type": r["agreement_type"]})
    if a.malls:
        for r in json.loads((ROOT / "data_local" / "yuan-yang__MALLS-v0__MALLS-v0.1-train.json").read_text()):
            if len(r["NL"].split()) <= 15:
                log["c_rows"] += 1
                add(r["NL"], r["FOL"], "MALLS-train_fallback", "c", {"priority": 2})
    # order: priority, shaped first, then sha1(rule_id)
    rules.sort(key=lambda r: (r["priority"], not r["shaped"], sha1(r["rule_id"])))
    coll = sum(ss.h(r["text"]) in ex for r in rules)
    assert coll == 0
    log.update({"rules": len(rules), "shaped": sum(r["shaped"] for r in rules),
                "by_source": {s: sum(r["source"] == s for r in rules) for s in {r["source"] for r in rules}},
                "atoms_total": sum(len(r["atoms"]) for r in rules), "collisions_final": coll,
                "exclusion_hash_count": len(ex), "exclusion_sources": exsrc})
    out = W / ("source_rules_malls.json" if a.malls else "source_rules.json")
    dump(out, rules)
    dump(W / ("source_pool_log_malls.json" if a.malls else "source_pool_log.json"), log)
    logger.info(json.dumps(log))


if __name__ == "__main__":
    main()
