# R_ADJ card: a gated, reference-aware frontier adjudicator label regime for NL→FOL faithfulness

run_u75jRHUss0zo · invention iteration 2 · `gen_art_dataset_2`. The rows are dataset E (iteration 1, `art_U4Hsqt4Ay9Tg`) and the iteration-1 screen, joined by the UNCHANGED `item_id`.

**R_ADJ DROPPED: both adjudicators FAILED the pre-registered gate.** Following the fallback ladder, dataset E was NOT relabelled as a regime. Design cell D was dual-labelled (primary + Grok) as fold `E_dual_ungated`, output `UNGATED`, and is descriptive only. The screen was not adjudicated.

## Status and incidents
- 2026-09-23 18:00:18 UTC: the shared OpenRouter key hit its $50/day limit (other runs share it) while the gate half and the Grok calibration pass were running. 36/134 gate calls and 259/269 Grok calls returned HTTP 403. A report produced at that moment counted those failures as wrong answers. It is VOID: it is logged as `step4_gate_scored_VOID` in prereg_radj.json and kept only as `work/gate_report_VOID_key_outage.json`. The prompt, items and thresholds were not changed. Failed calls are re-sent (answered ones come from the cache) only when the key has budget again, and the gate is scored only on complete runs. `src/gate.py report` refuses to score while any infrastructure failure remains.
- 2026-09-23 21:45 UTC: a contingency version was submitted with the key still at $0. That version is superseded by this card. Its projection was 'gate pass very unlikely, R_ADJ likely dropped', and the scored gate below confirms it.
- 2026-09-24 00:01 UTC: the shared key reset. The platform now routes calls through a local proxy (`$OPENROUTER_API_BASE`, which `src/or_client.py` honours) whose upstream is the same shared key. `src/watch_and_run.sh` ran `run_all.sh` to completion by 00:12 UTC. Answered calls came from the cache, and only the calls that had returned HTTP 403 were re-sent. The gate was scored on complete runs (0 infrastructure failures) at 00:03:43 UTC, logged as `step4_gate_scored`. Both models FAIL, so the pre-registered ladder applied: cell D was dual-labelled, the retest ran, and the screen and the other E cells were not adjudicated. Total spend is $3.66 of the $9.50 hard stop.

## 1. What this is
- **Adjudicator input**: exactly {sentence, candidate FOL, reference FOL, VERIFIED/UNVERIFIED tag}. It never sees a metric score, a panel vote, the solver label or the repair ops. No disguise and no reasoning trace.
- **Primary**: `anthropic/claude-sonnet-5` with params `{"temperature": 0.0, "max_tokens": 300, "reasoning": {"enabled": false}}` (returned id ['anthropic/claude-sonnet-5']; pilot $0.002761/call). **Grok check**: `x-ai/grok-4.20` with params `{"temperature": 0.0, "max_tokens": 300, "reasoning": {"enabled": false}}` (pilot $0.000851/call).
- Both are family-disjoint from the 9 generator families and the metric judges. **Caveat**: the primary is Anthropic, the same family as panel member Haiku-4.5 (P1), which voted in R_AB and co-wrote PANEL_REPAIRED references (T11 measures this).
- Prompt: `adjudication_prompt.txt`, sha256 `32bcc0f9a0cd35dbd3ec6a4f7726f8094bca3a7785f2e9f0fbe509df7cbb3011` (the variant chosen on dev, see T1). V2 is `adjudication_prompt_v2.txt`. Both were frozen before any calibration call.
- Step-1 pilot (10 dev items, V1, temperature 0, max_tokens 300): `sonnet5_off` parse 10/10, $0.002761/call, tokens in/out/reasoning 1098.4/56.4/0; `sonnet5_low` parse 1/1, $0.002604/call, tokens in/out/reasoning 1112/38/0; `sonnet46_off` parse 10/10, $0.004158/call, tokens in/out/reasoning 764.8/78.3/0; `grok43_off` parse 10/10, $0.000975/call, tokens in/out/reasoning 824.4/31.4/0; `grok420_off` parse 10/10, $0.000851/call, tokens in/out/reasoning 824.4/30.2/0; `grok47_off` parse 0/1, $0.0/call, tokens in/out/reasoning None/None/None; `grok47_low` parse 10/10, $0.004492/call, tokens in/out/reasoning 1897.1/703.5/674. Sonnet-5 accepted `reasoning.enabled=false` (0 reasoning tokens). Grok-4.7 rejects disabled reasoning (HTTP 400) and at effort=low cost $0.0045/call, over the $0.004 rule, so the Grok check model is the cheapest compliant one, grok-4.20. Note that the plan names grok-4.3 as the model that failed iteration 1's gate; grok-4.20 is a different model.

## 2. T1 — the gate (pre-registered; per-class recall with Wilson 95% CIs)
Gate rule (frozen in `prereg_radj.json` before any calibration call): on the **gate half** (unambiguous items), balanced accuracy ≥ 0.85 AND recall(faithful) ≥ 0.80 AND recall(unfaithful) ≥ 0.80. AMBIGUOUS_READING on an unambiguous item and a parse failure after one retry both count as WRONG. `robust_pass` = full-set Wilson lower bound on each class recall ≥ 0.75.

**Variant selection on the dev half** (primary model): V1 balanced accuracy 0.7303, V2 0.73. Rule: higher wins, and a tie within 0.01 goes to V1. **Chosen: V1.**

**Verdict: primary gate FAIL (robust_pass False); Grok gate FAIL (robust_pass False). Regime: `none_dual_ungated`.**

