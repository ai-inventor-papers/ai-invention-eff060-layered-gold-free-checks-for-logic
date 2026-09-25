"""Claim checker: pull each claim's value from its source file and compare.

Precision rule: MATCH iff |claim - source| <= 0.5 * 10^-d (d = decimals of the claim literal;
percentages are compared as fractions, so '44.9%' has d = 3). A CI matches only if both bounds
match, each at its own precision. Signs must agree. Statuses: MATCH, MISMATCH, NOT_FOUND,
AMBIGUOUS. String claims (verdict labels) must equal the source string exactly.
"""
from __future__ import annotations

import math
import re
from pathlib import Path
from typing import Any

from src import io_locators as L

NUM_RE = r"[+\-−]?\$?\d[\d,]*(?:\.\d+)?(?:e[+\-−]?\d+)?%?"


def norm(s: str) -> str:
    return s.replace("−", "-").replace("−", "-").strip()


def is_numeric_literal(s: str) -> bool:
    return bool(re.fullmatch(r"[+\-]?\$?\d[\d,]*(?:\.\d+)?(?:e[+\-]?\d+)?%?", norm(s)))


def parse_literal(s: str) -> tuple[float, float, dict]:
    """Return (value_as_fraction_or_number, tolerance, format_info)."""
    t = norm(s)
    info = {"sign": t.startswith("+"), "pct": t.endswith("%"), "usd": "$" in t, "sci": "e" in t.lower()}
    core = t.replace("$", "").replace(",", "").rstrip("%").lstrip("+")
    if info["sci"]:
        mant, exp = core.lower().split("e")
        dec = len(mant.split(".")[1]) if "." in mant else 0
        val = float(core)
        tol = 0.5 * 10 ** (-dec) * 10 ** int(exp)
        info["dec"], info["exp"] = dec, int(exp)
    else:
        dec = len(core.split(".")[1]) if "." in core else 0
        val = float(core)
        tol = 0.5 * 10 ** (-dec)
        info["dec"] = dec
    if info["pct"]:
        val /= 100.0
        tol /= 100.0
    info["thousands"] = "," in t
    return val, tol * (1 + 1e-9) + 1e-12, info


def parse_ci(s: str) -> list[str]:
    parts = [p.strip() for p in norm(s).strip("[]").split(",")]
    if len(parts) != 2:
        raise ValueError(f"bad CI literal {s}")
    return parts


def fmt_like(v: float, claim_literal: str) -> str:
    """Format a file value at the claim literal's precision/style (display only)."""
    _, _, info = parse_literal(claim_literal)
    x = v * 100.0 if info["pct"] else v
    if info.get("sci"):
        body = f"{x / 10 ** info['exp']:.{info['dec']}f}e{info['exp']}"
    elif info["thousands"]:
        body = f"{x:,.{info['dec']}f}"
    else:
        body = f"{x:.{info['dec']}f}"
    if body.startswith("-"):
        body = "−" + body[1:]
    elif info["sign"] and x > 0:
        body = "+" + body
    if info["usd"]:
        body = ("−$" + body[1:]) if body.startswith("−") else "$" + body
    return body + ("%" if info["pct"] else "")


def fmt_ci_like(ci: list[float], claim_ci: str) -> str:
    lo_l, hi_l = parse_ci(claim_ci)
    return f"[{fmt_like(ci[0], lo_l)}, {fmt_like(ci[1], hi_l)}]"


def num_match(claim_literal: str, source: float) -> bool:
    val, tol, _ = parse_literal(claim_literal)
    if val != 0 and source != 0 and math.copysign(1, val) != math.copysign(1, source) and abs(source) > tol:
        return False
    return abs(val - source) <= tol


def split_value_ci(v: Any) -> tuple[Any, list[float] | None]:
    """A source cell like '0.278 [0.239, 0.319]' carries its own CI."""
    if isinstance(v, str) and "[" in v:
        m = re.match(r"\s*([^\[]+)\[([^,]+),([^\]]+)\]", v)
        if m:
            return m.group(1).strip(), [L.to_float(m.group(2)), L.to_float(m.group(3))]
    return v, None


