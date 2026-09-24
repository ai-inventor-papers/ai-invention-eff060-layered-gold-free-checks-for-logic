# Dataset card: R_COMP-FREE name-free labels (T7b)

Run `run_u75jRHUss0zo`, iteration 4, `gen_art_dataset_5`. The workspace (all paths below are relative to it) is
`.`.

## Status: read this first

- **Labels are SEARCH-ONLY, sealed at 07:37Z, 2026-09-24** (all-row sha256 `9609ebbb…3dd`; untouched-subset sha256
  `b364a49a…500`).
- **The pre-registered gloss step never ran (deviation D9).** Every paid call returned HTTP 403
  `aii_run_budget_exhausted`: the run's Test-idea OpenRouter budget ($7.04 of $7.00) had been spent by earlier steps
  before this artifact's first call, so this artifact spent **$0.000**. Free models returned the 429 daily limit, the box
  has no GPU, and no local model is cached. No ungated substitute checker was used.
- **Consequences for the labels:**
  - **ERROR_CERT is final.** No map in the declared family makes the candidate z3-equivalent to an accepted reading.
    Every rejected map carries a certificate.
  - **MAPPED rows are `UNRESOLVED_GLOSS_NOT_RUN`.** At least one family map is z3-equivalent, but whether the mapped
    names mean the template atoms is not yet decided.
  - **The CORRECT class is empty, so FREE AUROC is NOT_TESTABLE until `src/resume_gloss.py all` runs** (≈$1.8 at
    catalogue prices).
- **Provisional view for iteration 5:** `metadata_label_binary_search_provisional` (ERROR_CERT vs MAPPED). Its
  contamination is audited below. It is TESTABLE by the ≥50/50 rule on all rows (759 / 1,506) and on the untouched
  subset (636 / 1,175). **Say that it is provisional wherever you use it.**

## Composition (`full_data_out.json`, exp_sel_data_out)

| group | rows | input | output |
|---|---|---|---|
| `rcomp_free_labels` | 2,652: every FREE generation record (last per sentence × slot × prompt variant), incl. 199 NO_OUTPUT and 188 UNPARSEABLE | JSON {text, candidate_fol, system, family, slot, prompt_variant, condition, template_id} | ERROR_CERT 759 · UNRESOLVED_GLOSS_NOT_RUN 1,506 · UNPARSEABLE 188 · NO_OUTPUT 199 |
| `gloss_gate_items` | 840: 7 known-answer classes × 120 (half A 442 / half B 398, split by sha1(sentence_id)) | JSON {sentence, candidate_atom, proposed_meaning} | YES / NO |
| `sig_soundness_replay` | 4,280: 2,140 on-signature SIG rows × {nonce, WordNet-synonym} rename | JSON {text, candidate_fol (renamed), rename, template_id} | known pure-z3 SIG label (CORRECT 1,595 / ERROR 429 / READING_CHOICE 116) |

**Sources:**
- FREE candidates: exp 7 `rcomp/raw/generations.jsonl`, raw generations with no scores. 10 slots from 9 families (meta ×2,
  qwen, mistral, deepseek, google ×2, microsoft, openai, cohere), 221 templated sentences (9 templates), few-shot and
  zero-shot prompt variants.
- References: exp 7 `rcomp/work/rcomp_sentences.json` (weak / strong readings; for T8 also the not-accepted converse),
  true by construction.
- Glosses: dataset 3 `lexicon.json`.

**Row keys:** exp 7's recipe `sha1(system|norm(text)|raw_output)[:16]|FREE|slot|prompt_variant`. All 2,652 keys exist
in exp 7's `rcomp_candidates.jsonl`.

## Label semantics: what each label is exact relative to

- **Map family** (prereg v1.1, `prereg_freelab.json`, sha256 `b081c399…`):
  - candidate *units* (unary predicates, or predicates whose other argument slots always hold the same private
    constants) map injectively onto template atoms over x;
  - bridges: B1 reification, B2 de-reification (n-ary), B5 lexical negation (name-regex licensed), B3 merge and B4 split
    (≤2 per map, never mixed);
  - genuinely binary predicates map onto template binary predicates, in either argument order;
  - constants map injectively or stay free.
- **Search is exhaustive over the family under sound prunes:**
  - z3 relevance (inert symbols dropped);
  - z3 monotonicity polarity;
  - coverage/count;
  - a 128-interpretation finite-model fingerprint, whose mismatches are certified countermodels;
  - z3 equivalence (2 s, retry 10 s) for the maps that survive.
- **Search results (2,163 unique classes):**
  - 156,066 maps enumerated;
  - 102,300 passed the fingerprint and went to z3;
  - 0 cap hits, 0 z3 UNKNOWN;
  - median 0.25 s per class, max 14 s.
- **ERROR_CERT is exact relative to that family and those caps.** It is NOT a meaning judgement about forms outside the
  family (below).
- **MAPPED:** at least one family map is z3-equivalent to the weak or strong reading. It says nothing yet about whether
  the names mean the template atoms. In 72% of MAPPED classes the maps need B1/B2 reification, and only 23% have a
  bridge-free map: free vocabulary diverges heavily from the template names.
- **T8 converse (D8).** Without names, the converse `∀x(S∧A∧P→Q)` is a Q↔P relabelling of the weak reading, so reading
  choice can only be settled by glosses. 80 classes carry converse maps.

## Validation

### (i) SIG replay: exact, known labels, $0 (`results/soundness_audit.json`)

Every symbol of the 2,140 SIG rows was renamed and the rows re-searched without names.

