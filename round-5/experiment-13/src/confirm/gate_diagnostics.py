#!/usr/bin/env python3
"""FALLBACK B diagnostics ($0): the gloss gate failed twice (gloss_v1 on half A, the ONE revision gloss_v2 on half B).
Reports which checker failed, on which class, and whether the failure is a verdict-FORMAT failure (NO_VERDICT) or a
judgement failure (accuracy on the verdicted items). It also computes the Haiku-only (s6-style) and Qwen-only gate rules
and the pass margins. It reads only results/gate_items.json + gate_report.json. Writes results/gate_diagnostics.json."""
from __future__ import annotations

import json

from cc import LAB, RES, dump, setup_logger, wilson

logger = setup_logger("gate_diagnostics")
CLASSES = ["YES_IDENT", "YES_SYN", "YES_FORM", "NO_NONCE", "NO_DONOR", "NO_ROLE", "NO_MERGE"]


def block(items: list[dict], f) -> dict:
    yes = [i for i in items if i["gold"] == "YES"]
    no = [i for i in items if i["gold"] == "NO"]
    ky, kn = sum(f(i) == "YES" for i in yes), sum(f(i) == "NO" for i in no)
    ry, rn = ky / max(len(yes), 1), kn / max(len(no), 1)
    out = {"n_yes": len(yes), "n_no": len(no), "recall_YES": round(ry, 4), "recall_YES_ci": wilson(ky, len(yes)),
           "recall_NO": round(rn, 4), "recall_NO_ci": wilson(kn, len(no)), "balanced_accuracy": round((ry + rn) / 2, 4),
           "no_verdict": sum(f(i) not in ("YES", "NO") for i in items)}
    out["per_class"] = {}
    for c in CLASSES:
        cr = [i for i in items if i["class"] == c]
        k = sum(f(i) == i["gold"] for i in cr)
        out["per_class"][c] = {"n": len(cr), "recall": round(k / max(len(cr), 1), 4), "ci": wilson(k, len(cr)),
                               "no_verdict": sum(f(i) not in ("YES", "NO") for i in cr), "flag_below_0.85": k / max(len(cr), 1) < 0.85}
    return out


@logger.catch(reraise=True)
def main() -> None:
    items = json.loads((LAB / "results/gate_items.json").read_text())
    rep = json.loads((LAB / "results/gate_report.json").read_text())
    out = {"gate_runs": {k: {"PASS": v["PASS"], "per_checker_BA": {c: v["per_checker"][c]["balanced_accuracy"] for c in v["per_checker"]},
                             "kappa": v["cohen_kappa_haiku_qwen"], "n_items": v["n_items"]} for k, v in rep.items()},
           "pass_rule": "BA >= 0.90 for haiku, qwen AND both_yes; both_yes recall_YES >= 0.85 and recall_NO >= 0.85"}
    for version, half in (("gloss_v1", "A"), ("gloss_v2", "B")):
        it = [i for i in items if i["half"] == half]
        hk = lambda i, v=version: i.get(f"haiku_{v}")  # noqa: E731
        qw = lambda i, v=version: i.get(f"qwen_{v}")  # noqa: E731
        both = lambda i: "YES" if hk(i) == "YES" and qw(i) == "YES" else "NO"  # noqa: E731
        d = {"haiku": block(it, hk), "qwen": block(it, qw), "both_yes": block(it, both)}
        # judgement accuracy on verdicted items only (separates format failures from judgement failures)
        d["haiku_verdicted_only"] = block([i for i in it if hk(i) in ("YES", "NO")], hk)
        d["qwen_verdicted_only"] = block([i for i in it if qw(i) in ("YES", "NO")], qw)
        d["single_checker_rules"] = {
            "haiku_only_pass": bool(d["haiku"]["balanced_accuracy"] >= 0.90 and d["haiku"]["recall_YES"] >= 0.85 and d["haiku"]["recall_NO"] >= 0.85),
            "qwen_only_pass": bool(d["qwen"]["balanced_accuracy"] >= 0.90 and d["qwen"]["recall_YES"] >= 0.85 and d["qwen"]["recall_NO"] >= 0.85),
            "haiku_verdicted_only_BA": d["haiku_verdicted_only"]["balanced_accuracy"]}
        d["which_failed"] = [c for c in ("haiku", "qwen", "both_yes") if d[c]["balanced_accuracy"] < 0.90]
        d["classes_below_0.85"] = {c: [k for k, v in d[c]["per_class"].items() if v["flag_below_0.85"]] for c in ("haiku", "qwen", "both_yes")}
        out[f"{version}_{half}"] = d
    out["reading"] = (
        "gloss_v1 (half A) failed on JUDGEMENT: no NO_VERDICT; haiku BA 0.776 (misses in-name negation forms, accepts non-word tokens and "
        "reversed roles), qwen BA 0.855. gloss_v2 (half B, held out) failed on FORMAT for haiku (verdict-first rule broken: analysis text "
        "truncated at max_tokens 300 -> NO_VERDICT) AND on judgement for qwen (BA 0.883 < 0.90 with 0 NO_VERDICT). A single-checker rescue "
        "(fallback C) is not available either: neither checker passes alone. Frozen consequence (FALLBACK B): MAPPED rows -> "
        "UNRESOLVED_GLOSS_GATE_FAILED; criterion (c) NOT_TESTABLE; no ungated checker substituted.")
    dump(RES / "gate_diagnostics.json", out)
    for k in ("gloss_v1_A", "gloss_v2_B"):
        d = out[k]
        logger.info(f"{k}: failed {d['which_failed']}; haiku BA {d['haiku']['balanced_accuracy']} (verdicted-only "
                    f"{d['haiku_verdicted_only']['balanced_accuracy']}, NO_VERDICT {d['haiku']['no_verdict']}); qwen BA {d['qwen']['balanced_accuracy']}; "
                    f"single-checker {d['single_checker_rules']}")


if __name__ == "__main__":
    main()
