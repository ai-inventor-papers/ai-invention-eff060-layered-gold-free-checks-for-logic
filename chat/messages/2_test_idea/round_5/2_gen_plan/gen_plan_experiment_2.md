# gen_plan_experiment_2 — test_idea

> Phase: `invention_loop` · round 5 · `gen_plan`
> Run: `run_u75jRHUss0zo` — Gold-Free Faithfulness Metrics for NL-to-FOL Translation
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_plan_experiment_2` (terminal_claude_agent, claude-opus-5-5)

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
Your workspace: `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_plan/gen_plan_experiment_2`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_plan/gen_plan_experiment_2/`:
GOOD: `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_plan/gen_plan_experiment_2/file.py`, `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_plan/gen_plan_experiment_2/results/out.json`
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

id: experiment_iter5_dir2
type: experiment
objective: >-
  MORE POWER: a second, independent untouched L25 sample. E2-A's 350 L25 sentences give MDE80 about 0.11 on L25, and the long
  pool has about 194 usable sentences, below the 237 that eval 3 says are needed. The observed E effect on L25 (+0.069) is
  therefore undetectable without more graded sentences. E2-B draws about 400 fresh MALLS-train L25 sentences by E2's frozen
  selection rule (the 98-sentence pre-ranked surplus first, then the next sha1-ordered eligible sentences, about 700 remain
  after filters). It generates and labels them with the byte-identical E2 code and scores the same frozen metrics with the
  same seal. It also adds the two comparators a reviewer names first: a COST-MATCHED stronger cheap judge and the frontier
  judge on a 300-row subsample.
approach: |-
  SHARED CROSS-ARTIFACT CONTRACT (identical text in all five directions). The five artifacts run in parallel and this is the last iteration, so every piece that joins two artifacts is done by polling for a marker file, and every consumer has a stated fallback that still produces a reportable result.
  (M1) FREEZE marker, written by the 'freeze' experiment: <its workspace>/freeze/CONSENSUS_FREEZE_READY.json with token 'aii_iter5_consensus_freeze_v1'. It holds the sha256 of freeze/consensus_variants.py, of freeze/selection.json (the H-IMPROVE winner, or 'NONE: V0 stands'), and of freeze/gg.py + freeze/gg_gate.json (H-RENAME: PASS/FAIL, gloss model id, prompt sha). Consumers find it with glob('/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/*/freeze/CONSENSUS_FREEZE_READY.json'), check the token, and copy (never import across paths) the frozen files into their own workspace. The expected write time is within about 90 minutes of start (V) and 3.5 h (GG).
  (M2) DRIFT marker, written by the E2-A experiment: <ws>/e2/E2_DRIFT_DECISION.json with token 'aii_iter5_e2_drift_v1' (PASS/FAIL, the numbers, the pinned provider per panel model).
  (M3) FINAL markers: <ws>/e2/E2A_FINAL_READY.json and <ws>/e2b/E2B_FINAL_READY.json with tokens 'aii_iter5_e2a_final_v1' and 'aii_iter5_e2b_final_v1'. Each points to that artifact's per-row file (row_key, sentence_id, stratum, label, tier, every frozen score) and gives its sha256.
  Every poll loop sleeps 5 min, logs each attempt, and has a hard deadline written into the prereg. A path found by glob is read-only; nothing is written outside the artifact's own workspace.
  SPEND: OpenRouter only, via os.environ OPENROUTER_BASE_URL / OPENROUTER_API_KEY. Make a 1-token probe first. Log cost after every call to cost_ledger.jsonl, and stop hard at the artifact cap. Estimate every sweep's cost from a small pilot BEFORE running it, and do not start a sweep whose estimate exceeds the remaining budget minus a 10% reserve. On HTTP 403/402 (run budget) do all CPU work first, then poll every 15 min; if the block persists past the deadline, report the partial result as partial.
  NO COMPLETION SELECTION (the lesson of iteration 4, exp 9): every paid sweep over sentences runs in a pre-registered sha1 order, and each batch of 50 sentences is completed end to end (generation, then labels) before the next batch starts. A budget stop therefore leaves a random subsample of each stratum, not a completion-selected one, and the report states the completed fraction per stratum.

  FROZEN METRIC DEFINITIONS (verbatim; the freeze experiment implements them in consensus_variants.py; fallback implementers use this text).
  For a candidate x of sentence s, P = the parseable peer outputs of s from slots whose family differs from x's family (exp 5 leave-own-family-out, byte-identical to /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/src). A(x,p) = the frozen exp-5 ALIGN equivalence modulo vocabulary (z3 2 s; UNKNOWN = not equivalent, counted). E(x,p) = exact equivalence (lowercased names + arity, no aligner).
  - V0 c_score_align = 1 - |{p in P: A(x,p)}| / |P|. This is the PRIMARY, pre-declared in iteration 3 and never re-selected.
  - V1 c_pn (plurality-normalised) = 1 - min(1, share_A(x) / max_class_share). Classes = the eval-2 pairwise_matrix class ids over P under A. max_class_share = the size of the largest class / |P|. A candidate in the plurality class scores 0.
  - V2 c_rw (reliability-weighted) = 1 - sum_{p in P, A(x,p)} w_f(p) / sum_{p in P} w_f(p). w_f = the mean pairwise A-agreement of family f with every other family, over sentences in the OTHER 4 sentence folds (fold = sha1('E_folds_v1|'+sentence_id) % 5 on E; the same recipe with 'E2_folds_v1|' on E2). It is label-free, a Dawid-Skene-style reliability, shrunk toward the grand mean with 20 pseudo-sentences.
  - V3 = V1 computed with w_f-weighted shares.
  - V4 two-channel = a logistic on (c_exact, c_align), cross-fitted on E's 5 folds for the screen, then refit once on all E R_AB rows and frozen (coefficients in selection.json) for E2.
  - V5 = V3 restricted to the eval-2 cross-fitted best 3-pool (deepseek + microsoft + openai), the cost-matched $0.001-per-sentence variant.
  - PT p_peer_text = the frozen exp-5 fusion, a SECONDARY row.
  - GG (gloss-gated, H-RENAME): x and p agree if E(x,p), OR if an exhaustive injective arity-consistent symbol map from x's symbols onto p's (dataset 5 freelab.equivalent_modulo_vocab_exhaustive, adapted from template atoms to peer symbols, capped at 2e4 maps / 10 s per pair; a cap hit counts as not agreeing) yields z3 equivalence AND the gloss checker confirms that EVERY non-identity mapped symbol pair means the same thing in this sentence. The aligner is NOT used. c_gg = 1 - share of peers agreeing under GG.

  INPUTS: the same as E2-A. Copy /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4 (without .venv) into ./e2bsrc. Relevant: census_E2.json (L25 supply after filters: 960 at 25-29 words + 186 at >= 30), prereg_E2.json (seed string, order, exclusion rules, surplus_rule), select_e2.py. Dataset E, exp 5, exp 6, eval 2 as in E2-A.
  Hard cap $9.5. Projected: 400 x $0.0118 = $4.7 + judges $0.4 + cost-matched judge $1.0 + frontier 300 rows $1.1 = about $7.2. Shrink order: frontier -> cost-matched original view -> L25 sentences (floor 250, always a sha1-order prefix).

  STEP 0, PREREG (prereg_iter5_E2B.json + sha256, before selection):
  - E2-B is a pre-registered REPLICATION SAMPLE drawn by E2's frozen rule; it is a declared deviation from E2's freeze (D-E2B), and the reason is written: power;
  - selection = E2's surplus order (98), then continue the SAME sha1 order ('E2_v1|' + sentence_id) over the remaining eligible L25 pool, disjoint from E, the screen, FOLIO, E2's 550 and the DT reserve, applying E2's 12-gram rule; target 400;
  - the same metric list, seal order and analyses as E2-A;
  - the union and meta-analysis rule;
  - the cost-matched judge spec.

  STEP 1, DRIFT: poll for E2_DRIFT_DECISION.json (M2) until T+1.5 h. Generation runs meanwhile, so no time is lost. Use its decision and its pinned providers. Fallback, only if M2 is absent at the deadline: run E2's gate yourself with the same pinning procedure (about $0.3), and record the pinning procedure in deviations.

  STEP 2, GENERATION + LABELS: E2's run_all.sh steps 5-7 on the E2-B sentences, 10 slots, in batches of 50 completed end to end. Rename controls: controls_e2.py.

  STEP 3, LABEL-FREE SCORING + SEAL: identical to E2-A Step 3 (same file-access allowlist, same fallback rule for M1).
  Plus two comparators:
  - COST-MATCHED JUDGE: deepseek/deepseek-v3.2 (reasoning off), rubric A JSON 0-100, disguised and original. Its cost per candidate (about $2-4e-4) brackets consensus FULL ($1.21e-4 per candidate for 9 peers). Frozen prompt = the flash-lite rubric A text byte-identical. Pilot on 30 rows for parse rate and cost.
  - FRONTIER: google/gemini-3.1-pro-preview, original view, on a 300-row subsample stratified by label-free words tercile x system family, drawn BEFORE labels are joined. Report IPW-corrected AUROC as in T1.

  STEP 4: join after both seals verify.

  STEP 5, ANALYSES (the same code as E2-A where shared):
  - L25 strat AUROC Delta V0 - flash-lite disguised with CI, plus vs flash-lite original, nano, the cost-matched judge and the frontier (ratio V0 / frontier with CI, and nested [frontier + V0] - frontier on the subsample);
  - nested over S4_E2B (cross-fitted);
  - H-MECH (i)-(iv) on E2-B;
  - H-IMPROVE carried variant;
  - rename FA + flip;
  - complexity curves;
  - coverage;
  - cost per candidate FULL/MARGINAL for every metric, including the cost-matched judge and the frontier: the 'does a large judge earn its cost' row the user asked for;
  - tau-b over system x variant.
  UNION: write E2B_FINAL_READY.json (M3), then check for E2A_FINAL_READY.json. If present, compute the union long-pool analysis and the inverse-variance meta-analysis with the SAME code and definition as in E2-A (sentence-cluster bootstrap over the union; strata = L25_E2A, L25_E2B, EXC; primary = V0 - flash-lite disguised). Also give the between-sample heterogeneity (Delta_E2A - Delta_E2B with CI): a replication check that could come out against us.

  OUTPUT:
  - e2b/ (sealed rows, seal.json, testability);
  - scores_E2B.jsonl, score_seal.json, per_item_E2B.jsonl;
  - confirm_verdict_E2B.json;
  - union_longpool.json (if computed here);
  - judges_costmatched.jsonl, judge_frontier.jsonl;
  - tables.md with source lines;
  - method_out.json (exp_gen_sol_out);
  - deviations.json, cost_ledger.jsonl, README.
what_it_would_show: ''
depends_on:
- id: art_2OmxzMInZZJY
  label: sampling frame
  relation_type:
  relation_rationale:
- id: art_U4Hsqt4Ay9Tg
  label: dev dataset
  relation_type:
  relation_rationale:
- id: art_zcwCQgTqk6DN
  label: rename code
  relation_type:
  relation_rationale:
</artifact_direction>

<dependencies>
Completed artifacts this artifact can use during execution.

--- Dependency 1 ---
id: art_U4Hsqt4Ay9Tg
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

--- Dependency 2 ---
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

--- Dependency 3 ---
id: art_2OmxzMInZZJY
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
  are NOT z3-equivalent t
ontology vocabulary injected into prompts),
anything that depends on a particular ontology, and building a better NL→FOL translator. The
contribution is the measurement, not the translator.

Deliverables: reusable Python functions taking (text, fol) — or a set of such pairs — each with a
precise statement of what it measures; the meta-evaluation dataset with its labels; and the results.

I appended a pilot study of this problem with some metrics I already used but haven't verified. Just for reference.
````

### [3] ASSISTANT · 2026-09-24 10:58:30 UTC

```
I'll start by reading the domain handbook and the sampling-frame artifact (E2, dataset 4) in parallel.
```

### [4] TOOL CALL — Skill · 2026-09-24 10:58:30 UTC

```
aii-handbook-auto-neurosymbolic
```

### [5] TOOL RESULT — Skill · 2026-09-24 10:58:30 UTC

```
{"success": true, "commandName": "aii-handbook-auto-neurosymbolic"}
```

### [6] TOOL CALL — Glob · 2026-09-24 10:58:30 UTC

```
Pattern: "*"
```

### [7] TOOL RESULT — Glob · 2026-09-24 10:58:30 UTC

```
{"filenames": ["/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/data_local/yuan-yang__MALLS-v0__MALLS-v0.1-train.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/data_local/yuan-yang__MALLS-v0__MALLS-v0.1-test.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/data_local/yfxiao__folio-refined__train.csv", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/data_local/opendatalab__ProverQA__dev_hard.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/data_local/folio_refined_validation.csv", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/data_local/DSAVlab-UNIUD_MALLS_test_subset-CURATED__MALLS_instances.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/data_local/DSAVlab-UNIUD_FOLIO_validation-curated__FOLIO_instances.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/E_ref/models_snapshot.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/work/models_snapshot.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/pytest.ini", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/E_ref/pytest.ini", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/labeller/complexity_counts.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/labeller/lint_smells.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/labeller/repair_census.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/labeller/repair_census.rows.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/raw/logiclm/FOLIO_dev_gpt-4.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/raw/logiclm/FOLIO_dev_gpt-3.5-turbo.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/raw/logiclm/FOLIO_dev_text-davinci-003.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/src/select_sentences.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/E_ref/exclusion_log.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/E_ref/calib_sentences.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/E_ref/fewshot_exemplars.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/work/fewshot_exemplars.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/prompts/fewshot_v1.txt", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/src/normalise.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/src/screen.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/labeller/disguise.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/src/gate.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/src/calibration.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/E_ref/calibration_items.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/work/calibration_items.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/labeller/label_lib.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/src/label_worker.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/tests/test_fol.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/labeller/fol.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/E_ref/uv.lock", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/E_ref/pyproject.toml", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/src/panel.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/E_ref/trackh_panel_rows.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/E_ref/gate_results.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/src/select_topup.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/E_ref/sentences_topup.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/E_ref/sentences.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/src/generate.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/src/extend_labels.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/src/run_label.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/src/stats.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/src/assemble.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/src/repair_refs.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/src/panel_run.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/E_ref/prereg_strata.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/src/card.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/src_d3/common.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/src_d3/perturb.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/.aii_claude_session.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/logs/venv_setup.log", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/src/or_client.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/code_freeze.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/src_e2/probe.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/logs/D0.diff", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/logs/hf_search.log", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/src_e2/select_e2.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/exclusion_log_E2.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/work/pool_E2.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/census_E2.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/logs/select.log", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/src_e2/e.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/src_e2/compat.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/work/models_snapshot_E2.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/src_e2/prereg_e2.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/prereg_E2.sha256", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/prereg_E2.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/work/sentences_pilot.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/work/sentences_E2_base.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/work/sentences.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/work/generation_manifest.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/logs/gen_pilot.log", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/src_e2/gen_retry.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/logs/generate.log", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/raw/generations.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/raw/ccg2lambda_candidates.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/src_e2/vex.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/src_e2/repair.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/.aii_cost_ledger.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/cost_ledger.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/logs/gate.log", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/logs/drift_run.log", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/work/trackh_panel_rows.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/work/gate_results.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/work/panel_cache.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/src_e2/key_poll.sh", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/src_e2/drift_report.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/panel_drift_E2.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/logs/label.log", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/logs/label_pilot.log", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/work/labels_heldout.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/src_e2/assemble_e2.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/work/sentences_E2_active.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/logs/panel_run.log", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/logs/assemble.log"], "durationMs": 94, "numFiles": 100, "truncated": true, "totalMatches": 135, "countIsComplete": true}
```

### [8] TOOL CALL — Glob · 2026-09-24 10:58:30 UTC

```
Pattern: "**/*"
```

### [9] TOOL RESULT — Glob · 2026-09-24 10:58:30 UTC

```
{"filenames": [".aii_claude_session.json", ".repl_agent.ptylog"], "durationMs": 94, "numFiles": 2, "truncated": false, "totalMatches": 2, "countIsComplete": true}
```

### [10] TOOL CALL — Read · 2026-09-24 10:58:34 UTC

```
/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/prereg_E2.json
```

### [11] TOOL RESULT — Read · 2026-09-24 10:58:34 UTC

```
{"type": "text", "file": {"filePath": "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/prereg_E2.json", "content": "{\n \"artifact\": \"E2 - fresh untouched NL->FOL confirmation set (run_u75jRHUss0zo, iteration 4, gen_art_dataset_4, plan gen_plan_dataset_1_idx3)\",\n \"frozen_at_utc\": \"2026-09-24T07:24:01Z\",\n \"frozen_before\": \"any E2 candidate generation, any E2 label, any metric. NO METRIC IS COMPUTED IN THIS ARTIFACT; iteration-4 experiments must not read E2.\",\n \"sources\": {\n  \"MALLS\": {\n   \"hf_repo\": \"yuan-yang/MALLS-v0\",\n   \"files\": [\n    \"MALLS-v0.1-train.json\",\n    \"MALLS-v0.1-test.json\"\n   ],\n   \"local_copy\": \"data_local/ (byte-identical copies of dataset E's data_local, sha256 in code_freeze.json)\",\n   \"licence\": \"CC-BY-NC-4.0\"\n  },\n  \"ProverQA\": {\n   \"hf_repo\": \"opendatalab/ProverQA\",\n   \"revision\": \"e2561beed450272690da658d21ae667570dbbafc\",\n   \"files\": [\n    \"dev/easy.json\",\n    \"dev/medium.json\",\n    \"dev/hard.json\"\n   ]\n  },\n  \"FOLIO (exclusion only)\": {\n   \"hf_repo\": \"tasksource/folio\",\n   \"revision\": \"295b95fb4fe9be4ff3f933b73142d142cf6b2c97\"\n  }\n },\n \"strata\": {\n  \"E_strata_verbatim\": {\n   \"EXC\": \"MALLS-train; all parseable unless/except/excluding/other-than items (sha1-ordered, cap 100), filled with 'without' then non-XOR 'but not' items with >=15 words\",\n   \"L25\": \">=25 words and n_conditions>=3 (gold-derived nconds), even over word bins 25-29/30-34/>=35\",\n   \"L20\": \"20-24 words and n_conditions>=3, even over bins 20-21/22/23-24\",\n   \"CTRL\": \"FOLIO-v2-train premises where tasksource original gold ≡ folio-refined (IDENTICAL_STRING/EQ/VOCAB/GRAN); reference = refined; bins <12/12-19/>=20 words; non-identical agreement preferred\"\n  },\n  \"L25_E2\": \"MALLS-v0.1-train, >=25 words AND gold n_conditions>=3 (E's rule and E's functions); bins 25-29 and >=30 (30-34; >=35 is exhausted): the >=30 bin gets min(supply, 45% of target), the rest from 25-29; sha1('E2_v1|'+sentence_id) order within bin\",\n  \"EXC_E2\": \"exception_type() of E EXCLUDING the XOR 'but not (both)' pattern, filled to target in pre-registered order (a) MALLS-train core unless/except/excluding/other-than not used by E, (b) MALLS-v0.1-test non-curated core-marker items >=15 words with parseable gold, (c) MALLS-train 'without' >=15 words, (d) non-XOR 'but not' >=15 words (train then test)\",\n  \"DT_E2\": \"ProverQA dev (easy/medium/hard): every nl2fol (sentence->FOL) unit plus question statement->conclusion_fol; gold must parse and round-trip (parse->emit->parse, z3 self-equivalence); dedup by normalised text and by entity-abstracted skeleton (constants -> ENT), 1 per skeleton; inclusion ladder (>=15w,>=2c) -> (>=12w,>=2c) -> (>=15w,>=1c); XOR/OR convention flag carried\"\n },\n \"targets\": {\n  \"L25\": 350,\n  \"EXC\": 100,\n  \"DT\": 100,\n  \"DT_reserve\": 10,\n  \"DT_reserve_rule\": \"used only if the DT gold-parse or generation failure rate exceeds 10%\"\n },\n \"seed_string\": \"E2_v1|\",\n \"order\": \"sha1('E2_v1|' + sentence_id), sentence_id = E's sid(): sha1('heldout|'+norm(text))[:12]\",\n \"exclusion_rules\": {\n  \"hash_exclusion\": \"E's build_exclusion() (FOLIO validation tasksource + refined, curated FOLIO/MALLS, MALLS-test, Logic-LM contexts/questions) + E's 700 sentences + E's 20 calibration sentences + E's 6 few-shot exemplars + every screen text + FOLIO-v2-train premises/conclusions (MALLS-test suppressed only for EXC pool b)\",\n  \"twelve_gram\": \"lowercase word-token 12-grams (E's norm()); drop any candidate sharing a 12-gram with any E sentence; within E2 keep only the first (E2 build order EXC -> L25 -> DT, sha1 order within) of two sentences sharing a 12-gram\"\n },\n \"selection_census\": {\n  \"seed_string\": \"E2_v1|\",\n  \"order\": \"sha1('E2_v1|' + sentence_id)\",\n  \"malls\": {\n   \"L25_supply_after_filters\": {\n    \"25-29\": 960,\n    \">=30\": 186,\n    \">=35\": 0\n   },\n   \"L25_targets\": {\n    \"base\": 350,\n    \"max_with_surplus\": 450,\n    \"base_long_short\": [\n     158,\n     192\n    ],\n    \"max_long_short\": [\n     186,\n     264\n    ]\n   },\n   \"L25_selected\": {\n    \"base\": 350,\n    \"surplus_reserve\": 98\n   },\n   \"EXC_pool_supply\": {\n    \"a_malls_train_core\": 0,\n    \"b_malls_test_noncurated_core\": 0,\n    \"c_malls_train_without\": 99,\n    \"d_but_not_nonxor\": 520\n   },\n   \"EXC_taken_per_pool\": {\n    \"a_malls_train_core\": 0,\n    \"b_malls_test_noncurated_core\": 0,\n    \"c_malls_train_without\": 92,\n    \"d_but_not_nonxor\": 8\n   },\n   \"EXC_type_counts\": {\n    \"without\": 92,\n    \"but_not\": 8\n   },\n   \"EXC_core_marker_share\": 0.0\n  },\n  \"dt\": {\n   \"primary_source\": \"opendatalab/ProverQA (dev easy/medium/hard)\",\n   \"hf_revision\": \"e2561beed450272690da658d21ae667570dbbafc\",\n   \"construction\": \"ProverGen: LLM-verbalised text over Prover9-validated FOL; nl2fol maps every context sentence to FOL\",\n   \"controlled_templates\": \"yes\",\n   \"license\": \"not stated on the HF card (the ProverGen GitHub repo is the reference; treat as research-use)\",\n   \"train_split\": \"train/provergen-5000.json is instruction-tuning format (system/instruction/input/output) with no nl2fol dict; not used\",\n   \"census_per_difficulty\": {\n    \"easy\": {\n     \"r1_ge15w_ge2c\": {\n      \"units\": 147,\n      \"skeletons\": 128\n     },\n     \"r2_ge12w_ge2c\": {\n      \"units\": 215,\n      \"skeletons\": 190\n     },\n     \"r3_ge15w_ge1c\": {\n      \"units\": 475,\n      \"skeletons\": 387\n     }\n    },\n    \"medium\": {\n     \"r1_ge15w_ge2c\": {\n      \"units\": 373,\n      \"skeletons\": 331\n     },\n     \"r2_ge12w_ge2c\": {\n      \"units\": 600,\n      \"skeletons\": 544\n     },\n     \"r3_ge15w_ge1c\": {\n      \"units\": 1212,\n      \"skeletons\": 1018\n     }\n    },\n    \"hard\": {\n     \"r1_ge15w_ge2c\": {\n      \"units\": 846,\n      \"skeletons\": 721\n     },\n     \"r2_ge12w_ge2c\": {\n      \"units\": 1398,\n      \"skeletons\": 1233\n     },\n     \"r3_ge15w_ge1c\": {\n      \"units\": 2187,\n      \"skeletons\": 1814\n     }\n    }\n   },\n   \"rung_taken\": {\n    \"r1_ge15w_ge2c\": 110\n   },\n   \"selected\": 110,\n   \"selected_base\": 100,\n   \"reserve\": 10,\n   \"distinct_skeletons_selected\": 110,\n   \"convention_flag_XOR_OR_source\": 2,\n   \"difficulty_counts\": {\n    \"ProverQA-dev-medium\": 32,\n    \"ProverQA-dev-hard\": 66,\n    \"ProverQA-dev-easy\": 12\n   },\n   \"secondary_census\": {\n    \"hitachi-nlp/FLD.v2\": \"not needed (ProverQA rung 1 alone exceeds 100 skeletons); abstract predicate symbols would make tier A impossible\",\n    \"tasksource/LogicNLI\": \"no FOL shipped (premise/hypothesis/label only) -> rejected\",\n    \"rejected_unverified_llm_gold\": [\n     \"ProofFOL (GPT-4o on ProofWriter)\",\n     \"NL2FOL (Lalwani 2024)\",\n     \"jhkim64/NL2FOL_sentence (7 downloads, FOLIO-overlapping LLM FOL)\",\n     \"MALLS-like corpora\"\n    ],\n    \"reason\": \"gold must be trusted by construction or audited\"\n   }\n  },\n  \"active_counts\": {\n   \"EXC\": 100,\n   \"L25\": 350,\n   \"DT\": 100\n  },\n  \"licences\": {\n   \"MALLS-v0.1\": \"CC-BY-NC-4.0 (yuan-yang/MALLS-v0)\",\n   \"ProverQA\": \"as stated on opendatalab/ProverQA (no licence field on the card)\"\n  }\n },\n \"selection_hashes\": {\n  \"work/pool_E2.json\": \"98cdccffa55226db6599c6b81b0228a667d4e805215e404f832edd9b776527f7\",\n  \"work/sentences.json (active base set)\": \"a056a0e8f17205d0a5540a57c1c62e7b78ade19beb3da5b43d4d7f8cc93134dc\"\n },\n \"pool_order\": {\n  \"EXC\": [\n   \"679fdea26cad\",\n   \"92cb8c181ca6\",\n   \"cc0419693c88\",\n   \"bf19b00949f8\",\n   \"455490393d95\",\n   \"3e00c6c48add\",\n   \"c8347d0542ba\",\n   \"e7bdc4b4fe9d\",\n   \"9c7a4557acb9\",\n   \"679570edc23d\",\n   \"656d5aee7ca2\",\n   \"41978924bbc9\",\n   \"56396143e920\",\n   \"74ce81615955\",\n   \"57c9d688367b\",\n   \"699cdd716bc4\",\n   \"a955bffc60c1\",\n   \"ceea02d5b915\",\n   \"716c963fbbde\",\n   \"749b55a36d7f\",\n   \"7deeb183ea5d\",\n   \"ddd89d871b74\",\n   \"ccec3f87204c\",\n   \"68294f495a62\",\n   \"5ab3f422164b\",\n   \"3f1b2750c7ae\",\n   \"30e18d8caa82\",\n   \"83aeedef5b0a\",\n   \"cf5b1bb534f7\",\n   \"65ce87bcda54\",\n   \"a0344dc5e50d\",\n   \"f8a331a52de0\",\n   \"95c32008fa38\",\n   \"624949c0569f\",\n   \"5b48ab13bbeb\",\n   \"be4ab6801ef5\",\n   \"639426eabf20\",\n   \"ac921224f9a2\",\n   \"37172550699d\",\n   \"8a091cfdb6dc\",\n   \"f7d2c32e7cf4\",\n   \"7f05c8875853\",\n   \"773c19411c34\",\n   \"f28e23d2f967\",\n   \"a94aa651b921\",\n   \"cfb73d3cf4cd\",\n   \"3ef9a14c85e2\",\n   \"fd0f4753b9c6\",\n   \"cef03058a69e\",\n   \"c5d3ee359d21\",\n   \"96ded0b5ea02\",\n   \"c6deaeb3d26a\",\n   \"db950e1e1337\",\n   \"c114a37c4590\",\n   \"c11ad480ede5\",\n   \"2ffac19e6136\",\n   \"b4a68566d74a\",\n   \"8074534c47ef\",\n   \"69693d9d8a34\",\n   \"9eb41fe4bb85\",\n   \"32ce72bc34e7\",\n   \"a55bfa1f8cd7\",\n   \"e7ed25cd912c\",\n   \"9686ae63c72d\",\n   \"a1216c1e6c98\",\n   \"522dac502174\",\n   \"338268269ffc\",\n   \"e9e72190bbad\",\n   \"461022795c96\",\n   \"d2d22855080d\",\n   \"5b5a3edbef06\",\n   \"936b3271f52d\",\n   \"37c5c49e5a10\",\n   \"60e59711265e\",\n   \"31645dc6f60c\",\n   \"828f9c8b8dcb\",\n   \"6b4b8517360c\",\n   \"974dd8eeb137\",\n   \"bfb17e03e594\",\n   \"51aa7ddfb437\",\n   \"5471d31e8d5d\",\n   \"fc0feef55e9c\",\n   \"3a8b872926c7\",\n   \"712d5eec665e\",\n   \"7e2f51fd2d15\",\n   \"4cb650fc350e\",\n   \"8deaff58620c\",\n   \"a1d9cf53485e\",\n   \"70209e2dff6c\",\n   \"ec4b76e571b6\",\n   \"c4c08bc10c14\",\n   \"6539476e0c2d\",\n   \"c97d841cc868\",\n   \"5982920a881b\",\n   \"a5d121b7d4fe\",\n   \"b12ba1a3c7d4\",\n   \"af02e81e3632\",\n   \"3d54deb0e329\",\n   \"a2b8567c19c5\",\n   \"1d951263f468\"\n  ],\n  \"L25\": [\n   \"ff1e71807b4d\",\n   \"f882dd4f2bad\",\n   \"9177c8fc41c7\",\n   \"3463d4d56a9f\",\n   \"33d2c6963321\",\n   \"4e80f520e8bc\",\n   \"7fe0445aeaaf\",\n   \"c41cc5adb9e6\",\n   \"9ef52fda67f0\",\n   \"bdd129e7249b\",\n   \"3d24fa9ee79e\",\n   \"3d036a3c648a\",\n   \"da9a2333586a\",\n   \"6f2d4c7ae4ce\",\n   \"73222a5f6b91\",\n   \"e61ddb3df6f2\",\n   \"b11111ca8561\",\n   \"726ddfd65fa9\",\n   \"23945b6b7c41\",\n   \"3f36e2dcc25f\",\n   \"fa011bac6a33\",\n   \"2db0390d9835\",\n   \"a55bf93a9afd\",\n   \"69545748bc88\",\n   \"9c8c7e8cd56c\",\n   \"69ce8d81e8fc\",\n   \"8f6b455b961f\",\n   \"f185ff47ba03\",\n   \"338d2dc17c19\",\n   \"6695f55148ea\",\n   \"bc3b9ffc19f3\",\n   \"c48499e82cf7\",\n   \"61d247d7403e\",\n   \"798263e94dbd\",\n   \"60d49b368db5\",\n   \"c68054c9e475\",\n   \"c68c2cc142ec\",\n   \"74933ffb4844\",\n   \"40c2aaa4765c\",\n   \"2704ad52af02\",\n   \"948b3708de29\",\n   \"d5a8c063b0ce\",\n   \"a8a794a098d4\",\n   \"2afc9e50d304\",\n   \"6f79ef272e91\",\n   \"2de10ce362ce\",\n   \"7f9c794f573b\",\n   \"a501dd027b88\",\n   \"247d1fe14de6\",\n   \"a36ad49a72ff\",\n   \"f3277a73bcf9\",\n   \"bd662fa3aa08\",\n   \"491a23154c13\",\n   \"f48bb3434c8a\",\n   \"8108ae029d93\",\n   \"4f6452956c37\",\n   \"e0f60c36994f\",\n   \"58220cb404cd\",\n   \"d9849801fbac\",\n   \"c4ff51c20320\",\n   \"43aa92af4ad3\",\n   \"71f64a239e68\",\n   \"f1071bc4bc76\",\n   \"9105a56452e5\",\n   \"881f995eab0f\",\n   \"47cb9a46e168\",\n   \"61ba3c2afb98\",\n   \"b8c170f14ce5\",\n   \"e5bb19fca72a\",\n   \"fdd600a5e637\",\n   \"d21311a9f36e\",\n   \"85ed3cbd9603\",\n   \"820619552035\",\n   \"943c6b3a6152\",\n   \"6979eb11fdbe\",\n   \"bc2cb5dd0933\",\n   \"93b23d92a82c\",\n   \"d012009e13b2\",\n   \"f1aaef678af9\",\n   \"8c4e83f06034\",\n   \"fff36b078fcc\",\n   \"7cc45b3f612a\",\n   \"e8fa54f087f4\",\n   \"9cf824311d9e\",\n   \"d4c3ae3bdf3d\",\n   \"e99fcf2f0d46\",\n   \"3a5f04295f7c\",\n   \"c7519f233666\",\n   \"d4d84d1a66d5\",\n   \"a1298a6ca63e\",\n   \"69d13e275a1a\",\n   \"f886f4eb9710\",\n   \"73158633f958\",\n   \"c7eae7108bbf\",\n   \"fc12e5383987\",\n   \"837508c851aa\",\n   \"e3ff16954f6f\",\n   \"94463f7c8904\",\n   \"a1a5bf76984b\",\n   \"9f388acc8807\",\n   \"f4adc7c85a41\",\n   \"8f1e48ea19fd\",\n   \"8a1b7ef983bd\",\n   \"339deae4612a\",\n   \"bfe7f1c1f5c3\",\n   \"83c11075058d\",\n   \"4113d7212dda\",\n   \"e25310b4238d\",\n   \"d3f8c4549b6c\",\n   \"bbe05140abc7\",\n   \"f1368b5d4fd5\",\n   \"bf9a38b53f2c\",\n   \"4bc9075e4d9d\",\n   \"8b266516e5f9\",\n   \"460968c0ce46\",\n   \"a6d43b31c956\",\n   \"21aa8063d8ac\",\n   \"2c012868e3ef\",\n   \"23eff1ec3bcb\",\n   \"424df6aa24dd\",\n   \"32c64d094fd4\",\n   \"59b25b8e9d56\",\n   \"239a3b2cd0ea\",\n   \"d69ecb4860ed\",\n   \"7f1ea003d7d1\",\n   \"ea740a4b7400\",\n   \"bb73f6fc0b45\",\n   \"e666243a05fa\",\n   \"6bf244654814\",\n   \"4713d84595c8\",\n   \"b3af9f7358db\",\n   \"c5861b036bb3\",\n   \"87650d8f72b8\",\n   \"c7de61e2c726\",\n   \"d1eb6a229d22\",\n   \"91fb46c4cf22\",\n   \"50ddc19070a7\",\n   \"ba99064269dd\",\n   \"8e857070f68c\",\n   \"d9ea03dacf4b\",\n   \"e8ff1a878801\",\n   \"9899e692a996\",\n   \"b445eea5c2a5\",\n   \"c6ca8173a878\",\n   \"abfed4fe7a3c\",\n   \"a8fc0b12e388\",\n   \"338e50dcb5b8\",\n   \"63a73e61111c\",\n   \"7e1b5fca9f28\",\n   \"b10e0b63f07b\",\n   \"7f634916374a\",\n   \"a23faa5d2a28\",\n   \"3621bd32bccf\",\n   \"2584645223ac\",\n   \"55d2d122dc93\",\n   \"80c15b71d4e2\",\n   \"b6646e245b71\",\n   \"5563cead1088\",\n   \"42d2243681d7\",\n   \"62428a3aed60\",\n   \"b4a6ba082e96\",\n   \"a7d156292e37\",\n   \"618af8b06ef6\",\n   \"7a3814b7bfeb\",\n   \"42ed3820630d\",\n   \"4b37661532dc\",\n   \"d52f5f9ada26\",\n   \"316dd0256011\",\n   \"cd5e2fd46ceb\",\n   \"721518b88b54\",\n   \"716c255c9136\",\n   \"8d0c50416766\",\n   \"482964e17177\",\n   \"634318676b5c\",\n   \"8179e857d260\",\n   \"e0897730b2da\",\n   \"7e42b2212ae9\",\n   \"51f5cffd048d\",\n   \"5556846c9176\",\n   \"fb804b22437f\",\n   \"3db47879ef0b\",\n   \"66d8825b2179\",\n   \"7a7fdf6e3e63\",\n   \"32fbb04668fb\",\n   \"e17e51a93df2\",\n   \"aa57efed5486\",\n   \"ca9cf6c7eb88\",\n   \"730c0f38ee73\",\n   \"c8f63c7b948b\",\n   \"5b86c29b7da4\",\n   \"ab21b4ca58b6\",\n   \"35ccca52a853\",\n   \"f820ee4ffbbb\",\n   \"337758fe265c\",\n   \"a44d4ac49417\",\n   \"ce20153687b7\",\n   \"300c68d0c84f\",\n   \"7fd014519579\",\n   \"c4ec6807415d\",\n   \"c0b14b516dbc\",\n   \"5b820147893d\",\n   \"46674ea78341\",\n   \"866a6dab6a10\",\n   \"418c08e20368\",\n   \"6abb9bc520aa\",\n   \"b465bf6c71bb\",\n   \"875410145813\",\n   \"9b08f3269c23\",\n   \"b8915795e542\",\n   \"27519ea97a20\",\n   \"55058612e806\",\n   \"694f35be91af\",\n   \"e29bbab8ebd5\",\n   \"f2571ced86d9\",\n   \"806f9da0740e\",\n   \"97f45f402b97\",\n   \"3794013c6e03\",\n   \"627373dff9e0\",\n   \"b56a006029c4\",\n   \"a2a9fc49eb7a\",\n   \"da61e6a916da\",\n   \"fb052bb8acf7\",\n   \"7556d59503ff\",\n   \"4e7550577f38\",\n   \"b9c6927d61d5\",\n   \"41ae28620aa2\",\n   \"b06755f873ed\",\n   \"e4a73cadec1f\",\n   \"a40ada7ead08\",\n   \"d53fbf746269\",\n   \"d48dd0b77ce4\",\n   \"900279896ee6\",\n   \"a184c6c63e58\",\n   \"a27622772fbc\",\n   \"ea421970f175\",\n   \"83f26fde5007\",\n   \"d6f47a5cdf38\",\n   \"b6af82484b6f\",\n   \"ee077346ede9\",\n   \"75f4f8242ac0\",\n   \"a653e89b70c4\",\n   \"b39fe39b989b\",\n   \"a0439529035f\",\n   \"e0b53d893013\",\n   \"e2437b6b08f5\",\n   \"c89ddc7228a2\",\n   \"78545e0969fa\",\n   \"fd9553d08f72\",\n   \"7540fc8d688f\",\n   \"ec2c63f5f5df\",\n   \"f50f53df22e7\",\n   \"ec6d25de306e\",\n   \"b03b41f97fba\",\n   \"7b4719388b84\",\n   \"f0a0b74a8bef\",\n   \"efb5ba35249c\",\n   \"7abeeaeee6b8\",\n   \"9d6f81e2fe41\",\n   \"97d240ae2bc5\",\n   \"a27c53f92d8d\",\n   \"f1167a083d6c\",\n   \"696816eaa716\",\n   \"e4b42110232a\",\n   \"e892707fc2d0\",\n   \"6be7670b7e0d\",\n   \"e861423f772f\",\n   \"8210a1fc39b3\",\n   \"a0ece7034932\",\n   \"ce2c0bde16ce\",\n   \"e3caa00ee67e\",\n   \"73c4030b28e9\",\n   \"7f5c28ec674e\",\n   \"cb91858a2368\",\n   \"f43528fb0682\",\n   \"bba693ccbe05\",\n   \"c1dc10ed162f\",\n   \"9c69df07ad2a\",\n   \"e2084eb1c305\",\n   \"794c59fb80e2\",\n   \"92445624d206\",\n   \"df993e7463f7\",\n   \"e27cd0978843\",\n   \"deaff2688453\",\n   \"fdbe46ba29fb\",\n   \"fb358ff36d01\",\n   \"7196a07ef021\",\n   \"81bd648e9294\",\n   \"d884082c8614\",\n   \"aabf2fd1221a\",\n   \"ed572a25c3d9\",\n   \"9b6037773cb4\",\n   \"8a074590c2df\",\n   \"8e38eb065c7a\",\n   \"bab8704e84fd\",\n   \"b569ff6ac37b\",\n   \"d26b836d1252\",\n   \"a44232a85c05\",\n   \"978313d5cff7\",\n   \"967629174c01\",\n   \"7f22d6ab60bb\",\n   \"a9561aa95ad4\",\n   \"f188728583de\",\n   \"66ca52628c53\",\n   \"62a07bdd4b4f\",\n   \"734dec522be8\",\n   \"f0d55485e39b\",\n   \"7634b8b627d2\",\n   \"b2e1e9894525\",\n   \"e54c4caa444d\",\n   \"b820a9243e3a\",\n   \"9f02db778313\",\n   \"e423dc920a8d\",\n   \"924e59223af3\",\n   \"c841aa916110\",\n   \"c9f015cfd286\",\n   \"7b7a07a21e27\",\n   \"6529f5c3dabb\",\n   \"d110272c7a6c\",\n   \"c0e65f5ae09c\",\n   \"82bda00edf79\",\n   \"7f5eddcef5e1\",\n   \"bc452c66a3da\",\n   \"f78206a1cd5d\",\n   \"d2fd7c8c51b8\",\n   \"dbafea01b477\",\n   \"8ea44b9aef2c\",\n   \"bf4c7f6a7cd8\",\n   \"7009b5a974c9\",\n   \"95be7b04daef\",\n   \"66235c801253\",\n   \"ea16f7ecb79f\",\n   \"9c755b61bb57\",\n   \"f9e249c55331\",\n   \"dacfc8528754\",\n   \"7f8ca689ea58\",\n   \"8eb7ef91b7bb\",\n   \"6c9b8220d61d\",\n   \"8dd238d6dfa8\",\n   \"c48939494f53\",\n   \"c5d72a3c6f35\",\n   \"c8597dd9110e\",\n   \"a50b38594311\",\n   \"f62ddbefcdf0\",\n   \"688a8ccc781a\",\n   \"8a27819cb4a4\",\n   \"68e6737b41c5\",\n   \"e372907648a1\",\n   \"69918aa59fa6\",\n   \"d6ab8c2487da\",\n   \"973bf22ce342\",\n   \"8aa5f5b1d587\",\n   \"21b6660985d0\",\n   \"8c9d38b9f425\",\n   \"9b86817890f9\",\n   \"8f5e945b2e1a\",\n   \"ee71965dd0e0\",\n   \"d85c00a71ca6\",\n   \"a086592805d3\",\n   \"834fa79e0feb\",\n   \"9562457bf9ba\",\n   \"c7fa4e6df756\",\n   \"8cf79c5478b5\",\n   \"ff56130e5ce7\",\n   \"4702a571d169\",\n   \"fa19e24c2234\",\n   \"26c9a2f51c57\",\n   \"ef38d500e385\",\n   \"f39462b1d1be\",\n   \"6baee5b3db50\",\n   \"7e9b2921b477\",\n   \"2e1f4a61147b\",\n   \"e7181957f426\",\n   \"6b9619d21706\",\n   \"b6777d043d54\",\n   \"e79d4aa3b5ee\",\n   \"ba60c60c535d\",\n   \"7b4200dc0cb6\",\n   \"8812c6a3534b\",\n   \"ed33bf7d3aaf\",\n   \"f91400b6f9fe\",\n   \"d9cf96cabd16\",\n   \"db6327912f05\",\n   \"58a808d7eddf\",\n   \"7afdd1854682\",\n   \"cc55e1857330\",\n   \"c3a6e80f2ead\",\n   \"cf784ef5fe9b\",\n   \"945d0b8bc605\",\n   \"72623a4283eb\",\n   \"b47809411217\",\n   \"80e4d740e800\",\n   \"faef242f5681\",\n   \"aa73a1bc46e9\",\n   \"c3af16c4c689\",\n   \"b120882326b3\",\n   \"e69080b6df7f\",\n   \"9d09ac0ac586\",\n   \"edf026cc8456\",\n   \"5e95c771b375\",\n   \"a437a09c343d\",\n   \"d7e97135879a\",\n   \"e7f0e25f2f51\",\n   \"365853da29c9\",\n   \"bf7967043e7a\",\n   \"5c68f7c70add\",\n   \"bd0d20c7fbd9\",\n   \"b8bf9522ac0d\",\n   \"cc90177a393e\",\n   \"695b7dd416c5\",\n   \"bea7679d8db2\",\n   \"e01452b28dca\",\n   \"6c7f80d70d29\",\n   \"dac71cfe8507\",\n   \"42cea09b4bdf\",\n   \"a0fefbd39f65\",\n   \"335a1c170ffb\",\n   \"e60a50dbfd04\",\n   \"9e50780e7a93\",\n   \"eb982919b01c\",\n   \"4c30c3b7283b\",\n   \"dd8206537a2c\",\n   \"98791709b852\",\n   \"abb7374efbb7\",\n   \"d25ff5c150e2\",\n   \"ace2ef95abc7\",\n   \"5e7c1e82d798\",\n   \"d5f153d1a766\",\n   \"e83c0c0aea82\",\n   \"b84e1771cf4f\",\n   \"9b27ceb243ce\",\n   \"b7be8928255b\",\n   \"dde658e490a6\",\n   \"72ec77fb15c3\",\n   \"a148ed05a4ca\",\n   \"99f0232b6d0f\",\n   \"f4b782bbd3d7\",\n   \"d17ddcf5a836\",\n   \"6ab02409c3b0\",\n   \"d8d50e90e81f\",\n   \"ab96b3b35d88\",\n   \"7c3f2e6c8d6c\",\n   \"7cdd373fb429\",\n   \"70f4ff13e17a\",\n   \"a85b1b57aa88\",\n   \"ad5b97f9f174\",\n   \"f66ce364e8f4\",\n   \"a3fe21cf1b2e\",\n   \"63feb99a5f93\"\n  ],\n  \"DT\": [\n   \"b91115ec794d\",\n   \"d244e72c0a26\",\n   \"e591dc2a10ff\",\n   \"93572dc919de\",\n   \"0a0642b820c2\",\n   \"e3a85804325a\",\n   \"2cab5a3f9e56\",\n   \"cfea0d703552\",\n   \"499634c702ca\",\n   \"30bc4c2707a1\",\n   \"b54a15c813dc\",\n   \"fac59476f67e\",\n   \"13a64af0537c\",\n   \"8e1c584d83fc\",\n   \"8f924891bc72\",\n   \"f43fb10cdef5\",\n   \"f8b0ce7af03e\",\n   \"004b883b4230\",\n   \"2318760c4ed9\",\n   \"82f904208d42\",\n   \"9dc93f7033d3\",\n   \"78c5688fc307\",\n   \"1e808ec3e15a\",\n   \"77151839d606\",\n   \"48133a75dbf7\",\n   \"468a0153f52e\",\n   \"eb3920345933\",\n   \"dca082d127e1\",\n   \"e5c8c52c2cdc\",\n   \"ada9d2de30e4\",\n   \"f6dd60aada7d\",\n   \"dedb97b85923\",\n   \"0374d7a0773a\",\n   \"726a83553b32\",\n   \"19076adeb5b3\",\n   \"b40fcef53861\",\n   \"56d3fad93d4d\",\n   \"7e323b857d78\",\n   \"033599b7fc61\",\n   \"535f7d70a400\",\n   \"0df228570ea8\",\n   \"f258cb73c087\",\n   \"6cfe8fd89ded\",\n   \"75c1daa3b223\",\n   \"bc30bb6c0875\",\n   \"5276c852ec18\",\n   \"468f1adb8802\",\n   \"73b80c0b5213\",\n   \"22aa22af6809\",\n   \"1b608b490f76\",\n   \"ba657893abce\",\n   \"61575cb71036\",\n   \"b754f1480a20\",\n   \"3bc986fa1a6a\",\n   \"f2277b67ff2f\",\n   \"62d79a2f705b\",\n   \"cca3f7f5a8f4\",\n   \"1af923105ccc\",\n   \"93f5bcbfec75\",\n   \"9388d5a8be92\",\n   \"a445674e9eda\",\n   \"1c5eec03425b\",\n   \"30ea9964b5e3\",\n   \"2b904e468437\",\n   \"b56407e95e50\",\n   \"b2b61e218e75\",\n   \"bb69764d36eb\",\n   \"e4cb724f4f14\",\n   \"f87ae5655264\",\n   \"fef10283a726\",\n   \"ddd9456210fa\",\n   \"7232cc09803c\",\n   \"18b47638853b\",\n   \"808d2a9e8129\",\n   \"5e4c286a5fe5\",\n   \"808083289048\",\n   \"77d038e177f2\",\n   \"695cb337747b\",\n   \"836026fd7db7\",\n   \"a79302c8997c\",\n   \"1f6405877d5b\",\n   \"33bc871f2bb0\",\n   \"255df98a87c5\",\n   \"08c0f477363c\",\n   \"bd2c935f35d2\",\n   \"73f59874a64e\",\n   \"dbe1917d5166\",\n   \"541025e083c6\",\n   \"513a0bacef6d\",\n   \"e2e1439cad08\",\n   \"5ef1e8888b58\",\n   \"03cbc6b626c0\",\n   \"e1f83c03b065\",\n   \"b66e74275122\",\n   \"5f2dcb2818d7\",\n   \"1d393f168d7c\",\n   \"8d165e3b475f\",\n   \"425f2ba5dda5\",\n   \"fd5d70920117\",\n   \"5db02149d570\",\n   \"d2e015d4d274\",\n   \"f61492aeea9c\",\n   \"49880f94baf4\",\n   \"17422629ac07\",\n   \"4643ba0b28ec\",\n   \"6f92046a1cd9\",\n   \"1d7709a71173\",\n   \"e34f2a33f33a\",\n   \"453efdce133b\",\n   \"ca29036391cd\"\n  ]\n },\n \"generator_slots\": {\n  \"G1\": {\n   \"model\": \"meta-llama/llama-3.1-8b-instruct\",\n   \"family\": \"meta\",\n   \"params\": {}\n  },\n  \"G1b\": {\n   \"model\": \"meta-llama/llama-3.3-70b-instruct\",\n   \"family\": \"meta\",\n   \"params\": {}\n  },\n  \"G2\": {\n   \"model\": \"qwen/qwen3-235b-a22b-2507\",\n   \"family\": \"qwen\",\n   \"params\": {}\n  },\n  \"G3\": {\n   \"model\": \"mistralai/mistral-small-3.2-24b-instruct\",\n   \"family\": \"mistral\",\n   \"params\": {}\n  },\n  \"G4\": {\n   \"model\": \"deepseek/deepseek-v3.2\",\n   \"family\": \"deepseek\",\n   \"params\": {\n    \"reasoning\": {\n     \"enabled\": false\n    }\n   }\n  },\n  \"G5\": {\n   \"model\": \"google/gemma-3-27b-it\",\n   \"family\": \"google-gemma\",\n   \"params\": {}\n  },\n  \"G6\": {\n   \"model\": \"microsoft/phi-4\",\n   \"family\": \"microsoft\",\n   \"params\": {}\n  },\n  \"G7\": {\n   \"model\": \"openai/gpt-4.1-mini\",\n   \"family\": \"openai\",\n   \"params\": {}\n  },\n  \"G8\": {\n   \"model\": \"google/gemini-2.5-flash\",\n   \"family\": \"google-gemini\",\n   \"params\": {\n    \"reasoning\": {\n     \"max_tokens\": 0\n    }\n   }\n  },\n  \"G9\": {\n   \"model\": \"cohere/command-r7b-12-2024\",\n   \"family\": \"cohere\",\n   \"params\": {}\n  }\n },\n \"generation\": {\n  \"prompt\": \"prompts/fewshot_v1.txt (verbatim, E)\",\n  \"prompt_sha1\": \"a1c7ae39f13979a96e6b360f8d3164735c334d80\",\n  \"temperature\": 0.0,\n  \"max_tokens\": 600,\n  \"variants\": [\n   \"fewshot_v1\"\n  ],\n  \"excluded\": \"no zero-shot rows, no GPT-5.1 frontier slot, no ccg2lambda\"\n },\n \"slot_unavailability_rule\": \"a model id no longer served is replaced by the same family's nearest current instruct model, logged and flagged slot_substituted=true; a family is never swapped. At freeze time all 10 slot ids and all 3 panel ids are served (work/models_snapshot_E2.json).\",\n \"labeller_sha256\": {\n  \"src/assemble.py\": \"1235c92b8f2bc21ab4218f1eb1d118071ad9876b8ebaf68a91502e55a328bd4a\",\n  \"src/calibration.py\": \"9c95f6d4a90f702ad7851863c4d5a8ab6cf3593ead5f7947ad8c827e1bcf5a9c\",\n  \"src/card.py\": \"762768ed489fc53b734caa681a7b97a4de967df3b63bbdfad34491022823e185\",\n  \"src/extend_labels.py\": \"7cdbeebf5f6240418cee7892ce4405248fb6254c6de6d0390fc8b9eb167a72a6\",\n  \"src/gate.py\": \"861ce080463cac27480c96eea4e11afb9360fe067140256b5017aac3c70276e4\",\n  \"src/generate.py\": \"9b5dd7120704c2000740a2c4632cd261407caff9ae37e16e27919b54fe679749\",\n  \"src/label_worker.py\": \"cf45e8934a3e7c785d37deed8263e001535fe30dbfb491b21bbcc402d4831e19\",\n  \"src/normalise.py\": \"d45fa8620934bbeee0c7c65e9fecba117a1d713fb58ad21006012b4b76420b5c\",\n  \"src/or_client.py\": \"35fbfa92f6a89c7f06e0bedb773abcc908f53773804a56c85317f3e6f7310bc9\",\n  \"src/panel.py\": \"4d07e0dc4d60209a9aa7d0f580c908c3ae7172600ab0a7ba857e97e026b27e6f\",\n  \"src/panel_run.py\": \"7a4ce4655b262aba5471023397c22bb4548827c57e323eeda15774ad19b6103a\",\n  \"src/repair_refs.py\": \"e128cf83405b21d623854f78ae07b9df6ec71ab1bdd04fab01f0ef2bfe9ca82b\",\n  \"src/run_label.py\": \"2eabd1c5e4e71eb1360d1c418aeb0159a8c7e51140128d09f298dc3081ba400e\",\n  \"src/screen.py\": \"e034bae16858948124d468e28bd01afe8a558e16ffc19be5512e272e7a5f5af8\",\n  \"src/select_sentences.py\": \"141ec601d6f84725414f82382b8d619e617b3f1b0911b192ef0d291fcddc4e89\",\n  \"src/select_topup.py\": \"b01d189b61e0cefe3d681b9ec147d8fa2f00e727de2d3c6ba62950360ba2f13b\",\n  \"src/stats.py\": \"8a90b47bf7923bf027780ac64eb6fb5e3542c93a4bbf56df0d5a0d412079bdf6\",\n  \"labeller/complexity_counts.py\": \"0461afd2f34a399181839d4d3463ad88d3976a0aaf172907c938f35fd30467fc\",\n  \"labeller/disguise.py\": \"b5afe3163c964841dc50ce0ca57e41828c9193658b42adeb39afafc4967eb893\",\n  \"labeller/fol.py\": \"e37a655f98af4899b1bdee943c66b395b27847870d6788b5509cf92ef3f95fe4\",\n  \"labeller/label_lib.py\": \"f3047b2e49b8c5a9cd6c57cb474ca32333ae1606acbd2c489d6a3f8bc400d8a1\",\n  \"labeller/lint_smells.py\": \"bf353d291adb640010adec1557ec0ac1a924300faf91a041fa249f8efbb14e83\",\n  \"labeller/repair_census.py\": \"64fdb06b4c2abc5ae3d5f8debe143d63fcbbb1b7f72f1da09bf39c98f095774f\",\n  \"labeller/repair_census.rows.json\": \"8e8dc86c6e8936e9434a252d3cef6670bb2aecd62aabd4d5c780f912d0a47d0d\"\n },\n \"code_freeze_sha256\": \"986334dc05d1c2be2543b010ba3ed072236d75c89ff52b174cd800669a2d706d\",\n \"panel\": {\n  \"P1\": {\n   \"model\": \"anthropic/claude-haiku-4.5\",\n   \"family\": \"anthropic\",\n   \"params\": {\n    \"temperature\": 0.0,\n    \"max_tokens\": 1500\n   }\n  },\n  \"P3\": {\n   \"model\": \"z-ai/glm-4.6\",\n   \"family\": \"zhipu\",\n   \"params\": {\n    \"temperature\": 0.0,\n    \"max_tokens\": 1500,\n    \"reasoning\": {\n     \"enabled\": false\n    }\n   }\n  },\n  \"R1\": {\n   \"model\": \"moonshotai/kimi-k2-0905\",\n   \"family\": \"moonshot\",\n   \"params\": {\n    \"temperature\": 0.0,\n    \"max_tokens\": 1500\n   }\n  },\n  \"production_prompt_sha1\": \"0b5ffbb951ec3d5489bb64812387b064354cc905\",\n  \"design\": \"disguised (labeller/disguise.py), blind, shuffled, <=8 formulas per call; stage 1 = P3+R1 on every class of every sentence (full class coverage on all E2 strata, as E did for its MALLS strata); stage 2 = P1 only where P3/R1 disagree or a vote is missing; pilot = all three raters (as E's 5c pilot)\",\n  \"cache\": \"fresh work/panel_cache.jsonl in this workspace (no reply cached for E can be served; E's cache file is never read by the panel code)\"\n },\n \"tier_rules_verbatim_from_E_card_section_2\": \"## 2. Final label rule (plan 5f, verbatim; `src/assemble.py::final_rule`)\\n- auto CORRECT (plain z3 EQ to the reference) → final CORRECT, tier A. Panel dissent is logged as panel false-alarm evidence.\\n- auto ERROR(ops) → final ERROR(ops), tier A, unless ≥2/3 panel models say faithful → CONTESTED (a likely convention,\\n  aligner or reference issue; convention_flags are recorded).\\n- auto VOCAB_GRAN → panel majority: faithful → CORRECT (correct_not_equivalent=true, tier B); unfaithful →\\n  ERROR('MEANING_RENAME' + panel ops, tier B).\\n- auto COMPOUND or TIMEOUT_UNKNOWN → panel majority: unfaithful → ERROR('COMPOUND', panel ops, tier B); faithful → CORRECT\\n  (correct_not_equivalent=true, tier B).\\n- If the panel majority flags the sentence AMBIGUOUS, add reading_choice=true and keep it out of primary pooling, as a\\n  separate class.\\n- A missing vote (a model failed) with a 1-1 split → CONTESTED.\\n- UNPARSEABLE → final UNPARSEABLE, kept in the denominator.\\n- NO_TRUSTED_REFERENCE or DISPUTED_REFERENCE → final = panel majority, tier C (secondary only).\\n\\nPrimary analyses use tiers A+B, exclude CONTESTED (and reading_choice rows), and report sensitivity with CONTESTED counted\\nas CORRECT and as ERROR.\\n\\n**Implementation details that matter for users:**\\n1. **Class collapse.** Per sentence, candidates are union-found into classes modulo vocabulary (`equivalent_modulo_vocab`).\\n   The panel judges one representative per class (disguised, blind, shuffled), and the label propagates to the members.\\n   - The reference class c0 is shown unlabelled among the candidates, so the gold audit is blind.\\n   - A candidate that joined c0 only modulo vocabulary or granularity (auto VOCAB_GRAN) is shown to the panel **as its own\\n     item** (`metadata_panel_item` = `<sid>:vg:<hash>`). A vote on the reference itself cannot tell whether the renaming\\n     preserved meaning.\\n2. **Panel design (budget-driven, label-preserving).** GLM-4.6 (P3) and Kimi-K2-0905 (R1) judge every shown item. Haiku-4.5\\n   (P1) judges only the items where they disagree or a vote is missing, plus the reference item when only the\\n   sentence-level ambiguity flag is split. Because P1 is only needed when the other two disagree, the 2-of-3 majority is the\\n   same as a full 3-vote majority. What is lost is a 3-rater κ on all items; it is reported on the 30-sentence pilot, which\\n   all three judged.\\n   - Why: the full 3-model pass was projected at $7.6 against about $6.3 of remaining budget.\\n   - Adjudicator calls see fewer items than a full call (a mild format difference from the gate).\\n3. **CTRL scope (plan 5c fallback).** For CTRL, a 20% sha1 sample of sentences gets full class coverage. For the rest, the\\n   panel sees the reference class plus all VOCAB_GRAN/COMPOUND/TIMEOUT classes. Their auto-ERROR classes keep the solver\\n   label (tier A, `label_source=solver`, no CONTESTED routing). MALLS strata (L25/L20/EXC) have full coverage.\\n   `metadata_panel_scope` records which applies.\\n4. **Reference audit and repair.**\\n   - MALLS gold with ≥2 unfaithful votes = GOLD_WRONG.\\n   - The panel models then write their own FOL for the original, undisguised sentence with the few-shot generation prompt.\\n     GLM and Kimi go first; Haiku is called only when those two are not mutually equivalent modulo vocabulary. The raw\\n     outputs are in `raw/reference_repair.jsonl`.\\n   - If ≥2 formulas are mutually equivalent modulo vocabulary, the one with the fewest atoms becomes the reference\\n     (PANEL_REPAIRED), and all rows are re-labelled by the solver against it (`work/labels_heldout_repaired.jsonl`).\\n     Otherwise the status is NO_TRUSTED_REFERENCE (tier C).\\n   - Caveat: a panel-written reference comes from the same families that judge the rows.\\n   - CTRL references judged unfaithful are DISPUTED_REFERENCE (tier C).\\n   - Panel votes on candidate classes are reference-free, so they stay valid after a repair.\\n\\n\",\n \"testability_rule_verbatim_from_E\": \"A stratum is TESTABLE only if, using tier A+B final labels only (CONTESTED excluded), it has >=50 ERROR rows AND >=50 CORRECT rows AND >=25 distinct sentences contributing ERROR rows AND >=25 distinct sentences contributing CORRECT rows. Declared per stratum after labelling, before any metric runs.\",\n \"testability_application_E2\": \"LLM systems only (gold-as-system rows excluded), tiers A+B, CONTESTED and reading_choice excluded; applied to regimes R_AB (primary), R_A (tier A only) and R_VEX (tier A+B rows whose candidate (name, arity) symbol set is a subset of the reference's; no rename step)\",\n \"drift_check_stop_rule\": \"replay E's 77 synthetic gate items and the 96 track-H expert pairs with today's P1/P3/R1, the v2 prompt and the fresh cache. If majority agreement with E's STORED votes is < 0.85, or a panel model id is no longer served, the panel is NOT used for E2: tier A against UNAUDITED gold only (reference_status UNAUDITED_GOLD_DRIFT_STOP), every non-EQ auto class stays UNRESOLVED, and the card marks E2 'tier-A-only confirmation'.\",\n \"budget\": {\n  \"hard_cap_usd\": 9.5,\n  \"phase_caps_usd\": {\n   \"drift (gate + gate_trackh)\": 0.8,\n   \"pilot\": 0.6,\n   \"generation\": 1.3,\n   \"panel stage 1 (panel_heldout)\": 4.6,\n   \"adjudication (panel_heldout_adj)\": 1.9,\n   \"reference repair\": 1.0\n  },\n  \"note\": \"pilot calls are booked under the production phase names (generation / panel_heldout / panel_heldout_adj / reference_repair) because the frozen scripts are used; pilot spend is reported separately by sentence id\"\n },\n \"shrink_order\": \"EXC -> 75, then L25 -> 300 (floor); DT never below 100\",\n \"surplus_rule\": \"if the pilot projection is <= $8.0, add L25 sentences from the pre-registered surplus order (pool_order.L25 after the first 350) until projected spend = $8.6, up to L25 = 450. Pilot data inform COST only.\",\n \"vex_flag\": \"new additive helper src_e2/vex.py: set(normalised (name, arity) of candidate predicates+constants) subset-of set(reference's), no rename step; vex_eq = plain z3 equivalence (no alignment). Changes no label.\",\n \"controls\": \"up to 300 final-CORRECT LLM rows (tier A first, then tier B), spread over strata, sha1 order; RENAME_SYN and RENAME_NONCE via dataset 3's perturb.control_rename; z3-verified under the inverse map; separate fold, never in R_AB pools\",\n \"seal\": \"sealed/labels_E2.jsonl + sealed/references_E2.jsonl separated from candidates_E2_nolabels.jsonl (no label, no reference, no gold-as-system row) and controls_E2_nolabels.jsonl; seal.json with sha256s; verify_seal.py scans for forbidden keys and reference strings\",\n \"deviations_known_at_freeze\": [\n  {\n   \"id\": \"D0\",\n   \"what\": \"or_client.py base-URL transport fix\",\n   \"effect\": \"none on labels\"\n  },\n  {\n   \"id\": \"D1\",\n   \"what\": \"src_e2/compat.py makes E's MALLS-only branches (gold row as a system, blind gold audit counted as GOLD_WRONG, reference repair) apply to the ProverQA DT gold, as the plan requires ('MALLS gold and ProverQA gold get the same audit'). E's code is unmodified; the shim wraps the source string.\",\n   \"effect\": \"DT sentences get the MALLS treatment instead of E's CTRL treatment (DISPUTED_REFERENCE)\"\n  },\n  {\n   \"id\": \"D2\",\n   \"what\": \"E's code is copied to ./src and ./labeller (not ./src_E) because its ROOT-relative paths require that layout; E2 wrappers live in ./src_e2\",\n   \"effect\": \"none\"\n  },\n  {\n   \"id\": \"D3\",\n   \"what\": \"EXC core-marker supply is exhausted: pools (a) and (b) are empty (E took all 67 MALLS-train core items; MALLS-test has only 3 core-marker items, all excluded). EXC = 'without' + non-XOR 'but not' items; core-marker share 0.0. Fallback (iv): keep EXC, never borrow E sentences.\",\n   \"effect\": \"EXC on E2 is about weaker exception constructions; the EXC-core testability row is empty by construction\"\n  }\n ],\n \"power_statement_corrected\": \"From E's L25 numbers the stratified dAUROC CI half-width was 0.085 at 300 sentences (SE ~0.043, SE ~ 1/sqrt(sentences with both classes)). Detecting d=0.08 at 80% power needs SE <= 0.0286, about 690 L25 sentences at E's yield. 350 L25 sentences give MDE80 ~0.11; 450 give ~0.10. The direction's claim that ~400 L25 sentences detect +0.08 is wrong.\",\n \"success_criterion_DT\": \"positive sign only (transfer check on a different, templated register)\"\n}", "numLines": 1027, "startLine": 1, "totalLines": 1027}}
```

### [12] TOOL CALL — Read · 2026-09-24 10:58:34 UTC

```
/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/census_E2.json
```

### [13] TOOL RESULT — Read · 2026-09-24 10:58:34 UTC

```
{"type": "text", "file": {"filePath": "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/census_E2.json", "content": "{\n \"seed_string\": \"E2_v1|\",\n \"order\": \"sha1('E2_v1|' + sentence_id)\",\n \"malls\": {\n  \"L25_supply_after_filters\": {\n   \"25-29\": 960,\n   \">=30\": 186,\n   \">=35\": 0\n  },\n  \"L25_targets\": {\n   \"base\": 350,\n   \"max_with_surplus\": 450,\n   \"base_long_short\": [\n    158,\n    192\n   ],\n   \"max_long_short\": [\n    186,\n    264\n   ]\n  },\n  \"L25_selected\": {\n   \"base\": 350,\n   \"surplus_reserve\": 98\n  },\n  \"EXC_pool_supply\": {\n   \"a_malls_train_core\": 0,\n   \"b_malls_test_noncurated_core\": 0,\n   \"c_malls_train_without\": 99,\n   \"d_but_not_nonxor\": 520\n  },\n  \"EXC_taken_per_pool\": {\n   \"a_malls_train_core\": 0,\n   \"b_malls_test_noncurated_core\": 0,\n   \"c_malls_train_without\": 92,\n   \"d_but_not_nonxor\": 8\n  },\n  \"EXC_type_counts\": {\n   \"without\": 92,\n   \"but_not\": 8\n  },\n  \"EXC_core_marker_share\": 0.0\n },\n \"dt\": {\n  \"primary_source\": \"opendatalab/ProverQA (dev easy/medium/hard)\",\n  \"hf_revision\": \"e2561beed450272690da658d21ae667570dbbafc\",\n  \"construction\": \"ProverGen: LLM-verbalised text over Prover9-validated FOL; nl2fol maps every context sentence to FOL\",\n  \"controlled_templates\": \"yes\",\n  \"license\": \"not stated on the HF card (the ProverGen GitHub repo is the reference; treat as research-use)\",\n  \"train_split\": \"train/provergen-5000.json is instruction-tuning format (system/instruction/input/output) with no nl2fol dict; not used\",\n  \"census_per_difficulty\": {\n   \"easy\": {\n    \"r1_ge15w_ge2c\": {\n     \"units\": 147,\n     \"skeletons\": 128\n    },\n    \"r2_ge12w_ge2c\": {\n     \"units\": 215,\n     \"skeletons\": 190\n    },\n    \"r3_ge15w_ge1c\": {\n     \"units\": 475,\n     \"skeletons\": 387\n    }\n   },\n   \"medium\": {\n    \"r1_ge15w_ge2c\": {\n     \"units\": 373,\n     \"skeletons\": 331\n    },\n    \"r2_ge12w_ge2c\": {\n     \"units\": 600,\n     \"skeletons\": 544\n    },\n    \"r3_ge15w_ge1c\": {\n     \"units\": 1212,\n     \"skeletons\": 1018\n    }\n   },\n   \"hard\": {\n    \"r1_ge15w_ge2c\": {\n     \"units\": 846,\n     \"skeletons\": 721\n    },\n    \"r2_ge12w_ge2c\": {\n     \"units\": 1398,\n     \"skeletons\": 1233\n    },\n    \"r3_ge15w_ge1c\": {\n     \"units\": 2187,\n     \"skeletons\": 1814\n    }\n   }\n  },\n  \"rung_taken\": {\n   \"r1_ge15w_ge2c\": 110\n  },\n  \"selected\": 110,\n  \"selected_base\": 100,\n  \"reserve\": 10,\n  \"distinct_skeletons_selected\": 110,\n  \"convention_flag_XOR_OR_source\": 2,\n  \"difficulty_counts\": {\n   \"ProverQA-dev-medium\": 32,\n   \"ProverQA-dev-hard\": 66,\n   \"ProverQA-dev-easy\": 12\n  },\n  \"secondary_census\": {\n   \"hitachi-nlp/FLD.v2\": \"not needed (ProverQA rung 1 alone exceeds 100 skeletons); abstract predicate symbols would make tier A impossible\",\n   \"tasksource/LogicNLI\": \"no FOL shipped (premise/hypothesis/label only) -> rejected\",\n   \"rejected_unverified_llm_gold\": [\n    \"ProofFOL (GPT-4o on ProofWriter)\",\n    \"NL2FOL (Lalwani 2024)\",\n    \"jhkim64/NL2FOL_sentence (7 downloads, FOLIO-overlapping LLM FOL)\",\n    \"MALLS-like corpora\"\n   ],\n   \"reason\": \"gold must be trusted by construction or audited\"\n  }\n },\n \"active_counts\": {\n  \"EXC\": 100,\n  \"L25\": 350,\n  \"DT\": 100\n },\n \"licences\": {\n  \"MALLS-v0.1\": \"CC-BY-NC-4.0 (yuan-yang/MALLS-v0)\",\n  \"ProverQA\": \"as stated on opendatalab/ProverQA (no licence field on the card)\"\n }\n}", "numLines": 129, "startLine": 1, "totalLines": 129}}
```

### [14] TOOL CALL — Glob · 2026-09-24 10:58:34 UTC

```
Pattern: "{src_e2/*,*.md,*.json,*.sh,sealed/*}"
```

### [15] TOOL RESULT — Glob · 2026-09-24 10:58:34 UTC

```
{"filenames": ["/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/.aii_claude_session.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/code_freeze.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/src_e2/probe.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/src_e2/select_e2.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/exclusion_log_E2.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/census_E2.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/src_e2/e.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/src_e2/compat.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/src_e2/prereg_e2.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/prereg_E2.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/src_e2/gen_retry.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/src_e2/vex.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/src_e2/repair.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/src_e2/key_poll.sh", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/src_e2/drift_report.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/panel_drift_E2.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/src_e2/assemble_e2.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/src_e2/controls_e2.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/src_e2/testability_e2.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/testability_E2.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/src_e2/seal_e2.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/src_e2/verify_seal.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/seal.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/sealed/references_E2.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/sealed/labels_E2.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/src_e2/run_all.sh", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/src_e2/activate_full.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/src_e2/card_e2.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/restore.sh", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/src_e2/pilot_projection.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/pilot_projection.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/preview_data_out.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/mini_data_out.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/full_data_out.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/dataset_card.md", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/reproducibility.md", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/README.md", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/.terminal_claude_agent_struct_out.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/.aii_worker_result.json"], "durationMs": 78, "numFiles": 39, "truncated": false, "totalMatches": 39, "countIsComplete": true}
```

### [16] TOOL CALL — Read · 2026-09-24 10:58:44 UTC

```
/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/src_e2/run_all.sh
```

### [17] TOOL RESULT — Read · 2026-09-24 10:58:44 UTC

```
{"type": "text", "file": {"filePath": "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/src_e2/run_all.sh", "content": "#!/bin/bash\n# E2 end-to-end, in execution order. Every step is resumable (append-only raw files, per-sentence skip, panel cache\n# never re-bills). Steps 0-2 are $0 and already executed; the LLM steps need the run's OpenRouter budget.\n# Spend stop: AII_HARD_CAP (cumulative cost_ledger.jsonl) = 9.5.\nset -e\ncd \"$(dirname \"$0\")/..\"\nPY=.venv/bin/python\nexport AII_HARD_CAP=${AII_HARD_CAP:-9.5}\nR=\"$PY src_e2/e.py\"\n# --- $0 steps ---------------------------------------------------------------------------------------------\n# $PY src_e2/select_e2.py && $PY src_e2/prereg_e2.py                            # step 1-2 (frozen; do not rerun)\n# --- step 3: panel drift check (fresh cache) -------------------------------------------------------------\n$R gate.py --mode synthetic --members P1,P3,R1 --cap 0.30\n$R gate.py --mode trackh --members P1,P3,R1 --cap 0.50\n$PY src_e2/drift_report.py\nPASS=$($PY -c \"import json;print(json.load(open('panel_drift_E2.json'))['passes'])\")\n# --- step 4: pilot (30 sentences; work/sentences.json = pilot) -------------------------------------------\ncp work/sentences_pilot.json work/sentences.json\n$R generate.py --slots G1,G1b,G2,G3,G4,G5,G6,G7,G8,G9 --variants fewshot_v1 --sentences work/sentences_pilot.json --cap 1.3\n$PY src_e2/gen_retry.py --sentences work/sentences_pilot.json --concurrency 3\n$R run_label.py --kind heldout --budget 8 --workers 4\nif [ \"$PASS\" = \"True\" ]; then\n  $R panel_run.py --kind heldout --members P1,P3,R1 --cap 4.6                   # pilot: all three raters (E's 5c)\nfi\n$PY src_e2/pilot_projection.py\n# --- step 5-6: full generation + solver labels ----------------------------------------------------------\n$PY src_e2/activate_full.py\n$R generate.py --slots G1,G1b,G2,G3,G4,G5,G6,G7,G8,G9 --variants fewshot_v1 --sentences work/sentences.json --cap 1.3\n$PY src_e2/gen_retry.py --sentences work/sentences.json --concurrency 4\n$R run_label.py --kind heldout --budget 8 --workers 4\n# --- step 7: panel (frozen protocol) ---------------------------------------------------------------------\nif [ \"$PASS\" = \"True\" ]; then\n  $R panel_run.py --kind heldout --members P3,R1 --cap 4.6                      # 7a/7c stage 1, full class coverage\n  $R panel_run.py --kind heldout --members P3,R1 --adjudicate P1 --cap 1.9      # stage 2 (disagreements)\n  $PY src_e2/repair.py --cap 1.0                                                  # 7b reference repair\n  $R run_label.py --kind heldout --refs work/reference_overrides.json --out labels_heldout_repaired.jsonl --budget 8\nfi\n# --- steps 7d-12 ($0) ------------------------------------------------------------------------------------\n$PY src_e2/assemble_e2.py\n$PY src_e2/controls_e2.py\n$PY src_e2/testability_e2.py\n$PY src_e2/seal_e2.py && $PY src_e2/verify_seal.py\n$PY data.py\n$PY src_e2/card_e2.py\n", "numLines": 45, "startLine": 1, "totalLines": 45}}
```

### [18] TOOL CALL — Read · 2026-09-24 10:58:44 UTC

```
/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/pilot_projection.json
```

### [19] TOOL RESULT — Read · 2026-09-24 10:58:44 UTC

```
{"type": "text", "file": {"filePath": "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/pilot_projection.json", "content": "{\n \"per_sentence_cost_usd\": {\n  \"L25\": {\n   \"generation\": 0.001,\n   \"panel_stage1\": 0.00664,\n   \"adjudication_P1\": 0.00277,\n   \"reference_repair\": 0.00141,\n   \"total\": 0.01182\n  },\n  \"EXC\": {\n   \"generation\": 0.00087,\n   \"panel_stage1\": 0.00667,\n   \"adjudication_P1\": 0.00231,\n   \"reference_repair\": 0.00093,\n   \"total\": 0.01078\n  },\n  \"DT\": {\n   \"generation\": 0.00081,\n   \"panel_stage1\": 0.00667,\n   \"adjudication_P1\": 0.00231,\n   \"reference_repair\": 0.00093,\n   \"total\": 0.01072\n  }\n },\n \"panel_cost_source\": \"E per-stratum measured costs (E2 panel pilot blocked by the run budget stop)\",\n \"pilot_sentences\": {\n  \"EXC\": 8,\n  \"L25\": 12,\n  \"DT\": 10\n },\n \"spent_so_far_usd\": 0.2409,\n \"projected_total_usd\": 6.793,\n \"decision\": \"SURPLUS: add 100 L25 sentences from the pre-registered surplus order\",\n \"add_l25\": 100,\n \"E_per_sentence_costs_by_stratum\": {\n  \"EXC\": {\n   \"P1\": 0.00231,\n   \"stage1\": 0.00667,\n   \"repair\": 0.00093\n  },\n  \"CTRL\": {\n   \"P1\": 0.00143,\n   \"stage1\": 0.00401\n  },\n  \"L25\": {\n   \"P1\": 0.00277,\n   \"stage1\": 0.00664,\n   \"repair\": 0.00141\n  },\n  \"L20\": {\n   \"P1\": 0.00254,\n   \"stage1\": 0.00644,\n   \"repair\": 0.00111\n  }\n },\n \"note\": \"COST ONLY; no pilot label was inspected for this decision\"\n}", "numLines": 57, "startLine": 1, "totalLines": 57}}
```

### [20] TOOL CALL — Grep · 2026-09-24 10:58:44 UTC

```
Pattern: "def |surplus|L25|12gram|twelve|sha1\("
```

### [21] TOOL RESULT — Grep · 2026-09-24 10:58:44 UTC

```
{"mode": "content", "numFiles": 0, "filenames": [], "content": "9:  * E2 order = sha1('E2_v1|' + sentence_id) (sentence_id = E's recipe sha1('heldout|'+norm(text))[:12]).\n10:  * L25: MALLS-train, >=25 words and gold n_conditions >=3; long bin (>=30 words) gets min(supply, 45% of target).\n15:Outputs: work/pool_E2.json (ranked pools incl. surplus/reserve), work/sentences.json (ACTIVE set), census_E2.json,\n49:def e2key(sentence_id: str) -> str:\n50:    return hashlib.sha1((SEED + sentence_id).encode()).hexdigest()\n53:def grams12(text: str) -> set:\n58:def build_exclusion_without_malls_test() -> tuple[set, dict]:\n63:    def load(fp, *a, **k):\n74:def extra_exclusion_texts() -> dict[str, list[str]]:\n89:def crosscheck_E_heldout(e_texts: set) -> dict:\n98:def feats(text: str, fol: str, e) -> dict:\n103:def malls_test_pool(ex_nomt: set) -> tuple[list, dict]:\n126:def constants(e, bound=frozenset()) -> set:\n137:def dt_units() -> tuple[list, dict]:\n183:def main():\n216:    def ok12(r, tag):\n231:    def take(rows, n, tag, used):\n267:    # ---- L25 (from MALLS-train minus EXC) ----\n272:    def l25_for(target):\n277:    base = take(long_, nl_base, \"L25\", used) + take(short, ns_base, \"L25\", used)\n278:    surplus = take(long_, nl_max - nl_base, \"L25\", used) + take(short, ns_max - ns_base, \"L25\", used)\n279:    base, surplus = srt(base), srt(surplus)\n280:    for i, r in enumerate(base + surplus):\n281:        r[\"source_stratum\"] = \"L25\"; r[\"e2_rank\"] = i; r[\"l25_tier\"] = \"base\" if i < len(base) else \"surplus\"\n310:    allrows = exc + base + surplus + dt\n325:    (W / \"pool_E2.json\").write_text(json.dumps({\"EXC\": exc, \"L25\": base + surplus, \"DT\": dt}, ensure_ascii=False, indent=1))\n330:             \"twelvegram_dropped_vs_E\": dict(drop12), \"twelvegram_dropped_within_E2\": dict(within12),\n332:             \"final_collisions_with_E_text\": coll_E, \"final_12gram_collisions_with_E\": coll_12}\n335:        \"seed_string\": SEED, \"order\": \"sha1('E2_v1|' + sentence_id)\",\n336:        \"malls\": {\"L25_supply_after_filters\": {\"25-29\": len(short), \">=30\": len(long_), \">=35\": sum(r[\"words\"] >= 35 for r in long_)},\n337:                  \"L25_targets\": {\"base\": a.l25, \"max_with_surplus\": a.l25_max, \"base_long_short\": [nl_base, ns_base], \"max_long_short\": [nl_max, ns_max]},\n338:                  \"L25_selected\": {\"base\": len(base), \"surplus_reserve\": len(surplus)},\n358:    logger.info(f\"E2 selection: active {census['active_counts']}; L25 supply {census['malls']['L25_supply_after_filters']}; \"", "numLines": 33, "totalLines": 33}
```

### [22] TOOL CALL — Read · 2026-09-24 10:58:48 UTC

```
/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/src_e2/select_e2.py
```

### [23] TOOL RESULT — Read · 2026-09-24 10:58:48 UTC

```
{"type": "text", "file": {"filePath": "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/src_e2/select_e2.py", "content": "def main():\n    ap = argparse.ArgumentParser()\n    ap.add_argument(\"--l25\", type=int, default=350)\n    ap.add_argument(\"--l25-max\", type=int, default=450)\n    ap.add_argument(\"--exc\", type=int, default=100)\n    ap.add_argument(\"--dt\", type=int, default=100)\n    a = ap.parse_args()\n\n    # ---- exclusion ----\n    ex_all, exsrc = ss.build_exclusion()\n    ex_nomt, exsrc_nomt = build_exclusion_without_malls_test()\n    extra = extra_exclusion_texts()\n    extra_counts = {}\n    for tag, texts in extra.items():\n        hs = {ss.h(t) for t in texts}\n        ex_all |= hs\n        ex_nomt |= hs\n        extra_counts[tag] = len(hs)\n    e_norm = {ss.norm(t) for t in extra[\"E_700_sentences\"]}\n    xcheck = crosscheck_E_heldout(e_norm)\n    e_grams = set()\n    for t in extra[\"E_700_sentences\"]:\n        e_grams |= grams12(t)\n\n    # ---- pools ----\n    train_pool, tlog = ss.malls_pool(ex_all)\n    test_pool, mlog = malls_test_pool(ex_nomt)\n    train_ids = {r[\"sentence_id\"] for r in train_pool}\n    test_pool = [r for r in test_pool if r[\"sentence_id\"] not in train_ids]\n    dt_pool, dlog = dt_units()\n    dt_pool = [r for r in dt_pool if ss.h(r[\"text\"]) not in ex_all]\n    drop12 = Counter()\n\n    def ok12(r, tag):\n        if grams12(r[\"text\"]) & e_grams:\n            drop12[tag] += 1\n            return False\n        return True\n    train_pool = [r for r in train_pool if ok12(r, \"malls_train\")]\n    test_pool = [r for r in test_pool if ok12(r, \"malls_test\")]\n    dt_pool = [r for r in dt_pool if ok12(r, \"proverqa\")]\n    for r in train_pool + test_pool + dt_pool:\n        r[\"e2_key\"] = e2key(r[\"sentence_id\"])\n    srt = lambda xs: sorted(xs, key=lambda r: r[\"e2_key\"])  # noqa: E731\n\n    accepted_grams: set = set()\n    within12 = Counter()\n\n    def take(rows, n, tag, used):\n        out = []\n        for r in rows:\n            if len(out) >= n:\n                break\n            if r[\"sentence_id\"] in used:\n                continue\n            g = grams12(r[\"text\"])\n            if g & accepted_grams:\n                within12[tag] += 1\n                continue\n            accepted_grams.update(g)\n            used.add(r[\"sentence_id\"])\n            out.append(r)\n        return out\n\n    used: set = set()\n    # ---- EXC ladder ----\n    exc_pools = {\n        \"a_malls_train_core\": srt([r for r in train_pool if r[\"exception_type\"] in CORE]),\n        \"b_malls_test_noncurated_core\": srt([r for r in test_pool if r[\"exception_type\"] in CORE and r[\"words\"] >= 15]),\n        \"c_malls_train_without\": srt([r for r in train_pool if r[\"exception_type\"] == \"without\" and r[\"words\"] >= 15]),\n        \"d_but_not_nonxor\": srt([r for r in train_pool if r[\"exception_type\"] == \"but_not\" and r[\"words\"] >= 15])\n        + srt([r for r in test_pool if r[\"exception_type\"] == \"but_not\" and r[\"words\"] >= 15]),\n    }\n    exc = []\n    exc_taken = {}\n    for name, rows in exc_pools.items():\n        got = take(rows, a.exc - len(exc), f\"EXC_{name}\", used)\n        for r in got:\n            r[\"exc_pool\"] = name\n        exc_taken[name] = len(got)\n        exc += got\n    for i, r in enumerate(exc):\n        r[\"source_stratum\"] = \"EXC\"; r[\"e2_rank\"] = i\n\n    # ---- L25 (from MALLS-train minus EXC) ----\n    l25_all = srt([r for r in train_pool if r[\"words\"] >= 25 and r[\"n_conditions\"] >= 3 and r[\"sentence_id\"] not in used])\n    short = [r for r in l25_all if r[\"words\"] <= 29]\n    long_ = [r for r in l25_all if r[\"words\"] >= 30]\n\n    def l25_for(target):\n        nl = min(len(long_), round(0.45 * target))\n        return nl, target - nl\n    nl_base, ns_base = l25_for(a.l25)\n    nl_max, ns_max = l25_for(a.l25_max)\n    base = take(long_, nl_base, \"L25\", used) + take(short, ns_base, \"L25\", used)\n    surplus = take(long_, nl_max - nl_base, \"L25\", used) + take(short, ns_max - ns_base, \"L25\", used)\n    base, surplus = srt(base), srt(surplus)\n    for i, r in enumerate(base + surplus):\n        r[\"source_stratum\"] = \"L25\"; r[\"e2_rank\"] = i; r[\"l25_tier\"] = \"base\" if i < len(base) else \"surplus\"\n        r[\"word_bin\"] = \"30-34\" if r[\"words\"] >= 30 else \"25-29\"\n\n    # ---- DT ladder (one sentence per skeleton) ----\n    rungs = [(\"r1_ge15w_ge2c\", lambda r: r[\"words\"] >= 15 and r[\"n_conditions\"] >= 2),\n             (\"r2_ge12w_ge2c\", lambda r: r[\"words\"] >= 12 and r[\"n_conditions\"] >= 2),\n             (\"r3_ge15w_ge1c\", lambda r: r[\"words\"] >= 15 and r[\"n_conditions\"] >= 1)]\n    census_dt = {}\n    for diff in (\"easy\", \"medium\", \"hard\"):\n        sub = [r for r in dt_pool if r[\"source\"].endswith(diff)]\n        census_dt[diff] = {name: {\"units\": sum(f(r) for r in sub), \"skeletons\": len({r[\"skeleton\"] for r in sub if f(r)})} for name, f in rungs}\n    need = int(a.dt * 1.1)  # +10% reserve\n    dt, skel_used, rung_taken = [], set(), {}\n    for name, f in rungs:\n        cnt = 0\n        for r in srt([r for r in dt_pool if f(r)]):\n            if len(dt) >= need:\n                break\n            if r[\"skeleton\"] in skel_used:\n                continue\n            got = take([r], 1, \"DT\", used)\n            if got:\n                skel_used.add(r[\"skeleton\"]); got[0][\"dt_rung\"] = name; dt.append(got[0]); cnt += 1\n        rung_taken[name] = cnt\n        if len(dt) >= need:\n            break\n    for i, r in enumerate(dt):\n        r[\"source_stratum\"] = \"DT\"; r[\"e2_rank\"] = i; r[\"dt_tier\"] = \"base\" if i < a.dt else \"reserve\"\n\n    allrows = exc + base + surplus + dt\n    for r in allrows:\n        r[\"source_dataset\"] = \"ProverQA\" if r[\"source\"].startswith(\"ProverQA\") else r[\"source\"]", "numLines": 130, "startLine": 183, "totalLines": 364}}
```

### [24] TOOL CALL — Glob · 2026-09-24 10:58:48 UTC

```
Pattern: "iter_4/gen_art/*evaluation*/**/power*"
```

### [25] TOOL CALL — Glob · 2026-09-24 10:58:48 UTC

```
Pattern: "iter_5/gen_plan/*"
```

### [26] TOOL RESULT — Glob · 2026-09-24 10:58:50 UTC

```
{"filenames": [], "durationMs": 2038, "numFiles": 0, "truncated": false, "totalMatches": 0, "countIsComplete": true}
```

### [27] TOOL RESULT — Glob · 2026-09-24 10:58:50 UTC

```
{"filenames": ["/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/power_E2.json"], "durationMs": 2055, "numFiles": 1, "truncated": false, "totalMatches": 1, "countIsComplete": true}
```

### [28] TOOL CALL — ToolSearch · 2026-09-24 10:59:26 UTC

```
{'query': 'select:WebSearch,WebFetch', 'max_results': 2}
```

### [29] TOOL CALL — Read · 2026-09-24 10:59:26 UTC

```
/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/power_E2.json
```

### [30] TOOL RESULT — ToolSearch · 2026-09-24 10:59:26 UTC

```
{"matches": ["WebSearch", "WebFetch"], "query": "select:WebSearch,WebFetch", "total_deferred_tools": 27}
```

### [31] TOOL RESULT — Read · 2026-09-24 10:59:26 UTC

```
{"type": "text", "file": {"filePath": "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/power_E2.json", "content": "{\n \"population\": {\n  \"n\": 2686,\n  \"n_err\": 1822,\n  \"n_cor\": 864,\n  \"n_sent\": 292,\n  \"source\": \"/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6/results/per_item_T1.jsonl :: in_R_AB & pool == E_POOL\"\n },\n \"comparators\": {\n  \"flashlite_disg\": \"judge_cheap_disg\",\n  \"flashlite_orig\": \"judge_cheap_orig\",\n  \"nano_orig\": \"judge_cheap2_orig\"\n },\n \"z_two_sided\": 2.8015852181129683,\n \"z_one_sided\": 2.4864748605243863,\n \"B\": 1000,\n \"cells\": {\n  \"L25\": {\n   \"n_rows\": 873,\n   \"n_err\": 697,\n   \"n_cor\": 176,\n   \"n_sent\": 111,\n   \"observed_delta\": {\n    \"flashlite_disg\": 0.06942089474370672,\n    \"flashlite_orig\": 0.061395428459632195,\n    \"nano_orig\": 0.043167960088691726\n   },\n   \"se\": {}\n  },\n  \"L20\": {\n   \"n_rows\": 821,\n   \"n_err\": 592,\n   \"n_cor\": 229,\n   \"n_sent\": 79,\n   \"observed_delta\": {\n    \"flashlite_disg\": 0.10793476336598617,\n    \"flashlite_orig\": 0.11303552460757715,\n    \"nano_orig\": 0.09145963649238775\n   },\n   \"se\": {}\n  },\n  \"EXC\": {\n   \"n_rows\": 606,\n   \"n_err\": 384,\n   \"n_cor\": 222,\n   \"n_sent\": 64,\n   \"observed_delta\": {\n    \"flashlite_disg\": 0.1968961148648649,\n    \"flashlite_orig\": 0.18973465653153165,\n    \"nano_orig\": 0.1887492961711712\n   },\n   \"se\": {}\n  },\n  \"CTRL\": {\n   \"n_rows\": 386,\n   \"n_err\": 149,\n   \"n_cor\": 237,\n   \"n_sent\": 38,\n   \"observed_delta\": {\n    \"flashlite_disg\": -0.06913884405176574,\n    \"flashlite_orig\": 0.16753037125138037,\n    \"nano_orig\": -0.002718545578115683\n   },\n   \"se\": {}\n  },\n  \"long\": {\n   \"n_rows\": 2300,\n   \"n_err\": 1673,\n   \"n_cor\": 627,\n   \"n_sent\": 254,\n   \"observed_delta\": {\n    \"flashlite_disg\": 0.11625879215576673,\n    \"flashlite_orig\": 0.11362842370039128,\n    \"nano_orig\": 0.09835860350288805\n   },\n   \"se\": {}\n  },\n  \"all\": {\n   \"n_rows\": 2686,\n   \"n_err\": 1822,\n   \"n_cor\": 864,\n   \"n_sent\": 292,\n   \"observed_delta\": {\n    \"flashlite_disg\": 0.09897545149036036,\n    \"flashlite_orig\": 0.11865332984865395,\n    \"nano_orig\": 0.08893587926114233\n   },\n   \"se\": {}\n  }\n },\n \"yield\": {\n  \"L25\": {\n   \"n_built\": 300,\n   \"n_usable\": 111,\n   \"yield\": 0.37,\n   \"yield_ci\": [\n    0.31666666666666665,\n    0.42333333333333334\n   ],\n   \"rows_per_usable_sentence\": 7.864864864864865,\n   \"correct_share\": 0.20160366552119124\n  },\n  \"L20\": {\n   \"n_built\": 150,\n   \"n_usable\": 79,\n   \"yield\": 0.5266666666666666,\n   \"yield_ci\": [\n    0.44666666666666666,\n    0.6066666666666667\n   ],\n   \"rows_per_usable_sentence\": 10.39240506329114,\n   \"correct_share\": 0.27892813641900127\n  },\n  \"EXC\": {\n   \"n_built\": 100,\n   \"n_usable\": 64,\n   \"yield\": 0.64,\n   \"yield_ci\": [\n    0.54,\n    0.74\n   ],\n   \"rows_per_usable_sentence\": 9.46875,\n   \"correct_share\": 0.36633663366336633\n  },\n  \"CTRL\": {\n   \"n_built\": 150,\n   \"n_usable\": 38,\n   \"yield\": 0.25333333333333335,\n   \"yield_ci\": [\n    0.18666666666666668,\n    0.32666666666666666\n   ],\n   \"rows_per_usable_sentence\": 10.157894736842104,\n   \"correct_share\": 0.6139896373056994\n  }\n },\n \"yield_note\": \"yield = #built sentences of the stratum contributing >= 1 R_AB row / #built (dataset E); CI = binomial parametric bootstrap\",\n \"se_fit\": {\n  \"CTRL|flashlite_disg\": {\n   \"a\": -0.6411006317523646,\n   \"b\": -0.4982126990952158,\n   \"n_for_mde_0.069\": 467.51982502230936,\n   \"n_for_mde_0.1\": 221.99437971250552\n  },\n  \"CTRL|flashlite_orig\": {\n   \"a\": -0.6457774287072859,\n   \"b\": -0.5086177112339458,\n   \"n_for_mde_0.069\": 408.49749071865784,\n   \"n_for_mde_0.1\": 196.9465882870296\n  },\n  \"CTRL|nano_orig\": {\n   \"a\": -0.5331577082094998,\n   \"b\": -0.5101971048812463,\n   \"n_for_mde_0.069\": 500.0013844609486,\n   \"n_for_mde_0.1\": 241.6078860518208\n  },\n  \"EXC|flashlite_disg\": {\n   \"a\": -1.1331667419733504,\n   \"b\": -0.5096049499561568,\n   \"n_for_mde_0.069\": 155.15612166522348,\n   \"n_for_mde_0.1\": 74.91034344865612\n  },\n  \"EXC|flashlite_orig\": {\n   \"a\": -1.3413141692830084,\n   \"b\": -0.503318217307356,\n   \"n_for_mde_0.069\": 109.2773704645141,\n   \"n_for_mde_0.1\": 52.282127413677834\n  },\n  \"EXC|nano_orig\": {\n   \"a\": -1.315208619039332,\n   \"b\": -0.5072561615664751,\n   \"n_for_mde_0.069\": 110.93160541737636,\n   \"n_for_mde_0.1\": 53.37819939047894\n  },\n  \"L20|flashlite_disg\": {\n   \"a\": -1.0098992072427915,\n   \"b\": -0.5123734583598655,\n   \"n_for_mde_0.069\": 192.05017772413476,\n   \"n_for_mde_0.1\": 93.08854815314308\n  },\n  \"L20|flashlite_orig\": {\n   \"a\": -1.1676605372792332,\n   \"b\": -0.5170929153371234,\n   \"n_for_mde_0.069\": 134.91930176840899,\n   \"n_for_mde_0.1\": 65.83035665248299\n  },\n  \"L20|nano_orig\": {\n   \"a\": -1.058590510722619,\n   \"b\": -0.5275650908526812,\n   \"n_for_mde_0.069\": 150.51477213207343,\n   \"n_for_mde_0.1\": 74.49334291551305\n  },\n  \"L25|flashlite_disg\": {\n   \"a\": -0.7948799190097076,\n   \"b\": -0.5025686295124865,\n   \"n_for_mde_0.069\": 326.416175274051,\n   \"n_for_mde_0.1\": 155.9973204457915\n  },\n  \"L25|flashlite_orig\": {\n   \"a\": -0.934516902938053,\n   \"b\": -0.5230009545969356,\n   \"n_for_mde_0.069\": 199.34800212652286,\n   \"n_for_mde_0.1\": 98.0583353476636\n  },\n  \"L25|nano_orig\": {\n   \"a\": -0.6705607672686412,\n   \"b\": -0.5167383727902036,\n   \"n_for_mde_0.069\": 354.2621191376214,\n   \"n_for_mde_0.1\": 172.76788335001254\n  },\n  \"all|flashlite_disg\": {\n   \"a\": -0.7916959629407039,\n   \"b\": -0.5144686203470104,\n   \"n_for_mde_0.069\": 287.2858824862146,\n   \"n_for_mde_0.1\": 139.66149859043324\n  },\n  \"all|flashlite_orig\": {\n   \"a\": -1.0546623244970075,\n   \"b\": -0.5042957396589947,\n   \"n_for_mde_0.069\": 191.17913343928856,\n   \"n_for_mde_0.1\": 91.59760789266686\n  },\n  \"all|nano_orig\": {\n   \"a\": -0.910841151843641,\n   \"b\": -0.5024042670732887,\n   \"n_for_mde_0.069\": 259.6291311533635,\n   \"n_for_mde_0.1\": 124.04920466395457\n  },\n  \"long|flashlite_disg\": {\n   \"a\": -0.8900722630009886,\n   \"b\": -0.5144825804706389,\n   \"n_for_mde_0.069\": 237.24898963798333,\n   \"n_for_mde_0.1\": 115.338761586516\n  },\n  \"long|flashlite_orig\": {\n   \"a\": -1.0714204822971762,\n   \"b\": -0.513160192947816,\n   \"n_for_mde_0.069\": 168.98481322765102,\n   \"n_for_mde_0.1\": 81.99953944402142\n  },\n  \"long|nano_orig\": {\n   \"a\": -0.9566064711074329,\n   \"b\": -0.5059808179314379,\n   \"n_for_mde_0.069\": 228.03738900804342,\n   \"n_for_mde_0.1\": 109.52516803109947\n  }\n },\n \"planned_E2\": [\n  {\n   \"cell\": \"L25\",\n   \"planned_sentences\": 250,\n   \"yield_scenario\": \"E_yield\",\n   \"yield\": 0.37,\n   \"n_usable\": 92.5,\n   \"comparator\": \"flashlite_disg\",\n   \"se_model_cell\": \"L25\",\n   \"se\": 0.046415911280574776,\n   \"mde80\": 0.13003813092890126,\n   \"mde80_yield_band\": [\n    0.12152905816800227,\n    0.14061901229629764\n   ],\n   \"mde80_one_sided\": 0.11541199652747945,\n   \"power_at_0.05\": 0.18868644450989153,\n   \"power_at_0.069\": 0.317962208974641,\n   \"power_at_0.099\": 0.5686449293197128,\n   \"power_at_0.1\": 0.5770959173563376,\n   \"power_at_0.15\": 0.8982577271124431,\n   \"mde80_labelmix_cor_x0.5\": 0.1667724855514821,\n   \"mde80_labelmix_cor_x1.5\": 0.11770378985425978,\n   \"verdict\": \"MARGINAL\"\n  },\n  {\n   \"cell\": \"L25\",\n   \"planned_sentences\": 250,\n   \"yield_scenario\": \"E_yield\",\n   \"yield\": 0.37,\n   \"n_usable\": 92.5,\n   \"comparator\": \"flashlite_orig\",\n   \"se_model_cell\": \"L25\",\n   \"se\": 0.036800224043740414,\n   \"mde80\": 0.10309896370418858,\n   \"mde80_yield_band\": [\n    0.0960879252320242,\n    0.11184300749482196\n   ],\n   \"mde80_one_sided\": 0.09150283194642561,\n   \"power_at_0.05\": 0.27382788479769526,\n   \"power_at_0.069\": 0.4661404740589433,\n   \"power_at_0.099\": 0.7673773438166083,\n   \"power_at_0.1\": 0.7755980989408133,\n   \"power_at_0.15\": 0.9828317698642984,\n   \"mde80_labelmix_cor_x0.5\": 0.1322232972121883,\n   \"mde80_labelmix_cor_x1.5\": 0.09331984911921483,\n   \"verdict\": \"MARGINAL\"\n  },\n  {\n   \"cell\": \"L25\",\n   \"planned_sentences\": 250,\n   \"yield_scenario\": \"E_yield\",\n   \"yield\": 0.37,\n   \"n_usable\": 92.5,\n   \"comparator\": \"nano_orig\",\n   \"se_model_cell\": \"L25\",\n   \"se\": 0.04929447882822848,\n   \"mde80\": 0.13810268321974759,\n   \"mde80_yield_band\": [\n    0.1288198749073718,\n    0.1496694996850532\n   ],\n   \"mde80_one_sided\": 0.12256948236904172,\n   \"power_at_0.05\": 0.17216315632501233,\n   \"power_at_0.069\": 0.28766711313439686,\n   \"power_at_0.099\": 0.5192911180636391,\n   \"power_at_0.1\": 0.5273701771540341,\n   \"power_at_0.15\": 0.8605898288172789,\n   \"mde80_labelmix_cor_x0.5\": 0.1771151859640226,\n   \"mde80_labelmix_cor_x1.5\": 0.12500340544646987,\n   \"verdict\": \"MARGINAL\"\n  },\n  {\n   \"cell\": \"L25\",\n   \"planned_sentences\": 300,\n   \"yield_scenario\": \"E_yield\",\n   \"yield\": 0.37,\n   \"n_usable\": 111.0,\n   \"comparator\": \"flashlite_disg\",\n   \"se_model_cell\": \"L25\",\n   \"se\": 0.04235189732051602,\n   \"mde80\": 0.11865244949219592,\n   \"mde80_yield_band\": [\n    0.1108884012182323,\n    0.12830690609703851\n   ],\n   \"mde80_one_sided\": 0.10530692798297321,\n   \"power_at_0.05\": 0.21787814763281893,\n   \"power_at_0.069\": 0.3704139599515343,\n   \"power_at_0.099\": 0.6471337506219684,\n   \"power_at_0.1\": 0.6558655183833452,\n   \"power_at_0.15\": 0.9431512377468814,\n   \"mde80_labelmix_cor_x0.5\": 0.1521685679455423,\n   \"mde80_labelmix_cor_x1.5\": 0.10739921983056229,\n   \"verdict\": \"MARGINAL\"\n  },\n  {\n   \"cell\": \"L25\",\n   \"planned_sentences\": 300,\n   \"yield_scenario\": \"E_yield\",\n   \"yield\": 0.37,\n   \"n_usable\": 111.0,\n   \"comparator\": \"flashlite_orig\",\n   \"se_model_cell\": \"L25\",\n   \"se\": 0.033453271519141486,\n   \"mde80\": 0.09372219098554635,\n   \"mde80_yield_band\": [\n    0.08734880115613422,\n    0.10167097061133445\n   ],\n   \"mde80_one_sided\": 0.08318071863464176,\n   \"power_at_0.05\": 0.32084333385399344,\n   \"power_at_0.069\": 0.5408655557326333,\n   \"power_at_0.099\": 0.8411965751573333,\n   \"power_at_0.1\": 0.8483260062751448,\n   \"power_at_0.15\": 0.9941969928878046,\n   \"mde80_labelmix_cor_x0.5\": 0.12019618345870914,\n   \"mde80_labelmix_cor_x1.5\": 0.0848333956503838,\n   \"verdict\": \"ADEQUATE\"\n  },\n  {\n   \"cell\": \"L25\",\n   \"planned_sentences\": 300,\n   \"yield_scenario\": \"E_yield\",\n   \"yield\": 0.37,\n   \"n_usable\": 111.0,\n   \"comparator\": \"nano_orig\",\n   \"se_model_cell\": \"L25\",\n   \"se\": 0.04486237808216381,\n   \"mde80\": 0.12568577528438535,\n   \"mde80_yield_band\": [\n    0.11723759069914584,\n    0.1362126112670062\n   ],\n   \"mde80_one_sided\": 0.11154917528464055,\n   \"power_at_0.05\": 0.1989313880711927,\n   \"power_at_0.069\": 0.3365391776754961,\n   \"power_at_0.099\": 0.5974626273409861,\n   \"power_at_0.1\": 0.6060641043228564,\n   \"power_at_0.15\": 0.9167587249684117,\n   \"mde80_labelmix_cor_x0.5\": 0.16118861867582499,\n   \"mde80_labelmix_cor_x1.5\": 0.11376549129084933,\n   \"verdict\": \"MARGINAL\"\n  },\n  {\n   \"cell\": \"L25\",\n   \"planned_sentences\": 350,\n   \"yield_scenario\": \"E_yield\",\n   \"yield\": 0.37,\n   \"n_usable\": 129.5,\n   \"comparator\": \"flashlite_disg\",\n   \"se_model_cell\": \"L25\",\n   \"se\": 0.03919471534779047,\n   \"mde80\": 0.10980733514651526,\n   \"mde80_yield_band\": [\n    0.10262206881142019,\n    0.11874208665482837\n   ],\n   \"mde80_one_sided\": 0.09745667437769033,\n   \"power_at_0.05\": 0.24689861785748335,\n   \"power_at_0.069\": 0.4209269936901481,\n   \"power_at_0.099\": 0.7142646105409962,\n   \"power_at_0.1\": 0.7228739069391656,\n   \"power_at_0.15\": 0.9690549703814374,\n   \"mde80_labelmix_cor_x0.5\": 0.14082368709193385,\n   \"mde80_labelmix_cor_x1.5\": 0.09939376051037874,\n   \"verdict\": \"MARGINAL\"\n  },\n  {\n   \"cell\": \"L25\",\n   \"planned_sentences\": 350,\n   \"yield_scenario\": \"E_yield\",\n   \"yield\": 0.37,\n   \"n_usable\": 129.5,\n   \"comparator\": \"flashlite_orig\",\n   \"se_model_cell\": \"L25\",\n   \"se\": 0.030862091928905912,\n   \"mde80\": 0.08646278054806635,\n   \"mde80_yield_band\": [\n    0.08058305238152441,\n    0.09379587403619712\n   ],\n   \"mde80_one_sided\": 0.07673781572441711,\n   \"power_at_0.05\": 0.36698344378535397,\n   \"power_at_0.069\": 0.6086447575888067,\n   \"power_at_0.099\": 0.89395789257956,\n   \"power_at_0.1\": 0.8997726293930528,\n   \"power_at_0.15\": 0.9981363736523868,\n   \"mde80_labelmix_cor_x0.5\": 0.11088519302242482,\n   \"mde80_labelmix_cor_x1.5\": 0.07826308589848942,\n   \"verdict\": \"ADEQUATE\"\n  },\n  {\n   \"cell\": \"L25\",\n   \"planned_sentences\": 350,\n   \"yield_scenario\": \"E_yield\",\n   \"yield\": 0.37,\n   \"n_usable\": 129.5,\n   \"comparator\": \"nano_orig\",\n   \"se_model_cell\": \"L25\",\n   \"se\": 0.041427460888348325,\n   \"mde80\": 0.1160625620487498,\n   \"mde80_yield_band\": [\n    0.10826121821803338,\n    0.12578340397891638\n   ],\n   \"mde80_one_sided\": 0.10300834003423537,\n   \"power_at_0.05\": 0.22571441712593893,\n   \"power_at_0.069\": 0.3842253327834917,\n   \"power_at_0.099\": 0.6663131547369268,\n   \"power_at_0.1\": 0.6750473759231037,\n   \"power_at_0.15\": 0.951625472657685,\n   \"mde80_labelmix_cor_x0.5\": 0.14884577518644923,\n   \"mde80_labelmix_cor_x1.5\": 0.10505577319677357,\n   \"verdict\": \"MARGINAL\"\n  },\n  {\n   \"cell\": \"L25\",\n   \"planned_sentences\": 400,\n   \"yield_scenario\": \"E_yield\",\n   \"yield\": 0.37,\n   \"n_usable\": 148.0,\n   \"comparator\": \"flashlite_disg\",\n   \"se_model_cell\": \"L25\",\n   \"se\": 0.03665072596420192,\n   \"mde80\": 0.10268013209441727,\n   \"mde80_yield_band\": [\n    0.09596123580723653,\n    0.11103496070290933\n   ],\n   \"mde80_one_sided\": 0.09113110872995647,\n   \"power_at_0.05\": 0.27567629435801444,\n   \"power_at_0.069\": 0.46918157364357177,\n   \"power_at_0.099\": 0.770717042948299,\n   \"power_at_0.1\": 0.778903399343987,\n   \"power_at_0.15\": 0.9835263289628692,\n   \"mde80_labelmix_cor_x0.5\": 0.1316824389791495,\n   \"mde80_labelmix_cor_x1.5\": 0.09294300371535022,\n   \"verdict\": \"MARGINAL\"\n  },\n  {\n   \"cell\": \"L25\",\n   \"planned_sentences\": 400,\n   \"yield_scenario\": \"E_yield\",\n   \"yield\": 0.37,\n   \"n_usable\": 148.0,\n   \"comparator\": \"flashlite_orig\",\n   \"se_model_cell\": \"L25\",\n   \"se\": 0.02878031327438531,\n   \"mde80\": 0.08063050024217833,\n   \"mde80_yield_band\": [\n    0.07514738461310429,\n    0.0874689455538225\n   ],\n   \"mde80_one_sided\": 0.07156152543477536,\n   \"power_at_0.05\": 0.4118979996663491,\n   \"power_at_0.069\": 0.6691285779458092,\n   \"power_at_0.099\": 0.9305483484460456,\n   \"power_at_0.1\": 0.9350673601066057,\n   \"power_at_0.15\": 0.9994268828513763,\n   \"mde80_labelmix_cor_x0.5\": 0.10340482342032581,\n   \"mde80_labelmix_cor_x1.5\": 0.07298433232135254,\n   \"verdict\": \"ADEQUATE\"\n  },\n  {\n   \"cell\": \"L25\",\n   \"planned_sentences\": 400,\n   \"yield_scenario\": \"E_yield\",\n   \"yield\": 0.37,\n   \"n_usable\": 148.0,\n   \"comparator\": \"nano_orig\",\n   \"se_model_cell\": \"L25\",\n   \"se\": 0.0386653238137865,\n   \"mde80\": 0.1083241996502556,\n   \"mde80_yield_band\": [\n    0.10104300309779744,\n    0.11739691356785502\n   ],\n   \"mde80_one_sided\": 0.09614035563701501,\n   \"power_at_0.05\": 0.25244495496427355,\n   \"power_at_0.069\": 0.43037510768032416,\n   \"power_at_0.099\": 0.7259033971850972,\n   \"power_at_0.1\": 0.7344516391494309,\n   \"power_at_0.15\": 0.9725382613544464,\n   \"mde80_labelmix_cor_x0.5\": 0.138920690102867,\n   \"mde80_labelmix_cor_x1.5\": 0.09805184591404943,\n   \"verdict\": \"MARGINAL\"\n  },\n  {\n   \"cell\": \"EXC\",\n   \"planned_sentences\": 75,\n   \"yield_scenario\": \"E_yield\",\n   \"yield\": 0.64,\n   \"n_usable\": 48.0,\n   \"comparator\": \"flashlite_disg\",\n   \"se_model_cell\": \"EXC\",\n   \"se\": 0.044781958200755985,\n   \"mde80\": 0.1254604721333908,\n   \"mde80_yield_band\": [\n    0.11651328199157579,\n    0.13680713168415312\n   ],\n   \"mde80_one_sided\": 0.11134921327123364,\n   \"power_at_0.05\": 0.19949039044360012,\n   \"power_at_0.069\": 0.33754780954162006,\n   \"power_at_0.099\": 0.598995425486385,\n   \"power_at_0.1\": 0.6076034328426111,\n   \"power_at_0.15\": 0.9176746956025377,\n   \"mde80_labelmix_cor_x0.5\": 0.13962245343392016,\n   \"mde80_labelmix_cor_x1.5\": 0.13318400236685657,\n   \"verdict\": \"MARGINAL\"\n  },\n  {\n   \"cell\": \"EXC\",\n   \"planned_sentences\": 75,\n   \"yield_scenario\": \"E_yield\",\n   \"yield\": 0.64,\n   \"n_usable\": 48.0,\n   \"comparator\": \"flashlite_orig\",\n   \"se_model_cell\": \"EXC\",\n   \"se\": 0.03726278539630735,\n   \"mde80\": 0.10439486875201046,\n   \"mde80_yield_band\": [\n    0.09703849679798279,\n    0.11371482789263754\n   ],\n   \"mde80_one_sided\": 0.09265297912103344,\n   \"power_at_0.05\": 0.26824065132293623,\n   \"power_at_0.069\": 0.4568984702258535,\n   \"power_at_0.099\": 0.7570492343155203,\n   \"power_at_0.1\": 0.7653684818117774,\n   \"power_at_0.15\": 0.980562141500598,\n   \"mde80_labelmix_cor_x0.5\": 0.11617896420452317,\n   \"mde80_labelmix_cor_x1.5\": 0.11082156961893835,\n   \"verdict\": \"MARGINAL\"\n  },\n  {\n   \"cell\": \"EXC\",\n   \"planned_sentences\": 75,\n   \"yield_scenario\": \"E_yield\",\n   \"yield\": 0.64,\n   \"n_usable\": 48.0,\n   \"comparator\": \"nano_orig\",\n   \"se_model_cell\": \"EXC\",\n   \"se\": 0.037669701383313256,\n   \"mde80\": 0.10553487856622006,\n   \"mde80_yield_band\": [\n    0.0980421052453685,\n    0.1150335510485465\n   ],\n   \"mde80_one_sided\": 0.09366476549306911,\n   \"power_at_0.05\": 0.26348526299097075,\n   \"power_at_0.069\": 0.448974318198774,\n   \"power_at_0.099\": 0.7479787970170633,\n   \"power_at_0.1\": 0.7563750115536383,\n   \"power_at_0.15\": 0.9784126547332183,\n   \"mde80_labelmix_cor_x0.5\": 0.11744765835569344,\n   \"mde80_labelmix_cor_x1.5\": 0.11203176010532918,\n   \"verdict\": \"MARGINAL\"\n  },\n  {\n   \"cell\": \"EXC\",\n   \"planned_sentences\": 100,\n   \"yield_scenario\": \"E_yield\",\n   \"yield\": 0.64,\n   \"n_usable\": 64.0,\n   \"comparator\": \"flashlite_disg\",\n   \"se_model_cell\": \"EXC\",\n   \"se\": 0.03867529915153337,\n   \"mde80\": 0.10835214640903293,\n   \"mde80_yield_band\": [\n    0.10062503332145688,\n    0.11815152701068175\n   ],\n   \"mde80_one_sided\": 0.09616515906354786,\n   \"power_at_0.05\": 0.2523384300911192,\n   \"power_at_0.069\": 0.4301942937659726,\n   \"power_at_0.099\": 0.7256833538832839,\n   \"power_at_0.1\": 0.7342328691512787,\n   \"power_at_0.15\": 0.972474942696453,\n   \"mde80_labelmix_cor_x0.5\": 0.12057044456665462,\n   \"mde80_labelmix_cor_x1.5\": 0.11503037933351966,\n   \"verdict\": \"MARGINAL\"\n  },\n  {\n   \"cell\": \"EXC\",\n   \"planned_sentences\": 100,\n   \"yield_scenario\": \"E_yield\",\n   \"yield\": 0.64,\n   \"n_usable\": 64.0,\n   \"comparator\": \"flashlite_orig\",\n   \"se_model_cell\": \"EXC\",\n   \"se\": 0.03223972830029843,\n   \"mde80\": 0.09032234624209441,\n   \"mde80_yield_band\": [\n    0.08395761986559305,\n    0.09838596648057171\n   ],\n   \"mde80_one_sided\": 0.08016327392882865,\n   \"power_at_0.05\": 0.3412395855220397,\n   \"power_at_0.069\": 0.5715228526180421,\n   \"power_at_0.099\": 0.8666687936085482,\n   \"power_at_0.1\": 0.8732312375443044,\n   \"power_at_0.15\": 0.996455994116304,\n   \"mde80_labelmix_cor_x0.5\": 0.10050751924748907,\n   \"mde80_labelmix_cor_x1.5\": 0.09588932102276713,\n   \"verdict\": \"ADEQUATE\"\n  },\n  {\n   \"cell\": \"EXC\",\n   \"planned_sentences\": 100,\n   \"yield_scenario\": \"E_yield\",\n   \"yield\": 0.64,\n   \"n_usable\": 64.0,\n   \"comparator\": \"nano_orig\",\n   \"se_model_cell\": \"EXC\",\n   \"se\": 0.032554890094023896,\n   \"mde80\": 0.09120529886470966,\n   \"mde80_yield_band\": [\n    0.08472989813143465,\n    0.09941423674703243\n   ],\n   \"mde80_one_sided\": 0.0809469158059248,\n   \"power_at_0.05\": 0.33574775079456265,\n   \"power_at_0.069\": 0.56337562372245,\n   \"power_at_0.099\": 0.8601634103676254,\n   \"power_at_0.1\": 0.8668817223724743,\n   \"power_at_0.15\": 0.9959471952840298,\n   \"mde80_labelmix_cor_x0.5\": 0.10149003776482542,\n   \"mde80_labelmix_cor_x1.5\": 0.09682669400963481,\n   \"verdict\": \"ADEQUATE\"\n  },\n  {\n   \"cell\": \"L20\",\n   \"planned_sentences\": 50,\n   \"yield_scenario\": \"E_yield\",\n   \"yield\": 0.5266666666666666,\n   \"n_usable\": 26.333333333333332,\n   \"comparator\": \"flashlite_disg\",\n   \"se_model_cell\": \"L20\",\n   \"se\": 0.06816742027886148,\n   \"mde80\": 0.19097683701015253,\n   \"mde80_yield_band\": [\n    0.1776289049223681,\n    0.207798395454254\n   ],\n   \"mde80_one_sided\": 0.16949657683018932,\n   \"power_at_0.05\": 0.11000984566720307,\n   \"power_at_0.069\": 0.17162830995177086,\n   \"power_at_0.099\": 0.305846848645364,\n   \"power_at_0.1\": 0.31101069655009367,\n   \"power_at_0.15\": 0.5950289342110708,\n   \"mde80_labelmix_cor_x0.5\": 0.23420946276425605,\n   \"mde80_labelmix_cor_x1.5\": 0.18230950880024,\n   \"verdict\": \"UNDERPOWERED\"\n  },\n  {\n   \"cell\": \"L20\",\n   \"planned_sentences\": 50,\n   \"yield_scenario\": \"E_yield\",\n   \"yield\": 0.5266666666666666,\n   \"n_usable\": 26.333333333333332,\n   \"comparator\": \"flashlite_orig\",\n   \"se_model_cell\": \"L20\",\n   \"se\": 0.05732683532856869,\n   \"mde80\": 0.16060601445771433,\n   \"mde80_yield_band\": [\n    0.14928112694593784,\n    0.1748883927092039\n   ],\n   \"mde80_one_sided\": 0.1425417348779073,\n   \"power_at_0.05\": 0.13834786251814457,\n   \"power_at_0.069\": 0.22472292646533,\n   \"power_at_0.099\": 0.4078713568211779,\n   \"power_at_0.1\": 0.4146574821349787,\n   \"power_at_0.15\": 0.7442846690281111,\n   \"mde80_labelmix_cor_x0.5\": 0.19696340640959478,\n   \"mde80_labelmix_cor_x1.5\": 0.15331704129435125,\n   \"verdict\": \"UNDERPOWERED\"\n  },\n  {\n   \"cell\": \"L20\",\n   \"planned_sentences\": 50,\n   \"yield_scenario\": \"E_yield\",\n   \"yield\": 0.5266666666666666,\n   \"n_usable\": 26.333333333333332,\n   \"comparator\": \"nano_orig\",\n   \"se_model_cell\": \"L20\",\n   \"se\": 0.06178039659114567,\n   \"mde80\": 0.17308304585891052,\n   \"mde80_yield_band\": [\n    0.16064029309840916,\n    0.18880044726390455\n   ],\n   \"mde80_one_sided\": 0.15361540299711018,\n   \"power_at_0.05\": 0.12493899667542324,\n   \"power_at_0.069\": 0.19958490204159485,\n   \"power_at_0.099\": 0.36035355054601637,\n   \"power_at_0.1\": 0.3664284997414696,\n   \"power_at_0.15\": 0.680104360633116,\n   \"mde80_labelmix_cor_x0.5\": 0.21226494175344154,\n   \"mde80_labelmix_cor_x1.5\": 0.1652278127871073,\n   \"verdict\": \"UNDERPOWERED\"\n  },\n  {\n   \"cell\": \"DT\",\n   \"planned_sentences\": 100,\n   \"yield_scenario\": \"CTRL_yield\",\n   \"yield\": 0.25333333333333335,\n   \"n_usable\": 25.333333333333336,\n   \"comparator\": \"flashlite_disg\",\n   \"se_model_cell\": \"all\",\n   \"se\": 0.08590434912664913,\n   \"mde80\": 0.24066835468483588,\n   \"mde80_yield_band\": [\n    0.2111617394906581,\n    0.2816116910823954\n   ],\n   \"mde80_one_sided\": 0.21359900451312308,\n   \"power_at_0.05\": 0.08411379755316034,\n   \"power_at_0.069\": 0.12368826960364732,\n   \"power_at_0.099\": 0.20968364456134736,\n   \"power_at_0.1\": 0.21305130957855056,\n   \"power_at_0.15\": 0.41533752958280656,\n   \"mde80_labelmix_cor_x0.5\": 0.2807120211322428,\n   \"mde80_labelmix_cor_x1.5\": 0.24215095097587247,\n   \"verdict\": \"UNDERPOWERED\"\n  },\n  {\n   \"cell\": \"DT\",\n   \"planned_sentences\": 100,\n   \"yield_scenario\": \"CTRL_yield\",\n   \"yield\": 0.25333333333333335,\n   \"n_usable\": 25.333333333333336,\n   \"comparator\": \"flashlite_orig\",\n   \"se_model_cell\": \"all\",\n   \"se\": 0.06824799648423967,\n   \"mde80\": 0.1912025781160717,\n   \"mde80_yield_band\": [\n    0.16819504557295623,\n    0.22303665925686886\n   ],\n   \"mde80_one_sided\": 0.16969692753921864,\n   \"power_at_0.05\": 0.10984708581914071,\n   \"power_at_0.069\": 0.17132421801800635,\n   \"power_at_0.099\": 0.3052457665582704,\n   \"power_at_0.1\": 0.31039906518665084,\n   \"power_at_0.15\": 0.5940217320655916,\n   \"mde80_labelmix_cor_x0.5\": 0.22301586853387775,\n   \"mde80_labelmix_cor_x1.5\": 0.1923804489396901,\n   \"verdict\": \"UNDERPOWERED\"\n  },\n  {\n   \"cell\": \"DT\",\n   \"planned_sentences\": 100,\n   \"yield_scenario\": \"CTRL_yield\",\n   \"yield\": 0.25333333333333335,\n   \"n_usable\": 25.333333333333336,\n   \"comparator\": \"nano_orig\",\n   \"se_model_cell\": \"all\",\n   \"se\": 0.0792876769816385,\n   \"mde80\": 0.22213118381027425,\n   \"mde80_yield_band\": [\n    0.19549597861181137,\n    0.2589650652076059\n   ],\n   \"mde80_one_sided\": 0.19714681556422217,\n   \"power_at_0.05\": 0.09186643347424206,\n   \"power_at_0.069\": 0.13791929662065805,\n   \"power_at_0.099\": 0.23843485051079927,\n   \"power_at_0.1\": 0.24235915810153907,\n   \"power_at_0.15\": 0.4728454827878905,\n   \"mde80_labelmix_cor_x0.5\": 0.2590905382867467,\n   \"mde80_labelmix_cor_x1.5\": 0.22349958502642894,\n   \"verdict\": \"UNDERPOWERED\"\n  },\n  {\n   \"cell\": \"DT\",\n   \"planned_sentences\": 100,\n   \"yield_scenario\": \"y0.3\",\n   \"yield\": 0.3,\n   \"n_usable\": 30.0,\n   \"comparator\": \"flashlite_disg\",\n   \"se_model_cell\": \"all\",\n   \"se\": 0.07874777249830155,\n   \"mde80\": 0.22061859539056455,\n   \"mde80_yield_band\": [\n    0.22061859539056455,\n    0.22061859539056455\n   ],\n   \"mde80_one_sided\": 0.19580435663932044,\n   \"power_at_0.05\": 0.09258136514521231,\n   \"power_at_0.069\": 0.1392381128796848,\n   \"power_at_0.099\": 0.24109469650100346,\n   \"power_at_0.1\": 0.24506980330530342,\n   \"power_at_0.15\": 0.47801019798463257,\n   \"mde80_labelmix_cor_x0.5\": 0.25730283476600685,\n   \"mde80_labelmix_cor_x1.5\": 0.2219923666735765,\n   \"verdict\": \"UNDERPOWERED\"\n  },\n  {\n   \"cell\": \"DT\",\n   \"planned_sentences\": 100,\n   \"yield_scenario\": \"y0.3\",\n   \"yield\": 0.3,\n   \"n_usable\": 30.0,\n   \"comparator\": \"flashlite_orig\",\n   \"se_model_cell\": \"all\",\n   \"se\": 0.06267004643453855,\n   \"mde80\": 0.17557547570945653,\n   \"mde80_yield_band\": [\n    0.17557547570945653,\n    0.17557547570945653\n   ],\n   \"mde80_one_sided\": 0.15582749496737605,\n   \"power_at_0.05\": 0.1225903826185647,\n   \"power_at_0.069\": 0.1951814207791105,\n   \"power_at_0.099\": 0.3518754895016439,\n   \"power_at_0.1\": 0.3578149983373706,\n   \"power_at_0.15\": 0.6676829147124524,\n   \"mde80_labelmix_cor_x0.5\": 0.20476999019714287,\n   \"mde80_labelmix_cor_x1.5\": 0.17666876771461962,\n   \"verdict\": \"UNDERPOWERED\"\n  },\n  {\n   \"cell\": \"DT\",\n   \"planned_sentences\": 100,\n   \"yield_scenario\": \"y0.3\",\n   \"yield\": 0.3,\n   \"n_usable\": 30.0,\n   \"comparator\": \"nano_orig\",\n   \"se_model_cell\": \"all\",\n   \"se\": 0.07283073494603064,\n   \"mde80\": 0.20404151044910301,\n   \"mde80_yield_band\": [\n    0.20404151044910301,\n    0.20404151044910301\n   ],\n   \"mde80_one_sided\": 0.18109179151682006,\n   \"power_at_0.05\": 0.10143086260114692,\n   \"power_at_0.069\": 0.15563476549469057,\n   \"power_at_0.099\": 0.27403731170386003,\n   \"power_at_0.1\": 0.2786296290682705,\n   \"power_at_0.15\": 0.5396714586234304,\n   \"mde80_labelmix_cor_x0.5\": 0.2379693287211335,\n   \"mde80_labelmix_cor_x1.5\": 0.2053120577803519,\n   \"verdict\": \"UNDERPOWERED\"\n  },\n  {\n   \"cell\": \"DT\",\n   \"planned_sentences\": 100,\n   \"yield_scenario\": \"y0.5\",\n   \"yield\": 0.5,\n   \"n_usable\": 50.0,\n   \"comparator\": \"flashlite_disg\",\n   \"se_model_cell\": \"all\",\n   \"se\": 0.06054859329899812,\n   \"mde80\": 0.16963204396400708,\n   \"mde80_yield_band\": [\n    0.16963204396400708,\n    0.16963204396400708\n   ],\n   \"mde80_one_sided\": 0.15055255507807414,\n   \"power_at_0.05\": 0.12835932273052947,\n   \"power_at_0.069\": 0.20599878149696027,\n   \"power_at_0.099\": 0.3726232270486424,\n   \"power_at_0.1\": 0.3788897700065658,\n   \"power_at_0.15\": 0.6975563080281098,\n   \"mde80_labelmix_cor_x0.5\": 0.19779902474114544,\n   \"mde80_labelmix_cor_x1.5\": 0.17071292279092393,\n   \"verdict\": \"UNDERPOWERED\"\n  },\n  {\n   \"cell\": \"DT\",\n   \"planned_sentences\": 100,\n   \"yield_scenario\": \"y0.5\",\n   \"yield\": 0.5,\n   \"n_usable\": 50.0,\n   \"comparator\": \"flashlite_orig\",\n   \"se_model_cell\": \"all\",\n   \"se\": 0.04843760231396959,\n   \"mde80\": 0.13570207064365172,\n   \"mde80_yield_band\": [\n    0.13570207064365172,\n    0.13570207064365172\n   ],\n   \"mde80_one_sided\": 0.12043888045776323,\n   \"power_at_0.05\": 0.17677950271369386,\n   \"power_at_0.069\": 0.2961690628769523,\n   \"power_at_0.099\": 0.5334330900487022,\n   \"power_at_0.1\": 0.5416326749277006,\n   \"power_at_0.15\": 0.8721898151249949,\n   \"mde80_labelmix_cor_x0.5\": 0.15823506338439025,\n   \"mde80_labelmix_cor_x1.5\": 0.13656675099236354,\n   \"verdict\": \"MARGINAL\"\n  },\n  {\n   \"cell\": \"DT\",\n   \"planned_sentences\": 100,\n   \"yield_scenario\": \"y0.5\",\n   \"yield\": 0.5,\n   \"n_usable\": 50.0,\n   \"comparator\": \"nano_orig\",\n   \"se_model_cell\": \"all\",\n   \"se\": 0.05634520120374588,\n   \"mde80\": 0.1578558828040155,\n   \"mde80_yield_band\": [\n    0.1578558828040155,\n    0.1578558828040155\n   ],\n   \"mde80_one_sided\": 0.14010092630430251,\n   \"power_at_0.05\": 0.14173048163541874,\n   \"power_at_0.069\": 0.23105712362241548,\n   \"power_at_0.099\": 0.41959186680804406,\n   \"power_at_0.1\": 0.4265400252782146,\n   \"power_at_0.15\": 0.7587218622851306,\n   \"mde80_labelmix_cor_x0.5\": 0.1840674611862364,\n   \"mde80_labelmix_cor_x1.5\": 0.15886172508145294,\n   \"verdict\": \"UNDERPOWERED\"\n  },\n  {\n   \"cell\": \"DT\",\n   \"planned_sentences\": 100,\n   \"yield_scenario\": \"y0.8\",\n   \"yield\": 0.8,\n   \"n_usable\": 80.0,\n   \"comparator\": \"flashlite_disg\",\n   \"se_model_cell\": \"all\",\n   \"se\": 0.04754345424139865,\n   \"mde80\": 0.13319703862073276,\n   \"mde80_yield_band\": [\n    0.13319703862073276,\n    0.13319703862073276\n   ],\n   \"mde80_one_sided\": 0.11821560375372925,\n   \"power_at_0.05\": 0.18186132370875202,\n   \"power_at_0.069\": 0.3054952485389628,\n   \"power_at_0.099\": 0.5486857540128002,\n   \"power_at_0.1\": 0.5570029805997172,\n   \"power_at_0.15\": 0.8839651716565655,\n   \"mde80_labelmix_cor_x0.5\": 0.1552966741984299,\n   \"mde80_labelmix_cor_x1.5\": 0.1340566552989307,\n   \"verdict\": \"MARGINAL\"\n  },\n  {\n   \"cell\": \"DT\",\n   \"planned_sentences\": 100,\n   \"yield_scenario\": \"y0.8\",\n   \"yield\": 0.8,\n   \"n_usable\": 80.0,\n   \"comparator\": \"flashlite_orig\",\n   \"se_model_cell\": \"all\",\n   \"se\": 0.038216050271621414,\n   \"mde80\": 0.10706552153563664,\n   \"mde80_yield_band\": [\n    0.10706552153563664,\n    0.10706552153563664\n   ],\n   \"mde80_one_sided\": 0.09502324826892279,\n   \"power_at_0.05\": 0.2573253705368387,\n   \"power_at_0.069\": 0.43863145613383125,\n   \"power_at_0.099\": 0.7358393371475671,\n   \"power_at_0.1\": 0.7443251792290112,\n   \"power_at_0.15\": 0.9752979976585215,\n   \"mde80_labelmix_cor_x0.5\": 0.12482949762230439,\n   \"mde80_labelmix_cor_x1.5\": 0.10775649266326101,\n   \"verdict\": \"MARGINAL\"\n  },\n  {\n   \"cell\": \"DT\",\n   \"planned_sentences\": 100,\n   \"yield_scenario\": \"y0.8\",\n   \"yield\": 0.8,\n   \"n_usable\": 80.0,\n   \"comparator\": \"nano_orig\",\n   \"se_model_cell\": \"all\",\n   \"se\": 0.04449448493512202,\n   \"mde80\": 0.12465509128178802,\n   \"mde80_yield_band\": [\n    0.12465509128178802,\n    0.12465509128178802\n   ],\n   \"mde80_one_sided\": 0.11063441822316193,\n   \"power_at_0.05\": 0.20151298436761222,\n   \"power_at_0.069\": 0.34119277980962254,\n   \"power_at_0.099\": 0.6045071591609608,\n   \"power_at_0.1\": 0.6131373791385799,\n   \"power_at_0.15\": 0.9209131203018313,\n   \"mde80_labelmix_cor_x0.5\": 0.14533747370378944,\n   \"mde80_labelmix_cor_x1.5\": 0.12545958060525736,\n   \"verdict\": \"MARGINAL\"\n  }\n ],\n \"n_needed\": {\n  \"L25\": {\n   \"flashlite_disg\": {\n    \"usable_for_mde_0.069\": 326.416175274051,\n    \"usable_for_mde_0.10\": 155.9973204457915,\n    \"planned_for_mde_0.069\": 882.2058791190568,\n    \"planned_for_mde_0.10\": 421.6143795832203\n   },\n   \"flashlite_orig\": {\n    \"usable_for_mde_0.069\": 199.34800212652286,\n    \"usable_for_mde_0.10\": 98.0583353476636,\n    \"planned_for_mde_0.069\": 538.7783841257375,\n    \"planned_for_mde_0.10\": 265.0225279666584\n   },\n   \"nano_orig\": {\n    \"usable_for_mde_0.069\": 354.2621191376214,\n    \"usable_for_mde_0.10\": 172.76788335001254,\n    \"planned_for_mde_0.069\": 957.4651868584363,\n    \"planned_for_mde_0.10\": 466.94022527030415\n   }\n  },\n  \"L20\": {\n   \"flashlite_disg\": {\n    \"usable_for_mde_0.069\": 192.05017772413476,\n    \"usable_for_mde_0.10\": 93.08854815314308,\n    \"planned_for_mde_0.069\": 364.65223618506604,\n    \"planned_for_mde_0.10\": 176.75040788571474\n   },\n   \"flashlite_orig\": {\n    \"usable_for_mde_0.069\": 134.91930176840899,\n    \"usable_for_mde_0.10\": 65.83035665248299,\n    \"planned_for_mde_0.069\": 256.175889433688,\n    \"planned_for_mde_0.10\": 124.99434807433481\n   },\n   \"nano_orig\": {\n    \"usable_for_mde_0.069\": 150.51477213207343,\n    \"usable_for_mde_0.10\": 74.49334291551305,\n    \"planned_for_mde_0.069\": 285.78754202292424,\n    \"planned_for_mde_0.10\": 141.44305616869568\n   }\n  },\n  \"EXC\": {\n   \"flashlite_disg\": {\n    \"usable_for_mde_0.069\": 155.15612166522348,\n    \"usable_for_mde_0.10\": 74.91034344865612,\n    \"planned_for_mde_0.069\": 242.43144010191168,\n    \"planned_for_mde_0.10\": 117.04741163852519\n   },\n   \"flashlite_orig\": {\n    \"usable_for_mde_0.069\": 109.2773704645141,\n    \"usable_for_mde_0.10\": 52.282127413677834,\n    \"planned_for_mde_0.069\": 170.74589135080328,\n    \"planned_for_mde_0.10\": 81.69082408387162\n   },\n   \"nano_orig\": {\n    \"usable_for_mde_0.069\": 110.93160541737636,\n    \"usable_for_mde_0.10\": 53.37819939047894,\n    \"planned_for_mde_0.069\": 173.33063346465056,\n    \"planned_for_mde_0.10\": 83.40343654762334\n   }\n  },\n  \"long\": {\n   \"flashlite_disg\": {\n    \"usable_for_mde_0.069\": 237.24898963798333,\n    \"usable_for_mde_0.10\": 115.338761586516,\n    \"planned_for_mde_0.069\": null,\n    \"planned_for_mde_0.10\": null\n   },\n   \"flashlite_orig\": {\n    \"usable_for_mde_0.069\": 168.98481322765102,\n    \"usable_for_mde_0.10\": 81.99953944402142,\n    \"planned_for_mde_0.069\": null,\n    \"planned_for_mde_0.10\": null\n   },\n   \"nano_orig\": {\n    \"usable_for_mde_0.069\": 228.03738900804342,\n    \"usable_for_mde_0.10\": 109.52516803109947,\n    \"planned_for_mde_0.069\": null,\n    \"planned_for_mde_0.10\": null\n   }\n  }\n },\n \"criterion_c_effects\": {\n  \"conservative\": {\n   \"value\": 0.069,\n   \"what\": \"observed E L25 pooled Delta c_score_align - flash-lite disguised (exp 6 tables_T1.md)\"\n  },\n  \"optimistic\": {\n   \"value\": 0.05788390284067524,\n   \"value_3pool\": 0.03988884314532737,\n   \"n\": 869,\n   \"what\": \"Part-1 graded c_vres (label-free liberal-vocabulary counterfactual) - flash-lite disguised on E L25 consensus-scorable rows\"\n  }\n },\n \"rcomp_free\": {\n  \"score_correlation_FREE_tierA\": 0.07445407611393627,\n  \"n_FREE_tierA\": 417,\n  \"icc_SIG_residual\": 0.4981780519323534,\n  \"auroc_assumed\": {\n   \"c_align_FREE_tierA\": 0.8,\n   \"judge\": 0.58\n  },\n  \"observed_FREE_tierA\": {\n   \"auroc_c_align\": 0.7732988802756244,\n   \"auroc_judge_cheap_disg\": 0.5639965546942292\n  },\n  \"scenarios\": [\n   {\n    \"n_err\": 420,\n    \"n_cor\": 34,\n    \"n_sent\": 221,\n    \"rows_per_sentence\": 2.0542986425339365,\n    \"design_effect\": 1.5252284438924812,\n    \"mde80_analytic\": 0.19179987691579534,\n    \"mde80_empirical_SIG\": 0.16179198302742362,\n    \"sig_delta_mean\": 0.3904300887021475\n   },\n   {\n    \"n_err\": 420,\n    \"n_cor\": 100,\n    \"n_sent\": 221,\n    \"rows_per_sentence\": 2.3529411764705883,\n    \"design_effect\": 1.6740055996731842,\n    \"mde80_analytic\": 0.12956165056775884,\n    \"mde80_empirical_SIG\": 0.1122005289432693,\n    \"sig_delta_mean\": 0.39351523809523814\n   },\n   {\n    \"n_err\": 420,\n    \"n_cor\": 200,\n    \"n_sent\": 221,\n    \"rows_per_sentence\": 2.8054298642533935,\n    \"design_effect\": 1.8994255326742489,\n    \"mde80_analytic\": 0.11025422990170483,\n    \"mde80_empirical_SIG\": 0.09274157079224399,\n    \"sig_delta_mean\": 0.39361950396825396\n   },\n   {\n    \"n_err\": 420,\n    \"n_cor\": 400,\n    \"n_sent\": 221,\n    \"rows_per_sentence\": 3.7104072398190047,\n    \"design_effect\": 2.350265398676379,\n    \"mde80_analytic\": 0.10383428515140421,\n    \"mde80_empirical_SIG\": 0.08527635823517321,\n    \"sig_delta_mean\": 0.3897691071428572\n   },\n   {\n    \"n_err\": 420,\n    \"n_cor\": 800,\n    \"n_sent\": 221,\n    \"rows_per_sentence\": 5.520361990950226,\n    \"design_effect\": 3.2519451306806384,\n    \"mde80_analytic\": 0.10942535872325079,\n    \"mde80_empirical_SIG\": 0.07600239210990603,\n    \"sig_delta_mean\": 0.3874858085317461\n   },\n   {\n    \"n_err\": 600,\n    \"n_cor\": 34,\n    \"n_sent\": 221,\n    \"rows_per_sentence\": 2.8687782805429864,\n    \"design_effect\": 1.930984323294398,\n    \"mde80_analytic\": 0.2119654330898864,\n    \"mde80_empirical_SIG\": 0.1651442162649592,\n    \"sig_delta_mean\": 0.38401119281045754\n   },\n   {\n    \"n_err\": 600,\n    \"n_cor\": 100,\n    \"n_sent\": 221,\n    \"rows_per_sentence\": 3.167420814479638,\n    \"design_effect\": 2.079761479075101,\n    \"mde80_analytic\": 0.13824424657548062,\n    \"mde80_empirical_SIG\": 0.11548453789810326,\n    \"sig_delta_mean\": 0.3941173055555556\n   },\n   {\n    \"n_err\": 600,\n    \"n_cor\": 200,\n    \"n_sent\": 221,\n    \"rows_per_sentence\": 3.6199095022624435,\n    \"design_effect\": 2.305181412076166,\n    \"mde80_analytic\": 0.11325479491977979,\n    \"mde80_empirical_SIG\": 0.08651686791551257,\n    \"sig_delta_mean\": 0.3880717361111111\n   },\n   {\n    \"n_err\": 600,\n    \"n_cor\": 400,\n    \"n_sent\": 221,\n    \"rows_per_sentence\": 4.524886877828054,\n    \"design_effect\": 2.7560212780782956,\n    \"mde80_analytic\": 0.10170061908891778,\n    \"mde80_empirical_SIG\": 0.07867653690148052,\n    \"sig_delta_mean\": 0.3916515208333333\n   },\n   {\n    \"n_err\": 600,\n    \"n_cor\": 800,\n    \"n_sent\": 221,\n    \"rows_per_sentence\": 6.334841628959276,\n    \"design_effect\": 3.657701010082555,\n    \"mde80_analytic\": 0.10206483378137968,\n    \"mde80_empirical_SIG\": 0.07422019330814635,\n    \"sig_delta_mean\": 0.391324625\n   },\n   {\n    \"n_err\": 900,\n    \"n_cor\": 34,\n    \"n_sent\": 221,\n    \"rows_per_sentence\": 4.226244343891403,\n    \"design_effect\": 2.607244122297593,\n    \"mde80_analytic\": 0.24277164650356262,\n    \"mde80_empirical_SIG\": 0.16274797563041987,\n    \"sig_delta_mean\": 0.38715577342047935\n   },\n   {\n    \"n_err\": 900,\n    \"n_cor\": 100,\n    \"n_sent\": 221,\n    \"rows_per_sentence\": 4.524886877828054,\n    \"design_effect\": 2.7560212780782956,\n    \"mde80_analytic\": 0.153394598545664,\n    \"mde80_empirical_SIG\": 0.12286012945236424,\n    \"sig_delta_mean\": 0.39073294444444445\n   },\n   {\n    \"n_err\": 900,\n    \"n_cor\": 200,\n    \"n_sent\": 221,\n    \"rows_per_sentence\": 4.97737556561086,\n    \"design_effect\": 2.9814412110793604,\n    \"mde80_analytic\": 0.12105041816521246,\n    \"mde80_empirical_SIG\": 0.08534032631845342,\n    \"sig_delta_mean\": 0.38889761111111115\n   },\n   {\n    \"n_err\": 900,\n    \"n_cor\": 400,\n    \"n_sent\": 221,\n    \"rows_per_sentence\": 5.882352941176471,\n    \"design_effect\": 3.4322810770814907,\n    \"mde80_analytic\": 0.10321962021907008,\n    \"mde80_empirical_SIG\": 0.07892078312035407,\n    \"sig_delta_mean\": 0.3862252685185185\n   },\n   {\n    \"n_err\": 900,\n    \"n_cor\": 800,\n    \"n_sent\": 221,\n    \"rows_per_sentence\": 7.6923076923076925,\n    \"design_effect\": 4.33396080908575,\n    \"mde80_analytic\": 0.09763469588111369,\n    \"mde80_empirical_SIG\": 0.07068512570103713,\n    \"sig_delta_mean\": 0.3911400254629629\n   }\n  ],\n  \"caveat\": \"order-of-magnitude guide only: analytic Hanley-McNeil + SIG-row resampling as an upper-variance proxy; no FREE-labelled data at these counts exist\"\n },\n \"recommendation\": [\n  \"L25 planned 250 -> ~92 usable: MDE80 0.130, power@0.069 0.32 => MARGINAL\",\n  \"L25 planned 300 -> ~111 usable: MDE80 0.119, power@0.069 0.37 => MARGINAL\",\n  \"L25 planned 350 -> ~130 usable: MDE80 0.110, power@0.069 0.42 => MARGINAL\",\n  \"L25 planned 400 -> ~148 usable: MDE80 0.103, power@0.069 0.47 => MARGINAL\",\n  \"To detect +0.069 on L25 at 80% power: ~326 usable sentences = ~882 planned at E's yield; for MDE 0.10: ~156 usable = ~422 planned.\",\n  \"Long pool (L25+L20+EXC) needs ~237 usable sentences for MDE 0.069: pre-declaring the long pool as criterion (c)'s primary cell is the cheaper route.\"\n ]\n}", "numLines": 1310, "startLine": 1, "totalLines": 1310}}
```

### [32] TOOL CALL — WebSearch · 2026-09-24 10:59:44 UTC

```
WMT 2024 metrics shared task findings meta-evaluation soft pairwise accuracy PERM-BOTH significance clusters
```

### [33] TOOL CALL — WebFetch · 2026-09-24 10:59:44 UTC

```
URL: https://openrouter.ai/deepseek/deepseek-v3.2
Prompt: What are the input and output prices per million tokens for deepseek/deepseek-v3.2? Does it support reasoning toggle? Quote the numbers.
```

### [34] TOOL CALL — WebFetch · 2026-09-24 10:59:44 UTC

```
URL: https://openrouter.ai/google/gemini-3.1-pro-preview
Prompt: What are the input and output prices per million tokens? Is reasoning mandatory, and can reasoning effort be set low? Quote the numbers and model id.
```

### [35] TOOL RESULT — WebFetch · 2026-09-24 10:59:46 UTC

```
{"bytes": 4276, "code": 200, "codeText": "OK", "result": "Based on the provided content, I cannot answer your question. The documentation does not include pricing information per million tokens for deepseek/deepseek-v3.2, nor does it specify whether reasoning toggle is supported.\n\nThe page mentions that `\"reasoning: optional — accepted by this model\"` as a request field, which suggests the model accepts reasoning parameters, but no detailed documentation about how this feature works is provided in this excerpt.\n\nFor pricing details, you would need to visit the model page at https://openrouter.ai/deepseek/deepseek-v3.2.", "durationMs": 2727, "url": "https://openrouter.ai/deepseek/deepseek-v3.2"}
```

### [36] TOOL RESULT — WebFetch · 2026-09-24 10:59:46 UTC

```
{"bytes": 3683, "code": 200, "codeText": "OK", "result": "Based on the provided content, I cannot answer your question about input and output prices per million tokens or whether reasoning is mandatory with adjustable effort levels.\n\nThe document does not include pricing information. While it mentions that the model accepts optional parameters like `reasoning`, `reasoning_effort`, and `max_tokens`, it only states these are \"optional — accepted by this model\" without specifying whether reasoning is required or details about effort level settings.\n\nFor pricing and detailed parameter specifications, you would need to consult the full API reference at https://openrouter.ai/docs/api/api-reference/chat/create-a-chat-completion or the model's page at https://openrouter.ai/google/gemini-3.1-pro-preview.", "durationMs": 2634, "url": "https://openrouter.ai/google/gemini-3.1-pro-preview"}
```

### [37] TOOL RESULT — WebSearch · 2026-09-24 11:00:00 UTC

```
{"query": "WMT 2024 metrics shared task findings meta-evaluation soft pairwise accuracy PERM-BOTH significance clusters", "results": [{"tool_use_id": "srvtoolu_01SC9QLDwA2cRCANnxR9ZFZK", "content": [{"title": "Which Metrics Save the Most Human Annotation? Prediction-Powered Evaluation and Meta-Evaluation", "url": "https://arxiv.org/pdf/2608.26638"}, {"title": "Evaluating WMT 2024 Metrics Shared Task Submissions on AfriMTE (the African Challenge Set) - ACL Anthology", "url": "https://aclanthology.org/2024.wmt-1.36/"}, {"title": "Feeding Two Birds or Favoring One? Adequacy-Fluency Tradeoffs in Evaluation and Meta-Evaluation of Machine Translation", "url": "https://arxiv.org/pdf/2509.20287"}, {"title": "Mind Which Bird You Favour: Parameterizing Adequacy-Fluency Balance in Meta-Evaluation of Machine Translation", "url": "https://arxiv.org/pdf/2609.14795"}, {"title": "MetricX-24: The Google Submission to the WMT 2024Metrics Shared Task", "url": "https://arxiv.org/html/2410.03983"}, {"title": "Dynamic Meta-Metrics: Source-Sentence Conditioned Weighting for MT Evaluation", "url": "https://arxiv.org/pdf/2605.09098"}, {"title": "MetricX-24: The Google Submission to the WMT 2024 Metrics Shared Task", "url": "https://arxiv.org/pdf/2410.03983"}, {"title": "Improving Statistical Significance in Human Evaluation of Automatic Metrics via Soft Pairwise Accuracy", "url": "https://arxiv.org/pdf/2409.09598"}, {"title": "Pitfalls and Outlooks in Using COMET", "url": "https://arxiv.org/pdf/2408.15366"}, {"title": "Contextual Metric Meta-Evaluation by Measuring Local Metric Accuracy", "url": "https://arxiv.org/pdf/2503.19828"}]}, "Let me search more specifically for the WMT 2024 metrics shared task results paper with the specific metrics you mentioned.", {"tool_use_id": "srvtoolu_01YTVqdkBngSAjV95ajKxPPu", "content": [{"title": "(PDF) Are LLMs Breaking MT Metrics? Results of the WMT24 Metrics Shared Task", "url": "https://www.researchgate.net/publication/386203978_Are_LLMs_Breaking_MT_Metrics_Results_of_the_WMT24_Metrics_Shared_Task"}, {"title": "MetaMetrics-MT: Tuning Meta-Metrics for Machine Translation via Human Preference Calibration", "url": "https://arxiv.org/pdf/2411.00390"}, {"title": "Adding Chocolate to Mint: Mitigating Metric Interference in Machine Translation", "url": "https://arxiv.org/pdf/2503.08327"}, {"title": "Are LLMs Breaking MT Metrics? Results of the WMT24 Metrics Shared Task. Authors", "url": "https://repository.tilburguniversity.edu/server/api/core/bitstreams/b51a379b-dc19-44a7-bf79-1f4f56d37e52/content"}, {"title": "Improving Statistical Significance in Human Evaluation of Automatic Metrics via Soft Pairwise Accuracy", "url": "https://arxiv.org/pdf/2409.09598"}, {"title": "Are LLMs Breaking MT Metrics? Results of the WMT24 Metrics Shared Task", "url": "https://research.google/pubs/are-llms-breaking-mt-metrics-results-of-the-wmt24-metrics-shared-task/"}, {"title": "GitHub - google-research/metricx · GitHub", "url": "https://github.com/google-research/metricx"}, {"title": "Training and Meta-Evaluating Machine Translation Evaluation Metrics at the Paragraph Level", "url": "https://arxiv.org/pdf/2308.13506"}, {"title": "Are LLMs Breaking MT Metrics? Results of the WMT24 ...", "url": "https://aclanthology.org/2024.wmt-1.2.pdf"}, {"title": "Are LLMs Breaking MT Metrics? Results of the WMT24 Metrics ...", "url": "https://www2.statmt.org/wmt24/pdf/2024.wmt-1.2.pdf"}]}, "Now let me search specifically for PERM-BOTH and significance clusters in the WMT24 metrics task.", {"tool_use_id": "srvtoolu_01FEvswJY2LwQE6Akzt2ZJSG", "content": [{"title": "(PDF) Are LLMs Breaking MT Metrics? Results of the WMT24 Metrics Shared Task", "url": "https://www.researchgate.net/publication/386203978_Are_LLMs_Breaking_MT_Metrics_Results_of_the_WMT24_Metrics_Shared_Task"}, {"title": "Improving Statistical Significance in Human Evaluation of Automatic Metrics via Soft Pairwise Accuracy", "url": "https://arxiv.org/pdf/2409.09598"}, {"title": "Are LLMs Breaking MT Metrics? Results of the WMT24 Metrics Shared Task. Authors", "url": "https://repository.tilburguniversity.edu/server/api/core/bitstreams/b51a379b-dc19-44a7-bf79-1f4f56d37e52/content"}, {"title": "Are LLMs Breaking MT Metrics? Results of the WMT24 ...", "url": "https://aclanthology.org/2024.wmt-1.2.pdf"}, {"title": "Are LLMs Breaking MT Metrics? Results of the WMT24 Metrics ...", "url": "https://www2.statmt.org/wmt24/pdf/2024.wmt-1.2.pdf"}, {"title": "Pairwise Adjusted Mutual Information", "url": "https://arxiv.org/pdf/2103.12641"}, {"title": "Utilizing machine learning and digital embedding processes to generate digital maps of biology and user interfaces for evaluating map efficacy", "url": "https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12073638"}, {"title": "Utilizing machine learning and digital embedding processes to generate digital maps of biology and user interfaces for evaluating map efficacy", "url": "https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12079992"}, {"title": "Probabilistic Clustering of Sequences: Inferring new bacterial regulons by comparative genomics", "url": "https://arxiv.org/pdf/physics/0206045"}, {"title": "AgentCollabBench: Diagnosing When Good Agents Make Bad Collaborators", "url": "https://arxiv.org/pdf/2605.08647"}]}, "Let me search more specifically for the main WMT24 metrics shared task results paper to find the PERM-BOTH methodology.", {"tool_use_id": "srvtoolu_01FpNEweDRyE7qbkz6k14iJM", "content": [{"title": "[PDF] Are LLMs Breaking MT Metrics? Results of the WMT24 Metrics Shared Task | Semantic Scholar", "url": "https://www.semanticscholar.org/paper/Are-LLMs-Breaking-MT-Metrics-Results-of-the-WMT24-Freitag-Mathur/9f8cc0001d433aa75ec5dbb2605ca9400cb57369"}, {"title": "Are LLMs breaking MT metrics? results of the WMT24 metrics shared task", "url": "https://it.pt/Publications/PaperConference/41443"}, {"title": "Are LLMs Breaking MT Metrics? Results of the WMT24 Metrics Shared Task. - Tilburg University Research Portal", "url": "https://research.tilburguniversity.edu/en/publications/are-llms-breaking-mt-metrics-results-of-the-wmt24-metrics-shared-/"}, {"title": "Are LLMs Breaking MT Metrics? Results of the WMT24 Metrics Shared Task - University of Lisbon", "url": "https://researchportal.ulisboa.pt/en/publications/are-llms-breaking-mt-metrics-results-of-the-wmt24-metrics-shared-/"}, {"title": "Are LLMs Breaking MT Metrics? Results of the WMT24 Metrics Shared Task - ACL Anthology", "url": "https://aclanthology.org/2024.wmt-1.2/"}, {"title": "Are LLMs Breaking MT Metrics? Results of the WMT24 Metrics Shared Task - University of Haifa", "url": "https://cris.haifa.ac.il/en/publications/are-llms-breaking-mt-metrics-results-of-the-wmt24-metrics-shared--2/"}, {"title": "Are LLMs Breaking MT Metrics? Results of the WMT24 Metrics Shared Task", "url": "https://research.google/pubs/are-llms-breaking-mt-metrics-results-of-the-wmt24-metrics-shared-task/"}, {"title": "Remedy-R: Generative Reasoning for Machine Translation Evaluation without Error Annotations", "url": "https://arxiv.org/pdf/2512.18906"}, {"title": "Improving Statistical Significance in Human Evaluation of Automatic Metrics via Soft Pairwise Accuracy", "url": "https://arxiv.org/pdf/2409.09598"}]}, "Let me search for Thompson et al. 2024 soft pairwise accuracy PERM-BOTH to find the specific methodology paper.", {"tool_use_id": "srvtoolu_01TuvWy3eQDxPkjUf1tFFomc", "content": [{"title": "Brian Thompson on alphaXiv", "url": "https://www.alphaxiv.org/@brian-thompson"}, {"title": "Brian Thompson's research works | Amazon, Seattle and other places", "url": "https://www.researchgate.net/scientific-contributions/Brian-Thompson-2107495353"}, {"title": "GreekBarBench: A Challenging Benchmark for Free-Text Legal Reasoning and Citations", "url": "https://arxiv.org/pdf/2505.17267"}, {"title": "Brian Thompson", "url": "https://thompsonb.github.io/"}, {"title": "Improving Statistical Significance in Human Evaluation of Automatic Metrics via Soft Pairwise Accuracy", "url": "https://arxiv.org/pdf/2409.09598"}, {"title": "A Finite Time Analysis of Thompson Sampling for Bayesian ...", "url": "https://arxiv.org/pdf/2604.25025"}, {"title": "Pairwise Logical Selection of Enthymeme Completions under Semantic-Link Uncertainty", "url": "https://arxiv.org/pdf/2608.18820"}, {"title": "The Comparative Trap: Pairwise Comparisons Amplifies Biased Preferences of LLM Evaluators", "url": "https://arxiv.org/pdf/2406.12319"}, {"title": "Generating and Detecting True Ambiguity: A Forgotten Danger in DNN Supervision Testing", "url": "https://arxiv.org/pdf/2207.10495"}, {"title": "Variance-sensitive Thompson sampling for generalised linear bandits, revisited", "url": "https://arxiv.org/pdf/2606.00431"}]}, "Based on my search results, I can now provide you with information about the WMT 2024 metrics shared task findings related to soft pairwise accuracy and significance clustering.\n\n## WMT 2024 Metrics Shared Task: Key Findings\n\nThe WMT24 Metrics Shared Task evaluated the performance of automatic metrics for machine translation (MT), with a major focus on LLM-based translations that were generated as part of the WMT24 General MT Translation Task.\n\n### Soft Pairwise Accuracy (SPA)\n\nSoft Pairwise Accuracy (SPA) is a new meta-metric that builds on Pairwise Accuracy (PA) but incorporates the statistical significance of both the human judgments and the metric scores. SPA was selected as the official system-level metric for the 2024 WMT Metrics Shared Task.\n\nSPA is more stable than PA with respect to changes in the number of systems/segments used for evaluation and is more discriminative than PA, producing more statistically significant comparisons between metrics.\n\n### Significance Clustering and PERM-BOTH\n\nStatistical significance of metric comparisons is computed using the PERM-INPUTS method. Significance clusters are greedily computed by starting with the highest scoring metric and assigning rank 1 to all metrics until encountering the first metric that is statistically significantly different from any previous metric; that metric is assigned rank 2, and the process repeats until all metrics have been assigned a rank.\n\nSPA increases the number of statistically significant pairwise comparisons by 31% and the number of significance clusters by 40% compared to PA, while producing similar scores for each metric.\n\n### Meta-Evaluation Refinement\n\nThe meta-evaluation procedure was refined to better reflect real-world usage of MT metrics, focusing on pairwise accuracy at both the system and segment levels."], "durationSeconds": 17.677665542000003, "searchCount": 5}
```

### [38] ASSISTANT · 2026-09-24 11:00:06 UTC

```
Reading done: I have E2's frozen selection rule, costs and power file. Next I'll find the frozen judge prompt and the exp-5 code paths, then write the plan.
```

### [39] TOOL CALL — Grep · 2026-09-24 11:00:06 UTC

```
Pattern: "rubric|RUBRIC_A|flash-lite"
```

### [40] TOOL CALL — Glob · 2026-09-24 11:00:06 UTC

```
Pattern: "iter_2/gen_art/gen_art_experiment_5/src/*.py"
```

### [41] TOOL RESULT — Glob · 2026-09-24 11:00:08 UTC

```
{"filenames": ["/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/src/data_views.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/src/run_api_E.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/src/__init__.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/src/local_judge_E.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/src/pool_scoring.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/src/peer_text.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/src/screen_fit.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/src/score_E.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/src/posthoc_nf_fusion.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/src/analyse_E.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/src/write_deviations.py"], "durationMs": 1681, "numFiles": 11, "truncated": false, "totalMatches": 11, "countIsComplete": true}
```

### [42] TOOL RESULT — Grep · 2026-09-24 11:00:10 UTC

```
{"mode": "files_with_matches", "filenames": ["/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_strat/gen_strat_1/build_strategy.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/upd_hypo/upd_hypo/build_out.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/review_report/review_report/audit/write_review.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/src/csc_tables.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/audit/rederive.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_experiment_9/src/report.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/src/t8_part4.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_experiment_9/src/analyse.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/src/t8_part3.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_experiment_9/vendor/e8src/analyse_perturb.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_experiment_9/vendor/e8src/vendor_a/fol_triage.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_experiment_9/vendor/e8src/vendor_a/llm.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_experiment_9/vendor/e8src/vendor_c/consensus.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_experiment_9/vendor/e8src/vendor_c/peers.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_experiment_9/vendor/e8src/vendor_d/judges.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_experiment_9/vendor/e8src/write_deviations.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_experiment_9/vendor/e8src/write_tables.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_experiment_9/vendor/e8src/freeze_prereg_perturb.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_experiment_9/vendor/e8src/local_judge_E.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_experiment_9/vendor/e8src/perturb_gpu.py"], "numFiles": 20, "totalFiles": 120, "appliedLimit": 20}
```

### [43] TOOL CALL — Grep · 2026-09-24 11:00:16 UTC

```
Pattern: "RUBRIC|rubric_A|def |MODEL|flash-lite|nano"
```

### [44] TOOL RESULT — Grep · 2026-09-24 11:00:16 UTC

```
{"mode": "content", "numFiles": 0, "filenames": [], "content": "19:PRIMARY = \"google/gemini-2.5-flash-lite\"\n20:PRIMARY_FALLBACKS = [\"qwen/qwen3-30b-a3b-instruct-2507\"]  # gemini-2.0-flash-lite-001 is no longer listed on OpenRouter\n21:SECONDARY = \"openai/gpt-4.1-nano\"\n23:RUBRIC_A = (\"You check whether a first-order logic formula faithfully expresses the meaning of an English sentence. \"\n32:RUBRIC_B = RUBRIC_A + \" \" + CENSUS\n47:PROMPT_SHA = {k: sha1(v) for k, v in {\"RUBRIC_A\": RUBRIC_A, \"RUBRIC_B\": RUBRIC_B, \"USER_JSON\": USER_JSON,\n55:def _load_cache() -> dict:\n69:def _ckey(component, model, messages, params) -> str:\n73:async def cached_call(b: Budget, *, component: str, model: str, messages: list[dict], max_tokens: int, item_id: str,\n94:def parse_judge_json(text: str) -> dict | None:\n126:def p_yes_from_logprobs(lp) -> float | None:\n141:def clean_verbalisation(text: str) -> tuple[str, bool]:\n163:def extract_formula(text: str) -> str | None:\n176:async def judge_json(b: Budget, *, component: str, model: str, rubric: str, text: str, fol: str | None, item_id: str,\n204:async def judge_logprob(b: Budget, *, component: str, model: str, rubric: str, text: str, fol: str | None,\n227:async def simple_text(b: Budget, *, component: str, model: str, prompt: str, item_id: str, max_tokens: int) -> dict:\n241:async def gather_limited(coros, label: str = \"\"):", "numLines": 17, "totalLines": 17}
```

### [45] TOOL CALL — Grep · 2026-09-24 11:00:16 UTC

```
Pattern: "^def |judge|S4"
```

### [46] TOOL RESULT — Grep · 2026-09-24 11:00:16 UTC

```
{"mode": "content", "numFiles": 0, "filenames": [], "content": "6:  2. judge_cheap_disg: exp D judge_json(RUBRIC_A, USER_JSON_A, google/gemini-2.5-flash-lite, max_tokens=150) on the exp-D\n8:  3. judge_cheap_orig: same on the original (text, fol).\n10:Unparseable candidates are never sent to the judge (the scorer sets them to 1.0 = flagged, like every metric).\n34:from vendor_d import judges as J  # noqa: E402\n40:VB.CAPS = {\"judge_cheap_primary\": 2.4, \"setup_probe\": 0.05}\n50:def key_remaining() -> float | None:\n60:def parseable(s: str) -> bool:\n70:def jl(p: Path) -> list[dict]:\n74:def build_disguise(rows: list[dict]) -> dict:\n127:async def judge_phase(units: list[tuple[str, str, str, str]], chunk: int = 400) -> bool:\n129:    outp = RES / \"E_judge.jsonl\"\n132:    logger.info(f\"judge: {len(todo)} units to score ({len(units)} requested)\")\n136:            logger.info(f\"judge chunk {s // chunk}: key remaining ${kr}; artifact judge spend ${b.spent:.4f}\")\n138:                logger.error(f\"shared key nearly exhausted (${kr}); stopping judge phase (resumable)\")\n142:            outs = await J.gather_limited([J.judge_json(b, component=\"judge_cheap_primary\", model=JUDGE_MODEL,\n145:                                           for k, c, t, f in part], f\"judge chunk {s // chunk}\")\n151:            logger.info(f\"judge chunk {s // chunk}: {len(part)} units in {time.time() - t0:.0f}s, failures {nf}; spend ${b.spent:.4f}\")\n160:def main():\n181:    logger.info(f\"parseable judge rows: {len(pars)} / {len(ordered)}\")\n200:        ok = asyncio.run(judge_phase(units(first, \"disg\")))\n202:        ok = asyncio.run(judge_phase(units(first, \"orig\")))\n204:        ok = asyncio.run(judge_phase(units(gold, \"disg\") + units(gold, \"orig\")))\n209:        ok = asyncio.run(judge_phase(units(rest, \"disg\") + units(rest, \"orig\")))", "numLines": 23, "totalLines": 23}
```

### [47] TOOL CALL — Grep · 2026-09-24 11:00:20 UTC

```
Pattern: "S4_full|S4 =|def s4|S4_COLS|FRONTIER|gemini-3"
```

### [48] TOOL RESULT — Grep · 2026-09-24 11:00:22 UTC

```
{"mode": "content", "numFiles": 0, "filenames": [], "content": "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6/tests/audit_T1.py:8:3 nested S4_full + c_score_align - S4_full (stratified, from the OOF columns)\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6/tests/audit_T1.py:78:    delta_block(P, \"3_nested\", \"S4_full_plus_c_score_align_oof\", \"S4_full_oof\",\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6/tests/audit_T1.py:79:                A[\"b_s4\"][\"nested\"][\"S4_full_plus_c_score_align - S4_full\"][\"strat\"])\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6/src/api_bar.py:58:async def frontier_judge(b, text: str, fol: str, view: str = \"orig\", model: str = \"google/gemini-3.1-pro-preview\",\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6/src/analyse_T1.py:338:        for a in (\"S4_full_oof\", \"S4_local_oof\", \"S4_full_plus_c_score_align_oof\", \"PT_refit_oof\"):\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6/src/analyse_T1.py:458:def s4_nesting(T, rows, regimes, P, yP, pre, api, cov, max_perm=100):\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6/src/analyse_T1.py:472:    S4_full = s4_local + entered\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6/src/analyse_T1.py:473:    judges_all = [f for f in S4_full if \"judge\" in f]\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6/src/analyse_T1.py:474:    sets = {\"S4_local\": s4_local, \"S4_full\": S4_full,\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6/src/analyse_T1.py:479:            \"S4_full_noJudge\": [f for f in S4_full if f not in judges_all],\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6/src/analyse_T1.py:480:            \"S4_full_strat\": S4_full + [\"strat_L25\", \"strat_L20\", \"strat_EXC\"],\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6/src/analyse_T1.py:481:            \"S4_full_plus_c_score_align\": S4_full + [\"c_score_align\"],\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6/src/analyse_T1.py:482:            \"S4_full_plus_p_peer_text\": S4_full + [\"p_peer_text\"],\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6/src/analyse_T1.py:483:            \"S4_full_plus_nf_c_score\": S4_full + [\"nf_c_score\"],\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6/src/analyse_T1.py:484:            \"S4_full_plus_g_c\": S4_full + [\"g_score\", \"c_score_align\"],\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6/src/analyse_T1.py:485:            \"S4_full_strat_plus_c_score_align\": S4_full + [\"strat_L25\", \"strat_L20\", \"strat_EXC\", \"c_score_align\"],\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6/src/analyse_T1.py:508:    for big, small in ((\"S4_full_plus_c_score_align\", \"S4_full\"), (\"S4_full_plus_p_peer_text\", \"S4_full\"),\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6/src/analyse_T1.py:509:                       (\"S4_full_plus_nf_c_score\", \"S4_full\"), (\"S4_full_plus_g_c\", \"S4_full\"),\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6/src/analyse_T1.py:510:                       (\"S4_full_strat_plus_c_score_align\", \"S4_full_strat\"), (\"S4_local_plus_c_score_align\", \"S4_local\"),\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6/src/analyse_T1.py:511:                       (\"S4_full\", \"S4_local\")):\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6/src/analyse_T1.py:513:    for a, bb in ((\"c_score_align\", \"S4_full_oof\"), (\"p_peer_text\", \"S4_full_oof\"), (\"PT_refit_oof\", \"S4_full_oof\"),\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6/src/analyse_T1.py:520:    out[\"nested_long\"] = {\"S4_full_plus_c_score_align - S4_full\": {st: cL.delta(\"S4_full_plus_c_score_align_oof\", \"S4_full_oof\", st)\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6/src/analyse_T1.py:532:        ob, _ = fit_s4_oof(tab, perm, folds, sets[\"S4_full_plus_c_score_align\"], C=1.0, fail_fill=ff)\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6/src/analyse_T1.py:533:        os_, _ = fit_s4_oof(tab, perm, folds, sets[\"S4_full\"], C=1.0, fail_fill=ff)\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6/src/analyse_T1.py:553:    obs_s = nested[\"S4_full_plus_c_score_align - S4_full\"][\"strat\"][\"delta\"]", "numLines": 25, "totalLines": 59, "appliedLimit": 25}
```

### [49] TOOL CALL — Read · 2026-09-24 11:00:26 UTC

```
/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6/src/analyse_T1.py
```

### [50] TOOL RESULT — Read · 2026-09-24 11:00:26 UTC

```
{"type": "text", "file": {"filePath": "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6/src/analyse_T1.py", "content": "def s4_nesting(T, rows, regimes, P, yP, pre, api, cov, max_perm=100):\n    from .s4 import fit_s4_oof\n    s4_local = [\"L:\" + f for f in pre[\"S4_sets\"][\"S4_local\"]]\n    api_full = [\"judge_cheap_disg\", \"judge_cheap_orig\", \"judge_cheap2_disg\", \"judge_cheap2_orig\", \"rt_nli_min\", \"rt_nli_fwd\",\n                \"rt_nli_bwd\", \"rt_nli_contra\", \"rt_embed_cos\", \"sc5_eq_frac\", \"sc5_entropy\"]\n    entered, substituted = [], {}\n    local_counterpart = {\"rt_nli_min\": \"L:rt_nli_min_local\", \"rt_nli_fwd\": \"L:rt_nli_fwd_local\", \"rt_nli_bwd\": \"L:rt_nli_bwd_local\",\n                         \"rt_nli_contra\": \"L:rt_nli_contra_local\", \"rt_embed_cos\": \"L:rt_embed_cos_local\",\n                         \"sc5_eq_frac\": \"L:sc5_local_eq_frac\", \"sc5_entropy\": \"L:sc5_local_entropy\"}\n    for c in api_full:\n        if c in api and cov[c][\"coverage_RAB\"] >= 0.95:\n            entered.append(c)\n        else:\n            substituted[c] = {\"coverage\": cov.get(c, {}).get(\"coverage_RAB\", 0.0), \"local_counterpart_kept\": local_counterpart.get(c)}\n    S4_full = s4_local + entered\n    judges_all = [f for f in S4_full if \"judge\" in f]", "numLines": 16, "startLine": 458, "totalLines": 1031}}
```

### [51] TOOL CALL — Read · 2026-09-24 11:00:26 UTC

```
/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6/src/api_bar.py
```

### [52] TOOL RESULT — Read · 2026-09-24 11:00:26 UTC

```
{"type": "text", "file": {"filePath": "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6/src/api_bar.py", "content": "    (verdict-token fallback gives p in {0,1}). RETURNS {'score': 1 - P(YES) or None, 'src', 'fail', 'cost'}.\"\"\"\n    from . import judges as J\n    o = await J.judge_logprob(b, component=\"judge_cheap2\", model=model, rubric=J.RUBRIC_A, text=text, fol=fol,\n                              item_id=item_id or view)\n    return {\"score\": None if o.get(\"p\") is None else 1.0 - o[\"p\"], \"src\": o.get(\"src\"), \"fail\": o.get(\"fail\"),\n            \"cost\": o.get(\"cost\"), \"view\": view}\n\n\nasync def frontier_judge(b, text: str, fol: str, view: str = \"orig\", model: str = \"google/gemini-3.1-pro-preview\",\n                         max_tokens: int = 4000, item_id: str = \"\") -> dict:\n    \"\"\"Frontier reasoning judge, same rubric-A JSON prompt (reasoning effort 'low'). Same output as judge_api.\"\"\"\n    from . import judges as J\n    o = await J.judge_json(b, component=\"strong\", model=model, rubric=J.RUBRIC_A, text=text, fol=fol, item_id=item_id or view,\n                           max_tokens=max_tokens, extra={\"reasoning\": {\"effort\": \"low\"}}, user_tmpl=J.USER_JSON_A)\n    return {\"score\": None if o.get(\"p\") is None else 1.0 - o[\"p\"], \"type\": o.get(\"type\"), \"fail\": o.get(\"fail\"),\n            \"cost\": o.get(\"cost\"), \"view\": view}\n\n\nasync def sc5_api(b, text: str, k: int = 5, model: str = \"openai/gpt-4.1-nano\") -> list[str | None]:\n    \"\"\"k independent T=0.7 formalisations of `text` with dataset E's few-shot generation prompt (the samples a\n    self-consistency metric compares the candidate against). RETURNS k extracted formulas (None = failed call).\"\"\"\n    import method as M  # noqa: PLC0415 - the SC call (and its cache key) lives in the orchestrator\n    from . import judges as J\n    outs = [await M._sc_call(b, J, text, \"api_bar\", i) for i in range(k)]\n    forms = [J.extract_formula(o.get(\"text\")) if o.get(\"text\") else None for o in outs]\n    return [f[4:].strip() if f and f.upper().startswith(\"FOL:\") else f for f in forms]\n\n\ndef sc5_score(candidate: str, samples: Sequence[str | None], ms: int = 2000) -> dict:\n    \"\"\"SC-5 modulo vocabulary. MEASURES: disagreement of the candidate with the model's own resamples of the sentence.", "numLines": 30, "startLine": 50, "totalLines": 378}}
```

### [53] ASSISTANT · 2026-09-24 11:04:25 UTC

```
Writing the plan now, along with the README and manifest the workspace contract requires.
```

### [54] TOOL CALL — Write · 2026-09-24 11:04:25 UTC

````
File: /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_plan/gen_plan_experiment_2/plan.md

# PLAN — experiment_iter5_dir2: E2-B, a second untouched L25 replication sample, plus a cost-matched and a frontier judge

Type: EXPERIMENT. Deps: art_2OmxzMInZZJY (E2 sampling frame and frozen code), art_U4Hsqt4Ay9Tg (dataset E: dev data, fold recipe, weights), art_zcwCQgTqk6DN (rename controls, `perturb.control_rename`).
Hard cap: $9.5 of OpenRouter spend. Reserve: 10%. Wall clock: 6 h.

---------------------------------------------------------------------------------------------------
## 0. What this artifact is for, in one paragraph

E2-A (the sibling artifact) labels 350 fresh L25 sentences. At E's yield of 0.37 usable sentences per built sentence, that gives an L25 MDE80 of 0.110 against flash-lite disguised (eval-3 `power_E2.json`). The observed E effect is +0.069, so E2-A alone has about 42% power for it.

E2-B adds about 400 more L25 sentences. They are drawn by E2's frozen rule and processed by E2's byte-identical code.

Power, computed from `power_E2.json` se_fit L25|flashlite_disg, where SE = e^a · n_usable^b with a = −0.795 and b = −0.503:

| Sample | Planned | Usable | SE | MDE80 | Power at +0.069 |
|---|---|---|---|---|---|
| E2-B alone | 400 | ≈148 | 0.037 | 0.103 | 0.47 |
| UNION L25 (E2-A 350 + E2-B 400) | 750 | ≈277 | 0.027 | ≈0.075 | ≈0.73 |

This is the only route in this iteration by which the user's priority stratum (L25) can reach adequate power. More metrics would not help; more graded sentences would.

E2-B also adds the two comparators a reviewer names first:
- a COST-MATCHED stronger cheap judge (deepseek-v3.2, reasoning off);
- the FRONTIER judge (gemini-3.1-pro-preview) on a 300-row subsample.

Every number that E2-B reports on its own is secondary to the union, except where §6 says otherwise.

---------------------------------------------------------------------------------------------------
## 1. Facts from the sampling frame that change the design (read from gen_art_dataset_4; the executor must re-verify)

F1. Supply. `census_E2.json` counts the L25 supply after filters: 960 at 25-29 words, 186 at ≥30 words, and 0 at ≥35. E2's base takes 158 long + 192 short sentences. The surplus of 98 (`prereg_E2.json` pool_order.L25 positions 351-448; `l25_tier == "surplus"` in `work/pool_E2.json`) is about 28 long + 70 short. After the surplus, the ≥30-word bin is EXHAUSTED.
- E2-B is therefore about 28 long + about 372 short sentences at 25-29 words.
- E2-A's L25 is 45% long; E2-B's is about 7% long.
- This is a real composition difference. It must be (a) pre-registered, (b) handled by word-bin strata in the union, and (c) named as the first candidate explanation for any A-vs-B heterogeneity. It is NOT a reason to change the rule: long supply does not exist.

F2. Build-order dependence of the 12-gram rule. In `select_e2.py`, `take()` shares one `accepted_grams` set across the build order EXC → L25 base+surplus → DT.
- To continue "the same rule", E2-B must seed `accepted_grams` with the 12-grams of ALL E2 rows: EXC 100, L25 448, DT 110 including the reserve.
- It must then continue `take(short, …)` and `take(long_, …)` over the SAME sha1 order ('E2_v1|' + sentence_id), skipping every `used` id.
- The E-exclusion (E's 700, calibration, few-shot, screen, FOLIO, curated sets) and E's 12-gram filter are inherited unchanged.
- Implement this as a NEW wrapper `src_e2b/select_e2b.py`. It imports `select_e2.py` functions, re-runs the frozen selection, asserts that it reproduces `work/pool_E2.json`'s sha256 `98cdccff…`, and only then continues the order. If the reproduction assert fails, STOP and debug. Never select E2-B from a pool that differs from E2's.

F3. Costs (`pilot_projection.json`, E-measured; the E2 panel pilot never ran). Per L25 sentence:

| Item | $ per sentence |
|---|---|
| generation | 0.00100 |
| panel stage 1 | 0.00664 |
| P1 adjudication | 0.00277 |
| reference repair | 0.00141 |
| **total** | **0.01182** |

F4. Without the panel, E2's final rule yields no CORRECT rows on MALLS strata. The 30-sentence pilot gave 36 ERROR / 244 UNRESOLVED / 0 CORRECT. E's L25 CORRECT class (176 rows) comes almost entirely from tier B and reference repair. So the panel is what makes L25 testable at all. See §4 for the drift branch.

F5. The frozen judges (vendored in `iter_4/gen_art/gen_art_experiment_9/vendor/e8src/vendor_d/judges.py`; the originals are exp D, used by exp 5 `run_api_E.py` and exp 6 `api_bar.py`):
- flash-lite = `google/gemini-2.5-flash-lite`, `judge_json(RUBRIC_A, USER_JSON_A, max_tokens=150)`, run on the disguised view and the original view;
- nano = `openai/gpt-4.1-nano`, `judge_logprob(RUBRIC_A)` → 1 − P(YES);
- frontier = `api_bar.frontier_judge`, `google/gemini-3.1-pro-preview`, reasoning effort "low", max_tokens 4000.

Assert that `judges.PROMPT_SHA` equals the sha1 recorded in exp 5/6 before any judge call.

F6. The S4 stack is exp 6 `analyse_T1.py::s4_nesting`: S4_local plus the API features with ≥95% R_AB coverage. Missing API features are substituted by their local counterparts, logged in `substituted`.

---------------------------------------------------------------------------------------------------
## 2. Workspace layout (all under this artifact's gen_art workspace, called <WS> below)

```
<WS>/e2bsrc/           copy of gen_art_dataset_4 CODE ONLY (see Step 0.2) — E2's byte-identical pipeline
<WS>/e2bsrc/src_e2b/   NEW wrappers (select_e2b.py, activate_e2b.py, budget.py) — E2 files untouched
<WS>/freeze_copy/      copies of the M1 frozen files (consensus_variants.py, selection.json, gg.py, gg_gate.json)
<WS>/e2b/              sealed rows, seal.json, testability_E2B.json, E2B_FINAL_READY.json, E2B_SURPLUS_CLAIM.json
<WS>/scores/           scores_E2B.jsonl, score_seal.json, judges_*.jsonl
<WS>/analysis/         per_item_E2B.jsonl, confirm_verdict_E2B.json, union_longpool.json, tables.md
<WS>/prereg_iter5_E2B.json (+ .sha256)   <WS>/deviations.json   <WS>/cost_ledger_master.jsonl
<WS>/method_out.json (exp_gen_sol_out)   <WS>/README.md   <WS>/.aii/manifest.yaml
```

---------------------------------------------------------------------------------------------------
## 3. Timeline (6 h wall clock; T = start)

| Window | Work |
|---|---|
| T+0:00-0:30 | Step 0: setup, probe, selection, prereg + hash, surplus claim |
| T+0:30-3:15 | Step 2: generation → solver labels → panel, in batches of 50 in sha1 order. In parallel from batch 1: label-free judges and consensus peers-only scoring |
| T+0:30-1:30 | Step 1: poll for M2 (drift), which gates the panel. Generation and solver labels do not wait |
| T+1:30-4:00 | Poll for M1 (freeze). Label-free scoring of every frozen variant as soon as it lands |
| T+3:15-3:45 | Seal the labels; seal the scores; verify both |
| T+3:45-4:45 | Join; E2-B analyses; write E2B_FINAL_READY.json |
| T+4:45-5:30 | Poll for E2A_FINAL_READY; union + meta-analysis |
| T+5:30-6:00 | Tables, README, manifest, method_out.json, validation |

Hard deadlines, written into the prereg:
- M2 T+1:30;
- M1 variants T+2:30;
- M1 GG T+4:00;
- last paid call T+4:30;
- M3 (E2-A) T+5:30.

---------------------------------------------------------------------------------------------------
## 4. Step-by-step

### Step 0 — Setup, prereg, selection ($0 except a 1-token probe)

0.1 Read the skills aii-python, aii-openrouter-llms, aii-parallel-computing, aii-long-running-tasks and aii-json. Make a 1-token probe call through `OPENROUTER_BASE_URL` / `OPENROUTER_API_KEY` and log it.

0.2 Copy `iter_4/gen_art/gen_art_dataset_4` to `<WS>/e2bsrc`, EXCLUDING the following:
- `.venv/`;
- `raw/generations.jsonl`, `raw/*` of E2's pilot;
- `work/labels_heldout*.jsonl`, `work/panel_cache.jsonl`, `work/sentences*.json`;
- `sealed/`, `seal.json`;
- `cost_ledger.jsonl`, `.aii_cost_ledger.jsonl`;
- `full/mini/preview_data_out.json`.

Keep:
- `src/`, `labeller/`, `src_e2/`, `src_d3/`, `prompts/`, `data_local/`, `E_ref/`, `tests/`;
- `code_freeze.json`, `prereg_E2.json`, `census_E2.json`;
- `work/pool_E2.json`, `work/models_snapshot_E2.json`, `work/fewshot_exemplars.json`, `work/calibration_items.json`;
- pyproject/uv.lock.

Then:
- Run `uv sync` in `e2bsrc` (Python 3.12).
- Verify every sha256 in `prereg_E2.json.labeller_sha256` and `code_freeze.json` against the copied files. Write `e2bsrc/code_freeze_check_E2B.json`. A mismatch stops the run.
- Start with a CLEAN raw/work state, so E2's pilot rows can never leak into E2-B's assemble step. `assemble_e2.py` reads whatever is in `raw/`.

0.3 `src_e2b/select_e2b.py` (F2):
1. Reproduce E2's selection and assert the pool sha256.
2. Take the 98 surplus in their `e2_rank` order.
3. Continue the sha1 order over the remaining eligible L25 rows (long first, then short, the same `take()`), with `accepted_grams` seeded from every E2 row. Target a total of 400.
4. Also write the next 150 in order as a reserve, used only if more than 10% of sentences fail gold parse or generation.

Record:
- the per-bin supply remaining (expected ≈ 0 long, ≈ 690 short);
- the within-E2B 12-gram drops;
- the collision checks (0 text or 12-gram collisions with E and E2 must be asserted).

Outputs: `e2b/sentences_E2B.json`, `e2b/census_E2B.json`.

0.4 Batches: order the 400 by sha1('E2B_batch_v1|' + sentence_id) and cut them into 8 batches of 50. Batch 1 must contain surplus AND continuation sentences in proportion. The order is a hash, not a choice.

0.5 `prereg_iter5_E2B.json`, written and hashed BEFORE any E2-B generation. It contains:

(a) Deviation D-E2B: "a pre-registered replication sample drawn by E2's frozen rule, beyond E2's freeze, reason = power (eval-3 power_E2.json: L25 needs ~882 planned sentences for +0.069)". Also D-E2B-comp: "E2-B is ~93% 25-29 words because the ≥30 bin is exhausted (F1)".

(b) The selection algorithm and its expected hashes.

(c) The metric list, verbatim from the SHARED CONTRACT's frozen definitions (V0-V5, PT, GG), with V0 as the PRIMARY.

(d) Comparators:
- flash-lite disguised (primary comparator), flash-lite original, nano original;
- cost-matched deepseek-v3.2, disguised (primary cost-matched) and original;
- frontier gemini-3.1-pro-preview, original.

(e) The confirmatory hierarchy of §6 with its α, and MDEs stated in advance: E2-B L25 0.103; union L25 ≈0.075; union long pool ≈0.07 (L25 ≈277 + E2-A EXC ≈64 usable, SE from the long se_fit).

(f) The union and meta-analysis rule (§6.3), the tie-breaking and duplicate rule (§4 Step 2.5), and the frontier subsample recipe.

(g) The cost-matched judge spec: the byte-identical RUBRIC_A text, USER_JSON_A, `reasoning: {enabled: false}`, temperature 0, max_tokens 150, and the JSON parse rule of `judges.parse_judge_json`.

(h) The shrink order: GG scoring → frontier → cost-matched original view → L25 sentences, at a floor of 250, always an 8-batch-order prefix.

(i) The deadlines.

0.6 Surplus claim. Write `e2b/E2B_SURPLUS_CLAIM.json` with token 'aii_iter5_e2b_surplus_v1' and the 98 ids. The hypothesis's P3 lets E2-A add the same surplus "if budget remains", so a collision is possible. The rule: a sentence labelled by both artifacts counts ONCE in the union, taking E2-B's copy. The duplicate pairs give a free test-retest label agreement, reported as the κ of final labels.

### Step 1 — Drift decision (M2)

Poll `glob('/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/*/e2/E2_DRIFT_DECISION.json')` every 5 minutes, and check the token 'aii_iter5_e2_drift_v1'. Log every attempt.

- PASS: use its pinned provider for each of P1/P3/R1 (OpenRouter `provider: {order: [...], allow_fallbacks: false}`). Record it.
- FAIL: run the panel anyway, under the same pinned protocol that E2-A uses for its drifted labels. Mark every E2-B label `label_regime = DRIFTED`. All E2-B and union results become SECONDARY. Report tier-A-only (R_A) rows alongside.
  - Why not skip the panel: F4 shows that a no-panel regime has no L25 CORRECT class. A drifted but internally consistent regime shared by E2-A and E2-B is the only testable one.
- ABSENT at T+1:30: run E2's gate yourself, as E2's `run_all.sh` step 3: `gate.py --mode synthetic` and `--mode trackh` with members P1,P3,R1, then `drift_report.py`. That costs about $0.3 against caps of 0.30 + 0.50.
  - Use the same pinning procedure: pin the provider that serves each id at the time of the call, and record it.
  - Book this as deviation D-E2B-drift.
  - Apply E2's stop rule verbatim: majority agreement < 0.85 → FAIL.
  - Also compute the hypothesis's criterion: the track-H flag rate on original errors must fall within the 95% CI of E's 0.84.
  - If E2-A's M2 appears later, report both decisions. The union uses E2-A's decision.

### Step 2 — Generation + labels, in batches of 50, each completed end to end

For each batch b = 1..8, in order:

2.1 Budget check (§7). Stop BEFORE a batch if its estimate exceeds the remaining budget minus the reserve.

2.2 Generation:
```
e2bsrc/src_e2/e.py generate.py --slots G1,G1b,G2,G3,G4,G5,G6,G7,G8,G9 --variants fewshot_v1 --sentences <batch file> --cap <remaining>
```
Then `gen_retry.py`. Apply the slot-unavailability rule from `prereg_E2.json`: same family, nearest current instruct model, flagged `slot_substituted`.

2.3 Solver labels: `run_label.py --kind heldout --workers 4`.

2.4 Panel, only after M2 is resolved:
- `panel_run.py --members P3,R1`;
- `--adjudicate P1`;
- `src_e2/repair.py`;
- `run_label.py --refs work/reference_overrides.json`.

Each script is wrapped by `src_e2b/activate_e2b.py`, which points `work/sentences.json` at the cumulative E2-B set, so the frozen scripts run unchanged. If E2's scripts cannot be restricted to a batch, run them on the cumulative set: they are resumable, skip sentences already done, and the panel cache never re-bills.

2.5 After each batch, log:
- rows, parse rate, spend per sentence (actual vs F3);
- the count of completed sentences per word bin.

Do NOT look at labels or score-label joins. The only label-derived quantity allowed before the seal is the count of CORRECT/ERROR per stratum, needed for testability. Write it to `e2b/progress.jsonl`.

2.6 After the last batch (or a budget stop), run:
- `assemble_e2.py`;
- `controls_e2.py`: RENAME_SYN / RENAME_NONCE on up to 300 final-CORRECT rows, via dataset 3's `perturb.control_rename`, z3-verified;
- `testability_e2.py`: rule verbatim, ≥50 ERROR, ≥50 CORRECT, ≥25 sentences each;
- `seal_e2.py`, `verify_seal.py`.

All of these run under `e2bsrc` with E2B output names. `seal.json` is copied to `e2b/seal.json`, and E2-B's testability is written to `e2b/testability_E2B.json`.

Label-free work that runs in PARALLEL from batch 1 (it only needs `candidates_E2B_nolabels`-equivalent rows = generations + parse status; it never touches labels):

(i) Cheap judges on every parseable row: flash-lite disguised, flash-lite original, nano original.
- Disguise: `labeller/disguise.py`, as in exp 5's `build_disguise`.
- An unparseable candidate is scored 1.0 (flagged), as for every metric.
- About 3,700 rows × 3 calls × ~$5e-5 ≈ $0.55.

(ii) The cost-matched judge (Step 3.2).

(iii) Local features for S4: L2-bow, the L3-free local round-trip counterparts and the local Qwen3-8B judge, IF the vendored code runs on this machine's hardware. Check with aii-use-hardware. If there is no GPU, drop the local judge from S4 and record it in `substituted`.

### Step 3 — Label-free scoring + score seal

3.1 Freeze marker (M1). Poll
```
glob('/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/*/freeze/CONSENSUS_FREEZE_READY.json')
```
every 5 minutes and check the token 'aii_iter5_consensus_freeze_v1'. Copy `consensus_variants.py`, `selection.json`, `gg.py` and `gg_gate.json` into `<WS>/freeze_copy/`, and verify their sha256 against the marker. Never import across paths.

Scoring of each metric:

| Metric | How it is scored on E2-B |
|---|---|
| V0 c_score_align | exp-5 `pool_scoring.py` byte-identical (`iter_2/gen_art/gen_art_experiment_5/src`). Assert the file sha against exp 5. Scored immediately; it does NOT wait for M1 |
| PT p_peer_text | exp-5 `peer_text.py` + the frozen fusion coefficients. Also immediate |
| V1-V5 | from `freeze_copy/consensus_variants.py` |
| V2 / V3 / V5 weights w_f | out-of-fold over E2-B's OWN sentences, fold = sha1('E2_folds_v1\|' + sentence_id) % 5, shrunk with 20 pseudo-sentences. Label-free |
| V4 | coefficients from `selection.json` (fit on E, frozen). Never refit |

For the union, V2/V3/V5 are recomputed out-of-fold over the union's sentences with the same recipe. This is declared in the prereg because it is still label-free.

If M1 is ABSENT at T+2:30:
- implement V1 and V2 from the verbatim contract text in `<WS>/fallback_variants.py`;
- score them as REPORTED-ONLY rows;
- H-IMPROVE is recorded as "no carried variant available to E2-B" (deviation D-E2B-M1);
- V4 and V5 are not scored (both need E-fitted objects).

The GG branch:
- If `gg_gate.json` = PASS by T+4:00: score c_gg on E2-B with `freeze_copy/gg.py` (its gloss model id and prompt sha). Gloss calls are paid. Pilot on 20 sentences, estimate the cost, and run only if the estimate is ≤ $0.4 AND fits §7.
  - GG is the FIRST item in the shrink order.
  - Score GG on (a) all L25 rows and (b) the rename controls.
- FAIL or absent: GG is not scored, and this is recorded.

3.2 The COST-MATCHED judge: `deepseek/deepseek-v3.2`, `extra={"reasoning": {"enabled": false}}`, `judges.judge_json(RUBRIC_A, USER_JSON_A, max_tokens=150)`. The prompt is byte-identical to flash-lite's.

Pilot on 30 rows, the first 30 parseable rows of batch 1 in sha1 order, both views. Report the parse rate, the $ per call and the latency.
- Parse failure > 10%: raise max_tokens to 300 once, as a pre-declared single retry rule, and log it.
- Still > 10%: report as NOT_TESTABLE_PARSE.

Budget:
- Run the DISGUISED view on all parseable rows. It is the cost-matched primary: disguised is the contamination-safe view, matching flash-lite disguised.
- Run the ORIGINAL view on all rows if the pilot cost is ≤ $1.6e-4 per call. Otherwise run it only on the frontier subsample plus as many L25 batches (in order) as fit the budget, and record the coverage.

The cost-matching claim is stated in $/candidate: deepseek measured, vs consensus FULL $1.21e-4 (9 peers) and MARGINAL (cost_units.csv).

3.3 The FRONTIER subsample:
- Size: 300 candidate rows.
- Drawn right after generation is complete and BEFORE any label join.
- Stratified by label-free words tercile (tercile cut-points from E2-B's sentences) × system family (10 slots → 9 families), allocated proportionally with a minimum of 3 per cell.
- Sampled within cells by sha1('E2B_frontier_v1|' + row_key).
- Store the inclusion probabilities.

Run `api_bar.frontier_judge` (original view, effort "low", max_tokens 4000).
- Pilot 10 rows for cost. Expected ≈ $3.65e-3 per item, so ≈ $1.1.
- If the pilot shows > $6e-3 per item, cut to the largest prefix of the sha1 order that fits, and recompute the inclusion probabilities.

About 2/3 of the rows are expected to land in R_AB, i.e. about 200 usable. State this in the prereg: the frontier ratio will have a wide CI.

3.4 Score seal. `scores/scores_E2B.jsonl` holds one row per row_key with every metric and judge score, plus the parse status. Write `scores/score_seal.json` with:
- the sha256 of the scores file;
- the sha256 of every scoring source file: `pool_scoring.py`, `peer_text.py`, `freeze_copy/*`, `judges.py`, the control-scoring code;
- the frontier-subsample file;
- the M1/M2 marker hashes.

The scoring code may read ONLY the following (the file-access allowlist):
- `e2bsrc/raw/generations*.jsonl`, `candidates_E2B_nolabels.jsonl`, `controls_E2B_nolabels.jsonl`;
- `e2b/sentences_E2B.json` (text + label-free strata);
- `freeze_copy/*`;
- exp-5 code;
- the judge caches.

Enforce this with a wrapper that monkey-patches `builtins.open` to refuse paths under `sealed/` or containing 'label' or 'reference', and logs every path opened to `scores/file_access_log.txt`. This is cheap, and a reviewer can check it.

Controls (rename) are scored for V0, PT, and GG if GG passed, with the same code, before the join. They are included in the score seal.

### Step 4 — Join

Join only after both `verify_seal.py` (labels) and a `verify_score_seal.py` (the score hashes still match) pass. `analysis/per_item_E2B.jsonl` holds:
- row_key, sentence_id, stratum (L25_E2B), word_bin, words, n_conditions, system, family;
- label, tier, reading_choice, contested;
- every score;
- in_frontier_subsample, ipw.

### Step 5 — Analyses (E2-B)

Reuse code. The stratified AUROC, the cluster bootstrap and `fit_s4_oof` come from exp 6's `analyse_T1.py`, copied, with its sha recorded. Use the SAME functions that E2-A uses where they are shared. If E2-A's analysis module is available via its M3 pointer, diff it against ours and report any difference.

Populations:
- R_AB = LLM systems only (no gold-as-system), tiers A+B, excluding CONTESTED and reading_choice (the primary);
- R_A = tier A only (sensitivity);
- CONTESTED counted as CORRECT, and as ERROR (sensitivity).

5.1 PRIMARY E2-B cell: L25_E2B, strat AUROC Δ = V0 − flash-lite disguised.
- Sentence-cluster bootstrap, B = 2,000, percentile 95% CI, strata = word bin (25-29 / ≥30).
- Also V0 − flash-lite original, V0 − nano, V0 − cost-matched (disguised and original).
- Report the AUROC of each metric with its CI, the AUPRC, and the counts (rows, ERROR, CORRECT, sentences with both classes).

5.2 Frontier (subsample, IPW-weighted AUROC as in T1):
- AUROC of the frontier, V0 and S4_E2B;
- ratio V0 / frontier with a bootstrap CI (resample sentences within the subsample);
- nested [frontier + V0] − frontier (cross-fitted logistic, 5 sentence folds).

5.3 Nested over S4_E2B: `fit_s4_oof` on S4_full-equivalent features, cross-fitted by E2-B sentence folds. Compare [S4_E2B + V0] − S4_E2B, with its strat CI. Record every substituted feature.

5.4 H-MECH (i)-(iv) on E2-B CORRECT candidates (L25_E2B), with the definitions and code copied from eval 3 (art_BvAL_KZTZuw8, pair classes) and eval 2 (SCATTER, NET):
- (i) the share of non-agreeing peers labelled ERROR (≥ 0.50);
- (ii) the SCATTER ratio SI_cor/SI_err (≥ 2);
- (iii) NET Δ(e+d) over the words terciles (> 0). With E2-B's narrow 25-29 range, the terciles are narrow, so report it, and flag range restriction;
- (iv) exact vs ALIGN per class: ALIGN d lower, e higher on MEANING_RENAME-type and ADD/DROP. Use e/d as defined in exp 9 (art_D7k2ZWgE3nVd) `src/analyse.py`: e = the fraction of ERROR candidates the peers endorse (c ≤ 0.5), d = the fraction of CORRECT candidates flagged (c > 0.5). If the code differs from this gloss, the code wins.

Each item is scored CONFIRMED or REFUTED with its CI.

5.5 H-IMPROVE: carried variant − V0 on L25_E2B (and in the union). If `selection.json` = 'NONE: V0 stands', report V1-V5 as development-only rows.

5.6 Rename, on the E2-B CORRECT controls:
- FA at c > 0.5 for V0 and PT, and GG if scored;
- the PAIRED FLIP (the control flagged while its original was not) with a Wilson CI;
- the base FA of the originals shown next to every FA.

5.7 Complexity curves: AUROC and FA against words, n_conditions, n_quant and depth, with bins pre-declared at the E2-B quartiles, for V0, flash-lite disguised, cost-matched and nano.

5.8 Coverage: parse rate per system, with unparseables in the denominator (scored 1.0), and consensus-scorable rate (|P| ≥ 1).

5.9 Cost per candidate, FULL and MARGINAL, for every metric and judge, in $ and in seconds, from the ledger: V0 FULL = the 9 peer generations + z3 time; MARGINAL = z3 only. This is the "does a large judge earn its cost" row: AUROC gain per extra $ vs flash-lite, for deepseek and for the frontier.

5.10 System-level: Kendall τ-b between each metric's system mean and the gold system accuracy (13 system × variant rows if available; here 10 slots, so say so), with a sentence-bootstrap CI. Descriptive only.

5.11 Judge self-preference control. For each judge, AUROC recomputed excluding rows generated by the judge's own family:
- flash-lite and the frontier → drop G8 (google-gemini);
- nano → drop G7 (openai);
- deepseek → drop G4 (deepseek).
Consensus is already leave-own-family-out, so this puts the comparison on equal footing. Report Δ with and without.

5.12 `confirm_verdict_E2B.json` holds each §6 claim with its verdict, the numbers, and the population. Then write `e2b/E2B_FINAL_READY.json` with token 'aii_iter5_e2b_final_v1', the path to `per_item_E2B.jsonl`, its sha256, the label regime (PASS/DRIFTED) and the completed fraction per bin.

### Step 6 — UNION and meta-analysis

Poll for `glob('…/iter_5/gen_art/*/e2/E2A_FINAL_READY.json')` (token 'aii_iter5_e2a_final_v1') until T+5:30.

Present:
- Load E2-A's per-row file read-only and verify its sha256.
- Harmonise the columns. The required columns are listed in the contract; any missing column → that analysis is NOT_COMPUTED, stated.
- Apply the duplicate rule (Step 0.6).
- If E2-A's label regime ≠ E2-B's (one PASS, one DRIFTED), the union is computed but marked SECONDARY, and the per-sample results are primary.
- Compute §6.2 and §6.3.

Absent: write `analysis/union.py`, runnable later with one command (`uv run analysis/union.py --e2a <path>`), and record union = NOT_COMPUTED_E2A_MISSING. If E2-A also computes the union, both must use the same definitions. Report the sha of the inputs so the two can be checked for identity.

---------------------------------------------------------------------------------------------------
## 5. Metric and comparator table (what is scored on E2-B)

| Row | Role | Source | $ (est.) |
|---|---|---|---|
| V0 c_score_align | PRIMARY | exp-5 `pool_scoring.py`, leave-own-family-out, 10-slot pool | 0 (peers are the generations) |
| PT p_peer_text | secondary | exp-5 | 0 |
| V1-V5 | H-IMPROVE (only the carried variant is confirmatory) | freeze | 0 |
| GG | H-RENAME (only if the gate PASSED) | freeze gg.py | ≤ 0.4 |
| flash-lite disguised | primary comparator | vendor_d judges | ~0.19 |
| flash-lite original | comparator | same | ~0.19 |
| nano original (logprob) | comparator | same | ~0.19 |
| deepseek-v3.2 disguised | COST-MATCHED primary | RUBRIC_A byte-identical | ~0.9 (pilot) |
| deepseek-v3.2 original | cost-matched | same | ~0.9 (or subsample) |
| gemini-3.1-pro-preview original | FRONTIER, 300 rows | api_bar.frontier_judge | ~1.1 |
| S4_E2B | stack | exp-6 fit_s4_oof | 0 |

---------------------------------------------------------------------------------------------------
## 6. Claims, the testing hierarchy, and the verdict rules (fixed in the prereg)

6.1 E2-B-alone claims. All are two-sided 95% sentence-cluster bootstrap CIs.
- (B1) L25_E2B: Δ(V0 − flash-lite disguised) CI > 0. MDE80 0.103, power at +0.069 of 0.47. A null here is EXPECTED under the E effect size and must be reported as "underpowered alone".
- (B2) Nested [S4_E2B + V0] − S4_E2B, CI > 0.
- (B3) Cost-matched: Δ(V0 − deepseek disguised). Reported with its CI. No directional prediction is pre-declared. This is the "does a stronger cheap judge close the gap" test, and it could go against us.
- (B4) Frontier: ratio V0/frontier and nested gain, descriptive with CIs.

6.2 UNION claims (the reason this artifact exists), in FIXED-SEQUENCE order. Each is tested at α = 0.05 only if the previous one was confirmed; otherwise it is reported as descriptive.
1. (U1) Union LONG POOL (L25_E2A ∪ L25_E2B ∪ EXC_E2A): strat Δ(V0 − flash-lite disguised) CI > 0, with point > 0 vs flash-lite original and nano. This is the hypothesis's CONFIRM (a), with more power. Strata = {L25_E2A, L25_E2B, EXC} × word bin, bootstrap over sentence_id within each stratum.
2. (U2) Union L25 (the user's priority stratum): the same Δ, CI > 0. MDE80 ≈ 0.075.
3. (U3) Union nested [S4 + V0] − S4, CI > 0.
4. (U4) The carried H-IMPROVE variant − V0 on the union long pool, CI > 0.

Fixed-sequence testing controls the family-wise error without splitting α, and the order is the hypothesis's own priority order.

Replication check: heterogeneity Δ_E2A − Δ_E2B (independent samples, so SE = sqrt(SE_A² + SE_B²)), plus Cochran's Q and I² over the two L25 samples.
- It is REPORTED whichever way it comes out.
- If the heterogeneity CI excludes 0, the union is still reported, but the paper must say "effect differs between samples". The first candidate explanation is the word-bin composition (F1). Test it by recomputing Δ within the 25-29 bin only, in both samples.

6.3 Meta-analysis cross-check. Fixed-effect inverse-variance pooling of the per-sample strat Δs (L25_E2A, L25_E2B, and EXC as a third component for the long pool). Report it next to the pooled-bootstrap union. The pooled bootstrap is the pre-declared primary; the meta-analysis is a consistency check. A disagreement larger than 0.02 is reported.

6.4 Verdict wording, pre-declared:
- U1 CI > 0 → "confirmed on untouched long sentences".
- U1 point > 0 with a CI including 0 → "direction replicated, not significant at MDE ≈0.07".
- U1 point ≤ 0 → DISCONFIRM (hypothesis §4): "E result was development-set optimism".

H-MECH items are scored individually. The cost-matched and frontier rows are reported, never gating.

---------------------------------------------------------------------------------------------------
## 7. Budget control (hard cap $9.5, reserve 10% → plan to $8.55)

`src_e2b/budget.py`:
- `spent()` sums `cost_ledger_master.jsonl`, into which every paid call writes (E2's `e.py` ledger is tailed and mirrored, and the judge wrappers append directly);
- `can_start(estimate)` returns remaining − 0.95 ≥ estimate.

Set `AII_HARD_CAP` for E2's scripts to the phase allowance each time they are launched.

| Phase | Estimate | Rule |
|---|---|---|
| drift fallback (only if M2 absent) | 0.30 | — |
| 400 L25 × $0.01182 | 4.73 | per batch of 50: $0.59; re-estimate after batch 1 from actuals |
| cheap judges ×3 | 0.55 | — |
| deepseek disguised | ~0.9 | pilot first |
| frontier 300 | ~1.1 | pilot first |
| deepseek original | ~0.9 | only if it fits |
| GG scoring | ≤0.4 | only if the gate PASSED; FIRST to drop |
| **total** | **≈8.5-8.9** | — |

Shrink order: GG → frontier → deepseek original → L25 sentences (floor 250, always a batch-order prefix).

On HTTP 402/403, do all CPU work first, then poll every 15 minutes until T+4:30. After that, the result is reported as PARTIAL, with the completed fraction per bin. Batches are never partially labelled: a batch that started is finished, or its sentences are excluded entirely.

---------------------------------------------------------------------------------------------------
## 8. Failure modes and fallbacks

| Failure | Response |
|---|---|
| Pool-reproduction assert fails | Stop. Debug the environment (package versions from uv.lock, data_local sha). Never proceed on a different pool |
| A generator id is no longer served | Prereg slot rule; flag it. If > 2 slots are substituted, report V0 on the unsubstituted-peer subset too |
| E2-B L25 NOT TESTABLE (< 50 CORRECT) | Expected CORRECT ≈ 0.20 × 7.9 rows × 148 ≈ 234, so unlikely. If it happens, report counts and contribute to the union only |
| M1 absent | See Step 3.1. V0 and PT are unaffected |
| M3 absent | Standalone E2-B plus the runnable `union.py` |
| Budget stop mid-run | Completed batches form a random prefix, NOT completion-selected. State the fraction |
| Frontier parse failures > 10% | Report coverage. AUROC on the parsed rows with IPW; failures listed |

---------------------------------------------------------------------------------------------------
## 9. Outputs (every file cited in `tables.md` by path; every table row carries its source line)

- `e2b/`: `sentences_E2B.json`, `census_E2B.json`, `seal.json`, `testability_E2B.json`, `E2B_SURPLUS_CLAIM.json`, `E2B_FINAL_READY.json`
- `scores/`: `scores_E2B.jsonl`, `score_seal.json`, `file_access_log.txt`, `judges_costmatched.jsonl`, `judge_frontier.jsonl`, `frontier_subsample.json`
- `analysis/`: `per_item_E2B.jsonl`, `confirm_verdict_E2B.json`, `union_longpool.json` (or NOT_COMPUTED), `union.py`, `tables.md`
- `method_out.json` (exp_gen_sol_out; validate it with aii-json and generate the mini/preview variants). Each example = one candidate row. Keys:
  - input = JSON{text, candidate_fol, system};
  - output = the final label;
  - `predict_V0`, `predict_flashlite_disg`, `predict_costmatched_disg`, and so on;
  - `metadata_*` for stratum, tier and sample.
- `prereg_iter5_E2B.json` + sha256, `deviations.json` (D-E2B, D-E2B-comp, D-E2B-drift?, D-E2B-M1?, and every slot substitution), `cost_ledger_master.jsonl`
- `README.md` with the layout, how to run, and a "Restoring removed files" section. `.aii/manifest.yaml`:
  - `e2bsrc/.venv/`: delete, regenerable (`cd e2bsrc && uv sync`);
  - `e2bsrc/data_local/`: delete, redownloadable (copied from gen_art_dataset_4/data_local);
  - raw/, work/ and sealed/: KEEP (paid, irreproducible).
- Run aii-file-size-limit on any file > 100 MB, since generations are small.

---------------------------------------------------------------------------------------------------
## 10. domain_practice (what the field does for this kind of study; what I read)

Read for this step:
- the neurosymbolic handbook (S13: FOLIO/MALLS gold 36-39% wrong; S6: compile ≠ faithful; open question 3: no agreed gold-free faithfulness metric);
- E2's `prereg_E2.json`, `census_E2.json`, `select_e2.py`, `pilot_projection.json` and `run_all.sh`;
- eval-3 `power_E2.json`;
- exp-6 `analyse_T1.py` / `api_bar.py` and the vendored `judges.py`;
- the WMT24 metrics-task results and Thompson et al. 2024 (soft pairwise accuracy; PERM-INPUTS significance and greedy significance clusters), via search.

Items marked (SK) are standing knowledge, not re-fetched this step.

BASELINES. Reference-free metric papers are judged against the incumbent a practitioner would actually use.
- In summarisation factuality (TRUE, Honovich et al. 2022; SummaC, Laban et al. 2022) the incumbents are NLI/QA metrics and, since 2023, LLM judges (G-Eval) (SK).
- In MT (WMT23-24) every submission is compared with the strongest LLM-judge metric of the year (GEMBA/xCOMET class) and with the baseline metric set (Freitag et al. 2024).
- The first comparator a reviewer names is a STRONGER judge at MATCHED COST, not the cheapest judge. The second is a frontier judge. That is exactly why this direction adds deepseek-v3.2 and gemini-3.1-pro.
- Fair tuning: the SAME prompt/rubric for every judge, no per-judge prompt engineering on test data, and temperature 0 (SK).

DATA. Fresh, untouched test data scored ONCE with frozen parameters is the WMT norm: a new test set every year, and metrics are submitted before the test outputs are released. FOLIO/MALLS original gold is noisy (S13), so labels come from an audited process (solver + blind disguised panel), not raw gold. ProverQA is the contamination-resistant alternative (handbook decision guide).

CONTROLS.
- Identical code for labels and metrics across samples.
- Seal scores before labels.
- LLM-judge self-preference: judges favour their own family's outputs (Panickssery et al. 2024; Zheng et al. 2023 MT-Bench) (SK). So own-family rows must be controlled.
- Contamination via memorised gold: disguised vs original views.
- Composition confounds between samples (here, word length).

HOW MUCH IS ENOUGH.
- Item-level meta-evaluation CIs must respect the clustering of outputs within an input. Deutsch et al. 2021 (TACL) showed that bootstrapping over inputs and systems gives much wider CIs than naive ones (SK), and WMT uses permutation tests over inputs (PERM-INPUTS).
- AUROC differences of about 0.05 need hundreds of positives and negatives. The field-standard move when underpowered is MORE graded items, stated with an a-priori MDE. Here that is the eval-3 MDE: +0.069 needs about 882 planned L25 sentences.
- Replication across two independent samples is judged with a heterogeneity statistic (Cochran's Q / I²), not by counting significant results (SK; meta-analysis norm).

MEASURES.
- Item level: ROC AUC is the standard for binary faithfulness (TRUE), with AUPRC for imbalance, and threshold-free.
- System level: pairwise accuracy / Kendall τ (WMT), with significance clusters.
- Ties must be handled explicitly (Deutsch et al. 2023, "Ties Matter") (SK). c_score_align is quantised, and AUROC counts ties as 0.5.
- Cost is reported per item, in $, with a fixed unit.

---------------------------------------------------------------------------------------------------
## 11. practice_alignment (point by point)

MEETS:
- Fresh, untouched data, scored once with frozen code and a score seal before the label join. This is WMT's fresh-test-set norm, and it is stronger than WMT's because of the hash seals and the file-access log.
- Paired, item-level, threshold-free AUROC with a sentence-cluster bootstrap. This matches the Deutsch/WMT concern about input clustering.
- The a-priori MDE is stated for every cell. The response to underpowering is more graded sentences (this artifact's purpose), not more metrics.
- A cost-matched stronger judge and a frontier judge, with the SAME rubric byte-identical. This closes the "you beat a weak judge" objection within budget.
- Contamination: disguised and original views for the cheap and cost-matched judges.
- Self-preference: own-family exclusion per judge (added in §5.11 because it was missing from the direction).
- Nesting over the best baseline stack (S4) with cross-fitting.
- Replication is judged by a heterogeneity test, not by "both significant". Multiplicity is handled by fixed-sequence testing (added in §6.2).
- Completion selection is prevented by the hash-ordered batches of 50, each completed end to end.

DEPARTS:
1. The frontier judge runs on the ORIGINAL view only, on 300 rows (about 200 usable), so its AUROC CI will be wide (about ±0.07).
   - Justification: budget ($1.1), and T1's precedent, which makes it comparable with iteration 3's frontier numbers.
   - Cost: the V0/frontier ratio stays close to descriptive, as in T1 (0.957 [0.887, 1.034]). The paper cannot claim "matches frontier" from it. There is also no disguised frontier view, so frontier contamination is not measured.
2. Labels come from a 3-family LLM panel plus the solver, not human annotators.
   - Justification: this is E/E2's frozen protocol, and the only one that gives an L25 CORRECT class (F4). Its accuracy is measured (gate items, track H), and a drift gate precedes it.
   - Cost: panel strictness (it accepts 0.61 of expert-corrected formulas on E) biases towards ERROR. The R_A sensitivity and the DRIFTED branch are reported. A human-annotated subset would be the field's preference, and none is affordable here.
3. E2-B is drawn from the same MALLS-train source as E and E2-A. It is untouched but NOT a different distribution. It is also mostly 25-29 words (F1), so it is not identically distributed to E2-A's L25.
   - Justification: the ≥30 supply is exhausted, and the rule is frozen. Domain transfer is DT's job (in E2-A).
   - Cost: the union L25 over-represents 25-29 words relative to E's L25. Word-bin strata and a within-bin heterogeneity check are pre-declared.
4. The cost-matched judge (deepseek) is also a GENERATOR family (G4), and the frontier (Gemini) shares a family with G8 and with flash-lite.
   - Cost: possible self-preference. It is handled by the §5.11 exclusion, not avoided.
5. The union's pooled bootstrap treats E2-A and E2-B as strata. The meta-analytic fixed-effect cross-check assumes a common effect.
   - If heterogeneity is significant, the fixed-effect pool is not the right summary. A random-effects estimate with 2 studies is not identifiable in any useful way, so the per-sample results are then the primary reading. Pre-declared.
6. System-level τ-b uses about 10 systems, far fewer than WMT's.
   - It is descriptive only, and the paper must not rank metrics on it.
7. No DeLong test is used; the cluster bootstrap is used instead, because DeLong assumes independent items.
   - Cost: none. This is the field's recommended treatment for clustered outputs.
8. Ties: the quantised c_score (|P| ≤ 9) has many ties. AUROC counts ties as 0.5, consistently for every metric.
   - Report the tie rate per metric so that a reader can see where quantisation limits the attainable AUROC.

Residual credibility risk a reviewer would raise first: the label regime (the panel) is shared by E2-A and E2-B. The union therefore adds SAMPLING power, not LABEL-regime independence. Instrument-disjoint confirmation is R_COMP FREE's role (the sibling artifact). This must be stated in the union's verdict text.
````

### [55] TOOL RESULT — Write · 2026-09-24 11:04:25 UTC

````
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_plan/gen_plan_experiment_2/plan.md", "content": "# PLAN — experiment_iter5_dir2: E2-B, a second untouched L25 replication sample, plus a cost-matched and a frontier judge\n\nType: EXPERIMENT. Deps: art_2OmxzMInZZJY (E2 sampling frame and frozen code), art_U4Hsqt4Ay9Tg (dataset E: dev data, fold recipe, weights), art_zcwCQgTqk6DN (rename controls, `perturb.control_rename`).\nHard cap: $9.5 of OpenRouter spend. Reserve: 10%. Wall clock: 6 h.\n\n---------------------------------------------------------------------------------------------------\n## 0. What this artifact is for, in one paragraph\n\nE2-A (the sibling artifact) labels 350 fresh L25 sentences. At E's yield of 0.37 usable sentences per built sentence, that gives an L25 MDE80 of 0.110 against flash-lite disguised (eval-3 `power_E2.json`). The observed E effect is +0.069, so E2-A alone has about 42% power for it.\n\nE2-B adds about 400 more L25 sentences. They are drawn by E2's frozen rule and processed by E2's byte-identical code.\n\nPower, computed from `power_E2.json` se_fit L25|flashlite_disg, where SE = e^a · n_usable^b with a = −0.795 and b = −0.503:\n\n| Sample | Planned | Usable | SE | MDE80 | Power at +0.069 |\n|---|---|---|---|---|---|\n| E2-B alone | 400 | ≈148 | 0.037 | 0.103 | 0.47 |\n| UNION L25 (E2-A 350 + E2-B 400) | 750 | ≈277 | 0.027 | ≈0.075 | ≈0.73 |\n\nThis is the only route in this iteration by which the user's priority stratum (L25) can reach adequate power. More metrics would not help; more graded sentences would.\n\nE2-B also adds the two comparators a reviewer names first:\n- a COST-MATCHED stronger cheap judge (deepseek-v3.2, reasoning off);\n- the FRONTIER judge (gemini-3.1-pro-preview) on a 300-row subsample.\n\nEvery number that E2-B reports on its own is secondary to the union, except where §6 says otherwise.\n\n---------------------------------------------------------------------------------------------------\n## 1. Facts from the sampling frame that change the design (read from gen_art_dataset_4; the executor must re-verify)\n\nF1. Supply. `census_E2.json` counts the L25 supply after filters: 960 at 25-29 words, 186 at ≥30 words, and 0 at ≥35. E2's base takes 158 long + 192 short sentences. The surplus of 98 (`prereg_E2.json` pool_order.L25 positions 351-448; `l25_tier == \"surplus\"` in `work/pool_E2.json`) is about 28 long + 70 short. After the surplus, the ≥30-word bin is EXHAUSTED.\n- E2-B is therefore about 28 long + about 372 short sentences at 25-29 words.\n- E2-A's L25 is 45% long; E2-B's is about 7% long.\n- This is a real composition difference. It must be (a) pre-registered, (b) handled by word-bin strata in the union, and (c) named as the first candidate explanation for any A-vs-B heterogeneity. It is NOT a reason to change the rule: long supply does not exist.\n\nF2. Build-order dependence of the 12-gram rule. In `select_e2.py`, `take()` shares one `accepted_grams` set across the build order EXC → L25 base+surplus → DT.\n- To continue \"the same rule\", E2-B must seed `accepted_grams` with the 12-grams of ALL E2 rows: EXC 100, L25 448, DT 110 including the reserve.\n- It must then continue `take(short, …)` and `take(long_, …)` over the SAME sha1 order ('E2_v1|' + sentence_id), skipping every `used` id.\n- The E-exclusion (E's 700, calibration, few-shot, screen, FOLIO, curated sets) and E's 12-gram filter are inherited unchanged.\n- Implement this as a NEW wrapper `src_e2b/select_e2b.py`. It imports `select_e2.py` functions, re-runs the frozen selection, asserts that it reproduces `work/pool_E2.json`'s sha256 `98cdccff…`, and only then continues the order. If the reproduction assert fails, STOP and debug. Never select E2-B from a pool that differs from E2's.\n\nF3. Costs (`pilot_projection.json`, E-measured; the E2 panel pilot never ran). Per L25 sentence:\n\n| Item | $ per sentence |\n|---|---|\n| generation | 0.00100 |\n| panel stage 1 | 0.00664 |\n| P1 adjudication | 0.00277 |\n| reference repair | 0.00141 |\n| **total** | **0.01182** |\n\nF4. Without the panel, E2's final rule yields no CORRECT rows on MALLS strata. The 30-sentence pilot gave 36 ERROR / 244 UNRESOLVED / 0 CORRECT. E's L25 CORRECT class (176 rows) comes almost entirely from tier B and reference repair. So the panel is what makes L25 testable at all. See §4 for the drift branch.\n\nF5. The frozen judges (vendored in `iter_4/gen_art/gen_art_experiment_9/vendor/e8src/vendor_d/judges.py`; the originals are exp D, used by exp 5 `run_api_E.py` and exp 6 `api_bar.py`):\n- flash-lite = `google/gemini-2.5-flash-lite`, `judge_json(RUBRIC_A, USER_JSON_A, max_tokens=150)`, run on the disguised view and the original view;\n- nano = `openai/gpt-4.1-nano`, `judge_logprob(RUBRIC_A)` → 1 − P(YES);\n- frontier = `api_bar.frontier_judge`, `google/gemini-3.1-pro-preview`, reasoning effort \"low\", max_tokens 4000.\n\nAssert that `judges.PROMPT_SHA` equals the sha1 recorded in exp 5/6 before any judge call.\n\nF6. The S4 stack is exp 6 `analyse_T1.py::s4_nesting`: S4_local plus the API features with ≥95% R_AB coverage. Missing API features are substituted by their local counterparts, logged in `substituted`.\n\n---------------------------------------------------------------------------------------------------\n## 2. Workspace layout (all under this artifact's gen_art workspace, called <WS> below)\n\n```\n<WS>/e2bsrc/           copy of gen_art_dataset_4 CODE ONLY (see Step 0.2) — E2's byte-identical pipeline\n<WS>/e2bsrc/src_e2b/   NEW wrappers (select_e2b.py, activate_e2b.py, budget.py) — E2 files untouched\n<WS>/freeze_copy/      copies of the M1 frozen files (consensus_variants.py, selection.json, gg.py, gg_gate.json)\n<WS>/e2b/              sealed rows, seal.json, testability_E2B.json, E2B_FINAL_READY.json, E2B_SURPLUS_CLAIM.json\n<WS>/scores/           scores_E2B.jsonl, score_seal.json, judges_*.jsonl\n<WS>/analysis/         per_item_E2B.jsonl, confirm_verdict_E2B.json, union_longpool.json, tables.md\n<WS>/prereg_iter5_E2B.json (+ .sha256)   <WS>/deviations.json   <WS>/cost_ledger_master.jsonl\n<WS>/method_out.json (exp_gen_sol_out)   <WS>/README.md   <WS>/.aii/manifest.yaml\n```\n\n---------------------------------------------------------------------------------------------------\n## 3. Timeline (6 h wall clock; T = start)\n\n| Window | Work |\n|---|---|\n| T+0:00-0:30 | Step 0: setup, probe, selection, prereg + hash, surplus claim |\n| T+0:30-3:15 | Step 2: generation → solver labels → panel, in batches of 50 in sha1 order. In parallel from batch 1: label-free judges and consensus peers-only scoring |\n| T+0:30-1:30 | Step 1: poll for M2 (drift), which gates the panel. Generation and solver labels do not wait |\n| T+1:30-4:00 | Poll for M1 (freeze). Label-free scoring of every frozen variant as soon as it lands |\n| T+3:15-3:45 | Seal the labels; seal the scores; verify both |\n| T+3:45-4:45 | Join; E2-B analyses; write E2B_FINAL_READY.json |\n| T+4:45-5:30 | Poll for E2A_FINAL_READY; union + meta-analysis |\n| T+5:30-6:00 | Tables, README, manifest, method_out.json, validation |\n\nHard deadlines, written into the prereg:\n- M2 T+1:30;\n- M1 variants T+2:30;\n- M1 GG T+4:00;\n- last paid call T+4:30;\n- M3 (E2-A) T+5:30.\n\n---------------------------------------------------------------------------------------------------\n## 4. Step-by-step\n\n### Step 0 — Setup, prereg, selection ($0 except a 1-token probe)\n\n0.1 Read the skills aii-python, aii-openrouter-llms, aii-parallel-computing, aii-long-running-tasks and aii-json. Make a 1-token probe call through `OPENROUTER_BASE_URL` / `OPENROUTER_API_KEY` and log it.\n\n0.2 Copy `iter_4/gen_art/gen_art_dataset_4` to `<WS>/e2bsrc`, EXCLUDING the following:\n- `.venv/`;\n- `raw/generations.jsonl`, `raw/*` of E2's pilot;\n- `work/labels_heldout*.jsonl`, `work/panel_cache.jsonl`, `work/sentences*.json`;\n- `sealed/`, `seal.json`;\n- `cost_ledger.jsonl`, `.aii_cost_ledger.jsonl`;\n- `full/mini/preview_data_out.json`.\n\nKeep:\n- `src/`, `labeller/`, `src_e2/`, `src_d3/`, `prompts/`, `data_local/`, `E_ref/`, `tests/`;\n- `code_freeze.json`, `prereg_E2.json`, `census_E2.json`;\n- `work/pool_E2.json`, `work/models_snapshot_E2.json`, `work/fewshot_exemplars.json`, `work/calibration_items.json`;\n- pyproject/uv.lock.\n\nThen:\n- Run `uv sync` in `e2bsrc` (Python 3.12).\n- Verify every sha256 in `prereg_E2.json.labeller_sha256` and `code_freeze.json` against the copied files. Write `e2bsrc/code_freeze_check_E2B.json`. A mismatch stops the run.\n- Start with a CLEAN raw/work state, so E2's pilot rows can never leak into E2-B's assemble step. `assemble_e2.py` reads whatever is in `raw/`.\n\n0.3 `src_e2b/select_e2b.py` (F2):\n1. Reproduce E2's selection and assert the pool sha256.\n2. Take the 98 surplus in their `e2_rank` order.\n3. Continue the sha1 order over the remaining eligible L25 rows (long first, then short, the same `take()`), with `accepted_grams` seeded from every E2 row. Target a total of 400.\n4. Also write the next 150 in order as a reserve, used only if more than 10% of sentences fail gold parse or generation.\n\nRecord:\n- the per-bin supply remaining (expected ≈ 0 long, ≈ 690 short);\n- the within-E2B 12-gram drops;\n- the collision checks (0 text or 12-gram collisions with E and E2 must be asserted).\n\nOutputs: `e2b/sentences_E2B.json`, `e2b/census_E2B.json`.\n\n0.4 Batches: order the 400 by sha1('E2B_batch_v1|' + sentence_id) and cut them into 8 batches of 50. Batch 1 must contain surplus AND continuation sentences in proportion. The order is a hash, not a choice.\n\n0.5 `prereg_iter5_E2B.json`, written and hashed BEFORE any E2-B generation. It contains:\n\n(a) Deviation D-E2B: \"a pre-registered replication sample drawn by E2's frozen rule, beyond E2's freeze, reason = power (eval-3 power_E2.json: L25 needs ~882 planned sentences for +0.069)\". Also D-E2B-comp: \"E2-B is ~93% 25-29 words because the ≥30 bin is exhausted (F1)\".\n\n(b) The selection algorithm and its expected hashes.\n\n(c) The metric list, verbatim from the SHARED CONTRACT's frozen definitions (V0-V5, PT, GG), with V0 as the PRIMARY.\n\n(d) Comparators:\n- flash-lite disguised (primary comparator), flash-lite original, nano original;\n- cost-matched deepseek-v3.2, disguised (primary cost-matched) and original;\n- frontier gemini-3.1-pro-preview, original.\n\n(e) The confirmatory hierarchy of §6 with its α, and MDEs stated in advance: E2-B L25 0.103; union L25 ≈0.075; union long pool ≈0.07 (L25 ≈277 + E2-A EXC ≈64 usable, SE from the long se_fit).\n\n(f) The union and meta-analysis rule (§6.3), the tie-breaking and duplicate rule (§4 Step 2.5), and the frontier subsample recipe.\n\n(g) The cost-matched judge spec: the byte-identical RUBRIC_A text, USER_JSON_A, `reasoning: {enabled: false}`, temperature 0, max_tokens 150, and the JSON parse rule of `judges.parse_judge_json`.\n\n(h) The shrink order: GG scoring → frontier → cost-matched original view → L25 sentences, at a floor of 250, always an 8-batch-order prefix.\n\n(i) The deadlines.\n\n0.6 Surplus claim. Write `e2b/E2B_SURPLUS_CLAIM.json` with token 'aii_iter5_e2b_surplus_v1' and the 98 ids. The hypothesis's P3 lets E2-A add the same surplus \"if budget remains\", so a collision is possible. The rule: a sentence labelled by both artifacts counts ONCE in the union, taking E2-B's copy. The duplicate pairs give a free test-retest label agreement, reported as the κ of final labels.\n\n### Step 1 — Drift decision (M2)\n\nPoll `glob('/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/*/e2/E2_DRIFT_DECISION.json')` every 5 minutes, and check the token 'aii_iter5_e2_drift_v1'. Log every attempt.\n\n- PASS: use its pinned provider for each of P1/P3/R1 (OpenRouter `provider: {order: [...], allow_fallbacks: false}`). Record it.\n- FAIL: run the panel anyway, under the same pinned protocol that E2-A uses for its drifted labels. Mark every E2-B label `label_regime = DRIFTED`. All E2-B and union results become SECONDARY. Report tier-A-only (R_A) rows alongside.\n  - Why not skip the panel: F4 shows that a no-panel regime has no L25 CORRECT class. A drifted but internally consistent regime shared by E2-A and E2-B is the only testable one.\n- ABSENT at T+1:30: run E2's gate yourself, as E2's `run_all.sh` step 3: `gate.py --mode synthetic` and `--mode trackh` with members P1,P3,R1, then `drift_report.py`. That costs about $0.3 against caps of 0.30 + 0.50.\n  - Use the same pinning procedure: pin the provider that serves each id at the time of the call, and record it.\n  - Book this as deviation D-E2B-drift.\n  - Apply E2's stop rule verbatim: majority agreement < 0.85 → FAIL.\n  - Also compute the hypothesis's criterion: the track-H flag rate on original errors must fall within the 95% CI of E's 0.84.\n  - If E2-A's M2 appears later, report both decisions. The union uses E2-A's decision.\n\n### Step 2 — Generation + labels, in batches of 50, each completed end to end\n\nFor each batch b = 1..8, in order:\n\n2.1 Budget check (§7). Stop BEFORE a batch if its estimate exceeds the remaining budget minus the reserve.\n\n2.2 Generation:\n```\ne2bsrc/src_e2/e.py generate.py --slots G1,G1b,G2,G3,G4,G5,G6,G7,G8,G9 --variants fewshot_v1 --sentences <batch file> --cap <remaining>\n```\nThen `gen_retry.py`. Apply the slot-unavailability rule from `prereg_E2.json`: same family, nearest current instruct model, flagged `slot_substituted`.\n\n2.3 Solver labels: `run_label.py --kind heldout --workers 4`.\n\n2.4 Panel, only after M2 is resolved:\n- `panel_run.py --members P3,R1`;\n- `--adjudicate P1`;\n- `src_e2/repair.py`;\n- `run_label.py --refs work/reference_overrides.json`.\n\nEach script is wrapped by `src_e2b/activate_e2b.py`, which points `work/sentences.json` at the cumulative E2-B set, so the frozen scripts run unchanged. If E2's scripts cannot be restricted to a batch, run them on the cumulative set: they are resumable, skip sentences already done, and the panel cache never re-bills.\n\n2.5 After each batch, log:\n- rows, parse rate, spend per sentence (actual vs F3);\n- the count of completed sentences per word bin.\n\nDo NOT look at labels or score-label joins. The only label-derived quantity allowed before the seal is the count of CORRECT/ERROR per stratum, needed for testability. Write it to `e2b/progress.jsonl`.\n\n2.6 After the last batch (or a budget stop), run:\n- `assemble_e2.py`;\n- `controls_e2.py`: RENAME_SYN / RENAME_NONCE on up to 300 final-CORRECT rows, via dataset 3's `perturb.control_rename`, z3-verified;\n- `testability_e2.py`: rule verbatim, ≥50 ERROR, ≥50 CORRECT, ≥25 sentences each;\n- `seal_e2.py`, `verify_seal.py`.\n\nAll of these run under `e2bsrc` with E2B output names. `seal.json` is copied to `e2b/seal.json`, and E2-B's testability is written to `e2b/testability_E2B.json`.\n\nLabel-free work that runs in PARALLEL from batch 1 (it only needs `candidates_E2B_nolabels`-equivalent rows = generations + parse status; it never touches labels):\n\n(i) Cheap judges on every parseable row: flash-lite disguised, flash-lite original, nano original.\n- Disguise: `labeller/disguise.py`, as in exp 5's `build_disguise`.\n- An unparseable candidate is scored 1.0 (flagged), as for every metric.\n- About 3,700 rows × 3 calls × ~$5e-5 ≈ $0.55.\n\n(ii) The cost-matched judge (Step 3.2).\n\n(iii) Local features for S4: L2-bow, the L3-free local round-trip counterparts and the local Qwen3-8B judge, IF the vendored code runs on this machine's hardware. Check with aii-use-hardware. If there is no GPU, drop the local judge from S4 and record it in `substituted`.\n\n### Step 3 — Label-free scoring + score seal\n\n3.1 Freeze marker (M1). Poll\n```\nglob('/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/*/freeze/CONSENSUS_FREEZE_READY.json')\n```\nevery 5 minutes and check the token 'aii_iter5_consensus_freeze_v1'. Copy `consensus_variants.py`, `selection.json`, `gg.py` and `gg_gate.json` into `<WS>/freeze_copy/`, and verify their sha256 against the marker. Never import across paths.\n\nScoring of each metric:\n\n| Metric | How it is scored on E2-B |\n|---|---|\n| V0 c_score_align | exp-5 `pool_scoring.py` byte-identical (`iter_2/gen_art/gen_art_experiment_5/src`). Assert the file sha against exp 5. Scored immediately; it does NOT wait for M1 |\n| PT p_peer_text | exp-5 `peer_text.py` + the frozen fusion coefficients. Also immediate |\n| V1-V5 | from `freeze_copy/consensus_variants.py` |\n| V2 / V3 / V5 weights w_f | out-of-fold over E2-B's OWN sentences, fold = sha1('E2_folds_v1\\|' + sentence_id) % 5, shrunk with 20 pseudo-sentences. Label-free |\n| V4 | coefficients from `selection.json` (fit on E, frozen). Never refit |\n\nFor the union, V2/V3/V5 are recomputed out-of-fold over the union's sentences with the same recipe. This is declared in the prereg because it is still label-free.\n\nIf M1 is ABSENT at T+2:30:\n- implement V1 and V2 from the verbatim contract text in `<WS>/fallback_variants.py`;\n- score them as REPORTED-ONLY rows;\n- H-IMPROVE is recorded as \"no carried variant available to E2-B\" (deviation D-E2B-M1);\n- V4 and V5 are not scored (both need E-fitted objects).\n\nThe GG branch:\n- If `gg_gate.json` = PASS by T+4:00: score c_gg on E2-B with `freeze_copy/gg.py` (its gloss model id and prompt sha). Gloss calls are paid. Pilot on 20 sentences, estimate the cost, and run only if the estimate is ≤ $0.4 AND fits §7.\n  - GG is the FIRST item in the shrink order.\n  - Score GG on (a) all L25 rows and (b) the rename controls.\n- FAIL or absent: GG is not scored, and this is recorded.\n\n3.2 The COST-MATCHED judge: `deepseek/deepseek-v3.2`, `extra={\"reasoning\": {\"enabled\": false}}`, `judges.judge_json(RUBRIC_A, USER_JSON_A, max_tokens=150)`. The prompt is byte-identical to flash-lite's.\n\nPilot on 30 rows, the first 30 parseable rows of batch 1 in sha1 order, both views. Report the parse rate, the $ per call and the latency.\n- Parse failure > 10%: raise max_tokens to 300 once, as a pre-declared single retry rule, and log it.\n- Still > 10%: report as NOT_TESTABLE_PARSE.\n\nBudget:\n- Run the DISGUISED view on all parseable rows. It is the cost-matched primary: disguised is the contamination-safe view, matching flash-lite disguised.\n- Run the ORIGINAL view on all rows if the pilot cost is ≤ $1.6e-4 per call. Otherwise run it only on the frontier subsample plus as many L25 batches (in order) as fit the budget, and record the coverage.\n\nThe cost-matching claim is stated in $/candidate: deepseek measured, vs consensus FULL $1.21e-4 (9 peers) and MARGINAL (cost_units.csv).\n\n3.3 The FRONTIER subsample:\n- Size: 300 candidate rows.\n- Drawn right after generation is complete and BEFORE any label join.\n- Stratified by label-free words tercile (tercile cut-points from E2-B's sentences) × system family (10 slots → 9 families), allocated proportionally with a minimum of 3 per cell.\n- Sampled within cells by sha1('E2B_frontier_v1|' + row_key).\n- Store the inclusion probabilities.\n\nRun `api_bar.frontier_judge` (original view, effort \"low\", max_tokens 4000).\n- Pilot 10 rows for cost. Expected ≈ $3.65e-3 per item, so ≈ $1.1.\n- If the pilot shows > $6e-3 per item, cut to the largest prefix of the sha1 order that fits, and recompute the inclusion probabilities.\n\nAbout 2/3 of the rows are expected to land in R_AB, i.e. about 200 usable. State this in the prereg: the frontier ratio will have a wide CI.\n\n3.4 Score seal. `scores/scores_E2B.jsonl` holds one row per row_key with every metric and judge score, plus the parse status. Write `scores/score_seal.json` with:\n- the sha256 of the scores file;\n- the sha256 of every scoring source file: `pool_scoring.py`, `peer_text.py`, `freeze_copy/*`, `judges.py`, the control-scoring code;\n- the frontier-subsample file;\n- the M1/M2 marker hashes.\n\nThe scoring code may read ONLY the following (the file-access allowlist):\n- `e2bsrc/raw/generations*.jsonl`, `candidates_E2B_nolabels.jsonl`, `controls_E2B_nolabels.jsonl`;\n- `e2b/sentences_E2B.json` (text + label-free strata);\n- `freeze_copy/*`;\n- exp-5 code;\n- the judge caches.\n\nEnforce this with a wrapper that monkey-patches `builtins.open` to refuse paths under `sealed/` or containing 'label' or 'reference', and logs every path opened to `scores/file_access_log.txt`. This is cheap, and a reviewer can check it.\n\nControls (rename) are scored for V0, PT, and GG if GG passed, with the same code, before the join. They are included in the score seal.\n\n### Step 4 — Join\n\nJoin only after both `verify_seal.py` (labels) and a `verify_score_seal.py` (the score hashes still match) pass. `analysis/per_item_E2B.jsonl` holds:\n- row_key, sentence_id, stratum (L25_E2B), word_bin, words, n_conditions, system, family;\n- label, tier, reading_choice, contested;\n- every score;\n- in_frontier_subsample, ipw.\n\n### Step 5 — Analyses (E2-B)\n\nReuse code. The stratified AUROC, the cluster bootstrap and `fit_s4_oof` come from exp 6's `analyse_T1.py`, copied, with its sha recorded. Use the SAME functions that E2-A uses where they are shared. If E2-A's analysis module is available via its M3 pointer, diff it against ours and report any difference.\n\nPopulations:\n- R_AB = LLM systems only (no gold-as-system), tiers A+B, excluding CONTESTED and reading_choice (the primary);\n- R_A = tier A only (sensitivity);\n- CONTESTED counted as CORRECT, and as ERROR (sensitivity).\n\n5.1 PRIMARY E2-B cell: L25_E2B, strat AUROC Δ = V0 − flash-lite disguised.\n- Sentence-cluster bootstrap, B = 2,000, percentile 95% CI, strata = word bin (25-29 / ≥30).\n- Also V0 − flash-lite original, V0 − nano, V0 − cost-matched (disguised and original).\n- Report the AUROC of each metric with its CI, the AUPRC, and the counts (rows, ERROR, CORRECT, sentences with both classes).\n\n5.2 Frontier (subsample, IPW-weighted AUROC as in T1):\n- AUROC of the frontier, V0 and S4_E2B;\n- ratio V0 / frontier with a bootstrap CI (resample sentences within the subsample);\n- nested [frontier + V0] − frontier (cross-fitted logistic, 5 sentence folds).\n\n5.3 Nested over S4_E2B: `fit_s4_oof` on S4_full-equivalent features, cross-fitted by E2-B sentence folds. Compare [S4_E2B + V0] − S4_E2B, with its strat CI. Record every substituted feature.\n\n5.4 H-MECH (i)-(iv) on E2-B CORRECT candidates (L25_E2B), with the definitions and code copied from eval 3 (art_BvAL_KZTZuw8, pair classes) and eval 2 (SCATTER, NET):\n- (i) the share of non-agreeing peers labelled ERROR (≥ 0.50);\n- (ii) the SCATTER ratio SI_cor/SI_err (≥ 2);\n- (iii) NET Δ(e+d) over the words terciles (> 0). With E2-B's narrow 25-29 range, the terciles are narrow, so report it, and flag range restriction;\n- (iv) exact vs ALIGN per class: ALIGN d lower, e higher on MEANING_RENAME-type and ADD/DROP. Use e/d as defined in exp 9 (art_D7k2ZWgE3nVd) `src/analyse.py`: e = the fraction of ERROR candidates the peers endorse (c ≤ 0.5), d = the fraction of CORRECT candidates flagged (c > 0.5). If the code differs from this gloss, the code wins.\n\nEach item is scored CONFIRMED or REFUTED with its CI.\n\n5.5 H-IMPROVE: carried variant − V0 on L25_E2B (and in the union). If `selection.json` = 'NONE: V0 stands', report V1-V5 as development-only rows.\n\n5.6 Rename, on the E2-B CORRECT controls:\n- FA at c > 0.5 for V0 and PT, and GG if scored;\n- the PAIRED FLIP (the control flagged while its original was not) with a Wilson CI;\n- the base FA of the originals shown next to every FA.\n\n5.7 Complexity curves: AUROC and FA against words, n_conditions, n_quant and depth, with bins pre-declared at the E2-B quartiles, for V0, flash-lite disguised, cost-matched and nano.\n\n5.8 Coverage: parse rate per system, with unparseables in the denominator (scored 1.0), and consensus-scorable rate (|P| ≥ 1).\n\n5.9 Cost per candidate, FULL and MARGINAL, for every metric and judge, in $ and in seconds, from the ledger: V0 FULL = the 9 peer generations + z3 time; MARGINAL = z3 only. This is the \"does a large judge earn its cost\" row: AUROC gain per extra $ vs flash-lite, for deepseek and for the frontier.\n\n5.10 System-level: Kendall τ-b between each metric's system mean and the gold system accuracy (13 system × variant rows if available; here 10 slots, so say so), with a sentence-bootstrap CI. Descriptive only.\n\n5.11 Judge self-preference control. For each judge, AUROC recomputed excluding rows generated by the judge's own family:\n- flash-lite and the frontier → drop G8 (google-gemini);\n- nano → drop G7 (openai);\n- deepseek → drop G4 (deepseek).\nConsensus is already leave-own-family-out, so this puts the comparison on equal footing. Report Δ with and without.\n\n5.12 `confirm_verdict_E2B.json` holds each §6 claim with its verdict, the numbers, and the population. Then write `e2b/E2B_FINAL_READY.json` with token 'aii_iter5_e2b_final_v1', the path to `per_item_E2B.jsonl`, its sha256, the label regime (PASS/DRIFTED) and the completed fraction per bin.\n\n### Step 6 — UNION and meta-analysis\n\nPoll for `glob('…/iter_5/gen_art/*/e2/E2A_FINAL_READY.json')` (token 'aii_iter5_e2a_final_v1') until T+5:30.\n\nPresent:\n- Load E2-A's per-row file read-only and verify its sha256.\n- Harmonise the columns. The required columns are listed in the contract; any missing column → that analysis is NOT_COMPUTED, stated.\n- Apply the duplicate rule (Step 0.6).\n- If E2-A's label regime ≠ E2-B's (one PASS, one DRIFTED), the union is computed but marked SECONDARY, and the per-sample results are primary.\n- Compute §6.2 and §6.3.\n\nAbsent: write `analysis/union.py`, runnable later with one command (`uv run analysis/union.py --e2a <path>`), and record union = NOT_COMPUTED_E2A_MISSING. If E2-A also computes the union, both must use the same definitions. Report the sha of the inputs so the two can be checked for identity.\n\n---------------------------------------------------------------------------------------------------\n## 5. Metric and comparator table (what is scored on E2-B)\n\n| Row | Role | Source | $ (est.) |\n|---|---|---|---|\n| V0 c_score_align | PRIMARY | exp-5 `pool_scoring.py`, leave-own-family-out, 10-slot pool | 0 (peers are the generations) |\n| PT p_peer_text | secondary | exp-5 | 0 |\n| V1-V5 | H-IMPROVE (only the carried variant is confirmatory) | freeze | 0 |\n| GG | H-RENAME (only if the gate PASSED) | freeze gg.py | ≤ 0.4 |\n| flash-lite disguised | primary comparator | vendor_d judges | ~0.19 |\n| flash-lite original | comparator | same | ~0.19 |\n| nano original (logprob) | comparator | same | ~0.19 |\n| deepseek-v3.2 disguised | COST-MATCHED primary | RUBRIC_A byte-identical | ~0.9 (pilot) |\n| deepseek-v3.2 original | cost-matched | same | ~0.9 (or subsample) |\n| gemini-3.1-pro-preview original | FRONTIER, 300 rows | api_bar.frontier_judge | ~1.1 |\n| S4_E2B | stack | exp-6 fit_s4_oof | 0 |\n\n---------------------------------------------------------------------------------------------------\n## 6. Claims, the testing hierarchy, and the verdict rules (fixed in the prereg)\n\n6.1 E2-B-alone claims. All are two-sided 95% sentence-cluster bootstrap CIs.\n- (B1) L25_E2B: Δ(V0 − flash-lite disguised) CI > 0. MDE80 0.103, power at +0.069 of 0.47. A null here is EXPECTED under the E effect size and must be reported as \"underpowered alone\".\n- (B2) Nested [S4_E2B + V0] − S4_E2B, CI > 0.\n- (B3) Cost-matched: Δ(V0 − deepseek disguised). Reported with its CI. No directional prediction is pre-declared. This is the \"does a stronger cheap judge close the gap\" test, and it could go against us.\n- (B4) Frontier: ratio V0/frontier and nested gain, descriptive with CIs.\n\n6.2 UNION claims (the reason this artifact exists), in FIXED-SEQUENCE order. Each is tested at α = 0.05 only if the previous one was confirmed; otherwise it is reported as descriptive.\n1. (U1) Union LONG POOL (L25_E2A ∪ L25_E2B ∪ EXC_E2A): strat Δ(V0 − flash-lite disguised) CI > 0, with point > 0 vs flash-lite original and nano. This is the hypothesis's CONFIRM (a), with more power. Strata = {L25_E2A, L25_E2B, EXC} × word bin, bootstrap over sentence_id within each stratum.\n2. (U2) Union L25 (the user's priority stratum): the same Δ, CI > 0. MDE80 ≈ 0.075.\n3. (U3) Union nested [S4 + V0] − S4, CI > 0.\n4. (U4) The carried H-IMPROVE variant − V0 on the union long pool, CI > 0.\n\nFixed-sequence testing controls the family-wise error without splitting α, and the order is the hypothesis's own priority order.\n\nReplication check: heterogeneity Δ_E2A − Δ_E2B (independent samples, so SE = sqrt(SE_A² + SE_B²)), plus Cochran's Q and I² over the two L25 samples.\n- It is REPORTED whichever way it comes out.\n- If the heterogeneity CI excludes 0, the union is still reported, but the paper must say \"effect differs between samples\". The first candidate explanation is the word-bin composition (F1). Test it by recomputing Δ within the 25-29 bin only, in both samples.\n\n6.3 Meta-analysis cross-check. Fixed-effect inverse-variance pooling of the per-sample strat Δs (L25_E2A, L25_E2B, and EXC as a third component for the long pool). Report it next to the pooled-bootstrap union. The pooled bootstrap is the pre-declared primary; the meta-analysis is a consistency check. A disagreement larger than 0.02 is reported.\n\n6.4 Verdict wording, pre-declared:\n- U1 CI > 0 → \"confirmed on untouched long sentences\".\n- U1 point > 0 with a CI including 0 → \"direction replicated, not significant at MDE ≈0.07\".\n- U1 point ≤ 0 → DISCONFIRM (hypothesis §4): \"E result was development-set optimism\".\n\nH-MECH items are scored individually. The cost-matched and frontier rows are reported, never gating.\n\n---------------------------------------------------------------------------------------------------\n## 7. Budget control (hard cap $9.5, reserve 10% → plan to $8.55)\n\n`src_e2b/budget.py`:\n- `spent()` sums `cost_ledger_master.jsonl`, into which every paid call writes (E2's `e.py` ledger is tailed and mirrored, and the judge wrappers append directly);\n- `can_start(estimate)` returns remaining − 0.95 ≥ estimate.\n\nSet `AII_HARD_CAP` for E2's scripts to the phase allowance each time they are launched.\n\n| Phase | Estimate | Rule |\n|---|---|---|\n| drift fallback (only if M2 absent) | 0.30 | — |\n| 400 L25 × $0.01182 | 4.73 | per batch of 50: $0.59; re-estimate after batch 1 from actuals |\n| cheap judges ×3 | 0.55 | — |\n| deepseek disguised | ~0.9 | pilot first |\n| frontier 300 | ~1.1 | pilot first |\n| deepseek original | ~0.9 | only if it fits |\n| GG scoring | ≤0.4 | only if the gate PASSED; FIRST to drop |\n| **total** | **≈8.5-8.9** | — |\n\nShrink order: GG → frontier → deepseek original → L25 sentences (floor 250, always a batch-order prefix).\n\nOn HTTP 402/403, do all CPU work first, then poll every 15 minutes until T+4:30. After that, the result is reported as PARTIAL, with the completed fraction per bin. Batches are never partially labelled: a batch that started is finished, or its sentences are excluded entirely.\n\n---------------------------------------------------------------------------------------------------\n## 8. Failure modes and fallbacks\n\n| Failure | Response |\n|---|---|\n| Pool-reproduction assert fails | Stop. Debug the environment (package versions from uv.lock, data_local sha). Never proceed on a different pool |\n| A generator id is no longer served | Prereg slot rule; flag it. If > 2 slots are substituted, report V0 on the unsubstituted-peer subset too |\n| E2-B L25 NOT TESTABLE (< 50 CORRECT) | Expected CORRECT ≈ 0.20 × 7.9 rows × 148 ≈ 234, so unlikely. If it happens, report counts and contribute to the union only |\n| M1 absent | See Step 3.1. V0 and PT are unaffected |\n| M3 absent | Standalone E2-B plus the runnable `union.py` |\n| Budget stop mid-run | Completed batches form a random prefix, NOT completion-selected. State the fraction |\n| Frontier parse failures > 10% | Report coverage. AUROC on the parsed rows with IPW; failures listed |\n\n---------------------------------------------------------------------------------------------------\n## 9. Outputs (every file cited in `tables.md` by path; every table row carries its source line)\n\n- `e2b/`: `sentences_E2B.json`, `census_E2B.json`, `seal.json`, `testability_E2B.json`, `E2B_SURPLUS_CLAIM.json`, `E2B_FINAL_READY.json`\n- `scores/`: `scores_E2B.jsonl`, `score_seal.json`, `file_access_log.txt`, `judges_costmatched.jsonl`, `judge_frontier.jsonl`, `frontier_subsample.json`\n- `analysis/`: `per_item_E2B.jsonl`, `confirm_verdict_E2B.json`, `union_longpool.json` (or NOT_COMPUTED), `union.py`, `tables.md`\n- `method_out.json` (exp_gen_sol_out; validate it with aii-json and generate the mini/preview variants). Each example = one candidate row. Keys:\n  - input = JSON{text, candidate_fol, system};\n  - output = the final label;\n  - `predict_V0`, `predict_flashlite_disg`, `predict_costmatched_disg`, and so on;\n  - `metadata_*` for stratum, tier and sample.\n- `prereg_iter5_E2B.json` + sha256, `deviations.json` (D-E2B, D-E2B-comp, D-E2B-drift?, D-E2B-M1?, and every slot substitution), `cost_ledger_master.jsonl`\n- `README.md` with the layout, how to run, and a \"Restoring removed files\" section. `.aii/manifest.yaml`:\n  - `e2bsrc/.venv/`: delete, regenerable (`cd e2bsrc && uv sync`);\n  - `e2bsrc/data_local/`: delete, redownloadable (copied from gen_art_dataset_4/data_local);\n  - raw/, work/ and sealed/: KEEP (paid, irreproducible).\n- Run aii-file-size-limit on any file > 100 MB, since generations are small.\n\n---------------------------------------------------------------------------------------------------\n## 10. domain_practice (what the field does for this kind of study; what I read)\n\nRead for this step:\n- the neurosymbolic handbook (S13: FOLIO/MALLS gold 36-39% wrong; S6: compile ≠ faithful; open question 3: no agreed gold-free faithfulness metric);\n- E2's `prereg_E2.json`, `census_E2.json`, `select_e2.py`, `pilot_projection.json` and `run_all.sh`;\n- eval-3 `power_E2.json`;\n- exp-6 `analyse_T1.py` / `api_bar.py` and the vendored `judges.py`;\n- the WMT24 metrics-task results and Thompson et al. 2024 (soft pairwise accuracy; PERM-INPUTS significance and greedy significance clusters), via search.\n\nItems marked (SK) are standing knowledge, not re-fetched this step.\n\nBASELINES. Reference-free metric papers are judged against the incumbent a practitioner would actually use.\n- In summarisation factuality (TRUE, Honovich et al. 2022; SummaC, Laban et al. 2022) the incumbents are NLI/QA metrics and, since 2023, LLM judges (G-Eval) (SK).\n- In MT (WMT23-24) every submission is compared with the strongest LLM-judge metric of the year (GEMBA/xCOMET class) and with the baseline metric set (Freitag et al. 2024).\n- The first comparator a reviewer names is a STRONGER judge at MATCHED COST, not the cheapest judge. The second is a frontier judge. That is exactly why this direction adds deepseek-v3.2 and gemini-3.1-pro.\n- Fair tuning: the SAME prompt/rubric for every judge, no per-judge prompt engineering on test data, and temperature 0 (SK).\n\nDATA. Fresh, untouched test data scored ONCE with frozen parameters is the WMT norm: a new test set every year, and metrics are submitted before the test outputs are released. FOLIO/MALLS original gold is noisy (S13), so labels come from an audited process (solver + blind disguised panel), not raw gold. ProverQA is the contamination-resistant alternative (handbook decision guide).\n\nCONTROLS.\n- Identical code for labels and metrics across samples.\n- Seal scores before labels.\n- LLM-judge self-preference: judges favour their own family's outputs (Panickssery et al. 2024; Zheng et al. 2023 MT-Bench) (SK). So own-family rows must be controlled.\n- Contamination via memorised gold: disguised vs original views.\n- Composition confounds between samples (here, word length).\n\nHOW MUCH IS ENOUGH.\n- Item-level meta-evaluation CIs must respect the clustering of outputs within an input. Deutsch et al. 2021 (TACL) showed that bootstrapping over inputs and systems gives much wider CIs than naive ones (SK), and WMT uses permutation tests over inputs (PERM-INPUTS).\n- AUROC differences of about 0.05 need hundreds of positives and negatives. The field-standard move when underpowered is MORE graded items, stated with an a-priori MDE. Here that is the eval-3 MDE: +0.069 needs about 882 planned L25 sentences.\n- Replication across two independent samples is judged with a heterogeneity statistic (Cochran's Q / I²), not by counting significant results (SK; meta-analysis norm).\n\nMEASURES.\n- Item level: ROC AUC is the standard for binary faithfulness (TRUE), with AUPRC for imbalance, and threshold-free.\n- System level: pairwise accuracy / Kendall τ (WMT), with significance clusters.\n- Ties must be handled explicitly (Deutsch et al. 2023, \"Ties Matter\") (SK). c_score_align is quantised, and AUROC counts ties as 0.5.\n- Cost is reported per item, in $, with a fixed unit.\n\n---------------------------------------------------------------------------------------------------\n## 11. practice_alignment (point by point)\n\nMEETS:\n- Fresh, untouched data, scored once with frozen code and a score seal before the label join. This is WMT's fresh-test-set norm, and it is stronger than WMT's because of the hash seals and the file-access log.\n- Paired, item-level, threshold-free AUROC with a sentence-cluster bootstrap. This matches the Deutsch/WMT concern about input clustering.\n- The a-priori MDE is stated for every cell. The response to underpowering is more graded sentences (this artifact's purpose), not more metrics.\n- A cost-matched stronger judge and a frontier judge, with the SAME rubric byte-identical. This closes the \"you beat a weak judge\" objection within budget.\n- Contamination: disguised and original views for the cheap and cost-matched judges.\n- Self-preference: own-family exclusion per judge (added in §5.11 because it was missing from the direction).\n- Nesting over the best baseline stack (S4) with cross-fitting.\n- Replication is judged by a heterogeneity test, not by \"both significant\". Multiplicity is handled by fixed-sequence testing (added in §6.2).\n- Completion selection is prevented by the hash-ordered batches of 50, each completed end to end.\n\nDEPARTS:\n1. The frontier judge runs on the ORIGINAL view only, on 300 rows (about 200 usable), so its AUROC CI will be wide (about ±0.07).\n   - Justification: budget ($1.1), and T1's precedent, which makes it comparable with iteration 3's frontier numbers.\n   - Cost: the V0/frontier ratio stays close to descriptive, as in T1 (0.957 [0.887, 1.034]). The paper cannot claim \"matches frontier\" from it. There is also no disguised frontier view, so frontier contamination is not measured.\n2. Labels come from a 3-family LLM panel plus the solver, not human annotators.\n   - Justification: this is E/E2's frozen protocol, and the only one that gives an L25 CORRECT class (F4). Its accuracy is measured (gate items, track H), and a drift gate precedes it.\n   - Cost: panel strictness (it accepts 0.61 of expert-corrected formulas on E) biases towards ERROR. The R_A sensitivity and the DRIFTED branch are reported. A human-annotated subset would be the field's preference, and none is affordable here.\n3. E2-B is drawn from the same MALLS-train source as E and E2-A. It is untouched but NOT a different distribution. It is also mostly 25-29 words (F1), so it is not identically distributed to E2-A's L25.\n   - Justification: the ≥30 supply is exhausted, and the rule is frozen. Domain transfer is DT's job (in E2-A).\n   - Cost: the union L25 over-represents 25-29 words relative to E's L25. Word-bin strata and a within-bin heterogeneity check are pre-declared.\n4. The cost-matched judge (deepseek) is also a GENERATOR family (G4), and the frontier (Gemini) shares a family with G8 and with flash-lite.\n   - Cost: possible self-preference. It is handled by the §5.11 exclusion, not avoided.\n5. The union's pooled bootstrap treats E2-A and E2-B as strata. The meta-analytic fixed-effect cross-check assumes a common effect.\n   - If heterogeneity is significant, the fixed-effect pool is not the right summary. A random-effects estimate with 2 studies is not identifiable in any useful way, so the per-sample results are then the primary reading. Pre-declared.\n6. System-level τ-b uses about 10 systems, far fewer than WMT's.\n   - It is descriptive only, and the paper must not rank metrics on it.\n7. No DeLong test is used; the cluster bootstrap is used instead, because DeLong assumes independent items.\n   - Cost: none. This is the field's recommended treatment for clustered outputs.\n8. Ties: the quantised c_score (|P| ≤ 9) has many ties. AUROC counts ties as 0.5, consistently for every metric.\n   - Report the tie rate per metric so that a reader can see where quantisation limits the attainable AUROC.\n\nResidual credibility risk a reviewer would raise first: the label regime (the panel) is shared by E2-A and E2-B. The union therefore adds SAMPLING power, not LABEL-regime independence. Instrument-disjoint confirmation is R_COMP FREE's role (the sibling artifact). This must be stated in the union's verdict text.\n", "structuredPatch": [], "originalFile": null, "userModified": false}
````

### [56] TOOL CALL — Edit · 2026-09-24 11:04:43 UTC

```
File: /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_plan/gen_plan_experiment_2/plan.md
OLD: union long pool ≈0.07 (L25 ≈277 + E2-A EXC ≈64 usable, SE from the long se_fit).
NEW: union long pool ≈0.057 (L25 ≈277 + E2-A EXC ≈64 = ≈341 usable; long se_fit a = −0.890, b = −0.5145 → SE ≈0.0205). E2-A's long pool alone (≈194 usable) has MDE ≈0.076.
```

### [57] TOOL RESULT — Edit · 2026-09-24 11:04:43 UTC

```
{"filePath": "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_plan/gen_plan_experiment_2/plan.md", "oldString": "union long pool ≈0.07 (L25 ≈277 + E2-A EXC ≈64 usable, SE from the long se_fit).", "newString": "union long pool ≈0.057 (L25 ≈277 + E2-A EXC ≈64 = ≈341 usable; long se_fit a = −0.890, b = −0.5145 → SE ≈0.0205). E2-A's long pool alone (≈194 usable) has MDE ≈0.076.", "originalFile": null, "structuredPatch": [{"oldStart": 149, "oldLines": 7, "newStart": 149, "newLines": 7, "lines": [" - cost-matched deepseek-v3.2, disguised (primary cost-matched) and original;", " - frontier gemini-3.1-pro-preview, original.", " ", "-(e) The confirmatory hierarchy of §6 with its α, and MDEs stated in advance: E2-B L25 0.103; union L25 ≈0.075; union long pool ≈0.07 (L25 ≈277 + E2-A EXC ≈64 usable, SE from the long se_fit).", "+(e) The confirmatory hierarchy of §6 with its α, and MDEs stated in advance: E2-B L25 0.103; union L25 ≈0.075; union long pool ≈0.057 (L25 ≈277 + E2-A EXC ≈64 = ≈341 usable; long se_fit a = −0.890, b = −0.5145 → SE ≈0.0205). E2-A's long pool alone (≈194 usable) has MDE ≈0.076.", " ", " (f) The union and meta-analysis rule (§6.3), the tie-breaking and duplicate rule (§4 Step 2.5), and the frontier subsample recipe.", " "]}], "userModified": false, "replaceAll": false}
```

### [58] TOOL CALL — Edit · 2026-09-24 11:04:43 UTC

```
File: /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_plan/gen_plan_experiment_2/plan.md
OLD: - U1 point > 0 with a CI including 0 → "direction replicated, not significant at MDE ≈0.07".
NEW: - U1 point > 0 with a CI including 0 → "direction replicated, not significant at MDE ≈0.057".
```

### [59] TOOL RESULT — Edit · 2026-09-24 11:04:43 UTC

```
{"filePath": "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_plan/gen_plan_experiment_2/plan.md", "oldString": "- U1 point > 0 with a CI including 0 → \"direction replicated, not significant at MDE ≈0.07\".", "newString": "- U1 point > 0 with a CI including 0 → \"direction replicated, not significant at MDE ≈0.057\".", "originalFile": null, "structuredPatch": [{"oldStart": 411, "oldLines": 7, "newStart": 411, "newLines": 7, "lines": [" ", " 6.4 Verdict wording, pre-declared:", " - U1 CI > 0 → \"confirmed on untouched long sentences\".", "-- U1 point > 0 with a CI including 0 → \"direction replicated, not significant at MDE ≈0.07\".", "+- U1 point > 0 with a CI including 0 → \"direction replicated, not significant at MDE ≈0.057\".", " - U1 point ≤ 0 → DISCONFIRM (hypothesis §4): \"E result was development-set optimism\".", " ", " H-MECH items are scored individually. The cost-matched and frontier rows are reported, never gating."]}], "userModified": false, "replaceAll": false}
```

### [60] TOOL CALL — Write · 2026-09-24 11:04:43 UTC

```
File: /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_plan/gen_plan_experiment_2/README.md

# gen_plan_experiment_2 — plan for E2-B (iteration 5, direction experiment_iter5_dir2)

This is a planning step, so it contains no code and no data. It writes the executable plan for E2-B.

E2-B is a second, untouched sample of about 400 L25 sentences (≥25 words, ≥3 conditions). It is drawn from MALLS-train by E2's frozen sha1 rule, and it is labelled and scored with E2's byte-identical code. It adds power to the L25 and long-pool confirmation of frozen `c_score_align`, and it adds a cost-matched judge (deepseek-v3.2) and a frontier judge (gemini-3.1-pro-preview, 300 rows).

## Layout
- `plan.md` — the full plan, covering:
  - setup, selection, prereg, drift, batches, seals, analyses, union and meta-analysis;
  - budget, fallbacks and outputs;
  - `domain_practice` and `practice_alignment` (§10-11).
- `README.md` — this file.
- `.aii/manifest.yaml` — no heavy files in this step (empty entries).

## Key numbers used by the plan

The power numbers come from `iter_4/gen_art/gen_art_evaluation_3/power_E2.json` se_fit:

| Cell | MDE80 | Power at +0.069 |
|---|---|---|
| E2-B L25 alone (≈148 usable) | 0.103 | 0.47 |
| Union L25 (≈277 usable) | ≈0.075 | ≈0.73 |
| Union long pool (≈341 usable) | ≈0.057 | — |

Cost is $0.01182 per L25 sentence (`gen_art_dataset_4/pilot_projection.json`). The projected total is about $8.5-8.9 against a hard cap of $9.5.

## Restoring removed files
Nothing is marked `delete`, so nothing needs restoring.
```

### [61] TOOL RESULT — Write · 2026-09-24 11:04:43 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_plan/gen_plan_experiment_2/README.md", "content": "# gen_plan_experiment_2 — plan for E2-B (iteration 5, direction experiment_iter5_dir2)\n\nThis is a planning step, so it contains no code and no data. It writes the executable plan for E2-B.\n\nE2-B is a second, untouched sample of about 400 L25 sentences (≥25 words, ≥3 conditions). It is drawn from MALLS-train by E2's frozen sha1 rule, and it is labelled and scored with E2's byte-identical code. It adds power to the L25 and long-pool confirmation of frozen `c_score_align`, and it adds a cost-matched judge (deepseek-v3.2) and a frontier judge (gemini-3.1-pro-preview, 300 rows).\n\n## Layout\n- `plan.md` — the full plan, covering:\n  - setup, selection, prereg, drift, batches, seals, analyses, union and meta-analysis;\n  - budget, fallbacks and outputs;\n  - `domain_practice` and `practice_alignment` (§10-11).\n- `README.md` — this file.\n- `.aii/manifest.yaml` — no heavy files in this step (empty entries).\n\n## Key numbers used by the plan\n\nThe power numbers come from `iter_4/gen_art/gen_art_evaluation_3/power_E2.json` se_fit:\n\n| Cell | MDE80 | Power at +0.069 |\n|---|---|---|\n| E2-B L25 alone (≈148 usable) | 0.103 | 0.47 |\n| Union L25 (≈277 usable) | ≈0.075 | ≈0.73 |\n| Union long pool (≈341 usable) | ≈0.057 | — |\n\nCost is $0.01182 per L25 sentence (`gen_art_dataset_4/pilot_projection.json`). The projected total is about $8.5-8.9 against a hard cap of $9.5.\n\n## Restoring removed files\nNothing is marked `delete`, so nothing needs restoring.\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [62] TOOL CALL — Write · 2026-09-24 11:04:43 UTC

```
File: /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_plan/gen_plan_experiment_2/.aii/manifest.yaml

entries: []
```

### [63] TOOL RESULT — Write · 2026-09-24 11:04:43 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_plan/gen_plan_experiment_2/.aii/manifest.yaml", "content": "entries: []\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [64] ASSISTANT · 2026-09-24 11:05:00 UTC

```
I've written the plan for the E2-B experiment (the second fresh sample of long sentences) to `plan.md`, with `README.md` and an empty `.aii/manifest.yaml`. Nothing was run: this step only reads files and writes the plan. The power figures are my own calculations from the saved power model and have not been checked independently.

**What the plan does**
- **Draws the sentences by E2's frozen rule.** A new wrapper first re-runs E2's selection and stops unless it reproduces E2's pool file exactly (hash `98cdccff…`). It then takes the 98 spare sentences E2 held in reserve, followed by the next sentences in the same order. It also carries the one-12-word-overlap filter forward correctly: that filter depends on what E2 had already picked, so it must be seeded with all of E2's rows.
- **Generates and labels in 8 batches of 50.** Each batch is finished completely before the next starts. If the budget stops the run, what's left is a random subset, not the "whatever finished" subset that sank exp 9.
- **Adds the two judges a reviewer asks for first:**
  - a cost-matched judge, deepseek-v3.2 with reasoning off, using the flash-lite prompt byte for byte;
  - the frontier judge, gemini-3.1-pro-preview, on 300 rows drawn before any label is seen.
- **Checks the judges for favouring their own model family.** Each judge is re-scored without rows generated by its own family. The direction didn't ask for this.
- **Seals the scores before joining labels.** The scoring code can't open label files, and every file it opens is logged.
- **Tests in a fixed order:** combined long pool, then combined L25, then the nested gain over the baseline stack, then the carried variant. Each step counts only if the one before it passed.
- **Treats replication honestly.** It reports whether E2-A and E2-B disagree (the difference between their effects, plus Q and I²), whichever way that comes out.

**Power**

| Cell | Usable sentences | Smallest detectable effect | Power at +0.069 |
|---|---|---|---|
| E2-B L25 alone | ≈148 | 0.103 | 0.47 |
| Combined L25 (E2-A + E2-B) | ≈277 | ≈0.075 | ≈0.73 |
| Combined long pool | ≈341 | ≈0.057 | — |

A null result from E2-B alone is therefore expected, and the plan says so in advance.

**Things you should know**
- **E2-B's sentences are shorter than E2-A's.** The ≥30-word supply runs out after the reserve, so E2-B is about 93% 25–29-word sentences, against 45% long in E2-A. The plan handles this with word-length strata and a within-bin check, and names it as the first explanation if the two samples disagree.
- **E2-B and E2-A could label the same 98 sentences.** The hypothesis lets E2-A use that reserve if budget allows. E2-B writes a claim file listing them, and a sentence labelled by both counts once in the combined analysis. Any overlap doubles as a free test–retest check on the labels.
- **The review panel is required.** Without it, E2's labelling rule produced 0 CORRECT rows in the 30-sentence pilot. So if the drift check fails, E2-B still runs the panel and marks every result secondary.
- **Budget:** about $8.5–8.9 projected against the $9.5 cap. The cut order if money runs short is: rename-invariance scoring (the gloss-gated variant), then the frontier judge, then the second deepseek view, then sentences (never below 250).
- **The shared labelling panel is the main remaining weakness.** E2-A and E2-B are labelled by the same panel, so combining them adds sample size, not an independent check of the labels. That independent check is the R_COMP FREE artifact's job.

The field-practice sections (§10–11) draw on the neurosymbolic handbook, the E2 and power files, and two web sources on how the MT metrics task tests significance. The other citations there come from memory and are marked as such.

Sources:
- [Are LLMs Breaking MT Metrics? Results of the WMT24 Metrics Shared Task](https://aclanthology.org/2024.wmt-1.2/)
- [Improving Statistical Significance in Human Evaluation of Automatic Metrics via Soft Pairwise Accuracy](https://arxiv.org/pdf/2409.09598)

Files are in `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_plan/gen_plan_experiment_2/`:
- `plan.md`
- `README.md`
- `.aii/manifest.yaml`
```

### [65] SYSTEM-USER prompt · 2026-09-24 11:05:03 UTC

````
<validation-feedback>
Attempt 1 failed validation.

The output file `./.terminal_claude_agent_struct_out.json` does not exist yet.



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

Produce `./.terminal_claude_agent_struct_out.json` again so it contains corrected JSON that matches the schema. Do not invent new fields.
</validation-feedback>
````

### [66] TOOL CALL — Write · 2026-09-24 11:06:33 UTC

```
File: /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_plan/gen_plan_experiment_2/.terminal_claude_agent_struct_out.json

{
  "title": "Second fresh sample of long sentences",
  "summary": "E2-B draws about 400 untouched MALLS-train L25 sentences (>=25 words, >=3 conditions) by E2's frozen sha1 rule: first the 98-sentence pre-ranked surplus, then the continuation of the same order. The >=30-word bin is exhausted, so E2-B is about 93% 25-29 words. It generates candidates with the 10 frozen slots and labels them with E2's byte-identical solver + panel code, in hash-ordered batches of 50 that are each completed end to end, so a budget stop never completion-selects. It scores the frozen V0 c_score_align (PRIMARY), PT and the M1-frozen variants, and seals the scores before the label join. Comparators: flash-lite disguised/original and nano; a COST-MATCHED stronger judge (deepseek-v3.2, reasoning off, byte-identical rubric A); and the FRONTIER judge (gemini-3.1-pro-preview) on a 300-row pre-label stratified subsample. Analyses: E2-B alone (L25 MDE80 0.103), then the UNION with E2-A in fixed-sequence order: long pool (MDE ~0.057), then L25 (MDE ~0.075, power ~0.73 at +0.069), then nested over S4, then the carried variant. Also an A-vs-B heterogeneity check (Q, I^2), an inverse-variance meta-analysis cross-check, judge own-family exclusion, H-MECH (i)-(iv), rename FA + paired flips, and cost per candidate. Hard cap $9.5; projected ~$8.5-8.9. The full plan is in plan.md in this workspace.",
  "builds_on": "REUSED, with where the executor picks each item up:\n\n(1) art_2OmxzMInZZJY (E2, /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4):\n- the whole frozen pipeline: src/, labeller/, src_e2/ (select_e2.py, e.py, generate.py, gen_retry.py, run_label.py, panel_run.py, repair.py, assemble_e2.py, controls_e2.py, testability_e2.py, seal_e2.py, verify_seal.py, drift_report.py, gate.py);\n- prereg_E2.json: seed 'E2_v1|', 12-gram rules, generator slots G1-G9, panel P1/P3/R1 with prompt sha, tier rules, testability rule, slot-unavailability rule, labeller sha256s;\n- code_freeze.json, census_E2.json (L25 supply 960 at 25-29 + 186 at >=30);\n- work/pool_E2.json (sha256 98cdccff...; the 98 surplus = L25 positions 351-448);\n- pilot_projection.json ($0.01182 per L25 sentence);\n- data_local/, E_ref/, prompts/fewshot_v1.txt, pyproject/uv.lock.\nCopy the CODE only into <WS>/e2bsrc; do not copy E2's raw/, labels, panel cache, sealed/ or ledgers.\n\n(2) art_U4Hsqt4Ay9Tg (dataset E, iter_1/gen_art/gen_art_dataset_1): the exclusion set (E's 700 sentences, calibration, few-shot) and the fold recipe sha1('E_folds_v1|'+sid)%5, reused as 'E2_folds_v1|'. It also supplies E-fitted frozen objects (V4 coefficients, via the freeze marker).\n\n(3) art_zcwCQgTqk6DN (dataset 3, iter_2/gen_art/gen_art_dataset_3): perturb.control_rename (RENAME_SYN / RENAME_NONCE), called through E2's controls_e2.py.\n\n(4) Exp 5 code (iter_2/gen_art/gen_art_experiment_5/src): pool_scoring.py (V0, byte-identical, sha asserted) and peer_text.py (PT fusion).\n\n(5) Exp 6 code (iter_3/gen_art/gen_art_experiment_6/src):\n- analyse_T1.py: stratified AUROC, sentence-cluster bootstrap, s4_nesting / fit_s4_oof with the >=95%-coverage substitution rule, IPW for the frontier subsample;\n- api_bar.py: frontier_judge (gemini-3.1-pro-preview, effort low, max_tokens 4000);\n- the vendored judges.py (vendor_d; also in iter_4/gen_art/gen_art_experiment_9/vendor/e8src/vendor_d/judges.py): RUBRIC_A, USER_JSON_A, judge_json for flash-lite, judge_logprob for nano. PROMPT_SHA is asserted.\n\n(6) Eval 3 (iter_4/gen_art/gen_art_evaluation_3/power_E2.json): the se_fit models that give every MDE stated in the prereg. Eval-3 pair-class code and eval-2 SCATTER/NET code are copied for H-MECH; exp 9 src/analyse.py supplies the e/d definitions.\n\n(7) Sibling markers (iter_5, polled read-only):\n- M1 CONSENSUS_FREEZE_READY.json (V1-V5, selection.json, gg.py, gg_gate.json);\n- M2 E2_DRIFT_DECISION.json (PASS/FAIL, pinned providers);\n- M3 E2A_FINAL_READY.json (E2-A per-row file for the union).\n\n(8) Negative findings carried as constraints:\n- the exp-9 completion-selection failure motivates the hash-ordered batches;\n- CSC is closed and not scored;\n- the budget-stop lesson motivates the ledger checks before every sweep.",
  "runpod_compute_profile": "cpu_plus",
  "implementation_pseudocode": "STEP 0 SETUP (T+0:00-0:30, $0 except a 1-token probe)\n- Read skills aii-python, aii-openrouter-llms, aii-parallel-computing, aii-long-running-tasks, aii-json. Probe OpenRouter with a 1-token call via OPENROUTER_BASE_URL / OPENROUTER_API_KEY and log it.\n- copy gen_art_dataset_4 -> <WS>/e2bsrc EXCLUDING .venv, raw/*, work/labels_heldout*, work/panel_cache.jsonl, work/sentences*.json, sealed/, seal.json, cost ledgers, *_data_out.json. KEEP src, labeller, src_e2, src_d3, prompts, data_local, E_ref, tests, code_freeze.json, prereg_E2.json, census_E2.json, work/pool_E2.json, work/models_snapshot_E2.json, work/fewshot_exemplars.json, work/calibration_items.json, pyproject, uv.lock.\n- cd e2bsrc; uv sync.\n- assert sha256 of every file in prereg_E2.labeller_sha256 and code_freeze.json; write code_freeze_check_E2B.json. Any mismatch -> STOP.\n\nselect_e2b.py (new wrapper; imports select_e2 functions; E2 files untouched):\n  pool = rerun E2 selection exactly; assert sha256(work/pool_E2.json) == 98cdccff...\n  used = ids of all E2 rows (EXC 100, L25 448, DT 110)\n  accepted_grams = union of 12-grams of all E2 rows\n  e2b = the 98 surplus in e2_rank order\n  continue take(long_) then take(short) in sha1('E2_v1|'+sid) order, skipping used, until len(e2b) == 400\n  reserve = the next 150 in the same order\n  assert 0 text or 12-gram collisions with E's 700 and with E2's rows\n  write e2b/sentences_E2B.json and census_E2B.json (per-bin supply remaining, drops)\n\nbatches = sort e2b by sha1('E2B_batch_v1|'+sid); cut into 8 x 50\n\nprereg_iter5_E2B.json + sha256, written BEFORE generation:\n- deviations D-E2B (power) and D-E2B-comp (word-bin composition);\n- selection algorithm + expected hashes;\n- metric list V0 (PRIMARY) / PT / V1-V5 / GG, verbatim from the contract;\n- comparators and the cost-matched judge spec (RUBRIC_A byte-identical, reasoning off, T=0, max_tokens 150);\n- confirmatory fixed-sequence hierarchy U1..U4, E2-B-alone B1..B4, and MDEs;\n- union / meta-analysis / duplicate rules; frontier subsample recipe;\n- shrink order GG > frontier > deepseek original > L25 sentences (floor 250, batch prefix);\n- deadlines M2 T+1:30, M1-variants T+2:30, M1-GG T+4:00, last paid call T+4:30, M3 T+5:30.\n\nwrite e2b/E2B_SURPLUS_CLAIM.json {token 'aii_iter5_e2b_surplus_v1', 98 ids}\n\nSTEP 1 DRIFT (runs in parallel; gates only the panel)\n  poll glob('.../iter_5/gen_art/*/e2/E2_DRIFT_DECISION.json') every 5 min; check the token; log every attempt\n  if found: use its decision and pin the providers (provider.order, allow_fallbacks=false)\n  elif T > T+1:30:\n    run gate.py --mode synthetic and --mode trackh (P1, P3, R1) + drift_report.py (~$0.3)\n    apply E2's stop rule (agreement < 0.85 -> FAIL) AND the hypothesis rule (track-H flag rate within the CI of E's 0.84)\n    log deviation D-E2B-drift\n  label_regime = PASS or DRIFTED; on FAIL, the panel still runs and every E2-B result is SECONDARY\n\nSTEP 2 GENERATION + LABELS, per batch b = 1..8\n  if not budget.can_start(est_batch): stop and report the completed fraction\n  e.py generate.py --slots G1,G1b,G2..G9 --variants fewshot_v1 --sentences batch_b --cap <remaining>; gen_retry.py\n  run_label.py --kind heldout\n  wait for M2; then:\n    panel_run.py --members P3,R1\n    panel_run.py --adjudicate P1\n    repair.py\n    run_label.py --refs reference_overrides\n  append to e2b/progress.jsonl: parse rate, $/sentence actual vs 0.01182, per-bin counts\n    (NO labels read except the CORRECT/ERROR counts needed for testability)\n\n  in parallel, label-free, from batch 1 onward:\n    flash-lite disg, flash-lite orig and nano orig on every parseable row (unparseable -> 1.0)\n    deepseek-v3.2 judge:\n      pilot 30 rows (parse rate, $/call); if parse failure > 10%: one retry at max_tokens 300\n      disguised view on all rows\n      original view on all rows if $/call <= 1.6e-4, else frontier subsample + batch prefix\n    local features for S4 (L2-bow, local round trip, local Qwen3-8B judge if the hardware allows, else substituted)\n\nafter the last batch:\n  assemble_e2.py; controls_e2.py (<=300 CORRECT rows, RENAME_SYN / NONCE, z3-verified); testability_e2.py\n  seal_e2.py; verify_seal.py; copy the results to e2b/\n\nfrontier subsample (drawn after generation, before labels):\n  cells = words tercile x family; 300 rows proportional, min 3 per cell\n  order within cell by sha1('E2B_frontier_v1|'+row_key); store inclusion probabilities\n  pilot 10 rows; if > $6e-3 per item, cut to the largest affordable prefix and recompute probabilities\n  api_bar.frontier_judge (original view)\n\nSTEP 3 SCORING + SCORE SEAL\n  V0 = exp-5 pool_scoring.py, leave-own-family-out (assert file sha); PT = exp-5 peer_text.py\n  poll the M1 freeze marker; verify its token + sha; copy the files to freeze_copy/\n  V1..V5 from freeze_copy:\n    w_f out-of-fold over E2-B's own sentences, fold = sha1('E2_folds_v1|'+sid)%5, 20 pseudo-sentences shrinkage\n    V4 coefficients from selection.json (never refit)\n  if no M1 by T+2:30: fallback_variants.py implements V1, V2 from the contract text as reported-only rows; V4, V5 not scored; deviation D-E2B-M1\n  if gg_gate PASS by T+4:00 and the 20-sentence pilot estimate <= $0.4: score c_gg on L25 rows + rename controls\n  score the rename controls (V0, PT, GG) with the same code\n  every read passes through an open() guard that refuses sealed/ and any path containing 'label' or 'reference'; paths are logged to scores/file_access_log.txt\n  write scores_E2B.jsonl and score_seal.json (sha256 of scores + every scoring source file + frontier subsample + marker hashes)\n\nSTEP 4 JOIN, only if verify_seal and verify_score_seal both pass -> analysis/per_item_E2B.jsonl\n\nSTEP 5 ANALYSES (exp-6 code copied, sha recorded)\n  populations: R_AB (LLM systems, tiers A+B, no CONTESTED / reading_choice) primary; R_A; CONTESTED -> CORRECT / -> ERROR\n  B1: L25_E2B strat AUROC delta V0 - flashlite_disg; strata = word bin; sentence-cluster bootstrap B=2000\n      also vs flashlite_orig, nano, deepseek disg/orig; AUROC, AUPRC, counts\n  B2: nested [S4_E2B + V0] - S4_E2B, cross-fitted by E2-B sentence folds\n  B3: V0 - deepseek (no directional prediction)\n  B4: frontier IPW AUROC, ratio V0/frontier CI, nested [frontier + V0] - frontier\n  H-MECH (i)-(iv) on L25_E2B CORRECT rows (eval-3 / eval-2 / exp-9 code); each item CONFIRMED or REFUTED\n  H-IMPROVE: carried variant - V0\n  rename: FA at c > 0.5 + paired flip (Wilson CI) + base FA\n  complexity curves (E2-B quartile bins)\n  coverage with unparseables in the denominator\n  $ and seconds per candidate, FULL and MARGINAL\n  system tau-b (descriptive)\n  judge own-family exclusion: flash-lite / frontier drop G8, nano drops G7, deepseek drops G4\n  tie rate per metric\n  write confirm_verdict_E2B.json\n  write e2b/E2B_FINAL_READY.json {token 'aii_iter5_e2b_final_v1', path, sha256, label_regime, completed fraction per bin}\n\nSTEP 6 UNION\n  poll glob('.../iter_5/gen_art/*/e2/E2A_FINAL_READY.json') until T+5:30\n  if present:\n    verify its sha; harmonise columns; duplicated sentence_ids -> keep the E2-B copy (report test-retest kappa)\n    strata = {L25_E2A, L25_E2B, EXC_E2A} x word bin; V2/V3/V5 weights recomputed out-of-fold over the union (label-free)\n    fixed sequence at alpha 0.05:\n      U1 long pool V0 - flashlite_disg CI > 0 (+ point > 0 vs orig / nano)\n      -> U2 union L25\n      -> U3 nested\n      -> U4 carried variant\n    heterogeneity Delta_A - Delta_B (SE = sqrt(SE_A^2 + SE_B^2)), Q, I^2; within-25-29-bin recheck\n    fixed-effect inverse-variance meta-analysis as a cross-check; report if it differs from the pooled estimate by > 0.02\n    if the two regimes differ (PASS vs DRIFTED): union SECONDARY\n  else: write analysis/union.py (runnable with --e2a <path>); union = NOT_COMPUTED_E2A_MISSING\n\nOUTPUT\n- tables.md with source lines\n- method_out.json (exp_gen_sol_out; one example per candidate row; predict_* per metric/judge; metadata_* for stratum, tier, sample); validate with aii-json; mini/preview variants\n- deviations.json, cost_ledger_master.jsonl, README.md, .aii/manifest.yaml (delete e2bsrc/.venv regenerable via uv sync; keep raw/, work/, sealed/)",
  "fallback_plan": "- Pool reproduction fails (sha mismatch): stop. Fix the environment from uv.lock and verify data_local shas. Never select from a different pool.\n\n- M2 (drift) absent at T+1:30: run E2's gate yourself (~$0.3) with the same pinning procedure and E2's stop rule. Deviation D-E2B-drift. The union later uses E2-A's decision if it appears.\n\n- Drift FAIL: the panel still runs under the pinned protocol. Labels are marked DRIFTED and every E2-B/union result is SECONDARY. R_A (tier A only) is reported alongside. A no-panel regime has no L25 CORRECT class (E2 pilot: 0 CORRECT), so skipping the panel would make E2-B untestable.\n\n- M1 (freeze) absent at T+2:30: V0 and PT are unaffected (exp-5 code). V1/V2 are implemented from the verbatim contract text as reported-only rows; V4/V5 are not scored. H-IMPROVE = 'no carried variant available'. GG is not scored unless gg_gate = PASS arrives by T+4:00.\n\n- Budget: before each sweep, estimate its cost from actuals. Stop if the estimate exceeds the remaining budget minus the 10% reserve ($0.95). Shrink order:\n  1. GG scoring;\n  2. frontier (or a smaller affordable prefix with recomputed inclusion probabilities);\n  3. deepseek original view (keep disguised);\n  4. L25 sentences (floor 250, always a batch-order prefix).\n  A started batch is always finished; otherwise its sentences are excluded entirely.\n\n- HTTP 402/403: finish all CPU work, then poll every 15 min until T+4:30, then report PARTIAL with the completed fraction per word bin (a random prefix, not completion-selected).\n\n- More than 2 generator slots are substituted (prereg rule: same family, nearest instruct model): also report V0 on the unsubstituted-peer subset.\n\n- deepseek parse failure > 10% after one max_tokens=300 retry: report NOT_TESTABLE_PARSE, with parse-rate and cost rows.\n\n- Frontier parse failure > 10%: IPW AUROC on the parsed rows, failures listed, coverage reported.\n\n- E2-B L25 NOT TESTABLE (< 50 CORRECT or < 25 sentences per class): report counts. E2-B contributes to the union only.\n\n- M3 (E2-A) absent at T+5:30: standalone E2-B results plus analysis/union.py runnable later; union = NOT_COMPUTED_E2A_MISSING.\n\n- A local judge cannot run (no GPU): drop it from S4 and record it in 'substituted', following exp-6's rule.",
  "testing_plan": "1. Code-freeze test ($0): assert every labeller/code sha256 from prereg_E2.json and code_freeze.json on the copied tree. Run E2's tests/test_fol.py (pytest) in e2bsrc.\n\n2. Selection test ($0):\n- re-running E2's selection must reproduce work/pool_E2.json sha256 98cdccff...;\n- E2-B must contain the 98 surplus ids first;\n- zero text or 12-gram collisions with E's 700 and all E2 rows;\n- re-running select_e2b.py twice must give identical output hashes;\n- the per-bin supply matches the census (>=30 bin exhausted after the surplus).\n\n3. Probe: a 1-token OpenRouter call; check that every slot and panel model id is served (models snapshot).\n\n4. Mini run on batch 1 only (50 sentences, ~$0.6):\n- generation parse rate per slot is comparable to E2's pilot (20 unparseable of 300);\n- solver labels run;\n- panel calls hit the fresh cache;\n- actual $/sentence is within +-30% of 0.01182, else re-project before batch 2.\n\n5. Judge pilots:\n- flash-lite / nano on 30 rows reproduce the parse behaviour of exp 5 (PROMPT_SHA asserted);\n- deepseek 30-row pilot: parse rate >= 90% and $/call measured;\n- frontier 10-row pilot: $/item measured.\n\n6. Scoring sanity ($0):\n- V0 from the copied exp-5 pool_scoring.py reproduces the stored exp-5 c_score_align on 50 random dataset-E rows exactly;\n- placebo: V0 with shuffled sentence peers gives AUROC ~0.5 after the join (a post-join check, reported);\n- the file-access log shows no sealed/ or label path opened before the join.\n\n7. Seal checks: verify_seal.py passes; verify_score_seal recomputes every hash; the join refuses to run if either fails.\n\n8. Analysis code check: run the copied exp-6 bootstrap on dataset E's T1 per_item file and reproduce T1's L25 delta +0.069 before applying it to E2-B.\n\n9. Union check: when E2-A's file exists, the union code run on E2-A alone must reproduce E2-A's own long-pool delta. Duplicate-id handling is unit-tested on a synthetic pair.\n\n10. Output validation: method_out.json passes aii-json against exp_gen_sol_out; mini/preview variants generated; file sizes checked (aii-file-size-limit).",
  "domain_practice": "What I read:\n- the neurosymbolic handbook: S13, FOLIO/MALLS gold 36-39% wrong; S6, compilation is not faithfulness; open question 3, no agreed gold-free faithfulness metric;\n- E2's prereg_E2.json, census_E2.json, select_e2.py, pilot_projection.json and run_all.sh;\n- eval-3 power_E2.json;\n- exp-6 analyse_T1.py and api_bar.py, and the vendored judges.py;\n- the WMT24 metrics-task results (Freitag et al. 2024) and Thompson et al. 2024 on soft pairwise accuracy and PERM-INPUTS significance clusters, via search.\nItems marked (SK) are standing knowledge, not re-fetched.\n\nBASELINES. Reference-free metric work is judged against the incumbent a practitioner uses.\n- Summarisation factuality (TRUE, Honovich et al. 2022; SummaC, Laban et al. 2022): NLI/QA metrics and, since 2023, LLM judges such as G-Eval (SK).\n- WMT23-24: every metric is compared with the strongest LLM-judge metric of the year and the baseline set.\n- The comparator a reviewer names first is a STRONGER judge at MATCHED COST; the second is a frontier judge.\n- Fair tuning means the same rubric byte-identical for every judge, temperature 0, and no per-judge prompt engineering on test data (SK).\n\nDATA. WMT's norm is a fresh test set every year, scored once with frozen submissions. FOLIO/MALLS original gold is noisy (S13), so labels must come from an audited process, not raw gold. ProverQA is the contamination-resistant alternative (handbook decision guide).\n\nCONTROLS:\n- identical label and metric code across samples;\n- scores sealed before labels;\n- LLM-judge self-preference: judges favour their own family's outputs (Panickssery et al. 2024; Zheng et al. 2023) (SK), so own-family rows are controlled;\n- contamination via memorised gold, controlled by disguised vs original views;\n- composition confounds between samples.\n\nHOW MUCH IS ENOUGH:\n- Item-level meta-evaluation CIs must respect clustering of outputs within an input. Deutsch et al. 2021 (TACL) showed that bootstrapping over inputs and systems widens CIs substantially (SK), and WMT uses permutation over inputs.\n- AUROC differences of ~0.05 need hundreds of positives and negatives. When a cell is underpowered, the accepted fix is more graded items with an a-priori MDE, not more metrics. Here, +0.069 on L25 needs ~882 planned sentences at E's yield of 0.37 (power_E2.json).\n- Replication across independent samples is judged by heterogeneity (Cochran's Q, I^2), not by counting significant results (SK).\n\nMEASURES:\n- item-level ROC AUC (TRUE's standard), with AUPRC for imbalance; threshold-free;\n- system-level pairwise accuracy or Kendall tau with significance clusters (WMT);\n- explicit tie handling (Deutsch et al. 2023, 'Ties Matter') (SK), which matters because c_score is quantised;\n- cost per item in $ with a fixed unit.",
  "practice_alignment": "MEETS:\n- Fresh, untouched data, scored once with frozen code. Scores are sealed before the label join, and a file-access log is kept: stricter than WMT's norm.\n- Paired, item-level, threshold-free AUROC with a sentence-cluster bootstrap, which matches the Deutsch/WMT concern about clustering.\n- An a-priori MDE for every cell (E2-B L25 0.103; union L25 ~0.075; union long pool ~0.057). The response to underpowering is more graded sentences, which is this artifact's purpose.\n- A cost-matched stronger judge (deepseek-v3.2) and a frontier judge with a byte-identical rubric, which closes the 'weak judge' objection.\n- Disguised and original views for contamination.\n- Own-family exclusion per judge for self-preference. This was ADDED; the direction lacked it.\n- Nesting over the S4 baseline stack with cross-fitting.\n- Replication is judged by heterogeneity plus a meta-analysis cross-check.\n- Multiplicity is handled by pre-declared fixed-sequence testing (ADDED).\n- Hash-ordered, end-to-end batches prevent completion selection.\n\nDEPARTS:\n1. The frontier judge uses the original view only, on 300 rows (~200 usable), so its CI is wide (~+-0.07).\n   - Justification: budget ($1.1) and comparability with iteration 3's T1.\n   - Cost: the V0/frontier ratio stays descriptive, 'matches frontier' cannot be claimed, and frontier contamination is not measured.\n2. Labels come from a 3-family LLM panel plus the solver, not humans.\n   - Justification: this is E/E2's frozen protocol, and the only regime with an L25 CORRECT class. Its accuracy is measured (gate items, track H), and a drift gate precedes it.\n   - Cost: the panel is strict (it accepts 0.61 of expert-corrected formulas on E), so ERROR is over-called. R_A and CONTESTED sensitivities are reported. There is no human-annotated subset, which the field would prefer.\n3. E2-B comes from the same MALLS-train source as E and E2-A, so it is untouched but not a new distribution. It is also ~93% 25-29 words, because the >=30 bin is exhausted.\n   - Justification: the frozen rule and the actual supply. Domain transfer is DT's role in E2-A.\n   - Cost: the union over-weights 25-29 words. Word-bin strata and a within-bin heterogeneity recheck are pre-declared.\n4. The cost-matched judge (deepseek) is also a generator family (G4), and the Gemini judges share a family with G8.\n   - Cost: possible self-preference, handled by exclusion sensitivity rather than avoided.\n5. The fixed-effect meta-analysis assumes a common effect. With 2 samples a random-effects estimate is not usefully identifiable, so under significant heterogeneity the per-sample results become the primary reading. Pre-declared.\n6. System-level tau-b uses ~10 systems, far fewer than WMT's. It is descriptive only.\n7. The cluster bootstrap is used instead of DeLong, which assumes independent items. There is no credibility cost.\n8. Ties in the quantised c_score (|P| <= 9) count 0.5 in AUROC for every metric, and the tie rate is reported per metric.\n\nRESIDUAL RISK: E2-A and E2-B share the label instrument (the panel). The union adds SAMPLING power, not label-regime independence. Instrument-disjoint confirmation is R_COMP FREE's job, and the union verdict text must say so."
}
```

### [67] TOOL RESULT — Write · 2026-09-24 11:06:33 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_plan/gen_plan_experiment_2/.terminal_claude_agent_struct_out.json", "content": "{\n  \"title\": \"Second fresh sample of long sentences\",\n  \"summary\": \"E2-B draws about 400 untouched MALLS-train L25 sentences (>=25 words, >=3 conditions) by E2's frozen sha1 rule: first the 98-sentence pre-ranked surplus, then the continuation of the same order. The >=30-word bin is exhausted, so E2-B is about 93% 25-29 words. It generates candidates with the 10 frozen slots and labels them with E2's byte-identical solver + panel code, in hash-ordered batches of 50 that are each completed end to end, so a budget stop never completion-selects. It scores the frozen V0 c_score_align (PRIMARY), PT and the M1-frozen variants, and seals the scores before the label join. Comparators: flash-lite disguised/original and nano; a COST-MATCHED stronger judge (deepseek-v3.2, reasoning off, byte-identical rubric A); and the FRONTIER judge (gemini-3.1-pro-preview) on a 300-row pre-label stratified subsample. Analyses: E2-B alone (L25 MDE80 0.103), then the UNION with E2-A in fixed-sequence order: long pool (MDE ~0.057), then L25 (MDE ~0.075, power ~0.73 at +0.069), then nested over S4, then the carried variant. Also an A-vs-B heterogeneity check (Q, I^2), an inverse-variance meta-analysis cross-check, judge own-family exclusion, H-MECH (i)-(iv), rename FA + paired flips, and cost per candidate. Hard cap $9.5; projected ~$8.5-8.9. The full plan is in plan.md in this workspace.\",\n  \"builds_on\": \"REUSED, with where the executor picks each item up:\\n\\n(1) art_2OmxzMInZZJY (E2, /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4):\\n- the whole frozen pipeline: src/, labeller/, src_e2/ (select_e2.py, e.py, generate.py, gen_retry.py, run_label.py, panel_run.py, repair.py, assemble_e2.py, controls_e2.py, testability_e2.py, seal_e2.py, verify_seal.py, drift_report.py, gate.py);\\n- prereg_E2.json: seed 'E2_v1|', 12-gram rules, generator slots G1-G9, panel P1/P3/R1 with prompt sha, tier rules, testability rule, slot-unavailability rule, labeller sha256s;\\n- code_freeze.json, census_E2.json (L25 supply 960 at 25-29 + 186 at >=30);\\n- work/pool_E2.json (sha256 98cdccff...; the 98 surplus = L25 positions 351-448);\\n- pilot_projection.json ($0.01182 per L25 sentence);\\n- data_local/, E_ref/, prompts/fewshot_v1.txt, pyproject/uv.lock.\\nCopy the CODE only into <WS>/e2bsrc; do not copy E2's raw/, labels, panel cache, sealed/ or ledgers.\\n\\n(2) art_U4Hsqt4Ay9Tg (dataset E, iter_1/gen_art/gen_art_dataset_1): the exclusion set (E's 700 sentences, calibration, few-shot) and the fold recipe sha1('E_folds_v1|'+sid)%5, reused as 'E2_folds_v1|'. It also supplies E-fitted frozen objects (V4 coefficients, via the freeze marker).\\n\\n(3) art_zcwCQgTqk6DN (dataset 3, iter_2/gen_art/gen_art_dataset_3): perturb.control_rename (RENAME_SYN / RENAME_NONCE), called through E2's controls_e2.py.\\n\\n(4) Exp 5 code (iter_2/gen_art/gen_art_experiment_5/src): pool_scoring.py (V0, byte-identical, sha asserted) and peer_text.py (PT fusion).\\n\\n(5) Exp 6 code (iter_3/gen_art/gen_art_experiment_6/src):\\n- analyse_T1.py: stratified AUROC, sentence-cluster bootstrap, s4_nesting / fit_s4_oof with the >=95%-coverage substitution rule, IPW for the frontier subsample;\\n- api_bar.py: frontier_judge (gemini-3.1-pro-preview, effort low, max_tokens 4000);\\n- the vendored judges.py (vendor_d; also in iter_4/gen_art/gen_art_experiment_9/vendor/e8src/vendor_d/judges.py): RUBRIC_A, USER_JSON_A, judge_json for flash-lite, judge_logprob for nano. PROMPT_SHA is asserted.\\n\\n(6) Eval 3 (iter_4/gen_art/gen_art_evaluation_3/power_E2.json): the se_fit models that give every MDE stated in the prereg. Eval-3 pair-class code and eval-2 SCATTER/NET code are copied for H-MECH; exp 9 src/analyse.py supplies the e/d definitions.\\n\\n(7) Sibling markers (iter_5, polled read-only):\\n- M1 CONSENSUS_FREEZE_READY.json (V1-V5, selection.json, gg.py, gg_gate.json);\\n- M2 E2_DRIFT_DECISION.json (PASS/FAIL, pinned providers);\\n- M3 E2A_FINAL_READY.json (E2-A per-row file for the union).\\n\\n(8) Negative findings carried as constraints:\\n- the exp-9 completion-selection failure motivates the hash-ordered batches;\\n- CSC is closed and not scored;\\n- the budget-stop lesson motivates the ledger checks before every sweep.\",\n  \"runpod_compute_profile\": \"cpu_plus\",\n  \"implementation_pseudocode\": \"STEP 0 SETUP (T+0:00-0:30, $0 except a 1-token probe)\\n- Read skills aii-python, aii-openrouter-llms, aii-parallel-computing, aii-long-running-tasks, aii-json. Probe OpenRouter with a 1-token call via OPENROUTER_BASE_URL / OPENROUTER_API_KEY and log it.\\n- copy gen_art_dataset_4 -> <WS>/e2bsrc EXCLUDING .venv, raw/*, work/labels_heldout*, work/panel_cache.jsonl, work/sentences*.json, sealed/, seal.json, cost ledgers, *_data_out.json. KEEP src, labeller, src_e2, src_d3, prompts, data_local, E_ref, tests, code_freeze.json, prereg_E2.json, census_E2.json, work/pool_E2.json, work/models_snapshot_E2.json, work/fewshot_exemplars.json, work/calibration_items.json, pyproject, uv.lock.\\n- cd e2bsrc; uv sync.\\n- assert sha256 of every file in prereg_E2.labeller_sha256 and code_freeze.json; write code_freeze_check_E2B.json. Any mismatch -> STOP.\\n\\nselect_e2b.py (new wrapper; imports select_e2 functions; E2 files untouched):\\n  pool = rerun E2 selection exactly; assert sha256(work/pool_E2.json) == 98cdccff...\\n  used = ids of all E2 rows (EXC 100, L25 448, DT 110)\\n  accepted_grams = union of 12-grams of all E2 rows\\n  e2b = the 98 surplus in e2_rank order\\n  continue take(long_) then take(short) in sha1('E2_v1|'+sid) order, skipping used, until len(e2b) == 400\\n  reserve = the next 150 in the same order\\n  assert 0 text or 12-gram collisions with E's 700 and with E2's rows\\n  write e2b/sentences_E2B.json and census_E2B.json (per-bin supply remaining, drops)\\n\\nbatches = sort e2b by sha1('E2B_batch_v1|'+sid); cut into 8 x 50\\n\\nprereg_iter5_E2B.json + sha256, written BEFORE generation:\\n- deviations D-E2B (power) and D-E2B-comp (word-bin composition);\\n- selection algorithm + expected hashes;\\n- metric list V0 (PRIMARY) / PT / V1-V5 / GG, verbatim from the contract;\\n- comparators and the cost-matched judge spec (RUBRIC_A byte-identical, reasoning off, T=0, max_tokens 150);\\n- confirmatory fixed-sequence hierarchy U1..U4, E2-B-alone B1..B4, and MDEs;\\n- union / meta-analysis / duplicate rules; frontier subsample recipe;\\n- shrink order GG > frontier > deepseek original > L25 sentences (floor 250, batch prefix);\\n- deadlines M2 T+1:30, M1-variants T+2:30, M1-GG T+4:00, last paid call T+4:30, M3 T+5:30.\\n\\nwrite e2b/E2B_SURPLUS_CLAIM.json {token 'aii_iter5_e2b_surplus_v1', 98 ids}\\n\\nSTEP 1 DRIFT (runs in parallel; gates only the panel)\\n  poll glob('.../iter_5/gen_art/*/e2/E2_DRIFT_DECISION.json') every 5 min; check the token; log every attempt\\n  if found: use its decision and pin the providers (provider.order, allow_fallbacks=false)\\n  elif T > T+1:30:\\n    run gate.py --mode synthetic and --mode trackh (P1, P3, R1) + drift_report.py (~$0.3)\\n    apply E2's stop rule (agreement < 0.85 -> FAIL) AND the hypothesis rule (track-H flag rate within the CI of E's 0.84)\\n    log deviation D-E2B-drift\\n  label_regime = PASS or DRIFTED; on FAIL, the panel still runs and every E2-B result is SECONDARY\\n\\nSTEP 2 GENERATION + LABELS, per batch b = 1..8\\n  if not budget.can_start(est_batch): stop and report the completed fraction\\n  e.py generate.py --slots G1,G1b,G2..G9 --variants fewshot_v1 --sentences batch_b --cap <remaining>; gen_retry.py\\n  run_label.py --kind heldout\\n  wait for M2; then:\\n    panel_run.py --members P3,R1\\n    panel_run.py --adjudicate P1\\n    repair.py\\n    run_label.py --refs reference_overrides\\n  append to e2b/progress.jsonl: parse rate, $/sentence actual vs 0.01182, per-bin counts\\n    (NO labels read except the CORRECT/ERROR counts needed for testability)\\n\\n  in parallel, label-free, from batch 1 onward:\\n    flash-lite disg, flash-lite orig and nano orig on every parseable row (unparseable -> 1.0)\\n    deepseek-v3.2 judge:\\n      pilot 30 rows (parse rate, $/call); if parse failure > 10%: one retry at max_tokens 300\\n      disguised view on all rows\\n      original view on all rows if $/call <= 1.6e-4, else frontier subsample + batch prefix\\n    local features for S4 (L2-bow, local round trip, local Qwen3-8B judge if the hardware allows, else substituted)\\n\\nafter the last batch:\\n  assemble_e2.py; controls_e2.py (<=300 CORRECT rows, RENAME_SYN / NONCE, z3-verified); testability_e2.py\\n  seal_e2.py; verify_seal.py; copy the results to e2b/\\n\\nfrontier subsample (drawn after generation, before labels):\\n  cells = words tercile x family; 300 rows proportional, min 3 per cell\\n  order within cell by sha1('E2B_frontier_v1|'+row_key); store inclusion probabilities\\n  pilot 10 rows; if > $6e-3 per item, cut to the largest affordable prefix and recompute probabilities\\n  api_bar.frontier_judge (original view)\\n\\nSTEP 3 SCORING + SCORE SEAL\\n  V0 = exp-5 pool_scoring.py, leave-own-family-out (assert file sha); PT = exp-5 peer_text.py\\n  poll the M1 freeze marker; verify its token + sha; copy the files to freeze_copy/\\n  V1..V5 from freeze_copy:\\n    w_f out-of-fold over E2-B's own sentences, fold = sha1('E2_folds_v1|'+sid)%5, 20 pseudo-sentences shrinkage\\n    V4 coefficients from selection.json (never refit)\\n  if no M1 by T+2:30: fallback_variants.py implements V1, V2 from the contract text as reported-only rows; V4, V5 not scored; deviation D-E2B-M1\\n  if gg_gate PASS by T+4:00 and the 20-sentence pilot estimate <= $0.4: score c_gg on L25 rows + rename controls\\n  score the rename controls (V0, PT, GG) with the same code\\n  every read passes through an open() guard that refuses sealed/ and any path containing 'label' or 'reference'; paths are logged to scores/file_access_log.txt\\n  write scores_E2B.jsonl and score_seal.json (sha256 of scores + every scoring source file + frontier subsample + marker hashes)\\n\\nSTEP 4 JOIN, only if verify_seal and verify_score_seal both pass -> analysis/per_item_E2B.jsonl\\n\\nSTEP 5 ANALYSES (exp-6 code copied, sha recorded)\\n  populations: R_AB (LLM systems, tiers A+B, no CONTESTED / reading_choice) primary; R_A; CONTESTED -> CORRECT / -> ERROR\\n  B1: L25_E2B strat AUROC delta V0 - flashlite_disg; strata = word bin; sentence-cluster bootstrap B=2000\\n      also vs flashlite_orig, nano, deepseek disg/orig; AUROC, AUPRC, counts\\n  B2: nested [S4_E2B + V0] - S4_E2B, cross-fitted by E2-B sentence folds\\n  B3: V0 - deepseek (no directional prediction)\\n  B4: frontier IPW AUROC, ratio V0/frontier CI, nested [frontier + V0] - frontier\\n  H-MECH (i)-(iv) on L25_E2B CORRECT rows (eval-3 / eval-2 / exp-9 code); each item CONFIRMED or REFUTED\\n  H-IMPROVE: carried variant - V0\\n  rename: FA at c > 0.5 + paired flip (Wilson CI) + base FA\\n  complexity curves (E2-B quartile bins)\\n  coverage with unparseables in the denominator\\n  $ and seconds per candidate, FULL and MARGINAL\\n  system tau-b (descriptive)\\n  judge own-family exclusion: flash-lite / frontier drop G8, nano drops G7, deepseek drops G4\\n  tie rate per metric\\n  write confirm_verdict_E2B.json\\n  write e2b/E2B_FINAL_READY.json {token 'aii_iter5_e2b_final_v1', path, sha256, label_regime, completed fraction per bin}\\n\\nSTEP 6 UNION\\n  poll glob('.../iter_5/gen_art/*/e2/E2A_FINAL_READY.json') until T+5:30\\n  if present:\\n    verify its sha; harmonise columns; duplicated sentence_ids -> keep the E2-B copy (report test-retest kappa)\\n    strata = {L25_E2A, L25_E2B, EXC_E2A} x word bin; V2/V3/V5 weights recomputed out-of-fold over the union (label-free)\\n    fixed sequence at alpha 0.05:\\n      U1 long pool V0 - flashlite_disg CI > 0 (+ point > 0 vs orig / nano)\\n      -> U2 union L25\\n      -> U3 nested\\n      -> U4 carried variant\\n    heterogeneity Delta_A - Delta_B (SE = sqrt(SE_A^2 + SE_B^2)), Q, I^2; within-25-29-bin recheck\\n    fixed-effect inverse-variance meta-analysis as a cross-check; report if it differs from the pooled estimate by > 0.02\\n    if the two regimes differ (PASS vs DRIFTED): union SECONDARY\\n  else: write analysis/union.py (runnable with --e2a <path>); union = NOT_COMPUTED_E2A_MISSING\\n\\nOUTPUT\\n- tables.md with source lines\\n- method_out.json (exp_gen_sol_out; one example per candidate row; predict_* per metric/judge; metadata_* for stratum, tier, sample); validate with aii-json; mini/preview variants\\n- deviations.json, cost_ledger_master.jsonl, README.md, .aii/manifest.yaml (delete e2bsrc/.venv regenerable via uv sync; keep raw/, work/, sealed/)\",\n  \"fallback_plan\": \"- Pool reproduction fails (sha mismatch): stop. Fix the environment from uv.lock and verify data_local shas. Never select from a different pool.\\n\\n- M2 (drift) absent at T+1:30: run E2's gate yourself (~$0.3) with the same pinning procedure and E2's stop rule. Deviation D-E2B-drift. The union later uses E2-A's decision if it appears.\\n\\n- Drift FAIL: the panel still runs under the pinned protocol. Labels are marked DRIFTED and every E2-B/union result is SECONDARY. R_A (tier A only) is reported alongside. A no-panel regime has no L25 CORRECT class (E2 pilot: 0 CORRECT), so skipping the panel would make E2-B untestable.\\n\\n- M1 (freeze) absent at T+2:30: V0 and PT are unaffected (exp-5 code). V1/V2 are implemented from the verbatim contract text as reported-only rows; V4/V5 are not scored. H-IMPROVE = 'no carried variant available'. GG is not scored unless gg_gate = PASS arrives by T+4:00.\\n\\n- Budget: before each sweep, estimate its cost from actuals. Stop if the estimate exceeds the remaining budget minus the 10% reserve ($0.95). Shrink order:\\n  1. GG scoring;\\n  2. frontier (or a smaller affordable prefix with recomputed inclusion probabilities);\\n  3. deepseek original view (keep disguised);\\n  4. L25 sentences (floor 250, always a batch-order prefix).\\n  A started batch is always finished; otherwise its sentences are excluded entirely.\\n\\n- HTTP 402/403: finish all CPU work, then poll every 15 min until T+4:30, then report PARTIAL with the completed fraction per word bin (a random prefix, not completion-selected).\\n\\n- More than 2 generator slots are substituted (prereg rule: same family, nearest instruct model): also report V0 on the unsubstituted-peer subset.\\n\\n- deepseek parse failure > 10% after one max_tokens=300 retry: report NOT_TESTABLE_PARSE, with parse-rate and cost rows.\\n\\n- Frontier parse failure > 10%: IPW AUROC on the parsed rows, failures listed, coverage reported.\\n\\n- E2-B L25 NOT TESTABLE (< 50 CORRECT or < 25 sentences per class): report counts. E2-B contributes to the union only.\\n\\n- M3 (E2-A) absent at T+5:30: standalone E2-B results plus analysis/union.py runnable later; union = NOT_COMPUTED_E2A_MISSING.\\n\\n- A local judge cannot run (no GPU): drop it from S4 and record it in 'substituted', following exp-6's rule.\",\n  \"testing_plan\": \"1. Code-freeze test ($0): assert every labeller/code sha256 from prereg_E2.json and code_freeze.json on the copied tree. Run E2's tests/test_fol.py (pytest) in e2bsrc.\\n\\n2. Selection test ($0):\\n- re-running E2's selection must reproduce work/pool_E2.json sha256 98cdccff...;\\n- E2-B must contain the 98 surplus ids first;\\n- zero text or 12-gram collisions with E's 700 and all E2 rows;\\n- re-running select_e2b.py twice must give identical output hashes;\\n- the per-bin supply matches the census (>=30 bin exhausted after the surplus).\\n\\n3. Probe: a 1-token OpenRouter call; check that every slot and panel model id is served (models snapshot).\\n\\n4. Mini run on batch 1 only (50 sentences, ~$0.6):\\n- generation parse rate per slot is comparable to E2's pilot (20 unparseable of 300);\\n- solver labels run;\\n- panel calls hit the fresh cache;\\n- actual $/sentence is within +-30% of 0.01182, else re-project before batch 2.\\n\\n5. Judge pilots:\\n- flash-lite / nano on 30 rows reproduce the parse behaviour of exp 5 (PROMPT_SHA asserted);\\n- deepseek 30-row pilot: parse rate >= 90% and $/call measured;\\n- frontier 10-row pilot: $/item measured.\\n\\n6. Scoring sanity ($0):\\n- V0 from the copied exp-5 pool_scoring.py reproduces the stored exp-5 c_score_align on 50 random dataset-E rows exactly;\\n- placebo: V0 with shuffled sentence peers gives AUROC ~0.5 after the join (a post-join check, reported);\\n- the file-access log shows no sealed/ or label path opened before the join.\\n\\n7. Seal checks: verify_seal.py passes; verify_score_seal recomputes every hash; the join refuses to run if either fails.\\n\\n8. Analysis code check: run the copied exp-6 bootstrap on dataset E's T1 per_item file and reproduce T1's L25 delta +0.069 before applying it to E2-B.\\n\\n9. Union check: when E2-A's file exists, the union code run on E2-A alone must reproduce E2-A's own long-pool delta. Duplicate-id handling is unit-tested on a synthetic pair.\\n\\n10. Output validation: method_out.json passes aii-json against exp_gen_sol_out; mini/preview variants generated; file sizes checked (aii-file-size-limit).\",\n  \"domain_practice\": \"What I read:\\n- the neurosymbolic handbook: S13, FOLIO/MALLS gold 36-39% wrong; S6, compilation is not faithfulness; open question 3, no agreed gold-free faithfulness metric;\\n- E2's prereg_E2.json, census_E2.json, select_e2.py, pilot_projection.json and run_all.sh;\\n- eval-3 power_E2.json;\\n- exp-6 analyse_T1.py and api_bar.py, and the vendored judges.py;\\n- the WMT24 metrics-task results (Freitag et al. 2024) and Thompson et al. 2024 on soft pairwise accuracy and PERM-INPUTS significance clusters, via search.\\nItems marked (SK) are standing knowledge, not re-fetched.\\n\\nBASELINES. Reference-free metric work is judged against the incumbent a practitioner uses.\\n- Summarisation factuality (TRUE, Honovich et al. 2022; SummaC, Laban et al. 2022): NLI/QA metrics and, since 2023, LLM judges such as G-Eval (SK).\\n- WMT23-24: every metric is compared with the strongest LLM-judge metric of the year and the baseline set.\\n- The comparator a reviewer names first is a STRONGER judge at MATCHED COST; the second is a frontier judge.\\n- Fair tuning means the same rubric byte-identical for every judge, temperature 0, and no per-judge prompt engineering on test data (SK).\\n\\nDATA. WMT's norm is a fresh test set every year, scored once with frozen submissions. FOLIO/MALLS original gold is noisy (S13), so labels must come from an audited process, not raw gold. ProverQA is the contamination-resistant alternative (handbook decision guide).\\n\\nCONTROLS:\\n- identical label and metric code across samples;\\n- scores sealed before labels;\\n- LLM-judge self-preference: judges favour their own family's outputs (Panickssery et al. 2024; Zheng et al. 2023) (SK), so own-family rows are controlled;\\n- contamination via memorised gold, controlled by disguised vs original views;\\n- composition confounds between samples.\\n\\nHOW MUCH IS ENOUGH:\\n- Item-level meta-evaluation CIs must respect clustering of outputs within an input. Deutsch et al. 2021 (TACL) showed that bootstrapping over inputs and systems widens CIs substantially (SK), and WMT uses permutation over inputs.\\n- AUROC differences of ~0.05 need hundreds of positives and negatives. When a cell is underpowered, the accepted fix is more graded items with an a-priori MDE, not more metrics. Here, +0.069 on L25 needs ~882 planned sentences at E's yield of 0.37 (power_E2.json).\\n- Replication across independent samples is judged by heterogeneity (Cochran's Q, I^2), not by counting significant results (SK).\\n\\nMEASURES:\\n- item-level ROC AUC (TRUE's standard), with AUPRC for imbalance; threshold-free;\\n- system-level pairwise accuracy or Kendall tau with significance clusters (WMT);\\n- explicit tie handling (Deutsch et al. 2023, 'Ties Matter') (SK), which matters because c_score is quantised;\\n- cost per item in $ with a fixed unit.\",\n  \"practice_alignment\": \"MEETS:\\n- Fresh, untouched data, scored once with frozen code. Scores are sealed before the label join, and a file-access log is kept: stricter than WMT's norm.\\n- Paired, item-level, threshold-free AUROC with a sentence-cluster bootstrap, which matches the Deutsch/WMT concern about clustering.\\n- An a-priori MDE for every cell (E2-B L25 0.103; union L25 ~0.075; union long pool ~0.057). The response to underpowering is more graded sentences, which is this artifact's purpose.\\n- A cost-matched stronger judge (deepseek-v3.2) and a frontier judge with a byte-identical rubric, which closes the 'weak judge' objection.\\n- Disguised and original views for contamination.\\n- Own-family exclusion per judge for self-preference. This was ADDED; the direction lacked it.\\n- Nesting over the S4 baseline stack with cross-fitting.\\n- Replication is judged by heterogeneity plus a meta-analysis cross-check.\\n- Multiplicity is handled by pre-declared fixed-sequence testing (ADDED).\\n- Hash-ordered, end-to-end batches prevent completion selection.\\n\\nDEPARTS:\\n1. The frontier judge uses the original view only, on 300 rows (~200 usable), so its CI is wide (~+-0.07).\\n   - Justification: budget ($1.1) and comparability with iteration 3's T1.\\n   - Cost: the V0/frontier ratio stays descriptive, 'matches frontier' cannot be claimed, and frontier contamination is not measured.\\n2. Labels come from a 3-family LLM panel plus the solver, not humans.\\n   - Justification: this is E/E2's frozen protocol, and the only regime with an L25 CORRECT class. Its accuracy is measured (gate items, track H), and a drift gate precedes it.\\n   - Cost: the panel is strict (it accepts 0.61 of expert-corrected formulas on E), so ERROR is over-called. R_A and CONTESTED sensitivities are reported. There is no human-annotated subset, which the field would prefer.\\n3. E2-B comes from the same MALLS-train source as E and E2-A, so it is untouched but not a new distribution. It is also ~93% 25-29 words, because the >=30 bin is exhausted.\\n   - Justification: the frozen rule and the actual supply. Domain transfer is DT's role in E2-A.\\n   - Cost: the union over-weights 25-29 words. Word-bin strata and a within-bin heterogeneity recheck are pre-declared.\\n4. The cost-matched judge (deepseek) is also a generator family (G4), and the Gemini judges share a family with G8.\\n   - Cost: possible self-preference, handled by exclusion sensitivity rather than avoided.\\n5. The fixed-effect meta-analysis assumes a common effect. With 2 samples a random-effects estimate is not usefully identifiable, so under significant heterogeneity the per-sample results become the primary reading. Pre-declared.\\n6. System-level tau-b uses ~10 systems, far fewer than WMT's. It is descriptive only.\\n7. The cluster bootstrap is used instead of DeLong, which assumes independent items. There is no credibility cost.\\n8. Ties in the quantised c_score (|P| <= 9) count 0.5 in AUROC for every metric, and the tie rate is reported per metric.\\n\\nRESIDUAL RISK: E2-A and E2-B share the label instrument (the panel). The union adds SAMPLING power, not label-regime independence. Instrument-disjoint confirmation is R_COMP FREE's job, and the union verdict text must say so.\"\n}\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [68] ASSISTANT · 2026-09-24 11:06:41 UTC

```
I've written the plan to `.terminal_claude_agent_struct_out.json` with every field the schema requires, plus the optional ones. I couldn't run a JSON validator here, so the file hasn't been checked against the schema; I only avoided inner double quotes and backslashes when writing it.

- **Title:** "Second fresh sample of long sentences".
- **Content:** the same plan as `plan.md`, reorganised into the schema's fields (pseudocode, fallback plan, testing plan, field practice and how the plan lines up with it, and what it reuses from earlier rounds).
- **Compute:** I set the compute profile to `cpu_plus`. The work is solver calls, API calls and bootstrap statistics; a GPU would only matter for the optional local Qwen3-8B judge, and the plan drops that judge if no GPU is available.

`plan.md`, `README.md` and `.aii/manifest.yaml` are unchanged. All four files are in `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_plan/gen_plan_experiment_2/`.
```
