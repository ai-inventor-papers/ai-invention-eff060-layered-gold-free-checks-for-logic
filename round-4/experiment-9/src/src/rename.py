"""RENAME controls for the E-side rename arm.

rename_syn(fol, seed): VERBATIM logic of iteration-2 dataset 3 src/perturb.py control_rename (RENAME_SYN = one predicate
token -> a mutual-first-sense NOUN WordNet synonym; the text is untouched). Returns None when no synonym exists (dataset 3
then fell back to a nonce rename; here the nonce arm is separate, so SYN rows are only those with a real synonym).
rename_nonce(row): dataset E's disguise map applied to the FORMULA only (metadata_disguised_fol; every predicate and
constant replaced by a nonce word), the English text untouched. Peers cannot read nonce meanings, so NONCE is a stress
boundary, not a gate."""
from __future__ import annotations

import hashlib
import re

import csc  # noqa: F401  (sets NLTK_DATA and the vendored parser path)
import repair_census as RC


def sha1(s: str) -> str:
    return hashlib.sha1(s.encode()).hexdigest()


def first_sense_synonyms(tok: str) -> set:
    from nltk.corpus import wordnet as wn
    ss_ = wn.synsets(tok)
    if not ss_ or ss_[0].pos() != "n" or wn.synsets(tok, pos="v") or wn.synsets(tok, pos="a"):
        return set()
    out = set()
    for lem in ss_[0].lemma_names():
        l = lem.lower()
        if l == tok:
            continue
        s2 = wn.synsets(l)
        if s2 and tok in {x.lower() for x in s2[0].lemma_names()}:
            out.add(l)
    return out


def rename_syn(fol: str, seed: str) -> dict | None:
    e = csc.parse(fol)
    if e is None:
        return None
    Pe, _ = RC.symbols(e)
    names = {p[0] for p in Pe}
    for p in sorted(Pe, key=lambda p: sha1(seed + p[0])):
        toks = re.findall(r"[A-Z]?[a-z]+|[A-Z]+(?![a-z])|\d+", p[0])
        for i, t in enumerate(toks):
            if len(t) < 4 or not t.isalpha():
                continue
            for s in sorted(first_sense_synonyms(t.lower())):
                if "_" in s or "-" in s or s == t.lower() or not s.isalpha() or len(s) < 3:
                    continue
                nt = toks[:i] + [s.capitalize() if t[0].isupper() else s] + toks[i + 1:]
                nn = "".join(nt)
                if nn not in names and nn != p[0] and nn.lower() not in {x.lower() for x in names}:
                    new = RC.rename(e, {p: nn}, {})
                    return {"fol": csc.PT.to_str(new), "map": {f"{p[0]}/{p[1]}": nn}}
    return None
