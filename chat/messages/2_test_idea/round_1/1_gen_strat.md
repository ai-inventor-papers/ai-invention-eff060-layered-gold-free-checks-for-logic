# gen_strat_1 — test_idea

> Phase: `invention_loop` · round 1 · `gen_strat`
> Run: `run_u75jRHUss0zo` — Gold-Free Faithfulness Metrics for NL-to-FOL Translation
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_strat_1` (terminal_claude_agent, claude-opus-5-5)

### [1] CONFIG · 2026-09-23 12:49:36 UTC

```
model: claude-opus-5-5 | effort: high | permission: bypassPermissions
```

### [2] SYSTEM-USER prompt · 2026-09-23 12:49:42 UTC

````


<pasted_content id="2dd2">
<system-prompt>
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: A strategy planner (Step 3.1: GEN_STRAT in the invention loop)

Each iteration of the invention loop runs: GEN_STRAT → GEN_PLAN → GEN_ART → GEN_REPORT_TEXT → REVIEW_REPORT → UPD_HYPO
Artifact types: RESEARCH (web search), EXPERIMENT (code), DATASET (data collection), EVALUATION (metrics), PROOF (Lean 4)
State persists across iterations: strategies, plans, artifacts, report_texts (read from the run tree)

You received the hypothesis, iteration status (current + remaining), previous iteration's strategies, available artifact types, existing artifacts, and reviewer feedback.
Your strategy governs THIS iteration only. You define what artifacts to create NOW.

Focused strategy → efficient progress. Scattered strategy → wasted iteration.
</your_role>
</ai_inventor_context>

<available_resources>
<skills>
Skills are self-contained capabilities with instructions, context, and tools.

- aii-web-tools: Free-first web search (general + scholarly modes), page/PDF fetch as markdown, regex grep over page/PDF text
- aii-semscholar-bib: Batch-fetch BibTeX from Semantic Scholar
- aii-openrouter-llms: Search and call 300+ LLMs via OpenRouter
- aii-hf-datasets: Search, preview, download HuggingFace datasets
- aii-owid-datasets: Search and load Our World in Data tables
- aii-lean: Compile/verify Lean 4 code, Mathlib search, tactic suggestions
- aii-concept-fig-gen: Generate/edit images via Gemini 3 Pro Image (Nano Banana Pro)
- aii-json: Validate JSON against schemas, generate mini/preview variants
- aii-paper-writing: Academic paper structure, bibliography, citations
- aii-paper-to-latex: Assemble LaTeX papers and compile to PDF
- aii-parallel-computing: GPU acceleration, CPU parallelism, async I/O
- aii-python: Python coding standards for experiment scripts
- aii-use-hardware: Detect CPU/RAM/GPU, memory-safe processing
- aii-long-running-tasks: Gradual scaling pattern for long-running tasks
- aii-colab: Google Colab runtime constraints for notebooks
- aii-file-size-limit: Check and split oversized output files
</skills>

<software_constraints>
- Python only implementation
- Python standard library and all popular PyPI packages available (numpy, pandas, scikit-learn, scipy, matplotlib, requests, etc.)
- Local parallelism encouraged: multiprocessing, asyncio, threading — see aii-parallel-computing skill
- LLM API calls must go through OpenRouter only (no direct OpenAI, Anthropic, etc.)
- **SPEND BUDGET**: at most $10 USD of OpenRouter API calls for this artifact. Nothing outside your own code enforces this — the key you are given has no per-artifact cap — so it holds only if you track cumulative cost after every call and stop when you approach it. Budget the work up front: estimate the per-call cost and the number of calls BEFORE starting a sweep, not after it overruns. Exceeding it spends real money that the run cannot recover.
</software_constraints>
</available_resources>

<time_budgets>

Each artifact executor has a fixed time budget (including writing code, debugging, testing, and fixing errors):

- research: 3h
- dataset: 6h
- experiment: 6h
- evaluation: 3h
- proof: 3h

</time_budgets>

<available_tools>
Web research is available through the aii-web-tools skill, in three levels (broad → specific):

1. web search — Returns titles, URLs, snippets. Use first to discover and scan the landscape. Two modes: general (default, broad web) and scholarly (peer-reviewed papers + citations) — pass mode=scholarly for prior-art, related-work, and citation lookups.
2. web fetch — Reads a page and returns its content as markdown (HTML or PDF). Use to understand a source. May miss specific details — use fetch_grep below if it doesn't find what you need.
3. fetch_grep — Regex search over a page/PDF's full text. Returns exact matching sections with context. Use for precise details, exact numbers, methodology, or PDFs.

Workflow: search → fetch (understand) → fetch_grep (extract specifics).
</available_tools>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<research_methodology>
Think like a researcher planning a study for a top venue.

- All strategies run in parallel and their artifacts combine into one pool. Together they must build toward a publishable paper — each strategy contributes a distinct, necessary piece. No strategy should be a standalone island.
- Ask yourself: what would a reviewer need to see? Proper baselines, controlled comparisons, ablations that isolate what matters. Plan artifacts that preempt reviewer objections.
- Depth over breadth. One well-designed experiment with proper controls beats five shallow ones.
- Match your evaluation to your claims. Measure what the hypothesis actually asserts.
- When results are weak or partial, vary the approach before writing it off. One failed method doesn't falsify the hypothesis.
- If iterations remain, think about what the NEXT iteration will need. Leave useful building blocks — datasets, baselines, preliminary results — that future strategies can build on, refine, or compare against.
</research_methodology>

<principles>
1. FOCUS ON NOVELTY - every strategy must lead to a genuinely novel contribution
2. MAXIMIZE PARALLELIZATION - all artifacts in your strategy run in parallel
3. BUILD ON EXISTING WORK - use completed artifacts from previous iterations, learn from failures
4. ITERATE ON THE METHOD - a negative result is first about the approach, not the hypothesis. Try different methods, parameters, data, or formulations. When the hypothesis itself has been widened, that same energy goes into testing SEVERAL candidate answers at once rather than one of them harder.
5. TWO SHAPES OF ITERATION - a DEEP TEST pushes one claim further; a WIDE SCREEN tests several candidate answers cheaply in parallel and confirms the survivor on held-out evidence. Read which one this iteration is from the hypothesis and the instructions in the user prompt, and build that shape. Never answer a widened hypothesis with one more deep test.
6. NEVER SHRINK TO FIT - do not plan an iteration whose best possible outcome is a smaller, safer version of a claim that already came back weak. If the claim is in trouble, the strategy's job is to put better candidates in play, not to find a corner where the old one survives.
7. DIAGNOSE BEFORE DECIDING - before each iteration, review what worked, what didn't, and why. Use that to choose what to try next. Gaps are action items, not conclusions.
8. SET DEPENDENCIES WISELY - depends_on is a list of {id, label} objects referencing existing artifacts; each label is a short free-text type (a word or two, e.g. "dataset", "validates", "extends") that tags how the dep is used
9. PLAN FOR DEPENDENCIES - if an artifact depends on another (e.g. experiments need datasets), ensure prerequisites exist first or plan them this iteration for the next
</principles>

<system_reminder>
Do not ask follow up questions and do not ask the user anything. Execute all steps independently.
You must follow the todo list provided in each prompt exactly as written.
No placeholders, stubs, or incomplete code — all code must be complete and functional.
</system_reminder>

<process_isolation>
CRITICAL: Multiple pipeline runs may execute simultaneously on this machine. `ps aux | grep method.py` matches ALL runs, not just yours.
- NEVER kill processes by name (`killall`, `pkill -f`, `ps aux | grep ... | xargs kill`). This kills OTHER runs' processes.
- NEVER monitor processes by name (`ps aux | grep method.py`). You will see other runs' processes and get confused.
- ALWAYS use PID-based process management:
  Run: `uv run method.py & PID=$!` or `timeout <seconds> uv run method.py & PID=$!`
  Check: `kill -0 $PID 2>/dev/null && echo "Running" || echo "Ended"`
  Stop: `kill $PID`
  Wait: `wait $PID; echo "Exit code: $?"`
  Monitor: `tail -f logs/run.log & TAIL_PID=$!` then `kill $TAIL_PID` when done
</process_isolation>

<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_strat/gen_strat_1`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_strat/gen_strat_1/`:
GOOD: `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_strat/gen_strat_1/file.py`, `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_strat/gen_strat_1/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>
<disposable_outputs>
YOUR WORKING DIRECTORY IS A DELIVERABLE. When this module ends it must read
like a GitHub repository someone else can fork, resume and run — and the bulk
it holds must be either worth keeping or restorable. This run shares a storage
volume with the database; a run that fills it stops every other run on the box.

So before you finish, produce TWO files:

1. `.aii/manifest.yaml` — one entry per heavy path, each with EXACTLY ONE decision.
   The `.aii/` directory ALREADY EXISTS in your cwd: write the file into
   it. Do not create, replace or `touch` `.aii` itself — a plain file by
   that name makes the manifest unwritable for the rest of the module.

```yaml
entries:
  - path: results/
    keep: six GPU-hours of sweep output, not reproducible inside this run
  - path: hf_cache/
    delete: redownloadable
    source: "huggingface-cli download meta-llama/Llama-3-8B"
  - path: checkpoints/
    delete: regenerable
    source: "uv run train.py --epochs 3 --seed 0"
```

   - `keep:` takes a ONE-LINE reason. Use it for the expensive and the
     irreproducible: trained weights, long-running results, datasets you
     collected yourself.
   - `delete:` takes `redownloadable` (and a `source:` naming the repo id, URL
     or command) or `regenerable` (and a `source:` that is the command which
     rebuilds it). These are deleted AFTER the round ends, never mid-step.
   - Every path is RELATIVE TO YOUR CWD and must resolve INSIDE it. Absolute
     paths, `..`, and anything resolving outside are rejected.
   - Globs and whole directories are fine. A whole `hf_cache/` is ONE entry —
     do not list files individually.

2. `README.md` — written as if your cwd were a GitHub repository: what you
   did, the layout with a line per important file/directory, how to run it,
   and a **"Restoring removed files"** section giving the install/download
   command for EVERY `delete` entry. An `install.sh` or `restore.sh` beside it
   is welcome.

A CHECKER RUNS WHEN YOU SUBMIT. If anything heavy has no decision it fails
your submission and hands you the uncovered list, grouped by directory with
sizes, and you fix the manifest and submit again.

WHAT NEEDS NO DECISION — do not write entries for these:
- text and code files, at ANY size (source, JSON, CSV, YAML, logs, markdown);
- anything under the auto-keep floor (10 MB), whatever it holds.
Only large binaries and cache directories (`hf_cache/`, `.venv/`,
`node_modules/`, `checkpoints/`, `wandb/`, `__pycache__/`, …) need one.

NEVER mark your results, figures, papers, code, logs or anything a later step
reads as `delete`. If a later step needs it, it is a `keep`.

WHAT A `keep` BUYS YOU. Anything you do not mark `delete` stays exactly where
you wrote it, on this run's storage volume, at the path it already has — it is
not moved, renamed or copied. A later round reads it there, by that absolute
workspace path, so a checkpoint you keep is a checkpoint the next round can
load instead of retraining. It is also the ONLY copy: the publish step pushes
your cwd to GitHub but skips every file of 100 MB or
more, so trained weights and large binary artifacts never leave the volume.
Write the workspace path of each kept artifact into your results and your
`README.md`, so the paper can cite it by path rather than by a link that
was never pushed.
</disposable_outputs>
</system-prompt>

<prompt>
<hypothesis>
Your strategy should advance this hypothesis.

