#!/usr/bin/env python3
"""Fill the LLM response cache with the local llama.cpp model (OpenRouter key exhausted for the day).
Priority: (1) primary L3 questionnaire on every H/HREF/L sentence, (2) nonce-disguised sentences (contamination),
(3) decomposed judge on track-L then HREF then H (text, formula) pairs. Stops cleanly at the deadline; method.py
then runs cache-only and counts any miss as a coverage failure. Labels are never read."""
import asyncio
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
logger.add(ROOT / "logs" / "local_llm.log", level="DEBUG")

from pipeline import scoring_view  # noqa: E402
import fol_triage as FT  # noqa: E402
from llm import LocalLLM  # noqa: E402

MODEL = "local/qwen2.5-1.5b-instruct-q4_k_m"


async def main(deadline: float, phases: str):
    items = scoring_view(json.loads((ROOT / "screen_items.json").read_text()))
    href = json.loads((ROOT / "href_items.json").read_text())
    H = [x for x in items if x["track"] == "H"]
    L = [x for x in items if x["track"] == "L"]
    hh = list(dict.fromkeys([x["text"] for x in H] + [h["text"] for h in href]))
    lt = list(dict.fromkeys(x["text"] for x in L))
    llm = LocalLLM(MODEL)
    t0 = time.time()

    def left():
        return deadline - time.time()
    if "q" in phases:
        texts = list(dict.fromkeys(hh + lt))
        fails = 0
        for i, t in enumerate(texts):
            if left() < 0:
                logger.warning("deadline reached in phase q"); return
            r = await FT.role_questionnaire(t, llm, MODEL, tag="L3")
            fails += r["q"] is None
            if (i + 1) % 20 == 0:
                logger.info(f"L3 {i + 1}/{len(texts)} fails={fails} elapsed={time.time() - t0:.0f}s new_calls={llm.n_calls}")
        logger.info(f"phase q done: {len(texts)} texts, fails={fails}")
    if "r" in phases:  # test-retest: first 60 parseable HREF sentences, fresh model instance, tag L3retest
        from fol import parse
        ok = []
        for h in href:
            try:
                parse(h["candidate_fol"]); ok.append(h["text"])
            except Exception:  # noqa: BLE001
                pass
        for i, t in enumerate(ok[:60]):
            if left() < 0:
                logger.warning("deadline reached in phase r"); return
            await FT.role_questionnaire(t, llm, MODEL, tag="L3retest")
        logger.info("phase r done")
    if "d" in phases:
        from disguise import lemma_map
        from fol import parse
        ok = []
        for h in href:
            try:
                parse(h["candidate_fol"]); ok.append(h["text"])
            except Exception:  # noqa: BLE001
                pass
        texts = list(dict.fromkeys(ok + lt))
        import random
        random.Random(0).shuffle(texts)  # partial coverage at the deadline = a random subset
        for i, t in enumerate(texts):
            if left() < 0:
                logger.warning("deadline reached in phase d"); return
            dt, _ = lemma_map(t)
            await FT.role_questionnaire(dt, llm, MODEL, tag="L3disguised")
            if (i + 1) % 20 == 0:
                logger.info(f"disguised {i + 1}/{len(texts)} elapsed={time.time() - t0:.0f}s")
        logger.info("phase d done")
    if "j" in phases:
        from fol import parse
        pairs = []
        for x in L + href + H:
            try:
                parse(x["candidate_fol"])
            except Exception:  # noqa: BLE001
                continue
            pairs.append((x["text"], x["candidate_fol"]))
        pairs = list(dict.fromkeys(pairs))
        import random
        nL = len(list(dict.fromkeys((x["text"], x["candidate_fol"]) for x in L)))
        head, tail = pairs[:nL], pairs[nL:]
        random.Random(0).shuffle(head); random.Random(1).shuffle(tail)
        pairs = head + tail  # track-L pairs first (random order), then HREF/H
        for i, (t, f) in enumerate(pairs):
            if left() < 0:
                logger.warning(f"deadline reached in phase j at {i}/{len(pairs)}"); return
            try:
                await FT.decomposed_profile(t, f, llm, MODEL)
            except Exception as ex:  # noqa: BLE001
                logger.error(f"DJ failed: {ex}")
            if (i + 1) % 20 == 0:
                logger.info(f"DJ {i + 1}/{len(pairs)} elapsed={time.time() - t0:.0f}s")
        logger.info("phase j done")


if __name__ == "__main__":
    deadline = float(sys.argv[1]); phases = sys.argv[2] if len(sys.argv) > 2 else "qdj"  # absolute epoch deadline
    asyncio.run(main(deadline, phases))
