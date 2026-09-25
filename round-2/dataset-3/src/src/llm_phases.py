#!/usr/bin/env python3
"""STEP 4a/4b: fluency rating and pre-generation reference audit of the preselected R_COMP sentences.

  fluency   claude-haiku-4.5, 10 sentences per call, temperature 0; grammaticality/fluency 1-5, explicitly NOT truth or
            plausibility -> raw/fluency.jsonl (call cache) + raw/fluency_items.jsonl (one line per sentence)
  audit     ADJUDICATOR model (work/adjudicator_model.json), 5 sentences per call; each sentence shown with its two
            readings UNLABELLED as Reading A / Reading B (order sha1-shuffled; T8 also shows the converse as Reading C);
            per reading FAITHFUL/UNFAITHFUL (under some legitimate reading), ops, and whether it is the plain reading.
            REF_FLAGGED = a reading the model calls the plain reading is UNFAITHFUL, or no accepted reading is FAITHFUL.
            -> raw/ref_audit.jsonl + raw/ref_audit_items.jsonl
Both are resumable (cached per call key) and stop cleanly on the OpenRouter key limit or the phase cap.
"""
from __future__ import annotations

import argparse
import json

from common import RAW, W, append_jsonl, load_jsonl, sha1, setup_logger
from llm import ANTHROPIC_NO_THINK, run_jobs

logger = setup_logger("llm_phases")
HAIKU = "anthropic/claude-haiku-4.5"

FLU_SYS = """You rate English sentences for grammaticality and fluency only, on a 1-5 scale:
5 = fully grammatical and natural; 4 = grammatical, slightly awkward; 3 = grammatical but clumsy or hard to read;
2 = a grammatical error or badly garbled phrasing; 1 = ungrammatical or unreadable.
Do NOT judge whether the sentence is true, plausible, sensible or consistent with the world: odd or absurd content is fine.
Return ONLY compact JSON: {"ratings": [{"item": <number>, "rating": <1-5>}, ...]}"""

AUDIT_SYS = """You check candidate first-order-logic (FOL) readings of English sentences. For each numbered sentence you see two or three formulas (Reading A, B, C). For EACH reading decide whether it faithfully expresses the sentence under some legitimate reading of the sentence (FAITHFUL) or misstates it (UNFAITHFUL). Predicate names are fixed; judge the logical structure (which conditions restrict, which is the consequence, how unless/except/provided that/only if are rendered, negations). Also say which reading is the plain, most natural reading of the sentence (plain=true for exactly one reading, the one you would pick first). If UNFAITHFUL, list edit types from [NEG, REV, QUANT, RESTR, CONN, MOVE, DROP, ADD, SWAP, BIND, SCOPE, UNGLUE, MEANING_RENAME, OTHER].
Return ONLY compact JSON: {"sentences": [{"item": <number>, "readings": [{"reading": "A", "verdict": "FAITHFUL|UNFAITHFUL", "plain": true|false, "ops": [...]}, ...]}, ...]}"""


def preselected() -> list[dict]:
    return sorted(json.loads((W / "rcomp_preselect.json").read_text()), key=lambda r: r["sentence_id"])


def fluency(cap: float):
    sents = preselected()
    jobs = []
    for i in range(0, len(sents), 10):
        ch = sents[i:i + 10]
        body = "\n".join(f"{k}. {s['text']}" for k, s in enumerate(ch, 1))
        jobs.append({"key": sha1("flu|" + "|".join(s["sentence_id"] for s in ch))[:16], "ids": [s["sentence_id"] for s in ch],
                     "messages": [{"role": "system", "content": FLU_SYS}, {"role": "user", "content": body}]})
    res, stop = run_jobs("fluency", cap, HAIKU, jobs, RAW / "fluency.jsonl", logger, concurrency=8,
                         params={"temperature": 0.0, "max_tokens": 400},
                         validate=lambda j, p: isinstance(p, dict) and isinstance(p.get("ratings"), list))
    done = {r["sentence_id"] for r in load_jsonl(RAW / "fluency_items.jsonl")}
    for j in jobs:
        if j["key"] not in res:
            continue
        rs = {int(x["item"]): x.get("rating") for x in res[j["key"]]["parsed"]["ratings"] if str(x.get("item", "")).isdigit()}
        for k, sid in enumerate(j["ids"], 1):
            if sid in done or not isinstance(rs.get(k), (int, float)):
                continue
            append_jsonl(RAW / "fluency_items.jsonl", {"sentence_id": sid, "rating": int(rs[k]), "call_key": j["key"], "model": HAIKU})
    logger.info(f"fluency items: {len(load_jsonl(RAW / 'fluency_items.jsonl'))}; stopped={stop}")
    return stop


