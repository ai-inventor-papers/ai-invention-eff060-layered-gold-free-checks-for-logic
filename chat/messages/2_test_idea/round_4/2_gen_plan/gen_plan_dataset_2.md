# gen_plan_dataset_2 — test_idea

> Phase: `invention_loop` · round 4 · `gen_plan`
> Run: `run_u75jRHUss0zo` — Gold-Free Faithfulness Metrics for NL-to-FOL Translation
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_plan_dataset_2` (terminal_claude_agent, claude-opus-5-5)

### [1] CONFIG · 2026-09-24 07:00:13 UTC

```
model: claude-opus-5-5 | effort: high | permission: bypassPermissions
```

### [2] SYSTEM-USER prompt · 2026-09-24 07:00:19 UTC

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
You are expanding an artifact direction of type: DATASET

DATASET
Collect, prepare, and merge datasets for experiments and analysis.
Runtime: Python 3.12, UV, isolated workspace.
Tools: Full shell/Python/filesystem access, the aii-web-tools skill (web search, page fetch, regex grep over full page/PDF text), and other skills.
Skills: aii-hf-datasets (HuggingFace Hub — ML datasets, many UCI/OpenML/Kaggle mirrors), aii-owid-datasets (Our World in Data — global statistics), aii-json (schema validation). Also any Python source (sklearn.datasets, openml, direct URLs, APIs) — must verify within 300MB limit.
Capabilities: Search, acquire, transform, combine, and standardize data from any available source.
Deps: REQUIRED none | OPTIONAL RESEARCH for guidance on what data to collect
</artifact_type_info>

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
- LLM API calls must go through OpenRouter only (no direct OpenAI, Anthropic, etc.), with base_url=os.environ["OPENROUTER_BASE_URL"] and api_key=os.environ["OPENROUTER_API_KEY"] (the OpenAI SDK's defaults, OPENAI_BASE_URL and OPENAI_API_KEY, point at the same place, so a plain OpenAI() client also works with OpenRouter model ids). The key is this run's own OpenRouter key and works only at that base URL: never hard-code OpenRouter's own URL, or every call fails with 401
- **SPEND BUDGET**: at most $10 USD of OpenRouter API calls for this artifact. Nothing outside your own code enforces this — the key you are given has no per-artifact cap — so it holds only if you track cumulative cost after every call and stop when you approach it. Budget the work up front: estimate the per-call cost and the number of calls BEFORE starting a sweep, not after it overruns. Exceeding it spends real money that the run cannot recover.
</software_constraints>
</available_resources>

<time_budget>

The dataset executor has 6h total (including writing code, debugging, testing, and fixing errors).

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
Your workspace: `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_plan/gen_plan_dataset_2`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_plan/gen_plan_dataset_2/`:
GOOD: `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_plan/gen_plan_dataset_2/file.py`, `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_plan/gen_plan_dataset_2/results/out.json`
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
title: Peer agreement in the candidate's own words
hypothesis: |-
  kind: hypothesis (iteration 4 of 5; move = DEEPEN on the lead that survived iteration 3, cross-family solver consensus. Its two open failures are attacked at their shared cause, and the first untouched confirmation set is built.)

  0. CORRECTED RECORD OF ITERATION 3. Every number here was executed. Where the iteration-3 report disagrees with a source file, this record replaces it, and each correction names its source. The paper step must transcribe these numbers rather than the report's wording.

  STATUS OF DATASET E. For every iteration-3 claim, E is DEVELOPMENT data, not held-out data. The scores were frozen in exp 5, so no thresholds were tuned on E. The choice of lead object was made on E, though: PT was narrowed to c_score_align after the iteration-2 results on E (tier A: 0.860 vs 0.818). HYB/NF selection also used screen+E. No data untouched by an earlier decision has yet confirmed any E-based claim.

  T1 (art_7GxreYjATkC5; results/tables_T1.md, verdict_T1.json, api_cost_ledger.json). R_AB E_POOL: n = 2,686 (1,822 ERROR / 864 CORRECT, 292 sentences).
  - Stratified AUROC: c_score_align 0.741, flash-lite disguised 0.642, so Δ +0.099 [0.049, 0.146].
    - Long pool: +0.116 [0.070, 0.163].
    - EXC: +0.197.
    - R_A L20+EXC: +0.299.
    - Against nano original: +0.089 [0.043, 0.134].
  - On L25, the user's priority stratum (≥25 words, ≥3 conditions), consensus does NOT significantly beat any judge:
    - c_score_align − flash-lite +0.069 [−0.020, 0.148];
    - against nano original +0.043;
    - against the local judge +0.049.
    Only p_peer_text is significant on L25 (+0.113).
  - On short or simple sentences the judge leads:
    - CTRL −0.069 [−0.23, 0.10];
    - <12 words −0.040;
    - n_conditions ≤1: judge 0.822 vs consensus 0.794.
  - Against the baseline stack:
    - c_score_align ALONE ≈ S4_full: +0.006 [−0.031, 0.042].
    - Only the NESTED addition is significant: [S4_full + c] − S4_full strat +0.039 [0.021, 0.057] (permutation p95 0.009).
    - S4_API 0.761; S4_full_noJudge 0.734; PT_refit − S4_full +0.043.
    - Against the local judge on ALL_TIERS: +0.019, n.s.
    - p_text on CTRL: −0.252.
  - Frontier frame (n = 284):
    - AUROC: frontier original 0.741, S4_full 0.745, c 0.710. c − frontier is −0.032 [−0.085, 0.024].
    - The ratio 0.957 [0.887, 1.034] meets the 0.95 bar on the point estimate only.
    - Nested [frontier + c] − frontier: +0.037 [0.008, 0.066].
    - Group recall for the frontier judge was computed on this frame of 284 rows only.
  - M3 has two specifications that disagree. They are reported together, and M3 is INCONCLUSIVE:
    - bootstrap Δslope over words: +0.146 [−0.051, 0.361];
    - stacked-GEE interaction: +0.274 [0.190, 0.359].
  - Contamination: flash-lite DiD +0.105 [0.006, 0.201]. This is MARGINAL EVIDENCE of contamination, since the CI excludes 0; MDE is a power statement and does not discount it.
  - Deviations:
    - D3: 108 R_AB rows received a fallback score of 0.5;
    - D5: matched-FA thresholds cannot be attained for quantised scores, so c_score_align's threshold is 1.0.
  - Spend $2.395.

  T2 / R_COMP (art_cxnoDYQNFolW).
  - SIG PASSES. Within-template AUROC: c_sig 0.954 vs flash-lite disguised 0.587, so +0.367 [0.328, 0.404]. Against the ORIGINAL-text judge: +0.278 [0.239, 0.319].
    - Disguise alone costs the cheap judge 0.085 [0.034, 0.132] on unmemorisable templates, so the +0.367 is measured against a handicapped bar.
  - FREE is NOT_TESTABLE: 420 ERROR / 34 CORRECT tier A, 1,811 UNRESOLVED, and the panel was never run.
    - FREE tier A: c_align 0.804 vs judge 0.581; c_align − judge +0.214 [−0.034, 0.377].
  - By the §3.1 rule, T2 is therefore NOT CONFIRMED.
  - SIG hands every translator a signature block, i.e. a controlled vocabulary, which the user excluded as an operating condition. So 0.954 is measured outside the user's regime.
  - Frontier subsample (n = 60): c_sig 0.956 vs frontier original 0.932 (disguised 0.735); [frontier + c_sig] − frontier +0.088 [0.019, 0.172].
  - SIG mechanism:
    - e = 0.000 and d = 0.260.
    - Weak-reading CORRECT rows have d = 0.14 (86% of CORRECT). Strong-reading CORRECT rows have d = 0.96, i.e. d under a shared vocabulary is almost entirely a READING CHOICE.
  - Rename: c_sig FA is 1.000 under nonce renames, so 'unaffected by predicate names' is false.
  - Deviations: D1 (the Sonnet lexicon and reference audits were not run); D2 (221 < 250 sentences, 75 dropped for fluency). Spend $1.58.

  Exp 8 (art_YYD-HDzfQfEj). The pre-registered RENAME-INVARIANT SELECTION FAILED: prereg_hyb.json → 'NEITHER ELIGIBLE'.
  - Rename FA on PERTURB at screen thresholds:
    - HYB 0.841 (RENAME_SYN) / 0.700 (RENAME_NONCE);
    - NF 0.686 / 0.485.
    The E-threshold FAs (c_nf 0.132, c_hyb 0.216) are not the pre-registered test.
  - Over-alignment: HYB's extra agreements are label-discordant 0.388 of the time, vs 0.127 for ALIGN agreements. HYB − ALIGN is −0.004 [−0.011, 0.004]; HYB − NF is +0.052.
  - PERTURB, per-operator consensus AUROC is an ARTEFACT (reviewer audit/perturb_c_align_constant.json):
    - 94-100% of mutants of EVERY operator score c = 1, and 26.8% of controls score c = 1, which predicts the all-operator 0.866 exactly.
    - So the operator rankings and 'polarity symmetry' are by construction.
    - Consensus covered only the 200 E bases: 3,419 of 5,402 rows. The 1,946 R_COMP-base rows have no_peers_yet.
  - MEANING_RENAME is an ERROR operator (a non-synonymous donor predicate).
    - c_align 0.872 and rt_nli_min_LOCAL 0.930 DETECT it correctly.
    - c_nf 0.499 is BLIND to it.
  - Judge cells, from perturb_sensitivity.csv (E_bases, ALL): DROP 0.589, ADD 0.695, SWAP 0.566, BIND 0.731, MEANING_RENAME 0.617.
  - The best PERTURB metrics are p_peer_text (within-base 0.948; 0.86-0.996 per operator) and L3/p_text (0.90-0.96 on NEG/REV/RESTR).
  - Error-type identification (T12):
    - peer-medoid typing 0.328 [0.277, 0.387] vs majority 0.177;
    - flash-lite judge 0.326; local judge 0.098;
    - ORACLE (true base) 0.802.
  - The local judges ran as nf4 (deviation). Spend $0.35.

  Eval 2 (art_FWy8D4_y9GBn). Pre-registered verdicts:
  - M1 (e falls with n_conditions): INCONCLUSIVE, slope −0.04 [−0.53, 0.45].
  - M2 (d rises with words): CONFIRMED but NON-SPECIFIC, because the shuffled-label placebo gives +1.75 [1.04, 2.45].
  - M3-local: INCONCLUSIVE.
  - M4: k95 = 3 overall, and 2/3/5 by words tercile. At k = 7 the tercile AUROCs are 0.777 / 0.721 / 0.726.
  - SCATTER CONFIRMED: SI_err 0.159 vs SI_cor 0.760 (ratio 4.45). SI_err falls with conditions.
  - NET Δ(e + d), words T3 − T1: +0.356 [0.198, 0.493]. BINARY CONSENSUS DEGRADES WITH LENGTH, DRIVEN BY d, not e (END_MAJ e = 0.124, d = 0.537).
  - Graded − binary: +0.114 [0.091, 0.140].
  - c_score_exact (no aligner) 0.748; VOCAB_EXACT pure-z3 labels 0.929.
  - eqmv is non-transitive in 15.8% of cases.
  - LOFO minimum Δ −0.011 (no single family carries the result).
  - Best cross-fitted 3-family pool: OOF 0.785.
  - Cost PER SENTENCE for k = 1/3/5/7: $0.000315 / 0.000946 / 0.001576 / 0.002206, i.e. about $0.002 per sentence for the best 3-pool.
    - Full consensus cost is $1.21e-4 per item, 2.5× flash-lite's $4.9e-5. Only the marginal z3 cost ($2.5e-7) is negligible.

  Prior art (art_VIF75I5R6f0v). NOT scooped: no work combines multi-family translations, solver equivalence and a faithfulness meta-evaluation on NL→FOL. But the METHOD is not new:
  - ARc 2511.09008 uses the same score form (the share of k LLM translations that entail the candidate), on a fixed schema with QA labels;
  - NoTB 2608.21962 applies cross-family equivalence to RTL;
  - GenV 2609.11085 reports single-model SC 0.863 on NL→FOL, and its metric-vs-judge ranking REVERSES when labels switch from Z3-reference to panel intent (this run's solver → panel shift echoes that: 0.849 → 0.779);
  - LLMs-as-Jury already recommends 3-4 cross-family models.
  C1, C3, C4 and C5 NEED QUALIFIERS. What this run can claim is the meta-evaluation (per-candidate, vs API judges, nested over the stack), the measured rename FA, and the e/d decomposition over length.

  Iteration-3 spend: ≈ $4.33.

  Verdict table:
  | Clause | Verdict |
  |-|-|
  | T1(a) | CONFIRMED on development E; L25 n.s. |
  | T1(b) | CONFIRMED (nested only) |
  | T1(c) | SIG PASS / FREE NOT_TESTABLE, so NOT CONFIRMED |
  | T1(d) | point estimate only |
  | T1(e) rename invariance | FAILED |
  | M1 | INCONCLUSIVE |
  | M2 | CONFIRMED, non-specific |
  | M3 | INCONCLUSIVE (specifications conflict) |
  | M4 | CONFIRMED |
  | NET | degrades |
  | Typing | at judge level (negative) |

  Frontier judge: it does NOT earn 30× its cost over S4_full + consensus.

  1. DIAGNOSIS: ONE CAUSE BEHIND ALL THREE OPEN FAILURES.
  The three failures are: the L25 null, degradation with length, and rename FA. Consensus's blind spot is NOT coincident error:
  - e is 0.000 on R_COMP and 0.124 on E;
  - errors scatter 4.45× more than correct translations.
  The blind spot is DIVERGENCE AMONG CORRECT TRANSLATIONS (d), and that divergence is mostly VOCABULARY/GRANULARITY:
  - d is 0.537 on E, where 0.77 of L25 CORRECT rows are not equivalent to the reference;
  - d falls to 0.14 for weak readings when translators share a vocabulary (SIG);
  - the same sentences lose 0.95 → 0.80 AUROC when vocabularies diverge (FREE).
  Post-hoc matching cannot fix this. Name-similarity alignment breaks under renames (FA 0.765). Name-free alignment cannot tell a synonym from a wrong predicate: MEANING_RENAME 0.499, and 0.388 of its extra agreements are label-discordant. This is ambiguous in principle once two formulas use unrelated names.

  2. CLAIM (same object, cross-family solver consensus, with the failure attacked at its cause).
  CANDIDATE-SIGNATURE CONSENSUS (CSC).
  - A candidate formula carries its own vocabulary: its predicate and constant symbols with arities. Give k cheap peer families the sentence plus ONLY that signature, in shuffled order, with no formula and no structure. Instruct them to use the listed symbols where they fit, to add new symbols if needed, and that they need not use all of them.
  - Score = the share of peers NOT exactly z3-equivalent to the candidate. There is no aligner anywhere. A graded version by claim-unit support is kept as a row.
  - CSC is the SIG regime obtained WITHOUT any external ontology or controlled vocabulary. The vocabulary comes from the system under test, so the metric stays gold-free, ontology-free and task-agnostic in the user's operating condition. It does NOT compare grounded with ungrounded generation of the candidate, so it is not the out-of-scope item.

  MECHANISM (why it should work, and where it should break).
  Sharing the candidate's symbols removes lexical/granularity divergence among correct peers (d → the reading-choice floor), while leaving errors free to scatter (e stays low). Consensus then stops degrading with length. It becomes rename-invariant BY CONSTRUCTION under synonym renames: a renamed candidate yields a renamed signature, which yields peers in the renamed symbols. And a WRONG predicate (MEANING_RENAME) or a wrong argument order is exposed rather than aligned away, because peers use a symbol only where its name fits the sentence.

  The opposing force is ANCHORING. The signature leaks the candidate's decomposition. An extra predicate (ADD) or a wrong name may pull peers into the same error and raise e. A missing symbol (DROP) should NOT anchor, because peers add the missing condition.

  Both outcomes are informative. If anchoring wins on ADD/MEANING_RENAME, the answer is a hybrid: CSC for d, free-peer ALIGN for anchored types. The decomposition is the finding either way.

  One-sentence finding if it holds: 'Cross-model agreement fails on long sentences not because models agree on errors (they almost never do) but because correct translations disagree about WORDS. Asking peers to translate in the candidate's own vocabulary removes that divergence, makes the check rename-invariant with no aligner, and restores its advantage over LLM judges on long conditioned sentences at about $0.001 per candidate.'

  3. DATA ROLES (fixed now; no re-screening on confirmation data).
  DEVELOPMENT, where selection is allowed and logged:
  - the screen;
  - ALL of E;
  - R_COMP SIG;
  - PERTURB (E bases and R_COMP bases).

  UNTOUCHED CONFIRMATION, built in iteration 4 and scored ONLY in iteration 5 with every metric frozen and hashed at the end of iteration 4:
  (i) E2. About 400 fresh MALLS-train sentences, disjoint from E and the screen: 250 L25, 100 EXC, 50 L20. It adds ≥100 sentences from a non-FOLIO/MALLS source with gold FOL for domain transfer (for example ProverQA-hard, LogicNLI or ProofWriter-derived rules, preferring ≥15 words and ≥2 conditions). Candidates come from the same 10 generator slots. Labels come from E's FROZEN solver + panel protocol (tiers A/B, CONTESTED and reading_choice excluded), plus a VEX subset. Testability (≥50/50 per cell) is declared before scoring.
  (ii) R_COMP FREE labels. The existing FREE candidates (2,024 rows, 1,811 unresolved) get an ALIGNMENT-FREE labeller:
    - It EXHAUSTIVELY searches arity-consistent injective maps (with merge/split bridges) from candidate symbols onto template atoms, against the weak and strong readings.
    - ERROR if NO map yields equivalence. This is certain whatever the names are.
    - CORRECT if a map exists AND an LLM gloss check confirms each mapped symbol's meaning. The gloss check is a lexical task, gated at balanced accuracy ≥0.90 on known SIG maps plus synonym/nonce/donor controls.
    - Otherwise UNRESOLVED.
    This replaces the panel route, which broke twice. That panel route is DROPPED.

  4. TESTS, in priority order. Each executor may spend ≤$10; API arms run right after the 00:00 UTC reset, and a cost estimate is made before each sweep.

  T6 CSC DEVELOPMENT (experiment, on development data only).
  - Peers from the cheapest adequate 3-4 families (from eval 2's best 3-pool: deepseek, microsoft, openai), temperature 0, few-shot.
  - CSC is scored on:
    - E R_AB (all 2,686 rows, or a stratified ≥1,500 if cost binds);
    - R_COMP FREE candidates (label-free statistics only: d proxies, class counts);
    - PERTURB E-base mutants and controls, with peers regenerated per mutant signature.
  - Arms:
    - CSC-exact;
    - CSC-graded;
    - CONTROL-OTHER-SIG: peers get the signature of ANOTHER candidate of the same sentence. This tests whether shared vocabulary per se causes the gain;
    - HYBRID: CSC OR free-peer ALIGN, whichever is less anchored per error type;
    - optional MULTI-READING peers: a peer may return both readings, and agreement with any reading endorsed by ≥2 families counts. This addresses the 96% FA on minority strong readings.
  - Report, each with its source file:
    - e and d, and their slopes over words and n_conditions, vs free-peer c_score_align on the SAME rows;
    - strat AUROC overall and on L25;
    - Δ vs flash-lite disguised AND original, and nested over S4_full, reusing exp 6 fold_E;
    - anchoring: e per operator (ADD, DROP, MEANING_RENAME, SWAP) under CSC vs free peers;
    - rename FA on RENAME_SYN (primary) and RENAME_NONCE (stress, reported separately);
    - recall and FA at a fixed threshold per operator. Within-base AUROC is NOT used for consensus, because of the base-endorsement artefact;
    - typing: minimal typed repair from the candidate to the CSC peer majority in the SAME vocabulary, vs the known operator on PERTURB and vs chance on E;
    - cost per CANDIDATE, FULL and MARGINAL.
  - Freeze the winning variant, k, families, prompt and threshold in prereg_csc.json, with a hash.

  T7 CONFIRMATION SET (dataset: E2 + R_COMP FREE alignment-free labels, as §3). Includes:
  - the gloss-check gate;
  - a panel-calibration replay on E's 96 expert pairs;
  - CNE and gold-wrong rates on E2.

  T8 RECORD AND MECHANISM TABLES (evaluation, $0).
  - Rerun pairwise_matrix / ed_decomposition on R_COMP SIG and FREE, label-free.
  - Build the consolidated tables the paper must carry:
    - hypothesis verdicts;
    - coverage vs request;
    - a cost table with units (per item / sentence / candidate; FULL vs MARGINAL);
    - the corrected PERTURB table;
    - the per-stratum Δ table including L25;
    - the function inventory (consensus_lib.py, peer_text.py, fol_triage.py, pairwise.py, mechanism.py);
    - label facts (CNE 0.773/0.721/0.441/0.215; the panel rejects 0.822 of MALLS gold and accepts 0.613 of expert-corrected formulas; the adjudicator-vs-expert ceiling is about 2/3).

  Iteration 5 (final): one confirmation experiment on E2 + R_COMP FREE with frozen c_score_align, frozen PT, frozen CSC, flash-lite disguised/original, nano, S4_full refit on E2 folds, and the frontier judge on a 300-row stratified E2 subsample. Then the paper.

  5. SUCCESS CRITERIA (pre-registered now).
  DEVELOPMENT GATES (T6, iteration 4; for selection, not claims):
  - G1: CSC d on E CORRECT ≤0.35 (free-peer END_MAJ 0.537), with a d-vs-words slope whose CI includes 0 or is below it;
  - G2: CSC strat AUROC ≥ c_score_align − 0.01 on R_AB, and > c_score_align on L25;
  - G3: RENAME_SYN FA ≤ base FA + 0.05;
  - G4: anchoring: CSC e on ADD, DROP and MEANING_RENAME ≤ free-peer e + 0.05;
  - G5: full cost ≤ $0.002 per candidate.
  If G1 or G3 fails, CSC is REFUTED as a fix, and that is reported. Iteration 5 then confirms frozen c_score_align/PT alone.

  CONFIRM, on E2 (untouched, iteration 5):
  - (a) frozen c_score_align (or PT) − flash-lite disguised: strat CI > 0 on E2 R_AB AND positive against flash-lite original;
  - (b) nested [S4_full + consensus] − S4_full: CI > 0;
  - (c) on E2 L25: CSC − flash-lite, CI > 0 (the stratum where iteration 3 was n.s.);
  - (d) on R_COMP FREE (alignment-free labels, if testable): CSC − judge (original and disguised), CI > 0; CSC ≥ c_score_align;
  - (e) CSC RENAME_SYN FA ≤ 0.10 above base FA on E2 controls;
  - (f) domain-transfer slice: positive sign.
  PARTIAL:
  - (a) and (b) hold but (c) and (d) do not: consensus confirmed, the long-sentence fix not confirmed.
  - (c) and (d) hold but (a) does not: CSC is the metric and plain consensus was development-set optimism.
  DISCONFIRM: (a) fails on E2. The E advantage was development-set optimism, and the judge or S4 stack is the incumbent.
  MECHANISM (scored CONFIRMED or REFUTED):
  - MD: d falls under CSC, and its length slope vanishes;
  - ME: e stays ≤0.15 under CSC (anchoring bounded);
  - ML: CSC's AUROC-by-words slope is ≥ the judge's, under BOTH M3 specifications;
  - MT: CSC typing on PERTURB ≥0.55 (peer-medoid 0.328; oracle 0.802) and above chance on E. If not, 'no gold-free metric here identifies error type better than a judge' stands as the negative answer to that ask.

  6. CARRIED AS SECONDARY ROWS, with no new development budget: PT fusion, TEXT (L2-bow + L3), NF/HYB, graded consensus, and the judges.
  CLOSED, one sentence each:
  - B2;
  - R_ADJ;
  - pilot structural metrics;
  - FOL-Triage L1/L2-role;
  - post-hoc NF/HYB alignment as a rename fix (pre-registered selection failed);
  - the panel route for R_COMP FREE (broke twice);
  - per-operator within-base AUROC for consensus (artefact).

  7. USER DELIVERABLES carried:
  - item-level AUROC/AUPRC and P/R/FA at frozen thresholds;
  - system-level τ-b;
  - per-type sensitivity (recall at fixed threshold);
  - one shared rewrite set;
  - coverage with unparseable rows in the denominator;
  - $ and seconds per candidate with units;
  - complexity curves;
  - contamination with MDE;
  - label-bias facts;
  - reusable functions: consensus_score(mode = align | nf | hyb | exact | csc), csc_peers(text, signature, families, k), graded_consensus, typed_repair_same_vocab, equivalent_modulo_vocab, exhaustive_map_label.
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
  Same consensus object; deepened by attacking its d/vocabulary failure at the cause, plus untouched confirmation
_confidence_delta: unchanged
_key_changes:
- >-
  The iteration-3 record is corrected from source files. E is relabelled as DEVELOPMENT data. L25 is n.s. (+0.069 [-0.020,
  0.148]). c alone ≈ S4_full (+0.006). Only the nested +0.039 is significant. The frontier ratio holds on the point estimate
  only. M3 is INCONCLUSIVE (bootstrap +0.146 n.s. vs stacked-GEE +0.274 CI>0). The flash-lite DiD +0.105 [0.006, 0.201] is
  marginal contamination evidence. Spend is ≈$4.33, and cost units are fixed (the k=3 pool costs ≈$0.001/sentence, not $0.000073).
- >-
  T2 is recorded as SIG PASS / FREE NOT_TESTABLE, so it is NOT confirmed. SIG is stated as a controlled-vocabulary regime
  the user excluded. Added: FREE 0.804 vs 0.581 on 34 CORRECT rows; +0.278 against the original judge; the 60-row frontier
  comparison (0.956 vs 0.932; nested +0.088); SIG d is almost all reading choice (weak 0.14, strong 0.96).
- >-
  The exp-8 record is corrected. The pre-registered rename-invariant selection FAILED (HYB 0.841/0.700, NF 0.686/0.485). MEANING_RENAME
  is an ERROR operator (c_nf is blind at 0.499). Per-operator consensus AUROC is a base-endorsement artefact. Judge cells
  are corrected. Consensus covered 3,419/5,402 rows. Typing is 0.328, equal to the judge's 0.326 (oracle 0.802). Spend $0.35.
- >-
  The eval-2 record uses the pre-registered M-definitions: M1 INCONCLUSIVE; M2 CONFIRMED but non-specific. NET +0.356 means
  binary consensus DEGRADES with length, driven by d rather than e. Added rows: SCATTER ratio 4.45, graded-binary +0.114,
  c_exact 0.748, VOCAB_EXACT 0.929, LOFO, k95 by tercile 2/3/5.
- >-
  The prior-art qualifiers are adopted: ARc shares the score form; NoTB and GenV (label-target reversal); LLMs-as-Jury for
  k=3-4. The claim is reframed as a meta-evaluation plus the e/d-by-length decomposition plus the measured rename FA.
- >-
  New diagnosis: all three open failures (the L25 null, length degradation, rename FA) share one cause, divergence among CORRECT
  translations over vocabulary and granularity, not coincident error. Post-hoc alignment cannot resolve it in principle.
- >-
  New deepen move on the same object: Candidate-Signature Consensus (CSC). Peers translate in the candidate's own symbols,
  the check is exact z3 with no aligner, and it is rename-invariant by construction. Pre-registered opposing force: anchoring
  (ADD/MEANING_RENAME). Control arm: another candidate's signature. The hybrid and multi-reading arms are secondary.
- >-
  Untouched confirmation for the first time. E2 (about 400 fresh MALLS-train L25/EXC/L20 sentences plus ≥100 non-FOLIO/MALLS
  sentences, labelled with E's frozen protocol) and alignment-free exhaustive-map + gloss-gated labels for R_COMP FREE are
  built in iteration 4 and scored only in iteration 5 with hashed frozen metrics.
- >-
  The panel route for R_COMP FREE broke twice and is dropped. Also closed: post-hoc NF/HYB rename fixes and within-base per-operator
  AUROC for consensus.
- >-
  Verdict recorded: the frontier judge does not earn 30× its cost over S4_full+consensus (frame: 0.741 vs 0.745 vs 0.710;
  nested +0.037). Error typing remains a negative answer unless CSC typing reaches ≥0.55 on PERTURB.
_strands:
- artifact: art_7GxreYjATkC5
  state: lead
  why: >-
    c_align−flash-lite strat +.099 [.049,.146], nested/S4_full +.039; but on dev E only (metric chosen on E), L25 +.069 n.s.,
    c alone≈S4_full, frontier ratio CI<.95
- artifact: art_cxnoDYQNFolW
  state: lead
  why: >-
    SIG .954 vs judge .587 (+.278 vs orig judge; ≥frontier on 60), e=0, but SIG is a controlled vocab regime; in-scope FREE
    untestable (34 CORRECT), c_align .804
- artifact: art_YYD-HDzfQfEj
  state: 'null'
  why: >-
    Prereg rename-invariant selection FAILED (HYB FA .841/.700, NF .686/.485); NF blind to MEANING_RENAME .499; typing .328
    = judge .326; per-op AUROC artefact
- artifact: art_FWy8D4_y9GBn
  state: lead
  why: >-
    SCATTER SI_err .159 vs SI_cor .760; graded>binary +.114; but NET +.356: consensus degrades with length via d=.537 not
    e=.124; M1 inconclusive, M2 non-specific
- artifact: art_VIF75I5R6f0v
  state: lead
  why: >-
    Positioning: no scoop of multi-family+solver+NL→FOL faithfulness meta-eval, but ARc shares c_score form; C1/C3-C5 need
    qualifiers; defines what is new
_evidence_state: lead
_move: deepen
_move_rationale: >-
  Consensus is a lead (dev-E win, L25 n.s., rename fix failed). Deepen: attack its d/vocabulary cause via candidate-signature
  peers and confirm on untouched E2 + R_COMP FREE.
_coverage: full
_coverage_statement: >-
  Iteration 4 answers the core ask on the user's priority stratum and operating condition: whether a cheap gold-free consensus
  metric, run in the candidate's own vocabulary with no ontology, predicts faithfulness on long conditioned sentences beyond
  judges and the baseline stack, with rename invariance, per-type recall, typing, coverage, cost, and untouched confirmation.
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

FIELD: meta-evaluation of reference-free (gold-free) quality metrics, applied to neuro-symbolic NL->FOL autoformalization. SOURCES READ FOR THIS STEP: the neurosymbolic handbook (aii-handbook-auto-neurosymbolic); the iteration-3 prior-art artifact art_VIF75I5R6f0v (ARc 2511.09008, NoTB 2608.21962, GenV 2609.11085, SCP-NL2TL 2608.05439, LLMs-as-Jury); the iteration-3 source files (exp 7 prereg_sig.json and the R_COMP candidate slots; exp 8 src and results listing; eval 2 src/pairwise.py and mechanism.py; the reviewer's audit/perturb_c_align_constant.json). I ran NO new web lookups in this bounded step. The MT-metrics and summarization-factuality norms below come from standing knowledge (WMT metrics shared tasks; Deutsch et al. TACL 2021 and EMNLP 2023 on metric CIs and tie calibration; TRUE and SummaC) and are provisional.
(1) PRINCIPLES. The field takes as given: - FOLIO/MALLS gold as shipped is about 36-42% wrong (2606.02837); - compiling or being provable is not faithfulness (2604.19459); - several FOL formulas are correct for one sentence, so how labels are built (vocabulary, granularity, reading choice) is part of the object of study; - gold-free round-trip certification is occupied (2604.25031) and can only be a baseline; - no agreed gold-free faithfulness metric exists (handbook open question 3). Still argued: whether solver-exact equivalence or panel intent is the right label target. GenV shows that metric-vs-judge rankings reverse between the two, and our own 0.849 -> 0.779 shift echoes it. So a result is read only if it states its label regime and holds under more than one.
(2) WHAT CONVINCES. In metric meta-evaluation, a win counts only when it is: - paired, item-level and threshold-free on REAL system outputs; - against the incumbent a practitioner would use (for NL->FOL in 2026, a cheap API judge); - scored ONCE with frozen parameters on data that no earlier decision touched (WMT re-runs metrics on each year's fresh test set for exactly this reason); - shown to add signal by nesting over the best existing combination. A mechanism is believed when a pre-registered decomposition, which could have come out the other way, predicts the fix before the fix is run.
(3) STANDARD MOVES and what each exists to rule out: - stratified within-stratum AUROC rules out stratum composition (our placebo is 0.59); - a sentence-clustered bootstrap rules out item dependence; - a matched-resource baseline (the same peer families and prompt without the intervention) rules out 'more or different peers'; - a sham control arm (another candidate's signature) rules out 'any shared vocabulary helps'; - nonce disguise with a DiD rules out memorised gold; - an instrument-disjoint label regime rules out circular validation (the aligner shared by labeller and metric was iteration 2's confound); - synthetic mutants used ONLY for per-type sensitivity at a fixed threshold rules out synthetic-for-real substitution (Goyal & Durrett 2021) and the base-endorsement artefact found in iteration 3; - tie-aware operating points for quantised scores (Deutsch et al. 2023) rule out artefacts at unattainable thresholds (our D5).
(4) USUAL FAILURE MODES. - Development-set optimism: the lead metric was chosen on E, so E cannot confirm it. - Verifier leakage/anchoring: whenever the checker sees part of the candidate (QA metrics generating questions from the summary; reference-free MT metrics rewarding copies; self-preference of same-family judges), it can inherit the candidate's error. This is the specific risk of giving peers the candidate's signature. - Instrument sharing between labeller and metric. - Quantised scores at unattainable thresholds. - Underpowered strata read as nulls or wins: the L25 CI half-width was ~0.085 with 300 sentences. - Cost stated in the wrong unit: iteration 3 mixed per-sentence and per-call costs, off by 13x.
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

id: dataset_iter4_dir4
type: dataset
objective: >-
  T7b: make the in-scope FREE condition of R_COMP testable, with labels that share no instrument with any consensus metric.
  An alignment-free labeller EXHAUSTIVELY searches arity-consistent injective symbol maps (with bounded merge/split and reification
  bridges) from each FREE candidate's symbols onto the template atoms, and checks z3 equivalence to the weak and strong readings.
  ERROR if no map yields equivalence. CORRECT if a map does AND a gated LLM gloss check confirms each mapped symbol's meaning.
  Otherwise UNRESOLVED. This replaces the panel route, which broke twice.
approach: |-
  INPUTS (read-only): R_COMP candidates /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/rcomp_candidates.jsonl (FREE rows: 2,024 incl. excluded; SIG rows with pure-z3 sig_labels.jsonl for the gate); exp 7 src/{label_sig.py, consensus_rcomp.py}; dataset 3 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/{full_data_out.json (rcomp_sentences: weak/strong references, template atoms, lexicon_ids), lexicon.json (atom English glosses), src/templates.py, src/verify.py, labeller/}.
  FIREWALL: do not read any consensus score, judge score or old FREE label while building the labeller. The old tier-A FREE labels are joined ONLY at the end, for an agreement table.
  STEP 0: prereg_freelab.json with sha256. It holds the map family, bridges, search caps, gloss prompt, gate, label rules and testability rule.
  MAP SEARCH:
  - Candidate symbols: predicates with arity, constants. Targets: template atoms and constants of the sentence.
  - Allowed maps: injective and arity-consistent, including argument permutations for binary predicates.
  - Bridges (bounded, declared): (a) reification: a candidate unary P(x) onto a template binary atom with one argument fixed to a template constant, and the converse; (b) merge: a candidate unary onto the conjunction of 2 template unaries; (c) split: 2 candidate unaries onto 1 template unary (both mapped to it).
  - Unmapped candidate symbols stay free uninterpreted symbols, which correctly makes ADD content non-equivalent.
  - Prefilter each map by truth-table fingerprints on 128 random finite interpretations (domain sizes 2-3); send only surviving maps to z3 (2 s timeout; UNKNOWN counted).
  - Cap per row at 2x10^5 maps or 90 s. Exceeding it gives UNRESOLVED_SEARCH_CAP, counted.
  Use a ProcessPool over 7 vCPUs.
  LABEL RULES:
  - ERROR_CERT: no map equivalent to weak OR strong. This is exact relative to the declared map and bridge family, and its soundness is audited below.
  - READING_CHOICE: equivalent only to the T8 converse. Excluded, as in SIG.
  - CORRECT: some equivalence map passes the gloss check for EVERY mapped symbol.
  - ERROR_GLOSS: every equivalence map fails the gloss check on at least one symbol, both checkers agreeing (e.g. structurally symmetric swapped roles).
  - UNRESOLVED otherwise.
  GLOSS CHECK: one call per (row, map) lists each mapped candidate symbol with the template atom's English gloss and the sentence, and asks YES/NO per symbol ('can this symbol name plausibly mean this in this sentence?'). Two checkers from families disjoint from the CSC peers (DeepSeek, Microsoft, OpenAI) and from the judges (Google flash-lite, OpenAI nano): anthropic/claude-haiku-4.5 and qwen/qwen3-235b-a22b-2507. A symbol passes only if BOTH say YES; a disagreement gives UNRESOLVED.
  GATE (before labelling FREE): balanced accuracy >= 0.90 per checker AND for the conjunction, with each class recall >= 0.85. The gate set comes from SIG rows and the lexicon: identity maps with template names (YES); WordNet-synonym renames (YES); nonce names (NO: meaning not confirmable); non-synonymous donor predicates from other lexicon entries (NO); argument-role swaps of binary atoms (NO). At least 100 items per class. If the gate fails, try ONE prompt revision on a fresh half of the gate set; if it still fails, FREE labels = ERROR_CERT + UNRESOLVED only, and that is declared.
  SOUNDNESS AUDITS:
  (i) Nonce-scramble every SIG row's symbols and run the map search. It must recover equivalence for >= 0.98 of SIG-CORRECT rows (the ERROR_CERT false-error rate) and certify all SIG-ERROR rows.
  (ii) Granularity outside the bridge family: for a stratified 60 FREE ERROR_CERT rows, one stronger model call (anthropic/claude-sonnet-4.5 or its successor) reports whether the candidate is a faithful translation with a different decomposition. This is an audit statistic only, never a label change; report the implied ERROR_CERT precision with a CI.
  (iii) Agreement with exp 7's old tier-A FREE labels, joined only now.
  TESTABILITY (before any metric): counts per template of ERROR / CORRECT / sentences. Testable = >= 50 ERROR and >= 50 CORRECT over >= 25 sentences, reported (1) on all FREE rows and (2) on rows NOT previously labelled tier A in iteration 3 (the untouched subset, which is primary for iteration 5). Previously seen rows are flagged seen_iter3.
  OUTPUT: full_data_out.json (exp_sel_data_out: input = JSON{text, candidate_fol, system, condition, template_id}, output = label; metadata: label_source, map certificate, gloss verdicts, unresolved_reason, seen_iter3, strata), gate_report.json, soundness_audit.json, testability_FREE_v2.json, seal.json (sha256 of the label vector), dataset_card.md. Reusable functions: exhaustive_map_label(candidate_fol, readings, atoms, glosses) and equivalent_modulo_vocab_exhaustive, with docstrings and tests. Spend cap $4 (expected ~$1.5: about 2.5k gloss calls x 2 checkers plus the gate and audit).
what_it_would_show: ''
depends_on: []
</artifact_direction>



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
id: art_zcwCQgTqk6DN
name: gen_art_dataset_3
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
iteration: 2
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

--- Artifact 7 ---
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

--- Artifact 8 ---
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

--- Artifact 9 ---
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

--- Artifact 10 ---
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

--- Artifact 11 ---
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

--- Artifact 12 ---
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

DATASET executor scope:
  Output: data_out.json with rows of {input, output, metadata_fold, ...} — raw data only, no derived computations
  DOES: Download/generate datasets, analyze candidates to pick the best ones, standardize to JSON schema (features, labels, folds, metadata), validate schema, split into full/mini/preview
  DOES NOT: Run experiments, train models, compute derived statistics (PID/MI/correlations/synergy matrices) as final output
  If you need to COMPUTE something from data (synergy matrices, MI scores, timing benchmarks), use an EXPERIMENT artifact instead
</artifact_executor_scope>

<artifact_planning_rules>
DATASET:
- Plan for REAL third-party datasets (HuggingFace, Kaggle, direct-download URLs) — downloadable within time and size constraints
- Describe dataset criteria (domain, size, format) — executors find exact sources, but you can suggest candidates or search directions
- ALWAYS prefer real datasets over synthetic. Synthetic is a LAST RESORT only when no suitable real data exists
</artifact_planning_rules>

<compute_profiles>
Choose the compute profile this artifact needs for execution.
Available profiles for dataset artifacts:
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
  "description": "Plan for a DATASET artifact.",
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
    "ideal_dataset_criteria": {
      "description": "What makes an ideal dataset for this purpose - size, format, content requirements",
      "title": "Ideal Dataset Criteria",
      "type": "string"
    },
    "dataset_search_plan": {
      "description": "Step-by-step plan for finding/creating this dataset - sources to check, fallback options",
      "title": "Dataset Search Plan",
      "type": "string"
    },
    "target_num_datasets": {
      "description": "How many individual datasets should be delivered. Count each dataset separately, not collections \u2014 a benchmark suite of N datasets counts as N. This controls how broadly the executor searches, so setting it too low will under-collect.",
      "title": "Target Num Datasets",
      "type": "integer"
    }
  },
  "required": [
    "title",
    "ideal_dataset_criteria",
    "dataset_search_plan",
    "target_num_datasets"
  ],
  "title": "DatasetPlan",
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

### [3] TOOL CALL — Skill · 2026-09-24 07:00:27 UTC

```
aii-handbook-auto-neurosymbolic
```

### [4] TOOL RESULT — Skill · 2026-09-24 07:00:27 UTC

```
{"success": true, "commandName": "aii-handbook-auto-neurosymbolic"}
```

### [5] TOOL CALL — Glob · 2026-09-24 07:00:27 UTC

```
Pattern: "**/*"
```

### [6] TOOL RESULT — Glob · 2026-09-24 07:00:27 UTC

```
{"filenames": ["/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/vendor_x5/vendor_a/fol_triage.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/vendor_x5/vendor_a/fol.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/vendor_x5/vendor_a/labeller.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/vendor_x5/vendor_a/content_accounting.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/vendor_x5/vendor_a/rewrites.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/vendor_x5/vendor_a/pipeline.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/vendor_x5/vendor_a/lint_smells.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/vendor_x5/vendor_a/repair_census.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/vendor_x5/vendor_a/disguise.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/vendor_x5/vendor_c/consensus.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/vendor_x5/vendor_c/repair_census.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/vendor_x5/vendor_c/eqcache.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/vendor_x5/vendor_c/common.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/vendor_x5/vendor_c/analysis.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/vendor_x5/vendor_c/fol.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/vendor_x5/vendor_c/rewrites.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/vendor_x5/vendor_d/labeller/__init__.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/vendor_x5/vendor_d/labeller/fol.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/vendor_x5/vendor_d/labeller/labeller.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/vendor_x5/vendor_d/labeller/repair_census.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/vendor_x5/vendor_d/judges.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/vendor_x5/vendor_d/disguise.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/vendor_x5/vendor_d/__init__.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/vendor_x5/vendor_e/fol.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/vendor_x5/vendor_e/disguise.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/vendor_x5/vendor_e/repair_census.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/vendor_x5/vendor_e/label_lib.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/vendor_x5/vendor_e/complexity_counts.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/vendor_x5/data_views.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/vendor_x5/__init__.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/vendor_x5/vendor_d/local_llm.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/vendor_x5/local_judge_E.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/vendor_x5/peer_text.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/vendor_x5/screen_fit.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/vendor_x5/score_E.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/vendor_x5/posthoc_nf_fusion.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/vendor_x5/analyse_E.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/vendor_x5/write_deviations.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/vendor_e_panel/assemble.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/vendor_x5/prereg_exp5.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/vendor_e_panel/disguise_e.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/vendor_x5/run_api_E.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/vendor_x5/key_monitor.sh", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/vendor_x5/vendor_a/llm.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/vendor_x5/vendor_c/peers.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/artifact_budget.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/vendor_e_panel/or_client.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/vendor_e_panel/panel.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/sig_prompt.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/gen_sig.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/label_sig.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/vendor_x5/vendor_d/common.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/vendor_x5/vendor_d/budget.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/testability.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/vendor_x5/pool_scoring.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/auc_tools.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/run_judges.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/key_poll.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/panel_rcomp.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/score_consensus.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/consensus_rcomp.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/write_records.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/analyse.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/local_judge_rcomp.py"], "durationMs": 42, "numFiles": 64, "truncated": false, "totalMatches": 64, "countIsComplete": true}
```

### [7] TOOL CALL — Glob · 2026-09-24 07:00:27 UTC

```
Pattern: "*"
```

### [8] TOOL RESULT — Glob · 2026-09-24 07:00:27 UTC

```
{"filenames": ["/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/labeller/fol.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/labeller/disguise.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/labeller/complexity_counts.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/pytest.ini", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/data_local/yuan-yang__MALLS-v0__MALLS-v0.1-train.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/data_local/yuan-yang__MALLS-v0__MALLS-v0.1-test.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/data_local/yfxiao__folio-refined__train.csv", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/data_local/opendatalab__ProverQA__dev_hard.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/data_local/folio_refined_validation.csv", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/data_local/DSAVlab-UNIUD_MALLS_test_subset-CURATED__MALLS_instances.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/data_local/DSAVlab-UNIUD_FOLIO_validation-curated__FOLIO_instances.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/work/e_models_snapshot.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/work/e_fewshot_exemplars.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/raw/logiclm/FOLIO_dev_text-davinci-003.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/raw/logiclm/FOLIO_dev_gpt-4.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/raw/logiclm/FOLIO_dev_gpt-3.5-turbo.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/tests/test_fol.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/prompts/zeroshot_v1.txt", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/prompts/fewshot_v1.txt", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/src_e/generate.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/src_e/or_client.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/src_e/normalise.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/src_e/select_sentences.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/labeller/repair_census.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/labeller/lint_smells.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/labeller/label_lib.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/work/models_snapshot.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/src/common.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/src/source_pool.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/logs/source_pool.log", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/work/source_pool_log.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/work/source_rules.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/cost_ledger.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/raw/lexicon_extract.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/work/lexicon_extract_jobs.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/logs/key_poll.pid", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/src/key_poll.sh", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/src/templates.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/tests/test_templates.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/logs/compose.log", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/work/lexicon_check_log.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/work/lexicon_checked.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/src/select_rcomp.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/tests/test_perturb.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/logs/perturb.pid", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/logs/perturb.log", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/src/perturb.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/logs/perturb_run.out", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/work/perturb_log.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/work/perturb_bases.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/work/perturb_controls.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/work/perturb_suite.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/temp/search/hf_search_results.txt", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/temp/search/hf_previews.txt", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/src/hf_preview.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/temp/search/hf_previews.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/.aii_cost_ledger.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/temp/search/web_research.txt", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/adjudication_prompt.txt", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/work/adjudicator_model.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/src/label_rcomp.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/logs/label_rcomp.log", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/work/rcomp_labels_dryrun.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/work/label_pair_cache_dryrun.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/logs/adjudicate.log", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/work/adjudicator_check_items.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/src/compose.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/work/compose_log.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/work/rcomp_pool.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/work/rcomp_preselect.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/work/select_log.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/work/rcomp_sentences.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/src/prereg.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/prereg_rcomp.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/logs/prereg.log", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/logs/assemble.log", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/watch_and_run.sh", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/src/make_variants.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/src/gen_rcomp.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/temp/search/selection.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/logs/watch.pid", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/src/verify.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/logs/verify.log", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/src/adjudicate.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/src/llm_phases.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/src/llm.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/src/lexicon.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/lexicon.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/logs/lexicon.log", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/work/lexicon_audit_jobs.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/work/executor_lexicon_spotcheck.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/logs/watch.log", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/src/assemble.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/work/assembled.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/work/stats.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/work/disguise_guard.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/data.py", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/run_all.sh", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/adjudicator_check_out.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/logs/data.log"], "durationMs": 63, "numFiles": 100, "truncated": true, "totalMatches": 118, "countIsComplete": true}
```

### [9] TOOL CALL — Glob · 2026-09-24 07:00:33 UTC

```
Pattern: "results/*"
```

### [10] TOOL RESULT — Glob · 2026-09-24 07:00:33 UTC

```
{"filenames": ["/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/prereg_sig.sha256", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/prereg_sig.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/sig_pilot_projection.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/scores_SIG_stage_mini.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/judge_regression_T4.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/sig_classes.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/sig_labels.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/testability_SIG.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/prices.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/disguise_map_SIG.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/scores_SIG.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/scores_SIG_stage_all.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/sig_repairs.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/judge_SIG.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/frontier_subsample.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/judge_frontier_SIG.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/disguise_map_FREE.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/scores_FREE_stage_mini.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/judge_rows_SIG.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/scores_FREE.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/scores_FREE_stage_all.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/llm_cache.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/costs.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/judge_FREE.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/budget_state.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/free_labels.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/scores_rename_SIG.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/judge_local_SIG.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/judge_local_FREE.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/local_cache.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/testability_FREE.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/testability.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/analysis_rows_SIG.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/tables.md", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/analysis.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/rcomp_candidates.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/audit_rederive.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/VENDOR_SHA256.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/deviations.json", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/rederive_raw.json"], "durationMs": 449, "numFiles": 40, "truncated": false, "totalMatches": 40, "countIsComplete": true}
```

### [11] TOOL CALL — Read · 2026-09-24 07:00:33 UTC

```
/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/label_sig.py
```

### [12] TOOL RESULT — Read · 2026-09-24 07:00:33 UTC

```
{"type": "text", "file": {"filePath": "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/label_sig.py", "content": "#!/usr/bin/env python3\n\"\"\"S5: SIG labels by PURE z3 equivalence to the template references (no aligner, no panel, no LLM).\n\ncanon_case(c, sentence): every predicate / constant of candidate c is mapped case-insensitively onto the sentence's\nsignature (exact equality after lower-casing, nothing else). A symbol without a case-insensitive match makes the row\nOFF_SIGNATURE; a matched predicate with a different arity makes it OFF_SIGNATURE_ARITY.\nSecondary label view (pre-registered F3 'OFF_SIG_EXACT_RENAME'): the loose normaliser lower-cases and strips '_' and '-'\n(still aligner-free: no similarity threshold).\n\nPer sentence, on-signature candidates collapse into exact classes (identical normalised canonical string, or plain z3 EQ,\nms=3000). Per class: ew = equivalent(class, weak), es = vs strong, T8 also ec = vs the not-accepted converse\n(ms=5000, retried at 20000 on None):\n  ew or es True                  -> CORRECT (matched_reading weak / strong / both)\n  T8 and ec True                 -> READING_CHOICE (excluded from the primary pool)\n  ew False and es False (and ec False on T8) -> ERROR\n  otherwise                      -> UNKNOWN (excluded, counted)\n  parse failure                  -> UNPARSEABLE (coverage view only)\n\nusage: label_sig.py label   -> results/sig_labels.jsonl (one row per SIG generation record) + results/sig_classes.json\n       label_sig.py repair  -> results/sig_repairs.jsonl (secondary: minimal typed repair ops of ERROR classes)\n\"\"\"\nfrom __future__ import annotations\n\nimport argparse\nimport hashlib\nimport json\nimport multiprocessing as mp\nimport re\nimport sys\nimport time\nfrom collections import Counter, defaultdict\nfrom concurrent.futures import ProcessPoolExecutor, as_completed\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nRC = ROOT / \"rcomp\"\nfor p in (RC / \"labeller\", RC / \"src_e\", ROOT / \"src\"):\n    if str(p) not in sys.path:\n        sys.path.insert(0, str(p))\nsys.setrecursionlimit(10000)\nfrom fol import parse, equivalent  # noqa: E402\nfrom repair_census import atoms, bound_vars  # noqa: E402\n\nimport sig_prompt as SP  # noqa: E402\n\nRES = ROOT / \"results\"\nGEN = RC / \"raw\" / \"generations_sig.jsonl\"\n\n\ndef sha1(s: str) -> str:\n    return hashlib.sha1(s.encode()).hexdigest()\n\n\ndef item_id(system: str, text: str, raw: str) -> str:\n    \"\"\"Dataset E's item_id recipe: sha1(system | norm(text) | raw)[:16].\"\"\"\n    import select_sentences as ss\n    return sha1(system + \"|\" + ss.norm(text) + \"|\" + (raw or \"\"))[:16]\n\n\ndef _to_str(e) -> str:\n    k = e[0]\n    if k == \"atom\":\n        return f\"{e[1]}({', '.join(e[2])})\" if e[2] else e[1]\n    if k in (\"all\", \"ex\"):\n        return f\"{'∀' if k == 'all' else '∃'}{e[1]} ({_to_str(e[2])})\"\n    if k == \"not\":\n        return f\"¬({_to_str(e[1])})\"\n    sym = {\"and\": \"∧\", \"or\": \"∨\", \"imp\": \"→\", \"iff\": \"↔\", \"xor\": \"⊕\"}[k]\n    return f\"({_to_str(e[1])} {sym} {_to_str(e[2])})\"\n\n\ndef _rename(e, pmap: dict, cmap: dict, bv=frozenset()):\n    k = e[0]\n    if k == \"atom\":\n        return (\"atom\", pmap.get(e[1], e[1]), tuple(x if x in bv else cmap.get(x, x) for x in e[2]))\n    if k in (\"all\", \"ex\"):\n        return (k, e[1], _rename(e[2], pmap, cmap, bv | {e[1]}))\n    if k == \"not\":\n        return (\"not\", _rename(e[1], pmap, cmap, bv))\n    return (k, _rename(e[1], pmap, cmap, bv), _rename(e[2], pmap, cmap, bv))\n\n\ndef _free_consts(e) -> set:\n    out = set()\n\n    def walk(x, bv):\n        if x[0] == \"atom\":\n            out.update(a for a in x[2] if a not in bv)\n        elif x[0] in (\"all\", \"ex\"):\n            walk(x[2], bv | {x[1]})\n        elif x[0] == \"not\":\n            walk(x[1], bv)\n        else:\n            walk(x[1], bv); walk(x[2], bv)\n    walk(e, frozenset())\n    return out\n\n\ndef _norm_loose(s: str) -> str:\n    return re.sub(r\"[_\\-]\", \"\", s.lower())\n\n\ndef canon_case(fol: str, sent: dict, loose: bool = False) -> tuple[str, object, dict]:\n    \"\"\"-> (status, canonical AST or None, info). status in ON_SIGNATURE / OFF_SIGNATURE / OFF_SIGNATURE_ARITY / UNPARSEABLE.\"\"\"\n    try:\n        e = parse(fol)\n    except Exception as ex:  # noqa: BLE001 - parser raises assorted errors on junk\n        return \"UNPARSEABLE\", None, {\"parse_error\": str(ex)[:120]}\n    sig_p, sig_c = SP.signature_symbols(sent)\n    f = _norm_loose if loose else str.lower\n    pl = defaultdict(list)\n    for n in sig_p:\n        pl[f(n)].append(n)\n    cl = defaultdict(list)\n    for c in sig_c:\n        cl[f(c)].append(c)\n    pmap, cmap, extra, arity_bad = {}, {}, [], []\n    for a in atoms(e):\n        name, ar = a[1], len(a[2])\n        hits = pl.get(f(name), [])\n        if len(hits) != 1:\n            extra.append(f\"{name}/{ar}\")\n            continue\n        tgt = hits[0]\n        if sig_p[tgt] != ar:\n            arity_bad.append(f\"{name}/{ar}->{tgt}/{sig_p[tgt]}\")\n            continue\n        pmap[name] = tgt\n    for c in _free_consts(e):\n        hits = cl.get(f(c), [])\n        if len(hits) != 1:\n            extra.append(f\"const:{c}\")\n        else:\n            cmap[c] = hits[0]\n    info = {\"extra_symbols\": sorted(set(extra)), \"arity_mismatch\": sorted(set(arity_bad))}\n    if extra:\n        return \"OFF_SIGNATURE\", None, info\n    if arity_bad:\n        return \"OFF_SIGNATURE_ARITY\", None, info\n    return \"ON_SIGNATURE\", _rename(e, pmap, cmap), info\n\n\ndef signature_status(fol: str, sent: dict) -> tuple[str, dict]:\n    st, _, info = canon_case(fol, sent)\n    return st, info\n\n\ndef _eq(a, b) -> bool | None:\n    r = equivalent(a, b, ms=5000)\n    if r is None:\n        r = equivalent(a, b, ms=20000)\n    return r\n\n\ndef label_sentence(job: dict) -> dict:\n    \"\"\"Worker: all SIG rows of one sentence -> per-row status + class ids + class labels (strict and loose views).\"\"\"\n    import sys as _s\n    _s.setrecursionlimit(10000)\n    sent, rows = job[\"sent\"], job[\"rows\"]\n    t0 = time.time()\n    refs = {\"weak\": parse(sent[\"reference_fol_weak\"]), \"strong\": parse(sent[\"reference_fol_strong\"])}\n    if sent.get(\"reading_converse\"):\n        refs[\"converse\"] = parse(sent[\"reading_converse\"])\n    out = {\"sentence_id\": sent[\"sentence_id\"], \"rows\": {}, \"classes\": {}, \"classes_loose\": {}}\n    for view in (\"strict\", \"loose\"):\n        reps = []\n        for r in rows:\n            key = r[\"row_key\"]\n            if not r.get(\"parse_ok\"):\n                st, ast, info = \"UNPARSEABLE\", None, {}\n            else:\n                st, ast, info = canon_case(r[\"candidate_fol\"], sent, loose=(view == \"loose\"))\n            rec = out[\"rows\"].setdefault(key, {})\n            rec[f\"sig_status_{view}\"] = st\n            if view == \"strict\":\n                rec[\"sig_info\"] = info\n            if ast is None:\n                rec[f\"class_{view}\"] = None\n                continue\n            cs = _to_str(ast)\n            norm = re.sub(r\"\\s+\", \"\", cs)\n            hit = None\n            for c in reps:\n                if c[\"norm\"] == norm:\n                    hit = c; break\n            if hit is None:\n                for c in reps:\n                    if equivalent(c[\"ast\"], ast, ms=3000) is True:\n                        hit = c; break\n            if hit is None:\n                hit = {\"class_id\": f\"{sent['sentence_id']}:{'k' if view == 'strict' else 'l'}{len(reps)}\", \"norm\": norm, \"ast\": ast, \"fol\": cs}\n                reps.append(hit)\n            rec[f\"class_{view}\"] = hit[\"class_id\"]\n            rec[f\"canon_{view}\"] = cs\n        tgt = out[\"classes\"] if view == \"strict\" else out[\"classes_loose\"]\n        for c in reps:\n            ew, es = _eq(c[\"ast\"], refs[\"weak\"]), _eq(c[\"ast\"], refs[\"strong\"])\n            ec = _eq(c[\"ast\"], refs[\"converse\"]) if \"converse\" in refs else None\n            if ew is True or es is True:\n                lab = \"CORRECT\"\n                mr = \"both\" if (ew is True and es is True) else (\"weak\" if ew is True else \"strong\")\n            elif \"converse\" in refs and ec is True:\n                lab, mr = \"READING_CHOICE\", None\n            elif ew is False and es is False and (\"converse\" not in refs or ec is False):\n                lab, mr = \"ERROR\", None\n            else:\n                lab, mr = \"UNKNOWN\", None\n            tgt[c[\"class_id\"]] = {\"fol\": c[\"fol\"], \"label\": lab, \"matched_reading\": mr, \"eq_weak\": ew, \"eq_strong\": es,\n                                  \"eq_converse\": ec}\n    out[\"secs\"] = round(time.time() - t0, 2)\n    return out\n\n\ndef load_sig_rows(sents: dict) -> list[dict]:\n    last = {}\n    for l in GEN.read_text().splitlines():\n        if not l.strip():\n            continue\n        r = json.loads(l)\n        if r[\"sentence_id\"] in sents:\n            last[(r[\"sentence_id\"], r[\"slot\"], r[\"prompt_variant\"])] = r\n    rows = []\n    for r in last.values():\n        if r.get(\"raw_output\") is None:\n            continue  # API failure: not a candidate (counted in the generation log)\n        r = dict(r)\n        r[\"item_id\"] = item_id(r[\"system\"], sents[r[\"sentence_id\"]][\"text\"], r[\"raw_output\"])\n        r[\"row_key\"] = r[\"item_id\"] + \"|SIG|\" + r[\"slot\"]\n        rows.append(r)\n    return rows\n\n\ndef run_label(workers: int = 16) -> None:\n    from loguru import logger\n    rs = json.loads((RC / \"work\" / \"rcomp_sentences.json\").read_text())\n    sents = {r[\"sentence_id\"]: r for r in rs}\n    rows = load_sig_rows(sents)\n    by = defaultdict(list)\n    for r in rows:\n        by[r[\"sentence_id\"]].append(r)\n    jobs = [{\"sent\": sents[sid], \"rows\": [{k: r[k] for k in (\"row_key\", \"candidate_fol\", \"parse_ok\")} for r in rr]}\n            for sid, rr in sorted(by.items())]\n    logger.info(f\"SIG labelling: {len(rows)} rows over {len(jobs)} sentences, {workers} workers\")\n    res = {}\n    t0 = time.time()\n    with ProcessPoolExecutor(max_workers=workers, mp_context=mp.get_context(\"spawn\")) as ex:\n        futs = {ex.submit(label_sentence, j): j[\"sent\"][\"sentence_id\"] for j in jobs}\n        for i, f in enumerate(as_completed(futs), 1):\n            sid = futs[f]\n            try:\n                res[sid] = f.result(timeout=900)\n            except Exception as e:  # noqa: BLE001 - one sentence must not kill the run; its rows become UNKNOWN\n                logger.error(f\"sentence {sid} failed: {type(e).__name__}: {e}\")\n                res[sid] = {\"sentence_id\": sid, \"rows\": {}, \"classes\": {}, \"classes_loose\": {}, \"error\": str(e)[:200]}\n            if i % 25 == 0:\n                logger.info(f\"labelled {i}/{len(jobs)} sentences, {time.time() - t0:.0f}s\")\n    out_rows = []\n    for r in rows:\n        s = sents[r[\"sentence_id\"]]\n        o = res[r[\"sentence_id\"]][\"rows\"].get(r[\"row_key\"], {})\n        cid, cidl = o.get(\"class_strict\"), o.get(\"class_loose\")\n        st = o.get(\"sig_status_strict\", \"UNKNOWN_WORKER_FAIL\")\n        if st == \"UNPARSEABLE\":\n            lab = \"UNPARSEABLE\"\n        elif st.startswith(\"OFF_SIGNATURE\"):\n            lab = st\n        elif cid is None:\n            lab = \"UNKNOWN\"\n        else:\n            lab = res[r[\"sentence_id\"]][\"classes\"][cid][\"label\"]\n        cl = res[r[\"sentence_id\"]][\"classes\"].get(cid, {}) if cid else {}\n        stl = o.get(\"sig_status_loose\")\n        if stl == \"UNPARSEABLE\":\n            labl = \"UNPARSEABLE\"\n        elif stl and stl.startswith(\"OFF_SIGNATURE\"):\n            labl = stl\n        elif cidl:\n            labl = res[r[\"sentence_id\"]][\"classes_loose\"][cidl][\"label\"]\n        else:\n            labl = \"UNKNOWN\"\n        out_rows.append({\"row_key\": r[\"row_key\"], \"item_id\": r[\"item_id\"], \"sentence_id\": r[\"sentence_id\"], \"condition\": \"SIG\",\n                         \"system\": r[\"system\"], \"slot\": r[\"slot\"], \"family\": r[\"family\"], \"model\": r[\"model\"],\n                         \"prompt_variant\": r[\"prompt_variant\"], \"raw_output\": r[\"raw_output\"], \"candidate_fol\": r[\"candidate_fol\"],\n                         \"parse_ok\": r[\"parse_ok\"], \"cost_usd\": r.get(\"cost_usd\"), \"finish_reason\": r.get(\"finish_reason\"),\n                         \"label\": lab, \"label_source\": \"z3_exact_sig\", \"label_tier\": \"A_exact\",\n                         \"matched_reading\": cl.get(\"matched_reading\"), \"off_signature\": st.startswith(\"OFF_SIGNATURE\"),\n                         \"sig_status\": st, \"sig_info\": o.get(\"sig_info\"), \"sig_class_id\": cid, \"canon_fol\": o.get(\"canon_strict\"),\n                         \"label_loose\": labl, \"sig_status_loose\": stl, \"sig_class_id_loose\": cidl,\n                         \"template_id\": s[\"template_id\"], \"clause_type\": s[\"clause_type\"]})\n    with (RES / \"sig_labels.jsonl\").open(\"w\") as fh:\n        for r in out_rows:\n            fh.write(json.dumps(r, ensure_ascii=False) + \"\\n\")\n    (RES / \"sig_classes.json\").write_text(json.dumps({sid: {\"classes\": v[\"classes\"], \"classes_loose\": v[\"classes_loose\"],\n                                                            \"secs\": v.get(\"secs\"), \"error\": v.get(\"error\")}\n                                                      for sid, v in res.items()}, ensure_ascii=False))\n    logger.info(f\"SIG labels: {dict(Counter(r['label'] for r in out_rows))}; loose view {dict(Counter(r['label_loose'] for r in out_rows))}; \"\n                f\"{time.time() - t0:.0f}s\")\n\n\ndef repair_class(job: dict) -> dict:\n    import sys as _s\n    _s.setrecursionlimit(10000)\n    from label_lib import minimal_typed_repair\n    c = parse(job[\"fol\"])\n    best = None\n    for rd in (\"weak\", \"strong\"):\n        ops, secs, st = minimal_typed_repair(c, parse(job[rd]), budget_s=8.0)\n        if st == \"FOUND\" and (best is None or len(ops) < len(best[1])):\n            best = (rd, ops)\n    return {\"class_id\": job[\"class_id\"], \"repair_status\": \"FOUND\" if best else \"COMPOUND\",\n            \"repair_reading\": best[0] if best else None, \"repair_ops\": best[1] if best else None}\n\n\ndef run_repair(workers: int = 5) -> None:\n    from loguru import logger\n    sents = {r[\"sentence_id\"]: r for r in json.loads((RC / \"work\" / \"rcomp_sentences.json\").read_text())}\n    cls = json.loads((RES / \"sig_classes.json\").read_text())\n    outp = RES / \"sig_repairs.jsonl\"\n    done = {json.loads(l)[\"class_id\"] for l in outp.read_text().splitlines() if l.strip()} if outp.exists() else set()\n    jobs = []\n    for sid, v in cls.items():\n        for cid, c in v[\"classes\"].items():\n            if c[\"label\"] == \"ERROR\" and cid not in done:\n                jobs.append({\"class_id\": cid, \"fol\": c[\"fol\"], \"weak\": sents[sid][\"reference_fol_weak\"],\n                             \"strong\": sents[sid][\"reference_fol_strong\"]})\n    logger.info(f\"repair: {len(jobs)} ERROR classes\")\n    with ProcessPoolExecutor(max_workers=workers, mp_context=mp.get_context(\"spawn\")) as ex, outp.open(\"a\") as fh:\n        futs = {ex.submit(repair_class, j): j for j in jobs}\n        for f in as_completed(futs):\n            try:\n                r = f.result(timeout=120)\n            except Exception as e:  # noqa: BLE001\n                r = {\"class_id\": futs[f][\"class_id\"], \"repair_status\": \"WORKER_FAIL\", \"error\": str(e)[:200]}\n            fh.write(json.dumps(r) + \"\\n\")\n            fh.flush()\n    logger.info(\"repair done\")\n\n\nif __name__ == \"__main__\":\n    from loguru import logger\n    logger.remove()\n    logger.add(sys.stdout, level=\"INFO\", format=\"{time:HH:mm:ss}|{level:<7}|{message}\")\n    logger.add(ROOT / \"logs\" / \"label_sig.log\", rotation=\"30 MB\", level=\"DEBUG\")\n    ap = argparse.ArgumentParser()\n    ap.add_argument(\"cmd\", choices=[\"label\", \"repair\"])\n    ap.add_argument(\"--workers\", type=int, default=16)\n    a = ap.parse_args()\n    run_label(a.workers) if a.cmd == \"label\" else run_repair(a.workers)\n", "numLines": 349, "startLine": 1, "totalLines": 349}}
```

### [13] TOOL CALL — Read · 2026-09-24 07:00:33 UTC

```
/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/src/templates.py
```

### [14] TOOL RESULT — Read · 2026-09-24 07:00:33 UTC

```
{"type": "text", "file": {"filePath": "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/src/templates.py", "content": "\"\"\"The 9 R_COMP templates. Each fills English text AND derives the weak / strong (/ converse) FOL readings\ncompositionally from the same slots, so the reference is correct by construction given a correct atom lexicon.\n\nSlot = dict(pred=..., atom=<FOL atom over x>, vp=<3sg verb phrase>, neg=<bool>) for conditions C1..C3;\nQ (consequent), E (exception) and P (proviso) are positive slots; N is the sortal noun with its FOL atom S.\nReadings (A_i = condition literal, S = sortal atom):\n  T1/T2/T4/T5/T6 weak  ∀x (S ∧ A1 ∧ A2 ∧ A3 ∧ ¬E → Q)        strong ∀x (S ∧ A1 ∧ A2 ∧ A3 → (Q ↔ ¬E))\n  T3             weak  ∀x (S ∧ A1 ∧ A2 ∧ P ∧ A3 → Q)         strong ∀x (S ∧ A1 ∧ A2 → (Q ↔ (P ∧ A3)))\n  T7 (no S)      weak  ∀x (A1 ∧ A2 ∧ A3 ∧ ¬E → Q)            strong ∀x (A1 ∧ A2 ∧ A3 → (Q ↔ ¬E))\n  T8             weak  ∀x (S ∧ A1 ∧ A2 ∧ A3 ∧ Q → P)         strong ∀x (S ∧ A1 ∧ A2 ∧ A3 → (Q ↔ P))\n                 converse (stored, NOT accepted) ∀x (S ∧ A1 ∧ A2 ∧ A3 ∧ P → Q)\n  T9             weak  ∀x (S ∧ A1 ∧ A2 ∧ A3 ∧ ¬E → ¬Q)       strong ∀x (S ∧ A1 ∧ A2 ∧ A3 → (¬Q ↔ ¬E))\n\"\"\"\nfrom __future__ import annotations\n\nimport re\n\nTEMPLATES = [\"T1\", \"T2\", \"T3\", \"T4\", \"T5\", \"T6\", \"T7\", \"T8\", \"T9\"]\nCLAUSE = {\"T1\": \"unless\", \"T2\": \"except_when\", \"T3\": \"provided_that\", \"T4\": \"as_long_as+unless\",\n          \"T5\": \"provided_that+unless\", \"T6\": \"except_when+provided_that\", \"T7\": \"unless\", \"T8\": \"but_only_if\",\n          \"T9\": \"unless\"}\nNESTED = {\"T4\": False, \"T5\": True, \"T6\": False}\nUSES_E = {\"T1\", \"T2\", \"T4\", \"T5\", \"T6\", \"T7\", \"T9\"}\nUSES_P = {\"T3\", \"T8\"}\n\n\ndef lit(s: dict) -> str:\n    return (\"¬\" if s.get(\"neg\") else \"\") + s[\"atom\"]\n\n\ndef cvp(s: dict) -> str:\n    return s[\"neg_vp\"] if s.get(\"neg\") else s[\"vp\"]\n\n\ndef art(noun: str) -> str:\n    return \"an\" if re.match(r\"[aeiou]\", noun.lower()) else \"a\"\n\n\ndef conj(*xs: str) -> str:\n    return \" ∧ \".join(xs)\n\n\ndef plural_vp(vp: str) -> str | None:\n    \"\"\"Re-inflect a 3sg verb phrase for 'they' by a fixed table: is->are, has->have, does->do, -s stripping.\"\"\"\n    w = vp.split()\n    if not w:\n        return None\n    f = w[0].lower()\n    table = {\"is\": \"are\", \"has\": \"have\", \"does\": \"do\", \"was\": \"were\", \"isn't\": \"aren't\", \"doesn't\": \"don't\",\n             \"hasn't\": \"haven't\"}\n    if f in table:\n        w[0] = table[f]\n    elif f in (\"can\", \"cannot\", \"can't\", \"will\", \"won't\", \"may\", \"might\", \"must\", \"should\", \"would\", \"could\"):\n        pass\n    elif re.fullmatch(r\"[a-z]+ies\", f) and len(f) > 4:\n        w[0] = f[:-3] + \"y\"\n    elif re.fullmatch(r\"[a-z]+(ches|shes|sses|xes|zzes|oes)\", f):\n        w[0] = f[:-2]\n    elif re.fullmatch(r\"[a-z]+s\", f) and not f.endswith(\"ss\"):\n        w[0] = f[:-1]\n    else:\n        return None\n    return \" \".join(w)\n\n\ndef fill(t: str, v: int, N: str, S: str, C: list[dict], Q: dict, X: dict | None, person: bool) -> dict:\n    \"\"\"t template id, v lexical variant (0/1), N noun, S sortal atom, C 3 condition slots, Q consequent,\n    X exception (E) or proviso (P) slot. Returns text + readings.\"\"\"\n    rel = \"who\" if person else \"that\"\n    c1, c2, c3 = (cvp(c) for c in C)\n    a1, a2, a3 = (lit(c) for c in C)\n    q, qa = Q[\"vp\"], Q[\"atom\"]\n    x, xa = (X[\"vp\"], X[\"atom\"]) if X else (None, None)\n    the = f\"the {N}\"\n    conv = None\n    if t == \"T1\":\n        det, exc = (\"Every\", \"unless\") if v == 0 else (\"Each\", \"except if\")\n        text = f\"{det} {N} {rel} {c1}, {rel} {c2}, and {rel} {c3} {q}, {exc} {the} {x}.\"\n        weak = f\"∀x ({conj(S, a1, a2, a3, '¬' + xa)} → {qa})\"\n        strong = f\"∀x ({conj(S, a1, a2, a3)} → ({qa} ↔ ¬{xa}))\"\n    elif t == \"T2\":\n        if v == 0:\n            text = f\"If {art(N)} {N} {c1} and {c2}, and {the} also {c3}, then {the} {q}, except when {the} {x}.\"\n        else:\n            text = f\"When {art(N)} {N} {c1} and {c2}, and {the} also {c3}, {the} {q}, except when {the} {x}.\"\n        weak = f\"∀x ({conj(S, a1, a2, a3, '¬' + xa)} → {qa})\"\n        strong = f\"∀x ({conj(S, a1, a2, a3)} → ({qa} ↔ ¬{xa}))\"\n    elif t == \"T3\":\n        det, prov = (\"Any\", \"provided that\") if v == 0 else (\"Every\", \"providing that\")\n        text = f\"{det} {N} that {c1} and that {c2} {q}, {prov} {the} {x} and {c3}.\"\n        weak = f\"∀x ({conj(S, a1, a2, xa, a3)} → {qa})\"\n        strong = f\"∀x ({conj(S, a1, a2)} → ({qa} ↔ ({xa} ∧ {a3})))\"\n    elif t == \"T4\":\n        al = \"as long as\" if v == 0 else \"so long as\"\n        text = f\"{art(N).capitalize()} {N} {rel} {c1} and {rel} {c2} {q} {al} {the} {c3}, unless {the} {x}.\"\n        weak = f\"∀x ({conj(S, a1, a2, a3, '¬' + xa)} → {qa})\"\n        strong = f\"∀x ({conj(S, a1, a2, a3)} → ({qa} ↔ ¬{xa}))\"\n    elif t == \"T5\":\n        det, exc = (\"Every\", \"unless\") if v == 0 else (\"Each\", \"except if\")\n        text = f\"{det} {N} {rel} {c1} and {rel} {c2} {q}, provided that {the} {c3}, {exc} {the} {x}.\"\n        weak = f\"∀x ({conj(S, a1, a2, a3, '¬' + xa)} → {qa})\"\n        strong = f\"∀x ({conj(S, a1, a2, a3)} → ({qa} ↔ ¬{xa}))\"\n    elif t == \"T6\":\n        exc, det = (\"Except when\", \"every\") if v == 0 else (\"Except if\", \"each\")\n        text = f\"{exc} {the} {x}, {det} {N} {rel} {c1} and {rel} {c2} {q}, provided that {the} {c3}.\"\n        weak = f\"∀x ({conj(S, a1, a2, a3, '¬' + xa)} → {qa})\"\n        strong = f\"∀x ({conj(S, a1, a2, a3)} → ({qa} ↔ ¬{xa}))\"\n    elif t == \"T7\":\n        who = \"Anyone\" if v == 0 else \"Anybody\"\n        px = plural_vp(x)\n        if px is None:\n            return None\n        text = f\"{who} who {c1}, {c2}, and {c3} {q} unless they {px}.\"\n        weak = f\"∀x ({conj(a1, a2, a3, '¬' + xa)} → {qa})\"\n        strong = f\"∀x ({conj(a1, a2, a3)} → ({qa} ↔ ¬{xa}))\"\n    elif t == \"T8\":\n        if v == 0:\n            text = f\"If {art(N)} {N} {c1}, {c2}, and {c3}, then {the} {q}, but only if {the} {x}.\"\n        else:\n            text = f\"When {art(N)} {N} {c1}, {c2}, and {c3}, {the} {q}, but only if {the} {x}.\"\n        weak = f\"∀x ({conj(S, a1, a2, a3, qa)} → {xa})\"\n        strong = f\"∀x ({conj(S, a1, a2, a3)} → ({qa} ↔ {xa}))\"\n        conv = f\"∀x ({conj(S, a1, a2, a3, xa)} → {qa})\"\n    elif t == \"T9\":\n        rel9 = rel if v == 0 else \"that\"\n        exc = \"unless\" if v == 0 else \"except when\"\n        text = f\"No {N} {rel9} {c1}, {rel9} {c2}, and {rel9} {c3} {q}, {exc} {the} {x}.\"\n        weak = f\"∀x ({conj(S, a1, a2, a3, '¬' + xa)} → ¬{qa})\"\n        strong = f\"∀x ({conj(S, a1, a2, a3)} → (¬{qa} ↔ ¬{xa}))\"\n    else:\n        raise ValueError(t)\n    text = re.sub(r\"\\s+\", \" \", text)\n    return {\"text\": text[0].upper() + text[1:], \"reference_fol_weak\": weak, \"reference_fol_strong\": strong,\n            \"reading_converse\": conv, \"template_id\": t, \"surface_variant\": f\"{t}v{v}\", \"clause_type\": CLAUSE[t],\n            \"nested\": NESTED.get(t, False)}\n", "numLines": 136, "startLine": 1, "totalLines": 136}}
```

### [15] TOOL CALL — Read · 2026-09-24 07:00:39 UTC

```
/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/rcomp_candidates.jsonl
```

### [16] TOOL RESULT — Read · 2026-09-24 07:00:39 UTC

```
{"type": "text", "file": {"filePath": "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/rcomp_candidates.jsonl", "content": "{\"row_key\": \"917ac90fc8143e08|SIG|G7\", \"item_id\": \"917ac90fc8143e08\", \"sentence_id\": \"001a7f0caf5a\", \"condition\": \"SIG\", \"template_id\": \"T1\", \"slot\": \"G7\", \"system\": \"G7:openai/gpt-4.1-mini\", \"family\": \"openai\", \"prompt_variant\": \"sig_v1\", \"candidate_fol\": \"∀x ((Legislator(x) ∧ At(x, boardGameNight) ∧ VisitRegularly(x, coffeeShop) ∧ Can(x, distinguishTheTasteOfDifferentCondiments) ∧ ¬ElectedOfficial(x)) → EmilysFriend_2(x))\", \"parse_ok\": true, \"label\": \"CORRECT\", \"label_source\": \"z3_exact_sig\", \"label_tier\": \"A_exact\", \"matched_reading\": \"weak\", \"off_signature\": false, \"sig_status\": \"ON_SIGNATURE\", \"repair_ops\": null, \"repair_status\": null, \"strata\": {\"words\": 34, \"word_tercile\": \"W2\", \"nconds_weak\": 5, \"nconds_bin\": \"5\", \"depth_weak\": 5, \"nquant\": 1, \"nested\": false, \"negated_condition\": false, \"clause_type\": \"unless\", \"template_id\": \"T1\"}, \"sig_class_id\": \"001a7f0caf5a:k0\", \"sig_class_id_size\": 8, \"sig_class_id_n_peers\": 9, \"sig_class_id_n_peers_same_class\": 7, \"sig_class_id_peer_majority_class\": \"001a7f0caf5a:k0\", \"sig_class_id_is_peer_majority\": true, \"free_solver_class_id\": null, \"free_align_class_id\": null, \"free_hyb_class_id\": null, \"free_align_class_id_size\": null, \"free_align_class_id_is_peer_majority\": null, \"free_hyb_class_id_size\": null, \"free_hyb_class_id_is_peer_majority\": null, \"n_peers_sig\": 9, \"n_peers_equal_sig\": 7, \"n_unknown_sig\": 0, \"n_peers_hyb\": null, \"correct_not_equivalent\": null, \"ref_flagged\": null, \"tier_B_provisional\": null, \"panel_votes\": null, \"cost_usd\": 0.000356, \"secs_sig\": 0.0, \"coverage_status\": \"OK\", \"c_score_sig\": 0.2222222222222222, \"c_score_align\": 0.2222222222222222, \"c_score_nf\": 0.2222222222222222, \"c_score_hyb\": 0.2222222222222222, \"g_align\": 0.0, \"g_nf\": 0.0, \"judge_cheap_disg\": 0.15000000000000002, \"judge_cheap_orig\": 0.050000000000000044, \"judge_frontier_orig\": null, \"judge_frontier_disg\": null, \"judge_local_disg\": 0.09999999999999998, \"judge_local_orig\": 0.09999999999999998}", "numLines": 1, "startLine": 1, "totalLines": 4863}}
```

### [17] TOOL CALL — Read · 2026-09-24 07:00:39 UTC

```
/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/lexicon.json
```

### [18] TOOL RESULT — Read · 2026-09-24 07:00:39 UTC

```
{"type": "text", "file": {"filePath": "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/lexicon.json", "content": "{\n \"n_entries\": 652,\n \"n_usable_not_wrong\": 652,\n \"audit_counts\": {\n  \"PENDING\": 652\n },\n \"groups\": {\n  \"event\": {\n   \"n_sortal\": 8,\n   \"n_nonsortal\": 14,\n   \"n_rules_nonsortal\": 6,\n   \"usable\": true\n  },\n  \"person\": {\n   \"n_sortal\": 57,\n   \"n_nonsortal\": 123,\n   \"n_rules_nonsortal\": 79,\n   \"usable\": true\n  },\n  \"object\": {\n   \"n_sortal\": 125,\n   \"n_nonsortal\": 225,\n   \"n_rules_nonsortal\": 97,\n   \"usable\": true\n  },\n  \"animal\": {\n   \"n_sortal\": 24,\n   \"n_nonsortal\": 21,\n   \"n_rules_nonsortal\": 13,\n   \"usable\": true\n  },\n  \"other\": {\n   \"n_sortal\": 13,\n   \"n_nonsortal\": 18,\n   \"n_rules_nonsortal\": 11,\n   \"usable\": true\n  },\n  \"organisation\": {\n   \"n_sortal\": 4,\n   \"n_nonsortal\": 7,\n   \"n_rules_nonsortal\": 3,\n   \"usable\": false\n  },\n  \"place\": {\n   \"n_sortal\": 7,\n   \"n_nonsortal\": 6,\n   \"n_rules_nonsortal\": 3,\n   \"usable\": false\n  }\n },\n \"log\": {\n  \"audit_pending\": 762,\n  \"dup_atom_vp\": 110,\n  \"renamed\": 6\n },\n \"entries\": [\n  {\n   \"lexicon_id\": \"15f52d64e3\",\n   \"atom_final\": \"Surprise(x)\",\n   \"pred_final\": \"Surprise\",", "numLines": 60, "startLine": 1, "totalLines": 14402}}
```

### [19] TOOL CALL — Read · 2026-09-24 07:00:39 UTC

```
/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/testability_FREE.json
```

### [20] TOOL RESULT — Read · 2026-09-24 07:00:39 UTC

```
{"type": "text", "file": {"filePath": "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/testability_FREE.json", "content": "{\n \"condition\": \"FREE\",\n \"utc\": \"2026-09-24T04:28:42Z\",\n \"primary_pool_rule\": \"tiers A+B, CORRECT/ERROR, excluding CONTESTED, reading_choice, REF_FLAGGED, UNRESOLVED; all FREE candidate rows (few-shot + zero-shot); the few-shot-only pool is reported alongside\",\n \"word_terciles\": {\n  \"cut_1\": 30,\n  \"cut_2\": 35,\n  \"rule\": \"T1: words < cut_1; T2: cut_1 <= words < cut_2; T3: words >= cut_2 (main sentences)\"\n },\n \"n_CORRECT\": 34,\n \"n_ERROR\": 420,\n \"sentences_with_CORRECT\": 15,\n \"sentences_with_ERROR\": 158,\n \"n_sentences_in_pool\": 159,\n \"label_counts_all_rows\": {\n  \"UNRESOLVED\": 1811,\n  \"ERROR\": 420,\n  \"UNPARSEABLE\": 188,\n  \"CORRECT\": 34,\n  \"NO_OUTPUT\": 199\n },\n \"per_template_counts\": {\n  \"T1\": {\n   \"ERROR\": 64,\n   \"CORRECT\": 7\n  },\n  \"T2\": {\n   \"ERROR\": 48,\n   \"CORRECT\": 4\n  },\n  \"T3\": {\n   \"ERROR\": 42\n  },\n  \"T4\": {\n   \"ERROR\": 31,\n   \"CORRECT\": 4\n  },\n  \"T5\": {\n   \"ERROR\": 52,\n   \"CORRECT\": 2\n  },\n  \"T6\": {\n   \"ERROR\": 34,\n   \"CORRECT\": 11\n  },\n  \"T7\": {\n   \"ERROR\": 54\n  },\n  \"T8\": {\n   \"ERROR\": 57,\n   \"CORRECT\": 2\n  },\n  \"T9\": {\n   \"ERROR\": 38,\n   \"CORRECT\": 4\n  }\n },\n \"strata\": {\n  \"word_tercile\": {\n   \"W1\": {\n    \"CORRECT\": 22,\n    \"ERROR\": 157,\n    \"reportable_30_30\": false\n   },\n   \"W2\": {\n    \"CORRECT\": 9,\n    \"ERROR\": 144,\n    \"reportable_30_30\": false\n   },\n   \"W3\": {\n    \"CORRECT\": 3,\n    \"ERROR\": 119,\n    \"reportable_30_30\": false\n   }\n  },\n  \"clause_type\": {\n   \"as_long_as+unless\": {\n    \"CORRECT\": 4,\n    \"ERROR\": 31,\n    \"reportable_30_30\": false\n   },\n   \"but_only_if\": {\n    \"CORRECT\": 2,\n    \"ERROR\": 57,\n    \"reportable_30_30\": false\n   },\n   \"except_when\": {\n    \"CORRECT\": 4,\n    \"ERROR\": 48,\n    \"reportable_30_30\": false\n   },\n   \"except_when+provided_that\": {\n    \"CORRECT\": 11,\n    \"ERROR\": 34,\n    \"reportable_30_30\": false\n   },\n   \"provided_that\": {\n    \"CORRECT\": 0,\n    \"ERROR\": 42,\n    \"reportable_30_30\": false\n   },\n   \"provided_that+unless\": {\n    \"CORRECT\": 2,\n    \"ERROR\": 52,\n    \"reportable_30_30\": false\n   },\n   \"unless\": {\n    \"CORRECT\": 11,\n    \"ERROR\": 156,\n    \"reportable_30_30\": false\n   }\n  },\n  \"template_id\": {\n   \"T1\": {\n    \"CORRECT\": 7,\n    \"ERROR\": 64,\n    \"reportable_30_30\": false\n   },\n   \"T2\": {\n    \"CORRECT\": 4,\n    \"ERROR\": 48,\n    \"reportable_30_30\": false\n   },\n   \"T3\": {\n    \"CORRECT\": 0,\n    \"ERROR\": 42,\n    \"reportable_30_30\": false\n   },\n   \"T4\": {\n    \"CORRECT\": 4,\n    \"ERROR\": 31,\n    \"reportable_30_30\": false\n   },\n   \"T5\": {\n    \"CORRECT\": 2,\n    \"ERROR\": 52,\n    \"reportable_30_30\": false\n   },\n   \"T6\": {\n    \"CORRECT\": 11,\n    \"ERROR\": 34,\n    \"reportable_30_30\": false\n   },\n   \"T7\": {\n    \"CORRECT\": 0,\n    \"ERROR\": 54,\n    \"reportable_30_30\": false\n   },\n   \"T8\": {\n    \"CORRECT\": 2,\n    \"ERROR\": 57,\n    \"reportable_30_30\": false\n   },\n   \"T9\": {\n    \"CORRECT\": 4,\n    \"ERROR\": 38,\n    \"reportable_30_30\": false\n   }\n  },\n  \"nconds_weak\": {\n   \"4\": {\n    \"CORRECT\": 0,\n    \"ERROR\": 54,\n    \"reportable_30_30\": false\n   },\n   \"5\": {\n    \"CORRECT\": 34,\n    \"ERROR\": 366,\n    \"reportable_30_30\": true\n   }\n  }\n },\n \"sha256_label_vector\": \"97997ea4964509459eaabc1dac4496f8eddd28551e9440365481d6511a06d2c2\",\n \"verdict\": \"NOT_TESTABLE\",\n \"few_shot_only\": {\n  \"n_CORRECT\": 29,\n  \"n_ERROR\": 358,\n  \"sentences_with_CORRECT\": 14,\n  \"sentences_with_ERROR\": 142,\n  \"n_sentences_in_pool\": 144,\n  \"label_counts_all_rows\": {\n   \"UNRESOLVED\": 1646,\n   \"ERROR\": 358,\n   \"UNPARSEABLE\": 177,\n   \"CORRECT\": 29\n  },\n  \"per_template_counts\": {\n   \"T1\": {\n    \"ERROR\": 55,\n    \"CORRECT\": 6\n   },\n   \"T2\": {\n    \"ERROR\": 39,\n    \"CORRECT\": 4\n   },\n   \"T3\": {\n    \"ERROR\": 32\n   },\n   \"T4\": {\n    \"ERROR\": 28,\n    \"CORRECT\": 3\n   },\n   \"T5\": {\n    \"ERROR\": 47,\n    \"CORRECT\": 1\n   },\n   \"T6\": {\n    \"ERROR\": 28,\n    \"CORRECT\": 9\n   },\n   \"T7\": {\n    \"ERROR\": 45\n   },\n   \"T8\": {\n    \"ERROR\": 48,\n    \"CORRECT\": 2\n   },\n   \"T9\": {\n    \"ERROR\": 36,\n    \"CORRECT\": 4\n   }\n  },\n  \"sha256_label_vector\": \"009f6e318348d496ce2b2c2a83d83237b303e8224902daaed1927c9c78cf9256\",\n  \"verdict\": \"NOT_TESTABLE\"\n },\n \"tier_A_only\": {\n  \"n_CORRECT\": 34,\n  \"n_ERROR\": 420,\n  \"sentences_with_CORRECT\": 15,\n  \"sentences_with_ERROR\": 158,\n  \"n_sentences_in_pool\": 159,\n  \"label_counts_all_rows\": {\n   \"UNRESOLVED\": 1811,\n   \"ERROR\": 420,\n   \"UNPARSEABLE\": 188,\n   \"CORRECT\": 34,\n   \"NO_OUTPUT\": 199\n  },\n  \"per_template_counts\": {\n   \"T1\": {\n    \"ERROR\": 64,\n    \"CORRECT\": 7\n   },\n   \"T2\": {\n    \"ERROR\": 48,\n    \"CORRECT\": 4\n   },\n   \"T3\": {\n    \"ERROR\": 42\n   },\n   \"T4\": {\n    \"ERROR\": 31,\n    \"CORRECT\": 4\n   },\n   \"T5\": {\n    \"ERROR\": 52,\n    \"CORRECT\": 2\n   },\n   \"T6\": {\n    \"ERROR\": 34,\n    \"CORRECT\": 11\n   },\n   \"T7\": {\n    \"ERROR\": 54\n   },\n   \"T8\": {\n    \"ERROR\": 57,\n    \"CORRECT\": 2\n   },\n   \"T9\": {\n    \"ERROR\": 38,\n    \"CORRECT\": 4\n   }\n  },\n  \"sha256_label_vector\": \"97997ea4964509459eaabc1dac4496f8eddd28551e9440365481d6511a06d2c2\",\n  \"verdict\": \"NOT_TESTABLE\"\n },\n \"tier_counts\": {\n  \"UNRESOLVED:none\": 1811,\n  \"ERROR:A\": 420,\n  \"UNPARSEABLE:-\": 188,\n  \"CORRECT:A\": 34,\n  \"NO_OUTPUT:-\": 199\n }\n}", "numLines": 285, "startLine": 1, "totalLines": 285}}
```

### [21] TOOL CALL — Glob · 2026-09-24 07:00:47 UTC

```
Pattern: "rcomp/**/*.jsonl"
```

### [22] TOOL RESULT — Glob · 2026-09-24 07:00:47 UTC

```
{"filenames": ["/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/rcomp/data_local/DSAVlab-UNIUD_FOLIO_validation-curated__FOLIO_instances.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/rcomp/data_local/DSAVlab-UNIUD_MALLS_test_subset-CURATED__MALLS_instances.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/rcomp/raw/lexicon_extract.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/rcomp/work/label_pair_cache_dryrun.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/rcomp/raw/fluency.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/rcomp/raw/fluency_items.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/rcomp/raw/generations_sig.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/rcomp/cost_ledger.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/rcomp/raw/generations.jsonl", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/rcomp/work/label_pair_cache.jsonl"], "durationMs": 597, "numFiles": 10, "truncated": false, "totalMatches": 10, "countIsComplete": true}
```

### [23] TOOL CALL — Grep · 2026-09-24 07:00:47 UTC

```
Pattern: ""lexicon_id": "15f52d64e3""
```

### [24] TOOL RESULT — Grep · 2026-09-24 07:00:47 UTC

```
{"mode": "content", "numFiles": 0, "filenames": [], "content": "58:   \"lexicon_id\": \"15f52d64e3\",\n59-   \"atom_final\": \"Surprise(x)\",\n60-   \"pred_final\": \"Surprise\",\n61-   \"pred\": \"Surprise\",\n62-   \"arity\": 1,\n63-   \"const\": null,\n64-   \"const_pos\": null,\n65-   \"vp_sg_pos\": \"is a surprise\",\n66-   \"vp_sg_neg\": \"is not a surprise\",\n67-   \"noun\": \"surprise\",\n68-   \"sortal\": true,\n69-   \"subject_sort\": \"event\",\n70-   \"role\": \"consequent\",\n71-   \"rule_id\": \"b_0f3e9b2f7a\",\n72-   \"source\": \"FOLIO-v2-train_agreed\",\n73-   \"source_text\": \"All scares are surprises.\",\n74-   \"source_fol\": \"∀x (Scare(x) → Surprise(x))\",\n75-   \"atom\": \"Surprise(x)\",\n76-   \"audit\": \"PENDING\",\n77-   \"audit_reason\": null\n78-  },\n79-  {\n80-   \"lexicon_id\": \"0812dde76d\",\n81-   \"atom_final\": \"Student(x)\",\n82-   \"pred_final\": \"Student\",\n83-   \"pred\": \"Student\",\n84-   \"arity\": 1,\n85-   \"const\": null,\n86-   \"const_pos\": null,\n87-   \"vp_sg_pos\": \"is a student\",\n88-   \"vp_sg_neg\": \"is not a student\",", "numLines": 31, "totalLines": 31}
```

### [25] TOOL CALL — Read · 2026-09-24 07:00:53 UTC

```
/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/rcomp/raw/generations.jsonl
```

### [26] TOOL RESULT — Read · 2026-09-24 07:00:53 UTC

```
{"type": "text", "file": {"filePath": "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/rcomp/raw/generations.jsonl", "content": "{\"sentence_id\": \"001a7f0caf5a\", \"slot\": \"G1\", \"system\": \"G1:meta-llama/llama-3.1-8b-instruct\", \"model\": \"meta-llama/llama-3.1-8b-instruct\", \"family\": \"meta\", \"prompt_variant\": \"fewshot_v1\", \"prompt_sha1\": \"a1c7ae39f13979a96e6b360f8d3164735c334d80\", \"raw_output\": \"FOL: ∀x ((Legislator(x) ∧ At(x, boardGameNight) ∧ RegularlyVisits(x, coffeeShop) ∧ CanDistinguish(x, differentCondiments)) → (Friend(x, emily) ∧ ¬ElectedOfficial(x)))\", \"candidate_fol\": \"∀x ((Legislator(x) ∧ At(x, boardGameNight) ∧ RegularlyVisits(x, coffeeShop) ∧ CanDistinguish(x, differentCondiments)) → (Friend(x, emily) ∧ ¬ElectedOfficial(x)))\", \"normalisation_applied\": [\"fol_prefix\"], \"parse_ok\": true, \"parse_error\": \"\", \"provider\": \"Novita\", \"model_returned\": \"meta-llama/llama-3.1-8b-instruct\", \"finish_reason\": \"stop\", \"cost_usd\": 1.245e-05, \"usage\": {\"prompt_tokens\": 485, \"completion_tokens\": 55, \"total_tokens\": 540, \"cost\": 1.245e-05, \"is_byok\": false, \"prompt_tokens_details\": {\"cached_tokens\": 0, \"cache_write_tokens\": 0, \"audio_tokens\": 0, \"video_tokens\": 0}, \"cost_details\": {\"upstream_inference_cost\": 1.245e-05, \"upstream_inference_prompt_cost\": 9.7e-06, \"upstream_inference_completions_cost\": 2.75e-06}, \"completion_tokens_details\": {\"reasoning_tokens\": 0, \"image_tokens\": 0, \"audio_tokens\": 0}}, \"api_error\": \"\", \"final_failure\": false}", "numLines": 1, "startLine": 1, "totalLines": 2852}}
```

### [27] TOOL CALL — Grep · 2026-09-24 07:00:53 UTC

```
Pattern: ""sentence_id""
```

### [28] TOOL RESULT — Grep · 2026-09-24 07:00:53 UTC

```
{"mode": "count", "numFiles": 1, "filenames": [], "content": "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/rcomp/work/rcomp_sentences.json:314", "numMatches": 314}
```

### [29] ASSISTANT · 2026-09-24 07:01:01 UTC

```
Checking one sentence record's fields so the plan uses the right field names, then I'll write the plan.
```

### [30] TOOL CALL — Grep · 2026-09-24 07:01:01 UTC

```
Pattern: ""sentence_id": "001a7f0caf5a""
```

### [31] TOOL RESULT — Grep · 2026-09-24 07:01:01 UTC

```
{"mode": "content", "numFiles": 0, "filenames": [], "content": "728-   \"ElectedOfficial/1\": \"NONMONO\"\n729-  },\n730-  \"vacuous\": false,\n731:  \"sentence_id\": \"001a7f0caf5a\",\n732-  \"words\": 34,\n733-  \"word_bin\": \"30-34\",\n734-  \"exception_type\": \"except\",\n735-  \"text_conditions\": 4,\n736-  \"preselect_pool\": \"main\",\n737-  \"fluency\": 5,\n738-  \"fluency_status\": \"RATED\",\n739-  \"audit_status\": \"PENDING\",\n740-  \"ref_flagged\": false,\n741-  \"audit_verdicts\": null,\n742-  \"topup_batch\": false,\n743-  \"batch\": \"main\"\n744- },\n745- {\n746-  \"text\": \"When an invertebrate does not produce milk to nourish its offspring and can read, and the invertebrate also is in Antarctica, the invertebrate sleeps, except when the invertebrate is a warm-blooded vertebrate.\",\n747-  \"reference_fol_weak\": \"∀x (Invertebrate(x) ∧ ¬ProducesMilk(x) ∧ CanRead(x) ∧ In(x, antarctica) ∧ ¬WarmBloodedVertebrate(x) → Sleep(x))\",\n748-  \"reference_fol_strong\": \"∀x (Invertebrate(x) ∧ ¬ProducesMilk(x) ∧ CanRead(x) ∧ In(x, antarctica) → (Sleep(x) ↔ ¬WarmBloodedVertebrate(x)))\",\n749-  \"reading_converse\": null,\n750-  \"template_id\": \"T2\",\n751-  \"surface_variant\": \"T2v1\",\n752-  \"clause_type\": \"except_when\",\n753-  \"nested\": false,\n754-  \"sort_group\": \"animal\",\n755-  \"sentence_seed\": \"4a88748fa4733a9bba51dfd600d749782d6ba110\",\n756-  \"compose_index\": 166,\n757-  \"noun_lexicon_id\": \"10fafbc5cc\",\n758-  \"condition_lexicon_ids\": [\n759-   \"b8324ea2cd\",\n760-   \"308c77d553\",\n761-   \"1394341682\"\n762-  ],\n763-  \"negated_condition\": 0,\n764-  \"Q_lexicon_id\": \"7e1036f659\",\n765-  \"E_lexicon_id\": \"1418c64fcd\",\n766-  \"lexicon_ids\": [\n767-   \"10fafbc5cc\",\n768-   \"b8324ea2cd\",\n769-   \"308c77d553\",\n770-   \"1394341682\",\n771-   \"7e1036f659\",\n772-   \"1418c64fcd\"\n773-  ],\n774-  \"source_rule_ids\": [\n775-   \"a_4bdf354934\",\n776-   \"a_b290b2cc97\",", "numLines": 49, "totalLines": 49}
```

### [32] TOOL CALL — Grep · 2026-09-24 07:01:01 UTC

```
Pattern: "def signature_symbols|def signature_block|lexicon"
```

### [33] TOOL RESULT — Grep · 2026-09-24 07:01:01 UTC

```
{"mode": "content", "numFiles": 0, "filenames": [], "content": "5:lexicon entry whose pred_final equals the predicate (its positive verb phrase `vp_sg_pos`) and a verbatim example atom.\n6-Lines are sorted alphabetically by predicate name (never template order), so the role of an atom (condition,\n7-consequent, exception, proviso) is not leaked; the block contains no wording about exceptions or readings.\n8-The few-shot system message and exemplars are byte-identical to prompts/fewshot_v1.txt; the block is appended to the\n9-final user message only (exemplars keep their own vocabulary; disclosed).\n10-\"\"\"\n11-from __future__ import annotations\n12-\n13-import hashlib\n14-import json\n15-import sys\n16-from pathlib import Path\n17-\n--\n34:def load_lexicon() -> dict:\n35:    return {e[\"lexicon_id\"]: e for e in json.loads((RC / \"lexicon.json\").read_text())[\"entries\"]}\n36-\n37-\n38-def reference_signature(sent: dict) -> tuple[dict, set, dict]:\n39-    \"\"\"-> ({(pred, arity): example_atom_string}, {constants}, {pred: first atom args}) over every stored reading.\"\"\"\n40-    preds, consts = {}, set()\n41-    for key in (\"reference_fol_weak\", \"reference_fol_strong\", \"reading_converse\"):\n42-        f = sent.get(key)\n43-        if not f:\n44-            continue\n45-        e = parse(f)\n46-        bv = bound_vars(e)\n47-        for a in atoms(e):\n--\n65:    for lid in sent[\"lexicon_ids\"]:\n66-        e = lex.get(lid)\n67-        if e is not None:\n68-            gloss[e[\"pred_final\"]] = e[\"vp_sg_pos\"]\n69-    lines = []\n70-    for (name, ar), atom in sorted(preds.items(), key=lambda kv: (kv[0][0].lower(), kv[0][0], kv[0][1])):\n71-        g = gloss.get(name)\n72-        if g is None:\n73:            raise KeyError(f\"no lexicon gloss for predicate {name} in sentence {sent['sentence_id']}\")\n74-        lines.append(f\"{name}/{ar}: {g}  e.g. {_example(atom)}\")\n75-    block = HEADER + \"\\n\" + \"\\n\".join(lines)\n76-    if consts:\n77-        block += \"\\nConstants: \" + \", \".join(sorted(consts, key=lambda c: (c.lower(), c)))\n78-    return block\n79-\n80-\n81-def sig_messages(sent: dict, prompt: dict, lex: dict) -> list[dict]:\n82-    user = prompt[\"user_template\"].format(sentence=sent[\"text\"]) + \"\\n\\n\" + build_signature_block(sent, lex)\n83-    return [{\"role\": \"system\", \"content\": prompt[\"system\"]}] + prompt[\"exemplars\"] + [{\"role\": \"user\", \"content\": user}]\n84-\n85-\n--\n91:def signature_symbols(sent: dict) -> tuple[dict, set]:\n92-    \"\"\"{pred_name: arity} (names unique per sentence by construction) and the constant set.\"\"\"\n93-    preds, consts, _ = reference_signature(sent)\n94-    out = {}\n95-    for (n, a) in preds:\n96-        if n in out and out[n] != a:\n97-            raise ValueError(f\"arity clash for {n} in {sent['sentence_id']}\")\n98-        out[n] = a\n99-    return out, consts", "numLines": 60, "totalLines": 60}
```

### [34] ASSISTANT · 2026-09-24 07:02:51 UTC

```
Writing the plan now; one last check on how FREE row keys are built so iteration 5 can join on them.
```

### [35] TOOL CALL — Grep · 2026-09-24 07:02:51 UTC

```
Pattern: "FREE\|"
```

### [36] TOOL RESULT — Grep · 2026-09-24 07:02:51 UTC

```
{"mode": "content", "numFiles": 0, "filenames": [], "content": "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/panel_rcomp.py:293:        out.append({\"row_key\": f\"{r['item_id']}|FREE|{r['slot']}|{r['prompt_variant']}\", \"item_id\": r[\"item_id\"], \"sentence_id\": sid,", "numLines": 1, "totalLines": 1}
```

### [37] TOOL CALL — Grep · 2026-09-24 07:02:51 UTC

```
Pattern: "def (formula_role_profile|evaluate|finite|fingerprint|equivalent)\b"
```

### [38] TOOL RESULT — Grep · 2026-09-24 07:02:53 UTC

```
{"mode": "content", "numFiles": 0, "filenames": [], "content": "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/labeller/fol.py:173:def equivalent(e1, e2, ms=5000):\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3/src/fol.py:170:def equivalent(e1, e2, ms=5000):\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3/src/analysis.py:107:def evaluate(df: pd.DataFrame, score: str, B: int, boots=None, thr_flag: str | None = None) -> dict:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/src/vendor_a/fol_triage.py:109:def formula_role_profile(fol, ms: int = 3000, mono: dict | None = None) -> dict:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/src/vendor_a/fol.py:170:def equivalent(e1, e2, ms=5000):\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/src/vendor_c/analysis.py:107:def evaluate(df: pd.DataFrame, score: str, B: int, boots=None, thr_flag: str | None = None) -> dict:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/src/vendor_c/fol.py:170:def equivalent(e1, e2, ms=5000):\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/src/vendor_d/labeller/fol.py:168:def equivalent(e1, e2, ms=5000):\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/src/analyse_E.py:125:def evaluate(rows: list[dict], metrics: list[str], y_key: str = \"y\", pairs: list[tuple] = (), b: int = B) -> dict:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/src/fol.py:170:def equivalent(e1, e2, ms=5000):\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/inputs_copy/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/src/fol_triage.py:109:def formula_role_profile(fol, ms: int = 3000, mono: dict | None = None) -> dict:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/inputs_copy/3_invention_loop/iter_1/gen_art/gen_art_experiment_3/src/analysis.py:107:def evaluate(df: pd.DataFrame, score: str, B: int, boots=None, thr_flag: str | None = None) -> dict:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/src/vendor_e/fol.py:173:def equivalent(e1, e2, ms=5000):\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/src/vendor_a/fol_triage.py:109:def formula_role_profile(fol, ms: int = 3000, mono: dict | None = None) -> dict:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/src/vendor_a/fol.py:170:def equivalent(e1, e2, ms=5000):", "numLines": 15, "totalLines": 44, "appliedLimit": 15}
```

### [39] TOOL CALL — Write · 2026-09-24 07:05:19 UTC

```
File: /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_plan/gen_plan_dataset_2/.terminal_claude_agent_struct_out.json

{
  "title": "Name-free labels for free-vocabulary rule translations",
  "summary": "T7b. Build the labels that make the in-scope FREE condition of R_COMP testable, with no instrument shared with any consensus metric or judge. For each FREE candidate (exp 7 rcomp/raw/generations.jsonl, the 10 slots x few-shot/zero-shot over 221 main templated sentences), an exhaustive, sound-pruned search over arity-consistent injective symbol maps (plus five declared bridges: reification both ways, merge, conjunctive split, lexical-negation) looks for a map under which the candidate is z3-equivalent to the template's weak or strong reading. No map gives ERROR_CERT. Every rejected map carries a certificate: a finite countermodel or z3 SAT. Rows equivalent only to the T8 converse are READING_CHOICE. If maps exist, a gated two-family LLM gloss check (anthropic/claude-haiku-4.5 + qwen/qwen3-235b-a22b-2507, both family-disjoint from the CSC peers and the judges) rules on the meaning of every mapped atom: CORRECT when both checkers accept every pair of some equivalent map, ERROR_GLOSS when both reject at least one pair of every equivalent map, UNRESOLVED otherwise. Everything is pre-registered and hashed before the first label: map family, bridges, prunes, caps, gloss prompt, gate, label rules and testability rule. The gate is 6 classes x >=100 pair items with known answers. Soundness is audited three ways: (i) a SIG replay under nonce and synonym renames (known z3 labels), (ii) a stronger-model audit of 60 ERROR_CERT and 60 CORRECT rows, (iii) agreement with the old tier-A labels, joined only after the seal. Testability is declared on all FREE rows and on the untouched subset (not tier-A-labelled in iteration 3), which is primary for iteration 5. Output: exp_sel_data_out with three groups (FREE labels, gloss-gate items, SIG soundness replay), plus a seal, audits, a dataset card and the reusable functions exhaustive_map_label / equivalent_modulo_vocab_exhaustive with tests. Expected spend is about $2.5-3.2 (hard stop $3.8, cap $4). CPU only.",
  "runpod_compute_profile": "cpu_plus",
  "target_num_datasets": 3,
  "ideal_dataset_criteria": "One labelled meta-evaluation table plus two validation tables, all derived from the run's own R_COMP data. No new third-party download is needed: R_COMP's references are true by construction, and its FREE candidates are real outputs of 10 LLM slots across 9 families. The one kind of label missing for the user's operating regime (no controlled vocabulary) is exactly what this artifact adds.\n\nGROUP 1 rcomp_free_labels. One row per FREE generation record: every slot, both prompt variants (fewshot_v1 and zero-shot), and the NO_OUTPUT and UNPARSEABLE rows too, so coverage keeps every failure in the denominator.\n- input = JSON string {text, candidate_fol, system, family, slot, prompt_variant, condition:'FREE', template_id}.\n- output is one of CORRECT / ERROR_CERT / ERROR_GLOSS / READING_CHOICE / UNRESOLVED_GLOSS / UNRESOLVED_SEARCH_CAP / UNRESOLVED_Z3_UNKNOWN / UNPARSEABLE / NO_OUTPUT.\n- metadata_label_binary: ERROR when output is ERROR_CERT or ERROR_GLOSS, CORRECT when it is CORRECT, EXCLUDED otherwise.\n- metadata fields:\n  - row_key, using exp 7's recipe item_id|FREE|slot|prompt_variant, with item_id = sha1(system|norm(text)|raw_output)[:16];\n  - sentence_id (the bootstrap cluster), template_id, clause_type, words, word_tercile (cuts 30/35 as in testability_FREE.json), nconds_weak, negated_condition, nested;\n  - label_source ('exhaustive_map_v1' or 'exhaustive_map_v1+gloss_v1');\n  - matched_reading (weak / strong / both);\n  - map_certificate: the winning map as {cand_symbol -> template_atom | bridge spec} plus bridges used;\n  - n_maps_enumerated, n_maps_fingerprint_pass, n_equiv_maps, n_equiv_map_orbits;\n  - nonequiv_certificate_type counts (countermodel / z3_sat);\n  - gloss_pairs [{cand_atom, template_atom, gloss, haiku, qwen}] and gloss_decision;\n  - unresolved_reason;\n  - irrelevant_symbols (semantically inert candidate symbols);\n  - search_secs;\n  - seen_iter3 (joined after the seal) and old_label_iter3 (joined after the seal, agreement table only);\n  - metadata_fold 'RCOMP_FREE'.\n\nGROUP 2 gloss_gate_items. At least 100 pair items per class in 6 known-answer classes, split into halves A and B by sentence hash:\n- YES_IDENT: the template name, _k suffix stripped;\n- YES_SYN: a WordNet synonym rename of the head token, from dataset 3's RENAME_SYN generator;\n- YES_FORM: a meaning-preserving name form, i.e. a reified or de-reified atom, a lexical-negation name such as NotElectedOfficial for ¬ElectedOfficial, or a modifier-dropping abbreviation;\n- NO_NONCE: a nonce name;\n- NO_DONOR: a non-synonymous donor predicate from another lexicon entry in the same sort group, from dataset 3's MEANING_RENAME donors;\n- NO_ROLE: an argument-role swap of a directional binary atom, or a positive name offered for a negated gloss.\nFields: input = {sentence, candidate_atom, proposed_meaning}; output = YES or NO; metadata = class, half, each checker's verdict, prompt_version.\n\nGROUP 3 sig_soundness_replay. The 1,904 SIG rows with their pure-z3 labels, each re-expressed under two renamings: all symbols consistently renamed to nonce tokens, and all symbols renamed to WordNet synonyms.\n- output = the known SIG label.\n- metadata = the new map-search outcome (map_equiv_found, identity_or_other_map, n_equiv_orbits). For the 300-row stratified gloss subsample, also the end-to-end label.\n\nQUALITY BARS.\n- Every CORRECT is backed by an explicit map certificate that re-verifies under z3 at write time.\n- Every ERROR_CERT is backed by a per-map non-equivalence certificate (countermodel or z3 SAT), and no map returned z3 UNKNOWN.\n- Labels are sealed by sha256 before any old label, consensus score or judge score is joined.\n- The whole file stays under the 300 MB limit (expected < 40 MB); if full_data_out.json exceeds the limit, split it with aii-file-size-limit.",
  "dataset_search_plan": "No external search is needed; the sources are this run's own artifacts, read-only. Work in STRICT ORDER. Track spend after EVERY OpenRouter call in cost_ledger.jsonl; the hard stop is $3.8.\n\nSTEP A. INPUTS AND FIREWALL (30 min)\n1. Vendor the needed code by COPYING it into ./vendor/, recording sha256 in VENDOR_SHA256.json:\n   - parse and equivalent: dataset 3 labeller/fol.py (/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/labeller/fol.py);\n   - atoms and bound_vars: labeller/repair_census.py;\n   - templates.py and verify.py from dataset 3 src/;\n   - formula_role_profile for per-predicate monotonicity: iter_2/gen_art/gen_art_experiment_5/src/vendor_a/fol_triage.py;\n   - the RENAME_SYN / RENAME_NONCE / MEANING_RENAME generators: dataset 3 src/perturb.py;\n   - reference_signature / signature_symbols: exp 7 src/sig_prompt.py.\n   Do NOT import or copy consensus_lib.py, peer_text.py, consensus_rcomp.py, the eqmv aligner, repair_census's alignment helpers or anything name-similarity based. Add a unit test that greps ./src and ./vendor for 'equivalent_modulo_vocab(' (the aligner), 'c_score', 'judge' and 'difflib', and fails if found.\n2. Sentences: /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/rcomp/work/rcomp_sentences.json (314 records = 250 main + reserve).\n   - Fields used: sentence_id, text, reference_fol_weak, reference_fol_strong, reading_converse (T8 only), template_id, clause_type, lexicon_ids, condition_lexicon_ids, Q/E/P lexicon ids, words.\n   - Keep only the sentences present in exp 7's FREE generations (221 after the fluency drop). Cross-check against dataset 3 full_data_out.json group rcomp_sentences.\n3. Glosses: dataset 3 lexicon.json entries (652), keyed by lexicon_id. Gloss = 'x ' + vp_sg_pos; the negative form is vp_sg_neg; constants come from the const field. Build a per-sentence map template_atom -> English gloss the way sig_prompt.build_signature_block does. Note that template names can carry _2 disambiguation suffixes, e.g. EmilysFriend_2, so the gloss comes from the lexicon and NEVER from the name.\n4. Candidates: read ONLY exp 7 rcomp/raw/generations.jsonl (FREE raw generations). This file has NO scores or labels.\n   - Keep the last record per (sentence_id, slot, prompt_variant), as in label_sig.load_sig_rows.\n   - raw_output None -> NO_OUTPUT; parse_ok False, or a failure of our parser -> UNPARSEABLE.\n   - Recompute item_id and row_key with exp 7's recipe (panel_rcomp.py line 293).\n   - Reconcile counts and log them. The hypothesis says 2,024 FREE rows; exp 7's testability_FREE.json label_counts sums to 2,652 incl. 199 NO_OUTPUT and 188 UNPARSEABLE; the actual count is whatever this file yields. Write the count table to results/input_counts.json.\n   - Do NOT open results/rcomp_candidates.jsonl, free_labels.jsonl, scores_FREE*.jsonl or judge_*.jsonl until STEP H.\n5. SIG rows (for the gate and audit (i)): exp 7 results/sig_labels.jsonl. It holds labels only, no scores, so it is allowed. Use the fields row_key, sentence_id, candidate_fol, label, matched_reading, sig_status.\n6. LABEL-FREE SHAPE CENSUS on a 100-row random FREE sample (seed 0). Record symbol counts, arity profiles, constant usage, and whether patterns occur such as unary-vs-binary-with-constant, Not-prefixed names, ∃y(N(y) ∧ R(x,y)) in place of a constant, and compound names that concatenate two template concepts. This looks only at inputs, never at labels or scores, so it is legitimate before the freeze. It decides whether the declared bridge set covers the common forms. Log it in results/shape_census.json.\n   - If the ∃-for-constant pattern appears in >=5% of rows, declare an optional bridge F (existential-constant: ∃y(N(y) ∧ R(x,y)) treated as R(x,c) when N glosses the constant) in the prereg.\n   - Otherwise list it as a known out-of-family form that audit (ii) quantifies.\n\nSTEP B. PRE-REGISTRATION (before ANY map-search output on FREE rows)\nWrite prereg_freelab.json and store its sha256 in prereg_freelab.sha256. It contains:\n(a) MAP FAMILY. Maps are injective and arity-consistent. Candidate predicates map to template predicates. Binary predicates may use either argument order. Candidate constants map injectively to template constants or stay free. An unmapped candidate symbol stays an uninterpreted fresh symbol.\n(b) BRIDGES:\n   - B1 reification: candidate unary P(x) := template R(x,c) for a template constant c.\n   - B2 de-reification: candidate binary P(x,k), with k a candidate constant that occurs only in that slot, := template unary U(x).\n   - B3 merge: candidate unary := A(x) ∧ B(x) for two template unaries that co-occur in one conjunction of a reference.\n   - B4 conjunctive split: two candidate unaries both := one template unary. Allowed only if the two candidate atoms occur ONLY as siblings in the same conjunction; checked syntactically.\n   - B5 lexical negation: candidate unary := ¬U(x). Allowed only if the candidate name's first CamelCase or underscore token matches ^(not|non|no|un|in|im|il|ir|dis|never|lacks?|without)$ or ^(Un|Non|In|Im|Dis)[A-Z].\n   - Optional B6 as decided in A6.\n   - At most 2 bridge uses per map.\n(c) SOUND PRUNES, so that the search is exhaustive over the family, not a sample:\n   - RELEVANCE: a symbol s is inert in F iff F ≡ F[s := fresh s'] (z3). Inert candidate symbols are recorded and dropped. Inert symbols cannot change meaning, and equivalent formulas have equal relevant-symbol sets.\n   - COUNT: #relevant candidate units after bridges = #relevant template atoms of the reading.\n   - POLARITY: per-predicate monotonicity (UP / DOWN / NONMONO / NONE from formula_role_profile, z3-exact) is a semantic invariant, so a candidate symbol may map only onto a template atom with the same polarity. Polarity flips under B5, and for merged or split units the polarity is computed after substitution.\n   - FINGERPRINT: evaluate candidate∘map and the reading on 128 random finite interpretations (domain sizes 2-3, seed fixed). A mismatch is a certified countermodel, i.e. non-equivalence. Only maps that agree on all 128 go to z3 equivalent(), with ms = 2000 and one retry at 10000 if the result is None.\n(d) CAPS: 2x10^5 maps enumerated or 90 s wall time per unique (sentence, candidate) class. Exceeding either gives UNRESOLVED_SEARCH_CAP. Any z3 UNKNOWN on a fingerprint-passing map, with no other map equivalent, gives UNRESOLVED_Z3_UNKNOWN.\n(e) LABEL RULES:\n   - If no map is equivalent to weak or strong, and on T8 no map is equivalent to the converse: ERROR_CERT.\n   - If maps are equivalent only to the T8 converse: READING_CHOICE.\n   - If maps are equivalent to weak or strong, the label follows the gloss rule (f).\n(f) GLOSS RULE. Collect the union of (candidate atom pattern, template atom or bridge meaning) pairs over ALL equivalent maps; symmetric conditions produce several equivalent maps, i.e. automorphism orbits. Each checker judges every pair independently (YES/NO).\n   - CORRECT iff some equivalent map has all of its pairs YES from BOTH checkers.\n   - ERROR_GLOSS iff every equivalent map contains at least one pair that is NO from BOTH checkers.\n   - Otherwise UNRESOLVED_GLOSS.\n(g) GLOSS PROMPT, verbatim, version gloss_v1. The system message says the task is lexical, not a judgement of the translation. The user message gives the sentence, then a shuffled numbered list of 'SYMBOL USE: <candidate atom as it appears, variables shown as x/y, constants shown> || PROPOSED MEANING: <x + template gloss, with the constant or negation spelled out>'. The question is: 'Could a careful translator plausibly have used this symbol use to express exactly this meaning in this sentence? Answer NO if the name means something different, broader or narrower in a way that changes truth conditions, opposite or negated, if the argument roles are reversed, or if the name is an arbitrary token whose meaning cannot be recognised.' The output is JSON {'1':'YES'|'NO',...}.\n   - temperature 0, max_tokens 300, at most 12 pairs per call.\n   - The checker never sees the whole candidate formula, the readings, any label, or which map was z3-equivalent.\n(h) GATE and TESTABILITY rules as in STEPS D and G.\n(i) AUDIT protocols as in STEP F.\nAfter the freeze, any change is logged in deviations.json with a timestamp.\n\nSTEP C. MAP SEARCH ON ALL FREE ROWS (CPU, about 1-2 h; $0)\n1. Deduplicate by (sentence_id, whitespace-normalised candidate_fol). Expect far fewer unique classes than rows.\n2. Run a ProcessPoolExecutor with the spawn context and workers = detected vCPUs (aii-use-hardware; 4 on cpu_plus). Each task is one sentence's unique classes, and a per-task timeout is enforced.\n3. Follow aii-long-running-tasks: run 10 classes, then 100, then all, extrapolating wall time at each step. Before the full run, unit-test the evaluator against z3 on 200 random formula pairs; the verdicts must agree 100% where z3 decides.\n4. Save results/map_search.jsonl, one line per class, with the certificate fields.\n5. Per-row time estimate: under the polarity and count prunes a typical weak reading has DOWN block {S, A1, A2, A3} and UP block {Q, E}. That is about 4! x 2! x (argument orders) x (bridge variants), i.e. hundreds of maps, so the cap should rarely bind. Report its hit rate.\n\nSTEP D. GLOSS GATE (about $0.3)\n1. Build the gate set from SIG sentences and the lexicon: 6 classes x >=100 items, stratified across templates and sort groups, split 50/50 into halves A and B by sha1(sentence_id).\n   - YES_FORM items are generated deterministically, e.g. EmilysFriend_2(x) -> Friend(x, emily); ¬ElectedOfficial -> NotElectedOfficial(x); Can(x, distinguishTheTasteOfDifferentCondiments) -> CanDistinguish(x, differentCondiments).\n   - Keep only NO_ROLE binary atoms whose relation is directional. Mark ambiguous ones, e.g. Friend, and exclude them from the gate.\n2. Run both checkers on half A with gloss_v1.\n3. PASS iff balanced accuracy >= 0.90 for Haiku, for Qwen AND for the both-YES conjunction, AND recall >= 0.85 for each of the YES and NO super-classes. Report per-class recall with Wilson CIs and Cohen's κ between the checkers.\n4. If it FAILS: make ONE prompt revision (gloss_v2) and re-freeze with a hash. Evaluate gloss_v2 on half B only, since half A was used to write it.\n5. If it still fails: skip STEP E-gloss. FREE labels are then ERROR_CERT / READING_CHOICE / UNRESOLVED_* only (every map-found row becomes UNRESOLVED_GLOSS_GATE_FAILED). Declare this in the card and in testability.\n\nSTEP E. GLOSS CHECK ON FREE (about $1.2-1.8)\n1. Only rows with >=1 equivalent map need calls. Cache pair verdicts by (sentence_id, cand_atom_pattern, template_atom_or_bridge), so identical pairs across slots share a verdict.\n2. Before the sweep, estimate cost as #unique pairs / 12 x per-call price (read live prices from the OpenRouter catalogue). Abort the sweep if the estimate exceeds $2.2; in that case, process untouched-subset rows first.\n3. Use asyncio with Semaphore(8), 3 retries with exponential backoff, and no retry loops on a 402. On a 402 or quota error, stop, write partial state and resume after the 00:00 UTC reset.\n4. Unparseable checker JSON: one re-ask, then treat the pair as NO_VERDICT, which makes it UNRESOLVED.\n5. Write results/gloss_verdicts.jsonl.\n\nSTEP F. SOUNDNESS AUDITS\n(i) SIG REPLAY ($0 search + about $0.3 gloss)\n   - For all 1,904 SIG rows, rename every symbol consistently to nonce tokens, then run the map search against the references.\n   - Report the ERROR_CERT false-error rate on SIG-CORRECT rows = share with no equivalent map. It must be <= 0.02 (pass bar >= 0.98 recovery).\n   - Report the rescue rate on SIG-ERROR rows = share where a NON-identity map is equivalent, e.g. swapped Q/E roles. These are exactly the rows the gloss check must stop.\n   - Repeat with WordNet-synonym renames. On a stratified 300 (150 CORRECT / 150 ERROR, stratified by template), run the full pipeline including the gloss check and report the end-to-end confusion matrix. Key numbers:\n     - false-CORRECT rate on known ERROR rows (must be <= 0.05);\n     - CORRECT recall on known CORRECT rows;\n     - UNRESOLVED share.\n(ii) STRONGER-MODEL AUDIT (about $1.0-1.5)\n   - Use the newest Anthropic Sonnet available on OpenRouter; check the catalogue and prefer anthropic/claude-sonnet-5, else anthropic/claude-sonnet-4.5.\n   - Draw 60 FREE ERROR_CERT rows stratified by template, plus 60 FREE CORRECT rows.\n   - The prompt shows the sentence, the candidate and the English meaning of each template atom (no formula readings, no label). It asks FAITHFUL / FAITHFUL_DIFFERENT_DECOMPOSITION / UNFAITHFUL / UNSURE, with a one-line reason.\n   - Report the implied ERROR_CERT precision = share not judged faithful, and the CORRECT precision, both with Wilson 95% CIs.\n   - The audit NEVER changes a label. Disagreement reasons are tallied into out-of-family forms, e.g. ∃-for-constant or an unbridged compound predicate.\n(iii) OLD-LABEL AGREEMENT: STEP H, after the seal.\n\nSTEP G. TESTABILITY and SEAL\n1. Write testability_FREE_v2.json with counts per template, per clause_type, per word tercile and per prompt_variant of CORRECT / ERROR (ERROR_CERT + ERROR_GLOSS) / each excluded class, and sentences with >=1 of each.\n2. Rule: TESTABLE iff >=50 ERROR and >=50 CORRECT spread over >=25 sentences (a sentence counts toward a class if it holds >=1 row of that class). Declare it on (1) all FREE rows and (2) the untouched subset. Also give descriptive 30/30 reportability per stratum.\n3. The per-stratum MDE for AUROC at the achieved n is about 0.10 at 50/50, per the hypothesis's power note; report it.\n4. seal.json holds sha256 over the sorted (row_key, label) vector for all rows and for the untouched subset, the prereg hash, the vendor hashes and the UTC time.\n\nSTEP H. POST-SEAL JOIN, the only step that opens exp 7's results/rcomp_candidates.jsonl\n1. Read that file with a whitelist JSON loader that keeps only row_key, label, label_tier and label_source, dropping every other key at parse time.\n2. Set seen_iter3 = old label in {CORRECT, ERROR} with tier A.\n3. Write soundness_audit.json (iii): a 2x2+ agreement table of old versus new labels with κ.\n4. Examine every disagreement by hand for 20 rows and classify it: old aligner over-acceptance, new bridge, gloss rejection, or the old label was UNRESOLVED.\n5. Verify that every new row_key exists in rcomp_candidates.jsonl, and report the mismatches.\n\nSTEP I. PACKAGE\n1. Write full_data_out.json in exp_sel_data_out format, with 3 groups (rcomp_free_labels, gloss_gate_items, sig_soundness_replay). Validate it with aii-json and make the mini/preview variants.\n2. Also write gate_report.json, soundness_audit.json, testability_FREE_v2.json, seal.json, prereg_freelab.json(.sha256), deviations.json, cost_ledger.jsonl and dataset_card.md, which records provenance, label semantics, what ERROR_CERT is exact relative to, the known out-of-family forms, the UNRESOLVED breakdown, the licence notes (templates built from FOLIO/MALLS atoms; the lexicon is from verified references) and intended use (iteration-5 confirmation only).\n3. src/freelab.py holds the reusable functions:\n   - exhaustive_map_label(candidate_fol, readings: dict[str, str], atoms: dict[str, tuple[int, str]], glosses: dict[str, str], checker=None) -> dict with label / certificate / reason;\n   - equivalent_modulo_vocab_exhaustive(a_fol, b_fol, bridges=..., caps=...) -> (bool | None, map | None, n_maps). It is symmetric and name-free.\n   Both have precise docstrings saying what is exact and what is bounded.\n4. tests/ (pytest):\n   - identity, synonym and nonce rename recover equivalence;\n   - a Q/E role swap is found as a non-identity map;\n   - DROP and ADD mutants from dataset 3 PERTURB give ERROR_CERT;\n   - each bridge B1-B5 is recovered on a hand-made example;\n   - an evaluator-vs-z3 agreement test;\n   - the firewall grep test.\n5. README.md and .aii/manifest.yaml; .venv/ is marked delete, regenerable with 'uv sync'.\n\nFAILURE SCENARIOS AND FALLBACKS\n- The search cap binds on more than 5% of classes: report it and do not raise the cap post hoc. The frozen prereg may pre-declare a single second pass at 4x the cap for capped classes only.\n- Few CORRECT rows (<50 in the untouched subset): declare NOT_TESTABLE on the untouched subset, and report all-rows testability as secondary. This is itself a finding for iteration 5, meaning FREE stays descriptive.\n- The gate fails twice: labels are certificate-only (ERROR_CERT vs UNRESOLVED). That supports a recall-only analysis, not AUROC, and is stated.\n- OpenRouter is unavailable: the map search, audit (i) search, testability of ERROR_CERT and the seal of the search-only labels all run at $0. The gloss steps resume after the key recovers. Never substitute a local model for a gated checker without re-running the gate on it, and log the substitution as a deviation.\n- Audit (ii) implies ERROR_CERT precision < 0.90: keep the labels as frozen, but flag in the card that the FREE ERROR class is contaminated by out-of-family correct forms, and give the estimated rate for iteration 5's sensitivity analysis. Iteration 5 then reports FREE AUROC with and without the audited-disagreement form classes.",
  "domain_practice": "SOURCES READ.\n- The neurosymbolic handbook (aii-handbook-auto-neurosymbolic), in particular: FOLIO/MALLS gold about 36-39% wrong (2606.02837); compiling or proving does not certify faithfulness (2604.19459, 2606.16541); gold-free round trip is occupied (2604.25031); the handbook's critical rule 'state which labels you scored on'.\n- This run's artifacts: exp 7 label_sig.py, sig_prompt.py, testability_FREE.json, the generations format; dataset 3 templates.py and the lexicon schema; the prior-art report art_VIF75I5R6f0v on GenV's label-target reversal (Z3-reference vs panel intent) and on ARc.\n- No new web lookups were made. The 55-minute bounded planning window went to reading the input files that the plan depends on. The norms below on label construction (Dror et al. / Deutsch et al. style meta-evaluation, WMT fresh-test-set practice, TRUE/SummaC label audits, Datasheets for Datasets) come from standing knowledge and are provisional.\n\nHOW LABELS FOR FORMAL-TRANSLATION META-EVALUATION ARE BUILT.\n(1) THE LABEL TARGET IS STATED EXPLICITLY. In NL->FOL / NL->SMT / NL->LTL work the dominant label is solver equivalence to a reference, e.g. LogicLLaMA's and MALLS' logical-equivalence scores and GenV's Z3-reference labels. Everyone knows it under-accepts vocabulary and granularity variants. The field's standard fix is predicate alignment by name similarity, as in LogicLLaMA-style and Vossel-style alignment, and that is exactly the instrument this run found confounded (it is shared with c_score_align, and rename FA is 0.765). A reviewer's first question on any gold-free-metric meta-evaluation is whether the labeller shares an instrument with the metric; the WMT metrics tasks and summarisation factuality (TRUE, SummaC) keep label production separate from the metrics being scored.\n(2) SOUNDNESS IS REPORTED AS PRECISION AND RECALL OF THE LABELLER AGAINST A KNOWN-ANSWER SET. Automatic labellers are validated on items with known answers; our analogues are SIG's pure-z3 labels and PERTURB's typed mutants. A second, independent annotator audits a stratified sample, and precision is reported with a CI (Wilson or Clopper-Pearson). About 50-100 audited items per class is the usual floor for a CI half-width of about 0.07-0.10.\n(3) LLM-AS-ANNOTATOR PRACTICE. Use models from families disjoint from the systems and metrics under test (self-preference bias). Gate the annotator on known-answer items before use. Report per-class recall and inter-annotator agreement (Cohen's κ). Treat disagreement as a separate class rather than forcing a label (human label variation). Keep prompts fixed, at temperature 0, versioned and hashed.\n(4) HOLD-OUT HYGIENE. Labels meant for confirmation are produced and sealed before any metric is joined. Items already used for selection are flagged, and confirmation is reported on the untouched subset, following WMT's practice of re-running metrics on each year's fresh test set.\n(5) TESTABILITY THRESHOLDS. Declare them per class before scoring. In this run the bar is >=50/50 per cell (AUROC SE about 0.05, MDE about 0.10), and strata below it are declared untestable in advance.\n(6) DATASET DOCUMENTATION. A datasheet or card with provenance, label semantics (what each label is exact relative to), known failure modes, licences and intended use. Coverage counts include every unparseable or no-output row.\n(7) EXACTNESS CLAIMS. In formal methods, a non-equivalence claim is trusted when it comes with a countermodel certificate. An equivalence claim relative to a restricted mapping family is stated as relative to that family: bounded model checking reports its bound, so ours reports the map and bridge family and the caps.",
  "practice_alignment": "MEETS\n- Instrument-disjoint labels (1). There is no name similarity anywhere. Maps are enumerated exhaustively under sound semantic prunes (relevance, count, per-predicate monotonicity, finite countermodels), the aligner, consensus and judge code are excluded by a firewall grep test, and inputs are read from the raw generations file, which has no scores. The gloss checkers (Haiku, Qwen) are family-disjoint from the CSC peers (DeepSeek/Microsoft/OpenAI) and the judges (Google/OpenAI).\n- Known-answer validation (2). A 6-class gate of >=100 items each, and the SIG replay: 1,904 rows with pure-z3 labels, re-expressed under nonce and synonym renames, give the false-error rate of ERROR_CERT and the end-to-end false-CORRECT rate on known errors.\n- Independent audit with CIs (2). 60 ERROR_CERT + 60 CORRECT rows audited by a stronger model with Wilson CIs.\n- Annotator practice (3). Temperature 0, versioned and hashed prompts, κ between checkers, and disagreement routed to UNRESOLVED rather than forced.\n- Hold-out hygiene (4). The prereg is hashed before any FREE search output. The label vector is sealed before the old labels are joined. seen_iter3 is flagged, and the untouched subset is primary.\n- Testability declared in advance (5).\n- Certificates for exactness claims (7). Every rejected map carries a countermodel or z3 SAT, and ERROR_CERT is stated as exact relative to the declared map and bridge family.\n- Coverage (6). NO_OUTPUT and UNPARSEABLE rows are kept as rows.\n\nDEPARTURES\n(a) Planner-side literature search. The strategist's field reasoning was not extended with new web reading, because the bounded window went to verifying input formats. Cost: the label-construction norms above are from standing knowledge. They are conservative and all standard, so the risk is low, but no 2026 NL->FOL labelling paper was checked for a newer alignment-free labeller. The executor should run one scholarly search ('predicate alignment equivalence NL FOL evaluation without gold names') and cite whatever it finds in the card, as a positioning note only.\n(b) Gloss checking per pair rather than one call per map, as the direction wrote it. Symmetric antecedent conditions create several z3-equivalent maps (automorphism orbits, e.g. 3! permutations of the DOWN conditions), and only one assignment is right. Judging the union of pairs and deciding at the map level deterministically handles this exactly, and caching makes it cheaper. It is the same test at a finer grain; nothing is lost.\n(c) One annotator family pair and no humans. A fully credible label set would have a human-annotated sample. The budget and the pipeline have no human annotators, so a stronger-model audit replaces them. Cost: the precision estimates are model-relative. The card must say so, and the SIG replay, whose labels are exact, carries the load-bearing soundness number.\n(d) Bridges B5 (lexical negation) and the optional B6 (∃-for-constant) go beyond the direction's list. They are added because the hypothesis itself lists 'lexical negation' among meaning-preserving CONVENTION rewrites, and because the pre-freeze shape census may show the ∃ form. Both are declared before labelling and guarded by the gloss check. Cost: a larger map family raises the chance of a spurious equivalence, which the audit-(i) false-CORRECT rate bounds.\n(e) Correct forms outside the family, e.g. a candidate that encodes one template atom as a relational structure with an extra quantifier, become ERROR_CERT. So ERROR is exact only relative to the family. The implied precision is measured by audit (ii) and is not corrected. Cost: the FREE ERROR class may carry a few percent of correct-but-differently-decomposed rows. The card gives iteration 5 the rate, so it can run a sensitivity analysis.\n(f) The untouched subset is 'not labelled in iteration 3', not 'never scored'. Consensus and judge scores were computed on all FREE rows in iteration 3, but they could only be compared against labels on the 454 tier-A rows, so no metric decision used the rest. Cost: the untouched subset is untouched with respect to label-dependent decisions, and the card states it that way.\n(g) The reference readings are template-built and not re-audited here. The Sonnet lexicon and reference audits were deviation D1 in exp 7 and are not repeated. Cost: a lexicon gloss error would propagate into the gloss check. Audit (ii)'s reasons column is used to flag any such case, and flagged sentences are listed in the card, not dropped.",
  "builds_on": "Continues the lead strand art_cxnoDYQNFolW (exp 7, R_COMP). It is not a fresh line: the direction replaces FREE's panel route, which broke twice, with an alignment-free labeller on the SAME candidates.\n\nREUSED, all read-only, paths absolute:\n(1) Candidates: /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/rcomp/raw/generations.jsonl. These are the FREE generations of the 10 slots and 9 families, few-shot and zero-shot, with no scores. They are used instead of results/rcomp_candidates.jsonl, which embeds consensus and judge scores and is opened only post-seal with a whitelist loader.\n(2) Sentences and references: exp 7 rcomp/work/rcomp_sentences.json (weak/strong/T8-converse readings, template_id, lexicon ids), cross-checked against dataset 3 (art_zcwCQgTqk6DN) /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/full_data_out.json group rcomp_sentences.\n(3) Glosses: dataset 3 lexicon.json (652 entries; vp_sg_pos / vp_sg_neg / const).\n(4) Code, copied into ./vendor with sha256:\n   - dataset 3 labeller/fol.py (parse, equivalent) and labeller/repair_census.py (atoms, bound_vars);\n   - src/templates.py, src/verify.py and src/perturb.py (the RENAME_SYN / RENAME_NONCE / MEANING_RENAME generators, reused for the gate and the SIG replay);\n   - iter_2 exp 5 src/vendor_a/fol_triage.py formula_role_profile (z3-exact per-predicate monotonicity, used as the sound polarity prune);\n   - exp 7 src/sig_prompt.py (reference_signature, signature_symbols) and src/label_sig.py (the canon/rename helpers and the last-record-per-slot loader).\n(5) Known-answer data: exp 7 results/sig_labels.jsonl (1,904 SIG rows, pure-z3 labels), for the gate and soundness audit (i).\n(6) The old tier-A FREE labels (exp 7, 420 ERROR / 34 CORRECT; testability_FREE.json label-vector sha256 97997ea4...) define seen_iter3 and are the agreement baseline, joined only after the seal.\n\nNEGATIVE FINDINGS BUILT PAST:\n- The name-similarity aligner over-accepts meaning-changing renames and fails renames (FA 0.765), hence no similarity anywhere.\n- NF/HYB post-hoc alignment cannot tell a synonym from a wrong predicate (MEANING_RENAME 0.499; 0.388 of extra agreements label-discordant), hence the solver side is paired with an explicit lexical gloss gate rather than trusting any map that makes the formulas equivalent.\n- The panel route for FREE is dropped.\n- SIG's d is mostly reading choice, hence the weak and strong readings are both accepted and the T8 converse is a separate class.\n\nThe outputs feed iteration 5's confirmation, where frozen CSC / c_score_align / judges are scored ONCE on the untouched FREE subset. This artifact PRODUCES those labels itself (STEPS C-G), so that confirmation phase has its inputs owned. The sibling T7a dataset owns E2's labels; this plan does not touch E2."
}
```

### [40] TOOL RESULT — Write · 2026-09-24 07:05:19 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_plan/gen_plan_dataset_2/.terminal_claude_agent_struct_out.json", "content": "{\n  \"title\": \"Name-free labels for free-vocabulary rule translations\",\n  \"summary\": \"T7b. Build the labels that make the in-scope FREE condition of R_COMP testable, with no instrument shared with any consensus metric or judge. For each FREE candidate (exp 7 rcomp/raw/generations.jsonl, the 10 slots x few-shot/zero-shot over 221 main templated sentences), an exhaustive, sound-pruned search over arity-consistent injective symbol maps (plus five declared bridges: reification both ways, merge, conjunctive split, lexical-negation) looks for a map under which the candidate is z3-equivalent to the template's weak or strong reading. No map gives ERROR_CERT. Every rejected map carries a certificate: a finite countermodel or z3 SAT. Rows equivalent only to the T8 converse are READING_CHOICE. If maps exist, a gated two-family LLM gloss check (anthropic/claude-haiku-4.5 + qwen/qwen3-235b-a22b-2507, both family-disjoint from the CSC peers and the judges) rules on the meaning of every mapped atom: CORRECT when both checkers accept every pair of some equivalent map, ERROR_GLOSS when both reject at least one pair of every equivalent map, UNRESOLVED otherwise. Everything is pre-registered and hashed before the first label: map family, bridges, prunes, caps, gloss prompt, gate, label rules and testability rule. The gate is 6 classes x >=100 pair items with known answers. Soundness is audited three ways: (i) a SIG replay under nonce and synonym renames (known z3 labels), (ii) a stronger-model audit of 60 ERROR_CERT and 60 CORRECT rows, (iii) agreement with the old tier-A labels, joined only after the seal. Testability is declared on all FREE rows and on the untouched subset (not tier-A-labelled in iteration 3), which is primary for iteration 5. Output: exp_sel_data_out with three groups (FREE labels, gloss-gate items, SIG soundness replay), plus a seal, audits, a dataset card and the reusable functions exhaustive_map_label / equivalent_modulo_vocab_exhaustive with tests. Expected spend is about $2.5-3.2 (hard stop $3.8, cap $4). CPU only.\",\n  \"runpod_compute_profile\": \"cpu_plus\",\n  \"target_num_datasets\": 3,\n  \"ideal_dataset_criteria\": \"One labelled meta-evaluation table plus two validation tables, all derived from the run's own R_COMP data. No new third-party download is needed: R_COMP's references are true by construction, and its FREE candidates are real outputs of 10 LLM slots across 9 families. The one kind of label missing for the user's operating regime (no controlled vocabulary) is exactly what this artifact adds.\\n\\nGROUP 1 rcomp_free_labels. One row per FREE generation record: every slot, both prompt variants (fewshot_v1 and zero-shot), and the NO_OUTPUT and UNPARSEABLE rows too, so coverage keeps every failure in the denominator.\\n- input = JSON string {text, candidate_fol, system, family, slot, prompt_variant, condition:'FREE', template_id}.\\n- output is one of CORRECT / ERROR_CERT / ERROR_GLOSS / READING_CHOICE / UNRESOLVED_GLOSS / UNRESOLVED_SEARCH_CAP / UNRESOLVED_Z3_UNKNOWN / UNPARSEABLE / NO_OUTPUT.\\n- metadata_label_binary: ERROR when output is ERROR_CERT or ERROR_GLOSS, CORRECT when it is CORRECT, EXCLUDED otherwise.\\n- metadata fields:\\n  - row_key, using exp 7's recipe item_id|FREE|slot|prompt_variant, with item_id = sha1(system|norm(text)|raw_output)[:16];\\n  - sentence_id (the bootstrap cluster), template_id, clause_type, words, word_tercile (cuts 30/35 as in testability_FREE.json), nconds_weak, negated_condition, nested;\\n  - label_source ('exhaustive_map_v1' or 'exhaustive_map_v1+gloss_v1');\\n  - matched_reading (weak / strong / both);\\n  - map_certificate: the winning map as {cand_symbol -> template_atom | bridge spec} plus bridges used;\\n  - n_maps_enumerated, n_maps_fingerprint_pass, n_equiv_maps, n_equiv_map_orbits;\\n  - nonequiv_certificate_type counts (countermodel / z3_sat);\\n  - gloss_pairs [{cand_atom, template_atom, gloss, haiku, qwen}] and gloss_decision;\\n  - unresolved_reason;\\n  - irrelevant_symbols (semantically inert candidate symbols);\\n  - search_secs;\\n  - seen_iter3 (joined after the seal) and old_label_iter3 (joined after the seal, agreement table only);\\n  - metadata_fold 'RCOMP_FREE'.\\n\\nGROUP 2 gloss_gate_items. At least 100 pair items per class in 6 known-answer classes, split into halves A and B by sentence hash:\\n- YES_IDENT: the template name, _k suffix stripped;\\n- YES_SYN: a WordNet synonym rename of the head token, from dataset 3's RENAME_SYN generator;\\n- YES_FORM: a meaning-preserving name form, i.e. a reified or de-reified atom, a lexical-negation name such as NotElectedOfficial for ¬ElectedOfficial, or a modifier-dropping abbreviation;\\n- NO_NONCE: a nonce name;\\n- NO_DONOR: a non-synonymous donor predicate from another lexicon entry in the same sort group, from dataset 3's MEANING_RENAME donors;\\n- NO_ROLE: an argument-role swap of a directional binary atom, or a positive name offered for a negated gloss.\\nFields: input = {sentence, candidate_atom, proposed_meaning}; output = YES or NO; metadata = class, half, each checker's verdict, prompt_version.\\n\\nGROUP 3 sig_soundness_replay. The 1,904 SIG rows with their pure-z3 labels, each re-expressed under two renamings: all symbols consistently renamed to nonce tokens, and all symbols renamed to WordNet synonyms.\\n- output = the known SIG label.\\n- metadata = the new map-search outcome (map_equiv_found, identity_or_other_map, n_equiv_orbits). For the 300-row stratified gloss subsample, also the end-to-end label.\\n\\nQUALITY BARS.\\n- Every CORRECT is backed by an explicit map certificate that re-verifies under z3 at write time.\\n- Every ERROR_CERT is backed by a per-map non-equivalence certificate (countermodel or z3 SAT), and no map returned z3 UNKNOWN.\\n- Labels are sealed by sha256 before any old label, consensus score or judge score is joined.\\n- The whole file stays under the 300 MB limit (expected < 40 MB); if full_data_out.json exceeds the limit, split it with aii-file-size-limit.\",\n  \"dataset_search_plan\": \"No external search is needed; the sources are this run's own artifacts, read-only. Work in STRICT ORDER. Track spend after EVERY OpenRouter call in cost_ledger.jsonl; the hard stop is $3.8.\\n\\nSTEP A. INPUTS AND FIREWALL (30 min)\\n1. Vendor the needed code by COPYING it into ./vendor/, recording sha256 in VENDOR_SHA256.json:\\n   - parse and equivalent: dataset 3 labeller/fol.py (/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/labeller/fol.py);\\n   - atoms and bound_vars: labeller/repair_census.py;\\n   - templates.py and verify.py from dataset 3 src/;\\n   - formula_role_profile for per-predicate monotonicity: iter_2/gen_art/gen_art_experiment_5/src/vendor_a/fol_triage.py;\\n   - the RENAME_SYN / RENAME_NONCE / MEANING_RENAME generators: dataset 3 src/perturb.py;\\n   - reference_signature / signature_symbols: exp 7 src/sig_prompt.py.\\n   Do NOT import or copy consensus_lib.py, peer_text.py, consensus_rcomp.py, the eqmv aligner, repair_census's alignment helpers or anything name-similarity based. Add a unit test that greps ./src and ./vendor for 'equivalent_modulo_vocab(' (the aligner), 'c_score', 'judge' and 'difflib', and fails if found.\\n2. Sentences: /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/rcomp/work/rcomp_sentences.json (314 records = 250 main + reserve).\\n   - Fields used: sentence_id, text, reference_fol_weak, reference_fol_strong, reading_converse (T8 only), template_id, clause_type, lexicon_ids, condition_lexicon_ids, Q/E/P lexicon ids, words.\\n   - Keep only the sentences present in exp 7's FREE generations (221 after the fluency drop). Cross-check against dataset 3 full_data_out.json group rcomp_sentences.\\n3. Glosses: dataset 3 lexicon.json entries (652), keyed by lexicon_id. Gloss = 'x ' + vp_sg_pos; the negative form is vp_sg_neg; constants come from the const field. Build a per-sentence map template_atom -> English gloss the way sig_prompt.build_signature_block does. Note that template names can carry _2 disambiguation suffixes, e.g. EmilysFriend_2, so the gloss comes from the lexicon and NEVER from the name.\\n4. Candidates: read ONLY exp 7 rcomp/raw/generations.jsonl (FREE raw generations). This file has NO scores or labels.\\n   - Keep the last record per (sentence_id, slot, prompt_variant), as in label_sig.load_sig_rows.\\n   - raw_output None -> NO_OUTPUT; parse_ok False, or a failure of our parser -> UNPARSEABLE.\\n   - Recompute item_id and row_key with exp 7's recipe (panel_rcomp.py line 293).\\n   - Reconcile counts and log them. The hypothesis says 2,024 FREE rows; exp 7's testability_FREE.json label_counts sums to 2,652 incl. 199 NO_OUTPUT and 188 UNPARSEABLE; the actual count is whatever this file yields. Write the count table to results/input_counts.json.\\n   - Do NOT open results/rcomp_candidates.jsonl, free_labels.jsonl, scores_FREE*.jsonl or judge_*.jsonl until STEP H.\\n5. SIG rows (for the gate and audit (i)): exp 7 results/sig_labels.jsonl. It holds labels only, no scores, so it is allowed. Use the fields row_key, sentence_id, candidate_fol, label, matched_reading, sig_status.\\n6. LABEL-FREE SHAPE CENSUS on a 100-row random FREE sample (seed 0). Record symbol counts, arity profiles, constant usage, and whether patterns occur such as unary-vs-binary-with-constant, Not-prefixed names, ∃y(N(y) ∧ R(x,y)) in place of a constant, and compound names that concatenate two template concepts. This looks only at inputs, never at labels or scores, so it is legitimate before the freeze. It decides whether the declared bridge set covers the common forms. Log it in results/shape_census.json.\\n   - If the ∃-for-constant pattern appears in >=5% of rows, declare an optional bridge F (existential-constant: ∃y(N(y) ∧ R(x,y)) treated as R(x,c) when N glosses the constant) in the prereg.\\n   - Otherwise list it as a known out-of-family form that audit (ii) quantifies.\\n\\nSTEP B. PRE-REGISTRATION (before ANY map-search output on FREE rows)\\nWrite prereg_freelab.json and store its sha256 in prereg_freelab.sha256. It contains:\\n(a) MAP FAMILY. Maps are injective and arity-consistent. Candidate predicates map to template predicates. Binary predicates may use either argument order. Candidate constants map injectively to template constants or stay free. An unmapped candidate symbol stays an uninterpreted fresh symbol.\\n(b) BRIDGES:\\n   - B1 reification: candidate unary P(x) := template R(x,c) for a template constant c.\\n   - B2 de-reification: candidate binary P(x,k), with k a candidate constant that occurs only in that slot, := template unary U(x).\\n   - B3 merge: candidate unary := A(x) ∧ B(x) for two template unaries that co-occur in one conjunction of a reference.\\n   - B4 conjunctive split: two candidate unaries both := one template unary. Allowed only if the two candidate atoms occur ONLY as siblings in the same conjunction; checked syntactically.\\n   - B5 lexical negation: candidate unary := ¬U(x). Allowed only if the candidate name's first CamelCase or underscore token matches ^(not|non|no|un|in|im|il|ir|dis|never|lacks?|without)$ or ^(Un|Non|In|Im|Dis)[A-Z].\\n   - Optional B6 as decided in A6.\\n   - At most 2 bridge uses per map.\\n(c) SOUND PRUNES, so that the search is exhaustive over the family, not a sample:\\n   - RELEVANCE: a symbol s is inert in F iff F ≡ F[s := fresh s'] (z3). Inert candidate symbols are recorded and dropped. Inert symbols cannot change meaning, and equivalent formulas have equal relevant-symbol sets.\\n   - COUNT: #relevant candidate units after bridges = #relevant template atoms of the reading.\\n   - POLARITY: per-predicate monotonicity (UP / DOWN / NONMONO / NONE from formula_role_profile, z3-exact) is a semantic invariant, so a candidate symbol may map only onto a template atom with the same polarity. Polarity flips under B5, and for merged or split units the polarity is computed after substitution.\\n   - FINGERPRINT: evaluate candidate∘map and the reading on 128 random finite interpretations (domain sizes 2-3, seed fixed). A mismatch is a certified countermodel, i.e. non-equivalence. Only maps that agree on all 128 go to z3 equivalent(), with ms = 2000 and one retry at 10000 if the result is None.\\n(d) CAPS: 2x10^5 maps enumerated or 90 s wall time per unique (sentence, candidate) class. Exceeding either gives UNRESOLVED_SEARCH_CAP. Any z3 UNKNOWN on a fingerprint-passing map, with no other map equivalent, gives UNRESOLVED_Z3_UNKNOWN.\\n(e) LABEL RULES:\\n   - If no map is equivalent to weak or strong, and on T8 no map is equivalent to the converse: ERROR_CERT.\\n   - If maps are equivalent only to the T8 converse: READING_CHOICE.\\n   - If maps are equivalent to weak or strong, the label follows the gloss rule (f).\\n(f) GLOSS RULE. Collect the union of (candidate atom pattern, template atom or bridge meaning) pairs over ALL equivalent maps; symmetric conditions produce several equivalent maps, i.e. automorphism orbits. Each checker judges every pair independently (YES/NO).\\n   - CORRECT iff some equivalent map has all of its pairs YES from BOTH checkers.\\n   - ERROR_GLOSS iff every equivalent map contains at least one pair that is NO from BOTH checkers.\\n   - Otherwise UNRESOLVED_GLOSS.\\n(g) GLOSS PROMPT, verbatim, version gloss_v1. The system message says the task is lexical, not a judgement of the translation. The user message gives the sentence, then a shuffled numbered list of 'SYMBOL USE: <candidate atom as it appears, variables shown as x/y, constants shown> || PROPOSED MEANING: <x + template gloss, with the constant or negation spelled out>'. The question is: 'Could a careful translator plausibly have used this symbol use to express exactly this meaning in this sentence? Answer NO if the name means something different, broader or narrower in a way that changes truth conditions, opposite or negated, if the argument roles are reversed, or if the name is an arbitrary token whose meaning cannot be recognised.' The output is JSON {'1':'YES'|'NO',...}.\\n   - temperature 0, max_tokens 300, at most 12 pairs per call.\\n   - The checker never sees the whole candidate formula, the readings, any label, or which map was z3-equivalent.\\n(h) GATE and TESTABILITY rules as in STEPS D and G.\\n(i) AUDIT protocols as in STEP F.\\nAfter the freeze, any change is logged in deviations.json with a timestamp.\\n\\nSTEP C. MAP SEARCH ON ALL FREE ROWS (CPU, about 1-2 h; $0)\\n1. Deduplicate by (sentence_id, whitespace-normalised candidate_fol). Expect far fewer unique classes than rows.\\n2. Run a ProcessPoolExecutor with the spawn context and workers = detected vCPUs (aii-use-hardware; 4 on cpu_plus). Each task is one sentence's unique classes, and a per-task timeout is enforced.\\n3. Follow aii-long-running-tasks: run 10 classes, then 100, then all, extrapolating wall time at each step. Before the full run, unit-test the evaluator against z3 on 200 random formula pairs; the verdicts must agree 100% where z3 decides.\\n4. Save results/map_search.jsonl, one line per class, with the certificate fields.\\n5. Per-row time estimate: under the polarity and count prunes a typical weak reading has DOWN block {S, A1, A2, A3} and UP block {Q, E}. That is about 4! x 2! x (argument orders) x (bridge variants), i.e. hundreds of maps, so the cap should rarely bind. Report its hit rate.\\n\\nSTEP D. GLOSS GATE (about $0.3)\\n1. Build the gate set from SIG sentences and the lexicon: 6 classes x >=100 items, stratified across templates and sort groups, split 50/50 into halves A and B by sha1(sentence_id).\\n   - YES_FORM items are generated deterministically, e.g. EmilysFriend_2(x) -> Friend(x, emily); ¬ElectedOfficial -> NotElectedOfficial(x); Can(x, distinguishTheTasteOfDifferentCondiments) -> CanDistinguish(x, differentCondiments).\\n   - Keep only NO_ROLE binary atoms whose relation is directional. Mark ambiguous ones, e.g. Friend, and exclude them from the gate.\\n2. Run both checkers on half A with gloss_v1.\\n3. PASS iff balanced accuracy >= 0.90 for Haiku, for Qwen AND for the both-YES conjunction, AND recall >= 0.85 for each of the YES and NO super-classes. Report per-class recall with Wilson CIs and Cohen's κ between the checkers.\\n4. If it FAILS: make ONE prompt revision (gloss_v2) and re-freeze with a hash. Evaluate gloss_v2 on half B only, since half A was used to write it.\\n5. If it still fails: skip STEP E-gloss. FREE labels are then ERROR_CERT / READING_CHOICE / UNRESOLVED_* only (every map-found row becomes UNRESOLVED_GLOSS_GATE_FAILED). Declare this in the card and in testability.\\n\\nSTEP E. GLOSS CHECK ON FREE (about $1.2-1.8)\\n1. Only rows with >=1 equivalent map need calls. Cache pair verdicts by (sentence_id, cand_atom_pattern, template_atom_or_bridge), so identical pairs across slots share a verdict.\\n2. Before the sweep, estimate cost as #unique pairs / 12 x per-call price (read live prices from the OpenRouter catalogue). Abort the sweep if the estimate exceeds $2.2; in that case, process untouched-subset rows first.\\n3. Use asyncio with Semaphore(8), 3 retries with exponential backoff, and no retry loops on a 402. On a 402 or quota error, stop, write partial state and resume after the 00:00 UTC reset.\\n4. Unparseable checker JSON: one re-ask, then treat the pair as NO_VERDICT, which makes it UNRESOLVED.\\n5. Write results/gloss_verdicts.jsonl.\\n\\nSTEP F. SOUNDNESS AUDITS\\n(i) SIG REPLAY ($0 search + about $0.3 gloss)\\n   - For all 1,904 SIG rows, rename every symbol consistently to nonce tokens, then run the map search against the references.\\n   - Report the ERROR_CERT false-error rate on SIG-CORRECT rows = share with no equivalent map. It must be <= 0.02 (pass bar >= 0.98 recovery).\\n   - Report the rescue rate on SIG-ERROR rows = share where a NON-identity map is equivalent, e.g. swapped Q/E roles. These are exactly the rows the gloss check must stop.\\n   - Repeat with WordNet-synonym renames. On a stratified 300 (150 CORRECT / 150 ERROR, stratified by template), run the full pipeline including the gloss check and report the end-to-end confusion matrix. Key numbers:\\n     - false-CORRECT rate on known ERROR rows (must be <= 0.05);\\n     - CORRECT recall on known CORRECT rows;\\n     - UNRESOLVED share.\\n(ii) STRONGER-MODEL AUDIT (about $1.0-1.5)\\n   - Use the newest Anthropic Sonnet available on OpenRouter; check the catalogue and prefer anthropic/claude-sonnet-5, else anthropic/claude-sonnet-4.5.\\n   - Draw 60 FREE ERROR_CERT rows stratified by template, plus 60 FREE CORRECT rows.\\n   - The prompt shows the sentence, the candidate and the English meaning of each template atom (no formula readings, no label). It asks FAITHFUL / FAITHFUL_DIFFERENT_DECOMPOSITION / UNFAITHFUL / UNSURE, with a one-line reason.\\n   - Report the implied ERROR_CERT precision = share not judged faithful, and the CORRECT precision, both with Wilson 95% CIs.\\n   - The audit NEVER changes a label. Disagreement reasons are tallied into out-of-family forms, e.g. ∃-for-constant or an unbridged compound predicate.\\n(iii) OLD-LABEL AGREEMENT: STEP H, after the seal.\\n\\nSTEP G. TESTABILITY and SEAL\\n1. Write testability_FREE_v2.json with counts per template, per clause_type, per word tercile and per prompt_variant of CORRECT / ERROR (ERROR_CERT + ERROR_GLOSS) / each excluded class, and sentences with >=1 of each.\\n2. Rule: TESTABLE iff >=50 ERROR and >=50 CORRECT spread over >=25 sentences (a sentence counts toward a class if it holds >=1 row of that class). Declare it on (1) all FREE rows and (2) the untouched subset. Also give descriptive 30/30 reportability per stratum.\\n3. The per-stratum MDE for AUROC at the achieved n is about 0.10 at 50/50, per the hypothesis's power note; report it.\\n4. seal.json holds sha256 over the sorted (row_key, label) vector for all rows and for the untouched subset, the prereg hash, the vendor hashes and the UTC time.\\n\\nSTEP H. POST-SEAL JOIN, the only step that opens exp 7's results/rcomp_candidates.jsonl\\n1. Read that file with a whitelist JSON loader that keeps only row_key, label, label_tier and label_source, dropping every other key at parse time.\\n2. Set seen_iter3 = old label in {CORRECT, ERROR} with tier A.\\n3. Write soundness_audit.json (iii): a 2x2+ agreement table of old versus new labels with κ.\\n4. Examine every disagreement by hand for 20 rows and classify it: old aligner over-acceptance, new bridge, gloss rejection, or the old label was UNRESOLVED.\\n5. Verify that every new row_key exists in rcomp_candidates.jsonl, and report the mismatches.\\n\\nSTEP I. PACKAGE\\n1. Write full_data_out.json in exp_sel_data_out format, with 3 groups (rcomp_free_labels, gloss_gate_items, sig_soundness_replay). Validate it with aii-json and make the mini/preview variants.\\n2. Also write gate_report.json, soundness_audit.json, testability_FREE_v2.json, seal.json, prereg_freelab.json(.sha256), deviations.json, cost_ledger.jsonl and dataset_card.md, which records provenance, label semantics, what ERROR_CERT is exact relative to, the known out-of-family forms, the UNRESOLVED breakdown, the licence notes (templates built from FOLIO/MALLS atoms; the lexicon is from verified references) and intended use (iteration-5 confirmation only).\\n3. src/freelab.py holds the reusable functions:\\n   - exhaustive_map_label(candidate_fol, readings: dict[str, str], atoms: dict[str, tuple[int, str]], glosses: dict[str, str], checker=None) -> dict with label / certificate / reason;\\n   - equivalent_modulo_vocab_exhaustive(a_fol, b_fol, bridges=..., caps=...) -> (bool | None, map | None, n_maps). It is symmetric and name-free.\\n   Both have precise docstrings saying what is exact and what is bounded.\\n4. tests/ (pytest):\\n   - identity, synonym and nonce rename recover equivalence;\\n   - a Q/E role swap is found as a non-identity map;\\n   - DROP and ADD mutants from dataset 3 PERTURB give ERROR_CERT;\\n   - each bridge B1-B5 is recovered on a hand-made example;\\n   - an evaluator-vs-z3 agreement test;\\n   - the firewall grep test.\\n5. README.md and .aii/manifest.yaml; .venv/ is marked delete, regenerable with 'uv sync'.\\n\\nFAILURE SCENARIOS AND FALLBACKS\\n- The search cap binds on more than 5% of classes: report it and do not raise the cap post hoc. The frozen prereg may pre-declare a single second pass at 4x the cap for capped classes only.\\n- Few CORRECT rows (<50 in the untouched subset): declare NOT_TESTABLE on the untouched subset, and report all-rows testability as secondary. This is itself a finding for iteration 5, meaning FREE stays descriptive.\\n- The gate fails twice: labels are certificate-only (ERROR_CERT vs UNRESOLVED). That supports a recall-only analysis, not AUROC, and is stated.\\n- OpenRouter is unavailable: the map search, audit (i) search, testability of ERROR_CERT and the seal of the search-only labels all run at $0. The gloss steps resume after the key recovers. Never substitute a local model for a gated checker without re-running the gate on it, and log the substitution as a deviation.\\n- Audit (ii) implies ERROR_CERT precision < 0.90: keep the labels as frozen, but flag in the card that the FREE ERROR class is contaminated by out-of-family correct forms, and give the estimated rate for iteration 5's sensitivity analysis. Iteration 5 then reports FREE AUROC with and without the audited-disagreement form classes.\",\n  \"domain_practice\": \"SOURCES READ.\\n- The neurosymbolic handbook (aii-handbook-auto-neurosymbolic), in particular: FOLIO/MALLS gold about 36-39% wrong (2606.02837); compiling or proving does not certify faithfulness (2604.19459, 2606.16541); gold-free round trip is occupied (2604.25031); the handbook's critical rule 'state which labels you scored on'.\\n- This run's artifacts: exp 7 label_sig.py, sig_prompt.py, testability_FREE.json, the generations format; dataset 3 templates.py and the lexicon schema; the prior-art report art_VIF75I5R6f0v on GenV's label-target reversal (Z3-reference vs panel intent) and on ARc.\\n- No new web lookups were made. The 55-minute bounded planning window went to reading the input files that the plan depends on. The norms below on label construction (Dror et al. / Deutsch et al. style meta-evaluation, WMT fresh-test-set practice, TRUE/SummaC label audits, Datasheets for Datasets) come from standing knowledge and are provisional.\\n\\nHOW LABELS FOR FORMAL-TRANSLATION META-EVALUATION ARE BUILT.\\n(1) THE LABEL TARGET IS STATED EXPLICITLY. In NL->FOL / NL->SMT / NL->LTL work the dominant label is solver equivalence to a reference, e.g. LogicLLaMA's and MALLS' logical-equivalence scores and GenV's Z3-reference labels. Everyone knows it under-accepts vocabulary and granularity variants. The field's standard fix is predicate alignment by name similarity, as in LogicLLaMA-style and Vossel-style alignment, and that is exactly the instrument this run found confounded (it is shared with c_score_align, and rename FA is 0.765). A reviewer's first question on any gold-free-metric meta-evaluation is whether the labeller shares an instrument with the metric; the WMT metrics tasks and summarisation factuality (TRUE, SummaC) keep label production separate from the metrics being scored.\\n(2) SOUNDNESS IS REPORTED AS PRECISION AND RECALL OF THE LABELLER AGAINST A KNOWN-ANSWER SET. Automatic labellers are validated on items with known answers; our analogues are SIG's pure-z3 labels and PERTURB's typed mutants. A second, independent annotator audits a stratified sample, and precision is reported with a CI (Wilson or Clopper-Pearson). About 50-100 audited items per class is the usual floor for a CI half-width of about 0.07-0.10.\\n(3) LLM-AS-ANNOTATOR PRACTICE. Use models from families disjoint from the systems and metrics under test (self-preference bias). Gate the annotator on known-answer items before use. Report per-class recall and inter-annotator agreement (Cohen's κ). Treat disagreement as a separate class rather than forcing a label (human label variation). Keep prompts fixed, at temperature 0, versioned and hashed.\\n(4) HOLD-OUT HYGIENE. Labels meant for confirmation are produced and sealed before any metric is joined. Items already used for selection are flagged, and confirmation is reported on the untouched subset, following WMT's practice of re-running metrics on each year's fresh test set.\\n(5) TESTABILITY THRESHOLDS. Declare them per class before scoring. In this run the bar is >=50/50 per cell (AUROC SE about 0.05, MDE about 0.10), and strata below it are declared untestable in advance.\\n(6) DATASET DOCUMENTATION. A datasheet or card with provenance, label semantics (what each label is exact relative to), known failure modes, licences and intended use. Coverage counts include every unparseable or no-output row.\\n(7) EXACTNESS CLAIMS. In formal methods, a non-equivalence claim is trusted when it comes with a countermodel certificate. An equivalence claim relative to a restricted mapping family is stated as relative to that family: bounded model checking reports its bound, so ours reports the map and bridge family and the caps.\",\n  \"practice_alignment\": \"MEETS\\n- Instrument-disjoint labels (1). There is no name similarity anywhere. Maps are enumerated exhaustively under sound semantic prunes (relevance, count, per-predicate monotonicity, finite countermodels), the aligner, consensus and judge code are excluded by a firewall grep test, and inputs are read from the raw generations file, which has no scores. The gloss checkers (Haiku, Qwen) are family-disjoint from the CSC peers (DeepSeek/Microsoft/OpenAI) and the judges (Google/OpenAI).\\n- Known-answer validation (2). A 6-class gate of >=100 items each, and the SIG replay: 1,904 rows with pure-z3 labels, re-expressed under nonce and synonym renames, give the false-error rate of ERROR_CERT and the end-to-end false-CORRECT rate on known errors.\\n- Independent audit with CIs (2). 60 ERROR_CERT + 60 CORRECT rows audited by a stronger model with Wilson CIs.\\n- Annotator practice (3). Temperature 0, versioned and hashed prompts, κ between checkers, and disagreement routed to UNRESOLVED rather than forced.\\n- Hold-out hygiene (4). The prereg is hashed before any FREE search output. The label vector is sealed before the old labels are joined. seen_iter3 is flagged, and the untouched subset is primary.\\n- Testability declared in advance (5).\\n- Certificates for exactness claims (7). Every rejected map carries a countermodel or z3 SAT, and ERROR_CERT is stated as exact relative to the declared map and bridge family.\\n- Coverage (6). NO_OUTPUT and UNPARSEABLE rows are kept as rows.\\n\\nDEPARTURES\\n(a) Planner-side literature search. The strategist's field reasoning was not extended with new web reading, because the bounded window went to verifying input formats. Cost: the label-construction norms above are from standing knowledge. They are conservative and all standard, so the risk is low, but no 2026 NL->FOL labelling paper was checked for a newer alignment-free labeller. The executor should run one scholarly search ('predicate alignment equivalence NL FOL evaluation without gold names') and cite whatever it finds in the card, as a positioning note only.\\n(b) Gloss checking per pair rather than one call per map, as the direction wrote it. Symmetric antecedent conditions create several z3-equivalent maps (automorphism orbits, e.g. 3! permutations of the DOWN conditions), and only one assignment is right. Judging the union of pairs and deciding at the map level deterministically handles this exactly, and caching makes it cheaper. It is the same test at a finer grain; nothing is lost.\\n(c) One annotator family pair and no humans. A fully credible label set would have a human-annotated sample. The budget and the pipeline have no human annotators, so a stronger-model audit replaces them. Cost: the precision estimates are model-relative. The card must say so, and the SIG replay, whose labels are exact, carries the load-bearing soundness number.\\n(d) Bridges B5 (lexical negation) and the optional B6 (∃-for-constant) go beyond the direction's list. They are added because the hypothesis itself lists 'lexical negation' among meaning-preserving CONVENTION rewrites, and because the pre-freeze shape census may show the ∃ form. Both are declared before labelling and guarded by the gloss check. Cost: a larger map family raises the chance of a spurious equivalence, which the audit-(i) false-CORRECT rate bounds.\\n(e) Correct forms outside the family, e.g. a candidate that encodes one template atom as a relational structure with an extra quantifier, become ERROR_CERT. So ERROR is exact only relative to the family. The implied precision is measured by audit (ii) and is not corrected. Cost: the FREE ERROR class may carry a few percent of correct-but-differently-decomposed rows. The card gives iteration 5 the rate, so it can run a sensitivity analysis.\\n(f) The untouched subset is 'not labelled in iteration 3', not 'never scored'. Consensus and judge scores were computed on all FREE rows in iteration 3, but they could only be compared against labels on the 454 tier-A rows, so no metric decision used the rest. Cost: the untouched subset is untouched with respect to label-dependent decisions, and the card states it that way.\\n(g) The reference readings are template-built and not re-audited here. The Sonnet lexicon and reference audits were deviation D1 in exp 7 and are not repeated. Cost: a lexicon gloss error would propagate into the gloss check. Audit (ii)'s reasons column is used to flag any such case, and flagged sentences are listed in the card, not dropped.\",\n  \"builds_on\": \"Continues the lead strand art_cxnoDYQNFolW (exp 7, R_COMP). It is not a fresh line: the direction replaces FREE's panel route, which broke twice, with an alignment-free labeller on the SAME candidates.\\n\\nREUSED, all read-only, paths absolute:\\n(1) Candidates: /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/rcomp/raw/generations.jsonl. These are the FREE generations of the 10 slots and 9 families, few-shot and zero-shot, with no scores. They are used instead of results/rcomp_candidates.jsonl, which embeds consensus and judge scores and is opened only post-seal with a whitelist loader.\\n(2) Sentences and references: exp 7 rcomp/work/rcomp_sentences.json (weak/strong/T8-converse readings, template_id, lexicon ids), cross-checked against dataset 3 (art_zcwCQgTqk6DN) /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/full_data_out.json group rcomp_sentences.\\n(3) Glosses: dataset 3 lexicon.json (652 entries; vp_sg_pos / vp_sg_neg / const).\\n(4) Code, copied into ./vendor with sha256:\\n   - dataset 3 labeller/fol.py (parse, equivalent) and labeller/repair_census.py (atoms, bound_vars);\\n   - src/templates.py, src/verify.py and src/perturb.py (the RENAME_SYN / RENAME_NONCE / MEANING_RENAME generators, reused for the gate and the SIG replay);\\n   - iter_2 exp 5 src/vendor_a/fol_triage.py formula_role_profile (z3-exact per-predicate monotonicity, used as the sound polarity prune);\\n   - exp 7 src/sig_prompt.py (reference_signature, signature_symbols) and src/label_sig.py (the canon/rename helpers and the last-record-per-slot loader).\\n(5) Known-answer data: exp 7 results/sig_labels.jsonl (1,904 SIG rows, pure-z3 labels), for the gate and soundness audit (i).\\n(6) The old tier-A FREE labels (exp 7, 420 ERROR / 34 CORRECT; testability_FREE.json label-vector sha256 97997ea4...) define seen_iter3 and are the agreement baseline, joined only after the seal.\\n\\nNEGATIVE FINDINGS BUILT PAST:\\n- The name-similarity aligner over-accepts meaning-changing renames and fails renames (FA 0.765), hence no similarity anywhere.\\n- NF/HYB post-hoc alignment cannot tell a synonym from a wrong predicate (MEANING_RENAME 0.499; 0.388 of extra agreements label-discordant), hence the solver side is paired with an explicit lexical gloss gate rather than trusting any map that makes the formulas equivalent.\\n- The panel route for FREE is dropped.\\n- SIG's d is mostly reading choice, hence the weak and strong readings are both accepted and the T8 converse is a separate class.\\n\\nThe outputs feed iteration 5's confirmation, where frozen CSC / c_score_align / judges are scored ONCE on the untouched FREE subset. This artifact PRODUCES those labels itself (STEPS C-G), so that confirmation phase has its inputs owned. The sibling T7a dataset owns E2's labels; this plan does not touch E2.\"\n}\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [41] ASSISTANT · 2026-09-24 07:05:32 UTC

```
I've written the plan for the FREE-condition labeller to `./.terminal_claude_agent_struct_out.json`, but nothing has checked that the JSON parses, because I couldn't run code here. It also rests on the input files I read, not on any new literature search.

**Firewall on inputs.** The labeller reads FREE candidates from exp 7's raw `rcomp/raw/generations.jsonl`, which holds no scores or labels. `results/rcomp_candidates.jsonl` stores consensus and judge scores in the same rows as the labels, so it is opened only after the labels are sealed, through a loader that keeps only the key and old-label fields. A unit test fails the build if any aligner, consensus or judge code gets imported.

**Map search.** It is exhaustive, with no name similarity anywhere. Four checks cut the search down without losing any correct map:
- Drop symbols that have no effect on the formula's meaning.
- Require the symbol counts to match.
- Match each predicate's polarity (whether it acts as a condition or a conclusion); equivalent formulas always agree on this.
- Test each map on 128 small random worlds; any mismatch is a concrete counterexample proving non-equivalence.

After these cuts a typical sentence leaves only hundreds of maps. The direction's four bridges (reification in both directions, merge, and split) are kept; split is allowed only for sibling conjuncts. I added a fifth for names like `NotElectedOfficial`, and a sixth for writing "the coffee shop" as "some coffee shop" is added only if a label-free look at 100 inputs finds it often enough. Every ERROR_CERT carries a counterexample or z3 proof for each rejected map.

**Gloss check changed from the direction.** The direction asked for one checker call per map. When conditions are symmetric, several maps are z3-equivalent but only one assignment is right. So each checker judges the pairs (candidate symbol, proposed meaning) once, and a deterministic rule decides per map. The checkers are Haiku 4.5 and Qwen3-235B. They never see the full formula, the readings or the solver result.

**Soundness evidence.** The most important check is a replay of the 1,904 SIG rows, whose labels are exact, after renaming their symbols to nonsense words and to synonyms. The labeller must recover equivalence for at least 98% of the correct rows, and at most 5% of known errors may end up labelled CORRECT. A stronger Sonnet model also audits 60 ERROR_CERT and 60 CORRECT rows, with confidence intervals; that audit never changes a label.

**Testability.** The rule is at least 50 ERROR and 50 CORRECT across at least 25 sentences. It is declared on all FREE rows and on the rows not labelled in iteration 3; the second set is the primary one for iteration 5.

**Row counts disagree.** The hypothesis says 2,024 FREE rows, but exp 7's label counts sum to 2,652, including 199 with no output and 188 unparseable. The plan has the executor count what the file actually holds and log that.

**Cost and compute.** Expected spend is about $2.5–3.2, with a hard stop at $3.8 against the $4 cap. It runs on CPU only (`cpu_plus`).

**Known gaps, stated in the plan:**
- No humans in the audit, so its precision estimates are relative to the model.
- Correct translations in a form outside the declared maps and bridges get ERROR_CERT; the audit measures how often.
- The "untouched" subset means rows not labelled in iteration 3. Consensus and judge scores were already computed on every FREE row.
```
