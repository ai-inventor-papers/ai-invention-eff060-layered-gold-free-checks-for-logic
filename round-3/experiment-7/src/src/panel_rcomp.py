#!/usr/bin/env python3
"""S8: FREE-condition adjudication with dataset E's blind, disguised, family-disjoint LLM panel (replaces dataset-3's
Sonnet-5 adjudicator, whose R_ADJ gate FAILED). Panel code, TEMPLATE and PROMPT_SHA1 are E's (src/vendor_e_panel/panel.py);
the Disguiser is E's (rcomp/labeller/disguise.py, byte-identical to E's labeller/disguise.py).

Per sentence: the routed solver classes plus BOTH reference readings (weak, strong) are shown shuffled and unlabelled
(<= 8 formulas per call, split above), disguised consistently in text and formulas. P1 (claude-haiku-4.5) and P3 (glm-4.6)
judge every item; R1 (kimi-k2-0905) judges only items where P1/P3 disagree or a vote is missing (E's rule: the 2-of-3
majority equals a full 3-model vote).
Routing (prereg_rcomp routing_step8): P1 VOCAB_GRAN > P2 COMPOUND/TIMEOUT_UNKNOWN > P3 ERROR with addrop_only_suspect,
SORTAL/ARITY_REIFY/XOR_OR flag or ONLY_IF_CONVERSE > P4 20% sha1 sample of other solver ERRORs. A sentence enters the
queue at its best priority and ALL its routed classes are judged in the same call (sentence-complete); sentences are
processed in (priority, sha1(sentence_id)) order until the cap.

usage: panel_rcomp.py check [--cap 0.2]     60 known-label items (30 PERTURB + 30 CONTROL on R_COMP bases) -> BA
       panel_rcomp.py run   [--cap 1.5] [--limit N]
       panel_rcomp.py assemble             -> results/free_labels.jsonl (prereg final_label_rule)
"""
from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RC = ROOT / "rcomp"
RES = ROOT / "results"
sys.path.insert(0, str(ROOT / "src" / "vendor_e_panel"))
sys.path.insert(0, str(RC / "labeller"))
sys.path.insert(0, str(ROOT / "src"))
sys.setrecursionlimit(10000)
from loguru import logger  # noqa: E402

from or_client import BudgetExceeded, Client  # noqa: E402  (E's client, patched: URL + artifact budget)
from panel import Panel, chunks, PROMPT_SHA1, MEMBERS  # noqa: E402
from disguise import Disguiser  # noqa: E402

