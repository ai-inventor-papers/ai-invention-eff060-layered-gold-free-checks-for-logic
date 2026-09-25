# PEER+TEXT on held-out dataset E: peer agreement plus text checks for NL→FOL faithfulness

This is iteration 2, GEN_ART experiment 5 of run `run_u75jRHUss0zo`.

**What this does.** It scores gold-free NL→FOL faithfulness metrics. Each metric takes a sentence, a candidate FOL
formula and the other systems' formalisations of the same sentence, and returns a score for how likely the candidate is to
be unfaithful. Everything was frozen on the iteration-1 screen, sha256-registered (`results/prereg.json`,
sha256 `b9f28b1b…`, 18:23:50 UTC, git commit `a6896ce`), and then scored **once** on the 8,507 held-out rows of dataset E.
The metrics and the baselines run in one pipeline on identical rows.

- **PEER.** The candidate's claims (split into claim units) are checked against the peers from other model families, after
  aligning each peer's predicates to the candidate's. Entailment uses a sound finite-model refuter first and z3 second.
  - `support` is the share of the candidate's claims that the peers entail.
  - `coverage` is the share of the peers' majority claims that the candidate entails.
  - `g_score = 1 − F1(support, coverage)`.
  - Unsupported claims get a unit error code (NEG / QUANT / SWAP / ADD); uncovered majority claims get DROP.
- **TEXT.** The iteration-1 checks, vendored unchanged:
  - L2-bow: content-word accounting between the sentence and the predicate names.
  - L3: a small LLM answers a role questionnaire from the **text only**, and z3 answers the same questions exactly from the
    formula.
- **PEER+TEXT.** A logistic fusion fitted on the screen, using only items where the solver label and the adjudicated label
  agree (the AGREE set).

## Headline results (dataset E; 95% sentence-cluster bootstrap CIs, B=2000)

Primary label regime R_AB: LLM rows, label tiers A and B, decided labels only (CONTESTED and reading_choice excluded).
That is 2,686 rows: 1,822 ERROR and 864 CORRECT, over 700 sentences.

| metric | pooled R_AB | stratified R_AB* | long pool (L25+L20+EXC) | R_A (tier A) L20+EXC |
|---|---|---|---|---|
| **PEER+TEXT (frozen fusion)** | **0.790 [0.75, 0.82]** | **0.753** | **0.768 [0.74, 0.80]** | 0.818 [0.73, 0.88] |
| c_score_align (iteration-1 aligner consensus) | 0.782 [0.74, 0.82] | 0.741 | 0.759 | **0.860** [0.79, 0.92] |
| PEER alone (graded ALIGN g) | 0.748 | 0.694 | 0.705 | 0.812 |
| NF-anchored c_score (name-free consensus) | 0.743 | 0.686 | 0.704 | 0.802 |
| TEXT alone (L2-bow + L3) | 0.693 | 0.670 | 0.690 | 0.665 |
| L2-bow | 0.734 | — | 0.717 | 0.678 |
| L3 | 0.579 | — | 0.580 | 0.587 |
| local judge Qwen3-8B, disguised (secondary bar) | 0.712 | 0.677 | 0.653 | 0.554 |
| flash-lite judge, disguised (pre-registered bar) | untestable: 20 rows | | | |

\*Stratified AUROC counts only (error, correct) pairs within the same stratum. It is reported because the within-stratum
label-permutation placebo is 0.59, not 0.50: pooled AUROC partly rewards the fact that long strata have both more errors
and higher scores. The global-shuffle placebo is 0.50 for every metric.

- **ΔAUROC PEER+TEXT − local judge.**
  - Pooled R_AB: **+0.078 [0.043, 0.112]**. Stratified: +0.075 [0.036, 0.114].
  - Long pool: **+0.115 [0.075, 0.157]**.
  - R_A L20+EXC: +0.264 [0.157, 0.359].
  - Per stratum: L25 +0.092 [0.031, 0.151]; L20 +0.064 [−0.001, 0.129]; EXC +0.114 [0.033, 0.194]; CTRL −0.031 [−0.142, 0.089].
  - Sensitivities: CONTESTED→CORRECT +0.068 [0.034, 0.098]; CONTESTED→ERROR +0.078 [0.049, 0.109]; without the L25
    top-up +0.074 [0.040, 0.110].
