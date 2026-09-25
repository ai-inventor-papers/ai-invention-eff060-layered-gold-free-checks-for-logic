"""Nonce DISGUISE of (text, formula) pairs: every content lemma -> a pronounceable nonce word, consistently in the text
AND in the predicate/constant names of the formula. Logic, quantifier and function words are untouched; arity,
argument order, variables and connectives are untouched.

Departure from the plan text (documented in README): the formula is disguised by TOKEN-LEVEL substitution of predicate
and constant identifiers in the raw string (whitespace, bracketing and symbols preserved byte-for-byte), and the result
is verified on the AST (assertion (i): the inverse name map applied to parse(disguised) == parse(original)). This keeps
the orig vs disg judge conditions identical in surface form except for the names, which is what the contamination
contrast needs; an AST re-printer would also change bracketing.
"""
from __future__ import annotations

import re
from functools import lru_cache

from .common import norm, sha1

PROTECTED = set("""all every each some any no none not never if then only unless except either or and nor both neither
is are be a an the who which that there exists also may can must does do of in on at to for with by from as than more most
least many few one two three their they it its he she his her someone something everyone everything people person thing
was were been being has have had am this these those what when where whether but so because while all anyone anything
nobody nothing somebody everybody others other another such same""".split())
CONS, VOWS = "bdfgklmnprstvz", "aeiou"
IDENT = re.compile(r"[A-Za-z_][A-Za-z0-9_'\-]*")
CAMEL = re.compile(r"[A-Z]?[a-z]+|[A-Z]+(?![a-z])|\d+")
CONTENT_POS = {"NOUN", "PROPN", "VERB", "ADJ", "ADV"}

_NLP = None
_WORDS = None
_STEM = None


def stem(w: str) -> str:
    """Canonical key for a lemma (Porter stem), so text 'engaged'/'engage' and name piece 'Engaged' share one nonce."""
    global _STEM
    if _STEM is None:
        from nltk.stem import PorterStemmer
        _STEM = PorterStemmer()
    return _STEM.stem(w.lower())


def nlp():
    global _NLP
    if _NLP is None:
        import spacy
        _NLP = spacy.load("en_core_web_sm", disable=["ner", "parser"])
    return _NLP


def english_words() -> set:
    global _WORDS
    if _WORDS is None:
        from nltk.corpus import words
        _WORDS = {w.lower() for w in words.words()}
    return _WORDS


@lru_cache(maxsize=200000)
def lemma_of_piece(piece: str) -> str:
    p = piece.lower()
    if p.isdigit() or len(p) <= 1:
        return p
    doc = nlp()(p)
    return (doc[0].lemma_ or p).lower() if len(doc) else p


def _nonce_from_int(h: int) -> str:
    out = []
    for syl in range(3):
        out.append(CONS[h % len(CONS)]); h //= len(CONS)
        out.append(VOWS[h % len(VOWS)]); h //= len(VOWS)
        if syl < 2 and h % 3 == 0:  # optional coda on the first two syllables
            h //= 3
            out.append(CONS[h % len(CONS)]); h //= len(CONS)
        else:
            h //= 3
    return "".join(out)


def nonce(lemma: str, seed_text: str, taken: set) -> str:
    k = 0
    while True:
        h = int(sha1(f"{norm(seed_text)}|{lemma}|{k}"), 16)
        w = _nonce_from_int(h)
        if w not in english_words() and w not in taken and w not in PROTECTED:
            return w
        k += 1


def split_name(name: str) -> list[str]:
    parts = []
    for chunk in re.split(r"[_\-']", name):
        parts.extend(CAMEL.findall(chunk))
    return parts or [name]


def _inflect(tok: str, lemma: str, nw: str) -> str:
    t = tok.lower()
    suf = ""
    if t != lemma and t.startswith(lemma) and t[len(lemma):] in ("s", "es", "ed", "d", "ing", "er", "r", "est", "st", "ly"):
        suf = {"d": "ed", "r": "er", "st": "est"}.get(t[len(lemma):], t[len(lemma):])
    elif t != lemma:
        for s in ("ing", "est", "ed", "er", "es", "ly", "s"):
            if t.endswith(s):
                suf = s
                break
    out = nw + suf
    if tok[:1].isupper():
        out = out[:1].upper() + out[1:]
    return out


def formula_roles(fol: str) -> list[tuple[str, str]]:
    """(identifier, role) in textual order; role in {pred, const, var}. Works on unparseable strings too."""
    ids = [m.group(0) for m in IDENT.finditer(fol)]
    # positions: an identifier followed (after spaces) by '(' is a predicate; identifier right after a quantifier symbol
    # is a variable; identifiers inside predicate argument lists are const unless bound somewhere as variable.
    roles = []
    bound = set(re.findall(r"[∀∃]\s*([a-z][a-z0-9]*)", fol))
    depth_args = 0
    pos = 0
    for m in IDENT.finditer(fol):
        name = m.group(0)
        after = fol[m.end():].lstrip()
        before = fol[:m.start()].rstrip()
        if before.endswith(("∀", "∃")):
            roles.append((name, "var"))
        elif after.startswith("("):
            roles.append((name, "pred"))
        else:
            # inside an argument list?  count unmatched '(' that belong to a predicate call
            inside = _inside_args(fol, m.start())
            if inside:
                roles.append((name, "var" if name in bound else "const"))
            else:
                roles.append((name, "pred"))  # propositional atom
        pos = m.end()
    del ids, depth_args, pos
    return roles


def _inside_args(fol: str, i: int) -> bool:
    depth, j = 0, i - 1
    while j >= 0:
        ch = fol[j]
        if ch == ")":
            depth += 1
        elif ch == "(":
            if depth == 0:
                k = j - 1
                while k >= 0 and fol[k] == " ":
                    k -= 1
                return k >= 0 and (fol[k].isalnum() or fol[k] in "_'-")
            depth -= 1
        j -= 1
    return False


