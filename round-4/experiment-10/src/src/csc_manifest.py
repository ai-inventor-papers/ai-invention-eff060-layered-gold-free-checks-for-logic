"""Job manifest for the CSC peer sweep that could not run (D-BUDGET) + the FREE firewall record.

data/csc_jobs.jsonl        one line per unique (stage, text, signature): sig_key, models, prompt sha1 per model
                           (prompts are rebuilt byte-identically by csc_lib.csc_prompt; nothing else is needed).
results/csc_job_manifest.json  counts per stage, projected $ from the sibling-measured per-call prices, and the
                           command that runs everything once the budget is raised: `python method.py --stage peers`.
results/firewall.json      whitelist, files never opened, sha256 of the firewalled FREE view, statement.
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path

SRC = Path(__file__).resolve().parent
ROOT = SRC.parent
sys.path.insert(0, str(SRC))
import csc_lib as L  # noqa: E402
import peers_run as PR  # noqa: E402
import views as V  # noqa: E402

DATA = ROOT / "data"
RES = ROOT / "results"
E9_PILOT = Path("../../../experiment-9/src/results/pilot.json")


def main() -> None:
    price = {m: d["usd_per_call"] for m, d in json.loads(E9_PILOT.read_text())["per_model"].items()}
    stages = {"perturb_E": PR.perturb_jobs(False), "free": PR.free_jobs(), "perturb_R": PR.perturb_jobs(True),
              "sig": PR.sig_jobs()}
    n_lines = 0
    summ = {}
    with (DATA / "csc_jobs.jsonl").open("w") as f:
        for st, jobs in stages.items():
            usd = 0.0
            for j in jobs:
                sig = PR.sig_tuples(j["signature"])
                msgs = L.csc_prompt(j["text"], sig)
                sha = {m: hashlib.sha1((m + "|" + json.dumps(msgs, ensure_ascii=False, sort_keys=True)).encode()).hexdigest()
                       for m in j["models"]}
                usd += sum(price[m] for m in j["models"])
                f.write(json.dumps({"stage": st, "text": j["text"], "sig_key": j["sig_key"], "signature": j["signature"],
                                    "models": j["models"], "prompt_sha1": sha}, ensure_ascii=False) + "\n")
                n_lines += 1
            summ[st] = {"n_signatures": len(jobs), "n_calls": sum(len(j["models"]) for j in jobs), "projected_usd": round(usd, 3)}
    summ["retest"] = {"n_signatures": 60, "n_calls": 240, "projected_usd": round(60 * sum(price.values()), 3)}
    tot = sum(v["projected_usd"] for v in summ.values())
    man = {"created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "stages": summ,
           "projected_total_usd": round(tot, 3), "projected_total_usd_x1.1": round(tot * 1.1, 3),
           "price_source": str(E9_PILOT), "prompt_variant": "v1 (block template sha256 " + L.block_template_sha256() + ")",
           "jobs_file": "data/csc_jobs.jsonl", "jobs_file_sha256": hashlib.sha256((DATA / "csc_jobs.jsonl").read_bytes()).hexdigest(),
           "how_to_run": "raise the run's 'Test idea' OpenRouter budget, then `.venv/bin/python method.py --stage peers` "
                         "(pilot -> sweeps -> retest; cached, resumable, hard stop $9.5) and `--stage score,typing,analysis,output`",
           "status": "NOT RUN: every call returned 403 aii_run_budget_exhausted (see results/deviations.json)"}
    (RES / "csc_job_manifest.json").write_text(json.dumps(man, indent=1))
    fv = DATA / "rcomp_free_view.jsonl"
    fw = {"whitelist_fields": list(V.FREE_WHITELIST), "files_never_opened": ["free_labels.jsonl"],
          "firewalled_view": "data/rcomp_free_view.jsonl", "firewalled_view_sha256": hashlib.sha256(fv.read_bytes()).hexdigest(),
          "csc_rcomp_free_peers": "NOT GENERATED (D-BUDGET); results/csc_rcomp_free_peers.jsonl does not exist",
          "n_rows": sum(1 for _ in fv.open()),
          "n_parseable": sum(1 for x in fv.read_text().splitlines() if json.loads(x)["cand_parse_ok"]),
          "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
          "statement": "no FREE label was read: FREE rows were projected to the whitelist at parse time (views.project_free); "
                       "free_labels.jsonl was never opened; no FREE row enters method_out.json or any labelled analysis"}
    (RES / "firewall.json").write_text(json.dumps(fw, indent=1))
    print(json.dumps(man, indent=1))


if __name__ == "__main__":
    main()