def _get_ci(ciloc: Any) -> tuple[list[float], str]:
    if isinstance(ciloc, list):
        (lo, s1), (hi, s2) = L.resolve(ciloc[0]), L.resolve(ciloc[1])
        return [L.to_float(lo), L.to_float(hi)], f"{s1} ; {s2}"
    v, s = L.resolve(ciloc)
    return [L.to_float(v[0]), L.to_float(v[1])], s


# ---------------------------------------------------------------- paper helpers
_PAPER_LINES: list[str] | None = None


def paper_lines() -> list[str]:
    global _PAPER_LINES
    if _PAPER_LINES is None:
        _PAPER_LINES = L._read_text(L.PAPER).splitlines()
    return _PAPER_LINES


def section_range(prefix: str | None) -> tuple[int, int]:
    """1-based inclusive line range of the paper section whose heading starts with prefix."""
    lines = paper_lines()
    if not prefix:
        return 1, len(lines)
    for i, ln in enumerate(lines):
        if ln.startswith(prefix):
            level = len(ln) - len(ln.lstrip("#"))
            for j in range(i + 1, len(lines)):
                m = re.match(r"^(#+) ", lines[j])
                if m and len(m.group(1)) <= level:
                    return i + 1, j
            return i + 1, len(lines)
    return 1, len(lines)


def headings() -> list[tuple[int, str]]:
    return [(i + 1, ln) for i, ln in enumerate(paper_lines()) if re.match(r"^#+ ", ln)]


def literal_variants(lit: str) -> list[str]:
    t = norm(lit)
    out = {t, t.lstrip("+"), t.replace("-", "−"), t.lstrip("+").replace("-", "−")}
    if t.endswith("%"):
        v = float(t.rstrip("%").replace(",", "")) / 100
        out.add(f"{v:.3f}".rstrip("0"))
    return sorted(out, key=len, reverse=True)


def grep_paper(lit: str, prefix: str | None) -> tuple[str | None, int | None]:
    lo, hi = section_range(prefix)
    lines = paper_lines()
    for var in literal_variants(lit):
        pat = r"(?<![\d.])" + re.escape(var) + r"(?![\d])"
        for i in range(lo - 1, hi):
            if re.search(pat, lines[i]):
                return var, i + 1
    return None, None


def paper_pattern(pp: Any, prefix: str | None) -> tuple[str | None, int | None]:
    pat, grp = (pp, 1) if isinstance(pp, str) else pp
    lo, hi = section_range(prefix)
    lines = paper_lines()
    for i in range(lo - 1, hi):
        m = re.search(pat, lines[i])
        if m:
            return m.group(grp), i + 1
    return None, None


