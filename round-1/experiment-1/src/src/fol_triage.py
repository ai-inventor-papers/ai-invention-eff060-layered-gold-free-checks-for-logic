"""FOL-Triage: a gold-free, three-layer faithfulness check for a (text, fol) pair.

Released functions (each takes the natural-language text and/or a candidate FOL formula; no gold, no ontology):

fol_lint(fol)                   L1  TEXT-FREE formula smells (frozen iter-3 list): improbable renderings of ANY English
                                    sentence -- EX_IMP ∃x(A→B), ALL_AND ∀x(A∧B), IFF_RESTR ∀x(A∧B↔C), GLUE (independent
                                    universal claims glued in one block), FREE variable, VACUOUS predicate (z3), TRIVIAL
                                    (valid/unsat, z3), ARITY clash, DANGLING universal variable.
content_accounting(text, fol)   L2-bow  bag-of-words baseline: predicates whose name no text word anchors (ADD) and the share
                                    of text content words no predicate/constant carries (DROP). Role-blind.
role_accounting(text, fol)      L2-role  role-aware accounting: spaCy dependency roles of text words (condition / asserted /
                                    exception, negation) must match the EXACT z3 monotonicity of the predicates they align
                                    to (condition->DOWN, asserted->UP, exception->UP, flipped by negation); plus
                                    subject/object slot order of binary predicates. Counts mismatches.
formula_role_profile(fol)       formula side of L3, answered EXACTLY: per predicate its z3 monotonicity, position,
                                    local negation, derived role, quantifier force, claim index and argument slots.
role_questionnaire(text, ...)   L3 text side: a small LLM reads ONLY the sentence and fills a frozen schema
                                    (concepts with role/negated/exception/force/claim; ordered relations).
l3_compare(q, profile)          per-field mismatch between the text questionnaire and a formula profile.
fol_triage(...)                 cascade L1 -> L2 -> L3 with a fused logistic p_error and an error-type code.
"""
from __future__ import annotations

import itertools
import json
import math
import re
import sys
from collections import Counter, defaultdict
from functools import lru_cache
from pathlib import Path

sys.setrecursionlimit(10000)
SRC = Path(__file__).resolve().parent
sys.path.insert(0, str(SRC))

import z3  # noqa: E402

from fol import parse, profile, preds, prenex_blocks, to_z3, mkpred, valid  # noqa: E402
import lint_smells  # noqa: E402
import content_accounting as ca  # noqa: E402

PS = ca.PS
LOGIC_WORDS = {"all", "every", "each", "any", "some", "no", "not", "none", "if", "then", "only", "unless", "except",
               "either", "or", "and", "neither", "nor", "both", "never", "always", "there", "exists"}


# =============================================================================================== L1
def fol_lint(fol: str) -> dict:
    """L1. Returns {'codes': sorted smell codes, 'parse_ok': bool, 'z3_unknown': bool}.
    Codes are the frozen iter-3 lint_smells.smells() output (verbatim); z3-dependent smells (VACUOUS, TRIVIAL) are
    re-checked at 1500 ms and, when z3 answers unknown or raises, z3_unknown=True (never silently absent)."""
    try:
        e = parse(fol) if isinstance(fol, str) else fol
    except Exception:  # noqa: BLE001
        return {"codes": [], "parse_ok": False, "z3_unknown": False}
    codes = sorted(lint_smells.smells(e))
    unk = False
    try:
        pr = profile(e, ms=1500)
        if any(v == "UNKNOWN" for v in pr.values()):
            unk = True
        P = {q: mkpred(q, m) for q, m in preds(e).items()}
        F = to_z3(e, {}, P)
        if valid(F, 1500) is None or valid(z3.Not(F), 1500) is None:
            unk = True
    except Exception:  # noqa: BLE001
        unk = True
    return {"codes": codes, "parse_ok": True, "z3_unknown": unk}


# =============================================================================================== L2 bag-of-words
def content_accounting(text: str, fol: str) -> dict:
    """L2-bow baseline (iter-3 code, LEX matching). flag iff >=1 unanchored predicate or uncarried share > 0.34."""
    r = ca.content_accounting(text, fol, mode="LEX")
    return {"uncarried_frac": r["drop_share"], "unanchored_preds": r["unanchored"], "n_unanchored": r["n_unanchored"],
            "n_content": len(ca.text_words(text)), "n_preds": r["k"],
            "flag": bool(r["n_unanchored"] >= 1 or r["drop_share"] > 0.34)}


# =============================================================================================== formula profile
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


# =============================================================================================== lexical alignment
@lru_cache(maxsize=None)
def name_words(name: str) -> tuple:
    return tuple(ca.name_words(name))


@lru_cache(maxsize=None)
def _lex(w: str) -> frozenset:
    return frozenset(ca.lex(w))


def word_match(w: str, pw: str, exact: bool = False) -> bool:
    """Text word w matches predicate-name word pw: same Porter stem (exact) or WordNet lemma/synonym/derivation."""
    sw, sp = PS.stem(w.lower()), PS.stem(pw.lower())
    if sw == sp:
        return True
    if exact:
        return False
    return sp in _lex(w.lower()) or sw in _lex(pw.lower())