| | nonce rename | synonym rename |
|---|---|---|
| ERROR_CERT on known-CORRECT rows (false-error rate; bar ≤ 0.02) | **0 / 1,595** (CI [0, 0.002]) | 0 / 1,595 |
| identity (un-renaming) map recovered on CORRECT rows | 100% | 100% |
| known-ERROR rows with a non-identity equivalent map ("rescue"; the gloss check must stop these) | 9.1% [6.7, 12.2] | 10.5% [7.9, 13.7] |
| READING_CHOICE rows mapped (to be resolved by glosses) | 100% | 100% |
| **oracle-checker ceiling** (a checker that says YES exactly on identity pairs) | CORRECT recall 1.00, false CORRECT 0.00 | same |

- Rescue rates by template: highest on T9 (0.37–0.43), T8 (0.27) and T3 (0.20); ≤0.13 elsewhere.
- The synonym rename only changed 13% of symbols. WordNet mutual first-sense synonyms are sparse; because the search is
  name-free, it matters only for B5 licences.
- The end-to-end gloss run on the pre-registered 300-row synonym subsample is **PENDING**.

### (ii) Executor audit: substitute for the blind Sonnet audit (D9)

- **Who:** the agent model (Claude Opus 5.5), reading sentence + candidate + references.
- **Blindness:** NON-blind, since the auditor knew which class it was sampling. It is weaker evidence than the planned
  blind audit.
- **Sample:** 60 rows per class, stratified by template.

| class | result |
|---|---|
| ERROR_CERT | 51 UNFAITHFUL, 1 UNSURE, **8 FAITHFUL_DIFFERENT_DECOMPOSITION** → implied precision **0.867 [0.758, 0.931]**, below the 0.90 flag |
| MAPPED | **52 / 60 faithful = 0.867 [0.758, 0.931]** |

The 8 unfaithful MAPPED rows are exactly the kind the gloss check is designed to reject:
- B3 merge rescue of a dropped sortal ×3;
- T8 converse ×2;
- B5/permutation rescue of a polarity error ×2;
- one lexical mismatch ("ProvidesFood" for "is food").

**Out-of-family faithful forms that ERROR_CERT contains** (known failure modes, ≈13% of ERROR_CERT):
- disjunctive split of an "A or B" concept, or one predicate reused with two constants (`Has(x,hair) ∨ Has(x,fur)`,
  `DesignedFor(x,a) ∧ DesignedFor(x,b)`): 4/60. Mapping two instances of one predicate to two template atoms is not a
  predicate substitution without unique names, so it is outside the family by design;
- relational / ∃-for-constant decompositions (`∃y(JobAt(x,y) ∧ School(y))`, `∃y Boss(y,x) ∧ Criticizes(y,x)`): 3/60.
  B6 was not declared because the label-free census found 1% (<5% bar);
- negation inside a name that is not at the first token (`DoesNotSupportWeightOfBridge`): 1/60.

**Iteration 5 should report FREE results with and without these form classes (sensitivity).**

### (iii) Old labels (post-seal join, whitelist loader)

- **All 34 old tier-A CORRECT rows are MAPPED.**
- **Of the 420 old tier-A ERROR rows, 123 are ERROR_CERT and 297 are MAPPED** (κ = 0.06 on ERROR vs CORRECT-or-MAPPED).
- **Hand classification of 20 random disagreements:**
  - 17 are **old false errors**: faithful candidates that the name-similarity aligner could not align (Q∨E forms,
    reifications, ternary de-reification);
  - 2 are T8 converse (old ERROR correct);
  - 1 is a B3 merge rescue of a dropped sortal (old ERROR correct; the gloss check must reject it).
- The iteration-3 FREE tier-A ERROR class is therefore substantially contaminated. This is independent evidence against
  the aligner-based labeller.

## Populations and testability (`results/testability_FREE_v2.json`)

- `seen_iter3` = tier-A labelled in iteration 3 (454 rows). The **untouched subset (2,198 rows) is primary**.
- "Untouched" means untouched with respect to label-dependent decisions. Consensus and judge scores exist for every row
  from iteration 3, but none was compared with labels outside tier A.
- Testability rule: ≥50 ERROR and ≥50 CORRECT, each spread over ≥25 sentences.
  - Search-only labels: NOT_TESTABLE (0 CORRECT).
  - Provisional ERROR_CERT vs MAPPED view: TESTABLE on both populations (per-stratum counts in the file; the
    AUROC-MDE planning figure is also there).

## Known limitations

- **Semi-synthetic sentences.** 9 templates, one exception clause each; the references are template-built.
- **Readings accepted.** Weak and strong are both accepted; the T8 converse is not.
- **The gloss check is model-relative.** Only the SIG replay numbers are exact.
- **B5 regex fires on `In…`-prefixed names.** The token `in` is licensed, so `In(x, crotonRiverWatershed)` may map to
  `¬In(…)`. This is always gloss-guarded, and it explains part of the synonym-vs-nonce rescue gap.
- **Free variables are read as constants.** A candidate with no quantifier (`Chef(x) ∧ … → …`) is read by the shared
  parser with `x` as a constant, i.e. as a ground claim, so it is ERROR_CERT. Operator precedence follows the shared
  FOLIO/MALLS parser (↔ lowest).
- **Lexicon glosses are not re-audited here** (deviation D1 of exp 7).

## Licences and intended use

- **Licences:** templates are built from FOLIO/MALLS/E-derived lexicon atoms (FOLIO CC-BY-SA-style; MALLS-v0 is
  CC-BY-NC-4.0). Candidate generations were produced by this run through OpenRouter.
- **Intended use:** iteration-5 confirmation only, scoring frozen metrics ONCE on the untouched subset. Not a training set.

## Reproduce / resume

See `README.md`. The search-only pipeline is deterministic and costs $0. The paid gloss steps resume with
`src/resume_gloss.py all`.
