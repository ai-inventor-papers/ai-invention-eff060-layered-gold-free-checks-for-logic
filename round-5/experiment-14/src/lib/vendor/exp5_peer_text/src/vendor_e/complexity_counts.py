"""How many gold-labelled sentence-level NL->FOL items exist per complexity stratum?
Answers review critique 4 (SARA infeasible) BEFORE any spend: counts long / heavily conditioned items
with sentence-level gold FOL in MALLS-v0.1 train+test, FOLIO-refined train+validation premises/conclusions,
and the curated FOLIO/MALLS sets. Complexity: words, quantifiers, max nesting depth, #conditions
(atoms in the antecedent of the main implication(s)), #exception markers in the text."""
import csv, json, re, sys
from collections import Counter, defaultdict
from pathlib import Path
from fol import parse

D = Path(__file__).resolve().parent.parent / "data_local"
EXC = re.compile(r"\b(unless|except|other than|excluding|but not|without|provided that|as long as|only if|however)\b", re.I)


def depth(e):
    if e[0] == "atom":
        return 0
    if e[0] in ("all", "ex"):
        return depth(e[2])
    if e[0] == "not":
        return 1 + depth(e[1])
    return 1 + max(depth(e[1]), depth(e[2]))


def nquant(e):
    if e[0] == "atom":
        return 0
    if e[0] in ("all", "ex"):
        return 1 + nquant(e[2])
    if e[0] == "not":
        return nquant(e[1])
    return nquant(e[1]) + nquant(e[2])


def natoms(e):
    if e[0] == "atom":
        return 1
    if e[0] in ("all", "ex"):
        return natoms(e[2])
    if e[0] == "not":
        return natoms(e[1])
    return natoms(e[1]) + natoms(e[2])


def nconds(e):
    """atoms inside antecedents of implications (restrictor / condition slots)"""
    if e[0] == "atom":
        return 0
    if e[0] in ("all", "ex"):
        return nconds(e[2])
    if e[0] == "not":
        return nconds(e[1])
    if e[0] == "imp":
        return natoms(e[1]) + nconds(e[2])
    return nconds(e[1]) + nconds(e[2])


def items():
    for r in json.load(open(D / "yuan-yang__MALLS-v0__MALLS-v0.1-train.json")):
        yield "MALLS-train", r["NL"], r["FOL"]
    for r in json.load(open(D / "yuan-yang__MALLS-v0__MALLS-v0.1-test.json")):
        yield "MALLS-test", r["NL"], r["FOL"]
    for split in ("train", "validation"):
        fn = D / ("yfxiao__folio-refined__train.csv" if split == "train" else "folio_refined_validation.csv")
        seen = set()
        for r in csv.DictReader(open(fn)):
            nls = [s for s in r["nl premises"].split("\n") if s.strip()]
            fols = [s for s in r["fol premises"].split("\n") if s.strip()]
            if len(nls) == len(fols):
                for n, f in zip(nls, fols):
                    if n not in seen:
                        seen.add(n)
                        yield f"FOLIOref-{split}-prem", n, f
            if r["nl conclusion"] not in seen:
                seen.add(r["nl conclusion"])
                yield f"FOLIOref-{split}-concl", r["nl conclusion"], r["fol conclusion"]


def main():
    agg = defaultdict(Counter)
    for src, nl, fol in items():
        a = agg[src]
        a["n"] += 1
        w = len(nl.split())
        try:
            e = parse(fol)
        except Exception:
            a["parse_fail"] += 1
            continue
        q, d, c, x = nquant(e), depth(e), nconds(e), len(EXC.findall(nl))
        a["parsed"] += 1
        a["words>=20"] += w >= 20
        a["words>=25"] += w >= 25
        a["words>=30"] += w >= 30
        a["conds>=3"] += c >= 3
        a["quant>=2"] += q >= 2
        a["depth>=4"] += d >= 4
        a["exception_marker"] += x >= 1
        a["LONG&COND(w>=20,conds>=3)"] += (w >= 20 and c >= 3)
        a["LONG&COND(w>=25,conds>=3)"] += (w >= 25 and c >= 3)
        a["exception&w>=15"] += (x >= 1 and w >= 15)
    for s, a in agg.items():
        print(s, dict(a))


if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    main()
