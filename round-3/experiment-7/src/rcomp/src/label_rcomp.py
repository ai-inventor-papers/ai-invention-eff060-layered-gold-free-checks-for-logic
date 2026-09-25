#!/usr/bin/env python3
"""STEP 7: solver labels for R_COMP candidates against BOTH readings (E's shared labeller, labeller/label_lib.py).

Per candidate class c (classes = identical normalised string or plain z3 EQ with identical symbols, per sentence;
never modulo vocabulary):
  lw = auto_label(c, weak, repair=False); ls = auto_label(c, strong, repair=False); T8 also lc = vs the converse
  - lw or ls CORRECT                       -> CORRECT, tier A, matched_reading weak / strong / both
  - else lw or ls VOCAB_GRAN               -> VOCAB_GRAN (routed P1)
  - else lw or ls TIMEOUT_UNKNOWN          -> TIMEOUT_UNKNOWN (routed P2)
  - else minimal_typed_repair vs weak AND strong (8 s each): FOUND with fewest ops (tie -> weak) -> ERROR(ops), tier A,
    repair_reading; neither FOUND -> COMPOUND (routed P2)
  - parse failure                          -> UNPARSEABLE (kept)
Also: convention_flags(c, weak); addrop_only_suspect (repair ops only ADD/DROP); ONLY_IF_CONVERSE (T8: c equivalent,
modulo vocabulary, to the NOT-accepted converse); lex_anchored_vocab (DIAGNOSTIC ONLY: every renamed predicate pair of
align(c, ref) shares a Porter stem with the reference atom's lexicon phrase).
ProcessPool of 4 (spawn), per-class hard guard 60 s, pair cache work/label_pair_cache.jsonl keyed sha1(cand|ref).
Input: raw/generations.jsonl (latest record per key) -> work/rcomp_labels.json.  --dry-run labels a synthetic
candidate set (PERTURB mutants/controls + vocabulary renames of R_COMP references) to test the code path only.
"""
from __future__ import annotations

import argparse
import json
import multiprocessing as mp
import re
from collections import Counter, defaultdict
from concurrent.futures import ProcessPoolExecutor, TimeoutError as FutTimeout

from common import RAW, ROOT, W, append_jsonl, dump, load_jsonl, sha1, setup_logger

GUARD_S = 60


def _stems(s: str) -> set:
    from nltk.stem import PorterStemmer
    ps = PorterStemmer()
    return {ps.stem(w) for w in re.findall(r"[a-z]+", s.lower()) if len(w) > 2}


def label_class(job: dict) -> dict:
    """Worker: label one candidate class of one sentence."""
    import common  # noqa: F401
    from fol import parse
    from label_lib import auto_label, minimal_typed_repair, convention_flags
    from repair_census import align, toks
    cand, weak, strong, conv = job["cand"], job["weak"], job["strong"], job.get("converse")
    out = {"class_key": job["class_key"]}
    try:
        c = parse(cand)
    except Exception as ex:  # noqa: BLE001 - parser raises assorted errors on junk
        return {**out, "label": "UNPARSEABLE", "parse_error": str(ex)[:120]}
    lw = auto_label(cand, weak, repair=False)
    ls = auto_label(cand, strong, repair=False) if strong else None
    out["auto_label_weak"], out["auto_label_strong"] = lw["auto_label"], (ls or {}).get("auto_label")
    out["equiv_status_weak"], out["equiv_status_strong"] = lw["equiv_status"], (ls or {}).get("equiv_status")
    if conv:
        lc = auto_label(cand, conv, repair=False)
        out["converse_status"] = lc["equiv_status"]
        out["only_if_converse"] = lc["auto_label"] in ("CORRECT", "VOCAB_GRAN")
    else:
        out["only_if_converse"] = False
    labs = [lw["auto_label"], (ls or {}).get("auto_label")]
    rw = parse(weak)
    out["convention_flags"] = convention_flags(c, rw)
    if "CORRECT" in labs:
        out["label"], out["label_tier"] = "CORRECT", "A"
        out["matched_reading"] = "both" if labs[0] == labs[1] == "CORRECT" else ("weak" if labs[0] == "CORRECT" else "strong")
    elif "VOCAB_GRAN" in labs:
        out["label"] = "VOCAB_GRAN"
        out["matched_reading_modulo_vocab"] = "both" if labs[0] == labs[1] else ("weak" if labs[0] == "VOCAB_GRAN" else "strong")
        # diagnostic lex_anchored_vocab: renamed predicates share a stem with the reference atom's lexicon phrase
        ref = rw if labs[0] == "VOCAB_GRAN" else parse(strong)
        _, pmap, _ = align(c, ref)
        phr = job.get("atom_phrases", {})
        ok = bool(pmap)
        for (p, _ar), q in pmap.items():
            vp = phr.get(q)
            if vp is None or not (set(toks(p)) and ({w for w in _stems(" ".join(toks(p)))} & _stems(vp))):
                ok = False
        out["lex_anchored_vocab"] = ok
    elif "TIMEOUT_UNKNOWN" in labs:
        out["label"] = "TIMEOUT_UNKNOWN"
    else:
        best = None
        for rd, ref in (("weak", weak), ("strong", strong)):
            if not ref:
                continue
            ops, secs, st = minimal_typed_repair(c, parse(ref), budget_s=8.0)
            out[f"repair_status_{rd}"] = st
            if st == "FOUND" and (best is None or len(ops) < len(best[1])):
                best = (rd, ops)
        if best:
            out["label"], out["label_tier"], out["repair_reading"], out["repair_ops"] = "ERROR", "A", best[0], best[1]
            out["addrop_only_suspect"] = set(best[1]) <= {"ADD", "DROP"}
        else:
            out["label"] = "COMPOUND"
    return out


