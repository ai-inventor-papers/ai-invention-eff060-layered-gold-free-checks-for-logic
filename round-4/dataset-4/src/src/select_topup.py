#!/usr/bin/env python3
"""Pre-registered L25 TOP-UP (prereg_strata.json 'top_up_rule', frozen at selection time, before any label was seen):
'If after Step 3 the tier-A-projected ERROR or CORRECT count of L25 is below 60, generate one more sha1-ordered batch
of 100 L25 sentences with the 5 cheapest generator slots, budget permitting.'  Triggered (tier-A CORRECT = 9).

Selection = the SAME rule as step 1 (select_sentences.py: MALLS-train pool, screen-hash exclusion, >=25 words and
n_conditions>=3, even over word bins 25-29/30-34/>=35, sha1 order) applied to the pool minus every sentence already
used (600 held-out, few-shot exemplars, calibration). The batch is appended to work/sentences.json with
topup_batch=1 and a frozen record is added to prereg_strata.json.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from select_sentences import build_exclusion, malls_pool, pick_binned, h  # noqa: E402

W = ROOT / "work"


def main():
    sents = json.loads((W / "sentences.json").read_text())
    if any(s.get("topup_batch") for s in sents):
        print("top-up already selected"); return
    used = {s["sentence_id"] for s in sents}
    used |= {s["sentence_id"] for s in json.loads((W / "fewshot_exemplars.json").read_text())}
    used |= {s["sentence_id"] for s in json.loads((W / "calib_sentences.json").read_text())}
    ex, _ = build_exclusion()
    pool, _ = malls_pool(ex)
    rest = [r for r in pool if r["sentence_id"] not in used and r["words"] >= 25 and r["n_conditions"] >= 3]
    top, log = pick_binned(rest, [(25, 29), (30, 34), (35, 10 ** 6)], [34, 33, 33])
    for r in top:
        r["source_stratum"] = "L25"
        r["topup_batch"] = 1
        r["reference_status_initial"] = "MALLS_GPT4_GOLD"
        r.setdefault("agreement_type", None)
    coll = sum(h(r["text"]) in ex for r in top)
    assert coll == 0 and len({r["sentence_id"] for r in top} & used) == 0 and len(top) == 100
    (W / "sentences.json").write_text(json.dumps(sents + top, ensure_ascii=False, indent=1))
    (W / "sentences_topup.json").write_text(json.dumps(top, ensure_ascii=False, indent=1))
    pre = json.loads((ROOT / "prereg_strata.json").read_text())
    pre["top_up_execution"] = {
        "executed_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "trigger": "tier-A CORRECT count of L25 after Step 3 = 9 (< 60)",
        "n_sentences": len(top), "l25_remaining_pool": len(rest), "bin_log": log, "hash_collisions_with_screen": coll,
        "slots": "5 cheapest few-shot generator slots by catalog price (see work/topup_slots.json)",
        "note": "selected by the frozen step-1 rule on the unused pool; decided by the pre-written rule, not by inspecting labels"}
    (ROOT / "prereg_strata.json").write_text(json.dumps(pre, indent=1))
    print(f"top-up: {len(top)} L25 sentences; bins {log}")


if __name__ == "__main__":
    main()