def const_match(phrase_words: list[str], const: str) -> bool:
    c = re.sub(r"[^a-z0-9]", "", const.lower())
    p = re.sub(r"[^a-z0-9]", "", "".join(phrase_words).lower())
    if not c or not p:
        return False
    return c == p or (len(p) >= 3 and (c.startswith(p) or p.startswith(c) or p in c))


# =============================================================================================== L2 role-aware
_NLP = None


def nlp():
    global _NLP
    if _NLP is None:
        import spacy
        _NLP = spacy.load("en_core_web_sm")
    return _NLP


COND_MARKS = ("if", "when", "whenever", "once", "provided", "as long as", "in case", "assuming", "given that")
EXC_MARKS = ("unless", "except", "excluding", "without", "but not", "other than")
GENERIC_DETS = {"all", "every", "each", "any", "no"}
GENERIC_PRON = {"everyone", "anyone", "everybody", "anybody", "everything", "anything", "nobody", "whoever", "those"}
NEG_WORDS = {"not", "n't", "never", "no", "none", "nobody", "nothing", "neither", "nor", "cannot"}


def _clause_head(t):
    x = t
    while x.dep_ not in ("ROOT", "advcl", "relcl", "ccomp", "xcomp", "acl") and x.head is not x and x.pos_ not in ("VERB", "AUX"):
        x = x.head
    return x


SUBJ_DEPS = ("nsubj", "nsubjpass", "csubj")


_NEITHER: set = set()  # token indices of the current doc under neither/nor or not-both (set per text_roles call)


def _neither_scope(doc) -> set:
    """Token indices negated by 'neither ... nor', 'not both' or 'not either': every token after the marker up to the
    next clause boundary (',', ';', 'then') or the end of the sentence; subjects excluded."""
    out = set()
    toks = list(doc)
    for t in toks:
        w = t.lower_
        prev = toks[t.i - 1].lower_ if t.i > 0 else ""
        if w == "neither" or (w in ("both", "either") and prev in ("not", "n't")):
            for x in toks[t.i + 1:]:
                if x.lower_ in (",", ";", "then"):
                    break
                if x.dep_ not in SUBJ_DEPS:
                    out.add(x.i)
    return out


def _negated(t, _depth: int = 0) -> bool:
    """Literal negation of the word where it appears. Subjects are never negated by their clause's 'not'; a subject's
    'no' determiner is handled by the no-subject rule (flips the assertion only). Negation of an object / attribute
    is inherited by its modifiers (amod, compound, acl, prep, pobj)."""
    if t.i in _NEITHER:
        return True
    if any(c.dep_ == "neg" or c.lower_ == "never" for c in t.children):
        return True
    if t.dep_ in SUBJ_DEPS:
        return False
    if any(c.dep_ == "det" and c.lower_ == "no" for c in t.children):
        return True
    if t.dep_ in ("acomp", "attr", "dobj", "xcomp", "oprd", "advmod", "prt", "dative") and \
            any(c.dep_ == "neg" or c.lower_ == "never" for c in t.head.children):
        return True
    if t.dep_ == "pobj" and t.head.dep_ == "prep":
        g = t.head.head
        if any(c.dep_ == "neg" or c.lower_ == "never" for c in g.children):
            return True
        if g.dep_ in ("acomp", "attr", "dobj", "xcomp") and _negated(g):
            return True
    if t.dep_ in ("compound", "amod", "acl", "prep", "pobj", "nmod") and t.head is not t and \
            t.head.dep_ not in SUBJ_DEPS and _depth < 6:
        return _negated(t.head, _depth + 1)
    return False


def _content(t) -> bool:
    w = t.lower_
    return (t.pos_ in ("NOUN", "PROPN", "VERB", "ADJ", "ADV", "NUM") and w not in ca.FUNC and w not in ca.HEDGE
            and w not in ca.SORTAL and w not in LOGIC_WORDS and len(w) > 1 and t.lemma_.lower() not in ("be", "have", "do"))


