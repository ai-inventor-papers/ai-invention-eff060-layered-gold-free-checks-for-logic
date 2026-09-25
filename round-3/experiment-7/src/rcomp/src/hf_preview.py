#!/usr/bin/env python3
"""TODO 3 helper: preview candidate HF datasets (downloads, card size, splits, 2 sample rows) via the Hub and
datasets-server APIs; writes temp/search/hf_previews.json."""
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import requests

IDS = ["tasksource/folio", "yale-nlp/FOLIO", "yuan-yang/MALLS-v0", "yfxiao/folio-refined",
       "DSAVlab-UNIUD/MALLS_test_subset-CURATED", "opendatalab/ProverQA", "cogint/LogicBench-v1.0", "tasksource/proofwriter"]


def one(i):
    out = {"id": i}
    try:
        m = requests.get(f"https://huggingface.co/api/datasets/{i}", timeout=30).json()
        out.update({"downloads": m.get("downloads"), "likes": m.get("likes"), "gated": m.get("gated"),
                    "license": [t for t in m.get("tags", []) if t.startswith("license:")],
                    "arxiv": [t for t in m.get("tags", []) if t.startswith("arxiv:")],
                    "files": [s["rfilename"] for s in m.get("siblings", [])][:12]})
        sp = requests.get(f"https://datasets-server.huggingface.co/splits?dataset={i}", timeout=30).json()
        splits = sp.get("splits", [])
        out["splits"] = [(s["config"], s["split"]) for s in splits][:8]
        if splits:
            s = splits[0]
            fr = requests.get(f"https://datasets-server.huggingface.co/first-rows?dataset={i}&config={s['config']}&split={s['split']}",
                              timeout=60).json()
            out["features"] = [f["name"] for f in fr.get("features", [])]
            out["sample_rows"] = [{k: str(v)[:300] for k, v in r["row"].items()} for r in fr.get("rows", [])[:2]]
        sz = requests.get(f"https://datasets-server.huggingface.co/size?dataset={i}", timeout=30).json()
        out["size_bytes"] = (sz.get("size", {}).get("dataset", {}) or {}).get("num_bytes_original_files")
    except (requests.RequestException, ValueError, KeyError) as ex:
        out["error"] = f"{type(ex).__name__}: {ex}"
    return out


with ThreadPoolExecutor(8) as ex:
    res = list(ex.map(one, IDS))
Path("temp/search/hf_previews.json").write_text(json.dumps(res, indent=1, ensure_ascii=False))
for r in res:
    print(r["id"], "| dl", r.get("downloads"), "| lic", r.get("license"), "| arxiv", r.get("arxiv"), "| MB",
          round((r.get("size_bytes") or 0) / 1e6, 1), "| feats", r.get("features"), "|", (r.get("sample_rows") or [{}])[0].__repr__()[:250], r.get("error", ""))