| model | half | subset | n | bal.acc | recall faithful | recall unfaithful | AMBIG rate; parse fails |
|---|---|---|---|---|---|---|---|
| sonnet-5 (primary) | gate | overall | 112 | 0.7668 | 0.825 [0.706, 0.902] (47/57) | 0.709 [0.579, 0.812] (39/55) | 0.036 [0.014, 0.088]; parse-fail 1 |
| sonnet-5 (primary) | gate | synthetic | 38 | 0.975 | 0.950 [0.764, 0.991] (19/20) | 1.000 [0.824, 1.000] (18/18) | 0.000 [0.000, 0.092]; parse-fail 0 |
| sonnet-5 (primary) | gate | STRICT | 10 | – | 0.900 [0.596, 0.982] (9/10) | – (0/0) | 0.000 [0.000, 0.278]; parse-fail 0 |
| sonnet-5 (primary) | gate | RENAME | 10 | – | 1.000 [0.723, 1.000] (10/10) | – (0/0) | 0.000 [0.000, 0.278]; parse-fail 0 |
| sonnet-5 (primary) | gate | TYPED_DOWN | 12 | – | – (0/0) | 1.000 [0.757, 1.000] (12/12) | 0.000 [0.000, 0.242]; parse-fail 0 |
| sonnet-5 (primary) | gate | TYPED_UP | 6 | – | – (0/0) | 1.000 [0.610, 1.000] (6/6) | 0.000 [0.000, 0.390]; parse-fail 0 |
| sonnet-5 (primary) | gate | H | 74 | 0.6622 | 0.757 [0.599, 0.866] (28/37) | 0.568 [0.409, 0.713] (21/37) | 0.054 [0.021, 0.131]; parse-fail 1 |
| sonnet-5 (primary) | gate | H-orig | 37 | – | – (0/0) | 0.568 [0.409, 0.713] (21/37) | 0.027 [0.005, 0.138]; parse-fail 0 |
| sonnet-5 (primary) | gate | H-corr | 37 | – | 0.757 [0.599, 0.866] (28/37) | – (0/0) | 0.081 [0.028, 0.213]; parse-fail 1 |
| sonnet-5 (primary) | dev (optimistic) | overall | 115 | 0.7303 | 0.741 [0.616, 0.837] (43/58) | 0.719 [0.592, 0.819] (41/57) | 0.043 [0.019, 0.098]; parse-fail 0 |
| sonnet-5 (primary) | dev (optimistic) | synthetic | 39 | 0.95 | 0.900 [0.699, 0.972] (18/20) | 1.000 [0.832, 1.000] (19/19) | 0.026 [0.004, 0.132]; parse-fail 0 |
| sonnet-5 (primary) | dev (optimistic) | STRICT | 10 | – | 1.000 [0.723, 1.000] (10/10) | – (0/0) | 0.000 [0.000, 0.278]; parse-fail 0 |
| sonnet-5 (primary) | dev (optimistic) | RENAME | 10 | – | 0.800 [0.490, 0.943] (8/10) | – (0/0) | 0.100 [0.018, 0.404]; parse-fail 0 |
| sonnet-5 (primary) | dev (optimistic) | TYPED_DOWN | 8 | – | – (0/0) | 1.000 [0.676, 1.000] (8/8) | 0.000 [0.000, 0.324]; parse-fail 0 |
| sonnet-5 (primary) | dev (optimistic) | TYPED_UP | 11 | – | – (0/0) | 1.000 [0.741, 1.000] (11/11) | 0.000 [0.000, 0.259]; parse-fail 0 |
| sonnet-5 (primary) | dev (optimistic) | H | 76 | 0.6184 | 0.658 [0.499, 0.788] (25/38) | 0.579 [0.422, 0.722] (22/38) | 0.053 [0.021, 0.128]; parse-fail 0 |
| sonnet-5 (primary) | dev (optimistic) | H-orig | 38 | – | – (0/0) | 0.579 [0.422, 0.722] (22/38) | 0.026 [0.005, 0.135]; parse-fail 0 |
| sonnet-5 (primary) | dev (optimistic) | H-corr | 38 | – | 0.658 [0.499, 0.788] (25/38) | – (0/0) | 0.079 [0.027, 0.208]; parse-fail 0 |
| sonnet-5 (primary) | all (optimistic) | overall | 227 | 0.7484 | 0.783 [0.699, 0.848] (90/115) | 0.714 [0.625, 0.790] (80/112) | 0.040 [0.021, 0.074]; parse-fail 1 |
| sonnet-5 (primary) | all (optimistic) | synthetic | 77 | 0.9625 | 0.925 [0.801, 0.974] (37/40) | 1.000 [0.906, 1.000] (37/37) | 0.013 [0.002, 0.070]; parse-fail 0 |
| sonnet-5 (primary) | all (optimistic) | STRICT | 20 | – | 0.950 [0.764, 0.991] (19/20) | – (0/0) | 0.000 [0.000, 0.161]; parse-fail 0 |
| sonnet-5 (primary) | all (optimistic) | RENAME | 20 | – | 0.900 [0.699, 0.972] (18/20) | – (0/0) | 0.050 [0.009, 0.236]; parse-fail 0 |
| sonnet-5 (primary) | all (optimistic) | TYPED_DOWN | 20 | – | – (0/0) | 1.000 [0.839, 1.000] (20/20) | 0.000 [0.000, 0.161]; parse-fail 0 |
| sonnet-5 (primary) | all (optimistic) | TYPED_UP | 17 | – | – (0/0) | 1.000 [0.816, 1.000] (17/17) | 0.000 [0.000, 0.184]; parse-fail 0 |
| sonnet-5 (primary) | all (optimistic) | H | 150 | 0.64 | 0.707 [0.596, 0.798] (53/75) | 0.573 [0.461, 0.679] (43/75) | 0.053 [0.027, 0.102]; parse-fail 1 |
| sonnet-5 (primary) | all (optimistic) | H-orig | 75 | – | – (0/0) | 0.573 [0.461, 0.679] (43/75) | 0.027 [0.007, 0.092]; parse-fail 0 |
| sonnet-5 (primary) | all (optimistic) | H-corr | 75 | – | 0.707 [0.596, 0.798] (53/75) | – (0/0) | 0.080 [0.037, 0.164]; parse-fail 1 |
| grok-4.20 (check) | gate | overall | 112 | 0.6343 | 0.614 [0.484, 0.729] (35/57) | 0.654 [0.522, 0.766] (36/55) | 0.000 [0.000, 0.033]; parse-fail 0 |
| grok-4.20 (check) | gate | synthetic | 38 | 0.8417 | 0.850 [0.640, 0.948] (17/20) | 0.833 [0.608, 0.942] (15/18) | 0.000 [0.000, 0.092]; parse-fail 0 |
| grok-4.20 (check) | gate | STRICT | 10 | – | 0.700 [0.397, 0.892] (7/10) | – (0/0) | 0.000 [0.000, 0.278]; parse-fail 0 |
| grok-4.20 (check) | gate | RENAME | 10 | – | 1.000 [0.723, 1.000] (10/10) | – (0/0) | 0.000 [0.000, 0.278]; parse-fail 0 |
| grok-4.20 (check) | gate | TYPED_DOWN | 12 | – | – (0/0) | 0.750 [0.468, 0.911] (9/12) | 0.000 [0.000, 0.242]; parse-fail 0 |
| grok-4.20 (check) | gate | TYPED_UP | 6 | – | – (0/0) | 1.000 [0.610, 1.000] (6/6) | 0.000 [0.000, 0.390]; parse-fail 0 |
| grok-4.20 (check) | gate | H | 74 | 0.527 | 0.486 [0.335, 0.641] (18/37) | 0.568 [0.409, 0.713] (21/37) | 0.000 [0.000, 0.049]; parse-fail 0 |
| grok-4.20 (check) | gate | H-orig | 37 | – | – (0/0) | 0.568 [0.409, 0.713] (21/37) | 0.000 [0.000, 0.094]; parse-fail 0 |
| grok-4.20 (check) | gate | H-corr | 37 | – | 0.486 [0.335, 0.641] (18/37) | – (0/0) | 0.000 [0.000, 0.094]; parse-fail 0 |
| grok-4.20 (check) | dev | overall | 115 | 0.6348 | 0.638 [0.509, 0.750] (37/58) | 0.632 [0.502, 0.745] (36/57) | 0.000 [0.000, 0.032]; parse-fail 0 |
| grok-4.20 (check) | dev | synthetic | 39 | 0.8211 | 0.800 [0.584, 0.919] (16/20) | 0.842 [0.624, 0.945] (16/19) | 0.000 [0.000, 0.090]; parse-fail 0 |
| grok-4.20 (check) | dev | STRICT | 10 | – | 0.800 [0.490, 0.943] (8/10) | – (0/0) | 0.000 [0.000, 0.278]; parse-fail 0 |
| grok-4.20 (check) | dev | RENAME | 10 | – | 0.800 [0.490, 0.943] (8/10) | – (0/0) | 0.000 [0.000, 0.278]; parse-fail 0 |
| grok-4.20 (check) | dev | TYPED_DOWN | 8 | – | – (0/0) | 0.875 [0.529, 0.978] (7/8) | 0.000 [0.000, 0.324]; parse-fail 0 |
| grok-4.20 (check) | dev | TYPED_UP | 11 | – | – (0/0) | 0.818 [0.523, 0.949] (9/11) | 0.000 [0.000, 0.259]; parse-fail 0 |
| grok-4.20 (check) | dev | H | 76 | 0.5395 | 0.553 [0.397, 0.699] (21/38) | 0.526 [0.373, 0.675] (20/38) | 0.000 [0.000, 0.048]; parse-fail 0 |
| grok-4.20 (check) | dev | H-orig | 38 | – | – (0/0) | 0.526 [0.373, 0.675] (20/38) | 0.000 [0.000, 0.092]; parse-fail 0 |
| grok-4.20 (check) | dev | H-corr | 38 | – | 0.553 [0.397, 0.699] (21/38) | – (0/0) | 0.000 [0.000, 0.092]; parse-fail 0 |
| grok-4.20 (check) | all | overall | 227 | 0.6345 | 0.626 [0.535, 0.709] (72/115) | 0.643 [0.551, 0.726] (72/112) | 0.000 [0.000, 0.017]; parse-fail 0 |
| grok-4.20 (check) | all | synthetic | 77 | 0.8314 | 0.825 [0.680, 0.912] (33/40) | 0.838 [0.689, 0.923] (31/37) | 0.000 [0.000, 0.048]; parse-fail 0 |
| grok-4.20 (check) | all | STRICT | 20 | – | 0.750 [0.531, 0.888] (15/20) | – (0/0) | 0.000 [0.000, 0.161]; parse-fail 0 |
| grok-4.20 (check) | all | RENAME | 20 | – | 0.900 [0.699, 0.972] (18/20) | – (0/0) | 0.000 [0.000, 0.161]; parse-fail 0 |
| grok-4.20 (check) | all | TYPED_DOWN | 20 | – | – (0/0) | 0.800 [0.584, 0.919] (16/20) | 0.000 [0.000, 0.161]; parse-fail 0 |
| grok-4.20 (check) | all | TYPED_UP | 17 | – | – (0/0) | 0.882 [0.657, 0.967] (15/17) | 0.000 [0.000, 0.184]; parse-fail 0 |
| grok-4.20 (check) | all | H | 150 | 0.5333 | 0.520 [0.409, 0.629] (39/75) | 0.547 [0.434, 0.654] (41/75) | 0.000 [0.000, 0.025]; parse-fail 0 |
| grok-4.20 (check) | all | H-orig | 75 | – | – (0/0) | 0.547 [0.434, 0.654] (41/75) | 0.000 [0.000, 0.049]; parse-fail 0 |
| grok-4.20 (check) | all | H-corr | 75 | – | 0.520 [0.409, 0.629] (39/75) | – (0/0) | 0.000 [0.000, 0.049]; parse-fail 0 |