def text_roles(text: str) -> dict:
    """spaCy dependency roles -> {'tokens': [{'i','w','lemma','role','neg','pos'}], 'generic': bool, 'no_subject': bool}"""
    doc = nlp()(text)
    _NEITHER.clear()
    _NEITHER.update(_neither_scope(doc))
    role = {}
    lower = text.lower()

    def mark_subtree(h, r, overwrite=False):
        for x in h.subtree:
            if overwrite or x.i not in role:
                role[x.i] = r
    # condition / exception adverbial clauses
    for t in doc:
        if t.dep_ == "advcl":
            sub = list(t.subtree)
            head_txt = " ".join(x.lower_ for x in sub[:3])
            marks = {c.lower_ for c in t.children if c.dep_ == "mark"}
            if marks & set(EXC_MARKS) or head_txt.startswith(EXC_MARKS):
                mark_subtree(t, "exception", True)
            elif marks & {"if", "when", "whenever", "once", "provided", "assuming"} or head_txt.startswith(COND_MARKS) \
                    or (t.i > 0 and doc[max(0, sub[0].i - 1)].lower_ in ("if", "when", "whenever")):
                mark_subtree(t, "condition", True)
        if t.dep_ == "prep" and t.lower_ in ("except", "without", "excluding") or \
                (t.lower_ == "than" and t.i > 0 and doc[t.i - 1].lower_ == "other"):
            mark_subtree(t, "exception", True)
    # sentence-final conditional ('Y holds if A, B, and C'): coordinated VPs after the marker are routinely attached to
    # the main verb by the parser; everything from the marker to the end of the sentence is the condition
    for t in doc:
        if t.lower_ in ("if", "when", "whenever") and t.i > 2 and t.dep_ == "mark" and t.head.i > t.i:
            for x in doc[t.i:]:
                if role.get(x.i) != "exception":
                    role[x.i] = "condition"
            break
    if not any(r == "condition" for r in role.values()) and lower.lstrip().startswith(("if ", "when ", "whenever ")):
        for x in doc:
            if x.lower_ in (",", "then") and x.i > 1:
                break
            role[x.i] = "condition"
    # generic subject: det all/every/each/any/no, bare plural, everyone/anyone ...; relative clauses on the subject
    root = [t for t in doc if t.dep_ == "ROOT"]
    generic = False
    no_subject = False
    subj_heads = []
    for r in root:
        for c in r.children:
            if c.dep_ in ("nsubj", "nsubjpass"):
                subj_heads.append(c)
        # subjects of coordinated / contrastive main clauses ('Wolves howl, while birds chirp', 'X do A and Y do B')
        for v in r.children:
            if v.dep_ == "conj" or (v.dep_ == "advcl" and {m.lower_ for m in v.children if m.dep_ == "mark"} &
                                    {"while", "whereas"}):
                for c in v.children:
                    if c.dep_ in ("nsubj", "nsubjpass"):
                        subj_heads.append(c)
        # conjoined/clausal: 'If x, then y' -> the root clause is the assertion
    for s in subj_heads:
        dets = {c.lower_ for c in s.children if c.dep_ in ("det", "predet")}
        is_gen = bool(dets & GENERIC_DETS) or s.lower_ in GENERIC_PRON or \
            (s.tag_ == "NNS" and not dets and not any(c.dep_ == "poss" for c in s.children))
        if dets & {"no"} or s.lower_ in ("nobody", "none", "nothing"):
            no_subject = True
        rel = [c for c in s.children if c.dep_ in ("relcl", "acl")]
        for rc in rel:
            mark_subtree(rc, "condition")
            generic = True
        if is_gen:
            generic = True
            role.setdefault(s.i, "condition")
            for c in s.children:
                if c.dep_ in ("amod", "compound", "nmod", "prep") and c.i not in role:
                    for x in c.subtree:
                        role.setdefault(x.i, "condition")
    if any(r == "condition" for r in role.values()):
        generic = True
    # 'A bird flies if it has wings' / 'An organization is non-profit if ...': in a conditional generic, an indefinite
    # (a/an) subject of the main clause is the restrictor, not an asserted property
    if generic:
        for s in subj_heads:
            dets = {c.lower_ for c in s.children if c.dep_ in ("det", "predet")}
            if dets & {"a", "an"} and s.i not in role:
                role[s.i] = "condition"
                for c in s.children:
                    if c.dep_ in ("amod", "compound") and c.i not in role:
                        for x in c.subtree:
                            role.setdefault(x.i, "condition")
    # 'Not all / not every X ...' = ¬∀x(X -> Y) = ∃x(X ∧ ¬Y): every expectation flips
    neg_all = bool(re.match(r"\s*(it is )?not (all|every|each|everyone|everything)\b", lower)) or \
        bool(re.match(r"\s*it is not (true|the case) that\b", lower))
    # assertion tokens: root-clause predicates outside condition/exception subtrees
    ASSERT_DEPS = {"ROOT", "acomp", "attr", "dobj", "xcomp", "oprd", "pobj", "conj", "compound", "amod", "prep", "advmod",
                   "npadvmod", "ccomp", "dative", "agent", "nsubj", "nsubjpass", "appos", "nmod", "poss", "acl", "relcl"}
    for r in root:
        for x in r.subtree:
            if x.i in role:
                continue
            if x in subj_heads and not generic:
                continue  # named/existential subject: the individual, not an asserted property
            if (x in subj_heads or (x.dep_ in ("compound", "amod") and x.head in subj_heads)) and generic and \
                    {c.lower_ for c in (x.children if x in subj_heads else x.head.children) if c.dep_ == "det"} & \
                    {"the", "this", "that", "these", "those", "such"}:
                continue  # anaphoric subject ('then THE student passes') re-mentions the condition, asserts nothing
            if x.dep_ in ASSERT_DEPS:
                role[x.i] = "asserted"
    toks = []
    for t in doc:
        if t.i not in role or not _content(t):
            continue
        r = role[t.i]
        if t in subj_heads and t.pos_ == "PROPN":
            continue
        neg = _negated(t)
        if r == "asserted" and no_subject:
            neg = not neg
        if neg_all:
            neg = not neg
        toks.append({"i": t.i, "w": t.lower_, "lemma": t.lemma_.lower(), "role": r, "neg": neg, "pos": t.pos_})
    return {"tokens": toks, "generic": generic, "no_subject": no_subject, "neg_all": neg_all, "doc": doc}


