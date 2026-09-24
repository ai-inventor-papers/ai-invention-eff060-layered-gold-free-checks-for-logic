# gen_strat_1 — test_idea

> Phase: `invention_loop` · round 1 · `gen_strat`
> Run: `run_u75jRHUss0zo` — Gold-Free Faithfulness Metrics for NL-to-FOL Translation
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_strat_1` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-09-23 12:49:42 UTC

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

### [2] SKILL-INPUT — aii-handbook-auto-neurosymbolic · 2026-09-23 12:49:54 UTC

The agent loaded the **aii-handbook-auto-neurosymbolic** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

```
---
name: aii-handbook-auto-neurosymbolic
description: "Field handbook for neuro-symbolic AI — text-to-logic autoformalization (NL to FOL), LLM-plus-solver and prover pipelines (Prolog, ASP, SMT), probabilistic-differentiable NeSy (DeepProbLog, Scallop), reasoning faithfulness and scope laundering, ontology and KG grounding, logic benchmarks (FOLIO, ProverQA, MALLS). ALWAYS read before ANY neuro-symbolic research work — ideation/novelty assessment, study planning, experiment/eval design, or write-up; do NOT work from priors alone (several obvious-looking directions are already crowded). Triggers: neurosymbolic, text2logic, autoformalization, semantic parsing to logic, solver-verified reasoning, Kautz coupling taxonomy, proof-chain evaluation. NOT for: pure formal methods or Lean proving with no neural component, generic prompt engineering, KG-embedding work without logic, activation-level interpretability (use aii-handbook-auto-mechanistic-interpretability), or agent orchestration (use aii-handbook-auto-multi-agent-llm-systems)."
tools: Read, Write, Bash
---

<!-- GENERATED by amg-handbook-forge — DRAFT for expert review. generated: 2026-07-07 ·
     next_check: 2026-10 (volatile half-life ≈ months). ✓x=exec · [Sn]=cited · ⚠️=candidate.
     Row fails → `STALE: <what>` in place. -->

# Neuro-symbolic AI — field handbook (mid-2026)

## Overview
The SUBSTRATE below is the star: a dense, grounded map of the field as of mid-2026 — organizing principles, a theme-balanced frontier, and an explicit do-not-redo list. The only lens is OPEN QUESTIONS (tensions the reader resolves their own way; no prescribed directions), then a thin execution floor. Every claim resolves to a verbatim quote in [SOURCES.md](SOURCES.md).

