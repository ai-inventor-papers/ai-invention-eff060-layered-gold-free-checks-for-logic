"""components() / entropy() copied verbatim from exp C src/consensus.py (SC-5 class entropy)."""
from __future__ import annotations

import math
from collections import defaultdict


def entropy(sizes: list[int]) -> float:
    n = sum(sizes)
    return abs(-sum(k / n * math.log(k / n) for k in sizes if k)) if n else 0.0


def components(nodes: list[str], eqf) -> list[list[str]]:
    parent = {n: n for n in nodes}

    def f(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for i, a in enumerate(nodes):
        for b in nodes[i + 1:]:
            if eqf(a, b) is True:
                parent[f(a)] = f(b)
    comps = defaultdict(list)
    for n in nodes:
        comps[f(n)].append(n)
    return list(comps.values())


def sc_scores_one(cand: str, samples: list, eqf) -> dict:
    """SC-5 for one candidate: eq_frac = #samples equivalent to cand / 5 (None/unparseable sample = not equivalent);
    entropy of the equivalence classes of {cand} ∪ parsed samples, missing samples counted as singleton classes."""
    eqs = [eqf(cand, f) if f else False for f in samples]
    nodes = ["__c__"] + [f"s{k}" for k in range(len(samples)) if samples[k]]
    fm = {"__c__": cand, **{f"s{k}": samples[k] for k in range(len(samples)) if samples[k]}}
    comps = components(nodes, lambda a, b: eqf(fm[a], fm[b]))
    sizes = [len(x) for x in comps] + [1] * sum(1 for f in samples if not f)
    return {"sc5_eq_frac": sum(bool(e) for e in eqs) / 5, "sc5_entropy": entropy(sizes)}
