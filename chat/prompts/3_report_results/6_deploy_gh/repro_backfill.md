# repro_backfill — report_results

> Phase: `gen_paper_repo` · `deploy_gh`
> Run: `run_u75jRHUss0zo` — Gold-Free Faithfulness Metrics for NL-to-FOL Translation
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `repro_backfill` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-09-24 23:20:55 UTC

````
<role>
You write the reproducibility.md of one finished research artifact, after the fact. The agent
that produced the artifact never wrote it, so everything you write has to come from what its
workspace actually holds: the code, the README, the results files, the data files, the
dependency pins, the seeds and configs in the code. You are a careful reader, not an author:
you do not run the code, install anything, or change any file except reproducibility.md.

Be exact where the workspace is exact: real file names, the real entry point, the real
command-line arguments, the real pinned versions, the real seeds, the real output files and the
real numbers they hold. Be honest where it is silent: when the workspace does not record
something the spec asks for (hardware, runtime, the exact search queries, a download URL), say
that it was not recorded and give the closest thing the files do support. Never invent a
version, a seed, a number or a command.
</role>

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
Your workspace: `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1/`:
GOOD: `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1/file.py`, `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>

<artifact>
Type: evaluation
Title: Re-checking earlier logic-metric results across label sets
Summary: Zero-LLM-spend, CPU-only re-analysis of the iteration-1 artifacts (exp A FOL-Triage, exp C consensus c_score, exp D judges/baselines, dataset E screen adjudication), joined on item_id. eval.py (+src/) writes eval_out.json (exp_eval_sol_out, validated; ~5.9k flat metrics_agg keys + structured metadata incl. VERDICT; 1,380 per-item examples with oriented scores, per-regime labels, PT OOF), tables/*.csv (each with a '# source:' line), figures/fig_regime_shift and fig_forest_common (json/png/pdf), and audit/ scripts. KEY FINDINGS. (1) Re-derivation gate: 57/57 reviewer audit numbers reproduce (n=389/160 err/151 sents; c_score .842, fused .767, judge_disg .785; tier A+B n=304 fused .872, bow .817, c_score .776, judge .771). (2) Same-item, same-label common sets for 13 regimes (testable: R_SOLVER_CONS n=373/155 err, own-label A/C/D, R_ADJ_AB 298/165, R_ADJ_ALL 498/271, CONTESTED->C/E, L_UNPARSEABLE_AS_ERROR 413/195; R_ADJ_A and all track-H regimes are untestable, reported sign-only). (3) The iteration-1 rule FAILS for fused_H and c_score in every regime (rewrite FA 0.275 / 0.96). fused_H minus judge is -0.013 under solver labels but +0.096 [.020,.171] under A+B; c_score minus judge is +0.067 [-.012,.148] under solver labels and +0.006 under A+B. (4) Label-only shift solver->A+B on the same 161 items: bow +0.102 and fused +0.080 (CI>0) go up; c_score -0.106 goes down. Rank Kendall tau is 0.60. On the 58 flipped items, bow/fused flag 81-83% vs c_score 34% (instrument-sharing confirmed). (5) SCREEN PREVIEW: PT (cross-fitted c_score+bow_uncarried+l3) minus judge_cheap_disg is +0.089 [.010,.165] solver, +0.104 [.039,.175] A+B, +0.090 [.038,.142] all tiers, +0.118 unparseable-as-error. Nested S4+PT over refit S4 is +0.04-0.06 (CI>0). Screen bar that iteration-2 confirmation must beat = these deltas. (6) P1: the structural clause is untestable (all QUANT/SCOPE/BIND/SWAP/NEG cells have <15 errors); text beats peers on peer-endorsed errors (CI>0). P2a CONFIRMED only for all tiers. P2b depends on the comparator: vs c_score the gain comes from endorsed errors; vs bow it comes from non-endorsed errors. (7) At matched FA 0.10 the ORIGINAL cheap judge has higher recall than the disguised one (+0.11/+0.20). Contamination DiD CIs include 0 but MDE = 0.12-0.21, so a 0.05 effect is undetectable. Frontier minus cheap under A+B is +0.166. (8) Invariance comparisons across A/C/D used different rewrite sets. (9) Candidate B was planned but gen_art_experiment_2 is an empty .aii/ dir: it never ran. (10) Exp C's -0.94/SD length interaction reproduces exactly. Exp A's L2-bow = n_unanch+uncarried (0.737) vs bow_uncarried (0.711). Panel expert-pair acceptance is .613 (unambiguous). Independent re-derivation (different code path) matches all headline numbers. On permuted labels the cross-fitted PT is biased below 0.5; the observed deltas exceed all 20 null deltas (null max .047 solver / .087 A+B).
Workspace: /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1
</artifact>

<workspace_files>
README.md (12,246 bytes)
eval.py (17,069 bytes)
eval_out.json (4,782,680 bytes)
full_eval_out.json (5,273,160 bytes)
mini_eval_out.json (1,376,211 bytes)
preview_eval_out.json (757,117 bytes)
pyproject.toml (857 bytes)
regimes.json (11,888 bytes)
requirements.txt (460 bytes)
audit/placebo_permutations.json (657 bytes)
audit/placebo_permutations.py (1,716 bytes)
audit/rederive_headlines.json (2,952 bytes)
audit/rederive_headlines.py (8,453 bytes)
data/panel_calibration.json (194,942 bytes)
figures/fig_forest_common.json (9,236 bytes)
figures/fig_forest_common.pdf (32,600 bytes)
figures/fig_forest_common.png (212,720 bytes)
figures/fig_regime_shift.json (5,403 bytes)
figures/fig_regime_shift.pdf (41,568 bytes)
figures/fig_regime_shift.png (538,491 bytes)
logs/full_run.out (4,306 bytes)
src/load.py (8,772 bytes)
src/outputs.py (20,343 bytes)
src/stats_utils.py (10,701 bytes)
src/steps_audit.py (58,814 bytes)
src/steps_core.py (34,567 bytes)
src/steps_models.py (21,114 bytes)
tables/available_case_H_ADJ_AB.csv (1,994 bytes)
tables/available_case_H_CURATOR.csv (2,031 bytes)
tables/available_case_H_SOLVER.csv (2,007 bytes)
tables/available_case_L_UNPARSEABLE_AS_ERROR.csv (2,483 bytes)
tables/available_case_R_ADJ_A.csv (2,248 bytes)
tables/available_case_R_ADJ_AB.csv (2,346 bytes)
tables/available_case_R_ADJ_AB_CONT_C.csv (2,498 bytes)
tables/available_case_R_ADJ_AB_CONT_E.csv (2,481 bytes)
tables/available_case_R_ADJ_ALL.csv (2,360 bytes)
tables/available_case_R_SOLVER_CONS.csv (2,162 bytes)
tables/available_case_R_SOLVER_OWN_A.csv (2,376 bytes)
tables/available_case_R_SOLVER_OWN_C.csv (2,402 bytes)
tables/available_case_R_SOLVER_OWN_D.csv (2,348 bytes)
tables/bookkeeping.csv (1,623 bytes)
tables/common_items_H_ADJ_AB.csv (8,909 bytes)
tables/common_items_H_CURATOR.csv (9,438 bytes)
tables/common_items_H_SOLVER.csv (9,387 bytes)
tables/common_items_L_UNPARSEABLE_AS_ERROR.csv (11,651 bytes)
tables/common_items_R_ADJ_A.csv (9,926 bytes)
tables/common_items_R_ADJ_AB.csv (11,066 bytes)
tables/common_items_R_ADJ_AB_CONT_C.csv (11,274 bytes)
tables/common_items_R_ADJ_AB_CONT_E.csv (11,303 bytes)
tables/common_items_R_ADJ_ALL.csv (11,192 bytes)
tables/common_items_R_SOLVER_CONS.csv (11,237 bytes)
tables/common_items_R_SOLVER_OWN_A.csv (11,267 bytes)
tables/common_items_R_SOLVER_OWN_C.csv (11,267 bytes)
tables/common_items_R_SOLVER_OWN_D.csv (11,294 bytes)
tables/complexity_bins.csv (12,194 bytes)
tables/complexity_gee.csv (2,371 bytes)
tables/contamination.csv (4,729 bytes)
tables/coverage_vs_request.csv (2,351 bytes)
tables/flipped_items.csv (18,712 bytes)
tables/frontier_same_item.csv (9,013 bytes)
tables/function_inventory.csv (19,932 bytes)
tables/invariance_crosscheck.csv (9,881 bytes)
tables/invariance_paired_mcnemar.csv (512 bytes)
tables/invariance_set_overlap.csv (689 bytes)
tables/judge_matched_fa.csv (21,251 bytes)
tables/label_disagreements.csv (36,444 bytes)
tables/mustfix_A.csv (40,135 bytes)
tables/mustfix_C.csv (24,424 bytes)
tables/mustfix_D.csv (344,110 bytes)
tables/mustfix_E.csv (25,523 bytes)
tables/p1_crossover_R_ADJ_AB.csv (20,188 bytes)
tables/p1_crossover_R_ADJ_ALL.csv (22,484 bytes)
tables/p1_crossover_R_SOLVER_CONS.csv (20,439 bytes)
tables/p1_diff_R_ADJ_AB.csv (4,375 bytes)
tables/p1_diff_R_ADJ_ALL.csv (5,242 bytes)
tables/p1_diff_R_SOLVER_CONS.csv (4,587 bytes)
tables/p2.csv (16,617 bytes)
tables/rank_kendall_tau.csv (3,970 bytes)
tables/rederivation.csv (4,755 bytes)
tables/regime_auroc_matrix.csv (5,857 bytes)
tables/regime_shift.csv (34,995 bytes)
</workspace_files>

<reproducibility_spec>
Write `reproducibility.md` in your workspace with COMPLETE step-by-step instructions to reproduce your exact results on Ubuntu — describe what you ACTUALLY ran, not an idealized version. Cover: (1) getting this artifact: your workspace is published as one folder of a public GitHub repository, so start from a clone of that repository and `cd` into the folder; (2) system packages, the Python version, venv creation, and the exact library versions you actually installed, pinned (match pyproject.toml); (3) any data/model/checkpoint downloads plus env vars or API keys needed, by NAME only, never values; (4) the exact commands you ran, in order, with seeds, configs, hardware used (GPU type, VRAM) and approximate runtime; (5) which output files and numbers a reader should get, and where they appear in the paper. PORTABLE PATHS: a reader has only the published repository, never this server, so every path in this file, in `restore.sh` or any install script, and in your code must be RELATIVE to your workspace (in code, anchor it on `Path(__file__)`), never an absolute `/ai-inventor/...` path. Read an input another artifact produced through ONE relative constant or environment variable and name that artifact by its id; the repository publishes it as a sibling folder. An input the user uploaded is private and is not published: say so, and say how a reader supplies their own copy. This is a REQUIRED output file, like the others above.
</reproducibility_spec>

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.

<todos>
TODO 1. Read the artifact's workspace `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1` (listed below): the entry-point code, any README, pyproject.toml or requirements file, the configs, the seeds set in the code, the results and output JSON files, and the data files. Open the files; do not guess their contents from their names. Do not run, install or modify anything.
TODO 2. Write `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1/reproducibility.md` following the specification below, which is the one the artifact's own agent was given. Take every command, file name, version, seed and number from the files you read. Where the workspace does not record a point the specification asks for, state that it was not recorded rather than inventing it.
TODO 3. Re-read `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1/reproducibility.md` against the workspace: every file it names exists, every command matches the code's real arguments, every number matches the results files. Fix anything that does not. Then return the structured output.
</todos>

---

Output the result as JSON to: `./.terminal_claude_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "ReproducibilityDocExpectedFiles": {
      "description": "The one file the backfill writes.",
      "properties": {
        "reproducibility": {
          "description": "Path to reproducibility.md. Example: 'reproducibility.md'",
          "title": "Reproducibility",
          "type": "string"
        }
      },
      "required": [
        "reproducibility"
      ],
      "title": "ReproducibilityDocExpectedFiles",
      "type": "object"
    }
  },
  "description": "Structured output of the reproducibility.md backfill agent.",
  "properties": {
    "summary": {
      "description": "Which workspace files the instructions were derived from, and which of the spec's points the workspace did not record.",
      "maxLength": 2000,
      "minLength": 50,
      "title": "Summary",
      "type": "string"
    },
    "out_expected_files": {
      "$ref": "#/$defs/ReproducibilityDocExpectedFiles",
      "description": "All output files you created. Must include reproducibility.md."
    }
  },
  "required": [
    "summary",
    "out_expected_files"
  ],
  "title": "ReproducibilityDoc",
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
