#!/usr/bin/env python3
"""Pre-registered cost-matched judge rule, applied to the 30-row pilot (both views): parse failure > 10% -> one retry
rule at max_tokens 300; still > 10% -> NOT_TESTABLE_PARSE. Original view on all rows iff pilot $/call <= 1.6e-4.
Prints one of: RUN_DISG_AND_ORIG | RUN_DISG_ONLY | RETRY_MT300 | NOT_TESTABLE_PARSE | PILOT_INCOMPLETE; writes
scores/costmatched_decision.json."""
import json
import sys
from pathlib import Path

WS = Path(__file__).resolve().parents[1]
SC = WS / "scores"


def stats(p: Path, keys: set) -> dict:
    rs = [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.exists() else []
    last = {}
    for r in rs:
        if r["row_key"] in keys:
            last[(r["row_key"], r["cond"])] = r
    vals = list(last.values())
    answered = [r for r in vals if r.get("p") is not None or r.get("fail") == "json_parse"]
    parse_fail = sum(r.get("fail") == "json_parse" for r in answered)
    cost = [r["cost"] for r in answered if r.get("cost")]
    return {"n_units": len(vals), "n_answered": len(answered), "parse_fail": parse_fail,
            "parse_fail_rate": parse_fail / len(answered) if answered else None, "usd_per_call": sum(cost) / len(cost) if cost else None,
            "api_fail": sum(1 for r in vals if str(r.get("fail") or "").startswith("api"))}


def main():
    rows = [json.loads(l) for l in (SC / "rows_E2B.jsonl").read_text().splitlines() if l.strip()]
    first = sorted([r for r in rows if r["parse_ok"] and r["e2b_batch"] == 1],
                   key=lambda r: (r["batch_key"], ["G1", "G1b", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9"].index(r["slot"])))[:30]
    keys = {r["row_key"] for r in first}
    s150 = stats(SC / "judge_costmatched.jsonl", keys)
    s300 = stats(SC / "judge_costmatched_mt300.jsonl", keys)
    if s150["n_answered"] < 50:
        d = "PILOT_INCOMPLETE"
    elif s150["parse_fail_rate"] <= 0.10:
        d = "RUN_DISG_AND_ORIG" if (s150["usd_per_call"] or 1) <= 1.6e-4 else "RUN_DISG_ONLY"
    elif s300["n_answered"] < 50:
        d = "RETRY_MT300"
    elif s300["parse_fail_rate"] <= 0.10:
        d = "RUN_DISG_AND_ORIG_MT300" if (s300["usd_per_call"] or 1) <= 1.6e-4 else "RUN_DISG_ONLY_MT300"
    else:
        d = "NOT_TESTABLE_PARSE"
    (SC / "costmatched_decision.json").write_text(json.dumps({"decision": d, "pilot_max_tokens_150": s150, "retry_max_tokens_300": s300,
                                                              "rule": "parse failure > 10% -> one retry at max_tokens 300; orig view on all rows iff $/call <= 1.6e-4"}, indent=1))
    print(d)


if __name__ == "__main__":
    main()
