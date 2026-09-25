> NOTE (published copy): this file names server paths this repository
> does not publish (a stage it does not ship, or another run's workspace),
> so the steps that read them will not run from a clone as written:
>   /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/*/

# §5 Iteration 5 — skeleton (cells are `{{file::json.path}}` shells)

## §5.1 Reasoning block

- The iteration-4 review scored the record 3<!-- n:rv4_score --> (blocking) with 11<!-- n:rv4_n --> critiques; the corrected record (`record_final.md`, this artifact) closes them with file-sourced text.
- Move: **Test the model-agreement check on fresh data** — DEEPEN on the one live lead, frozen `c_score_align`; E is development data, E2 / E2-B / R_COMP FREE are the untouched confirmation data.
- Predictions (strategy, stated in advance): After this iteration:
(1) E2 is complete and sealed, with the drift gate decided under pinned providers; frozen scores are sealed before labels; and there is a verdict CONFIRM / PARTIAL / DISCONFIRM on the pre-declared long-pool primary, plus nesting over S4_E2, DT sign, H-MECH (i)-(iv), rename FA/flip, tau-b, coverage and cost.
(2) E2-B adds about 400 fresh L25 sentences, with a union long-pool estimate at MDE below 0.09, a between-sample heterogeneity check, and cost-matched-judge and frontier comparisons with cost per candidate.
(3) R_COMP FREE has gated, sealed, instrument-disjoint labels (expected CORRECT well above 200 on the untouched subset) and a verdict on criterion (c).
(4) The freeze package: the H-IMPROVE winner (or NONE) and the GG gate, frozen before labels, plus the deliverable function library.
(5) A file-sourced corrected record closing all 11 blocking items, a claims l
- Gates: the CONFIRM / PARTIAL / DISCONFIRM rules below (verbatim from the hypothesis §4), the drift gate, the freeze markers (token-checked).
- Planned artifacts and caps (iteration-5 strategy):

| type | objective (truncated) | cap |
|-|-|-|
| experiment | REPLICATION on untouched data (the primary confirmation). Finish the frozen 550-sentence E2 set (L25 350, EXC 100, DT 10… | $9.5<!-- n:i5_cap_0 --> |
| experiment | MORE POWER: a second, independent untouched L25 sample. E2-A's 350 L25 sentences give MDE80 about 0.11 on L25, and the l… | $9.5<!-- n:i5_cap_1 --> |
| experiment | FIX, claim unchanged: make R_COMP FREE (in-scope free vocabulary; long templated sentences with trusted-by-construction … | $4.0<!-- n:i5_cap_2 --> |
| experiment | MECHANISM -> CLEANER MEASURE, and BOUNDARY, on development data at about $0-1.5, frozen for the E2 confirmers. (A) H-IMP… | $2.0<!-- n:i5_cap_3 --> |
| evaluation | Close every BLOCKING review item with file-sourced, paste-ready paper text ($0, CPU). The previous review blocks publica… | $0.0<!-- n:i5_cap_4 --> |

## Decision rules (verbatim, hypothesis §4)

```
4. SUCCESS CRITERIA (fixed now)
========================================================================

CONFIRM (the lead becomes a finding):
- (a) E2 long pool: frozen c_score_align − flash-lite disguised strat CI > 0 AND point > 0 vs flash-lite original and nano.
- (b) E2 nested [S4_E2 + c] − S4_E2 strat CI > 0.
- (c) R_COMP FREE untouched (if testable): within-template c_score_align − flash-lite, disguised AND original, CI > 0. This is the first in-scope, free-vocabulary, trusted-reference test on long conditioned sentences.

PARTIAL:
- (a) holds, (c) is untestable or n.s.: confirmed on real long sentences, free-vocabulary templated text unresolved.
- (c) holds, (a) is n.s. with point ≥ +0.05: 'underpowered on E2, confirmed on R_COMP FREE'.

DISCONFIRM: the (a) point ≤ 0 on the E2 long pool. The E result was development-set optimism, and the judge/stack is the incumbent. This is reported plainly.

Also reported, not gating:
- L25 alone (expected MDE 0.11; the point estimate is stated with its power);
- DT sign (domain transfer);
- frontier ratio and nested gain on the 300-row subsample;
- system-level τ-b over 13 system × variant rows;
- rename FA and paired flip for c_score_align on E2 CORRECT rows under RENAME_SYN and RENAME_NONCE;
- coverage with unparseables in the denominator;
- $ and seconds per candidate, FULL vs MARGINAL.

H-MECH is scored CONFIRMED or REFUTED per item (i)-(iv).

H-IMPROVE: the carried variant − V0 on the E2 long pool, strat CI > 0 → CONFIRMED improvement; otherwise V0 stands and the variant is reported as a development-only result.

H-RENAME: CONFIRMED only if GG passed the dev gate AND on E2 CORRECT rows its RENAME_SYN paired flip is ≤ 0.05 while its E2 long-pool AUROC is ≥ c_score_align − 0.01.

ERROR TYPE (the user's 'which kind of error'):
- The answer is NEGATIVE outside a shared vocabulary: free3 0.123 on E; medoid 0.328 vs judge 0.326.
- Within a shared vocabulary, typed repair reaches 0.784 (SIGPROXY), but that regime is out of scope.
- No new budget.

===================================================================
```

### §5.2 Drift gate (E2 panel, pinned providers)

| quantity | value (shell) | resolution |
|-|-|-|
| decision (PASS/FAIL) | "PASS" (from `../../experiment-11/src/e2/E2_DRIFT_DECISION.json`) | FIELD_PRESENT; FILLED (seal present) |
| drift criteria (track-H flag rates etc.) | {"combined_majority_agreement": {"value": 0.9554, "threshold": 0.85, "n_items": 269, "ok": true}, "every_panel_model_id_ (from `../../experiment-11/src/e2/E2_DRIFT_DECISION.json`) | FIELD_PRESENT; FILLED (seal present) |
| replayed judgements / per-member agreement | {"synthetic_gate": 77, "trackh_judgements": 192, "combined": 269, "n_no_majority_new": 0} (from `../../experiment-11/src/e2/E2_DRIFT_DECISION.json`) | FIELD_PRESENT; FILLED (seal present) |
| pinned provider per panel model | {"anthropic/claude-haiku-4.5": {"order": ["Amazon Bedrock"], "allow_fallbacks": false}, "z-ai/glm-4.6": {"order": ["Veni (from `../../experiment-11/src/e2/E2_DRIFT_DECISION.json`) | FIELD_PRESENT; FILLED (seal present) |

### §5.3 E2-A long-pool confirmation (PRIMARY, pre-declared)

| quantity | value (shell) | resolution |
|-|-|-|
| Δ strat c_score_align − flash-lite disguised [CI] | {{confirm_verdict_E2A.json::longpool.delta_strat_flashlite_disg.ci}} | FILE_MISSING |
| Δ vs flash-lite original | {{confirm_verdict_E2A.json::longpool.delta_strat_flashlite_orig.point}} | FILE_MISSING |
| Δ vs gpt-4.1-nano | {{confirm_verdict_E2A.json::longpool.delta_strat_nano.point}} | FILE_MISSING |
| nested [S4_E2 + c] − S4_E2 [CI] | {{confirm_verdict_E2A.json::nested.delta_strat.ci}} | FILE_MISSING |
| L25 alone Δ [CI] (MDE stated) | {{confirm_verdict_E2A.json::L25.delta_strat_flashlite_disg.ci}} | FILE_MISSING |
| DT sign | {{confirm_verdict_E2A.json::DT.delta_sign}} | FILE_MISSING |
| n (usable sentences / rows) and completed fraction per stratum | {{confirm_verdict_E2A.json::n}} | FILE_MISSING |
| verdict | {{confirm_verdict_E2A.json::verdict}} | FILE_MISSING |

### §5.4 E2-B replication, union and heterogeneity

| quantity | value (shell) | resolution |
|-|-|-|
| E2-B long-pool Δ [CI] | {{confirm_verdict_E2B.json::longpool.delta_strat_flashlite_disg.ci}} | FILE_MISSING |
| union long-pool Δ [CI] | {{union_longpool.json::union.delta_strat_flashlite_disg.ci}} | FILE_MISSING |
| between-sample heterogeneity | {{union_longpool.json::heterogeneity}} | FILE_MISSING |
| cost-matched judge Δ | {{confirm_verdict_E2B.json::costmatched.delta}} | FILE_MISSING |
| frontier ratio [CI], 300-row subsample | {{confirm_verdict_E2B.json::frontier.ratio.ci}} | FILE_MISSING |

### §5.5 R_COMP FREE, criterion (c)

| quantity | value (shell) | resolution |
|-|-|-|
| gloss gate balanced accuracy | {{confirm_verdict_rcomp.json::gloss_gate.balanced_accuracy}} | FIELD_MISSING (proposed name; resolve at paper time) |
| CORRECT / ERROR rows (untouched) | {{confirm_verdict_rcomp.json::labels.counts_untouched}} | FIELD_MISSING (proposed name; resolve at paper time) |
| within-template Δ vs flash-lite disguised [CI] | {{confirm_verdict_rcomp.json::criterion_c.disg.ci}} | FIELD_MISSING (proposed name; resolve at paper time) |
| within-template Δ vs flash-lite original [CI] | {{confirm_verdict_rcomp.json::criterion_c.orig.ci}} | FIELD_MISSING (proposed name; resolve at paper time) |
| with/without out-of-family form classes | {{confirm_verdict_rcomp.json::sensitivity.excl_out_of_family}} | FIELD_MISSING (proposed name; resolve at paper time) |
| verdict | {{confirm_verdict_rcomp.json::verdict}} | FIELD_MISSING (proposed name; resolve at paper time) |

### §5.6 H-MECH (i)–(iv) on E2 labels

| quantity | value (shell) | resolution |
|-|-|-|
| (i) share of non-agreeing peers of CORRECT labelled ERROR | {{hmech_E2.json::i.share_peer_error}} | FILE_MISSING |
| (ii) SCATTER ratio | {{hmech_E2.json::ii.scatter_ratio}} | FILE_MISSING |
| (iii) NET Δ(e+d) [CI] | {{hmech_E2.json::iii.net_delta.ci}} | FILE_MISSING |
| (iv) exact vs ALIGN d and e (MR-type, ADD/DROP) | {{hmech_E2.json::iv.align_vs_exact}} | FILE_MISSING |

### §5.7 H-IMPROVE (dev screen → frozen → E2)

| quantity | value (shell) | resolution |
|-|-|-|
| variants screened / winner or NONE | "NONE: V0 stands" (from `../../experiment-14/src/freeze/selection.json`) | FIELD_PRESENT; FILLED (seal present) |
| screen table (E long pool, L25, CTRL) | {"ALL-strat": {"V0_rep": {"delta": -0.0002918956959380159, "ci": [-0.000915901954164422, 0.0], "se": 0.00026602165526958 (from `../../experiment-14/src/results/screen_E.json`) | FIELD_PRESENT; FILLED (seal present) |
| winner − V0 on E2 long pool [CI] | {{improve_E2.json::delta_vs_V0.ci}} | FILE_MISSING |

### §5.8 H-RENAME / GG

| quantity | value (shell) | resolution |
|-|-|-|
| GG dev gate PASS/FAIL (gloss model id, prompt sha) | "FAIL(g3)" (from `../../experiment-14/src/freeze/gg_gate.json`) | FIELD_PRESENT; FILLED (seal present) |
| RENAME_SYN paired flip on E2 CORRECT | {{rename_E2.json::RENAME_SYN.flip}} | FILE_MISSING |
| c_score_align rename FA and flip on E2 | {{rename_E2.json::c_score_align}} | FILE_MISSING |

### §5.9 Complexity, coverage, cost, system-level τ-b

| quantity | value (shell) | resolution |
|-|-|-|
| d / e slopes over words and conditions | {{confirm_verdict_E2A.json::complexity}} | FILE_MISSING |
| coverage (unparseables in denominator) | {{confirm_verdict_E2A.json::coverage}} | FILE_MISSING |
| $ and seconds per candidate, FULL vs MARGINAL | {{confirm_verdict_E2A.json::cost}} | FILE_MISSING |
| system-level τ-b (13 system × variant rows) | {{confirm_verdict_E2A.json::system_level.tau_b}} | FILE_MISSING |

### §5.10 Verdict table

| quantity | value (shell) | resolution |
|-|-|-|
| H-PRIMARY | {{confirm_verdict_E2A.json::verdict}} | FILE_MISSING |
| criterion (c) | {{confirm_verdict_rcomp.json::verdict}} | FIELD_MISSING (proposed name; resolve at paper time) |
| H-MECH (i)–(iv) | {{hmech_E2.json::verdicts}} | FILE_MISSING |
| H-IMPROVE | {{improve_E2.json::verdict}} | FILE_MISSING |
| H-RENAME | {{rename_E2.json::verdict}} | FILE_MISSING |

Resolution of every shell cell: `skeleton_resolution.json` (globbed `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/*/`; this artifact's own workspace excluded). A value is filled only if the file exists AND its seal marker exists; otherwise the `{{…}}` placeholder stays.
