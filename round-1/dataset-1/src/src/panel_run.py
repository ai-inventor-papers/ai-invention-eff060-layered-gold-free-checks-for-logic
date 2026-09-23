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
import hashlib
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


UNCERTAIN = ("VOCAB_GRAN", "COMPOUND", "TIMEOUT_UNKNOWN")


def vg_cid(sid: str, fol: str) -> str:
    """Panel item id of a VOCAB_GRAN candidate that joined the reference class (judged on its own string)."""
    return f"{sid}:vg:{hashlib.sha1(fol.strip().encode()).hexdigest()[:8]}"


def vg_strings(lab: dict, fol_of: dict) -> list[str]:
    """Distinct candidate strings auto-labelled VOCAB_GRAN (equivalent to the reference only modulo vocabulary or
    granularity). The class representative is the reference itself, so a vote on it cannot tell whether the renaming
    preserved meaning: each distinct string is shown to the panel as its own item (plan 5f MEANING_RENAME)."""
    out = {fol_of[k].strip() for k, r in lab["rows"].items() if r.get("auto_label") == "VOCAB_GRAN" and (fol_of.get(k) or "").strip()}
    return sorted(out)


def ctrl_full_sample(sid: str) -> bool:
    """Plan 5c budget fallback: 20% sha1 sample of CTRL sentences gets FULL class coverage."""
    return int(hashlib.sha1(("ctrlfull|" + sid).encode()).hexdigest()[:8], 16) % 5 == 0


ctrl_reduced = False
vg_only = False


def sentence_units(kind: str, labels_file: str):
    """-> list of (sentence_id, text, all_formulas, [(class_id, rep_fol, is_ref)])"""
    # sentences whose reference does not parse have no classes (label record carries 'error'): nothing to adjudicate
    labs = {r["sentence_id"]: r for r in load_jsonl(ROOT / "work" / labels_file) if "error" not in r}
    units = []
    if kind == "heldout":
        sents = {s["sentence_id"]: s for s in json.loads((ROOT / "work" / "sentences.json").read_text())}
        from run_label import heldout_jobs
        jobs = {j["sentence_id"]: j for j in heldout_jobs()}
        for sid, lab in labs.items():
            s = sents[sid]
            fol_of = {c["key"]: c["fol"] for c in jobs[sid]["cands"]}
            allf = [lab["reference"]] + [c["fol"] for c in jobs[sid]["cands"] if c["fol"]]
            full = s["source_stratum"] != "CTRL" or not ctrl_reduced or ctrl_full_sample(sid)
            cls = [(f"{sid}:c{c['class_idx']}", c["rep_fol"], c["is_ref"]) for c in lab["classes"]
                   if full or c["is_ref"] or c.get("auto_label") in UNCERTAIN]
            cls += [(vg_cid(sid, f), f, False) for f in vg_strings(lab, fol_of)]
            units.append((sid, s["text"], allf, cls))
    else:
        items = json.loads((ROOT / "work" / "screen_items.json").read_text())
        by = {}
        for it in items:
            by.setdefault(it["screen_sentence_id"], []).append(it)
        for sid, lab in labs.items():
            its = by[sid]
            fol_of = {i["item_id"]: i["candidate_fol_normalised"] for i in its}
            allf = [lab["reference"]] + [i["candidate_fol_normalised"] for i in its]
            vg = [(vg_cid(sid, f), f, False) for f in vg_strings(lab, fol_of)]
            if vg_only:  # supplementary pass: the VOCAB_GRAN strings alone (main screen pass pre-dated vg items)
                if vg:
                    units.append((sid, its[0]["raw_text"], allf, vg))
                continue
            cls = [(f"{sid}:c{c['class_idx']}", c["rep_fol"], c["is_ref"]) for c in lab["classes"]]
            units.append((sid, its[0]["raw_text"], allf, cls + vg))
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


