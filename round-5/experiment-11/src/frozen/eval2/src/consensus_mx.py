"""Readouts of the label-free eqmv matrix: per-row consensus quantities (re-derived c_score_align for gate G2,
aligner-free c_score_exact, endorsement rules END_MAJ / END_PLUR / END_FAM2 / END_FAMMAJ, per-other-family
equivalence counts for M4), classes (connected components, greedy cliques) and non-transitivity.

UNKNOWN (None) is treated as NOT equivalent everywhere, as in the frozen score. A peer whose canonical string equals the
candidate's counts as True (exact), as the frozen eq() did (a == b -> True)."""
from __future__ import annotations

from collections import defaultdict
from itertools import combinations

import numpy as np


class SentenceMatrix:
    """One sentence's matrix record (pairwise_classes / pair_matrix line) with O(1) node-pair lookups."""

    def __init__(self, rec: dict):
        self.rec = rec
        self.sid = rec["sentence_id"]
        self.nodes = rec["nodes"]
        self.n = len(self.nodes)
        self.eq = {}
        self.reason = {}
        self.secs = {}
        for i, j, e, rs, s in rec["pairs"]:
            self.eq[(i, j)] = self.eq[(j, i)] = e
            self.reason[(i, j)] = self.reason[(j, i)] = rs
            self.secs[(i, j)] = self.secs[(j, i)] = s
        self.row_node = {}
        self.row_meta = {}
        for nd in self.nodes:
            for r in nd["rows"]:
                self.row_node[r["row_key"]] = nd["node_id"]
                self.row_meta[r["row_key"]] = r
        self.adj = defaultdict(set)
        for (i, j), e in self.eq.items():
            if e is True:
                self.adj[i].add(j)
        self.comp = self._components()

    def is_eq(self, i: int, j: int) -> bool:
        return True if i == j else self.eq.get((i, j)) is True

    def is_exact(self, i: int, j: int) -> bool:
        return True if i == j else (self.eq.get((i, j)) is True and self.reason.get((i, j)) == "exact")

    def _components(self) -> list[int]:
        comp = [-1] * self.n
        c = 0
        for s in range(self.n):
            if comp[s] >= 0:
                continue
            stack = [s]
            comp[s] = c
            while stack:
                u = stack.pop()
                for v in self.adj[u]:
                    if comp[v] < 0:
                        comp[v] = c
                        stack.append(v)
            c += 1
        return comp

    def components(self) -> list[list[int]]:
        by = defaultdict(list)
        for i, c in enumerate(self.comp):
            by[c].append(i)
        return [by[c] for c in sorted(by)]

    def cliques(self) -> list[list[int]]:
        """Greedy clique partition: take the max-degree remaining node and its pairwise-True common neighbours."""
        left = set(range(self.n))
        out = []
        while left:
            u = max(sorted(left), key=lambda x: len(self.adj[x] & left))
            cl = [u]
            for v in sorted(self.adj[u] & left, key=lambda x: -len(self.adj[x] & left)):
                if all(self.is_eq(v, w) for w in cl):
                    cl.append(v)
            out.append(sorted(cl))
            left -= set(cl)
        return out

    def nontransitive(self) -> tuple[int, int]:
        """(#open wedges a~b, b~c, a!~c ; #wedges a~b, b~c) over unordered node triples, counted per centre b."""
        n_open = n_w = 0
        for b in range(self.n):
            nb = sorted(self.adj[b])
            for a, c in combinations(nb, 2):
                n_w += 1
                if not self.is_eq(a, c):
                    n_open += 1
        return n_open, n_w