Diagnostics (primary; Grok in brackets):
- reference_wrong recall on H-corr items (the reference is the expert-REJECTED original, tagged UNVERIFIED): unambiguous 0.387 [0.285, 0.500] [0.680 [0.568, 0.775]]; all 0.385 [0.294, 0.485].
- reference_wrong raised on VERIFIED references (should be ~0): 0.013 [0.004, 0.047].
- Op identification on H-orig items the adjudicator flagged UNFAITHFUL, against the census operator class (typed-op census items only): any-overlap 0.360 [0.203, 0.555], exact-set 0.160 [0.064, 0.346] (n=25 of 35). VOCAB-census items flagged UNFAITHFUL with MEANING_RENAME: 1.000 [0.206, 1.000].
  Iteration-1 panel members on the same items (their own `orig_ops`, same scoring): P1 any-overlap 0.533 [0.361, 0.698], exact 0.133 [0.053, 0.297]; P3 any-overlap 0.500 [0.314, 0.686], exact 0.125 [0.043, 0.310]; R1 any-overlap 0.609 [0.408, 0.778], exact 0.043 [0.008, 0.210].
- The 42 curator-ambiguous items (excluded from the gate): accuracy vs the curator's direction 0.643 [0.492, 0.770], AMBIGUOUS_READING rate 0.024 [0.004, 0.123]; verdicts `H-corr|FAITHFUL` 14, `H-orig|UNFAITHFUL` 13, `H-orig|FAITHFUL` 8, `H-corr|UNFAITHFUL` 5, `H-corr|AMBIGUOUS_READING` 1, `H-corr|None` 1.

