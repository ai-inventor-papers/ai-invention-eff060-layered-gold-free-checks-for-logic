import asyncio, json, sys
from pathlib import Path
from loguru import logger
from llm import LLM
from fol_triage import role_questionnaire, formula_role_profile, l3_compare
ROOT = Path(__file__).resolve().parent.parent
logger.remove(); logger.add(sys.stdout, level="INFO")
async def main(model, n):
    href = json.loads((ROOT / "href_items.json").read_text())[:n]
    async with LLM() as llm:
        rs = await asyncio.gather(*[role_questionnaire(h["text"], llm, model) for h in href])
        cost = sum(r["cost_usd"] for r in rs)
        for h, r in zip(href, rs):
            if r["q"] is None:
                print("FAIL", h["text"]); continue
            try:
                prof = formula_role_profile(h["candidate_fol"])
            except Exception as ex:
                print("parse fail", ex); continue
            c = l3_compare(r["q"], prof)
            print(h["text"][:90], "|", h["candidate_fol"][:80])
            print("   ", [(x["phrase"], x["role"], x["negated"], x["force"], x["claim"]) for x in r["q"]["concepts"]])
            print("   ", {k: (round(v, 2) if isinstance(v, float) else v) for k, v in c.items() if k != "extra_keys"})
        print(f"model {model}: cost ${cost:.5f} for {n} -> per call ${cost/n:.6f}; projected 3000 calls ${3000*cost/n:.2f}; fails {sum(r['q'] is None for r in rs)}")
asyncio.run(main(sys.argv[1], int(sys.argv[2])))
