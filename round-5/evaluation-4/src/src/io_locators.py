"""Loaders that read one value from a source file and return (value, locator_string).

Every number in the corrected record is pulled through one of these functions. A locator
is a small dict (see `resolve`) so it can be stored in claims_spec.yaml and replayed.
Paths are absolute and read-only; every file read is hashed into a registry.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import re
from pathlib import Path
from typing import Any

RUN = str(Path(__file__).resolve().parents[4])
I3 = f"{RUN}/iter_3/gen_art"
I4 = f"{RUN}/iter_4/gen_art"
PAPER = f"{RUN}/iter_4/gen_report_text/gen_report_text/paper_draft.md"
REVIEW = f"{RUN}/iter_4/review_report/review_report/.terminal_claude_agent_struct_out.json"

HASHES: dict[str, str] = {}
_JSON_CACHE: dict[str, Any] = {}
_TEXT_CACHE: dict[str, str] = {}


class NotFound(Exception):
    """The file or the key does not exist."""


class Ambiguous(Exception):
    """More than one candidate cell matched."""


def _read_text(path: str) -> str:
    if path not in _TEXT_CACHE:
        p = Path(path)
        if not p.exists():
            raise NotFound(f"source missing: {path}")
        b = p.read_bytes()
        HASHES[path] = hashlib.sha256(b).hexdigest()
        _TEXT_CACHE[path] = b.decode("utf-8", errors="replace")
    return _TEXT_CACHE[path]


def _load_json(path: str) -> Any:
    if path not in _JSON_CACHE:
        _JSON_CACHE[path] = json.loads(_read_text(path))
    return _JSON_CACHE[path]


def _walk_key(obj: Any, key: str) -> Any:
    """Resolve a dotted key where individual keys may themselves contain dots/spaces.

    At each level the longest prefix of the remaining path that is a key is taken.
    List indices are written as [i] directly after a key or as a bare integer part.
    """
    rest = key
    cur = obj
    while rest:
        m = re.match(r"^\[(\d+)\]\.?", rest)
        if m and isinstance(cur, list):
            cur = cur[int(m.group(1))]
            rest = rest[m.end():]
            continue
        if isinstance(cur, list):
            m = re.match(r"^(\d+)\.?", rest)
            if not m:
                raise NotFound(f"list index expected at '{rest}'")
            cur = cur[int(m.group(1))]
            rest = rest[m.end():]
            continue
        if not isinstance(cur, dict):
            raise NotFound(f"cannot descend into {type(cur).__name__} at '{rest}'")
        hit = None
        for k in sorted(cur.keys(), key=len, reverse=True):
            if rest == k or rest.startswith(k + ".") or rest.startswith(k + "["):
                hit = k
                break
        if hit is None:
            raise NotFound(f"key not found at '{rest[:60]}'")
        cur = cur[hit]
        rest = rest[len(hit):]
        if rest.startswith("."):
            rest = rest[1:]
    return cur


def json_key(path: str, dotted_key: str) -> tuple[Any, str]:
    return _walk_key(_load_json(path), dotted_key), f"{path} :: {dotted_key}"


def _csv_rows(path: str) -> list[dict[str, str]]:
    text = _read_text(path)
    lines = [ln for ln in text.splitlines() if not ln.startswith("# source") and not ln.startswith("#")]
    return list(csv.DictReader(io.StringIO("\n".join(lines))))


def csv_cell(path: str, row_filter: dict[str, str], col: str) -> tuple[Any, str]:
    rows = [r for r in _csv_rows(path) if all(str(r.get(k, "")) == str(v) for k, v in row_filter.items())]
    if not rows:
        raise NotFound(f"no csv row {row_filter} in {path}")
    vals = {r.get(col) for r in rows}
    if len(vals) > 1:
        raise Ambiguous(f"{len(rows)} rows with differing '{col}' for {row_filter}")
    if col not in rows[0]:
        raise NotFound(f"column {col} missing in {path}")
    filt = ", ".join(f"{k}={v}" for k, v in row_filter.items())
    return rows[0][col], f"{path} :: row[{filt}] col[{col}]"


def md_table_cell(path: str, table_heading: str, row_regex: str, col_index: int) -> tuple[Any, str]:
    """Fallback reader for markdown tables (used only when no machine source exists)."""
    text = _read_text(path)
    start = text.find(table_heading)
    if start < 0:
        raise NotFound(f"heading '{table_heading}' not in {path}")
    nxt = re.search(r"\n#{2,3} ", text[start + len(table_heading):])
    block = text[start: start + len(table_heading) + (nxt.start() if nxt else len(text))]
    rows = [ln for ln in block.splitlines() if ln.startswith("|") and re.search(row_regex, ln)]
    if not rows:
        raise NotFound(f"row /{row_regex}/ not in table '{table_heading}'")
    if len(rows) > 1:
        raise Ambiguous(f"{len(rows)} rows match /{row_regex}/")
    cells = [c.strip() for c in rows[0].strip().strip("|").split("|")]
    return cells[col_index], f"{path} :: table '{table_heading}' row /{row_regex}/ col {col_index}"


def regex(path: str, pattern: str, group: int = 1) -> tuple[Any, str]:
    text = _read_text(path)
    ms = list(re.finditer(pattern, text, flags=re.M))
    if not ms:
        raise NotFound(f"/{pattern}/ not in {path}")
    vals = {m.group(group) for m in ms}
    if len(vals) > 1:
        raise Ambiguous(f"/{pattern}/ matched {len(ms)} differing values")
    return ms[0].group(group), f"{path} :: regex /{pattern}/ group {group}"


def jsonl_count(path: str, where: dict[str, Any]) -> tuple[int, str]:
    text = _read_text(path)
    n = 0
    for ln in text.splitlines():
        if not ln.strip():
            continue
        r = json.loads(ln)
        if all(r.get(k) == v for k, v in where.items()):
            n += 1
    return n, f"{path} :: count rows where {where}"


def ledger_sum(path: str, field: str = "cost_usd") -> tuple[float, str]:
    text = _read_text(path)
    s = 0.0
    for ln in text.splitlines():
        if ln.strip():
            try:
                s += float(json.loads(ln).get(field) or 0.0)
            except (json.JSONDecodeError, TypeError, ValueError):
                continue
    return s, f"{path} :: sum({field})"


def to_float(v: Any) -> float:
    if isinstance(v, bool):
        return float(v)
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).strip().replace("−", "-").replace(",", "").replace("$", "")
    m = re.search(r"-?\d+(?:\.\d+)?(?:e-?\d+)?", s)
    if not m:
        raise ValueError(f"no number in {v!r}")
    return float(m.group(0))


def resolve(loc: dict[str, Any]) -> tuple[Any, str]:
    """Resolve a locator dict to (value, locator_string)."""
    t = loc["t"]
    if t == "json":
        v, s = json_key(loc["f"], loc["k"])
    elif t == "csv":
        v, s = csv_cell(loc["f"], loc["where"], loc["col"])
    elif t == "md":
        v, s = md_table_cell(loc["f"], loc["h"], loc["row"], loc["col"])
    elif t == "regex":
        v, s = regex(loc["f"], loc["pat"], loc.get("g", 1))
    elif t == "jsonl_count":
        v, s = jsonl_count(loc["f"], loc["where"])
    elif t == "ledger":
        v, s = ledger_sum(loc["f"], loc.get("field", "cost_usd"))
    elif t == "expr":
        env = {}
        parts = []
        for name, sub in loc["args"].items():
            val, sloc = resolve(sub)
            env[name] = to_float(val)
            parts.append(f"{name}={sloc}")
        v = eval(loc["expr"], {"__builtins__": {}}, env)  # noqa: S307 - arithmetic on file values only
        s = f"expr[{loc['expr']}] with " + " ; ".join(parts)
    elif t == "const":
        v, s = loc["v"], f"CONTEXT (no file value): {loc.get('why', '')}"
    else:
        raise ValueError(f"unknown locator type {t}")
    if "idx" in loc:
        v = v[loc["idx"]]
        s += f" [{loc['idx']}]"
    return v, s