## 3. T3 — Sonnet vs Grok (family-independence check)
- Calibration, all 269: Cohen κ(verdict) = 0.4974, raw agreement 0.7361; unambiguous 227: κ = 0.5112, raw 0.7445.
- Verdict matrix (Sonnet|Grok), all items: `FAITHFUL|FAITHFUL` 102, `UNFAITHFUL|UNFAITHFUL` 96, `FAITHFUL|UNFAITHFUL` 40, `UNFAITHFUL|FAITHFUL` 19, `AMBIGUOUS_READING|FAITHFUL` 6, `AMBIGUOUS_READING|UNFAITHFUL` 4, `PARSE_FAIL|UNFAITHFUL` 2.
- By gold class: **UNFAITHFUL**: `UNFAITHFUL|UNFAITHFUL` 66, `FAITHFUL|FAITHFUL` 25, `UNFAITHFUL|FAITHFUL` 14, `FAITHFUL|UNFAITHFUL` 5, `AMBIGUOUS_READING|UNFAITHFUL` 1, `AMBIGUOUS_READING|FAITHFUL` 1; **FAITHFUL**: `FAITHFUL|FAITHFUL` 64, `FAITHFUL|UNFAITHFUL` 26, `UNFAITHFUL|UNFAITHFUL` 14, `AMBIGUOUS_READING|FAITHFUL` 5, `UNFAITHFUL|FAITHFUL` 3, `AMBIGUOUS_READING|UNFAITHFUL` 2, `None|UNFAITHFUL` 1; **UNFAITHFUL_amb**: `UNFAITHFUL|UNFAITHFUL` 11, `FAITHFUL|FAITHFUL` 5, `FAITHFUL|UNFAITHFUL` 3, `UNFAITHFUL|FAITHFUL` 2; **FAITHFUL_amb**: `FAITHFUL|FAITHFUL` 8, `FAITHFUL|UNFAITHFUL` 6, `UNFAITHFUL|UNFAITHFUL` 5, `AMBIGUOUS_READING|UNFAITHFUL` 1, `None|UNFAITHFUL` 1
- On real E rows (cell D, 520 rows): κ = 0.4162, raw agreement 0.8269; matrix `FAITHFUL|FAITHFUL` 391, `FAITHFUL|UNFAITHFUL` 57, `UNFAITHFUL|UNFAITHFUL` 39, `UNFAITHFUL|FAITHFUL` 17, `AMBIGUOUS_READING|UNFAITHFUL` 13, `AMBIGUOUS_READING|FAITHFUL` 3.

## 4. T2 — test-retest (primary, cache bypassed)
- calibration: n=50, flip rate 0.100 [0.043, 0.214], κ(first, retest) = 0.8117
- E: n=50, flip rate 0.040 [0.011, 0.135], κ(first, retest) = 0.8113
- ALL: n=100, flip rate 0.070 [0.034, 0.138], κ(first, retest) = 0.8344

