#!/usr/bin/env python3
"""STEP A2-A6: sentences + references + lexicon glosses, FREE candidate rows (raw generations only), SIG rows,
input count table and the label-free shape census.

Outputs: work/sentences.json (221 FREE sentences with template units + glosses), work/free_rows.jsonl (one row per
FREE generation record, last record per (sentence_id, slot, prompt_variant)), work/sig_rows.jsonl,
results/input_counts.json, results/shape_census.json.
NEVER reads exp 7 label, score or evaluator-model output files (firewall; see tests/test_firewall.py).
"""
from __future__ import annotations

import json
import random
import re
from collections import Counter, defaultdict

from common import (D3_FULL, GEN_FREE, LEXICON, RES, SENTS, SIG_LABELS, WORK, dump, item_id, load_jsonl,
                    setup_logger)
from fol import parse
from repair_census_min import atoms, bound_vars

logger = setup_logger("inputs")


def unit_str(a) -> str:
    return f"{a[1]}({', '.join(a[2])})" if a[2] else a[1]


def template_units(sent: dict, lex: dict) -> dict:
    """Template atoms of every stored reading -> {unit_str: {pred, arity, args, const, gloss}} with the gloss taken from
    the lexicon entry whose pred_final equals the predicate (NEVER from the name)."""
    gl = {}
    for lid in sent["lexicon_ids"]:
        e = lex.get(lid)
        if e is not None:
            gl[e["pred_final"]] = e
    units = {}
    for key in ("reference_fol_weak", "reference_fol_strong", "reading_converse"):
        f = sent.get(key)
        if not f:
            continue
        e = parse(f)
        bv = bound_vars(e)
        for a in atoms(e):
            u = unit_str(a)
            if u in units:
                continue
            le = gl.get(a[1])
            if le is None:
                raise KeyError(f"no lexicon entry for {a[1]} in {sent['sentence_id']}")
            consts = [x for x in a[2] if x not in bv]
            units[u] = {"pred": a[1], "arity": len(a[2]), "args": list(a[2]), "consts": consts,
                        "gloss_pos": "x " + le["vp_sg_pos"], "gloss_neg": "x " + le["vp_sg_neg"],
                        "lexicon_id": le["lexicon_id"], "const_field": le.get("const")}
    return units


def main() -> None:
    lex = {e["lexicon_id"]: e for e in json.loads(LEXICON.read_text())["entries"]}
    sents_all = {s["sentence_id"]: s for s in json.loads(SENTS.read_text())}
    gens = load_jsonl(GEN_FREE)
    last = {}
    for r in gens:
        last[(r["sentence_id"], r["slot"], r["prompt_variant"])] = r
    free_sids = sorted({k[0] for k in last})
    logger.info(f"generations.jsonl: {len(gens)} records -> {len(last)} last-per-key rows over {len(free_sids)} sentences")
    # cross-check against dataset 3's rcomp_sentences group
    d3 = json.loads(D3_FULL.read_text())
    d3_rs = {}
    for g in d3["datasets"]:
        if g["dataset"] == "rcomp_sentences":
            for ex in g["examples"]:
                inp = json.loads(ex["input"]) if isinstance(ex["input"], str) else ex["input"]
                d3_rs[ex.get("metadata_sentence_id") or inp.get("sentence_id")] = (inp, ex)
    xcheck = Counter()
    for sid in free_sids:
        s = sents_all[sid]
        if sid not in d3_rs:
            xcheck["missing_in_d3"] += 1
            continue
        inp, ex = d3_rs[sid]
        same = (inp.get("text") == s["text"] or inp.get("sentence") == s["text"])
        xcheck["text_match" if same else "text_mismatch"] += 1
    logger.info(f"dataset-3 cross-check: {dict(xcheck)}")
    sents = {}
    for sid in free_sids:
        s = sents_all[sid]
        units = template_units(s, lex)
        sents[sid] = {k: s.get(k) for k in ("sentence_id", "text", "reference_fol_weak", "reference_fol_strong",
                                            "reading_converse", "template_id", "clause_type", "nested", "words",
                                            "nconds_weak", "negated_condition", "sort_group", "lexicon_ids",
                                            "profile_weak", "profile_strong", "batch")}
        sents[sid]["units"] = units
    dump(WORK / "sentences.json", sents)
    # FREE rows
    rows = []
    for (sid, slot, pv), r in sorted(last.items()):
        s = sents_all[sid]
        iid = item_id(r["system"], s["text"], r.get("raw_output"))
        if r.get("raw_output") is None:
            status = "NO_OUTPUT"
        elif not r.get("parse_ok"):
            status = "UNPARSEABLE"
        else:
            try:
                parse(r["candidate_fol"])
                status = "PARSED"
            except Exception as ex:  # noqa: BLE001 - parser raises assorted errors on junk
                logger.debug(f"our parser failed on {sid}/{slot}/{pv}: {ex}")
                status = "UNPARSEABLE"
        rows.append({"row_key": f"{iid}|FREE|{slot}|{pv}", "item_id": iid, "sentence_id": sid, "slot": slot,
                     "system": r["system"], "family": r["family"], "model": r["model"], "prompt_variant": pv,
                     "raw_output": r.get("raw_output"), "candidate_fol": r.get("candidate_fol"),
                     "parse_ok": r.get("parse_ok"), "input_status": status, "template_id": s["template_id"]})
    assert len({r["row_key"] for r in rows}) == len(rows), "row_key collision"
    with (WORK / "free_rows.jsonl").open("w") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    # SIG rows (labels only, pure z3)
    sig = load_jsonl(SIG_LABELS)
    keep = ("row_key", "sentence_id", "slot", "system", "family", "prompt_variant", "candidate_fol", "label",
            "matched_reading", "sig_status", "template_id", "clause_type")
    with (WORK / "sig_rows.jsonl").open("w") as fh:
        for r in sig:
            fh.write(json.dumps({k: r.get(k) for k in keep}, ensure_ascii=False) + "\n")
    counts = {
        "generation_records": len(gens), "free_rows_last_per_key": len(rows), "sentences": len(free_sids),
        "by_input_status": dict(Counter(r["input_status"] for r in rows)),
        "by_slot_variant": {f"{k[0]}|{k[1]}": v for k, v in sorted(Counter((r["slot"], r["prompt_variant"]) for r in rows).items())},
        "by_template": dict(sorted(Counter(r["template_id"] for r in rows).items())),
        "reconciliation": ("hypothesis text says 2,024 FREE rows (that is the SIG primary pool size); exp 7 "
                           "testability_FREE.json label_counts_all_rows sums to 2,652 incl. 199 NO_OUTPUT and 188 "
                           "UNPARSEABLE; this file yields the number above"),
        "dataset3_crosscheck": dict(xcheck),
        "sig_rows": len(sig), "sig_labels": dict(Counter(r["label"] for r in sig)),
        "unique_parsed_classes": len({(r["sentence_id"], re.sub(r"\s+", "", r["candidate_fol"]))
                                      for r in rows if r["input_status"] == "PARSED"}),
    }
    dump(RES / "input_counts.json", counts)
    logger.info(f"counts: {json.dumps(counts)[:600]}")
    shape_census(rows, sents)