- **Criteria.**
  - Against the pre-registered bar (flash-lite disguised), criteria (a) and (c) are **untestable**: the shared OpenRouter
    key hit its $50/day limit minutes after launch, with 20 judge units done.
  - Against the labelled secondary bar (the local Qwen3-8B judge, exp D's local bar, screen AUROC .757), criterion (a) is
    met: CI > 0 pooled R_AB and sign > 0 in R_A. Criterion (c)-long is also met: CI > 0 in the long pool.
- **The fusion does not add significant signal over the iteration-1 aligner consensus alone.**
  - PEER+TEXT − c_score_align, stratified: +0.011 [−0.012, 0.038].
  - On the solver-only tier A, c_score_align is higher: 0.860 vs 0.818.
  - The advantage over the judge is carried mainly by the aligner consensus. That aligner is **shared with the solver
    labeller**, so this confound stays open in this run.
- **Name-free alignment (the planned F1) did not pass the pre-registered gate on the screen.**
  - The gate's deterministic FA-0.10 threshold is degenerate: more than 10% of CORRECT items tie at g = 1.
  - Post hoc, with exact (fractional) tie-breaking, NF-anchored passes both gates: RENAME FA .074 and ROLE_PERMUTE recall .77.
    NF-pure fails ROLE_PERMUTE (.19), as the plan predicted.
  - The NF-based fusion (fitted on the screen only, applied to E, labelled **post hoc**) scores 0.759 pooled R_AB. That is
    −0.031 [−0.042, −0.020] vs the aligner fusion, but still +0.047 [0.011, 0.082] over the local judge.
- **Graded consensus is worse than binary equivalence.** On the screen AGREE set, ALIGN g scores .827 vs .873 for ALIGN
  equivalence and .891 for c_score_align. The frozen fusion gives g a near-zero weight (−0.12). This is a negative result
  for the planned F2 (graded) design.
- **Mechanism tests (pre-registered rules, results/p_tests.json).**
  - **P1 INCONCLUSIVE.**
    - PEER beats TEXT on COVERAGE (ADD/DROP) errors: +0.093 [0.046, 0.147] at matched FA 0.10.
    - TEXT beats PEER on NF-peer-endorsed errors: −0.103 [−0.171, −0.051].
    - STRUCT has only n=36.
  - **P2 REFUTED.** Spearman(PEER, TEXT) among errors = 0.29, below the 0.4 cut, but the fusion gain does not come from
    peer-endorsed errors (share −0.20).
  - **P3 INCONCLUSIVE.** No significant score × length interaction for any metric. However, the PEER+TEXT − judge gap grows
    from CTRL to the long strata: diff-in-Δ +0.146 [0.020, 0.269].
  - **P4 REFUTED.** Fused false alarms on rewrites of CORRECT bases exceed 0.10: RENAME .385 (inherited from the aligner,
    .859), REORDER .222 (L3). The judges are also unstable: flash-lite on screen RENAME .485, DEMORGAN .520.
- **Error typing.** The top unit code matches the solver's repair operator on 37% of 1–2-op tier-A errors (chance 38%);
  restricted to codable operators, 56%. The typing readout is at chance and should not be claimed.
- **System level (descriptive, 13 system × variant rows).** Kendall τ-b vs the R_AB error rate:
  - PEER+TEXT .718 [.59, .85];
  - local judge .667 [.51, .78].
- **Contamination.** Disguise *improves* the local judge: AUROC(orig) − AUROC(disg) = −0.064 [−0.098, −0.032], MDE 0.047.
  So there is no contamination benefit. PEER signals have no text channel.
- **Coverage and cost.**
  - Every row is in the denominator: 1,086 UNPARSEABLE rows are scored 1.0 by every metric; 38 rows have fewer than 2
    peers (they fall back to the frozen TEXT model); 2.3% of rows have ≥1 UNKNOWN (z3 timeout) unit.
  - Cost per row: PEER pairs 0.026 cpu-s and text side 0.22 cpu-s. The API cost is only the L3 questionnaire (one call per
    sentence), $1.8e-5 per row.
  - Total OpenRouter spend of this artifact: **$0.155**.
- **Threshold transfer.** At the frozen threshold, fused FA on E is 0.29 (screen target 0.10: screen sentences are short).
  FA on tier-B CORRECT (correct but not equivalent to the reference) is .42, against .14 on tier-A CORRECT. PEER+TEXT
  penalises vocabulary and granularity differences.

## Layout

| path | what |
|---|---|
| `method.py` | end-to-end driver (`views`, `api`, `local`, `screen`, `score`, `analyse`, `outputs`, `all`); builds `method_out.json` |
| `src/peer_text.py` | **reusable functions** (see "Functions" below) |
| `src/pool_scoring.py` | per-sentence worker: all pairs, graded consensus per LOFO pool, k=6 subsample, sensitivity family map, c_score_align, medoid repair, text side; SIGALRM caps |
| `src/data_views.py` | E blind ALLOWLIST view (`data/E_blind.jsonl`, sha256 in `data/E_blind.sha256`), label view (`data/E_labels.jsonl`), API row order |
| `src/run_api_E.py` | L3 questionnaires and the flash-lite judges (exp D prompt/disguise, vendored budget), resumable |
| `src/local_judge_E.py` | local Qwen3-8B judge on E (labelled secondary bar; GPU; `.venv_gpu`) |
| `src/key_monitor.sh` | re-launches the API job when the shared key has budget |
| `src/screen_fit.py` | screen pools, labels (AGREE set), probes, variant selection, fusion fit, **prereg freeze** |
| `src/score_E.py` | scores E from the blind view + prereg only (mini → 100 → all), then assembles `results/per_item_E.jsonl` |
| `src/analyse_E.py` | the only label join; guard (prereg hash + mtimes); analyses (a)–(k), placebos, stratified AUROC |
| `src/posthoc_nf_fusion.py` | the labelled post-hoc NF-fusion sensitivity |
| `src/write_deviations.py` | `results/deviations.json` |
| `src/vendor_{a,c,d,e}/` | iteration-1 code, copied unchanged: exp A (fol_triage, content_accounting, llm), exp C (consensus, repair_census, common), exp D (judges, budget, disguise, local_llm; ROOT path patched), dataset-E labeller (fol parser, disguise). Hashes are in `results/prereg.json:code_sha1` |
| `tests/test_peer_text.py` | 12 unit tests (identity, full rename g=0, DROP, QUANT, NEG, SWAP, ADD, contrapositive / De Morgan / prenex g=0, identical-string cache, timeout→UNKNOWN, units ≡ formula) |
| `tests/test_isolation.py` | blind view has no label key; scorers never reference labels; analysis guard refuses a missing, mismatched or newer prereg |
| `tests/prefilter_audit.py` | 500 screen pairs: finite-model 'False' never coincides with z3 'True' (0 conflicts; 37% of pairs refuted without z3) |
| `tests/judge_cache_regression.py` | 30 screen items re-judged hit exp D's cache exactly (30/30, $0), which proves prompt and disguise identity |
| `tests/audit_rederive.py` | recomputes the pooled AUROCs and the headline Δ through sklearn only (all match to 1e-9) |
| `results/prereg.json`, `prereg.sha256`, `prereg_selection.json` | frozen rules, models, thresholds, analyses |
| `results/per_item_E.jsonl` | **one line per E row** (`row_key` = item_id\|prompt_variant; also item_id, fold_E = sha1('E_folds_v1\|'+sentence_id)%5): every score, unit codes, judges, cost, seconds |
| `results/analysis.json`, `tables.md`, `p_tests.json`, `deviations.json` | results |
| `results/screen_scores.jsonl`, `screen_fit.json`, `screen_probes.json`, `rewrite_scores_pt.jsonl` | screen features (3 variants), selection/fit evidence, probes, rewrite/probe scores under the frozen pipeline |
| `results/E_sentences.jsonl` | raw per-sentence worker outputs (all variants, stats) |
| `results/E_judge.jsonl`, `E_judge_local.jsonl`, `E_l3_q.jsonl`, `E_disguise_map.jsonl` | judge outputs, L3 questionnaires, exp-D disguise of every E row |
| `results/posthoc_nf_fusion.json`, `prefilter_audit.json`, `judge_cache_regression.json`, `audit_rederive.json` | checks |
| `method_out.json` (+ `full_`/`mini_`/`preview_`) | exp_gen_sol_out: one example per E row, `predict_*` = every metric (higher = more likely an error) |
| `data/screen/` | copies of the iteration-1 screen inputs (exp C pools, screen labels, exp A/D per-item files) |

Workspace path (all kept artifacts are read from here):
`../../../../../../../../round-2/experiment-5/src/`.
In particular: `results/per_item_E.jsonl` (the join input for iteration 3), `results/prereg.json` and `results/analysis.json`.

## Functions (`src/peer_text.py`)

Each function takes a formula, or `(text, fol)`, or a set of formalisations, and needs no gold formula.
- `parse_fol(s)`: dataset-E parser. Returns None for an unparseable formula, which is a coverage failure and is counted.
- `claim_units(ast)`: independent closed claims whose conjunction is equivalent to the formula.
- `symbol_signature(ast)`: a name-free structural signature per predicate: polarity, quantifier force, quantifier block,
  1-WL neighbourhood, and a semantic clamp profile.
- `name_free_align(cand, peer, text, variant, k)`: the k best peer→candidate bijections (Murty). `NF-pure` uses structure
  only; `NF-anchored` also uses text anchors.
- `pair_result(cand, peer, ent, variant)`: the accepted mapping (by entailment verification) and the unit entailments in
  both directions. `variant='ALIGN'` uses the iteration-1 name aligner instead.
- `Entailer` / `fm_refutes` / `z3_entails`: a sound finite-model refuter (64 random interpretations over domains 1–3),
  then z3. A timeout gives UNKNOWN, never False.
- `graded_consensus(cand, pool, pairs, ent)` → `g_score`, `support`, `coverage`, `c_score_nf`, `unit_codes`, `n_unknown`.
  It is blind to errors shared by the majority of peers, and to meaning renames that keep the structure.
- `l2_bow(text, fol)`, `l3_z3(q, fol)`, `text_side(...)`: TEXT signals (iteration-1 code). L3 needs the text-only
  questionnaire `q`.
- `fused_score(frozen, feats)`, `peer_text_score(text, fol, peers, frozen, q)`: the frozen PEER+TEXT fusion, with a
  one-call API.

## How to run

```bash
bash restore.sh                                 # venvs + WordNet (see below)
export NLTK_DATA=$PWD/data/nltk_data
.venv/bin/python -m pytest -c pytest.ini tests/test_peer_text.py tests/test_isolation.py
.venv/bin/python method.py all                  # every stage is cached/resumable; the prereg is never re-frozen if present
.venv/bin/python tests/audit_rederive.py
```

The API stage needs `OPENROUTER_API_KEY` (the budget is capped at $3 in `src/run_api_E.py`). The local judge needs a GPU
(about 16 GB of VRAM; Qwen3-8B in bf16).

## Deviations (full list: `results/deviations.json`)

- **D1.** The shared OpenRouter key was exhausted at 18:00 UTC. The replacement key issued at ~19:07 UTC was also already at its
  daily limit (a test call returned 403 "Key limit exceeded"); a monitor polled it every 2 min from 19:10 to 22:13 UTC and budget never returned, so the flash-lite bar stays untestable. The flash-lite bar is untestable on E. The local Qwen3-8B
  judge is the labelled secondary bar, as pre-registered in the prereg fallback. The disguised-L3 contamination arm did not
  run.
- **D2.** F1 FAILED by the pre-registered rule. The peer signal is graded consensus with the iteration-1 aligner (ALIGN)
  plus c_score_align. The shared-aligner confound with the labeller stays open.
- **D3.** Post hoc: the F1 failure is a threshold-tie artefact. NF-anchored passes with exact FA. The NF-fusion
  sensitivity is labelled post hoc.
- **D4.** P1/P4 use fractional (exact) matched-FA tie-breaking, because deterministic thresholds give recall 0 by
  construction for tied scores. Both versions are in analysis.json.
- **D5.** Pre-scoring design fixes, from the unit tests:
  - a semantic clamp signature;
  - exact Murty k-best;
  - an anchored-cost rule;
  - NEG as a literal toggle;
  - mapping acceptance by the refuter count;
  - coverage as a mean over peers;
  - `row_key` (115 E item_ids are not unique).
- **D6.** The c_score_align screen regression gives .8597 vs .866 ± .005. L2-bow and L3 reproduce exp A exactly (903/903).
- **D7.** medoid repair budget: 2 s.
- **D8.** Reduced B for some secondary CIs.
- **D9.** Post-freeze edits to assemble and analyse only; no scoring change.
- **D10.** Fusion thresholds are in-sample on the screen, so E FA is .29.
- **D11.** R_ADJ, R_COMP, S4-nested Δ and the frontier ratio are left to the iteration-3 join.

## Restoring removed files

The manifest (`.aii/manifest.yaml`) marks these as `delete`:
- `.venv/`: `uv venv .venv --python=3.12 && uv pip install --python .venv/bin/python -r pyproject.toml`
- `.venv_gpu/`: `uv venv .venv_gpu --python=3.12 && uv pip install --python .venv_gpu/bin/python torch transformers accelerate loguru huggingface_hub aiohttp requests z3-solver`
- `data/nltk_data/`: WordNet, OMW-1.4 and the `words` corpus. Download
  `https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/{wordnet,omw-1.4,words}.zip` into
  `data/nltk_data/corpora/` and unzip. `restore.sh` does all of the above.
- `**/__pycache__/`: regenerated automatically.
- `.pytest_cache/`: regenerated by running the tests (`.venv/bin/python -m pytest -c pytest.ini tests/test_peer_text.py tests/test_isolation.py`).

The Qwen3-8B weights for the local judge live in the run's shared HF cache:
`snapshot_download('Qwen/Qwen3-8B')`.
