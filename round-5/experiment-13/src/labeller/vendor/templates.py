"""The 9 R_COMP templates. Each fills English text AND derives the weak / strong (/ converse) FOL readings
compositionally from the same slots, so the reference is correct by construction given a correct atom lexicon.

Slot = dict(pred=..., atom=<FOL atom over x>, vp=<3sg verb phrase>, neg=<bool>) for conditions C1..C3;
Q (consequent), E (exception) and P (proviso) are positive slots; N is the sortal noun with its FOL atom S.
Readings (A_i = condition literal, S = sortal atom):
  T1/T2/T4/T5/T6 weak  ∀x (S ∧ A1 ∧ A2 ∧ A3 ∧ ¬E → Q)        strong ∀x (S ∧ A1 ∧ A2 ∧ A3 → (Q ↔ ¬E))
  T3             weak  ∀x (S ∧ A1 ∧ A2 ∧ P ∧ A3 → Q)         strong ∀x (S ∧ A1 ∧ A2 → (Q ↔ (P ∧ A3)))
  T7 (no S)      weak  ∀x (A1 ∧ A2 ∧ A3 ∧ ¬E → Q)            strong ∀x (A1 ∧ A2 ∧ A3 → (Q ↔ ¬E))
  T8             weak  ∀x (S ∧ A1 ∧ A2 ∧ A3 ∧ Q → P)         strong ∀x (S ∧ A1 ∧ A2 ∧ A3 → (Q ↔ P))
                 converse (stored, NOT accepted) ∀x (S ∧ A1 ∧ A2 ∧ A3 ∧ P → Q)
  T9             weak  ∀x (S ∧ A1 ∧ A2 ∧ A3 ∧ ¬E → ¬Q)       strong ∀x (S ∧ A1 ∧ A2 ∧ A3 → (¬Q ↔ ¬E))
"""
from __future__ import annotations

import re

TEMPLATES = ["T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9"]
CLAUSE = {"T1": "unless", "T2": "except_when", "T3": "provided_that", "T4": "as_long_as+unless",
          "T5": "provided_that+unless", "T6": "except_when+provided_that", "T7": "unless", "T8": "but_only_if",
          "T9": "unless"}
NESTED = {"T4": False, "T5": True, "T6": False}
USES_E = {"T1", "T2", "T4", "T5", "T6", "T7", "T9"}
USES_P = {"T3", "T8"}


def lit(s: dict) -> str:
    return ("¬" if s.get("neg") else "") + s["atom"]


def cvp(s: dict) -> str:
    return s["neg_vp"] if s.get("neg") else s["vp"]


def art(noun: str) -> str:
    return "an" if re.match(r"[aeiou]", noun.lower()) else "a"


def conj(*xs: str) -> str:
    return " ∧ ".join(xs)


def plural_vp(vp: str) -> str | None:
    """Re-inflect a 3sg verb phrase for 'they' by a fixed table: is->are, has->have, does->do, -s stripping."""
    w = vp.split()
    if not w:
        return None
    f = w[0].lower()
    table = {"is": "are", "has": "have", "does": "do", "was": "were", "isn't": "aren't", "doesn't": "don't",
             "hasn't": "haven't"}
    if f in table:
        w[0] = table[f]
    elif f in ("can", "cannot", "can't", "will", "won't", "may", "might", "must", "should", "would", "could"):
        pass
    elif re.fullmatch(r"[a-z]+ies", f) and len(f) > 4:
        w[0] = f[:-3] + "y"
    elif re.fullmatch(r"[a-z]+(ches|shes|sses|xes|zzes|oes)", f):
        w[0] = f[:-2]
    elif re.fullmatch(r"[a-z]+s", f) and not f.endswith("ss"):
        w[0] = f[:-1]
    else:
        return None
    return " ".join(w)


