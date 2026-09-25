#!/usr/bin/env python3
"""Build the shared screen: screen_items.json, href_items.json, invariance_set.json, screen_meta.json."""
import json
import sys
import time
from pathlib import Path

from loguru import logger

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.setrecursionlimit(10000)
ROOT = Path(__file__).resolve().parent.parent
logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(ROOT / "logs" / "screen.log", rotation="30 MB", level="DEBUG")


@logger.catch(reraise=True)
def main():
    import screen
    t0 = time.time()
    mx = int(sys.argv[1]) if len(sys.argv) > 1 else None
    out = screen.build(max_items=mx)
    outdir = ROOT / ("results/mini_screen" if mx else ".")
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "screen_items.json").write_text(json.dumps(out["items"], ensure_ascii=False, indent=1))
    (outdir / "href_items.json").write_text(json.dumps(out["href"], ensure_ascii=False, indent=1))
    inv = screen.build_invariance(out["items"])
    (outdir / "invariance_set.json").write_text(json.dumps(inv, ensure_ascii=False, indent=1))
    meta = out["meta"]
    from collections import Counter
    meta["invariance"] = {f: dict(Counter(str(r["verified_equiv"]) for r in inv if r["family"] == f))
                          for f in sorted({r["family"] for r in inv})}
    meta["n_invariance_items"] = len({r["item_id"] for r in inv})
    meta["unmatched_conclusions_sample"] = out["unmatched_conclusions"][:40]
    meta["n_unmatched_conclusion_texts"] = len(out["unmatched_conclusions"])
    meta["build_secs"] = round(time.time() - t0, 1)
    (outdir / "screen_meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1))
    (ROOT / "results").mkdir(exist_ok=True)
    (ROOT / "results" / "premise_agreement.json").write_text(json.dumps(out["premise_meta"], ensure_ascii=False, indent=1))
    logger.info(json.dumps({k: meta[k] for k in ("n_by_track_label", "match_rate", "premise_agreement", "invariance")}, indent=1))


if __name__ == "__main__":
    main()
