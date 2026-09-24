"""Extracted verbatim from ../../../../round-2/experiment-5/src/src/vendor_a/fol_triage.py (sha256 560368c934b3f80f13a72e54344fdf4f1507c5f445401de519d7e023009ec951): _occurrences, formula_role_profile."""
from __future__ import annotations
from collections import Counter, defaultdict  # noqa: F401
from fol import parse, profile, prenex_blocks  # noqa: F401


def _occurrences(e):
    """Every atom occurrence with its syntactic context."""
    occ = []

    def go(x, ante, neg, qs, conj, under_all):
        k = x[0]
        if k == "atom":
            occ.append({"key": f"{x[1]}/{len(x[2])}", "name": x[1], "args": x[2], "ante": ante, "neg": neg, "qs": qs,
                        "conj": conj})
        elif k in ("all", "ex"):
            go(x[2], ante, neg, qs + ((x[1], k),), conj, under_all or k == "all")
        elif k == "not":
            go(x[1], ante, neg + 1, qs, conj, under_all)
        elif k == "imp":
            go(x[1], True, 0, qs, conj, under_all)
            go(x[2], ante, 0, qs, conj, under_all)
        elif k == "iff":
            go(x[1], True if under_all else ante, 0, qs, conj, under_all)
            go(x[2], ante, 0, qs, conj, under_all)
        else:
            go(x[1], ante, neg, qs, conj, under_all)
            go(x[2], ante, neg, qs, conj, under_all)
    for i, part in enumerate(prenex_blocks(e)):
        go(part, False, 0, (), i, False)
    return occ


def formula_role_profile(fol, ms: int = 3000, mono: dict | None = None) -> dict:
    """Formula side of L3, exact. -> {pred_key: {'mono','pos','local_neg','role','force','claim','slots'}}.
    mono: z3 monotonicity (UP / DOWN / NONMONO / VACUOUS / UNKNOWN) of the whole formula in that predicate.
    pos: 'antecedent' if any occurrence sits left of → (or left of ↔ under ∀), else 'consequent'.
    local_neg: odd number of explicit ¬ between the (first) occurrence and its antecedent/consequent root.
    role: DOWN&¬neg -> condition; UP&¬neg -> asserted; DOWN&neg -> negated-asserted; UP&neg -> negated-condition;
          NONMONO -> mixed; else unknown.
    force: quantifier of the outermost block binding an argument variable (all/some), 'named' if constant-only.
    claim: top-level conjunct index split into variable-connectivity components (int ids in order of appearance).
    slots: argument tuple; variables mapped to their restrictor predicate (unary predicate over that variable,
           antecedent occurrence preferred), constants kept as names."""
    e = parse(fol) if isinstance(fol, str) else fol
    if mono is None:
        mono = profile(e, ms=ms)
    occ = _occurrences(e)
    # claims: union-find over (conj, var) through shared atoms; constant-only atoms of a conjunct share one component
    parent = {}

    def f(a):
        while parent.setdefault(a, a) != a:
            a = parent[a]
        return a

    def u(a, b):
        parent[f(a)] = f(b)
    comp_of = []
    for o in occ:
        qv = {v for v, _ in o["qs"]}
        vs = [a for a in o["args"] if a in qv]
        nodes = [(o["conj"], v) for v in vs] or [(o["conj"], "#const")]
        for n in nodes[1:]:
            u(nodes[0], n)
        f(nodes[0])
        comp_of.append(nodes[0])
    claim_ids = {}
    restr = {}
    for o in occ:
        if len(o["args"]) == 1 and o["args"][0] in {v for v, _ in o["qs"]}:
            v = (o["conj"], o["args"][0])
            if v not in restr or (o["ante"] and not restr[v][1]):
                restr[v] = (o["name"], o["ante"])
    out = {}
    for o, c in zip(occ, comp_of):
        root = f(c)
        if root not in claim_ids:
            claim_ids[root] = len(claim_ids)
        k = o["key"]
        if k in out:
            out[k]["pos"] = "antecedent" if (o["ante"] or out[k]["pos"] == "antecedent") else "consequent"
            continue
        qv = [v for v, _ in o["qs"]]
        force = None
        for v, q in o["qs"]:
            if v in o["args"]:
                force = "all" if q == "all" else "some"
                break
        if force is None:
            force = "named" if o["args"] else "none"
        m = mono.get(k, "UNKNOWN")
        ln = o["neg"] % 2 == 1
        role = {("DOWN", False): "condition", ("UP", False): "asserted", ("DOWN", True): "negated-asserted",
                ("UP", True): "negated-condition"}.get((m, ln), "mixed" if m == "NONMONO" else "unknown")
        slots = []
        for a in o["args"]:
            if a in qv:
                r = restr.get((o["conj"], a))
                slots.append(("var", r[0] if r and r[0] != o["name"] else None))
            else:
                slots.append(("const", a))
        out[k] = {"mono": m, "pos": "antecedent" if o["ante"] else "consequent", "local_neg": ln, "role": role,
                  "force": force, "claim": claim_ids[root], "slots": slots, "name": o["name"], "arity": len(o["args"])}
    return out
