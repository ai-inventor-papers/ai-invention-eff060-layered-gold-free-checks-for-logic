"""Lints over record_final.md. The run fails if any fires. Each lint encodes a misreading the
iteration-4 review found (held-out E; recall without base FA; FA without flip; 0.683 as AUROC;
re-typed CIs; costs without units; markers pointing at missing files; untraced numbers)."""
from __future__ import annotations

import re
from pathlib import Path

TAG = r"<!-- n:([A-Za-z0-9_]+) -->"


def _unstruck(text: str) -> str:
    """Remove struck originals (~~...~~), backticked spans, verbatim-tagged rows and HTML tags."""
    t = re.sub(r"~~.*?~~", " ", text, flags=re.S)
    t = re.sub(r"```.*?```", " ", t, flags=re.S)
    t = re.sub(r"`[^`\n]*`", " ", t)
    return t


def _lines_no_verbatim(text: str) -> list[tuple[int, str]]:
    out = []
    for i, ln in enumerate(text.splitlines(), 1):
        if "<!-- v:" in ln and "<!-- n:" not in ln:
            continue
        # strip verbatim segments inside a line: "..."<!-- v:x -->
        ln = re.sub(r'"[^"]*"<!-- v:[^>]+-->', " ", ln)
        ln = re.sub(r"[^|]*<!-- v:[^>]+-->", " ", ln)
        out.append((i, ln))
    return out


def lint_all(md: str, numbers: dict[str, dict]) -> list[dict]:
    fails: list[dict] = []
    clean_lines = [(i, _unstruck(ln)) for i, ln in _lines_no_verbatim(md)]

    # L1 no 'held-out' within 60 chars of E
    for i, ln in clean_lines:
        for m in re.finditer(r"held-out", ln, flags=re.I):
            ctx = ln[max(0, m.start() - 60): m.end() + 60]
            if re.search(r"\bE\b|dataset E", ctx):
                fails.append(dict(lint="held_out_E", line=i, text=ctx.strip()))

    # L2 every decimal / % / $ number traces to a numbers.csv row (tag directly after it)
    for i, ln in clean_lines:
        if re.match(r"^#+ ", ln):
            ln = re.sub(r"^#+\s*[\d.]+", "", ln)
        ln2 = re.sub(r"§\s?\d+(?:\.\d+)*", " ", ln)
        ln2 = re.sub(r"95% (CI|bar)", " ", ln2)
        ln2 = re.sub(r"(?:L|lines? )\d+(?:-\d+)?", " ", ln2)
        ln2 = re.sub(r"\d{4}-\d\d-\d\dT[\d:+.]+", " ", ln2)  # timestamps in the method line
        for m in re.finditer(r"[+−-]?\$?\d+\.\d+(?:e[−-]?\d+)?%?|\d+%", ln2):
            tail = ln2[m.end(): m.end() + 60]
            # allowed if a tag follows before the next whitespace-separated token that is not part of a CI/× suffix
            if re.match(r"(?:\]|\s?\[[^\]]*\]|×|\)|%)*\s?<!-- n:", tail) or re.match(r"[^<\n]{0,40}\]<!-- n:", tail):
                continue
            fails.append(dict(lint="untraced_number", line=i, text=ln2[max(0, m.start() - 40): m.end() + 40].strip()))

    # L3 recall number in §4.3 section (section 10) must have 'base FA' in the same row/sentence
    sec = re.search(r"## 10\..*?(?=\n## 11\.)", md, flags=re.S)
    if sec:
        body = _unstruck(sec.group(0))
        for unit in re.split(r"(?<=[.!?])\s+|\n", body):
            if re.search(r"recall[^|\n]{0,20}\d", unit, flags=re.I) and "base FA" not in unit and "recall ≈" not in unit:
                fails.append(dict(lint="recall_without_base_FA", line=None, text=unit[:160]))

    # L4 FA for a rename control must come with flip
    for i, ln in clean_lines:
        for unit in re.split(r"(?<=[.;])\s+", ln):
            if re.search(r"RENAME_(SYN|NONCE)|rename control", unit) and re.search(r"\bFA\b", unit) and "flip" not in unit.lower():
                fails.append(dict(lint="rename_FA_without_flip", line=i, text=unit[:160]))

    # L5 no 0.683 adjacent to AUROC
    for i, ln in clean_lines:
        for m in re.finditer(r"0\.683", ln):
            if re.search(r"AUROC", ln[max(0, m.start() - 40): m.end() + 40]):
                fails.append(dict(lint="0683_as_AUROC", line=i, text=ln[max(0, m.start() - 40): m.end() + 40]))

    # L6 every CI string equals numbers.csv source_ci byte-for-byte
    for i, ln in enumerate(md.splitlines(), 1):
        for m in re.finditer(r"(\[[^\[\]]+\])" + TAG, ln):
            ci, rid = m.group(1), m.group(2)
            if rid not in numbers:
                fails.append(dict(lint="unknown_row", line=i, text=rid))
            elif numbers[rid].get("source_ci") != ci:
                fails.append(dict(lint="ci_not_verbatim", line=i, text=f"{rid}: {ci} vs {numbers[rid].get('source_ci')}"))
        for m in re.finditer(TAG, ln):
            if m.group(1) not in numbers:
                fails.append(dict(lint="unknown_row", line=i, text=m.group(1)))

    # L7 every $ amount carries a unit token nearby (per item/candidate/sentence/call, total, spend, budget)
    unit_re = r"per (item|candidate|sentence|call|item-call)|/candidate|/sentence|total|spend|budget|window|unaccounted|FULL|MARGINAL|projection|evidenced|artifacts|dataset|exp \d|in window"
    for i, ln in clean_lines:
        for m in re.finditer(r"\$\d", ln):
            ctx = ln[max(0, m.start() - 120): m.end() + 120]
            if ln.startswith("|") or re.search(unit_re, ctx):
                continue
            fails.append(dict(lint="cost_without_unit", line=i, text=ctx.strip()[:160]))

    # L8 every [Correction marker names an existing absolute path
    for i, ln in enumerate(md.splitlines(), 1):
        for m in re.finditer(r"\[Correction, iter 4: .*?; source (\S+?)\](?: \(|$)", ln):
            p = m.group(1)
            if not (p.startswith("/") and Path(p).exists()):
                fails.append(dict(lint="marker_path_missing", line=i, text=p))
    return fails
