"""Uniform LLM-output normaliser (plan step 0d). No semantic repair: only surface syntax mapping.

normalise(raw) -> (formula_str, applied: list[str])
  strips code fences / 'FOL:' prefix; keeps the first formula line; unwraps LaTeX; maps ASCII
  connectives and quantifiers to the Unicode notation that labeller/fol.py parses.
"""
from __future__ import annotations

import re
import unicodedata

LATEX = [
    (r"\\text\{([^{}]*)\}", r"\1"), (r"\\mathrm\{([^{}]*)\}", r"\1"), (r"\\operatorname\{([^{}]*)\}", r"\1"),
    (r"\\forall\s*", "∀"), (r"\\exists\s*", "∃"), (r"\\land\b|\\wedge\b", "∧"), (r"\\lor\b|\\vee\b", "∨"),
    (r"\\neg\b|\\lnot\b", "¬"), (r"\\leftrightarrow\b|\\iff\b|\\Leftrightarrow\b", "↔"),
    (r"\\rightarrow\b|\\to\b|\\Rightarrow\b|\\implies\b", "→"), (r"\\oplus\b", "⊕"),
    (r"\\\(|\\\)|\\\[|\\\]|\$", ""), (r"\\[,;!: ]", " "),
]
WORDOPS = [
    (r"\bforall\s+([a-z][a-z0-9]*)\s*[.:]?", r"∀\1 "), (r"\ball\s+([a-z])\s*\.", r"∀\1 "),
    (r"\bexists\s+([a-z][a-z0-9]*)\s*[.:]?", r"∃\1 "), (r"\bexist\s+([a-z])\s*\.", r"∃\1 "),
    (r"<->|<=>|⟷|⇔|≡", "↔"), (r"->|=>|⟶|⇒|⊃", "→"), (r"&&|&", "∧"), (r"\|\||\|", "∨"),
    (r"\bxor\b|⊻", "⊕"), (r"\bnot\s+", "¬"), (r"[~!]|¬", "¬"), (r"\band\b", "∧"), (r"\bor\b", "∨"),
]


def normalise(raw: str | None) -> tuple[str, list[str]]:
    applied: list[str] = []
    if raw is None:
        return "", ["none"]
    s = raw.strip()
    if "```" in s:
        m = re.search(r"```(?:[a-zA-Z]*)\n?(.*?)```", s, re.S)
        if m:
            s = m.group(1).strip()
            applied.append("code_fence")
    m = re.search(r"FOL\s*[:：]\s*(.+)", s)
    if m:
        s = m.group(1)
        applied.append("fol_prefix")
    lines = [ln.strip() for ln in s.splitlines() if ln.strip()]
    if len(lines) > 1:
        applied.append("first_line")
    s = lines[0] if lines else ""
    if "\\" in s or "$" in s:
        for a, b in LATEX:
            s = re.sub(a, b, s)
        applied.append("latex")
    s2 = s
    for a, b in WORDOPS:
        s2 = re.sub(a, b, s2)
    if s2 != s:
        applied.append("ascii_ops")
    s = s2.strip().strip("`").strip()
    s = re.sub(r"\s+", " ", s).rstrip(".")
    folded = "".join(_fold(ch) for ch in s)
    if folded != s:
        applied.append("ascii_fold")
        s = folded
    return s, applied


def _fold(ch: str) -> str:
    """Diacritic folding of non-ASCII LETTERS only (Sūduva -> Suduva); logic symbols are untouched."""
    if ch.isascii() or not unicodedata.category(ch).startswith("L"):
        return ch
    base = "".join(c for c in unicodedata.normalize("NFKD", ch) if not unicodedata.combining(c))
    return base if base.isascii() and base else "_"
