#!/usr/bin/env python3
"""STEP 6a: rebuild the shared frozen screen (track L + track H) with the screen's exact item_id recipe.

item_id = sha1(system + '|' + norm_screen(text) + '|' + candidate_fol_raw)[:16]
  norm_screen = lowercase, apostrophes removed, other punctuation stripped, whitespace collapsed
  candidate_fol_raw = the formula string exactly as in the source (Logic-LM 'FOL ::: NL' left side, whitespace-stripped;
  curated FOL_sentence_old for track H). system = Logic-LM model name, or 'human_original' for track H.
Raw join keys (system, raw_text, normtext, raw_fol) are stored so iteration 2 can re-join under another norm.
TRACK L: Logic-LM FOLIO_dev lines whose norm text matches a curated corrected conclusion (reference = corrected
  gold) or a FOLIO-validation premise whose original gold (tasksource v2 validation) ≡ folio-refined (EQ/VOCAB or
  identical string; reference = refined formula).
TRACK H: the 302 curated items (202 FOLIO conclusions + 100 MALLS-test): candidate = original gold, reference =
  corrected gold; ambiguity-flagged items are marked READING_CHOICE candidates.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "labeller"))
sys.setrecursionlimit(10000)
from normalise import normalise  # noqa: E402
from fol import parse  # noqa: E402
from label_lib import equivalent_modulo_vocab  # noqa: E402
from select_sentences import exception_type  # noqa: E402
from complexity_counts import depth, nquant, nconds  # noqa: E402

SYSTEMS = ("gpt-3.5-turbo", "gpt-4", "text-davinci-003")


def norm_screen(t: str) -> str:
    t = t.lower().replace("’", "").replace("'", "").replace("‘", "")
    t = re.sub(r"[^\w\s]", "", t)
    return re.sub(r"\s+", " ", t).strip()


def item_id(system: str, text: str, fol_raw: str) -> str:
    return hashlib.sha1((system + "|" + norm_screen(text) + "|" + fol_raw).encode()).hexdigest()[:16]


def load_jsonl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


def logiclm_lines():
    out, counts = [], {}
    for m in SYSTEMS:
        recs = json.load(open(ROOT / f"raw/logiclm/FOLIO_dev_{m}.json"))
        counts[m] = len(recs)
        for r in recs:
            prog = r["raw_logic_programs"][0] if isinstance(r["raw_logic_programs"], list) else r["raw_logic_programs"]
            sec = None
            for line in prog.splitlines():
                s = line.strip()
                if s.rstrip(":") in ("Predicates", "Premises", "Conclusion"):
                    sec = s.rstrip(":").lower(); continue
                if sec in ("premises", "conclusion") and ":::" in s:
                    fol, nl = s.split(":::", 1)
                    out.append({"system": m, "record_id": r["id"], "role": "premise" if sec == "premises" else "conclusion",
                                "raw_fol": fol.strip(), "raw_text": nl.strip(), "raw_line": line})
    return out, counts


def main():
    F = load_jsonl(ROOT / "data_local/DSAVlab-UNIUD_FOLIO_validation-curated__FOLIO_instances.jsonl")
    M = load_jsonl(ROOT / "data_local/DSAVlab-UNIUD_MALLS_test_subset-CURATED__MALLS_instances.jsonl")
    concl = {}
    for r in F:
        if str(r["id"]).startswith("story"):
            continue
        concl.setdefault(norm_screen(r["NL_sentence"]), r)
    # agreed premises: tasksource v2 validation original vs folio_refined_validation.csv
    ts = load_jsonl(ROOT / "raw/hf/tasksource__folio/folio_v2_validation.jsonl")
    ref_rows = list(csv.DictReader(open(ROOT / "data_local/folio_refined_validation.csv")))
    refmap = {}
    for r in ref_rows:
        nls = [s for s in r["nl premises"].split("\n") if s.strip()]
        refmap.setdefault(tuple(norm_screen(s) for s in nls), [s for s in r["fol premises"].split("\n") if s.strip()])
    agreed, alog = {}, Counter()
    for r in ts:
        nls = [s for s in r["premises"].split("\n") if s.strip()]
        fols = [s for s in r["premises-FOL"].split("\n") if s.strip()]
        key = tuple(norm_screen(s) for s in nls)
        rf = refmap.get(key)
        if rf is None or not (len(nls) == len(fols) == len(rf)):
            alog["story_unmatched_or_linecount"] += 1
            continue
        for t, of, ff in zip(nls, fols, rf):
            n = norm_screen(t)
            if n in agreed:
                continue
            if of.strip() == ff.strip():
                st = "IDENTICAL_STRING"
            else:
                try:
                    st = equivalent_modulo_vocab(parse(ff), parse(of))
                except Exception:  # noqa: BLE001
                    st = "UNPARSEABLE"
            alog[st] += 1
            if st in ("IDENTICAL_STRING", "EQ", "VOCAB"):
                agreed[n] = {"text": t, "reference_fol": ff.strip(), "original_fol": of.strip(), "agreement_type": st}
    items = []
    lines, counts = logiclm_lines()
    matched_concl = set()
    for ln in lines:
        n = norm_screen(ln["raw_text"])
        if n in concl:
            c = concl[n]
            ref, rsrc, amb = c["FOL_sentence"], "curated_corrected_conclusion", str(c.get("ambiguity")) == "True"
            matched_concl.add(n)
        elif n in agreed:
            ref, rsrc, amb = agreed[n]["reference_fol"], f"agreed_premise_{agreed[n]['agreement_type']}", False
        else:
            continue
        items.append({"track": "L", "system": ln["system"], "role": ln["role"], "record_id": ln["record_id"],
                      "raw_text": ln["raw_text"], "raw_fol": ln["raw_fol"], "reference_fol": ref, "reference_source": rsrc,
                      "ambiguous": amb})
    for r in F:
        if str(r["id"]).startswith("story"):
            continue
        items.append({"track": "H", "system": "human_original", "role": "conclusion", "record_id": r["id"],
                      "raw_text": r["NL_sentence"], "raw_fol": r["FOL_sentence_old"], "reference_fol": r["FOL_sentence"],
                      "reference_source": "curated_corrected_FOLIO", "ambiguous": str(r.get("ambiguity")) == "True",
                      "curated_corrected": r.get("corrected")})
    for r in M:
        items.append({"track": "H", "system": "human_original", "role": "sentence", "record_id": r["id"],
                      "raw_text": r["NL_sentence"], "raw_fol": r["FOL_sentence_old"], "reference_fol": r["FOL_sentence_new"],
                      "reference_source": "curated_corrected_MALLS", "ambiguous": str(r.get("ambiguity")) == "True",
                      "curated_corrected": r.get("corrected")})
    seen, out = set(), []
    for it in items:
        it["normtext"] = norm_screen(it["raw_text"])
        it["item_id"] = item_id(it["system"], it["raw_text"], it["raw_fol"])
        if it["item_id"] in seen:  # identical (system, text, fol) triple repeated across stories
            continue
        seen.add(it["item_id"])
        fol, applied = normalise(it["raw_fol"])
        it["candidate_fol_normalised"], it["normalisation_applied"] = fol, applied
        it["screen_sentence_id"] = hashlib.sha1(f"screen|{it['track']}|{it['normtext']}|{it['reference_fol']}".encode()).hexdigest()[:12]
        it["join_keys"] = {"system": it["system"], "raw_text": it["raw_text"], "normtext": it["normtext"], "raw_fol": it["raw_fol"]}
        try:
            e = parse(it["reference_fol"])
            st = {"words": len(it["raw_text"].split()), "n_quant": nquant(e), "depth": depth(e), "n_conditions": nconds(e)}
        except Exception:  # noqa: BLE001
            st = {"words": len(it["raw_text"].split()), "n_quant": None, "depth": None, "n_conditions": None, "reference_unparseable": True}
        st["exception_type"] = exception_type(it["raw_text"])
        it["strata"] = st
        out.append(it)
    meta = {"logiclm_records_per_file": counts, "logiclm_lines": len(lines), "curated_conclusions": len(concl),
            "distinct_conclusions_matched": len(matched_concl),
            "conclusion_match_rate": round(len(matched_concl) / max(1, len(concl)), 3),
            "agreed_premise_pool": len(agreed), "agreement_log": dict(alog),
            "items_per_track": dict(Counter(i["track"] for i in out)),
            "items_per_system": dict(Counter(f"{i['track']}:{i['system']}" for i in out).most_common()),
            "track_L_reference_source": dict(Counter(i["reference_source"] for i in out if i["track"] == "L")),
            "screen_sentences": len({i["screen_sentence_id"] for i in out}),
            "fallback_note": "track L always includes agreed premises (screen definition in the experiment-1 plan); the <150-conclusion fallback is therefore subsumed"}
    (ROOT / "work" / "screen_items.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
    (ROOT / "work" / "screen_meta.json").write_text(json.dumps(meta, indent=1))
    print(json.dumps(meta, indent=1))


if __name__ == "__main__":
    main()
