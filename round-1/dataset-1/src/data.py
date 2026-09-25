# /// script
# requires-python = ">=3.12"
# dependencies = ["loguru", "pandas", "pyarrow"]
# ///
"""Build full_data_out (exp_sel_data_out) for the held-out NL->FOL faithfulness meta-evaluation set.

Inputs
- work/assembled.json: the 4 labelled groups produced by the pipeline in src/
  (select_sentences -> generate -> ccg2lambda_candidates -> screen -> run_label -> calibration/gate -> assemble).
- temp/datasets/ (symlinks to the sources). EVERY row is re-verified against them here:
    heldout_candidates / heldout_sentences:
      - sentence + original reference == the MALLS-v0.1-train record (L25/L20/EXC), or the tasksource FOLIO-v2-train
        premise + folio-refined train formula (CTRL);
      - LLM candidate raw output == the generations.jsonl record for (sentence, slot, variant);
      - ccg2lambda raw logical form == a folio_by_ccg2lambda train row;
      - malls_gpt4_gold candidate == the MALLS gold.
    screen_audit:
      - track L: the (system, FOL ::: NL) line exists in Logic-LM FOLIO_dev_<system>.json;
      - track H: text / original / corrected == the DSAVlab-UNIUD curated record.
    panel_calibration:
      - synthetic: sentence + reference == a folio-refined train premise/formula;
      - track H: the curated record.
  The result is stored per row as metadata_source_verified (+ metadata_source_file). Rows are never dropped.

One example per data row, grouped by dataset. Output: full_data_out.json (single file; split into
full_data_out/full_data_out_{i}.json only if it would exceed the 100 MB limit) + mini_data_out.json / preview_data_out.json.
Run: uv run data.py
"""
from __future__ import annotations

import csv
import json
import re
import shutil
import sys
from collections import Counter
from pathlib import Path

import pandas as pd
from loguru import logger

ROOT = Path(__file__).resolve().parent
TD = ROOT / "temp" / "datasets"
(ROOT / "logs").mkdir(exist_ok=True)
logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(ROOT / "logs" / "data_py.log", rotation="30 MB", level="DEBUG")

GROUP_ORDER = ["heldout_candidates", "heldout_sentences", "panel_calibration", "screen_audit"]
FORBIDDEN = {"split", "dataset", "context"}
LIMIT = 100 * 1000 * 1000  # aii-file-size-limit: 100 MB per file


def ws(s: str | None) -> str:
    return re.sub(r"\s+", " ", (s or "").strip())