## 5. The E sampling design (frozen before any E call)
- Frame: dataset E heldout_candidates, system_class == llm, final_label != UNPARSEABLE: **6838 rows**. 1062 LLM rows are UNPARSEABLE, ERROR by rule and never adjudicated. PANEL_REPAIRED reference check: 0 substitutions were needed (every row already carries the repaired formula).
- `sampling_frame.json` sha256 `7ad39a339eb4e37c660bc23393f5673acc1c9f8141832faa3792628835b741b4` (logged 2026-09-23T18:02:27Z).
- Cells, first match, in this order: D (trusted ref, panel majority exists, solver binary ≠ panel majority, CONTESTED included) → U (UNRESOLVED, or trusted ref without a panel majority) → B (tier B agreeing) → L (L25 tier A agreeing) → A (tier A L20/EXC/CTRL agreeing) → C (everything else, reference UNVERIFIED). Cell sizes {'A': 578, 'B': 1343, 'C': 3681, 'U': 450, 'L': 116, 'D': 670}; targets {'D': 610, 'U': 40, 'B': 150, 'L': 100, 'A': 150, 'C': 150} (D trimmed from min(670, 640) to keep the total ≤ 1,200); 1200 selected, 1070 calls after dedupe.
- Design units (N_h → n_h): `A|CTRL|error` 10→3, `A|CTRL|faithful` 186→44, `A|EXC|error` 120→35, `A|EXC|faithful` 97→23, `A|L20|error` 129→37, `A|L20|faithful` 36→8, `B|CTRL|-` 75→8, `B|EXC|-` 239→27, `B|L20|-` 445→50, `B|L25|-` 584→65, `C|CTRL|-` 883→36, `C|EXC|-` 437→18, `C|L20|-` 774→31, `C|L25|-` 1587→65, `D|CTRL|-` 61→55, `D|EXC|-` 170→155, `D|L20|-` 239→218, `D|L25|-` 200→182, `L|L25|-` 116→100, `U|CTRL|-` 344→31, `U|EXC|-` 46→4, `U|L20|-` 20→2, `U|L25|-` 40→3
- U is dominated by CTRL rows whose auto-ERROR classes were never shown to the panel (iteration-1 CTRL reduced scope), so it has no majority. That is also why cell A has only 10 CTRL solver-error rows.
- Budget plan before E: `{"regime": "none_dual_ungated", "spent_before": 1.5493, "available": 7.7007, "cost_per_call_primary_est": 0.00392, "cost_per_call_grok_est": 0.00056, "E_dual_cell_D_calls": 529, "proj_dual": 2.368, "proj_retest": 0.392, "cell_caps": {"D": 529}, "screen": false, "grokE": false, "proj_total_after": 4.309}`
- **Labelled**: 601 / 1200 selected rows (per cell labelled {'D': 601} of {'D': 610, 'A': 150, 'L': 100, 'B': 150, 'C': 150, 'U': 40}); dedupe rows reusing a label: 130; label distribution {'CORRECT': 522, 'ERROR': 62, 'AMBIGUOUS_READING': 17}. Unlabelled selected rows stay in the file with output `NOT_LABELLED`, and the realised inclusion_prob = n_labelled_h/N_h.

## 6. T4 — solver binary × panel majority × UNGATED primary labels (descriptive only, NOT a regime)
Key `solver|panel|adjudicator`, counts of labelled rows.
- **cell D**: `error|faithful|CORRECT` 277, `faithful|error|CORRECT` 245, `error|faithful|ERROR` 52, `error|faithful|AMBIGUOUS_READING` 17, `faithful|error|ERROR` 10
- **stratum L25**: `error|faithful|CORRECT` 85, `faithful|error|CORRECT` 65, `error|faithful|ERROR` 19, `error|faithful|AMBIGUOUS_READING` 7, `faithful|error|ERROR` 3
- **ALL**: `error|faithful|CORRECT` 277, `faithful|error|CORRECT` 245, `error|faithful|ERROR` 52, `error|faithful|AMBIGUOUS_READING` 17, `faithful|error|ERROR` 10
- **stratum L20**: `error|faithful|CORRECT` 108, `faithful|error|CORRECT` 90, `error|faithful|ERROR` 13, `error|faithful|AMBIGUOUS_READING` 5, `faithful|error|ERROR` 1
- **stratum EXC**: `faithful|error|CORRECT` 65, `error|faithful|CORRECT` 57, `error|faithful|ERROR` 19, `faithful|error|ERROR` 6, `error|faithful|AMBIGUOUS_READING` 3
- **stratum CTRL**: `error|faithful|CORRECT` 27, `faithful|error|CORRECT` 25, `error|faithful|AMBIGUOUS_READING` 2, `error|faithful|ERROR` 1

**Who does the adjudicator side with in cell D?** (rows where solver and panel disagree, AMBIGUOUS excluded; share siding with the panel, Wilson CI)
- L25: solver 84, panel 88 → panel share 0.512 [0.438, 0.585]
- ALL: solver 297, panel 287 → panel share 0.491 [0.451, 0.532]
- D-type solver=COMPOUND/panel=faithful: solver 30, panel 174 → panel share 0.853 [0.798, 0.895]
- L20: solver 103, panel 109 → panel share 0.514 [0.447, 0.581]
- D-type solver=ERROR/panel=faithful: solver 22, panel 103 → panel share 0.824 [0.748, 0.881]
- EXC: solver 84, panel 63 → panel share 0.429 [0.351, 0.509]
- D-type solver=VOCAB_GRAN/panel=error: solver 195, panel 8 → panel share 0.039 [0.020, 0.076]
- CTRL: solver 26, panel 27 → panel share 0.509 [0.379, 0.639]
- D-type solver=CORRECT/panel=error: solver 50, panel 2 → panel share 0.038 [0.011, 0.130]

**Two-model characterisation of cell D** (primary and Grok, both on every row): n, both models agree, and when they agree, how often they side with the solver or the panel.
- solver=error/panel=faithful: {'n': 346, 'models_agree': 274, 'agree_with_solver': 35, 'agree_with_panel': 239}
- solver=faithful/panel=error: {'n': 255, 'models_agree': 233, 'agree_with_solver': 225, 'agree_with_panel': 8}