def _expected(role: str, neg: bool) -> str | None:
    base = {"condition": "DOWN", "asserted": "UP", "exception": "UP"}.get(role)
    if base is None:
        return None
    if neg:
        base = "UP" if base == "DOWN" else "DOWN"
    return base


def _align_token(t: dict, prof: dict, exact: bool = False) -> list[str]:
    out = []
    for k, p in prof.items():
        ws = name_words(p["name"])
        if any(word_match(t["w"], pw, exact) or word_match(t["lemma"], pw, exact) for pw in ws):
            out.append(k)
    return out


def _phrase_words_of(tok) -> list[str]:
    ws = [x.text for x in tok.subtree if x.dep_ in ("compound", "flat") or x is tok]
    return ws


def role_accounting(text: str, fol, prof: dict | None = None) -> dict:
    """L2-role. -> {'cond_in_up','assert_in_down','pol_flip','slot_swap','exc_wrong','n_role_words','n_resolved','flag',
    'codes','generic'}.  Role rules (condition->DOWN, asserted->UP, exception->UP) apply only to generic/universal
    sentences (a condition token exists); named/existential sentences get the polarity + slot rules only.
    A token fires only when ALL predicates it aligns to are strictly (UP/DOWN) opposite to the expectation;
    NONMONO/UNKNOWN/VACUOUS never fire. A mismatch involving negation (text token negated, or the aligned predicate's
    occurrence locally negated) is counted as pol_flip, otherwise as a role error."""
    e = parse(fol) if isinstance(fol, str) else fol
    prof = prof if prof is not None else formula_role_profile(e)
    tr = text_roles(text)
    res = {"cond_in_up": 0, "assert_in_down": 0, "pol_flip": 0, "slot_swap": 0, "exc_wrong": 0,
           "n_role_words": len(tr["tokens"]), "n_resolved": 0, "generic": tr["generic"], "codes": []}
    for t in tr["tokens"]:
        al = _align_token(t, prof)
        if not al:
            continue
        res["n_resolved"] += 1
        exp = _expected(t["role"], t["neg"])
        if exp is None:
            continue
        monos = [prof[k]["mono"] for k in al]
        if not all(m in ("UP", "DOWN") for m in monos):
            continue
        opp = "UP" if exp == "DOWN" else "DOWN"
        if not all(m == opp for m in monos):
            continue
        neg_involved = t["neg"] or any(prof[k]["local_neg"] for k in al)
        if not tr["generic"]:
            if neg_involved:
                res["pol_flip"] += 1
            continue
        if neg_involved:
            res["pol_flip"] += 1
        elif t["role"] == "condition":
            res["cond_in_up"] += 1
        elif t["role"] == "asserted":
            res["assert_in_down"] += 1
        else:
            res["exc_wrong"] += 1
    # slot order of binary predicates
    doc = tr["doc"]
    binp = {k: p for k, p in prof.items() if p["arity"] == 2}
    if binp:
        for v in doc:
            if v.pos_ not in ("VERB", "AUX", "ADJ", "NOUN"):
                continue
            subj = [c for c in v.children if c.dep_ in ("nsubj", "nsubjpass")]
            if not subj:
                continue
            s = subj[0]
            passive = s.dep_ == "nsubjpass"
            if s.lower_ in ("who", "that", "which") and v.dep_ == "relcl":
                s = v.head
            objs = [c for c in v.children if c.dep_ in ("dobj", "attr", "dative")]
            agent = None
            for c in v.children:
                if c.dep_ in ("prep", "agent"):
                    po = [g for g in c.children if g.dep_ == "pobj"]
                    if po:
                        if c.lower_ == "by" and passive:
                            agent = po[0]
                        else:
                            objs.append(po[0])
            if passive:
                lsubj, lobj = agent, s
            else:
                lsubj, lobj = s, (objs[0] if objs else None)
            if lsubj is None or lobj is None:
                continue
            vt = {"w": v.lower_, "lemma": v.lemma_.lower()}
            for k in _align_token(vt, binp):
                p = binp[k]

                def slot_hit(tok, slot):
                    kind, val = slot
                    if val is None:
                        return False
                    if kind == "const":
                        return const_match(_phrase_words_of(tok), val) or const_match([tok.text], val)
                    return any(word_match(tok.lower_, pw) or word_match(tok.lemma_.lower(), pw)
                               for pw in name_words(val))
                s0, s1 = slot_hit(lsubj, p["slots"][0]), slot_hit(lsubj, p["slots"][1])
                o0, o1 = slot_hit(lobj, p["slots"][0]), slot_hit(lobj, p["slots"][1])
                if s1 and not s0 and o0 and not o1:
                    res["slot_swap"] += 1
    codes = []
    for c, lab in (("cond_in_up", "RESTR"), ("assert_in_down", "REV"), ("pol_flip", "NEG"), ("slot_swap", "SWAP"),
                   ("exc_wrong", "EXC")):
        if res[c]:
            codes.append(c)
    res["codes"] = codes
    res["count"] = res["cond_in_up"] + res["assert_in_down"] + res["pol_flip"] + res["slot_swap"] + res["exc_wrong"]
    res["flag"] = res["count"] >= 1
    return res


