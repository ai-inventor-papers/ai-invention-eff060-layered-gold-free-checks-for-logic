#!/usr/bin/env python3
"""Score seal (Step 3.4) and its verification.

  seal    -> scores/score_seal.json: sha256 of scores/scores_E2B.jsonl, controls_scores_E2B.jsonl, every judge / pool /
             matrix / variants / local file, the frontier subsample, every scoring source file (exp5src/src/**.py,
             eval2src/*.py, freeze_copy/*, exp6src/src/pilot_metrics.py, src/score_e2b.py, src/pairwise_e2b.py), the
             M1/M2 marker copies, and whether any path under sealed/ or containing 'label'/'reference' (other than the
             label-free *_nolabels.jsonl files) appears in scores/file_access_log.txt. Refuses to seal if it does.
  verify  -> exit 0 iff every hash still matches (the label join refuses to run otherwise)."""
from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path

WS = Path(__file__).resolve().parents[1]
SC = WS / "scores"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def targets() -> list[Path]:
    fs = [SC / n for n in ("scores_E2B.jsonl", "controls_scores_E2B.jsonl", "rows_E2B.jsonl", "pool_E2B.jsonl", "pairwise_classes_E2B.jsonl",
                           "variants_E2B.jsonl", "variants_meta_E2B.json", "local_E2B.jsonl", "disguise_E2B.jsonl", "judge_flashlite.jsonl",
                           "judge_nano.jsonl", "judge_costmatched.jsonl", "judge_costmatched_mt300.jsonl", "judge_frontier.jsonl",
                           "frontier_subsample.json", "costmatched_decision.json", "gg_scores_E2B.jsonl", "controls_lf_E2B.jsonl", "controls_lf_scores_E2B.jsonl")]
    fs += sorted((WS / "exp5src" / "src").rglob("*.py")) + sorted((WS / "eval2src").glob("*.py")) + sorted((WS / "freeze_copy").glob("*"))
    fs += [WS / "exp6src" / "src" / "pilot_metrics.py", WS / "src" / "score_e2b.py", WS / "src" / "pairwise_e2b.py",
           WS / "exp5src" / "results" / "prereg.json", WS / "exp5src" / "results" / "E_l3_q.jsonl", WS / "e2b" / "drift_decision.json",
           WS / "e2b" / "prompt_sha_expected.json", WS / "prereg_iter5_E2B.json"]
    return [p for p in fs if p.exists() and p.is_file()]


def access_violations() -> list[str]:
    p = SC / "file_access_log.txt"
    bad = []
    if p.exists():
        for line in p.read_text().splitlines():
            parts = line.split("\t")
            if len(parts) < 3:
                continue
            path = parts[2].lower()
            name = path.rsplit("/", 1)[-1]
            if "/sealed/" in path or ("label" in name and "nolabel" not in name) or "reference" in name:
                bad.append(parts[2])
    return bad


def seal() -> int:
    bad = access_violations()
    if bad:
        print(json.dumps({"refused": "file access log shows label/reference paths", "paths": bad[:20]}))
        return 1
    files = {str(p.relative_to(WS)): sha(p) for p in targets()}
    rows = [json.loads(l) for l in (SC / "scores_E2B.jsonl").read_text().splitlines() if l.strip()]
    out = {"sealed_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "n_score_rows": len(rows), "files": files,
           "file_access_log_lines": len((SC / "file_access_log.txt").read_text().splitlines()) if (SC / "file_access_log.txt").exists() else 0,
           "file_access_violations": 0, "label_seal_json_sha256": sha(WS / "e2bsrc" / "seal.json") if (WS / "e2bsrc" / "seal.json").exists() else None,
           "protocol": "every score in scores/ was computed before any label join; analysis/analyse_e2b.py verifies this seal and the label seal before joining"}
    (SC / "score_seal.json").write_text(json.dumps(out, indent=1))
    print(json.dumps({"sealed": len(files), "n_score_rows": len(rows)}))
    return 0


def verify() -> int:
    s = json.loads((SC / "score_seal.json").read_text())
    bad = [rel for rel, h in s["files"].items() if not (WS / rel).exists() or sha(WS / rel) != h]
    print(json.dumps({"score_seal_intact": not bad, "mismatches": bad}))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit({"seal": seal, "verify": verify}[sys.argv[1]]())