async def adjudicate(kind, member, raters, cap, in_path, out_path):
    """Budget design (plan 5c fallback, label-preserving): the two cheaper raters judge every item; the third member
    judges ONLY the items where they disagree or a vote is missing (plus the reference item when only the
    sentence-level ambiguity flag is split). The 2-of-3 majority is then identical to a full 3-model vote."""
    recs = [json.loads(l) for l in in_path.read_text().splitlines() if l.strip()]
    got = {}  # items already adjudicated (earlier records; a budget-interrupted record is resumed item by item)
    for l in (out_path.read_text().splitlines() if out_path.exists() else []):
        if l.strip():
            a = json.loads(l)
            got.setdefault(a["sentence_id"], set()).update(a["votes"])
    todo = []
    for r in recs:
        if member in r.get("members", []):
            continue
        items = [cid for cid in r["shown"] if (not all(m in r["votes"].get(cid, {}) for m in raters)
                 or len({r["votes"][cid][m]["faithful"] for m in raters}) > 1) and cid not in got.get(r["sentence_id"], set())]
        if r["sentence_id"] in got and not items:
            continue
        amb = r.get("ambiguous", {})
        amb_split = not all(m in amb for m in raters) or len({amb[m] for m in raters}) > 1
        if not items and amb_split:
            ref = f"{r['sentence_id']}:c0"
            items = [ref] if ref in r["shown"] else list(r["shown"])[:1]
        if items:
            todo.append((r, items))
    # priority under a budget cap: MALLS strata (L25 > L20 > EXC) before CTRL; within, sentences missing a rater first
    sents = {x["sentence_id"]: x for x in json.loads((ROOT / "work" / "sentences.json").read_text())} if kind == "heldout" else {}
    rank = {"L25": 0, "L20": 1, "EXC": 2, "CTRL": 3}
    todo.sort(key=lambda t: (rank.get(sents.get(t[0]["sentence_id"], {}).get("source_stratum"), 4),
                             -sum(not all(m in t[0]["votes"].get(c, {}) for m in raters) for c in t[1]), t[0]["sentence_id"]))
    logger.info(f"adjudication by {member}: {len(todo)} sentences, {sum(len(i) for _, i in todo)} items "
                f"(of {sum(len(r['shown']) for r in recs)} items in {len(recs)} sentences)")
    lock = asyncio.Lock()
    async with Client(f"panel_{kind}_adj", phase_cap=cap, concurrency=16) as client:
        panel = Panel(client)

        async def one(r, items):
            sid = r["sentence_id"]
            shown = [(cid, r["shown"][cid]) for cid in items]
            votes, amb, errs = {}, None, []
            for ch in chunks(shown, 8):
                try:
                    res = await panel.judge(member, sid, r["disguised_text"], ch, tag=f"{kind}_adj")
                except BudgetExceeded as e:
                    errs.append(f"{member}: budget {e}"); continue
                if "verdicts" in res:
                    votes.update(res["verdicts"])
                    amb = bool(amb) or res["ambiguous"]
                else:
                    errs.append(f"{member}: {res.get('error', '')[:120]}")
            rec = {"sentence_id": sid, "member": member, "items": items, "votes": votes, "ambiguous": amb, "errors": errs}
            async with lock:
                with open(out_path, "a", encoding="utf-8") as f:
                    f.write(json.dumps(rec, ensure_ascii=False) + "\n")

        n = 0
        for b in range(0, len(todo), 16):  # batches in priority order (as_completed would not preserve it)
            await asyncio.gather(*[one(r, i) for r, i in todo[b:b + 16]])
            n += len(todo[b:b + 16])
            logger.info(f"adj {n}/{len(todo)} phase ${client.spent_phase:.3f} total ${client.spent_total:.3f}")
            if client.spent_total >= float(__import__("os").environ.get("AII_HARD_CAP", "9.5")):
                break
        logger.info(f"adjudication done: phase ${client.spent_phase:.3f} total ${client.spent_total:.3f}")


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
    ap.add_argument("--ctrl-reduced", action="store_true")
    ap.add_argument("--vg-only", action="store_true")
    ap.add_argument("--adjudicate", default="", help="member that judges only the disagreements of --members")
    a = ap.parse_args()
    global ctrl_reduced, vg_only
    ctrl_reduced, vg_only = a.ctrl_reduced, a.vg_only
    if a.adjudicate:
        src = ROOT / "work" / (a.out or f"panel_{a.kind}.jsonl")
        asyncio.run(adjudicate(a.kind, a.adjudicate, a.members.split(","), a.cap, src, src.with_name(src.stem + "_adj.jsonl")))
        return
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