## Organizing principles (how the field reasons)
- **No settled integration recipe.** ["To date, no single predominant approach exists"](https://en.wikipedia.org/wiki/Neuro-symbolic_AI) [S2]. The shared design-space map is Kautz's coupling taxonomy; the text2logic pattern is type 3 — a ["neural architecture to interpret perceptual data as symbols and relationships that are further reasoned about symbolically"](https://en.wikipedia.org/wiki/Neuro-symbolic_AI) [S2].
- **Verification is entering BOTH inference and training.** The 2024–2026 through-line: techniques ["that increasingly connect generation with verification"](https://arxiv.org/abs/2606.08728) [S12] — verification is no longer a post-hoc add-on.
- **Deep work is judged on principled integration serving trust.** The durable framing centers ["trust, safety, interpretability and accountability"](https://arxiv.org/abs/2012.05876) [S4]; the 2024 systematic review (1,428→167 papers) finds ["Explainability and trustworthiness are less represented (28%), with meta-cognition being the least explored area (5%)"](https://arxiv.org/html/2501.05435v1) [S1].
- **The stated scale bottleneck is knowledge acquisition, not inference:** ["knowledge extraction is the main bottleneck"](https://en.wikipedia.org/wiki/Neuro-symbolic_AI) computationally at large scale [S2].
- **The field now applies a correction rule to its own headlines:** ["high compilation rates or accuracies should not be equated with faithful reasoning"](https://arxiv.org/abs/2604.19459) [S6][S5] — accuracy gains no longer certify the reasoning behind them.

## Frontier (2025 H2 – 2026 H1, recency-weighted, theme-balanced)

**Text→logic / autoformalization.**
- Scale is not the lever for NL→FOL: ["Our fine-tuned Flan-T5-XXL achieves 70% accuracy with predicate lists, outperforming GPT-4o and even the DeepSeek-R1-0528 model with CoT reasoning ability"](https://arxiv.org/abs/2509.22338); ["predicate availability boosts performance by 15-20%"](https://arxiv.org/abs/2509.22338) — the predicate list, not model size, is the lever [S8] (2025-09).
- **Wedge now OCCUPIED (rank it down):** gold-free certification of autoformalization exists — ["We propose a roundtrip verification approach which does not require ground-truth annotations: formalize a statement, translate the result back to natural language, re-formalize, and use a formal tool to check logical equivalence."](https://arxiv.org/abs/2604.25031) [S9] (2026-04, SMT-community authors). Proposing gold-free roundtrip certification as novel re-treads this.
- The "LLMs can't do NL→FOL" premise is being walked back — ["recent literature provides contrasting results"](https://arxiv.org/abs/2511.11816), but sentence-level translation is largely handled [S23] (2025-11) → crowded lane 4.

**LLM+solver coupling.**
- The intermediate representation is a live design axis: reframing math reasoning as verifiable code (SymPy) moves failures from opaque fallacies to transparent program errors, ["demonstrating significant accuracy improvements of up to 13.6 percentage points over baselines"](https://arxiv.org/abs/2510.25975) [S11] (2025-10).
- Formalize-everything, forward-only pipelines are the diagnosed failure shape — they ["often suffer from redundant inference paths, hallucinated steps, and semantic drift"](https://arxiv.org/abs/2512.03360); the 2025-12 counter-design couples selective, confidence-aware translation with hypothesis-driven backward reasoning [S20].

**Probabilistic / differentiable NeSy.**
- Normative result, live controversy: the independence assumption (the tractability trick in DeepProbLog/Scallop-style predictors) formally ["entails that a model can never represent uncertainty over certain concept combinations"](https://arxiv.org/abs/2507.11357) [S14] (2025-07).
- Adoption is bottlenecked by tooling, not algorithms: ["A majority of the NeSy research focuses on algorithms instead of providing generic frameworks for declarative problem"](https://arxiv.org/abs/2509.07122)-solving [S15] (2025-09).

**Benchmarks & eval methodology.**
- Benchmark-validity result: canonical NL→FOL gold is broken — ["approximately 39% and 36% of entries, respectively, contain incorrect FOL formalizations (i.e., ground truth labels)"](https://arxiv.org/abs/2606.02837) in FOLIO and MALLS; corrected labels shift model accuracy +9–22pp, so scores on the originals partly measure annotation noise [S13] (2026-06).
- Eval is shifting from one-gold-proof to multi-path: LogicGraph ships solver-verified instances ["where each instance is associated with an exhaustive set of minimal proofs"](https://arxiv.org/abs/2602.21044) [S19] (2026-02).

**Faithfulness / auditable traces** *(hottest thread — deliberately capped here; see crowded list).*
- Formal structure raises accuracy, yet ["this gain does not imply faithful reasoning"](https://arxiv.org/abs/2606.16118): scope laundering — reporting solver-inconsistent verdicts without executing the formal reasoning — ["persists across all models"](https://arxiv.org/abs/2606.16118) [S5] (2026-06, COLM-2026 under review).
- Baseline-correcting dissent: under UNIFIED generation there is ["no evidence of systematic gaming in unified generation"](https://arxiv.org/abs/2604.19459) — ["models prefer reporting failure over forcing proofs"](https://arxiv.org/abs/2604.19459); unfaithfulness surfaces in the TWO-STAGE split and differs by model (axiom fabrication vs premise mistranslation that evades detection) [S6] (2026-04). Reading this paper as "models game formalization" is a documented misreading.
- Per-step trace validation exists: VeriCoT formalizes each CoT step to FOL and types its grounding premise (source / commonsense / prior step); validity ["serves as a strong predictor of final answer correctness"](https://arxiv.org/abs/2511.04662) [S10] (2025-11).
- Terminology (single 2-author preprint — lead only): ["a formal statement can typecheck and be provable, yet still encode a different theorem than the source intended."](https://arxiv.org/abs/2606.16541) [S7] (2026-06).

**Ontology / KG grounding.**
- **Wedge PARTLY OCCUPIED — and this section's one peer-reviewed anchor:** pretrained NL-term embeddings collide with formal ontology term syntax (SUMO/SUO-KIF), so models ["produce syntactic errors or hallucinate non-existent terms due to conflicting embeddings learned during base training"](https://proceedings.mlr.press/v284/thompson25a.html); a tokenization fix mitigates it [S18] (NeSy 2025, PMLR v284). "Ontology as a faithfulness lever" is no longer blank space.
- Ontology-grounded pipelines are being positioned for high-assurance domains (law/medicine), whose reasoning is ["inherently involving defeasible or non-monotonic logic due to numerous exceptions"](https://arxiv.org/abs/2510.01530) — grounding as an assurance lever, not just background knowledge [S16] (2025-10).

## Recent (~1–2 yr, compressed)
- **ProverGen/ProverQA** (ICLR 2025): prover-synthesized FOL eval — scalable, contamination-resistant, with ["accessible and logically coherent intermediate reasoning steps for each problem"](https://arxiv.org/abs/2502.06563); ["state-of-the-art LLMs struggle to solve ProverQA problems, even with CoT prompting"](https://arxiv.org/abs/2502.06563) [S25] (2025-02).
- **NL2FOL** (2024-05): the named key challenge is ["the integration of implicit background knowledge"](https://arxiv.org/abs/2405.02318) [S32].
- **GSM-Symbolic** (2024-10): pure-neural reasoning is perturbation-fragile — ["Adding a single clause that seems relevant to the question causes significant performance drops (up to 65%)"](https://arxiv.org/abs/2410.05229) [S29].
- **AlphaGeometry** (Nature 2024): the field's flagship result — the 2024 review found ["only one entry at the intersection of all 4 of the main research focal areas"](https://arxiv.org/html/2501.05435v1): AlphaGeometry [S1][S28].

## Durable core (foundations an expert still leans on)
- **Logic-LM / LINC** (2023) — the canonical parser+solver pattern: the LLM translates; ["These expressions are then offloaded to an external theorem prover, which symbolically performs deductive inference."](https://arxiv.org/abs/2310.15164) [S26][S24]. Self-refinement = the solver's error messages fed back [S24].
- **DeepProbLog / DeepStochLog / Scallop / Logic Tensor Networks** — settled probabilistic-differentiable canon; know them, do not re-propose them [S1][S2].
- **Kautz coupling taxonomy + Garcez & Lamb third-wave framing** — the field's shared vocabulary [S2][S4].

## Already crowded — go ELSEWHERE (do-not-redo)
Saturated threads with strong 2025–26 work; adding to them is incremental. The blank space is NOT here:
1. **Accuracy ≠ faithfulness diagnosis** — the gap is documented across [S5][S6][S7]; merely diagnosing it again is months late. Nuance inside the lane: the "formalization gaming" headline is already contested [S6].
2. **Interventional / counterfactual faithfulness** — a named lane: RFEval [S21]; Executable Counterfactuals — which itself notes existing evals ["tend to skip the abduction step, effectively reducing to interventional reasoning"](https://arxiv.org/abs/2510.01539) [S17]; label-flip evaluation with judge-model selection (Truth-or-Twist [S22] — a judge-selection study, not a proof-DAG benchmark).
3. **Proof-DAG / counterfactual-twin benchmarks** — LogicGraph already ships solver-verified, exhaustive minimal-proof sets [S19]; LogiConBench is a further lead (403-blocked; candidate lane).
4. **Bare NL→FOL translators** — saturated since Logic-LM/LINC 2023 [S24][S26]; ["state-of-the-art, dialogue-oriented LLMs demonstrate strong NL-FOL translation skills"](https://arxiv.org/abs/2511.11816) [S23]. Another translator is incremental.
5. **Per-axiom / per-step source-grounded ATTESTATION at the formalization seam** — grounding each formal atom or CoT step in an identified source premise + a solver/entailment check is an occupied lane: VeriCoT types each step's grounding premise and finds validity ["serves as a strong predictor of final answer correctness"](https://arxiv.org/abs/2511.04662) [S10], and premise-correspondence / scope-laundering checks already probe the same seam [S5][S7]. "Gate every premise against the source" re-treads this — the open move is what these do NOT do (e.g. defeating *shared-bias* mistranslation, not just per-premise support).
6. **Reverse-direction / NL-first, solver-certified benchmarks** — real-text (not template) inputs, expert-audited + Z3-checked, scored on formalization faithfulness: an active 2026 lane — LLMEval-Logic ["verifies annotated answers with Z3, constructs expert rubrics for natural-to-formal grading"](https://arxiv.org/abs/2605.19597) [S33]. "A reverse-direction certified benchmark" as the contribution re-treads it; only a distinct axis (e.g. a synthetic→natural transfer diagnostic) stays open.

## Open questions the field hasn't answered (the whole lens — answer in your own way)
1. Canonical pipelines equated accuracy boosts with ["a promising avenue for faithful logical reasoning"](https://arxiv.org/abs/2305.12295) [S24]; 2026 evidence shows the gain ["does not imply faithful reasoning"](https://arxiv.org/abs/2606.16118) [S5]. What property should a text→logic system be optimized and reported on — and what evidence would let a faithfulness claim survive both [S5]'s divergence protocol and [S6]'s two-stage protocol?
2. A solver in the loop is assumed to transfer soundness to the user-visible answer — ["a solver produces a sound and independently verifiable answer"](https://arxiv.org/abs/2606.19588) — yet ["the soundness guarantee can be lost in the interaction between the solver and the model"](https://arxiv.org/abs/2606.19588) [S27], scope laundering ["persists across all models"](https://arxiv.org/abs/2606.16118) [S5], while a Lean-4 study finds no systematic gaming under unified generation [S6]. Where along NL → formalization → execution → reported answer does soundness actually leak, and what task / pipeline-split / model differences reconcile the clashing results?
3. Per-step validators exist [S10] and roundtrip equivalence certification covers translation [S9], but there is no agreed gold-free faithfulness metric (as of 2026-07). What would a gold-free, process-level faithfulness measure have to certify for the field to accept it as a primary reported number?
4. Prover-synthesis provides gold chains [S25] and exhaustive minimal-proof sets [S19], while hand-curated gold is ~36–39% wrong [S13] — yet accuracy is still the primary reported metric. What blocks process-level scoring from becoming the default, and what would unblock it?
5. The independence assumption is ubiquitous for tractability yet formally ["entails that a model can never represent uncertainty over certain concept combinations"](https://arxiv.org/abs/2507.11357) [S14]. Where does this limitation actually bite on realistic tasks — and does the community's scepticism that it rarely matters hold up?
6. An upper ontology is assumed to supply clean background structure, but peer-reviewed evidence shows NL-term embeddings collide with formal term syntax, yielding hallucinated terms [S18], while high-assurance framings demand defeasible, evidence-grounded reasoning [S16]. What is ontology grounding actually good for in an LLM-era pipeline — and at what integration cost?

## What counts as DEEP here (taste)
| Deep / killed | Contrast | Separating cue · reopening condition | src |
| --- | --- | --- | --- |
| AlphaGeometry (Nature 2024): dissolved the structural bottleneck (proof-data scarcity) — ["sidesteps the need for human demonstrations by synthesizing millions of theorems and proofs"](https://www.nature.com/articles/s41586-023-06747-5) | AlphaGeometry2: same recipe scaled/tuned — ["we have significantly boosted the overall solving rate of AG to 84%"](https://arxiv.org/abs/2502.03544) (from 54%) | deep = attack the bottleneck so a new capability becomes possible; incremental = push the same paradigm's number | [S28][S31] |
| killed: the bare NL→FOL translator as the contribution | dismissal (2025-11): SOTA dialogue LLMs translate sentence-level logic well [S23] | reopen where translation still fails: beyond sentence level (long documents; dense modal/temporal/higher-order logic), or where ["embedding-centric models perform markedly worse"](https://arxiv.org/abs/2511.11816) | [S23] |
| killed: purely-neural end-to-end reasoners | dismissal (2024-10): ["current LLMs cannot perform genuine logical reasoning; they replicate reasoning steps from their training data"](https://arxiv.org/abs/2410.05229); compositional collapse [S30] | reopen only on demonstrated out-of-distribution, clause-count-robust reasoning that clears the GSM-Symbolic bar | [S29][S30] |
| killed: trusting FOLIO/MALLS original gold labels | dismissal (2026-06): ~39%/36% incorrect formalizations [S13] | reopen via the released corrected splits — relabeling framework reached ["90% dataset accuracy after reviewing fewer than 24% of instances"](https://arxiv.org/abs/2606.02837) | [S13] |

The line as THIS field draws it: contributions are weighed on principled integration serving trust/interpretability [S4], and the under-served areas (explainability & trust ~28%, meta-cognition ~5% [S1]) are where work reads deep — not another accuracy point on a saturated translator [S23].

## Critical rules (execution · eval · validity)
| Naive move | Expert move | Why (failure prevented) | src |
| --- | --- | --- | --- |
| Evaluate NL→FOL on FOLIO/MALLS as shipped | Use the corrected re-annotations or prover-synthesized sets; state which labels you scored on | ~39%/36% wrong gold; +9–22pp label-noise swings → wrong-result | [S13][S25] |
| Read compilation / typecheck / accuracy as faithfulness evidence | Measure faithfulness separately, on the reported answer | compilation rates ≉ faithful reasoning [S6]; typecheck+provable can encode a different theorem [S7] → wrong-result | [S6][S5][S7] |
| Default to prompting the largest reasoning LLM for NL→FOL | Also benchmark a fine-tuned small encoder-decoder and supply the predicate list | predicate availability +15–20%; T5-XXL beats GPT-4o / R1-0528 → wasted-cost | [S8] |
| Formalize the whole document and forward-chain | Weigh selective, confidence-aware translation and hypothesis-driven backward reasoning | forward-only: redundant paths, hallucinated steps, semantic drift → wrong-result | [S20] |
| Assume ontology terms ground cleanly | Test formal-term grounding separately (NL-embedding / term-syntax collision) | hallucinated non-existent terms in SUO-KIF-style languages → wrong-result | [S18] |
| Score reasoning against one gold proof chain | Account for alternate minimal proofs (multi-path eval) | penalizes valid derivations; distorts process scores → wrong-result | [S19] |

## Decision guide
- **Benchmark choice:** template sets (RuleTaker/ProofWriter) when you need scale + control and accept shortcut risk; FOLIO/MALLS ONLY with corrected labels [S13]; ProverQA for contamination-resistant, chain-accessible eval [S25]; LogicGraph when multiple valid proofs matter [S19].
- **Intermediate representation:** verifiable code (SymPy-style) when the domain is computational math [S11]; logic forms when deduction/entailment is itself the object [S24][S26].
- **Probabilistic substrate:** independence-assuming predictors (DeepProbLog/Scallop lane) buy tractability but formally cannot represent uncertainty over some concept combinations [S14] — decide by whether that uncertainty is load-bearing for the task.
- **Sourcing:** most 2025–26 results above are arXiv preprints; [S18] (PMLR) and the 2023–25 EMNLP/ICLR/Nature anchors are the peer-reviewed exceptions — prefer published versions for load-bearing claims (volatile.md tracks status).

## Ground rules (known-lane — terse)
- LLM = semantic parser, solver = deterministic inference — the Logic-LM/LINC division of labor [S24][S26].
- Self-refinement = feed the solver's error messages back to revise formalizations [S24].
- NL→FOL's named key challenge: implicit background knowledge the text leaves unstated [S32].
- Template benchmarks: scalable but simplistic; hand-curated: small + contamination-prone; prover-synthesis is the scalable route [S25].
- Scope laundering = reporting a solver-inconsistent verdict without executing the formal reasoning; sibling failure modes: implicit-constraint blindness, program-synthesis errors [S5].
- text2logic sits at Kautz type 3 ("Neural | Symbolic") on the coupling map [S2].
- Knowledge extraction is the stated main computational bottleneck at scale [S2].

## Reference documentation
- **[volatile.md](volatile.md)** — wedge-occupancy status, peer-review status of load-bearing preprints, venue/edition facts; re-check before any novelty verdict or write-up.
- **[SOURCES.md](SOURCES.md)** — provenance: every [Sn] resolves here with its verbatim quote and scrutiny verdict.

## Candidate lane  ⚠️ (expert to resolve — NOT verified)
- ⚠️ **LogiConBench** (OpenReview forum id ULEHJkolxB; reportedly ICLR 2026, controllable-depth reasoning graphs) — PDF returned HTTP 403 during mining; lead only. If confirmed, it further crowds lane 3. Confirm via OpenReview.
- ⚠️ **FRIT** (intervention-training for faithfulness) and **SATBench** (EMNLP 2025) — named by the tool-equipped baseline, not independently fetched; their lanes are confirmed by [S21][S19] regardless. Fetch abstracts before citing either.
- ⚠️ **Driftbench** — real: 2,183 NL/Lean-4 ["pairs with controlled drift labels across six subfields of mathlib4"](https://arxiv.org/abs/2606.16541), released by [S7], NOT by the formalization-gaming paper a search snippet attributed it to; [S7] is a quality-flagged single preprint, so treat as a lead until corroborated.
- ⚠️ **NeSy 2026 logistics** (Lisbon, Sep 1–4; PMLR; OpenReview, 10pg full / 5pg short; X-NeSy special issue) — from a live baseline fetch whose quote was not retained. Confirm at nesyconf.org before venue planning.
```