def read_jsonl(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


def load_sources() -> dict:
    L = TD / "local_sources"
    src = {}
    src["malls_train"] = {ws(r["NL"]): ws(r["FOL"]) for r in json.load(open(L / "yuan-yang__MALLS-v0__MALLS-v0.1-train.json"))}
    src["folio_train_premises"] = {ws(p) for r in read_jsonl(TD / "tasksource__folio" / "folio_v2_train.jsonl") for p in r["premises"].split("\n")}
    refined, refined_pairs = set(), set()
    for r in csv.DictReader(open(L / "yfxiao__folio-refined__train.csv")):
        nls = [s for s in r["nl premises"].split("\n") if s.strip()]
        fols = [s for s in r["fol premises"].split("\n") if s.strip()]
        refined |= {ws(f) for f in fols}
        if len(nls) == len(fols):
            refined_pairs |= {(ws(n), ws(f)) for n, f in zip(nls, fols)}
    src["refined_train_fols"], src["refined_train_pairs"] = refined, refined_pairs
    src["refined_val_fols"] = {ws(f) for r in csv.DictReader(open(L / "folio_refined_validation.csv")) for f in r["fol premises"].split("\n") if f.strip()}
    src["gens"] = {(g["sentence_id"], g["slot"], g["prompt_variant"]): g["raw_output"]
                   for g in read_jsonl(TD / "generated_candidates" / "generations.jsonl") if g.get("raw_output") is not None}
    df = pd.read_parquet(TD / "kenken6696__folio_by_ccg2lambda" / "data" / "train-00000-of-00001.parquet")
    src["ccg_forms"] = {ws(x) for x in df["logical_form"]}
    cur = {}
    for f, newk in [("DSAVlab-UNIUD_FOLIO_validation-curated__FOLIO_instances.jsonl", "FOL_sentence"),
                    ("DSAVlab-UNIUD_MALLS_test_subset-CURATED__MALLS_instances.jsonl", "FOL_sentence_new")]:
        for r in read_jsonl(L / f):
            cur[str(r["id"])] = (ws(r["NL_sentence"]), ws(r["FOL_sentence_old"]), ws(r[newk]), f)
    src["curated"] = cur
    src["curated_corrected_fols"] = {v[2] for v in cur.values()}
    lines = set()
    for m in ("gpt-3.5-turbo", "gpt-4", "text-davinci-003"):
        for r in json.load(open(TD / "logiclm_FOLIO_dev_outputs" / f"FOLIO_dev_{m}.json")):
            prog = r["raw_logic_programs"][0] if isinstance(r["raw_logic_programs"], list) else r["raw_logic_programs"]
            for line in prog.splitlines():
                if ":::" in line:
                    fol, nl = line.strip().split(":::", 1)
                    lines.add((m, ws(fol), ws(nl)))
    src["logiclm_lines"] = lines
    return src


def verify_heldout(ex: dict, src: dict, sentence_row: bool = False) -> tuple[bool, str]:
    inp = json.loads(ex["input"])
    text = ws(inp["text"])
    stratum = ex["metadata_strata"]["source_stratum"]
    orig_ref = ws(ex.get("metadata_original_reference_fol") or inp["reference_fol"]) if sentence_row else None
    if stratum == "CTRL":
        ref = ws(inp["reference_fol"])
        ok = text in src["folio_train_premises"] and ((text, ref) in src["refined_train_pairs"] or ref in src["refined_train_fols"])
        file = "tasksource__folio/folio_v2_train.jsonl + local_sources/yfxiao__folio-refined__train.csv"
    else:
        gold = src["malls_train"].get(text)
        ref = orig_ref if sentence_row else ws(inp["reference_fol"])
        ok = gold is not None and (ref == gold or ex.get("metadata_reference_status") == "PANEL_REPAIRED")
        file = "local_sources/yuan-yang__MALLS-v0__MALLS-v0.1-train.json"
    if sentence_row or not ok:
        return ok, file
    sys_ = ex["metadata_system"]
    if sys_ == "malls_gpt4_gold":
        return ws(inp["candidate_fol"]) == src["malls_train"].get(text), file
    if sys_ == "ccg2lambda":
        return ws(ex["metadata_raw_output"]) in src["ccg_forms"], file + " + kenken6696__folio_by_ccg2lambda/train"
    raw = src["gens"].get((ex["metadata_sentence_id"], ex["metadata_slot"], ex["metadata_prompt_variant"]))
    return raw is not None and raw == ex["metadata_raw_output"], file + " + generated_candidates/generations.jsonl"


def verify_screen(ex: dict, src: dict) -> tuple[bool, str]:
    inp = json.loads(ex["input"])
    if ex["metadata_track"] == "H":
        c = src["curated"].get(str(ex["metadata_record_id"]))
        ok = c is not None and c[0] == ws(inp["text"]) and c[1] == ws(inp["candidate_fol"]) and c[2] == ws(inp["reference_fol"])
        return ok, f"local_sources/{c[3] if c else 'DSAVlab-UNIUD curated'}"
    ok_line = (ex["metadata_system"], ws(inp["candidate_fol"]), ws(inp["text"])) in src["logiclm_lines"]
    ref = ws(inp["reference_fol"])
    ok_ref = ref in src["curated_corrected_fols"] or ref in src["refined_val_fols"]
    return ok_line and ok_ref, f"logiclm_FOLIO_dev_outputs/FOLIO_dev_{ex['metadata_system']}.json"


def verify_calib(ex: dict, src: dict) -> tuple[bool, str]:
    inp = json.loads(ex["input"])
    if ex["metadata_subset"] == "synthetic_gate":
        text, ref = ws(inp["text"]), ws(inp["reference_fol"])
        return text in src["folio_train_premises"] and ((text, ref) in src["refined_train_pairs"] or ref in src["refined_train_fols"]), \
            "local_sources/yfxiao__folio-refined__train.csv"
    c = src["curated"].get(str(ex["metadata_record_id"]))
    ok = c is not None and c[0] == ws(inp["text"]) and c[1] == ws(inp["original_fol"]) and c[2] == ws(inp["corrected_fol"])
    return ok, f"local_sources/{c[3] if c else 'DSAVlab-UNIUD curated'}"


def check_schema(obj: dict) -> None:
    assert isinstance(obj.get("datasets"), list) and obj["datasets"]
    for d in obj["datasets"]:
        assert set(d) == {"dataset", "examples"} and d["examples"], d.get("dataset")
        for ex in d["examples"]:
            assert isinstance(ex["input"], str) and isinstance(ex["output"], str)
            for k in ex:
                assert k in ("input", "output") or (k.startswith("metadata_") and re.fullmatch(r"metadata_[a-zA-Z_][a-zA-Z0-9_]*", k)), k
                assert k not in FORBIDDEN


def trunc(x, n=200):
    if isinstance(x, str):
        return x if len(x) <= n else x[:n] + "..."
    if isinstance(x, list):
        return [trunc(v, n) for v in x]
    if isinstance(x, dict):
        return {k: trunc(v, n) for k, v in x.items()}
    return x


def mini(obj, k=3):
    return {"metadata": obj.get("metadata", {}), "datasets": [{"dataset": d["dataset"], "examples": d["examples"][:k]} for d in obj["datasets"]]}


def write_parts(obj: dict) -> list[Path]:
    out = ROOT / "full_data_out"
    if out.exists():
        shutil.rmtree(out)
    out.mkdir()
    parts, cur, size = [], [], 0
    for d in obj["datasets"]:
        chunk = []
        for ex in d["examples"]:
            sz = len(json.dumps(ex, ensure_ascii=False).encode())
            if size + sz > LIMIT and (cur or chunk):
                if chunk:
                    cur.append({"dataset": d["dataset"], "examples": chunk})
                parts.append(cur); cur, chunk, size = [], [], 0
            chunk.append(ex); size += sz
        if chunk:
            cur.append({"dataset": d["dataset"], "examples": chunk})
    if cur:
        parts.append(cur)
    paths = []
    for i, p in enumerate(parts, 1):
        o = {"metadata": {**obj["metadata"], "part": i, "n_parts": len(parts)}, "datasets": p}
        check_schema(o)
        f = out / f"full_data_out_{i}.json"
        f.write_text(json.dumps(o, ensure_ascii=False))
        (out / f"mini_full_data_out_{i}.json").write_text(json.dumps(mini(o), ensure_ascii=False, indent=1))
        (out / f"preview_full_data_out_{i}.json").write_text(json.dumps(trunc(mini(o)), ensure_ascii=False, indent=1))
        paths.append(f)
    m = mini(obj)
    (ROOT / "mini_data_out.json").write_text(json.dumps(m, ensure_ascii=False, indent=1))
    (ROOT / "preview_data_out.json").write_text(json.dumps(trunc(m), ensure_ascii=False, indent=1))
    return paths


@logger.catch(reraise=True)
def main() -> None:
    A = json.loads((ROOT / "work" / "assembled.json").read_text(encoding="utf-8"))
    groups = {d["dataset"]: d["examples"] for d in A["datasets"]}
    assert list(groups) == GROUP_ORDER, list(groups)
    src = load_sources()
    logger.info(f"sources loaded: MALLS-train {len(src['malls_train'])}, generations {len(src['gens'])}, Logic-LM lines {len(src['logiclm_lines'])}")
    report = {}
    for name, fn in [("heldout_candidates", lambda e: verify_heldout(e, src)),
                     ("heldout_sentences", lambda e: verify_heldout(e, src, sentence_row=True)),
                     ("panel_calibration", lambda e: verify_calib(e, src)),
                     ("screen_audit", lambda e: verify_screen(e, src))]:
        c = Counter()
        for ex in groups[name]:
            ok, f = fn(ex)
            ex["metadata_source_verified"] = bool(ok)
            ex["metadata_source_file"] = f
            c[ok] += 1
        report[name] = {"rows": len(groups[name]), "verified": c[True], "unverified": c[False],
                        "labels": dict(Counter(e["output"] for e in groups[name]))}
        logger.info(f"{name}: {report[name]}")
    obj = {"metadata": {**A["metadata"], "source_verification": report,
                        "reading": "for f in sorted(glob('full_data_out/full_data_out_*.json')): concatenate each group's examples"},
           "datasets": [{"dataset": g, "examples": groups[g]} for g in GROUP_ORDER]}
    check_schema(obj)
    blob = json.dumps(obj, ensure_ascii=False)
    if len(blob.encode()) <= LIMIT:
        if (ROOT / "full_data_out").exists():
            shutil.rmtree(ROOT / "full_data_out")
        (ROOT / "full_data_out.json").write_text(blob)
        m = mini(obj)
        (ROOT / "mini_data_out.json").write_text(json.dumps(m, ensure_ascii=False, indent=1))
        (ROOT / "preview_data_out.json").write_text(json.dumps(trunc(m), ensure_ascii=False, indent=1))
        paths = [ROOT / "full_data_out.json"]
    else:
        (ROOT / "full_data_out.json").unlink(missing_ok=True)
        paths = write_parts(obj)
    for p in paths:
        logger.info(f"{p.relative_to(ROOT)} {p.stat().st_size / 1e6:.2f} MB")
    (ROOT / "work" / "source_verification.json").write_text(json.dumps(report, indent=1))


if __name__ == "__main__":
    main()
