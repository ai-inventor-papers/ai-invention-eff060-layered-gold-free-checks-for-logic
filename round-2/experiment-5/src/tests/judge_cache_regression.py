#!/usr/bin/env python3
"""Judge prompt-identity regression: re-score 30 exp-D screen items (disguised) through the vendored judge_json with the
exact rubric/template/model/max_tokens used on E. Every call must HIT the vendored exp-D cache (0 new cost) and reproduce
exp D's per-item score exactly. Writes results/judge_cache_regression.json."""
import asyncio
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
from vendor_d import budget as VB  # noqa: E402
from vendor_d import judges as J  # noqa: E402

items = json.loads((ROOT / "data" / "screen" / "expD_screen_items.json").read_text())
dmap = json.loads((ROOT / "data" / "screen" / "expD_disguise_map.json").read_text())
ref = {json.loads(l)["item_id"]: json.loads(l) for l in (ROOT / "data" / "screen" / "expD_per_item_scores.jsonl").read_text().splitlines()}
sel = [x for x in sorted(items, key=lambda x: x["item_id"]) if x["track"] == "L" and x["item_id"] in ref
       and ref[x["item_id"]]["oriented_scores"].get("judge_cheap_disg") is not None][:30]


async def run():
    async with VB.Budget() as b:
        spent0 = b.spent
        outs = await asyncio.gather(*[J.judge_json(b, component="judge_cheap_primary", model="google/gemini-2.5-flash-lite",
                                                   rubric=J.RUBRIC_A, text=dmap[x["item_id"]]["text_d"], fol=dmap[x["item_id"]]["fol_d"],
                                                   item_id=x["item_id"], max_tokens=150, user_tmpl=J.USER_JSON_A) for x in sel])
        return outs, b.spent - spent0, b.n_calls
outs, new_cost, n_calls = asyncio.run(run())
match = [abs((1 - o["p"]) - ref[x["item_id"]]["oriented_scores"]["judge_cheap_disg"]) < 1e-12 for x, o in zip(sel, outs) if o.get("p") is not None]
res = {"n": len(sel), "n_scored": len(match), "n_exact_match": sum(match), "new_api_calls": n_calls, "new_cost_usd": new_cost}
(ROOT / "results" / "judge_cache_regression.json").write_text(json.dumps(res, indent=1))
print(json.dumps(res))
