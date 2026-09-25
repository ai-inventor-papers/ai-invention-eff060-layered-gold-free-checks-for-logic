#!/usr/bin/env python3
"""Independent re-verification of every row of full_data_out.json (no reuse of the generator's own verdicts).

  perturb_suite PERTURB rows      candidate parses; z3 (8 s) says NOT equivalent to the base and to every accepted
                                  reading; recomputed item_id matches
  perturb_suite PERTURB_CONTROL   z3 (8 s) EQUIVALENT to the base (RENAME: after applying the inverse rename map)
  rcomp_sentences                 both readings parse; weak ≢ strong; every lexicon phrase used appears in the text;
                                  the lexicon atoms appear in the weak reading; recomputed sentence_id matches
  all groups                      item_id unique within the group
Writes work/verify_report.json; exits 1 on any failure.
"""
from __future__ import annotations

import json
import multiprocessing as mp
from collections import Counter
from concurrent.futures import ProcessPoolExecutor

from common import ROOT, W, dump, sha1, setup_logger


def check_perturb(ex: dict) -> tuple[str, str | None]:
    import common  # noqa: F401
    from fol import parse, equivalent
    from repair_census import rename
    inp = json.loads(ex["input"])
    try:
        c, b = parse(inp["candidate_fol"]), parse(inp["reference_fol"])
    except Exception as e:  # noqa: BLE001
        return ex["metadata_item_id"], f"parse:{e}"
    if ex["metadata_fold"] == "PERTURB":
        refs = [b] + ([parse(inp["reference_fol_strong"])] if inp.get("reference_fol_strong") else []) + \
               ([parse(ex["metadata_reading_converse"])] if ex.get("metadata_reading_converse") else [])
        for r in refs:
            if equivalent(c, r, ms=8000) is not False:
                return ex["metadata_item_id"], "mutant_not_proven_nonequivalent"
    else:
        if ex["metadata_control_type"] == "RENAME":
            inv = {}
            for k, v in (ex["metadata_rename_map"] or {}).items():
                n, ar = k.rsplit("/", 1)
                inv[(v, int(ar))] = n
            c = rename(c, inv, {})
        if equivalent(c, b, ms=8000) is not True:
            return ex["metadata_item_id"], "control_not_proven_equivalent"
    return ex["metadata_item_id"], None


def main():
    logger = setup_logger("verify")
    import select_sentences as ss
    from fol import parse, equivalent
    d = json.loads((ROOT / "full_data_out.json").read_text())
    G = {g["dataset"]: g["examples"] for g in d["datasets"]}
    rep = {"failures": [], "counts": {}}
    for name, exs in G.items():
        ids = Counter(e.get("metadata_item_id") or e.get("metadata_sentence_id") for e in exs)
        dup = [k for k, v in ids.items() if v > 1]
        rep["counts"][f"{name}_rows"] = len(exs)
        rep["counts"][f"{name}_dup_ids"] = len(dup)
        rep["failures"] += [[name, k, "duplicate_id"] for k in dup[:20]]
    rows = G["perturb_suite"]
    for e in rows:  # item_id recipe
        inp = json.loads(e["input"])
        if sha1(inp["system"] + "|" + ss.norm(inp["text"]) + "|" + inp["candidate_fol"])[:16] != e["metadata_item_id"]:
            rep["failures"].append(["perturb_suite", e["metadata_item_id"], "item_id_recipe"])
    with ProcessPoolExecutor(max_workers=4, mp_context=mp.get_context("spawn")) as pool:
        res = list(pool.map(check_perturb, rows, chunksize=32))
    bad = [(i, why) for i, why in res if why]
    rep["counts"]["perturb_rows_verified"] = len(res) - len(bad)
    rep["failures"] += [["perturb_suite", i, why] for i, why in bad]
    lex = {x["lexicon_id"]: x for x in json.loads((ROOT / "lexicon.json").read_text())["entries"]}
    nok = 0
    for e in G["rcomp_sentences"]:
        inp = json.loads(e["input"])
        w, s = parse(inp["reference_fol_weak"]), parse(inp["reference_fol_strong"])
        errs = []
        if equivalent(w, s, ms=8000) is not False:
            errs.append("weak_eq_strong")
        if sha1("rcomp|" + ss.norm(inp["text"]))[:12] != e["metadata_sentence_id"]:
            errs.append("sentence_id_recipe")
        neg = e["metadata_negated_condition"]
        for k, lid in enumerate(e["metadata_lexicon_ids"]):
            x = lex[lid]
            cond_ids = e["metadata_condition_lexicon_ids"]
            phrase = x["vp_sg_neg"] if (lid in cond_ids and neg is not None and cond_ids.index(lid) == neg) else x["vp_sg_pos"]
            if e["metadata_template_id"] == "T7" and lid == e["metadata_lexicon_ids"][-1]:
                phrase = None  # the exception phrase is re-inflected for 'they'
            if lid == e["metadata_noun_lexicon_id"]:
                phrase = x["noun"]
            if phrase and phrase not in inp["text"]:
                errs.append(f"phrase_missing:{lid}")
            if x["atom_final"] not in inp["reference_fol_weak"]:
                errs.append(f"atom_missing:{lid}")
        if errs:
            rep["failures"].append(["rcomp_sentences", e["metadata_sentence_id"], errs])
        else:
            nok += 1
    rep["counts"]["rcomp_sentences_verified"] = nok
    rep["ok"] = not rep["failures"]
    dump(W / "verify_report.json", rep)
    logger.info(f"verify: {rep['counts']}; failures {len(rep['failures'])}")
    for f in rep["failures"][:10]:
        logger.error(f)
    raise SystemExit(0 if rep["ok"] else 1)


if __name__ == "__main__":
    main()