def classes_for(sent: dict, cands: list[dict]) -> tuple[dict, dict]:
    """Collapse candidates of one sentence into classes: identical normalised string, then plain z3 EQ with identical
    symbols between class representatives (never modulo vocabulary)."""
    from fol import parse, equivalent
    from repair_census import symbols
    reps, cls_of = [], {}
    for c in cands:
        f = (c.get("candidate_fol") or "").strip()
        if not c.get("parse_ok"):
            cls_of[c["item_id"]] = None
            continue
        norm = re.sub(r"\s+", "", f)
        hit = None
        try:
            e = parse(f)
            sy = symbols(e)
        except Exception:  # noqa: BLE001
            cls_of[c["item_id"]] = None
            continue
        for r in reps:
            if r["norm"] == norm or (r["symbols"] == sy and equivalent(r["ast"], e, ms=3000) is True):
                hit = r; break
        if hit is None:
            hit = {"class_id": f"{sent['sentence_id']}:k{len(reps)}", "norm": norm, "fol": f, "ast": e, "symbols": sy}
            reps.append(hit)
        cls_of[c["item_id"]] = hit["class_id"]
    return {r["class_id"]: r["fol"] for r in reps}, cls_of


def load_candidates(sents: dict) -> list[dict]:
    """Latest generations.jsonl record per (sentence_id, slot, prompt_variant) for R_COMP sentences, with E's item_id."""
    import select_sentences as ss
    last = {}
    for r in load_jsonl(RAW / "generations.jsonl"):
        if r["sentence_id"] in sents:
            last[(r["sentence_id"], r["slot"], r["prompt_variant"])] = r
    out = []
    for r in last.values():
        if r.get("final_failure") and "Key limit exceeded" in (r.get("api_error") or ""):
            continue  # not data: retried by generate.py
        raw = r.get("raw_output") or ""
        r = dict(r)
        r["item_id"] = sha1(r["system"] + "|" + ss.norm(sents[r["sentence_id"]]["text"]) + "|" + raw)[:16]
        out.append(r)
    return out


