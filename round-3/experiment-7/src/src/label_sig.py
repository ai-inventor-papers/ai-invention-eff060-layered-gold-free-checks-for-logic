#!/usr/bin/env python3
"""S5: SIG labels by PURE z3 equivalence to the template references (no aligner, no panel, no LLM).

canon_case(c, sentence): every predicate / constant of candidate c is mapped case-insensitively onto the sentence's
signature (exact equality after lower-casing, nothing else). A symbol without a case-insensitive match makes the row
OFF_SIGNATURE; a matched predicate with a different arity makes it OFF_SIGNATURE_ARITY.
Secondary label view (pre-registered F3 'OFF_SIG_EXACT_RENAME'): the loose normaliser lower-cases and strips '_' and '-'
(still aligner-free: no similarity threshold).

Per sentence, on-signature candidates collapse into exact classes (identical normalised canonical string, or plain z3 EQ,
ms=3000). Per class: ew = equivalent(class, weak), es = vs strong, T8 also ec = vs the not-accepted converse
(ms=5000, retried at 20000 on None):
  ew or es True                  -> CORRECT (matched_reading weak / strong / both)
  T8 and ec True                 -> READING_CHOICE (excluded from the primary pool)
  ew False and es False (and ec False on T8) -> ERROR
  otherwise                      -> UNKNOWN (excluded, counted)
  parse failure                  -> UNPARSEABLE (coverage view only)

usage: label_sig.py label   -> results/sig_labels.jsonl (one row per SIG generation record) + results/sig_classes.json
       label_sig.py repair  -> results/sig_repairs.jsonl (secondary: minimal typed repair ops of ERROR classes)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import multiprocessing as mp
import re
import sys
import time
from collections import Counter, defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RC = ROOT / "rcomp"
for p in (RC / "labeller", RC / "src_e", ROOT / "src"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))
sys.setrecursionlimit(10000)
from fol import parse, equivalent  # noqa: E402
from repair_census import atoms, bound_vars  # noqa: E402

import sig_prompt as SP  # noqa: E402

RES = ROOT / "results"
GEN = RC / "raw" / "generations_sig.jsonl"


def sha1(s: str) -> str:
    return hashlib.sha1(s.encode()).hexdigest()


def item_id(system: str, text: str, raw: str) -> str:
    """Dataset E's item_id recipe: sha1(system | norm(text) | raw)[:16]."""
    import select_sentences as ss
    return sha1(system + "|" + ss.norm(text) + "|" + (raw or ""))[:16]


def _to_str(e) -> str:
    k = e[0]
    if k == "atom":
        return f"{e[1]}({', '.join(e[2])})" if e[2] else e[1]
    if k in ("all", "ex"):
        return f"{'∀' if k == 'all' else '∃'}{e[1]} ({_to_str(e[2])})"
    if k == "not":
        return f"¬({_to_str(e[1])})"
    sym = {"and": "∧", "or": "∨", "imp": "→", "iff": "↔", "xor": "⊕"}[k]
    return f"({_to_str(e[1])} {sym} {_to_str(e[2])})"


def _rename(e, pmap: dict, cmap: dict, bv=frozenset()):
    k = e[0]
    if k == "atom":
        return ("atom", pmap.get(e[1], e[1]), tuple(x if x in bv else cmap.get(x, x) for x in e[2]))
    if k in ("all", "ex"):
        return (k, e[1], _rename(e[2], pmap, cmap, bv | {e[1]}))
    if k == "not":
        return ("not", _rename(e[1], pmap, cmap, bv))
    return (k, _rename(e[1], pmap, cmap, bv), _rename(e[2], pmap, cmap, bv))


def _free_consts(e) -> set:
    out = set()

    def walk(x, bv):
        if x[0] == "atom":
            out.update(a for a in x[2] if a not in bv)
        elif x[0] in ("all", "ex"):
            walk(x[2], bv | {x[1]})
        elif x[0] == "not":
            walk(x[1], bv)
        else:
            walk(x[1], bv); walk(x[2], bv)
    walk(e, frozenset())
    return out


