#!/usr/bin/env python3
"""TODO 3-5 survey: preview 12 HF candidates via the Datasets Server API (no `datasets` dependency), then download the
6 kept ones (parquet/json rows) into temp/datasets/. Context/positioning only: the artifact's labels come from this
run's own R_COMP data (see README)."""
from __future__ import annotations

import asyncio
import json
import os
import sys

import httpx

from common import ROOT

API = "https://datasets-server.huggingface.co"
HUB = "https://huggingface.co/api/datasets"
CANDS = ["tasksource/folio", "yale-nlp/FOLIO", "yuan-yang/MALLS-v0", "DSAVlab-UNIUD/MALLS_test_subset-CURATED",
         "opendatalab/ProverQA", "tasksource/LogicNLI", "tasksource/proofwriter", "tasksource/ruletaker",
         "KK04/LogicInference_OA", "sxiong/entailmentbank", "Isotonic/symbolic_data_first_order_logic", "minimario/FOLIO"]
H = {"Authorization": f"Bearer {os.environ.get('HF_TOKEN', '')}"} if os.environ.get("HF_TOKEN") else {}


async def preview(c: httpx.AsyncClient, ds: str) -> dict:
    out = {"id": ds}
    try:
        meta = (await c.get(f"{HUB}/{ds}", headers=H)).json()
        out.update(downloads=meta.get("downloads"), likes=meta.get("likes"), gated=meta.get("gated"),
                   card=(meta.get("cardData") or {}).get("license"), tags=[t for t in meta.get("tags", []) if ":" in t][:8])
        sp = (await c.get(f"{API}/splits", params={"dataset": ds}, headers=H)).json()
        splits = sp.get("splits", [])
        out["splits"] = [(s["config"], s["split"]) for s in splits]
        if splits:
            s0 = splits[0]
            fr = (await c.get(f"{API}/first-rows", params={"dataset": ds, "config": s0["config"], "split": s0["split"]}, headers=H)).json()
            out["columns"] = [f["name"] for f in fr.get("features", [])]
            out["rows"] = [{k: (str(v)[:300]) for k, v in r["row"].items()} for r in fr.get("rows", [])[:2]]
            sz = (await c.get(f"{API}/size", params={"dataset": ds}, headers=H)).json()
            out["num_rows"] = (sz.get("size", {}).get("dataset", {}) or {}).get("num_rows")
            out["bytes"] = (sz.get("size", {}).get("dataset", {}) or {}).get("num_bytes_parquet_files")
        else:
            out["error"] = sp.get("error")
    except (httpx.HTTPError, ValueError, KeyError) as e:
        out["error"] = f"{type(e).__name__}: {e}"
    return out


async def download(c: httpx.AsyncClient, ds: str, config: str, split: str, max_rows: int = 20000) -> dict:
    rows, off = [], 0
    while off < max_rows:
        r = (await c.get(f"{API}/rows", params={"dataset": ds, "config": config, "split": split, "offset": off, "length": 100},
                         headers=H)).json()
        batch = [x["row"] for x in r.get("rows", [])]
        rows += batch
        if len(batch) < 100:
            break
        off += 100
    p = ROOT / "temp/datasets" / f"full_{ds.replace('/', '_')}_{config}_{split}.json"
    p.write_text(json.dumps(rows, ensure_ascii=False))
    return {"id": ds, "config": config, "split": split, "rows": len(rows), "path": str(p.relative_to(ROOT))}


async def main(mode: str) -> None:
    async with httpx.AsyncClient(timeout=60) as c:
        if mode == "preview":
            res = await asyncio.gather(*[preview(c, d) for d in CANDS])
            (ROOT / "temp/hf_preview_12.json").write_text(json.dumps(res, indent=1, ensure_ascii=False))
            for r in res:
                print(r["id"], r.get("downloads"), r.get("num_rows"), r.get("columns"), r.get("error", "")[:80] if r.get("error") else "")
        else:
            keep = json.loads(sys.argv[2])
            sem = asyncio.Semaphore(4)

            async def one(k):
                async with sem:
                    return await download(c, *k)
            res = await asyncio.gather(*[one(k) for k in keep])
            (ROOT / "temp/datasets/download_log.json").write_text(json.dumps(res, indent=1))
            print(json.dumps(res, indent=1))


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1]))