# =============================================================================================== L3 questionnaire
L3_SCHEMA_TEXT = """{"concepts": [{"id": "c1", "phrase": "<exact words copied from the sentence>", "role": "condition" | "asserted" | "background", "negated": true | false, "exception": true | false, "force": "all" | "some" | "named" | "none", "claim": <int>}], "relations": [{"phrase": "<verb or relational words>", "first": "<concept id>", "second": "<concept id>"}]}"""

L3_SYSTEM = """You analyse the logical structure of ONE English sentence. You never see any formula. Return ONLY a JSON object with this schema:
""" + L3_SCHEMA_TEXT + """

Field definitions:
- concepts: every property, class, action, relation word-group or named individual the sentence talks about. "phrase" = the SHORTEST span of the sentence's own words naming it (e.g. "barks", "dog", "loud", "chases", "Mia"). Relation verbs are concepts too.
- role: "condition" = restricts WHO/WHEN the statement applies to (subject class of a general statement such as "every dog", words inside a relative clause on that subject, an if/when clause, the restricting part of an "only ... if"); "asserted" = what the sentence claims holds (main predicate, the then-part); "background" = named individuals, or words that are neither.
- negated: true if the sentence says the concept does NOT hold (not, never, no, none, cannot) for it, taken literally where it appears. For "No A is B", A is a condition with negated=false and B is asserted with negated=true.
- exception: true only for concepts introduced by unless / except / other than / without / but not.
- force: how the thing the concept is said of is quantified: "all" (every, all, any, bare plural generic, if-something), "some" (some, a certain, there is, at least one), "named" (said of a named individual), "none" (does not apply).
- claim: statements that could be true or false independently get different integers (1, 2, ...); concepts of the same statement share the claim number.
- relations: for every two-place relation, "first" is the concept id of the one who DOES / HAS the relation (logical subject, also in passive voice: "X is liked by Y" -> first = Y), "second" is the one it is done to. A named individual is its own concept.

Worked examples (not from any benchmark):
1. "Every dog that barks is loud unless it is asleep."
{"concepts":[{"id":"c1","phrase":"dog","role":"condition","negated":false,"exception":false,"force":"all","claim":1},{"id":"c2","phrase":"barks","role":"condition","negated":false,"exception":false,"force":"all","claim":1},{"id":"c3","phrase":"loud","role":"asserted","negated":false,"exception":false,"force":"all","claim":1},{"id":"c4","phrase":"asleep","role":"condition","negated":false,"exception":true,"force":"all","claim":1}],"relations":[]}
2. "No teacher who owns a bicycle drives to work."
{"concepts":[{"id":"c1","phrase":"teacher","role":"condition","negated":false,"exception":false,"force":"all","claim":1},{"id":"c2","phrase":"owns","role":"condition","negated":false,"exception":false,"force":"all","claim":1},{"id":"c3","phrase":"bicycle","role":"condition","negated":false,"exception":false,"force":"some","claim":1},{"id":"c4","phrase":"drives to work","role":"asserted","negated":true,"exception":false,"force":"all","claim":1}],"relations":[{"phrase":"owns","first":"c1","second":"c3"}]}
3. "Mia is not a painter, and Leo admires Mia."
{"concepts":[{"id":"c1","phrase":"Mia","role":"background","negated":false,"exception":false,"force":"named","claim":1},{"id":"c2","phrase":"painter","role":"asserted","negated":true,"exception":false,"force":"named","claim":1},{"id":"c3","phrase":"Leo","role":"background","negated":false,"exception":false,"force":"named","claim":2},{"id":"c4","phrase":"admires","role":"asserted","negated":false,"exception":false,"force":"named","claim":2}],"relations":[{"phrase":"admires","first":"c3","second":"c1"}]}
4. "Some kettles are made of copper, and if a kettle is made of copper then it is heavy."
{"concepts":[{"id":"c1","phrase":"kettles","role":"asserted","negated":false,"exception":false,"force":"some","claim":1},{"id":"c2","phrase":"made of copper","role":"asserted","negated":false,"exception":false,"force":"some","claim":1},{"id":"c3","phrase":"kettle","role":"condition","negated":false,"exception":false,"force":"all","claim":2},{"id":"c4","phrase":"made of copper","role":"condition","negated":false,"exception":false,"force":"all","claim":2},{"id":"c5","phrase":"heavy","role":"asserted","negated":false,"exception":false,"force":"all","claim":2}],"relations":[]}
Output the JSON object only, compact on ONE line (no indentation, no newlines)."""

