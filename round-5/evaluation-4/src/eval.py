#!/usr/bin/env python3
"""Corrected record and paper-ready fixes (iteration 5, evaluation 4). CPU only, no LLM calls, $0.

Pipeline: claims_spec -> numbers.csv (MATCH/MISMATCH vs files and vs the paper) -> record_final.md
(17 sections, lints) -> claims_ledger.csv -> reviewer_checklist.csv -> skeleton_iter5.md (+ resolution)
-> figures F1-F4 -> independent audit (audit/rederive.py, separate code path) -> eval_out.json.
"""
from __future__ import annotations

import csv
import json
import re
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path

from loguru import logger

WS = Path(__file__).resolve().parent
sys.path.insert(0, str(WS))
(WS / "logs").mkdir(exist_ok=True)
logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(WS / "logs/run.log", rotation="30 MB", level="DEBUG")

from src import checker as CK  # noqa: E402
from src import io_locators as L  # noqa: E402
from src.claims_spec import CLAIMS  # noqa: E402
from src.ctx import Ctx  # noqa: E402
from src.lints import lint_all  # noqa: E402
from src.transcribe import T as TRANSCRIBED  # noqa: E402

NUM_COLS = ["claim_id", "section", "claim_text", "claim_value", "claim_ci", "source_path", "locator", "source_value",
            "source_ci", "match_hyp_vs_file", "paper_value", "paper_line", "match_paper_vs_file", "data_role", "note"]


def write_numbers(rows: list[dict], path: Path) -> None:
    with path.open("w", newline="") as f:
        f.write("# source: every row's value is read by src/io_locators.py from source_path at locator (never typed); "
                "claim_value is the hypothesis/review literal; statuses per src/checker.py precision rule\n")
        w = csv.writer(f)
        w.writerow(NUM_COLS)
        for r in rows:
            w.writerow([r["id"], r.get("sec"), r.get("text"), r.get("value") or "", r.get("ci") or "", r.get("source_path"),
                        r.get("locator"), r.get("source_value"), r.get("source_ci"), r.get("match_hyp_vs_file"),
                        r.get("paper_value"), r.get("paper_line"), r.get("match_paper_vs_file"), r.get("role"), r.get("note")])


def review_numbers(rows: list[dict]) -> list[dict]:
    """(ii) every number named in the 11 critiques -> covered by a numbers.csv row or UNMAPPED."""
    rv = json.loads(L._read_text(L.REVIEW))
    vals = []
    for r in rows:
        for key in ("source_value_raw",):
            v = r.get(key)
            if isinstance(v, float):
                vals.append((v, r["id"]))
        ci = r.get("source_ci_raw")
        if ci:
            vals += [(ci[0], r["id"]), (ci[1], r["id"])]
        pv = r.get("paper_value")
        if pv and str(pv).startswith("["):
            try:
                for b in CK.parse_ci(str(pv)):
                    vals.append((CK.parse_literal(b)[0], r["id"] + "(paper CI)"))
            except ValueError:
                pass
        if pv and re.fullmatch(r"[+\-−]?\$?\d[\d.,]*%?", str(pv)):
            try:
                vals.append((CK.parse_literal(str(pv))[0], r["id"] + "(paper)"))
            except ValueError:
                pass
    out = []
    for k, cr in enumerate(rv["critiques"], 1):
        text = cr["description"] + " " + cr["suggested_action"]
        for m in re.finditer(r"(?<![\w.])[+\-−]?\$?\d+(?:\.\d+)?%?(?![\w])", text):
            lit = m.group(0)
            pre = text[max(0, m.start() - 8): m.start()]
            if re.search(r"(§|§\d(?:\.\d)?[–-]|arXiv |\()$", pre) or re.fullmatch(r"\d{4}\.\d{5}", lit):
                continue  # section numbers and arXiv ids are not measurements
            if not re.search(r"\.\d|%", lit):
                continue  # integers (section numbers, counts) are not checked here
            try:
                val, tol, _ = CK.parse_literal(lit)
            except ValueError:
                continue
            hits = sorted({rid for v, rid in vals if abs(abs(v) - abs(val)) <= tol})
            out.append(dict(critique=k, literal=lit, context=text[max(0, m.start() - 50): m.end() + 30].replace("\n", " "),
                            covered_by=";".join(hits[:5]), status="MAPPED" if hits else "UNMAPPED"))
    return out