def _norm_loose(s: str) -> str:
    return re.sub(r"[_\-]", "", s.lower())


def canon_case(fol: str, sent: dict, loose: bool = False) -> tuple[str, object, dict]:
    """-> (status, canonical AST or None, info). status in ON_SIGNATURE / OFF_SIGNATURE / OFF_SIGNATURE_ARITY / UNPARSEABLE."""
    try:
        e = parse(fol)
    except Exception as ex:  # noqa: BLE001 - parser raises assorted errors on junk
        return "UNPARSEABLE", None, {"parse_error": str(ex)[:120]}
    sig_p, sig_c = SP.signature_symbols(sent)
    f = _norm_loose if loose else str.lower
    pl = defaultdict(list)
    for n in sig_p:
        pl[f(n)].append(n)
    cl = defaultdict(list)
    for c in sig_c:
        cl[f(c)].append(c)
    pmap, cmap, extra, arity_bad = {}, {}, [], []
    for a in atoms(e):
        name, ar = a[1], len(a[2])
        hits = pl.get(f(name), [])
        if len(hits) != 1:
            extra.append(f"{name}/{ar}")
            continue
        tgt = hits[0]
        if sig_p[tgt] != ar:
            arity_bad.append(f"{name}/{ar}->{tgt}/{sig_p[tgt]}")
            continue
        pmap[name] = tgt
    for c in _free_consts(e):
        hits = cl.get(f(c), [])
        if len(hits) != 1:
            extra.append(f"const:{c}")
        else:
            cmap[c] = hits[0]
    info = {"extra_symbols": sorted(set(extra)), "arity_mismatch": sorted(set(arity_bad))}
    if extra:
        return "OFF_SIGNATURE", None, info
    if arity_bad:
        return "OFF_SIGNATURE_ARITY", None, info
    return "ON_SIGNATURE", _rename(e, pmap, cmap), info


def signature_status(fol: str, sent: dict) -> tuple[str, dict]:
    st, _, info = canon_case(fol, sent)
    return st, info


def _eq(a, b) -> bool | None:
    r = equivalent(a, b, ms=5000)
    if r is None:
        r = equivalent(a, b, ms=20000)
    return r


def label_sentence(job: dict) -> dict:
    """Worker: all SIG rows of one sentence -> per-row status + class ids + class labels (strict and loose views)."""
    import sys as _s
    _s.setrecursionlimit(10000)
    sent, rows = job["sent"], job["rows"]
    t0 = time.time()
    refs = {"weak": parse(sent["reference_fol_weak"]), "strong": parse(sent["reference_fol_strong"])}
    if sent.get("reading_converse"):
        refs["converse"] = parse(sent["reading_converse"])
    out = {"sentence_id": sent["sentence_id"], "rows": {}, "classes": {}, "classes_loose": {}}
    for view in ("strict", "loose"):
        reps = []
        for r in rows:
            key = r["row_key"]
            if not r.get("parse_ok"):
                st, ast, info = "UNPARSEABLE", None, {}
            else:
                st, ast, info = canon_case(r["candidate_fol"], sent, loose=(view == "loose"))
            rec = out["rows"].setdefault(key, {})
            rec[f"sig_status_{view}"] = st
            if view == "strict":
                rec["sig_info"] = info
            if ast is None:
                rec[f"class_{view}"] = None
                continue
            cs = _to_str(ast)
            norm = re.sub(r"\s+", "", cs)
            hit = None
            for c in reps:
                if c["norm"] == norm:
                    hit = c; break
            if hit is None:
                for c in reps:
                    if equivalent(c["ast"], ast, ms=3000) is True:
                        hit = c; break
            if hit is None:
                hit = {"class_id": f"{sent['sentence_id']}:{'k' if view == 'strict' else 'l'}{len(reps)}", "norm": norm, "ast": ast, "fol": cs}
                reps.append(hit)
            rec[f"class_{view}"] = hit["class_id"]
            rec[f"canon_{view}"] = cs
        tgt = out["classes"] if view == "strict" else out["classes_loose"]
        for c in reps:
            ew, es = _eq(c["ast"], refs["weak"]), _eq(c["ast"], refs["strong"])
            ec = _eq(c["ast"], refs["converse"]) if "converse" in refs else None
            if ew is True or es is True:
                lab = "CORRECT"
                mr = "both" if (ew is True and es is True) else ("weak" if ew is True else "strong")
            elif "converse" in refs and ec is True:
                lab, mr = "READING_CHOICE", None
            elif ew is False and es is False and ("converse" not in refs or ec is False):
                lab, mr = "ERROR", None
            else:
                lab, mr = "UNKNOWN", None
            tgt[c["class_id"]] = {"fol": c["fol"], "label": lab, "matched_reading": mr, "eq_weak": ew, "eq_strong": es,
                                  "eq_converse": ec}
    out["secs"] = round(time.time() - t0, 2)
    return out


