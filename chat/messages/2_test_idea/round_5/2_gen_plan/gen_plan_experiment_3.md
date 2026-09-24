# gen_plan_experiment_3 — test_idea

> Phase: `invention_loop` · round 5 · `gen_plan`
> Run: `run_u75jRHUss0zo` — Gold-Free Faithfulness Metrics for NL-to-FOL Translation
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_plan_experiment_3` (terminal_claude_agent, claude-opus-5-5)

### [1] CONFIG · 2026-09-24 10:58:06 UTC

```
model: claude-opus-5-5 | effort: high | permission: bypassPermissions
```

### [2] SYSTEM-USER prompt · 2026-09-24 10:58:14 UTC

````
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: A plan generator (Step 3.2: GEN_PLAN in the invention loop)

You received the hypothesis, an artifact direction to elaborate, and dependency artifacts relevant to the plan.
Your job: elaborate this direction into a detailed, actionable plan for the executor agent.

Specific, actionable plan → valuable artifact. Vague plan → wasted execution.
</your_role>
</ai_inventor_context>

<artifact_type_info>
You are expanding an artifact direction of type: EXPERIMENT

EXPERIMENT
Run code to test hypotheses, implement methods, and collect empirical results.
Runtime: Python 3.12, UV (any pip package), isolated workspace, gradual scaling (mini → full data).
Tools: Full shell/Python/filesystem access, the aii-web-tools skill (web search, page fetch, regex grep over full page/PDF text), and other skills.
Skills: aii-json (schema validation), aii-openrouter-llms (call any LLM — GPT, Gemini, Llama, etc.), domain-specific as needed.
Capabilities: Implement and run any code-based experiment, compare method vs baselines.
Deps: REQUIRED at least one DATASET | OPTIONAL RESEARCH for methodology guidance
</artifact_type_info>

<available_resources>
<software_constraints>
- Python only implementation
- Python standard library and all popular PyPI packages available (numpy, pandas, scikit-learn, scipy, matplotlib, requests, etc.)
- Local parallelism encouraged: multiprocessing, asyncio, threading — see aii-parallel-computing skill
- LLM API calls must go through OpenRouter only (no direct OpenAI, Anthropic, etc.), with base_url=os.environ["OPENROUTER_BASE_URL"] and api_key=os.environ["OPENROUTER_API_KEY"] (the OpenAI SDK's defaults, OPENAI_BASE_URL and OPENAI_API_KEY, point at the same place, so a plain OpenAI() client also works with OpenRouter model ids). The key is this run's own OpenRouter key and works only at that base URL: never hard-code OpenRouter's own URL, or every call fails with 401
- **SPEND BUDGET**: at most $10 USD of OpenRouter API calls for this artifact. Nothing outside your own code enforces this — the key you are given has no per-artifact cap — so it holds only if you track cumulative cost after every call and stop when you approach it. Budget the work up front: estimate the per-call cost and the number of calls BEFORE starting a sweep, not after it overruns. Exceeding it spends real money that the run cannot recover.
</software_constraints>

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
</available_resources>

<time_budget>

The experiment executor has 6h total (including writing code, debugging, testing, and fixing errors).

</time_budget>

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

<plan_guidelines>
You are expanding an artifact direction from the strategy into a detailed plan.
The artifact direction specifies what to do at a high level (type, objective, approach, dependencies).
Your job is to make it concrete and actionable as a detailed plan.
Use web research to look up technical details, verify feasibility, and find reference materials
that will make your plan more concrete and actionable for the executor.

GOOD PLANS:
- Make each component SPECIFIC and actionable (not vague platitudes)
- Consider both success AND failure scenarios
- Build on the approach in the artifact direction
- Add concrete details the executor needs

BAD PLANS:
- Vague hand-waving ("do research on X")
- Ignoring the approach in the artifact direction
- Missing critical details the executor needs
</plan_guidelines>

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
Your workspace: `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_plan/gen_plan_experiment_3`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_plan/gen_plan_experiment_3/`:
GOOD: `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_plan/gen_plan_experiment_3/file.py`, `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_plan/gen_plan_experiment_3/results/out.json`
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

<hypothesis>
kind: hypothesis
title: Cross-model agreement, tested on fresh data
hypothesis: |-
  kind: hypothesis (iteration 5 of 5, FINAL). Move = DEEPEN on the one live lead: cross-family solver consensus (frozen c_score_align, with PT = p_peer_text as its fused row). The lead gets its first test on data no earlier decision touched. The two confirmation sets that the budget broke in iteration 4 (E2, and the R_COMP FREE gloss labels) are each FIXED ONCE, with their claims unchanged. The lead's false-alarm cause, which iteration 4 re-diagnosed as wrong and scattered peers rather than vocabulary, is attacked with $0 development-screened variants. Candidate-Signature Consensus (CSC) is CLOSED. The paper is then written from the corrected record below.

  ========================================================================
  0. CORRECTED RECORD (the paper step TRANSCRIBES these numbers; each has a source)
  ========================================================================

  0.1 DATA ROLES
  - E, the screen, R_COMP SIG and PERTURB are DEVELOPMENT data. Every number from them is development evidence. The paper must NEVER call E 'held-out'.
  - The only untouched confirmation evidence is:
    - E2: sealed; seal.json and verify_seal.py are in gen_art_dataset_4;
    - the R_COMP FREE untouched subset (2,198 rows; seal b364a49a…, gen_art_dataset_5).

  0.2 ITERATION 3, CORRECTED
  The iter-3 record in iter_3/upd_hypo §0 is authoritative, together with the eval-3 Part-4 tables in gen_art_evaluation_3/tables/: hypothesis_verdicts_iter3.csv, perturb_corrected.csv, t2_record.csv, rename_selection_dead_end.csv, cost_units.csv, coverage_vs_request_iter3.csv, function_inventory.csv, label_facts.csv, corrections_iter12.csv, artifact_id_map.csv, prior_art.csv. Essentials:

  T1 (art_7GxreYjATkC5), R_AB n = 2,686 (1,822 ERROR / 864 CORRECT, 292 sentences):
  - c_score_align strat AUROC 0.741 vs flash-lite disguised 0.642: Δ +0.099 [0.049, 0.146].
    - long pool +0.116 [0.070, 0.163]; EXC +0.197; vs nano original +0.089 [0.043, 0.134].
  - L25 (the user's priority stratum): Δ +0.069 [−0.020, 0.148], n.s.
  - CTRL −0.069 [−0.23, 0.10].
  - Against the baseline stack:
    - c alone ≈ S4_full: +0.006 [−0.031, 0.042];
    - nested [S4_full + c] − S4_full: strat +0.039 [0.021, 0.057].
  - Frontier frame (n = 284):
    - AUROC: judge 0.741, S4_full 0.745, c 0.710;
    - ratio 0.957 [0.887, 1.034], so the 0.95 bar is met on the point estimate only;
    - nested +0.037 [0.008, 0.066].
  - M3 is INCONCLUSIVE because its two specifications conflict: bootstrap +0.146 [−0.051, 0.361] vs stacked GEE +0.274 [0.190, 0.359].
  - Flash-lite contamination DiD +0.105 [0.006, 0.201]: marginal evidence of contamination.
  - Spend $2.395.

  T2 (art_cxnoDYQNFolW), NOT CONFIRMED:
  - SIG passes: 0.954 vs 0.587; +0.278 vs the original judge. But SIG is the controlled-vocabulary regime the user excluded.
  - FREE was NOT_TESTABLE.
  - [Correction, iter 4] The iter-3 FREE tier-A deltas (c_align − judge +0.214; 'falls to ~0.80') are VOID. Those labels over-call ERROR: 297 of 420 old ERROR rows are MAPPED (gen_art_dataset_5/results/old_label_agreement.json).

  Exp 8 (art_YYD-HDzfQfEj):
  - The pre-registered rename-invariant selection FAILED (HYB 0.841/0.700, NF 0.686/0.485).
  - MEANING_RENAME is an ERROR operator, and c_nf is blind to it (0.499).
  - Per-operator consensus AUROC is a base-endorsement artefact. Do not rank operators by it, and do not claim 'polarity symmetry'.
  - Coverage 3,419 of 5,402 rows.
  - Typing: peer-medoid 0.328 vs judge 0.326; the gold-using oracle reaches 0.802.

  Eval 2 (art_FWy8D4_y9GBn), pre-registered definitions:
  - M1 INCONCLUSIVE; M2 CONFIRMED but non-specific; M4 k95 = 3 overall, 2/3/5 by words tercile (long tercile = 5).
  - NET +0.356 [0.198, 0.493]: consensus DEGRADES with length.
  - SCATTER ratio 4.45; graded − binary +0.114.

  Costs (cost_units.csv):
  - consensus $1.21e-4 per candidate FULL;
  - k = 1/3/5/7 pools: $0.000315 / 0.000946 / 0.001576 / 0.002206 per SENTENCE;
  - flash-lite $4.9e-5 per call; frontier $3.65e-3 per item;
  - SIG generation $0.000116 per candidate; MARGINAL z3 $2.5e-7.
  - The old '$0.000024–0.000170 per sentence' column is wrong.

  Prior art (art_VIF75I5R6f0v; needs its own section and marker in the paper):
  - Not scooped. The method is not new: ARc 2511.09008 uses the same score form; NoTB 2608.21962; GenV 2609.11085 reports a label-target reversal; LLMs-as-Jury recommends 3-4 families.
  - C1 and C3-C5 need qualifiers (prior_art.csv).
  - Iter-3 spend $4.33 (not '$1.58 plus T1').

  0.3 ITERATION 4, the record per artifact (spend from ledgers)

  A. Exp 9, CSC on E (art_D7k2ZWgE3nVd; tables.md T0-T17; csc_gate_E.json). PROVISIONAL.
  Population and selection:
  - The platform refused paid calls after 1,033 of ~9,000 planned. PRIMARY is therefore a COMPLETION-SELECTED subset: 354 R_AB rows (196 ERROR / 158 CORRECT, 144 sentences).
  - CTRL makes up 44.9% of PRIMARY CORRECT rows vs 27.4% on FULL.
  - No stratum reaches 50/50, so L25 is NOT_READ.
  - c_csc tie rate is 0.986.

  Strat AUROC [CIs as in T4]:
  | Metric | Strat AUROC |
  |-|-|
  | c_csc | 0.614 [0.493, 0.736] |
  | FREE_exact (same 3 families) | 0.770 [0.686, 0.844] |
  | FREE_ALIGN | 0.731 [0.635, 0.825] |
  | c_score_align | 0.774 [0.682, 0.857] |
  | p_peer_text | 0.799 [0.700, 0.880] |
  | S4_full | 0.736 [0.635, 0.826] |
  | flash-lite disguised | 0.664 [0.568, 0.750] |
  | HYB_MEAN | 0.709 [0.586, 0.817] |

  Paired Δ for c_csc (T5):
  - vs FREE_exact −0.156 [−0.290, −0.031];
  - vs c_score_align −0.160 [−0.275, −0.064];
  - vs flash-lite −0.050 [−0.212, 0.107], n.s.;
  - vs S4_full −0.123 [−0.269, 0.010], n.s.;
  - phi-4 exemplar leakage removed (T17, 58 CSC calls copied the exemplar): c_csc_clean 0.639; vs FREE_exact −0.132 [−0.251, −0.023].

  e and d:
  - CSC e 0.459 vs FREE_exact 0.173; CSC d 0.139 vs 0.323.
  - FULL T2: FREE_exact d 0.583 vs ALIGN 0.328.

  Anchoring by class (T9, PRIMARY; e_CSC / e_FREE_exact / e_FREE_ALIGN):
  | Class | e_CSC | e_FREE_exact | e_FREE_ALIGN |
  |-|-|-|-|
  | ADD | 0.490 | 0.135 | 0.375 |
  | DROP | 0.472 | 0.169 | 0.380 |
  | COMPOUND | 0.282 | 0.107 | 0.184 |
  | MEANING_RENAME-type (n = 28) | 0.821 | 0.036 | 0.750 |
  | structural | 0.336 | 0.153 | 0.282 |
  | polarity | 0.200 | 0.133 | 0.200 |
  - MEANING_RENAME-type Δ CSC − FREE_ALIGN is +0.071 [−0.083, 0.269], NOT_READ.
  - FULL T9b: FREE_ALIGN e on MEANING_RENAME-type is 0.624, vs 0.104 for exact.
  - READING: every vocabulary bridge (the aligner, or peers cued with the candidate's symbols) lowers d AND raises e, class by class. The aligner that c_score_align uses already endorses meaning-rename errors almost as often as CSC does.

  Gates (the text of prereg_csc_E.json):
  - G1 FAIL: d 0.139 ≤ 0.35, but the words slope is +1.25 [0.41, 2.09].
  - G2 = 'strat ≥ c_score_align − 0.01 AND pooled > c_score_align on L25' → NOT_READ (the R_AB part FAILS; L25 Δ −0.067 [−0.183, 0.040], n = 81, not read).
  - G3-E = RENAME_SYN false alarm: NOT_RUN.
  - G4 null.
  - G5 PASS: $5.25e-4 per candidate ($2.76e-4 deduped).

  Length:
  - M3 bootstrap −0.232 [−0.770, −0.023]; stacked GEE −0.351 [−0.694, −0.009].
  - NET is length degradation WITHIN each arm, and every arm degrades: FULL FREE_exact +0.452, FREE_align +0.401.

  Other tables:
  - T8: 53% of free-exact disagreements with CORRECT candidates are structural; only 20.2% of flagged CORRECT rows are fully vocabulary-resolvable.
  - T10 typing: own_majority 0.185, below the majority class 0.262.
  - T14: CSC τ-b 0.256 (p = 0.25) vs c_score_align 0.513 (p = 0.015).
  - T15: 9-peer c_score_align rename FA 0.595 → 0.868, ΔFA +0.273 [0.164, 0.384].
  - Spend $0.108.
  - Prior art: this is the correlated-failure mode of Chen & Avizienis 1978. What is new is the per-class e measurement and the bridge-trades-d-for-e table.

  B. Exp 10, CSC on PERTURB (art_pAmLrGqsmFUx). BROKEN: 0 CSC peers were generated ($0.0000088). G3-P, G4 and MT are UNTESTED.
  Zero-cost arms:
  - SIGPROXY (out-of-scope controlled vocabulary): k = 3 within-template 0.930 [0.916, 0.943]; d 0.149 cued vs 0.757 uncued FREE3-ALIGN.
  - Prior art for the shared-vocabulary lever: Vossel et al. 2025 ('predicate availability boosts performance by 15-20%') and ARc's fixed schema. The only addition here is a measured d reduction on long templated sentences, in an excluded regime.

  CORRECTIONS:
  - FREE-consensus mutant recall ≈ 1 comes with base FA at c > 0.5 of:
    - 0.712 (c_align_exp8, E);
    - 0.803 (FREE3_exact, E);
    - 0.986 (FREE3_exact, R_COMP);
    - 0.757 (FREE3_align, R_COMP).
    So that recall is trivial.
  - Rename-control FA is mostly base FA. The paired flips are 0.18-0.53 (c_align E: SYN 0.182, NONCE 0.327).
  - LOCAL2 e 0.341 comes entirely from insufficient-peer ties at c = 0.5 (e_excl 0.012/0.007).
  - The judge's 12.4% mutant miss rate is NOT END_MAJ e.
  - Typing:
    - 'oracle' repairs against the gold base, so it is NOT gold-free;
    - free3 on E is 0.123 [0.081, 0.169]; the pooled 0.085 includes R_COMP rows at 0.
  - Split the controls by base source: FREE3_exact REORDER/CONTRA is 0.842/0.840 on E and 0.986 on R_COMP.
  - Uncued d by words tercile: 0.47 / 0.80 / 0.91.

  C. Dataset 4, E2 (art_2OmxzMInZZJY). BROKEN (budget stop).
  - 550 sentences frozen: L25 350, EXC 100 (92 'without' + 8 'but not'; the core-exception supply is exhausted, D3), DT 100 (ProverQA).
  - 30-sentence pilot: 300 candidates, labelled 36 ERROR / 274 UNRESOLVED (incl. gold-as-system) / 20 UNPARSEABLE / 0 CORRECT.
  - Panel drift check:
    - the stop rule is UNDECIDED (passes = false; combined majority agreement 0.394);
    - synthetic gate items 0.974;
    - on 22 unambiguous track-H judgements, today's panel flags 0.12 of original errors vs 0.84 in E: a DRIFT WARNING on small n.
  - Deviations D0-D7 must be listed.
  - Spend $0.241.
  - Power (eval 3):
    - L25 yield 0.37, so 350 L25 gives MDE80 0.110;
    - +0.069 on L25 needs ~882 planned sentences;
    - the long pool needs ~237 usable sentences.

  D. Dataset 5, R_COMP FREE labels (art_Ia_FT284H33j). BROKEN for its purpose: the gloss step was not run, so the CORRECT class is empty.
  - Search-only labels: ERROR_CERT 759, MAPPED 1,506, UNPARSEABLE 188, NO_OUTPUT 199.
  - Search soundness: 0 of 1,595 false ERROR_CERT on SIG renames; known-ERROR rescue 9-10% (T8 0.27; T9 0.37-0.43).
  - Audit: ERROR_CERT precision 0.867; MAPPED faithful 0.867. One MAPPED certificate swaps LivesIn and StudentInClass.
  - Old iter-3 labels are contaminated by UP TO 70.7%. MAPPED is an upper bound. Old/new kappa is 0.058.
  - D6 amended the map family after the freeze. Spend $0.

  E. Eval 3 (art_BvAL_KZTZuw8), $0.
  - MAIN FINDING: among pairs of a CORRECT candidate and a non-agreeing peer, 77% (9-family) / 61% (3-pool) of those peers are labelled ERROR. Only 9% of CORRECT-CORRECT disagreements are vocabulary-resolvable.
  - Pair classes: IRREDUCIBLE 69.4%, EXACT 13.6%, ALIGN_ONLY 15.1%, VOCAB 1.6%.
  - The no-anchoring oracle d floor:
    - 3-pool 0.385;
    - L25 0.542 vs END_MAJ 0.735;
    - 9-family 0.586 > END_MAJ 0.537, because most peers are wrong.
  - The post-hoc instruments predict almost no fix: bracket [0.396, 0.415]; the gap_closed rule is ill-conditioned (denominator 0.013).
  - The instruments are shown to UNDER-COUNT vocabulary effects: predicted endorsement 0.20 vs actual SIG 0.575, calibration error −0.372 [−0.423, −0.323].
    - SIG also changes granularity (D7), so the SIG−FREE agreement drop of +0.479 [0.447, 0.513] is an upper bound.
    - Non-transitivity (0.131) is a separate diagnostic.
  - The number 0.683 is d under the exact rule on E's 3-pool. It is NOT an AUROC and NOT R_COMP. Delete 'theoretical AUROC 0.683'.
  - c_vres on L25: −0.014 [−0.028, −0.001].
  - NET DEGRADES under every rule (+0.35 to +0.39).
  - VOCAB agreements are not label-specific.
  - R_COMP FREE needs ≥ 200 CORRECT rows.

  F. Iteration-4 spend: $0.108 + $0.0000088 + $0.241 + $0 + $0 ≈ $0.35. The rest of the $7 'Test idea' phase budget was consumed by processes recorded in NO iteration-4 artifact ledger. The paper states this and does not guess.

  ========================================================================
  1. WHAT THE EVIDENCE NOW SAYS (the revised diagnosis)
  ========================================================================
  The lead stands on development data: consensus beats cheap judges on long and exception sentences, and it adds signal over the stack only when nested. It is not confirmed on untouched data, and not on L25. The iteration-3 diagnosis said consensus fails on long sentences because CORRECT translations disagree about WORDS. Iteration 4 REFUTES that as the dominant cause on real LLM outputs (E):
  - 61-77% of the disagreement a correct candidate meets comes from peers that are themselves WRONG;
  - only 9% of correct-correct disagreement is vocabulary.
  - Every vocabulary bridge trades d for e:
    - the aligner: d 0.583 → 0.328, but meaning-rename e 0.104 → 0.624;
    - candidate-signature cues: d → 0.139, but e → 0.459, the anchoring.
  - CSC fails provisionally, and the aligner already carries much of the same anchoring cost.

  Vocabulary divergence is real in templated free-vocabulary text (R_COMP: exact agreement 0.048 FREE vs 0.528 SIG). But on real long sentences the binding constraint is PEER ACCURACY: on L25 about 80% of candidates are wrong, so a correct candidate's class is a small plurality.

  Candidate one-sentence finding, if iteration 5 confirms: 'Cross-family solver agreement is a gold-free faithfulness check that beats cheap LLM judges on long, conditioned sentences at ~$1e-4 per candidate. Where it fails, the cause is that the other models are wrong in different ways, not that correct translations use different words. Any device that makes peers share the candidate's vocabulary lowers false alarms only by making peers copy the candidate's errors.'

  ========================================================================
  2. CLAIMS FOR ITERATION 5 (all metrics frozen and hashed BEFORE any confirmation label is joined)
  ========================================================================

  H-PRIMARY (pre-declared in iteration 3; NOT re-selected). On E2 and on R_COMP FREE, the frozen c_score_align:
  - uses the E2 10-slot pool, leave-own-family-out, with the exp-5 code byte-identical;
  - is compared with the flash-lite rubric-A judge (disguised AND original) and with gpt-4.1-nano.
  p_peer_text is a secondary row, frozen.

  H-MECH (the label-based replication of the iter-4 diagnosis; no instrument needed). On E2 CORRECT candidates:
  - (i) ≥ 50% of non-agreeing peers are labelled ERROR;
  - (ii) SCATTER ratio SI_cor / SI_err ≥ 2;
  - (iii) NET Δ(e+d) over the words terciles is > 0 (degradation replicates);
  - (iv) exact vs ALIGN on E2 FULL reproduces the trade: ALIGN has lower d and higher e on MEANING_RENAME-type and ADD/DROP errors.

  H-IMPROVE (the deepen on the cause; a DEVELOPMENT screen at $0, on E's stored pairwise matrix, 29,107 pairs). The mechanism is that wrong peers scatter (they agree with few others), so a correct candidate's plurality is diluted by them. So a score that discounts scattered or unreliable peers should lower d on long sentences WITHOUT raising e. Unlike CSC and the aligner, it changes no peer output and bridges no vocabulary.

  Candidates screened, all label-free:
  - V1 plurality-normalised: c_pn = 1 − share_agree / max_class_share among the sentence's peers;
  - V2 reliability-weighted: per-family weights from mean pairwise agreement across ALL sentences (Dawid-Skene-style, label-free), estimated out of sentence fold;
  - V3 = V1 + V2;
  - V4 two-channel: a cross-fitted logistic on (c_exact, c_align), trading the aligner's d gain against its e cost;
  - V5 V3 on the eval-2 best 3-pool (cost-matched, $0.001 per sentence);
  - V0 the frozen c_score_align.

  Selection rule (pre-registered before running):
  - the winner is the variant with the highest E long-pool strat AUROC that
    - beats V0 by ≥ +0.015 there,
    - AND is ≥ V0 on L25 (point),
    - AND is ≥ V0 − 0.01 on CTRL.
  - If none qualifies, NO variant is carried and V0 stands alone.
  The winner is a CANDIDATE only; E2 confirms or kills it. Report how many variants were screened (5).

  H-RENAME (the user's invariance requirement, the last attempt on a new mechanism, secondary budget). GLOSS-GATED name-free agreement (GG):
  - A peer agrees with the candidate if they are exactly z3-equivalent, OR if an exhaustive injective symbol map (freelab.equivalent_modulo_vocab_exhaustive) yields equivalence AND a cheap LLM gloss check confirms every non-identity mapped symbol pair is a same-meaning pair in this sentence.
  - This targets exactly why NF/HYB failed: NF cannot tell a synonym from a wrong predicate (0.388 of HYB's extra agreements are label-discordant; MEANING_RENAME 0.499). The gloss adds the lexical meaning test the solver lacks, without cueing peers, so there is no anchoring.
  - The gloss model family for GG MUST differ from the one that labels R_COMP FREE (instrument-sharing firewall). GG is therefore never evaluated on R_COMP FREE.
  - Dev gate on PERTURB E-bases plus E R_AB:
    - RENAME_SYN paired flip ≤ 0.05 and FA ≤ base FA + 0.05;
    - MEANING_RENAME recall at fixed threshold ≥ c_align's − 0.05;
    - E strat AUROC ≥ c_score_align − 0.01.
  - Fail → rename non-invariance of consensus is reported as a measured boundary: c_align PERTURB NONCE/SYN FA 0.765/0.565 with paired flips 0.327/0.182; 9-peer ΔFA +0.273. No further rename work.

  ========================================================================
  3. WORK ORDER AND BUDGET (each sweep costed before it runs; stop when the next sweep's estimate exceeds the remainder minus a 10% reserve)
  ========================================================================
  P1. R_COMP FREE gloss (FIX ONCE; the panel route stays dropped). About $0.8-1.8.
  - Gloss gate on the 840 known-answer items: balanced accuracy ≥ 0.90, per class reported.
  - Then gloss the MAPPED rows → CORRECT / ERROR / UNRESOLVED, and seal.
  - A Sonnet-5 audit only on a 120-row stratified sample.
  - Out-of-family faithful forms (13% of ERROR_CERT) are carried as a label-noise bound; the AUROC is reported with and without those template classes.
  - Testable only if ≥ 50 CORRECT rows; power is adequate at ≥ 200. The judge scores for FREE rows already exist from iter 3.

  P2. E2 drift gate FIRST (~$0.3). Replay the full track-H set (192 judgements) with pinned model ids.
  - PASS (flag rate on original errors within the CI of E's 0.84): E's frozen solver + panel protocol labels E2.
  - FAIL: E2-L25/EXC labels are reported as DRIFTED (secondary), and the primary confirmation becomes R_COMP FREE plus E2-DT. DT is labelled by the alignment-free exhaustive-map + gloss labeller against the trusted prover-built gold.

  P3. E2 generation for all 550 sentences (10 slots). Then the panel in the order L25 → EXC → DT, then the L25 surplus (98) if budget remains.
  - The LONG POOL (L25 + EXC) is PRE-DECLARED PRIMARY, and its MDE (~0.11-0.12) is stated in advance.
  - The 30 pilot sentences are included (sealed; never read by a selection step), and results are reported with and without them.

  P4. Judges on E2: flash-lite disguised and original, and nano, on every parseable row (~$0.5). Also a local Qwen3-8B judge, L2-bow and the local round trip for S4_E2, which is cross-fitted by E2 sentence folds.

  P5. The GG dev screen (gloss calls only on pairs where exact/ALIGN fail but a map exists; <$0.5).

  P6. Frontier gemini-3.1-pro on a 300-row stratified E2 subsample (~$1.1). This is the first thing dropped if budget binds.

  DROPPED:
  - all remaining CSC arms (PERTURB G3-P/G4/MT, OTHER-SIG, multi-reading);
  - any new dataset construction beyond E2;
  - the SIG regime as evidence for the user's operating condition.

  ========================================================================
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

  ========================================================================
  5. PAPER OBLIGATIONS (all transcription; blocking review items)
  ========================================================================
  - Apply eval-3 Part 4 in place. Each corrected item gets a '[Correction, iter 4: …; source <path>]' marker next to the struck original text:
    - §3.4 from perturb_corrected.csv: MEANING_RENAME = an ERROR operator; per-operator consensus AUROC = base endorsement; the judge cells from perturb_sensitivity.csv; coverage 3,419/5,402;
    - §3.3 from t2_record.csv: T2 NOT CONFIRMED, and the FREE deltas are void;
    - §3.5 with the pre-registered M1-M4, NET +0.356, and cost_units.csv;
    - the iter-1/2 items in corrections_iter12.csv: frontier C4 'strengthens'; the 588 common items; 'fitted under solver labels'.
  - Replace the placeholder artifact IDs from artifact_id_map.csv.
  - Add the following sections and tables:
    - '3.7 Hypothesis verdicts';
    - 'Prior-art positioning [ARTIFACT:art_VIF75I5R6f0v]': scoop rule, neighbour table, C1-C5 verdicts;
    - the coverage-against-request table, with one-line answers: long sentences → pending E2; no controlled vocabulary → pending R_COMP FREE; error type → negative;
    - the function inventory;
    - ONE cost table with units;
    - the iteration-4 spend table (§0.3F);
    - a reasoning block at the start of §3 and §4 (previous review score and blocking status, move, prediction, gates, planned vs actual artifacts).
  - Rewrite §4.2-4.6 from §0.3A-E exactly, with CIs copied verbatim. 'CSC is a dead end' becomes 'provisional negative on a completion-selected subset; L25 and RENAME untested'.
  - Extend the dead-ends table:
    - rename-invariant selection (NF/HYB INELIGIBLE);
    - candidate B1 (never ran);
    - the FOL-Triage rewrite-FA gate;
    - P2 and P4 REFUTED;
    - CSC_graded, CSC_multi and HYB_MEAN (all fail G1);
    - E2 EXC-core supply;
    - correct the c_nf reason to 'selection failure + MEANING_RENAME blindness'.
  - 'What we have learned' must drop '0.954 on R_COMP' and '96% of frontier' as headlines, or caveat them (out-of-scope SIG; point estimate only). It must state the long-tercile k95 = 5.

  ========================================================================
  6. CARRIED AS SECONDARY ROWS; CLOSED
  ========================================================================
  Secondary rows: PT, TEXT (L2-bow + L3), NF/HYB, graded consensus, S4 stacks, round trip, SC-5, pilot structural metrics, the local judges.

  CLOSED, one sentence each in the paper:
  - CSC and all its arms;
  - post-hoc NF/HYB as a rename fix;
  - the panel route for R_COMP FREE;
  - per-operator within-base AUROC for consensus;
  - B1/B2; R_ADJ; L1 lint and L2-role on LLM outputs;
  - the vocabulary-divergence diagnosis of iteration 3 (refuted on E by the label-based decomposition).

  DELIVERABLE FUNCTIONS:
  - consensus_score(mode = align | exact | nf | hyb | pn | rw | gg);
  - graded_consensus;
  - pairwise_matrix / ed_decomposition;
  - exhaustive_map_label + gloss_decision (the labelling tools);
  - equivalent_modulo_vocab(_exhaustive);
  - minimal_typed_repair;
  - fol_triage;
  - peer_text.
  Each has a one-line statement of what it measures, and each is marked gold-free or gold-using.
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
_relation_rationale: >-
  Same consensus object; CSC closed; cause re-diagnosed as wrong peers; broken confirmation sets fixed once
_confidence_delta: decreased
_key_changes:
- >-
  The CSC fix is CLOSED as a provisional negative. On a completion-selected 354-row subset, c_csc strat is 0.614 [0.493, 0.736]
  vs FREE_exact 0.770, Δ −0.156 [−0.290, −0.031]; anchoring e is 0.459 vs 0.173. G1 FAIL, G2 NOT_READ, G3 NOT_RUN. The title
  changes because the candidate's-own-words idea is dead.
- >-
  The diagnosis is revised from label-based evidence (eval 3). 61-77% of the disagreement a CORRECT candidate meets comes
  from peers labelled ERROR; only 9% of correct-correct disagreement is vocabulary. Every vocabulary bridge trades d for e:
  the aligner's meaning-rename e is 0.624 vs 0.104 for exact. The iter-3 'words not errors' story is refuted on E.
- >-
  Iteration 5 is confirmation-first. The two budget-broken confirmation sets are each fixed ONCE, with claims unchanged: the
  R_COMP FREE gloss labels (priority 1, in-scope free vocabulary) and E2 (long pool pre-declared primary, MDE ~0.11 stated).
  Frozen c_score_align is the pre-declared primary and is not re-selected.
- >-
  A drift gate comes before E2 labelling, because today's panel flags 0.12 vs 0.84 of original errors on 22 track-H items.
  On failure, the primary switches to R_COMP FREE + DT, labelled by the alignment-free map + gloss labeller against trusted
  gold.
- >-
  New $0 development screen aimed at the re-diagnosed cause (wrong, scattered peers): plurality-normalised, reliability-weighted
  and two-channel exact/align consensus. The selection rule is pre-registered; the winner is only a candidate for E2.
- >-
  The last rename attempt uses a new mechanism: gloss-gated name-free agreement. The lexical check separates synonyms from
  wrong predicates, which NF/HYB could not, and no cueing means no anchoring. It is dev-gated on PERTURB; on failure, rename
  non-invariance is reported as a measured boundary.
- >-
  The iteration-4 record is corrected for the paper: CIs copied verbatim from T4/T5, COMPOUND e 0.282/0.107, G2 NOT_READ,
  M3 under both specifications, NET within-arm, FREE consensus recall paired with base FA 0.71-0.99, LOCAL2 ties, typing free3
  0.123 on E (oracle is gold-using), E2 drift, FREE labels 'up to 70.7%', eval-3 misreadings removed ('0.683 theoretical AUROC'),
  and spend ≈$0.35 with the rest of the $7 phase budget unaccounted.
- >-
  Every blocking review item is listed as a paper transcription obligation: in-place corrections from eval-3 Part 4, the prior-art
  section for art_VIF75I5R6f0v, coverage-vs-request, one cost table with units, the spend table, the extended dead-ends table,
  and reasoning blocks.
- >-
  The error-type ask is answered negatively outside a shared vocabulary (free3 0.123; medoid 0.328 ≈ judge 0.326). No further
  budget goes to it.
_strands:
- artifact: art_D7k2ZWgE3nVd
  state: 'null'
  why: >-
    CSC strat 0.614 [.493,.736] vs FREE exact .770 (Δ −.156 CI<0); anchoring e .459 vs .173; G1 fail, G2 NOT_READ; completion-selected
    subset but clear negative
- artifact: art_pAmLrGqsmFUx
  state: broken
  why: >-
    0 CSC peers generated (budget 403); G3-P/G4/MT untested; $0 arms are out-of-scope SIGPROXY or trivial (FREE recall≈1 at
    base FA .71-.99)
- artifact: art_2OmxzMInZZJY
  state: broken
  why: >-
    Budget stop after 30/550 sentences: 0 CORRECT, no testable cell; drift stop rule UNDECIDED (track-H flag .12 vs .84 on
    22 items)
- artifact: art_Ia_FT284H33j
  state: broken
  why: >-
    Gloss step not run so CORRECT class empty, FREE AUROC untestable; search sound (0/1,595 false ERROR_CERT) and shows old
    FREE labels over-call ERROR
- artifact: art_BvAL_KZTZuw8
  state: lead
  why: >-
    Label-based: 61-77% of peers disagreeing with CORRECT candidates are ERROR; only 9% vocab-resolvable; d is peer error
    not vocabulary; oracle d L25 .542 vs .735
_evidence_state: lead
_move: deepen
_move_rationale: >-
  Lead (consensus + eval-3 cause). Deepen: confirm frozen consensus on untouched E2/R_COMP FREE (fix each once), attack wrong-peer
  cause at $0; CSC closed.
_coverage: full
_coverage_statement: >-
  Iteration 5 answers whether a cheap gold-free cross-model agreement score predicts faithfulness on long, conditioned sentences
  with no controlled vocabulary. It tests this on untouched data against judges and the baseline stack, and also reports invariance,
  per-type recall, coverage and cost, plus a negative answer on error typing.
_candidates_considered: 12
relation_type: evolution
</hypothesis>

<available_domain_handbooks>
Domain handbooks below capture expert knowledge for a specific field — its landscape, prior work, dead ends, evaluation norms, and what counts as a genuinely novel contribution. If one is relevant to your research topic, READ that skill BEFORE proceeding; read the most relevant one(s), or none if none apply. When none fit, do not force one — instead ground your work harder in primary sources and hold novelty claims to extra scrutiny, since you have no curated map of this field's prior work and dead ends. Use it for the methods, proper baselines, and evaluation this field demands.

- **aii-handbook-auto-computational-linguistics** — Field handbook for computational linguistics as a SCIENCE of language — grammaticality and minimal pairs (BLiMP), surprisal versus reading times, linguistic structure in LMs, annotator disagreement an
- **aii-handbook-auto-mechanistic-interpretability** — Field handbook for mechanistic interpretability of neural networks — circuit discovery, activation and attribution patching, sparse autoencoders, transcoders, attribution graphs, steering vectors, pro
- **aii-handbook-auto-multi-agent-llm-systems** — Field handbook for multi-agent LLM systems (MAS) — orchestration topology, multi-agent debate, mixture-of-agents, verifier and critic agents, inter-agent protocols (MCP/A2A), failure attribution and s
- **aii-handbook-auto-neurosymbolic** — Field handbook for neuro-symbolic AI — text-to-logic autoformalization (NL to FOL), LLM-plus-solver and prover pipelines (Prolog, ASP, SMT), probabilistic-differentiable NeSy (DeepProbLog, Scallop), r
</available_domain_handbooks>

<strategy_domain_reasoning>
How the strategist established that researchers in this field reason, at the level of the field's principles and standards of evidence. Take it as the starting point for the concrete practice below — extend or correct it where your own reading disagrees, and say so when you do.

FIELD: meta-evaluation of reference-free (gold-free) quality metrics, the methodology of the WMT metrics shared tasks, summarization-factuality meta-evaluation (FRANK, TRUE, SummaC) and LLM-as-judge validation, applied to neuro-symbolic NL->FOL autoformalization. READ FOR THIS STEP: the neurosymbolic handbook (aii-handbook-auto-neurosymbolic): [S13] FOLIO/MALLS gold is about 36-39% wrong; [S6] compilation is not faithfulness; [S9] gold-free round-trip certification is occupied; [S8] predicate lists are the NL->FOL lever; open question 3, 'no agreed gold-free faithfulness metric'. Also the iteration-4 artifacts and the power file (eval-3 power_E2.json), E2's prereg / census / drift file, dataset 5's resume script, and the prior-art artifact art_VIF75I5R6f0v (ARc, NoTB, GenV, LLMs-as-Jury, Chen & Avizienis). I ran no new web lookups in this bounded step. The MT/summarization norms below are standing knowledge (WMT's fresh test set each year; Deutsch et al. on metric CIs and ties), marked provisional.
(1) PRINCIPLES. Taken as given:
- benchmark gold is partly wrong, so the label construction is itself part of the result;
- several FOL formulas are correct for one sentence, so solver-exact vs intent labels can reverse rankings (GenV);
- compiling is not faithfulness;
- the incumbent a practitioner uses is a cheap API LLM judge.
Still argued: which label target is right, and whether a metric validated on one label regime transfers.
(2) WHAT CONVINCES. A metric win counts when it is paired, item-level and threshold-free, on real system outputs, against the incumbent, and scored ONCE with frozen parameters on data that no selection step touched. That is why WMT re-scores metrics on each year's fresh test set. It must also be shown to add signal by nesting over the best baseline combination, and must hold under a second, instrument-disjoint label regime. A development-set win plus a mechanism story is a lead, not a finding. A mechanism is believed when a label-based decomposition that could have come out the other way replicates on new data.
(3) STANDARD MOVES and what each rules out:
- stratified within-stratum AUROC: stratum composition;
- a sentence-clustered bootstrap: item dependence;
- a pre-declared primary cell with its MDE stated: forking paths and underpowered nulls read as wins or losses;
- a score seal before the label join: post-hoc metric tuning;
- instrument-disjoint labels: circular validation (the aligner shared by labeller and metric);
- a cost-matched and a frontier comparator: the 'you beat a weak judge' objection;
- nonce disguise with a DiD: memorised gold;
- base FA next to every recall: trivial recall (iteration 4's FREE recall of about 1 came at base FA 0.71-0.99);
- a paired flip, not raw FA, for invariance: base-rate confusion.
(4) USUAL FAILURE MODES:
- development-set optimism (the lead was chosen on E);
- completion-selected subsets after a budget stop (exp 9's PRIMARY was 45% CTRL);
- label drift when a panel is replayed months later;
- shared-instrument labels;
- quantised scores at unattainable thresholds;
- underpowered strata (the L25 +0.069 needs about 882 planned sentences);
- cost in the wrong unit (off by 13x in iteration 3);
- transcription drift between artifacts and the paper, the current BLOCKING cause.
</strategy_domain_reasoning>

<domain_practice>
FIRST WORK OUT HOW THIS KIND OF STUDY IS ACTUALLY BUILT IN THIS FIELD. Then
write the plan.

The strategy already settled what the field believes and what it counts as
convincing. Your job is the level below that: how work of exactly this kind
is designed, run and reported by the people who do it, concretely enough that
the executor's output would be recognised as competent by one of them.

Establish, for this field and this artifact type:

- BASELINES AND COMPARISONS. Which comparisons appear in every paper of this
  kind, named specifically. Which one would a reviewer name first if it were
  missing, and what is the standard way of tuning it fairly?
- CASES AND DATA. Which datasets, corpora, cohorts, benchmarks, case sets or
  sources are standard here, and which are known to be saturated, leaked,
  deprecated or unrepresentative. Prefer the ones the field actually uses,
  and say why when you pick something else.
- CONTROLS AND WHAT IS HELD CONSTANT. What has to be held fixed for the
  comparison to mean anything, and which confound this design is most likely
  to be caught on.
- HOW MUCH IS ENOUGH. Sample sizes, item counts, seeds, repeats, splits —
  the number below which nobody in this field believes a result, and what the
  field reports alongside a point estimate (variance, intervals, a
  significance or uncertainty treatment). When a power analysis, or the
  effect sizes already on record, say the panel cannot detect the size of
  effect the plan is chasing, the fix is more graded samples or checkpoints
  — not more candidate metrics. An underpowered panel stays underpowered no
  matter how many readouts run over it.
- MEASURES AND REPORTING CONVENTIONS. Which measures are standard, how they
  are computed here, and the conventions a reader will expect to see — what
  is reported, against what, in what form.

Not every axis applies to every artifact type: a proof has proof standards
and an accepted level of rigour rather than sample sizes, a research artifact
has source quality and coverage, a dataset has provenance, licensing and
documentation norms. Answer the ones that apply and skip the ones that do not
rather than inventing content for them.

HOW MUCH EFFORT. Bounded, like the strategist's: the fitting domain handbook
plus a handful of targeted lookups — one or two recent papers doing this exact
kind of study, a benchmark or dataset card, a methods or reproducibility note.
Read what the field does; do not reason it out from first principles. You
cannot run code, so this is reading only.

THEN CHECK THE PLAN AGAINST IT.
- `domain_practice`: what you established above, concretely — named baselines,
  named data, the numbers, the measures, with what you read.
- `practice_alignment`: go through the plan you just wrote against that list
  and say, point by point, where it MEETS the field's practice and where it
  DEPARTS from it. For every departure: why it is justified here (budget,
  scope, the claim being narrower) and what it costs the result's
  credibility. A departure nobody named is the one a reviewer finds.
- Where the check exposes a gap you can close inside the budget, close it in
  the plan rather than reporting it. `practice_alignment` is for what remains
  after you have fixed what you can.
</domain_practice>

<artifact_direction>
Make this direction concrete and actionable. Keep the same type and respect dependencies.

id: experiment_iter5_dir3
type: experiment
objective: >-
  FIX, claim unchanged: make R_COMP FREE (in-scope free vocabulary; long templated sentences with trusted-by-construction
  gold) testable, then run confirmation criterion (c). Iteration 4 built a sound name-free map search (0/1,595 false ERROR_CERT)
  but never ran the gloss step, so the CORRECT class is empty. Run the frozen gloss pipeline of dataset 5 once, seal the labels,
  and test whether frozen c_score_align (already scored in iteration 3, never joined to these labels) beats the flash-lite
  judge within template, in both the disguised and original views. The labels share NO instrument with the metric: no aligner,
  and checker families disjoint from the peers and the judges.
approach: |-
  SHARED CROSS-ARTIFACT CONTRACT (identical text in all five directions). The five artifacts run in parallel and this is the last iteration, so every piece that joins two artifacts is done by polling for a marker file, and every consumer has a stated fallback that still produces a reportable result.
  (M1) FREEZE marker, written by the 'freeze' experiment: <its workspace>/freeze/CONSENSUS_FREEZE_READY.json with token 'aii_iter5_consensus_freeze_v1'. It holds the sha256 of freeze/consensus_variants.py, of freeze/selection.json (the H-IMPROVE winner, or 'NONE: V0 stands'), and of freeze/gg.py + freeze/gg_gate.json (H-RENAME: PASS/FAIL, gloss model id, prompt sha). Consumers find it with glob('/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/*/freeze/CONSENSUS_FREEZE_READY.json'), check the token, and copy (never import across paths) the frozen files into their own workspace. The expected write time is within about 90 minutes of start (V) and 3.5 h (GG).
  (M2) DRIFT marker, written by the E2-A experiment: <ws>/e2/E2_DRIFT_DECISION.json with token 'aii_iter5_e2_drift_v1' (PASS/FAIL, the numbers, the pinned provider per panel model).
  (M3) FINAL markers: <ws>/e2/E2A_FINAL_READY.json and <ws>/e2b/E2B_FINAL_READY.json with tokens 'aii_iter5_e2a_final_v1' and 'aii_iter5_e2b_final_v1'. Each points to that artifact's per-row file (row_key, sentence_id, stratum, label, tier, every frozen score) and gives its sha256.
  Every poll loop sleeps 5 min, logs each attempt, and has a hard deadline written into the prereg. A path found by glob is read-only; nothing is written outside the artifact's own workspace.
  SPEND: OpenRouter only, via os.environ OPENROUTER_BASE_URL / OPENROUTER_API_KEY. Make a 1-token probe first. Log cost after every call to cost_ledger.jsonl, and stop hard at the artifact cap. Estimate every sweep's cost from a small pilot BEFORE running it, and do not start a sweep whose estimate exceeds the remaining budget minus a 10% reserve. On HTTP 403/402 (run budget) do all CPU work first, then poll every 15 min; if the block persists past the deadline, report the partial result as partial.
  NO COMPLETION SELECTION (the lesson of iteration 4, exp 9): every paid sweep over sentences runs in a pre-registered sha1 order, and each batch of 50 sentences is completed end to end (generation, then labels) before the next batch starts. A budget stop therefore leaves a random subsample of each stratum, not a completion-selected one, and the report states the completed fraction per stratum.

  INPUTS (read-only; copy): dataset 5 = /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5:
  - src/resume_gloss.py: gate -> free_gloss -> finalize + seal -> sig_e2e -> audit_ii -> package, with gloss.Client and its ledger;
  - src/freelab.py, prompts/, prereg_freelab.json (v1.1) + sha256, deviations.json (D1-D9, including D6, the post-freeze family amendment);
  - full_data_out.json groups rcomp_free_labels (2,652 rows; untouched subset 2,198, seal b364a49a...), gloss_gate_items (840 = 7 classes x 120, halves A/B) and sig_soundness_replay;
  - work/models_snapshot.json.
  Frozen scores to confirm = /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results:
  - rcomp_candidates.jsonl: FREE rows, c_score_align and the other consensus scores, template_id, slot;
  - judge_FREE.jsonl: flash-lite rubric A disguised and original;
  - judge_local_FREE.jsonl;
  - src/consensus_rcomp.py.
  Eval-3 = /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3: pairwise_classes_RCOMP.jsonl (label-free FREE classes under exact / ALIGN / NF) and power_E2.json (R_COMP FREE needs >= 200 CORRECT).
  Hard cap $4. Dataset 5's estimate: gate $0.10 + FREE gloss $0.95 + SIG e2e $0.25 + audit $0.45.

  STEP 0: score_seal_rcomp.json = sha256 of the FREE score columns (c_score_align, c_exact, judges) for the 2,198 untouched rows, computed BEFORE any gloss call. The labeller never reads these files (FIREWALL, as in dataset 5). Write prereg_rcomp_confirm.json (+ sha256) with:
  - the criterion: within-template Delta c_score_align - flash-lite disguised AND - flash-lite original, template-stratified sentence-cluster bootstrap B = 2000, both CIs > 0;
  - testability >= 50 CORRECT (power adequate at >= 200);
  - the untouched subset as PRIMARY, all FREE rows secondary;
  - the sensitivity rows below.

  STEP 1: resume_gloss.py gate. The checkers are anthropic/claude-haiku-4.5 and qwen/qwen3-235b-a22b-2507 (as frozen). PASS = balanced accuracy >= 0.90 per checker and for the conjunction, each class recall >= 0.85, per class reported. On FAIL: ONE hashed prompt revision on half B, as dataset 5 pre-registered; if that fails too, labels = ERROR_CERT + UNRESOLVED only and (c) = NOT_TESTABLE, declared.

  STEP 2: free_gloss on the MAPPED rows, then finalize (CORRECT / ERROR_GLOSS / UNRESOLVED), seal and verify, then sig_e2e (the end-to-end check on known SIG rows) and audit_ii. The audit becomes anthropic/claude-sonnet-5 on a 120-row stratified sample (label x template): the audit statistic is ERROR_CERT precision and CORRECT precision with CIs, never a label change. The old iter-3 FREE labels are joined only after the seal, for an agreement table: kappa, and the share of old ERROR now CORRECT.

  STEP 3 (after both seals verify), CONFIRMATION (c) on the untouched subset:
  - within-template AUROC of frozen c_score_align, c_exact, flash-lite disguised / original, the local judge; the paired Deltas; nested [judge + c] - judge;
  - e and d of END_MAJ under exact vs ALIGN on FREE CORRECT / ERROR rows: H-MECH (iv) on a second population, with the trusted gold. Does the aligner lower d and raise e here too?
  - the share of non-agreeing peers of CORRECT candidates that are themselves ERROR: H-MECH (i) on R_COMP FREE;
  - sensitivity rows, each reported, none gating: (s1) excluding the template classes holding the out-of-family faithful forms named in the dataset-5 audit (disjunctive split, one predicate with two constants, exists-for-constant, in-name negation), matched by their certificate / unresolved_reason codes, with the rule written in the prereg before the join; (s2) UNRESOLVED counted as ERROR and then as CORRECT (bounds); (s3) including the 454 seen_iter3 rows; (s4) per template and per weak/strong reading;
  - the V1-V5 variants (computed from the FREE pairwise classes with the verbatim definitions, or copied from the freeze marker M1 if present) as EXPLORATORY rows, Holm-corrected; GG is NEVER evaluated here (firewall);
  - complexity by words tercile and n_conditions within FREE;
  - coverage with unparseable and no-output rows in the denominator;
  - cost.
  Verdict (c): CONFIRMED / NOT CONFIRMED / NOT_TESTABLE.

  OUTPUT:
  - rcomp_free_labels_final.jsonl + seal.json;
  - gate_report.json, audit_report.json, old_label_agreement.json;
  - per_item_rcomp_free.jsonl;
  - confirm_verdict_rcomp.json;
  - tables.md with source lines;
  - method_out.json (exp_gen_sol_out);
  - src/ (the reusable exhaustive_map_label, equivalent_modulo_vocab_exhaustive and gloss_decision, with docstrings saying each is a gold-USING labelling tool);
  - deviations.json, cost_ledger.jsonl.
what_it_would_show: ''
depends_on:
- id: art_Ia_FT284H33j
  label: labeller
  relation_type:
  relation_rationale:
- id: art_zcwCQgTqk6DN
  label: R_COMP
  relation_type:
  relation_rationale:
</artifact_direction>

<dependencies>
Completed artifacts this artifact can use during execution.

--- Dependency 1 ---
id: art_zcwCQgTqk6DN
type: dataset
title: Long logic sentences and FOL error suite
summary: >-
  Two held-out NL->FOL faithfulness tables (full_data_out.json, aii exp_sel_data_out, every row re-verified against its sources
  by data.py and z3-re-verified by src/verify.py, 0 failures). (1) PERTURB (group perturb_suite, COMPLETE): 4,234 typed mutants
  (metadata_fold PERTURB, output ERROR, error_ops=[op]) plus 868 meaning-preserving controls (PERTURB_CONTROL, output CORRECT).
  They cover 300 bases: 36 TRUSTED_AGREED + 95 GOLD_PANEL_OK + 69 PANEL_REPAIRED dataset-E references, and 100 R_COMP weak
  readings. Operators are NEG, REV, QUANT, RESTR, CONN, MOVE, DROP, ADD (ADD_FOREIGN / ADD_INTERNAL), SWAP, BIND and MEANING_RENAME,
  at DOWN/UP positions (metadata_position_polarity, polarity_method, matched_pair_id; 1,354 complete pairs). QUANT/REV/RESTR
  are UP-only; SCOPE and UNGLUE have 0 rows. Each mutant is z3 non-equivalent to every accepted reading. Controls are RENAME_SYN
  / RENAME_NONCE, REORDER and CONTRAPOSITIVE/DEMORGAN, each z3-equivalent. (2) R_COMP (group rcomp_sentences): 250 main +
  100 reserve templated sentences, each with >=25 words, >=3 conditions and one unless/except/provided-that/only-if clause
  (9 templates). Weak and strong references come from the template (T8 also stores a not-accepted converse), are unit-tested
  and z3-checked, and are built from a 652-entry atom lexicon mined from verified FOLIO/MALLS references. Provenance fields:
  template_id, lexicon_ids, source_rule_ids. CAVEAT: the shared OpenRouter key hit its daily limit 5 minutes in ($0.41 spent);
  the 21:38 UTC replacement key was also already exhausted. Pending: the Sonnet lexicon and reference audits, fluency, generator
  candidates (rcomp_candidates), solver labels, adjudication and the testability declaration. ./run_all.sh completes them
  resumably under the pre-registered prereg_rcomp.json. Until then R_COMP must not be used for metric claims. PERTURB is ready
  for per-operator sensitivity and invariance analysis. Rows carry item_id (E's recipe) and disguised_text/fol. adjudicator_check_out.json
  holds 60 known-label QA items. See dataset_card.md.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3
out_expected_files:
- data.py
- full_data_out.json
- preview_data_out.json
- mini_data_out.json
out_dependency_files:
  file_list:
  - data.py
  - full_data_out.json
  - mini_data_out.json
  - preview_data_out.json
  data_file_paths:
  - full_data_out.json
  - mini_data_out.json
  - preview_data_out.json

--- Dependency 2 ---
id: art_Ia_FT284H33j
type: dataset
title: Name-free labels for free-vocabulary logic translations
summary: >-
  T7b name-free labels for R_COMP FREE (free-vocabulary NL->FOL rule translations; 221 templated sentences, 10 LLM slots /
  9 families). full_data_out.json (exp_sel_data_out) has 3 groups: (1) rcomp_free_labels, 2,652 rows (one per FREE generation
  record, row_key = exp-7 recipe), label from an exhaustive, certificate-backed, name-free map search (injective symbol maps
  + B1/B2 reification, B3 merge, B4 split, B5 lexical negation; z3 relevance/polarity prunes, 128-model finite countermodels,
  z3 equivalence; 0 caps, 0 z3 unknown) under a hashed prereg v1.1. IMPORTANT: labels are SEARCH-ONLY (deviation D9: run OpenRouter
  budget exhausted before this artifact's first call, $0 spent): ERROR_CERT 759 (final, exact relative to the family), UNRESOLVED_GLOSS_NOT_RUN
  1,506 (z3-equivalent under some map, gloss check pending), UNPARSEABLE 188, NO_OUTPUT 199; no CORRECT class yet -> AUROC
  NOT_TESTABLE; metadata_label_binary_search_provisional (ERROR_CERT vs MAPPED) is TESTABLE (all 759/1,506; untouched 636/1,175)
  with audited contamination ~13% each side. Metadata: seen_iter3 (454 rows; untouched subset 2,198 is primary), map_certificate,
  gloss_pairs, certificate counts, strata (template, clause_type, word_tercile, prompt_variant). Seal sha256 9609ebbb... (all),
  b364a49a... (untouched). (2) gloss_gate_items: 840 known-answer (symbol use, meaning) items, 7 classes x 120, halves A/B;
  checker verdicts pending. (3) sig_soundness_replay: 4,280 = 2,140 SIG rows x {nonce, synonym} renames with known pure-z3
  labels: false ERROR_CERT on known-CORRECT 0/1,595, identity map recovery 100%, known-ERROR rescue by non-identity maps 9-10%
  (what the gloss check must stop), oracle-checker ceiling recall 1.00 / false-CORRECT 0.00. Executor (non-blind) audit: ERROR_CERT
  precision 0.867 [0.76,0.93] (out-of-family faithful forms: disjunctive split, one predicate with two constants, exists-for-constant,
  in-name negation); MAPPED faithful 0.867. Old iter-3 tier-A labels: 34/34 CORRECT are MAPPED; 297/420 old ERROR are MAPPED,
  17/20 hand-checked are old aligner false errors. Reusable functions in src/freelab.py (exhaustive_map_label, equivalent_modulo_vocab_exhaustive,
  gloss_decision); src/resume_gloss.py runs gate -> FREE gloss -> final labels/seal -> SIG e2e -> Sonnet-5 audit (~$1.8) once
  budget is available. See dataset_card.md, deviations.json.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5
out_expected_files:
- data.py
- full_data_out.json
- preview_data_out.json
- mini_data_out.json
- reproducibility.md
out_dependency_files:
  file_list:
  - data.py
  - full_data_out.json
  - mini_data_out.json
  - preview_data_out.json
  - reproducibility.md
  data_file_paths:
  - full_data_out.json
  - mini_data_out.json
  - preview_data_out.json
</dependencies>

<prior_work>
Everything this run has already produced, earlier rounds included. This is what
the plan builds on.

--- Artifact 1 ---
id: art_d0njuqy2Csj-
name: gen_art_experiment_1
type: experiment
title: Screening a three-layer logic-translation checker
summary: >-
  FOL-Triage wide screen (iter-1 exp A), all under this workspace. Frozen shared screen: screen_items.json (track L = 753
  Logic-LM FOLIO-dev outputs of gpt-3.5/gpt-4/davinci-003 vs DSAVlab corrected gold, 112/202 conclusions + 271 agreed premises;
  track H = 302 curated original->corrected), href_items.json, invariance_set.json, screen_meta.json; item_id=sha1(system|norm(text)|fol)[:16]
  for joining with sibling experiments. Labels (iter-3 repair census, xor precedence fixed): L CORRECT 278 / ERROR 199 / UNCERTAIN
  204 / UNPARSEABLE 60; 59% of ERRORs are pure ADD+DROP vocabulary artefacts (needs panel adjudication). Released functions
  in src/fol_triage.py: fol_lint (L1), content_accounting (L2-bow), role_accounting (L2-role), formula_role_profile + role_questionnaire
  (gemini-2.5-flash-lite, text only) + l3_compare (L3); fused logistic fitted on track H with sentence-leak guard, frozen
  in prereg.json before track-L labels. PRIMARY (L ERROR vs CORRECT, n=477, 199 pos): fused AUROC 0.759 [0.695,0.825]; L2-bow
  0.737; L3 0.756; L2-role 0.557; L1 0.508 (lint does not transfer to LLM outputs; 0.655 on track H); fused-L2bow +0.022 CI
  [-0.019,0.061] not significant; decomposed judge (LLM reads formula instead of z3) lowers L3 AUROC by 0.059 (sig.); nonce-disguise
  shows no contamination (0.765 vs 0.770). Gates: AUROC/coverage 0.92/cost $0.0002 pass; rewrite-FA FAILS (0.275; originals
  flagged at same rate, fused FA on L CORRECT 0.19 vs 0.10 calibrated on H; flip rate <=0.06). Long/conditioned strata UNTESTABLE
  on this screen. L3 gate on HREF: role .91, claims .86, missing .92, extra .92 gated; force .69 excluded. Robustness rows:
  qwen3-30b and local Qwen2.5-1.5B (OpenRouter outage fallback). Headline AUROCs re-derived independently (results/audit_rederive.json,
  placebos ~0.5). Judge/round-trip/self-consistency baselines are NOT here (experiments C/D; join on item_id in iteration
  2). Outputs: method_out.json (exp_gen_sol_out; predict_fol_triage + per-layer predict_* per item), results/metrics.json,
  results/per_item.jsonl, README.md. Spend $0.29.
iteration: 1
workspace_path: >-
  /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_1
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json
out_dependency_files:
  file_list:
  - method.py
  - full_method_out.json
  - mini_method_out.json
  - preview_method_out.json

--- Artifact 2 ---
id: art_i3cVDxBp-USk
name: gen_art_experiment_3
type: experiment
title: Do other models' translations agree? Consensus metric for NL-to-logic
summary: >-
  Experiment 3 screens candidate C, a text-free, gold-free consensus metric for NL->FOL faithfulness, on the shared frozen
  screen (label hash 0e43cbdd...). c_score = 1 - eq_frac: the share of OTHER systems' translations of the same sentence that
  are NOT z3-equivalent to the candidate modulo vocabulary alignment. The pool has 6 fresh OpenRouter families (llama-3.3-70b,
  qwen3-235b, deepseek-v3.1, mistral-small-3.2, gemini-2.5-flash-lite, gpt-4.1-mini) plus the 3 released Logic-LM systems,
  leave-one-out. Also scored: medoid repair depth and operators, and semantic entropy over z3 classes. Baselines: K=5 self-consistency
  (gpt-4.1-nano T=0.7 on all items; true same-model gpt-3.5-turbo SC for gpt-3.5 candidates), predicate-set stability, and
  FOL length. PRIMARY (track L, 297 CORRECT vs 249 ERROR, sentence-clustered bootstrap 2000): c_score AUROC 0.866 [0.821,
  0.906]; peers-only 0.872; non-OpenAI peers 0.863; other Logic-LM systems only 0.753; cluster entropy 0.773; medoid depth
  0.722; sc5_cheap 0.725 [0.669, 0.781] (n=546, now complete). Paired Δ c_score - sc5_cheap = +0.140 [0.085, 0.197]; c_score
  - sc5_same = +0.140 [0.057, 0.227] (n=167). Cross-fitted [c_score, sc5] vs [sc5] = +0.147. Vocab-clean subset (shared-aligner
  confound control): c_score 0.852 vs SC 0.714. At the medoid threshold: recall 0.62, false alarms 0.14. Shared blind spot:
  38% of errors are endorsed by the consensus (POLARITY 5%, COVERAGE 41%, STRUCT 57%). Repair operators match the labeller's
  81% of the time (chance 46%). RENAME rewrites cause 96% false alarms (the aligner does not survive synonym or constant renaming);
  z3-equivalent rewrites flip 0% by construction. Long/conditioned stratum n=5, descriptive only. Cost: $1.52 total; the peer
  pool costs $0.0015 per sentence. This re-run completed the SC_cheap arm that the shared-key limit had cut to 231/307 units,
  and restored WordNet for RENAME.
iteration: 1
workspace_path: >-
  /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json
out_dependency_files:
  file_list:
  - method.py
  - full_method_out.json
  - mini_method_out.json
  - preview_method_out.json

--- Artifact 3 ---
id: art_elDZY26Pu6GD
name: gen_art_experiment_4
type: experiment
title: Cheap LLM judge and baseline scores for logic translations
summary: >-
  Experiment D (baseline/null arm) on the SHARED FROZEN SCREEN: data/screen_items.json, 1,090 items. Track L = 796 Logic-LM
  FOLIO-dev outputs labelled vs corrected gold or agreed premises: 294 CORRECT / 230 ERROR / 216 UNCERTAIN / 56 UNPARSEABLE.
  Track H = 294 curated original-vs-corrected items. Label-vector sha1 122d01df... FINAL judges are the planned API models,
  under prereg.json: judge_cheap = gemini-2.5-flash-lite (JSON 0-100, rubric A), judge_cheap2 = gpt-4.1-nano (P(YES)), judge_strong
  = gemini-3.1-pro-preview (frontier; 200L+96H subset). Open-weight local judges (Qwen3-8B, Llama-3.1-8B, Qwen3-14B-nf4; run
  during a key outage) are kept as judge_local_* rows. API spend $2.02. Track L AUROC [95% CI]: judge_cheap_disg 0.777 [0.720,
  0.827] = THE BAR; judge_cheap_orig 0.749; gpt-4.1-nano 0.750/0.714; frontier orig 0.802 on the subset, which is +0.077 [0.006,
  0.154] over the cheap judge on the same items (DeLong p=.015), with the gap vanishing under disguise; rt_nli_min 0.710 (API
  verbaliser) / 0.740 (local verbaliser); rt_embed_cos 0.633; rt_reformalise_eq 0.513 (near chance). User's pilot structural
  metrics are 0.50-0.53 (a negative result); cross-system rerun Jaccard 0.720. The cross-fitted S4 combination of all cheap
  baselines has OOF AUROC 0.817 [0.762, 0.867], which is +0.039 [-0.010, 0.087] over the judge (not significant). best_baseline_oof
  per item and data/folds.json are provided for nested deltas in iteration 2. Contamination: no evidence. Every DiD CI includes
  0; the frontier judge loses ~0.07 under disguise on both tracks (lost lexical meaning); the recall probe matches the corrected
  gold 15.9% vs the erroneous original 4.4%. Invariance: the judges false-alarm on contrapositive (cheap 0.67, nano 0.97),
  De Morgan and rename rewrites. Judge correctness falls with sentence length (p=1.6e-5); long sentences are untestable on
  track L. Label noise: 56% of L ERRORs are subst_only; results/judge_label_disagreements.csv is there for dataset-E adjudication.
  All headline numbers were re-derived independently, with placebos, in results/audit_headlines.json. Outputs: method_out.json
  / full_method_out.json (workspace root; also results/method_out.json) (predict_* = oriented scores), results/analysis.json,
  results/summary.md.
iteration: 1
workspace_path: >-
  /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_4
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json
out_dependency_files:
  file_list:
  - method.py
  - full_method_out.json
  - mini_method_out.json
  - preview_method_out.json

--- Artifact 4 ---
id: art_U4Hsqt4Ay9Tg
name: gen_art_dataset_1
type: dataset
title: Held-out logic translation test set, panel-checked
summary: >-
  Held-out NL->FOL faithfulness meta-evaluation set (run_u75jRHUss0zo, iter 1, dataset E). full_data_out.json (exp_sel_data_out,
  27.7 MB) has 4 groups. (1) heldout_candidates: 8,507 rows = real FOL candidates for 700 screen-disjoint sentences. Strata:
  MALLS-train L25=300 (>=25 words, >=3 conditions; includes a pre-registered 100-sentence top-up), L20=150, EXC=100 (unless/except/without),
  and FOLIO-train CTRL=150. Generators: 10 LLM slots over 9 families, few-shot at temperature 0; zero-shot Llama-70B/Qwen3;
  GPT-5.1 on 200 sentences; ccg2lambda; the MALLS GPT-4 gold as a system. input=JSON{text,candidate_fol,reference_fol,system,prompt_variant};
  output=CORRECT/ERROR/CONTESTED/UNRESOLVED/UNPARSEABLE. Labels combine the shared z3 solver labeller with a blind, nonce-disguised,
  family-disjoint panel (Haiku-4.5/GLM-4.6/Kimi-K2; Haiku adjudicates only GLM/Kimi disagreements). The combination rule gives
  tier A (solver), B (panel-decided VOCAB_GRAN/COMPOUND) and C (no trusted reference). Metadata per row: sentence_id (bootstrap
  cluster), item_id, strata {words,n_quant,depth,n_conditions,exception_type,source_stratum,l25_topup_batch}, auto_label,
  repair_ops, panel_votes, error_ops, label_tier, reference_status, correct_not_equivalent, reading_choice, disguised_text/fol.
  Tier A+B testable: L25 176 CORRECT/697 ERROR; L20, EXC and CTRL are also testable. (2) heldout_sentences: 700 rows with
  reference status (GOLD_PANEL_OK 95, PANEL_REPAIRED 145, NO_TRUSTED_REFERENCE 295, TRUSTED_AGREED 36, DISPUTED 112). (3)
  panel_calibration: 77 synthetic gate items plus 96 expert track-H real-error pairs with panel votes. (4) screen_audit: 1,173
  Logic-LM track-L and curated track-H rows keyed by the screen's item_id; also in screen_adjudicated_labels.json. Caveats:
  the panel is STRICT. Its majority accuracy on real errors is 0.727, and it accepts only 0.61 of expert-corrected formulas.
  It rejected 82% of MALLS gold, so ERROR is over-called: confirm on tier A too. HELD-OUT: iteration 2 must not tune thresholds
  on it. Primary analysis = tiers A+B excluding CONTESTED and reading_choice, bootstrapped by sentence_id. See dataset_card.md.
  Cost $9.83.
iteration: 1
workspace_path: >-
  /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_dataset_1
out_expected_files:
- data.py
- full_data_out.json
- preview_data_out.json
- mini_data_out.json
out_dependency_files:
  file_list:
  - data.py
  - full_data_out.json
  - mini_data_out.json
  - preview_data_out.json
  data_file_paths:
  - full_data_out.json
  - mini_data_out.json
  - preview_data_out.json

--- Artifact 5 ---
id: art_TaxJRnPcJMuZ
name: gen_art_experiment_5
type: experiment
title: Peer agreement plus text checks, held-out test
summary: >-
  Held-out confirmation of PEER+TEXT (NL->FOL faithfulness without gold) on dataset E (8,507 candidate rows, 700 sentences),
  frozen on the iteration-1 screen (prereg sha256 b9f28b1b, git a6896ce) and scored once. PEER = graded cross-family consensus
  (claim units, peer aligned into candidate vocabulary, finite-model refuter + z3 entailment; support/coverage/g_score, unit
  error codes); TEXT = iteration-1 L2-bow + L3 (text-only questionnaire vs z3 role profile); fused by a screen-fitted logistic.
  RESULTS (R_AB tiers A+B, 1822 ERR/864 COR): PEER+TEXT AUROC .790 [.75,.82] (stratified .753; long pool .768; tier-A L20+EXC
  .818) vs iteration-1 c_score_align .782, NF-anchored c_score .743, TEXT .693, local Qwen3-8B disguised judge .712. Delta
  vs local judge +.078 [.043,.112] pooled, +.115 long pool, +.075 stratified; CTRL -.031 n.s. The pre-registered flash-lite
  judge bar is UNTESTABLE (shared OpenRouter key hit $0 at 18:00 UTC; the replacement key was also exhausted, polled 19:10-22:13
  UTC; 20 rows); the local judge is a labelled secondary bar. Fusion does NOT beat c_score_align alone (stratified +.011 n.s.;
  tier A c_score_align .860 > .818), and that aligner is shared with the solver labeller (confound open). Name-free alignment
  'failed' the screen gate only through a threshold-tie artefact; post hoc NF-anchored passes (RENAME FA .074, ROLE_PERMUTE
  recall .77) and its fusion gives .759 on E. P1 INCONCLUSIVE (PEER>TEXT on ADD/DROP errors, TEXT>PEER on peer-endorsed),
  P2 REFUTED, P3 INCONCLUSIVE (gap vs judge grows with length, diff-in-delta +.146 CI>0), P4 REFUTED (fused RENAME FA .385).
  Unit-code typing at chance (.37 vs .38). Disguise improves the judge (no contamination benefit). Within-stratum placebo
  .59 (composition), global .50. FILES: results/per_item_E.jsonl (row_key=item_id|prompt_variant, fold_E=sha1('E_folds_v1|'+sid)%5,
  every score) for the iteration-3 join; results/analysis.json, tables.md, p_tests.json, deviations.json, prereg.json; src/peer_text.py
  reusable functions; method_out.json (exp_gen_sol_out, predict_* for all metrics). Audits: tests/audit_rederive.py re-derives
  pooled AUROCs and headline delta to 1e-9; tests/placebo_headline.py (shuffled labels fail); prefilter audit 0 conflicts;
  judge prompt identity 30/30. OpenRouter spend $0.155.
iteration: 2
workspace_path: >-
  /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_5
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json
out_dependency_files:
  file_list:
  - method.py
  - full_method_out.json
  - mini_method_out.json
  - preview_method_out.json

--- Artifact 6 ---
id: art_HepAw8c6Eu7-
name: gen_art_evaluation_1
type: evaluation
title: Re-checking earlier logic-metric results across label sets
summary: >-
  Zero-LLM-spend, CPU-only re-analysis of the iteration-1 artifacts (exp A FOL-Triage, exp C consensus c_score, exp D judges/baselines,
  dataset E screen adjudication), joined on item_id. eval.py (+src/) writes eval_out.json (exp_eval_sol_out, validated; ~5.9k
  flat metrics_agg keys + structured metadata incl. VERDICT; 1,380 per-item examples with oriented scores, per-regime labels,
  PT OOF), tables/*.csv (each with a '# source:' line), figures/fig_regime_shift and fig_forest_common (json/png/pdf), and
  audit/ scripts. KEY FINDINGS. (1) Re-derivation gate: 57/57 reviewer audit numbers reproduce (n=389/160 err/151 sents; c_score
  .842, fused .767, judge_disg .785; tier A+B n=304 fused .872, bow .817, c_score .776, judge .771). (2) Same-item, same-label
  common sets for 13 regimes (testable: R_SOLVER_CONS n=373/155 err, own-label A/C/D, R_ADJ_AB 298/165, R_ADJ_ALL 498/271,
  CONTESTED->C/E, L_UNPARSEABLE_AS_ERROR 413/195; R_ADJ_A and all track-H regimes are untestable, reported sign-only). (3)
  The iteration-1 rule FAILS for fused_H and c_score in every regime (rewrite FA 0.275 / 0.96). fused_H minus judge is -0.013
  under solver labels but +0.096 [.020,.171] under A+B; c_score minus judge is +0.067 [-.012,.148] under solver labels and
  +0.006 under A+B. (4) Label-only shift solver->A+B on the same 161 items: bow +0.102 and fused +0.080 (CI>0) go up; c_score
  -0.106 goes down. Rank Kendall tau is 0.60. On the 58 flipped items, bow/fused flag 81-83% vs c_score 34% (instrument-sharing
  confirmed). (5) SCREEN PREVIEW: PT (cross-fitted c_score+bow_uncarried+l3) minus judge_cheap_disg is +0.089 [.010,.165]
  solver, +0.104 [.039,.175] A+B, +0.090 [.038,.142] all tiers, +0.118 unparseable-as-error. Nested S4+PT over refit S4 is
  +0.04-0.06 (CI>0). Screen bar that iteration-2 confirmation must beat = these deltas. (6) P1: the structural clause is untestable
  (all QUANT/SCOPE/BIND/SWAP/NEG cells have <15 errors); text beats peers on peer-endorsed errors (CI>0). P2a CONFIRMED only
  for all tiers. P2b depends on the comparator: vs c_score the gain comes from endorsed errors; vs bow it comes from non-endorsed
  errors. (7) At matched FA 0.10 the ORIGINAL cheap judge has higher recall than the disguised one (+0.11/+0.20). Contamination
  DiD CIs include 0 but MDE = 0.12-0.21, so a 0.05 effect is undetectable. Frontier minus cheap under A+B is +0.166. (8) Invariance
  comparisons across A/C/D used different rewrite sets. (9) Candidate B was planned but gen_art_experiment_2 is an empty .aii/
  dir: it never ran. (10) Exp C's -0.94/SD length interaction reproduces exactly. Exp A's L2-bow = n_unanch+uncarried (0.737)
  vs bow_uncarried (0.711). Panel expert-pair acceptance is .613 (unambiguous). Independent re-derivation (different code
  path) matches all headline numbers. On permuted labels the cross-fitted PT is biased below 0.5; the observed deltas exceed
  all 20 null deltas (null max .047 solver / .087 A+B).
iteration: 2
workspace_path: >-
  /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1
out_expected_files:
- eval.py
- full_eval_out.json
- mini_eval_out.json
- preview_eval_out.json
out_dependency_files:
  file_list:
  - eval.py
  - full_eval_out.json
  - mini_eval_out.json
  - preview_eval_out.json

--- Artifact 7 ---
id: art_7GxreYjATkC5
name: gen_art_experiment_6
type: experiment
title: Peer agreement vs paid AI judges on held-out logic
summary: >-
  T1 head-on test on held-out NL->FOL dataset E (8,507 real candidates, 700 sentences). The frozen peer-agreement consensus
  metric (c_score_align, exp 5) and PEER+TEXT fusion (p_peer_text) are compared with newly scored paid API comparators: gemini-2.5-flash-lite
  rubric-A JSON judge (disguised + original, every parseable row), gpt-4.1-nano P(YES) judge (both views), gemini-3.1-pro-preview
  frontier judge (original view, 284-row frame; disguised view blocked by the pre-registered shared-key reserve rule), API
  round trip (flash-lite verbaliser -> DeBERTa NLI/mpnet) and API SC-5 (nano, T=0.7, z3 modulo vocabulary); plus S4_full,
  a cross-fitted stack of all 28 baselines. Pre-registered in prereg_T1.json (sha256 c2a6cf84, frozen before any sweep score).
  Main population R_AB E_POOL PRIMARY n=2,686 (1,822 ERROR/864 CORRECT, 292 sentences); sentence-cluster bootstrap B=2000.
  RESULTS: stratified AUROC c_score_align 0.741 vs flash-lite disguised 0.642 (pooled 0.782 vs 0.696). (a) CONFIRMED: strat
  dAUROC +0.099 [0.049,0.146]; long pool +0.116 [0.070,0.163]; R_A L20+EXC +0.299; also vs best cheap judge (nano orig) +0.089
  [0.043,0.134]. (b) CONFIRMED: nested [S4_full+c]-S4_full strat +0.039 [0.021,0.057], permutation-null p95 0.009; c alone
  ~= S4_full (+0.006 [-0.031,0.042]). (d) CONFIRMED: frame ratio vs frontier 0.957 [0.887,1.034], consensus $1.2e-4 vs frontier
  $3.65e-3/item, nested frame gain +0.037 [0.008,0.066]. VEX aligner-confound control CONFIRMED: +0.306 [0.232,0.376]. M3
  (smaller length slope than the judge) DISCONFIRMED: +0.146 [-0.051,0.361]. Overall T1 (this artifact): CONFIRMED. Caveats:
  no advantage on the short FOLIO CTRL stratum (-0.069 [-0.23,0.10]) or on <12-word / <=1-condition sentences; the advantage
  concentrates in long, conditioned, exception sentences (EXC +0.197). Consensus misses aligner-masked MEANING_RENAME errors
  (recall 0.07 at FA 0.10 vs judges 0.13-0.20) and peer-endorsed errors (0.00). Flash-lite contamination DiD +0.105 [0.006,0.201]
  (MDE 0.14). Test-retest Spearman 0.975. API spend $2.395 (cap $4.60). Independent checks: tests/audit_T1.py (5 headline
  numbers match to 1e-3) and tests/audit_raw_T1.py (raw files -> identical confirmatory/long-pool delta and frame ratio; placebos
  fail as required). Files: results/analysis_T1.json, verdict_T1.json, tables_T1.md, per_item_T1.jsonl, deviations.json, api_cost_ledger.json,
  llm_cache.jsonl; figures/forest_T1, complexity_curves; full_method_out.json (predict_* oriented scores for every metric).
iteration: 3
workspace_path: >-
  /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json
- reproducibility.md
out_dependency_files:
  file_list:
  - method.py
  - full_method_out.json
  - mini_method_out.json
  - preview_method_out.json
  - reproducibility.md

--- Artifact 8 ---
id: art_cxnoDYQNFolW
name: gen_art_experiment_7
type: experiment
title: Model agreement vs judges on long rule sentences
summary: >-
  R_COMP (221 templated long rule sentences, >=25 words, >=3 conditions, one unless/except/provided-that/only-if clause; references
  trusted by construction) translated by 10 few-shot LLM slots (9 families) in two conditions. SIG (signature block given)
  is labelled by pure z3 equivalence to the weak or strong reading; FREE uses dataset 3's solver labels (tier A only: the
  dataset-E panel was not run because the shared key was exhausted, so FREE is NOT_TESTABLE and descriptive). PRIMARY (pre-registered,
  criterion c): within-template AUROC of c_score_sig (share of family-disjoint peers not z3-equivalent) vs the disguised gemini-2.5-flash-lite
  rubric-A judge on 1,904 SIG rows (395 ERROR / 1,509 CORRECT, 220 sentences): 0.954 vs 0.587, delta +0.367 [0.328, 0.404]
  (sentence-clustered, template-stratified bootstrap, B=2000) -> PASS. vs the original-text judge: +0.278 [0.239, 0.319].
  Nested [judge + c_sig] over [judge] +0.377; the judge adds ~0 over c_sig. Frontier gemini-3.1-pro on a 60-row subsample:
  c_sig 0.956 vs frontier orig 0.932 / disg 0.735; [frontier + c_sig] over frontier +0.088 [0.019, 0.172]. On R_COMP the disguise
  itself costs judges AUROC (cheap +0.085, local Qwen3-8B +0.175 orig - disg), because templated sentences cannot be memorised.
  Rename invariance: NF-anchored and HYB consensus are invariant (FA 0.26 = unrenamed), ALIGN and SIG-exact are not (FA 1.0
  on nonce renames). Mechanism: error endorsement e = 0; consensus false alarms are correct translations of the minority strong
  reading (flagged 96% vs 14% for weak). Complexity: no length slope for consensus (GEE). FREE tier A: c_align - judge +0.214
  [-0.034, 0.377], and consensus AUROC falls from 0.95 (SIG) to about 0.80, the vocabulary-divergence cost. Every headline
  number was re-derived from the raw files via an independent brute-force path (tests/rederive_raw.py, all match to 1e-9;
  placebos fail). Outputs: method_out.json (R_COMP_SIG, R_COMP_FREE; predict_* oriented higher = error), results/rcomp_candidates.jsonl
  (per-row labels, strata, z3 class ids, all scores), results/analysis.json, results/tables.md, results/deviations.json (15
  deviations), src/consensus_rcomp.py (consensus_exact, consensus_scores). Spend $1.58.
iteration: 3
workspace_path: >-
  /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json
- reproducibility.md
out_dependency_files:
  file_list:
  - method.py
  - full_method_out.json
  - mini_method_out.json
  - preview_method_out.json
  - reproducibility.md

--- Artifact 9 ---
id: art_YYD-HDzfQfEj
name: gen_art_experiment_8
type: experiment
title: Rename-proof logic consensus and error-type tests
summary: >-
  Iteration-3 T3+T5 experiment (workspace gen_art_experiment_8). PART A: PEER_HYB consensus = ALIGN (name-similarity eqmv)
  OR NF-anchored name-free map, z3-verified; pair verdicts for every E candidate-peer pair in results/pairs_E.jsonl (sentence_id,
  cand, peer, align_eq, nf_eq, hyb_eq, nf_cost; joinable by T4). Pre-registered selection (results/prereg_hyb.json, frozen
  before label join): NEITHER HYB nor NF-anchored eligible (rename FA on PERTURB RENAME_SYN/NONCE HYB 0.841/0.700, NF 0.686/0.485
  at screen thresholds; exp D RENAME 0.050/0.030) -> nothing frozen, sibling R_COMP read uses ALIGN (results/selection.json).
  Mechanism: NF keeps 100% of a base's peer endorsers under renames (flip 0), HYB 74-75%, ALIGN 0-33%; NF's FA equals the
  unrenamed-reference FA (references often unendorsed on long sentences). E R_AB stratified AUROC (sentence-cluster CI): c_hyb
  0.738, c_align 0.741, c_nf 0.686; HYB-ALIGN -0.004 [-0.011,0.004]; HYB-NF +0.052; HYB-local Qwen judge +0.060 [0.018,0.100];
  placebo 0.515. Over-alignment: HYB's extra agreements are label-discordant 0.388 vs 0.127 for ALIGN agreements. PART B:
  27 metrics on 4,234 PERTURB mutants + 868 controls + 300 bases (results/perturb_scores.jsonl, perturb_sensitivity.csv, perturb_downup.csv,
  invariance_table.csv, tradeoff.csv, coverage_perturb.csv; prereg_perturb.json). Within-base AUROC over all E-base mutants:
  PEER+TEXT 0.948, c_align 0.866, c_hyb 0.847, p_text 0.845, l3 0.816, c_nf 0.785 (0.50 on MEANING_RENAME), S4_local 0.753,
  round-trip NLI 0.749, flash-lite judge (disguised) 0.680, SC-5 0.666, L2-bow 0.659, local Llama/Qwen judges (nf4) 0.653/0.643,
  pilot metrics ~0.50. Consensus polarity-symmetric (|DOWN-UP|<0.01); local judges, embedding round trip and L3 miss DOWN
  edits (-0.12 to -0.15). PART C: peer-medoid typed-repair typing 0.328 [0.277,0.387] > majority 0.177; oracle 0.802; 20 s
  fallback unchanged. PART D: src/consensus_lib.py (consensus_score exact/align/nf/hyb, graded_consensus, peer_pool, equivalent_modulo_vocab,
  minimal_typed_repair) + tests (31 pass). Deviations: 16 GB GPU -> nf4 local judges with thresholds refit on nf4 E calibration
  rows (AUROC cost 0.015-0.035); S4 full-E fit. Cost $0.35 OpenRouter. Independent raw re-derivation (tests/audit_raw.py)
  reproduces all headline numbers exactly; placebos ~0.5.
iteration: 3
workspace_path: >-
  /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_8
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json
- reproducibility.md
out_dependency_files:
  file_list:
  - method.py
  - full_method_out.json
  - mini_method_out.json
  - preview_method_out.json
  - reproducibility.md

--- Artifact 10 ---
id: art_FWy8D4_y9GBn
name: gen_art_evaluation_2
type: evaluation
title: Why cross-model agreement flags logic errors
summary: >-
  T4 consensus-mechanism audit on dataset E (CPU only, $0, no LLM calls) plus a file-sourced verified record of iteration
  2. Recomputed the label-free pairwise z3 eqmv matrix over every parseable output of all 700 E sentences (29,107 pairs; bit-identical
  across 3 runs); it reproduces the FROZEN c_score_align (G2 mismatch 0.33%, explained by PYTHONHASHSEED); gates G0/G1 pass.
  R_AB (2,672 scorable rows): graded c_score_align AUROC 0.784 vs binary majority END_MAJ 0.669 (delta +0.114 [0.091,0.140]);
  END_MAJ e=0.124, d=0.537 (AUROC_b = 1-(e+d)/2, a bookkeeping identity). Aligner-free c_score_exact 0.748. VOCAB_EXACT pure-z3
  labels (85/412): c_score_align 0.929. eqmv non-transitivity 15.8% (classes approximate). Verdicts: M1 (e falls with n_conditions,
  partial) INCONCLUSIVE; M2 (d rises with words) CONFIRMED by the prereg rule but NON-SPECIFIC (shuffled-label placebo still
  +1.75; label x words interaction -0.29 [-0.77,0.20]); NET Delta(e+d) words T3-T1 +0.356 [0.198,0.493] -> binary consensus
  DEGRADES with length, driven by d (placebo -0.034, covers 0); SCATTER SI_err 0.159 vs SI_cor 0.760 (ratio 4.45), SI_err
  falls with conditions, joint failure rises (errors co-occur but differ); M3-local INCONCLUSIVE; M4 k95=3 CONFIRMED (AUROC(k)
  0.685..0.784; long-sentence tercile k95=5); cross-fitted best 3-family pool deepseek+microsoft+openai OOF 0.785 = full pool
  at ~$0.002/sentence; LOFO min delta -0.011 (no single family carries it). Verified record: 48/48 hypothesis clauses VERIFIED_MATCH;
  reviewer PT-S4 audit reproduced (points 1e-4, CIs 0.01) plus stratified rows (PT-S4 strat +0.059); corrections, R_PANEL
  renames, R_ADJ gate (DROPPED), B2 dead end, PERTURB counts (4234/868/1354), label facts. Independent audit re-derived 13
  headline numbers to 1e-9 with placebo checks. Scope: E only (R_COMP rerun via shipped pairwise_matrix()/ed_decomposition()
  in iteration 4). Files: eval_out.json (335 metrics, one example per R_AB row with predict_c_score_align/exact/b_endmaj/endfam2/c_k3_best_oof),
  pairwise_classes_E.jsonl (label-free join key), tables/*.csv with '# source:' lines, figures fig1-4, prereg_mech.json, audit/,
  results/part_a.json.
iteration: 3
workspace_path: >-
  /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2
out_expected_files:
- eval.py
- full_eval_out.json
- mini_eval_out.json
- preview_eval_out.json
- reproducibility.md
out_dependency_files:
  file_list:
  - eval.py
  - full_eval_out.json
  - mini_eval_out.json
  - preview_eval_out.json
  - reproducibility.md

--- Artifact 11 ---
id: art_VIF75I5R6f0v
name: gen_art_research_1
type: research
title: What is new about peer agreement for logic
summary: >-
  Prior-art positioning (web research, $0 LLM spend, 63 sources, 139 verbatim quotes machine-checked against fetched text)
  for the iteration-3 claim that cross-family solver consensus is a gold-free NL->FOL faithfulness metric. SCOOP RULE (multi-family
  translations + solver equivalence + faithfulness-label meta-eval on NL->FOL): no hit meets all three, so C1 is not scooped.
  Closest neighbours meet two of three each: ARc 2511.09008 (NL->SMT, k LLMs, per-translation confidence = share of k translations
  entailing it, i.e. the same score form as c_score, but a fixed schema and downstream-QA labels); NoTB 2608.21962 (RTL, 4
  families, precision 63/85.3/87/94.7% at >=1..4 families, coverage 100/49/33/27%, spec-level, no AUROC); GenV 2609.11085
  (NL->FOL, single trained verifier, AUROC 0.961 on Z3-reference labels; single-model SC K=5 = 0.863; the judge beats GenV
  0.778 vs 0.679 when labels switch to panel intent). The closest meta-evaluation design is SCP-NL2TL 2608.05439 (NL->temporal
  logic, single-model SC vs judge vs back-translation AUROC by difficulty tier; SC AUROC rises with tier). VERDICTS: C1 NEEDS-QUALIFIER
  (the method is not new; claim the first meta-evaluation of cross-family consensus as a per-candidate NL->FOL faithfulness
  score vs an API judge, nested over the baseline stack; win and loss wordings are given); C2 SAFE (cite GenV's label-target
  reversal and wrong-gold rates, 2606.02837 v1 39%/36% vs v2 42.5%/42%); C3 NEEDS-QUALIFIER (predicate alignment exists in
  LogicLLaMA and Vossel; no neighbour reports a rename false-alarm rate); C4 NEEDS-QUALIFIER (balanced-accuracy maths; the
  scatter premise is stated by LLMs-as-Jury, CLOVER and Chen & Avizienis 1978, who noted identical wrong results from missing
  logic; the new piece is a measured identical-wrong vs both-wrong curve over number of conditions, set against Eckhardt-Lee's
  coincident-failure-rises-with-difficulty); C5 NEEDS-QUALIFIER (LLMs-as-Jury already recommend 3-4 cross-family models; effective-N
  results: 7 models ~ 2.58, 9 judges ~ 2). Also supplies: the positioning table on 10 axes; a premise-evidence table (60%
  agree-when-both-wrong on MCQ, rho 0.20-0.59, beta 0.052-0.127, KL 1255 tests); judge-degradation evidence (AutoEval: equivalence
  verification fails beyond toy complexity; >20 operators <50%); cost norms; 8 required extra rows (single-family SC, precision@coverage
  by k, endorsement vs both-wrong by conditions, k-curve per tercile, rename FA per matcher, label-protocol sensitivity, n_eff,
  cite ARc); AuthorYYYY citation strings; and a search log. Files: research_report.md (main), notes/QUOTES.md (quote ledger).
iteration: 3
workspace_path: >-
  /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_research_1
out_expected_files:
- research_out.json
- reproducibility.md
out_dependency_files:
  file_list:
  - research_out.json
  - research_verification.json

--- Artifact 12 ---
id: art_D7k2ZWgE3nVd
name: gen_art_experiment_9
type: experiment
title: Peers given the formula's symbols copy its errors
summary: >-
  T6-E (iteration 4, DEVELOPMENT set E): Candidate-Signature Consensus (CSC). 3 family-disjoint cheap peers (DeepSeek-V3.2
  / Phi-4 / GPT-4.1-mini / Qwen3-235B) translate the sentence with the dataset-E few-shot prompt plus the candidate's own
  symbol list; c_csc = 1 - share of peers z3-equivalent to the candidate (lowercased name+arity, no aligner); higher = more
  likely ERROR. BUDGET EVENT: the platform refused paid calls (HTTP 403, shared 'Test idea' phase budget exhausted by siblings)
  after 1,033 of ~9,000 planned calls; this artifact spent $0.108. CSC is evaluated on PRIMARY = 354 R_AB rows (196 ERROR/158
  CORRECT) whose 3 peer calls completed (fixed in prereg addendum before scoring); FORMAT-ONLY, PLACEBO, RENAME NOT_RUN; L25
  NOT_READ. $0 analyses use all 2,686 rows. RESULT (sharp negative, provisional): CSC lowers correct-row divergence d (0.139
  vs 0.323 for the same free peers scored exactly) but raises error endorsement e (0.459 vs 0.173; MEANING_RENAME-type 0.82
  vs 0.04; ADD 0.49 vs 0.14) = anchoring. Strat AUROC c_csc 0.614 [0.49,0.74] vs FREE-matched exact 0.770, c_score_align 0.774,
  flash-lite judge 0.664; paired delta vs FREE exact -0.156 [-0.290,-0.031] (holds on GE2/MINI200 and after removing phi-4
  exemplar leakage). d still rises with length (GEE slope +1.25 [+0.41,+2.09]); no nesting gain over S4_full (+0.006). Gates
  (csc_gate_E.json, PROVISIONAL): G1 FAIL, G2 FAIL (R_AB; L25 NOT_READ), G3-E NOT_RUN, G4 null, G5 PASS ($5.25e-4/candidate).
  Recommendation for iteration-5 rule: CSC not a fix; fall back to frozen c_score_align + p_peer_text. $0 FULL-population
  facts: matched free peers exact vs ALIGN d 0.583 vs 0.328; 53% of free-exact disagreements with CORRECT candidates are structural
  (only 20% of flagged CORRECT rows fully vocabulary-resolvable); 9-peer c_score_align rename FA 0.595->0.868 under WordNet-synonym
  rename. Reproduction checks pass (eval-2 3-pool strat 0.7428 vs 0.7427). Headline CSC/FREE numbers independently re-derived
  (results/audit_rederive.json; permuted-label placebo CI includes 0). Files: method.py (stage runner), src/csc.py (library
  + tests), tables.md, csc_gate_E.json, results/per_item_csc_E.jsonl, results/analysis.json, results/llm_cache.jsonl (only
  copy of 599 paid peer generations), method_out.json (exp_gen_sol_out; predict_* higher=ERROR; NA where CSC not generated),
  deviations.json.
iteration: 4
workspace_path: >-
  /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_experiment_9
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json
- reproducibility.md
out_dependency_files:
  file_list:
  - method.py
  - full_method_out.json
  - mini_method_out.json
  - preview_method_out.json
  - reproducibility.md

--- Artifact 13 ---
id: art_pAmLrGqsmFUx
name: gen_art_experiment_10
type: experiment
title: Do symbol hints help model agreement checks?
summary: >-
  Iteration-4 T6-P experiment on Candidate-Signature Consensus (CSC): three peer families (deepseek-v3.2, phi-4, gpt-4.1-mini;
  +qwen3-235b for K4) are cued with the candidate's own symbol list, and agreement is exact case-insensitive z3 equivalence.
  DEVIATION D-BUDGET: the run-wide OpenRouter budget was exhausted by other artifacts before the first pilot call (403 aii_run_budget_exhausted;
  :free models also rate-limited), so NO CSC peer was generated. Gates G3-P (rename FA), G4 (anchoring) and MT (typing on
  E) are UNTESTED, not failed. The spend was $0.0000088. The full pipeline is built, unit-tested (73 tests pass) and resumable.
  The job list data/csc_jobs.jsonl holds 17,075 calls, projected at $3.07 using sibling-measured prices; run it with `method.py
  --stage pilot,peers,...`. Zero-cost arms, all labelled, frozen in prereg_csc_P.json before any join: (1) SIGPROXY: exp-7
  SIG outputs of the same four families, cued with the closed template signature, on 77 R_COMP bases. Recall on 1,196 mutants
  is 1.000 and recall given base endorsed is 1.000. On the same 74 long bases, correct-base FA d is 0.149 cued vs 0.757 uncued
  FREE3-ALIGN, a paired diff of -0.608 [-0.716, -0.500]. Rename FA is 1.000 under a base-signature cue, which shows renames
  need re-cueing. (2) SIG labelled check, k=3 family-matched: within-template AUROC 0.930 [0.916, 0.943] vs 9-peer c_score_sig
  0.952 and disguised flash-lite judge 0.587. (3) Same-vocabulary typed repair: ORACLE 0.928 on E (exp 8 oracle 0.802); SIGPROXY
  majority 0.784 [0.711, 0.849] on R_COMP; uncued FREE3 majority 0.123 on E (exp 8 baselines: medoid 0.328, judge 0.326).
  (4) Uncued d grows with length on E (c_align 0.47/0.80/0.91 by word tercile). (5) LOCAL2 is a secondary arm (qwen2.5-1.5b
  and gemma-2-2b, same CSC prompt, 27 E bases). Small peers use genuine listed symbols 0.81 and synonyms 0.70, but foreign,
  donor and nonce symbols only 0.11-0.16. Using a foreign or donor symbol never reproduced the mutant (0/25). Delta-anchor
  was 0 for ADD_FOREIGN and MEANING_RENAME; power is low (base endorsement 0.30). Independent re-derivation: tests/rederive.py
  makes 429 table checks with 0 mismatches; tests/rederive_headline.py recomputes the AUROC, the paired d, typing and the
  d terciles from raw files with failing placebos. Outputs: method_out.json (PERTURB_E_CSC 3,456, PERTURB_RCOMP_CSC 1,946,
  RCOMP_SIG_CSC 2,210; predict_* strings, higher = error; c_csc = NA), results/tables.md, anchoring.csv, controls_fa.csv,
  typing_csc.csv, rcomp_sig_csc.json, local2_anchoring.json, csc_gate_P.json, firewall.json (FREE labels never read), perturb_csc_scores.jsonl.
iteration: 4
workspace_path: >-
  /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_experiment_10
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json
- reproducibility.md
out_dependency_files:
  file_list:
  - method.py
  - full_method_out.json
  - mini_method_out.json
  - preview_method_out.json
  - reproducibility.md

--- Artifact 14 ---
id: art_2OmxzMInZZJY
name: gen_art_dataset_4
type: dataset
title: Fresh logic test set, paused by budget
summary: >-
  E2 (PARTIAL, budget-stopped): the frozen, sealed design of a fresh NL->FOL faithfulness confirmation set disjoint from dataset
  E, labelled by E's byte-identical code (code_freeze.json). The run-level 'Test idea' OpenRouter budget ($7, shared by all
  concurrent artifacts) ran out at 07:26 UTC after this artifact spent $0.24. The proxy refuses paid calls until the user
  raises the budget. WHAT EXISTS: (1) 550 active sentences with gold references, pre-registered and hashed before generation
  (prereg_E2.json): L25 350 (MALLS-v0.1-train, >=25 words, >=3 conditions, 45% in the 30-34-word bin, mean 28.8 words / 4.65
  conditions); EXC 100; DT 100 (ProverQA dev, prover-built gold, 1 per entity skeleton, >=15 words and >=2 conditions). Also
  a ranked L25 surplus order (98) and a DT reserve (10). EXC CAVEAT: the core-exception supply is exhausted (E took all 67
  MALLS-train items; MALLS-test has 3, all excluded), so E2-EXC is 92 'without' + 8 non-XOR 'but not' items, core-marker share
  0.0. (2) A 30-sentence pilot (12 L25 / 8 EXC / 10 DT): 300 real candidates from E's 10 few-shot slots (9 families, temperature
  0) + 30 gold-as-system rows, solver-labelled by E's labeller. Without panel votes E's final rule gives 36 ERROR (tier A_unaudited_ref),
  244 UNRESOLVED, 20 UNPARSEABLE, 0 CORRECT. (3) A partial panel drift check: the 77 synthetic gate items were replayed with
  a fresh cache (majority agreement with E's stored votes 0.974; balanced accuracy P1 0.861 / P3 0.875 / R1 0.837 vs E 0.861
  / 0.85 / 0.863). Track H was cut off, so the stop rule is UNDECIDED. (4) A seal: candidates_E2_nolabels.jsonl vs sealed/labels_E2.jsonl
  + references, sha256 in seal.json, verify_seal.py passes. (5) testability_E2.json: NO cell is testable now. Projected MDE80
  if completed is 0.112 at L25=350 and 0.099 at 450; the direction's '400 L25 detect +0.08' claim is wrong (needs ~690). full_data_out.json
  groups: e2_candidates (300), e2_gold_as_system (30), e2_sentences (550, status PENDING_GENERATION_BUDGET_STOP for 520),
  e2_panel_drift (173). All source-checked rows verify. RESUME: `bash src_e2/run_all.sh` (resumable; projected $6.8, ~2.5
  h). DOWNSTREAM: in this state E2 cannot confirm any metric. Iteration 5 must either wait for the resume or use E2 only as
  a pipeline/seal smoke test. Deviations D0-D7 are in dataset_card.md.
iteration: 4
workspace_path: >-
  /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4
out_expected_files:
- data.py
- full_data_out.json
- preview_data_out.json
- mini_data_out.json
- reproducibility.md
out_dependency_files:
  file_list:
  - data.py
  - full_data_out.json
  - mini_data_out.json
  - preview_data_out.json
  - reproducibility.md
  data_file_paths:
  - full_data_out.json
  - mini_data_out.json
  - preview_data_out.json

--- Artifact 15 ---
id: art_BvAL_KZTZuw8
name: gen_art_evaluation_3
type: evaluation
title: Can shared vocabulary fix consensus blind spots?
summary: >-
  T8 (iteration 4) is a CPU-only evaluation: no LLM calls, $0. It never reads the sibling CSC experiment. Eval-2 functions
  are imported unchanged (code sha dd73975642f428cc). E and R_COMP are DEVELOPMENT data, so nothing here is confirmation.
  Gates all pass: G0 reproduces END_MAJ e 0.124 / d 0.537 and AUROC c_exact 0.748 / c_align 0.784; G1 pairs_E coverage 100%;
  G2 align concordance 99.97%; G3 recomputed R_COMP scores match exp 7 on 100% of rows. prereg_d_split.json was hashed before
  Part 1 ran. PART 1 (E, 2,672 scorable rows, 25,358 candidate-peer pairs). Pair classes (9-family): EXACT 13.6%, NAME_ONLY
  0.3%, ALIGN_ONLY 15.1%, VOCAB 1.6%, IRREDUCIBLE 69.4%. Matched 3-family pool (PRIMARY): d under END_MAJ 0.415; predicted
  d_floor (R_point_label, an oracle-assisted prediction) 0.402 [0.336, 0.471]; bracket [0.396, 0.415]; exact-only 0.683; no-anchoring
  oracle floor 0.385 (0.345 with a labelled denominator); e_ceiling 0.162. 9-family: 0.537 / 0.532 / 0.522, with oracle 0.586.
  The pre-registered gap_closed rule is ill-conditioned: its denominator is 0.013. Behind d, 77% (9-family) / 61% (3-pool)
  of non-agreeing peers of CORRECT candidates are labelled ERROR, and only 9% of CORRECT-CORRECT disagreements are NF/HYB-resolvable.
  The specificity placebo shows VOCAB agreements are not label-specific (ratio 1.98 [0.43, 11.4] 3-pool; 0.83 9-family). c_vres
  does not beat c_score_align on L25 (-0.014 [-0.028, -0.001]), which predicts that G2 fails. NET stays DEGRADES under every
  rule. PART 2 (R_COMP): SIG e 0.000, d 0.2596 (weak 0.143 / strong 0.965), SCATTER ratio 4.38. Paired same-slot-pair exact
  agreement is SIG 0.528 vs FREE 0.048, a drop of +0.479 [0.447, 0.513]. Post-hoc ALIGN recovers 41% of it, NF 18%, ALIGN∪NF
  45%. The out-of-sample validation of the Part-1 method FAILED: predicted 0.20 vs actual SIG endorsement 0.575, calibration
  error -0.37 [-0.42, -0.32]; Spearman across templates 0.97. So the instruments under-count vocabulary effects. PART 3 (power_E2.json):
  yield is L25 0.37, L20 0.53, EXC 0.64, CTRL 0.25. Planned L25 250/300/350/400 gives MDE80 0.130/0.119/0.110/0.103, all MARGINAL.
  Detecting +0.069 needs about 882 planned L25 sentences, or about 237 usable sentences in the long pool. R_COMP FREE needs
  at least 200 CORRECT rows. PART 4: 13 record tables (a)-(m) read by code with source lines; 64 claims, 60 match, 1 mismatch
  (the plan's $0.000996/candidate is a unit error: the source gives $0.000116 per candidate). The '26.8% of controls' figure
  holds for non-rename controls only. Audit: 11/11 independent re-derivations pass, and the placebos behave as expected. Outputs:
  eval_out.json (157 metrics; 2,672 E rows + 4,862 R_COMP rows), tables/*.csv, record.md, power_E2.json, pairwise_classes_RCOMP.jsonl,
  figures, README.md, reproducibility.md.
iteration: 4
workspace_path: >-
  /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3
out_expected_files:
- eval.py
- full_eval_out.json
- mini_eval_out.json
- preview_eval_out.json
- reproducibility.md
out_dependency_files:
  file_list:
  - eval.py
  - full_eval_out.json
  - mini_eval_out.json
  - preview_eval_out.json
  - reproducibility.md
</prior_work>

<build_on_prior_work>
BUILD ON WHAT THE EARLIER ROUNDS ALREADY PRODUCED. That is the default, not an option.

<prior_work> lists what this run has already built. Before planning anything
from scratch, go through it and find what this artifact can stand on:
- data that is already collected, cleaned, split or labelled
- models, fits, checkpoints or indexes that are already trained or built
- harnesses, scripts and evaluation code that already run
- the findings themselves, the NEGATIVE ones included — a condition already
  ruled out is a result to build past, not ground to cover again

Then say in `builds_on`, concretely, what this plan reuses: which artifact,
which file, from where. The executor gets a dependency's files only through
the direction's declared dependencies, so when the plan leans on an artifact
that is not among them, say in the plan where the executor picks it up
(workspace path, output file) and keep the plan runnable if it is missing.

STARTING A FRESH LINE is allowed on exactly two grounds:
1. The iteration's move is a WIDEN — the run deliberately went back to the
   original ask to screen different candidate answers, so a new line is the
   point of the round.
2. The line this would have continued is a SETTLED NEGATIVE — already tested
   well enough that pushing it further buys nothing.
On either ground, `builds_on` says which one it is and why, and still names
whatever infrastructure (data, harness, code) the new line can reuse.

"Cleaner to start over" is not one of the two grounds. Neither is a plan that
simply does not mention the earlier rounds.
</build_on_prior_work>

<own_your_inputs>
A STEP THIS PLAN COMMISSIONS MUST HAVE ITS INPUTS OWNED BY SOMETHING SCHEDULED.

If this plan pre-registers a later phase — a held-out confirmation, a blind
set, a second pass, a replication — that phase needs inputs of its own:
labels, ground truth, an annotation pass, a scored reference. Before writing
that phase into the plan, name what produces those inputs and where that
production is scheduled: inside this artifact's own steps, or as one of the
direction's declared dependencies. Say it concretely, not "labels will be
added" — which task, at which point in the plan.

A later step whose inputs nobody is scheduled to produce is not a plan for
that step, it is a plan to skip it while looking like it was included.
</own_your_inputs>



<instructions>
YOUR ROLE: Write a detailed PLAN for the artifact. A separate executor agent runs the actual artifact later.

You are a PLANNER, not an executor. Your output is a plan that tells the executor what to do and how.
Do NOT execute the artifact itself — a separate agent handles that. Your job is to plan it so well that the executor can follow your plan step by step.

You CAN and SHOULD: search the web, read papers, and explore library docs to make your plan concrete.
You CANNOT run shell commands or scripts — code execution is disabled. Research via web tools only.

Do NOT do the executor's job: don't download datasets, don't implement code, don't run experiments, don't write proofs, don't compute evaluations.

<artifact_executor_scope>
IMPORTANT: Each artifact executor has a focused prompt that guides it to do ONE thing well. It will NOT perform tasks outside its scope — assigning the wrong work to the wrong artifact type wastes an iteration. Match the task to the right executor.

EXPERIMENT executor scope:
  Output: method_out.json with results (metrics, predictions, analysis) — the core computational work
  DOES: Implement and run methods/algorithms, compute metrics, compare approaches, produce quantitative results
  DOES NOT: Collect new datasets (depends on DATASET artifacts for input data), write formal proofs
  This is the right artifact for any code that processes data and produces results
</artifact_executor_scope>

<artifact_planning_rules>
EXPERIMENT: Must depend on at least one DATASET. Define clear metrics and baselines before running. Consider trying multiple method variations rather than a single approach.
</artifact_planning_rules>

<compute_profiles>
Choose the compute profile this artifact needs for execution.
Available profiles for experiment artifacts:
  - gpu_basic: 1x NVIDIA RTX A4500, 20GB VRAM, 7 vCPUs, 29GB RAM — ML training, CUDA, large models (fallback: GPUs cheap→expensive: 2000 Ada → A4000 → 4000 Ada → L4 → 4090 → 5090)
  - cpu_plus: 4 vCPUs, 32GB RAM — large datasets, memory-intensive processing (fallback: CPUs cheap→expensive, then GPU hosts cheap→expensive (all ≥32GB RAM))

Set runpod_compute_profile to one of these exact tier names.
</compute_profiles>
GOOD PLANS: specific, actionable, consider failure scenarios, build on the suggested approach.
BAD PLANS: vague hand-waving, ignoring the suggested approach, missing critical executor details.
</instructions><user_data>
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
  "description": "Plan for an EXPERIMENT artifact.",
  "properties": {
    "domain_practice": {
      "default": "",
      "description": "How a study of exactly this kind is actually built and run in THIS field: the baselines every comparable paper reports, the datasets/corpora/cohorts/case sets that are standard (and the ones known to be saturated or unrepresentative), what is held constant, the sample sizes and repeats below which nobody believes a result, and the measures and reporting conventions a reader expects. Name what you read.",
      "title": "Domain Practice",
      "type": "string"
    },
    "practice_alignment": {
      "default": "",
      "description": "This plan checked point by point against that practice: where it meets the field's norms and where it departs from them, with why each departure is justified here and what it costs the result's credibility.",
      "title": "Practice Alignment",
      "type": "string"
    },
    "builds_on": {
      "default": "",
      "description": "What this plan REUSES from earlier rounds, named concretely: which artifacts, files, datasets, checkpoints, fitted models or negative findings, and where the executor picks each one up. If the plan starts a fresh line instead, say so here and give the reason it is allowed to \u2014 the iteration is a widen, or the prior line is a settled negative.",
      "title": "Builds On",
      "type": "string"
    },
    "title": {
      "description": "Plan title in plain, everyday language \u2014 short and jargon-free so a non-expert grasps it at a glance and it fits the run visualizations. Aim for about 4-8 words (~40 characters).",
      "title": "Title",
      "type": "string"
    },
    "summary": {
      "default": "",
      "description": "Brief summary",
      "title": "Summary",
      "type": "string"
    },
    "runpod_compute_profile": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": "cpu_basic",
      "description": "Compute tier for execution \u2014 pick from the available profiles list (e.g., 'gpu_basic', 'gpu_plus', 'cpu_plus', 'cpu_basic'). Only used in RunPod mode.",
      "title": "Runpod Compute Profile"
    },
    "implementation_pseudocode": {
      "description": "High-level pseudocode for the experiment implementation",
      "title": "Implementation Pseudocode",
      "type": "string"
    },
    "fallback_plan": {
      "description": "What to do if the primary approach fails - alternative methods, simplified versions",
      "title": "Fallback Plan",
      "type": "string"
    },
    "testing_plan": {
      "description": "How to validate the experiment works: start with small/fast tests, look for confirmation signals before running full-scale experiments",
      "title": "Testing Plan",
      "type": "string"
    }
  },
  "required": [
    "title",
    "implementation_pseudocode",
    "fallback_plan",
    "testing_plan"
  ],
  "title": "ExperimentPlan",
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
````

### [3] ASSISTANT · 2026-09-24 10:58:20 UTC

```
I'll start by reading the dependency files the plan must build on.
```

### [4] TOOL CALL — Glob · 2026-09-24 10:58:20 UTC

```
Pattern: "*"
```

### [5] TOOL CALL — Glob · 2026-09-24 10:58:20 UTC

```
Pattern: "**/*.{py,json,md,sh}"
```

### [6] TOOL RESULT — Glob · 2026-09-24 10:58:20 UTC

```
{"filenames": ["/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/vendor_copy.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/inputs.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/common.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/run_search.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/prereg.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/hf_survey.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/gloss.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/gate.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/freelab.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/sig_rename.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/assemble_labels.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/post_seal_join.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/resume_gloss.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/soundness.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/build_output.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/provisional_view.py"], "durationMs": 103, "numFiles": 16, "truncated": false, "totalMatches": 16, "countIsComplete": true}
```

### [7] TOOL RESULT — Glob · 2026-09-24 10:58:20 UTC

```
{"filenames": ["/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/.aii_claude_session.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/VENDOR_SHA256.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/vendor/__init__.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/vendor/label_sig_min.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/vendor/sig_prompt_min.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/vendor/fol_triage_min.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/vendor/perturb_min.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/vendor/repair_census_min.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/vendor/templates.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/vendor/fol.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/vendor_copy.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/work/sig_rows.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/work/free_rows.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/work/sentences.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/logs/inputs.log", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/results/shape_census.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/results/input_counts.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/work/dev_trial_D1.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/pytest.ini", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/tests/test_firewall.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/tests/conftest.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/inputs.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/common.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/work/models_snapshot.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/prompts/gloss_v1.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/prereg_freelab_v1.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/tests/test_freelab.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/run_search.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/prereg.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/prereg_freelab_v1.sha256", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/prereg_freelab.sha256", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/prereg_freelab.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/logs/stage100.out", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/temp/hf_search_24.txt", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/temp/hf_preview_12.txt", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/hf_survey.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/temp/hf_preview_12.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/.aii_cost_ledger.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/temp/web_research.txt", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/temp/datasets/full_tasksource_folio_default_validation.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/temp/datasets/full_tasksource_folio_default_train.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/temp/datasets/full_yuan-yang_MALLS-v0_default_test.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/temp/datasets/full_sxiong_entailmentbank_task1_test.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/temp/datasets/download_log.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/temp/datasets/full_tasksource_LogicNLI_default_test.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/gloss.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/logs/stage_all.out", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/gate.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/freelab.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/logs/gate.log", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/results/gate_items.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/work/probe_free_models_D9.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/sig_rename.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/work/sig_renamed_nonce.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/work/sig_renamed_syn.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/logs/sig_rename.log", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/logs/stage_all2.out", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/logs/search_free.log", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/results/map_search.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/deviations.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/assemble_labels.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/logs/assemble.log", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/post_seal_join.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/logs/search_sig_nonce.log", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/logs/sig_nonce.out", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/results/sig_replay_nonce.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/results/free_labels_v2.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/logs/post_seal_join.log", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/results/old_label_agreement.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/results/seal.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/work/audit_errcert_keys.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/work/audit_mapped_keys.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/work/audit_mapped_view.txt", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/logs/search_sig_syn.log", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/logs/sig_syn.out", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/results/sig_replay_syn.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/work/executor_audit_verdicts.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/resume_gloss.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/tests/test_gloss.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/soundness.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/logs/soundness.log", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/results/soundness_audit.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/results/sig_replay_rows.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/build_output.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/results/testability_FREE_v2.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/provisional_view.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/cost_ledger.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/temp/dataset_survey.md", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/results/gate_report.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/dataset_card.md", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/results/dataset_card.md", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/temp/candidates_data_out.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/logs/data.log", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/temp/preview_candidates_data_out.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/temp/mini_candidates_data_out.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/logs/build_output.log", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/preview_data_out.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/mini_data_out.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/full_data_out.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/README.md"], "durationMs": 144, "numFiles": 100, "truncated": true, "totalMatches": 108, "countIsComplete": true}
```

### [8] TOOL CALL — Read · 2026-09-24 10:58:24 UTC

```
/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/resume_gloss.py
```

### [9] TOOL RESULT — Read · 2026-09-24 10:58:24 UTC

```
{"type": "text", "file": {"filePath": "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/resume_gloss.py", "content": "#!/usr/bin/env python3\n\"\"\"Resume every step that needs paid LLM calls, in the pre-registered order (D9: the run's OpenRouter budget was exhausted\nbefore this artifact's first call). Run once the Test-idea budget is raised:\n\n    .venv/bin/python src/resume_gloss.py all        # gate -> FREE gloss -> final labels + seal -> join -> SIG e2e -> audit (ii) -> package\n    .venv/bin/python src/resume_gloss.py <step>     # gate | free_gloss | finalize | sig_e2e | audit_ii | package\n\nBudget: every call goes through gloss.Client (ledger cost_ledger.jsonl, artifact hard stop $6). Estimated total at the\ncatalogue prices in work/models_snapshot.json: gate ~$0.10, FREE gloss ~$0.95, SIG e2e ~$0.25, audit (ii) ~$0.45.\nIf the gate FAILS, the script stops: write prompts/gloss_v2.json (ONE revision, hashed into deviations.json), then run\n`src/gate.py run --half B --version gloss_v2` and `resume_gloss.py free_gloss --version gloss_v2` onward.\n\"\"\"\nfrom __future__ import annotations\n\nimport argparse\nimport asyncio\nimport json\nimport subprocess\nimport sys\nimport time\nfrom collections import defaultdict\n\nfrom common import RES, ROOT, WORK, dump, load_jsonl, setup_logger\nfrom run_search import class_key\n\nlogger = setup_logger(\"resume_gloss\")\nPY = sys.executable\n\n\ndef run(cmd: list[str]) -> None:\n    logger.info(\"$ \" + \" \".join(cmd))\n    subprocess.run(cmd, check=True, cwd=ROOT)\n\n\ndef gate(version: str, half: str) -> bool:\n    run([PY, \"src/gate.py\", \"run\", \"--half\", half, \"--version\", version])\n    rep = json.loads((RES / \"gate_report.json\").read_text())[f\"{version}_{half}\"]\n    return bool(rep[\"PASS\"])\n\n\ndef pair_jobs(search_rows: list[dict], sents: dict, first_keys: set | None = None) -> list[dict]:\n    by = defaultdict(set)\n    for r in search_rows:\n        if r.get(\"status\") != \"MAPPED\":\n            continue\n        for u, m in r[\"pairs_union\"]:\n            by[r[\"sentence_id\"]].add((u, m))\n    jobs = [{\"sentence_id\": sid, \"sentence\": sents[sid][\"text\"], \"pairs\": sorted(p)} for sid, p in by.items()]\n    if first_keys:  # untouched-subset sentences first\n        jobs.sort(key=lambda j: (j[\"sentence_id\"] not in first_keys, j[\"sentence_id\"]))\n    return jobs\n\n\nasync def rate(jobs: list[dict], version: str, phase: str) -> dict:\n    import gloss\n    client = gloss.Client(phase=phase)\n    try:\n        return await gloss.rate_pairs(client, jobs, version=version, logger=logger)\n    finally:\n        await client.close()\n\n\ndef free_gloss(version: str) -> None:\n    import gloss\n    sents = json.loads((WORK / \"sentences.json\").read_text())\n    search = load_jsonl(RES / \"map_search.jsonl\")\n    rows = load_jsonl(RES / \"free_labels_v2.jsonl\")\n    untouched_sids = {r[\"sentence_id\"] for r in rows if not r.get(\"seen_iter3\", False)}\n    jobs = pair_jobs(search, sents, untouched_sids)\n    n = sum(len(j[\"pairs\"]) for j in jobs)\n    est = gloss.estimate_cost(n, gloss.live_prices())\n    logger.info(f\"FREE gloss: {n} unique pairs over {len(jobs)} sentences; estimated ${est:.2f}\")\n    v = asyncio.run(rate(jobs, version, f\"free_gloss_{version}\"))\n    with (RES / \"gloss_verdicts.jsonl\").open(\"w\") as fh:\n        for j in jobs:\n            for (u, m) in j[\"pairs\"]:\n                fh.write(json.dumps({\"sentence_id\": j[\"sentence_id\"], \"use\": u, \"meaning\": m, \"version\": version,\n                                     \"haiku\": v.get((\"haiku\", j[\"sentence_id\"], u, m)),\n                                     \"qwen\": v.get((\"qwen\", j[\"sentence_id\"], u, m))}, ensure_ascii=False) + \"\\n\")\n\n\ndef verify_correct_certificates() -> dict:\n    \"\"\"Re-verify, under z3 at write time, the map certificate of every CORRECT class: re-run the deterministic search,\n    find the map with the certificate's entry set, rebuild its image and prove equivalence to the reading again.\"\"\"\n    import freelab as FL\n    sents = json.loads((WORK / \"sentences.json\").read_text())\n    rows = load_jsonl(RES / \"free_labels_v2.jsonl\")\n    done, ok, bad = set(), 0, []\n    for r in rows:\n        if r[\"label\"] not in (\"CORRECT\", \"READING_CHOICE\") or r[\"class_key\"] in done:\n            continue\n        done.add(r[\"class_key\"])\n        s = sents[r[\"sentence_id\"]]\n        cert = r[\"map_certificate\"]\n        rfol = {\"weak\": s[\"reference_fol_weak\"], \"strong\": s[\"reference_fol_strong\"], \"converse\": s.get(\"reading_converse\")}[cert[\"reading\"]]\n        cand, rd = FL.Candidate(r[\"candidate_fol\"]), FL.Reading(rfol, s[\"units\"])\n        res = FL.search(cand, rd)\n        want = sorted(cert[\"map\"])\n        hit = None\n        for m in res[\"equiv_maps\"]:\n            ents = sorted(f\"{a} => {b}\" for a, b in FL.map_to_json(m[\"assign\"], m[\"cmap\"], cand, rd).items())\n            if ents == want:\n                hit = m\n                break\n        if hit is not None and FL.z3_equiv_retry(FL.build_image(cand, rd, hit[\"assign\"], hit[\"cmap\"]), rd.e) is True:\n            ok += 1\n        else:\n            bad.append(r[\"class_key\"])\n    return {\"n_classes\": len(done), \"reverified\": ok, \"failed\": bad}\n\n\ndef finalize() -> None:\n    run([PY, \"src/assemble_labels.py\", \"--mode\", \"final\"])\n    rep = verify_correct_certificates()\n    dump(RES / \"certificate_reverification.json\", rep)\n    logger.info(f\"certificate re-verification: {rep['reverified']}/{rep['n_classes']}; failed {len(rep['failed'])}\")\n    run([PY, \"src/post_seal_join.py\"])\n\n\ndef sig_e2e(version: str) -> None:\n    import freelab as FL\n    sents = json.loads((WORK / \"sentences.json\").read_text())\n    rows = load_jsonl(RES / \"sig_replay_rows.jsonl\")\n    sel = [r for r in rows if r[\"in_e2e_gloss_subsample_300\"]]\n    search = {r[\"class_key\"]: r for r in load_jsonl(RES / \"sig_replay_syn.jsonl\")}\n    srows = [search[class_key(r[\"sentence_id\"], r[\"renamed_fol\"])] for r in sel]\n    v = asyncio.run(rate(pair_jobs(srows, sents), version, f\"sig_e2e_{version}\"))\n    conf = defaultdict(int)\n    for r, sr in zip(sel, srows):\n        if sr[\"status\"] == \"MAPPED\":\n            vd = {(u, m): (v.get((\"haiku\", r[\"sentence_id\"], u, m)), v.get((\"qwen\", r[\"sentence_id\"], u, m))) for u, m in sr[\"pairs_union\"]}\n            lab, _ = FL.gloss_decision(sr[\"equiv_maps\"], sr[\"pairs_union\"], vd)\n        else:\n            lab = sr[\"status\"]\n        r[\"e2e_gloss_label\"] = lab\n        conf[(r[\"sig_label\"], lab)] += 1\n    by = {r[\"row_key\"] + r[\"rename\"]: r for r in sel}\n    with (RES / \"sig_replay_rows.jsonl\").open(\"w\") as fh:\n        for r in rows:\n            fh.write(json.dumps(by.get(r[\"row_key\"] + r[\"rename\"], r), ensure_ascii=False) + \"\\n\")\n    err = [r for r in sel if r[\"sig_label\"] == \"ERROR\"]\n    cor = [r for r in sel if r[\"sig_label\"] == \"CORRECT\"]\n    sa = json.loads((RES / \"soundness_audit.json\").read_text())\n    sa[\"i_sig_replay\"][\"e2e_gloss_subsample_300\"] = {\n        \"n\": len(sel), \"status\": \"DONE\", \"version\": version, \"utc\": time.strftime(\"%Y-%m-%dT%H:%M:%SZ\", time.gmtime()),\n        \"confusion\": {f\"{a}->{b}\": n for (a, b), n in sorted(conf.items())},\n        \"false_CORRECT_on_known_ERROR\": round(sum(r[\"e2e_gloss_label\"] == \"CORRECT\" for r in err) / max(len(err), 1), 4),\n        \"bar\": \"<= 0.05\",\n        \"CORRECT_recall_on_known_CORRECT\": round(sum(r[\"e2e_gloss_label\"] == \"CORRECT\" for r in cor) / max(len(cor), 1), 4),\n        \"UNRESOLVED_share\": round(sum(str(r[\"e2e_gloss_label\"]).startswith(\"UNRESOLVED\") for r in sel) / max(len(sel), 1), 4)}\n    dump(RES / \"soundness_audit.json\", sa)\n\n\nAUDIT_SYS = (\"You audit first-order-logic translations of English rule sentences. Judge whether the candidate formula is \"\n             \"faithful to the sentence, given the English meaning of each concept. Different predicate names, splitting or \"\n             \"merging concepts, and logically equivalent restatements are fine if the truth conditions match the sentence \"\n             \"(either the 'X unless E' = 'if not E then X' reading or the biconditional reading of the exception is acceptable).\")\nAUDIT_USER = (\"Sentence: {text}\\n\\nConcepts used in the sentence (meaning of each, for reference):\\n{concepts}\\n\\n\"\n              \"Candidate formula: {fol}\\n\\nAnswer with JSON only: {{\\\"verdict\\\": \\\"FAITHFUL\\\" | \\\"FAITHFUL_DIFFERENT_DECOMPOSITION\\\" | \"\n              \"\\\"UNFAITHFUL\\\" | \\\"UNSURE\\\", \\\"reason\\\": \\\"<one line>\\\"}}\")\n\n\ndef audit_ii() -> None:\n    import random\n    import gloss\n    rows = load_jsonl(RES / \"free_labels_v2.jsonl\")\n    sents = json.loads((WORK / \"sentences.json\").read_text())\n    rng = random.Random(20260924)\n    pick = []\n    for lab, n in ((\"ERROR_CERT\", 60), (\"CORRECT\", 60)):\n        by = defaultdict(list)\n        for r in rows:\n            if r[\"label\"] == lab:\n                by[r[\"template_id\"]].append(r)\n        chosen = []\n        for t in sorted(by):\n            rng.shuffle(by[t])\n        i = 0\n        while len(chosen) < n and any(by.values()):\n            t = sorted(by)[i % len(by)]\n            if by[t]:\n                chosen.append(by[t].pop())\n            i += 1\n        pick += chosen\n\n    async def go():\n        client = gloss.Client(phase=\"audit_ii\", concurrency=4)\n        out = []\n        try:\n            async def one(r):\n                s = sents[r[\"sentence_id\"]]\n                concepts = \"\\n\".join(f\"- {u['gloss_pos']}\" for u in s[\"units\"].values())\n                msgs = [{\"role\": \"system\", \"content\": AUDIT_SYS},\n                        {\"role\": \"user\", \"content\": AUDIT_USER.format(text=s[\"text\"], concepts=concepts, fol=r[\"candidate_fol\"])}]\n                txt, _ = await client.chat(gloss.AUDITOR, msgs, 400, logger)\n                try:\n                    d = json.loads(txt[txt.index(\"{\"): txt.rindex(\"}\") + 1]) if txt else {}\n                except ValueError:\n                    d = {}\n                out.append({\"row_key\": r[\"row_key\"], \"label\": r[\"label\"], \"template_id\": r[\"template_id\"],\n                            \"verdict\": d.get(\"verdict\"), \"reason\": d.get(\"reason\")})\n            await asyncio.gather(*[one(r) for r in pick])\n        finally:\n            await client.close()\n        return out\n    res = asyncio.run(go())\n    sa = json.loads((RES / \"soundness_audit.json\").read_text())\n    ec = [r for r in res if r[\"label\"] == \"ERROR_CERT\" and r[\"verdict\"]]\n    co = [r for r in res if r[\"label\"] == \"CORRECT\" and r[\"verdict\"]]\n    from soundness import wilson\n    k1 = sum(r[\"verdict\"] in (\"UNFAITHFUL\", \"UNSURE\") for r in ec)\n    k2 = sum(r[\"verdict\"] in (\"FAITHFUL\", \"FAITHFUL_DIFFERENT_DECOMPOSITION\") for r in co)\n    sa[\"ii_stronger_model_audit\"] = {\"model\": gloss.AUDITOR, \"n_ERROR_CERT\": len(ec), \"n_CORRECT\": len(co),\n                                     \"ERROR_CERT_precision\": round(k1 / max(len(ec), 1), 3), \"ERROR_CERT_ci\": wilson(k1, len(ec)),\n                                     \"CORRECT_precision\": round(k2 / max(len(co), 1), 3), \"CORRECT_ci\": wilson(k2, len(co)),\n                                     \"rows\": res}\n    dump(RES / \"soundness_audit.json\", sa)\n\n\ndef main() -> None:\n    ap = argparse.ArgumentParser()\n    ap.add_argument(\"step\", choices=[\"all\", \"gate\", \"free_gloss\", \"finalize\", \"sig_e2e\", \"audit_ii\", \"package\"])\n    ap.add_argument(\"--version\", default=\"gloss_v1\")\n    a = ap.parse_args()\n    steps = [\"gate\", \"free_gloss\", \"finalize\", \"sig_e2e\", \"audit_ii\", \"package\"] if a.step == \"all\" else [a.step]\n    for st in steps:\n        logger.info(f\"=== {st} ===\")\n        if st == \"gate\":\n            if not gate(a.version, \"A\" if a.version == \"gloss_v1\" else \"B\"):\n                logger.error(\"gate FAILED: write ONE revision prompts/gloss_v2.json, log it in deviations.json, then run \"\n                             \"`src/gate.py run --half B --version gloss_v2`; if that fails too, run finalize with no \"\n                             \"verdicts (MAPPED -> UNRESOLVED_GLOSS_GATE_FAILED)\")\n                return\n        elif st == \"free_gloss\":\n            free_gloss(a.version)\n        elif st == \"finalize\":\n            finalize()\n        elif st == \"sig_e2e\":\n            sig_e2e(a.version)\n        elif st == \"audit_ii\":\n            audit_ii()\n        elif st == \"package\":\n            run([PY, \"src/build_output.py\"])\n\n\nif __name__ == \"__main__\":\n    main()\n", "numLines": 248, "startLine": 1, "totalLines": 248}}
```

### [10] TOOL CALL — Read · 2026-09-24 10:58:24 UTC

```
/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/deviations.json
```

### [11] TOOL RESULT — Read · 2026-09-24 10:58:24 UTC

```
{"type": "text", "file": {"filePath": "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/deviations.json", "content": "{\n \"deviations\": [\n  {\n   \"id\": \"D1\",\n   \"utc\": \"2026-09-24T07:16:00Z\",\n   \"when\": \"pre-freeze\",\n   \"what\": \"a 12-row FREE dev trial of the search code (seed 3) printed maps before the v1 freeze; no labels / scores / gloss\",\n   \"cost\": \"minimal: it only confirmed the reification forms the label-free census had shown\"\n  },\n  {\n   \"id\": \"D2\",\n   \"utc\": \"2026-09-24T07:21:00Z\",\n   \"when\": \"pre-freeze (in v1)\",\n   \"what\": \"B1/B2/B5 uncapped; only structural bridges (B3/B4) capped at 2, instead of the plan's 'at most 2 bridge uses'\",\n   \"cost\": \"larger family -> more spurious-equivalence chances, bounded by the gloss gate and audit (i)\"\n  },\n  {\n   \"id\": \"D3\",\n   \"utc\": \"2026-09-24T07:21:00Z\",\n   \"when\": \"pre-freeze (in v1)\",\n   \"what\": \"B2 generalised to n-ary constant absorption; gate class NO_MERGE added (7 classes)\",\n   \"cost\": \"none on labels; one more gate class (~$0.02)\"\n  },\n  {\n   \"id\": \"D5\",\n   \"utc\": \"2026-09-24T07:21:00Z\",\n   \"when\": \"pre-freeze (in v1)\",\n   \"what\": \"audit (i) uses all 2,140 on-signature SIG rows (CORRECT/ERROR/READING_CHOICE), not the plan's 1,904 scored subset\",\n   \"cost\": \"none (superset)\"\n  },\n  {\n   \"id\": \"D6\",\n   \"utc\": \"2026-09-24T07:25:46Z\",\n   \"when\": \"post-v1-freeze, before any label\",\n   \"what\": \"a map never combines a B3 merge with a B4 split (structural uses <= 2 of ONE kind)\",\n   \"why\": \"the 10-class staging run (first sentence in id order; search output only, no gloss, no label joined) showed compensating merge+split re-partitions (one symbol := A∧B while two symbols := C) that exist whenever a 1:1 map exists, inflating the gloss pair union from 20 to 68 per class (and the gloss cost ~3x) without adding any meaning-preserving form; with the amendment the unit count separates the structural levels\",\n   \"cost\": \"exactness now relative to the amended family; re-frozen as v1.1\"\n  },\n  {\n   \"id\": \"D7\",\n   \"utc\": \"2026-09-24T07:25:46Z\",\n   \"when\": \"post-v1-freeze\",\n   \"what\": \"verify.py from dataset 3 not vendored (it depends on dataset-3 common.py and is not called); vendored functions are ast-extracted, not whole files, where the source file also holds aligner / similarity helpers (repair_census, perturb, fol_triage, sig_prompt, label_sig)\",\n   \"cost\": \"none\"\n  },\n  {\n   \"id\": \"D8\",\n   \"utc\": \"2026-09-24T07:31:30Z\",\n   \"when\": \"post-v1.1-freeze, before any label (search output only)\",\n   \"what\": \"T8 reading choice resolved at the gloss level: converse-equivalent maps are stored with reading=converse; label CORRECT if some weak/strong map passes both checkers, else READING_CHOICE if some converse map does, else ERROR_GLOSS / UNRESOLVED_GLOSS\",\n   \"why\": \"name-free, the stored converse ∀x(S∧A∧P→Q) is a relabelling (Q↔P) of the weak reading ∀x(S∧A∧Q→P), so every converse-equivalent candidate also has a weak-equivalent (swapped) map; the prereg rule (e) \\\"maps equivalent only to the converse\\\" can never fire (0 of 2,163 classes); 80 T8 classes have converse maps\",\n   \"cost\": \"READING_CHOICE depends on the gloss check; search-only it is empty\"\n  },\n  {\n   \"id\": \"D9\",\n   \"utc\": \"2026-09-24T07:32:40Z\",\n   \"when\": \"STEP D (first paid call)\",\n   \"what\": \"NO LLM CALL COULD BE MADE. The first gate call returned HTTP 403 aii_run_budget_exhausted (\\\"AI Inventor per-run OpenRouter budget reached for Test idea: $7.04 of $7.00 spent by this run in that phase ... It does not reset while this run goes on\\\"); the budget had been spent by earlier steps of this run before this artifact made any call (this artifact spent $0.000). All free (:free) models returned HTTP 429 free-models-per-day (daily limit 1000, remaining 0, reset 2026-09-25T00:00Z, after this step ends). No local model is cached and the box has no GPU.\",\n   \"consequence\": \"plan fallback \\\"OpenRouter unavailable\\\" applied: map search, audit (i) search, ERROR_CERT testability and the seal of the SEARCH-ONLY labels run at $0; gate, FREE gloss check, SIG end-to-end gloss subsample and the stronger-model audit (ii) are NOT run; every MAPPED row is labelled UNRESOLVED_GLOSS_NOT_RUN; no ungated substitute checker was used. src/resume_gloss.py runs every pending step in order once the Test-idea budget is raised (estimated cost ~$1.3 total at catalogue prices).\",\n   \"substitute_audit\": \"audit (ii) replaced for now by a NON-BLIND executor audit (the agent model, Claude Opus 5.5, read 60 ERROR_CERT and 60 MAPPED rows); disclosed as weaker evidence than the planned blind Sonnet audit\"\n  }\n ]\n}", "numLines": 63, "startLine": 1, "totalLines": 63}}
```

### [12] TOOL CALL — Read · 2026-09-24 10:58:24 UTC

```
/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/gloss.py
```

### [13] TOOL RESULT — Read · 2026-09-24 10:58:24 UTC

```
{"type": "text", "file": {"filePath": "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/gloss.py", "content": "\"\"\"Gloss checker client: two family-disjoint checkers rate (symbol use, proposed meaning) pairs, <= 12 per call, one\nsentence per call, temperature 0, prompt gloss_v1 (hashed in the prereg). Every call is written to cost_ledger.jsonl\nand every verdict to results/gloss_cache.jsonl (keyed by checker|prompt_version|sentence_id|use|meaning), so re-runs\nnever re-bill. Budget guard: stops before a call when the artifact total would pass HARD_STOP_USD.\nThe checker never sees a whole candidate formula, a reading, a label, or which map was z3-equivalent.\n\"\"\"\nfrom __future__ import annotations\n\nimport asyncio\nimport json\nimport os\nimport random\nimport re\nimport time\nfrom pathlib import Path\n\nimport httpx\n\nfrom common import RES, ROOT, sha1\n\nCHECKERS = {\"haiku\": \"anthropic/claude-haiku-4.5\", \"qwen\": \"qwen/qwen3-235b-a22b-2507\"}\nAUDITOR = \"anthropic/claude-sonnet-5\"\nHARD_STOP_USD = 6.0\nLEDGER = ROOT / \"cost_ledger.jsonl\"\nCACHE = RES / \"gloss_cache.jsonl\"\n_lock = asyncio.Lock()\n\n\nclass BudgetExceeded(RuntimeError):\n    pass\n\n\nclass QuotaError(RuntimeError):\n    pass\n\n\ndef spent() -> float:\n    if not LEDGER.exists():\n        return 0.0\n    return sum(json.loads(l).get(\"usd\", 0.0) for l in LEDGER.read_text().splitlines() if l.strip())\n\n\ndef load_prompt(version: str = \"gloss_v1\") -> dict:\n    return json.loads((ROOT / \"prompts\" / f\"{version}.json\").read_text())\n\n\ndef cache_key(checker: str, version: str, sid: str, use: str, meaning: str) -> str:\n    return sha1(f\"{checker}|{version}|{sid}|{use}|{meaning}\")\n\n\ndef load_cache() -> dict:\n    out = {}\n    if CACHE.exists():\n        for l in CACHE.read_text().splitlines():\n            if l.strip():\n                r = json.loads(l)\n                out[r[\"key\"]] = r[\"verdict\"]\n    return out\n\n\nclass Client:\n    def __init__(self, phase: str, concurrency: int = 8):\n        self.phase = phase\n        self.sem = asyncio.Semaphore(concurrency)\n        self.base = os.environ[\"OPENROUTER_BASE_URL\"].rstrip(\"/\")\n        self.key = os.environ[\"OPENROUTER_API_KEY\"]\n        self.http = httpx.AsyncClient(timeout=120)\n        self.total = spent()\n        self.stop = False\n\n    async def close(self):\n        await self.http.aclose()\n\n    async def chat(self, model: str, messages: list[dict], max_tokens: int, logger=None) -> tuple[str | None, float]:\n        \"\"\"One chat completion with 3 retries (exponential backoff); no retry on 402 / quota errors.\"\"\"\n        if self.stop:\n            raise QuotaError(\"stopped\")\n        if self.total >= HARD_STOP_USD:\n            raise BudgetExceeded(f\"artifact spend {self.total:.3f} >= {HARD_STOP_USD}\")\n        body = {\"model\": model, \"messages\": messages, \"temperature\": 0, \"max_tokens\": max_tokens,\n                \"usage\": {\"include\": True}}\n        async with self.sem:\n            for attempt in range(4):\n                try:\n                    r = await self.http.post(f\"{self.base}/chat/completions\", json=body,\n                                             headers={\"Authorization\": f\"Bearer {self.key}\"})\n                except httpx.HTTPError as e:\n                    if logger:\n                        logger.warning(f\"{model} http error {type(e).__name__} attempt {attempt}\")\n                    await asyncio.sleep(2 ** attempt)\n                    continue\n                if r.status_code == 402 or (r.status_code == 403 and \"limit\" in r.text.lower()):\n                    self.stop = True\n                    raise QuotaError(f\"{r.status_code}: {r.text[:200]}\")\n                if r.status_code != 200:\n                    if logger:\n                        logger.warning(f\"{model} status {r.status_code}: {r.text[:200]} attempt {attempt}\")\n                    await asyncio.sleep(2 ** attempt)\n                    continue\n                d = r.json()\n                if \"error\" in d:\n                    if logger:\n                        logger.warning(f\"{model} error body {str(d['error'])[:200]}\")\n                    await asyncio.sleep(2 ** attempt)\n                    continue\n                usage = d.get(\"usage\") or {}\n                usd = float(usage.get(\"cost\") or 0.0)\n                async with _lock:\n                    self.total += usd\n                    with LEDGER.open(\"a\") as fh:\n                        fh.write(json.dumps({\"utc\": time.strftime(\"%Y-%m-%dT%H:%M:%SZ\", time.gmtime()), \"phase\": self.phase,\n                                             \"model\": model, \"usd\": usd, \"prompt_tokens\": usage.get(\"prompt_tokens\"),\n                                             \"completion_tokens\": usage.get(\"completion_tokens\"),\n                                             \"cum_usd\": round(self.total, 6)}) + \"\\n\")\n                txt = (d.get(\"choices\") or [{}])[0].get(\"message\", {}).get(\"content\")\n                if logger:\n                    logger.debug(f\"{model} -> {str(txt)[:300]}\")\n                return txt, usd\n        return None, 0.0\n\n\ndef parse_verdicts(txt: str | None, n: int) -> dict | None:\n    if not txt:\n        return None\n    m = re.search(r\"\\{.*\\}\", txt, re.S)\n    if not m:\n        return None\n    try:\n        d = json.loads(m.group(0))\n    except json.JSONDecodeError:\n        return None\n    out = {}\n    for i in range(1, n + 1):\n        v = str(d.get(str(i), \"\")).strip().upper()\n        if v not in (\"YES\", \"NO\"):\n            return None\n        out[i] = v\n    return out\n\n\ndef build_messages(prompt: dict, sentence: str, pairs: list[tuple[str, str]]) -> list[dict]:\n    items = \"\\n\".join(prompt[\"item_template\"].format(n=i + 1, use=u, meaning=m) for i, (u, m) in enumerate(pairs))\n    return [{\"role\": \"system\", \"content\": prompt[\"system\"]},\n            {\"role\": \"user\", \"content\": prompt[\"user_template\"].format(sentence=sentence, items=items)}]\n\n\nasync def rate_pairs(client: Client, jobs: list[dict], version: str = \"gloss_v1\", logger=None) -> dict:\n    \"\"\"jobs: [{'sentence_id', 'sentence', 'pairs': [(use, meaning), ...]}]. Returns {(checker, sid, use, meaning): verdict}\n    with verdict YES / NO / NO_VERDICT, using and extending the cache.\"\"\"\n    prompt = load_prompt(version)\n    cache = load_cache()\n    out = {}\n    calls = []\n    for j in jobs:\n        for ck in CHECKERS:\n            todo = []\n            for (u, m) in j[\"pairs\"]:\n                k = cache_key(ck, version, j[\"sentence_id\"], u, m)\n                if k in cache:\n                    out[(ck, j[\"sentence_id\"], u, m)] = cache[k]\n                else:\n                    todo.append((u, m))\n            todo = sorted(set(todo))\n            random.Random(sha1(j[\"sentence_id\"] + ck)).shuffle(todo)\n            for i in range(0, len(todo), prompt[\"max_items_per_call\"]):\n                calls.append((ck, j, todo[i:i + prompt[\"max_items_per_call\"]]))\n\n    async def one(ck, j, chunk):\n        msgs = build_messages(prompt, j[\"sentence\"], chunk)\n        v = None\n        for _ask in range(2):  # one re-ask on unparseable JSON\n            txt, _ = await client.chat(CHECKERS[ck], msgs, prompt[\"max_tokens\"], logger)\n            v = parse_verdicts(txt, len(chunk))\n            if v is not None:\n                break\n        rec = []\n        for i, (u, m) in enumerate(chunk):\n            verdict = v[i + 1] if v else \"NO_VERDICT\"\n            out[(ck, j[\"sentence_id\"], u, m)] = verdict\n            rec.append({\"key\": cache_key(ck, version, j[\"sentence_id\"], u, m), \"checker\": ck, \"version\": version,\n                        \"sentence_id\": j[\"sentence_id\"], \"use\": u, \"meaning\": m, \"verdict\": verdict})\n        async with _lock:\n            with CACHE.open(\"a\") as fh:\n                for r in rec:\n                    fh.write(json.dumps(r, ensure_ascii=False) + \"\\n\")\n\n    if logger:\n        logger.info(f\"rate_pairs: {len(calls)} calls needed ({sum(len(c[2]) for c in calls)} pair-verdicts), \"\n                    f\"artifact spend so far ${client.total:.3f}\")\n    res = await asyncio.gather(*[one(*c) for c in calls], return_exceptions=True)\n    errs = [r for r in res if isinstance(r, Exception)]\n    if errs and logger:\n        logger.error(f\"{len(errs)} calls failed; first: {type(errs[0]).__name__}: {errs[0]}\")\n    return out\n\n\ndef estimate_cost(n_pairs: int, prices: dict, per_call_in: int = 520, per_call_out: int = 75, per_call: int = 12) -> float:\n    calls = -(-n_pairs // per_call)\n    return sum(calls * (per_call_in * p[\"prompt\"] + per_call_out * p[\"completion\"]) for p in prices.values())\n\n\ndef live_prices() -> dict:\n    snap = json.loads((ROOT / \"work/models_snapshot.json\").read_text())\n    by = {m[\"id\"]: m[\"pricing\"] for m in snap}\n    return {ck: {\"prompt\": float(by[m][\"prompt\"]), \"completion\": float(by[m][\"completion\"])} for ck, m in CHECKERS.items()}\n", "numLines": 206, "startLine": 1, "totalLines": 206}}
```

### [14] TOOL CALL — Read · 2026-09-24 10:58:30 UTC

```
/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/prereg_freelab.json
```

### [15] TOOL RESULT — Read · 2026-09-24 10:58:30 UTC

```
{"type": "text", "file": {"filePath": "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/prereg_freelab.json", "content": "{\n \"id\": \"prereg_freelab_v1.1\",\n \"utc\": \"2026-09-24T07:25:46Z\",\n \"scope\": \"FREE condition of R_COMP (exp 7 rcomp/raw/generations.jsonl, last record per (sentence, slot, prompt_variant)); SIG rows (exp 7 results/sig_labels.jsonl) only for the gate and soundness audit (i)\",\n \"a_map_family\": {\n  \"units\": \"a candidate predicate is a UNIT if in every occurrence all argument positions except one subject position hold the same constants and those constants occur nowhere else in the formula (constant absorption; unary predicates are units). Template units = atom instances over the single variable x.\",\n  \"unit_map\": \"candidate unit -> exactly one template unit (plain rename; B1 reification P(x):=R(x,c); B2 de-reification P(x,k[,k2..]):=U(x) (generalised from binary to n-ary constant absorption); P(x,k):=R(x,c)); the subject argument keeps its term\",\n  \"relation_map\": \"a relevant non-unit binary candidate predicate -> a template binary predicate, either argument order; its non-absorbed relevant constants -> template constants injectively, or free (fresh)\",\n  \"injective\": \"each template unit / template predicate is the target of at most one candidate symbol (B4 excepted)\",\n  \"unmapped\": \"an unmapped candidate symbol stays a fresh uninterpreted symbol (only relevance-UNKNOWN symbols may stay unmapped; a relevant unmapped symbol makes the map non-equivalent, certificate 'coverage')\",\n  \"other_arity\": \"a relevant candidate symbol of arity 0, or arity >= 3 that is not a unit, has no target (certificate 'unmappable_symbol')\"\n },\n \"b_bridges\": {\n  \"B1\": \"reification: candidate unary P(x) := template R(x,c)\",\n  \"B2\": \"de-reification: candidate P(x,k..) with constants k only in those slots := template unary U(x)\",\n  \"B3\": \"merge: candidate unit := u1 ∧ u2 for two template units that are direct sibling conjuncts of one ∧-chain of the reading\",\n  \"B4\": \"conjunctive split: two candidate units both := one template unit; only if both occur ONLY as positive direct sibling conjuncts with the same subject term (checked syntactically on every occurrence)\",\n  \"B5\": \"lexical negation: candidate unit := ¬u; only if the first CamelCase/underscore token matches ^(not|non|no|un|in|im|il|ir|dis|never|lacks?|without)$ (case-insensitive) or the name matches ^(Un|Non|In|Im|Dis)[A-Z]\",\n  \"B6\": \"NOT declared: label-free shape census found the ∃-for-constant form in 1% of 100 sampled rows (< 5% bar); it is a known out-of-family form quantified by audit (ii)\",\n  \"cap\": \"structural bridge uses (B3 + B4) <= 2 per map; B1/B2/B5 are 1:1 unit forms and are NOT capped (deviation D2 from the plan's 'at most 2 bridge uses', decided from the label-free shape census: 37% of sampled rows have more unary predicates than the template and 37% fewer binary ones, i.e. >=3 reification uses per row are common)\"\n },\n \"c_sound_prunes\": {\n  \"relevance\": \"symbol s is inert iff F ≡ F[s := fresh] (z3: VACUOUS in fol.profile for predicates; F ≡ F[c := c'] for constants); inert symbols are recorded and dropped (kept fresh in the image)\",\n  \"coverage_count\": \"every relevant template unit must be covered by the image (a relevant template predicate absent from the image makes equivalence impossible); subtree prune when the remaining symbols cannot cover the remaining units\",\n  \"polarity\": \"z3-exact per-predicate monotonicity (UP / DOWN / NONMONO) of the candidate must equal that of the target unit (flipped under B5); for B3/B4 required only when the candidate side is UP or DOWN; UNKNOWN = no prune (and an UNKNOWN-relevance symbol may stay unmapped)\",\n  \"fingerprint\": \"evaluate image and reading on 128 finite interpretations (domain 2/3, predicate densities 50/75/90/25%, crc32-seeded, fixed); a mismatch is a certified finite countermodel\",\n  \"z3\": \"maps that agree on all 128 go to z3 equivalence, 2000 ms, one retry at 10000 ms if unknown\"\n },\n \"d_caps\": {\n  \"max_maps_per_candidate_reading\": 200000,\n  \"max_secs_per_candidate_reading\": 90.0,\n  \"cap_hit\": \"UNRESOLVED_SEARCH_CAP\",\n  \"second_pass\": \"a single second pass at 4x both caps for capped classes only\",\n  \"z3_unknown\": \"any z3 UNKNOWN on a fingerprint-passing map (or UNKNOWN relevance) with no equivalent map -> UNRESOLVED_Z3_UNKNOWN\"\n },\n \"e_label_rules\": {\n  \"unit_of_search\": \"unique (sentence_id, whitespace-normalised candidate_fol) class\",\n  \"ERROR_CERT\": \"no map equivalent to weak or strong (and on T8 none to the converse); every rejected map carries a certificate (countermodel / z3_sat / polarity / coverage / unmappable)\",\n  \"READING_CHOICE\": \"maps equivalent only to the T8 converse\",\n  \"MAPPED\": \"maps equivalent to weak or strong -> gloss rule (f); matched_reading weak / strong / both\",\n  \"NO_OUTPUT\": \"raw_output None\",\n  \"UNPARSEABLE\": \"exp 7 parse_ok False or our parser fails\",\n  \"binary\": \"ERROR = ERROR_CERT or ERROR_GLOSS; CORRECT = CORRECT; EXCLUDED otherwise\"\n },\n \"f_gloss_rule\": \"union of (symbol use, meaning) pairs over ALL z3-equivalent maps; each checker rates every pair independently; CORRECT iff some equivalent map has all pairs YES from BOTH checkers; ERROR_GLOSS iff every equivalent map contains a pair that is NO from BOTH; otherwise UNRESOLVED_GLOSS. Unparseable checker JSON: one re-ask, then NO_VERDICT (-> UNRESOLVED). Cache key (sentence_id, use, meaning).\",\n \"g_gloss_prompt\": {\n  \"version\": \"gloss_v1\",\n  \"system\": \"You are a careful lexical annotator. The task is LEXICAL: it is not a judgement of any translation or formula. Each numbered item shows one SYMBOL USE taken from a first-order logic formula (a predicate name applied to variables such as x or y and/or to constants) and a PROPOSED MEANING in English, both relative to the given sentence. You judge each item independently.\",\n  \"user_template\": \"Sentence: {sentence}\\n\\nItems:\\n{items}\\n\\nQuestion: for each item, could a careful translator plausibly have used this symbol use to express exactly this meaning in this sentence? Answer NO if the name means something different, broader or narrower in a way that changes truth conditions, opposite or negated, if the argument roles are reversed, or if the name is an arbitrary token whose meaning cannot be recognised. Otherwise answer YES.\\n\\nReturn ONLY a JSON object mapping each item number to \\\"YES\\\" or \\\"NO\\\", e.g. {{\\\"1\\\": \\\"YES\\\", \\\"2\\\": \\\"NO\\\"}}.\",\n  \"item_template\": \"{n}. SYMBOL USE: {use} || PROPOSED MEANING: {meaning}\",\n  \"temperature\": 0,\n  \"max_tokens\": 300,\n  \"max_items_per_call\": 12\n },\n \"g_gloss_prompt_sha256\": \"a2eecd6618b1b272be90a7407a85688034cb09ae53e8efbbe2aa4e5bf52d7048\",\n \"checkers\": {\n  \"A\": \"anthropic/claude-haiku-4.5\",\n  \"B\": \"qwen/qwen3-235b-a22b-2507\",\n  \"family_disjointness\": \"CSC peers are DeepSeek/Microsoft/OpenAI, the LLM evaluators under test Google/OpenAI; checkers are Anthropic and Alibaba\"\n },\n \"h_gate\": {\n  \"classes\": {\n   \"YES_IDENT\": \"template name, _k suffix stripped\",\n   \"YES_SYN\": \"WordNet mutual first-sense synonym of one name token (dataset 3 first_sense_synonyms)\",\n   \"YES_FORM\": \"reified (R+Const as unary), de-reified (Head(x, rest)), lexical-negation name for the negated gloss, or merged name for a conjunction of two sibling glosses\",\n   \"NO_NONCE\": \"nonce CVCVC name\",\n   \"NO_DONOR\": \"another lexicon entry's predicate of the same sort group whose tokens are not WordNet synonyms\",\n   \"NO_ROLE\": \"argument swap of a directional binary unit, or the positive name offered for the negated gloss\",\n   \"NO_MERGE\": \"(added, D3) one unit's name offered for the conjunction of its gloss and a sibling's gloss (the DROP-rescue case of B3)\"\n  },\n  \"n_per_class\": \">= 100 (target 120), stratified over templates and sort groups, halves A/B by sha1(sentence_id) parity\",\n  \"pass\": \"balanced accuracy >= 0.90 for Haiku, for Qwen AND for the both-YES conjunction, AND recall >= 0.85 for each of the YES and NO super-classes (conjunction), on half A\",\n  \"fail\": \"one revision gloss_v2, re-frozen with a hash, evaluated on half B only; a second failure -> no gloss step: every MAPPED row becomes UNRESOLVED_GLOSS_GATE_FAILED\"\n },\n \"i_testability\": {\n  \"rule\": \"TESTABLE iff >= 50 ERROR and >= 50 CORRECT rows spread over >= 25 sentences each (a sentence counts toward a class if it has >= 1 row of that class)\",\n  \"populations\": [\n   \"all FREE rows\",\n   \"untouched subset (not tier-A labelled in iteration 3) = PRIMARY\"\n  ],\n  \"descriptive\": \"30/30 reportability per stratum (template, clause_type, word tercile 30/35, prompt_variant)\",\n  \"mde_note\": \"AUROC SE ~0.05 and MDE ~0.10 at 50/50\"\n },\n \"j_audits\": {\n  \"i_sig_replay\": \"all SIG CORRECT/ERROR/READING_CHOICE rows with an on-signature candidate, every symbol consistently renamed (a) to nonce tokens, (b) to WordNet synonyms where one exists; map search vs references; report ERROR_CERT false-error rate on SIG-CORRECT (bar <= 0.02) and the non-identity rescue rate on SIG-ERROR; on a stratified 300 (150 CORRECT / 150 ERROR by template) of the synonym renames run the full pipeline incl. gloss: false-CORRECT on known ERROR (bar <= 0.05), CORRECT recall, UNRESOLVED share\",\n  \"ii_stronger_model\": \"anthropic/claude-sonnet-5 (newest Sonnet in the catalogue), 60 ERROR_CERT (stratified by template) + 60 CORRECT FREE rows; prompt shows sentence, candidate, English meaning of each template atom; FAITHFUL / FAITHFUL_DIFFERENT_DECOMPOSITION / UNFAITHFUL / UNSURE + reason; Wilson 95% CIs; never changes a label\",\n  \"iii_old_labels\": \"post-seal join of exp 7 tier-A FREE labels via a whitelist loader (row_key, label, label_tier, label_source); kappa + 20 hand-classified disagreements\"\n },\n \"budget\": {\n  \"plan_estimate_usd\": \"2.5-3.2\",\n  \"plan_hard_stop_usd\": 3.8,\n  \"rule\": \"if the FREE gloss sweep estimate exceeds $2.2, untouched-subset rows are processed first; the artifact hard stop is $6.0 (artifact budget $10), logged as deviation D4 if the $3.8 plan stop is passed\"\n },\n \"code_sha256\": {\n  \"src/freelab.py\": \"05a5151ee07934c60f4068288c4682d53aedad7de3bd80aeb21d276182bace7c\"\n },\n \"vendor_sha256\": {\n  \"__init__.py\": \"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855\",\n  \"fol.py\": \"e37a655f98af4899b1bdee943c66b395b27847870d6788b5509cf92ef3f95fe4\",\n  \"fol_triage_min.py\": \"b074c41135b8c1e7fe67057afab852b650b9c66426e061ce2eb93971705a212f\",\n  \"label_sig_min.py\": \"8b275ba5b710b5014e4a5a667b242cf74eb47565f29c886125179a936fae9e3e\",\n  \"perturb_min.py\": \"577e2fae8cecc0144dfc7931796ef3379ba90400db205bf9685d4d7bc39e3c4a\",\n  \"repair_census_min.py\": \"9a97cfbf0846aa395bf752cf0fca727a3229799650202e59e14e5f43e32533dc\",\n  \"sig_prompt_min.py\": \"95cbc1050e1fa48d81964adb0a4858838afc979b1744cf0c4fcb8d5c902a7cf5\",\n  \"templates.py\": \"4fe4ad153406142bd81ce4d283f80f342f3f5dd511eb1fea38380d6e469e0393\"\n },\n \"pre_freeze_disclosures\": [\n  \"D1: a 12-row FREE dev trial of the search code (random seed 3; printed maps, no labels, no scores) was run before this freeze; it confirmed the reification forms also seen in the label-free census\",\n  \"D2: B1/B2/B5 uncapped; only B3+B4 <= 2 (see b_bridges.cap)\",\n  \"D3: gate class NO_MERGE added; B2 generalised to n-ary constant absorption\",\n  \"D5: the plan's '1,904 SIG rows' is the subset with both exp-7 scores; audit (i) uses every SIG row labelled CORRECT / ERROR / READING_CHOICE (2,140) - a superset, chosen before any replay output\"\n ],\n \"supersedes\": {\n  \"file\": \"prereg_freelab_v1.json\",\n  \"sha256\": \"8ee7213d618be5be592464a9e0c83e40c5347a63ca5725283cdc4e0e70f51472\"\n },\n \"amendments\": [\n  {\n   \"id\": \"D6\",\n   \"utc\": \"2026-09-24T07:25:46Z\",\n   \"change\": \"a map never combines a B3 merge with a B4 split (structural uses <= 2 of ONE kind)\",\n   \"why\": \"the 10-class staging run (first sentence in id order; search output only, no gloss, no label joined) showed compensating merge+split re-partitions (one symbol := A∧B while two symbols := C) that exist whenever a 1:1 map exists, inflating the gloss pair union from 20 to 68 per class (and the gloss cost ~3x) without adding any meaning-preserving form; with the amendment the unit count separates the structural levels\",\n   \"effect_on_exactness\": \"ERROR_CERT is exact relative to the amended (smaller) family\"\n  }\n ]\n}", "numLines": 126, "startLine": 1, "totalLines": 126}}
```

### [16] TOOL CALL — Read · 2026-09-24 10:58:30 UTC

```
/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/gate.py
```

### [17] TOOL RESULT — Read · 2026-09-24 10:58:30 UTC

```
{"type": "text", "file": {"filePath": "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/gate.py", "content": "#!/usr/bin/env python3\n\"\"\"STEP D: gloss gate. Known-answer (symbol use, meaning) items built deterministically from the R_COMP sentences and the\ndataset-3 lexicon (7 classes, target 120 each, one item per class per sentence, stratified over templates), halves A/B\nby sha1(sentence_id) parity. Both checkers rate half A with gloss_v1; PASS rule from the prereg.\n\nusage: gate.py build | gate.py run [--half A|B] [--version gloss_v1]  -> results/gate_items.json, results/gate_report.json\n\"\"\"\nfrom __future__ import annotations\n\nimport argparse\nimport asyncio\nimport json\nimport math\nimport os\nimport random\nimport re\nfrom collections import Counter, defaultdict\n\nfrom common import LEXICON, NLTK_DATA, RES, SENTS, dump, setup_logger, sha1\n\nos.environ.setdefault(\"NLTK_DATA\", str(NLTK_DATA))\nfrom fol import parse  # noqa: E402\nfrom inputs import template_units  # noqa: E402\nfrom perturb_min import first_sense_synonyms, wn_synonyms  # noqa: E402\n\nTARGET = 120\nCLASSES = [\"YES_IDENT\", \"YES_SYN\", \"YES_FORM\", \"NO_NONCE\", \"NO_DONOR\", \"NO_ROLE\", \"NO_MERGE\"]\nSYMMETRIC = {\"friend\", \"friends\", \"sibling\", \"siblings\", \"married\", \"neighbor\", \"neighbour\", \"related\", \"near\", \"with\",\n             \"meet\", \"meets\", \"partner\", \"similar\", \"equal\", \"adjacent\", \"connected\", \"together\", \"and\"}\nCONS, VOW = \"bdfgklmptvz\", \"aeiou\"\n\n\ndef toks(n: str) -> list[str]:\n    return re.findall(r\"[A-Z]?[a-z]+|[A-Z]+(?![a-z])|\\d+\", n.replace(\"_\", \" \"))\n\n\ndef strip_k(name: str) -> str:\n    return re.sub(r\"_\\d+$\", \"\", name)\n\n\ndef disp(name: str, arity: int, subj: int, fills: dict) -> str:\n    return f\"{name}({', '.join(fills.get(j, 'x') if j != subj else 'x' for j in range(arity))})\"\n\n\ndef nonce(rng: random.Random) -> str:\n    while True:\n        w = \"\".join(rng.choice(CONS) + rng.choice(VOW) for _ in range(2)) + rng.choice(CONS)\n        w = w.capitalize()\n        if not re.match(r\"^(Un|Non|In|Im|Dis|No|Not)\", w):\n            return w\n\n\ndef units_of(sent: dict, lex: dict) -> list[dict]:\n    us = template_units(sent, lex)\n    out = []\n    for uid, u in us.items():\n        subj = u[\"args\"].index(\"x\") if \"x\" in u[\"args\"] else 0\n        fills = {j: a for j, a in enumerate(u[\"args\"]) if j != subj}\n        out.append({\"uid\": uid, **u, \"subj\": subj, \"fills\": fills})\n    return out\n\n\ndef siblings(sent: dict) -> list[tuple[str, str]]:\n    e = parse(sent[\"reference_fol_weak\"])\n    # weak reading antecedent: one flat conjunction of units\n    ante = e[2][1] if e[0] == \"all\" and e[2][0] == \"imp\" else None\n    if ante is None:\n        return []\n    acc = []\n\n    def flat(x):\n        if x[0] == \"and\":\n            flat(x[1]); flat(x[2])\n        elif x[0] == \"atom\":\n            acc.append(f\"{x[1]}({', '.join(x[2])})\")\n    flat(ante)\n    return [(a, b) for i, a in enumerate(acc) for b in acc[i + 1:]]\n\n\ndef build(logger) -> list[dict]:\n    lex = {e[\"lexicon_id\"]: e for e in json.loads(LEXICON.read_text())[\"entries\"]}\n    sents = sorted(json.loads(SENTS.read_text()), key=lambda s: sha1(s[\"sentence_id\"]))\n    by_sort = defaultdict(list)\n    su = {}\n    for s in sents:\n        su[s[\"sentence_id\"]] = units_of(s, lex)\n        for u in su[s[\"sentence_id\"]]:\n            by_sort[s[\"sort_group\"]].append((s[\"sentence_id\"], u))\n    items = []\n    counts = Counter()\n    per_template = defaultdict(Counter)\n    for s in sents:\n        sid = s[\"sentence_id\"]\n        rng = random.Random(int(sha1(\"gate|\" + sid), 16))\n        us = su[sid]\n        rng.shuffle(us)\n        half = \"A\" if int(sha1(sid), 16) % 2 == 0 else \"B\"\n        t = s[\"template_id\"]\n        uid_g = {u[\"uid\"]: u for u in us}\n\n        def add(cls, use, meaning, note=\"\"):\n            gold = \"YES\" if cls.startswith(\"YES\") else \"NO\"\n            # balance templates: at most ceil(TARGET/9)+2 per (class, template)\n            if counts[cls] >= TARGET or per_template[cls][t] >= math.ceil(TARGET / 9) + 2:\n                return False\n            counts[cls] += 1\n            per_template[cls][t] += 1\n            items.append({\"item_id\": sha1(f\"{cls}|{sid}|{use}|{meaning}\")[:16], \"class\": cls, \"gold\": gold,\n                          \"sentence_id\": sid, \"sentence\": s[\"text\"], \"template_id\": t, \"half\": half,\n                          \"candidate_atom\": use, \"proposed_meaning\": meaning, \"note\": note})\n            return True\n        # YES_IDENT\n        u = us[0]\n        add(\"YES_IDENT\", disp(strip_k(u[\"pred\"]), u[\"arity\"], u[\"subj\"], u[\"fills\"]), u[\"gloss_pos\"])\n        # YES_SYN: mutual first-sense WordNet synonym of one name token\n        for u in us:\n            tk = toks(strip_k(u[\"pred\"]))\n            done = False\n            for i, w in enumerate(tk):\n                if len(w) < 4 or not w.isalpha():\n                    continue\n                for syn in sorted(first_sense_synonyms(w.lower())):\n                    if not syn.isalpha() or len(syn) < 3 or syn == w.lower():\n                        continue\n                    nn = \"\".join(tk[:i] + [syn.capitalize()] + tk[i + 1:])\n                    done = add(\"YES_SYN\", disp(nn, u[\"arity\"], u[\"subj\"], u[\"fills\"]), u[\"gloss_pos\"], f\"{w}->{syn}\")\n                    break\n                if done:\n                    break\n            if done:\n                break\n        # YES_FORM: reify / de-reify / lexical negation / merged name (rotating by sentence hash)\n        forms = []\n        for u in us:\n            if u[\"arity\"] == 2 and u[\"fills\"]:\n                c = list(u[\"fills\"].values())[0]\n                forms.append((\"reify\", f\"{strip_k(u['pred'])}{c[0].upper() + c[1:]}(x)\", u[\"gloss_pos\"]))\n            tk = toks(strip_k(u[\"pred\"]))\n            if u[\"arity\"] == 1 and len(tk) >= 2:\n                rest = \"\".join(tk[1:])\n                forms.append((\"dereify\", f\"{tk[0]}(x, {rest[0].lower() + rest[1:]})\", u[\"gloss_pos\"]))\n            if u[\"arity\"] == 1:\n                forms.append((\"lexneg\", f\"Not{strip_k(u['pred'])}(x)\", u[\"gloss_neg\"]))\n        sib = siblings(s)\n        if sib:\n            a, b = sib[0]\n            if a in uid_g and b in uid_g and uid_g[a][\"arity\"] == 1 and uid_g[b][\"arity\"] == 1:\n                forms.append((\"merge\", f\"{strip_k(uid_g[a]['pred'])}{strip_k(uid_g[b]['pred'])}(x)\",\n                              uid_g[a][\"gloss_pos\"] + \" and \" + uid_g[b][\"gloss_pos\"]))\n        if forms:\n            f = forms[int(sha1(\"form|\" + sid), 16) % len(forms)]\n            add(\"YES_FORM\", f[1], f[2], f[0])\n        # NO_NONCE\n        u = us[1 % len(us)]\n        add(\"NO_NONCE\", disp(nonce(rng), u[\"arity\"], u[\"subj\"], u[\"fills\"]), u[\"gloss_pos\"])\n        # NO_DONOR: same-sort predicate from another sentence, no shared token / WordNet synonym\n        u = us[2 % len(us)]\n        tp = {w.lower() for w in toks(strip_k(u[\"pred\"]))}\n        syn = set().union(*[wn_synonyms(w) for w in tp]) if tp else set()\n        pool = [x for x in by_sort[s[\"sort_group\"]] if x[0] != sid and x[1][\"arity\"] == u[\"arity\"]]\n        rng.shuffle(pool)\n        own = {strip_k(x[\"pred\"]) for x in us}\n        for _, d in pool:\n            td = {w.lower() for w in toks(strip_k(d[\"pred\"]))}\n            if td & (tp | syn) or strip_k(d[\"pred\"]) in own:\n                continue\n            add(\"NO_DONOR\", disp(strip_k(d[\"pred\"]), u[\"arity\"], u[\"subj\"], u[\"fills\"] if u[\"arity\"] > 1 else {}),\n                u[\"gloss_pos\"], f\"donor={d['pred']}\")\n            break\n        # NO_ROLE: swapped directional binary unit, else positive name for the negated gloss\n        role_done = False\n        for u in us:\n            if u[\"arity\"] == 2 and u[\"fills\"] and not ({w.lower() for w in toks(u[\"pred\"])} & SYMMETRIC):\n                c = list(u[\"fills\"].values())[0]\n                role_done = add(\"NO_ROLE\", f\"{strip_k(u['pred'])}({c}, x)\", u[\"gloss_pos\"], \"swap\")\n                break\n        if not role_done:\n            u = us[3 % len(us)]\n            add(\"NO_ROLE\", disp(strip_k(u[\"pred\"]), u[\"arity\"], u[\"subj\"], u[\"fills\"]), u[\"gloss_neg\"], \"pos_for_neg\")\n        # NO_MERGE: one unit's name for the conjunction of its gloss and a sibling's\n        if sib:\n            a, b = sib[-1]\n            if a in uid_g and b in uid_g:\n                ua, ub = uid_g[a], uid_g[b]\n                add(\"NO_MERGE\", disp(strip_k(ua[\"pred\"]), ua[\"arity\"], ua[\"subj\"], ua[\"fills\"]),\n                    ua[\"gloss_pos\"] + \" and \" + ub[\"gloss_pos\"])\n    logger.info(f\"gate items: {dict(counts)}; halves {dict(Counter(i['half'] for i in items))}\")\n    dump(RES / \"gate_items.json\", items)\n    return items\n\n\ndef wilson(k: int, n: int, z: float = 1.96) -> list:\n    if n == 0:\n        return [None, None]\n    p = k / n\n    d = 1 + z * z / n\n    c = (p + z * z / (2 * n)) / d\n    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d\n    return [round(c - h, 3), round(c + h, 3)]\n\n\ndef kappa(a: list, b: list) -> float | None:\n    n = len(a)\n    if n == 0:\n        return None\n    po = sum(x == y for x, y in zip(a, b)) / n\n    ca, cb = Counter(a), Counter(b)\n    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / (n * n)\n    return round((po - pe) / (1 - pe), 3) if pe < 1 else None\n\n\ndef evaluate(items: list[dict], verdicts: dict, half: str, version: str) -> dict:\n    rows = [i for i in items if i[\"half\"] == half]\n    rep = {\"half\": half, \"version\": version, \"n_items\": len(rows), \"per_class\": {}, \"per_checker\": {}}\n    views = {\"haiku\": lambda i: verdicts.get((\"haiku\", i[\"sentence_id\"], i[\"candidate_atom\"], i[\"proposed_meaning\"])),\n             \"qwen\": lambda i: verdicts.get((\"qwen\", i[\"sentence_id\"], i[\"candidate_atom\"], i[\"proposed_meaning\"]))}\n    views[\"both_yes\"] = lambda i: (\"YES\" if views[\"haiku\"](i) == \"YES\" and views[\"qwen\"](i) == \"YES\" else \"NO\")\n    for v, f in views.items():\n        yes = [i for i in rows if i[\"gold\"] == \"YES\"]\n        no = [i for i in rows if i[\"gold\"] == \"NO\"]\n        ry = sum(f(i) == \"YES\" for i in yes) / max(len(yes), 1)\n        rn = sum(f(i) == \"NO\" for i in no) / max(len(no), 1)\n        rep[\"per_checker\"][v] = {\"recall_YES\": round(ry, 3), \"recall_NO\": round(rn, 3), \"balanced_accuracy\": round((ry + rn) / 2, 3),\n                                 \"recall_YES_ci\": wilson(sum(f(i) == \"YES\" for i in yes), len(yes)),\n                                 \"recall_NO_ci\": wilson(sum(f(i) == \"NO\" for i in no), len(no)),\n                                 \"no_verdict\": sum(f(i) not in (\"YES\", \"NO\") for i in rows)}\n        for cls in CLASSES:\n            cr = [i for i in rows if i[\"class\"] == cls]\n            k = sum(f(i) == cr[0][\"gold\"] for i in cr) if cr else 0\n            rep[\"per_class\"].setdefault(cls, {\"n\": len(cr)})[v] = {\"recall\": round(k / max(len(cr), 1), 3), \"ci\": wilson(k, len(cr))}\n    both = [(views[\"haiku\"](i), views[\"qwen\"](i)) for i in rows if views[\"haiku\"](i) in (\"YES\", \"NO\") and views[\"qwen\"](i) in (\"YES\", \"NO\")]\n    rep[\"cohen_kappa_haiku_qwen\"] = kappa([a for a, _ in both], [b for _, b in both])\n    pc = rep[\"per_checker\"]\n    rep[\"PASS\"] = bool(pc[\"haiku\"][\"balanced_accuracy\"] >= 0.90 and pc[\"qwen\"][\"balanced_accuracy\"] >= 0.90\n                       and pc[\"both_yes\"][\"balanced_accuracy\"] >= 0.90 and pc[\"both_yes\"][\"recall_YES\"] >= 0.85\n                       and pc[\"both_yes\"][\"recall_NO\"] >= 0.85)\n    return rep\n\n\nasync def run(half: str, version: str, logger) -> dict:\n    import gloss\n    items = json.loads((RES / \"gate_items.json\").read_text())\n    jobs = defaultdict(lambda: {\"pairs\": []})\n    for i in items:\n        if i[\"half\"] != half:\n            continue\n        j = jobs[i[\"sentence_id\"]]\n        j.update(sentence_id=i[\"sentence_id\"], sentence=i[\"sentence\"])\n        j[\"pairs\"].append((i[\"candidate_atom\"], i[\"proposed_meaning\"]))\n    client = gloss.Client(phase=f\"gate_{version}_{half}\")\n    try:\n        v = await gloss.rate_pairs(client, list(jobs.values()), version=version, logger=logger)\n    finally:\n        await client.close()\n    rep = evaluate(items, v, half, version)\n    rep[\"artifact_spend_usd\"] = round(gloss.spent(), 4)\n    for i in items:\n        if i[\"half\"] == half:\n            i[f\"haiku_{version}\"] = v.get((\"haiku\", i[\"sentence_id\"], i[\"candidate_atom\"], i[\"proposed_meaning\"]))\n            i[f\"qwen_{version}\"] = v.get((\"qwen\", i[\"sentence_id\"], i[\"candidate_atom\"], i[\"proposed_meaning\"]))\n    dump(RES / \"gate_items.json\", items)\n    prev = json.loads((RES / \"gate_report.json\").read_text()) if (RES / \"gate_report.json\").exists() else {}\n    prev[f\"{version}_{half}\"] = rep\n    dump(RES / \"gate_report.json\", prev)\n    logger.info(f\"gate {version} half {half}: PASS={rep['PASS']} {json.dumps(rep['per_checker'])}\")\n    return rep\n\n\nif __name__ == \"__main__\":\n    lg = setup_logger(\"gate\")\n    ap = argparse.ArgumentParser()\n    ap.add_argument(\"cmd\", choices=[\"build\", \"run\"])\n    ap.add_argument(\"--half\", default=\"A\")\n    ap.add_argument(\"--version\", default=\"gloss_v1\")\n    a = ap.parse_args()\n    if a.cmd == \"build\":\n        build(lg)\n    else:\n        asyncio.run(run(a.half, a.version, lg))\n", "numLines": 280, "startLine": 1, "totalLines": 280}}
```

### [18] TOOL CALL — Read · 2026-09-24 10:58:30 UTC

```
/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/assemble_labels.py
```

### [19] TOOL RESULT — Read · 2026-09-24 10:58:30 UTC

```
{"type": "text", "file": {"filePath": "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/assemble_labels.py", "content": "#!/usr/bin/env python3\n\"\"\"STEP G: one label per FREE generation row from the map search (+ gloss verdicts when available), testability\ndeclaration and the seal (sha256 over the sorted (row_key, label) vector). Nothing from exp 7's label / score files is\nread here (the post-seal join is src/post_seal_join.py).\n\nModes: search-only (no verdict file / gate not passed): MAPPED -> UNRESOLVED_GLOSS_NOT_RUN (or _GATE_FAILED).\n       final (results/gloss_verdicts.jsonl + a passing gate): prereg gloss rule (f) + D8.\nusage: assemble_labels.py [--mode search_only|final]\n\"\"\"\nfrom __future__ import annotations\n\nimport argparse\nimport json\nimport time\nfrom collections import Counter, defaultdict\n\nfrom common import RES, ROOT, WORK, dump, load_jsonl, setup_logger, sha256_bytes, sha256_file\nfrom run_search import class_key\n\nlogger = setup_logger(\"assemble\")\nBINARY = {\"CORRECT\": \"CORRECT\", \"ERROR_CERT\": \"ERROR\", \"ERROR_GLOSS\": \"ERROR\"}\n\n\ndef word_tercile(w: int) -> str:\n    return \"W1\" if w < 30 else (\"W2\" if w < 35 else \"W3\")\n\n\ndef load_verdicts() -> dict:\n    \"\"\"{(sentence_id, use, meaning): (haiku, qwen)} from results/gloss_verdicts.jsonl (written by resume_gloss.py).\"\"\"\n    p = RES / \"gloss_verdicts.jsonl\"\n    out = {}\n    if p.exists():\n        for r in load_jsonl(p):\n            out[(r[\"sentence_id\"], r[\"use\"], r[\"meaning\"])] = (r.get(\"haiku\"), r.get(\"qwen\"))\n    return out\n\n\ndef label_rows(mode: str) -> list[dict]:\n    import freelab as FL\n    sents = json.loads((WORK / \"sentences.json\").read_text())\n    search = {r[\"class_key\"]: r for r in load_jsonl(RES / \"map_search.jsonl\")}\n    verdicts = load_verdicts() if mode == \"final\" else {}\n    gate_ok = False\n    if mode == \"final\":\n        gr = json.loads((RES / \"gate_report.json\").read_text())\n        gate_ok = any(v.get(\"PASS\") for v in gr.values())\n    out = []\n    for r in load_jsonl(WORK / \"free_rows.jsonl\"):\n        s = sents[r[\"sentence_id\"]]\n        base = {k: r[k] for k in (\"row_key\", \"item_id\", \"sentence_id\", \"slot\", \"system\", \"family\", \"model\", \"prompt_variant\",\n                                  \"raw_output\", \"candidate_fol\")}\n        base.update(template_id=s[\"template_id\"], clause_type=s[\"clause_type\"], words=s[\"words\"],\n                    word_tercile=word_tercile(s[\"words\"]), nconds_weak=s[\"nconds_weak\"],\n                    negated_condition=s[\"negated_condition\"], nested=s[\"nested\"], text=s[\"text\"])\n        if r[\"input_status\"] != \"PARSED\":\n            out.append({**base, \"label\": r[\"input_status\"], \"search_status\": None, \"label_source\": \"input\",\n                        \"unresolved_reason\": None})\n            continue\n        ck = class_key(r[\"sentence_id\"], r[\"candidate_fol\"])\n        sr = search.get(ck)\n        if sr is None:\n            out.append({**base, \"label\": \"UNRESOLVED_SEARCH_CAP\", \"search_status\": \"MISSING\", \"label_source\": \"exhaustive_map_v1\",\n                        \"unresolved_reason\": \"class missing from map_search.jsonl\"})\n            continue\n        rec = {**base, \"class_key\": ck, \"search_status\": sr[\"status\"], \"matched_reading_search\": sr.get(\"matched_reading\"),\n               \"n_maps_enumerated\": sr.get(\"n_maps_enumerated\"), \"n_maps_fingerprint_pass\": sr.get(\"n_maps_fingerprint_pass\"),\n               \"n_equiv_maps\": sr.get(\"n_equiv_maps\"), \"n_equiv_pairsets\": sr.get(\"n_equiv_pairsets\"),\n               \"n_equiv_map_orbits\": sr.get(\"n_equiv_map_orbits\"),\n               \"nonequiv_certificate_type_counts\": sr.get(\"nonequiv_certificate_type_counts\"),\n               \"irrelevant_symbols\": sr.get(\"irrelevant_symbols\"), \"search_secs\": sr.get(\"search_secs\"),\n               \"label_source\": \"exhaustive_map_v1\"}\n        st = sr[\"status\"]\n        if st != \"MAPPED\":\n            rec.update(label=st, unresolved_reason=st if st.startswith(\"UNRESOLVED\") else None, map_certificate=None,\n                       gloss_pairs=None, gloss_decision=None)\n            out.append(rec)\n            continue\n        ents = sr[\"map_entries_union\"]\n        maps = sr[\"equiv_maps\"]\n        first = next((m for m in maps if m[\"reading\"] != \"converse\"), maps[0])\n        pairs = [{\"cand_atom\": u, \"meaning\": m,\n                  \"haiku\": verdicts.get((r[\"sentence_id\"], u, m), (None, None))[0],\n                  \"qwen\": verdicts.get((r[\"sentence_id\"], u, m), (None, None))[1]} for u, m in sr[\"pairs_union\"]]\n        if mode != \"final\":\n            rec.update(label=\"UNRESOLVED_GLOSS_NOT_RUN\", unresolved_reason=\"gloss check not run (D9: API budget exhausted)\",\n                       gloss_decision=None,\n                       map_certificate={\"status\": \"z3_equivalent_map_not_gloss_checked\", \"reading\": first[\"reading\"],\n                                        \"map\": [ents[i] for i in first[\"entry_ids\"]], \"bridges\": first[\"bridges\"]})\n        elif not gate_ok:\n            rec.update(label=\"UNRESOLVED_GLOSS_GATE_FAILED\", unresolved_reason=\"gloss gate failed twice\", gloss_decision=None,\n                       map_certificate=None)\n        else:\n            vd = {(u, m): verdicts.get((r[\"sentence_id\"], u, m), (None, None)) for u, m in sr[\"pairs_union\"]}\n            lab, idx = FL.gloss_decision(maps, sr[\"pairs_union\"], vd)\n            cert = None\n            if idx is not None:\n                m = maps[idx]\n                cert = {\"status\": \"z3_equivalent_and_gloss_accepted\", \"reading\": m[\"reading\"],\n                        \"map\": [ents[i] for i in m[\"entry_ids\"]], \"bridges\": m[\"bridges\"]}\n            rec.update(label=lab, gloss_decision=lab, map_certificate=cert,\n                       unresolved_reason=\"mixed or missing checker verdicts\" if lab == \"UNRESOLVED_GLOSS\" else None,\n                       label_source=\"exhaustive_map_v1+gloss_v1\")\n            if lab == \"CORRECT\":\n                rec[\"matched_reading\"] = maps[idx][\"reading\"]\n        rec[\"gloss_pairs\"] = pairs\n        out.append(rec)\n    for o in out:\n        o[\"label_binary\"] = BINARY.get(o[\"label\"], \"EXCLUDED\")\n    return out\n\n\ndef testability(rows: list[dict], name: str) -> dict:\n    def block(rs):\n        c = Counter(r[\"label_binary\"] for r in rs)\n        se = {k: len({r[\"sentence_id\"] for r in rs if r[\"label_binary\"] == k}) for k in (\"ERROR\", \"CORRECT\")}\n        return {\"n_ERROR\": c[\"ERROR\"], \"n_CORRECT\": c[\"CORRECT\"], \"sentences_with_ERROR\": se[\"ERROR\"],\n                \"sentences_with_CORRECT\": se[\"CORRECT\"],\n                \"TESTABLE\": bool(c[\"ERROR\"] >= 50 and c[\"CORRECT\"] >= 50 and se[\"ERROR\"] >= 25 and se[\"CORRECT\"] >= 25),\n                \"reportable_30_30\": bool(c[\"ERROR\"] >= 30 and c[\"CORRECT\"] >= 30),\n                \"label_counts\": dict(Counter(r[\"label\"] for r in rs))}\n    out = {\"population\": name, \"n_rows\": len(rows), **block(rows), \"strata\": {}}\n    for key in (\"template_id\", \"clause_type\", \"word_tercile\", \"prompt_variant\", \"slot\"):\n        g = defaultdict(list)\n        for r in rows:\n            g[r[key]].append(r)\n        out[\"strata\"][key] = {k: block(v) for k, v in sorted(g.items())}\n    n1, n0 = out[\"n_ERROR\"], out[\"n_CORRECT\"]\n    if n1 and n0:\n        import math\n        # Hanley-McNeil SE of AUROC at 0.75 as a planning figure; MDE ~ 2.8 * SE (two-sided 5%, 80% power)\n        a = 0.75\n        q1, q2 = a / (2 - a), 2 * a * a / (1 + a)\n        se = math.sqrt((a * (1 - a) + (n1 - 1) * (q1 - a * a) + (n0 - 1) * (q2 - a * a)) / (n1 * n0))\n        out[\"auroc_se_at_0.75\"] = round(se, 4)\n        out[\"auroc_mde_approx\"] = round(2.8 * se, 4)\n    return out\n\n\ndef label_vector_sha(rows: list[dict]) -> str:\n    v = sorted((r[\"row_key\"], r[\"label\"]) for r in rows)\n    return sha256_bytes(json.dumps(v, ensure_ascii=False).encode())\n\n\ndef main() -> None:\n    ap = argparse.ArgumentParser()\n    ap.add_argument(\"--mode\", choices=[\"search_only\", \"final\"], default=\"search_only\")\n    a = ap.parse_args()\n    rows = label_rows(a.mode)\n    with (RES / \"free_labels_v2.jsonl\").open(\"w\") as fh:\n        for r in rows:\n            fh.write(json.dumps(r, ensure_ascii=False) + \"\\n\")\n    logger.info(f\"labels ({a.mode}): {dict(Counter(r['label'] for r in rows))}\")\n    t = {\"mode\": a.mode, \"utc\": time.strftime(\"%Y-%m-%dT%H:%M:%SZ\", time.gmtime()),\n         \"rule\": \"TESTABLE iff >= 50 ERROR and >= 50 CORRECT rows, each class spread over >= 25 sentences\",\n         \"word_terciles\": {\"cut_1\": 30, \"cut_2\": 35}, \"all_rows\": testability(rows, \"all FREE rows\"),\n         \"untouched_subset\": \"declared after the seal by src/post_seal_join.py (needs exp-7 label tiers)\"}\n    if a.mode == \"search_only\":\n        t[\"note\"] = (\"SEARCH-ONLY labels (D9): no CORRECT class exists until the gloss step runs, so AUROC is NOT_TESTABLE; \"\n                     \"the ERROR_CERT class alone supports recall-type analyses; MAPPED rows are UNRESOLVED_GLOSS_NOT_RUN\")\n    dump(RES / \"testability_FREE_v2.json\", t)\n    seal = {\"utc\": time.strftime(\"%Y-%m-%dT%H:%M:%SZ\", time.gmtime()), \"mode\": a.mode,\n            \"label_vector_sha256_all_rows\": label_vector_sha(rows), \"n_rows\": len(rows),\n            \"label_counts\": dict(Counter(r[\"label\"] for r in rows)),\n            \"prereg_sha256\": (ROOT / \"prereg_freelab.sha256\").read_text().split()[0],\n            \"prereg_v1_sha256\": (ROOT / \"prereg_freelab_v1.sha256\").read_text().split()[0],\n            \"vendor_sha256\": json.loads((ROOT / \"VENDOR_SHA256.json\").read_text())[\"vendor\"],\n            \"code_sha256\": {p: sha256_file(ROOT / p) for p in (\"src/freelab.py\", \"src/run_search.py\", \"src/assemble_labels.py\")},\n            \"map_search_sha256\": sha256_file(RES / \"map_search.jsonl\"),\n            \"old_labels_joined\": False}\n    prev = json.loads((RES / \"seal.json\").read_text()) if (RES / \"seal.json\").exists() else {\"seals\": []}\n    prev[\"seals\"].append(seal)\n    dump(RES / \"seal.json\", prev)\n    logger.info(f\"sealed {a.mode}: {seal['label_vector_sha256_all_rows']}\")\n\n\nif __name__ == \"__main__\":\n    main()\n", "numLines": 178, "startLine": 1, "totalLines": 178}}
```

### [20] TOOL CALL — Read · 2026-09-24 10:58:36 UTC

```
/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/common.py
```

### [21] TOOL RESULT — Read · 2026-09-24 10:58:36 UTC

```
{"type": "text", "file": {"filePath": "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/common.py", "content": "\"\"\"Shared paths, hashing and JSON helpers for the FREE name-free labeller (no metric, evaluator-model or aligner code here).\"\"\"\nfrom __future__ import annotations\n\nimport hashlib\nimport json\nimport re\nimport sys\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nfor _p in (ROOT / \"vendor\", ROOT / \"src\"):\n    if str(_p) not in sys.path:\n        sys.path.insert(0, str(_p))\nsys.setrecursionlimit(10000)\n\nRUN = Path(\"/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop\")\nE7 = RUN / \"iter_3/gen_art/gen_art_experiment_7\"\nD3 = RUN / \"iter_2/gen_art/gen_art_dataset_3\"\nGEN_FREE = E7 / \"rcomp/raw/generations.jsonl\"          # FREE raw generations: no scores, no labels\nSENTS = E7 / \"rcomp/work/rcomp_sentences.json\"\nD3_FULL = D3 / \"full_data_out.json\"\nLEXICON = D3 / \"lexicon.json\"\nSIG_LABELS = E7 / \"results/sig_labels.jsonl\"            # SIG labels only (pure z3), no scores\nOLD_CANDIDATES = E7 / \"results/rcomp_candidates.jsonl\"  # opened ONLY in STEP H (post-seal) via a whitelist loader\nNLTK_DATA = E7 / \"data/nltk_data\"\nRES = ROOT / \"results\"\nWORK = ROOT / \"work\"\nLOGS = ROOT / \"logs\"\nfor _d in (RES, WORK, LOGS):\n    _d.mkdir(exist_ok=True)\n\n\ndef sha1(s: str) -> str:\n    return hashlib.sha1(s.encode()).hexdigest()\n\n\ndef sha256_bytes(b: bytes) -> str:\n    return hashlib.sha256(b).hexdigest()\n\n\ndef sha256_file(p: Path) -> str:\n    return hashlib.sha256(Path(p).read_bytes()).hexdigest()\n\n\ndef norm_text(s: str) -> str:\n    \"\"\"Dataset E's select_sentences.norm (verbatim logic) used in the item_id recipe.\"\"\"\n    s = s.lower().replace(\"’\", \"'\").replace(\"‘\", \"'\").replace(\"“\", '\"').replace(\"”\", '\"')\n    s = re.sub(r\"[^a-z0-9 ]\", \" \", s)\n    return re.sub(r\"\\s+\", \" \", s).strip()\n\n\ndef item_id(system: str, text: str, raw: str | None) -> str:\n    \"\"\"exp 7 / dataset 3 recipe: sha1(system | norm(text) | raw_output)[:16] (raw None -> '').\"\"\"\n    return sha1(system + \"|\" + norm_text(text) + \"|\" + (raw or \"\"))[:16]\n\n\ndef load_jsonl(p: Path) -> list[dict]:\n    return [json.loads(l) for l in Path(p).read_text().splitlines() if l.strip()]\n\n\ndef dump(p: Path, obj) -> None:\n    Path(p).write_text(json.dumps(obj, indent=1, ensure_ascii=False))\n\n\ndef setup_logger(name: str):\n    from loguru import logger\n    logger.remove()\n    logger.add(sys.stdout, level=\"INFO\", format=\"{time:HH:mm:ss}|{level:<7}|{message}\")\n    logger.add(LOGS / f\"{name}.log\", rotation=\"30 MB\", level=\"DEBUG\")\n    return logger\n", "numLines": 71, "startLine": 1, "totalLines": 71}}
```

### [22] TOOL CALL — Read · 2026-09-24 10:58:36 UTC

```
/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/post_seal_join.py
```

### [23] TOOL RESULT — Read · 2026-09-24 10:58:36 UTC

```
{"type": "text", "file": {"filePath": "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/post_seal_join.py", "content": "#!/usr/bin/env python3\n\"\"\"STEP H (post-seal only): join exp 7's iteration-3 FREE labels through a WHITELIST loader (row_key, label, label_tier,\nlabel_source; every other key is dropped at parse time, so no score ever enters memory), define seen_iter3, declare\ntestability on the untouched subset, and write the old-vs-new agreement table (audit iii) + 20 disagreements for hand\nclassification. Refuses to run unless results/seal.json holds a seal.\n\"\"\"\nfrom __future__ import annotations\n\nimport json\nimport random\nimport time\nfrom collections import Counter\n\nfrom assemble_labels import label_vector_sha, testability\nfrom common import OLD_CANDIDATES, RES, dump, load_jsonl, setup_logger\n\nlogger = setup_logger(\"post_seal_join\")\nWHITELIST = (\"row_key\", \"label\", \"label_tier\", \"label_source\")\n\n\ndef whitelist_hook(pairs):\n    return {k: v for k, v in pairs if k in WHITELIST}\n\n\ndef load_old() -> dict:\n    out = {}\n    with OLD_CANDIDATES.open() as fh:\n        for line in fh:\n            if not line.strip():\n                continue\n            r = json.loads(line, object_pairs_hook=whitelist_hook)\n            if \"|FREE|\" in r.get(\"row_key\", \"\"):\n                out[r[\"row_key\"]] = r\n    return out\n\n\ndef kappa(pairs) -> float | None:\n    n = len(pairs)\n    if not n:\n        return None\n    po = sum(a == b for a, b in pairs) / n\n    ca, cb = Counter(a for a, _ in pairs), Counter(b for _, b in pairs)\n    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / (n * n)\n    return round((po - pe) / (1 - pe), 3) if pe < 1 else None\n\n\ndef main() -> None:\n    seal = json.loads((RES / \"seal.json\").read_text())[\"seals\"]\n    assert seal, \"no seal: run assemble_labels.py first\"\n    last = seal[-1]\n    rows = load_jsonl(RES / \"free_labels_v2.jsonl\")\n    assert label_vector_sha(rows) == last[\"label_vector_sha256_all_rows\"], \"labels changed after the seal\"\n    old = load_old()\n    logger.info(f\"old FREE rows (whitelisted keys only): {len(old)}; tiers {dict(Counter((o.get('label'), o.get('label_tier')) for o in old.values()))}\")\n    missing = [r[\"row_key\"] for r in rows if r[\"row_key\"] not in old]\n    for r in rows:\n        o = old.get(r[\"row_key\"], {})\n        r[\"seen_iter3\"] = bool(o.get(\"label\") in (\"CORRECT\", \"ERROR\") and o.get(\"label_tier\") == \"A\")\n        r[\"old_label_iter3\"] = o.get(\"label\")\n        r[\"old_label_tier_iter3\"] = o.get(\"label_tier\")\n    with (RES / \"free_labels_v2.jsonl\").open(\"w\") as fh:\n        for r in rows:\n            fh.write(json.dumps(r, ensure_ascii=False) + \"\\n\")\n    untouched = [r for r in rows if not r[\"seen_iter3\"]]\n    t = json.loads((RES / \"testability_FREE_v2.json\").read_text())\n    t[\"untouched_subset\"] = testability(untouched, \"untouched subset (not tier-A labelled in iteration 3) - PRIMARY\")\n    t[\"seen_iter3_subset\"] = testability([r for r in rows if r[\"seen_iter3\"]], \"seen_iter3 subset\")\n    dump(RES / \"testability_FREE_v2.json\", t)\n    last2 = dict(last)\n    last2.update(utc=time.strftime(\"%Y-%m-%dT%H:%M:%SZ\", time.gmtime()), stage=\"post_seal_untouched_declaration\",\n                 label_vector_sha256_untouched=label_vector_sha(untouched), n_untouched=len(untouched),\n                 old_labels_joined=True, note=\"labels unchanged (all-row hash re-verified before the join)\")\n    seal_all = json.loads((RES / \"seal.json\").read_text())\n    seal_all[\"seals\"].append(last2)\n    dump(RES / \"seal.json\", seal_all)\n    # agreement: old tier-A binary vs new search-level view (ERROR_CERT vs MAPPED) and vs final binary\n    tab = Counter()\n    pairs = []\n    dis = []\n    for r in rows:\n        if not r[\"seen_iter3\"]:\n            continue\n        new_view = {\"ERROR_CERT\": \"ERROR\", \"UNRESOLVED_GLOSS_NOT_RUN\": \"MAPPED\", \"CORRECT\": \"CORRECT\",\n                    \"ERROR_GLOSS\": \"ERROR\"}.get(r[\"label\"], r[\"label\"])\n        tab[(r[\"old_label_iter3\"], new_view)] += 1\n        nv = \"ERROR\" if new_view == \"ERROR\" else \"CORRECT_OR_MAPPED\"\n        ov = \"ERROR\" if r[\"old_label_iter3\"] == \"ERROR\" else \"CORRECT_OR_MAPPED\"\n        pairs.append((ov, nv))\n        if ov != nv:\n            dis.append(r)\n    rng = random.Random(0)\n    sample = rng.sample(dis, min(20, len(dis)))\n    rep = {\"utc\": time.strftime(\"%Y-%m-%dT%H:%M:%SZ\", time.gmtime()),\n           \"old_rows_found\": len(old), \"new_rows\": len(rows), \"new_row_keys_missing_in_old\": len(missing),\n           \"missing_examples\": missing[:10],\n           \"seen_iter3\": sum(r[\"seen_iter3\"] for r in rows), \"untouched\": len(untouched),\n           \"old_label_counts_on_new_rows\": dict(Counter(r[\"old_label_iter3\"] for r in rows)),\n           \"agreement_table_old_tierA_vs_new\": {f\"{a}|{b}\": v for (a, b), v in sorted(tab.items())},\n           \"kappa_old_vs_new_search_view\": kappa(pairs),\n           \"note\": (\"search-only mode: the new side is ERROR (ERROR_CERT) vs MAPPED (z3-equivalent under some family map, not yet \"\n                    \"gloss-checked); MAPPED is an upper bound of CORRECT\"),\n           \"disagreement_sample_for_hand_classification\": [\n               {k: r.get(k) for k in (\"row_key\", \"sentence_id\", \"template_id\", \"text\", \"candidate_fol\", \"old_label_iter3\",\n                                      \"label\", \"search_status\", \"map_certificate\", \"nonequiv_certificate_type_counts\")}\n               for r in sample]}\n    dump(RES / \"old_label_agreement.json\", rep)\n    logger.info(f\"agreement: {rep['agreement_table_old_tierA_vs_new']} kappa={rep['kappa_old_vs_new_search_view']}; \"\n                f\"untouched {len(untouched)}; missing keys {len(missing)}\")\n\n\nif __name__ == \"__main__\":\n    main()\n", "numLines": 113, "startLine": 1, "totalLines": 113}}
```

### [24] TOOL CALL — Grep · 2026-09-24 10:58:36 UTC

```
Pattern: "def (gloss_decision|exhaustive_map_label|equivalent_modulo_vocab_exhaustive|search)\b"
```

### [25] TOOL RESULT — Grep · 2026-09-24 10:58:36 UTC

```
{"mode": "content", "numFiles": 0, "filenames": [], "content": "483:def search(cand: Candidate, rd: Reading, max_maps: int = MAX_MAPS, max_secs: float = MAX_SECS,\n484-           keep_equiv: int = 100_000) -> dict:\n485-    \"\"\"Exhaustive enumeration of the declared family for one (candidate, reading). Returns counts, certificates and\n486-    every z3-equivalent map (up to keep_equiv stored).\"\"\"\n487-    t0 = time.time()\n488-    res = {\"n_maps_enumerated\": 0, \"n_fp_pass\": 0, \"n_equiv\": 0, \"cert\": Counter(), \"equiv_maps\": [],\n489-           \"z3_unknown\": 0, \"capped\": False, \"unmappable\": [], \"images\": set()}\n490-    units, rels = cand.sy[\"units\"], cand.sy[\"rels\"]\n491-    relevant_other = [k for k in cand.sy[\"other\"] if cand.prof.get(k) not in (\"VACUOUS\",)]\n492-    if relevant_other:\n493-        res[\"unmappable\"] = relevant_other\n494-        res[\"cert\"][\"unmappable_symbol\"] += 1\n495-        return _finish(res, t0)\n496-    rel_units = [k for k in units if cand.prof.get(k) != \"VACUOUS\"]\n497-    rel_rels = [k for k in rels if cand.prof.get(k) != \"VACUOUS\"]\n498-    consts = [c for c in cand.sy[\"consts\"] if cand.const_rel.get(c) != \"INERT\"]\n499-    # split variants: none, or one/two disjoint licensed pairs\n500-    pairs = [p for p in cand.split_pairs if p[0] in rel_units and p[1] in rel_units]\n501-    split_sets = [()]\n502-    for n in range(1, MAX_STRUCT + 1):\n503-        for combo in itertools.combinations(pairs, n):\n504-            flat = [k for p in combo for k in p]\n505-            if len(flat) == len(set(flat)):\n506-                split_sets.append(combo)\n507-    need = set(rd.relevant_units)\n508-    for splits in split_sets:\n--\n765:def gloss_decision(maps: list[dict], pairs_union: list, verdict: dict) -> tuple[str, int | None]:\n766-    \"\"\"verdict[(use, meaning)] = (checker_a, checker_b), each 'YES' / 'NO' / None (no verdict).\n767-    CORRECT iff some weak/strong equivalent map has ALL its pairs YES from BOTH checkers (returns the first such index);\n768-    else READING_CHOICE iff some T8-converse map does (v1.1 amendment D8: without names the converse is a relabelling of\n769-    the weak reading, so the reading is resolved at the gloss level); ERROR_GLOSS iff EVERY equivalent map (any reading)\n770-    has at least one pair that is NO from BOTH checkers; else UNRESOLVED_GLOSS.\"\"\"\n771-    best, best_conv = None, None\n772-    all_rejected = True\n773-    for i, m in enumerate(maps):\n774-        vs = [verdict.get(tuple(pairs_union[j]), (None, None)) for j in m[\"pair_ids\"]]\n775-        if all(a == \"YES\" and b == \"YES\" for a, b in vs):\n776-            if m[\"reading\"] == \"converse\":\n777-                best_conv = i if best_conv is None else best_conv\n778-            elif best is None:\n779-                best = i\n780-        if not any(a == \"NO\" and b == \"NO\" for a, b in vs):\n781-            all_rejected = False\n782-    if best is not None:\n783-        return \"CORRECT\", best\n784-    if best_conv is not None:\n785-        return \"READING_CHOICE\", best_conv\n786-    if maps and all_rejected:\n787-        return \"ERROR_GLOSS\", None\n788-    return \"UNRESOLVED_GLOSS\", None\n789-\n790-\n791:def exhaustive_map_label(candidate_fol: str, readings: dict, atoms: dict | None = None, glosses: dict | None = None,\n792-                         checker=None) -> dict:\n793-    \"\"\"End-to-end name-free label of one candidate.\n794-\n795-    candidate_fol: candidate formula (FOLIO/MALLS unicode syntax). readings: {'weak': fol, 'strong': fol\n796-    [, 'converse': fol]} accepted readings (converse = stored but NOT accepted -> READING_CHOICE). atoms: optional\n797-    {unit_str: (arity, predicate)} for documentation only (units are derived from the readings). glosses:\n798-    {unit_str: {'gloss_pos': 'x ...', 'gloss_neg': 'x is not ...'}}. checker: callable(list[(use, meaning)]) ->\n799-    {pair: (verdict_a, verdict_b)}; if None, a MAPPED candidate gets label UNRESOLVED_GLOSS (search-only mode).\n800-\n801-    Returns {'label', 'certificate', 'reason', 'search': <label_candidate output>}.\n802-    EXACT: ERROR_CERT = no map of the declared family makes the candidate z3-equivalent to an accepted reading (every\n803-    rejected map carries a countermodel, a z3 SAT, or a sound-prune certificate). CORRECT = a z3-verified map whose\n804-    every (symbol use, meaning) pair both checkers accept. BOUNDED: family + caps (see module docstring); the gloss\n805-    check is model-relative.\"\"\"\n806-    s = label_candidate(candidate_fol, readings, glosses)\n807-    st = s[\"status\"]\n808-    if st != \"MAPPED\":\n809-        return {\"label\": st, \"certificate\": s.get(\"nonequiv_certificate_type_counts\"), \"reason\": st, \"search\": s}\n810-    if checker is None:\n811-        return {\"label\": \"UNRESOLVED_GLOSS\", \"certificate\": s[\"equiv_maps\"][0], \"reason\": \"no checker\", \"search\": s}\n812-    uniq = [tuple(p) for p in s[\"pairs_union\"]]\n813-    verdict = checker(uniq)\n814-    lab, idx = gloss_decision(s[\"equiv_maps\"], s[\"pairs_union\"], verdict)\n815-    return {\"label\": lab, \"certificate\": s[\"equiv_maps\"][idx] if idx is not None else None, \"reason\": lab, \"search\": s}\n816-\n--\n818:def equivalent_modulo_vocab_exhaustive(a_fol: str, b_fol: str, max_maps: int = MAX_MAPS, max_secs: float = MAX_SECS\n819-                                       ) -> tuple[bool | None, dict | None, int]:\n820-    \"\"\"Is there a map of the declared family (units, B1-B5, relations, constants) under which a is z3-equivalent to b,\n821-    or b to a? Symmetric (both directions are searched) and name-free (names are identifiers only; B5 uses the\n822-    negation regex). Returns (True, map, n_maps) if found; (False, None, n) if the family is exhausted with\n823-    certificates; (None, None, n) if a cap was hit or z3 returned unknown.\n824-    Note: equivalence here is 'equivalent up to a family renaming', NOT meaning-equivalence: pair it with a gloss\n825-    check before calling two formulas meaning-equivalent.\"\"\"\n826-    n = 0\n827-    unknown = False\n828-    for x, y in ((a_fol, b_fol), (b_fol, a_fol)):\n829-        cand = Candidate(x)\n830-        rd = Reading(y)\n831-        r = search(cand, rd, max_maps=max_maps, max_secs=max_secs)\n832-        n += r[\"n_maps_enumerated\"]\n833-        if r[\"n_equiv\"] > 0:\n834-            m = r[\"equiv_maps\"][0]\n835-            return True, map_to_json(m[\"assign\"], m[\"cmap\"], cand, rd), n\n836-        if r[\"capped\"] or r[\"z3_unknown\"] or any(v == \"UNKNOWN\" for v in cand.prof.values()):\n837-            unknown = True\n838-    return (None if unknown else False), None, n", "numLines": 101, "totalLines": 101}
```

### [26] TOOL CALL — Read · 2026-09-24 10:58:40 UTC

```
/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/dataset_card.md
```

### [27] TOOL RESULT — Read · 2026-09-24 10:58:40 UTC

```
{"type": "text", "file": {"filePath": "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/dataset_card.md", "content": "# Dataset card: R_COMP-FREE name-free labels (T7b)\n\nRun `run_u75jRHUss0zo`, iteration 4, `gen_art_dataset_5`. The workspace (all paths below are relative to it) is\n`/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5`.\n\n## Status: read this first\n\n- **Labels are SEARCH-ONLY, sealed at 07:37Z, 2026-09-24** (all-row sha256 `9609ebbb…3dd`; untouched-subset sha256\n  `b364a49a…500`).\n- **The pre-registered gloss step never ran (deviation D9).** Every paid call returned HTTP 403\n  `aii_run_budget_exhausted`: the run's Test-idea OpenRouter budget ($7.04 of $7.00) had been spent by earlier steps\n  before this artifact's first call, so this artifact spent **$0.000**. Free models returned the 429 daily limit, the box\n  has no GPU, and no local model is cached. No ungated substitute checker was used.\n- **Consequences for the labels:**\n  - **ERROR_CERT is final.** No map in the declared family makes the candidate z3-equivalent to an accepted reading.\n    Every rejected map carries a certificate.\n  - **MAPPED rows are `UNRESOLVED_GLOSS_NOT_RUN`.** At least one family map is z3-equivalent, but whether the mapped\n    names mean the template atoms is not yet decided.\n  - **The CORRECT class is empty, so FREE AUROC is NOT_TESTABLE until `src/resume_gloss.py all` runs** (≈$1.8 at\n    catalogue prices).\n- **Provisional view for iteration 5:** `metadata_label_binary_search_provisional` (ERROR_CERT vs MAPPED). Its\n  contamination is audited below. It is TESTABLE by the ≥50/50 rule on all rows (759 / 1,506) and on the untouched\n  subset (636 / 1,175). **Say that it is provisional wherever you use it.**\n\n## Composition (`full_data_out.json`, exp_sel_data_out)\n\n| group | rows | input | output |\n|---|---|---|---|\n| `rcomp_free_labels` | 2,652: every FREE generation record (last per sentence × slot × prompt variant), incl. 199 NO_OUTPUT and 188 UNPARSEABLE | JSON {text, candidate_fol, system, family, slot, prompt_variant, condition, template_id} | ERROR_CERT 759 · UNRESOLVED_GLOSS_NOT_RUN 1,506 · UNPARSEABLE 188 · NO_OUTPUT 199 |\n| `gloss_gate_items` | 840: 7 known-answer classes × 120 (half A 442 / half B 398, split by sha1(sentence_id)) | JSON {sentence, candidate_atom, proposed_meaning} | YES / NO |\n| `sig_soundness_replay` | 4,280: 2,140 on-signature SIG rows × {nonce, WordNet-synonym} rename | JSON {text, candidate_fol (renamed), rename, template_id} | known pure-z3 SIG label (CORRECT 1,595 / ERROR 429 / READING_CHOICE 116) |\n\n**Sources:**\n- FREE candidates: exp 7 `rcomp/raw/generations.jsonl`, raw generations with no scores. 10 slots from 9 families (meta ×2,\n  qwen, mistral, deepseek, google ×2, microsoft, openai, cohere), 221 templated sentences (9 templates), few-shot and\n  zero-shot prompt variants.\n- References: exp 7 `rcomp/work/rcomp_sentences.json` (weak / strong readings; for T8 also the not-accepted converse),\n  true by construction.\n- Glosses: dataset 3 `lexicon.json`.\n\n**Row keys:** exp 7's recipe `sha1(system|norm(text)|raw_output)[:16]|FREE|slot|prompt_variant`. All 2,652 keys exist\nin exp 7's `rcomp_candidates.jsonl`.\n\n## Label semantics: what each label is exact relative to\n\n- **Map family** (prereg v1.1, `prereg_freelab.json`, sha256 `b081c399…`):\n  - candidate *units* (unary predicates, or predicates whose other argument slots always hold the same private\n    constants) map injectively onto template atoms over x;\n  - bridges: B1 reification, B2 de-reification (n-ary), B5 lexical negation (name-regex licensed), B3 merge and B4 split\n    (≤2 per map, never mixed);\n  - genuinely binary predicates map onto template binary predicates, in either argument order;\n  - constants map injectively or stay free.\n- **Search is exhaustive over the family under sound prunes:**\n  - z3 relevance (inert symbols dropped);\n  - z3 monotonicity polarity;\n  - coverage/count;\n  - a 128-interpretation finite-model fingerprint, whose mismatches are certified countermodels;\n  - z3 equivalence (2 s, retry 10 s) for the maps that survive.\n- **Search results (2,163 unique classes):**\n  - 156,066 maps enumerated;\n  - 102,300 passed the fingerprint and went to z3;\n  - 0 cap hits, 0 z3 UNKNOWN;\n  - median 0.25 s per class, max 14 s.\n- **ERROR_CERT is exact relative to that family and those caps.** It is NOT a meaning judgement about forms outside the\n  family (below).\n- **MAPPED:** at least one family map is z3-equivalent to the weak or strong reading. It says nothing yet about whether\n  the names mean the template atoms. In 72% of MAPPED classes the maps need B1/B2 reification, and only 23% have a\n  bridge-free map: free vocabulary diverges heavily from the template names.\n- **T8 converse (D8).** Without names, the converse `∀x(S∧A∧P→Q)` is a Q↔P relabelling of the weak reading, so reading\n  choice can only be settled by glosses. 80 classes carry converse maps.\n\n## Validation\n\n### (i) SIG replay: exact, known labels, $0 (`results/soundness_audit.json`)\n\nEvery symbol of the 2,140 SIG rows was renamed and the rows re-searched without names.\n\n| | nonce rename | synonym rename |\n|---|---|---|\n| ERROR_CERT on known-CORRECT rows (false-error rate; bar ≤ 0.02) | **0 / 1,595** (CI [0, 0.002]) | 0 / 1,595 |\n| identity (un-renaming) map recovered on CORRECT rows | 100% | 100% |\n| known-ERROR rows with a non-identity equivalent map (\"rescue\"; the gloss check must stop these) | 9.1% [6.7, 12.2] | 10.5% [7.9, 13.7] |\n| READING_CHOICE rows mapped (to be resolved by glosses) | 100% | 100% |\n| **oracle-checker ceiling** (a checker that says YES exactly on identity pairs) | CORRECT recall 1.00, false CORRECT 0.00 | same |\n\n- Rescue rates by template: highest on T9 (0.37–0.43), T8 (0.27) and T3 (0.20); ≤0.13 elsewhere.\n- The synonym rename only changed 13% of symbols. WordNet mutual first-sense synonyms are sparse; because the search is\n  name-free, it matters only for B5 licences.\n- The end-to-end gloss run on the pre-registered 300-row synonym subsample is **PENDING**.\n\n### (ii) Executor audit: substitute for the blind Sonnet audit (D9)\n\n- **Who:** the agent model (Claude Opus 5.5), reading sentence + candidate + references.\n- **Blindness:** NON-blind, since the auditor knew which class it was sampling. It is weaker evidence than the planned\n  blind audit.\n- **Sample:** 60 rows per class, stratified by template.\n\n| class | result |\n|---|---|\n| ERROR_CERT | 51 UNFAITHFUL, 1 UNSURE, **8 FAITHFUL_DIFFERENT_DECOMPOSITION** → implied precision **0.867 [0.758, 0.931]**, below the 0.90 flag |\n| MAPPED | **52 / 60 faithful = 0.867 [0.758, 0.931]** |\n\nThe 8 unfaithful MAPPED rows are exactly the kind the gloss check is designed to reject:\n- B3 merge rescue of a dropped sortal ×3;\n- T8 converse ×2;\n- B5/permutation rescue of a polarity error ×2;\n- one lexical mismatch (\"ProvidesFood\" for \"is food\").\n\n**Out-of-family faithful forms that ERROR_CERT contains** (known failure modes, ≈13% of ERROR_CERT):\n- disjunctive split of an \"A or B\" concept, or one predicate reused with two constants (`Has(x,hair) ∨ Has(x,fur)`,\n  `DesignedFor(x,a) ∧ DesignedFor(x,b)`): 4/60. Mapping two instances of one predicate to two template atoms is not a\n  predicate substitution without unique names, so it is outside the family by design;\n- relational / ∃-for-constant decompositions (`∃y(JobAt(x,y) ∧ School(y))`, `∃y Boss(y,x) ∧ Criticizes(y,x)`): 3/60.\n  B6 was not declared because the label-free census found 1% (<5% bar);\n- negation inside a name that is not at the first token (`DoesNotSupportWeightOfBridge`): 1/60.\n\n**Iteration 5 should report FREE results with and without these form classes (sensitivity).**\n\n### (iii) Old labels (post-seal join, whitelist loader)\n\n- **All 34 old tier-A CORRECT rows are MAPPED.**\n- **Of the 420 old tier-A ERROR rows, 123 are ERROR_CERT and 297 are MAPPED** (κ = 0.06 on ERROR vs CORRECT-or-MAPPED).\n- **Hand classification of 20 random disagreements:**\n  - 17 are **old false errors**: faithful candidates that the name-similarity aligner could not align (Q∨E forms,\n    reifications, ternary de-reification);\n  - 2 are T8 converse (old ERROR correct);\n  - 1 is a B3 merge rescue of a dropped sortal (old ERROR correct; the gloss check must reject it).\n- The iteration-3 FREE tier-A ERROR class is therefore substantially contaminated. This is independent evidence against\n  the aligner-based labeller.\n\n## Populations and testability (`results/testability_FREE_v2.json`)\n\n- `seen_iter3` = tier-A labelled in iteration 3 (454 rows). The **untouched subset (2,198 rows) is primary**.\n- \"Untouched\" means untouched with respect to label-dependent decisions. Consensus and judge scores exist for every row\n  from iteration 3, but none was compared with labels outside tier A.\n- Testability rule: ≥50 ERROR and ≥50 CORRECT, each spread over ≥25 sentences.\n  - Search-only labels: NOT_TESTABLE (0 CORRECT).\n  - Provisional ERROR_CERT vs MAPPED view: TESTABLE on both populations (per-stratum counts in the file; the\n    AUROC-MDE planning figure is also there).\n\n## Known limitations\n\n- **Semi-synthetic sentences.** 9 templates, one exception clause each; the references are template-built.\n- **Readings accepted.** Weak and strong are both accepted; the T8 converse is not.\n- **The gloss check is model-relative.** Only the SIG replay numbers are exact.\n- **B5 regex fires on `In…`-prefixed names.** The token `in` is licensed, so `In(x, crotonRiverWatershed)` may map to\n  `¬In(…)`. This is always gloss-guarded, and it explains part of the synonym-vs-nonce rescue gap.\n- **Free variables are read as constants.** A candidate with no quantifier (`Chef(x) ∧ … → …`) is read by the shared\n  parser with `x` as a constant, i.e. as a ground claim, so it is ERROR_CERT. Operator precedence follows the shared\n  FOLIO/MALLS parser (↔ lowest).\n- **Lexicon glosses are not re-audited here** (deviation D1 of exp 7).\n\n## Licences and intended use\n\n- **Licences:** templates are built from FOLIO/MALLS/E-derived lexicon atoms (FOLIO CC-BY-SA-style; MALLS-v0 is\n  CC-BY-NC-4.0). Candidate generations were produced by this run through OpenRouter.\n- **Intended use:** iteration-5 confirmation only, scoring frozen metrics ONCE on the untouched subset. Not a training set.\n\n## Reproduce / resume\n\nSee `README.md`. The search-only pipeline is deterministic and costs $0. The paid gloss steps resume with\n`src/resume_gloss.py all`.\n", "numLines": 163, "startLine": 1, "totalLines": 163}}
```

### [28] TOOL CALL — Glob · 2026-09-24 10:58:40 UTC

```
Pattern: "{results/*,src/*,*.json,*.md}"
```

### [29] TOOL RESULT — Glob · 2026-09-24 10:58:42 UTC

```
{"filenames": ["/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/artifact_budget.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/sig_prompt.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/gen_sig.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/label_sig.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/prereg_sig.sha256", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/prereg_sig.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/sig_pilot_projection.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/scores_SIG_stage_mini.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/judge_regression_T4.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/testability.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/sig_classes.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/sig_labels.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/testability_SIG.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/prices.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/disguise_map_SIG.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/scores_SIG.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/scores_SIG_stage_all.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/sig_repairs.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/judge_SIG.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/frontier_subsample.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/auc_tools.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/judge_frontier_SIG.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/run_judges.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/disguise_map_FREE.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/scores_FREE_stage_mini.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/judge_rows_SIG.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/scores_FREE.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/scores_FREE_stage_all.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/.aii_claude_session.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/llm_cache.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/costs.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/judge_FREE.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/budget_state.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/key_poll.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/panel_rcomp.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/free_labels.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/score_consensus.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/consensus_rcomp.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/scores_rename_SIG.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/write_records.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/judge_local_SIG.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/analyse.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/local_judge_rcomp.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/judge_local_FREE.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/local_cache.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/testability_FREE.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/testability.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/analysis_rows_SIG.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/tables.md", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/analysis.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/rcomp_candidates.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/audit_rederive.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/VENDOR_SHA256.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/deviations.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/method_out.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/preview_method_out.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/mini_method_out.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/full_method_out.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/rederive_raw.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/reproducibility.md", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/.terminal_claude_agent_struct_out.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/README.md", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/.aii_worker_result.json"], "durationMs": 513, "numFiles": 63, "truncated": false, "totalMatches": 63, "countIsComplete": true}
```

### [30] TOOL CALL — Grep · 2026-09-24 10:58:48 UTC

```
Pattern: "\|FREE\|"
```

### [31] TOOL RESULT — Grep · 2026-09-24 10:58:48 UTC

```
{"mode": "content", "numFiles": 0, "filenames": [], "content": "2211:[Omitted long matching line]", "numLines": 1, "totalLines": 2652, "appliedLimit": 1}
```

### [32] TOOL CALL — Grep · 2026-09-24 10:58:48 UTC

```
Pattern: "."
```

### [33] TOOL RESULT — Grep · 2026-09-24 10:58:48 UTC

```
{"mode": "content", "numFiles": 0, "filenames": [], "content": "1:{\"row_key\": \"00ef58b6b930b1d1|FREE|G7|fewshot_v1\", \"cond\": \"disg\", \"judge\": \"cheap\", \"model\": \"google/gemini-2.5-flash-lite\", \"p\": 0.95, \"verdict\": \"FAITHFUL\", \"type\": \"NONE\", \"reason\": \"The formula accurately captures the conditional and exception structure of the sentence.\", \"fail\": null, \"cost\": 0.0, \"seconds\": 1.8040263652801514}\n2:{\"row_key\": \"6453f87cb72764a1|FREE|G9|fewshot_v1\", \"cond\": \"disg\", \"judge\": \"cheap\", \"model\": \"google/gemini-2.5-flash-lite\", \"p\": 0.0, \"verdict\": \"UNFAITHFUL\", \"type\": \"CONN\", \"reason\": \"The formula uses 'AND' and 'OR' (implied by XOR) where the sentence uses 'unless' and 'and'.\", \"fail\": null, \"cost\": 5.66e-05, \"seconds\": 0.9160463809967041}", "numLines": 2, "totalLines": 1227, "appliedLimit": 2}
```

### [34] TOOL CALL — Grep · 2026-09-24 10:58:48 UTC

```
Pattern: "."
```

### [35] TOOL RESULT — Grep · 2026-09-24 10:58:48 UTC

```
{"mode": "content", "numFiles": 0, "filenames": [], "content": "1:[Omitted long matching line]", "numLines": 1, "totalLines": 24, "appliedLimit": 1}
```

### [36] ASSISTANT · 2026-09-24 10:58:54 UTC

```
Still reading dependency files. Next I need the exact score field names in the earlier experiment's FREE outputs.
```

### [37] TOOL CALL — Grep · 2026-09-24 10:58:54 UTC

```
Pattern: ""(c_[a-z_]+|p_[a-z_]+|judge[a-z_]*|pred[a-z_]*|label[a-z_]*|template_id|slot|condition|sentence_id)":"
```

### [38] TOOL RESULT — Grep · 2026-09-24 10:58:54 UTC

```
{"mode": "content", "numFiles": 0, "filenames": [], "content": "1:\"sentence_id\":\n1:\"c_score_align\":\n1:\"c_score_hyb\":\n1:\"c_score_align\":\n1:\"c_score_hyb\":\n1:\"c_score_align\":\n1:\"c_score_hyb\":\n1:\"c_score_align\":\n1:\"c_score_hyb\":\n1:\"c_score_align\":\n1:\"c_score_hyb\":\n1:\"c_score_align\":\n1:\"c_score_hyb\":\n1:\"c_score_align\":\n1:\"c_score_hyb\":\n1:\"c_score_align\":\n1:\"c_score_hyb\":\n1:\"c_score_align\":\n1:\"c_score_hyb\":\n1:\"c_score_align\":\n1:\"c_score_hyb\":\n1:\"c_score_align\":\n1:\"c_score_hyb\":\n2:\"sentence_id\":\n2:\"c_score_align\":\n2:\"c_score_hyb\":\n2:\"c_score_align\":\n2:\"c_score_hyb\":\n2:\"c_score_align\":\n2:\"c_score_hyb\":\n2:\"c_score_align\":\n2:\"c_score_hyb\":\n2:\"c_score_align\":\n2:\"c_score_hyb\":\n2:\"c_score_align\":\n2:\"c_score_hyb\":\n2:\"c_score_align\":\n2:\"c_score_hyb\":\n2:\"c_score_align\":\n2:\"c_score_hyb\":", "numLines": 40, "totalLines": 4740, "appliedLimit": 40}
```

### [39] TOOL CALL — Grep · 2026-09-24 10:58:54 UTC

```
Pattern: "FREE"
```

### [40] TOOL RESULT — Grep · 2026-09-24 10:58:54 UTC

```
{"mode": "content", "numFiles": 0, "filenames": [], "content": "241:## FREE (sign readout; tier-B labels provisional if the panel check BA < 0.80)\n252:### SIG vs FREE (vocabulary-divergence cost of consensus)\n254:| metric | SIG AUROC | FREE tier-A AUROC | SIG d | FREE tier-A d |", "numLines": 3, "totalLines": 3}
```

### [41] TOOL CALL — Grep · 2026-09-24 10:59:00 UTC

```
Pattern: ""[A-Za-z_0-9]+":"
```

### [42] TOOL CALL — Read · 2026-09-24 10:59:00 UTC

```
/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/tables.md
```

### [43] TOOL RESULT — Grep · 2026-09-24 10:59:00 UTC

```
{"mode": "content", "numFiles": 0, "filenames": [], "content": "1:\"row_key\":\n1:\"item_id\":\n1:\"sentence_id\":\n1:\"condition\":\n1:\"template_id\":\n1:\"slot\":\n1:\"system\":\n1:\"family\":\n1:\"prompt_variant\":\n1:\"candidate_fol\":\n1:\"parse_ok\":\n1:\"label\":\n1:\"label_source\":\n1:\"label_tier\":\n1:\"matched_reading\":\n1:\"off_signature\":\n1:\"sig_status\":\n1:\"repair_ops\":\n1:\"repair_status\":\n1:\"strata\":\n1:\"words\":\n1:\"word_tercile\":\n1:\"nconds_weak\":\n1:\"nconds_bin\":\n1:\"depth_weak\":\n1:\"nquant\":\n1:\"nested\":\n1:\"negated_condition\":\n1:\"clause_type\":\n1:\"template_id\":\n1:\"sig_class_id\":\n1:\"sig_class_id_size\":\n1:\"sig_class_id_n_peers\":\n1:\"sig_class_id_n_peers_same_class\":\n1:\"sig_class_id_peer_majority_class\":\n1:\"sig_class_id_is_peer_majority\":\n1:\"free_solver_class_id\":\n1:\"free_align_class_id\":\n1:\"free_hyb_class_id\":\n1:\"free_align_class_id_size\":\n1:\"free_align_class_id_is_peer_majority\":\n1:\"free_hyb_class_id_size\":\n1:\"free_hyb_class_id_is_peer_majority\":\n1:\"n_peers_sig\":\n1:\"n_peers_equal_sig\":\n1:\"n_unknown_sig\":\n1:\"n_peers_hyb\":\n1:\"correct_not_equivalent\":\n1:\"ref_flagged\":\n1:\"tier_B_provisional\":\n1:\"panel_votes\":\n1:\"cost_usd\":\n1:\"secs_sig\":\n1:\"coverage_status\":\n1:\"c_score_sig\":\n1:\"c_score_align\":\n1:\"c_score_nf\":\n1:\"c_score_hyb\":\n1:\"g_align\":\n1:\"g_nf\":\n1:\"judge_cheap_disg\":\n1:\"judge_cheap_orig\":\n1:\"judge_frontier_orig\":\n1:\"judge_frontier_disg\":\n1:\"judge_local_disg\":\n1:\"judge_local_orig\":\n2:\"row_key\":\n2:\"item_id\":\n2:\"sentence_id\":\n2:\"condition\":\n2:\"template_id\":\n2:\"slot\":\n2:\"system\":\n2:\"family\":\n2:\"prompt_variant\":\n2:\"candidate_fol\":\n2:\"parse_ok\":\n2:\"label\":\n2:\"label_source\":\n2:\"label_tier\":", "numLines": 80, "totalLines": 205590, "appliedLimit": 80}
```

### [44] TOOL RESULT — Read · 2026-09-24 10:59:00 UTC

````
{"type": "text", "file": {"filePath": "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/tables.md", "content": "  \"strong\": 0.7135779999999998\n },\n \"artifact_ledger_usd_total\": 1.5809425042500005\n}\n```\n\n## FREE (sign readout; tier-B labels provisional if the panel check BA < 0.80)\n\nverdict NOT_TESTABLE; label tiers {'UNRESOLVED:none': 1811, 'ERROR:A': 420, 'UNPARSEABLE:-': 188, 'CORRECT:A': 34, 'NO_OUTPUT:-': 199}\n\n| view | n (ERR/COR) | c_align - bar [CI] | c_hyb - bar [CI] | c_nf - bar [CI] | AUROC bar (template) |\n|---|---|---|---|---|---|\n| tier_AB | 454 (420/34) | 0.214 [-0.034, 0.377] | 0.191 [-0.043, 0.348] | 0.230 [-0.050, 0.431] | 0.581 |\n| tier_A | 454 (420/34) | 0.214 [-0.034, 0.377] | 0.191 [-0.043, 0.348] | 0.230 [-0.050, 0.431] | 0.581 |\n| tier_B_only_errors_or_corrects | 0 (0/0) | untestable | untestable | untestable | - |\n| few_shot_AB | 387 (358/29) | 0.157 [-0.085, 0.305] | 0.128 [-0.105, 0.271] | 0.186 [-0.091, 0.377] | 0.618 |\n\n### SIG vs FREE (vocabulary-divergence cost of consensus)\n\n| metric | SIG AUROC | FREE tier-A AUROC | SIG d | FREE tier-A d |\n|---|---|---|---|---|\n| c_score_align | 0.952 | 0.804 | 0.260 | 0.324 |\n| c_score_hyb | 0.950 | 0.783 | 0.260 | 0.324 |\n| c_score_nf | 0.950 | 0.798 | 0.263 | 0.529 |\n| judge_cheap_disg | 0.587 | 0.581 | - | - |\n| judge_cheap_orig | 0.673 | 0.372 | - | - |\n\nPanel known-label check: {\"n_items\": null, \"n_answered\": null, \"balanced_accuracy\": null, \"recall_error\": null, \"recall_correct\": null, \"tier_B_provisional\": null, \"not_run\": true}\n", "numLines": 29, "startLine": 235, "totalLines": 263}}
````

### [45] TOOL CALL — Grep · 2026-09-24 10:59:06 UTC

```
Pattern: "."
```

### [46] TOOL RESULT — Grep · 2026-09-24 10:59:06 UTC

```
{"mode": "content", "numFiles": 0, "filenames": [], "content": "1:[Omitted long matching line]\n2:[Omitted long matching line]", "numLines": 2, "totalLines": 98, "appliedLimit": 2}
```

### [47] TOOL CALL — Grep · 2026-09-24 10:59:06 UTC

```
Pattern: "RCOMP|R_COMP|FREE|CORRECT"
```

### [48] TOOL RESULT — Grep · 2026-09-24 10:59:06 UTC

```
{"mode": "content", "numFiles": 0, "filenames": [], "content": "1137:  \"score_correlation_FREE_tierA\": 0.07445407611393627,\n1138:  \"n_FREE_tierA\": 417,\n1141:   \"c_align_FREE_tierA\": 0.8,\n1144:  \"observed_FREE_tierA\": {\n1300:  \"caveat\": \"order-of-magnitude guide only: analytic Hanley-McNeil + SIG-row resampling as an upper-variance proxy; no FREE-labelled data at these counts exist\"", "numLines": 5, "totalLines": 5}
```

### [49] TOOL CALL — Grep · 2026-09-24 10:59:24 UTC

```
Pattern: ""[A-Za-z_0-9]+":"
```

### [50] TOOL RESULT — Grep · 2026-09-24 10:59:24 UTC

```
{"mode": "content", "numFiles": 0, "filenames": [], "content": "1:\"sentence_id\":\n1:\"source_stratum\":\n1:\"words\":\n1:\"n_conditions\":\n1:\"nodes\":\n1:\"node_id\":\n1:\"canon_fol\":\n1:\"rows\":\n1:\"row_key\":\n1:\"slot\":\n1:\"family\":\n1:\"family_field\":\n1:\"system_class\":\n1:\"is_peer\":\n1:\"node_id\":\n1:\"canon_fol\":\n1:\"rows\":\n1:\"row_key\":\n1:\"slot\":\n1:\"family\":\n1:\"family_field\":\n1:\"system_class\":\n1:\"is_peer\":\n1:\"node_id\":\n1:\"canon_fol\":\n1:\"rows\":\n1:\"row_key\":\n1:\"slot\":\n1:\"family\":\n1:\"family_field\":", "numLines": 30, "totalLines": 43534, "appliedLimit": 30}
```

### [51] TOOL CALL — Read · 2026-09-24 10:59:24 UTC

```
/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/power_E2.json
```

### [52] TOOL RESULT — Read · 2026-09-24 10:59:24 UTC

```
{"type": "text", "file": {"filePath": "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/power_E2.json", "content": "    \"planned_for_mde_0.10\": null\n   }\n  }\n },\n \"criterion_c_effects\": {\n  \"conservative\": {\n   \"value\": 0.069,\n   \"what\": \"observed E L25 pooled Delta c_score_align - flash-lite disguised (exp 6 tables_T1.md)\"\n  },\n  \"optimistic\": {\n   \"value\": 0.05788390284067524,\n   \"value_3pool\": 0.03988884314532737,\n   \"n\": 869,\n   \"what\": \"Part-1 graded c_vres (label-free liberal-vocabulary counterfactual) - flash-lite disguised on E L25 consensus-scorable rows\"\n  }\n },\n \"rcomp_free\": {\n  \"score_correlation_FREE_tierA\": 0.07445407611393627,\n  \"n_FREE_tierA\": 417,\n  \"icc_SIG_residual\": 0.4981780519323534,\n  \"auroc_assumed\": {\n   \"c_align_FREE_tierA\": 0.8,\n   \"judge\": 0.58\n  },\n  \"observed_FREE_tierA\": {\n   \"auroc_c_align\": 0.7732988802756244,\n   \"auroc_judge_cheap_disg\": 0.5639965546942292\n  },\n  \"scenarios\": [\n   {\n    \"n_err\": 420,\n    \"n_cor\": 34,\n    \"n_sent\": 221,\n    \"rows_per_sentence\": 2.0542986425339365,\n    \"design_effect\": 1.5252284438924812,\n    \"mde80_analytic\": 0.19179987691579534,\n    \"mde80_empirical_SIG\": 0.16179198302742362,\n    \"sig_delta_mean\": 0.3904300887021475\n   },\n   {\n    \"n_err\": 420,\n    \"n_cor\": 100,\n    \"n_sent\": 221,\n    \"rows_per_sentence\": 2.3529411764705883,\n    \"design_effect\": 1.6740055996731842,\n    \"mde80_analytic\": 0.12956165056775884,\n    \"mde80_empirical_SIG\": 0.1122005289432693,\n    \"sig_delta_mean\": 0.39351523809523814\n   },\n   {\n    \"n_err\": 420,\n    \"n_cor\": 200,\n    \"n_sent\": 221,\n    \"rows_per_sentence\": 2.8054298642533935,\n    \"design_effect\": 1.8994255326742489,\n    \"mde80_analytic\": 0.11025422990170483,\n    \"mde80_empirical_SIG\": 0.09274157079224399,\n    \"sig_delta_mean\": 0.39361950396825396\n   },\n   {\n    \"n_err\": 420,\n    \"n_cor\": 400,\n    \"n_sent\": 221,\n    \"rows_per_sentence\": 3.7104072398190047,\n    \"design_effect\": 2.350265398676379,\n    \"mde80_analytic\": 0.10383428515140421,\n    \"mde80_empirical_SIG\": 0.08527635823517321,\n    \"sig_delta_mean\": 0.3897691071428572\n   },\n   {\n    \"n_err\": 420,\n    \"n_cor\": 800,\n    \"n_sent\": 221,\n    \"rows_per_sentence\": 5.520361990950226,\n    \"design_effect\": 3.2519451306806384,\n    \"mde80_analytic\": 0.10942535872325079,\n    \"mde80_empirical_SIG\": 0.07600239210990603,\n    \"sig_delta_mean\": 0.3874858085317461\n   },\n   {\n    \"n_err\": 600,\n    \"n_cor\": 34,\n    \"n_sent\": 221,\n    \"rows_per_sentence\": 2.8687782805429864,\n    \"design_effect\": 1.930984323294398,\n    \"mde80_analytic\": 0.2119654330898864,\n    \"mde80_empirical_SIG\": 0.1651442162649592,\n    \"sig_delta_mean\": 0.38401119281045754\n   },\n   {\n    \"n_err\": 600,\n    \"n_cor\": 100,\n    \"n_sent\": 221,\n    \"rows_per_sentence\": 3.167420814479638,\n    \"design_effect\": 2.079761479075101,\n    \"mde80_analytic\": 0.13824424657548062,\n    \"mde80_empirical_SIG\": 0.11548453789810326,\n    \"sig_delta_mean\": 0.3941173055555556\n   },\n   {\n    \"n_err\": 600,\n    \"n_cor\": 200,\n    \"n_sent\": 221,\n    \"rows_per_sentence\": 3.6199095022624435,\n    \"design_effect\": 2.305181412076166,\n    \"mde80_analytic\": 0.11325479491977979,\n    \"mde80_empirical_SIG\": 0.08651686791551257,\n    \"sig_delta_mean\": 0.3880717361111111\n   },\n   {\n    \"n_err\": 600,\n    \"n_cor\": 400,\n    \"n_sent\": 221,\n    \"rows_per_sentence\": 4.524886877828054,\n    \"design_effect\": 2.7560212780782956,\n    \"mde80_analytic\": 0.10170061908891778,\n    \"mde80_empirical_SIG\": 0.07867653690148052,\n    \"sig_delta_mean\": 0.3916515208333333\n   },\n   {\n    \"n_err\": 600,\n    \"n_cor\": 800,\n    \"n_sent\": 221,\n    \"rows_per_sentence\": 6.334841628959276,\n    \"design_effect\": 3.657701010082555,\n    \"mde80_analytic\": 0.10206483378137968,\n    \"mde80_empirical_SIG\": 0.07422019330814635,\n    \"sig_delta_mean\": 0.391324625\n   },\n   {\n    \"n_err\": 900,\n    \"n_cor\": 34,\n    \"n_sent\": 221,\n    \"rows_per_sentence\": 4.226244343891403,\n    \"design_effect\": 2.607244122297593,\n    \"mde80_analytic\": 0.24277164650356262,\n    \"mde80_empirical_SIG\": 0.16274797563041987,\n    \"sig_delta_mean\": 0.38715577342047935\n   },\n   {\n    \"n_err\": 900,\n    \"n_cor\": 100,\n    \"n_sent\": 221,\n    \"rows_per_sentence\": 4.524886877828054,\n    \"design_effect\": 2.7560212780782956,\n    \"mde80_analytic\": 0.153394598545664,\n    \"mde80_empirical_SIG\": 0.12286012945236424,\n    \"sig_delta_mean\": 0.39073294444444445\n   },\n   {\n    \"n_err\": 900,\n    \"n_cor\": 200,\n    \"n_sent\": 221,\n    \"rows_per_sentence\": 4.97737556561086,\n    \"design_effect\": 2.9814412110793604,\n    \"mde80_analytic\": 0.12105041816521246,\n    \"mde80_empirical_SIG\": 0.08534032631845342,\n    \"sig_delta_mean\": 0.38889761111111115\n   },\n   {\n    \"n_err\": 900,\n    \"n_cor\": 400,\n    \"n_sent\": 221,\n    \"rows_per_sentence\": 5.882352941176471,\n    \"design_effect\": 3.4322810770814907,\n    \"mde80_analytic\": 0.10321962021907008,\n    \"mde80_empirical_SIG\": 0.07892078312035407,\n    \"sig_delta_mean\": 0.3862252685185185\n   },\n   {\n    \"n_err\": 900,\n    \"n_cor\": 800,\n    \"n_sent\": 221,\n    \"rows_per_sentence\": 7.6923076923076925,\n    \"design_effect\": 4.33396080908575,\n    \"mde80_analytic\": 0.09763469588111369,\n    \"mde80_empirical_SIG\": 0.07068512570103713,\n    \"sig_delta_mean\": 0.3911400254629629\n   }\n  ],\n  \"caveat\": \"order-of-magnitude guide only: analytic Hanley-McNeil + SIG-row resampling as an upper-variance proxy; no FREE-labelled data at these counts exist\"\n },\n \"recommendation\": [\n  \"L25 planned 250 -> ~92 usable: MDE80 0.130, power@0.069 0.32 => MARGINAL\",\n  \"L25 planned 300 -> ~111 usable: MDE80 0.119, power@0.069 0.37 => MARGINAL\",", "numLines": 185, "startLine": 1120, "totalLines": 1310}}
```

### [53] TOOL CALL — Grep · 2026-09-24 10:59:26 UTC

```
Pattern: ""model": "[^"]*""
```

### [54] TOOL RESULT — Grep · 2026-09-24 10:59:26 UTC

```
{"mode": "content", "numFiles": 0, "filenames": [], "content": "1:\"model\": \"meta-llama/llama-3.1-8b-instruct\"\n2:\"model\": \"meta-llama/llama-3.3-70b-instruct\"\n3:\"model\": \"meta-llama/llama-3.3-70b-instruct\"\n4:\"model\": \"qwen/qwen3-235b-a22b-2507\"\n5:\"model\": \"qwen/qwen3-235b-a22b-2507\"\n6:\"model\": \"mistralai/mistral-small-3.2-24b-instruct\"\n7:\"model\": \"deepseek/deepseek-v3.2\"\n8:\"model\": \"google/gemma-3-27b-it\"\n9:\"model\": \"microsoft/phi-4\"\n10:\"model\": \"openai/gpt-4.1-mini\"\n11:\"model\": \"google/gemini-2.5-flash\"\n12:\"model\": \"cohere/command-r7b-12-2024\"", "numLines": 12, "totalLines": 2652, "appliedLimit": 12}
```

### [55] TOOL CALL — Read · 2026-09-24 10:59:26 UTC

```
/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/results/testability_FREE_v2.json
```

### [56] TOOL RESULT — Read · 2026-09-24 10:59:26 UTC

```
{"type": "text", "file": {"filePath": "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/results/testability_FREE_v2.json", "content": "{\n \"mode\": \"search_only\",\n \"utc\": \"2026-09-24T07:37:10Z\",\n \"rule\": \"TESTABLE iff >= 50 ERROR and >= 50 CORRECT rows, each class spread over >= 25 sentences\",\n \"word_terciles\": {\n  \"cut_1\": 30,\n  \"cut_2\": 35\n },\n \"all_rows\": {\n  \"population\": \"all FREE rows\",\n  \"n_rows\": 2652,\n  \"n_ERROR\": 759,\n  \"n_CORRECT\": 0,\n  \"sentences_with_ERROR\": 208,\n  \"sentences_with_CORRECT\": 0,\n  \"TESTABLE\": false,\n  \"reportable_30_30\": false,\n  \"label_counts\": {\n   \"ERROR_CERT\": 759,\n   \"UNRESOLVED_GLOSS_NOT_RUN\": 1506,\n   \"UNPARSEABLE\": 188,\n   \"NO_OUTPUT\": 199\n  },\n  \"strata\": {\n   \"template_id\": {\n    \"T1\": {\n     \"n_ERROR\": 75,\n     \"n_CORRECT\": 0,\n     \"sentences_with_ERROR\": 26,\n     \"sentences_with_CORRECT\": 0,\n     \"TESTABLE\": false,\n     \"reportable_30_30\": false,\n     \"label_counts\": {\n      \"ERROR_CERT\": 75,\n      \"UNRESOLVED_GLOSS_NOT_RUN\": 196,\n      \"UNPARSEABLE\": 30,\n      \"NO_OUTPUT\": 23\n     }\n    },\n    \"T2\": {\n     \"n_ERROR\": 112,\n     \"n_CORRECT\": 0,\n     \"sentences_with_ERROR\": 27,\n     \"sentences_with_CORRECT\": 0,\n     \"TESTABLE\": false,\n     \"reportable_30_30\": false,\n     \"label_counts\": {\n      \"UNPARSEABLE\": 18,\n      \"ERROR_CERT\": 112,\n      \"UNRESOLVED_GLOSS_NOT_RUN\": 182,\n      \"NO_OUTPUT\": 24\n     }\n    },\n    \"T3\": {\n     \"n_ERROR\": 63,\n     \"n_CORRECT\": 0,\n     \"sentences_with_ERROR\": 20,\n     \"sentences_with_CORRECT\": 0,\n     \"TESTABLE\": false,\n     \"reportable_30_30\": false,", "numLines": 60, "startLine": 1, "totalLines": 2245}}
```

### [57] TOOL CALL — Grep · 2026-09-24 10:59:56 UTC

```
Pattern: "^def |^    \"\"\"|weight"
```

### [58] TOOL CALL — Read · 2026-09-24 10:59:56 UTC

```
/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/results/gate_report.json
```

### [59] TOOL RESULT — Read · 2026-09-24 10:59:56 UTC

```
{"type": "text", "file": {"filePath": "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/results/gate_report.json", "content": "{\n \"status\": \"NOT_RUN\",\n \"reason\": \"D9: HTTP 403 aii_run_budget_exhausted on every gate call (190 calls refused, $0 billed); free models 429 daily limit\",\n \"items\": \"results/gate_items.json (840 items, 7 classes x 120, halves A 442 / B 398) are built and frozen\",\n \"runner\": \"src/resume_gloss.py gate\"\n}", "numLines": 6, "startLine": 1, "totalLines": 6}}
```

### [60] TOOL RESULT — Grep · 2026-09-24 10:59:56 UTC

```
{"mode": "content", "numFiles": 0, "filenames": [], "content": "1:\"\"\"Stratified, cluster-weighted AUROC machinery for S10 (pure numpy; no labels are read here).\n2-\n3-auroc_within(stratum) = sum_s U_s / sum_s P_s where, inside stratum s, U_s counts ERROR x CORRECT pairs with the ERROR\n4-row scored higher (ties 0.5) and P_s = n_err_s * n_cor_s. Stratum = one value for the pooled AUROC, template_id for the\n--\n7:Bootstrap weights: each replicate gives every sentence (cluster) an integer multiplicity k (sentences resampled with\n8:replacement WITHIN each template). A row inherits the multiplicity of its sentence, so a pair (i, j) is weighted k_i*k_j\n9-(identical to physically duplicating the rows). For the within-sentence stratum a duplicated sentence is a duplicated\n10-stratum, so its pairs must count k (not k^2): rows then carry sqrt(k).\n11-\"\"\"\n--\n18:    \"\"\"Precomputes per-stratum score ranks once; value(cluster_weights) is then O(n) per replicate.\"\"\"\n19-\n20-    def __init__(self, score: np.ndarray, is_err: np.ndarray, stratum: np.ndarray, cluster: np.ndarray,\n21-                 stratum_is_cluster: bool = False):\n--\n54:def boot_weights(cluster_stratum: np.ndarray, B: int, seed: int) -> np.ndarray:\n55:    \"\"\"(B, n_clusters) integer multiplicities; clusters resampled with replacement within their stratum (template).\"\"\"\n56-    rng = np.random.default_rng(seed)\n57-    n = len(cluster_stratum)\n58-    W = np.zeros((B, n), dtype=np.int32)\n--\n67:def summarize(point: float, boots: np.ndarray) -> dict:\n68-    boots = boots[~np.isnan(boots)]\n69-    if len(boots) == 0:\n70-        return {\"est\": point, \"ci\": [None, None], \"se\": None, \"n_boot\": 0}", "numLines": 26, "totalLines": 26}
```

### [61] ASSISTANT · 2026-09-24 11:00:12 UTC

```
Now checking the earlier evaluation's pairwise-class file layout and what the experiment-7 README says about score orientation.
```

### [62] TOOL CALL — Grep · 2026-09-24 11:00:12 UTC

```
Pattern: ""(edges|pairs|exact|align|nf|condition|classes)[a-z_]*":"
```

### [63] TOOL RESULT — Grep · 2026-09-24 11:00:12 UTC

```
{"mode": "content", "numFiles": 0, "filenames": [], "content": "1:\"pairs\":\n1:\"condition\":\n2:\"pairs\":\n2:\"condition\":\n3:\"pairs\":\n3:\"condition\":\n4:\"pairs\":\n4:\"condition\":\n5:\"pairs\":\n5:\"condition\":\n6:\"pairs\":\n6:\"condition\":\n7:\"pairs\":\n7:\"condition\":\n8:\"pairs\":", "numLines": 15, "totalLines": 884, "appliedLimit": 15}
```

### [64] TOOL CALL — Grep · 2026-09-24 11:00:12 UTC

```
Pattern: "(?i)orient|higher = |judge_cheap|c_score_align"
```

### [65] TOOL RESULT — Grep · 2026-09-24 11:00:12 UTC

```
{"mode": "content", "numFiles": 0, "filenames": [], "content": "21:| **Primary (criterion c)**: within-template AUROC, c_score_sig vs judge_cheap_disg (n = 1,904 with both scores, 220 sentences) | 0.954 vs 0.587, **delta +0.367 [0.328, 0.404]**, one-sided p < 0.0005 → **PASS** |\n97:Primary test (criterion c): the within-template stratified paired delta AUROC(c_score_sig) − AUROC(judge_cheap_disg) on\n100:above 0. All metric parameters are frozen from exp 5, with no fitting on R_COMP. Metrics are oriented so that higher =", "numLines": 3, "totalLines": 3}
```

### [66] TOOL CALL — Grep · 2026-09-24 11:00:18 UTC

```
Pattern: ""pairs": \[\{[^\]]{0,400}"
```

### [67] TOOL RESULT — Grep · 2026-09-24 11:00:18 UTC

```
{"mode": "content", "numFiles": 0, "filenames": [], "content": "", "numLines": 0, "totalLines": 0}
```

### [68] TOOL CALL — Grep · 2026-09-24 11:00:18 UTC

```
Pattern: "pairwise_classes_RCOMP"
```

### [69] TOOL RESULT — Grep · 2026-09-24 11:00:18 UTC

```
{"mode": "content", "numFiles": 0, "filenames": [], "content": "68-| `src/t8_part1.py: endorse_det / endorse_mc` | Endorsement of every candidate under the counting rules R_exact / R_align / R_name / R_liberal / R_oracle (deterministic) and R_point_MC / R_point_label (500 MC draws). **R_point_label and R_oracle use gold-side labels: they are oracle-assisted predictions, never gold-free metrics** |\n69-| `src/t8_part1.py: ed_ci(y, en, W)` | e, d and AUROC_b with sentence-cluster CIs for binary endorsements or MC draws (replicate b uses draw b mod 500) |\n70:| eval-2 `pairwise_matrix`, `ed_decomposition`, `scatter_index`, `net_test` | Unchanged, now applied to R_COMP (`pairwise_classes_RCOMP.jsonl`, with a `condition` field) |\n71-\n72-## Deviations and caveats\n--\n105-|---|---|\n106-| `prereg_d_split.json` / `.sha256` | Pre-registration: classes, rules, 0.388 discount (read from exp 8), cuts (from eval 2), pools, decision rule, validation criterion, power grid |\n107:| `src/t8_run_rcomp_matrix.py` → `results/pair_matrix_RCOMP.jsonl`, `pairwise_classes_RCOMP.jsonl` | R_COMP eqmv matrix (442 tasks, 11,912 pairs, 0 UNKNOWN), staged mini → 50 → all |\n108-| `src/t8_part1.py`, `src/t8_part1_net.py` | Part 1 → `results/part1.json`, `results/part1_net.json`, `tables/p1_*.csv` |\n109-| `src/t8_part2.py` | Part 2 → `results/part2.json`, `tables/p2_*.csv` |", "numLines": 11, "totalLines": 11}
```

### [70] TOOL CALL — Grep · 2026-09-24 11:00:24 UTC

```
Pattern: ""[A-Za-z_0-9]+":"
```

### [71] TOOL CALL — Glob · 2026-09-24 11:00:24 UTC

```
Pattern: "src/*.py"
```

### [72] TOOL RESULT — Grep · 2026-09-24 11:00:24 UTC

```
{"mode": "content", "numFiles": 0, "filenames": [], "content": "1:\"nodes\":\n1:\"node_id\":\n1:\"canon_fol\":\n1:\"rows\":\n1:\"row_key\":\n1:\"slot\":\n1:\"family\":\n1:\"family_field\":\n1:\"system_class\":\n1:\"is_peer\":\n1:\"node_id\":\n1:\"canon_fol\":\n1:\"rows\":\n1:\"row_key\":\n1:\"slot\":\n1:\"family\":\n1:\"family_field\":\n1:\"system_class\":\n1:\"is_peer\":\n1:\"row_key\":\n1:\"slot\":\n1:\"family\":\n1:\"family_field\":\n1:\"system_class\":\n1:\"is_peer\":", "numLines": 25, "totalLines": 42208, "appliedLimit": 25}
```

### [73] TOOL RESULT — Glob · 2026-09-24 11:00:24 UTC

```
{"filenames": ["/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/src/t8_paths.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/src/t8_run_rcomp_matrix.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/src/t8_prereg.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/src/t8_classes.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/src/t8_part1.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/src/t8_part3.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/src/t8_part1_net.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/src/t8_part2.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/src/t8_part4.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/src/t8_figs.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/src/t8_eval_out.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/src/t8_record_md.py"], "durationMs": 249, "numFiles": 12, "truncated": false, "totalMatches": 12, "countIsComplete": true}
```

### [74] TOOL CALL — Grep · 2026-09-24 11:00:30 UTC

```
Pattern: ""(pairs|edges|eq[a-z_]*|exact[a-z_]*|align[a-z_]*|nf[a-z_]*|hyb[a-z_]*|cls[a-z_]*|class[a-z_]*|condition|sentence_id)":"
```

### [75] TOOL RESULT — Grep · 2026-09-24 11:00:30 UTC

```
{"mode": "content", "numFiles": 0, "filenames": [], "content": "1:\"pairs\":\n1:\"sentence_id\":\n1:\"eqmv_ms\":\n1:\"condition\":\n2:\"pairs\":\n2:\"sentence_id\":\n2:\"eqmv_ms\":\n2:\"condition\":\n3:\"pairs\":\n3:\"sentence_id\":\n3:\"eqmv_ms\":\n3:\"condition\":", "numLines": 12, "totalLines": 1768, "appliedLimit": 12}
```

### [76] TOOL CALL — Grep · 2026-09-24 11:00:30 UTC

```
Pattern: "^def "
```

### [77] TOOL RESULT — Grep · 2026-09-24 11:00:30 UTC

```
{"mode": "content", "numFiles": 0, "filenames": [], "content": "34:def sboot_mean(vals: np.ndarray, sids: np.ndarray, B: int = 2000) -> dict:\n35-    \"\"\"Mean of pair/row-level values with a sentence-cluster bootstrap CI (stats.SentBoot weights).\"\"\"\n36-    m = ~np.isnan(vals)\n--\n46:def main() -> None:\n47-    A = {}\n48-    pre = json.loads((ROOT / \"prereg_d_split.json\").read_text())", "numLines": 7, "totalLines": 7}
```

### [78] TOOL CALL — Grep · 2026-09-24 11:00:34 UTC

```
Pattern: "pair_matrix_RCOMP|pairs\"\]|\[\"pairs|p\[\"|pr\[\""
```

### [79] TOOL RESULT — Grep · 2026-09-24 11:00:34 UTC

```
{"mode": "content", "numFiles": 0, "filenames": [], "content": "48-    pre = json.loads((ROOT / \"prereg_d_split.json\").read_text())\n49-    p_acc = float(pre[\"vocab_discount\"][\"accept_prob\"])\n50:    mats = jl(RESD / \"pair_matrix_RCOMP.jsonl\")\n51-    sms = {(r[\"sentence_id\"], r[\"condition\"]): CS.SentenceMatrix(r) for r in mats}\n52-    zver, csha = mats[0][\"z3_version\"], mats[0][\"code_sha\"]\n--\n61-            nt[k[1]][1] += line[\"n_wedges\"]\n62-    A[\"nontransitivity\"] = {c: {\"open\": v[0], \"wedges\": v[1], \"rate\": v[0] / max(v[1], 1)} for c, v in nt.items()}\n63:    A[\"matrix\"] = {\"n_tasks\": len(mats), \"n_pairs\": int(sum(len(r[\"pairs\"]) for r in mats)),\n64:                   \"reason_counts\": {c: dict(pd.Series([p[3] for r in mats if r[\"condition\"] == c for p in r[\"pairs\"]]).value_counts()) for c in (\"SIG\", \"FREE\")},\n65:                   \"n_unknown\": int(sum(p[2] is None for r in mats for p in r[\"pairs\"])), \"z3\": zver, \"code_sha\": csha}\n66-    # ---------------- per-row readouts\n67-    C = pd.DataFrame(jl(E7 / \"results\" / \"rcomp_candidates.jsonl\"))\n--\n138-        sc = MC.scatter_index(Plab, sms_sig, cut)\n139-        A[\"SIG_scatter\"] = {\"overall\": sc[\"summary\"][\"overall\"], \"by_words_tercile\": sc[\"summary\"][\"by_words_tercile\"],\n140:                            \"pair_gee\": sc[\"summary\"][\"pair_gee\"], \"n_pairs\": sc[\"summary\"][\"n_pairs\"], \"prediction\": sc[\"summary\"][\"prediction\"]}\n141-    except (ValueError, KeyError, ZeroDivisionError) as e:\n142-        logger.error(f\"scatter_index failed: {e}\")\n--\n214-        for wt, g in both.groupby(\"word_tercile\"):\n215-            drops[rule][\"by_word_tercile\"][wt] = sboot_mean((g.sig_exact - g[col]).values.astype(float), g.sentence_id.values)\n216:    A[\"drop_pairs\"] = drops\n217-    ag = {k: sboot_mean(both[k].values.astype(float), sids) for k in (\"sig_exact\", \"sig_align\", \"sig_nf\", \"free_exact\", \"free_align\", \"free_nf\", \"free_align_or_nf\", \"free_name\")}\n218:    A[\"agreement_rates_pairs\"] = ag\n219-    bt2 = SentBoot(sids, b=2000, seed=0)\n220-    W2 = bt2.W()", "numLines": 27, "totalLines": 27}
```

### [80] ASSISTANT · 2026-09-24 11:00:46 UTC

```
Dependencies are mapped. Now reading the neurosymbolic field handbook for the domain-practice check.
```

### [81] TOOL CALL — Skill · 2026-09-24 11:00:46 UTC

```
aii-handbook-auto-neurosymbolic
```

### [82] TOOL RESULT — Skill · 2026-09-24 11:00:46 UTC

```
{"success": true, "commandName": "aii-handbook-auto-neurosymbolic"}
```

### [83] ASSISTANT · 2026-09-24 11:00:50 UTC

```
Handbook read. One quick lookup to confirm the reporting conventions of the factuality meta-evaluation benchmarks, then I'll write the plan.
```

### [84] TOOL CALL — ToolSearch · 2026-09-24 11:00:50 UTC

```
{'query': 'select:WebSearch', 'max_results': 1}
```

### [85] TOOL RESULT — ToolSearch · 2026-09-24 11:00:50 UTC

```
{"matches": ["WebSearch"], "query": "select:WebSearch", "total_deferred_tools": 27}
```

### [86] TOOL CALL — WebSearch · 2026-09-24 11:00:55 UTC

```
TRUE benchmark factual consistency evaluation ROC AUC Honovich 2022 meta-evaluation reference-free metrics
```

### [87] TOOL CALL — WebSearch · 2026-09-24 11:00:55 UTC

```
Deutsch Dror Roth 2021 statistical analysis summarization evaluation metrics resampling bootstrap confidence intervals permutation test
```

### [88] TOOL RESULT — WebSearch · 2026-09-24 11:01:01 UTC

```
{"query": "Deutsch Dror Roth 2021 statistical analysis summarization evaluation metrics resampling bootstrap confidence intervals permutation test", "results": [{"tool_use_id": "srvtoolu_01PZsjphnDMphHhuRCdW8iWy", "content": [{"title": "A Statistical Analysis of Summarization Evaluation Metrics Using Resampling Methods - ACL Anthology", "url": "https://aclanthology.org/2021.tacl-1.67/"}, {"title": "A Critical Look at Meta-evaluating Summarisation ...", "url": "https://aclanthology.org/2024.findings-emnlp.869.pdf"}, {"title": "[2104.00054] A Statistical Analysis of Summarization Evaluation Metrics using Resampling Methods", "url": "https://arxiv.org/abs/2104.00054"}, {"title": "Beyond correlation: The Impact of Human Uncertainty in Measuring the Effectiveness of Automatic Evaluation and LLM-as-a-Judge", "url": "https://arxiv.org/pdf/2410.03775"}, {"title": "A Statistical Analysis of Summarization Evaluation Metrics Using Resampling Methods | Transactions of the Association for Computational Linguistics | MIT Press", "url": "https://direct.mit.edu/tacl/article-abstract/doi/10.1162/tacl_a_00417/107833"}, {"title": "TACL/EMNLP 2021: A Statistical Analysis of Summarization Evaluation Metrics Using Resampling Methods - YouTube", "url": "https://www.youtube.com/watch?v=doKv85BeXio"}, {"title": "A Statistical Analysis of Summarization Evaluation Metrics using Resampling Methods - ADS", "url": "https://ui.adsabs.harvard.edu/abs/2021arXiv210400054D/abstract"}, {"title": "TACL’21 A Statistical Analysis of Summarization Evaluation Metrics Using", "url": "https://cogcomp.seas.upenn.edu/papers/DeutschDrRo21.pdf"}, {"title": "Re-Examining System-Level Correlations of Automatic Summarization Evaluation Metrics", "url": "https://arxiv.org/pdf/2204.10216"}, {"title": "Publications | Daniel Deutsch", "url": "https://danieldeutsch.github.io/publications/"}]}, "Based on the search results, I found the paper you're looking for:\n\n## \"A Statistical Analysis of Summarization Evaluation Metrics Using Resampling Methods\"\n\nThe paper is authored by Daniel Deutsch, Rotem Dror, and Dan Roth and was published in the Transactions of the Association for Computational Linguistics, Volume 9, in 2021.\n\n### Key Contributions:\n\nThe work proposes methods for calculating confidence intervals and running hypothesis tests for correlations using two resampling methods: bootstrapping and permutation. After evaluating which proposed methods are most appropriate for summarization through two simulation experiments, the authors analyze the results of applying these methods to several different automatic evaluation metrics across three sets of human annotations.\n\n### Main Findings:\n\nThe confidence intervals are rather wide, demonstrating high uncertainty in the reliability of automatic metrics. While many metrics fail to show statistical improvements over ROUGE, two recent works, QAEval and BERTScore, do show improvements in some evaluation settings.\n\nThe paper addresses a fundamental problem in summarization evaluation: it was unclear how precise correlation estimates are, nor whether differences between two metrics' correlations reflect a true difference or if it is due to mere chance."], "durationSeconds": 7.155508318000008, "searchCount": 1}
```

### [89] TOOL RESULT — WebSearch · 2026-09-24 11:01:01 UTC

```
{"query": "TRUE benchmark factual consistency evaluation ROC AUC Honovich 2022 meta-evaluation reference-free metrics", "results": [{"tool_use_id": "srvtoolu_01AxFjWveN4WWQdKMscHbJFs", "content": [{"title": "(PDF) TRUE: Re-evaluating Factual Consistency Evaluation", "url": "https://www.researchgate.net/publication/361069161_TRUE_Re-evaluating_Factual_Consistency_Evaluation"}, {"title": "Can We Trust the Judges? Validation of Factuality Evaluation Methods via Answer Perturbation", "url": "https://arxiv.org/html/2609.15561v1"}, {"title": "TRUE: Re-evaluating Factual Consistency Evaluation Or HonovichT ∗ Roee AharoniG", "url": "https://arxiv.org/pdf/2204.04991"}, {"title": "WeCheck: Strong Factual Consistency Checker via Weakly Supervised Learning", "url": "https://arxiv.org/pdf/2212.10057"}, {"title": "TRUE: Re-evaluating Factual Consistency Evaluation", "url": "https://aclanthology.org/2022.naacl-main.287.pdf"}, {"title": "CAN WE TRUST THE JUDGES? VALIDATION OF FACTUALITY", "url": "https://arxiv.org/pdf/2609.15561"}, {"title": "TrueTeacher: Learning Factual Consistency Evaluation with Large Language Models", "url": "https://arxiv.org/pdf/2305.11171"}, {"title": "(PDF) TrueTeacher: Learning Factual Consistency Evaluation with Large Language Models", "url": "https://www.researchgate.net/publication/376393015_TrueTeacher_Learning_Factual_Consistency_Evaluation_with_Large_Language_Models"}, {"title": "BUMP: A Benchmark of Unfaithful Minimal Pairs for Meta-Evaluation of Faithfulness Metrics", "url": "https://arxiv.org/pdf/2212.09955"}, {"title": "GitHub - google-research/true: Code and data accompanying the paper \"TRUE: Re-evaluating Factual Consistency Evaluation\". · GitHub", "url": "https://github.com/google-research/true"}]}, "Based on the search results, I found comprehensive information about the TRUE benchmark for factual consistency evaluation:\n\n## TRUE Benchmark Overview\n\nTRUE (Honovich et al., 2022) argues that system-level correlation with human judgment is the wrong meta-evaluation target. Instead, it recasts 11 annotated datasets, from summarization to knowledge-grounded dialogue, into a single binary labelling scheme, scored by example-level ROC AUC.\n\n## Benchmark Composition\n\nThe TRUE benchmark consists of 11 datasets of 4 tasks including text summarization, dialogue generation, paraphrasing, and fact checking, where each sample in datasets is annotated with a binary label manually.\n\n## Evaluation Methodology\n\nFollowing TRUE, metrics are normalized into a logit and their ROC AUC is reported with respect to binary logits. Evaluation with ROC AUC does not require metrics to set specific decision thresholds. This approach avoids the need for threshold tuning, making ROC AUC a more objective meta-evaluation metric.\n\n## Key Findings\n\nThe benchmark finds that large-scale NLI and QA-QA approaches come out strongest and mutually complementary, well ahead of BARTScore, BERTScore, and n-gram overlap.\n\nThe TRUE benchmark represents an important contribution to reference-free factual consistency evaluation by establishing a standardized meta-evaluation approach across multiple diverse tasks and datasets."], "durationSeconds": 7.805856704000005, "searchCount": 1}
```

### [90] ASSISTANT · 2026-09-24 11:04:41 UTC

```
I have enough to write the plan. Writing the plan JSON now.
```

### [91] TOOL CALL — Write · 2026-09-24 11:04:41 UTC

```
File: /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_plan/gen_plan_experiment_3/.terminal_claude_agent_struct_out.json

{
"title": "Finish free-vocabulary labels, then test agreement",
"summary": "Resume, once, the frozen gloss step of dataset 5 (art_Ia_FT284H33j) that never ran in iteration 4. That step is the gate on 840 known-answer items, then the Haiku-4.5 + Qwen3-235B gloss check of the 1,506 MAPPED R_COMP FREE rows, then finalize + seal, the SIG end-to-end check and a blind Sonnet-5 audit. This turns R_COMP FREE (221 long templated sentences, free vocabulary, gold trusted by construction) into a labelled confirmation set with a CORRECT class. The frozen iteration-3 scores are then joined, for the first time, to these labels. Before any gloss call, the scores are sealed: c_score_align, c_exact, the flash-lite rubric-A judge in the disguised and original views, and the local Qwen3-8B judge. Criterion (c) is tested ONCE on the untouched 2,198-row subset: within-template AUROC of c_score_align minus flash-lite, disguised AND original, with template-stratified sentence-cluster bootstrap B=2000, and both 95% CIs > 0. Also scored: the nested gain over the judge; H-MECH (i) and (iv) replicated on a second population with trusted gold (share of ERROR peers behind a CORRECT candidate's disagreement; exact vs ALIGN e/d, where ERROR_GLOSS rows are the meaning-rename analogue); complexity, coverage, cost; pre-declared label-regime sensitivities, including a Haiku-only label regime that shares no family with any peer or judge; and the V1-V5 variants as Holm-corrected exploratory rows. GG is never evaluated here. Hard cap $4, expected spend ~$2.0.",
"runpod_compute_profile": "cpu_plus",
"domain_practice": "WHAT I READ: the neurosymbolic handbook (aii-handbook-auto-neurosymbolic): [S13] FOLIO/MALLS gold ~36-39% wrong, so the label construction is part of the result; [S6]/[S7] compiling is not faithfulness; [S9] round-trip gold-free certification is occupied; [S8] the predicate list is the NL->FOL lever, which is why a free-vocabulary test matters. Also TRUE (Honovich et al., NAACL 2022, arXiv 2204.04991); Deutsch, Dror & Roth (TACL 2021, 'A Statistical Analysis of Summarization Evaluation Metrics Using Resampling Methods'); and the run's own artifacts: dataset-5 prereg_freelab.json v1.1, gloss.py/gate.py/assemble_labels.py/post_seal_join.py/resume_gloss.py, dataset_card.md; exp-7 tables.md, auc_tools.py, README; eval-3 power_E2.json (rcomp_free block) and t8_part2.py.\n\nHOW THIS KIND OF STUDY IS BUILT (meta-evaluation of a reference-free faithfulness metric).\n(1) MEASURE. Item-level, threshold-free ROC AUC against BINARY faithful/unfaithful labels on real system outputs. This is the TRUE convention: 11 datasets recast to binary labels and scored by example-level ROC AUC, precisely so that no metric needs a threshold. Precision/recall at a fixed operating point is added only as a secondary row. System-level correlation (Kendall tau over systems) is reported but is known to be low-powered with ~10 systems.\n(2) UNCERTAINTY. Deutsch et al. 2021 show that metric-comparison CIs are wide. The expected practice is bootstrap CIs over the INPUT unit (documents or sentences), and paired tests on the DIFFERENCE between two metrics computed on the same resamples (bootstrap or permutation), never two overlapping marginal CIs. Here the input unit is the sentence (10 candidates per sentence are dependent), so the resample is a sentence-cluster bootstrap. It is stratified by template, because templates differ in base rate and in how hard they are.\n(3) BASELINES a reviewer names first. The incumbent practitioners actually use: a cheap API LLM-as-judge, in both the original view and a disguised view that controls for memorised gold (the contamination check the user explicitly asked for). A frontier judge, to answer 'you only beat a weak judge'. The strongest non-LLM baseline stack, with a nested test showing added signal. Fair tuning means a frozen prompt, the same prompt as on the development data, and no refit on the test labels.\n(4) DATA. The field distrusts FOLIO/MALLS gold (S13). Prover-built or construction-built gold (ProverQA, template sets) is accepted, but only as templated or semi-synthetic text with known shortcut and external-validity limits. R_COMP is exactly that: 9 templates, >=25 words, >=3 conditions, one exception clause.\n(5) LABEL QUALITY. The labeller's own accuracy is measured on known-answer items before it labels anything (the gate). A blind audit sample with Wilson CIs is standard, and so is agreement with a previous label version (kappa). Labellers must share no instrument with the metric: no aligner, and no checker model that is also a system or peer under test.\n(6) HOW MUCH IS ENOUGH. Nobody reads an AUROC from fewer than ~50 per class. The run's rule is >=50 ERROR and >=50 CORRECT over >=25 sentences each, and eval-3 power_E2.json puts R_COMP FREE at MDE80 ~0.11 with 200 CORRECT and ~0.10 with 400. The expected FREE gap is large (iteration-3 tier-A, contaminated labels: c_align 0.804 vs judge_disg 0.581), so power is not the binding constraint. Label validity is. More labels, not more metrics, is the fix if power binds.\n(7) FRESHNESS. As in WMT, which re-scores metrics on a new test set each year, confirmation counts only if it is scored once with frozen parameters on data no selection step touched. Score and label seals written before the join are this run's version of that.",
"practice_alignment": "MEETS:\n- (1) The primary measure is item-level, threshold-free within-template AUROC on binary labels (TRUE convention). Precision/recall at the exp-5 frozen operating threshold is a secondary row.\n- (2) Paired deltas are computed on shared sentence-cluster bootstrap weights, template-stratified, B=2000 (Deutsch et al.). A within-template label-permutation placebo checks the interval machinery.\n- (3) The incumbent flash-lite rubric-A judge is compared in BOTH views, plus the local Qwen3-8B judge. The nested [judge + c] - judge and the reverse [c + judge] - c are cross-fitted by sentence folds. All prompts are frozen from iteration 3 (judge scores are reused, not re-run).\n- (5) The labeller is gated on 840 known-answer items before it labels. The blind audit uses Wilson CIs. The agreement table against the old labels reports kappa. The firewall holds: no aligner in the labeller, and the labeller never reads score files.\n- (6) The testability rule and the MDE are stated in the prereg before labels exist.\n- (7) Scores are sealed before the first gloss call and labels are sealed before the join. The verdict is read once.\n\nDEPARTURES, each with its justification and what it costs:\n(a) SEMI-SYNTHETIC TEXT. R_COMP has 9 templates of templated English. This is justified because it is the only in-scope free-vocabulary set with trustworthy gold. The cost: a confirmation here says nothing about natural long sentences (that is E2's job, a sibling artifact). The paper must say 'templated' next to every R_COMP FREE number.\n(b) MODEL-RELATIVE LABELS. The CORRECT/ERROR_GLOSS labels depend on two LLM checkers. This is mitigated by the gate (balanced accuracy >= 0.90 per checker and for the conjunction), the SIG end-to-end check on 300 known rows (false-CORRECT bar <= 0.05), and the blind audit. The cost: the labels are not human.\n(c) INSTRUMENT OVERLAP I found in the frozen prereg, which the direction does not mention. The Qwen checker (qwen/qwen3-235b-a22b-2507) is the SAME model as one FREE generator/peer slot. The Sonnet-5 auditor is the same family (Anthropic) as the Haiku checker. The checkers are frozen, so I do not change them. I add two $0 sensitivity regimes, pre-declared: s5 drops the qwen-slot candidate rows (self-preference in glossing its own names), and s6 uses Haiku-only labels, which share no family with any peer (meta, qwen, mistral, deepseek, google, microsoft, openai, cohere) or judge (google, qwen-local). I also add a second blind auditor from a family disjoint from checkers, peers and judges (z-ai GLM-4.6, fallback moonshotai Kimi-K2), ~$0.10. Residual cost: if s6 flips the verdict, (c) is reported as label-regime-sensitive.\n(d) POPULATION SELECTION. The 'untouched' subset is defined as rows NOT tier-A labelled by iteration 3's aligner-based labeller, which mostly means rows the aligner could not resolve against the reference. It is selected by an instrument that c_score_align shares. This is justified because the subset is what was never read. It is mitigated by s3 (all FREE rows, including the 454 seen rows) as a pre-declared sensitivity. The cost: a residual selection effect that cannot be removed.\n(e) FRONTIER JUDGE. There is no frontier judge on FREE by default. A 150-row stratified gemini-3.1-pro original-view run (~$0.55) is budget-conditional (step F). If it does not run, the 'weak-judge' objection stays answered only by the E frame (ratio 0.957, point estimate only).\n(f) NO RENAME INVARIANCE ROW here. GG is firewalled from R_COMP FREE by design, and the rename rows belong to sibling artifacts. This is stated as scope.\n(g) SYSTEM LEVEL. Kendall tau over 10 slots x 2 prompt variants is descriptive only (20 points). This is standard practice but low-powered.\n(h) OUT-OF-FAMILY FAITHFUL FORMS. About 13% of ERROR_CERT rows are out-of-family faithful forms, so ERROR is over-called by a bounded amount. s1 (a label-free syntactic filter) and s2 (UNRESOLVED bounds) bracket the effect. The cost: label noise that biases AUROCs for ALL metrics toward 0.5, and does not bias the paired sign.",
"builds_on": "This plan continues the consensus lead. It is a FIX-ONCE of the dataset-5 labeller with the claim unchanged, not a fresh line. It reuses the following artifacts; all paths are read-only, and the executor copies what it needs.\n\n(1) DATASET 5 (art_Ia_FT284H33j), /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5. The whole labeller is reused byte-identically:\n- src/ (freelab.py sha 05a5151e..., run_search.py, assemble_labels.py, gloss.py, gate.py, resume_gloss.py, post_seal_join.py, soundness.py, common.py, inputs.py, build_output.py);\n- vendor/ and VENDOR_SHA256.json;\n- prompts/gloss_v1.json (sha a2eecd66...);\n- prereg_freelab.json v1.1 + .sha256, prereg_freelab_v1.json + .sha256;\n- deviations.json (D1-D9);\n- work/ (sentences.json, free_rows.jsonl, sig_rows.jsonl, models_snapshot.json);\n- results/ (map_search.jsonl: 2,163 classes, 0 caps, 0 z3 unknown; the search is NOT re-run; gate_items.json with 840 items and halves A 442 / B 398; sig_replay_rows.jsonl and sig_replay_syn.jsonl with in_e2e_gloss_subsample_300; soundness_audit.json; free_labels_v2.jsonl; seal.json holding the search-only seal 9609ebbb... / untouched b364a49a...);\n- tests/.\nThe search-only negative findings are carried as facts: 0/1,595 false ERROR_CERT; rescue 9-10% (the thing the gloss must stop); ERROR_CERT precision 0.867 on the executor audit; 297/420 old ERROR rows MAPPED.\n\n(2) EXP 7 (art_cxnoDYQNFolW), /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7. Reused:\n- results/rcomp_candidates.jsonl: per-row frozen scores c_score_align, c_score_sig (= the exact name-based consensus on FREE rows, verified in step 0), c_score_nf, c_score_hyb, g_align, g_nf, judge_cheap_disg/orig, judge_local_disg/orig, cost_usd, coverage_status, strata, template_id, slot, family, prompt_variant;\n- judge_FREE.jsonl and judge_local_FREE.jsonl (raw judge verdicts, for cost and seconds);\n- src/auc_tools.py (the within-template AUROC and template-stratified cluster-bootstrap machinery; copied verbatim);\n- src/consensus_rcomp.py (the peer-pool definition and the fallback recompute of c_score_align);\n- rcomp/raw/generations.jsonl, rcomp/work/rcomp_sentences.json and data/nltk_data, which common.py reads by absolute path.\nThe SIG result (0.954 vs 0.587) is used only as the $0 reproduction gate G0.\n\n(3) EVAL 3 (art_BvAL_KZTZuw8), /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3. Reused:\n- results/pair_matrix_RCOMP.jsonl (label-free exact/ALIGN/NF pair verdicts, 11,912 pairs, with a condition field);\n- pairwise_classes_RCOMP.jsonl;\n- src/t8_paths.py + t8_part2.py (the pattern that loads eval-2's SentenceMatrix / scatter_index / net_test / ed_decomposition unchanged);\n- power_E2.json rcomp_free (MDE grid).\n\n(4) R_COMP source dataset 3 (art_zcwCQgTqk6DN), iter_2/gen_art/gen_art_dataset_3: lexicon.json and full_data_out.json, read by dataset-5 common.py.\n\n(5) SIBLING FREEZE (optional): marker M1 at iter_5/gen_art/*/freeze/CONSENSUS_FREEZE_READY.json for the V1-V5 code (see step 4). If it is missing, V1/V2/V3/V5 are implemented from the verbatim definitions in the hypothesis and V4 is NOT_COMPUTED.\n\nNEGATIVE FINDINGS this plan builds past:\n- the aligner-based FREE labels of iteration 3 are void (over-call ERROR);\n- the panel route for R_COMP FREE is closed;\n- CSC is closed;\n- SIG evidence is out of scope for the user's condition.",
"implementation_pseudocode": "WORKSPACE = /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/<this artifact> (all writes inside). Layout: labeller/ (the dataset-5 copy), confirm/ (new analysis code), results/, src/, logs/, the top-level deliverables, and .aii/manifest.yaml + README.md.\n\n=== S-1 SETUP AND REPRODUCTION GATES ($0, ~30 min) ===\n1. Copy dataset-5 dirs into WS/labeller/: src vendor prompts work results tests, the files pytest.ini, prereg_freelab*.json/.sha256, VENDOR_SHA256.json, deviations.json and cost_ledger.jsonl. Do NOT copy temp/, full_data_out.json or the .venv. common.py derives ROOT from its own file, so every relative path lands in labeller/. Absolute reads (E7, D3) stay read-only.\n2. uv venv; install z3-solver (pin the version recorded in labeller/results/seal.json vendor/code metadata or logs/; if none is recorded, use the version printed in labeller/logs/search_free.log), httpx, loguru, nltk, numpy, scipy, pandas, scikit-learn and pytest. Run `pytest labeller/tests -q`; all must pass. sha256-check freelab.py == 05a5151e... and every vendor file against prereg vendor_sha256.\n3. BUG FIX: labeller/results/gate_report.json currently holds {'status':'NOT_RUN',...}. assemble_labels.py final mode does any(v.get('PASS') for v in gr.values()), which crashes on string values. Rename the file to gate_report_D9_notrun.json before the gate. Log it as deviation D10.\n4. BUDGET GUARD: in labeller/src/gloss.py set HARD_STOP_USD = 3.6 (the $4 cap minus a 10% reserve). Record the before/after sha in deviations D11. gloss.py is NOT in the sealed code hash (only freelab, run_search and assemble_labels are), but log it anyway.\n5. R0 (labeller reproducibility): copy free_labels_v2.jsonl aside; run `python src/assemble_labels.py --mode search_only` in a scratch copy of labeller/; the label_vector_sha256_all_rows must == 9609ebbb... (full value from seal.json). If it does not match, STOP and diagnose (z3 version); do not proceed to paid calls.\n6. G0 (score-side reproduction, SIG only, so no FREE labels are touched): load rcomp_candidates.jsonl rows with condition=='SIG' and the exp-7 SIG labels (pure z3). Compute the within-template AUROC of c_score_sig and judge_cheap_disg with the copied auc_tools.py. They must equal 0.954 and 0.587 (+-0.001, n=1,904), which confirms the orientation (higher = ERROR) and the machinery.\n7. 1-token probe to OPENROUTER_BASE_URL (cheapest model) and log it to the ledger. On 402/403: go to FALLBACK A (do all CPU work first).\n\n=== STEP 0 SCORE SEAL + PREREG ($0, BEFORE ANY GLOSS CALL) ===\n8. Whitelist loader for rcomp_candidates.jsonl: json.loads with object_pairs_hook, keeping ONLY row_key, item_id, sentence_id, condition, template_id, slot, system, family, prompt_variant, parse_ok, coverage_status, words, word_tercile, nconds_weak, depth_weak, nquant, nested, negated_condition, clause_type, c_score_align, c_score_sig, c_score_nf, c_score_hyb, g_align, g_nf, judge_cheap_disg, judge_cheap_orig, judge_local_disg, judge_local_orig, cost_usd, secs_sig and n_peers_*. Every label-derived key is DROPPED at parse time: label*, matched_reading, repair_*, correct_not_equivalent, tier_B_provisional, panel_votes, ref_flagged, sig_status, off_signature.\n   Keep condition=='FREE'. Assert that the row_key set == the 2,652 dataset-5 FREE keys.\n9. c_exact = c_score_sig on FREE rows. VERIFY it by recomputing 1 - share(peers with exact z3 equivalence) from eval-3 pair_matrix_RCOMP.jsonl (condition FREE, the 'exact' reason code), using the peer-pool rule in exp-7 consensus_rcomp.py (leave-own-family-out; same sentence and prompt variant, if that is the rule; read the code). Agreement must be >= 99% of rows, else use the recomputed column and log a deviation. Do the same cross-check for c_score_align vs the ALIGN flags.\n10. Label-free derived scores, computed now from pair_matrix_RCOMP (FREE):\n   - END_MAJ binary under exact and under ALIGN (the eval-2 definition: the candidate is in the largest peer class; ties per eval-2 code);\n   - V1 c_pn = 1 - share_agree / max_class_share among the sentence's peers;\n   - V2 reliability-weighted: per-family weight w_f = mean pairwise ALIGN agreement of family f across all OTHER sentences (out of the sentence's fold, 5 folds by sha1('rcomp_folds_v1|'+sid)%5); c_rw = 1 - sum_w(agree)/sum_w(peers);\n   - V3 = V1 applied with the V2 weights;\n   - V5 = V3 on the 3-pool deepseek+microsoft+openai.\n   If M1 is already present, use its frozen code instead (step 20). V4 needs frozen E-fitted coefficients: M1 only.\n11. Write score_seal_rcomp.json: sha256 of the sorted (row_key, score-column) vectors for every score column, separately for the untouched rows (untouched = NOT seen_iter3; seen_iter3 is read from labeller/results/free_labels_v2.jsonl, a label-free membership flag already computed in iteration 4) and for all FREE rows; n rows; code shas; UTC time. The labeller processes never import confirm/ (re-run dataset-5 tests/test_firewall.py).\n12. Write prereg_rcomp_confirm.json + .sha256 (see the testing plan for the required content): the criterion, the testability rule, PRIMARY = untouched subset, the estimands, bootstrap details (B=2000, seed 20260924, sentences resampled within template, percentile CI), the nested model spec, sensitivity rows s1-s8 with their exact rules, the audit additions, the exploratory rows with Holm, the poll deadlines, the budget and stop rule, and the verdict map. Commit it (git add + commit), so the timestamp precedes the ledger's first gloss call.\n\n=== STEP 1 GATE (~$0.12) ===\n13. Pilot the cost: run rate_pairs on 3 sentences of half A (both checkers); measure $/pair-verdict; extrapolate to the gate (442 items) and to FREE (the unique pairs from pair_jobs on map_search MAPPED rows; log n_pairs and n_calls). Write cost_projection.json. Proceed only if the projected mandatory total (gate + FREE + SIG e2e + audits) <= $3.24 (the cap minus reserve minus a $0.36 contingency).\n14. `python src/resume_gloss.py gate` (gloss_v1, half A). Read gate_report.json['gloss_v1_A']: balanced accuracy per checker and for both_yes, recall_YES/NO, per-class recall with Wilson CIs, and kappa between Haiku and Qwen.\n    PASS = BA >= 0.90 for haiku, qwen AND both_yes, AND both_yes recall_YES >= 0.85 and recall_NO >= 0.85 (as coded).\n    ALSO REPORT (not gating, direction's 'each class recall >= 0.85'): the classes below 0.85, flagged.\n    FAIL: write prompts/gloss_v2.json. This is ONE revision, decided only from the half-A per-class error pattern; sha it, log it as D12, then run `python src/gate.py run --half B --version gloss_v2`. If that FAILS too, go to FALLBACK B.\n\n=== STEP 2 LABELS ($0.95 + $0.25 + ~$0.6) ===\n15. FREE gloss with NO completion selection. Modify resume_gloss.free_gloss ONLY in its job order and batching (log as D13; verdict logic unchanged):\n    - order = (not untouched, sha1('rcomp_confirm_v1|'+sentence_id));\n    - call rate_pairs per batch of 50 sentences;\n    - after each batch, append the batch's sentence ids to gloss_batches_done.json and re-check the budget.\n    If a budget stop hits, only sentences whose batch completed get gloss verdicts. Rows of unfinished sentences are labelled UNRESOLVED_GLOSS_NOT_RUN, and the completed fraction per template is reported.\n    Then write gloss_verdicts.jsonl exactly as the original code does, for all completed jobs.\n16. `python src/resume_gloss.py finalize --version <passing version>`. This runs assemble_labels --mode final, which applies rule (f) + D8 and writes the final seal, then verify_correct_certificates (MUST be reverified == n_classes, failed == [], else STOP and report), then post_seal_join. post_seal_join sets seen_iter3, writes the untouched hash, and writes old_label_agreement.json (kappa, the old-vs-new table, 20 disagreements).\n    Extend the agreement report with the share of old tier-A ERROR rows that are now CORRECT, and the share of old CORRECT rows that are now ERROR.\n    Copy to WS/: results/rcomp_free_labels_final.jsonl (= free_labels_v2.jsonl) and results/seal.json. Write verify_seal.py, which recomputes both label hashes from the file.\n17. `python src/resume_gloss.py sig_e2e`: on the 300 synonym-renamed SIG rows, false_CORRECT_on_known_ERROR (bar <= 0.05), CORRECT recall, UNRESOLVED share. If the bar FAILS, the labels stand (they are sealed) but criterion (c) is reported with the flag 'label soundness bar failed' and s6 is promoted to co-primary.\n18. `python src/resume_gloss.py audit_ii` (anthropic/claude-sonnet-5, 60 ERROR_CERT + 60 CORRECT stratified by template, seed 20260924). ADDITIONS, pre-declared in the prereg, log D14:\n    (a) +20 ERROR_GLOSS rows through the same prompt (ERROR_GLOSS precision);\n    (b) the same 140 rows through a second blind auditor from a disjoint family (z-ai/glm-4.6; fallback moonshotai/kimi-k2-0905; check the catalogue first), via the same gloss.Client so every call is ledgered;\n    (c) auditor-auditor kappa.\n    Report the precision of each label class with Wilson CIs. An audit NEVER changes a label.\n    If Sonnet-5 is unavailable, use the newest Anthropic Sonnet in the catalogue and log it.\n\n=== STEP 3 CONFIRMATION (c) ($0, after both seals verify) ===\n19. Verify: the label hashes (all + untouched) recompute; score_seal_rcomp.json recomputes from the same whitelist loader; the prereg sha is unchanged. Only then join on row_key.\n20. Poll M1 (only if it has not yet been consumed): glob('/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/*/freeze/CONSENSUS_FREEZE_READY.json'), check token 'aii_iter5_consensus_freeze_v1', verify the listed sha256s, and COPY the files to WS/freeze_copy/. If the frozen consensus_variants.py can score the R_COMP pair matrix within 30 min of adapter work, compute its V scores, sha them into score_seal_rcomp_v.json with a timestamp, and flag them 'scored after label seal, code frozen externally' if that is the case. Otherwise keep the step-10 verbatim variants.\n    Poll every 5 min only while other STEP 3 work runs; hard deadline T0+4h30m. Log each attempt to logs/poll_M1.log.\n21. PRIMARY population P0 = untouched AND label_binary in {ERROR, CORRECT} AND both c_score_align and the judge are non-null. Declare testability: >= 50 CORRECT and >= 50 ERROR over >= 25 sentences each (power adequate at >= 200 CORRECT; report the MDE from power_E2.json that is closest to the realised counts).\n22. For each metric m in [c_score_align (PRIMARY), c_exact, c_score_hyb, c_score_nf, g_align, judge_cheap_disg, judge_cheap_orig, judge_local_disg, judge_local_orig], compute the within-template AUROC (auc_tools, stratum = template_id; ties 0.5) with a CI from the template-stratified sentence bootstrap, B=2000, seed 20260924. Also compute the pooled AUROC as a descriptive row.\n23. Paired deltas on the SAME bootstrap weights: c_score_align - judge_cheap_disg and c_score_align - judge_cheap_orig (the CRITERION: BOTH 95% percentile CIs > 0); also vs the local judges, and c_exact vs c_score_align.\n24. Nesting: 5 sentence folds (sha1('rcomp_folds_v1|'+sid)%5). Fit a logistic on the train folds and predict OOF for [judge_disg], [judge_disg + c_align], [judge_orig], [judge_orig + c_align], [c_align], [c_align + judge_disg], all features rank-normalised within the train fold. Report the within-template AUROC deltas [j+c]-[j] and [c+j]-[c] with a bootstrap over sentences on the fixed OOF predictions (disclosed: no refit per replicate). Add a label-permutation null: 50 within-template shuffles, report the p95 of the null delta.\n25. Operating point: at exp-5's frozen c_score_align threshold (read it from the exp-5 prereg; if it is absent, report at FA = 0.10 on CORRECT), give recall, FA and precision with Wilson CIs, next to the judge's rubric threshold (p < 0.5 = UNFAITHFUL).\n26. H-MECH on FREE with trusted gold, using the eval-2 functions through the eval-3 t8_paths import pattern:\n    (i) among the CORRECT candidates' non-agreeing peers (exact and ALIGN rules), the share labelled ERROR, UNRESOLVED or UNPARSEABLE (and NO_OUTPUT if it is in the pool), with CIs; the bar is >= 0.50 ERROR;\n    (ii) SCATTER ratio SI_cor/SI_err (bar >= 2);\n    (iii) NET delta(e+d) over word terciles W1<30 / W2<35 / W3 (bar > 0);\n    (iv) END_MAJ e and d under exact vs ALIGN, overall and by error type: ERROR_GLOSS (z3-equivalent under a family map but the names are wrong = the MEANING_RENAME analogue); ERROR_CERT by dominant certificate type (coverage / polarity / countermodel / z3_sat / unmappable); prediction ALIGN d lower AND e higher. Give per-item CONFIRMED/REFUTED.\n27. Sensitivities (all reported, none gating):\n    - s1a: drop, from ALL labels, rows whose candidate matches the label-free out-of-family syntactic detectors frozen in the prereg: one predicate name with >= 2 distinct constants in the same argument slot; a disjunction of two atoms with the same predicate; an existential quantifier under the universal introducing a variable used as an argument of a sentence-template predicate slot; a negation token (not|non|no|never|lacks|without|doesnot) inside a CamelCase name at a non-first token.\n    - s1b: drop only ERROR_CERT rows that match those detectors (upper bound).\n    - s2: UNRESOLVED_GLOSS as ERROR, then as CORRECT.\n    - s3: all FREE rows (including the 454 seen_iter3).\n    - s4: per template, and ERROR vs CORRECT-weak and ERROR vs CORRECT-strong (matched_reading); READING_CHOICE excluded from the primary, as in the prereg (EXCLUDED).\n    - s5: drop rows generated by the qwen/qwen3-235b-a22b-2507 slot.\n    - s6: HAIKU-ONLY labels, re-deriving gloss_decision with verdict = (haiku, haiku) for every pair, $0.\n    - s7: fewshot prompt variant only.\n    - s8: primary with batch-incomplete sentences dropped (identical if there was no budget stop).\n28. Exploratory rows: V1, V2, V3, V5 (and V4 if M1) minus V0, and minus judge_disg; Holm-corrected across all exploratory paired deltas (report raw and adjusted p from bootstrap sign proportions).\n29. Complexity: within-template AUROC and delta by word tercile and by nconds_weak bins, the T3-T1 delta-of-deltas with CI, and the c_align vs judge slope comparison (same bootstrap).\n30. System level: per slot x prompt_variant (<= 20 systems), the mean metric score vs the ERROR rate; Kendall tau-b with a bootstrap CI over sentences; descriptive.\n31. Coverage: for each metric, the scored share over ALL 2,652 FREE rows, with UNPARSEABLE (188) and NO_OUTPUT (199) in the denominator; plus the 'unparseable-as-ERROR' row, with the consensus score set to its maximum for unparseable candidates (a declared convention).\n32. Cost: consensus $ per candidate FULL (all peer generations amortised) and MARGINAL (z3 only), taken from exp-7 cost_usd / costs.jsonl and cost_units.csv units; judge $ and seconds per call from judge_FREE.jsonl. The labeller cost (gloss + audit $ per row) is reported SEPARATELY as a labelling cost, never as a metric cost.\n33. VERDICT (confirm_verdict_rcomp.json):\n    - NOT_TESTABLE if P0 has < 50 CORRECT (or < 25 sentences);\n    - CONFIRMED if both CIs > 0;\n    - NOT CONFIRMED otherwise (state which view failed and the point estimates).\n    Add flags: underpowered (CORRECT < 200), soundness_bar_failed, s6_flip (the s6 verdict differs), s3_flip, s1a_flip, partial_budget.\n\n=== STEP F (optional, budget-conditional; do it LAST and only if the remaining budget >= $1.00 after step 18) ===\n34. Frontier judge: google/gemini-3.1-pro-preview, original view, the exp-7 run_judges.py rubric prompt verbatim, on a 150-row stratified sample of P0 (75 ERROR / 75 CORRECT, round-robin over templates, seed 20260924). Report the AUROC ratio c_align/frontier with a CI, and the nested [frontier + c] - frontier. If its cost projection from a 5-row pilot exceeds the remainder minus reserve, skip it and say so.\n\n=== OUTPUTS ===\n35. results/:\n    - rcomp_free_labels_final.jsonl, seal.json, verify_seal.py;\n    - gate_report.json, audit_report.json (Sonnet + second auditor), old_label_agreement.json, sig_e2e_report.json;\n    - per_item_rcomp_free.jsonl (row_key, sentence_id, template_id, strata, label, label_binary, label_haiku_only, s1 flag, seen_iter3, every score);\n    - confirm_verdict_rcomp.json, analysis_rcomp.json, tables.md (every table with a '# source:' line naming the file and function);\n    - cost_ledger.jsonl (top-level copy of labeller/cost_ledger.jsonl plus probe calls), deviations.json (D10+ appended to D1-D9).\n    method_out.json (exp_gen_sol_out, validated with aii-json): one example per FREE row, input = JSON {text, candidate_fol, template_id}, output = label, predict_c_score_align / predict_c_exact / predict_judge_cheap_disg / ... as strings (higher = ERROR); metadata carries the verdict and the headline numbers. Also write full/mini/preview variants.\n    src/labelling_tools.py re-exports exhaustive_map_label, equivalent_modulo_vocab_exhaustive and gloss_decision from the unchanged freelab.py, with docstrings stating: GOLD-USING labelling tool (needs the accepted readings plus the atom glosses); never a gold-free metric.\n    README.md + .aii/manifest.yaml (.venv delete: regenerable via `uv venv && uv pip install -r requirements.txt`; everything else keep).",
"fallback_plan": "A. OPENROUTER 402/403 (run budget) or a persistent 5xx:\n- First do ALL $0 work: S-1, STEP 0, the step-10 variants, and the analysis code, tested on the PROVISIONAL view.\n- Then poll every 15 min (logged) until the hard deadline T0+5h.\n- If the block started mid-gloss, the batch rule means the completed sentences are a random (sha1-ordered) subset. Finalize with the verdicts from the completed batches, report the completed fraction per template, and run STEP 3 if >= 50 CORRECT; flag it 'partial_budget'.\n- If no gloss verdicts exist at the deadline: (c) = NOT_TESTABLE. Report, CLEARLY LABELLED PROVISIONAL and non-confirmatory, the ERROR_CERT vs MAPPED view on the untouched rows (636/1,175; ~13% contamination on each side, per the dataset-5 audit), with the same statistics. The paper must not count it as confirmation.\n\nB. GATE FAILS TWICE (v1 on half A, v2 on half B): every MAPPED row becomes UNRESOLVED_GLOSS_GATE_FAILED (the frozen rule), and (c) = NOT_TESTABLE, declared. Also run s6-style single-checker diagnostics on the gate halves (which checker failed, and on which class) and report them. Run the provisional view as in A. Do NOT substitute an ungated checker.\n\nC. ONE CHECKER UNAVAILABLE (model retired, or provider errors > 20% after retries):\n- Qwen gone: Haiku-only labels (the s6 regime) become PRIMARY, with deviation D-checker. The gate must still pass for Haiku alone (BA >= 0.90, recall >= 0.85 per super-class).\n- Haiku gone: the Qwen-only regime becomes PRIMARY, and the qwen-slot rows are EXCLUDED from the primary (self-check risk). Declare it.\n\nD. COST OVERRUN RISK: if the pilot projection for the FREE gloss exceeds $2.2, process the untouched sentences first (already the order) and stop at the $3.6 stop line; the seen_iter3 sentences are the ones sacrificed. If the audits would breach the line, drop the step-18 additions first, then shrink the Sonnet audit to 40+40, then skip STEP F.\n\nE. CERTIFICATE RE-VERIFICATION FAILS for any CORRECT class: set those classes to UNRESOLVED_CERT_FAIL (a new code, logged), re-seal with a deviation, and report the count. If > 2% of CORRECT classes fail, stop and report the labeller as unsound.\n\nF. R0 HASH MISMATCH (search-only labels do not reproduce): try the z3 version pinned in the dataset-5 logs, and PYTHONHASHSEED=0. If it still mismatches, re-run run_search on the 2,163 classes (~10-20 min CPU), diff the statuses, and proceed only if 0 status changes; else report and use the dataset-5 map_search.jsonl as-is (it is sealed), with a deviation.\n\nG. G0 FAILS (exp-7 SIG AUROCs do not reproduce): check the score orientation (1 - p for the judge), the stratum key and the tie handling. If it is unresolved, recompute c_score_align on FREE from consensus_rcomp.py (frozen code) and pair_matrix_RCOMP, and use the recomputed column, with a deviation.\n\nH. FEW CORRECT (50-199): run everything; state the MDE (0.13-0.19 per power_E2.json) next to the verdict; a NOT CONFIRMED is then reported as 'underpowered'.\n\nI. The M1 marker is absent or unusable by the deadline: V1/V2/V3/V5 come from the verbatim definitions; V4 = NOT_COMPUTED. Nothing in the verdict depends on M1.\n\nJ. Sonnet-5 or GLM-4.6 is unavailable: the newest Anthropic Sonnet; for the second auditor, moonshotai/kimi-k2-0905, else skip it with a note.",
"testing_plan": "ORDERED CHECKS; each must pass before the next stage spends money.\n\n1. ENVIRONMENT: `pytest labeller/tests -q` all pass (test_freelab, test_gloss, test_firewall); the freelab.py and vendor sha256 values equal the prereg values.\n\n2. R0: the search-only re-assembly reproduces label_vector_sha256_all_rows 9609ebbb... exactly, and the untouched count is 2,198.\n\n3. G0: the exp-7 SIG within-template AUROCs reproduce, c_score_sig 0.954 and judge_cheap_disg 0.587 (n = 1,904), within 1e-3, through the copied auc_tools. auroc_within also equals a brute-force per-template U-statistic on 3 templates to 1e-9.\n\n4. SCORE LOADER: the whitelist loader yields no key outside the whitelist (assert). The row_key set equals the 2,652 dataset-5 FREE keys. The c_exact recompute agrees with c_score_sig on >= 99% of rows, and the c_align recompute likewise.\n\n5. PREREG CONTENT CHECK, before hashing: the file must contain\n   - the criterion text;\n   - the testability rule;\n   - PRIMARY = untouched;\n   - B = 2000, seed 20260924, the resampling scheme;\n   - the nested spec;\n   - the s1a detector regexes, verbatim;\n   - s1b-s8;\n   - the H-MECH bars;\n   - the Holm set;\n   - the audit additions (+20 ERROR_GLOSS, the second auditor);\n   - the budget stop $3.6 and the per-sweep projection rule;\n   - the M1 deadline;\n   - the verdict map.\n   Its git commit time must precede the first gloss ledger entry (check at the end).\n\n6. GLOSS PILOT: rate_pairs on 3 half-A sentences. JSON parses for >= 95% of calls without the re-ask. The cost per call matches the models_snapshot estimate within 3x; if it does not, re-project before the gate.\n\n7. GATE: read gate_report.json. If PASS, proceed. Sanity: YES_IDENT recall should be ~1.0 and NO_NONCE recall ~1.0; if either is < 0.9, inspect the prompt formatting before trusting the result.\n\n8. FREE GLOSS, SMALL FIRST: run batch 1 (50 sentences). Then spot-check 10 random verdict records (a use/meaning pair looks sensible; no NO_VERDICT storm, NO_VERDICT < 2%). Check the ledger cum_usd against the projection, then continue with the remaining batches.\n\n9. FINALIZE:\n   - certificate re-verification = 100%;\n   - label counts are plausible: CORRECT + ERROR_GLOSS + UNRESOLVED_GLOSS + READING_CHOICE == 1,506 MAPPED rows; ERROR_CERT still 759;\n   - verify_seal.py passes;\n   - post_seal_join reports 0 missing keys.\n   An early read of the CORRECT count (count only, no scores) triggers the testability declaration.\n\n10. SIG E2E: false-CORRECT on known ERROR <= 0.05 (report, flag if it fails).\n\n11. ANALYSIS CODE is tested BEFORE the join on (a) synthetic data (a perfect score gives AUROC 1.0, a reversed score gives 0.0, a random score ~0.5) and (b) the SIG rows (reproduces G0). Only then is it run once on P0.\n\n12. PLACEBOS after the run:\n   - labels shuffled within template (20 shuffles): the delta CI covers 0 in >= 18/20;\n   - a random score: AUROC CI covers 0.5.\n\n13. INDEPENDENT RE-DERIVATION: a separate script (tests/rederive_confirm.py, written without importing auc_tools) recomputes, from per_item_rcomp_free.jsonl, the PRIMARY within-template AUROCs of c_score_align, judge_disg and judge_orig and both deltas by brute-force pair counting; they must match to 1e-9.\n\n14. OUTPUT VALIDATION: method_out.json validated with aii-json (exp_gen_sol_out); mini/preview generated; aii-file-size-limit check; every tables.md table has a source line; the deviations list is complete (D10 gate_report rename, D11 hard stop, D12 gloss_v2 if used, D13 batching/order, D14 audit additions, plus any fallback); the ledger total <= $4 and equals the sum of per-call usd.\n\n15. MANIFEST/README: .aii/manifest.yaml covers .venv and any cache (delete, regenerable). The README lists the kept result paths (absolute workspace paths) and has a 'Restoring removed files' section."
}
```

### [92] TOOL RESULT — Write · 2026-09-24 11:04:41 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_plan/gen_plan_experiment_3/.terminal_claude_agent_struct_out.json", "content": "{\n\"title\": \"Finish free-vocabulary labels, then test agreement\",\n\"summary\": \"Resume, once, the frozen gloss step of dataset 5 (art_Ia_FT284H33j) that never ran in iteration 4. That step is the gate on 840 known-answer items, then the Haiku-4.5 + Qwen3-235B gloss check of the 1,506 MAPPED R_COMP FREE rows, then finalize + seal, the SIG end-to-end check and a blind Sonnet-5 audit. This turns R_COMP FREE (221 long templated sentences, free vocabulary, gold trusted by construction) into a labelled confirmation set with a CORRECT class. The frozen iteration-3 scores are then joined, for the first time, to these labels. Before any gloss call, the scores are sealed: c_score_align, c_exact, the flash-lite rubric-A judge in the disguised and original views, and the local Qwen3-8B judge. Criterion (c) is tested ONCE on the untouched 2,198-row subset: within-template AUROC of c_score_align minus flash-lite, disguised AND original, with template-stratified sentence-cluster bootstrap B=2000, and both 95% CIs > 0. Also scored: the nested gain over the judge; H-MECH (i) and (iv) replicated on a second population with trusted gold (share of ERROR peers behind a CORRECT candidate's disagreement; exact vs ALIGN e/d, where ERROR_GLOSS rows are the meaning-rename analogue); complexity, coverage, cost; pre-declared label-regime sensitivities, including a Haiku-only label regime that shares no family with any peer or judge; and the V1-V5 variants as Holm-corrected exploratory rows. GG is never evaluated here. Hard cap $4, expected spend ~$2.0.\",\n\"runpod_compute_profile\": \"cpu_plus\",\n\"domain_practice\": \"WHAT I READ: the neurosymbolic handbook (aii-handbook-auto-neurosymbolic): [S13] FOLIO/MALLS gold ~36-39% wrong, so the label construction is part of the result; [S6]/[S7] compiling is not faithfulness; [S9] round-trip gold-free certification is occupied; [S8] the predicate list is the NL->FOL lever, which is why a free-vocabulary test matters. Also TRUE (Honovich et al., NAACL 2022, arXiv 2204.04991); Deutsch, Dror & Roth (TACL 2021, 'A Statistical Analysis of Summarization Evaluation Metrics Using Resampling Methods'); and the run's own artifacts: dataset-5 prereg_freelab.json v1.1, gloss.py/gate.py/assemble_labels.py/post_seal_join.py/resume_gloss.py, dataset_card.md; exp-7 tables.md, auc_tools.py, README; eval-3 power_E2.json (rcomp_free block) and t8_part2.py.\\n\\nHOW THIS KIND OF STUDY IS BUILT (meta-evaluation of a reference-free faithfulness metric).\\n(1) MEASURE. Item-level, threshold-free ROC AUC against BINARY faithful/unfaithful labels on real system outputs. This is the TRUE convention: 11 datasets recast to binary labels and scored by example-level ROC AUC, precisely so that no metric needs a threshold. Precision/recall at a fixed operating point is added only as a secondary row. System-level correlation (Kendall tau over systems) is reported but is known to be low-powered with ~10 systems.\\n(2) UNCERTAINTY. Deutsch et al. 2021 show that metric-comparison CIs are wide. The expected practice is bootstrap CIs over the INPUT unit (documents or sentences), and paired tests on the DIFFERENCE between two metrics computed on the same resamples (bootstrap or permutation), never two overlapping marginal CIs. Here the input unit is the sentence (10 candidates per sentence are dependent), so the resample is a sentence-cluster bootstrap. It is stratified by template, because templates differ in base rate and in how hard they are.\\n(3) BASELINES a reviewer names first. The incumbent practitioners actually use: a cheap API LLM-as-judge, in both the original view and a disguised view that controls for memorised gold (the contamination check the user explicitly asked for). A frontier judge, to answer 'you only beat a weak judge'. The strongest non-LLM baseline stack, with a nested test showing added signal. Fair tuning means a frozen prompt, the same prompt as on the development data, and no refit on the test labels.\\n(4) DATA. The field distrusts FOLIO/MALLS gold (S13). Prover-built or construction-built gold (ProverQA, template sets) is accepted, but only as templated or semi-synthetic text with known shortcut and external-validity limits. R_COMP is exactly that: 9 templates, >=25 words, >=3 conditions, one exception clause.\\n(5) LABEL QUALITY. The labeller's own accuracy is measured on known-answer items before it labels anything (the gate). A blind audit sample with Wilson CIs is standard, and so is agreement with a previous label version (kappa). Labellers must share no instrument with the metric: no aligner, and no checker model that is also a system or peer under test.\\n(6) HOW MUCH IS ENOUGH. Nobody reads an AUROC from fewer than ~50 per class. The run's rule is >=50 ERROR and >=50 CORRECT over >=25 sentences each, and eval-3 power_E2.json puts R_COMP FREE at MDE80 ~0.11 with 200 CORRECT and ~0.10 with 400. The expected FREE gap is large (iteration-3 tier-A, contaminated labels: c_align 0.804 vs judge_disg 0.581), so power is not the binding constraint. Label validity is. More labels, not more metrics, is the fix if power binds.\\n(7) FRESHNESS. As in WMT, which re-scores metrics on a new test set each year, confirmation counts only if it is scored once with frozen parameters on data no selection step touched. Score and label seals written before the join are this run's version of that.\",\n\"practice_alignment\": \"MEETS:\\n- (1) The primary measure is item-level, threshold-free within-template AUROC on binary labels (TRUE convention). Precision/recall at the exp-5 frozen operating threshold is a secondary row.\\n- (2) Paired deltas are computed on shared sentence-cluster bootstrap weights, template-stratified, B=2000 (Deutsch et al.). A within-template label-permutation placebo checks the interval machinery.\\n- (3) The incumbent flash-lite rubric-A judge is compared in BOTH views, plus the local Qwen3-8B judge. The nested [judge + c] - judge and the reverse [c + judge] - c are cross-fitted by sentence folds. All prompts are frozen from iteration 3 (judge scores are reused, not re-run).\\n- (5) The labeller is gated on 840 known-answer items before it labels. The blind audit uses Wilson CIs. The agreement table against the old labels reports kappa. The firewall holds: no aligner in the labeller, and the labeller never reads score files.\\n- (6) The testability rule and the MDE are stated in the prereg before labels exist.\\n- (7) Scores are sealed before the first gloss call and labels are sealed before the join. The verdict is read once.\\n\\nDEPARTURES, each with its justification and what it costs:\\n(a) SEMI-SYNTHETIC TEXT. R_COMP has 9 templates of templated English. This is justified because it is the only in-scope free-vocabulary set with trustworthy gold. The cost: a confirmation here says nothing about natural long sentences (that is E2's job, a sibling artifact). The paper must say 'templated' next to every R_COMP FREE number.\\n(b) MODEL-RELATIVE LABELS. The CORRECT/ERROR_GLOSS labels depend on two LLM checkers. This is mitigated by the gate (balanced accuracy >= 0.90 per checker and for the conjunction), the SIG end-to-end check on 300 known rows (false-CORRECT bar <= 0.05), and the blind audit. The cost: the labels are not human.\\n(c) INSTRUMENT OVERLAP I found in the frozen prereg, which the direction does not mention. The Qwen checker (qwen/qwen3-235b-a22b-2507) is the SAME model as one FREE generator/peer slot. The Sonnet-5 auditor is the same family (Anthropic) as the Haiku checker. The checkers are frozen, so I do not change them. I add two $0 sensitivity regimes, pre-declared: s5 drops the qwen-slot candidate rows (self-preference in glossing its own names), and s6 uses Haiku-only labels, which share no family with any peer (meta, qwen, mistral, deepseek, google, microsoft, openai, cohere) or judge (google, qwen-local). I also add a second blind auditor from a family disjoint from checkers, peers and judges (z-ai GLM-4.6, fallback moonshotai Kimi-K2), ~$0.10. Residual cost: if s6 flips the verdict, (c) is reported as label-regime-sensitive.\\n(d) POPULATION SELECTION. The 'untouched' subset is defined as rows NOT tier-A labelled by iteration 3's aligner-based labeller, which mostly means rows the aligner could not resolve against the reference. It is selected by an instrument that c_score_align shares. This is justified because the subset is what was never read. It is mitigated by s3 (all FREE rows, including the 454 seen rows) as a pre-declared sensitivity. The cost: a residual selection effect that cannot be removed.\\n(e) FRONTIER JUDGE. There is no frontier judge on FREE by default. A 150-row stratified gemini-3.1-pro original-view run (~$0.55) is budget-conditional (step F). If it does not run, the 'weak-judge' objection stays answered only by the E frame (ratio 0.957, point estimate only).\\n(f) NO RENAME INVARIANCE ROW here. GG is firewalled from R_COMP FREE by design, and the rename rows belong to sibling artifacts. This is stated as scope.\\n(g) SYSTEM LEVEL. Kendall tau over 10 slots x 2 prompt variants is descriptive only (20 points). This is standard practice but low-powered.\\n(h) OUT-OF-FAMILY FAITHFUL FORMS. About 13% of ERROR_CERT rows are out-of-family faithful forms, so ERROR is over-called by a bounded amount. s1 (a label-free syntactic filter) and s2 (UNRESOLVED bounds) bracket the effect. The cost: label noise that biases AUROCs for ALL metrics toward 0.5, and does not bias the paired sign.\",\n\"builds_on\": \"This plan continues the consensus lead. It is a FIX-ONCE of the dataset-5 labeller with the claim unchanged, not a fresh line. It reuses the following artifacts; all paths are read-only, and the executor copies what it needs.\\n\\n(1) DATASET 5 (art_Ia_FT284H33j), /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5. The whole labeller is reused byte-identically:\\n- src/ (freelab.py sha 05a5151e..., run_search.py, assemble_labels.py, gloss.py, gate.py, resume_gloss.py, post_seal_join.py, soundness.py, common.py, inputs.py, build_output.py);\\n- vendor/ and VENDOR_SHA256.json;\\n- prompts/gloss_v1.json (sha a2eecd66...);\\n- prereg_freelab.json v1.1 + .sha256, prereg_freelab_v1.json + .sha256;\\n- deviations.json (D1-D9);\\n- work/ (sentences.json, free_rows.jsonl, sig_rows.jsonl, models_snapshot.json);\\n- results/ (map_search.jsonl: 2,163 classes, 0 caps, 0 z3 unknown; the search is NOT re-run; gate_items.json with 840 items and halves A 442 / B 398; sig_replay_rows.jsonl and sig_replay_syn.jsonl with in_e2e_gloss_subsample_300; soundness_audit.json; free_labels_v2.jsonl; seal.json holding the search-only seal 9609ebbb... / untouched b364a49a...);\\n- tests/.\\nThe search-only negative findings are carried as facts: 0/1,595 false ERROR_CERT; rescue 9-10% (the thing the gloss must stop); ERROR_CERT precision 0.867 on the executor audit; 297/420 old ERROR rows MAPPED.\\n\\n(2) EXP 7 (art_cxnoDYQNFolW), /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7. Reused:\\n- results/rcomp_candidates.jsonl: per-row frozen scores c_score_align, c_score_sig (= the exact name-based consensus on FREE rows, verified in step 0), c_score_nf, c_score_hyb, g_align, g_nf, judge_cheap_disg/orig, judge_local_disg/orig, cost_usd, coverage_status, strata, template_id, slot, family, prompt_variant;\\n- judge_FREE.jsonl and judge_local_FREE.jsonl (raw judge verdicts, for cost and seconds);\\n- src/auc_tools.py (the within-template AUROC and template-stratified cluster-bootstrap machinery; copied verbatim);\\n- src/consensus_rcomp.py (the peer-pool definition and the fallback recompute of c_score_align);\\n- rcomp/raw/generations.jsonl, rcomp/work/rcomp_sentences.json and data/nltk_data, which common.py reads by absolute path.\\nThe SIG result (0.954 vs 0.587) is used only as the $0 reproduction gate G0.\\n\\n(3) EVAL 3 (art_BvAL_KZTZuw8), /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3. Reused:\\n- results/pair_matrix_RCOMP.jsonl (label-free exact/ALIGN/NF pair verdicts, 11,912 pairs, with a condition field);\\n- pairwise_classes_RCOMP.jsonl;\\n- src/t8_paths.py + t8_part2.py (the pattern that loads eval-2's SentenceMatrix / scatter_index / net_test / ed_decomposition unchanged);\\n- power_E2.json rcomp_free (MDE grid).\\n\\n(4) R_COMP source dataset 3 (art_zcwCQgTqk6DN), iter_2/gen_art/gen_art_dataset_3: lexicon.json and full_data_out.json, read by dataset-5 common.py.\\n\\n(5) SIBLING FREEZE (optional): marker M1 at iter_5/gen_art/*/freeze/CONSENSUS_FREEZE_READY.json for the V1-V5 code (see step 4). If it is missing, V1/V2/V3/V5 are implemented from the verbatim definitions in the hypothesis and V4 is NOT_COMPUTED.\\n\\nNEGATIVE FINDINGS this plan builds past:\\n- the aligner-based FREE labels of iteration 3 are void (over-call ERROR);\\n- the panel route for R_COMP FREE is closed;\\n- CSC is closed;\\n- SIG evidence is out of scope for the user's condition.\",\n\"implementation_pseudocode\": \"WORKSPACE = /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/<this artifact> (all writes inside). Layout: labeller/ (the dataset-5 copy), confirm/ (new analysis code), results/, src/, logs/, the top-level deliverables, and .aii/manifest.yaml + README.md.\\n\\n=== S-1 SETUP AND REPRODUCTION GATES ($0, ~30 min) ===\\n1. Copy dataset-5 dirs into WS/labeller/: src vendor prompts work results tests, the files pytest.ini, prereg_freelab*.json/.sha256, VENDOR_SHA256.json, deviations.json and cost_ledger.jsonl. Do NOT copy temp/, full_data_out.json or the .venv. common.py derives ROOT from its own file, so every relative path lands in labeller/. Absolute reads (E7, D3) stay read-only.\\n2. uv venv; install z3-solver (pin the version recorded in labeller/results/seal.json vendor/code metadata or logs/; if none is recorded, use the version printed in labeller/logs/search_free.log), httpx, loguru, nltk, numpy, scipy, pandas, scikit-learn and pytest. Run `pytest labeller/tests -q`; all must pass. sha256-check freelab.py == 05a5151e... and every vendor file against prereg vendor_sha256.\\n3. BUG FIX: labeller/results/gate_report.json currently holds {'status':'NOT_RUN',...}. assemble_labels.py final mode does any(v.get('PASS') for v in gr.values()), which crashes on string values. Rename the file to gate_report_D9_notrun.json before the gate. Log it as deviation D10.\\n4. BUDGET GUARD: in labeller/src/gloss.py set HARD_STOP_USD = 3.6 (the $4 cap minus a 10% reserve). Record the before/after sha in deviations D11. gloss.py is NOT in the sealed code hash (only freelab, run_search and assemble_labels are), but log it anyway.\\n5. R0 (labeller reproducibility): copy free_labels_v2.jsonl aside; run `python src/assemble_labels.py --mode search_only` in a scratch copy of labeller/; the label_vector_sha256_all_rows must == 9609ebbb... (full value from seal.json). If it does not match, STOP and diagnose (z3 version); do not proceed to paid calls.\\n6. G0 (score-side reproduction, SIG only, so no FREE labels are touched): load rcomp_candidates.jsonl rows with condition=='SIG' and the exp-7 SIG labels (pure z3). Compute the within-template AUROC of c_score_sig and judge_cheap_disg with the copied auc_tools.py. They must equal 0.954 and 0.587 (+-0.001, n=1,904), which confirms the orientation (higher = ERROR) and the machinery.\\n7. 1-token probe to OPENROUTER_BASE_URL (cheapest model) and log it to the ledger. On 402/403: go to FALLBACK A (do all CPU work first).\\n\\n=== STEP 0 SCORE SEAL + PREREG ($0, BEFORE ANY GLOSS CALL) ===\\n8. Whitelist loader for rcomp_candidates.jsonl: json.loads with object_pairs_hook, keeping ONLY row_key, item_id, sentence_id, condition, template_id, slot, system, family, prompt_variant, parse_ok, coverage_status, words, word_tercile, nconds_weak, depth_weak, nquant, nested, negated_condition, clause_type, c_score_align, c_score_sig, c_score_nf, c_score_hyb, g_align, g_nf, judge_cheap_disg, judge_cheap_orig, judge_local_disg, judge_local_orig, cost_usd, secs_sig and n_peers_*. Every label-derived key is DROPPED at parse time: label*, matched_reading, repair_*, correct_not_equivalent, tier_B_provisional, panel_votes, ref_flagged, sig_status, off_signature.\\n   Keep condition=='FREE'. Assert that the row_key set == the 2,652 dataset-5 FREE keys.\\n9. c_exact = c_score_sig on FREE rows. VERIFY it by recomputing 1 - share(peers with exact z3 equivalence) from eval-3 pair_matrix_RCOMP.jsonl (condition FREE, the 'exact' reason code), using the peer-pool rule in exp-7 consensus_rcomp.py (leave-own-family-out; same sentence and prompt variant, if that is the rule; read the code). Agreement must be >= 99% of rows, else use the recomputed column and log a deviation. Do the same cross-check for c_score_align vs the ALIGN flags.\\n10. Label-free derived scores, computed now from pair_matrix_RCOMP (FREE):\\n   - END_MAJ binary under exact and under ALIGN (the eval-2 definition: the candidate is in the largest peer class; ties per eval-2 code);\\n   - V1 c_pn = 1 - share_agree / max_class_share among the sentence's peers;\\n   - V2 reliability-weighted: per-family weight w_f = mean pairwise ALIGN agreement of family f across all OTHER sentences (out of the sentence's fold, 5 folds by sha1('rcomp_folds_v1|'+sid)%5); c_rw = 1 - sum_w(agree)/sum_w(peers);\\n   - V3 = V1 applied with the V2 weights;\\n   - V5 = V3 on the 3-pool deepseek+microsoft+openai.\\n   If M1 is already present, use its frozen code instead (step 20). V4 needs frozen E-fitted coefficients: M1 only.\\n11. Write score_seal_rcomp.json: sha256 of the sorted (row_key, score-column) vectors for every score column, separately for the untouched rows (untouched = NOT seen_iter3; seen_iter3 is read from labeller/results/free_labels_v2.jsonl, a label-free membership flag already computed in iteration 4) and for all FREE rows; n rows; code shas; UTC time. The labeller processes never import confirm/ (re-run dataset-5 tests/test_firewall.py).\\n12. Write prereg_rcomp_confirm.json + .sha256 (see the testing plan for the required content): the criterion, the testability rule, PRIMARY = untouched subset, the estimands, bootstrap details (B=2000, seed 20260924, sentences resampled within template, percentile CI), the nested model spec, sensitivity rows s1-s8 with their exact rules, the audit additions, the exploratory rows with Holm, the poll deadlines, the budget and stop rule, and the verdict map. Commit it (git add + commit), so the timestamp precedes the ledger's first gloss call.\\n\\n=== STEP 1 GATE (~$0.12) ===\\n13. Pilot the cost: run rate_pairs on 3 sentences of half A (both checkers); measure $/pair-verdict; extrapolate to the gate (442 items) and to FREE (the unique pairs from pair_jobs on map_search MAPPED rows; log n_pairs and n_calls). Write cost_projection.json. Proceed only if the projected mandatory total (gate + FREE + SIG e2e + audits) <= $3.24 (the cap minus reserve minus a $0.36 contingency).\\n14. `python src/resume_gloss.py gate` (gloss_v1, half A). Read gate_report.json['gloss_v1_A']: balanced accuracy per checker and for both_yes, recall_YES/NO, per-class recall with Wilson CIs, and kappa between Haiku and Qwen.\\n    PASS = BA >= 0.90 for haiku, qwen AND both_yes, AND both_yes recall_YES >= 0.85 and recall_NO >= 0.85 (as coded).\\n    ALSO REPORT (not gating, direction's 'each class recall >= 0.85'): the classes below 0.85, flagged.\\n    FAIL: write prompts/gloss_v2.json. This is ONE revision, decided only from the half-A per-class error pattern; sha it, log it as D12, then run `python src/gate.py run --half B --version gloss_v2`. If that FAILS too, go to FALLBACK B.\\n\\n=== STEP 2 LABELS ($0.95 + $0.25 + ~$0.6) ===\\n15. FREE gloss with NO completion selection. Modify resume_gloss.free_gloss ONLY in its job order and batching (log as D13; verdict logic unchanged):\\n    - order = (not untouched, sha1('rcomp_confirm_v1|'+sentence_id));\\n    - call rate_pairs per batch of 50 sentences;\\n    - after each batch, append the batch's sentence ids to gloss_batches_done.json and re-check the budget.\\n    If a budget stop hits, only sentences whose batch completed get gloss verdicts. Rows of unfinished sentences are labelled UNRESOLVED_GLOSS_NOT_RUN, and the completed fraction per template is reported.\\n    Then write gloss_verdicts.jsonl exactly as the original code does, for all completed jobs.\\n16. `python src/resume_gloss.py finalize --version <passing version>`. This runs assemble_labels --mode final, which applies rule (f) + D8 and writes the final seal, then verify_correct_certificates (MUST be reverified == n_classes, failed == [], else STOP and report), then post_seal_join. post_seal_join sets seen_iter3, writes the untouched hash, and writes old_label_agreement.json (kappa, the old-vs-new table, 20 disagreements).\\n    Extend the agreement report with the share of old tier-A ERROR rows that are now CORRECT, and the share of old CORRECT rows that are now ERROR.\\n    Copy to WS/: results/rcomp_free_labels_final.jsonl (= free_labels_v2.jsonl) and results/seal.json. Write verify_seal.py, which recomputes both label hashes from the file.\\n17. `python src/resume_gloss.py sig_e2e`: on the 300 synonym-renamed SIG rows, false_CORRECT_on_known_ERROR (bar <= 0.05), CORRECT recall, UNRESOLVED share. If the bar FAILS, the labels stand (they are sealed) but criterion (c) is reported with the flag 'label soundness bar failed' and s6 is promoted to co-primary.\\n18. `python src/resume_gloss.py audit_ii` (anthropic/claude-sonnet-5, 60 ERROR_CERT + 60 CORRECT stratified by template, seed 20260924). ADDITIONS, pre-declared in the prereg, log D14:\\n    (a) +20 ERROR_GLOSS rows through the same prompt (ERROR_GLOSS precision);\\n    (b) the same 140 rows through a second blind auditor from a disjoint family (z-ai/glm-4.6; fallback moonshotai/kimi-k2-0905; check the catalogue first), via the same gloss.Client so every call is ledgered;\\n    (c) auditor-auditor kappa.\\n    Report the precision of each label class with Wilson CIs. An audit NEVER changes a label.\\n    If Sonnet-5 is unavailable, use the newest Anthropic Sonnet in the catalogue and log it.\\n\\n=== STEP 3 CONFIRMATION (c) ($0, after both seals verify) ===\\n19. Verify: the label hashes (all + untouched) recompute; score_seal_rcomp.json recomputes from the same whitelist loader; the prereg sha is unchanged. Only then join on row_key.\\n20. Poll M1 (only if it has not yet been consumed): glob('/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/*/freeze/CONSENSUS_FREEZE_READY.json'), check token 'aii_iter5_consensus_freeze_v1', verify the listed sha256s, and COPY the files to WS/freeze_copy/. If the frozen consensus_variants.py can score the R_COMP pair matrix within 30 min of adapter work, compute its V scores, sha them into score_seal_rcomp_v.json with a timestamp, and flag them 'scored after label seal, code frozen externally' if that is the case. Otherwise keep the step-10 verbatim variants.\\n    Poll every 5 min only while other STEP 3 work runs; hard deadline T0+4h30m. Log each attempt to logs/poll_M1.log.\\n21. PRIMARY population P0 = untouched AND label_binary in {ERROR, CORRECT} AND both c_score_align and the judge are non-null. Declare testability: >= 50 CORRECT and >= 50 ERROR over >= 25 sentences each (power adequate at >= 200 CORRECT; report the MDE from power_E2.json that is closest to the realised counts).\\n22. For each metric m in [c_score_align (PRIMARY), c_exact, c_score_hyb, c_score_nf, g_align, judge_cheap_disg, judge_cheap_orig, judge_local_disg, judge_local_orig], compute the within-template AUROC (auc_tools, stratum = template_id; ties 0.5) with a CI from the template-stratified sentence bootstrap, B=2000, seed 20260924. Also compute the pooled AUROC as a descriptive row.\\n23. Paired deltas on the SAME bootstrap weights: c_score_align - judge_cheap_disg and c_score_align - judge_cheap_orig (the CRITERION: BOTH 95% percentile CIs > 0); also vs the local judges, and c_exact vs c_score_align.\\n24. Nesting: 5 sentence folds (sha1('rcomp_folds_v1|'+sid)%5). Fit a logistic on the train folds and predict OOF for [judge_disg], [judge_disg + c_align], [judge_orig], [judge_orig + c_align], [c_align], [c_align + judge_disg], all features rank-normalised within the train fold. Report the within-template AUROC deltas [j+c]-[j] and [c+j]-[c] with a bootstrap over sentences on the fixed OOF predictions (disclosed: no refit per replicate). Add a label-permutation null: 50 within-template shuffles, report the p95 of the null delta.\\n25. Operating point: at exp-5's frozen c_score_align threshold (read it from the exp-5 prereg; if it is absent, report at FA = 0.10 on CORRECT), give recall, FA and precision with Wilson CIs, next to the judge's rubric threshold (p < 0.5 = UNFAITHFUL).\\n26. H-MECH on FREE with trusted gold, using the eval-2 functions through the eval-3 t8_paths import pattern:\\n    (i) among the CORRECT candidates' non-agreeing peers (exact and ALIGN rules), the share labelled ERROR, UNRESOLVED or UNPARSEABLE (and NO_OUTPUT if it is in the pool), with CIs; the bar is >= 0.50 ERROR;\\n    (ii) SCATTER ratio SI_cor/SI_err (bar >= 2);\\n    (iii) NET delta(e+d) over word terciles W1<30 / W2<35 / W3 (bar > 0);\\n    (iv) END_MAJ e and d under exact vs ALIGN, overall and by error type: ERROR_GLOSS (z3-equivalent under a family map but the names are wrong = the MEANING_RENAME analogue); ERROR_CERT by dominant certificate type (coverage / polarity / countermodel / z3_sat / unmappable); prediction ALIGN d lower AND e higher. Give per-item CONFIRMED/REFUTED.\\n27. Sensitivities (all reported, none gating):\\n    - s1a: drop, from ALL labels, rows whose candidate matches the label-free out-of-family syntactic detectors frozen in the prereg: one predicate name with >= 2 distinct constants in the same argument slot; a disjunction of two atoms with the same predicate; an existential quantifier under the universal introducing a variable used as an argument of a sentence-template predicate slot; a negation token (not|non|no|never|lacks|without|doesnot) inside a CamelCase name at a non-first token.\\n    - s1b: drop only ERROR_CERT rows that match those detectors (upper bound).\\n    - s2: UNRESOLVED_GLOSS as ERROR, then as CORRECT.\\n    - s3: all FREE rows (including the 454 seen_iter3).\\n    - s4: per template, and ERROR vs CORRECT-weak and ERROR vs CORRECT-strong (matched_reading); READING_CHOICE excluded from the primary, as in the prereg (EXCLUDED).\\n    - s5: drop rows generated by the qwen/qwen3-235b-a22b-2507 slot.\\n    - s6: HAIKU-ONLY labels, re-deriving gloss_decision with verdict = (haiku, haiku) for every pair, $0.\\n    - s7: fewshot prompt variant only.\\n    - s8: primary with batch-incomplete sentences dropped (identical if there was no budget stop).\\n28. Exploratory rows: V1, V2, V3, V5 (and V4 if M1) minus V0, and minus judge_disg; Holm-corrected across all exploratory paired deltas (report raw and adjusted p from bootstrap sign proportions).\\n29. Complexity: within-template AUROC and delta by word tercile and by nconds_weak bins, the T3-T1 delta-of-deltas with CI, and the c_align vs judge slope comparison (same bootstrap).\\n30. System level: per slot x prompt_variant (<= 20 systems), the mean metric score vs the ERROR rate; Kendall tau-b with a bootstrap CI over sentences; descriptive.\\n31. Coverage: for each metric, the scored share over ALL 2,652 FREE rows, with UNPARSEABLE (188) and NO_OUTPUT (199) in the denominator; plus the 'unparseable-as-ERROR' row, with the consensus score set to its maximum for unparseable candidates (a declared convention).\\n32. Cost: consensus $ per candidate FULL (all peer generations amortised) and MARGINAL (z3 only), taken from exp-7 cost_usd / costs.jsonl and cost_units.csv units; judge $ and seconds per call from judge_FREE.jsonl. The labeller cost (gloss + audit $ per row) is reported SEPARATELY as a labelling cost, never as a metric cost.\\n33. VERDICT (confirm_verdict_rcomp.json):\\n    - NOT_TESTABLE if P0 has < 50 CORRECT (or < 25 sentences);\\n    - CONFIRMED if both CIs > 0;\\n    - NOT CONFIRMED otherwise (state which view failed and the point estimates).\\n    Add flags: underpowered (CORRECT < 200), soundness_bar_failed, s6_flip (the s6 verdict differs), s3_flip, s1a_flip, partial_budget.\\n\\n=== STEP F (optional, budget-conditional; do it LAST and only if the remaining budget >= $1.00 after step 18) ===\\n34. Frontier judge: google/gemini-3.1-pro-preview, original view, the exp-7 run_judges.py rubric prompt verbatim, on a 150-row stratified sample of P0 (75 ERROR / 75 CORRECT, round-robin over templates, seed 20260924). Report the AUROC ratio c_align/frontier with a CI, and the nested [frontier + c] - frontier. If its cost projection from a 5-row pilot exceeds the remainder minus reserve, skip it and say so.\\n\\n=== OUTPUTS ===\\n35. results/:\\n    - rcomp_free_labels_final.jsonl, seal.json, verify_seal.py;\\n    - gate_report.json, audit_report.json (Sonnet + second auditor), old_label_agreement.json, sig_e2e_report.json;\\n    - per_item_rcomp_free.jsonl (row_key, sentence_id, template_id, strata, label, label_binary, label_haiku_only, s1 flag, seen_iter3, every score);\\n    - confirm_verdict_rcomp.json, analysis_rcomp.json, tables.md (every table with a '# source:' line naming the file and function);\\n    - cost_ledger.jsonl (top-level copy of labeller/cost_ledger.jsonl plus probe calls), deviations.json (D10+ appended to D1-D9).\\n    method_out.json (exp_gen_sol_out, validated with aii-json): one example per FREE row, input = JSON {text, candidate_fol, template_id}, output = label, predict_c_score_align / predict_c_exact / predict_judge_cheap_disg / ... as strings (higher = ERROR); metadata carries the verdict and the headline numbers. Also write full/mini/preview variants.\\n    src/labelling_tools.py re-exports exhaustive_map_label, equivalent_modulo_vocab_exhaustive and gloss_decision from the unchanged freelab.py, with docstrings stating: GOLD-USING labelling tool (needs the accepted readings plus the atom glosses); never a gold-free metric.\\n    README.md + .aii/manifest.yaml (.venv delete: regenerable via `uv venv && uv pip install -r requirements.txt`; everything else keep).\",\n\"fallback_plan\": \"A. OPENROUTER 402/403 (run budget) or a persistent 5xx:\\n- First do ALL $0 work: S-1, STEP 0, the step-10 variants, and the analysis code, tested on the PROVISIONAL view.\\n- Then poll every 15 min (logged) until the hard deadline T0+5h.\\n- If the block started mid-gloss, the batch rule means the completed sentences are a random (sha1-ordered) subset. Finalize with the verdicts from the completed batches, report the completed fraction per template, and run STEP 3 if >= 50 CORRECT; flag it 'partial_budget'.\\n- If no gloss verdicts exist at the deadline: (c) = NOT_TESTABLE. Report, CLEARLY LABELLED PROVISIONAL and non-confirmatory, the ERROR_CERT vs MAPPED view on the untouched rows (636/1,175; ~13% contamination on each side, per the dataset-5 audit), with the same statistics. The paper must not count it as confirmation.\\n\\nB. GATE FAILS TWICE (v1 on half A, v2 on half B): every MAPPED row becomes UNRESOLVED_GLOSS_GATE_FAILED (the frozen rule), and (c) = NOT_TESTABLE, declared. Also run s6-style single-checker diagnostics on the gate halves (which checker failed, and on which class) and report them. Run the provisional view as in A. Do NOT substitute an ungated checker.\\n\\nC. ONE CHECKER UNAVAILABLE (model retired, or provider errors > 20% after retries):\\n- Qwen gone: Haiku-only labels (the s6 regime) become PRIMARY, with deviation D-checker. The gate must still pass for Haiku alone (BA >= 0.90, recall >= 0.85 per super-class).\\n- Haiku gone: the Qwen-only regime becomes PRIMARY, and the qwen-slot rows are EXCLUDED from the primary (self-check risk). Declare it.\\n\\nD. COST OVERRUN RISK: if the pilot projection for the FREE gloss exceeds $2.2, process the untouched sentences first (already the order) and stop at the $3.6 stop line; the seen_iter3 sentences are the ones sacrificed. If the audits would breach the line, drop the step-18 additions first, then shrink the Sonnet audit to 40+40, then skip STEP F.\\n\\nE. CERTIFICATE RE-VERIFICATION FAILS for any CORRECT class: set those classes to UNRESOLVED_CERT_FAIL (a new code, logged), re-seal with a deviation, and report the count. If > 2% of CORRECT classes fail, stop and report the labeller as unsound.\\n\\nF. R0 HASH MISMATCH (search-only labels do not reproduce): try the z3 version pinned in the dataset-5 logs, and PYTHONHASHSEED=0. If it still mismatches, re-run run_search on the 2,163 classes (~10-20 min CPU), diff the statuses, and proceed only if 0 status changes; else report and use the dataset-5 map_search.jsonl as-is (it is sealed), with a deviation.\\n\\nG. G0 FAILS (exp-7 SIG AUROCs do not reproduce): check the score orientation (1 - p for the judge), the stratum key and the tie handling. If it is unresolved, recompute c_score_align on FREE from consensus_rcomp.py (frozen code) and pair_matrix_RCOMP, and use the recomputed column, with a deviation.\\n\\nH. FEW CORRECT (50-199): run everything; state the MDE (0.13-0.19 per power_E2.json) next to the verdict; a NOT CONFIRMED is then reported as 'underpowered'.\\n\\nI. The M1 marker is absent or unusable by the deadline: V1/V2/V3/V5 come from the verbatim definitions; V4 = NOT_COMPUTED. Nothing in the verdict depends on M1.\\n\\nJ. Sonnet-5 or GLM-4.6 is unavailable: the newest Anthropic Sonnet; for the second auditor, moonshotai/kimi-k2-0905, else skip it with a note.\",\n\"testing_plan\": \"ORDERED CHECKS; each must pass before the next stage spends money.\\n\\n1. ENVIRONMENT: `pytest labeller/tests -q` all pass (test_freelab, test_gloss, test_firewall); the freelab.py and vendor sha256 values equal the prereg values.\\n\\n2. R0: the search-only re-assembly reproduces label_vector_sha256_all_rows 9609ebbb... exactly, and the untouched count is 2,198.\\n\\n3. G0: the exp-7 SIG within-template AUROCs reproduce, c_score_sig 0.954 and judge_cheap_disg 0.587 (n = 1,904), within 1e-3, through the copied auc_tools. auroc_within also equals a brute-force per-template U-statistic on 3 templates to 1e-9.\\n\\n4. SCORE LOADER: the whitelist loader yields no key outside the whitelist (assert). The row_key set equals the 2,652 dataset-5 FREE keys. The c_exact recompute agrees with c_score_sig on >= 99% of rows, and the c_align recompute likewise.\\n\\n5. PREREG CONTENT CHECK, before hashing: the file must contain\\n   - the criterion text;\\n   - the testability rule;\\n   - PRIMARY = untouched;\\n   - B = 2000, seed 20260924, the resampling scheme;\\n   - the nested spec;\\n   - the s1a detector regexes, verbatim;\\n   - s1b-s8;\\n   - the H-MECH bars;\\n   - the Holm set;\\n   - the audit additions (+20 ERROR_GLOSS, the second auditor);\\n   - the budget stop $3.6 and the per-sweep projection rule;\\n   - the M1 deadline;\\n   - the verdict map.\\n   Its git commit time must precede the first gloss ledger entry (check at the end).\\n\\n6. GLOSS PILOT: rate_pairs on 3 half-A sentences. JSON parses for >= 95% of calls without the re-ask. The cost per call matches the models_snapshot estimate within 3x; if it does not, re-project before the gate.\\n\\n7. GATE: read gate_report.json. If PASS, proceed. Sanity: YES_IDENT recall should be ~1.0 and NO_NONCE recall ~1.0; if either is < 0.9, inspect the prompt formatting before trusting the result.\\n\\n8. FREE GLOSS, SMALL FIRST: run batch 1 (50 sentences). Then spot-check 10 random verdict records (a use/meaning pair looks sensible; no NO_VERDICT storm, NO_VERDICT < 2%). Check the ledger cum_usd against the projection, then continue with the remaining batches.\\n\\n9. FINALIZE:\\n   - certificate re-verification = 100%;\\n   - label counts are plausible: CORRECT + ERROR_GLOSS + UNRESOLVED_GLOSS + READING_CHOICE == 1,506 MAPPED rows; ERROR_CERT still 759;\\n   - verify_seal.py passes;\\n   - post_seal_join reports 0 missing keys.\\n   An early read of the CORRECT count (count only, no scores) triggers the testability declaration.\\n\\n10. SIG E2E: false-CORRECT on known ERROR <= 0.05 (report, flag if it fails).\\n\\n11. ANALYSIS CODE is tested BEFORE the join on (a) synthetic data (a perfect score gives AUROC 1.0, a reversed score gives 0.0, a random score ~0.5) and (b) the SIG rows (reproduces G0). Only then is it run once on P0.\\n\\n12. PLACEBOS after the run:\\n   - labels shuffled within template (20 shuffles): the delta CI covers 0 in >= 18/20;\\n   - a random score: AUROC CI covers 0.5.\\n\\n13. INDEPENDENT RE-DERIVATION: a separate script (tests/rederive_confirm.py, written without importing auc_tools) recomputes, from per_item_rcomp_free.jsonl, the PRIMARY within-template AUROCs of c_score_align, judge_disg and judge_orig and both deltas by brute-force pair counting; they must match to 1e-9.\\n\\n14. OUTPUT VALIDATION: method_out.json validated with aii-json (exp_gen_sol_out); mini/preview generated; aii-file-size-limit check; every tables.md table has a source line; the deviations list is complete (D10 gate_report rename, D11 hard stop, D12 gloss_v2 if used, D13 batching/order, D14 audit additions, plus any fallback); the ledger total <= $4 and equals the sum of per-call usd.\\n\\n15. MANIFEST/README: .aii/manifest.yaml covers .venv and any cache (delete, regenerable). The README lists the kept result paths (absolute workspace paths) and has a 'Restoring removed files' section.\"\n}\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [93] ASSISTANT · 2026-09-24 11:04:54 UTC

```
The plan is written to `./.terminal_claude_agent_struct_out.json`. I haven't parsed it with a JSON validator; I only checked the quoting by eye.

**What the plan does:** it finishes the dataset-5 labeller once, by running `resume_gloss.py` byte-identical apart from four logged fixes. That labeller is the only way to get a CORRECT class for R_COMP FREE. The plan then tests criterion (c) once on the 2,198 untouched rows. The spend cap is $4, with a hard stop at $3.6 and about $2.0 expected. The test is: within-template AUROC of the frozen `c_score_align` minus the flash-lite judge, in both the disguised and original views, with a template-stratified sentence-cluster bootstrap (B = 2000). Both confidence intervals must be above 0.

Reading the frozen code turned up four problems. The plan corrects each one and pre-declares it:

- **A crash in the resume path.** `results/gate_report.json` still holds the iteration-4 `NOT_RUN` stub. `assemble_labels.py --mode final` calls `v.get('PASS')` on its values and would crash on the strings. The executor renames the stub before the gate runs.
- **The budget guard is set too high.** `gloss.py` has `HARD_STOP_USD = 6.0`. The plan sets it to 3.6.
- **A label checker is also one of the models being checked.** The frozen Qwen gloss checker (`qwen/qwen3-235b-a22b-2507`) is the same model as one of the FREE generator slots, even though the direction claims the checker families are disjoint from the peers. The planned Sonnet-5 auditor is also the same family as the Haiku checker. The checkers stay frozen, and the plan adds:
  - s5: drop the rows generated by the Qwen slot;
  - s6: labels from Haiku alone, which shares no family with any generator or judge ($0);
  - a second blind auditor from an unrelated family (GLM-4.6, with Kimi-K2 as fallback; about $0.10).
- **The "untouched" rows are chosen by the aligner that `c_score_align` also uses.** They are the rows the iteration-3 aligner-based labeller could not resolve. Sensitivity row s3 (all FREE rows) checks this.

**Reproduction checks before any paid call:**
- The search-only labels must reproduce seal `9609ebbb…`.
- The iteration-3 SIG result (0.954 vs 0.587) must reproduce from the stored scores, which confirms which way the scores point.

**Against completion selection:** the gloss runs in a fixed pre-registered order, in batches of 50 sentences. A budget stop therefore leaves a random subset, and the report gives the completed fraction per template. Fallbacks cover a blocked budget, the gate failing twice, a checker model being unavailable, too few CORRECT rows, and the sibling freeze marker never appearing.

**Also scored:**
- H-MECH (i) and (iv) on trusted gold; ERROR_GLOSS rows stand in for the meaning-rename errors.
- Sensitivity rows s1–s8.
- V1–V5 as Holm-corrected exploratory rows.
- Coverage with unparseable and no-output rows in the denominator, and cost.
- An optional frontier judge on 150 rows, run only if at least $1 remains at the end.

For the domain-practice section I read the neurosymbolic handbook and two meta-evaluation references:
- [TRUE (Honovich et al. 2022)](https://arxiv.org/pdf/2204.04991): binary labels scored by threshold-free ROC AUC.
- [Deutsch, Dror & Roth 2021](https://aclanthology.org/2021.tacl-1.67/): bootstrap and permutation tests on the difference between two metrics.
```
