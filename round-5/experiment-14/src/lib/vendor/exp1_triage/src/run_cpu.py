"""Warm the CPU-layer cache for every (text, fol) the pipeline scores (labels never read)."""
import json, sys, time
from pathlib import Path
from loguru import logger
sys.path.insert(0, str(Path(__file__).resolve().parent))
from pipeline import run_cpu_layers, scoring_view
ROOT = Path(__file__).resolve().parent.parent
logger.remove(); logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(ROOT / "logs" / "cpu.log", level="DEBUG")
if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else None
    items = scoring_view(json.loads((ROOT / "screen_items.json").read_text()))
    href = json.loads((ROOT / "href_items.json").read_text())
    inv = json.loads((ROOT / "invariance_set.json").read_text())
    text_of = {x["item_id"]: x["text"] for x in items}
    pairs = [(x["text"], x["candidate_fol"]) for x in items + href]
    pairs += [(text_of[r["item_id"]], r["rewritten_fol"]) for r in inv if r["rewritten_fol"]]
    if n:
        pairs = pairs[:n]
    t0 = time.time()
    res = run_cpu_layers(pairs)
    from collections import Counter
    logger.info(f"done {len(res)} in {time.time()-t0:.0f}s; status {Counter(r['status'] for r in res.values())}")