def row_consensus(sm: SentenceMatrix, row_key: str, family_key: str = "family") -> dict | None:
    """All consensus readouts of one candidate row (None if unparseable). family_key='family' (vendor, primary) or
    'family_field' (slot-level sensitivity)."""
    if row_key not in sm.row_node:
        return None
    ci = sm.row_node[row_key]
    me = sm.row_meta[row_key]
    fam = me[family_key]
    P = [(rk, m) for rk, m in sm.row_meta.items() if m["is_peer"] and m[family_key] != fam and rk != row_key]
    npc = len(P)
    fam_stats = defaultdict(lambda: [0, 0, 0])  # family -> [n_rows, n_eq, n_eq_exact]
    n_eq = n_ex = 0
    for rk, m in P:
        pj = sm.row_node[rk]
        e = sm.is_eq(ci, pj)
        x = sm.is_exact(ci, pj)
        n_eq += e
        n_ex += x
        fs = fam_stats[m[family_key]]
        fs[0] += 1
        fs[1] += e
        fs[2] += x
    out = {"npc": npc, "n_eq": n_eq, "n_eq_exact": n_ex, "node": ci, "comp": sm.comp[ci],
           "fam_stats": {k: list(v) for k, v in fam_stats.items()}}
    if npc < 2:
        out.update(c_re=None, c_exact=None, end_maj=None, end_plur=None, end_fam2=None, end_fammaj=None)
        return out
    out["c_re"] = 1 - n_eq / npc
    out["c_exact"] = 1 - n_ex / npc
    out["end_maj"] = bool(n_eq > npc / 2)
    fams_endorse = [f for f, v in fam_stats.items() if v[1] > 0]
    out["end_fam2"] = bool(len(fams_endorse) >= 2)
    out["end_fammaj"] = bool(len(fams_endorse) > len(fam_stats) / 2)
    out["n_fam_avail"] = len(fam_stats)
    out["n_fam_endorse"] = len(fams_endorse)
    # END_PLUR: components of the True graph induced on the peer nodes; class size = peer rows
    pnodes = sorted({sm.row_node[rk] for rk, _ in P})
    rows_per_node = defaultdict(int)
    for rk, _ in P:
        rows_per_node[sm.row_node[rk]] += 1
    comp = {}
    c = 0
    for s in pnodes:
        if s in comp:
            continue
        comp[s] = c
        stack = [s]
        while stack:
            u = stack.pop()
            for v in sm.adj[u]:
                if v in rows_per_node and v not in comp:
                    comp[v] = c
                    stack.append(v)
        c += 1
    size = defaultdict(int)
    for nd, k in rows_per_node.items():
        size[comp[nd]] += k
    best = max(size.values())
    tops = [k for k, v in size.items() if v == best]
    if len(tops) > 1:
        out["end_plur"] = False
    else:
        cls = [nd for nd in pnodes if comp[nd] == tops[0]]
        out["end_plur"] = bool(any(sm.is_eq(ci, nd) for nd in cls))
    out["plur_top_share"] = best / npc
    return out


def c_from_fams(fam_stats: dict, fams, exact: bool = False) -> float | None:
    """Consensus over the pool rows of the chosen families only (M4 subsets); None if no rows."""
    n = sum(fam_stats[f][0] for f in fams if f in fam_stats)
    if n == 0:
        return None
    e = sum(fam_stats[f][2 if exact else 1] for f in fams if f in fam_stats)
    return 1 - e / n


def pairwise_class_line(sm: SentenceMatrix, zver: str, code_sha: str) -> dict:
    """The label-free pairwise_classes_E.jsonl line for one sentence."""
    r = sm.rec
    n_open, n_w = sm.nontransitive()
    return {"sentence_id": sm.sid, "source_stratum": r.get("source_stratum"), "words": r.get("words"),
            "n_conditions": r.get("n_conditions"), "nodes": r["nodes"], "pairs": r["pairs"],
            "unparseable_row_keys": r.get("unparseable", []), "components": sm.components(), "cliques": sm.cliques(),
            "n_nontransitive_triples": n_open, "n_wedges": n_w, "eqmv_ms": r.get("eqmv_ms"), "pair_cap_s": r.get("pair_cap_s"),
            "z3_version": zver, "code_sha": code_sha}


def safe_mean(x):
    x = [v for v in x if v is not None]
    return float(np.mean(x)) if x else None
