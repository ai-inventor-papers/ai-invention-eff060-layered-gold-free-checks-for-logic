#!/usr/bin/env python3
"""STEP 8: reference-aware adjudication with the shared ADJ-PROMPT (adjudication_prompt.txt = sibling R_ADJ V1, verbatim).

User message (sibling template + the ONLY R_COMP addition, both readings and the either-reading line):
  SENTENCE: <text>
  CANDIDATE FOL: <fol>
  REFERENCE FOL (VERIFIED), reading 1 (<weak label>): <weak>
  REFERENCE FOL (VERIFIED), reading 2 (<strong label>): <strong>
  A translation equivalent in meaning to either reading is faithful.
Model/params: work/adjudicator_model.json (claude-sonnet-5, temperature 0, max_tokens 300, reasoning disabled).
Parse failure -> one retry -> UNRESOLVED.

  select   8a known-label check items: 30 PERTURB + 30 PERTURB_CONTROL rows on R_COMP bases (ops spread, DROP / ADD /
           MEANING_RENAME included), sha1 order -> work/adjudicator_check_items.json   ($0)
  check    run the 60 known-label items (cap $0.2) -> raw/adjudication.jsonl; balanced accuracy -> work/adjudicator_check.json
  queue    8b priority queue over solver CLASSES (work/rcomp_labels.json), strict order P1 VOCAB_GRAN, P2 COMPOUND /
           TIMEOUT_UNKNOWN, P3 ERROR with addrop_only_suspect / SORTAL / ARITY_REIFY / XOR_OR / ONLY_IF_CONVERSE,
           P4 a 20% sha1 sample of other solver ERRORs; within a priority, sentences in sha1(sentence_id) order and
           SENTENCE-COMPLETE (a sentence's items are only dispatched if the remaining cap covers all of them)
  run      execute the queue under the $2.5 cap -> raw/adjudication.jsonl
"""
from __future__ import annotations

import argparse
import asyncio
import json
from collections import Counter, defaultdict

from common import RAW, ROOT, W, append_jsonl, dump, load_jsonl, sha1, setup_logger
from llm import parse_json
from or_client import BudgetExceeded, Client

logger = setup_logger("adjudicate")
OPS = ["NEG", "REV", "QUANT", "RESTR", "CONN", "MOVE", "DROP", "ADD", "SWAP", "BIND", "SCOPE", "UNGLUE", "MEANING_RENAME", "OTHER"]
READ_LABEL = {"T3": ("weak proviso", "strong proviso"), "T8": ("literal only-if", "biconditional")}
EST_COST = 0.0030  # $/call (sibling pilot mean 0.00276-0.0033)


def user_msg(text: str, cand: str, weak: str, strong: str, template_id: str) -> str:
    l1, l2 = READ_LABEL.get(template_id, ("weak exception", "strong exception"))
    return (f"SENTENCE: {text}\nCANDIDATE FOL: {cand}\nREFERENCE FOL (VERIFIED), reading 1 ({l1}): {weak}\n"
            f"REFERENCE FOL (VERIFIED), reading 2 ({l2}): {strong}\nA translation equivalent in meaning to either reading is faithful.")


def valid_verdict(p) -> bool:
    return isinstance(p, dict) and p.get("verdict") in ("FAITHFUL", "UNFAITHFUL", "AMBIGUOUS_READING")


