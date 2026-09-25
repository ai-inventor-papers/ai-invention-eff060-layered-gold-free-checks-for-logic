"""Rendering context: every number in record_final.md comes from a numbers.csv row via these helpers."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from src import checker as CK
from src import io_locators as L


class Ctx:
    def __init__(self, rows: list[dict]):
        self.rows = rows
        self.r = {row["id"]: row for row in rows}
        self.markers: list[dict] = []
        self.used: set[str] = set()
        self.section = ""

    # ---- computed rows (values produced by this artifact's code from a file, e.g. counts, spend)
    def add(self, id: str, value: Any, fmt: str, locator: str, text: str, role: str = "DESCRIPTIVE") -> str:
        if id in self.r:
            return id
        raw = float(value) if isinstance(value, (int, float)) else value
        disp = CK.fmt_like(raw, fmt) if isinstance(raw, float) else str(raw)
        row = dict(id=id, sec="computed", text=text, value=None, ci=None, role=role, source_path=locator.split(" :: ")[0],
                   locator=locator, source_value=disp, source_ci="", match_hyp_vs_file="COMPUTED", paper_value="",
                   paper_line="", match_paper_vs_file="n/a", note="", source_value_raw=raw, source_ci_raw=None)
        self.rows.append(row)
        self.r[id] = row
        return id

    def _row(self, id: str) -> dict:
        if id not in self.r:
            raise KeyError(f"numbers.csv has no row {id}")
        self.used.add(id)
        return self.r[id]

    def v(self, id: str) -> str:
        row = self._row(id)
        return f"{row['source_value']}<!-- n:{id} -->"

    def ci(self, id: str) -> str:
        row = self._row(id)
        return f"{row['source_ci']}<!-- n:{id} -->"

    def vc(self, id: str) -> str:
        row = self._row(id)
        return f"{row['source_value']} {row['source_ci']}<!-- n:{id} -->"

    def ns(self, id: str) -> str:
        row = self._row(id)
        ci = row.get("source_ci_raw")
        if ci is None:
            return ""
        return " (n.s.: CI covers 0)" if ci[0] <= 0 <= ci[1] else ""

    def raw(self, id: str) -> Any:
        return self._row(id)["source_value_raw"]

    # ---- paper quoting and correction markers
    def find(self, pat: str, whole: bool = False, start_prefix: str | None = None) -> tuple[int, str]:
        lines = CK.paper_lines()
        lo, hi = CK.section_range(start_prefix) if start_prefix else (1, len(lines))
        for i in range(lo - 1, hi):
            m = re.search(pat, lines[i])
            if not m:
                continue
            ln = lines[i]
            if whole:
                return i + 1, ln.strip()
            # sentence containing the match: boundaries are '. ' / start / end of line
            s0 = max(ln.rfind(". ", 0, m.start()), ln.rfind("! ", 0, m.start()))
            s0 = 0 if s0 < 0 else s0 + 2
            e = re.search(r"[.!](?=\s|$)", ln[m.end():])
            e1 = len(ln) if not e else m.end() + e.end()
            sent = ln[s0:e1].strip()
            assert sent in ln, "quoted text must be verbatim"
            return i + 1, sent
        raise LookupError(f"paper pattern not found: {pat}")

    def strike(self, pat: str, what: str, src: str, whole: bool = False, start_prefix: str | None = None,
               critique: str = "") -> str:
        try:
            line, sent = self.find(pat, whole=whole, start_prefix=start_prefix)
        except LookupError:
            self.markers.append(dict(section=self.section, line=None, original="", what=what, source=src,
                                     critique=critique, status="ORIGINAL_NOT_FOUND"))
            return f"[Correction, iter 4: {what}; source {src}] (original sentence not found in paper_draft.md)"
        self.markers.append(dict(section=self.section, line=line, original=sent, what=what, source=src,
                                 critique=critique, status="OK"))
        return f"~~{sent}~~ [Correction, iter 4: {what}; source {src}] (paper_draft.md L{line})"

    def replaces(self, heading_prefix: str) -> str:
        lo, hi = CK.section_range(heading_prefix)
        head = CK.paper_lines()[lo - 1].strip()
        return f"Replaces: paper_draft.md `{head}`, lines {lo}-{hi}"


def verbatim_table(path: str, cols: list[str], tag: str, rename: dict | None = None, max_cell: int = 400,
                   row_filter=None) -> str:
    """Copy a csv table cell-for-cell (cells truncated only if > max_cell, marked with '…')."""
    rows = L._csv_rows(path)
    if row_filter:
        rows = [r for r in rows if row_filter(r)]
    hdr = [rename.get(c, c) if rename else c for c in cols]
    out = ["| " + " | ".join(hdr) + " |", "|" + "|".join("-" for _ in cols) + "|"]
    for r in rows:
        cells = []
        for c in cols:
            x = (r.get(c) or "").replace("|", "/").replace("\n", " ")
            if len(x) > max_cell:
                x = x[:max_cell] + "…"
            cells.append(x)
        out.append("| " + " | ".join(cells) + f" |<!-- v:{tag} -->")
    return "\n".join(out)


def src_line(paths: list[str]) -> str:
    return "Sources: " + "; ".join(f"`{p}`" for p in paths)
