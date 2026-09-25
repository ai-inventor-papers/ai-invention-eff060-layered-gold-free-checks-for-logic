"""Per-sentence nonce disguise (plan step 5a), used for the panel and stored as disguised_text / disguised_fol.

Lexicon = Porter stems of the sentence's content words ∪ CamelCase/underscore tokens of every predicate and constant
name across ALL formulas of that sentence. Each stem -> a pronounceable CVCVC nonce (seeded by sha1(sentence_id),
rejected if it is a WordNet lemma or already used; bijective). Text is rewritten word-wise (nonce + the word's
inflectional remainder when the stem is a prefix); names are rewritten token-wise. Logic/function/quantifier words,
numbers and digit-bearing tokens are kept. Distinct names that would collapse get a numeric suffix. Every disguised
formula is re-parsed (guard). Deviation from plan: Porter stems (NLTK) instead of spaCy lemmas + Porter.
"""
from __future__ import annotations

import hashlib
import random
import re
from pathlib import Path

from nltk.stem import PorterStemmer

from fol import parse

_ST = PorterStemmer()
KEEP = set("""a an the all every each some any no none not never nothing nobody noone if then else unless except excluding
without but only either or neither nor and both than other is are was were be been being am do does did done has have had
having can could may might must shall should will would of in on at to for from by with as into onto about over under
between among through during before after above below up down out off than that which who whom whose what when where
while whenever wherever why how this these those there here it its it's they them their he him his she her we us our you
your i me my one ones also too very more most less least many much few several such same so because since although though
yet however whether just even still already once twice at least exactly lest per via s x y z true false""".split())
KEEP |= {"zero", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "hundred", "thousand", "first", "second"}
CONS, VOW = "bdfgklmnprtvz", "aeiou"
TOKRE = re.compile(r"[A-Z]?[a-z]+|[A-Z]+(?![a-z])|\d+")
_WN = None


def _wn():
    global _WN
    if _WN is None:
        import nltk
        nltk.data.path.insert(0, str(Path(__file__).resolve().parents[1] / "nltk_data"))
        from nltk.corpus import wordnet as wn
        _WN = set(wn.all_lemma_names())
    return _WN


def _synonym_stem(word: str, text_stems: set) -> str | None:
    _wn()
    from nltk.corpus import wordnet as wn
    for syn in wn.synsets(word)[:6]:
        for lem in syn.lemma_names():
            if "_" not in lem:
                st = stem(lem)
                if st in text_stems:
                    return st
    return None


def stem(w: str) -> str:
    w = w.lower()
    return _ST.stem(w) if len(w) > 3 else w


def name_tokens(name: str) -> list[str]:
    out = []
    for part in re.split(r"[_\-]", name):
        out += TOKRE.findall(part)
    return out


def _names(e, acc):
    k = e[0]
    if k == "atom":
        acc["pred"].add(e[1])
        for a in e[2]:
            acc["arg"].add(a)
    elif k in ("all", "ex"):
        acc["var"].add(e[1]); _names(e[2], acc)
    elif k == "not":
        _names(e[1], acc)
    else:
        _names(e[1], acc); _names(e[2], acc)
    return acc


