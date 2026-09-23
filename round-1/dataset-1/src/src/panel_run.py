#!/usr/bin/env python3
"""STEP 5b (held-out) and 6b (screen): blind panel pass over every distinct candidate class of each sentence.

Per sentence: Disguiser over ALL formulas of the sentence (reference + every candidate row); shown = disguised
representative of every parseable class (reference class included, unlabelled, shuffled; <=8 per call, split above).
One call per (sentence, chunk, panel member). Results -> work/panel_<kind>.jsonl (one line per sentence).
Usage: panel_run.py --kind heldout|screen [--limit N] [--members P1,P3,R1] [--cap 3.0] [--only file-with-sentence-ids]
"""
from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

from loguru import logger

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "labeller"))
sys.setrecursionlimit(10000)
from or_client import BudgetExceeded, Client  # noqa: E402
from panel import Panel, chunks  # noqa: E402
from disguise import Disguiser  # noqa: E402

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(ROOT / "logs" / "panel_run.log", level="DEBUG")


def load_jsonl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


def sentence_units(kind: str, labels_file: str):
    """-> list of (sentence_id, text, all_formulas, [(class_id, rep_fol, is_ref)])"""
    labs = {r["sentence_id"]: r for r in load_jsonl(ROOT / "work" / labels_file)}
    units = []
    if kind == "heldout":
        sents = {s["sentence_id"]: s for s in json.loads((ROOT / "work" / "sentences.json").read_text())}
        from run_label import heldout_jobs
        jobs = {j["sentence_id"]: j for j in heldout_jobs()}
        for sid, lab in labs.items():
            s = sents[sid]
            allf = [lab["reference"]] + [c["fol"] for c in jobs[sid]["cands"] if c["fol"]]
            cls = [(f"{sid}:c{c['class_idx']}", c["rep_fol"], c["is_ref"]) for c in lab["classes"]]
            units.append((sid, s["text"], allf, cls))
    else:
        items = json.loads((ROOT / "work" / "screen_items.json").read_text())
        by = {}
        for it in items:
            by.setdefault(it["screen_sentence_id"], []).append(it)
        for sid, lab in labs.items():
            its = by[sid]
            allf = [lab["reference"]] + [i["candidate_fol_normalised"] for i in its]
            cls = [(f"{sid}:c{c['class_idx']}", c["rep_fol"], c["is_ref"]) for c in lab["classes"]]
            units.append((sid, its[0]["raw_text"], allf, cls))
    return units


async def run(kind, units, members, cap, out_path):
    done = set()
    if out_path.exists():
        done = {json.loads(l)["sentence_id"] for l in out_path.read_text().splitlines() if l.strip()}
    todo = [u for u in units if u[0] not in done]
    logger.info(f"panel {kind}: {len(todo)} sentences to do ({len(done)} done)")
    lock = asyncio.Lock()
    async with Client(f"panel_{kind}", phase_cap=cap, concurrency=16) as client:
        panel = Panel(client)

        async def one(u):
            sid, text, allf, cls = u
            d = Disguiser(sid, text, sorted(set(allf)))
            shown = []
            for cid, rep, is_ref in cls:
                if not rep.strip():
                    continue  # empty output = UNPARSEABLE, never shown
                df = d.formula(rep)
                if df is not None:
                    shown.append((cid, df))
            dtext = d.text(text)
            votes, amb, errs = {}, {}, []
            for m in members:
                for ch in chunks(shown, 8):
                    try:
                        r = await panel.judge(m, sid, dtext, ch, tag=kind)
                    except BudgetExceeded as e:
                        errs.append(f"{m}: budget {e}"); continue
                    if "verdicts" in r:
                        for cid, v in r["verdicts"].items():
                            votes.setdefault(cid, {})[m] = v
                        amb[m] = amb.get(m, False) or r["ambiguous"]
                    else:
                        errs.append(f"{m}: {r.get('error', '')[:120]}")
            rec = {"sentence_id": sid, "disguised_text": dtext, "shown": dict(shown), "votes": votes, "ambiguous": amb, "errors": errs,
                   "members": members}
            async with lock:
                with open(out_path, "a", encoding="utf-8") as f:
                    f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            return rec

        n = 0
        for fut in asyncio.as_completed([one(u) for u in todo]):
            await fut
            n += 1
            if n % 50 == 0:
                logger.info(f"{n}/{len(todo)} phase ${client.spent_phase:.3f} total ${client.spent_total:.3f}")
        logger.info(f"panel {kind} done: phase ${client.spent_phase:.3f} total ${client.spent_total:.3f}")


@logger.catch(reraise=True)
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kind", default="heldout")
    ap.add_argument("--labels", default="")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--members", default="P1,P3,R1")
    ap.add_argument("--cap", type=float, default=3.0)
    ap.add_argument("--only", default="")
    ap.add_argument("--out", default="")
    a = ap.parse_args()
    units = sentence_units(a.kind, a.labels or f"labels_{a.kind}.jsonl")
    units.sort(key=lambda u: u[0])
    if a.only:
        keep = set(json.loads((ROOT / a.only).read_text()))
        units = [u for u in units if u[0] in keep]
    if a.limit:
        units = units[: a.limit]
    out = ROOT / "work" / (a.out or f"panel_{a.kind}.jsonl")
    asyncio.run(run(a.kind, units, a.members.split(","), a.cap, out))


if __name__ == "__main__":
    main()
