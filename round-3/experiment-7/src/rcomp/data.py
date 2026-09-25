# /// script
# requires-python = ">=3.12"
# dependencies = ["loguru"]
# ///
"""Build full_data_out.json (aii exp_sel_data_out) for R_COMP + PERTURB and re-verify EVERY row against the sources.

Input: work/assembled.json, the groups built by the pipeline in src/ (source_pool -> lexicon -> compose -> select_rcomp
-> perturb -> adjudicate select -> assemble). Sources in temp/datasets/ (symlinks):
  tasksource__folio/folio_v2_{train,validation}.jsonl   FOLIO v2 (CC-BY-SA-4.0)
  yfxiao__folio-refined__{train,validation}.csv         folio-refined (MIT)
  yuan-yang__MALLS-v0__MALLS-v0.1-{train,test}.json     MALLS-v0.1 (CC-BY-NC-4.0)
  DSAVlab-UNIUD_*_curated*.jsonl                        curated FOLIO/MALLS corrections (screen exclusion only)
  logiclm_FOLIO_dev_outputs/                            Logic-LM outputs (screen exclusion only)
  E_heldout_dataset1_full_data_out.json                 dataset E (iter 1): trusted / repaired references
Per-row checks (stored as metadata_source_verified + metadata_source_file + metadata_verify_notes; rows are NEVER
dropped):
  rcomp_sentences   every lexicon entry used traces to its source: text == a FOLIO-v2-train premise whose folio-refined
                    formula == the entry's source formula, or == an E heldout TRUSTED_AGREED/GOLD_PANEL_OK row (and, for
                    GOLD_PANEL_OK, == a MALLS-v0.1-train NL/FOL record); the entry's atom occurs in that formula; the
                    composed text is screen-disjoint (hash not in the exclusion set rebuilt from the sources).
  perturb_suite     base text + base formula == the E heldout row (TRUSTED_AGREED: FOLIO-v2 premise + folio-refined
                    formula; GOLD_PANEL_OK: MALLS-v0.1-train record; PANEL_REPAIRED: MALLS text + E's repaired formula);
                    R_COMP bases == the rcomp_sentences weak reading; recomputed item_id == metadata_item_id.
  adjudicator_check the item exists in perturb_suite with the same candidate and the same known label.
  rcomp_candidates  (once generated) raw_output == the latest raw/generations.jsonl record for (sentence, slot, variant).
One example per data row, grouped by dataset. full_data_out.json holds the 2 chosen datasets (R_COMP groups +
perturb_suite); adjudicator_check goes to adjudicator_check_out.json. mini/preview: aii-json format script (run_all.sh).
Run: uv run data.py
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

from loguru import logger

ROOT = Path(__file__).resolve().parent
T = ROOT / "temp" / "datasets"
logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(ROOT / "logs" / "data.log", rotation="30 MB", level="DEBUG")


# ---- exact copies of dataset E's src_e/select_sentences.py helpers (kept standalone so data.py needs no z3)
def norm(s: str) -> str:
    s = s.lower().replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def h(s: str) -> str:
    return hashlib.sha1(norm(s).encode()).hexdigest()


def split_sents(block: str) -> list[str]:
    return [p.strip() for p in re.split(r"(?<=[.!?])\s+|\n+", block) if p.strip()]


def jl(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


def fsq(f: str) -> str:
    """Formula comparison key: whitespace removed."""
    return re.sub(r"\s+", "", f or "")


def load_sources() -> dict:
    S = {}
    S["folio_train_premises"] = set()
    for r in jl(T / "tasksource__folio" / "folio_v2_train.jsonl"):
        for p in r["premises"].split("\n"):
            if p.strip():
                S["folio_train_premises"].add(norm(p))
    refined = defaultdict(set)
    for r in csv.DictReader(open(T / "yfxiao__folio-refined__train.csv", encoding="utf-8")):
        nls = [x for x in r["nl premises"].split("\n") if x.strip()]
        fols = [x for x in r["fol premises"].split("\n") if x.strip()]
        if len(nls) == len(fols):
            for n, f in zip(nls, fols):
                refined[norm(n)].add(fsq(f))
    S["refined"] = refined
    malls = defaultdict(set)
    for r in json.loads((T / "yuan-yang__MALLS-v0__MALLS-v0.1-train.json").read_text()):
        malls[norm(r["NL"])].add(fsq(r["FOL"]))
    S["malls_train"] = malls
    ex = set()

    def add(s):
        for x in [s] + split_sents(s):
            if x.strip():
                ex.add(h(x))
    for r in jl(T / "tasksource__folio" / "folio_v2_validation.jsonl"):
        for p in r["premises"].split("\n"):
            add(p)
        add(r["conclusion"])
    for r in csv.DictReader(open(T / "yfxiao__folio-refined__validation.csv", encoding="utf-8")):
        for p in r["nl premises"].split("\n"):
            add(p)
        add(r["nl conclusion"])
    for f in ("DSAVlab-UNIUD_FOLIO_validation-curated__FOLIO_instances.jsonl",
              "DSAVlab-UNIUD_MALLS_test_subset-CURATED__MALLS_instances.jsonl"):
        for r in jl(T / f):
            add(r["NL_sentence"])
    for r in json.loads((T / "yuan-yang__MALLS-v0__MALLS-v0.1-test.json").read_text()):
        add(r["NL"])
    for m in ("gpt-3.5-turbo", "gpt-4", "text-davinci-003"):
        for r in json.loads((T / "logiclm_FOLIO_dev_outputs" / f"FOLIO_dev_{m}.json").read_text()):
            add(r["context"])
            add(r["question"].split("?", 1)[-1])
    S["exclusion"] = ex
    e = json.loads((T / "E_heldout_dataset1_full_data_out.json").read_text())
    hs = [g for g in e["datasets"] if g["dataset"] == "heldout_sentences"][0]["examples"]
    S["E_by_sid"] = {x["metadata_sentence_id"]: {**json.loads(x["input"]), "status": x["output"],
                                                 "orig": x.get("metadata_original_reference_fol")} for x in hs}
    S["E_by_text"] = defaultdict(list)
    for sid, x in S["E_by_sid"].items():
        S["E_by_text"][norm(x["text"])].append(x)
    logger.info(f"sources: {len(S['folio_train_premises'])} FOLIO-v2 train premises, {len(refined)} refined premises, "
                f"{len(malls)} MALLS-train texts, {len(ex)} exclusion hashes, {len(hs)} E heldout sentences")
    return S


def verify_lexicon_entry(e: dict, S: dict) -> tuple[bool, str, str]:
    n, f = norm(e["source_text"]), fsq(e["source_fol"])
    pred = e["pred"]
    if not re.search(r"(?<![A-Za-z0-9_])" + re.escape(pred) + r"\(", e["source_fol"]):
        return False, "", f"atom {pred} not in source formula"
    if e["source"] == "FOLIO-v2-train_agreed":
        ok = n in S["folio_train_premises"] and f in S["refined"].get(n, set())
        return ok, "tasksource__folio/folio_v2_train.jsonl + yfxiao__folio-refined__train.csv", "" if ok else "FOLIO source mismatch"
    if e["source"].startswith("E_heldout_"):
        rows = [x for x in S["E_by_text"].get(n, []) if fsq(x["reference_fol"]) == f]
        ok = bool(rows) and rows[0]["status"] == e["source"].replace("E_heldout_", "")
        src = "E_heldout_dataset1_full_data_out.json"
        if ok and rows[0]["status"] == "GOLD_PANEL_OK":
            ok = f in S["malls_train"].get(n, set())
            src += " + yuan-yang__MALLS-v0__MALLS-v0.1-train.json"
        elif ok and rows[0]["status"] == "TRUSTED_AGREED":
            ok = n in S["folio_train_premises"] and f in S["refined"].get(n, set())
            src += " + tasksource__folio + yfxiao__folio-refined"
        return ok, src, "" if ok else "E source mismatch"
    return False, "", f"unknown source {e['source']}"


@logger.catch(reraise=True)
def main():
    A = json.loads((ROOT / "work" / "assembled.json").read_text())
    S = load_sources()
    lex = {x["lexicon_id"]: x for x in json.loads((ROOT / "lexicon.json").read_text())["entries"]}
    lex_ver = {lid: verify_lexicon_entry(x, S) for lid, x in lex.items()}
    logger.info(f"lexicon entries traced to source: {sum(v[0] for v in lex_ver.values())}/{len(lex_ver)}")
    G = {g["dataset"]: g["examples"] for g in A["datasets"]}
    stats = Counter()
    # ---- rcomp_sentences
    rc_weak = {}
    for e in G["rcomp_sentences"]:
        inp = json.loads(e["input"])
        rc_weak[e["metadata_sentence_id"]] = inp["reference_fol_weak"]
        notes = [f"{lid}: {lex_ver[lid][2]}" for lid in e["metadata_lexicon_ids"] if not lex_ver[lid][0]]
        if h(inp["text"]) in S["exclusion"]:
            notes.append("screen hash collision")
        if inp["reference_fol"] != inp["reference_fol_weak"]:
            notes.append("reference_fol != weak reading")
        e["metadata_source_verified"] = not notes
        e["metadata_source_file"] = "; ".join(sorted({lex_ver[lid][1] for lid in e["metadata_lexicon_ids"] if lex_ver[lid][1]}))
        e["metadata_verify_notes"] = notes
        stats[f"rcomp_sentences_verified_{not notes}"] += 1
    # ---- perturb_suite
    pert_ids = {}
    for e in G["perturb_suite"]:
        inp = json.loads(e["input"])
        notes = []
        if hashlib.sha1((inp["system"] + "|" + norm(inp["text"]) + "|" + inp["candidate_fol"]).encode()).hexdigest()[:16] != e["metadata_item_id"]:
            notes.append("item_id recipe mismatch")
        src = e["metadata_base_source"]
        n, f = norm(inp["text"]), fsq(inp["reference_fol"])
        if src == "RCOMP":
            if fsq(rc_weak.get(e["metadata_sentence_id"], "")) != f:
                notes.append("R_COMP base != weak reading")
            sf = "rcomp_sentences (this dataset)"
        else:
            er = S["E_by_sid"].get(e["metadata_sentence_id"])
            sf = "E_heldout_dataset1_full_data_out.json"
            if er is None or norm(er["text"]) != n or fsq(er["reference_fol"]) != f or "E_" + er["status"] != src:
                notes.append("E base mismatch")
            elif src == "E_TRUSTED_AGREED":
                sf += " + tasksource__folio + yfxiao__folio-refined"
                if not (n in S["folio_train_premises"] and f in S["refined"].get(n, set())):
                    notes.append("FOLIO source mismatch")
            elif src == "E_GOLD_PANEL_OK":
                sf += " + yuan-yang__MALLS-v0__MALLS-v0.1-train.json"
                if f not in S["malls_train"].get(n, set()):
                    notes.append("MALLS source mismatch")
            elif src == "E_PANEL_REPAIRED":
                sf += " (repaired formula) + yuan-yang__MALLS-v0__MALLS-v0.1-train.json (text)"
                if n not in S["malls_train"] or fsq(er["orig"] or "") not in S["malls_train"][n]:
                    notes.append("MALLS text/original-gold mismatch")
        e["metadata_source_verified"] = not notes
        e["metadata_source_file"] = sf
        e["metadata_verify_notes"] = notes
        pert_ids[e["metadata_item_id"]] = (inp["candidate_fol"], e["output"])
        stats[f"perturb_verified_{not notes}"] += 1
    # ---- adjudicator_check
    for e in G["adjudicator_check"]:
        inp = json.loads(e["input"])
        p = pert_ids.get(e["metadata_item_id"])
        ok = p is not None and p[0] == inp["candidate_fol"] and p[1] == e["output"]
        e["metadata_source_verified"] = ok
        e["metadata_source_file"] = "perturb_suite (this dataset)"
        e["metadata_verify_notes"] = [] if ok else ["not found in perturb_suite with the same candidate/label"]
        stats[f"adjudicator_check_verified_{ok}"] += 1
    # ---- rcomp_candidates (present once generation has run)
    if "rcomp_candidates" in G:
        last = {}
        for r in jl(ROOT / "raw" / "generations.jsonl"):
            last[(r["sentence_id"], r["slot"], r["prompt_variant"])] = r
        for e in G["rcomp_candidates"]:
            inp = json.loads(e["input"])
            r = last.get((e["metadata_sentence_id"], e["metadata_slot"], e["metadata_prompt_variant"]))
            ok = r is not None and (r.get("raw_output") or "") == (e["metadata_raw_output"] or "")
            e["metadata_source_verified"] = ok
            e["metadata_source_file"] = "raw/generations.jsonl"
            e["metadata_verify_notes"] = [] if ok else ["raw_output mismatch"]
            stats[f"rcomp_candidates_verified_{ok}"] += 1
    # The two chosen datasets: R_COMP (rcomp_candidates once generated + rcomp_sentences) and PERTURB (perturb_suite).
    # adjudicator_check (60 known-label QA rows) is an auxiliary label-quality table -> adjudicator_check_out.json.
    order = ["rcomp_candidates", "rcomp_sentences", "perturb_suite"]
    groups = [{"dataset": k, "examples": G[k]} for k in order if k in G]
    meta = dict(A["metadata"])
    meta["groups"] = {g["dataset"]: len(g["examples"]) for g in groups}
    meta["datasets_chosen"] = {"R_COMP": [k for k in ("rcomp_candidates", "rcomp_sentences") if k in G],
                               "PERTURB": ["perturb_suite"]}
    meta["auxiliary_file"] = "adjudicator_check_out.json (60 known-label adjudicator QA rows, same row format)"
    meta["source_verification"] = dict(stats)
    (ROOT / "full_data_out.json").write_text(json.dumps({"metadata": meta, "datasets": groups}, ensure_ascii=False, indent=1))
    aux = {"metadata": {"description": "adjudicator known-label check items (STEP 8a) on R_COMP bases",
                        "source_verification": {k: v for k, v in stats.items() if k.startswith("adjudicator")}},
           "datasets": [{"dataset": "adjudicator_check", "examples": G["adjudicator_check"]}]}
    (ROOT / "adjudicator_check_out.json").write_text(json.dumps(aux, ensure_ascii=False, indent=1))
    size = (ROOT / "full_data_out.json").stat().st_size
    logger.info(f"full_data_out.json {size / 1e6:.1f} MB; groups {({g['dataset']: len(g['examples']) for g in groups})}; "
                f"verification {dict(stats)}")
    bad = [e for g in groups for e in g["examples"] if not e["metadata_source_verified"]]
    for e in bad[:10]:
        logger.warning(f"unverified {e.get('metadata_item_id') or e.get('metadata_sentence_id')}: {e['metadata_verify_notes']}")
    if size > 30e6:
        logger.warning("full_data_out.json exceeds 30 MB: split with aii-file-size-limit")


if __name__ == "__main__":
    main()