# ---------------------------------------------------------------- main check
def check_claim(cl: dict) -> dict:
    row = {k: cl.get(k) for k in ("id", "sec", "text", "value", "ci", "role", "ps")}
    row.update(source_path="", locator="", source_value="", source_ci="", match_hyp_vs_file="", paper_value="",
               paper_line="", match_paper_vs_file="", note="", source_value_raw=None, source_ci_raw=None)
    try:
        v, s = L.resolve(cl["loc"])
        row["locator"] = s
        row["source_path"] = s.split(" :: ")[0] if " :: " in s else s
        v, inline_ci = split_value_ci(v)
        ci_src = None
        if cl.get("ciloc"):
            ci_src, cs = _get_ci(cl["ciloc"])
            row["locator"] += f" || CI: {cs}"
        elif inline_ci is not None:
            ci_src = inline_ci
        if cl["loc"]["t"] == "const":
            row["note"] = "CONTEXT: no file value; " + cl["loc"].get("why", "")
        if cl["value"] is None:  # transcription row: value read by code, no claim literal
            fv = L.to_float(v)
            row["source_value_raw"] = fv
            fmt = cl.get("fmt", "0.000")
            row["source_value"] = (re.sub(r"e([+-])0*(\d)", lambda m: "e" + ("−" if m.group(1) == "-" else "") + m.group(2), f"{fv:.2e}") if fmt == "0.00e0" else fmt_like(fv, fmt))
            ok = True
        elif is_numeric_literal(cl["value"]):
            fv = L.to_float(v)
            row["source_value_raw"] = fv
            row["source_value"] = fmt_like(fv, cl["value"])
            ok = num_match(cl["value"], fv)
        else:
            row["source_value"] = str(v)
            row["source_value_raw"] = str(v)
            ok = str(v) == cl["value"]
        if cl.get("ci") and cl["value"] is None:
            if ci_src is not None:
                row["source_ci_raw"] = ci_src
                row["source_ci"] = fmt_ci_like(ci_src, cl["ci"])
        elif cl.get("ci"):
            if ci_src is None:
                if cl["id"] == "t1_vs_s4":  # CI of S4-c, sign-flipped
                    raw, cs = L.resolve({"t": "json", "f": cl["loc"]["args"]["a"]["f"],
                                         "k": cl["loc"]["args"]["a"]["k"][: -len(".delta")] + ".ci"})
                    ci_src = [-L.to_float(raw[1]), -L.to_float(raw[0])]
                    row["locator"] += f" || CI (negated, bounds swapped): {cs}"
                else:
                    row["note"] += " CI not in source;"
            if ci_src is not None:
                row["source_ci_raw"] = ci_src
                row["source_ci"] = fmt_ci_like(ci_src, cl["ci"])
                lo_l, hi_l = parse_ci(cl["ci"])
                ok = ok and num_match(lo_l, ci_src[0]) and num_match(hi_l, ci_src[1])
        elif ci_src is not None:
            row["source_ci_raw"] = ci_src
            row["source_ci"] = f"[{ci_src[0]:.3f}, {ci_src[1]:.3f}]".replace("-", "−")
        row["match_hyp_vs_file"] = ("TRANSCRIBED" if cl["value"] is None else ("MATCH" if ok else "MISMATCH"))
    except L.NotFound as e:
        row["match_hyp_vs_file"] = "NOT_FOUND"
        row["note"] += str(e)[:200]
        return row
    except L.Ambiguous as e:
        row["match_hyp_vs_file"] = "AMBIGUOUS"
        row["note"] += str(e)[:200]
        return row
    # paper side
    if cl["value"] is None:
        row["match_paper_vs_file"] = "n/a"
        return row
    if cl.get("pp"):
        pv, line = paper_pattern(cl["pp"], cl.get("ps"))
        if pv is None:
            row["paper_value"], row["match_paper_vs_file"] = "", "NOT_IN_PAPER"
        else:
            row["paper_value"], row["paper_line"] = pv, line
            if pv.startswith("["):
                lo_l, hi_l = parse_ci(pv)
                okp = row["source_ci_raw"] is not None and num_match(lo_l, row["source_ci_raw"][0]) and num_match(hi_l, row["source_ci_raw"][1])
            elif is_numeric_literal(pv) and isinstance(row["source_value_raw"], float):
                okp = num_match(pv, row["source_value_raw"])
            else:
                okp = pv == str(row["source_value_raw"])
            row["match_paper_vs_file"] = "MATCH" if okp else "MISMATCH"
    else:
        var, line = grep_paper(cl["value"], cl.get("ps")) if is_numeric_literal(cl["value"]) else (None, None)
        if var is None:
            row["match_paper_vs_file"] = "NOT_IN_PAPER"
        else:
            row["paper_value"], row["paper_line"] = var, line
            row["match_paper_vs_file"] = row["match_hyp_vs_file"]
    return row


def check_all(claims: list[dict]) -> list[dict]:
    return [check_claim(c) for c in claims]


def write_hashes(path: Path) -> None:
    lines = ["# source: sha256 of every file read by the locators (computed at read time)", "path,sha256"]
    lines += [f"{p},{h}" for p, h in sorted(L.HASHES.items())]
    path.write_text("\n".join(lines) + "\n")
