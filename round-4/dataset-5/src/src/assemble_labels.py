#!/usr/bin/env python3
"""STEP G: one label per FREE generation row from the map search (+ gloss verdicts when available), testability
declaration and the seal (sha256 over the sorted (row_key, label) vector). Nothing from exp 7's label / score files is
read here (the post-seal join is src/post_seal_join.py).

Modes: search-only (no verdict file / gate not passed): MAPPED -> UNRESOLVED_GLOSS_NOT_RUN (or _GATE_FAILED).
       final (results/gloss_verdicts.jsonl + a passing gate): prereg gloss rule (f) + D8.
usage: assemble_labels.py [--mode search_only|final]
"""
from __future__ import annotations

import argparse
import json
import time
from collections import Counter, defaultdict

from common import RES, ROOT, WORK, dump, load_jsonl, setup_logger, sha256_bytes, sha256_file
from run_search import class_key

logger = setup_logger("assemble")
BINARY = {"CORRECT": "CORRECT", "ERROR_CERT": "ERROR", "ERROR_GLOSS": "ERROR"}


def word_tercile(w: int) -> str:
    return "W1" if w < 30 else ("W2" if w < 35 else "W3")


def load_verdicts() -> dict:
    """{(sentence_id, use, meaning): (haiku, qwen)} from results/gloss_verdicts.jsonl (written by resume_gloss.py)."""
    p = RES / "gloss_verdicts.jsonl"
    out = {}
    if p.exists():
        for r in load_jsonl(p):
            out[(r["sentence_id"], r["use"], r["meaning"])] = (r.get("haiku"), r.get("qwen"))
    return out


def label_rows(mode: str) -> list[dict]:
    import freelab as FL
    sents = json.loads((WORK / "sentences.json").read_text())
    search = {r["class_key"]: r for r in load_jsonl(RES / "map_search.jsonl")}
    verdicts = load_verdicts() if mode == "final" else {}
    gate_ok = False
    if mode == "final":
        gr = json.loads((RES / "gate_report.json").read_text())
        gate_ok = any(v.get("PASS") for v in gr.values())
    out = []
    for r in load_jsonl(WORK / "free_rows.jsonl"):
        s = sents[r["sentence_id"]]
        base = {k: r[k] for k in ("row_key", "item_id", "sentence_id", "slot", "system", "family", "model", "prompt_variant",
                                  "raw_output", "candidate_fol")}
        base.update(template_id=s["template_id"], clause_type=s["clause_type"], words=s["words"],
                    word_tercile=word_tercile(s["words"]), nconds_weak=s["nconds_weak"],
                    negated_condition=s["negated_condition"], nested=s["nested"], text=s["text"])
        if r["input_status"] != "PARSED":
            out.append({**base, "label": r["input_status"], "search_status": None, "label_source": "input",
                        "unresolved_reason": None})
            continue
        ck = class_key(r["sentence_id"], r["candidate_fol"])
        sr = search.get(ck)
        if sr is None:
            out.append({**base, "label": "UNRESOLVED_SEARCH_CAP", "search_status": "MISSING", "label_source": "exhaustive_map_v1",
                        "unresolved_reason": "class missing from map_search.jsonl"})
            continue
        rec = {**base, "class_key": ck, "search_status": sr["status"], "matched_reading_search": sr.get("matched_reading"),
               "n_maps_enumerated": sr.get("n_maps_enumerated"), "n_maps_fingerprint_pass": sr.get("n_maps_fingerprint_pass"),
               "n_equiv_maps": sr.get("n_equiv_maps"), "n_equiv_pairsets": sr.get("n_equiv_pairsets"),
               "n_equiv_map_orbits": sr.get("n_equiv_map_orbits"),
               "nonequiv_certificate_type_counts": sr.get("nonequiv_certificate_type_counts"),
               "irrelevant_symbols": sr.get("irrelevant_symbols"), "search_secs": sr.get("search_secs"),
               "label_source": "exhaustive_map_v1"}
        st = sr["status"]
        if st != "MAPPED":
            rec.update(label=st, unresolved_reason=st if st.startswith("UNRESOLVED") else None, map_certificate=None,
                       gloss_pairs=None, gloss_decision=None)
            out.append(rec)
            continue
        ents = sr["map_entries_union"]
        maps = sr["equiv_maps"]
        first = next((m for m in maps if m["reading"] != "converse"), maps[0])
        pairs = [{"cand_atom": u, "meaning": m,
                  "haiku": verdicts.get((r["sentence_id"], u, m), (None, None))[0],
                  "qwen": verdicts.get((r["sentence_id"], u, m), (None, None))[1]} for u, m in sr["pairs_union"]]
        if mode != "final":
            rec.update(label="UNRESOLVED_GLOSS_NOT_RUN", unresolved_reason="gloss check not run (D9: API budget exhausted)",
                       gloss_decision=None,
                       map_certificate={"status": "z3_equivalent_map_not_gloss_checked", "reading": first["reading"],
                                        "map": [ents[i] for i in first["entry_ids"]], "bridges": first["bridges"]})
        elif not gate_ok:
            rec.update(label="UNRESOLVED_GLOSS_GATE_FAILED", unresolved_reason="gloss gate failed twice", gloss_decision=None,
                       map_certificate=None)
        else:
            vd = {(u, m): verdicts.get((r["sentence_id"], u, m), (None, None)) for u, m in sr["pairs_union"]}
            lab, idx = FL.gloss_decision(maps, sr["pairs_union"], vd)
            cert = None
            if idx is not None:
                m = maps[idx]
                cert = {"status": "z3_equivalent_and_gloss_accepted", "reading": m["reading"],
                        "map": [ents[i] for i in m["entry_ids"]], "bridges": m["bridges"]}
            rec.update(label=lab, gloss_decision=lab, map_certificate=cert,
                       unresolved_reason="mixed or missing checker verdicts" if lab == "UNRESOLVED_GLOSS" else None,
                       label_source="exhaustive_map_v1+gloss_v1")
            if lab == "CORRECT":
                rec["matched_reading"] = maps[idx]["reading"]
        rec["gloss_pairs"] = pairs
        out.append(rec)
    for o in out:
        o["label_binary"] = BINARY.get(o["label"], "EXCLUDED")
    return out


