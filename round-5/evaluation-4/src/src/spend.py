"""Iteration-4 spend from every cost ledger in the run tree (evidence only, never guessed).

Method (plan PART 2 (14)):
- glob the run root for *ledger*.json*, .aii_cost_ledger.jsonl and budget_state.json;
- de-duplicate by file sha256 AND by (ts, model, cost) record key (repo clones hold copies);
- window = [min ts of any iter_4/gen_art ledger record - 6 h, first HTTP-403 budget refusal];
- the first-403 time is grepped from logs/*.log and *.jsonl in the iter_4 gen_art dirs;
- sum by artifact directory; report evidenced total, the $7 phase budget and the difference.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import re
from collections import defaultdict
from pathlib import Path

from loguru import logger

RUN_ROOT = Path("/ai-inventor/aii_data/runs/run_u75jRHUss0zo")
I4 = RUN_ROOT / "3_invention_loop/iter_4/gen_art"
PHASE_BUDGET = 7.0
SELF = Path(__file__).resolve().parents[1]
COST_FIELDS = ("cost_usd", "usd", "cost", "total_cost_usd")
TS_FIELDS = ("ts", "timestamp", "time", "t", "utc")


def _ts(rec: dict) -> float | None:
    for f in TS_FIELDS:
        v = rec.get(f)
        if v is None:
            continue
        if isinstance(v, (int, float)):
            return float(v) / (1000.0 if v > 1e12 else 1.0)
        try:
            return dt.datetime.fromisoformat(str(v).replace("Z", "+00:00")).timestamp()
        except ValueError:
            continue
    return None


def _cost(rec: dict) -> float | None:
    for f in COST_FIELDS:
        v = rec.get(f)
        if isinstance(v, (int, float)) and not isinstance(v, bool):
            return float(v)
    return None


def _records(path: Path) -> list[dict]:
    text = path.read_text(errors="replace")
    out: list[dict] = []
    if path.suffix == ".jsonl":
        for ln in text.splitlines():
            try:
                r = json.loads(ln)
                if isinstance(r, dict):
                    out.append(r)
            except json.JSONDecodeError:
                continue
    else:
        try:
            d = json.loads(text)
        except json.JSONDecodeError:
            return out
        if isinstance(d, list):
            out = [r for r in d if isinstance(r, dict)]
        elif isinstance(d, dict):
            for k in ("records", "calls", "entries", "ledger"):
                if isinstance(d.get(k), list):
                    out = [r for r in d[k] if isinstance(r, dict)]
    return out


def first_403() -> tuple[float | None, str]:
    best, where = None, ""
    pat = re.compile(r"aii_run_budget_exhausted|HTTP 403|status.?code.?403|\b403\b.{0,40}(Forbidden|budget)")
    tpat = re.compile(r"(20\d\d-\d\d-\d\d[ T]\d\d:\d\d:\d\d)")
    for d in sorted(I4.iterdir()):
        files = list(d.glob("logs/*.log")) + list(d.glob("logs/*.jsonl")) + list(d.glob("*ledger*.jsonl")) + list(d.glob("results/*ledger*.jsonl"))
        for f in files:
            if f.stat().st_size > 30_000_000 or "llm_cache" in f.name:
                continue
            try:
                for ln in f.open(errors="replace"):
                    if not pat.search(ln):
                        continue
                    t = None
                    m = tpat.search(ln)
                    if m:
                        t = dt.datetime.fromisoformat(m.group(1).replace(" ", "T")).replace(tzinfo=dt.timezone.utc).timestamp()
                    elif ln.lstrip().startswith("{"):
                        try:
                            t = _ts(json.loads(ln))
                        except json.JSONDecodeError:
                            t = None
                    if t and (best is None or t < best):
                        best, where = t, f"{f}"
            except OSError:
                continue
    return best, where


def run(out_dir: Path) -> dict:
    cands = []
    skip = {".venv", ".shared_cache", "node_modules", "__pycache__", "hf_cache", ".git", "vendor", "site-packages"}
    for dirpath, dirnames, filenames in os.walk(RUN_ROOT):
        dirnames[:] = [d for d in dirnames if d not in skip and not d.startswith(".cache")]
        if str(SELF) in dirpath:
            continue
        for fn in filenames:
            if (("ledger" in fn and (fn.endswith(".json") or fn.endswith(".jsonl"))) or fn == "budget_state.json"):
                cands.append(Path(dirpath) / fn)
    cands = sorted(set(cands))
    logger.info(f"spend: {len(cands)} ledger-like files in the run tree")
    seen_sha, files_used, dup_files = {}, [], []
    for p in cands:
        h = hashlib.sha256(p.read_bytes()).hexdigest()
        if h in seen_sha:
            dup_files.append((str(p), seen_sha[h]))
            continue
        seen_sha[h] = str(p)
        files_used.append(p)
    i4_ts = []
    per_file = {}
    for p in files_used:
        recs = [(r, _ts(r), _cost(r)) for r in _records(p)]
        per_file[p] = recs
        if str(p).startswith(str(I4)):
            i4_ts += [t for _, t, c in recs if t is not None]
    t403, where403 = first_403()
    lo = (min(i4_ts) - 6 * 3600) if i4_ts else None
    hi = t403
    # cross-file de-duplication: the same call is often logged by two ledgers of one artifact (ms-apart ts)
    # and by repo clones. Key = (artifact, whole second, model, cost); merged multiplicity = MAX over files.
    per_key_file: dict[tuple, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for p, recs in per_file.items():
        rel = p.relative_to(RUN_ROOT)
        parts = rel.parts
        art = "/".join(parts[:4]) if parts[0] == "3_invention_loop" else "/".join(parts[:2])
        for r, t, c in recs:
            if c is None or t is None or lo is None:
                continue
            if t < lo or (hi is not None and t > hi + 60):
                continue
            per_key_file[(round(t), str(r.get("model")), round(c, 10))][str(p)] += 1
    by_art: dict[str, float] = defaultdict(float)
    n_by_art: dict[str, int] = defaultdict(int)
    dup_records = 0
    for (t, model, c), files in per_key_file.items():
        mult = max(files.values())
        dup_records += sum(files.values()) - mult
        src = max(files, key=files.get)
        rel = Path(src).relative_to(RUN_ROOT).parts
        art = "/".join(rel[:4]) if rel[0] == "3_invention_loop" else "/".join(rel[:2])
        by_art[art] += c * mult
        n_by_art[art] += mult
    total = sum(by_art.values())
    no_ledger = [str(d) for d in sorted(I4.iterdir()) if d.is_dir() and not any(str(p).startswith(str(d) + "/") for p in files_used)]
    notes = []
    for p, recs in per_file.items():
        for r, t, c in recs:
            n = str(r.get("note") or "")
            if "budget" in n.lower() and n not in [x["note"] for x in notes]:
                notes.append(dict(file=str(p), note=n[:400], code=r.get("code"), utc=r.get("utc")))
    in_i4 = {k: v for k, v in by_art.items() if "/iter_4/" in k}
    res = {
        "method": __doc__.strip(),
        "n_ledger_files_found": len(cands),
        "n_duplicate_files_by_sha256": len(dup_files),
        "duplicate_files_examples": dup_files[:10],
        "n_duplicate_records_by_key": dup_records,
        "window_utc": [dt.datetime.fromtimestamp(lo, dt.timezone.utc).isoformat() if lo else None,
                       dt.datetime.fromtimestamp(hi, dt.timezone.utc).isoformat() if hi else None],
        "first_403_source": where403,
        "by_artifact_usd": {k: round(v, 7) for k, v in sorted(by_art.items(), key=lambda kv: -kv[1])},
        "records_by_artifact": dict(n_by_art),
        "evidenced_total_usd": round(total, 6),
        "evidenced_iter4_artifacts_usd": round(sum(in_i4.values()), 6),
        "evidenced_other_artifacts_in_window_usd": round(total - sum(in_i4.values()), 6),
        "window_note": "records of other artifacts whose ledger timestamps fall inside the iteration-4 window are listed; the ledgers do not say which phase budget they were charged to",
        "phase_budget_usd": PHASE_BUDGET,
        "unaccounted_usd": round(PHASE_BUDGET - total, 6),
        "unaccounted_note": "unaccounted (no ledger in the run tree records it); not attributed to any process",
        "iter4_gen_art_dirs_without_ledger": no_ledger,
        "ledger_budget_notes": notes[:10],
    }
    (out_dir / "spend_iter4.json").write_text(json.dumps(res, indent=1))
    return res
