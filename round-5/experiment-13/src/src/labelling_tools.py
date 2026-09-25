"""Re-export of the dataset-5 name-free labelling functions (labeller/src/freelab.py, unchanged, sha 06e14f58...).

GOLD-USING LABELLING TOOLS: every function here needs the ACCEPTED READINGS of the sentence (gold formulas) and, for the
gloss step, the gold atom glosses. They build meta-evaluation LABELS; they are NEVER a gold-free faithfulness metric and
must not be reported as one.

- exhaustive_map_label(candidate_fol, readings, atoms=None, glosses=None, checker=None) -> {'label', 'certificate', ...}:
  ERROR_CERT when no map of the declared symbol-map family makes the candidate z3-equivalent to an accepted reading
  (exact relative to the family); otherwise the gloss checker decides CORRECT / READING_CHOICE / ERROR_GLOSS /
  UNRESOLVED_GLOSS (model-relative; in iteration 5 the two-checker gloss gate FAILED, so no gated checker exists).
- equivalent_modulo_vocab_exhaustive(a_fol, b_fol) -> (True | False | None, map, n_maps): equivalence up to a family
  renaming (name-free; NOT meaning-equivalence without a gloss check).
- gloss_decision(maps, pairs_union, verdict) -> (label, map index): the frozen two-checker decision rule.
"""
from __future__ import annotations

import sys
from pathlib import Path

_LAB = Path(__file__).resolve().parents[1] / "labeller"
for _p in (_LAB / "vendor", _LAB / "src"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from freelab import equivalent_modulo_vocab_exhaustive, exhaustive_map_label, gloss_decision  # noqa: E402

__all__ = ["exhaustive_map_label", "equivalent_modulo_vocab_exhaustive", "gloss_decision"]