def load_sig_rows(sents: dict) -> list[dict]:
    last = {}
    for l in GEN.read_text().splitlines():
        if not l.strip():
            continue
        r = json.loads(l)
        if r["sentence_id"] in sents:
            last[(r["sentence_id"], r["slot"], r["prompt_variant"])] = r
    rows = []
    for r in last.values():
        if r.get("raw_output") is None:
            continue  # API failure: not a candidate (counted in the generation log)
        r = dict(r)
        r["item_id"] = item_id(r["system"], sents[r["sentence_id"]]["text"], r["raw_output"])
        r["row_key"] = r["item_id"] + "|SIG|" + r["slot"]
        rows.append(r)
    return rows


def run_label(workers: int = 16) -> None:
    from loguru import logger
    rs = json.loads((RC / "work" / "rcomp_sentences.json").read_text())
    sents = {r["sentence_id"]: r for r in rs}
    rows = load_sig_rows(sents)
    by = defaultdict(list)
    for r in rows:
        by[r["sentence_id"]].append(r)
    jobs = [{"sent": sents[sid], "rows": [{k: r[k] for k in ("row_key", "candidate_fol", "parse_ok")} for r in rr]}
            for sid, rr in sorted(by.items())]
    logger.info(f"SIG labelling: {len(rows)} rows over {len(jobs)} sentences, {workers} workers")
    res = {}
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=workers, mp_context=mp.get_context("spawn")) as ex:
        futs = {ex.submit(label_sentence, j): j["sent"]["sentence_id"] for j in jobs}
        for i, f in enumerate(as_completed(futs), 1):
            sid = futs[f]
            try:
                res[sid] = f.result(timeout=900)
            except Exception as e:  # noqa: BLE001 - one sentence must not kill the run; its rows become UNKNOWN
                logger.error(f"sentence {sid} failed: {type(e).__name__}: {e}")
                res[sid] = {"sentence_id": sid, "rows": {}, "classes": {}, "classes_loose": {}, "error": str(e)[:200]}
            if i % 25 == 0:
                logger.info(f"labelled {i}/{len(jobs)} sentences, {time.time() - t0:.0f}s")
    out_rows = []
    for r in rows:
        s = sents[r["sentence_id"]]
        o = res[r["sentence_id"]]["rows"].get(r["row_key"], {})
        cid, cidl = o.get("class_strict"), o.get("class_loose")
        st = o.get("sig_status_strict", "UNKNOWN_WORKER_FAIL")
        if st == "UNPARSEABLE":
            lab = "UNPARSEABLE"
        elif st.startswith("OFF_SIGNATURE"):
            lab = st
        elif cid is None:
            lab = "UNKNOWN"
        else:
            lab = res[r["sentence_id"]]["classes"][cid]["label"]
        cl = res[r["sentence_id"]]["classes"].get(cid, {}) if cid else {}
        stl = o.get("sig_status_loose")
        if stl == "UNPARSEABLE":
            labl = "UNPARSEABLE"
        elif stl and stl.startswith("OFF_SIGNATURE"):
            labl = stl
        elif cidl:
            labl = res[r["sentence_id"]]["classes_loose"][cidl]["label"]
        else:
            labl = "UNKNOWN"
        out_rows.append({"row_key": r["row_key"], "item_id": r["item_id"], "sentence_id": r["sentence_id"], "condition": "SIG",
                         "system": r["system"], "slot": r["slot"], "family": r["family"], "model": r["model"],
                         "prompt_variant": r["prompt_variant"], "raw_output": r["raw_output"], "candidate_fol": r["candidate_fol"],
                         "parse_ok": r["parse_ok"], "cost_usd": r.get("cost_usd"), "finish_reason": r.get("finish_reason"),
                         "label": lab, "label_source": "z3_exact_sig", "label_tier": "A_exact",
                         "matched_reading": cl.get("matched_reading"), "off_signature": st.startswith("OFF_SIGNATURE"),
                         "sig_status": st, "sig_info": o.get("sig_info"), "sig_class_id": cid, "canon_fol": o.get("canon_strict"),
                         "label_loose": labl, "sig_status_loose": stl, "sig_class_id_loose": cidl,
                         "template_id": s["template_id"], "clause_type": s["clause_type"]})
    with (RES / "sig_labels.jsonl").open("w") as fh:
        for r in out_rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    (RES / "sig_classes.json").write_text(json.dumps({sid: {"classes": v["classes"], "classes_loose": v["classes_loose"],
                                                            "secs": v.get("secs"), "error": v.get("error")}
                                                      for sid, v in res.items()}, ensure_ascii=False))
    logger.info(f"SIG labels: {dict(Counter(r['label'] for r in out_rows))}; loose view {dict(Counter(r['label_loose'] for r in out_rows))}; "
                f"{time.time() - t0:.0f}s")