def fill(t: str, v: int, N: str, S: str, C: list[dict], Q: dict, X: dict | None, person: bool) -> dict:
    """t template id, v lexical variant (0/1), N noun, S sortal atom, C 3 condition slots, Q consequent,
    X exception (E) or proviso (P) slot. Returns text + readings."""
    rel = "who" if person else "that"
    c1, c2, c3 = (cvp(c) for c in C)
    a1, a2, a3 = (lit(c) for c in C)
    q, qa = Q["vp"], Q["atom"]
    x, xa = (X["vp"], X["atom"]) if X else (None, None)
    the = f"the {N}"
    conv = None
    if t == "T1":
        det, exc = ("Every", "unless") if v == 0 else ("Each", "except if")
        text = f"{det} {N} {rel} {c1}, {rel} {c2}, and {rel} {c3} {q}, {exc} {the} {x}."
        weak = f"∀x ({conj(S, a1, a2, a3, '¬' + xa)} → {qa})"
        strong = f"∀x ({conj(S, a1, a2, a3)} → ({qa} ↔ ¬{xa}))"
    elif t == "T2":
        if v == 0:
            text = f"If {art(N)} {N} {c1} and {c2}, and {the} also {c3}, then {the} {q}, except when {the} {x}."
        else:
            text = f"When {art(N)} {N} {c1} and {c2}, and {the} also {c3}, {the} {q}, except when {the} {x}."
        weak = f"∀x ({conj(S, a1, a2, a3, '¬' + xa)} → {qa})"
        strong = f"∀x ({conj(S, a1, a2, a3)} → ({qa} ↔ ¬{xa}))"
    elif t == "T3":
        det, prov = ("Any", "provided that") if v == 0 else ("Every", "providing that")
        text = f"{det} {N} that {c1} and that {c2} {q}, {prov} {the} {x} and {c3}."
        weak = f"∀x ({conj(S, a1, a2, xa, a3)} → {qa})"
        strong = f"∀x ({conj(S, a1, a2)} → ({qa} ↔ ({xa} ∧ {a3})))"
    elif t == "T4":
        al = "as long as" if v == 0 else "so long as"
        text = f"{art(N).capitalize()} {N} {rel} {c1} and {rel} {c2} {q} {al} {the} {c3}, unless {the} {x}."
        weak = f"∀x ({conj(S, a1, a2, a3, '¬' + xa)} → {qa})"
        strong = f"∀x ({conj(S, a1, a2, a3)} → ({qa} ↔ ¬{xa}))"
    elif t == "T5":
        det, exc = ("Every", "unless") if v == 0 else ("Each", "except if")
        text = f"{det} {N} {rel} {c1} and {rel} {c2} {q}, provided that {the} {c3}, {exc} {the} {x}."
        weak = f"∀x ({conj(S, a1, a2, a3, '¬' + xa)} → {qa})"
        strong = f"∀x ({conj(S, a1, a2, a3)} → ({qa} ↔ ¬{xa}))"
    elif t == "T6":
        exc, det = ("Except when", "every") if v == 0 else ("Except if", "each")
        text = f"{exc} {the} {x}, {det} {N} {rel} {c1} and {rel} {c2} {q}, provided that {the} {c3}."
        weak = f"∀x ({conj(S, a1, a2, a3, '¬' + xa)} → {qa})"
        strong = f"∀x ({conj(S, a1, a2, a3)} → ({qa} ↔ ¬{xa}))"
    elif t == "T7":
        who = "Anyone" if v == 0 else "Anybody"
        px = plural_vp(x)
        if px is None:
            return None
        text = f"{who} who {c1}, {c2}, and {c3} {q} unless they {px}."
        weak = f"∀x ({conj(a1, a2, a3, '¬' + xa)} → {qa})"
        strong = f"∀x ({conj(a1, a2, a3)} → ({qa} ↔ ¬{xa}))"
    elif t == "T8":
        if v == 0:
            text = f"If {art(N)} {N} {c1}, {c2}, and {c3}, then {the} {q}, but only if {the} {x}."
        else:
            text = f"When {art(N)} {N} {c1}, {c2}, and {c3}, {the} {q}, but only if {the} {x}."
        weak = f"∀x ({conj(S, a1, a2, a3, qa)} → {xa})"
        strong = f"∀x ({conj(S, a1, a2, a3)} → ({qa} ↔ {xa}))"
        conv = f"∀x ({conj(S, a1, a2, a3, xa)} → {qa})"
    elif t == "T9":
        rel9 = rel if v == 0 else "that"
        exc = "unless" if v == 0 else "except when"
        text = f"No {N} {rel9} {c1}, {rel9} {c2}, and {rel9} {c3} {q}, {exc} {the} {x}."
        weak = f"∀x ({conj(S, a1, a2, a3, '¬' + xa)} → ¬{qa})"
        strong = f"∀x ({conj(S, a1, a2, a3)} → (¬{qa} ↔ ¬{xa}))"
    else:
        raise ValueError(t)
    text = re.sub(r"\s+", " ", text)
    return {"text": text[0].upper() + text[1:], "reference_fol_weak": weak, "reference_fol_strong": strong,
            "reading_converse": conv, "template_id": t, "surface_variant": f"{t}v{v}", "clause_type": CLAUSE[t],
            "nested": NESTED.get(t, False)}