RATERS = ["P1", "P3"]
ADJ = "R1"
FEW = {"G1", "G1b", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9"}


def jl(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.exists() else []


def sha1(s: str) -> str:
    return hashlib.sha1(s.encode()).hexdigest()


def sents() -> dict:
    return {s["sentence_id"]: s for s in json.loads((RC / "work" / "rcomp_sentences.json").read_text())}


def maj(votes: dict) -> tuple[int, int, int]:
    """E's assemble.maj: (n faithful, n unfaithful, n votes)."""
    f = sum(1 for v in votes.values() if v["faithful"])
    return f, len(votes) - f, len(votes)


def route(r: dict) -> int | None:
    """prereg routing for one solver class (dataset-3 adjudicate.build_queue logic)."""
    L = r["solver_label"]
    flags = set(r.get("solver_convention_flags") or [])
    if L == "VOCAB_GRAN":
        return 1
    if L in ("COMPOUND", "TIMEOUT_UNKNOWN"):
        return 2
    if L == "ERROR" and (r.get("solver_addrop_only_suspect") or flags & {"SORTAL", "ARITY_REIFY", "XOR_OR"}
                         or r.get("solver_only_if_converse")):
        return 3
    if L == "ERROR" and int(sha1("p4|" + r["class_id"])[:8], 16) / 16 ** 8 < 0.20:
        return 4
    if r.get("solver_only_if_converse"):
        return 3
    return None


async def judge_sentence(panel: Panel, sid: str, text: str, allf: list[str], items: list[tuple[str, str]], tag: str) -> dict:
    """items = [(item_id, fol)]; returns {'votes': {item_id: {member: vote}}, 'ambiguous': {...}, 'errors': [...]}"""
    d = Disguiser(sid, text, sorted(set(allf)))
    shown = []
    for cid, f in items:
        if not (f or "").strip():
            continue
        df = d.formula(f)
        if df is not None:
            shown.append((cid, df))
    dtext = d.text(text)
    votes, amb, errs = {}, {}, []
    for m in RATERS:
        for ch in chunks(shown, 8):
            try:
                r = await panel.judge(m, sid, dtext, ch, tag=tag)
            except BudgetExceeded as e:
                errs.append(f"{m}: budget {e}"); continue
            if "verdicts" in r:
                for cid, v in r["verdicts"].items():
                    votes.setdefault(cid, {})[m] = v
                amb[m] = amb.get(m, False) or r["ambiguous"]
            else:
                errs.append(f"{m}: {r.get('error', '')[:120]}")
    need = [(cid, df) for cid, df in shown if not all(m in votes.get(cid, {}) for m in RATERS)
            or len({votes[cid][m]["faithful"] for m in RATERS}) > 1]
    for ch in chunks(need, 8) if need else []:
        try:
            r = await panel.judge(ADJ, sid, dtext, ch, tag=tag + "_adj")
        except BudgetExceeded as e:
            errs.append(f"{ADJ}: budget {e}"); continue
        if "verdicts" in r:
            for cid, v in r["verdicts"].items():
                votes.setdefault(cid, {})[ADJ] = v
            amb[ADJ] = r["ambiguous"]
        else:
            errs.append(f"{ADJ}: {r.get('error', '')[:120]}")
    return {"sentence_id": sid, "disguised_text": dtext, "shown": dict(shown), "votes": votes, "ambiguous": amb, "errors": errs}


async def _run_units(units: list[dict], phase: str, cap: float, outp: Path, concurrency: int = 8) -> None:
    done = {r["sentence_id"] for r in jl(outp) if not any("budget" in e for e in r.get("errors", []))}
    todo = [u for u in units if u["sentence_id"] not in done]
    logger.info(f"[{phase}] {len(todo)} sentences to adjudicate ({len(done)} done); PROMPT_SHA1 {PROMPT_SHA1}")
    async with Client(phase, phase_cap=cap, concurrency=16, timeout=240) as client:
        panel = Panel(client)
        for b in range(0, len(todo), concurrency):  # waves in priority order
            wave = todo[b:b + concurrency]
            recs = await asyncio.gather(*[judge_sentence(panel, u["sentence_id"], u["text"], u["allf"], u["items"], phase)
                                          for u in wave], return_exceptions=True)
            stop = False
            with outp.open("a") as fh:
                for u, r in zip(wave, recs):
                    if isinstance(r, Exception):
                        logger.error(f"[{phase}] {u['sentence_id']} failed: {r}")
                        continue
                    r["priority"] = u.get("priority")
                    r["items_meta"] = u.get("meta", {})
                    fh.write(json.dumps(r, ensure_ascii=False) + "\n")
                    if any("budget" in e for e in r["errors"]):
                        stop = True
            logger.info(f"[{phase}] {min(b + concurrency, len(todo))}/{len(todo)} phase ${client.spent_phase:.4f}")
            if stop:
                logger.error(f"[{phase}] budget/key stop; remaining sentences stay un-adjudicated (UNRESOLVED / adj_pending)")
                break


def run_check(cap: float) -> None:
    items = json.loads((RC / "work" / "adjudicator_check_items.json").read_text())
    S = {**{s["sentence_id"]: s for s in json.loads((RC / "work" / "rcomp_sentences_preliminary_iter2.json").read_text())}, **sents()}
    by = defaultdict(list)
    for it in items:
        by[it["sentence_id"]].append(it)
    units = []
    for sid, its in sorted(by.items(), key=lambda kv: sha1(kv[0])):
        s = S[sid]
        allf = [s["reference_fol_weak"], s["reference_fol_strong"]] + [i["candidate_fol"] for i in its]
        units.append({"sentence_id": sid, "text": s["text"], "allf": allf,
                      "items": [(f"chk:{i['item_id']}", i["candidate_fol"]) for i in its]
                      + [(f"{sid}:REF_weak", s["reference_fol_weak"]), (f"{sid}:REF_strong", s["reference_fol_strong"])]})
    outp = RES / "panel_check.jsonl"
    asyncio.run(_run_units(units, "panel_known_label_check", cap, outp))
    got = {}
    for r in jl(outp):
        for cid, v in r["votes"].items():
            got[cid] = v
    tp = tn = npos = nneg = 0
    per = []
    for it in items:
        v = got.get(f"chk:{it['item_id']}")
        if not v or len(v) < 2:
            per.append({"item_id": it["item_id"], "known": it["known_label"], "verdict": None}); continue
        nf, nu, n = maj(v)
        verdict = "FAITHFUL" if nf >= 2 else ("UNFAITHFUL" if nu >= 2 else None)
        per.append({"item_id": it["item_id"], "known": it["known_label"], "verdict": verdict, "operator": it.get("operator"),
                    "control_type": it.get("control_type"), "votes": {m: x["faithful"] for m, x in v.items()}})
        if verdict is None:
            continue
        if it["known_label"] == "ERROR":
            npos += 1; tp += verdict == "UNFAITHFUL"
        else:
            nneg += 1; tn += verdict == "FAITHFUL"
    re_, rc_ = (tp / npos if npos else None), (tn / nneg if nneg else None)
    ba = (re_ + rc_) / 2 if npos and nneg else None
    out = {"n_items": len(items), "n_answered": npos + nneg, "recall_error": re_, "recall_correct": rc_, "balanced_accuracy": ba,
           "tier_B_provisional": (ba is None or ba < 0.80), "prompt_sha1": PROMPT_SHA1, "members": RATERS + [ADJ + " on disagreement"],
           "per_operator": {k: dict(Counter(p["verdict"] for p in per if (p.get("operator") or p.get("control_type")) == k))
                            for k in sorted({(p.get("operator") or p.get("control_type") or "?") for p in per})},
           "rows": per}
    (RES / "panel_check.json").write_text(json.dumps(out, indent=1))
    logger.info(f"known-label check: BA {ba} (ERROR recall {re_}, CORRECT recall {rc_}), n={npos + nneg}/{len(items)}")


def build_units() -> list[dict]:
    lab = json.loads((RC / "work" / "rcomp_labels.json").read_text())
    S = sents()
    cls = {}
    for r in lab:
        if r["class_id"] and r["class_id"] not in cls:
            cls[r["class_id"]] = r
    by = defaultdict(list)
    for cid, r in cls.items():
        pri = route(r)
        if pri is not None:
            by[r["sentence_id"]].append((pri, cid, r["candidate_fol"]))
    allf_by = defaultdict(list)
    for r in lab:
        if r.get("candidate_fol"):
            allf_by[r["sentence_id"]].append(r["candidate_fol"])
    units = []
    for sid, lst in by.items():
        s = S[sid]
        items = [(cid, f) for _, cid, f in sorted(lst)] + [(f"{sid}:REF_weak", s["reference_fol_weak"]),
                                                           (f"{sid}:REF_strong", s["reference_fol_strong"])]
        units.append({"sentence_id": sid, "text": s["text"], "priority": min(p for p, _, _ in lst),
                      "allf": [s["reference_fol_weak"], s["reference_fol_strong"]] + allf_by[sid], "items": items,
                      "meta": {cid: p for p, cid, _ in lst}})
    units.sort(key=lambda u: (u["priority"], sha1(u["sentence_id"])))
    (RES / "panel_queue.json").write_text(json.dumps([{k: u[k] for k in ("sentence_id", "priority", "meta")} for u in units], indent=0))
    logger.info(f"panel queue: {len(units)} sentences, {sum(len(u['meta']) for u in units)} routed classes; "
                f"by best priority {dict(Counter(u['priority'] for u in units))}; routed classes by priority "
                f"{dict(Counter(p for u in units for p in u['meta'].values()))}")
    return units


def run_panel(cap: float, limit: int) -> None:
    units = build_units()
    if limit:
        units = units[:limit]
    asyncio.run(_run_units(units, "panel_free", cap, RES / "panel_free.jsonl"))


def assemble() -> None:
    """prereg final_label_rule with the panel as adjudicator -> results/free_labels.jsonl (one row per FREE candidate)."""
    lab = json.loads((RC / "work" / "rcomp_labels.json").read_text())
    S = sents()
    chk = json.loads((RES / "panel_check.json").read_text()) if (RES / "panel_check.json").exists() else {}
    provisional = chk.get("tier_B_provisional", True)
    votes, amb, reached = {}, defaultdict(dict), set()
    for r in jl(RES / "panel_free.jsonl"):
        if any("budget" in e for e in r.get("errors", [])):
            continue
        reached.add(r["sentence_id"])
        votes.update(r["votes"])
        amb[r["sentence_id"]] = r["ambiguous"]
    ref_flag = {}
    for sid in reached:
        vw, vs = votes.get(f"{sid}:REF_weak", {}), votes.get(f"{sid}:REF_strong", {})
        uw = maj(vw)[1] >= 2 if len(vw) >= 2 else False
        us = maj(vs)[1] >= 2 if len(vs) >= 2 else False
        ref_flag[sid] = {"weak_unfaithful": uw, "strong_unfaithful": us, "ref_flagged": uw and us}
    out = []
    for r in lab:
        sid = r["sentence_id"]
        L = r["solver_label"]
        cid = r["class_id"]
        pri = route({**r, "class_id": cid}) if cid else None
        v = votes.get(cid, {}) if cid else {}
        nf, nu, n = maj(v) if v else (0, 0, 0)
        rec = {"label": None, "label_tier": None, "label_source": None, "correct_not_equivalent": False, "adj_pending": False}
        if r.get("raw_output") is None:  # API failure (e.g. zero-shot G2 bodiless HTTP 404): no candidate exists
            rec.update(label="NO_OUTPUT", label_tier="-", label_source="api_failure")
        elif L == "UNPARSEABLE" or cid is None:
            rec.update(label="UNPARSEABLE", label_tier="-", label_source="parser")
        elif L == "CORRECT":
            rec.update(label="CORRECT", label_tier="A", label_source="solver", panel_dissent=(nu >= 2 if n >= 2 else None))
        elif pri in (1, 2):  # routed uncertain classes
            if sid not in reached or n < 2:
                rec.update(label="UNRESOLVED", label_tier="none", label_source="pending_panel")
            elif nf >= 2:
                rec.update(label="CORRECT", label_tier="B", label_source="solver+panel", correct_not_equivalent=True)
            elif nu >= 2:
                rec.update(label="ERROR", label_tier="B", label_source="solver+panel")
            else:
                rec.update(label="CONTESTED", label_tier="B", label_source="solver+panel")
        elif L == "ERROR":
            if pri in (3, 4) and sid in reached and n >= 2:
                if nf >= 2:
                    rec.update(label="CONTESTED", label_tier="A", label_source="solver_vs_panel")
                else:
                    rec.update(label="ERROR", label_tier="A", label_source="solver+panel")
            else:
                rec.update(label="ERROR", label_tier="A", label_source="solver", adj_pending=pri in (3, 4))
        else:  # VOCAB_GRAN/COMPOUND/TIMEOUT never routed (cannot happen) -> unresolved
            rec.update(label="UNRESOLVED", label_tier="none", label_source="unrouted")
        rf = ref_flag.get(sid, {}).get("ref_flagged", False)
        if rf and rec["label"] in ("CORRECT", "ERROR"):
            rec["label_tier"] = "C"
        s = S[sid]
        out.append({"row_key": f"{r['item_id']}|FREE|{r['slot']}|{r['prompt_variant']}", "item_id": r["item_id"], "sentence_id": sid,
                    "condition": "FREE", "system": r["system"], "slot": r["slot"], "family": r["family"], "model": r["model"],
                    "prompt_variant": r["prompt_variant"], "candidate_fol": r["candidate_fol"], "parse_ok": r["parse_ok"],
                    "solver_label": L, "solver_repair_ops": r.get("solver_repair_ops"), "matched_reading": r.get("solver_matched_reading"),
                    "only_if_converse": r.get("solver_only_if_converse"), "addrop_only_suspect": r.get("solver_addrop_only_suspect"),
                    "free_solver_class_id": cid, "route_priority": pri, "panel_votes": {m: x["faithful"] for m, x in v.items()} if v else None,
                    "panel_ops": sorted({o for x in v.values() if not x["faithful"] for o in x.get("ops", [])}) if v else None,
                    "reading_choice": False, "ref_flagged": rf, "ref_panel": ref_flag.get(sid),
                    "tier_B_provisional": provisional if rec["label_tier"] == "B" else None,
                    "template_id": s["template_id"], "clause_type": s["clause_type"], **rec})
    with (RES / "free_labels.jsonl").open("w") as fh:
        for r in out:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    logger.info(f"FREE labels: {dict(Counter((r['label'], r['label_tier']) for r in out))}; sentences reached {len(reached)}; "
                f"ref_flagged {sum(v['ref_flagged'] for v in ref_flag.values())}")


def main():
    logger.remove()
    logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
    logger.add(ROOT / "logs" / "panel_rcomp.log", rotation="30 MB", level="DEBUG")
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["check", "run", "assemble"])
    ap.add_argument("--cap", type=float, default=1.5)
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()
    if a.cmd == "check":
        run_check(a.cap)
    elif a.cmd == "run":
        run_panel(a.cap, a.limit)
    else:
        assemble()


if __name__ == "__main__":
    main()