@logger.catch(reraise=True)
def main() -> None:
    t0 = time.time()
    assert "openai" not in sys.modules and "requests" not in sys.modules
    import yaml
    (WS / "claims_spec.yaml").write_text("# hand-curated claim list: literal as written in hypothesis §0.2-0.3 / review + one locator each (values are pulled by code)\n"
                                         + yaml.safe_dump({"claims": CLAIMS, "transcriptions": TRANSCRIBED}, allow_unicode=True, sort_keys=False, width=200))
    logger.info(f"checking {len(CLAIMS)} claims + {len(TRANSCRIBED)} transcription rows")
    rows = CK.check_all(CLAIMS) + CK.check_all(TRANSCRIBED)
    cnt = Counter(r["match_hyp_vs_file"] for r in rows)
    logger.info(f"hyp-vs-file: {dict(cnt)}; paper-vs-file: {dict(Counter(r['match_paper_vs_file'] for r in rows))}")
    bad = [r for r in rows if r["match_hyp_vs_file"] in ("NOT_FOUND", "AMBIGUOUS")]
    for r in bad:
        logger.warning(f"{r['id']}: {r['match_hyp_vs_file']} {r['note'][:160]}")

    # spend ledger
    from src.spend import run as spend_run
    (WS / "results").mkdir(exist_ok=True)
    sp = spend_run(WS / "results")

    # record_final.md
    from src.sections import build
    ctx = Ctx(rows)
    md, ids = build(ctx, sp)
    (WS / "record_final.md").write_text(md)
    numbers = {r["id"]: r for r in ctx.rows}
    fails = lint_all(md, numbers)
    (WS / "lint_report.json").write_text(json.dumps({"n_failures": len(fails), "failures": fails}, indent=1))
    logger.info(f"record_final.md: {len(md)} chars, {len(ctx.markers)} correction markers, lint failures {len(fails)}")
    for f in fails[:40]:
        logger.warning(f"LINT {f}")

    write_numbers(ctx.rows, WS / "numbers.csv")
    mism = [r for r in ctx.rows if r.get("match_hyp_vs_file") in ("MISMATCH", "NOT_FOUND", "AMBIGUOUS") or r.get("match_paper_vs_file") == "MISMATCH"]
    write_numbers(mism, WS / "mismatches.csv")
    with (WS / "tables/correction_markers.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["section", "line", "status", "critique", "original", "what", "source"])
        w.writeheader()
        for m in ctx.markers:
            w.writerow({k: m.get(k) for k in w.fieldnames})
    with (WS / "tables/placeholder_ids.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["line", "placeholder", "new", "status", "via"])
        w.writeheader()
        for r in ids:
            w.writerow({k: r.get(k, "") for k in w.fieldnames})
    rn = review_numbers(ctx.rows)
    with (WS / "tables/review_numbers.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["critique", "literal", "status", "covered_by", "context"])
        w.writeheader()
        for r in rn:
            w.writerow(r)
    logger.info(f"review critique numbers: {Counter(r['status'] for r in rn)}")

    # remaining parts
    from src.ledger_checklist import write_checklist, write_claims_ledger
    ledger = write_claims_ledger(ctx, WS / "claims_ledger.csv")
    checklist = write_checklist(ctx, WS / "reviewer_checklist.csv", fails)
    from src.skeleton import write_skeleton
    skel = write_skeleton(ctx, WS)
    from src.figures import make_figures
    figs = make_figures(ctx, WS / "figures")
    write_numbers(ctx.rows, WS / "numbers.csv")  # figures/skeleton may have added computed rows

    # independent audit (separate process, imports nothing from src/)
    logger.info("running audit/rederive.py (independent code path)")
    subprocess.run([sys.executable, str(WS / "audit/rederive.py")], check=True, cwd=WS, timeout=3000)
    aud = json.loads((WS / "audit/rederive.json").read_text())
    from src.mutation import mutation_test
    mut = mutation_test(CLAIMS, WS / "audit/checker_mutation.json")

    CK.write_hashes(WS / "tables/source_hashes.csv")
    from src.eval_out import write_eval_out
    write_eval_out(WS, ctx, fails, ledger, checklist, ids, sp, aud, mut, skel, figs)
    assert "openai" not in sys.modules and "requests" not in sys.modules, "no LLM/network client may be imported"
    logger.info(f"done in {time.time() - t0:.0f}s")
    if fails:
        raise SystemExit(f"{len(fails)} lint failures (see lint_report.json)")


if __name__ == "__main__":
    main()
