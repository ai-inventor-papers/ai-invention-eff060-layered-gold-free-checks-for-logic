#!/usr/bin/env python3
"""Build labelling jobs and run label_worker over them.

heldout: per sentence, candidates = every generation row (re-normalised from raw_output), ccg2lambda rows, and
         (MALLS only) the GPT-4 gold as system 'malls_gpt4_gold'. Row key = f"{slot}|{prompt_variant}".
screen:  per screen sentence (work/screen_items.json), candidates = the track-L / track-H rows; key = item_id.
refs:    --refs work/reference_overrides.json replaces the reference of listed sentences (PANEL_REPAIRED) and
         writes to a separate output file.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from loguru import logger

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from label_worker import run  # noqa: E402
from normalise import normalise  # noqa: E402

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(ROOT / "logs" / "label.log", level="DEBUG")


def load_jsonl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


def heldout_jobs(refs: dict | None = None) -> list[dict]:
    sents = json.loads((ROOT / "work" / "sentences.json").read_text())
    gens = load_jsonl(ROOT / "raw" / "generations.jsonl")
    ccg = load_jsonl(ROOT / "raw" / "ccg2lambda_candidates.jsonl")
    by: dict[str, dict] = {}
    for g in gens:
        if g.get("raw_output") is None:
            continue
        fol, _ = normalise(g["raw_output"])
        by.setdefault(g["sentence_id"], {})[f"{g['slot']}|{g['prompt_variant']}"] = {"fol": fol, "no_repair": False}
    for c in ccg:
        if c["candidate_fol"]:
            by.setdefault(c["sentence_id"], {})["CCG|none"] = {"fol": c["candidate_fol"], "no_repair": True}
        else:
            by.setdefault(c["sentence_id"], {})["CCG|none"] = {"fol": "", "no_repair": True}
    jobs = []
    for s in sents:
        ref = s["reference_fol"]
        if refs is not None:
            if s["sentence_id"] not in refs:
                continue
            ref = refs[s["sentence_id"]]
        cands = [{"key": k, **v} for k, v in sorted(by.get(s["sentence_id"], {}).items())]
        if s["source"].startswith("MALLS"):
            cands.append({"key": "GOLD|none", "fol": s["reference_fol"], "no_repair": False})
        jobs.append({"sentence_id": s["sentence_id"], "reference": ref, "cands": cands})
    return jobs


def screen_jobs() -> list[dict]:
    items = json.loads((ROOT / "work" / "screen_items.json").read_text())
    by: dict[str, dict] = {}
    for it in items:
        j = by.setdefault(it["screen_sentence_id"], {"sentence_id": it["screen_sentence_id"], "reference": it["reference_fol"], "cands": []})
        j["cands"].append({"key": it["item_id"], "fol": it["candidate_fol_normalised"], "no_repair": False})
    return list(by.values())


@logger.catch(reraise=True)
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kind", default="heldout")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--budget", type=float, default=8.0)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--refs", default="")
    ap.add_argument("--out", default="")
    a = ap.parse_args()
    refs = json.loads((ROOT / a.refs).read_text()) if a.refs else None
    jobs = heldout_jobs(refs) if a.kind == "heldout" else screen_jobs()
    jobs.sort(key=lambda j: j["sentence_id"])
    if a.limit:
        jobs = jobs[: a.limit]
    out = ROOT / "work" / (a.out or f"labels_{a.kind}.jsonl")
    run(jobs, out, a.budget, a.workers, log=logger.info)


if __name__ == "__main__":
    main()