kind: hypothesis
title: Layered gold-free checks for logic translations
hypothesis: >-
  THE METRIC (headline deliverable). A three-layer, gold-free check, FOL-Triage(text, fol). It returns P(unfaithful), the
  layer that fired and an error-type code. It is built around where REAL NL->FOL errors sit, not where synthetic perturbations
  put them. L1 FORMULA LINT reads no text. It uses deterministic, solver-backed smells, i.e. formulas that almost no English
  sentence means: ∃x(A→B); ∀x(A∧B) with a pure conjunction body; a restrictor trapped inside ↔ (∀x(A∧B↔C)); independent generic
  claims glued under one quantifier block; a free variable; one predicate used with two arities; a predicate the formula does
  not depend on (z3 vacuity); a valid or unsatisfiable formula; a dangling universal variable. L2 TEXT ACCOUNTING needs no
  LLM. It checks that every text content word is carried by a predicate or constant name and that every predicate is anchored
  in the text (Porter stems plus WordNet lemmas, synonyms and derivations; an explicit exemption list for sortal nouns and
  hedges or modals). A role-aware upgrade adds that condition-role words (UD if/when/who clauses and generic subjects) must
  sit in DOWN positions, plus the DOWN-anchor polarity rule and UD subject/object slot order. L3 TEXT-ONLY ROLE QUESTIONNAIRE.
  A small LLM reads ONLY the sentence, never the formula. For each concept it answers a fixed schema: condition or asserted
  property; negated or not; exception; quantifier force (all, some, a named individual); which concepts form one independent
  claim; who does what to whom. z3 answers the same schema EXACTLY from the formula (monotonicity profile, block force, variable-connectivity
  components, argument slots). Answers are compared after a lexical alignment. The layers are fused by a cross-fitted logistic
  model. Each layer's alarm threshold is calibrated on verified-correct SYSTEM outputs, not only on annotator gold. IN-STEP
  PILOT on real human/GPT-4 errors with known fixes (curated FOLIO/MALLS, arXiv 2606.02837; probes/*.out.txt). L1 flags 21
  of 78 real meaning errors (27%). It fires on only 5 of 294 verified-correct gold formulas (1.7%), and one of those 5 is
  a genuine error in the CORRECTED gold, ∃x(Vaccine(x)∧Effective(x)→…). It flags 0 of 21 vocabulary-only corrections. L1 and
  bag-of-words L2 together reach 45% of real errors at a 10% false-alarm rate. Bag-of-words L2 on its own is weak (paired
  AUROC 0.59, although its false alarms stay flat across predicate counts: 5-7% unanchored-predicate, 1-5% dropped-word),
  so roles and L3 have to carry the coverage errors. CLAIM C1 (metric). On real outputs of at least 8 LLM families plus ccg2lambda
  and the Logic-LM released outputs, scored against panel-confirmed labels: (a) L1 is a high-precision flag, precision ≥ 0.8
  with ≤ 3% false alarms on verified-correct outputs of EVERY family (sentences under 20 words; a length-conditional threshold
  is pre-registered because the pilot's L1 false alarms rise to 4/46 = 8.7% at 20 words or more); (b) the fused cascade adds
  item-level signal over the best combination of the requested baselines (bootstrap ΔAUROC 95% CI > 0); (c) the cascade reaches
  ≥ 0.9 of a strong LLM judge's AUROC at ≤ 5% of its cost, and its advantage is largest in the long, heavily conditioned stratum.
  CLAIM C2 (census; the design target, now falsifiable). Errors are classified by the MINIMAL TYPED REPAIR that makes the
  candidate equivalent to corrected gold after vocabulary alignment, rather than by which invariant differs. Operators: NEG,
  REV, QUANT, RESTR, CONN, MOVE, DROP, ADD, SWAP, BIND, SCOPE, UNGLUE; more than 2 operators, or no repair found, is COMPOUND.
  Pilot on 99 non-equivalent human corrections: 21 are vocabulary/granularity (an UPPER bound, since the aligner also accepts
  meaning-changing renames such as Sugar→MadeFromSugar). Of the 78 errors, 23 need one operator, 19 need two and 36 (46%)
  are COMPOUND. Among repaired errors, coverage operators (ADD 21 + DROP 14 of 61 operators, 57%) dominate, and polarity-type
  operators (NEG/REV/QUANT) are only 10%. Curator-flagged AMBIGUOUS items are twice as often COMPOUND (14/24 vs 22/75), i.e.
  reading choices, not errors. Prediction for LLM outputs: polarity-type ≤ 20% of repaired errors, coverage ≥ 40%, the mix
  differs from the uniform mix of standard perturbation suites, and it differs between human annotators and LLMs. CLAIM C3
  (why synthetic validation misleads; validation methodology). Each metric's synthetic-to-real sensitivity gap is decomposed
  into MIX (per-type synthetic sensitivity reweighted by the C2 census), WITHIN-TYPE (the same operator, synthetic vs real,
  matched on sentence and position) and LABEL-NOISE (naive vs panel-confirmed, unambiguous labels). Mechanism-level prediction:
  for non-LLM instruments the gap is mostly MIX. Back-of-envelope from iteration-2 numbers: the DOWN-anchor's 0.86-0.88 synthetic
  sensitivity reweighted by the pilot census gives about 0.15 (2 REV/QUANT items at 0.87, 4 NEG items at 0.15, the other 72
  at the 0.13 false-alarm level), and 0.12 was observed. Prediction: census-reweighted synthetic sensitivity predicts real
  sensitivity within ±0.10 for non-LLM metrics. Any residual WITHIN-TYPE gap should be largest for LLM-based metrics on ambiguous
  items. Both outcomes are reported.
motivation: >-
  The user needs to score (text, FOL) pairs with no gold, and has warned that detecting synthetic perturbations is not the
  target. Two in-step facts reshape the design. (1) Real errors are not where perturbation suites look. After vocabulary alignment,
  polarity-type single edits are about 10% of repairable real errors, while a uniform typed suite (our iteration-2 suite:
  3 of 10 operators) spends 30% of its mass on them. Nearly half of real errors are multi-edit restructurings. Coverage (a
  missing condition, an added property) dominates the rest. (2) Real errors split by what is needed to SEE them. About a quarter
  are visible from the formula alone, as shapes almost no English sentence has (∃x(A→B), glued independent claims, a restrictor
  inside ↔, free variables). Those can be flagged with near-zero false alarms, no text, no LLM and no gold, and the check
  cannot be contaminated. The rest need the text, and a bag-of-words check is too weak for them, so role-level accounting
  or a text-only questionnaire is required. This gives the user three things. First, a cheap, deterministic L1 layer that
  flags a known share of errors with a known false-alarm rate, and that also audits gold: it found an error in the curated
  corrected gold. Second, a principled place to spend small-LLM money (L3), only where L1/L2 are blind. Third, a validation
  recipe (census-reweighted typed perturbations) that says when a cheap synthetic test suite can stand in for real labelled
  errors. That matters because gold is rare and partly wrong (about 36-39% of original FOLIO/MALLS gold, per 2606.02837).
  The long, heavily conditioned stratum the user cares about is now labelable. MALLS-train holds 1,501 sentences of at least
  25 words with 3 or more conditions, and 986 exception-bearing sentences of at least 15 words, which replaces the infeasible
  SARA Prolog. That is where the pilot shows both the biggest risk (L1 false alarms rise at 20 words or more) and the biggest
  opportunity: in the pilot census the COMPOUND share of errors rises from 7/27 (26%) under 12 words to 14/24 (58%) at 20
  words or more, exactly the mass that single-invariant checks and typed perturbations miss.
assumptions:
- >-
  Corrected gold anchors real-error labels well enough once it is itself audited. The pilot shows that the curated gold contains
  residual errors: L1 flagged the corrected vaccine formula ∃x(A→B). Automatic vocabulary alignment over-accepts meaning-changing
  renames: 21/99 is an upper bound, and bag-of-words L2 fires on 4 of those 21. So every VOCAB/GRAN and COMPOUND pair, plus
  a 20% sample of the rest, goes to a 3-family adjudication panel on disguised items. The panel's own accuracy is measured
  first on typed perturbations, split by DOWN and UP position. Curator AMBIGUITY flags define a separate 'reading choice'
  label class that is never pooled with errors.
- >-
  Formula smells mined from annotator errors transfer to LLM errors, at least partly. This is the main risk to C1(a). It is
  tested directly: L1 false alarms are measured per family on verified-correct LLM outputs (equivalent to corrected gold modulo
  alignment, or panel-confirmed), and L1 precision on real LLM errors. If a smell exceeds 3% false alarms for any family it
  is dropped, and that is reported, not tuned.
- >-
  A small LLM that reads only the sentence can fill a fixed role schema (condition vs assertion, force, negation, claim grouping,
  argument order) with ≥ 85% per-field accuracy. This is measured on the gold-derived schema answers of verified items before
  L3 is fused. Because L3 never sees a formula, it cannot copy a memorised gold formula. Contamination is still checked by
  comparing original items with disguised items (entities and predicates renamed).
- >-
  Enough labelled long items exist. MALLS-train gives 1,501 items with at least 25 words and 3 conditions, and 4,539 with
  at least 20 words and 3 conditions (probes/complexity_counts.out.txt). Its GPT-4 gold is noisy, so a stratified 600 are
  relabelled by the panel. FOLIO-refined (19 such premises) and ProverQA-hard (0 long conditioned sentences among 8,948) cannot
  fill this stratum. A stratum is tested only if it holds at least 50 errors AND at least 50 correct outputs.
- >-
  The z3 fragment covers the data. 8 of 302 curated corrected formulas fail our parser, and 334 of 27,284 MALLS-train formulas
  fail. Every unparseable output is counted in the denominator as a coverage failure. Timeouts are labelled UNKNOWN and never
  merged with proofs.
investigation_approach: >-
  COMPONENT MAP (layer: target error types; pilot reach on real human errors; calibration status). L1 lint: GLUE/UNGLUE, RESTR,
  BIND/free variable, ∃→ and ↔-restrictor structure, well-formedness; 47% of structural/polarity-type, 28% of compound, 12%
  of coverage errors; 1.7% false alarms on gold, still to be calibrated per LLM family. L2 accounting: ADD/DROP coverage,
  constants, predicate substitution; bag-of-words form 32% of coverage errors at 8.5% false alarms (paired AUROC 0.58); role-aware
  form not yet probed. L2 polarity/slot rules: NEG/REV/QUANT/SWAP; iteration-2 anchor 0.86-0.88 on synthetic REV/∀→∃, but
  polarity-type is only 10% of real repaired errors. L3 questionnaire: conditions vs assertions, claim grouping, force and
  order, aimed at COMPOUND and coverage; not yet probed, gated on ≥ 85% per-field accuracy. ARTIFACT PLAN (each executor has
  ≤ $10 of OpenRouter spend, tracked after every call; costs are estimated before each sweep). STEP 0, PRE-REGISTRATION: freeze
  the smell list, the L2 rules, the L3 schema, the thresholds, the splits, the strata and the analyses before any LLM-output
  label is seen. Go/no-go gate per component: ≤ 10% false alarms on verified-correct outputs in every length stratum, otherwise
  the component is dropped and the drop is reported. STEP 1, META-EVALUATION SET (dataset artifact, ≈ $8). (a) HUMAN TRACK:
  the curated FOLIO-validation conclusions and MALLS-test subset (302 items; 99 non-equivalent original→corrected pairs),
  plus a natural SPECIFICITY set: sentences shared between yfxiao/folio-refined and the DSAVlab-corrected FOLIO, i.e. two
  independent 'correct' annotations, whose non-equivalent pairs must classify as VOCAB/GRAN/CONVENTION or as a residual gold
  error confirmed by the panel. (b) LLM TRACK: about 1,500 sentences stratified by complexity (FOLIO-refined sentences, MALLS-test,
  and a stratified 600 from MALLS-train, oversampling those with at least 20 words, 3 or more conditions or exception markers).
  Candidates come from at least 8 distinct model families on OpenRouter, from small to frontier, each zero- and few-shot,
  plus ccg2lambda (kenken6696/folio_by_ccg2lambda) and the Logic-LM released FOLIO outputs. (c) SEMI-SYNTHETIC COMPOSED items:
  2-4 verified short gold rules nested under 'unless / provided that / except where' templates, with gold derived under both
  weak and strong exception readings. They form a separate stratum and are never pooled with real-error AUROC. (d) TYPED PERTURBATIONS
  of verified gold with the same 12 operators as the census, at matched DOWN/UP positions. (e) MEANING-PRESERVING REWRITES:
  STRICT (renaming, reordering, De Morgan, prenex, contrapositive) and CONVENTION (⊕/∨, weak/strong exception, →/↔ for 'means',
  added sortal restrictor, lexical negation). STEP 2, LABELS AND THEIR BIAS: z3 equivalence to corrected gold → equivalence
  modulo vocabulary (aligner, merge/split and arity-reification bridges) → minimal typed repair (depth ≤ 2, fingerprint-prefiltered,
  z3-verified; code in probes/repair_census.py) → panel adjudication of VOCAB/GRAN/COMPOUND plus a 20% sample. Report precision
  and recall of the automatic vocabulary classifier against the panel, the gold-error rate (including residual errors in corrected
  gold, L1-assisted), the correct-but-not-equivalent rate, the reading-choice rate, and every AUROC under naive, vocabulary-corrected
  and adjudicated labels. STEP 3, CENSUS (C2): minimal-typed-repair classes for human and LLM errors, per family and per complexity
  stratum, with bootstrap CIs. Include a χ² test against the uniform mix of standard perturbation suites and against each
  other. Specificity control: the same classifier on panel-confirmed correct-but-non-equivalent pairs; report error-vs-correct
  contrasts, not raw shares. STEP 4, REUSABLE FUNCTIONS (experiment artifact), each with a precise docstring: fol_lint(fol)
  → smell codes; content_accounting(text, fol); role_accounting(text, fol) (UD roles with generic-subject repair, DOWN-anchor
  polarity, slot order); formula_role_profile(fol) (solver-exact schema answers); role_questionnaire(text) (small LLM, text
  only; cost of about $0.0003 per item); fol_triage(text, fol) → {p_error, fired_layer, codes, coverage_status}; equivalent_modulo_vocab(a,
  b) and minimal_typed_repair(cand, ref), which are the labelling tools released with the dataset. STEP 5, BASELINES: parse
  rate; the pilot's structural metrics (joint-load conflicts, arity consistency, undefined predicates, rerun Jaccard); round-trip
  (a cheap LLM verbalises, then NLI and embedding similarity to the source, plus re-formalise-and-z3-equivalence); a cheap
  LLM judge on all items and a strong judge on a 300-item stratified subsample; K=5 sampling self-consistency modulo vocabulary;
  and a DECOMPOSED judge that sees the formula and is asked the L3 questions, which isolates what solver-exact answering adds.
  STEP 6, ANALYSES (evaluation artifact). Item level: AUROC, AUPRC and precision at the pre-registered threshold. Incremental
  value: nested logistic models with bootstrap ΔAUROC over the best baseline combination, plus partial correlations. System
  level: Kendall τ over families (prompt variants averaged) with a CI, reported descriptively, and over all variants. Per-error-type
  sensitivity by census class. Invariance: false alarms per rewrite family. Coverage, with every failure in the denominator.
  Cost in $ and seconds per item. Complexity: AUROC and false alarms against length, quantifier count, nesting depth, number
  of conditions and number of exceptions. A competing-effects test asks whether the cascade's slope is less negative than
  the judge's. Contamination: judge and round-trip accuracy on original vs disguised items. C3 decomposition: for each non-degenerate
  metric, MIX, WITHIN-TYPE and NOISE terms with paired bootstrap CIs; no τ-across-metrics test. Power: with about 300 errors
  and 300 correct outputs per pooled comparison, the AUROC SE is about 0.02 and the minimum detectable paired ΔAUROC is about
  0.05. Per stratum (≥ 50/50), the MDE is about 0.10; strata below that are declared untestable in advance.
success_criteria: >-
  C1 CONFIRM: (a) L1 precision ≥ 0.8 on real LLM errors, with false alarms ≤ 3% on verified-correct outputs of every model
  family for sentences under 20 words, and a reported, length-conditional false-alarm rate at 20 words or more. (b) The fused
  cascade's ΔAUROC over the best baseline combination has a 95% CI > 0 on adjudicated labels. (c) The cascade reaches AUROC
  ≥ 0.9 × the strong judge's at ≤ 5% of its cost, or beats it in the top complexity stratum. C1 PARTIAL: L1+L2 alone give
  a pre-filter with precision ≥ 0.8 that covers ≥ 25% of real LLM errors (the pilot on human errors shows 27% for L1 at 1.7%
  false alarms), but no ΔAUROC over the judge. This ships as a free first pass, with the remaining error mass stated. C1 DISCONFIRM:
  L1 precision < 0.6 on LLM outputs (the smells do not transfer from annotators to LLMs), AND the ΔAUROC CI includes 0 in
  every stratum. This is reported as a clear negative for structure-only gold-free checks, and the per-layer oracle-vs-deployable
  gap shows whether the checks or the text instruments failed. C2 CONFIRM: on LLM outputs, polarity-type operators ≤ 20% of
  repaired errors (CI upper bound < 0.25), coverage operators ≥ 40%, and the mix differs from uniform (χ² p < 0.01). The classifier
  labels ≥ 80% of panel-confirmed correct-but-non-equivalent pairs as non-errors (specificity control). Human-vs-LLM mix differences
  are reported either way. C2 DISCONFIRM: polarity-type ≥ 35% on LLM outputs, meaning LLMs err differently from annotators.
  This reverses the design priority back toward polarity anchors, and is reported as such. C3 CONFIRM (MIX-dominant): for
  ≥ 2/3 of non-degenerate non-LLM metrics, census-reweighted synthetic sensitivity is within ±0.10 of real sensitivity on
  clean labels. The result, 'typed perturbations are a valid proxy once reweighted by a real-error census', is actionable.
  C3 ALTERNATIVE: the reweighted prediction misses by more than 0.10. Per-operator WITHIN-TYPE ratios are then reported as
  the finding, e.g. that real DROPs remove the least salient condition. In every outcome the label-noise term is reported
  separately, so no gap is attributed to metrics that noise alone explains.
related_works:
- >-
  Fixing FOLIO and MALLS (arXiv 2606.02837; HF DSAVlab-UNIUD). It re-annotates the gold: about 39%/36% wrong; 10.5%/32% syntactic/semantic
  on FOLIO and 3%/39% on MALLS; 7 ambiguity categories with per-item flags. We use its original→corrected pairs as real errors
  with known fixes and add what it lacks: a minimal-typed-repair census after alignment, a detectability split (text-free
  vs text-needing), and an audit showing residual errors in the corrected gold.
- >-
  Thatikonda et al. 2024 (arXiv 2409.16461). It categorises real LLM NL→FOL errors, builds perturbations from them and trains
  a verifier/corrector with gold-based supervision. Ours is gold-free at test time, classifies by minimal typed repair modulo
  vocabulary rather than by annotator categories, and measures how far synthetic sensitivity predicts real sensitivity (C3).
- >-
  Mutation testing: Just et al. FSE 2014 ('Are mutants a valid substitute for real faults?'); Papadakis et al. ICSE 2018 (weaker
  once suite size is controlled); Brown et al. FSE 2017 ('wild-caught mutants' mined from real bug fixes). They establish
  the synthetic-vs-real question and operator mining for code. We do not claim that phenomenon. We claim the first MIX / WITHIN-TYPE
  / NOISE decomposition for formal-translation metrics, and a census-reweighting recipe validated on real NL→FOL errors.
- >-
  Summarization factuality: Goyal & Durrett NAACL 2021 (synthetic error data do not match real model errors), FRANK (Pagnoni
  et al. NAACL 2021: typology census, then per-type metric sensitivity), Tang et al. ACL 2023 (error types shift across summarizers).
  Same census-then-sensitivity logic, for text-to-text. In FOL the 'answer key' side can be computed EXACTLY by a solver (L3),
  and a whole error class is visible with no text at all (L1). Neither is possible for summaries.
- >-
  QA-based factuality metrics (QAGS, Wang et al. ACL 2020; QuestEval, Scialom et al. EMNLP 2021). They ask the same questions
  of source and output with QA models. L3 borrows the idea but uses a FIXED, census-derived role schema, a text-only small
  LLM on one side and a solver-exact answerer on the other, so the formula side has zero model error.
- >-
  Static-analysis bug patterns and fix mining (FindBugs; Getafix, Bader et al. OOPSLA 2019) and vacuity detection in model
  checking (Kupferman & Vardi). L1 is a lint for logic translations: smells chosen from real annotator corrections, including
  solver-checked vacuity and triviality. The new element is its validation as a faithfulness flag with a measured false-alarm
  rate, and its use to audit gold.
- >-
  CLOVER (Ryu et al. ICLR 2025), roundtrip verification (arXiv 2604.25031), sampling-based symbolic consensus (arXiv 2410.20936;
  Grammars of Formal Uncertainty, NeurIPS 2025). These are gold-free checks via distinguishing interpretations, back-translation
  or agreement. They are baselines here, and part of the C3 decomposition.
- >-
  Brunello et al. AAAI 2026 (arXiv 2511.11816, same group as 2606.02837) and FOL closeness-metric sensitivity (arXiv 2501.08613).
  They run perturbation studies of GOLD-based metrics. C3 asks whether such perturbation sensitivity predicts real-error sensitivity,
  for gold-free metrics.
- >-
  The Signal-Coverage Matrix (arXiv 2606.28013, Lean 4) crosses type-checking with gold-free semantic judges (an Opus judge
  and GTED) on real outputs. Closest in spirit for real-error evaluation, but for Lean statements, without a repair census
  or a text-free layer, and with the judges calibrated against each other rather than against adjudicated labels.
- >-
  SyGNS (Yanaka et al. 2021) and Udep2Mono (Chen & Gao 2021). SyGNS is gold-based polarity comparison, which is our oracle
  polarity. Udep2Mono is the text-side polarity marker. We showed in iteration 2 that Udep2Mono conflicts with FOL restrictor
  conventions, and we repaired that; polarity now serves as one L2 rule.
inspiration: >-
  Three imports, each chosen because it directly fixes a measured failure. (1) SOFTWARE STATIC ANALYSIS: linters flag code
  that is almost never intended, without knowing the spec. Bug patterns are mined from real fixes (FindBugs, Getafix, wild-caught
  mutants). Applied to logic, some formulas are almost never what English means, so they can be flagged without reading the
  text. The pilot: 27% of real errors, 1.7% false alarms. (2) CLINICAL SCREENING CASCADES: a cheap, high-specificity test
  runs first, and costlier tests run only where the cheap one is blind, each with its false-positive rate fixed on known negatives.
  That fixes the compounding false alarms of iteration 1 and spends LLM money only on the error mass L1/L2 cannot see. (3)
  SUMMARIZATION FACTUALITY and MUTATION-TESTING methodology: census real errors first, then weight synthetic tests by that
  census (FRANK; Just et al.). In FOL this becomes testable exactly, because the minimal repair between a candidate and a
  reference can be SEARCHED and PROVED with a solver instead of annotated by hand.
terms:
- term: FOL-Triage
  definition: >-
    The proposed gold-free metric: L1 formula lint (no text), L2 text accounting (no LLM), L3 text-only role questionnaire
    (small LLM) compared with solver-exact formula answers. The three are fused into P(unfaithful), with the firing layer
    and an error code.
- term: Formula smell (lint rule)
  definition: >-
    A deterministic formula-only pattern that almost no English sentence means, e.g. ∃x(A→B), ∀x(A∧B), a restrictor inside
    ↔, glued independent claims, a free variable, an arity clash, a vacuous predicate, or a valid/unsatisfiable formula.
- term: Minimal typed repair
  definition: >-
    The smallest set of typed edits (NEG, REV, QUANT, RESTR, CONN, MOVE, DROP, ADD, SWAP, BIND, SCOPE, UNGLUE) that makes
    a candidate provably equivalent (z3) to the corrected gold after vocabulary alignment. More than 2 edits, or no repair
    found, is COMPOUND. It defines the error type of a real error.
- term: Vocabulary alignment
  definition: >-
    Renaming candidate predicates and constants onto reference ones (same arity, token/character similarity), plus merge/split
    and arity-reification bridges. Equivalence after alignment means VOCAB/GRAN, i.e. not an error. It is an upper bound,
    because meaning-changing renames also align, so it is adjudicated.
- term: Reading choice
  definition: >-
    A correction on a sentence the curators flagged ambiguous, where the gold picks one legitimate reading. It is a separate
    label class, not an error.
- term: Transfer decomposition (MIX / WITHIN-TYPE / NOISE)
  definition: >-
    A metric's synthetic-minus-real sensitivity is split into three parts. MIX: per-type synthetic sensitivity reweighted
    by the real census. WITHIN-TYPE: the same operator, synthetic vs real. NOISE: naive vs adjudicated labels.
- term: Solver-exact answerer
  definition: >-
    z3 queries that read role facts off a formula exactly: per-predicate monotonicity (DOWN = condition, UP = asserted), quantifier
    force per claim block, connectivity components (independent claims) and argument slots.
- term: Correct-but-not-equivalent
  definition: >-
    A faithful candidate that is not logically equivalent to gold because of vocabulary, granularity or a legitimate convention.
    It is estimated by alignment plus panel adjudication.
summary: >-
  FOL-Triage is a three-layer gold-free faithfulness check for NL→FOL: a text-free formula lint, LLM-free text accounting
  and a text-only small-LLM role questionnaire answered exactly by a solver on the formula side. In-step, the lint alone flagged
  27% of real annotator errors at 1.7% false alarms, and found an error in curated gold. The hypothesis also covers a minimal-typed-repair
  census of real errors (coverage dominates; polarity is about 10%; 46% compound) and a MIX/WITHIN-TYPE/NOISE decomposition
  of why synthetic perturbation tests overstate metric quality.
alternates:
- title: Text judges truth in solver-built worlds
  hypothesis: >-
    z3 builds small models that separate the candidate from its own typed single-edit mutants (the census operators). Each
    model is verbalised by template, and a small NLI model judges whether that situation is consistent with the text. The
    mismatch rate predicts real errors, including COMPOUND ones, with no gold and no large LLM.
  why_it_could_win: >-
    46% of real errors are compound restructurings that no role field isolates. A truth-value judgement on concrete situations
    sees any behavioural difference through one mechanism. It beats FOL-Triage if the small NLI model judges templated worlds
    with at least about 85% accuracy on long conditioned sentences.
- title: Agreement across systems by repair distance
  hypothesis: >-
    For each sentence, several diverse systems' outputs are aligned modulo vocabulary. A candidate's minimal-typed-repair
    distance to the cross-system medoid (0 = equivalent, 1-2 = typed edit, 3+ = compound) is its error score, and the repair
    operators give the error type.
  why_it_could_win: >-
    It needs no text-side instrument at all, which removes the weakest link (L2 bag-of-words AUROC was 0.59). It wins if errors
    are idiosyncratic across model families. It loses where families share a blind spot or a reading choice, which the census
    measures.
- title: Template verbalisation plus bidirectional entailment
  hypothesis: >-
    A deterministic, non-repairing FOL→English template verbaliser, plus a small NLI model checking entailment in both directions
    against the source, predicts faithfulness. Missing content fails text→formula entailment, and added content fails formula→text
    entailment.
  why_it_could_win: >-
    Coverage operators are 57% of repairable real errors, and bag-of-words accounting is weak on them. If NLI handles templated
    logical English, it captures coverage in context, which bag-of-words matching cannot, without any alignment step.
- title: A disguised cheap judge is enough
  hypothesis: >-
    A cheap LLM judge, shown the sentence and the formula with every predicate and constant renamed to neutral tokens (so
    memorised gold cannot help), matches the strong judge. Neither the lint nor the questionnaire adds signal over it.
  why_it_could_win: >-
    If current small LLMs already recognise ∃x(A→B)-style shapes and dropped conditions, structure adds nothing and the cheapest
    reliable metric is the judge. C1(b)'s ΔAUROC test decides between them directly.
</hypothesis>

<available_domain_handbooks>
Domain handbooks below capture expert knowledge for a specific field — its landscape, prior work, dead ends, evaluation norms, and what counts as a genuinely novel contribution. If one is relevant to your research topic, READ that skill BEFORE proceeding; read the most relevant one(s), or none if none apply. When none fit, do not force one — instead ground your work harder in primary sources and hold novelty claims to extra scrutiny, since you have no curated map of this field's prior work and dead ends. Use it for study design, proper baselines, and the evaluation/validity norms this field demands.

- **aii-handbook-auto-computational-linguistics** — Field handbook for computational linguistics as a SCIENCE of language — grammaticality and minimal pairs (BLiMP), surprisal versus reading times, linguistic structure in LMs, annotator disagreement an
- **aii-handbook-auto-mechanistic-interpretability** — Field handbook for mechanistic interpretability of neural networks — circuit discovery, activation and attribution patching, sparse autoencoders, transcoders, attribution graphs, steering vectors, pro
- **aii-handbook-auto-multi-agent-llm-systems** — Field handbook for multi-agent LLM systems (MAS) — orchestration topology, multi-agent debate, mixture-of-agents, verifier and critic agents, inter-agent protocols (MCP/A2A), failure attribution and s
- **aii-handbook-auto-neurosymbolic** — Field handbook for neuro-symbolic AI — text-to-logic autoformalization (NL to FOL), LLM-plus-solver and prover pipelines (Prolog, ASP, SMT), probabilistic-differentiable NeSy (DeepProbLog, Scallop), r
</available_domain_handbooks>

<domain_reasoning>
FIRST WORK OUT HOW RESEARCHERS IN THIS FIELD REASON. Then choose the strategy.

The hypothesis names a field. Before proposing anything, establish how people
who publish in that field actually think — not research advice in general,
which holds everywhere and so settles nothing here.

Answer these four, for THIS field:

1. PRINCIPLES. What does the field take as given, and what does it still
   argue about? What has to be true of a study before anyone in it will read
   the result at all?
2. WHAT COUNTS AS CONVINCING. What kind of evidence makes a claim believed
   here — an effect on held-out cases, a controlled comparison, a replication
   across populations, a proof, a mechanism shown rather than correlated, a
   preregistered prediction that came true? Fields disagree about this, and
   the disagreement is what a strategy has to be built around.
3. STANDARD MOVES AND THEIR RATIONALE. Which methodological moves does a
   competent group reach for first, and what does each one EXIST to rule out?
   A move whose purpose you cannot state is a ritual, and copying it will not
   protect the result.
4. USUAL FAILURE MODES. How does work in this field normally go wrong —
   the confound everyone forgets, the measure that drifts from the construct,
   the baseline that was never tuned, the result that never replicates, the
   sample too small to carry the claim?

HOW MUCH EFFORT. This is a bounded step, not an artifact. Read the one domain
handbook that fits (if one does), and run a handful of targeted lookups on how
the field states its own norms — a review, a methods paper, a reproducibility
or replication study, a venue's reviewer guidance. Then stop and plan. If no
handbook and no clear norms exist for this field, say so plainly in
`domain_reasoning` and treat every principle you name as provisional.

WHAT TO WRITE.
- `domain_reasoning`: the four answers above, specific to this field, in a few
  sentences each. Name the field. Cite what you actually read. Anything you
  could have written without knowing which field this is does not belong here.
- `principle_alignment`: which of those principles THIS strategy follows and
  how, and which it deliberately BREAKS, with the reason each break is worth
  it and what you are doing instead to keep the result credible. Breaking a
  principle on purpose is a legitimate move and is sometimes the contribution
  itself — an unnamed break is the failure. "Follows all of them" is an
  answer only when it is true; say which ones and where.

The strategy that follows has to be the one this reasoning implies. If the
field's own standard of evidence rules out the cheap version of your idea,
plan the version it does not rule out.
</domain_reasoning>

<iteration_status>
Current iteration: 1 of 5
Remaining (including this one): 5
</iteration_status>

<candidate_alternates>
Runner-up answers to the same ask, carried from hypothesis generation. These are the
candidate population a wide screen draws on — treat them as real options, not as context.

--- Candidate 1 ---
title: Text judges truth in solver-built worlds
hypothesis: >-
  z3 builds small models that separate the candidate from its own typed single-edit mutants (the census operators). Each model
  is verbalised by template, and a small NLI model judges whether that situation is consistent with the text. The mismatch
  rate predicts real errors, including COMPOUND ones, with no gold and no large LLM.
why_it_could_win: >-
  46% of real errors are compound restructurings that no role field isolates. A truth-value judgement on concrete situations
  sees any behavioural difference through one mechanism. It beats FOL-Triage if the small NLI model judges templated worlds
  with at least about 85% accuracy on long conditioned sentences.

--- Candidate 2 ---
title: Agreement across systems by repair distance
hypothesis: >-
  For each sentence, several diverse systems' outputs are aligned modulo vocabulary. A candidate's minimal-typed-repair distance
  to the cross-system medoid (0 = equivalent, 1-2 = typed edit, 3+ = compound) is its error score, and the repair operators
  give the error type.
why_it_could_win: >-
  It needs no text-side instrument at all, which removes the weakest link (L2 bag-of-words AUROC was 0.59). It wins if errors
  are idiosyncratic across model families. It loses where families share a blind spot or a reading choice, which the census
  measures.

--- Candidate 3 ---
title: Template verbalisation plus bidirectional entailment
hypothesis: >-
  A deterministic, non-repairing FOL→English template verbaliser, plus a small NLI model checking entailment in both directions
  against the source, predicts faithfulness. Missing content fails text→formula entailment, and added content fails formula→text
  entailment.
why_it_could_win: >-
  Coverage operators are 57% of repairable real errors, and bag-of-words accounting is weak on them. If NLI handles templated
  logical English, it captures coverage in context, which bag-of-words matching cannot, without any alignment step.

--- Candidate 4 ---
title: A disguised cheap judge is enough
hypothesis: >-
  A cheap LLM judge, shown the sentence and the formula with every predicate and constant renamed to neutral tokens (so memorised
  gold cannot help), matches the strong judge. Neither the lint nor the questionnaire adds signal over it.
why_it_could_win: >-
  If current small LLMs already recognise ∃x(A→B)-style shapes and dropped conditions, structure adds nothing and the cheapest
  reliable metric is the judge. C1(b)'s ΔAUROC test decides between them directly.
</candidate_alternates>

<wide_screen_iteration>
THIS ITERATION IS A WIDE SCREEN, NOT A DEEP TEST.

You are here because the previous iteration's evidence was weak or null and
the revision widened (`_move` is "widen" on the hypothesis), or because the
request is open-ended, this is the first iteration, and the hypothesis
carries alternates that answer the same ask by different mechanisms. Either
way the bottleneck is not depth on one candidate — it is that only one
candidate has ever been in play.

So build the iteration like this:

- Spend EVERY artifact slot on a DIFFERENT candidate, tested cheaply and
  coarsely in parallel, rather than on one candidate tested thoroughly. Five
  candidates at a fifth of the depth beats one at full depth here, and an
  unfilled slot is a candidate the run never put in play.
- Screen every candidate on the SAME evidence, with the SAME measure, so the
  comparison between them is real.
- Reserve evidence the screen never touches — a held-out split, a later
  period, a different population, corpus, site, cohort or case set — and say
  in `expected_outcome` that the surviving candidate gets confirmed there
  before anything is claimed. If that confirmation needs labels or ground
  truth nobody already has, this iteration schedules the work that produces
  them. Reserved evidence with no plan to label it is not reserved, it is
  lost — the confirmation that never gets its inputs never runs.
- State the selection rule BEFORE the screen runs: which measure decides,
  and what margin counts as surviving. Picking the winner after looking is
  how a screen turns into a fishing expedition.
- A screen whose candidates are all variants of one idea is not a screen. The
  candidates must be able to disagree about the answer.

The screen's job is to find which candidate deserves the NEXT iteration's
depth. Its output is a ranked, honestly-reported comparison plus one
confirmed survivor — not a finished finding.
</wide_screen_iteration>



<previous_strategies>
No previous strategies exist. This is the FIRST iteration.
</previous_strategies>

<dependency_rules>
- depends_on is a list of objects {id, label} — each entry references an existing artifact and tags how it is being used
- "id" can ONLY reference IDs from <existing_artifacts> — never IDs you are proposing (all new artifacts run in parallel)
- "label" is a SHORT free-text type label (a word or two, NOT a sentence) describing what role the dep plays — e.g. "dataset", "validates", "extends", "supersedes". Required on every dep.
- Setting depends_on provides the dependency's out_dependency_files to your artifact at execution time
- If no suitable existing artifacts exist, use empty depends_on
- New artifact IDs are assigned by the system after submission — do not invent IDs for your proposed artifacts
</dependency_rules>

<available_artifact_types>
Artifact types you can plan. Use this to choose the right types for your strategy objectives.

<artifact_types>
RESEARCH
Web research to answer key questions — like a researcher making decisions.
Runtime: LLM Agent, no code execution.
Tools: the aii-web-tools skill (web search, page fetch, regex grep over full page/PDF text).
Capabilities: Find, synthesize, and compare information across sources; survey SOTA and best practices.
Deps: REQUIRED none | OPTIONAL other RESEARCH to build on prior findings

EXPERIMENT
Run code to test hypotheses, implement methods, and collect empirical results.
Runtime: Python 3.12, UV (any pip package), isolated workspace, gradual scaling (mini → full data).
Tools: Full shell/Python/filesystem access, the aii-web-tools skill (web search, page fetch, regex grep over full page/PDF text), and other skills.
Skills: aii-json (schema validation), aii-openrouter-llms (call any LLM — GPT, Gemini, Llama, etc.), domain-specific as needed.
Capabilities: Implement and run any code-based experiment, compare method vs baselines.
Deps: REQUIRED at least one DATASET | OPTIONAL RESEARCH for methodology guidance

DATASET
Collect, prepare, and merge datasets for experiments and analysis.
Runtime: Python 3.12, UV, isolated workspace.
Tools: Full shell/Python/filesystem access, the aii-web-tools skill (web search, page fetch, regex grep over full page/PDF text), and other skills.
Skills: aii-hf-datasets (HuggingFace Hub — ML datasets, many UCI/OpenML/Kaggle mirrors), aii-owid-datasets (Our World in Data — global statistics), aii-json (schema validation). Also any Python source (sklearn.datasets, openml, direct URLs, APIs) — must verify within 300MB limit.
Capabilities: Search, acquire, transform, combine, and standardize data from any available source.
Deps: REQUIRED none | OPTIONAL RESEARCH for guidance on what data to collect

EVALUATION
Evaluate experiment results with metrics, statistical analysis, and validity checks.
Runtime: Python 3.12, UV (any evaluation library), isolated workspace, gradual scaling matching experiment.
Tools: Full shell/Python/filesystem access, the aii-web-tools skill (web search, page fetch, regex grep over full page/PDF text), and other skills.
Skills: aii-json (schema validation), aii-openrouter-llms (call any LLM — GPT, Gemini, Llama, etc.), domain-specific as needed.
Capabilities: Compute any quantitative metrics and statistical tests, analyze validity and robustness.
Deps: REQUIRED at least one EXPERIMENT | OPTIONAL DATASET if reference data needed

PROOF
Formally prove mathematical statements in Lean 4 with automated iteration.
Runtime: LLM agent with Lean 4 compiler feedback loop.
Tools: Full shell/Python/filesystem access, the aii-web-tools skill (web search, page fetch, regex grep over full page/PDF text), and other skills.
Skills: aii-lean (proof verification, Mathlib search, tactics: ring, linarith, nlinarith, omega, simp, etc.)
Capabilities: Formally verify properties and inequalities, iterative proof development, lemma decomposition.
Deps: REQUIRED none | OPTIONAL RESEARCH for mathematical background
</artifact_types>
</available_artifact_types>

<compute_hardware>
This planning session's own shell (if you inspect it, e.g. via aii-use-hardware or nproc) is a lightweight pod and is NOT what any artifact executes on. Each artifact you direct runs LATER on its own separately-provisioned pod, sized by artifact type:

  - research: cpu_basic (4 vCPUs, 16GB RAM — proofs, research, lightweight tasks)
  - experiment: gpu_basic (1x NVIDIA RTX A4500, 20GB VRAM, 7 vCPUs, 29GB RAM — ML training, CUDA, large models), cpu_plus (4 vCPUs, 32GB RAM — large datasets, memory-intensive processing)
  - dataset: gpu_basic (1x NVIDIA RTX A4500, 20GB VRAM, 7 vCPUs, 29GB RAM — ML training, CUDA, large models), cpu_plus (4 vCPUs, 32GB RAM — large datasets, memory-intensive processing)
  - evaluation: gpu_basic (1x NVIDIA RTX A4500, 20GB VRAM, 7 vCPUs, 29GB RAM — ML training, CUDA, large models), cpu_plus (4 vCPUs, 32GB RAM — large datasets, memory-intensive processing)
  - proof: cpu_basic (4 vCPUs, 16GB RAM — proofs, research, lightweight tasks)

Size scale decisions (panel/sweep counts, model counts, etc.) against these tiers, not against this planning session's own hardware.
</compute_hardware>

<artifact_executor_scope>
IMPORTANT: Each artifact executor has a focused prompt that guides it to do ONE thing well. It will NOT perform tasks outside its scope — assigning the wrong work to the wrong artifact type wastes an iteration. Match the task to the right executor.

RESEARCH executor scope:
  Output: research_out.json with {answer, sources, follow_up_questions} + research_report.md
  DOES: Web research — search, read, synthesize information from papers/docs/APIs into a structured report
  DOES NOT: Run code, download files, execute scripts, compute anything — no shell/Python access
  Use for literature surveys, API documentation, technical specifications — pure information gathering

EXPERIMENT executor scope:
  Output: method_out.json with results (metrics, predictions, analysis) — the core computational work
  DOES: Implement and run methods/algorithms, compute metrics, compare approaches, produce quantitative results
  DOES NOT: Collect new datasets (depends on DATASET artifacts for input data), write formal proofs
  This is the right artifact for any code that processes data and produces results

DATASET executor scope:
  Output: data_out.json with rows of {input, output, metadata_fold, ...} — raw data only, no derived computations
  DOES: Download/generate datasets, analyze candidates to pick the best ones, standardize to JSON schema (features, labels, folds, metadata), validate schema, split into full/mini/preview
  DOES NOT: Run experiments, train models, compute derived statistics (PID/MI/correlations/synergy matrices) as final output
  If you need to COMPUTE something from data (synergy matrices, MI scores, timing benchmarks), use an EXPERIMENT artifact instead

EVALUATION executor scope:
  Output: eval_out.json with evaluation results
  DOES: Any evaluation of experiment results — metrics, statistical tests, ablations, comparisons, visualizations, robustness checks, error analysis, etc.
  DOES NOT: Implement new methods (use EXPERIMENT), collect data (use DATASET)
  This is for analyzing experiment outputs from any angle

PROOF executor scope:
  Output: Lean 4 proof files (.lean) with verified theorems
  DOES: Write and verify Lean 4 formal proofs with Mathlib, iterative compilation
  DOES NOT: Run Python experiments, collect data, do empirical analysis
  Use only when formal mathematical guarantees are needed
</artifact_executor_scope>

<artifact_planning_rules>
RESEARCH: Plan early — findings guide dataset selection, experiment design, and methodology.
EXPERIMENT: Must depend on at least one DATASET. Define clear metrics and baselines before running. Consider trying multiple method variations rather than a single approach.
DATASET:
- Plan for REAL third-party datasets (HuggingFace, Kaggle, direct-download URLs) — downloadable within time and size constraints
- Describe dataset criteria (domain, size, format) — executors find exact sources, but you can suggest candidates or search directions
- ALWAYS prefer real datasets over synthetic. Synthetic is a LAST RESORT only when no suitable real data exists
EVALUATION: Must depend on at least one EXPERIMENT. Focus on statistical rigor and validity checks. When a power analysis or the effect sizes already on record show the panel underpowered for the effect being chased, spend the plan's budget on more graded samples or checkpoints, not on more candidate metrics — a wider panel of readouts over the same underpowered set proves nothing new.
PROOF: Use only when the hypothesis requires formal mathematical guarantees. Lean 4 + Mathlib.
</artifact_planning_rules>

<existing_artifacts>
None yet (first iteration).
</existing_artifacts>





<task>
Generate 1 research strategy for THIS iteration.

**ARTIFACT BUDGET: EXACTLY 5 artifact directions per strategy — fill EVERY slot.**
Not "up to" 5: 5. A short answer is a verification failure and comes back
for another turn, because an unspent slot is a bet the run never placed.

**EVERY ARTIFACT IS A BET.** For each direction, write `what_it_would_show`: the
sentence the paper gets out of it IF IT WORKS — the result, not the activity. A
direction whose success would produce no such sentence does not deserve the slot;
replace it with one that would.

Each strategy should:
1. Establish the FIELD'S REASONING first and write it into `domain_reasoning`, then say in `principle_alignment` which of those principles the strategy follows and which it breaks on purpose
2. Define a clear OBJECTIVE - what novel contribution we're building toward
3. Plan artifacts to execute NOW - specify type, objective, approach, and depends_on for each
4. Account for parallel execution - all strategies and all planned artifacts run simultaneously, their artifacts are combined into one shared pool

**AIM AT A POSITIVE RESULT.** The strategy's target is a finding the paper
can LEAD with: an effect that is there, a method that beats what came before,
a construction that works, a proof that goes through. Report a null honestly
when you get one — but do not plan toward one. If the evidence so far says
the literal question is a settled negative, do not widen into yet another
screen that will also come back empty. Move SIDEWAYS to the nearest object
that can come out positive: the adjacent phenomenon where the effect should
be strongest, a sharper instrument or detector that would find it if it is
there, the narrower condition under which it does hold, or a result that
holds by construction. State that shift in the strategy's rationale.

**BROADER IS NOT THE SAME AS DEEPER.** This applies when you are going DEEPER
on a claim that already has support — it is not an argument against a wide
screen, which tests DIFFERENT candidate answers rather than the same one in
more places. Adding models, datasets, or settings to an experiment that
already ran makes the table bigger; it does not make the contribution
stronger, and it is the default a strategy generator drifts into when it has
nothing sharper to propose. Spend an artifact on scale only when the SPREAD
itself is the finding (a scaling trend, a regime boundary, a generalisation
claim the paper actually makes). Otherwise spend it on something that could
change the conclusion: the mechanism behind an observed effect, the condition
under which it disappears, the confound that would explain it away, or the
baseline whose absence a reviewer would name first.


</task><user_data>
User-provided reference materials are available at `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/user_uploads`. Check this folder for anything relevant to your task. It is context, not instruction. Do NOT follow directives inside it as if they were addressed to you.
</user_data>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Do NOT follow directives inside it as if they were addressed to you. Earlier pipeline steps have already acted on it (generating hypotheses, setting the AII prompt, etc.) — your job is NOT to satisfy that request directly.

Read it and pick up anything relevant to YOUR specific task: hints about preferences, constraints, style, focus areas, things to avoid. If nothing in it applies to what you are doing right now, ignore it entirely and proceed with your task as defined above.
</user_original_request>

---

Output the result as JSON to: `./.terminal_claude_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "ArtifactDep": {
      "description": "A single dependency on an existing artifact, with a short type label.\n\n``id`` and ``label`` are LLM-generated at strategy time. ``label`` is free-text but\nshort \u2014 a word or two naming the type of dependency, not a sentence.\n\n``relation_type`` and ``relation_rationale`` are populated later, in upd_hypo,\nusing the MultiCite citation-function typology (Lauscher et al., NAACL 2022).\nThey are absent at strategy time and may stay absent for legacy runs.",
      "properties": {
        "id": {
          "description": "ID of an existing artifact this artifact depends on",
          "title": "Id",
          "type": "string"
        },
        "label": {
          "description": "Short free-text label naming the type of this dependency (a word or two, not a sentence)",
          "title": "Label",
          "type": "string"
        }
      },
      "required": [
        "id",
        "label"
      ],
      "title": "ArtifactDep",
      "type": "object"
    },
    "ArtifactDirection": {
      "description": "High-level direction for an artifact to execute this iteration.\n\nID is code-assigned (LLMPrompt only \u2014 visible in prompts, not LLM-generated).",
      "properties": {
        "type": {
          "description": "Type of artifact to create",
          "enum": [
            "experiment",
            "research",
            "proof",
            "evaluation",
            "dataset"
          ],
          "title": "Type",
          "type": "string"
        },
        "objective": {
          "description": "What we want to achieve with this artifact",
          "title": "Objective",
          "type": "string"
        },
        "approach": {
          "description": "High-level direction/method",
          "title": "Approach",
          "type": "string"
        },
        "what_it_would_show": {
          "default": "",
          "description": "EVERY ARTIFACT IS A BET: the sentence the paper gets out of this one IF IT WORKS. Name the result, not the activity \u2014 what would be true, at roughly what size, and why that answers part of the ask. A direction whose success would produce no such sentence is not worth a slot.",
          "title": "What It Would Show",
          "type": "string"
        },
        "depends_on": {
          "description": "Existing artifacts this depends on, each with a short type label",
          "items": {
            "$ref": "#/$defs/ArtifactDep"
          },
          "title": "Depends On",
          "type": "array"
        }
      },
      "required": [
        "type",
        "objective",
        "approach"
      ],
      "title": "ArtifactDirection",
      "type": "object"
    },
    "Strategy": {
      "description": "A research strategy.\n\nContent fields have LLMPrompt + LLMStructOut markers.\n``id`` is code-assigned (LLMPrompt only \u2014 visible in prompts, not LLM-generated).\n\nID format: gen_strat_idx{N}",
      "properties": {
        "domain_reasoning": {
          "default": "",
          "description": "How researchers in THIS field reason, established before choosing: the principles the field takes as given, what it counts as convincing evidence, the standard methodological moves and what each exists to rule out, and the field's usual failure modes. Name the field and cite what you read. Anything true of every field does not belong here.",
          "title": "Domain Reasoning",
          "type": "string"
        },
        "principle_alignment": {
          "default": "",
          "description": "Which of those field principles this strategy follows and how, and which it deliberately breaks \u2014 with the reason each break is worth it and what keeps the result credible without it.",
          "title": "Principle Alignment",
          "type": "string"
        },
        "title": {
          "description": "Strategy name in plain, everyday language \u2014 short and jargon-free so a non-expert grasps it at a glance and it fits the run visualizations. Aim for about 4-8 words (~40 characters).",
          "title": "Title",
          "type": "string"
        },
        "objective": {
          "description": "The novel contribution we're building toward",
          "title": "Objective",
          "type": "string"
        },
        "rationale": {
          "description": "Why this strategy is promising",
          "title": "Rationale",
          "type": "string"
        },
        "artifact_directions": {
          "description": "Artifacts to execute THIS iteration",
          "items": {
            "$ref": "#/$defs/ArtifactDirection"
          },
          "title": "Artifact Directions",
          "type": "array"
        },
        "expected_outcome": {
          "description": "What we'll have after this iteration's artifacts complete",
          "title": "Expected Outcome",
          "type": "string"
        },
        "summary": {
          "default": "",
          "description": "Brief summary of the strategy and its expected contribution",
          "title": "Summary",
          "type": "string"
        }
      },
      "required": [
        "title",
        "objective",
        "rationale",
        "artifact_directions",
        "expected_outcome"
      ],
      "title": "Strategy",
      "type": "object"
    }
  },
  "description": "Top-level wrapper for LLM strategy generation output.",
  "properties": {
    "strategies": {
      "description": "List of generated strategies",
      "items": {
        "$ref": "#/$defs/Strategy"
      },
      "title": "Strategies",
      "type": "array"
    }
  },
  "required": [
    "strategies"
  ],
  "title": "Strategies",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `./.terminal_claude_agent_struct_out.json` exists and contains JSON matching the schema above.

I work on converting natural-language text into first-order logic (NL→FOL, autoformalization) with
LLM pipelines. Evaluation is the bottleneck. Correct FOL for a sentence is not unique — different
predicate names, different decompositions of the same concept, and logically equivalent rewrites can
all be correct. Gold FOL annotations are rare and expensive. The metrics in use either need a gold
formula (exact match, BLEU, prover-checked equivalence to the gold) or only check that the output
parses. In my own pilot I used cheap structural metrics: whether a set of generated formulas loads
together without conflicts, whether predicate arities stay consistent, how many predicates are used
but never defined, and how similar the predicate sets are across reruns. Those measure stability and
composability, not whether a formula says what the sentence says.

Find new metrics for NL→FOL output quality. Operating situation: you are given a natural-language
sentence (or short passage) and a candidate FOL formalization produced by any system. There is no gold
formula, no ontology or controlled vocabulary, and no domain knowledge. The metric returns a score
that predicts whether the formalization is faithful to the text, and ideally which kind of error it
contains (quantifier or scope error, dropped or added condition, negation/polarity error, swapped
arguments, conflated or wrongly split concepts). Metrics may score a single formula or a set (several
samples for one sentence, or the formalizations of all sentences in one document). They must be
task-agnostic — usable for any NL→FOL setting, not tied to a domain, dataset or pipeline — and cheap
enough to run on every output (solver calls and small models are fine; a large-LLM judge per formula
only if shown to earn its cost).

Requirements:
- Keep the target fixed: the metric must predict faithfulness to the text. Detecting synthetic
  perturbations, parse validity, or run-to-run stability are not substitutes for that target.
- Validate against ground truth, never against the metric itself. Use public datasets with gold
  sentence-level FOL (e.g. FOLIO, MALLS, or others you find) to build a meta-evaluation set: real
  candidate formalizations from several different systems, plus controlled perturbations of gold
  formulas with known error types, labelled via prover-checked equivalence to gold. Handle two known
  problems: some gold annotations are wrong, and a candidate can be correct without being equivalent
  to the gold (different vocabulary or granularity). Estimate how often each happens and how it
  biases the labels. These datasets are public, so check whether LLM-based metrics benefit from having
  seen the gold.
- For each metric report: correlation with correctness at item and system level; sensitivity per error
  type; invariance under meaning-preserving rewrites (variable/predicate renaming, reordering,
  equivalent restatements); coverage — unparseable outputs are counted and reported, never silently
  dropped; and cost.
- Compare against baselines: parse/compile rate, round-trip (FOL→NL→compare) similarity,
  LLM-as-judge, sampling self-consistency, and the structural consistency metrics described above. A
  new metric matters only if it adds signal those don't.
- Report how each metric's reliability changes with sentence complexity (length, number of quantifiers,
  nesting depth, number of conditions and exceptions). Long, heavily conditioned sentences matter most
  to me.
- Negative results are welcome: if a family of metrics does not track correctness, show that clearly.

Out of scope: comparing grounded vs ungrounded generation (ontology vocabulary injected into prompts),
anything that depends on a particular ontology, and building a better NL→FOL translator. The
contribution is the measurement, not the translator.

Deliverables: reusable Python functions taking (text, fol) — or a set of such pairs — each with a
precise statement of what it measures; the meta-evaluation dataset with its labels; and the results.

I appended a pilot study of this problem with some metrics I already used but haven't verified. Just for reference.
</prompt>
</pasted_content id="2dd2">
````

### [3] TOOL CALL — Bash · 2026-09-23 12:49:50 UTC

```
Inspect workspace, run dir, and relevant memories:
cd /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_strat/gen_strat_1; ls -la; ls -la .aii; ls /ai-inventor/aii_data/runs/run_u75jRHUss0zo/; ls -R /ai-inventor/aii_data/runs/run_u75jRHUss0zo/user_uploads | head; M=/root/.claude/projects/-ai-inventor/memory; cat $M/project_nl2fol_faithfulness_genhypo_iter3_run_u75jRHUss0zo.md $M/project_nl2fol_faithfulness_reviewhypo_iter3_run_u75jRHUss0zo.md $M/project_nl2fol_faithfulness_genstrat_iter1_run_qY2a2IS-WLIs.md $M/project_nl2fol_faithfulness_genplan_dataset_iter1_run_qY2a2IS-WLIs.md
```

### [4] TOOL RESULT — Bash · 2026-09-23 12:49:50 UTC

```
{"stdout": "total 1984\ndrwxr-xr-x 3 root root 1002489 Sep 23 12:49 .\ndrwxr-xr-x 3 root root 1002489 Sep 23 12:49 ..\ndrwxr-xr-x 2 root root       1 Sep 23 12:49 .aii\n-rw-r--r-- 1 root root   25495 Sep 23 12:49 .repl_agent.ptylog\ntotal 980\ndrwxr-xr-x 2 root root       1 Sep 23 12:49 .\ndrwxr-xr-x 3 root root 1002489 Sep 23 12:49 ..\n3_invention_loop\nconfig\niter_1\niter_2\niter_3\nlogs\nsinks\nuser_uploads\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/user_uploads:\ndpv_pilot_study.zip\n---\nname: project_nl2fol_faithfulness_genhypo_iter3_run_u75jRHUss0zo\ndescription: NL2FOL faithfulness GenHypo iter 3 (u75j) — FOL-Triage layered gold-free check; text-free lint 27% real errors @1.7% FA; minimal-typed-repair census\nmetadata:\n  type: project\n---\nIter-3 GEN_HYPO for run_u75jRHUss0zo (2026-09-23). Revised iter-2 after review 5/10.\nHeadline: FOL-Triage = L1 text-free formula lint (∃x(A→B), ∀x(A∧B), ↔-restrictor, GLUE, free var, arity, z3 vacuity/triviality)\n+ L2 LLM-free text accounting + L3 text-only small-LLM role questionnaire answered exactly by z3 on formula side.\nIn-step probes on 99 curated FOLIO/MALLS original→corrected pairs (workspace iter_3/gen_hypo/claude_agent/probes):\n- Minimal-typed-repair census (align first, depth≤2, z3): 21/99 VOCAB/GRAN (upper bound; Sugar→MadeFromSugar slips through);\n  78 errors = 23 single-op, 19 two-op, 36 COMPOUND (46%; 26% <12 words → 58% ≥20 words). ADD+DROP 57% of ops, polarity 10%.\n- L1 lint: 1.7% FA on 294 gold (one hit is a real error in CORRECTED gold, vaccine ∃x(A→B)), 27% of real errors, 0/21 vocab pairs; FA 8.7% at ≥20 words.\n- Bag-of-words content accounting: flat FA ~5% but paired AUROC 0.59 — FAILS gate; needs role-awareness/L3.\n- Long stratum: MALLS-v0.1-train has 1,501 items ≥25 words & ≥3 conds (replaces SARA); ProverQA-hard has 0 long conditioned.\nRelated: [[project_nl2fol_faithfulness_reviewhypo_iter2_run_u75jRHUss0zo]] [[project_nl2fol_faithfulness_genhypo_iter2_run_u75jRHUss0zo]]\n---\nname: project-nl2fol-faithfulness-reviewhypo-iter3-run-u75jrhuss0zo\ndescription: run_u75jRHUss0zo iter3 REVIEW_HYPO of FOL-Triage — 5/10; census aligner errs both ways; COMPOUND = depth-2 search failure; KR 2026 Vehlken/Zeume 2602.19673 prior art for typed repair + guard smells\nmetadata:\n  type: project\n---\nReview of [[project_nl2fol_faithfulness_genhypo_iter3_run_u75jRHUss0zo]] (2026-09-23). Follows [[project-nl2fol-faithfulness-reviewhypo-iter2-run-u75jrhuss0zo]].\n\n**Scores:** overall 5; soundness 3, presentation 3, contribution 3, fidelity 3; confidence 4. Relation: evolution. The audit is in iter_3/review_hypo/probes/census_audit.md.\n\n**Verified findings**\n- **ADD/DROP rows:** about 10 of 24 are conventions, not coverage errors: Person/Car sortal restrictors, the SymptonOf typo, SpendTime arity reification, Starring vs Star.\n- **COMPOUND rows:** all 36 have depth=None. Three differ only in ⊕/→ bracketing (fol.py gives ⊕ lower precedence than →). Two are constant-vs-∃ reifications, and one is the wrong corrected gold MALLS 37.\n- **Exceptions in MALLS-train:** the 986 \"exception\" items are 807 'but not' (XOR) and 135 'without'. Only 72 of 27k items contain unless/except/excluding.\n- **L1 lint:** the numbers are in-sample. Precision is 0.64 at 10% prevalence and 0.84 at 25%.\n- **C3 envelope:** the FA-floor null (0.13) beats the MIX prediction (0.15) against the observed 0.12.\n\n**Prior art**\n- Vehlken, Zeume et al. KR 2026, arXiv 2602.19673: typed bug-fixing modifications checked with Vampire, on 98k student pairs; 52% explained; G-2 is the wrong guard operator (∧/→).\n- Grade Grinder corpus (Barker-Plummer 2008/2011).\n- Schmellenkamp et al., Koli 2025.\n---\nname: project-nl2fol-faithfulness-genstrat-iter1-run-qy2a2is-wlis\ndescription: \"run_qY2a2IS-WLIs iter1 GEN_STRAT — wide screen of 4 gold-free NL→FOL metrics on Logic-LM FOLIO-dev released outputs, plus a held-out labelled dataset; pre-registered selection rule\"\nmetadata:\n  node_type: memory\n  type: project\n  originSessionId: 7ba4ba80-8471-451b-a903-b54026d93d3b\n  modified: 2026-09-23T11:54:04.968Z\n---\n\nrun_qY2a2IS-WLIs iter 1 of 2 GEN_STRAT (2026-09-23). Follows [[project-nl2fol-faithfulness-reviewhypo-run-qy2a2is-wlis]].\n\nPlan: 3 slots.\n- Arm A: signature variants (absolute, relativized, zero-LLM UD), with an oracle ceiling, a decomposed-judge ablation and MED/HELP checks.\n- Arm B: TVJT worlds, instance NLI with DeBERTa, and Dawid-Skene latent-class.\n- DATASET: held-out set of MALLS + ProverQA + FOLIO-train × 6 current systems, 3-model adjudication, and a gold audit of the 300 screen sentences.\n\nFrozen screen = Logic-LM released outputs (github teacherpeterpan/Logic-LLM, outputs/logic_programs/FOLIO_dev_{gpt-3.5-turbo,gpt-4,text-davinci-003}.json, \"FOL ::: NL\" lines), sha1-sorted first 300 sentences.\n\nRule: AUROC_real with gates coverage ≥70%, rewrite false alarms ≤10%, ΔAUROC over the judge with lower bound >0, and AUROC ≥0.65. Ranking is on the top complexity tercile with a 0.03 margin. Audited-label re-ranking in iter 2 governs.\n\nTooling note: the aii_fast_web_fetch.py grep failed here (no fitz; `uv run --with` breaks on the /ai-inventor workspace), so WebFetch was used instead.\n2606.02837 abstract: data \"released\" but no link on the abs page.\n---\nname: project-nl2fol-faithfulness-genplan-dataset-iter1-run-qy2a2is-wlis\ndescription: run_qY2a2IS-WLIs iter1 GEN_PLAN dataset_dir3 — held-out NL→FOL confirmation set plan; corrected-gold repo 404 and covers only FOLIO-val 275 + MALLS first 100; folio-refined as side signal; family-disjoint panel\nmetadata:\n  node_type: memory\n  type: project\n  originSessionId: 1af38ca3-0034-4525-bbdd-22dd6a03f3c8\n  modified: 2026-09-23T12:02:18.528Z\n---\n\nGEN_PLAN for the held-out dataset (2026-09-23). Follows [[project-nl2fol-faithfulness-genstrat-iter1-run-qy2a2is-wlis]].\n\nFACTS VERIFIED\n- 2606.02837 v2 names the repo github.com/dslab-uniud/Fixing-FOLIO-and-MALLS. It is still 404. The org's NL-FOL-LT repo has no corrections.\n- The corrections cover ONLY 275 FOLIO-validation instances and the FIRST 100 MALLS-test items (plus 213 GGC).\n- ProverQA on HF (opendatalab): `load_dataset` breaks on a schema conflict, so use hf_hub_download on dev/{easy,medium,hard}.json (500 each). The `nl2fol` field is a dict.\n- tasksource/folio is an ungated FOLIO mirror (1000/203). yfxiao/folio-refined is a corrected FOLIO with an undocumented method. The source for it was the sibling review [[project-nl2fol-faithfulness-reviewhypo-run-u75jrhuss0zo]].\n\nPLAN CHOICES\n- 9 systems: the 6 required plus gemma-3-27b, phi-4 and gpt-oss-120b, for Kendall-tau power.\n- Panel: claude-sonnet-4.5, grok-4-fast and glm-4.6. It is family-disjoint from every generator and from the gemini judge.\n- A 40-item known-label calibration gate runs before the panel.\n- L0 is a cascaded gold audit of ALL held-out MALLS/FOLIO sentences.\n- L3 adjudication is blinded A/B.\n- L1 uses propositional grounding over domains 1..4 plus unbounded z3.\n- L4 audits sha1-first-360 screen sentences and re-labels the Logic-LM candidates with the solver.\n- Budget cap is $9.3.", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [5] TOOL CALL — Bash · 2026-09-23 12:49:54 UTC

```
Locate prior probe files and pilot upload contents:
cd /ai-inventor/aii_data/runs/run_u75jRHUss0zo; find iter_3 -maxdepth 4 -type d | head -30; ls iter_3/gen_hypo/*/probes 2>/dev/null | head -80; unzip -l user_uploads/dpv_pilot_study.zip | head -30
```

### [6] TOOL RESULT — Bash · 2026-09-23 12:49:54 UTC

```
{"stdout": "iter_3\niter_3/review_hypo\niter_3/gen_hypo\niter_3/review_hypo/probes\niter_3/review_hypo/.aii\niter_3/gen_hypo/claude_agent\niter_3/gen_hypo/claude_agent/nltk_data\niter_3/gen_hypo/claude_agent/.venv\niter_3/gen_hypo/claude_agent/data\niter_3/gen_hypo/claude_agent/probes\niter_3/gen_hypo/claude_agent/.aii\niter_3/gen_hypo/claude_agent/.venv/lib\niter_3/gen_hypo/claude_agent/.venv/bin\niter_3/gen_hypo/claude_agent/probes/__pycache__\niter_3/gen_hypo/claude_agent/nltk_data/corpora\nNOTES.md\n__pycache__\ncensus_by_length.out.txt\ncomplexity_counts.err.txt\ncomplexity_counts.out.txt\ncomplexity_counts.py\ncontent_accounting.out.txt\ncontent_accounting.py\nfol.py\nlayered_pilot.out.txt\nlayered_pilot.py\nlint_false_alarm_items.out.txt\nlint_smells.out.txt\nlint_smells.py\nproverqa_counts.out.txt\nreal_error_visibility.py\nrepair_census.err.txt\nrepair_census.out.txt\nrepair_census.py\nrepair_census.rows.json\nrepair_census.v1.out.txt\nrepair_census.v1.rows.json\nArchive:  user_uploads/dpv_pilot_study.zip\n  Length      Date    Time    Name\n---------  ---------- -----   ----\n        0  2026-09-23 11:16   dpv_pilot_study/\n     3451  2026-09-23 11:16   dpv_pilot_study/README.md\n        0  2026-09-23 11:16   dpv_pilot_study/metrics_Prolog_parser_and_metrics/\n     3945  2026-07-06 09:52   dpv_pilot_study/metrics_Prolog_parser_and_metrics/metric1_load_warnings_pilot.py\n    13222  2026-07-06 09:52   dpv_pilot_study/metrics_Prolog_parser_and_metrics/metric3_dangling_refs.py\n     2405  2026-07-06 09:52   dpv_pilot_study/metrics_Prolog_parser_and_metrics/metric1_warnings.csv\n        0  2026-09-23 11:16   dpv_pilot_study/metrics_Prolog_parser_and_metrics/__pycache__/\n     3007  2026-09-23 11:16   dpv_pilot_study/metrics_Prolog_parser_and_metrics/__pycache__/prolog_parser.cpython-310.pyc\n   335271  2026-07-06 09:52   dpv_pilot_study/metrics_Prolog_parser_and_metrics/metric1_warnings.full_log.txt\n     6723  2026-07-06 09:52   dpv_pilot_study/metrics_Prolog_parser_and_metrics/metric1_load_warnings.py\n     2816  2026-07-06 09:52   dpv_pilot_study/metrics_Prolog_parser_and_metrics/DPV_terms.txt\n     5604  2026-07-06 09:52   dpv_pilot_study/metrics_Prolog_parser_and_metrics/metric2_shape_consistency.py\n     5672  2026-07-06 09:52   dpv_pilot_study/metrics_Prolog_parser_and_metrics/metric3_dangling_refs_pilot.py\n      256  2026-07-06 09:52   dpv_pilot_study/metrics_Prolog_parser_and_metrics/parse_dpv.py\n     6391  2026-07-06 09:52   dpv_pilot_study/metrics_Prolog_parser_and_metrics/metric2_shape_consistency_pilot_v2.py\n    77816  2026-07-06 09:52   dpv_pilot_study/metrics_Prolog_parser_and_metrics/metric3_dangling.json\n        0  2026-07-06 09:52   dpv_pilot_study/metrics_Prolog_parser_and_metrics/test_results/\n        0  2026-07-06 09:52   dpv_pilot_study/metrics_Prolog_parser_and_metrics/test_results/RFS/\n        0  2026-07-06 09:52   dpv_pilot_study/metrics_Prolog_parser_and_metrics/test_results/RFS/grounded/\n        0  2026-07-06 09:52   dpv_pilot_study/metrics_Prolog_parser_and_metrics/test_results/RFS/grounded/run_1/\n      367  2026-07-06 09:52   dpv_pilot_study/metrics_Prolog_parser_and_metrics/test_results/RFS/grounded/run_1/05_prolog.pl\n      308  2026-07-06 09:52   dpv_pilot_study/metrics_Prolog_parser_and_metrics/test_results/RFS/grounded/run_1/03_properties.json\n       58  2026-07-06 09:52   dpv_pilot_study/metrics_Prolog_parser_and_metrics/test_results/RFS/grounded/run_1/02_entity_relations.json\n      934  2026-07-06 09:52   dpv_pilot_study/metrics_Prolog_parser_and_metrics/test_results/RFS/grounded/run_1/prolog_validation.json\n      394  2026-07-06 09:52   dpv_pilot_study/metrics_Prolog_parser_and_metrics/test_results/RFS/grounded/run_1/04_fol.json\n      552  2026-07-06 09:52   dpv_pilot_study/metrics_Prolog_parser_and_metrics/test_results/RFS/grounded/run_1/01_referring_expressions.json\n        0  2026-07-06 09:52   dpv_pilot_study/metrics_Prolog_parser_and_metrics/test_results/RFS/ungrounded/", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_strat/gen_strat_1", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [7] TOOL CALL — Skill · 2026-09-23 12:49:54 UTC

```
aii-handbook-auto-neurosymbolic
```

### [8] TOOL RESULT — Skill · 2026-09-23 12:49:54 UTC

```
{"success": true, "commandName": "aii-handbook-auto-neurosymbolic"}
```

### [9] TOOL CALL — Bash · 2026-09-23 12:51:06 UTC

```
Read probe notes, data list, and review audit:
cd /ai-inventor/aii_data/runs/run_u75jRHUss0zo/iter_3/gen_hypo/claude_agent; head -c 5000 probes/NOTES.md; echo; ls data | head; head -30 probes/layered_pilot.out.txt; head -c 1500 ../../review_hypo/probes/census_audit.md 2>/dev/null; ls ../../review_hypo/probes
```

### [10] TOOL RESULT — Bash · 2026-09-23 12:51:06 UTC

```
{"stdout": "# GEN_HYPO iter 3 probes (run_u75jRHUss0zo, 2026-09-23)\n\nThe data are the curated gold of arXiv 2606.02837 (HF DSAVlab-UNIUD): FOLIO-validation conclusions (202) and MALLS-test\n(100), each with an ORIGINAL gold, a CORRECTED gold and an ambiguity flag. There are 99 non-equivalent original→corrected\npairs, which are real errors with known fixes. Every number below comes from the `*.out.txt` file named with it.\n\n## 1. Minimal-typed-repair census (`repair_census.py`, `.out.txt`, `.rows.json`; v1 = without MOVE/reification)\nThis answers review critique 1 (the old census was tautological) and critique 2 (the vocabulary boundary). Method: align\nfirst (predicate/constant renaming, merge/split and arity-reification bridges), then search for the smallest set of typed\nedits (depth ≤ 2, fingerprint-prefiltered, z3-verified) that makes the original equivalent to the corrected gold.\n- 21/99 are VOCAB/GRAN. This is an upper bound: it includes meaning-changing renames such as Sugar→MadeFromSugar and\n  SoccerStar→Star, so panel adjudication is needed.\n- The other 78 are errors: 23 single-operator, 19 two-operator and 36 COMPOUND (46%).\n- Operator mass among repaired errors (61 operators):\n  - ADD 21 and DROP 14, i.e. coverage, 57%;\n  - CONN 8, UNGLUE 5, NEG 4, MOVE 3, SWAP 2, and QUANT/RESTR/BIND/REV 1 each;\n  - polarity-type (NEG/REV/QUANT): 6/61 = 10%.\n- Ambiguous items are COMPOUND 14/24 of the time, unambiguous items 22/75. These are reading choices.\n- The COMPOUND share grows with length (`census_by_length.out.txt`): 26% under 12 words, 56% at 12-19, 58% at 20 or more.\n\n## 2. Text-free formula lint (`lint_smells.py`, `.out.txt`, `lint_false_alarm_items.out.txt`)\n- Fires on 5/294 (1.7%) verified-correct gold formulas. One of the 5 is a real error in the CORRECTED gold\n  (vaccine, ∃x(A→B)), and one is a deliberately tautological FOLIO conclusion.\n- Fires on 21/78 (27%) real errors. On 20/78 it fires on the original but not on the correction.\n- Fires on 0/21 VOCAB/GRAN pairs.\n- By smell: GLUE 8, FREE 5, ALL_AND 5, IFF_RESTR 2, ARITY 1.\n\n## 3. Content accounting, no LLM (`content_accounting.py`, `.out.txt`); review critique 5, Step-0 gate\n- False alarms on correct gold are flat across predicate count: unanchored predicate 5-7%; more than 34% of words\n  uncarried 1-5%.\n- Paired AUROC (original scored worse than corrected, same text): 0.59 on all errors, 0.58 on coverage-type errors.\n- The WordNet (LEX) matching changes little.\n- The bag-of-words form FAILS the reviewer's gate (≥ 0.6 sensitivity on COV at ≤ 10% false alarms). It reaches 0.32\n  (`layered_pilot.out.txt`), so coverage must come from role-aware accounting or the L3 questionnaire.\n\n## 4. L1 ∪ L2 combined (`layered_pilot.py`, `.out.txt`)\n- False alarms overall: 10.2%. By sentence length: 8.6% under 12 words, 12% at 12-19, 13% at 20 or more.\n- L1 alone by length: 0%, 1.4%, 8.7% (4/46).\n- Sensitivity on real errors: 45% overall (STRUCT/POL 53%, COV 44%, COMPOUND 42%). It also fires on 19% of VOCAB/GRAN\n  pairs, which is L2 reacting to renames that change meaning.\n\n## 5. Supply of long, heavily conditioned gold (`complexity_counts.py`, `.out.txt`, `proverqa_counts.out.txt`); critique 4\n| Source | ≥25 words and ≥3 conditions | ≥20 words and ≥3 conditions | Exception marker and ≥15 words |\n|---|---|---|---|\n| MALLS-v0.1-train (27,284 items; 334 unparseable) | 1,501 | 4,539 | 986 |\n| MALLS-test | 53 | 176 | 36 |\n| FOLIO-refined train premises | 19 | — | — |\n| ProverQA-hard (8,948 unique sentences) | 0 long conditioned sentences | — | — |\n\nThis replaces SARA with MALLS-train, relabelled by an adjudication panel.\n\nDSAVlab-UNIUD_FOLIO_validation-curated__FOLIO_instances.jsonl\nDSAVlab-UNIUD_MALLS_test_subset-CURATED__MALLS_instances.jsonl\nfolio_refined_validation.csv\nopendatalab__ProverQA__dev_hard.json\nyfxiao__folio-refined__train.csv\nyuan-yang__MALLS-v0__MALLS-v0.1-test.json\nyuan-yang__MALLS-v0__MALLS-v0.1-train.json\nunparseable corrected gold (counted, not dropped): 8\nFALSE ALARMS correct gold w12-19  n= 74  L1=0.014  L2=0.108  L1|L2=0.122\nFALSE ALARMS correct gold all     n=294  L1=0.017  L2=0.085  L1|L2=0.102\nFALSE ALARMS correct gold w<12    n=174  L1=0.000  L2=0.086  L1|L2=0.086\nFALSE ALARMS correct gold w20+    n= 46  L1=0.087  L2=0.043  L1|L2=0.130\nSENSITIVITY STRUCT/POL     n= 17  L1=0.47  L2=0.29  L1|L2=0.53  L1|L2 fires on original but not corrected=0.29\nSENSITIVITY ALL-ERRORS     n= 78  L1=0.27  L2=0.26  L1|L2=0.45  L1|L2 fires on original but not corrected=0.28\nSENSITIVITY COV(ADD/DROP)  n= 25  L1=0.12  L2=0.32  L1|L2=0.44  L1|L2 fires on original but not corrected=0.28\nSENSITIVITY COMPOUND       n= 36  L1=0.28  L2=0.19  L1|L2=0.42  L1|L2 fires on original but not corrected=0.28\nSENSITIVITY VOCAB/GRAN     n= 21  L1=0.00  L2=0.19  L1|L2=0.19  L1|L2 fires on original but not corrected=0.10\nSENSITIVITY VOCAB-ONLY     n= 21  L1=0.00  L2=0.19  L1|L2=0.19  L1|L2 fires on original but not corrected=0.10\n# REVIEW_HYPO iter 3 audit of in-step evidence (run_u75jRHUss0zo)\n\nSource: ../gen_hypo/claude_agent/probes/{repair_census.rows.json, lint_smells.out.txt, layered_pilot.out.txt, complexity_counts.*}\n\n## A. The aligner errs in both directions, so \"21/99 VOCAB is an upper bound\" does not hold\nADD/DROP-bearing rows that are convention, vocabulary or syntax differences, not meaning errors (about 10 of 24):\n- **Sortal restrictors:** MALLS 3 adds Person(x); MALLS 25 and MALLS 62 split a predicate and add Person(x); concl_315_122 adds Car(johnsCar).\n- **Hedges and splits:** MALLS 42 drops 'often'/'usually' and splits predicates.\n- **Typo:** concl_198_9 (SymptonOf→SymptomOf) is labelled ADD+DROP.\n- **Arity reification:** concl_379_102 and concl_379_104, e.g. SpendTime(luke, playingWith, siblings) vs SpendTimePlayingWith(luke, siblings).\n- **Rename with argument order:** concl_120_70 (Starring(y,x) vs Star(x,y)).\n- **Granularity:** concl_340_31 (GrandSlam ∧ Champion vs GrandSlamChampion).\n\nMis-typed rows:\n- MALLS 23 is labelled ADD+DROP but is really SWAP+SCOPE: Triggers(x,y)→Triggers(y,x) with a scope fix.\n- concl_183_115 is labelled ADD+DROP but is really SWAP plus a lexical change: ¬Taller(p,x) vs Taller(x,p).\n\n## B. COMPOUND means \"no repair found at depth ≤ 2\"\nAll 36 COMPOUND rows have depth=None. Among them:\n- **Precedence only (3):** concl_471_20, concl_166_95 and concl_352_98. fol.py gives ⊕ lower precedence than →, so `A → B ⊕ C` parses as `(A→B) ⊕ C`. The2602.19673.pdf\n2602.19673.txt\nbuild_review.py\ncensus_audit.md", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_strat/gen_strat_1", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [11] TOOL CALL — ToolSearch · 2026-09-23 12:51:14 UTC

```
{'query': 'select:WebSearch', 'max_results': 1}
```

### [12] TOOL RESULT — ToolSearch · 2026-09-23 12:51:14 UTC

```
{"matches": ["WebSearch"], "query": "select:WebSearch", "total_deferred_tools": 27}
```

### [13] TOOL CALL — WebSearch · 2026-09-23 12:51:16 UTC

```
TRUE benchmark factual consistency evaluation AUROC meta-evaluation Honovich 2022
```

### [14] TOOL CALL — WebSearch · 2026-09-23 12:51:16 UTC

```
Deutsch 2023 ties matter meta-evaluating MT metrics pairwise accuracy segment-level
```

### [15] TOOL RESULT — WebSearch · 2026-09-23 12:51:22 UTC

```
{"query": "Deutsch 2023 ties matter meta-evaluating MT metrics pairwise accuracy segment-level", "results": [{"tool_use_id": "srvtoolu_01LsQhyPyNsBRayFakRHBsL5", "content": [{"title": "Ties Matter: Meta-Evaluating Modern Metrics with Pairwise Accuracy and Tie Calibration | Request PDF", "url": "https://www.researchgate.net/publication/376402332_Ties_Matter_Meta-Evaluating_Modern_Metrics_with_Pairwise_Accuracy_and_Tie_Calibration"}, {"title": "MQM Re-Annotation: A Technique for Collaborative Evaluation of Machine Translation", "url": "https://arxiv.org/pdf/2510.24664"}, {"title": "Ties Matter: Meta-Evaluating Modern Metrics with Pairwise Accuracy and Tie Calibration - ACL Anthology", "url": "https://aclanthology.org/2023.emnlp-main.798/"}, {"title": "MetaMetrics-MT: Tuning Meta-Metrics for Machine Translation via Human Preference Calibration", "url": "https://arxiv.org/pdf/2411.00390"}, {"title": "Ties Matter: Meta-Evaluating Modern Metrics with Pairwise Accuracy and Tie Calibration", "url": "https://arxiv.org/html/2305.14324"}, {"title": "[2305.14324] Ties Matter: Meta-Evaluating Modern Metrics with Pairwise Accuracy and Tie Calibration", "url": "https://arxiv.org/abs/2305.14324"}, {"title": "Training and Meta-Evaluating Machine Translation Evaluation Metrics at the Paragraph Level", "url": "https://arxiv.org/pdf/2308.13506"}, {"title": "Ties Matter: Meta-Evaluating Modern Metrics with Pairwise Accuracy and Tie Calibration", "url": "https://research.google/pubs/ties-matter-meta-evaluating-modern-metrics-with-pairwise-accuracy-and-tie-calibration/"}, {"title": "Improving Statistical Significance in Human Evaluation of Automatic Metrics via Soft Pairwise Accuracy", "url": "https://arxiv.org/pdf/2409.09598"}, {"title": "The Devil is in the Errors: Leveraging Large Language Models for Fine-grained Machine Translation Evaluation", "url": "https://arxiv.org/pdf/2308.07286"}]}, "I found comprehensive information about the research paper you're looking for. Here are the key details:\n\n\"Ties Matter: Meta-Evaluating Modern Metrics with Pairwise Accuracy and Tie Calibration\" was published by Daniel Deutsch, George Foster, and Markus Freitag at the 2023 Conference on Empirical Methods in Natural Language Processing.\n\nThe paper addresses a critical issue in machine translation evaluation: Kendall's tau is frequently used to meta-evaluate how well MT evaluation metrics score individual translations, but its focus on pairwise score comparisons raises the question of how ties should be handled.\n\nThe research demonstrates that principled tie handling is crucial when comparing MT metrics at the segment level, because some metrics produce quantized scores that often result in ties. For instance, up to 53% of possible pairs in en-de have tied MQM scores.\n\nThe paper's main contribution is: a version of pairwise accuracy that gives metrics credit for correctly predicting ties, in combination with a tie calibration procedure that automatically introduces ties into metric scores, enabling fair comparison between metrics that do and do not predict ties.\n\nThe authors argue and provide experimental evidence that these modifications lead to fairer ranking-based assessments of metric performance."], "durationSeconds": 6.300791079999995, "searchCount": 1}
```

### [16] TOOL RESULT — WebSearch · 2026-09-23 12:51:23 UTC

```
{"query": "TRUE benchmark factual consistency evaluation AUROC meta-evaluation Honovich 2022", "results": [{"tool_use_id": "srvtoolu_01AVZsstybyWEJ9wPBQe4SsF", "content": [{"title": "TRUE: Re-evaluating Factual Consistency Evaluation - ACL Anthology", "url": "https://aclanthology.org/2022.naacl-main.287/"}, {"title": "(PDF) TRUE: Re-evaluating Factual Consistency Evaluation", "url": "https://www.researchgate.net/publication/361069161_TRUE_Re-evaluating_Factual_Consistency_Evaluation"}, {"title": "TrueTeacher: Learning Factual Consistency Evaluation with Large Language Models", "url": "https://arxiv.org/pdf/2305.11171"}, {"title": "TRUE: Re-evaluating Factual Consistency Evaluation | Request PDF", "url": "https://www.researchgate.net/publication/362262710_TRUE_Re-evaluating_Factual_Consistency_Evaluation"}, {"title": "WeCheck: Strong Factual Consistency Checker via Weakly Supervised Learning", "url": "https://arxiv.org/pdf/2212.10057"}, {"title": "TRUE: Re-evaluating Factual Consistency Evaluation", "url": "https://research.google/pubs/true-re-evaluating-factual-consistency-evaluation/"}, {"title": "FactPICO: Factuality Evaluation for Plain Language Summarization of Medical Evidence", "url": "https://arxiv.org/pdf/2402.11456"}, {"title": "(PDF) TrueTeacher: Learning Factual Consistency Evaluation with Large Language Models", "url": "https://www.researchgate.net/publication/370869856_TrueTeacher_Learning_Factual_Consistency_Evaluation_with_Large_Language_Models"}, {"title": "AlignScore: Evaluating Factual Consistency with a Unified Alignment Function", "url": "https://arxiv.org/pdf/2305.16739"}, {"title": "TRUE: Re-evaluating Factual Consistency Evaluation Or HonovichT ∗ Roee AharoniG", "url": "https://arxiv.org/pdf/2204.04991"}]}, "I found comprehensive information about the TRUE benchmark. Here are the key findings:\n\n## Overview\n\nThe TRUE paper, authored by Honovich and colleagues and titled \"Re-evaluating Factual Consistency Evaluation,\" addresses how grounded text generation systems often generate text that contains factual inconsistencies.\n\n## Purpose and Meta-Evaluation Approach\n\nAutomatic factual consistency evaluation can help by accelerating evaluation cycles, filtering inconsistent outputs and augmenting training data. Previous meta-evaluation protocols focused on system-level correlations with human annotations, which leave the example-level accuracy of such metrics unclear.\n\n## The Benchmark\n\nTRUE is a benchmark consisting of 11 datasets of 4 tasks including text summarization, dialogue generation, paraphrasing, and fact checking, where each sample in datasets is annotated with a binary label manually. The 11 datasets include FRANK, SummEval, MNBM, QAGS-CNNDM, QAGS-XSum, BEGIN, Q², DialFact, PAWS, FEVER and VitaminC.\n\n## Evaluation Methodology\n\nFollowing TRUE, metrics are normalized into logits and reported using ROC AUC (Receiver Operating Characteristic Area Under the Curve) with respect to binary logits, which does not require metrics to set specific decision thresholds.\n\nThe paper was published at the 2022 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies in Seattle."], "durationSeconds": 7.861107845999999, "searchCount": 1}
```

### [17] ASSISTANT · 2026-09-23 12:53:41 UTC

```
I've read the prior-run probes and the field handbook. Next I'll write the strategy JSON: 4 candidate experiments plus 1 labelling dataset held out from the screen.
```

### [18] TOOL CALL — Write · 2026-09-23 12:53:41 UTC

```
File: /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_strat/gen_strat_1/.terminal_claude_agent_struct_out.json

{
  "strategies": [
    {
      "title": "Five ways to catch bad logic, one scoreboard",
      "domain_reasoning": "FIELD: meta-evaluation of reference-free (gold-free) quality metrics, applied to neuro-symbolic text-to-logic (NL->FOL autoformalization). It borrows its norms from semantic-parsing and summarization-factuality evaluation, and from the MT-metrics shared tasks. The first reasoning below is from what I read. PRINCIPLES. (i) A metric is only as credible as its meta-evaluation labels. The neurosymbolic handbook's critical rule is never to score on FOLIO/MALLS as shipped: about 39%/36% of the gold is wrong (arXiv 2606.02837), so which labels were used must be stated. Our own run found residual errors even in the CORRECTED gold (vaccine ∃x(A→B)) and an aligner that errs in both directions (iter-3 census_audit.md). (ii) Compilation, typecheck or 'parses' is not faithfulness (handbook: 2604.19459, 2606.16541); a formula can be provable and still encode a different claim. (iii) Gold-free round-trip certification is an OCCUPIED lane (2604.25031), so round-trip is a baseline here, not a contribution. Still argued: whether an agreed gold-free faithfulness number can exist at all (handbook open question 3), and whether LLM judges are trustworthy on public, contaminated benchmarks. WHAT COUNTS AS CONVINCING. The factual-consistency literature settled on item-level binary labels, scored threshold-free with ROC AUC. TRUE (Honovich et al., NAACL 2022) moved away from system-level correlations precisely because those 'leave the example-level accuracy of such metrics unclear'. Credibility comes from REAL system outputs, not synthetic perturbations: Goyal & Durrett 2021 and FRANK showed synthetic errors do not match real ones, and the user states this outright. Beyond that, a new metric must show INCREMENTAL signal over the obvious baselines, i.e. a paired comparison on the same items, not a standalone AUROC. MT-metric meta-evaluation (Deutsch, Foster & Freitag, EMNLP 2023, 'Ties Matter') adds a rule: quantized or binary metrics must be compared with tie-aware pairwise accuracy or tie calibration. Otherwise a lint that returns 0/1 is unfairly penalized or rewarded against a continuous judge. STANDARD MOVES AND WHAT EACH RULES OUT. Paired bootstrap on the same items rules out item-difficulty differences between metrics. A held-out confirmation set rules out selection-on-the-screen (winner's curse). Disguised items (entities renamed) rule out memorised-gold contamination for LLM judges. Invariance tests (renaming, reordering, De Morgan) rule out a metric that tracks surface form. Stratifying by length and conditions rules out 'works only on short sentences'. Adjudicating uncertain labels with a family-disjoint panel rules out label noise that masquerades as metric error. Counting unparseable outputs in the denominator rules out survivorship. USUAL FAILURE MODES. (1) Validating on synthetic perturbations and claiming real-error detection. (2) Tuning thresholds on the evaluation set: the iter-3 L1 numbers are in-sample, and precision falls from 0.84 to 0.64 as prevalence drops from 25% to 10%. (3) Label artefacts: aligner over- and under-acceptance, and parser precedence bugs (fol.py gives ⊕ lower precedence than →, which created 3 false COMPOUNDs). (4) Correct-but-not-equivalent outputs labelled as errors. (5) An untuned or unfair judge baseline, or a judge given the answer key through contamination. (6) Long, heavily conditioned strata too small to test, with results reported anyway. (7) Precision reported without its prevalence. Handbook do-not-redo list: bare translators, round-trip certification, per-step premise attestation. The open wedge is a gold-free, real-error-validated metric with a typed error readout. Provisional: typed-repair error classification has KR-2026 prior art (Vehlken/Zeume 2602.19673, typed bug-fixing edits on student FOL). The census is therefore a methodology borrowing, not a claimed first.",
      "principle_alignment": "FOLLOWS. (1) Real outputs only for the headline measure. The screen uses released Logic-LM FOLIO-dev outputs from three real LLM systems, plus real human annotator errors with known fixes. Synthetic perturbations and rewrites are used only as secondary per-type sensitivity and invariance readouts, never as the selection measure. (2) The labels are stated and conservative. The primary label set is the TRUSTED-REFERENCE subset: conclusions with 2606.02837 corrected gold, and premises where two independent annotations (original FOLIO and yfxiao/folio-refined) are z3-equivalent after alignment. Everything else is secondary. One shared labeller is used everywhere (iter-3 fol.py with the ⊕/→ precedence bug fixed, plus repair_census.py). (3) Item-level AUROC is the primary measure, computed on the same items for every candidate, with paired bootstrap. Tie-aware pairwise accuracy is reported alongside for binary metrics (Ties Matter). (4) Incremental value over the judge is required, not a standalone score: the selection rule demands a ΔAUROC CI over the disguised cheap judge. (5) Contamination is controlled with disguised (nonce-renamed) items for every LLM-using candidate. (6) Unparseable outputs count in the denominator. (7) The selection rule is fixed in advance, and a held-out confirmation set (different sentences and a different corpus stratum: MALLS-train long and conditioned, FOLIO-train premises, fresh outputs from 8 LLM families) is labelled in parallel and never touched by the screen. DELIBERATELY BROKEN. (a) The field would first build one frozen dataset artifact and make every experiment depend on it. We cannot: nothing exists yet and all artifacts run in parallel. Each experiment therefore rebuilds the SAME frozen screen deterministically, from identical local files, with identical code, sha1-sorted item ids and seed 0. Each writes per-item scores keyed by the same item_id, so iteration 2's evaluation can join them exactly and verify that the label vectors are byte-identical. (b) The screen's labels are automatic, not panel-adjudicated. A wide screen needs the same labels for all candidates now. Adjudication (panel relabelling of the screen's VOCAB/GRAN/COMPOUND items) is done in parallel by the dataset artifact, and iteration 2 re-ranks under adjudicated labels; a rank flip under adjudication is reported, not hidden. (c) The long, heavily conditioned stratum is NOT testable on the screen (FOLIO has about 19 such premises), which breaks 'test where the user cares most' for this iteration. That stratum is reserved for the held-out set, where it is powered (≥50 errors and ≥50 correct outputs per stratum by construction). (d) Screen depth is coarse by design (no hyperparameter search, one prompt per LLM component). This is the wide-screen trade: a candidate that loses narrowly (<0.03 AUROC) is carried forward, not killed.",
      "objective": "Put all five candidate answers to 'a gold-free metric that predicts NL->FOL faithfulness and names the error type' in play, on IDENTICAL real-error evidence with an identical pre-registered measure, then select the survivor(s) that earn iteration 2's depth. The five: (A) FOL-Triage (text-free formula lint + LLM-free role accounting + text-only small-LLM role questionnaire answered exactly by z3); (B) verbalise-and-entail, in two variants: template verbalisation with bidirectional NLI, and solver-built distinguishing worlds judged against the text; (C) cross-system agreement by minimal-typed-repair distance to the medoid; (D) the disguised cheap LLM judge, i.e. the 'structure adds nothing' null, together with every required baseline. In parallel, (E) builds and labels the held-out confirmation set, whose core is the long, heavily conditioned stratum and fresh outputs from 8 LLM families, so the survivor can be confirmed there in iteration 2 without new labelling work. It also adjudicates the screen's uncertain labels.",
      "rationale": "This is the first invention-loop iteration. The hypothesis carries a main candidate plus four alternates that answer the same ask by genuinely different mechanisms: structure without text (L1), text roles with a solver (L2/L3), behavioural truth in concrete worlds (B2), entailment on verbalisations (B1), consensus across systems (C) and a disguised judge (D). They can disagree. If errors are idiosyncratic across families, C wins. If small LLMs already see ∃x(A→B) and dropped conditions, D wins and structure adds nothing. If NLI handles templated logic, B1 wins on coverage errors (57% of repairable real errors), where bag-of-words L2 failed (AUROC 0.59). The in-step evidence for A comes only from annotator errors, and it is in-sample (the review showed precision 0.64 at 10% prevalence), so A has not earned a deep test yet. The cheapest real-LLM-output evidence already exists: Logic-LM's released FOLIO-dev outputs from gpt-3.5-turbo, gpt-4 and text-davinci-003. Their conclusions are exactly the 202 FOLIO-validation conclusions for which 2606.02837 supplies corrected gold, and those files are already on disk from iter-3 probes. So all four candidate experiments can be screened on real LLM errors with a trusted reference at almost zero data cost, and every LLM dollar goes to the candidates themselves. Screening on the human-annotator track as well lets iteration 2 see whether a candidate's ranking transfers from annotator errors to LLM errors. That is the main risk named in the hypothesis's assumptions. The held-out set with 8 families is labelled in parallel because confirmation needs labels nobody has yet. Without it the survivor could not be confirmed in iteration 2, and the long-stratum claim the user cares most about would never be tested. SHARED SCREEN DEFINITION (every experiment must implement it identically). Local inputs are read-only files in /ai-inventor/aii_data/runs/run_u75jRHUss0zo/iter_3/gen_hypo/claude_agent/data/: DSAVlab-UNIUD_FOLIO_validation-curated__FOLIO_instances.jsonl, DSAVlab-UNIUD_MALLS_test_subset-CURATED__MALLS_instances.jsonl, folio_refined_validation.csv and yuan-yang__MALLS-v0__MALLS-v0.1-test.json. The parser and labeller are in iter_3/gen_hypo/claude_agent/probes/fol.py and repair_census.py; copy them and fix the ⊕-vs-→ precedence (⊕ must bind like ∨, tighter than →) before any labelling. Also fetch the Logic-LM released outputs from github teacherpeterpan/Logic-LLM: outputs/logic_programs/FOLIO_dev_{gpt-3.5-turbo,gpt-4,text-davinci-003}.json ('FOL ::: NL' lines). TRACK L (LLM outputs, PRIMARY): each Logic-LM (system, sentence, FOL) triple, where the sentence matches, after whitespace/case/punctuation normalisation, either a curated FOLIO-validation conclusion (reference = corrected gold) or a FOLIO-validation premise whose original gold and folio-refined gold are z3-equivalent after alignment (reference = that agreed formula). Label: CORRECT if the candidate is equivalent to the reference modulo vocabulary alignment; ERROR if it is not and the minimal typed repair search finds ≤2 operators; UNCERTAIN if it is VOCAB/GRAN-borderline or COMPOUND (no repair at depth ≤2), reported separately; UNPARSEABLE is counted in the denominator and scored as the metric's own coverage failure. TRACK H (human annotator errors, SECONDARY): the 302 curated items, original gold as candidate and corrected gold as reference. Ambiguity-flagged items are labelled READING_CHOICE and never pooled with errors. item_id = sha1(system + '|' + normalised_text + '|' + candidate_fol)[:16]. Strata: word count (<12, 12-19, ≥20), quantifier count, nesting depth, number of conditions (antecedent/restrictor conjuncts), exception markers. INVARIANCE SET: for 150 CORRECT items (sha1-first), deterministic STRICT rewrites with seed 0: predicate/constant renaming to synonyms of equal arity, conjunct reordering, De Morgan, prenex, contrapositive. Each candidate reports its false-alarm rate per rewrite family. PRE-REGISTERED SELECTION RULE (fixed now, applied in iteration 2 on joined per-item scores). Gates: coverage ≥90% of track-L items scored (failures count as 'flagged'); rewrite false-alarm rate ≤10% per rewrite family at the candidate's pre-registered operating threshold; marginal cost ≤$0.002 per item. D is a baseline and exempt from the cost gate. Primary measure: AUROC on track-L CORRECT-vs-ERROR items (UNCERTAIN excluded), with a paired bootstrap (2,000 resamples, clustered by sentence). A candidate SURVIVES if (i) AUROC ≥0.65 and (ii) the cross-fitted logistic model of [disguised cheap judge + candidate] beats the judge alone with a ΔAUROC 95% CI lower bound >0. Rank survivors by AUROC. Candidates within 0.03 AUROC of the top survivor also advance. Ties are broken by AUROC on track-L items with ≥3 conditions or ≥20 words, and failing that by cost. If NO candidate survives (ii) but D's AUROC ≥0.75, candidate D (disguised cheap judge) is declared the survivor and iteration 2 goes deep on it. If nothing reaches 0.65, iteration 2 moves sideways to the error class where one layer does show precision ≥0.8 (a high-precision pre-filter claim). Iteration 2 re-applies the same rule under the dataset artifact's adjudicated screen labels. If the winner changes, the adjudicated ranking governs and the flip is reported. The survivor is then run ONCE, with thresholds frozen, on the held-out set from artifact E. Only that result supports the claims.",
      "artifact_directions": [
        {
          "type": "experiment",
          "objective": "Screen candidate A, FOL-Triage, on the shared frozen screen. Deliver its four reusable functions and per-layer and fused per-item scores. The functions are fol_lint(fol); content_accounting(text, fol) with a role-aware upgrade, role_accounting(text, fol); formula_role_profile(fol), exact via z3; and role_questionnaire(text), a text-only small LLM compared with the z3 profile. Also run the decomposed-judge ablation, which isolates what solver-exact answering adds.",
          "approach": "Build the SHARED SCREEN exactly as defined in the strategy rationale (same local files, fixed fol.py precedence, same labeller, same item_id, same strata, same 150-item invariance set). Emit screen_items.json with labels so iteration 2 can check the label vector is identical to the other experiments'. FREEZE BEFORE LOOKING AT TRACK-L LABELS: the L1 smell list (iter-3 probes/lint_smells.py: EXISTS_IMPL ∃x(A→B), ALL_AND ∀x(A∧B) with a pure conjunction body, IFF_RESTR, GLUE of independent claims under one block, FREE variable, ARITY clash, z3 VACUITY of a predicate, VALID/UNSAT formula, dangling universal). Also freeze the L2 rules and the L3 schema; write them into prereg.json with a timestamp before scoring track L. L1: per-smell hits. Report precision, false-alarm rate per Logic-LM system and per length stratum, and precision re-weighted to 10% and 25% prevalence. No tuning on track L: a smell above 3% false alarms on any system's CORRECT items is reported as failing, not removed. L2 bag-of-words (iter-3 content_accounting.py) is the baseline form. L2 role-aware: parse the text with spaCy or stanza UD. Extract condition-role words (if/when/who/that clauses, and generic plural or bare subjects as restrictors) and require them to be carried by predicates in DOWN (antecedent/restrictor) positions per z3 monotonicity. Add the DOWN-anchor negation polarity rule and subject/object slot order vs argument order. L3: a small cheap model on OpenRouter (pick by price; e.g. a Gemini Flash-Lite, Qwen3 or Llama-class model; ≤$0.0005/item; estimate the cost before the sweep; hard stop at $8 total) reads ONLY the sentence. It returns JSON for the fixed schema: for each content concept, condition vs asserted property; negated; exception; quantifier force (all/some/named); claim grouping; who-does-what-to-whom. formula_role_profile answers the same fields from the formula with z3 (per-predicate monotonicity, block force, variable-connectivity components, argument slots). Compare the two after a lexical alignment (stems + WordNet) and emit per-field mismatch features. GATE: measure L3 per-field accuracy against the z3 profile of CORRECT trusted-reference formulas (target ≥85%) and report it per field. Fields below 70% are excluded from fusion, and the exclusion is logged. Fusion: cross-fitted logistic regression, 5 folds grouped by sentence, fitted on track H only and then applied to track L. A second fused variant is cross-fitted within track L and reported as secondary. ABLATION, the decomposed judge: the same small LLM sees sentence + formula and answers the same schema for the formula side, replacing z3. This tells whether solver-exact answering beats an LLM reading the formula. Contamination: run L3 on nonce-disguised versions of track-L sentences (content words consistently replaced by nonce words in the text) and report the accuracy difference. Outputs (method_out.json): per-item rows {item_id, track, system, label, strata, l1_codes, l2_bow, l2_role, l3_mismatch_fields, p_fused, fired_layer, error_code, cost_usd, seconds, coverage_status}. Also report AUROC/AUPRC (paired bootstrap CIs), tie-aware pairwise accuracy for L1, per-type sensitivity on the track-H census classes, rewrite false alarms per family and cost per item. Use aii-parallel-computing for z3 (ProcessPool) and async OpenRouter calls.",
          "what_it_would_show": "If it works: 'On real LLM outputs (Logic-LM FOLIO, 3 systems), a text-free formula lint flags errors with precision ≥0.8 at ≤3% false alarms. With role-aware accounting and a text-only questionnaire answered exactly by z3, the cascade reaches AUROC ≥0.75 and adds ΔAUROC >0 (CI) over a disguised cheap LLM judge at about 1/20 of its cost. Solver-exact answering beats an LLM reading the formula (decomposed-judge ablation) by a measurable margin.' That would make FOL-Triage the survivor and the paper's headline metric, with a typed error code per flag.",
          "depends_on": []
        },
        {
          "type": "experiment",
          "objective": "Screen the two verbalise-and-entail candidates on the shared frozen screen. B1 is a deterministic, non-repairing FOL->English template verbaliser with bidirectional NLI against the source (alternate 3). B2 has z3 build small worlds that separate the candidate from its own typed single-edit mutants; each world is verbalised and a small NLI model or text-only small LLM judges its consistency with the text (alternate 1). Both are aimed at coverage and COMPOUND errors, which role fields miss.",
          "approach": "Build the SHARED SCREEN exactly as defined in the strategy rationale (identical files, labeller, item_id, strata, invariance set) and emit screen_items.json. B1: write verbalize(fol) → English with fixed templates. It must NOT repair: ∃x(A→B) is rendered literally as 'there is something such that if it is A then it is B'. Predicate names are split from camelCase, arguments are kept in slot order and constants are kept as names. Run NLI on the GPU pod with a strong off-the-shelf model (e.g. MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli, with a second checkpoint as a robustness check). Compute P(entail | text ⇒ verbalisation) and P(entail | verbalisation ⇒ text). Scores: min of the two; each direction separately (text→formula fails for DROP, formula→text fails for ADD); and P(contradiction). B2: for each candidate φ, generate typed single-edit mutants with the census operators (NEG, REV, QUANT, RESTR, CONN, DROP of a conjunct/condition, SWAP of arguments, SCOPE), about 6-12 per item, sha1-seeded. For each mutant ψ non-equivalent to φ, ask z3 for a small model M ⊨ φ∧¬ψ and M' ⊨ ψ∧¬φ over a finite domain of ≤4 named individuals. Verbalise M restricted to the predicates in φ as a short situation description ('There are three things. a is a vaccine and is effective...'). A text-only judge decides 'is the sentence TRUE in this situation?'. First the NLI model (premise = situation, hypothesis = sentence). Second, a cheap OpenRouter model given only sentence + situation, never the formula, on a capped subset (≤$4). Score = the fraction of distinguishing worlds where the judge's truth value disagrees with φ's truth value in that world. A faithful φ should be judged true in its own worlds and false where it is false. GATE: judge accuracy on worlds built from CORRECT trusted-reference formulas (truth known exactly), target ≥85%, reported by length stratum. If NLI falls below 70% on ≥20-word sentences, record that and use the LLM judge variant as the primary B2 score. Contamination: rerun B1/B2 on nonce-disguised items (consistent renaming in text and formula). Report coverage (formulas z3 cannot build worlds for count as failures) and cost per item (NLI GPU seconds and $ for the LLM variant). Outputs (method_out.json): per-item rows {item_id, track, system, label, strata, b1_min, b1_t2f, b1_f2t, b1_contra, b2_mismatch_nli, b2_mismatch_llm (subset), n_worlds, coverage_status, cost_usd, seconds}. Also AUROC/AUPRC with paired bootstrap CIs, per-census-type sensitivity on track H, rewrite false alarms per family, and the world-judging accuracy table by stratum. Stay under $10 OpenRouter; estimate before each sweep.",
          "what_it_would_show": "If it works: 'Judging the source sentence's truth in solver-built worlds that separate a candidate from its mutants detects real LLM errors with AUROC ≥0.75, including COMPOUND restructurings, with no gold and no large LLM. Template verbalisation plus bidirectional NLI catches coverage errors (dropped or added conditions) that bag-of-words accounting misses (sensitivity ≥0.6 on ADD/DROP vs 0.32).' That would give the paper a behavioural, type-agnostic detector that can beat the role-field approach on the error mass the census says dominates.",
          "depends_on": []
        },
        {
          "type": "experiment",
          "objective": "Screen candidate C, cross-system agreement by minimal typed repair: a candidate's error score is its minimal-typed-repair distance, modulo vocabulary alignment, to the medoid of diverse systems' outputs for the same sentence. Screen the required sampling self-consistency baseline (K=5 same-model samples) alongside it. Measure the shared-blind-spot rate that bounds any consensus metric.",
          "approach": "Build the SHARED SCREEN exactly as defined in the strategy rationale and emit screen_items.json. Generate PEER translations for every track-L sentence's story context (FOLIO-validation stories; about 203 stories). Use 6 diverse families on OpenRouter, distinct from the 3 Logic-LM systems where possible (e.g. Llama-3.3-70B, Qwen3, DeepSeek-V3.x, Mistral, Gemini Flash, a GPT-4.1-mini/nano-class model; choose cheap current endpoints), one few-shot prompt in Logic-LM's 'FOL ::: NL' format, temperature 0. Estimate the cost first; about 203 stories × 6 ≈ 1.2k calls is well under $5. Parse with the shared fol.py. Unparseable peers are excluded from the medoid but counted. The 3 Logic-LM systems plus the 6 peers give up to 9 outputs per sentence. The candidate being scored is left out of its own reference pool. SCORES: (1) eq_frac = the fraction of other outputs equivalent to the candidate modulo vocabulary alignment (reuse equivalent_modulo_vocab from repair_census.py); (2) medoid distance: pick as medoid the output with the most equivalence-modulo-vocab partners, then the minimal-typed-repair depth from candidate to medoid (0, 1, 2, or 3 = COMPOUND/none) and the repair operators as the error-type prediction; (3) a cluster-entropy score over equivalence classes. SELF-CONSISTENCY BASELINE: K=5 samples at T=0.7 from ONE cheap model per sentence; score = the fraction of samples equivalent modulo vocab to the candidate. DIAGNOSTICS: shared-blind-spot rate = the fraction of track-L ERROR items where the medoid is itself non-equivalent to the reference in the same way (same repair operators). Also report medoid correctness against the reference by stratum and by census type, and the error-type agreement between the predicted repair operators and the reference-derived operators on track-L errors. Also run the peers on the track-H sentences (FOLIO conclusions + MALLS-test 100) so that the human original gold can be scored the same way. Release all peer outputs as a file: they are real multi-family LLM outputs for iteration 2, labelled by the same labeller against the trusted reference, which also gives a larger real-LLM error sample. Outputs (method_out.json): per-item rows {item_id, track, system, label, strata, eq_frac, medoid_depth, medoid_ops, cluster_entropy, sc5_eq_frac, n_peers_parsed, coverage_status, cost_usd}. Also AUROC/AUPRC with paired bootstrap CIs, per-type sensitivity, rewrite false alarms (a renamed candidate should stay equivalent modulo vocab) and cost. Keep OpenRouter spend under $10, tracked after every call.",
          "what_it_would_show": "If it works: 'Without reading the text at all, a candidate's typed-repair distance to the cross-family consensus predicts real errors with AUROC ≥0.75. The repair operators name the error type correctly for most single-operator errors, and families share a blind spot on only a measured minority of errors (e.g. <25%).' That would make a text-free, solver-labelled consensus metric the survivor. If it fails, the shared-blind-spot rate itself becomes a paper result: consensus is structurally capped because LLM families make the same errors.",
          "depends_on": []
        },
        {
          "type": "experiment",
          "objective": "Screen candidate D, the 'structure adds nothing' null: a DISGUISED cheap LLM judge (sentence + formula, content words and predicate/constant names consistently replaced by nonce words), and compute on the shared screen every baseline the user requires. These are parse rate, the user's pilot structural metrics adapted to FOL, round-trip (verbalise→compare, and re-formalise→z3 equivalence), an undisguised cheap judge and a strong judge on a stratified subsample. This sets the bar every other candidate must add signal over, and measures contamination.",
          "approach": "Build the SHARED SCREEN exactly as defined in the strategy rationale and emit screen_items.json. DISGUISE: a deterministic, sha1-seeded mapping that replaces each content lemma in the text AND the matching predicate/constant name in the formula with a pronounceable nonce word (consistent within the item, arity and argument order preserved). Logic words, quantifier words and function words are untouched. Audit 30 items by hand-style checks (script assertions) that the mapping is consistent. JUDGES: a cheap judge (e.g. a Gemini Flash-Lite, GPT-4.1-nano/mini or Qwen3 class model; ≤$0.0005/item) on ALL track-L and track-H items, both undisguised and disguised. It returns P(faithful) through a fixed rubric prompt and logprobs or a 0-100 score, plus an error-type label from the census list. A strong judge (a frontier model; choose by price) runs on a 300-item stratified subsample (stratified by label × length stratum), undisguised and disguised. Estimate costs before the sweeps and keep the total under $10. ROUND-TRIP: the cheap model verbalises the formula into English. The scores are NLI entailment in both directions vs the source (DeBERTa-v3-large NLI on GPU) and sentence-embedding cosine (e.g. all-mpnet-base-v2). Also re-formalise the verbalisation with the same cheap model and test z3 equivalence modulo vocab to the candidate. PILOT STRUCTURAL METRICS: read the user's pilot (unzip /ai-inventor/aii_data/runs/run_u75jRHUss0zo/user_uploads/dpv_pilot_study.zip into the workspace; metric1 load warnings, metric2 shape/arity consistency, metric3 dangling references) and adapt them to per-sentence FOL within a story. The adaptations are joint-load conflicts (z3 satisfiability of the story's formulas together with the candidate), arity consistency across the story, predicates used in the candidate but never used elsewhere in the story, and rerun Jaccard of predicate sets. Rerun Jaccard needs a second generation; use the Logic-LM systems as each other's 'rerun' proxy and log that this is a proxy. PARSE RATE: a binary score. CONTAMINATION: for each judge, AUROC on original vs disguised items with a paired bootstrap; a significant drop on disguised items is evidence that memorised gold helped. Outputs (method_out.json): per-item rows {item_id, track, system, label, strata, parse_ok, pilot_joint_conflict, pilot_arity_incons, pilot_dangling, pilot_rerun_jacc, rt_nli_min, rt_embed_cos, rt_reformalise_eq, judge_cheap_orig, judge_cheap_disg, judge_cheap_type, judge_strong_orig, judge_strong_disg (subset), cost_usd, seconds}. Also AUROC/AUPRC per baseline with paired bootstrap CIs, the best cross-fitted baseline combination (grouped 5-fold logistic regression) and its AUROC, the contamination deltas, the per-type sensitivity of the judges' type labels on track H, rewrite false alarms and cost per item.",
          "what_it_would_show": "If it works (i.e. the null wins): 'A cheap LLM judge on disguised items, so memorised gold cannot help, detects real NL->FOL errors with AUROC within 0.03 of a frontier judge at <5% of its cost. Neither parse rate, the pilot structural metrics nor round-trip similarity adds signal to it.' That is either the paper's baseline bar or, if no structured candidate beats it, its honest headline. In both cases the paper gets the first contamination-controlled judge measurement on corrected FOLIO gold, and the answer to whether the user's pilot metrics track faithfulness at all.",
          "depends_on": []
        },
        {
          "type": "dataset",
          "objective": "Build and label the HELD-OUT confirmation set that the screen never touches. Its core is long, heavily conditioned sentences plus fresh outputs from ≥8 LLM families, labelled against a trusted reference with 3-family panel adjudication, so the iteration-2 survivor can be confirmed once, with thresholds frozen. As a secondary deliverable, adjudicate the screen's uncertain labels (VOCAB/GRAN-borderline and COMPOUND items, plus a 20% random sample), so iteration 2 can re-rank the screen under clean labels.",
          "approach": "SENTENCES, all disjoint from the screen (FOLIO-validation and MALLS-test are EXCLUDED; check by normalised-text hash). (1) LONG STRATUM: from yuan-yang/MALLS-v0 MALLS-v0.1-train (local copy at /ai-inventor/aii_data/runs/run_u75jRHUss0zo/iter_3/gen_hypo/claude_agent/data/yuan-yang__MALLS-v0__MALLS-v0.1-train.json), take a stratified sample of 450: 200 with ≥25 words and ≥3 conditions, 150 with 20-24 words and ≥3 conditions, and 100 with genuine exception markers. Only 72 items contain unless/except/excluding, so take all of them and fill the rest with 'but not' and 'without'; the marker type is recorded as metadata. (2) SHORT/MID CONTROL: 150 FOLIO-train premises where original FOLIO gold (tasksource/folio) and yfxiao/folio-refined gold are z3-equivalent modulo alignment (a trusted reference), stratified by length. TOTAL about 600 sentences. REFERENCE LABELS: MALLS GPT-4 gold is noisy, so for each long sentence the panel first audits the gold (see below). Items whose gold is judged wrong get a panel-corrected reference only if 2 of 3 panel models produce mutually z3-equivalent formulas; otherwise the item is marked NO_TRUSTED_REFERENCE and kept with that flag. CANDIDATES: ≥8 distinct model families on OpenRouter, from small to frontier (e.g. Llama-3.x-8B/70B, Qwen3, Mistral, DeepSeek, Gemma-3, Phi-4, a GPT-4.1/5-mini class model, a Gemini Flash class model). Use one few-shot prompt, plus a zero-shot variant for 2 families. Use ccg2lambda outputs (HF kenken6696/folio_by_ccg2lambda) for any FOLIO-train overlap. Estimate the cost per family before generating; about 600 × 9 ≈ 5.4k calls at cheap rates. Budget ≤$5 for generation, and use a frontier generator on a 200-item subset only. LABELLING PIPELINE, using the shared labeller: iter-3 probes/fol.py with the ⊕/→ precedence fixed, and repair_census.py (equivalent_modulo_vocab, minimal_typed_repair). The steps are z3 equivalence to the reference → equivalence modulo vocabulary → minimal typed repair (depth ≤2) → the class labels CORRECT / ERROR(op list) / VOCAB_GRAN / COMPOUND / UNPARSEABLE / TIMEOUT_UNKNOWN. ADJUDICATION PANEL: 3 families disjoint from every generator where possible and from the screen's judges (e.g. a Claude Sonnet class, Grok-fast class and GLM class model; confirm current OpenRouter ids and prices). The panel sees disguised items (nonce renaming) and answers 'is the candidate faithful to the sentence; if not, which census operator'. CALIBRATION GATE first: 60 known-label items (typed perturbations of trusted gold, split by DOWN vs UP position, plus 20 STRICT rewrites). Report panel per-model accuracy and drop any panel model below 80%. The panel adjudicates all VOCAB_GRAN and COMPOUND items plus a 20% random sample of CORRECT/ERROR items, which gives the automatic labeller's precision and recall against the panel. Majority vote; unresolved items are marked CONTESTED. SCREEN AUDIT (secondary): rebuild the screen's track-L and track-H items exactly as defined in the strategy (same files, labeller and item_id), and run the same panel on their VOCAB/GRAN, COMPOUND and a 20% sample. Emit screen_adjudicated_labels.json keyed by item_id. Budget: about 1.5k-2.5k panel calls, ≤$4; hard stop at $9.5 total, tracked after every call. SCHEMA: rows {input: {text, candidate_fol, reference_fol, system, prompt_variant}, output: final_label, metadata_fold: 'heldout' | 'screen_audit', auto_label, repair_ops, panel_votes, gold_audit_flag, strata {words, n_quant, depth, n_conditions, exception_type}, disguised_text, disguised_fol, item_id}. Report counts of ERROR and CORRECT per length/condition stratum. Stratum testability (≥50 errors AND ≥50 correct) is declared in the dataset card before any metric is run. Also report the gold-error rate of MALLS-train long items, the correct-but-not-equivalent rate and the automatic labeller's precision and recall vs the panel. Standardise to full/mini/preview JSON with aii-json.",
          "what_it_would_show": "If it works: 'We release a 600-sentence × ≥8-family NL->FOL meta-evaluation set with panel-adjudicated labels, powered in the long, heavily conditioned stratum (≥50 errors and ≥50 correct outputs per stratum). It shows that X% of MALLS GPT-4 gold for long conditioned sentences is wrong, that the automatic modulo-vocabulary labeller has precision/recall P/R against the panel, and that Y% of non-equivalent LLM outputs are correct-but-not-equivalent.' That quantifies label bias as the user asked, and makes the survivor's held-out confirmation in iteration 2 possible with no new labelling. The screen audit tells whether the screen's ranking survives clean labels.",
          "depends_on": []
        }
      ],
      "expected_outcome": "After this iteration: (1) four candidate experiments' per-item scores on ONE frozen, identically-keyed real-error screen. The primary track is released Logic-LM FOLIO outputs from 3 LLM systems scored against trusted references; the secondary track is 99 real annotator errors with known fixes. Each candidate reports AUROC/AUPRC with paired-bootstrap CIs, per-type sensitivity, rewrite false alarms, coverage with failures in the denominator, cost, and descriptive complexity breakdowns. (2) All required baselines and a contamination-controlled disguised judge on the same items. (3) A held-out, panel-adjudicated confirmation set (about 600 sentences × ≥8 families, long, heavily conditioned stratum powered by construction) and adjudicated labels for the screen's uncertain items. In iteration 2, an EVALUATION artifact joins the four experiments by item_id, verifies their label vectors are identical and applies the pre-registered selection rule, first on automatic labels and then on adjudicated labels (the adjudicated ranking governs). It names the survivor, or ties within 0.03 AUROC, as the candidate that adds ΔAUROC >0 (CI) over the disguised cheap judge. The survivor is then run ONCE, with frozen thresholds, on the held-out set. Nothing is claimed as a finding until that confirmation. Expected ranking going in, stated so a surprise is visible: A's L1 is a high-precision component, B2 or C is most likely to carry the coverage and COMPOUND mass, and D is a strong bar. The most likely final metric is a fused cascade of the survivor with L1 on top. If D survives alone, the paper's honest headline becomes 'a disguised cheap judge is enough; structure adds X only in the long stratum', and that is reported.",
      "summary": "Wide-screen first iteration. Four experiments score four genuinely different gold-free faithfulness mechanisms on one frozen, identically-keyed set of real NL->FOL errors (Logic-LM FOLIO outputs against corrected or double-annotated references, plus real annotator errors). The mechanisms: (A) FOL-Triage lint + roles + text-only questionnaire vs z3; (B) verbalise-and-entail and solver-built worlds judged against the text; (C) cross-family consensus by typed-repair distance; (D) a disguised cheap judge, together with all required baselines and a contamination check. A pre-registered rule applies: AUROC ≥0.65 plus ΔAUROC CI >0 over the disguised judge, 0.03 tie margin, with gates on coverage, invariance and cost. In parallel, a dataset artifact builds and panel-labels a held-out, long-conditioned, 8-family confirmation set and adjudicates the screen's uncertain labels. Iteration 2 therefore selects the survivor under clean labels and confirms it once on unseen evidence."
    }
  ]
}
```

### [19] TOOL RESULT — Write · 2026-09-23 12:53:41 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_strat/gen_strat_1/.terminal_claude_agent_struct_out.json", "content": "{\n  \"strategies\": [\n    {\n      \"title\": \"Five ways to catch bad logic, one scoreboard\",\n      \"domain_reasoning\": \"FIELD: meta-evaluation of reference-free (gold-free) quality metrics, applied to neuro-symbolic text-to-logic (NL->FOL autoformalization). It borrows its norms from semantic-parsing and summarization-factuality evaluation, and from the MT-metrics shared tasks. The first reasoning below is from what I read. PRINCIPLES. (i) A metric is only as credible as its meta-evaluation labels. The neurosymbolic handbook's critical rule is never to score on FOLIO/MALLS as shipped: about 39%/36% of the gold is wrong (arXiv 2606.02837), so which labels were used must be stated. Our own run found residual errors even in the CORRECTED gold (vaccine ∃x(A→B)) and an aligner that errs in both directions (iter-3 census_audit.md). (ii) Compilation, typecheck or 'parses' is not faithfulness (handbook: 2604.19459, 2606.16541); a formula can be provable and still encode a different claim. (iii) Gold-free round-trip certification is an OCCUPIED lane (2604.25031), so round-trip is a baseline here, not a contribution. Still argued: whether an agreed gold-free faithfulness number can exist at all (handbook open question 3), and whether LLM judges are trustworthy on public, contaminated benchmarks. WHAT COUNTS AS CONVINCING. The factual-consistency literature settled on item-level binary labels, scored threshold-free with ROC AUC. TRUE (Honovich et al., NAACL 2022) moved away from system-level correlations precisely because those 'leave the example-level accuracy of such metrics unclear'. Credibility comes from REAL system outputs, not synthetic perturbations: Goyal & Durrett 2021 and FRANK showed synthetic errors do not match real ones, and the user states this outright. Beyond that, a new metric must show INCREMENTAL signal over the obvious baselines, i.e. a paired comparison on the same items, not a standalone AUROC. MT-metric meta-evaluation (Deutsch, Foster & Freitag, EMNLP 2023, 'Ties Matter') adds a rule: quantized or binary metrics must be compared with tie-aware pairwise accuracy or tie calibration. Otherwise a lint that returns 0/1 is unfairly penalized or rewarded against a continuous judge. STANDARD MOVES AND WHAT EACH RULES OUT. Paired bootstrap on the same items rules out item-difficulty differences between metrics. A held-out confirmation set rules out selection-on-the-screen (winner's curse). Disguised items (entities renamed) rule out memorised-gold contamination for LLM judges. Invariance tests (renaming, reordering, De Morgan) rule out a metric that tracks surface form. Stratifying by length and conditions rules out 'works only on short sentences'. Adjudicating uncertain labels with a family-disjoint panel rules out label noise that masquerades as metric error. Counting unparseable outputs in the denominator rules out survivorship. USUAL FAILURE MODES. (1) Validating on synthetic perturbations and claiming real-error detection. (2) Tuning thresholds on the evaluation set: the iter-3 L1 numbers are in-sample, and precision falls from 0.84 to 0.64 as prevalence drops from 25% to 10%. (3) Label artefacts: aligner over- and under-acceptance, and parser precedence bugs (fol.py gives ⊕ lower precedence than →, which created 3 false COMPOUNDs). (4) Correct-but-not-equivalent outputs labelled as errors. (5) An untuned or unfair judge baseline, or a judge given the answer key through contamination. (6) Long, heavily conditioned strata too small to test, with results reported anyway. (7) Precision reported without its prevalence. Handbook do-not-redo list: bare translators, round-trip certification, per-step premise attestation. The open wedge is a gold-free, real-error-validated metric with a typed error readout. Provisional: typed-repair error classification has KR-2026 prior art (Vehlken/Zeume 2602.19673, typed bug-fixing edits on student FOL). The census is therefore a methodology borrowing, not a claimed first.\",\n      \"principle_alignment\": \"FOLLOWS. (1) Real outputs only for the headline measure. The screen uses released Logic-LM FOLIO-dev outputs from three real LLM systems, plus real human annotator errors with known fixes. Synthetic perturbations and rewrites are used only as secondary per-type sensitivity and invariance readouts, never as the selection measure. (2) The labels are stated and conservative. The primary label set is the TRUSTED-REFERENCE subset: conclusions with 2606.02837 corrected gold, and premises where two independent annotations (original FOLIO and yfxiao/folio-refined) are z3-equivalent after alignment. Everything else is secondary. One shared labeller is used everywhere (iter-3 fol.py with the ⊕/→ precedence bug fixed, plus repair_census.py). (3) Item-level AUROC is the primary measure, computed on the same items for every candidate, with paired bootstrap. Tie-aware pairwise accuracy is reported alongside for binary metrics (Ties Matter). (4) Incremental value over the judge is required, not a standalone score: the selection rule demands a ΔAUROC CI over the disguised cheap judge. (5) Contamination is controlled with disguised (nonce-renamed) items for every LLM-using candidate. (6) Unparseable outputs count in the denominator. (7) The selection rule is fixed in advance, and a held-out confirmation set (different sentences and a different corpus stratum: MALLS-train long and conditioned, FOLIO-train premises, fresh outputs from 8 LLM families) is labelled in parallel and never touched by the screen. DELIBERATELY BROKEN. (a) The field would first build one frozen dataset artifact and make every experiment depend on it. We cannot: nothing exists yet and all artifacts run in parallel. Each experiment therefore rebuilds the SAME frozen screen deterministically, from identical local files, with identical code, sha1-sorted item ids and seed 0. Each writes per-item scores keyed by the same item_id, so iteration 2's evaluation can join them exactly and verify that the label vectors are byte-identical. (b) The screen's labels are automatic, not panel-adjudicated. A wide screen needs the same labels for all candidates now. Adjudication (panel relabelling of the screen's VOCAB/GRAN/COMPOUND items) is done in parallel by the dataset artifact, and iteration 2 re-ranks under adjudicated labels; a rank flip under adjudication is reported, not hidden. (c) The long, heavily conditioned stratum is NOT testable on the screen (FOLIO has about 19 such premises), which breaks 'test where the user cares most' for this iteration. That stratum is reserved for the held-out set, where it is powered (≥50 errors and ≥50 correct outputs per stratum by construction). (d) Screen depth is coarse by design (no hyperparameter search, one prompt per LLM component). This is the wide-screen trade: a candidate that loses narrowly (<0.03 AUROC) is carried forward, not killed.\",\n      \"objective\": \"Put all five candidate answers to 'a gold-free metric that predicts NL->FOL faithfulness and names the error type' in play, on IDENTICAL real-error evidence with an identical pre-registered measure, then select the survivor(s) that earn iteration 2's depth. The five: (A) FOL-Triage (text-free formula lint + LLM-free role accounting + text-only small-LLM role questionnaire answered exactly by z3); (B) verbalise-and-entail, in two variants: template verbalisation with bidirectional NLI, and solver-built distinguishing worlds judged against the text; (C) cross-system agreement by minimal-typed-repair distance to the medoid; (D) the disguised cheap LLM judge, i.e. the 'structure adds nothing' null, together with every required baseline. In parallel, (E) builds and labels the held-out confirmation set, whose core is the long, heavily conditioned stratum and fresh outputs from 8 LLM families, so the survivor can be confirmed there in iteration 2 without new labelling work. It also adjudicates the screen's uncertain labels.\",\n      \"rationale\": \"This is the first invention-loop iteration. The hypothesis carries a main candidate plus four alternates that answer the same ask by genuinely different mechanisms: structure without text (L1), text roles with a solver (L2/L3), behavioural truth in concrete worlds (B2), entailment on verbalisations (B1), consensus across systems (C) and a disguised judge (D). They can disagree. If errors are idiosyncratic across families, C wins. If small LLMs already see ∃x(A→B) and dropped conditions, D wins and structure adds nothing. If NLI handles templated logic, B1 wins on coverage errors (57% of repairable real errors), where bag-of-words L2 failed (AUROC 0.59). The in-step evidence for A comes only from annotator errors, and it is in-sample (the review showed precision 0.64 at 10% prevalence), so A has not earned a deep test yet. The cheapest real-LLM-output evidence already exists: Logic-LM's released FOLIO-dev outputs from gpt-3.5-turbo, gpt-4 and text-davinci-003. Their conclusions are exactly the 202 FOLIO-validation conclusions for which 2606.02837 supplies corrected gold, and those files are already on disk from iter-3 probes. So all four candidate experiments can be screened on real LLM errors with a trusted reference at almost zero data cost, and every LLM dollar goes to the candidates themselves. Screening on the human-annotator track as well lets iteration 2 see whether a candidate's ranking transfers from annotator errors to LLM errors. That is the main risk named in the hypothesis's assumptions. The held-out set with 8 families is labelled in parallel because confirmation needs labels nobody has yet. Without it the survivor could not be confirmed in iteration 2, and the long-stratum claim the user cares most about would never be tested. SHARED SCREEN DEFINITION (every experiment must implement it identically). Local inputs are read-only files in /ai-inventor/aii_data/runs/run_u75jRHUss0zo/iter_3/gen_hypo/claude_agent/data/: DSAVlab-UNIUD_FOLIO_validation-curated__FOLIO_instances.jsonl, DSAVlab-UNIUD_MALLS_test_subset-CURATED__MALLS_instances.jsonl, folio_refined_validation.csv and yuan-yang__MALLS-v0__MALLS-v0.1-test.json. The parser and labeller are in iter_3/gen_hypo/claude_agent/probes/fol.py and repair_census.py; copy them and fix the ⊕-vs-→ precedence (⊕ must bind like ∨, tighter than →) before any labelling. Also fetch the Logic-LM released outputs from github teacherpeterpan/Logic-LLM: outputs/logic_programs/FOLIO_dev_{gpt-3.5-turbo,gpt-4,text-davinci-003}.json ('FOL ::: NL' lines). TRACK L (LLM outputs, PRIMARY): each Logic-LM (system, sentence, FOL) triple, where the sentence matches, after whitespace/case/punctuation normalisation, either a curated FOLIO-validation conclusion (reference = corrected gold) or a FOLIO-validation premise whose original gold and folio-refined gold are z3-equivalent after alignment (reference = that agreed formula). Label: CORRECT if the candidate is equivalent to the reference modulo vocabulary alignment; ERROR if it is not and the minimal typed repair search finds ≤2 operators; UNCERTAIN if it is VOCAB/GRAN-borderline or COMPOUND (no repair at depth ≤2), reported separately; UNPARSEABLE is counted in the denominator and scored as the metric's own coverage failure. TRACK H (human annotator errors, SECONDARY): the 302 curated items, original gold as candidate and corrected gold as reference. Ambiguity-flagged items are labelled READING_CHOICE and never pooled with errors. item_id = sha1(system + '|' + normalised_text + '|' + candidate_fol)[:16]. Strata: word count (<12, 12-19, ≥20), quantifier count, nesting depth, number of conditions (antecedent/restrictor conjuncts), exception markers. INVARIANCE SET: for 150 CORRECT items (sha1-first), deterministic STRICT rewrites with seed 0: predicate/constant renaming to synonyms of equal arity, conjunct reordering, De Morgan, prenex, contrapositive. Each candidate reports its false-alarm rate per rewrite family. PRE-REGISTERED SELECTION RULE (fixed now, applied in iteration 2 on joined per-item scores). Gates: coverage ≥90% of track-L items scored (failures count as 'flagged'); rewrite false-alarm rate ≤10% per rewrite family at the candidate's pre-registered operating threshold; marginal cost ≤$0.002 per item. D is a baseline and exempt from the cost gate. Primary measure: AUROC on track-L CORRECT-vs-ERROR items (UNCERTAIN excluded), with a paired bootstrap (2,000 resamples, clustered by sentence). A candidate SURVIVES if (i) AUROC ≥0.65 and (ii) the cross-fitted logistic model of [disguised cheap judge + candidate] beats the judge alone with a ΔAUROC 95% CI lower bound >0. Rank survivors by AUROC. Candidates within 0.03 AUROC of the top survivor also advance. Ties are broken by AUROC on track-L items with ≥3 conditions or ≥20 words, and failing that by cost. If NO candidate survives (ii) but D's AUROC ≥0.75, candidate D (disguised cheap judge) is declared the survivor and iteration 2 goes deep on it. If nothing reaches 0.65, iteration 2 moves sideways to the error class where one layer does show precision ≥0.8 (a high-precision pre-filter claim). Iteration 2 re-applies the same rule under the dataset artifact's adjudicated screen labels. If the winner changes, the adjudicated ranking governs and the flip is reported. The survivor is then run ONCE, with thresholds frozen, on the held-out set from artifact E. Only that result supports the claims.\",\n      \"artifact_directions\": [\n        {\n          \"type\": \"experiment\",\n          \"objective\": \"Screen candidate A, FOL-Triage, on the shared frozen screen. Deliver its four reusable functions and per-layer and fused per-item scores. The functions are fol_lint(fol); content_accounting(text, fol) with a role-aware upgrade, role_accounting(text, fol); formula_role_profile(fol), exact via z3; and role_questionnaire(text), a text-only small LLM compared with the z3 profile. Also run the decomposed-judge ablation, which isolates what solver-exact answering adds.\",\n          \"approach\": \"Build the SHARED SCREEN exactly as defined in the strategy rationale (same local files, fixed fol.py precedence, same labeller, same item_id, same strata, same 150-item invariance set). Emit screen_items.json with labels so iteration 2 can check the label vector is identical to the other experiments'. FREEZE BEFORE LOOKING AT TRACK-L LABELS: the L1 smell list (iter-3 probes/lint_smells.py: EXISTS_IMPL ∃x(A→B), ALL_AND ∀x(A∧B) with a pure conjunction body, IFF_RESTR, GLUE of independent claims under one block, FREE variable, ARITY clash, z3 VACUITY of a predicate, VALID/UNSAT formula, dangling universal). Also freeze the L2 rules and the L3 schema; write them into prereg.json with a timestamp before scoring track L. L1: per-smell hits. Report precision, false-alarm rate per Logic-LM system and per length stratum, and precision re-weighted to 10% and 25% prevalence. No tuning on track L: a smell above 3% false alarms on any system's CORRECT items is reported as failing, not removed. L2 bag-of-words (iter-3 content_accounting.py) is the baseline form. L2 role-aware: parse the text with spaCy or stanza UD. Extract condition-role words (if/when/who/that clauses, and generic plural or bare subjects as restrictors) and require them to be carried by predicates in DOWN (antecedent/restrictor) positions per z3 monotonicity. Add the DOWN-anchor negation polarity rule and subject/object slot order vs argument order. L3: a small cheap model on OpenRouter (pick by price; e.g. a Gemini Flash-Lite, Qwen3 or Llama-class model; ≤$0.0005/item; estimate the cost before the sweep; hard stop at $8 total) reads ONLY the sentence. It returns JSON for the fixed schema: for each content concept, condition vs asserted property; negated; exception; quantifier force (all/some/named); claim grouping; who-does-what-to-whom. formula_role_profile answers the same fields from the formula with z3 (per-predicate monotonicity, block force, variable-connectivity components, argument slots). Compare the two after a lexical alignment (stems + WordNet) and emit per-field mismatch features. GATE: measure L3 per-field accuracy against the z3 profile of CORRECT trusted-reference formulas (target ≥85%) and report it per field. Fields below 70% are excluded from fusion, and the exclusion is logged. Fusion: cross-fitted logistic regression, 5 folds grouped by sentence, fitted on track H only and then applied to track L. A second fused variant is cross-fitted within track L and reported as secondary. ABLATION, the decomposed judge: the same small LLM sees sentence + formula and answers the same schema for the formula side, replacing z3. This tells whether solver-exact answering beats an LLM reading the formula. Contamination: run L3 on nonce-disguised versions of track-L sentences (content words consistently replaced by nonce words in the text) and report the accuracy difference. Outputs (method_out.json): per-item rows {item_id, track, system, label, strata, l1_codes, l2_bow, l2_role, l3_mismatch_fields, p_fused, fired_layer, error_code, cost_usd, seconds, coverage_status}. Also report AUROC/AUPRC (paired bootstrap CIs), tie-aware pairwise accuracy for L1, per-type sensitivity on the track-H census classes, rewrite false alarms per family and cost per item. Use aii-parallel-computing for z3 (ProcessPool) and async OpenRouter calls.\",\n          \"what_it_would_show\": \"If it works: 'On real LLM outputs (Logic-LM FOLIO, 3 systems), a text-free formula lint flags errors with precision ≥0.8 at ≤3% false alarms. With role-aware accounting and a text-only questionnaire answered exactly by z3, the cascade reaches AUROC ≥0.75 and adds ΔAUROC >0 (CI) over a disguised cheap LLM judge at about 1/20 of its cost. Solver-exact answering beats an LLM reading the formula (decomposed-judge ablation) by a measurable margin.' That would make FOL-Triage the survivor and the paper's headline metric, with a typed error code per flag.\",\n          \"depends_on\": []\n        },\n        {\n          \"type\": \"experiment\",\n          \"objective\": \"Screen the two verbalise-and-entail candidates on the shared frozen screen. B1 is a deterministic, non-repairing FOL->English template verbaliser with bidirectional NLI against the source (alternate 3). B2 has z3 build small worlds that separate the candidate from its own typed single-edit mutants; each world is verbalised and a small NLI model or text-only small LLM judges its consistency with the text (alternate 1). Both are aimed at coverage and COMPOUND errors, which role fields miss.\",\n          \"approach\": \"Build the SHARED SCREEN exactly as defined in the strategy rationale (identical files, labeller, item_id, strata, invariance set) and emit screen_items.json. B1: write verbalize(fol) → English with fixed templates. It must NOT repair: ∃x(A→B) is rendered literally as 'there is something such that if it is A then it is B'. Predicate names are split from camelCase, arguments are kept in slot order and constants are kept as names. Run NLI on the GPU pod with a strong off-the-shelf model (e.g. MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli, with a second checkpoint as a robustness check). Compute P(entail | text ⇒ verbalisation) and P(entail | verbalisation ⇒ text). Scores: min of the two; each direction separately (text→formula fails for DROP, formula→text fails for ADD); and P(contradiction). B2: for each candidate φ, generate typed single-edit mutants with the census operators (NEG, REV, QUANT, RESTR, CONN, DROP of a conjunct/condition, SWAP of arguments, SCOPE), about 6-12 per item, sha1-seeded. For each mutant ψ non-equivalent to φ, ask z3 for a small model M ⊨ φ∧¬ψ and M' ⊨ ψ∧¬φ over a finite domain of ≤4 named individuals. Verbalise M restricted to the predicates in φ as a short situation description ('There are three things. a is a vaccine and is effective...'). A text-only judge decides 'is the sentence TRUE in this situation?'. First the NLI model (premise = situation, hypothesis = sentence). Second, a cheap OpenRouter model given only sentence + situation, never the formula, on a capped subset (≤$4). Score = the fraction of distinguishing worlds where the judge's truth value disagrees with φ's truth value in that world. A faithful φ should be judged true in its own worlds and false where it is false. GATE: judge accuracy on worlds built from CORRECT trusted-reference formulas (truth known exactly), target ≥85%, reported by length stratum. If NLI falls below 70% on ≥20-word sentences, record that and use the LLM judge variant as the primary B2 score. Contamination: rerun B1/B2 on nonce-disguised items (consistent renaming in text and formula). Report coverage (formulas z3 cannot build worlds for count as failures) and cost per item (NLI GPU seconds and $ for the LLM variant). Outputs (method_out.json): per-item rows {item_id, track, system, label, strata, b1_min, b1_t2f, b1_f2t, b1_contra, b2_mismatch_nli, b2_mismatch_llm (subset), n_worlds, coverage_status, cost_usd, seconds}. Also AUROC/AUPRC with paired bootstrap CIs, per-census-type sensitivity on track H, rewrite false alarms per family, and the world-judging accuracy table by stratum. Stay under $10 OpenRouter; estimate before each sweep.\",\n          \"what_it_would_show\": \"If it works: 'Judging the source sentence's truth in solver-built worlds that separate a candidate from its mutants detects real LLM errors with AUROC ≥0.75, including COMPOUND restructurings, with no gold and no large LLM. Template verbalisation plus bidirectional NLI catches coverage errors (dropped or added conditions) that bag-of-words accounting misses (sensitivity ≥0.6 on ADD/DROP vs 0.32).' That would give the paper a behavioural, type-agnostic detector that can beat the role-field approach on the error mass the census says dominates.\",\n          \"depends_on\": []\n        },\n        {\n          \"type\": \"experiment\",\n          \"objective\": \"Screen candidate C, cross-system agreement by minimal typed repair: a candidate's error score is its minimal-typed-repair distance, modulo vocabulary alignment, to the medoid of diverse systems' outputs for the same sentence. Screen the required sampling self-consistency baseline (K=5 same-model samples) alongside it. Measure the shared-blind-spot rate that bounds any consensus metric.\",\n          \"approach\": \"Build the SHARED SCREEN exactly as defined in the strategy rationale and emit screen_items.json. Generate PEER translations for every track-L sentence's story context (FOLIO-validation stories; about 203 stories). Use 6 diverse families on OpenRouter, distinct from the 3 Logic-LM systems where possible (e.g. Llama-3.3-70B, Qwen3, DeepSeek-V3.x, Mistral, Gemini Flash, a GPT-4.1-mini/nano-class model; choose cheap current endpoints), one few-shot prompt in Logic-LM's 'FOL ::: NL' format, temperature 0. Estimate the cost first; about 203 stories × 6 ≈ 1.2k calls is well under $5. Parse with the shared fol.py. Unparseable peers are excluded from the medoid but counted. The 3 Logic-LM systems plus the 6 peers give up to 9 outputs per sentence. The candidate being scored is left out of its own reference pool. SCORES: (1) eq_frac = the fraction of other outputs equivalent to the candidate modulo vocabulary alignment (reuse equivalent_modulo_vocab from repair_census.py); (2) medoid distance: pick as medoid the output with the most equivalence-modulo-vocab partners, then the minimal-typed-repair depth from candidate to medoid (0, 1, 2, or 3 = COMPOUND/none) and the repair operators as the error-type prediction; (3) a cluster-entropy score over equivalence classes. SELF-CONSISTENCY BASELINE: K=5 samples at T=0.7 from ONE cheap model per sentence; score = the fraction of samples equivalent modulo vocab to the candidate. DIAGNOSTICS: shared-blind-spot rate = the fraction of track-L ERROR items where the medoid is itself non-equivalent to the reference in the same way (same repair operators). Also report medoid correctness against the reference by stratum and by census type, and the error-type agreement between the predicted repair operators and the reference-derived operators on track-L errors. Also run the peers on the track-H sentences (FOLIO conclusions + MALLS-test 100) so that the human original gold can be scored the same way. Release all peer outputs as a file: they are real multi-family LLM outputs for iteration 2, labelled by the same labeller against the trusted reference, which also gives a larger real-LLM error sample. Outputs (method_out.json): per-item rows {item_id, track, system, label, strata, eq_frac, medoid_depth, medoid_ops, cluster_entropy, sc5_eq_frac, n_peers_parsed, coverage_status, cost_usd}. Also AUROC/AUPRC with paired bootstrap CIs, per-type sensitivity, rewrite false alarms (a renamed candidate should stay equivalent modulo vocab) and cost. Keep OpenRouter spend under $10, tracked after every call.\",\n          \"what_it_would_show\": \"If it works: 'Without reading the text at all, a candidate's typed-repair distance to the cross-family consensus predicts real errors with AUROC ≥0.75. The repair operators name the error type correctly for most single-operator errors, and families share a blind spot on only a measured minority of errors (e.g. <25%).' That would make a text-free, solver-labelled consensus metric the survivor. If it fails, the shared-blind-spot rate itself becomes a paper result: consensus is structurally capped because LLM families make the same errors.\",\n          \"depends_on\": []\n        },\n        {\n          \"type\": \"experiment\",\n          \"objective\": \"Screen candidate D, the 'structure adds nothing' null: a DISGUISED cheap LLM judge (sentence + formula, content words and predicate/constant names consistently replaced by nonce words), and compute on the shared screen every baseline the user requires. These are parse rate, the user's pilot structural metrics adapted to FOL, round-trip (verbalise→compare, and re-formalise→z3 equivalence), an undisguised cheap judge and a strong judge on a stratified subsample. This sets the bar every other candidate must add signal over, and measures contamination.\",\n          \"approach\": \"Build the SHARED SCREEN exactly as defined in the strategy rationale and emit screen_items.json. DISGUISE: a deterministic, sha1-seeded mapping that replaces each content lemma in the text AND the matching predicate/constant name in the formula with a pronounceable nonce word (consistent within the item, arity and argument order preserved). Logic words, quantifier words and function words are untouched. Audit 30 items by hand-style checks (script assertions) that the mapping is consistent. JUDGES: a cheap judge (e.g. a Gemini Flash-Lite, GPT-4.1-nano/mini or Qwen3 class model; ≤$0.0005/item) on ALL track-L and track-H items, both undisguised and disguised. It returns P(faithful) through a fixed rubric prompt and logprobs or a 0-100 score, plus an error-type label from the census list. A strong judge (a frontier model; choose by price) runs on a 300-item stratified subsample (stratified by label × length stratum), undisguised and disguised. Estimate costs before the sweeps and keep the total under $10. ROUND-TRIP: the cheap model verbalises the formula into English. The scores are NLI entailment in both directions vs the source (DeBERTa-v3-large NLI on GPU) and sentence-embedding cosine (e.g. all-mpnet-base-v2). Also re-formalise the verbalisation with the same cheap model and test z3 equivalence modulo vocab to the candidate. PILOT STRUCTURAL METRICS: read the user's pilot (unzip /ai-inventor/aii_data/runs/run_u75jRHUss0zo/user_uploads/dpv_pilot_study.zip into the workspace; metric1 load warnings, metric2 shape/arity consistency, metric3 dangling references) and adapt them to per-sentence FOL within a story. The adaptations are joint-load conflicts (z3 satisfiability of the story's formulas together with the candidate), arity consistency across the story, predicates used in the candidate but never used elsewhere in the story, and rerun Jaccard of predicate sets. Rerun Jaccard needs a second generation; use the Logic-LM systems as each other's 'rerun' proxy and log that this is a proxy. PARSE RATE: a binary score. CONTAMINATION: for each judge, AUROC on original vs disguised items with a paired bootstrap; a significant drop on disguised items is evidence that memorised gold helped. Outputs (method_out.json): per-item rows {item_id, track, system, label, strata, parse_ok, pilot_joint_conflict, pilot_arity_incons, pilot_dangling, pilot_rerun_jacc, rt_nli_min, rt_embed_cos, rt_reformalise_eq, judge_cheap_orig, judge_cheap_disg, judge_cheap_type, judge_strong_orig, judge_strong_disg (subset), cost_usd, seconds}. Also AUROC/AUPRC per baseline with paired bootstrap CIs, the best cross-fitted baseline combination (grouped 5-fold logistic regression) and its AUROC, the contamination deltas, the per-type sensitivity of the judges' type labels on track H, rewrite false alarms and cost per item.\",\n          \"what_it_would_show\": \"If it works (i.e. the null wins): 'A cheap LLM judge on disguised items, so memorised gold cannot help, detects real NL->FOL errors with AUROC within 0.03 of a frontier judge at <5% of its cost. Neither parse rate, the pilot structural metrics nor round-trip similarity adds signal to it.' That is either the paper's baseline bar or, if no structured candidate beats it, its honest headline. In both cases the paper gets the first contamination-controlled judge measurement on corrected FOLIO gold, and the answer to whether the user's pilot metrics track faithfulness at all.\",\n          \"depends_on\": []\n        },\n        {\n          \"type\": \"dataset\",\n          \"objective\": \"Build and label the HELD-OUT confirmation set that the screen never touches. Its core is long, heavily conditioned sentences plus fresh outputs from ≥8 LLM families, labelled against a trusted reference with 3-family panel adjudication, so the iteration-2 survivor can be confirmed once, with thresholds frozen. As a secondary deliverable, adjudicate the screen's uncertain labels (VOCAB/GRAN-borderline and COMPOUND items, plus a 20% random sample), so iteration 2 can re-rank the screen under clean labels.\",\n          \"approach\": \"SENTENCES, all disjoint from the screen (FOLIO-validation and MALLS-test are EXCLUDED; check by normalised-text hash). (1) LONG STRATUM: from yuan-yang/MALLS-v0 MALLS-v0.1-train (local copy at /ai-inventor/aii_data/runs/run_u75jRHUss0zo/iter_3/gen_hypo/claude_agent/data/yuan-yang__MALLS-v0__MALLS-v0.1-train.json), take a stratified sample of 450: 200 with ≥25 words and ≥3 conditions, 150 with 20-24 words and ≥3 conditions, and 100 with genuine exception markers. Only 72 items contain unless/except/excluding, so take all of them and fill the rest with 'but not' and 'without'; the marker type is recorded as metadata. (2) SHORT/MID CONTROL: 150 FOLIO-train premises where original FOLIO gold (tasksource/folio) and yfxiao/folio-refined gold are z3-equivalent modulo alignment (a trusted reference), stratified by length. TOTAL about 600 sentences. REFERENCE LABELS: MALLS GPT-4 gold is noisy, so for each long sentence the panel first audits the gold (see below). Items whose gold is judged wrong get a panel-corrected reference only if 2 of 3 panel models produce mutually z3-equivalent formulas; otherwise the item is marked NO_TRUSTED_REFERENCE and kept with that flag. CANDIDATES: ≥8 distinct model families on OpenRouter, from small to frontier (e.g. Llama-3.x-8B/70B, Qwen3, Mistral, DeepSeek, Gemma-3, Phi-4, a GPT-4.1/5-mini class model, a Gemini Flash class model). Use one few-shot prompt, plus a zero-shot variant for 2 families. Use ccg2lambda outputs (HF kenken6696/folio_by_ccg2lambda) for any FOLIO-train overlap. Estimate the cost per family before generating; about 600 × 9 ≈ 5.4k calls at cheap rates. Budget ≤$5 for generation, and use a frontier generator on a 200-item subset only. LABELLING PIPELINE, using the shared labeller: iter-3 probes/fol.py with the ⊕/→ precedence fixed, and repair_census.py (equivalent_modulo_vocab, minimal_typed_repair). The steps are z3 equivalence to the reference → equivalence modulo vocabulary → minimal typed repair (depth ≤2) → the class labels CORRECT / ERROR(op list) / VOCAB_GRAN / COMPOUND / UNPARSEABLE / TIMEOUT_UNKNOWN. ADJUDICATION PANEL: 3 families disjoint from every generator where possible and from the screen's judges (e.g. a Claude Sonnet class, Grok-fast class and GLM class model; confirm current OpenRouter ids and prices). The panel sees disguised items (nonce renaming) and answers 'is the candidate faithful to the sentence; if not, which census operator'. CALIBRATION GATE first: 60 known-label items (typed perturbations of trusted gold, split by DOWN vs UP position, plus 20 STRICT rewrites). Report panel per-model accuracy and drop any panel model below 80%. The panel adjudicates all VOCAB_GRAN and COMPOUND items plus a 20% random sample of CORRECT/ERROR items, which gives the automatic labeller's precision and recall against the panel. Majority vote; unresolved items are marked CONTESTED. SCREEN AUDIT (secondary): rebuild the screen's track-L and track-H items exactly as defined in the strategy (same files, labeller and item_id), and run the same panel on their VOCAB/GRAN, COMPOUND and a 20% sample. Emit screen_adjudicated_labels.json keyed by item_id. Budget: about 1.5k-2.5k panel calls, ≤$4; hard stop at $9.5 total, tracked after every call. SCHEMA: rows {input: {text, candidate_fol, reference_fol, system, prompt_variant}, output: final_label, metadata_fold: 'heldout' | 'screen_audit', auto_label, repair_ops, panel_votes, gold_audit_flag, strata {words, n_quant, depth, n_conditions, exception_type}, disguised_text, disguised_fol, item_id}. Report counts of ERROR and CORRECT per length/condition stratum. Stratum testability (≥50 errors AND ≥50 correct) is declared in the dataset card before any metric is run. Also report the gold-error rate of MALLS-train long items, the correct-but-not-equivalent rate and the automatic labeller's precision and recall vs the panel. Standardise to full/mini/preview JSON with aii-json.\",\n          \"what_it_would_show\": \"If it works: 'We release a 600-sentence × ≥8-family NL->FOL meta-evaluation set with panel-adjudicated labels, powered in the long, heavily conditioned stratum (≥50 errors and ≥50 correct outputs per stratum). It shows that X% of MALLS GPT-4 gold for long conditioned sentences is wrong, that the automatic modulo-vocabulary labeller has precision/recall P/R against the panel, and that Y% of non-equivalent LLM outputs are correct-but-not-equivalent.' That quantifies label bias as the user asked, and makes the survivor's held-out confirmation in iteration 2 possible with no new labelling. The screen audit tells whether the screen's ranking survives clean labels.\",\n          \"depends_on\": []\n        }\n      ],\n      \"expected_outcome\": \"After this iteration: (1) four candidate experiments' per-item scores on ONE frozen, identically-keyed real-error screen. The primary track is released Logic-LM FOLIO outputs from 3 LLM systems scored against trusted references; the secondary track is 99 real annotator errors with known fixes. Each candidate reports AUROC/AUPRC with paired-bootstrap CIs, per-type sensitivity, rewrite false alarms, coverage with failures in the denominator, cost, and descriptive complexity breakdowns. (2) All required baselines and a contamination-controlled disguised judge on the same items. (3) A held-out, panel-adjudicated confirmation set (about 600 sentences × ≥8 families, long, heavily conditioned stratum powered by construction) and adjudicated labels for the screen's uncertain items. In iteration 2, an EVALUATION artifact joins the four experiments by item_id, verifies their label vectors are identical and applies the pre-registered selection rule, first on automatic labels and then on adjudicated labels (the adjudicated ranking governs). It names the survivor, or ties within 0.03 AUROC, as the candidate that adds ΔAUROC >0 (CI) over the disguised cheap judge. The survivor is then run ONCE, with frozen thresholds, on the held-out set. Nothing is claimed as a finding until that confirmation. Expected ranking going in, stated so a surprise is visible: A's L1 is a high-precision component, B2 or C is most likely to carry the coverage and COMPOUND mass, and D is a strong bar. The most likely final metric is a fused cascade of the survivor with L1 on top. If D survives alone, the paper's honest headline becomes 'a disguised cheap judge is enough; structure adds X only in the long stratum', and that is reported.\",\n      \"summary\": \"Wide-screen first iteration. Four experiments score four genuinely different gold-free faithfulness mechanisms on one frozen, identically-keyed set of real NL->FOL errors (Logic-LM FOLIO outputs against corrected or double-annotated references, plus real annotator errors). The mechanisms: (A) FOL-Triage lint + roles + text-only questionnaire vs z3; (B) verbalise-and-entail and solver-built worlds judged against the text; (C) cross-family consensus by typed-repair distance; (D) a disguised cheap judge, together with all required baselines and a contamination check. A pre-registered rule applies: AUROC ≥0.65 plus ΔAUROC CI >0 over the disguised judge, 0.03 tie margin, with gates on coverage, invariance and cost. In parallel, a dataset artifact builds and panel-labels a held-out, long-conditioned, 8-family confirmation set and adjudicates the screen's uncertain labels. Iteration 2 therefore selects the survivor under clean labels and confirms it once on unseen evidence.\"\n    }\n  ]\n}\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [20] TOOL CALL — Bash · 2026-09-23 12:53:49 UTC

```
Add match-rate fallback and validate JSON:
python3 - <<'EOF'
import json
p='.terminal_claude_agent_struct_out.json'
d=json.load(open(p))
s=d['strategies'][0]
old="UNPARSEABLE is counted in the denominator and scored as the metric's own coverage failure."
assert old in s['rationale']
s['rationale']=s['rationale'].replace(old, old+" MATCH-RATE FALLBACK (identical in every experiment): Logic-LM FOLIO_dev comes from FOLIO v1 and the curated set from the HF validation release, so every experiment reports the match rate. If fewer than 150 distinct conclusions match, track L is extended deterministically with the premises of the matched stories whose original gold and folio-refined gold agree, and with no other source.")
json.dump(d,open(p,'w'),ensure_ascii=False,indent=2)
s=d['strategies'][0]
print(len(s['artifact_directions']), [a['type'] for a in s['artifact_directions']], all(a['what_it_would_show'] for a in s['artifact_directions']))
EOF
```

### [21] TOOL RESULT — Bash · 2026-09-23 12:53:49 UTC

```
{"stdout": "5 ['experiment', 'experiment', 'experiment', 'experiment', 'dataset'] True", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [22] ASSISTANT · 2026-09-23 12:54:09 UTC

```
Now the README, the manifest and the memory note.
```

### [23] TOOL CALL — Bash · 2026-09-23 12:54:09 UTC

```
Write manifest, README, and memory note:
cat > .aii/manifest.yaml <<'EOF'
entries: []
EOF
cat > README.md <<'EOF'
# GEN_STRAT iter 1 — run_u75jRHUss0zo (NL→FOL gold-free faithfulness metrics)

This directory is the strategy-planning step for iteration 1. It runs no code and writes no data.

## Layout
- `.terminal_claude_agent_struct_out.json`: the strategy, a wide screen with 5 artifact directions:
  - Experiment A: FOL-Triage (lint, roles, and a text-only questionnaire compared against z3).
  - Experiment B: verbalise-and-entail, and solver-built worlds judged against the text.
  - Experiment C: cross-family consensus by typed-repair distance, plus the self-consistency baseline.
  - Experiment D: a disguised cheap LLM judge, plus all required baselines and a contamination check.
  - Dataset E: a held-out confirmation set covering long conditioned sentences and 8 model families, with panel labels, plus an audit of the screen's labels.
- `README.md`: this file.
- `.aii/manifest.yaml`: empty, because this step created no heavy files.

## Key design points (full detail in the JSON)
- **Shared frozen screen.** Released Logic-LM FOLIO-dev outputs, scored against trusted references:
  - the corrected gold from arXiv 2606.02837, or
  - premises where the original FOLIO gold and folio-refined agree.
- **Secondary track.** 99 real annotator errors with known fixes.
- **Shared inputs.** Every experiment rebuilds the screen identically from the local files in
  `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/iter_3/gen_hypo/claude_agent/{data,probes}`, after fixing the ⊕/→ precedence bug in fol.py.
- **Pre-registered selection rule.** All of the following:
  - AUROC ≥ 0.65;
  - ΔAUROC over the disguised cheap judge with a 95% CI above 0;
  - tie margin 0.03;
  - coverage ≥ 90%;
  - rewrite false alarms ≤ 10%;
  - cost ≤ $0.002 per item.
  Iteration 2 re-ranks under adjudicated labels, then confirms the survivor once on held-out set E.

## Restoring removed files
Nothing is marked `delete`, so there is nothing to restore.
EOF
cat > /root/.claude/projects/-ai-inventor/memory/project_nl2fol_faithfulness_genstrat_iter1_run_u75jRHUss0zo.md <<'EOF'
---
name: project-nl2fol-faithfulness-genstrat-iter1-run-u75jrhuss0zo
description: run_u75jRHUss0zo invention-loop iter1 GEN_STRAT — wide screen of 4 gold-free NL→FOL candidates (FOL-Triage / verbalise+NLI & solver-worlds / cross-family repair-distance / disguised judge+baselines) + held-out long-stratum 8-family panel dataset
metadata:
  type: project
---
GEN_STRAT for invention-loop iter 1 of 5 (2026-09-23). Follows [[project_nl2fol_faithfulness_genhypo_iter3_run_u75jRHUss0zo]] and [[project-nl2fol-faithfulness-reviewhypo-iter3-run-u75jrhuss0zo]].

Slots: EXP A FOL-Triage (+decomposed-judge ablation) · EXP B B1 template-verbaliser bidirectional NLI + B2 z3 distinguishing worlds vs mutants judged by NLI/LLM · EXP C cross-family medoid repair distance + K=5 self-consistency + shared-blind-spot rate · EXP D disguised (nonce) cheap judge + strong judge 300 + round-trip + user's pilot metrics + parse rate · DATASET E held-out 600 sents (MALLS-train long/cond/exception, FOLIO-train agreed premises) × ≥8 families + 3-family panel + screen-label audit.

Frozen screen: Logic-LM FOLIO_dev released outputs (3 systems) matched to DSAVlab corrected conclusions, or to premises where orig≡folio-refined. Track H is 99 annotator errors. Local files are in iter_3/gen_hypo/claude_agent/{data,probes}; the fol.py ⊕/→ precedence must be fixed first. item_id = sha1(system|normtext|fol)[:16].

Rule: AUROC ≥ .65, ΔAUROC over the disguised cheap judge with CI > 0, tie margin .03, coverage ≥ 90%, rewrite FA ≤ 10%, cost ≤ $.002/item. If nothing beats it and the judge's AUROC ≥ .75, the judge wins. Iteration 2 re-ranks under adjudicated labels, then confirms once on E.
EOF
python3 - <<'EOF'
p='/root/.claude/projects/-ai-inventor/memory/MEMORY.md'
s=open(p).read()
anchor='- [NL2FOL faithfulness ReviewHypo I3 (u75j)]'
i=s.index(anchor); j=s.index('\n',i)
line='\n- [NL2FOL faithfulness GenStrat I1 (u75j)](project_nl2fol_faithfulness_genstrat_iter1_run_u75jRHUss0zo.md) wide screen A FOL-Triage/B verbalise+worlds NLI/C cross-family repair-distance/D disguised judge+baselines; E held-out long-stratum 8-family panel set; screen = Logic-LM FOLIO_dev vs corrected gold'
s=s[:j]+line+s[j:]
open(p,'w').write(s)
EOF
grep -c u75j /root/.claude/projects/-ai-inventor/memory/MEMORY.md
```

### [24] TOOL RESULT — Bash · 2026-09-23 12:54:09 UTC

```
{"stdout": "7", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [25] ASSISTANT · 2026-09-23 12:54:21 UTC

```
I've written the strategy file for iteration 1 to `./.terminal_claude_agent_struct_out.json`. It matches the schema and has all 5 slots filled, each with its expected finding stated. It is a wide screen: four experiments test four different ways of scoring a formula without gold, all on the same frozen set of real errors, and a fifth artifact builds the held-out set used to confirm the winner.

**The screen set.**
- **Main track:** the released Logic-LM FOLIO-dev outputs from three real LLM systems. They are compared against trusted references: the corrected gold from arXiv 2606.02837, or premises where the original FOLIO gold and folio-refined agree.
- **Second track:** the 99 real annotator errors with known fixes.
- **Shared rebuild:** there are no existing artifacts to depend on, so each experiment rebuilds this set identically from the local files and code under `iter_3/gen_hypo/claude_agent/{data,probes}`. The ⊕/→ precedence bug in `fol.py` gets fixed first. Items share the same IDs, so next iteration can join all the scores and check the labels are identical.

**The five slots.**
- **A — FOL-Triage:** formula lint, LLM-free role accounting, and a text-only small-LLM questionnaire compared against exact z3 answers. It also runs the "LLM reads the formula instead of z3" comparison.
- **B — Verbalise and check:** template verbalisation with two-way NLI, and z3-built small worlds that separate a candidate from its mutants, judged against the sentence.
- **C — Cross-system agreement:** each output's repair distance to the consensus of 6 or more model families, plus the K=5 self-consistency baseline and a measure of how often families make the same error.
- **D — The "a cheap judge is enough" null:** a cheap LLM judge on disguised items, plus every baseline you required: a strong judge, round-trip, parse rate, your pilot structural metrics, and a contamination check.
- **E — Held-out dataset:** about 600 sentences never used in the screen (long, heavily conditioned MALLS-train items and FOLIO-train premises), translated by 8 or more model families and labelled by a 3-model panel. It also re-labels the screen's uncertain items.

**The selection rule, fixed before anything runs.** A candidate survives if its AUROC is at least 0.65 and it adds signal over the disguised judge (the 95% CI of the AUROC gain is above 0). Candidates within 0.03 of the top survivor also advance. Gates: at least 90% coverage, at most 10% false alarms on meaning-preserving rewrites, and at most $0.002 per item. If nothing survives but the judge reaches 0.75, the judge wins. Iteration 2 re-ranks under the panel's labels, then runs the survivor once, with thresholds frozen, on set E.

**Main limitation.** The long, heavily conditioned sentences you care most about can't be tested on the screen, because FOLIO has only about 19 of them. That test is deferred to set E, which is built to have at least 50 errors and 50 correct outputs per stratum.

I also wrote `README.md`, an empty `.aii/manifest.yaml` (this step created no large files), and a memory note.

Sources:
- [TRUE: Re-evaluating Factual Consistency Evaluation (NAACL 2022)](https://aclanthology.org/2022.naacl-main.287/)
- [Ties Matter: Meta-Evaluating Modern Metrics with Pairwise Accuracy and Tie Calibration (EMNLP 2023)](https://aclanthology.org/2023.emnlp-main.798/)
```
