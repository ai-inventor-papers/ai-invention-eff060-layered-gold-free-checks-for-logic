"""E2 compatibility shim (deviation D1, logged in prereg_E2.json): E's frozen code treats a sentence as carrying a
gold reference that is shown as a system row ('GOLD|none'), blind-audited and repaired only when
``sentence['source'].startswith('MALLS')``. The E2 plan requires the SAME treatment for the ProverQA (DT) gold.

Instead of editing E's code, every JSON-decoded dict whose 'source' starts with 'ProverQA' gets its value wrapped in
GoldSource, a str subclass whose startswith('MALLS') is True. The string value, equality and hashing are unchanged, so
nothing else in E's code (or in any output file) changes. install() patches json.loads/json.load process-wide.
"""
from __future__ import annotations

import json


class GoldSource(str):
    def startswith(self, prefix, *a):  # noqa: D401
        if prefix == "MALLS":
            return True
        return str.startswith(self, prefix, *a)


_real_loads = json.loads


def _hook(d: dict) -> dict:
    s = d.get("source")
    if isinstance(s, str) and s.startswith("ProverQA"):
        d["source"] = GoldSource(s)
    return d


def _loads(s, *a, **k):
    if "object_hook" not in k and "object_pairs_hook" not in k:
        k["object_hook"] = _hook
    return _real_loads(s, *a, **k)


def install() -> None:
    json.loads = _loads
    json.load = lambda fp, *a, **k: _loads(fp.read(), *a, **k)