L3_JSON_SCHEMA = {
    "type": "object",
    "properties": {
        "concepts": {"type": "array", "items": {"type": "object", "properties": {
            "id": {"type": "string"}, "phrase": {"type": "string"},
            "role": {"type": "string", "enum": ["condition", "asserted", "background"]},
            "negated": {"type": "boolean"}, "exception": {"type": "boolean"},
            "force": {"type": "string", "enum": ["all", "some", "named", "none"]}, "claim": {"type": "integer"}},
            "required": ["id", "phrase", "role", "negated", "exception", "force", "claim"]}},
        "relations": {"type": "array", "items": {"type": "object", "properties": {
            "phrase": {"type": "string"}, "first": {"type": "string"}, "second": {"type": "string"}},
            "required": ["phrase", "first", "second"]}}},
    "required": ["concepts", "relations"]}

ROLES = {"condition", "asserted", "background"}
FORCES = {"all", "some", "named", "none"}


def validate_questionnaire(js) -> dict:
    """Schema check (frozen). Raises ValueError on invalid structure; returns the normalised object."""
    if not isinstance(js, dict) or not isinstance(js.get("concepts"), list):
        raise ValueError("no concepts list")
    ids = set()
    cs = []
    for c in js["concepts"]:
        if not isinstance(c, dict) or not isinstance(c.get("phrase"), str):
            raise ValueError("bad concept")
        role = str(c.get("role", "")).lower()
        force = str(c.get("force", "")).lower()
        if role not in ROLES or force not in FORCES:
            raise ValueError(f"bad role/force {role}/{force}")
        cid = str(c.get("id", f"c{len(cs) + 1}"))
        ids.add(cid)
        try:
            claim = int(c.get("claim", 1))
        except (TypeError, ValueError):
            claim = 1
        cs.append({"id": cid, "phrase": c["phrase"], "role": role, "negated": bool(c.get("negated", False)),
                   "exception": bool(c.get("exception", False)), "force": force, "claim": claim})
    rels = []
    for r in js.get("relations", []) or []:
        if isinstance(r, dict) and str(r.get("first")) in ids and str(r.get("second")) in ids:
            rels.append({"phrase": str(r.get("phrase", "")), "first": str(r["first"]), "second": str(r["second"])})
    return {"concepts": cs, "relations": rels}


def parse_json_text(t: str):
    t = t.strip()
    if t.startswith("```"):
        t = re.sub(r"^```(?:json)?", "", t).rstrip("`").strip()
    try:
        return json.loads(t)
    except json.JSONDecodeError:
        m = re.search(r"\{.*\}", t, re.S)
        if m:
            return json.loads(m.group(0))
        raise


L3_SYSTEM_V0 = L3_SYSTEM.replace(", compact on ONE line (no indentation, no newlines).", ".")  # prompt used by the
# OpenRouter flash-lite calls made before the key hit its daily limit (T5 + dry run); kept to read those cached answers


async def role_questionnaire(text: str, llm, model: str, tag: str = "L3", system: str | None = None) -> dict:
    """L3 text side (TEXT ONLY; the formula is never in the prompt). -> {'q': validated schema | None,
    'coverage_status': 'OK' | 'L3_FAIL', 'cost_usd', 'secs', 'tries'}. Up to 2 retries on invalid JSON."""
    cost = secs = 0.0
    for attempt in range(3):
        r = await llm.chat_json(model, system or L3_SYSTEM, f"Sentence: {text}", temperature=0.0, max_tokens=900,
                                tag=f"{tag}#{attempt}", schema=L3_JSON_SCHEMA)
        cost += r["cost_usd"] if not r["cached"] else 0.0
        secs += r["secs"]
        try:
            q = validate_questionnaire(parse_json_text(r["text"]))
            return {"q": q, "coverage_status": "OK", "cost_usd": r["cost_usd"] if attempt == 0 else cost,
                    "secs": secs, "tries": attempt + 1, "cached": r["cached"]}
        except (ValueError, json.JSONDecodeError):
            continue
    return {"q": None, "coverage_status": "L3_FAIL", "cost_usd": cost, "secs": secs, "tries": 3}


# =============================================================================================== L3 compare
def phrase_words(phrase: str) -> list[str]:
    ws = re.findall(r"[A-Za-z]+|\d+", phrase)
    return [w.lower() for w in ws if w.lower() not in ca.FUNC and w.lower() not in ca.HEDGE and len(w) > 1
            and w.lower() not in LOGIC_WORDS] or [w.lower() for w in ws if len(w) > 1][:1]


def align_concepts(q: dict, prof: dict, exact: bool = False) -> dict:
    """concept id -> ('pred', key) | ('const', name) | None.  Predicate match: overlap coefficient of phrase content
    words vs predicate-name words (match = same stem or WordNet link; exact=True -> stem only) >= 0.5, ties broken by
    Jaccard; named individuals may match a constant by normalised string."""
    consts = sorted({s[1] for p in prof.values() for s in p["slots"] if s[0] == "const"})
    out = {}
    for c in q["concepts"]:
        pw = phrase_words(c["phrase"])
        best, bs = None, (0.0, 0.0)
        if c["force"] == "named" or c["role"] == "background":
            for k in consts:
                if const_match(re.findall(r"[A-Za-z0-9]+", c["phrase"]), k):
                    best = ("const", k)
                    break
            if best:
                out[c["id"]] = best
                continue
        for k, p in prof.items():
            nw = name_words(p["name"])
            if not nw or not pw:
                continue
            m_p = sum(any(word_match(w, x, exact) for w in pw) for x in nw)
            m_t = sum(any(word_match(w, x, exact) for x in nw) for w in pw)
            m = min(m_p, m_t) if min(m_p, m_t) > 0 else 0
            if m == 0:
                continue
            ov = m / min(len(nw), len(pw))
            jac = m / (len(nw) + len(pw) - m)
            if ov >= 0.5 and (ov, jac) > bs:
                best, bs = ("pred", k), (ov, jac)
        out[c["id"]] = best
    return out