def repair_class(job: dict) -> dict:
    import sys as _s
    _s.setrecursionlimit(10000)
    from label_lib import minimal_typed_repair
    c = parse(job["fol"])
    best = None
    for rd in ("weak", "strong"):
        ops, secs, st = minimal_typed_repair(c, parse(job[rd]), budget_s=8.0)
        if st == "FOUND" and (best is None or len(ops) < len(best[1])):
            best = (rd, ops)
    return {"class_id": job["class_id"], "repair_status": "FOUND" if best else "COMPOUND",
            "repair_reading": best[0] if best else None, "repair_ops": best[1] if best else None}


def run_repair(workers: int = 5) -> None:
    from loguru import logger
    sents = {r["sentence_id"]: r for r in json.loads((RC / "work" / "rcomp_sentences.json").read_text())}
    cls = json.loads((RES / "sig_classes.json").read_text())
    outp = RES / "sig_repairs.jsonl"
    done = {json.loads(l)["class_id"] for l in outp.read_text().splitlines() if l.strip()} if outp.exists() else set()
    jobs = []
    for sid, v in cls.items():
        for cid, c in v["classes"].items():
            if c["label"] == "ERROR" and cid not in done:
                jobs.append({"class_id": cid, "fol": c["fol"], "weak": sents[sid]["reference_fol_weak"],
                             "strong": sents[sid]["reference_fol_strong"]})
    logger.info(f"repair: {len(jobs)} ERROR classes")
    with ProcessPoolExecutor(max_workers=workers, mp_context=mp.get_context("spawn")) as ex, outp.open("a") as fh:
        futs = {ex.submit(repair_class, j): j for j in jobs}
        for f in as_completed(futs):
            try:
                r = f.result(timeout=120)
            except Exception as e:  # noqa: BLE001
                r = {"class_id": futs[f]["class_id"], "repair_status": "WORKER_FAIL", "error": str(e)[:200]}
            fh.write(json.dumps(r) + "\n")
            fh.flush()
    logger.info("repair done")


if __name__ == "__main__":
    from loguru import logger
    logger.remove()
    logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
    logger.add(ROOT / "logs" / "label_sig.log", rotation="30 MB", level="DEBUG")
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["label", "repair"])
    ap.add_argument("--workers", type=int, default=16)
    a = ap.parse_args()
    run_label(a.workers) if a.cmd == "label" else run_repair(a.workers)