class Disguiser:
    def __init__(self, sentence_id: str, text: str, formulas: list[str]):
        self.rng = random.Random(int(hashlib.sha1(sentence_id.encode()).hexdigest()[:12], 16))
        self.map: dict[str, str] = {}
        self.used: set[str] = set()
        self.asts = {}
        for f in formulas:
            try:
                self.asts[f] = parse(f)
            except Exception:  # noqa: BLE001 - unparseable formulas are not shown to the panel
                pass
        words = re.findall(r"[A-Za-z]+", text)
        for w in words:
            if w.lower() not in KEEP:
                self._nonce(stem(w))
        self.vars, self.preds, self.args = set(), set(), set()
        for e in self.asts.values():
            acc = _names(e, {"pred": set(), "arg": set(), "var": set()})
            self.vars |= acc["var"]; self.preds |= acc["pred"]; self.args |= acc["arg"]
        self.text_stems = set(self.map)
        self.alias: dict[str, str] = {}
        for n in sorted(self.preds | (self.args - self.vars)):
            for t in name_tokens(n):
                if not t.isdigit() and t.lower() not in KEEP:
                    st = stem(t)
                    if st not in self.map:
                        syn = _synonym_stem(t.lower(), self.text_stems)
                        if syn:  # WordNet synonym of a sentence word -> same nonce (keeps the text link)
                            self.alias[st] = syn
                            continue
                    self._nonce(st)
        self.name_map: dict[str, str] = {}
        self._build_name_map()

    def _nonce(self, s: str) -> str:
        s = self.alias.get(s, s) if hasattr(self, "alias") else s
        if s in self.map:
            return self.map[s]
        wn = _wn()
        while True:
            w = "".join(self.rng.choice(CONS) + self.rng.choice(VOW) for _ in range(2)) + self.rng.choice(CONS)
            if w not in wn and w not in self.used and not w.endswith("s"):
                break
        self.used.add(w)
        self.map[s] = w
        return w

    def _dis_name(self, n: str, is_pred: bool) -> str:
        toks = name_tokens(n)
        if not toks:
            return n
        out = []
        for t in toks:
            if t.isdigit() or t.lower() in KEEP:
                out.append(t)
            else:
                st = stem(t)
                rest = t[len(st):] if t.lower().startswith(st) else ""
                out.append(self._nonce(st) + rest.lower())
        s = "".join(x[:1].upper() + x[1:] for x in out)
        if not is_pred:
            s = s[:1].lower() + s[1:]
            if re.fullmatch(r"[a-z]", s) or re.fullmatch(r"[a-z]\d*", s):
                s = s + "q"
        return s

    def _build_name_map(self):
        taken: dict[str, str] = {}
        for n, is_pred in [(p, True) for p in sorted(self.preds)] + [(a, False) for a in sorted(self.args - self.vars)]:
            d = self._dis_name(n, is_pred)
            base, i = d, 2
            while d in taken and taken[d] != n:
                d = f"{base}{i}"; i += 1
            taken[d] = n
            self.name_map[(n, is_pred)] = d

    def text(self, text: str) -> str:
        def rep(m):
            w = m.group(0)
            if w.lower() in KEEP:
                return w
            s = stem(w)
            nw = self.map.get(s)
            if nw is None:
                return w
            rest = w[len(s):] if w.lower().startswith(s) else ""
            out = nw + rest
            return out[:1].upper() + out[1:] if w[:1].isupper() else out
        return re.sub(r"[A-Za-z]+", rep, text)

    def formula(self, f: str) -> str | None:
        e = self.asts.get(f)
        if e is None:
            return None
        s = self._emit(e, frozenset())
        parse(s)  # guard: every disguised formula must parse
        return s

    def ast(self, f: str):
        e = self.asts.get(f)
        return None if e is None else self._rename(e, frozenset())

    def _rename(self, e, bv):
        k = e[0]
        if k == "atom":
            return ("atom", self.name_map.get((e[1], True), e[1]),
                    tuple(a if a in bv or a in self.vars else self.name_map.get((a, False), a) for a in e[2]))
        if k in ("all", "ex"):
            return (k, e[1], self._rename(e[2], bv | {e[1]}))
        if k == "not":
            return ("not", self._rename(e[1], bv))
        return (k, self._rename(e[1], bv), self._rename(e[2], bv))

    def _emit(self, e, bv) -> str:
        return emit(self._rename(e, bv))


SYM = {"and": "∧", "or": "∨", "imp": "→", "iff": "↔", "xor": "⊕"}


def emit(e) -> str:
    k = e[0]
    if k == "atom":
        return f"{e[1]}({', '.join(e[2])})" if e[2] else e[1]
    if k in ("all", "ex"):
        return f"{'∀' if k == 'all' else '∃'}{e[1]} ({emit(e[2])})"
    if k == "not":
        return f"¬{emit(e[1])}" if e[1][0] in ("atom", "not", "all", "ex") else f"¬({emit(e[1])})"
    return f"({emit(e[1])} {SYM[k]} {emit(e[2])})"