def _rand_index(a: list, b: list) -> float | None:
    n = len(a)
    if n < 2:
        return None
    agree = tot = 0
    for i, j in itertools.combinations(range(n), 2):
        tot += 1
        agree += (a[i] == a[j]) == (b[i] == b[j])
    return agree / tot


def expected_mono(role: str, negated: bool, exception: bool) -> str | None:
    if role == "background":
        return None
    base = "DOWN" if role == "condition" else "UP"
    if exception:
        base = "UP"
    if negated:
        base = "UP" if base == "DOWN" else "DOWN"
    return base


L3_FIELDS = ["mm_role", "mm_force", "mm_claims", "mm_order", "mm_exception", "missing_frac", "extra_frac"]


def l3_compare(q: dict, prof: dict, exact: bool = False) -> dict:
    """Per-field mismatch between the text questionnaire q and a formula profile (z3 or LLM-read).
    Returns fractions in [0,1] (None when the field has no applicable concept) plus counts and alignment stats."""
    al = align_concepts(q, prof, exact)
    cons = {c["id"]: c for c in q["concepts"]}
    role_n = role_bad = force_n = force_bad = exc_n = exc_bad = 0
    tp, fp_ = [], []
    for c in q["concepts"]:
        a = al.get(c["id"])
        if not a or a[0] != "pred":
            continue
        p = prof[a[1]]
        exp = expected_mono(c["role"], c["negated"], c["exception"])
        if exp is not None and p["mono"] in ("UP", "DOWN"):
            role_n += 1
            role_bad += exp != p["mono"]
        if c["force"] in ("all", "some", "named") and p["force"] in ("all", "some", "named"):
            force_n += 1
            force_bad += c["force"] != p["force"]
        if c["exception"]:
            exc_n += 1
            ok = p["mono"] == "UP" or (p["pos"] == "antecedent" and p["local_neg"])
            exc_bad += not ok
        tp.append(c["claim"]); fp_.append(p["claim"])
    ri = _rand_index(tp, fp_)
    ord_n = ord_bad = 0
    for r in q["relations"]:
        rc = {"id": "_r", "phrase": r["phrase"], "role": "asserted", "force": "all", "negated": False, "exception": False,
              "claim": 0}
        ra = align_concepts({"concepts": [rc]}, {k: v for k, v in prof.items() if v["arity"] == 2}, exact).get("_r")
        if not ra:
            continue
        p = prof[ra[1]]
        a1, a2 = al.get(r["first"]), al.get(r["second"])

        def hit(aa, slot):
            if not aa or slot[1] is None:
                return False
            if aa[0] == "const":
                return slot == ("const", aa[1])
            return slot[0] == "var" and prof.get(aa[1], {}).get("name") == slot[1]
        s = p["slots"]
        f0, f1 = hit(a1, s[0]), hit(a1, s[1])
        g0, g1 = hit(a2, s[0]), hit(a2, s[1])
        if (f0 or g1) and not (f1 and g0):
            ord_n += 1
        elif f1 and g0 and not (f0 or g1):
            ord_n += 1
            ord_bad += 1
    need = [c for c in q["concepts"] if c["role"] in ("condition", "asserted")]
    missing = sum(1 for c in need if not al.get(c["id"]))
    matched_preds = {a[1] for a in al.values() if a and a[0] == "pred"}
    extra_keys = [k for k, p in prof.items() if k not in matched_preds
                  and not any(w in ca.SORTAL for w in name_words(p["name"])) and name_words(p["name"])]
    out = {
        "mm_role": role_bad / role_n if role_n else None,
        "mm_force": force_bad / force_n if force_n else None,
        "mm_claims": (1 - ri) if ri is not None else None,
        "mm_order": ord_bad / ord_n if ord_n else None,
        "mm_exception": exc_bad / exc_n if exc_n else None,
        "missing_frac": missing / len(need) if need else None,
        "extra_frac": len(extra_keys) / len(prof) if prof else None,
        "n_concepts": len(q["concepts"]), "n_aligned": sum(1 for a in al.values() if a),
        "n_role": role_n, "n_force": force_n, "n_order": ord_n, "n_exc": exc_n, "n_missing": missing,
        "n_extra": len(extra_keys), "extra_keys": extra_keys, "n_need": len(need),
        "n_pred_eval": sum(1 for k, p in prof.items() if not any(w in ca.SORTAL for w in name_words(p["name"]))
                           and name_words(p["name"])),
    }
    return out