NEG_NAME = re.compile(r"^(not|non|no|un|in|im|il|ir|dis|never|lacks?|without)$", re.I)


def shape_census(rows: list[dict], sents: dict) -> None:
    """Label-free: inputs only (candidate strings + template units)."""
    rng = random.Random(0)
    parsed = [r for r in rows if r["input_status"] == "PARSED"]
    sample = rng.sample(parsed, 100)
    c = Counter()
    per = []
    for r in sample:
        e = parse(r["candidate_fol"])
        bv = bound_vars(e)
        ats = atoms(e)
        preds = {(a[1], len(a[2])) for a in ats}
        consts = {x for a in ats for x in a[2] if x not in bv}
        tu = sents[r["sentence_id"]]["units"]
        t_un = sum(1 for u in tu.values() if u["arity"] == 1)
        t_bin = sum(1 for u in tu.values() if u["arity"] == 2)
        c_un = sum(1 for p in preds if p[1] == 1)
        c_bin = sum(1 for p in preds if p[1] == 2)
        c_other = sum(1 for p in preds if p[1] not in (1, 2))
        n_q = len(bv)
        notpref = sum(1 for p in preds if NEG_NAME.match(re.findall(r"[A-Z]?[a-z]+|[A-Z]+(?![a-z])|\d+", p[0].replace("_", " "))[0] if re.findall(r"[A-Z]?[a-z]+|[A-Z]+(?![a-z])|\d+", p[0].replace("_", " ")) else ""))
        ex_for_const = bool(re.search(r"∃\s*[a-z]\w*\s*\(?\s*\(?[A-Z]\w*\([a-z]\w*\)\s*∧\s*[A-Z]\w*\([a-z]\w*,\s*[a-z]\w*\)", r["candidate_fol"]))
        tmpl_names = {u["pred"] for u in tu.values()}
        same_names = len({p[0] for p in preds} & tmpl_names)
        per.append({"row_key": r["row_key"], "n_preds": len(preds), "n_unary": c_un, "n_binary": c_bin, "n_other_arity": c_other,
                    "n_consts": len(consts), "n_bound_vars": n_q, "t_unary": t_un, "t_binary": t_bin,
                    "not_prefixed_names": notpref, "exists_for_constant": ex_for_const,
                    "n_names_identical_to_template": same_names})
        c["unary_count_gt_template"] += c_un > t_un
        c["binary_count_lt_template"] += c_bin < t_bin
        c["binary_count_gt_template"] += c_bin > t_bin
        c["has_not_prefixed_name"] += notpref > 0
        c["exists_for_constant"] += ex_for_const
        c["more_than_one_bound_var"] += n_q > 1
        c["n_preds_ne_template_units"] += len(preds) != len(tu)
        c["other_arity"] += c_other > 0
    frac_ex = c["exists_for_constant"] / 100
    out = {"sample": 100, "seed": 0, "counts": dict(c), "exists_for_constant_share": frac_ex,
           "B6_declared": frac_ex >= 0.05, "rows": per}
    dump(RES / "shape_census.json", out)
    logger.info(f"shape census: {dict(c)}; ∃-for-constant share {frac_ex:.2f} -> B6 {'DECLARED' if frac_ex >= 0.05 else 'not declared'}")


if __name__ == "__main__":
    main()
