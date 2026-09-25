"""Contamination control: nonce-disguise a sentence and the matching formula vocabulary consistently.

Content lemmas (NOUN / PROPN / VERB / ADJ, not function or logic words) -> pronounceable CVCVC nonces derived from
sha1(lemma). The same lemma -> nonce map is applied to the CamelCase tokens of predicate and constant names (matched by
Porter stem), so the disguised formula renders the disguised sentence exactly as the original formula rendered the
original sentence, while no memorised FOLIO/MALLS wording survives.
"""
from __future__ import annotations

import hashlib
import re

from fol import parse, to_str
import content_accounting as ca
from fol_triage import nlp, LOGIC_WORDS

C = "bdfgklmnprstvz"
V = "aeiou"
TOKRE = re.compile(r"[A-Z]?[a-z]+|[A-Z]+(?![a-z])|\d+")


def nonce(lemma: str) -> str:
    h = hashlib.sha1(lemma.encode()).digest()
    return C[h[0] % 14] + V[h[1] % 5] + C[h[2] % 14] + V[h[3] % 5] + C[h[4] % 14]


def lemma_map(text: str) -> tuple[str, dict]:
    """-> (disguised text, {porter_stem: nonce})"""
    doc = nlp()(text)
    stem_map = {}
    out = []
    for t in doc:
        w = t.lower_
        if t.pos_ in ("NOUN", "PROPN", "VERB", "ADJ") and w not in ca.FUNC and w not in LOGIC_WORDS and \
                t.lemma_.lower() not in ("be", "have", "do") and t.is_alpha and len(w) > 1:
            lem = t.lemma_.lower()
            nn = nonce(lem)
            for s in {ca.PS.stem(lem), ca.PS.stem(w)}:
                stem_map.setdefault(s, nn)
            suf = "s" if t.tag_ in ("NNS", "VBZ", "NNPS") else ("ed" if t.tag_ in ("VBD", "VBN") else
                                                                 ("ing" if t.tag_ == "VBG" else ""))
            word = nn + suf
            if t.text[0].isupper():
                word = word[0].upper() + word[1:]
            out.append(word + t.whitespace_)
        else:
            out.append(t.text_with_ws)
    return "".join(out), stem_map


def _disguise_name(name: str, stem_map: dict) -> str:
    parts = TOKRE.findall(name)
    if not parts or "".join(parts) != name.replace("_", ""):
        parts = [name]
    out = []
    for i, p in enumerate(parts):
        s = ca.PS.stem(p.lower())
        n = stem_map.get(s)
        if n is None:
            out.append(p)
            continue
        out.append(n[0].upper() + n[1:] if p[0].isupper() else n)
    return "".join(out)


def disguise_formula(fol: str, stem_map: dict) -> str:
    e = parse(fol)
    bv = set()

    def go(x, bound):
        k = x[0]
        if k == "atom":
            return ("atom", _disguise_name(x[1], stem_map),
                    tuple(a if a in bound else _disguise_name(a, stem_map) for a in x[2]))
        if k in ("all", "ex"):
            return (k, x[1], go(x[2], bound | {x[1]}))
        if k == "not":
            return ("not", go(x[1], bound))
        return (k, go(x[1], bound), go(x[2], bound))
    return to_str(go(e, frozenset(bv)))