## 7. T5 — label transitions R_AB → UNGATED primary labels (descriptive only, NOT a regime)
- **ALL**: `CORRECT->CORRECT` 224, `ERROR->CORRECT` 195, `CONTESTED->CORRECT` 103, `CORRECT->ERROR` 32, `CONTESTED->ERROR` 22, `CORRECT->AMBIGUOUS_READING` 11, `ERROR->ERROR` 8, `CONTESTED->AMBIGUOUS_READING` 6
- **stratum CTRL**: `ERROR->CORRECT` 25, `CONTESTED->CORRECT` 24, `CORRECT->CORRECT` 3, `CONTESTED->AMBIGUOUS_READING` 2, `CONTESTED->ERROR` 1
- **stratum EXC**: `CORRECT->CORRECT` 51, `ERROR->CORRECT` 49, `CONTESTED->CORRECT` 22, `CORRECT->ERROR` 11, `CONTESTED->ERROR` 9, `ERROR->ERROR` 5, `CONTESTED->AMBIGUOUS_READING` 2, `CORRECT->AMBIGUOUS_READING` 1
- **stratum L20**: `CORRECT->CORRECT` 96, `ERROR->CORRECT` 70, `CONTESTED->CORRECT` 32, `CORRECT->ERROR` 9, `CONTESTED->ERROR` 5, `CORRECT->AMBIGUOUS_READING` 4, `CONTESTED->AMBIGUOUS_READING` 1
- **stratum L25**: `CORRECT->CORRECT` 74, `ERROR->CORRECT` 51, `CONTESTED->CORRECT` 25, `CORRECT->ERROR` 12, `CONTESTED->ERROR` 7, `CORRECT->AMBIGUOUS_READING` 6, `ERROR->ERROR` 3, `CONTESTED->AMBIGUOUS_READING` 1
- **cell D**: `CORRECT->CORRECT` 224, `ERROR->CORRECT` 195, `CONTESTED->CORRECT` 103, `CORRECT->ERROR` 32, `CONTESTED->ERROR` 22, `CORRECT->AMBIGUOUS_READING` 11, `ERROR->ERROR` 8, `CONTESTED->AMBIGUOUS_READING` 6
- **system F:openai/gpt-5.1|fewshot_v1**: `ERROR->CORRECT` 9, `CORRECT->CORRECT` 8, `CONTESTED->CORRECT` 5, `CORRECT->AMBIGUOUS_READING` 1
- **system G1:meta-llama/llama-3.1-8b-instruct|fewshot_v1**: `ERROR->CORRECT` 13, `CONTESTED->CORRECT` 5, `CORRECT->CORRECT` 5, `CORRECT->ERROR` 2, `CONTESTED->ERROR` 1, `ERROR->ERROR` 1
- **system G1b:meta-llama/llama-3.3-70b-instruct|fewshot_v1**: `ERROR->CORRECT` 16, `CORRECT->CORRECT` 11, `CONTESTED->CORRECT` 6, `ERROR->ERROR` 3, `CORRECT->ERROR` 2, `CONTESTED->ERROR` 1, `CORRECT->AMBIGUOUS_READING` 1
- **system G1b:meta-llama/llama-3.3-70b-instruct|zeroshot_v1**: `ERROR->CORRECT` 13, `CORRECT->ERROR` 4, `CORRECT->CORRECT` 3, `CONTESTED->CORRECT` 2, `ERROR->ERROR` 1, `CONTESTED->AMBIGUOUS_READING` 1, `CONTESTED->ERROR` 1
- **system G2:qwen/qwen3-235b-a22b-2507|fewshot_v1**: `CORRECT->CORRECT` 25, `ERROR->CORRECT` 17, `CONTESTED->CORRECT` 7, `CONTESTED->ERROR` 2, `CORRECT->AMBIGUOUS_READING` 2, `CONTESTED->AMBIGUOUS_READING` 2, `CORRECT->ERROR` 2
- **system G2:qwen/qwen3-235b-a22b-2507|zeroshot_v1**: `ERROR->CORRECT` 21, `CORRECT->CORRECT` 18, `CONTESTED->CORRECT` 6, `CONTESTED->ERROR` 3, `CONTESTED->AMBIGUOUS_READING` 1, `CORRECT->AMBIGUOUS_READING` 1, `CORRECT->ERROR` 1
- **system G3:mistralai/mistral-small-3.2-24b-instruct|fewshot_v1**: `CORRECT->CORRECT` 26, `ERROR->CORRECT` 17, `CONTESTED->CORRECT` 16, `CORRECT->ERROR` 4, `CONTESTED->ERROR` 2
- **system G4:deepseek/deepseek-v3.2|fewshot_v1**: `CORRECT->CORRECT` 39, `ERROR->CORRECT` 14, `CONTESTED->CORRECT` 10, `CORRECT->AMBIGUOUS_READING` 3, `CORRECT->ERROR` 3, `CONTESTED->ERROR` 2
- **system G5:google/gemma-3-27b-it|fewshot_v1**: `ERROR->CORRECT` 13, `CORRECT->CORRECT` 13, `CONTESTED->CORRECT` 7, `CORRECT->ERROR` 2, `CONTESTED->ERROR` 1
- **system G6:microsoft/phi-4|fewshot_v1**: `CORRECT->CORRECT` 25, `ERROR->CORRECT` 21, `CONTESTED->CORRECT` 10, `CORRECT->ERROR` 4, `ERROR->ERROR` 2, `CORRECT->AMBIGUOUS_READING` 1
- **system G7:openai/gpt-4.1-mini|fewshot_v1**: `CORRECT->CORRECT` 31, `ERROR->CORRECT` 16, `CONTESTED->CORRECT` 13, `CORRECT->ERROR` 4, `ERROR->ERROR` 1, `CORRECT->AMBIGUOUS_READING` 1, `CONTESTED->AMBIGUOUS_READING` 1, `CONTESTED->ERROR` 1
- **system G8:google/gemini-2.5-flash|fewshot_v1**: `ERROR->CORRECT` 15, `CORRECT->CORRECT` 14, `CONTESTED->CORRECT` 12, `CONTESTED->ERROR` 8, `CORRECT->ERROR` 4, `CONTESTED->AMBIGUOUS_READING` 1, `CORRECT->AMBIGUOUS_READING` 1
- **system G9:cohere/command-r7b-12-2024|fewshot_v1**: `ERROR->CORRECT` 10, `CORRECT->CORRECT` 6, `CONTESTED->CORRECT` 4