def l3_score(cmp: dict, gated: list[str]) -> float:
    """Sum of the gated field mismatches (weights frozen = 1; each field already a fraction; None -> 0)."""
    return float(sum((cmp.get(f) or 0.0) for f in gated))


# =============================================================================================== decomposed judge
DJ_SYSTEM = """You read a first-order-logic formula together with the English sentence it is meant to translate. Describe what THE FORMULA states (not what the sentence says). Return ONLY JSON:
{"predicates": [{"predicate": "<predicate name exactly as in the formula>", "role": "condition" | "asserted" | "background", "negated": true | false, "force": "all" | "some" | "named" | "none", "claim": <int>, "args": ["<for each argument: the name of the predicate that restricts that variable, or the constant name>"]}]}
Definitions (formula side): role "condition" = the predicate restricts when the formula applies (sits in an antecedent / restrictor, e.g. left of →), "asserted" = the formula claims it (consequent, or a plain conjunct); negated = the predicate appears under ¬ within its antecedent/consequent; force = quantifier binding its argument ("all" for ∀, "some" for ∃, "named" for constants only); claim = independent top-level statements get different integers; args = for each argument position, the restricting predicate of that variable (or the constant). One entry per distinct predicate. Output JSON only, compact on ONE line."""

DJ_JSON_SCHEMA = {
    "type": "object",
    "properties": {"predicates": {"type": "array", "items": {"type": "object", "properties": {
        "predicate": {"type": "string"}, "role": {"type": "string", "enum": ["condition", "asserted", "background"]},
        "negated": {"type": "boolean"}, "force": {"type": "string", "enum": ["all", "some", "named", "none"]},
        "claim": {"type": "integer"}, "args": {"type": "array", "items": {"type": "string"}}},
        "required": ["predicate", "role", "negated", "force", "claim", "args"]}}},
    "required": ["predicates"]}


async def decomposed_profile(text: str, fol: str, llm, model: str) -> dict:
    """Ablation: the same LLM reads the FORMULA and answers the role schema -> LLM formula profile (same keys as
    formula_role_profile: mono derived from (role, negated), force, claim, slots)."""
    e = parse(fol)
    ar = preds(e)
    for attempt in range(3):
        r = await llm.chat_json(model, DJ_SYSTEM, f"Sentence: {text}\nFormula: {fol}", temperature=0.0, max_tokens=900,
                                tag=f"DJ#{attempt}", schema=DJ_JSON_SCHEMA)
        try:
            js = parse_json_text(r["text"])
            lst = js["predicates"]
            out = {}
            for p in lst:
                nm = str(p.get("predicate", "")).split("(")[0].strip()
                keys = [k for k in ar if k.split("/")[0] == nm]
                if not keys:
                    continue
                k = keys[0]
                role = str(p.get("role", "")).lower()
                neg = bool(p.get("negated", False))
                exp = expected_mono(role if role in ROLES else "background", neg, False)
                args = p.get("args", []) or []
                slots = []
                for i in range(ar[k]):
                    a = str(args[i]) if i < len(args) else ""
                    a = a.split("(")[0].strip()
                    if any(kk.split("/")[0] == a for kk in ar):
                        slots.append(("var", a))
                    elif a:
                        slots.append(("const", a))
                    else:
                        slots.append(("var", None))
                force = str(p.get("force", "none")).lower()
                try:
                    claim = int(p.get("claim", 1))
                except (TypeError, ValueError):
                    claim = 1
                out[k] = {"mono": exp or "UNKNOWN", "role_raw": role, "local_neg": neg, "force": force,
                          "claim": claim, "slots": slots, "name": k.split("/")[0], "arity": ar[k],
                          "pos": "antecedent" if role == "condition" else "consequent"}
            for k in ar:  # predicates the LLM skipped: unknown
                out.setdefault(k, {"mono": "UNKNOWN", "role_raw": None, "local_neg": False, "force": "none",
                                   "claim": -1, "slots": [("var", None)] * ar[k], "name": k.split("/")[0],
                                   "arity": ar[k], "pos": "consequent", "skipped": True})
            return {"profile": out, "cost_usd": r["cost_usd"], "status": "OK", "cached": r["cached"]}
        except (ValueError, KeyError, TypeError, json.JSONDecodeError):
            continue
    return {"profile": None, "cost_usd": 0.0, "status": "DJ_FAIL"}


# =============================================================================================== cascade
ERROR_CODE = {"EX_IMP": "RESTR", "ALL_AND": "RESTR", "IFF_RESTR": "CONN", "GLUE": "UNGLUE", "FREE": "BIND",
              "ARITY": "BIND", "DANGLING": "BIND", "VACUOUS": "DROP", "TRIVIAL": "COMPOUND", "unanchored": "ADD",
              "uncarried": "DROP", "cond_in_up": "RESTR", "assert_in_down": "REV", "pol_flip": "NEG",
              "slot_swap": "SWAP", "exc_wrong": "RESTR", "mm_force": "QUANT", "mm_claims": "UNGLUE", "mm_role": "REV",
              "mm_order": "SWAP", "mm_exception": "RESTR", "missing_frac": "DROP", "extra_frac": "ADD"}