def dry_run_candidates(sents: dict) -> list[dict]:
    """Synthetic candidates to exercise the code path: PERTURB mutants/controls on R_COMP bases + vocab renames."""
    rows = [m for m in json.loads((W / "perturb_suite.json").read_text()) if m["base_source"] == "RCOMP"][:60]
    ctr = [c for c in json.loads((W / "perturb_controls.json").read_text()) if c["base_source"] == "RCOMP"][:30]
    out = []
    for m in rows + ctr:
        out.append({"sentence_id": m["sentence_id"], "system": m["system"], "slot": "DRY", "prompt_variant": "none",
                    "candidate_fol": m["candidate_fol"], "raw_output": m["candidate_fol"], "parse_ok": True,
                    "item_id": m["item_id"], "expected": "ERROR" if m["system"].startswith("PERTURB") else "CORRECT_OR_VG"})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    logger = setup_logger("label_rcomp")
    rs = json.loads((W / "rcomp_sentences.json").read_text())
    sents = {r["sentence_id"]: r for r in rs}
    lex = {e["lexicon_id"]: e for e in json.loads((ROOT / "lexicon.json").read_text())["entries"]}
    cands = dry_run_candidates(sents) if a.dry_run else load_candidates(sents)
    logger.info(f"candidates {len(cands)} over {len({c['sentence_id'] for c in cands})} sentences")
    by_s = defaultdict(list)
    for c in cands:
        by_s[c["sentence_id"]].append(c)
    cache_p = W / ("label_pair_cache_dryrun.jsonl" if a.dry_run else "label_pair_cache.jsonl")
    cache = {r["pair_key"]: r for r in load_jsonl(cache_p)}
    jobs, cls_all, class_fol = [], {}, {}
    for sid, cs in sorted(by_s.items()):
        s = sents[sid]
        reps, cls_of = classes_for(s, cs)
        cls_all.update(cls_of)
        phr = {lex[x]["pred_final"]: lex[x]["vp_sg_pos"] for x in s["lexicon_ids"] if x in lex}
        for cid, fol in reps.items():
            class_fol[cid] = fol
            pk = sha1(fol + "|" + s["reference_fol_weak"] + "|" + s["reference_fol_strong"])
            if pk in cache:
                continue
            jobs.append({"class_key": cid, "pair_key": pk, "cand": fol, "weak": s["reference_fol_weak"],
                         "strong": s["reference_fol_strong"], "converse": s.get("reading_converse"), "atom_phrases": phr})
    logger.info(f"classes {len(class_fol)}; to label {len(jobs)} (cache {len(cache)})")
    with ProcessPoolExecutor(max_workers=int(__import__('os').environ.get('RCOMP_LABEL_WORKERS', '4')), mp_context=mp.get_context("spawn")) as pool:  # PATCH iter3 exp7: worker count from env (48-core box)
        futs = [(j, pool.submit(label_class, j)) for j in jobs]
        for n, (j, f) in enumerate(futs, 1):
            try:
                r = f.result(timeout=GUARD_S * 4)
            except FutTimeout:
                r = {"class_key": j["class_key"], "label": "TIMEOUT_UNKNOWN", "guard_timeout": True}
            except Exception as ex:  # noqa: BLE001 - one class must not kill the run
                logger.error(f"class {j['class_key']} failed: {type(ex).__name__}: {ex}")
                r = {"class_key": j["class_key"], "label": "TIMEOUT_UNKNOWN", "worker_error": str(ex)[:200]}
            r["pair_key"] = j["pair_key"]
            append_jsonl(cache_p, r)
            cache[j["pair_key"]] = r
            if n % 100 == 0:
                logger.info(f"{n}/{len(jobs)} classes labelled")
    rows = []
    for c in cands:
        s = sents[c["sentence_id"]]
        cid = cls_all.get(c["item_id"])
        if cid is None:
            lab = {"label": "UNPARSEABLE"}
        else:
            pk = sha1(class_fol[cid] + "|" + s["reference_fol_weak"] + "|" + s["reference_fol_strong"])
            lab = {k: v for k, v in cache[pk].items() if k not in ("class_key", "pair_key")}
        rows.append({**{k: c.get(k) for k in ("item_id", "sentence_id", "system", "slot", "family", "model", "prompt_variant",
                                                "raw_output", "candidate_fol", "parse_ok", "parse_error", "api_error",
                                                "cost_usd", "normalisation_applied", "finish_reason", "provider", "expected")},
                     "class_id": cid, **{f"solver_{k}": v for k, v in lab.items()}})
    csize = Counter(r["class_id"] for r in rows if r["class_id"])
    for r in rows:
        r["class_size"] = csize.get(r["class_id"])
    out = W / ("rcomp_labels_dryrun.json" if a.dry_run else "rcomp_labels.json")
    dump(out, rows)
    logger.info(f"labels: {dict(Counter(r['solver_label'] for r in rows))}")
    if a.dry_run:
        logger.info(f"dry-run expected vs solver: {dict(Counter((r['expected'], r['solver_label']) for r in rows))}")


if __name__ == "__main__":
    main()