## 8. T6 — correct-but-not-equivalent rate, UNGATED primary labels (descriptive only, NOT a regime) vs R_AB
Rows not plain-z3-equivalent to the reference (auto label ≠ CORRECT), R_AB-decided (tier A/B, CORRECT/ERROR); share judged CORRECT. IPW over the frame with a sentence-clustered bootstrap (2,000). Iteration-1 published R_AB values: L25 0.163, L20 0.218, EXC 0.203, CTRL 0.255.
| stratum | adjudicator IPW | R_AB IPW, same rows | adjudicator unweighted | AMBIGUOUS share |
|---|---|---|---|---|
| L25 | 0.881 [0.807, 0.942] (n=126, sents=60) | 0.591 [0.453, 0.725] (n=132, sents=62) | 0.881 [0.807, 0.942] (n=126, sents=60) | 0.045 [0.021, 0.096] |
| L20 | 0.948 [0.890, 0.993] (n=154, sents=53) | 0.557 [0.422, 0.688] (n=158, sents=54) | 0.948 [0.890, 0.993] (n=154, sents=53) | 0.025 [0.010, 0.063] |
| EXC | 0.849 [0.739, 0.931] (n=99, sents=33) | 0.460 [0.292, 0.629] (n=100, sents=33) | 0.849 [0.739, 0.931] (n=99, sents=33) | 0.010 [0.002, 0.054] |
| CTRL | 1.000 [1.000, 1.000] (n=28, sents=8) | 0.107 [0.020, 0.312] (n=28, sents=8) | 1.000 [1.000, 1.000] (n=28, sents=8) | 0.000 [0.000, 0.121] |
| ALL | 0.906 [0.865, 0.941] (n=407, sents=154) | 0.514 [0.426, 0.602] (n=418, sents=157) | 0.907 [0.865, 0.942] (n=407, sents=154) | 0.026 [0.015, 0.046] |

Pooled CORRECT share (IPW vs unweighted): L25: 0.838 [0.749, 0.913] (n=179, sents=74) vs 0.838 [0.749, 0.913] (n=179, sents=74); L20: 0.912 [0.845, 0.962] (n=217, sents=65) vs 0.912 [0.845, 0.962] (n=217, sents=65); EXC: 0.813 [0.714, 0.892] (n=150, sents=43) vs 0.813 [0.714, 0.892] (n=150, sents=43); CTRL: 0.946 [0.867, 1.000] (n=55, sents=11) vs 0.946 [0.867, 1.000] (n=55, sents=11); ALL: 0.868 [0.826, 0.905] (n=601, sents=193) vs 0.869 [0.826, 0.906] (n=601, sents=193)

## 9. T7 — reference_wrong
Sentence level (a reference counts as wrong if most adjudicated rows of its sentence set reference_wrong). On VERIFIED (trusted) references the prompt only asks for a check when the tag is UNVERIFIED, so there it is a LOWER bound. Iteration-1 panel: 0.822 of MALLS gold judged wrong.
- ALL: 0.000 [0.000, 0.019]
- status GOLD_PANEL_OK: 0.000 [0.000, 0.057]
- status PANEL_REPAIRED: 0.000 [0.000, 0.032]
- status TRUSTED_AGREED: 0.000 [0.000, 0.259]
- stratum CTRL: 0.000 [0.000, 0.259]
- stratum EXC: 0.000 [0.000, 0.082]
- stratum L20: 0.000 [0.000, 0.056]
- stratum L25: 0.000 [0.000, 0.049]
- tag VERIFIED: 0.000 [0.000, 0.019]
- Row level by reference_status: GOLD_PANEL_OK 0.016 [0.005, 0.046]; PANEL_REPAIRED 0.008 [0.003, 0.024]; TRUSTED_AGREED 0.000 [0.000, 0.065]

## 10. T8 — error-type census
UNGATED primary labels (descriptive only, NOT a regime) ERROR rows: 62; with ≥1 op: 62. Share of those rows containing ≥1 op of each class (IPW and unweighted, sentence-clustered bootstrap).
| class | IPW | unweighted |
|---|---|---|
| polarity | 0.129 [0.048, 0.246] (n=62, sents=44) | 0.129 [0.048, 0.245] (n=62, sents=44) |
| coverage | 0.307 [0.165, 0.461] (n=62, sents=44) | 0.306 [0.164, 0.462] (n=62, sents=44) |
| structural | 0.645 [0.500, 0.781] (n=62, sents=44) | 0.645 [0.500, 0.780] (n=62, sents=44) |
| MEANING_RENAME | 0.194 [0.067, 0.339] (n=62, sents=44) | 0.194 [0.068, 0.339] (n=62, sents=44) |
Pre-registered predictions: polarity ≤ 0.20 → True; coverage ≥ 0.40 → False. Op mass: `CONN` 26, `RESTR` 13, `MEANING_RENAME` 12, `DROP` 11, `ADD` 9, `NEG` 5, `QUANT` 3, `SCOPE` 2.