def disguise_item(text: str, fol: str | None, seed_text: str | None = None) -> dict:
    """Returns {text_d, fol_d, lemma_map, name_map, ok, fail_reasons, leak_text, leak_formula}."""
    seed = seed_text if seed_text is not None else text
    doc = nlp()(text)
    lemmas = []
    for t in doc:
        lw = (t.lemma_ or t.text).lower()
        if t.pos_ in CONTENT_POS and t.text.lower() not in PROTECTED and lw not in PROTECTED and t.text.isalpha():
            lemmas.append(stem(lw))
    orig_lemmas = {(t.lemma_ or t.text).lower() for t in doc if t.pos_ in CONTENT_POS and t.text.isalpha()
                   and t.text.lower() not in PROTECTED}
    roles = formula_roles(fol) if fol else []
    for name, role in roles:
        if role in ("pred", "const"):
            for p in split_name(name):
                lp = lemma_of_piece(p)
                if lp not in PROTECTED and not lp.isdigit() and len(lp) > 1:
                    lemmas.append(stem(lp))
                    orig_lemmas.add(lp)
    lemma_map, taken = {}, set()
    for lw in sorted(set(lemmas)):
        w = nonce(lw, seed, taken)
        lemma_map[lw] = w
        taken.add(w)
    # ---- text
    out = []
    for t in doc:
        lw = (t.lemma_ or t.text).lower()
        tl = t.text.lower()
        sk = stem(lw) if t.text.isalpha() else None
        if t.text.isalpha() and tl not in PROTECTED and lw not in PROTECTED and (sk in lemma_map or stem(tl) in lemma_map):
            key = sk if sk in lemma_map else stem(tl)
            out.append(_inflect(t.text, lw, lemma_map[key]) + t.whitespace_)
        else:
            out.append(t.text_with_ws)
    text_d = "".join(out)
    # ---- formula (token-level substitution, surface form preserved)
    name_map, used = {}, {}
    fol_d = None
    if fol:
        pieces_out = []
        last = 0
        ridx = 0
        for m in IDENT.finditer(fol):
            name, role = roles[ridx]
            ridx += 1
            pieces_out.append(fol[last:m.start()])
            last = m.end()
            if role == "var":
                pieces_out.append(name)
                continue
            key = (name, role)
            if key not in name_map:
                parts = []
                for p in split_name(name):
                    lp = lemma_of_piece(p)
                    if stem(lp) in lemma_map and lp not in PROTECTED:
                        parts.append(lemma_map[stem(lp)])
                    else:
                        parts.append(p.lower())  # protected / digit piece kept
                if role == "pred":
                    new = "".join(x[:1].upper() + x[1:] for x in parts)
                else:
                    new = "".join(parts).lower()
                    if not new[:1].isalpha():
                        new = "k" + new
                base, k = new, 0
                while new in used and used[new] != key:
                    k += 1
                    new = base + ("Zo" if role == "pred" else "zo") * k
                used[new] = key
                name_map[key] = new
            pieces_out.append(name_map[key])
        pieces_out.append(fol[last:])
        fol_d = "".join(pieces_out)
    # ---- assertions
    fails = []
    if fol:
        from .labeller.fol import parse
        from .labeller.repair_census import rename
        inv_p = {}
        inv_c = {}
        for (name, role), new in name_map.items():
            (inv_p if role == "pred" else inv_c)[new] = name
        try:
            e0 = parse(fol)
            try:
                e1 = parse(fol_d)
                # inverse map on AST
                from .labeller.repair_census import symbols
                P1, _ = symbols(e1)
                pmap = {(n, a): inv_p.get(n, n) for (n, a) in P1}
                back = rename(e1, pmap, inv_c)
                if back != e0:
                    fails.append("inverse_map_ast_mismatch")
                from .labeller.fol import preds
                if sorted(preds(e0).values()) != sorted(preds(e1).values()):
                    fails.append("arity_multiset_changed")
            except Exception as ex:  # noqa: BLE001
                fails.append(f"disguised_unparseable:{str(ex)[:60]}")
        except Exception:  # noqa: BLE001 - original unparseable: disguise still applied token-wise
            pass
        new_names = list(name_map.values())
        if len(set(new_names)) != len(new_names):
            fails.append("name_collision")
    vals = list(lemma_map.values())
    if len(set(vals)) != len(vals):
        fails.append("nonce_collision")
    # protected word counts unchanged
    def pcount(s):
        toks = re.findall(r"[A-Za-z]+", s.lower())
        return sorted(t for t in toks if t in PROTECTED)
    if pcount(text) != pcount(text_d):
        fails.append("protected_count_changed")
    # leaks
    cont = {l for l in orig_lemmas if len(l) >= 4 and l not in PROTECTED}
    text_toks = {(t.lemma_ or t.text).lower() for t in nlp()(text_d)} | set(re.findall(r"[a-z]+", text_d.lower()))
    leak_t = sum(1 for l in cont if l in text_toks) / max(1, len(cont))
    leak_f = 0.0
    if fol_d:
        f_pieces = {lemma_of_piece(p) for n in IDENT.findall(fol_d) for p in split_name(n)}
        leak_f = sum(1 for l in cont if l in f_pieces) / max(1, len(cont))
        if leak_f > 0:
            fails.append("formula_leak")
    return {"text_d": text_d, "fol_d": fol_d, "lemma_map": lemma_map,
            "name_map": {f"{k[0]}|{k[1]}": v for k, v in name_map.items()}, "ok": not fails, "fail_reasons": fails,
            "leak_text": round(leak_t, 4), "leak_formula": round(leak_f, 4)}