def testability(rows: list[dict], name: str) -> dict:
    def block(rs):
        c = Counter(r["label_binary"] for r in rs)
        se = {k: len({r["sentence_id"] for r in rs if r["label_binary"] == k}) for k in ("ERROR", "CORRECT")}
        return {"n_ERROR": c["ERROR"], "n_CORRECT": c["CORRECT"], "sentences_with_ERROR": se["ERROR"],
                "sentences_with_CORRECT": se["CORRECT"],
                "TESTABLE": bool(c["ERROR"] >= 50 and c["CORRECT"] >= 50 and se["ERROR"] >= 25 and se["CORRECT"] >= 25),
                "reportable_30_30": bool(c["ERROR"] >= 30 and c["CORRECT"] >= 30),
                "label_counts": dict(Counter(r["label"] for r in rs))}
    out = {"population": name, "n_rows": len(rows), **block(rows), "strata": {}}
    for key in ("template_id", "clause_type", "word_tercile", "prompt_variant", "slot"):
        g = defaultdict(list)
        for r in rows:
            g[r[key]].append(r)
        out["strata"][key] = {k: block(v) for k, v in sorted(g.items())}
    n1, n0 = out["n_ERROR"], out["n_CORRECT"]
    if n1 and n0:
        import math
        # Hanley-McNeil SE of AUROC at 0.75 as a planning figure; MDE ~ 2.8 * SE (two-sided 5%, 80% power)
        a = 0.75
        q1, q2 = a / (2 - a), 2 * a * a / (1 + a)
        se = math.sqrt((a * (1 - a) + (n1 - 1) * (q1 - a * a) + (n0 - 1) * (q2 - a * a)) / (n1 * n0))
        out["auroc_se_at_0.75"] = round(se, 4)
        out["auroc_mde_approx"] = round(2.8 * se, 4)
    return out


def label_vector_sha(rows: list[dict]) -> str:
    v = sorted((r["row_key"], r["label"]) for r in rows)
    return sha256_bytes(json.dumps(v, ensure_ascii=False).encode())


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["search_only", "final"], default="search_only")
    a = ap.parse_args()
    rows = label_rows(a.mode)
    with (RES / "free_labels_v2.jsonl").open("w") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    logger.info(f"labels ({a.mode}): {dict(Counter(r['label'] for r in rows))}")
    t = {"mode": a.mode, "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
         "rule": "TESTABLE iff >= 50 ERROR and >= 50 CORRECT rows, each class spread over >= 25 sentences",
         "word_terciles": {"cut_1": 30, "cut_2": 35}, "all_rows": testability(rows, "all FREE rows"),
         "untouched_subset": "declared after the seal by src/post_seal_join.py (needs exp-7 label tiers)"}
    if a.mode == "search_only":
        t["note"] = ("SEARCH-ONLY labels (D9): no CORRECT class exists until the gloss step runs, so AUROC is NOT_TESTABLE; "
                     "the ERROR_CERT class alone supports recall-type analyses; MAPPED rows are UNRESOLVED_GLOSS_NOT_RUN")
    dump(RES / "testability_FREE_v2.json", t)
    seal = {"utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "mode": a.mode,
            "label_vector_sha256_all_rows": label_vector_sha(rows), "n_rows": len(rows),
            "label_counts": dict(Counter(r["label"] for r in rows)),
            "prereg_sha256": (ROOT / "prereg_freelab.sha256").read_text().split()[0],
            "prereg_v1_sha256": (ROOT / "prereg_freelab_v1.sha256").read_text().split()[0],
            "vendor_sha256": json.loads((ROOT / "VENDOR_SHA256.json").read_text())["vendor"],
            "code_sha256": {p: sha256_file(ROOT / p) for p in ("src/freelab.py", "src/run_search.py", "src/assemble_labels.py")},
            "map_search_sha256": sha256_file(RES / "map_search.jsonl"),
            "old_labels_joined": False}
    prev = json.loads((RES / "seal.json").read_text()) if (RES / "seal.json").exists() else {"seals": []}
    prev["seals"].append(seal)
    dump(RES / "seal.json", prev)
    logger.info(f"sealed {a.mode}: {seal['label_vector_sha256_all_rows']}")


if __name__ == "__main__":
    main()