def audit_readings(s: dict) -> list[tuple[str, str, str]]:
    """[(label, role, fol)] with role weak/strong/converse, order shuffled by sha1(sentence_id)."""
    rd = [("weak", s["reference_fol_weak"]), ("strong", s["reference_fol_strong"])]
    order = sorted(rd, key=lambda x: sha1(s["sentence_id"] + x[0]))
    if s.get("reading_converse"):
        order.append(("converse", s["reading_converse"]))
    return [(chr(65 + i), role, f) for i, (role, f) in enumerate(order)]


def audit(cap: float):
    model_cfg = json.loads((W / "adjudicator_model.json").read_text())
    sents = preselected()
    jobs = []
    for i in range(0, len(sents), 5):
        ch = sents[i:i + 5]
        parts = []
        for k, s in enumerate(ch, 1):
            rds = audit_readings(s)
            parts.append(f"Sentence {k}: {s['text']}\n" + "\n".join(f"Reading {lab}: {f}" for lab, _, f in rds))
        jobs.append({"key": sha1("audit|" + "|".join(s["sentence_id"] for s in ch))[:16], "ids": [s["sentence_id"] for s in ch],
                     "messages": [{"role": "system", "content": AUDIT_SYS}, {"role": "user", "content": "\n\n".join(parts)}]})
    res, stop = run_jobs("reference_audit", cap, model_cfg["model"], jobs, RAW / "ref_audit.jsonl", logger, concurrency=8,
                         params={"temperature": 0.0, "max_tokens": 900, **ANTHROPIC_NO_THINK},
                         validate=lambda j, p: isinstance(p, dict) and isinstance(p.get("sentences"), list))
    byid = {s["sentence_id"]: s for s in sents}
    done = {r["sentence_id"] for r in load_jsonl(RAW / "ref_audit_items.jsonl")}
    for j in jobs:
        if j["key"] not in res:
            continue
        got = {int(x["item"]): x for x in res[j["key"]]["parsed"]["sentences"] if str(x.get("item", "")).isdigit()}
        for k, sid in enumerate(j["ids"], 1):
            if sid in done or k not in got:
                continue
            rds = {lab: role for lab, role, _ in audit_readings(byid[sid])}
            verdicts = []
            for r in got[k].get("readings", []):
                lab = str(r.get("reading", "")).strip().upper()[:1]
                if lab in rds:
                    verdicts.append({"reading": lab, "role": rds[lab], "verdict": r.get("verdict"), "plain": bool(r.get("plain")),
                                     "ops": r.get("ops") or []})
            acc = [v for v in verdicts if v["role"] in ("weak", "strong")]
            flagged = (any(v["plain"] and v["verdict"] == "UNFAITHFUL" and v["role"] in ("weak", "strong") for v in verdicts)
                       or not any(v["verdict"] == "FAITHFUL" for v in acc))
            append_jsonl(RAW / "ref_audit_items.jsonl", {"sentence_id": sid, "verdicts": verdicts, "ref_flagged": flagged,
                                                          "call_key": j["key"], "model": model_cfg["model"]})
    logger.info(f"audit items: {len(load_jsonl(RAW / 'ref_audit_items.jsonl'))}; stopped={stop}")
    return stop


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["fluency", "audit"])
    ap.add_argument("--cap", type=float, default=0.1)
    a = ap.parse_args()
    stop = fluency(a.cap) if a.cmd == "fluency" else audit(a.cap)
    raise SystemExit(3 if stop == "KEYLIMIT" else 0)  # a phase-cap stop is a planned truncation
