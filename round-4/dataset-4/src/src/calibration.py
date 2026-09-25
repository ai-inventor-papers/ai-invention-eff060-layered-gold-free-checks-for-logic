#!/usr/bin/env python3
"""STEP 4a: synthetic known-label calibration set (80 items on 20 TRUSTED_AGREED sentences).

Per sentence: 2 UNFAITHFUL typed perturbations of the reference (one at a DOWN site, one at an UP site when both exist;
operators cycle over NEG / REV / QUANT / DROP / ADD / SWAP), each z3-verified NON-equivalent; 1 STRICT faithful
rewrite (conjunct reorder / De Morgan / contrapositive / prenex / variable rename, cycling) z3-verified EQUIVALENT; and
1 predicate-rename (naming-convention change: 'Is'+P for unary, 'Has'+P otherwise; WordNet synonyms were tried
and rejected because first senses changed meaning) = known VOCAB.
Site polarity: syntactic (antecedent of → and ¬ flip; sites under ↔/⊕ are skipped); for atom-level edits it is
cross-checked against fol.profile (z3 monotonicity) and both are recorded.
Output: work/calibration_items.json
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "labeller"))
sys.setrecursionlimit(10000)
from fol import parse, equivalent, profile  # noqa: E402
from repair_census import subterms, replace, symbols  # noqa: E402
from disguise import emit  # noqa: E402

UNF_OPS = ["NEG", "REV", "QUANT", "DROP", "ADD", "SWAP"]
STRICT = ["REORDER", "DEMORGAN", "CONTRAPOSITIVE", "PRENEX", "VARRENAME"]
STRICT_FALLBACK = ["DOUBLENEG"]


def polarity(e, path):
    sign, x = 1, e
    for i in path:
        k = x[0]
        if k in ("iff", "xor"):
            return None
        if k == "not":
            sign = -sign
        if k == "imp" and i == 1:
            sign = -sign
        x = x[i]
    return "UP" if sign == 1 else "DOWN"


def perturbations(e, foreign_pred):
    out = []
    for path, node, scope in subterms(e):
        pol = polarity(e, path)
        if pol is None:
            continue
        k = node[0]
        if k == "atom":
            out.append(("NEG", replace(e, path, ("not", node)), pol, node[1]))
            args = node[2]
            if len(args) >= 2 and args[0] != args[1]:
                out.append(("SWAP", replace(e, path, ("atom", node[1], (args[1], args[0]) + args[2:])), pol, node[1]))
            if scope and foreign_pred:
                out.append(("ADD", replace(e, path, ("and", node, ("atom", foreign_pred, (scope[-1],)))), pol, node[1]))
        if k in ("all", "ex"):
            out.append(("QUANT", replace(e, path, ("ex" if k == "all" else "all", node[1], node[2])), pol, None))
        if k == "imp":
            out.append(("REV", replace(e, path, ("imp", node[2], node[1])), pol, None))
        if k == "and":
            out.append(("DROP", replace(e, path, node[1]), pol, None))
            out.append(("DROP", replace(e, path, node[2]), pol, None))
    return out


def strict_rewrite(e, kind):
    paths = list(subterms(e))
    if kind == "REORDER":
        for p, n, _ in paths:
            if n[0] in ("and", "or"):
                return replace(e, p, (n[0], n[2], n[1]))
    if kind == "DEMORGAN":
        for p, n, _ in paths:
            if n[0] == "not" and n[1][0] in ("and", "or"):
                a, b = n[1][1], n[1][2]
                return replace(e, p, ("or" if n[1][0] == "and" else "and", ("not", a), ("not", b)))
        for p, n, _ in paths:
            if n[0] == "and":
                return replace(e, p, ("not", ("or", ("not", n[1]), ("not", n[2]))))
    if kind == "CONTRAPOSITIVE":
        for p, n, _ in paths:
            if n[0] == "imp":
                return replace(e, p, ("imp", ("not", n[2]), ("not", n[1])))
    if kind == "PRENEX":
        # ∀x (A → ∀y B)  =>  ∀x ∀y (A → B) when y not free in A;  (∀x A) ∧ B => ∀x (A ∧ B) when x not free in B
        for p, n, _ in paths:
            if n[0] == "imp" and n[2][0] in ("all", "ex") and not _free(n[1], n[2][1]):
                q = n[2]
                return replace(e, p, (q[0], q[1], ("imp", n[1], q[2])))
            if n[0] == "and" and n[1][0] in ("all", "ex") and not _free(n[2], n[1][1]):
                q = n[1]
                return replace(e, p, (q[0], q[1], ("and", q[2], n[2])))
    if kind == "DOUBLENEG":
        return ("not", ("not", e))
    if kind == "VARRENAME":
        for p, n, _ in paths:
            if n[0] in ("all", "ex"):
                return replace(e, p, (n[0], "w", _subst(n[2], n[1], "w")))
    return None


def _free(e, v):
    k = e[0]
    if k == "atom":
        return v in e[2]
    if k in ("all", "ex"):
        return False if e[1] == v else _free(e[2], v)
    if k == "not":
        return _free(e[1], v)
    return _free(e[1], v) or _free(e[2], v)


def _subst(e, v, w):
    k = e[0]
    if k == "atom":
        return ("atom", e[1], tuple(w if a == v else a for a in e[2]))
    if k in ("all", "ex"):
        return e if e[1] == v else (k, e[1], _subst(e[2], v, w))
    if k == "not":
        return ("not", _subst(e[1], v, w))
    return (k, _subst(e[1], v, w), _subst(e[2], v, w))


def synonym_rename(e):
    import nltk
    nltk.data.path.insert(0, str(ROOT / "nltk_data"))
    from nltk.corpus import wordnet as wn
    from disguise import name_tokens
    preds, _ = symbols(e)
    pmap = {}
    from disguise import KEEP
    for name, ar in preds:
        toks = name_tokens(name)
        head = toks[-1] if toks else name
        new = None
        syns = wn.synsets(head.lower(), pos=wn.NOUN)
        if False:  # WordNet first-sense synonyms proved meaning-changing (Band->Set, Club->Nine, Lost->Doomed): disabled
            for lem in syns[0].lemma_names():  # first noun sense of a base-form noun head: meaning-preserving
                if "_" not in lem and lem.lower() != head.lower() and lem.isalpha():
                    new = lem[:1].upper() + lem[1:]
                    break
        if new:
            pmap[(name, ar)] = "".join(toks[:-1]) + new
        else:  # meaning-neutral naming-convention change
            pmap[(name, ar)] = ("Is" if ar == 1 else "Has") + name
    def ren(x):
        k = x[0]
        if k == "atom":
            return ("atom", pmap[(x[1], len(x[2]))], x[2])
        if k in ("all", "ex"):
            return (k, x[1], ren(x[2]))
        if k == "not":
            return ("not", ren(x[1]))
        return (k, ren(x[1]), ren(x[2]))
    return ren(e), {f"{k[0]}/{k[1]}": v for k, v in pmap.items()}


def main():
    sents = json.loads((ROOT / "work" / "calib_sentences.json").read_text())
    unary = []
    for s in sents:
        for (n, ar) in symbols(parse(s["reference_fol"]))[0]:
            if ar == 1:
                unary.append((s["sentence_id"], n))
    items, log = [], {"down": 0, "up": 0}
    # pass 0: verified perturbations per sentence, by polarity
    ver = []
    for si, s in enumerate(sents):
        e = parse(s["reference_fol"])
        foreign = next((n for sid, n in unary if sid != s["sentence_id"] and n not in {p[0] for p in symbols(e)[0]}), None)
        perts = sorted(perturbations(e, foreign), key=lambda t: (UNF_OPS.index(t[0]) - si) % 6)
        seen_ops = {}
        for lab, c, pol, pred in perts:
            k2 = (lab, pol, 1) if (lab, pol, 0) in seen_ops else (lab, pol, 0)
            if k2 in seen_ops:
                continue
            if equivalent(c, e, ms=3000) is False:
                seen_ops[k2] = (lab, c, pol, pred)
        ver.append(list(seen_ops.values()))
    pick = [[] for _ in sents]
    for si, v in enumerate(ver):  # pass 1: one DOWN if available
        d = [x for x in v if x[2] == "DOWN"]
        pick[si].append(d[0] if d else (v[0] if v else None))
    n_down = sum(1 for p in pick if p[0] and p[0][2] == "DOWN")
    for si, v in enumerate(ver):  # pass 2: second item; DOWN while the global DOWN count is < 20
        first = pick[si][0]
        rest = [x for x in v if first is None or x[0] != first[0]] or [x for x in v if x is not first]
        want = "DOWN" if n_down < 20 else "UP"
        cand = [x for x in rest if x[2] == want] or rest
        if cand:
            pick[si].append(cand[0]); n_down += cand[0][2] == "DOWN"
        pick[si] = [x for x in pick[si] if x]
    for si, s in enumerate(sents):
        e = parse(s["reference_fol"])
        foreign = next((n for sid, n in unary if sid != s["sentence_id"] and n not in {p[0] for p in symbols(e)[0]}), None)
        prof = profile(e, ms=2000)
        perts = perturbations(e, foreign)
        seed = int(hashlib.sha1(s["sentence_id"].encode()).hexdigest()[:8], 16)
        chosen = pick[si]
        for lab, c, pol, pred in chosen:
            items.append({"sentence_id": s["sentence_id"], "text": s["text"], "reference_fol": s["reference_fol"],
                          "variant_fol": emit(c), "gold": "UNFAITHFUL", "variant_type": lab, "position": pol,
                          "position_z3_profile": next((v for k, v in prof.items() if pred and k.startswith(pred + "/")), None),
                          "z3_verified": "NONEQUIVALENT"})
        kinds = STRICT[si % 5:] + STRICT[:si % 5] + STRICT_FALLBACK
        for kind in kinds:
            r = strict_rewrite(e, kind)
            if r is not None and r != e and equivalent(r, e, ms=3000) is True:
                items.append({"sentence_id": s["sentence_id"], "text": s["text"], "reference_fol": s["reference_fol"],
                              "variant_fol": emit(r), "gold": "FAITHFUL", "variant_type": f"STRICT_{kind}", "position": None,
                              "z3_verified": "EQUIVALENT"})
                break
        rn, pmap = synonym_rename(e)
        items.append({"sentence_id": s["sentence_id"], "text": s["text"], "reference_fol": s["reference_fol"],
                      "variant_fol": emit(rn), "gold": "FAITHFUL", "variant_type": "RENAME_SYNONYM", "position": None,
                      "rename_map": pmap, "z3_verified": "VOCAB_BY_CONSTRUCTION"})
    for i, it in enumerate(items):
        it["calib_id"] = f"cal{i:03d}"
        # profile of the edited predicate (z3 monotonicity), recorded as a cross-check of the syntactic position
    (ROOT / "work" / "calibration_items.json").write_text(json.dumps(items, ensure_ascii=False, indent=1))
    from collections import Counter
    print(len(items), Counter(i["gold"] for i in items), Counter(i["variant_type"] for i in items), Counter(i["position"] for i in items if i["gold"] == "UNFAITHFUL"))


if __name__ == "__main__":
    main()
