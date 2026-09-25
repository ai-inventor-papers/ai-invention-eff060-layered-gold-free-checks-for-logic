"""Extracted verbatim from ../../../../../../../round-2/dataset-3/src/src/perturb.py (sha256 256d5937eb710159f1c6377e319e7db775f5547a0ffa3bf8a5660a93a254a155): name_tokens, wn_synonyms, meaning_rename, first_sense_synonyms, control_rename."""
from __future__ import annotations
import random
import re
import hashlib


def sha1(s: str) -> str:
    return hashlib.sha1(s.encode()).hexdigest()


CONS, VOW = 'bdfgklmnprtvz', 'aeiou'


def name_tokens(n):
    return [t.lower() for t in re.findall(r"[A-Z]?[a-z]+|[A-Z]+(?![a-z])|\d+", n.replace("_", " "))]


def wn_synonyms(tok: str) -> set:
    from nltk.corpus import wordnet as wn
    out = set()
    for s in wn.synsets(tok)[:8]:
        out |= {l.lower() for l in s.lemma_names()}
    return out


def meaning_rename(e, donor):
    """Own MEANING_RENAME: all occurrences of one base predicate -> a same-arity donor predicate whose name tokens are
    not WordNet synonyms of the original's tokens (and not already in the base)."""
    from repair_census import symbols, rename
    Pe, _ = symbols(e)
    Pd, _ = symbols(donor)
    names_e = {p[0] for p in Pe}
    for p in sorted(Pe):
        tp = set(name_tokens(p[0]))
        syn = set().union(*[wn_synonyms(t) for t in tp]) if tp else set()
        for q in sorted(Pd):
            if q[1] != p[1] or q[0] in names_e:
                continue
            tq = set(name_tokens(q[0]))
            if tq & (tp | syn):
                continue
            yield "MEANING_RENAME", "MEANING_RENAME", p, rename(e, {p: q[0]}, {})


def first_sense_synonyms(tok: str) -> set:
    """Mutual first-sense WordNet synonyms: s is in tok's first synset AND tok is in s's first synset
    (guards against wrong-sense swaps such as steal -> bargain)."""
    from nltk.corpus import wordnet as wn
    ss_ = wn.synsets(tok)
    if not ss_ or ss_[0].pos() != "n" or wn.synsets(tok, pos="v") or wn.synsets(tok, pos="a"):
        return set()  # nouns only: verb/adjective senses make wrong-sense swaps likely
    out = set()
    for lem in ss_[0].lemma_names():
        l = lem.lower()
        if l == tok:
            continue
        s2 = wn.synsets(l)
        if s2 and tok in {x.lower() for x in s2[0].lemma_names()}:
            out.add(l)
    return out


def control_rename(e, seed: str):
    """RENAME_SYN: one predicate token -> a WordNet synonym (single word, not already a token); else RENAME_NONCE."""
    from repair_census import symbols, rename
    Pe, _ = symbols(e)
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
                if nn not in names and nn != p[0]:
                    return "RENAME_SYN", {p: nn}, rename(e, {p: nn}, {})
    rng = random.Random(int(sha1(seed), 16))
    p = sorted(Pe, key=lambda p: sha1(seed + p[0]))[0]
    while True:
        w = "".join(rng.choice(CONS) + rng.choice(VOW) for _ in range(2)) + rng.choice(CONS)
        nn = w.capitalize()
        if nn not in names:
            break
    return "RENAME_NONCE", {p: nn}, rename(e, {p: nn}, {})