## 12. T11 — self-preference diagnostics
- Adjudicator agreement with each panel member's vote on shared rows: Haiku P1 0.390 [0.327, 0.457], GLM P3 0.509 [0.468, 0.549], Kimi R1 0.537 [0.495, 0.579]. A clearly higher agreement with P1 would suggest same-family correlation; note that P1 votes only on items where GLM and Kimi disagreed, so its items are harder.
- reference_wrong on PANEL_REPAIRED references 0.008 [0.003, 0.024] vs GOLD_PANEL_OK 0.016 [0.005, 0.046] (both tagged VERIFIED).

## 14. T12 — cost
| phase | calls | USD | prompt tokens | completion tokens |
|---|---|---|---|---|
| pilot | 52 | 0.135 | 56001 | 9336 |
| gate_primary | 409 | 1.2884 | 480082 | 32828 |
| gate_grok | 259 | 0.1259 | 214351 | 9564 |
| E_dual_primary | 542 | 1.5941 | 646217 | 30171 |
| E_dual_grok_check | 529 | 0.2361 | 458151 | 17089 |
| retest | 100 | 0.2804 | 112879 | 5467 |
Total **$3.6601** (hard stop $9.50; artifact budget $10). Seconds per item are in `metadata_adj_seconds`.

## 15. Departures, limits and how to use this
- NO NEW HUMAN ANNOTATION. The only human anchor is the 96 expert-corrected FOLIO/MALLS pairs (DSAVlab-UNIUD, arXiv 2606.02837), which are short curated items. The gate says nothing about adjudicator accuracy on long, heavily conditioned sentences: **accuracy on L25 is untested.**
- SAME FAMILY AS PANEL MEMBER P1 (Haiku-4.5, Anthropic). It is measured in T11, not assumed away.
- REFERENCE-AWARE, NOT BLIND. The adjudicator may anchor on the reference. The H-corr items (a correct candidate against a wrong UNVERIFIED reference) test this directly, together with reference_wrong recall.
- NOT DISGUISED. Memorised FOLIO/MALLS gold could help the adjudicator. Most E references are panel-repaired or rejected MALLS gold rather than public gold, but contamination is NOT measured here.
- GATE POWER. Per-class recall on the gate half rests on 55-57 items (Wilson half-width about ±0.1). A pass without robust_pass is a weaker regime.
- The track-H 'gold' is the curators' correction direction. The iteration-1 panel accepted only 0.613 of the corrected formulas, and the curators flag 21/96 pairs as ambiguous. Some unambiguous corrections are also contestable (e.g. constant `taxHaven` vs ∃x TaxHaven(x) for 'a tax haven'; `largerFamily` vs `largeFamily`). A failure on track H is therefore partly disagreement with a strict expert convention, not only adjudicator error. The gate was pre-registered with these items, and the thresholds were not changed after seeing them.
- A frontier adjudicator is a model, not ground truth. Where R_AB and the adjudicator disagree, this card presents the disagreement; it does not declare either one correct.
- Sampling: at most 1,200 of the 6,838 frame rows. Pooled E numbers must use IPW (weight 1/metadata_inclusion_prob). Per-system transitions are descriptive (small n per system).
- Pilot spend was $0.135 against the plan's $0.10 line, because a 1-call acceptance probe of 6 configs came before the 10-call pilot. It is covered by the hard stop.
- HF dataset search (TODO 2-4) was run for documentation: FOLIO (tasksource, yale-nlp), MALLS-v0, DSAVlab curated MALLS/FOLIO. All are already upstream of dataset E. The plan forbids new external data, since the task is to relabel THESE rows, so nothing new was downloaded. The HF preview tool failed in this environment (missing `datasets` module). Source provenance was verified in iteration 1 (`work/source_verification.json` of dataset E).
- UNGATED SCOPE. Only design cell D (rows where the solver binary and the panel majority disagree) is labelled: 601 of its 610 selected rows. Every E-level number in T4-T8 therefore describes cell D, NOT dataset E. IPW and unweighted estimates coincide because cell D is sampled almost as a census (inclusion probability 0.88-0.91 per unit). The 599 NOT_LABELLED rows in cells A/B/C/L/U keep the full design, but they were never sent under the fallback.
- 9 cell-D rows are NOT_LABELLED because of PARSE FAILURES that persisted after the one pre-registered retry: the model answered with prose analysis and no JSON verdict (the raw text is kept in `metadata_adj_raw`). They are not missing at random. All 9 discuss connective structure (scope, grouping or precedence; e.g. `(A∧B)∨C` vs `A∧(B∨C)`, `A→B→C`, `unless`), so the cell-D ERROR share is probably slightly understated. They were not re-queried with a larger max_tokens, because that would depart from the frozen protocol.

## 16. Files
- `data_out.json` sha256 `c2bdc2689418584c90833de634b0105e76f4312b9b3ee4bef99c9066874f0734`
- `full_data_out.json` sha256 `80e1b34d92166ef0cdf1d35b2c22eafdf7b3c82fcbcfb308702dcefebddbfcce`
- `adjudication_prompt.txt` sha256 `32bcc0f9a0cd35dbd3ec6a4f7726f8094bca3a7785f2e9f0fbe509df7cbb3011`
- `adjudication_prompt_v2.txt` sha256 `8806818fbb5fe262c62f4caf6edfb3a79e9b32b0ff1c6402b8f56414ab720766`
- `prereg_radj.json` sha256 `d360d962051186a36a9c72a84a0ffafdca538298075c2ea40269aae786538eed`
- `sampling_frame.json` sha256 `7ad39a339eb4e37c660bc23393f5673acc1c9f8141832faa3792628835b741b4`
- `calibration_split.json` sha256 `c5380f56dfd13db3c731448e2b0a0e03071f78eaf2d10e92151b748481115da6`
- `gate_report.json` sha256 `1d5d341b6521f35aa90f969d5c0d1178ca6edf99d95fb34dee33e371c2181121`