def select_check():
    rows = [m for m in json.loads((W / "perturb_suite.json").read_text()) if m["base_source"] == "RCOMP"]
    ctr = [c for c in json.loads((W / "perturb_controls.json").read_text()) if c["base_source"] == "RCOMP"]
    rc = {r["sentence_id"]: r for r in json.loads((W / "rcomp_sentences.json").read_text())}
    by_op = defaultdict(list)
    for m in sorted(rows, key=lambda m: sha1("kl|" + m["item_id"])):
        by_op[m["select_key"]].append(m)
    must = ["DROP", "ADD", "MEANING_RENAME"]
    order = must + sorted(k for k in by_op if k not in must)
    pick, i = [], 0
    while len(pick) < 30 and any(by_op[k] for k in order):  # round-robin over ops, the must-have ops first
        k = order[i % len(order)]
        if by_op[k]:
            pick.append(by_op[k].pop(0))
        i += 1
    by_c = defaultdict(list)
    for c in sorted(ctr, key=lambda c: sha1("kl|" + c["item_id"])):
        by_c[c["control_type"]].append(c)
    cpick, i = [], 0
    ct = sorted(by_c)
    while len(cpick) < 30 and any(by_c[k] for k in ct):
        k = ct[i % len(ct)]
        if by_c[k]:
            cpick.append(by_c[k].pop(0))
        i += 1
    items = []
    for m, lab in [(m, "ERROR") for m in pick] + [(c, "CORRECT") for c in cpick]:
        s = rc[m["sentence_id"]]
        items.append({"item_id": m["item_id"], "sentence_id": m["sentence_id"], "known_label": lab,
                      "system": m["system"], "operator": m.get("operator"), "subtype": m.get("subtype"),
                      "control_type": m.get("control_type"), "position_polarity": m.get("position_polarity"),
                      "text": s["text"], "candidate_fol": m["candidate_fol"], "reference_fol_weak": s["reference_fol_weak"],
                      "reference_fol_strong": s["reference_fol_strong"], "template_id": s["template_id"]})
    dump(W / "adjudicator_check_items.json", items)
    logger.info(f"known-label items {len(items)}: {dict(Counter((i['known_label'], i['operator'] or i['control_type']) for i in items))}")


async def _call_all(items: list[dict], phase: str, cap: float, sentence_groups: list[list[dict]] | None = None):
    cfg = json.loads((W / "adjudicator_model.json").read_text())
    sysmsg = (ROOT / "adjudication_prompt.txt").read_text()
    done = {r["key"] for r in load_jsonl(RAW / "adjudication.jsonl") if r.get("verdict") is not None or r.get("final")}
    stop = False
    async with Client(phase, phase_cap=cap, concurrency=12, timeout=120) as client:
        async def one(it):
            msgs = [{"role": "system", "content": sysmsg}, {"role": "user", "content": it["user"]}]
            for attempt in range(2):
                r = await client.chat(cfg["model"], msgs, tag=f"{phase}:{it['key']}", retries=3, **cfg["params"])
                if r["text"] is None and "Key limit exceeded" in (r["error"] or ""):
                    return "KEYLIMIT"
                p = parse_json(r["text"])
                if valid_verdict(p):
                    append_jsonl(RAW / "adjudication.jsonl", {"key": it["key"], "phase": phase, "verdict": p["verdict"],
                                 "ops": [o for o in (p.get("ops") or []) if o in OPS], "location": p.get("location"),
                                 "reference_wrong": bool(p.get("reference_wrong")), "raw": r["text"], "cost_usd": r["cost_usd"],
                                 "model": cfg["model"], "attempt": attempt, "final": True})
                    return "OK"
            append_jsonl(RAW / "adjudication.jsonl", {"key": it["key"], "phase": phase, "verdict": None, "raw": r["text"],
                                                      "error": r["error"] or "parse_fail", "cost_usd": r["cost_usd"], "final": True})
            return "UNRESOLVED"
        groups = sentence_groups or [items[i:i + 12] for i in range(0, len(items), 12)]
        for g in groups:
            todo = [it for it in g if it["key"] not in done]
            if not todo:
                continue
            if client.spent_phase + len(todo) * EST_COST > cap:
                logger.warning(f"[{phase}] sentence-complete stop: ${client.spent_phase:.3f} + {len(todo)} items > cap {cap}")
                stop = "CAP"  # planned truncation: the pipeline continues (UNRESOLVED / adj_pending rows)
                break
            res = await asyncio.gather(*[one(it) for it in todo], return_exceptions=True)
            if "KEYLIMIT" in res:
                logger.error(f"[{phase}] stop: OpenRouter key limit"); stop = "KEYLIMIT"
                break
            if any(isinstance(x, BudgetExceeded) for x in res):
                logger.error(f"[{phase}] stop: phase/hard cap"); stop = "CAP"
                break
        logger.info(f"[{phase}] spent phase ${client.spent_phase:.4f} total ${client.spent_total:.4f}")
    return stop


