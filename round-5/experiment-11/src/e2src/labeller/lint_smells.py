"""Step-0 probe: TEXT-FREE formula 'smells' (lint rules) on real errors vs verified-correct gold.

Idea (static analysis / bug-pattern mining, e.g. FindBugs, Getafix): some formulas are improbable renderings of ANY
English sentence, so they can be flagged without reading the text. Each smell is a deterministic check:
  EX_IMP      ∃x (A → B)                      existential with an implication body (almost always meant ∃x(A ∧ B))
  ALL_AND     ∀x (A(x) ∧ B(x)) with >=2 atoms  universal with a pure conjunction body (restriction→conjunction)
  IFF_RESTR   ∀x (A ∧ B ↔ C)                  biconditional whose left side is a conjunction: restrictor trapped in ↔
  GLUE        >=2 universal vars in one block that never share an atom (independent claims glued)
  FREE        free variable (lower-case single-letter argument not bound)
  VACUOUS     a predicate the formula's truth does not depend on (z3 monotonicity profile = VACUOUS; vacuity detection)
  TRIVIAL     formula is valid or unsatisfiable (z3)
  ARITY       same predicate name used with two arities
  DANGLING    a universally quantified variable that occurs in exactly one atom, in the consequent only
Reports firing rate on corrected (verified) gold = false alarms, and on ORIGINAL formulas of real non-equivalent pairs
(by repair-census class) = sensitivity; plus paired contrast (fires on original but not on corrected).
"""
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import z3

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fol import parse, profile, connectivity_flags, prenex_blocks, to_z3, mkpred, preds, valid  # noqa: E402

D = Path(__file__).resolve().parent.parent / "data_local"


def walk(e, bv=frozenset(), parent=None):
    yield e, bv, parent
    k = e[0]
    if k in ("all", "ex"):
        yield from walk(e[2], bv | {e[1]}, e)
    elif k == "not":
        yield from walk(e[1], bv, e)
    elif k != "atom":
        yield from walk(e[1], bv, e)
        yield from walk(e[2], bv, e)


def natoms(e):
    return sum(1 for x, _, _ in walk(e) if x[0] == "atom")


def body_of(e):
    while e[0] in ("all", "ex"):
        e = e[2]
    return e


def smells(e):
    out = set()
    ar = defaultdict(set)
    for x, bv, par in walk(e):
        k = x[0]
        if k == "ex" and body_of(x)[0] == "imp":
            out.add("EX_IMP")
        if k == "all" and (par is None or par[0] != "all"):
            b = body_of(x)
            if b[0] == "and" and natoms(b) >= 2 and all(y[0] != "imp" for y, _, _ in walk(b)):
                out.add("ALL_AND")
            if b[0] == "iff" and b[1][0] == "and":
                out.add("IFF_RESTR")
        if k == "atom":
            ar[x[1]].add(len(x[2]))
            for a in x[2]:
                if re.fullmatch(r"[a-z]", a) and a not in bv:
                    out.add("FREE")
    if any(len(v) > 1 for v in ar.values()):
        out.add("ARITY")
    for part in prenex_blocks(e):
        vs, b = [], part
        while b[0] == "all":
            vs.append(b[1]); b = b[2]
        if len(vs) >= 2 and connectivity_flags(part):
            out.add("GLUE")
        if b[0] == "imp" and vs:
            ant = {a for y, _, _ in walk(b[1]) if y[0] == "atom" for a in y[2]}
            cnt = Counter(a for y, _, _ in walk(b) if y[0] == "atom" for a in y[2])
            if any(v not in ant and cnt[v] == 1 for v in vs):
                out.add("DANGLING")
    try:
        pr = profile(e, ms=1500)
        if any(v == "VACUOUS" for v in pr.values()):
            out.add("VACUOUS")
        P = {q: mkpred(q, m) for q, m in preds(e).items()}
        F = to_z3(e, {}, P)
        if valid(F, 1500) is True or valid(z3.Not(F), 1500) is True:
            out.add("TRIVIAL")
    except Exception:
        pass
    return out


def load(p):
    return [json.loads(l) for l in open(p) if l.strip()]


def items():
    for r in load(D / "DSAVlab-UNIUD_MALLS_test_subset-CURATED__MALLS_instances.jsonl"):
        yield "MALLS", r["id"], r["FOL_sentence_old"], r["FOL_sentence_new"]
    for r in load(D / "DSAVlab-UNIUD_FOLIO_validation-curated__FOLIO_instances.jsonl"):
        if not str(r["id"]).startswith("story"):
            yield "FOLIO-concl", r["id"], r["FOL_sentence_old"], r["FOL_sentence"]


def main():
    census = {(r["src"], r["id"]): r["cls"] for r in json.loads(Path(__file__).with_name("repair_census.rows.json").read_text())}
    fa, n_ok = Counter(), 0
    sens = defaultdict(Counter)
    nerr = Counter()
    for src, iid, old, new in items():
        try:
            ne = parse(new)
        except Exception:
            continue
        sn = smells(ne)
        n_ok += 1
        for s in sn:
            fa[s] += 1
        fa["ANY"] += bool(sn)
        cls = census.get((src, iid))
        if cls is None:
            continue
        g = "VOCAB/GRAN" if cls in ("VOCAB", "GRAN") else "ERROR"
        try:
            so = smells(parse(old))
        except Exception:
            continue
        nerr[g] += 1
        for s in so - sn:
            sens[g][s] += 1
        sens[g]["ANY(new smell on original, absent on corrected)"] += bool(so - sn)
        sens[g]["ANY(on original)"] += bool(so)
    print(f"verified-correct gold formulas: {n_ok}")
    for s, v in fa.most_common():
        print(f"  false-alarm {s:10s} {v:3d} ({v/n_ok:.3f})")
    for g in sens:
        print(f"== real non-equivalent pairs, class {g}: n={nerr[g]}")
        for s, v in sens[g].most_common():
            print(f"  {s:50s} {v:3d} ({v/nerr[g]:.2f})")


if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    main()