def run_check(cap: float) -> bool:
    items = json.loads((W / "adjudicator_check_items.json").read_text())
    for it in items:
        it["key"] = "check|" + it["item_id"]
        it["user"] = user_msg(it["text"], it["candidate_fol"], it["reference_fol_weak"], it["reference_fol_strong"], it["template_id"])
    stop = asyncio.run(_call_all(items, "known_label_check", cap))
    res = {r["key"]: r for r in load_jsonl(RAW / "adjudication.jsonl") if r.get("final")}
    tp = tn = npos = nneg = unres = amb = 0
    per = []
    for it in items:
        r = res.get(it["key"])
        v = r.get("verdict") if r else None
        per.append({"item_id": it["item_id"], "known_label": it["known_label"], "verdict": v,
                    "ops": (r or {}).get("ops"), "operator": it["operator"], "control_type": it["control_type"]})
        if r is None:
            continue
        if v is None:
            unres += 1
        if v == "AMBIGUOUS_READING":
            amb += 1
        if it["known_label"] == "ERROR":
            npos += 1; tp += v == "UNFAITHFUL"
        else:
            nneg += 1; tn += v == "FAITHFUL"
    rec_e = tp / npos if npos else None
    rec_c = tn / nneg if nneg else None
    ba = (rec_e + rec_c) / 2 if npos and nneg else None
    out = {"n_items": len(items), "n_answered": npos + nneg, "recall_error": rec_e, "recall_correct": rec_c,
           "balanced_accuracy": ba, "unresolved": unres, "ambiguous_reading": amb,
           "tier_B_provisional_by_check": (ba is not None and ba < 0.80), "complete": npos + nneg == len(items), "rows": per}
    dump(W / "adjudicator_check.json", out)
    logger.info(f"known-label check: BA {ba} (E recall {rec_e}, C recall {rec_c}) n={npos + nneg}/{len(items)}")
    return stop


def build_queue() -> list[dict]:
    lab = json.loads((W / "rcomp_labels.json").read_text())
    rc = {r["sentence_id"]: r for r in json.loads((W / "rcomp_sentences.json").read_text())}
    cls = {}
    for r in lab:
        if r["class_id"] and r["class_id"] not in cls:
            cls[r["class_id"]] = r
    q = []
    for cid, r in cls.items():
        L = r["solver_label"]
        flags = set(r.get("solver_convention_flags") or [])
        pri = None
        if L == "VOCAB_GRAN":
            pri = 1
        elif L in ("COMPOUND", "TIMEOUT_UNKNOWN"):
            pri = 2
        elif L == "ERROR" and (r.get("solver_addrop_only_suspect") or flags & {"SORTAL", "ARITY_REIFY", "XOR_OR"}
                               or r.get("solver_only_if_converse")):
            pri = 3
        elif L == "ERROR" and int(sha1("p4|" + cid)[:8], 16) / 16 ** 8 < 0.20:
            pri = 4
        if pri is None and r.get("solver_only_if_converse"):
            pri = 3
        if pri is None:
            continue
        s = rc[r["sentence_id"]]
        q.append({"key": "rcomp|" + cid, "class_id": cid, "sentence_id": r["sentence_id"], "priority": pri,
                  "user": user_msg(s["text"], r["candidate_fol"], s["reference_fol_weak"], s["reference_fol_strong"], s["template_id"])})
    q.sort(key=lambda x: (x["priority"], sha1(x["sentence_id"]), x["class_id"]))
    dump(W / "adjudication_queue.json", q)
    logger.info(f"queue {len(q)} class-items: {dict(Counter(x['priority'] for x in q))}; est ${len(q) * EST_COST:.2f}")
    return q


def run_queue(cap: float) -> bool:
    q = json.loads((W / "adjudication_queue.json").read_text())
    groups, cur, key = [], [], None
    for it in q:  # sentence-complete units within each priority
        k = (it["priority"], it["sentence_id"])
        if k != key and cur:
            groups.append(cur); cur = []
        cur.append(it); key = k
    if cur:
        groups.append(cur)
    return asyncio.run(_call_all(q, "adjudication", cap, sentence_groups=groups))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["select", "check", "queue", "run"])
    ap.add_argument("--cap", type=float, default=2.5)
    a = ap.parse_args()
    if a.cmd == "select":
        select_check()
    elif a.cmd == "check":
        raise SystemExit(3 if run_check(a.cap) == "KEYLIMIT" else 0)
    elif a.cmd == "queue":
        build_queue()
    else:
        raise SystemExit(3 if run_queue(a.cap) == "KEYLIMIT" else 0)
