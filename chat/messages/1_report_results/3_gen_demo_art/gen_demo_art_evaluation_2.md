# gen_demo_art_evaluation_2 — report_results

> Phase: `gen_paper_repo` · `gen_demo_art`
> Run: `gen_paper_repo_a2e1d024cc16` — Cross-Family Solver Consensus as a Gold-Free Faithfulness Metric for Logic Translation
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_demo_art_evaluation_2` (terminal_claude_agent, claude-opus-5-5)

### [1] CONFIG · 2026-09-25 16:30:52 UTC

```
model: claude-opus-5-5 | effort: high | permission: bypassPermissions
```

### [2] SYSTEM-USER prompt · 2026-09-25 16:30:58 UTC

````
<conversion_philosophy>
**MINIMAL CHANGES — PRESERVE THE ORIGINAL CODE**

The goal is to make the artifact's code READABLE, UNDERSTANDABLE, and RUNNABLE in a short time
to someone reviewing the research, with the option to easily scale parameters back to original
values for a full run (which can take much longer). Think of this as annotating and reformatting,
not refactoring.

**DO:**
- Split the original script into logical notebook cells (imports, setup, processing, results)
- Add markdown cells BETWEEN code cells explaining what each section does and why
- Add inline comments where the logic is non-obvious
- Add a visualization/summary cell at the end showing key outputs
- Fix hardcoded file paths to use the GitHub data loading pattern

**DO NOT:**
- Rewrite functions or change algorithms
- Rename variables or restructure logic
- Add error handling, type hints, or "improvements" that weren't in the original
- Simplify or "clean up" the original code
- Remove any original comments or logic
- Change the computational approach

The reader should recognize the original script when looking at the notebook — it's the
same code, just split into cells with explanatory markdown between sections.
</conversion_philosophy>

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
Your workspace: `/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_FWy8D4_y9GBn`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_FWy8D4_y9GBn/`:
GOOD: `/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_FWy8D4_y9GBn/file.py`, `/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_FWy8D4_y9GBn/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>
<disposable_outputs>
A SHARED CACHE ALREADY EXISTS FOR THIS RUN: `/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/.shared_cache`
`HF_HOME`, `HF_HUB_CACHE`, `TRANSFORMERS_CACHE`, `HF_DATASETS_CACHE`,
`TORCH_HOME`, `PIP_CACHE_DIR` and `UV_CACHE_DIR` are ALREADY set to point
there. Every step and every iteration of this run shares it, so a model or
dataset an earlier experiment downloaded is already on disk for you.

DO NOT override those variables. In particular do NOT write the common
pattern `os.environ["HF_HOME"] = <workspace>/hf_cache` — `HF_HOME` and
`TRANSFORMERS_CACHE` are read differently by `huggingface_hub` (one has
`/hub` appended, the other does not), so pointing both at one directory
stores every weight TWICE. That mistake cost one run 25 GB of identical
blobs. If you must set them, use the values above verbatim.

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
Name each kept artifact in your results and your `README.md` by its path
RELATIVE to your cwd, and say it stays on the run's volume rather than in the
published repository. Never write an absolute server path into a file that is
published: a reader's machine has none of them.
</disposable_outputs>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<task>
Convert this artifact's Python script into a demo notebook with MINIMAL changes to the original code.
Split into cells, add markdown explanations between sections, add a visualization cell at the end.
Output: mini_demo_data.json + code_demo.ipynb (notebook that loads data from GitHub URL)
</task>

<artifact_info>
id: art_FWy8D4_y9GBn
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
workspace_path: >-
  /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2
out_expected_files:
- eval.py
- full_eval_out.json
- mini_eval_out.json
- preview_eval_out.json
- reproducibility.md
out_demo_files:
- path: eval.py
  description: Evaluation script with metrics computation
</artifact_info>

<github_repo>
Repo URL: https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic
Raw data URL: https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/fork/run_An1uy2kF2SjZ/round-3/evaluation-2/demo/mini_demo_data.json

URLs won't work yet — files pushed to GitHub AFTER notebook creation.
Use local fallback pattern so notebook works locally (now) and in Colab (after deployment).
</github_repo>

<data_file_sizes>
Data files come in three sizes:
- preview_*_out.json — READ THIS to inspect the data structure
- mini_*_out.json (~3 examples) — use for prototyping/testing
- full_*_out.json (complete) — use for the final production run. NEVER open it directly (too large to read into context). Instead, extract values programmatically with shell commands (e.g. grep) or a Python script (use aii-long-running-tasks skill for scripts).
</data_file_sizes>

<install_dependencies_pattern>
Follow the aii-colab skill exactly. It has the install cell pattern, pre-installed package list, numpy 2.0 compat shims, and all Colab-specific rules.
</install_dependencies_pattern>

<data_loading_pattern>
`mini_demo_data.json` = curated subset for the demo.
Use this pattern for Colab compatibility (GitHub URL with local fallback):
```python
GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/fork/run_An1uy2kF2SjZ/round-3/evaluation-2/demo/mini_demo_data.json"
import json
from pathlib import Path

def load_data():
    try:
        import urllib.request
        with urllib.request.urlopen(GITHUB_DATA_URL) as response:
            return json.loads(response.read().decode())
    except Exception: pass
    local = Path("mini_demo_data.json")
    if local.exists(): return json.loads(local.read_text())
    raise FileNotFoundError("Could not load mini_demo_data.json")
```
</data_loading_pattern>

<notebook_structure>
--- Setup ---
Cell 1 (markdown): Title, description, what this artifact does.
Cell 2 (code): Install dependencies — follow the aii-colab skill's install cell pattern exactly. Fill in all packages imported by the artifact's code.
Cell 3 (code): Imports — copy original import block as-is, plus any additional imports needed for the notebook (e.g. matplotlib for visualization).
Cell 4 (code): Data loading helper — use the <data_loading_pattern> above.
Cell 5 (code): `data = load_data()`

--- Config ---
Config cell (code): Define ALL tunable parameters (iterations, epochs, n_samples, hidden_size, etc.) as variables at the top of this cell. Start with the ABSOLUTE MINIMUM values — the smallest that produce any output at all (e.g. 1 iteration, 2 samples, smallest array size). These get gradually increased during testing — see TODOs.

--- Processing ---
Remaining cells: One code cell per logical section of the original script. Add a markdown cell BEFORE each code cell. Copy code as closely as possible, with these changes:
  1. Replace file paths to use the loaded `data` variable.
  2. Use the config variables from the config cell (NOT hardcoded values).
  3. Minimal fixes are allowed if something doesn't work in notebook context (e.g. adjusting paths, removing CLI args, fixing imports), but keep changes to the absolute minimum.

--- Results ---
Visualization cell (code): Print key results in a readable table, plot numeric data with matplotlib if appropriate.
</notebook_structure>

<priority>
WORKING > OPTIMIZED. A small-scale demo that runs correctly is the goal. Once the notebook passes with minimum config values, scale up only if time permits — do NOT spend multiple retries chasing larger parameters. If a working version exists, finish and move on.
</priority>

<max_notebook_total_runtime>600s (10 min)</max_notebook_total_runtime>

<test_environment>
To test-run the notebook in a clean environment (simulating Colab), use the disposable venv at `/tmp/aii_nb_test_envs/art_FWy8D4_y9GBn-4ed788879ab6`. It is on this machine's local disk, outside your workspace, which is on a slow network volume: never create a venv inside your workspace.
```bash
UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_FWy8D4_y9GBn-4ed788879ab6
UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_FWy8D4_y9GBn-4ed788879ab6/bin/python jupyter ipykernel
/tmp/aii_nb_test_envs/art_FWy8D4_y9GBn-4ed788879ab6/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb
```
The timeout is set to <max_notebook_total_runtime>. The entire notebook must finish within this time.
`UV_VENV_CLEAR=1` recreates the venv empty at the start of every test, so each test starts clean. Do NOT delete it yourself: the pipeline removes it after you finish. If you run a test in the background, wait for its result before starting the next test.

What happens: the venv starts with only pip, jupyter and ipykernel. When the notebook's install cell runs, `google.colab` is NOT in sys.modules, so ALL packages get installed — non-Colab packages unconditionally, and Colab packages (numpy, pandas, etc.) at Colab's exact versions via the guard block. The result mirrors Colab's environment as closely as possible. If a cell fails, fix the notebook and re-run.
</test_environment>

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.


<todos>
TODO 1. Read and STRICTLY follow these skills: aii-colab, aii-long-running-tasks.
TODO 2. Read demo file and relevant preview_* files (preview only). Understand script structure: imports, setup, processing, output. Identify ALL tunable parameters (iterations, epochs, n_samples, hidden_size, batch_size, etc.) — these go in the config cell.
TODO 3. Create `mini_demo_data.json`: curated subset from at most ONE dataset (no more than 100 diverse examples). CRITICAL: do NOT read/grep full output file — may crash. Use `head -c 5000` or stream first entries with Python to pick examples.
TODO 4. Create `code_demo.ipynb` via NotebookEdit following <notebook_structure>. Set ALL config parameters to ABSOLUTE MINIMUM values — the smallest that produce any output (e.g. 1 iteration, 2 samples, smallest array sizes). Test-run using <test_environment>. Fix all errors until it passes.
TODO 5. GRADUALLY SCALE (but don't overdo it): increase config params step by step (e.g. ~2x each round). After each increase: test-run, record runtime, fix errors. STOP SCALING as soon as results look meaningful — a working small-scale demo beats a failed large-scale one. If full original params fit within <max_notebook_total_runtime> (10% margin), use them. Otherwise keep whatever works and comment out the true original values. Do NOT spend more than 2-3 scaling rounds.
TODO 6. Verify: (1) code_demo.ipynb contains GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/fork/run_An1uy2kF2SjZ/round-3/evaluation-2/demo/mini_demo_data.json" exactly, (2) mini_demo_data.json exists, (3) uses GitHub URL pattern not just open('mini_demo_data.json').
</todos>

---

Output the result as JSON to: `./.terminal_claude_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "DemoExpectedFiles": {
      "description": "Expected output files from code demo notebook generation.",
      "properties": {
        "notebook": {
          "default": "",
          "description": "Path to the generated demo notebook. Example: 'code_demo.ipynb'",
          "title": "Notebook",
          "type": "string"
        },
        "mini_data_file": {
          "default": "",
          "description": "Path to the mini demo data JSON (curated subset). Example: 'mini_demo_data.json'",
          "title": "Mini Data File",
          "type": "string"
        }
      },
      "title": "DemoExpectedFiles",
      "type": "object"
    }
  },
  "description": "Dataset/experiment/evaluation \u2192 Jupyter notebook demo.\n\nTitle and summary come from the parent artifact (gen_art step),\nnot from the demo agent. The agent only outputs expected files.",
  "properties": {
    "out_expected_files": {
      "$ref": "#/$defs/DemoExpectedFiles",
      "description": "All output files you created. Must include the demo notebook."
    }
  },
  "required": [],
  "title": "CodeDemo",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `./.terminal_claude_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [3] HUMAN-USER prompt · 2026-09-25 16:30:58 UTC

```
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
```

### [4] TOOL CALL — Skill · 2026-09-25 16:31:02 UTC

```
aii-colab
```

### [5] TOOL CALL — Skill · 2026-09-25 16:31:02 UTC

```
aii-long-running-tasks
```

### [6] TOOL RESULT — Skill · 2026-09-25 16:31:02 UTC

```
{"success": true, "commandName": "aii-colab"}
```

### [7] TOOL RESULT — Skill · 2026-09-25 16:31:02 UTC

```
{"success": true, "commandName": "aii-long-running-tasks"}
```

### [8] TOOL CALL — Bash · 2026-09-25 16:31:06 UTC

```
cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_FWy8D4_y9GBn; ls -la; ls -la .aii; W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2; ls -la $W; du -sh $W/*; wc -l $W/eval.py; cat $W/reproducibility.md | head -80
```

### [9] TOOL RESULT — Bash · 2026-09-25 16:31:06 UTC

````
{"stdout": "total 2966\ndrwxr-xr-x 3 root root 1003066 Sep 25 16:30 .\ndrwxr-xr-x 6 root root 2000120 Sep 25 16:30 ..\ndrwxr-xr-x 2 root root       1 Sep 25 16:30 .aii\n-rw------- 1 root root      54 Sep 25 16:30 .aii_claude_session.json\n-rw-r--r-- 1 root root   31348 Sep 25 16:31 .repl_agent.ptylog\ntotal 981\ndrwxr-xr-x 2 root root       1 Sep 25 16:30 .\ndrwxr-xr-x 3 root root 1003066 Sep 25 16:30 ..\ntotal 26037\ndrwxr-xr-x 12 root root 2005008 Sep 24 06:57 .\ndrwxr-xr-x  7 root root 3000107 Sep 24 01:33 ..\ndrwxr-xr-x  2 root root   98200 Sep 24 03:25 .aii\n-rw-------  1 root root      54 Sep 24 03:16 .aii_claude_session.json\n-rw-------  1 root root    7434 Sep 24 03:25 .aii_worker_result.json\n-rw-r--r--  1 root root  221720 Sep 24 03:25 .repl_agent.ptylog\n-rw-r--r--  1 root root    2767 Sep 24 03:23 .terminal_claude_agent_struct_out.json\n-rw-r--r--  1 root root   15340 Sep 24 03:15 README.md\ndrwxr-xr-x  2 root root 1001905 Sep 24 03:14 audit\n-rw-r--r--  1 root root   24856 Sep 24 03:15 eval.py\n-rw-r--r--  1 root root 2970006 Sep 24 03:21 eval_out.json\ndrwxr-xr-x  2 root root 1068840 Sep 24 01:58 figures\n-rw-r--r--  1 root root 3215695 Sep 24 03:21 full_eval_out.json\ndrwxr-xr-x  3 root root 2002556 Sep 24 02:00 inputs_copy\ndrwxr-xr-x  2 root root 1008397 Sep 24 03:17 logs\n-rw-r--r--  1 root root   45660 Sep 24 03:21 mini_eval_out.json\n-rw-r--r--  1 root root 3597729 Sep 24 03:18 pairwise_classes_E.jsonl\n-rw-r--r--  1 root root    5707 Sep 24 03:18 prereg_mech.json\n-rw-r--r--  1 root root      83 Sep 24 03:18 prereg_mech.sha256\n-rw-r--r--  1 root root   36997 Sep 24 03:21 preview_eval_out.json\n-rw-r--r--  1 root root    1067 Sep 24 03:12 pyproject.toml\n-rw-r--r--  1 root root      27 Sep 24 01:55 pytest.ini\n-rw-r--r--  1 root root    5950 Sep 24 03:15 reproducibility.md\ndrwxr-xr-x  5 root root 2001292 Sep 24 03:07 results\ndrwxr-xr-x  2 root root 1014251 Sep 24 23:37 src\ndrwxr-xr-x  2 root root 1026193 Sep 24 02:00 tables\ndrwxr-xr-x  2 root root 1000310 Sep 24 06:57 tests\n-rw-r--r--  1 root root  220888 Sep 24 03:12 uv.lock\ndrwxr-xr-x  7 root root 1054970 Sep 24 23:37 vendor_exp5\n15K\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/README.md\n998K\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/audit\n25K\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/eval.py\n2.9M\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/eval_out.json\n1.7M\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/figures\n3.1M\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/full_eval_out.json\n63M\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/inputs_copy\n1.1M\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/logs\n45K\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/mini_eval_out.json\n3.5M\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/pairwise_classes_E.jsonl\n6.0K\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/prereg_mech.json\n512\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/prereg_mech.sha256\n37K\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/preview_eval_out.json\n1.5K\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/pyproject.toml\n512\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/pytest.ini\n6.0K\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/reproducibility.md\n20M\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/results\n1.2M\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src\n1.3M\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/tables\n981K\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/tests\n216K\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/uv.lock\n6.4M\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/vendor_exp5\n383 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/eval.py\n# Reproducing this artifact (consensus-mechanism audit, T4 on dataset E, plus the verified record)\n\nThese are the steps that were actually run to produce the files in this folder (2026-09-24). It is CPU only. **No API keys are needed and no LLM calls are made.**\n\n## 1. Get the folder\n\n```bash\ncp -r /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2 ~/work/consensus_audit\ncd ~/work/consensus_audit\n```\n\nThe code reads its **inputs by absolute path** (`src/paths.py`: `RUN = /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop`). The inputs are:\n- exp 5 (`iter_2/gen_art/gen_art_experiment_5`)\n- exp 6 (`iter_2/gen_art/gen_art_experiment_6`)\n- dataset E (`iter_1/gen_art/gen_art_dataset_1`, whose 27.7 MB `full_data_out.json` and `raw/generations.jsonl` are not copied)\n- datasets 2 and 3 and evaluation 1 (`iter_2/gen_art/...`)\n- the reviewer audit (`iter_2/review_report/review_report/audit/`)\n- iteration-1 exp 1, 3 and 4\n\nEvery input smaller than 10 MB is mirrored under `inputs_copy/3_invention_loop/...`, with its sha256 in `tables/source_hashes.csv`. On another machine, either recreate that directory tree at the same absolute path, or edit `RUN` in `src/paths.py`. The vendored exp-5 scoring code is in `vendor_exp5/`, and its hashes are checked identical to the source.\n\n## 2. Environment (as used)\n\n- OS: Debian 12 container (Ubuntu works the same), Linux 6.8, **4 vCPU (AMD EPYC 9655P), 29 GB RAM cgroup limit, no GPU**.\n- Python **3.12.14**, installed with `uv` (no system packages beyond `uv`).\n\n```bash\nuv venv .venv --python=3.12\nuv pip install --python .venv/bin/python -r pyproject.toml\n```\n\n`pyproject.toml` pins all 32 packages to the versions installed (from `uv pip freeze`). The key ones:\n- `z3-solver==5.1.0.0` (identical to exp 5; a different z3 can flip eqmv outcomes and break gate G2)\n- `numpy==2.5.3`, `pandas==3.0.6`, `scipy==1.18.1`, `scikit-learn==1.9.1`, `statsmodels==0.15.0`, `loguru==0.7.3`\n- `matplotlib`, `pyyaml`, `psutil` and `pytest` are pinned as well\n\nNo data, model or checkpoint downloads. No environment variables are required. `eval.py` sets `PYTHONHASHSEED=0` itself by re-executing, because eqmv's aligner iterates hashed sets.\n\n## 3. Commands that were run, in order\n\n```bash\nuv run pytest -q tests                            # 23 passed (~25 s)\n.venv/bin/python eval.py --stage all              # ~5 min wall on 4 vCPU:\n#   src/copy_inputs.py      -> inputs_copy/, tables/source_hashes.csv\n#   src/run_matrix.py rab   -> 292 R_AB sentences, 4 spawn workers, ~30 s\n#   src/run_matrix.py rest  -> remaining 408 sentences, ~70 s       => results/pair_matrix_E.jsonl (700 sentences, 29,107 pairs)\n#   PART A (src/part_a.py)  -> gates G0/G1/G2, prereg_mech.json(+sha256), pairwise_classes_E.jsonl, cuts, M1/M2/NET/SCATTER/M3/M4 (~4.5 min)\n#   PART B (src/record.py)  -> verified-record tables (~10 s)\n#   audit/rederive.py, audit/m2_specificity.py -> audit/*.json (~1.5 min)\n#   figures + eval_out.json\n.venv/bin/python eval.py --stage all --skip-matrix   # the final run: reuses the matrix, re-runs every analysis + audits\npython /ai-inventor/.claude/skills/aii-json/scripts/aii_json_format_mini_preview.py --input eval_out.json   # full_/mini_/preview_\npython /ai-inventor/.claude/skills/aii-json/scripts/aii_json_validate_schema.py --format exp_eval_sol_out --file $PWD/eval_out.json\n```\n\nSeeds are fixed throughout:\n- the sentence-cluster bootstrap uses `numpy.random.default_rng(0)` with B = 2000;\n- the M4 draws use `sha1('M4|'+row_key+'|'+k+'|'+j)` with 50 draws per k;\n- the M3 tie-break uses `sha1('M3|'+row_key)`;\n- the audits use `default_rng(7/11/123)`.\n\nThe matrix is deterministic: three independent computations gave 0 differing pairs out of 29,107 (`results/matrix_determinism_check.json`). The matrix stage is resumable. It skips sentences already in `results/pair_matrix_E.jsonl`, so move that file away to recompute it.\n\n## 4. What you should get\n\nEverything below is in `eval_out.json` → `metrics_agg` / `metadata.verdicts`, `results/part_a.json`, and `tables/*.csv`.\n\n- **Gates:**\n  - G0: R_AB n = 2686 (1822 ERROR / 864 CORRECT, 292 sentences); R_A L20+EXC = 449 (261/188).\n  - G1: frozen c_score_align AUROC 0.7824 (R_AB) and 0.8599 (R_A L20+EXC).\n  - G2: mismatch rate 0.00325 (24 of 7,383 rows).\n- **Decomposition, R_AB (2,672 scorable rows):**\n  - END_MAJ: e = 0.124, d = 0.537, AUROC_b = 0.669.\n  - Graded c_score_align: 0.784; Δ = +0.114 [0.091, 0.140].\n  - c_score_exact: 0.748.\n  - `tables/ed_decomposition_cuts.csv` and `figures/fig1_e_d_by_complexity.*` hold the cuts.\n- **Verdicts:**\n  - M1 INCONCLUSIVE (n_conditions partial slope −0.04 [−0.53, 0.45]).\n  - M2 CONFIRMED (+1.95 [1.12, 2.77]) but **non-specific**: the shuffled-label placebo also gives a positive slope, and the label×words interaction is −0.29 [−0.77, 0.20]. See `audit/m2_specificity.json`.\n  - NET: DEGRADES with length, Δ(e+d) = +0.356 [0.198, 0.493], driven by d. Its placebo gives −0.034 [−0.108, 0.034].", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
````

### [10] TOOL CALL — Bash · 2026-09-25 16:31:10 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2; cat $W/eval.py; ls -la $W/src $W/vendor_exp5 $W/results $W/tables; wc -l $W/src/*.py
```

### [11] TOOL RESULT — Bash · 2026-09-25 16:31:10 UTC

```
{"stdout": "#!/usr/bin/env python3\n\"\"\"Consensus mechanism audit + verified record (iteration 3, T4 on dataset E). CPU only, $0, no LLM calls.\n\nusage: uv run eval.py --stage mini|rab|all [--skip-matrix]\n  mini : 12-sentence matrix smoke test only\n  rab  : matrix for the 292 R_AB sentences, then every analysis\n  all  : matrix for all 700 E sentences (R_AB first), then every analysis\nOutputs: results/ (matrix, part_a.json), tables/*.csv, figures/*, pairwise_classes_E.js... [truncated, 32217 chars total]
```

### [12] TOOL CALL — Read · 2026-09-25 16:31:12 UTC

```
/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/eval.py
```

### [13] TOOL RESULT — Read · 2026-09-25 16:31:12 UTC

```
{"type": "text", "file": {"filePath": "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/eval.py", "content": "#!/usr/bin/env python3\n\"\"\"Consensus mechanism audit + verified record (iteration 3, T4 on dataset E). CPU only, $0, no LLM calls.\n\nusage: uv run eval.py --stage mini|rab|all [--skip-matrix]\n  mini : 12-sentence matrix smoke test only\n  rab  : matrix for the 292 R_AB sentences, then every analysis\n  all  : matrix ... [truncated, 26840 chars total]
```

### [14] TOOL CALL — Bash · 2026-09-25 16:31:16 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2; ls -la $W/src $W/results $W/tables $W/audit; wc -l $W/src/*.py; grep -n "^def \|^class " $W/src/*.py
```

### [15] TOOL RESULT — Bash · 2026-09-25 16:31:18 UTC

```
{"stdout": "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/audit:\ntotal 2957\ndrwxr-xr-x  2 root root 1001905 Sep 24 03:14 .\ndrwxr-xr-x 12 root root 2005008 Sep 24 06:57 ..\n-rw-r--r--  1 root root     897 Sep 24 03:21 m2_specificity.json\n-rw-r--r--  1 root root    2530 Sep 24 03:14 m2_specificity.py\n-rw-r--r--  1 root root    3928 Sep 24 03:21 rederive.json\n-rw-r--r--  1 root root   12158 Sep 24 03:13 rederive.py\n\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/results:\ntotal 15150\ndrwxr-xr-x  5 root root 2001292 Sep 24 03:07 .\ndrwxr-xr-x 12 root root 2005008 Sep 24 06:57 ..\ndrwxr-xr-x  2 root root 1006320 Sep 24 01:49 diag\n-rw-r--r--  1 root root  383474 Sep 24 03:20 frame_min.pkl\n-rw-r--r--  1 root root     272 Sep 24 03:07 matrix_determinism_check.json\n-rw-r--r--  1 root root     112 Sep 24 03:02 matrix_stage_rab.json\n-rw-r--r--  1 root root     113 Sep 24 03:03 matrix_stage_rest.json\n-rw-r--r--  1 root root 3495885 Sep 24 03:03 pair_matrix_E.jsonl\n-rw-r--r--  1 root root  120904 Sep 24 03:20 part_a.json\n-rw-r--r--  1 root root 1453221 Sep 24 03:20 population_RAB.pkl\ndrwxr-xr-x  2 root root 2000333 Sep 24 02:00 prev_run\ndrwxr-xr-x  2 root root 2000333 Sep 24 03:01 prev_run2\n-rw-r--r--  1 root root 1042757 Sep 24 03:20 rab_all.pkl\n\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src:\ntotal 3094\ndrwxr-xr-x  2 root root 1014251 Sep 24 23:37 .\ndrwxr-xr-x 12 root root 2005008 Sep 24 06:57 ..\n-rw-r--r--  1 root root    7296 Sep 24 01:39 consensus_mx.py\n-rw-r--r--  1 root root    3411 Sep 24 02:00 copy_inputs.py\n-rw-r--r--  1 root root    6476 Sep 24 03:00 frame.py\n-rw-r--r--  1 root root   10745 Sep 24 02:59 m4.py\n-rw-r--r--  1 root root   25039 Sep 24 03:00 mechanism.py\n-rw-r--r--  1 root root    4232 Sep 24 01:36 pairwise.py\n-rw-r--r--  1 root root   26487 Sep 24 01:54 part_a.py\n-rw-r--r--  1 root root     929 Sep 24 01:36 paths.py\n-rw-r--r--  1 root root   51228 Sep 24 01:59 record.py\n-rw-r--r--  1 root root    5578 Sep 24 01:36 run_matrix.py\n-rw-r--r--  1 root root    4517 Sep 24 01:42 stats.py\n\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/tables:\ntotal 3232\ndrwxr-xr-x  2 root root 1026193 Sep 24 02:00 .\ndrwxr-xr-x 12 root root 2005008 Sep 24 06:57 ..\n-rw-r--r--  1 root root    2050 Sep 24 03:20 b2_dead_end.csv\n-rw-r--r--  1 root root    4890 Sep 24 03:20 corrections.csv\n-rw-r--r--  1 root root    5576 Sep 24 03:20 coverage_vs_request.csv\n-rw-r--r--  1 root root   66979 Sep 24 03:18 ed_decomposition_cuts.csv\n-rw-r--r--  1 root root    3650 Sep 24 03:20 exp6_COVERAGE_pooled.csv\n-rw-r--r--  1 root root    1701 Sep 24 03:20 exp6_Per_stratum_R_AB_AUROC.csv\n-rw-r--r--  1 root root    3655 Sep 24 03:20 exp6_R_AB_long_L25_L20_EXC.csv\n-rw-r--r--  1 root root    3640 Sep 24 03:20 exp6_R_AB_pooled.csv\n-rw-r--r--  1 root root    3657 Sep 24 03:20 exp6_R_A_pooled_L20_EXC_CTRL.csv\n-rw-r--r--  1 root root    1152 Sep 24 03:20 exp6_complexity_gee.csv\n-rw-r--r--  1 root root     407 Sep 24 03:20 exp6_contamination_DiD.csv\n-rw-r--r--  1 root root    2870 Sep 24 03:20 exp6_deviations.csv\n-rw-r--r--  1 root root     562 Sep 24 03:20 exp6_frame_284.csv\n-rw-r--r--  1 root root    1775 Sep 24 03:20 exp6_system_level.csv\n-rw-r--r--  1 root root   47686 Sep 24 03:20 function_inventory.csv\n-rw-r--r--  1 root root    1699 Sep 24 03:17 g2_mismatches.csv\n-rw-r--r--  1 root root    2410 Sep 24 03:18 graded_trace_c_score_align.csv\n-rw-r--r--  1 root root    2215 Sep 24 03:18 graded_trace_c_score_exact.csv\n-rw-r--r--  1 root root   14806 Sep 24 03:20 hypothesis_verdicts.csv\n-rw-r--r--  1 root root    4567 Sep 24 03:20 label_facts.csv\n-rw-r--r--  1 root root    2079 Sep 24 03:20 m4_auroc_k_cost.csv\n-rw-r--r--  1 root root    1486 Sep 24 03:20 m4_fixed_pools_k2.csv\n-rw-r--r--  1 root root    3361 Sep 24 03:20 m4_fixed_pools_k3.csv\n-rw-r--r--  1 root root    4696 Sep 24 03:20 m4_fixed_pools_k4.csv\n-rw-r--r--  1 root root    1629 Sep 24 03:20 m4_lofo.csv\n-rw-r--r--  1 root root    3146 Sep 24 03:20 perturb_counts.csv\n-rw-r--r--  1 root root    6010 Sep 24 03:20 pt_vs_s4_rerun.csv\n-rw-r--r--  1 root root    4956 Sep 24 03:20 radj_gate.csv\n-rw-r--r--  1 root root    2524 Sep 24 03:20 regimes_R_PANEL.csv\n-rw-r--r--  1 root root   25872 Sep 24 03:19 scatter_sentence_table.csv\n-rw-r--r--  1 root root   36514 Sep 24 03:17 source_hashes.csv\n   187 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/consensus_mx.py\n    60 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/copy_inputs.py\n   120 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/frame.py\n   197 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/m4.py\n   441 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/mechanism.py\n   109 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/pairwise.py\n   379 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/part_a.py\n    25 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/paths.py\n   654 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/record.py\n   129 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/run_matrix.py\n   125 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/stats.py\n  2426 total\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/consensus_mx.py:15:class SentenceMatrix:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/consensus_mx.py:97:def row_consensus(sm: SentenceMatrix, row_key: str, family_key: str = \"family\") -> dict | None:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/consensus_mx.py:165:def c_from_fams(fam_stats: dict, fams, exact: bool = False) -> float | None:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/consensus_mx.py:174:def pairwise_class_line(sm: SentenceMatrix, zver: str, code_sha: str) -> dict:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/consensus_mx.py:185:def safe_mean(x):\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/copy_inputs.py:35:def main():\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/frame.py:18:def regime(r: dict, which: str) -> int | None:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/frame.py:32:def build_frame() -> tuple[pd.DataFrame, dict]:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/frame.py:90:def gates_G0_G1(df: pd.DataFrame) -> dict:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/m4.py:21:def _draw(row_key: str, k: int, j: int, fams: list[str]) -> list[str]:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/m4.py:26:def auroc_k(P: pd.DataFrame, boot: SentBoot, fam_col: str, all_fams: list[str], k_max: int, primary: bool = True,\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/m4.py:82:def pool_scores(P: pd.DataFrame, fam_col: str, pool: tuple, neutral: float) -> np.ndarray:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/m4.py:91:def fixed_pools(P: pd.DataFrame, fam_col: str, all_fams: list[str], neutral: float, size: int, fold: np.ndarray) -> dict:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/m4.py:115:def lofo(P: pd.DataFrame, boot: SentBoot, fam_col: str, all_fams: list[str], neutral: float, judge_bar: float) -> dict:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/m4.py:145:def cost_table(gen_path, fam_map: dict, pair_secs: np.ndarray, rows_per_family: float, k_max: int, frontier: dict,\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/mechanism.py:26:def ed_decomposition(y, endorsed) -> dict:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/mechanism.py:39:def normalise_name(s: str) -> str:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/mechanism.py:44:def make_bins(df: pd.DataFrame, cut: dict) -> pd.DataFrame:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/mechanism.py:57:def prereg_cuts(rab: pd.DataFrame) -> dict:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/mechanism.py:69:def cell_stats(sub: pd.DataFrame, ycol: str, rule_cols: dict, boot: SentBoot, W_all: np.ndarray, pos: np.ndarray,\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/mechanism.py:106:def run_cuts(P: pd.DataFrame, boot: SentBoot, regimes: dict, rule_cols: dict) -> pd.DataFrame:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/mechanism.py:127:def graded_trace(y, c) -> dict:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/mechanism.py:154:def gee_fit(data: pd.DataFrame, formula: str, groups: str = \"sentence_id\") -> dict:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/mechanism.py:180:def vif_table(data: pd.DataFrame, cols: list[str], strat: bool = True) -> dict:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/mechanism.py:188:def verdict_slope(coef: dict | None, key: str, want: str) -> str:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/mechanism.py:197:def zcols(d: pd.DataFrame) -> pd.DataFrame:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/mechanism.py:204:def mechanism_M1_M2(P: pd.DataFrame, rule_cols: dict) -> dict:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/mechanism.py:244:def _ame(X: np.ndarray, yv: np.ndarray, w: np.ndarray, j: int) -> float:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/mechanism.py:250:def net_test(P: pd.DataFrame, boot: SentBoot, col: str = \"end_MAJ\", long_only: bool = False) -> dict:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/mechanism.py:301:def scatter_index(P_lab: pd.DataFrame, sms: dict, cut: dict, boot_seed: int = 0, B: int = 2000) -> dict:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/mechanism.py:387:def m3_local(P: pd.DataFrame, boot: SentBoot, exp6_judge_slope) -> dict:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/pairwise.py:32:class _TO(Exception):\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/pairwise.py:36:def _alarm(signum, frame):  # noqa: ARG001\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/pairwise.py:40:def init_worker(mem_gb: float = 3.5) -> None:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/pairwise.py:50:def _with_alarm(secs: int, fn, *a, **kw):\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/pairwise.py:61:def pairwise_matrix(rows: list[dict], eqmv_ms: int = EQMV_MS, pair_cap_s: int = PAIR_CAP_S) -> dict:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/pairwise.py:94:def work(task: dict) -> dict:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/pairwise.py:104:def code_sha() -> str:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/part_a.py:31:def jdump(p, o):\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/part_a.py:35:def write_csv(df: pd.DataFrame, name: str, sources: list[str]):\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/part_a.py:44:def write_prereg(cut: dict) -> dict:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/part_a.py:101:def vocab_exact(df: pd.DataFrame, trusted: list[str]) -> pd.DataFrame:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/part_a.py:128:def run(stage: str = \"all\") -> dict:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/paths.py:20:def jl(p: Path) -> list[dict]:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/paths.py:24:def sha256_file(p: Path) -> str:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/record.py:27:def write_csv(df: pd.DataFrame, name: str, sources: list[str]):\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/record.py:34:def get(obj, path: str, default=NIF):\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/record.py:56:def J(p: Path):\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/record.py:61:def md_tables(md: str) -> dict[str, pd.DataFrame]:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/record.py:84:def _slug(s: str) -> str:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/record.py:88:def exp6_tables() -> dict:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/record.py:170:def radj_gate() -> pd.DataFrame:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/record.py:217:def _f(x):\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/record.py:225:def pt_vs_s4() -> dict:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/record.py:318:def corrections() -> pd.DataFrame:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/record.py:399:def regimes_panel() -> pd.DataFrame:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/record.py:423:def hypothesis_verdicts(A: dict, pts: dict, lab: pd.DataFrame) -> pd.DataFrame:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/record.py:533:def coverage_vs_request() -> pd.DataFrame:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/record.py:563:def function_inventory() -> pd.DataFrame:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/record.py:592:def perturb_counts() -> dict:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/record.py:619:def label_facts(df_frame: pd.DataFrame, radj: pd.DataFrame) -> pd.DataFrame:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/run_matrix.py:39:def detect_cpus() -> int:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/run_matrix.py:52:def in_rab(L: dict) -> bool:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/run_matrix.py:58:def build_tasks() -> tuple[list[dict], set]:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/run_matrix.py:76:def main():\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/stats.py:13:def auc(y, s) -> float:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/stats.py:25:def strat_auc(y, s, strata) -> float:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/stats.py:39:class ClusterBoot:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/stats.py:53:def ci(vals, lo=2.5, hi=97.5):\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/stats.py:60:def boot_stat(boot: ClusterBoot, fn) -> list:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/stats.py:65:class WAuc:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/stats.py:84:class WStratAuc:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/stats.py:106:class SentBoot:", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [16] ASSISTANT · 2026-09-25 16:31:24 UTC

```
Reading the original evaluation code (`eval.py` plus its `src/` helpers) to decide which parts can run from a small data subset.
```

### [17] TOOL CALL — Bash · 2026-09-25 16:31:24 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2; cat $W/src/stats.py; sed -n 1,160p $W/src/mechanism.py; sed -n 250,300p $W/src/mechanism.py
```

### [18] TOOL RESULT — Bash · 2026-09-25 16:31:24 UTC

```
{"stdout": "\"\"\"Statistics shared by every analysis: tie-aware AUROC, stratified (within-stratum pair) AUROC, and a\nsentence-cluster bootstrap that yields resample index arrays (numpy default_rng(0), B=2000).\"\"\"\nfrom __future__ import annotations\n\nfrom collections import defaultdict\n\nimport numpy as np\nfrom scipy.stats import rankdata\n\nB_DEFAULT = 2000\n\n\ndef auc(y, s) -> float:\n    \"\"\"Mann-Whitney AUROC with ties = 0.5 (identical to sklearn roc_auc_score).\"\"\"\n    y = np.asarray(y, dtype=float)\n    s = np.asarray(s, dtype=float)\n    n1 = int(y.sum())\n    n0 = len(y) - n1\n    if n1 == 0 or n0 == 0:\n        return float(\"nan\")\n    r = rankdata(s)\n    return float((r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))\n\n\ndef strat_auc(y, s, strata) -> float:\n    \"\"\"Within-stratum pair AUROC: sum_s w_s AUROC_s with w_s = n_err,s * n_cor,s (exp 5 'stratified').\"\"\"\n    y, s, strata = np.asarray(y, float), np.asarray(s, float), np.asarray(strata)\n    num = den = 0.0\n    for st in np.unique(strata):\n        m = strata == st\n        n1 = int(y[m].sum())\n        n0 = int(m.sum()) - n1\n        if n1 and n0:\n            num += auc(y[m], s[m]) * n1 * n0\n            den += n1 * n0\n    return num / den if den else float(\"nan\")\n\n\nclass ClusterBoot:\n    \"\"\"Sentence-cluster bootstrap resamples (sentence_ids drawn with replacement; all rows of a drawn sentence kept).\"\"\"\n\n    def __init__(self, sids, b: int = B_DEFAULT, seed: int = 0):\n        by = defaultdict(list)\n        for i, s in enumerate(sids):\n            by[s].append(i)\n        keys = sorted(by)\n        arr = [np.array(by[k]) for k in keys]\n        rng = np.random.default_rng(seed)\n        self.idx = [np.concatenate([arr[j] for j in rng.integers(0, len(keys), len(keys))]) for _ in range(b)]\n        self.n_clusters = len(keys)\n\n\ndef ci(vals, lo=2.5, hi=97.5):\n    v = np.asarray([x for x in vals if x is not None and not np.isnan(x)], float)\n    if len(v) == 0:\n        return [None, None]\n    return [float(np.percentile(v, lo)), float(np.percentile(v, hi))]\n\n\ndef boot_stat(boot: ClusterBoot, fn) -> list:\n    return [fn(ix) for ix in boot.idx]\n\n\n# ------------------------------------------------------------------ weighted (bootstrap-count) statistics\nclass WAuc:\n    \"\"\"AUROC under row weights (bootstrap multiplicities); ties = 0.5. Precomputes the score ranking once.\"\"\"\n\n    def __init__(self, y, s):\n        self.y = np.asarray(y, float)\n        vals, self.inv = np.unique(np.asarray(s, float), return_inverse=True)\n        self.nv = len(vals)\n\n    def __call__(self, w) -> float:\n        w = np.asarray(w, float)\n        W1 = np.bincount(self.inv, weights=w * self.y, minlength=self.nv)\n        W0 = np.bincount(self.inv, weights=w * (1 - self.y), minlength=self.nv)\n        den = W1.sum() * W0.sum()\n        if den <= 0:\n            return float(\"nan\")\n        cum0 = np.cumsum(W0) - W0\n        return float((W1 * (cum0 + 0.5 * W0)).sum() / den)\n\n\nclass WStratAuc:\n    \"\"\"Within-stratum pair AUROC under row weights.\"\"\"\n\n    def __init__(self, y, s, strata):\n        self.y = np.asarray(y, float)\n        strata = np.asarray(strata)\n        self.parts = [(np.where(strata == st)[0], WAuc(self.y[strata == st], np.asarray(s, float)[strata == st]))\n                      for st in np.unique(strata)]\n\n    def __call__(self, w) -> float:\n        w = np.asarray(w, float)\n        num = den = 0.0\n        for ix, wa in self.parts:\n            ww = w[ix]\n            n1 = (ww * self.y[ix]).sum()\n            n0 = (ww * (1 - self.y[ix])).sum()\n            if n1 > 0 and n0 > 0:\n                num += wa(ww) * n1 * n0\n                den += n1 * n0\n        return num / den if den else float(\"nan\")\n\n\nclass SentBoot:\n    \"\"\"Sentence-cluster bootstrap as multiplicity weights: W[b, i] = #times row i's sentence was drawn in replicate b\n    (numpy default_rng(seed); sentence_ids resampled with replacement).\"\"\"\n\n    def __init__(self, sids, b: int = B_DEFAULT, seed: int = 0):\n        sids = np.asarray(sids)\n        self.keys, self.sent_ix = np.unique(sids, return_inverse=True)\n        S = len(self.keys)\n        rng = np.random.default_rng(seed)\n        self.C = np.stack([np.bincount(rng.integers(0, S, S), minlength=S) for _ in range(b)]).astype(float)\n        self.B = b\n\n    def weights(self, b: int, mask=None):\n        w = self.C[b][self.sent_ix]\n        return w if mask is None else w[mask]\n\n    def W(self, mask=None):\n        \"\"\"(B, n_rows[mask]) weight matrix.\"\"\"\n        W = self.C[:, self.sent_ix]\n        return W if mask is None else W[:, mask]\n\"\"\"PART 2 + STEP 4: exact decomposition AUROC_b = 1 - (e + d)/2 of binary cross-family consensus, its cuts, the graded\ntrace, the VOCAB_EXACT aligner-free control, and the mechanism tests M1 / M2 / NET / SCATTER / M3-local.\n\ned_decomposition(y, endorsed) is the reusable function (iteration 4 applies it unchanged to R_COMP).\"\"\"\nfrom __future__ import annotations\n\nimport re\nimport warnings\nfrom collections import Counter, defaultdict\n\nimport numpy as np\nimport pandas as pd\nimport statsmodels.api as sm\nimport statsmodels.formula.api as smf\nfrom loguru import logger\nfrom sklearn.linear_model import LogisticRegression\nfrom statsmodels.stats.outliers_influence import variance_inflation_factor\n\nfrom stats import SentBoot, WAuc, WStratAuc, auc, ci, strat_auc\n\nRULES = [\"MAJ\", \"PLUR\", \"FAM2\", \"FAMMAJ\", \"MAJ_EXACT\"]\nMIN_ROWS, MIN_SENT = 30, 10\n\n\n# =================================================================================================== identity\ndef ed_decomposition(y, endorsed) -> dict:\n    \"\"\"y: 1 = ERROR, 0 = CORRECT; endorsed: 1 = the cross-family peer rule endorses the candidate.\n    Returns e = P(endorsed | ERROR) (error-endorsement), d = P(not endorsed | CORRECT) (correct-divergence) and\n    AUROC_b of b = 1 - endorsed, asserting the bookkeeping identity AUROC_b = 1 - (e + d)/2 (balanced accuracy).\"\"\"\n    y = np.asarray(y, int)\n    en = np.asarray(endorsed, int)\n    e = float(en[y == 1].mean())\n    d = float((1 - en[y == 0]).mean())\n    a = auc(y, 1 - en)\n    assert abs(a - (1 - (e + d) / 2)) < 1e-12, (a, e, d)\n    return {\"n_err\": int((y == 1).sum()), \"n_cor\": int((y == 0).sum()), \"e\": e, \"d\": d, \"auroc_b\": a}\n\n\ndef normalise_name(s: str) -> str:\n    return re.sub(r\"[^a-z0-9]\", \"\", s.lower())\n\n\n# =================================================================================================== bins\ndef make_bins(df: pd.DataFrame, cut: dict) -> pd.DataFrame:\n    q1, q2 = cut[\"words_tercile_cuts\"]\n    df = df.copy()\n    df[\"words_t\"] = np.where(df.words <= q1, \"T1\", np.where(df.words <= q2, \"T2\", \"T3\"))\n    nc = df.n_conditions.fillna(-1).astype(int)\n    df[\"ncond_bin\"] = np.where(nc <= 1, \"0-1\", np.where(nc == 2, \"2\", np.where(nc == 3, \"3\", \"4+\")))\n    et = df.exception_type.fillna(\"none\").astype(str)\n    keep = set(cut[\"exception_types_kept\"])\n    df[\"exc_bin\"] = np.where(et == \"none\", \"none\", np.where(et.isin(keep), et, \"other_exc\"))\n    df[\"long\"] = df.stratum.isin([\"L25\", \"L20\", \"EXC\"])\n    return df\n\n\ndef prereg_cuts(rab: pd.DataFrame) -> dict:\n    sent = rab.drop_duplicates(\"sentence_id\")\n    q1, q2 = np.quantile(sent.words.values, [1 / 3, 2 / 3])\n    et = rab.exception_type.fillna(\"none\").astype(str)\n    cnt = Counter(et[et != \"none\"])\n    return {\"words_tercile_cuts\": [float(q1), float(q2)], \"words_tercile_rule\": \"T1: words<=q1, T2: q1<words<=q2, T3: >q2; \"\n            \"cut points = 1/3, 2/3 quantiles of R_AB SENTENCE words (np.quantile, linear)\",\n            \"n_conditions_bins\": [\"0-1\", \"2\", \"3\", \"4+\"], \"exception_types_kept\": sorted(k for k, v in cnt.items() if v >= 30),\n            \"exception_type_counts_R_AB_rows\": dict(cnt)}\n\n\n# =================================================================================================== cuts\ndef cell_stats(sub: pd.DataFrame, ycol: str, rule_cols: dict, boot: SentBoot, W_all: np.ndarray, pos: np.ndarray,\n               score_col: str = \"c_frozen\") -> list[dict]:\n    \"\"\"e, d, AUROC_b per rule and AUROC(score) for one cell, with sentence-cluster bootstrap CIs.\"\"\"\n    y = sub[ycol].values.astype(int)\n    n1, n0 = int(y.sum()), int((1 - y).sum())\n    nsent = sub.sentence_id.nunique()\n    W = W_all[:, pos]\n    ok_e = n1 >= MIN_ROWS and nsent >= MIN_SENT\n    ok_d = n0 >= MIN_ROWS and nsent >= MIN_SENT\n    out = []\n    a_c = auc(y, sub[score_col].values) if n1 and n0 else float(\"nan\")\n    a_c_ci = [None, None]\n    if ok_e and ok_d:\n        wa = WAuc(y, sub[score_col].values)\n        a_c_ci = ci([wa(W[b]) for b in range(W.shape[0])])\n    for rule, col in rule_cols.items():\n        en = sub[col].values.astype(float)\n        if np.isnan(en).any():\n            m = ~np.isnan(en)\n            logger.warning(f\"rule {rule}: {int((~m).sum())} rows without a value dropped in cell\")\n        e = float(en[y == 1].mean()) if n1 else float(\"nan\")\n        d = float((1 - en[y == 0]).mean()) if n0 else float(\"nan\")\n        ab = 1 - (e + d) / 2 if n1 and n0 else float(\"nan\")\n        if n1 and n0:\n            assert abs(ab - auc(y, 1 - en)) < 1e-12\n        rec = {\"rule\": rule, \"n_err\": n1, \"n_cor\": n0, \"n_sent\": nsent, \"e\": e, \"d\": d, \"auroc_b\": ab, \"auroc_c\": a_c,\n               \"auroc_c_ci\": a_c_ci, \"inference\": \"tested\" if (ok_e and ok_d) else (\"partial\" if (ok_e or ok_d) else \"descriptive\")}\n        with np.errstate(invalid=\"ignore\", divide=\"ignore\"):\n            eb = (W @ (en * y)) / (W @ y) if ok_e else None\n            db = (W @ ((1 - en) * (1 - y))) / (W @ (1 - y)) if ok_d else None\n        rec[\"e_ci\"] = ci(eb) if eb is not None else [None, None]\n        rec[\"d_ci\"] = ci(db) if db is not None else [None, None]\n        rec[\"auroc_b_ci\"] = ci(1 - (eb + db) / 2) if (eb is not None and db is not None) else [None, None]\n        out.append(rec)\n    return out\n\n\ndef run_cuts(P: pd.DataFrame, boot: SentBoot, regimes: dict, rule_cols: dict) -> pd.DataFrame:\n    \"\"\"P = consensus-scorable population frame (aligned with boot rows). regimes = {name: (mask, ycol)}.\"\"\"\n    W_all = boot.W()\n    rows = []\n    dims = {\"ALL\": lambda d: pd.Series(\"ALL\", index=d.index), \"stratum\": lambda d: d.stratum,\n            \"long_pool\": lambda d: pd.Series(np.where(d.long, \"L25+L20+EXC\", None), index=d.index),\n            \"words_tercile\": lambda d: d.words_t, \"ncond_bin\": lambda d: d.ncond_bin, \"exception_type\": lambda d: d.exc_bin,\n            \"label_tier\": lambda d: d.label_tier}\n    for rname, (mask, ycol) in regimes.items():\n        sub0 = P[mask]\n        pos0 = np.where(mask)[0]\n        for dim, fn in dims.items():\n            lab = fn(sub0)\n            for val in sorted(v for v in lab.dropna().unique()):\n                m = (lab == val).values\n                for rec in cell_stats(sub0[m], ycol, rule_cols, boot, W_all, pos0[m]):\n                    rows.append({\"regime\": rname, \"dim\": dim, \"cell\": val, **rec})\n    return pd.DataFrame(rows)\n\n\n# =================================================================================================== graded trace\ndef graded_trace(y, c) -> dict:\n    \"\"\"(e_t, d_t) at every distinct threshold t of the graded score (flag = c >= t); the ROC = (d_t, 1 - e_t).\n    Asserts the trapezoid area equals the tie-aware AUROC to 1e-9.\"\"\"\n    y = np.asarray(y, int)\n    c = np.asarray(c, float)\n    ts = np.unique(c)\n    pts = [(0.0, 0.0)]\n    tr = []\n    for t in ts[::-1]:\n        fl = c >= t\n        tpr = fl[y == 1].mean()\n        fpr = fl[y == 0].mean()\n        tr.append({\"t\": float(t), \"e_t\": float(1 - tpr), \"d_t\": float(fpr)})\n        pts.append((fpr, tpr))\n    pts.append((1.0, 1.0))\n    xs, ys = zip(*pts)\n    area = float(np.trapezoid(ys, xs))\n    a = auc(y, c)\n    assert abs(area - a) < 1e-9, (area, a)\n    named = {}\n    for nm, en in ((\"any_peer_agrees (c<1)\", c < 1), (\"majority END_MAJ (c<0.5)\", c < 0.5), (\"all_peers_agree (c==0)\", c == 0)):\n        named[nm] = {\"e\": float(en[y == 1].mean()), \"d\": float((~en)[y == 0].mean()),\n                     \"auroc_b\": float(1 - (en[y == 1].mean() + (~en)[y == 0].mean()) / 2)}\n    return {\"trace\": tr, \"trapezoid_area\": area, \"auroc\": a, \"named_points\": named}\n\n\n# =================================================================================================== GEE\ndef gee_fit(data: pd.DataFrame, formula: str, groups: str = \"sentence_id\") -> dict:\n    \"\"\"Binomial-logit GEE, exchangeable working correlation, robust SE; falls back to Independence.\"\"\"\n    out = {\"formula\": formula, \"n\": len(data), \"n_clusters\": int(data[groups].nunique())}\n    for cs_name, cs in ((\"Exchangeable\", sm.cov_struct.Exchangeable()), (\"Independence\", sm.cov_struct.Independence())):\n        try:\n            with warnings.catch_warnings(record=True) as wl:\n                warnings.simplefilter(\"always\")\ndef net_test(P: pd.DataFrame, boot: SentBoot, col: str = \"end_MAJ\", long_only: bool = False) -> dict:\n    \"\"\"Delta(e+d) top vs bottom words tercile (and n_conditions 4+ vs 0-1) with cluster-bootstrap CIs, plus the summed\n    average marginal effect per SD (AME_e + AME_d) from plain logistic refits in every replicate.\"\"\"\n    mask = P.in_RAB.values & (P.long.values if long_only else True)\n    W = boot.W(mask)\n    d = P[mask]\n    y = d.y_AB.values.astype(int)\n    en = d[col].values.astype(float)\n    out = {}\n    for nm, lo_m, hi_m in ((\"words_T3_minus_T1\", d.words_t.values == \"T1\", d.words_t.values == \"T3\"),\n                           (\"ncond_4p_minus_01\", d.ncond_bin.values == \"0-1\", d.ncond_bin.values == \"4+\")):\n        def ed(Wm, m):\n            with np.errstate(invalid=\"ignore\", divide=\"ignore\"):\n                e = (Wm[..., m] @ (en[m] * y[m])) / (Wm[..., m] @ y[m])\n                dd = (Wm[..., m] @ ((1 - en[m]) * (1 - y[m]))) / (Wm[..., m] @ (1 - y[m]))\n            return e, dd\n        one = np.ones(len(d))\n        e_lo, d_lo = ed(one, lo_m)\n        e_hi, d_hi = ed(one, hi_m)\n        eb_lo, db_lo = ed(W, lo_m)\n        eb_hi, db_hi = ed(W, hi_m)\n        delta = (e_hi + d_hi) - (e_lo + d_lo)\n        dB = (eb_hi + db_hi) - (eb_lo + db_lo)\n        c = ci(dB)\n        verdict = (\"IMPROVES_WITH_COMPLEXITY (scatter dominates)\" if c[1] is not None and c[1] < 0 else\n                   \"DEGRADES_WITH_COMPLEXITY (legitimate divergence dominates)\" if c[0] is not None and c[0] > 0 else\n                   \"BALANCED_OR_UNDETERMINED\")\n        out[nm] = {\"delta_e_plus_d\": float(delta), \"ci\": c, \"delta_e\": float(e_hi - e_lo), \"delta_e_ci\": ci(eb_hi - eb_lo),\n                   \"delta_d\": float(d_hi - d_lo), \"delta_d_ci\": ci(db_hi - db_lo), \"e_lo\": float(e_lo), \"d_lo\": float(d_lo),\n                   \"e_hi\": float(e_hi), \"d_hi\": float(d_hi), \"n_lo\": int(lo_m.sum()), \"n_hi\": int(hi_m.sum()),\n                   \"delta_auroc_b\": float(-delta / 2), \"verdict\": verdict,\n                   \"driver\": \"e\" if abs(e_hi - e_lo) > abs(d_hi - d_lo) else \"d\"}\n    # AME per SD (words and n_conditions), plain logistic with stratum dummies (dropped within the long pool? kept)\n    dz = zcols(d)\n    X = np.column_stack([dz.zw.values, dz.zn.values, pd.get_dummies(d.stratum, drop_first=True).values.astype(float)])\n    err, cor = y == 1, y == 0\n    for j, nm in ((0, \"words\"), (1, \"n_conditions\")):\n        ame_e = _ame(X[err], en[err], np.ones(err.sum()), j)\n        ame_d = _ame(X[cor], 1 - en[cor], np.ones(cor.sum()), j)\n        bs = []\n        for b in range(W.shape[0]):\n            w = W[b]\n            try:\n                bs.append(_ame(X[err], en[err], w[err] + 1e-12, j) + _ame(X[cor], 1 - en[cor], w[cor] + 1e-12, j))\n            except ValueError:\n                continue\n        out[f\"AME_sum_per_SD_{nm}\"] = {\"ame_e\": ame_e, \"ame_d\": ame_d, \"sum\": ame_e + ame_d, \"ci\": ci(bs), \"n_boot\": len(bs)}\n    return out\n\n\n# =================================================================================================== SCATTER", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [19] TOOL CALL — Bash · 2026-09-25 16:31:34 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2; sed -n 195,250p $W/src/mechanism.py; grep -n "graded_vs_binary\|delta_ci\|graded_trace\|c_score_exact\|prereg_cuts\|make_bins\|SentBoot(\|net_test" $W/src/part_a.py
```

### [20] TOOL RESULT — Bash · 2026-09-25 16:31:34 UTC

```
{"stdout": "def zcols(d: pd.DataFrame) -> pd.DataFrame:\n    d = d.copy()\n    d[\"zn\"] = (d.n_conditions - d.n_conditions.mean()) / d.n_conditions.std()\n    d[\"zw\"] = (d.words - d.words.mean()) / d.words.std()\n    return d\n\n\ndef mechanism_M1_M2(P: pd.DataFrame, rule_cols: dict) -> dict:\n    \"\"\"M1: endorsed ~ z(n_conditions) + z(words) + C(stratum) among R_AB ERROR rows (prediction: n_conditions < 0).\n    M2: divergent ~ z(words) + z(n_conditions) + C(stratum) among R_AB CORRECT rows (prediction: words > 0).\"\"\"\n    res = {\"M1\": {}, \"M2\": {}}\n    ab = P[P.in_RAB]\n    for rule, col in rule_cols.items():\n        for side, yv, dep, key, want in ((\"M1\", 1, \"endorsed\", \"zn\", \"neg\"), (\"M2\", 0, \"divergent\", \"zw\", \"pos\")):\n            base = ab[ab.y_AB == yv].copy()\n            base[\"endorsed\"] = base[col].astype(int)\n            base[\"divergent\"] = 1 - base[\"endorsed\"]\n            variants = {\"primary\": (zcols(base), f\"{dep} ~ zn + zw + C(stratum)\")}\n            if rule == \"MAJ\":\n                variants[\"long_pool_only\"] = (zcols(base[base.long]), f\"{dep} ~ zn + zw + C(stratum)\")\n                variants[\"plus_vendor_family\"] = (zcols(base), f\"{dep} ~ zn + zw + C(stratum) + C(family_vendor)\")\n                variants[\"no_stratum_dummies\"] = (zcols(base), f\"{dep} ~ zn + zw\")\n                variants[\"EXPLORATORY_ncond_only\"] = (zcols(base), f\"{dep} ~ zn\")\n                variants[\"EXPLORATORY_words_only\"] = (zcols(base), f\"{dep} ~ zw\")\n                ra = base[base.label_tier == \"A\"]\n                variants[\"R_A_only\"] = (zcols(ra), f\"{dep} ~ zn + zw + C(stratum)\")\n                if side == \"M2\":\n                    for cne in (True, False):\n                        sub = base[base.correct_not_equivalent == cne]\n                        variants[f\"CNE={cne}\"] = (zcols(sub), f\"{dep} ~ zn + zw + C(stratum)\")\n            for vn, (d, f) in variants.items():\n                g = gee_fit(d, f)\n                kk = key if key in (g[\"coef\"] or {}) else (\"zw\" if key == \"zn\" else \"zn\")  # EXPLORATORY single-predictor fits\n                g[\"verdict\"] = verdict_slope(g[\"coef\"], kk, want)\n                g[\"verdict_on\"] = kk\n                g[\"rate\"] = float(d[dep].mean())\n                res[side][f\"{rule}|{vn}\"] = g\n    base = zcols(ab)\n    res[\"VIF\"] = vif_table(base, [\"zn\", \"zw\"])\n    res[\"corr_words_ncond_rows\"] = float(np.corrcoef(ab.words, ab.n_conditions)[0, 1])\n    # d split by correct_not_equivalent (the hypothesis puts d in the CNE rows)\n    cor = ab[ab.y_AB == 0]\n    res[\"M2_d_by_CNE\"] = {str(k): {\"n\": int(len(g)), \"d_MAJ\": float(1 - g[\"end_MAJ\"].mean())} for k, g in cor.groupby(\"correct_not_equivalent\")}\n    return res\n\n\n# =================================================================================================== NET\ndef _ame(X: np.ndarray, yv: np.ndarray, w: np.ndarray, j: int) -> float:\n    m = LogisticRegression(C=1e6, max_iter=500).fit(X, yv, sample_weight=w)\n    p = m.predict_proba(X)[:, 1]\n    return float(np.average(m.coef_[0][j] * p * (1 - p), weights=w))\n\n\ndef net_test(P: pd.DataFrame, boot: SentBoot, col: str = \"end_MAJ\", long_only: bool = False) -> dict:\n196:    cut = MC.prereg_cuts(rab_all)\n198:    df = MC.make_bins(df, cut)\n211:    P[\"c_score_exact\"] = P.c_exact.astype(float)\n218:    boot = SentBoot(P.sentence_id.values, b=2000, seed=0)\n248:    # VOCAB_EXACT: c_score_align vs c_score_exact side by side (+ the dataset label)\n251:            \"c_score_align_vs_y_exact\": auc(vx.y_exact, vx.c_frozen), \"c_score_exact_vs_y_exact\": auc(vx.y_exact, vx.c_score_exact),\n252:            \"c_score_align_vs_dataset_label\": auc(vx.y_AB, vx.c_frozen), \"c_score_exact_vs_dataset_label\": auc(vx.y_AB, vx.c_score_exact)}\n267:    # ---------------- graded vs binary + c_score_exact\n268:    gt = MC.graded_trace(y, P.c_frozen.values)\n269:    gte = MC.graded_trace(y, P.c_score_exact.values)\n272:    wa_c, wa_b, wa_x = WAuc(y, P.c_frozen.values), WAuc(y, 1 - P.end_MAJ.values), WAuc(y, P.c_score_exact.values)\n275:    A[\"graded_vs_binary\"] = {\"auroc_c_score_align\": gt[\"auroc\"], \"auroc_b_END_MAJ\": auc(y, 1 - P.end_MAJ.values),\n276:                             \"delta_graded_minus_binary\": gt[\"auroc\"] - auc(y, 1 - P.end_MAJ.values), \"delta_ci\": ci(d_cb),\n278:                             \"auroc_c_score_exact\": gte[\"auroc\"], \"delta_align_minus_exact\": gt[\"auroc\"] - gte[\"auroc\"],\n283:    pd.DataFrame(gt[\"trace\"]).to_csv(TAB / \"graded_trace_c_score_align.csv\", index=False)\n284:    pd.DataFrame(gte[\"trace\"]).to_csv(TAB / \"graded_trace_c_score_exact.csv\", index=False)\n291:    bq = SentBoot(Q.sentence_id.values, b=2000, seed=0)\n303:    A[\"NET\"] = {\"R_AB\": MC.net_test(P, boot), \"long_pool\": MC.net_test(P, boot, long_only=True)}\n360:           \"delta_ci_lo\": v[\"all_rows\"][\"delta_ci\"][0], \"delta_ci_hi\": v[\"all_rows\"][\"delta_ci\"][1]}\n366:            \"ncond_bin\", \"exc_bin\", \"label_tier\", \"correct_not_equivalent\", \"final_label\", \"y_AB\", \"c_frozen\", \"c_score_exact\",", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [21] TOOL CALL — Bash · 2026-09-25 16:31:40 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2; sed -n 185,305p $W/src/part_a.py; head -c 3000 $W/preview_eval_out.json; python3 -c "
import json;d=json.load(open('$W/full_eval_out.json'));ex=d['datasets'][0]['examples'];print(len(ex));print(json.dumps(ex[0],indent=1));
import collections;print(collections.Counter((e['output'],e['metadata_consensus_scorable']) for e in ex)); print(list(d['metadata'].keys())); print(len(d['metrics_agg']))
print(collections.Counter(json.loads(e['input'])['stratum'] for e in ex))
"
```

### [22] TOOL RESULT — Bash · 2026-09-25 16:31:40 UTC

```
{"stdout": "                                    \"mean_cliques\": float(NT.n_cliques.mean())}\n    A[\"nontransitivity\"] = ntr\n    reasons = Counter(p[3] for r in mats.values() for p in r[\"pairs\"])\n    A[\"matrix_summary\"] = {\"n_sentences\": len(mats), \"n_pairs\": int(sum(len(r[\"pairs\"]) for r in mats.values())),\n                           \"reason_counts\": dict(reasons), \"z3_version\": zver, \"code_sha\": csha,\n                           \"pair_secs_pctl_50_90_99_max\": [float(x) for x in np.percentile(\n                               [p[4] for r in mats.values() for p in r[\"pairs\"]], [50, 90, 99, 100])],\n                           \"wall_s_by_stage\": {s: json.loads((RES / f\"matrix_stage_{s}.json\").read_text()) for s in (\"mini\", \"rab\", \"rest\")\n                                               if (RES / f\"matrix_stage_{s}.json\").exists()}}\n    # ---------------- prereg (cut points on R_AB sentences)\n    rab_all = df[df.y_AB.notna()]\n    cut = MC.prereg_cuts(rab_all)\n    pre = write_prereg(cut)\n    df = MC.make_bins(df, cut)\n    # ---------------- VOCAB_EXACT on R_AB rows\n    ve = vocab_exact(df[df.y_AB.notna()], pre[\"vocab_exact\"][\"trusted_reference_status\"])\n    df = df.merge(ve, on=\"row_key\", how=\"left\")\n    df[\"vocab_exact\"] = df.vocab_exact.fillna(False).astype(bool)\n    # ---------------- consensus-scorable R_AB population\n    df[\"in_RAB\"] = df.y_AB.notna()\n    P = df[df.in_RAB & df.parseable & df.c_frozen_raw.notna()].copy().reset_index(drop=True)\n    P[\"end_MAJ\"] = (P.c_frozen_raw < 0.5).astype(int)\n    P[\"end_PLUR\"] = P.end_plur.astype(int)\n    P[\"end_FAM2\"] = P.end_fam2.astype(int)\n    P[\"end_FAMMAJ\"] = P.end_fammaj.astype(int)\n    P[\"end_MAJ_EXACT\"] = (P.c_exact < 0.5).astype(int)\n    P[\"c_score_exact\"] = P.c_exact.astype(float)\n    RULES = {\"MAJ\": \"end_MAJ\", \"PLUR\": \"end_PLUR\", \"FAM2\": \"end_FAM2\", \"FAMMAJ\": \"end_FAMMAJ\", \"MAJ_EXACT\": \"end_MAJ_EXACT\"}\n    A[\"population\"] = {\"R_AB_rows\": int(df.in_RAB.sum()), \"consensus_scorable\": len(P),\n                       \"excluded_unparseable\": int((df.in_RAB & ~df.parseable).sum()),\n                       \"excluded_npc_lt2\": int((df.in_RAB & df.parseable & df.c_frozen_raw.isna()).sum()),\n                       \"scorable_err\": int(P.y_AB.sum()), \"scorable_cor\": int((P.y_AB == 0).sum()),\n                       \"n_sent\": int(P.sentence_id.nunique())}\n    boot = SentBoot(P.sentence_id.values, b=2000, seed=0)\n    # VOCAB_EXACT testability (declared before AUROCs on it)\n    vx = P[P.vocab_exact & P.y_exact.notna()]\n    ve_info = {\"n_rows_vocab_exact_R_AB\": int(P.vocab_exact.sum()), \"n_with_y_exact\": len(vx),\n               \"n_err_exact\": int((vx.y_exact == 1).sum()), \"n_cor_exact\": int((vx.y_exact == 0).sum())}\n    ve_info[\"testable\"] = ve_info[\"n_err_exact\"] >= 50 and ve_info[\"n_cor_exact\"] >= 50\n    if len(vx):\n        from sklearn.metrics import cohen_kappa_score\n        ve_info[\"kappa_vs_dataset_label\"] = float(cohen_kappa_score(vx.y_AB.astype(int), vx.y_exact.astype(int)))\n        ve_info[\"crosstab\"] = {f\"label={a}|exact={b}\": int(((vx.y_AB == a) & (vx.y_exact == b)).sum()) for a in (0, 1) for b in (0, 1)}\n        ve_info[\"by_tier\"] = {t: int((vx.label_tier == t).sum()) for t in (\"A\", \"B\")}\n    A[\"vocab_exact\"] = ve_info\n    P[\"y_VX\"] = P.y_exact\n    vx_cor = set(vx[vx.y_exact == 0].row_key)\n    ra_cor = set(P[(P.label_tier == \"A\") & (P.y_AB == 0)].row_key)\n    A[\"vocab_exact\"][\"overlap\"] = {\"VX_CORRECT\": len(vx_cor), \"R_A_CORRECT\": len(ra_cor), \"intersection\": len(vx_cor & ra_cor),\n                                   \"note\": \"tier-A CORRECT rows are (almost) all vocabulary-exact: the label side of tier-A CORRECT needs no alignment\"}\n    # ---------------- cuts\n    regimes = {\"R_AB\": (np.ones(len(P), bool), \"y_AB\"), \"R_A\": ((P.label_tier == \"A\").values, \"y_AB\"),\n               \"VOCAB_EXACT\": ((P.vocab_exact & P.y_exact.notna()).values, \"y_VX\")}\n    cuts = MC.run_cuts(P, boot, regimes, RULES)\n    cuts_out = cuts.copy()\n    for c in (\"e_ci\", \"d_ci\", \"auroc_b_ci\", \"auroc_c_ci\"):\n        cuts_out[c + \"_lo\"] = cuts_out[c].apply(lambda v: v[0])\n        cuts_out[c + \"_hi\"] = cuts_out[c].apply(lambda v: v[1])\n        del cuts_out[c]\n    write_csv(cuts_out, \"ed_decomposition_cuts.csv\", [f\"{ROOT}/results/pair_matrix_E.jsonl :: eqmv matrix (this artifact)\",\n                                                      f\"{E5}/results/per_item_E.jsonl :: c_score_align (FROZEN)\",\n                                                      f\"{E5}/data/E_labels.jsonl :: final_label, label_tier\"])\n    A[\"cuts_headline\"] = cuts[(cuts.dim == \"ALL\")].to_dict(\"records\")\n    # VOCAB_EXACT: c_score_align vs c_score_exact side by side (+ the dataset label)\n    if len(vx):\n        A[\"vocab_exact\"][\"auroc\"] = {\n            \"c_score_align_vs_y_exact\": auc(vx.y_exact, vx.c_frozen), \"c_score_exact_vs_y_exact\": auc(vx.y_exact, vx.c_score_exact),\n            \"c_score_align_vs_dataset_label\": auc(vx.y_AB, vx.c_frozen), \"c_score_exact_vs_dataset_label\": auc(vx.y_AB, vx.c_score_exact)}\n    # stratified AUROC_b (within-stratum pairs) per rule, R_AB\n    y = P.y_AB.values.astype(int)\n    A[\"stratified\"] = {}\n    for rule, col in RULES.items():\n        s_b = strat_auc(y, 1 - P[col].values, P.stratum.values)\n        wsum = 0\n        acc = 0\n        for st, g in P.groupby(\"stratum\"):\n            dd = MC.ed_decomposition(g.y_AB.values.astype(int), g[col].values)\n            w = dd[\"n_err\"] * dd[\"n_cor\"]\n            acc += w * dd[\"auroc_b\"]\n            wsum += w\n        A[\"stratified\"][rule] = {\"strat_auroc_b\": s_b, \"sum_ws_identity\": acc / wsum, \"match\": abs(s_b - acc / wsum) < 1e-12}\n    A[\"stratified\"][\"c_score_align_strat_auroc\"] = strat_auc(y, P.c_frozen.values, P.stratum.values)\n    # ---------------- graded vs binary + c_score_exact\n    gt = MC.graded_trace(y, P.c_frozen.values)\n    gte = MC.graded_trace(y, P.c_score_exact.values)\n    W = boot.W()\n    from stats import WAuc\n    wa_c, wa_b, wa_x = WAuc(y, P.c_frozen.values), WAuc(y, 1 - P.end_MAJ.values), WAuc(y, P.c_score_exact.values)\n    d_cb = [wa_c(W[b]) - wa_b(W[b]) for b in range(W.shape[0])]\n    d_cx = [wa_c(W[b]) - wa_x(W[b]) for b in range(W.shape[0])]\n    A[\"graded_vs_binary\"] = {\"auroc_c_score_align\": gt[\"auroc\"], \"auroc_b_END_MAJ\": auc(y, 1 - P.end_MAJ.values),\n                             \"delta_graded_minus_binary\": gt[\"auroc\"] - auc(y, 1 - P.end_MAJ.values), \"delta_ci\": ci(d_cb),\n                             \"trapezoid_area_check\": gt[\"trapezoid_area\"], \"named_points\": gt[\"named_points\"],\n                             \"auroc_c_score_exact\": gte[\"auroc\"], \"delta_align_minus_exact\": gt[\"auroc\"] - gte[\"auroc\"],\n                             \"delta_align_minus_exact_ci\": ci(d_cx), \"named_points_exact\": gte[\"named_points\"],\n                             \"share_endorsements_needing_align_or_gran\": float(1 - P.n_eq_exact.sum() / max(P.n_eq.sum(), 1)),\n                             \"share_endorsements_needing_align_or_gran_ERROR\": float(1 - P[P.y_AB == 1].n_eq_exact.sum() / max(P[P.y_AB == 1].n_eq.sum(), 1)),\n                             \"share_endorsements_needing_align_or_gran_CORRECT\": float(1 - P[P.y_AB == 0].n_eq_exact.sum() / max(P[P.y_AB == 0].n_eq.sum(), 1))}\n    pd.DataFrame(gt[\"trace\"]).to_csv(TAB / \"graded_trace_c_score_align.csv\", index=False)\n    pd.DataFrame(gte[\"trace\"]).to_csv(TAB / \"graded_trace_c_score_exact.csv\", index=False)\n    # system_class cut (tiers A+B, any system incl. GOLD / CCG)\n    df[\"y_ABsys\"] = [(1 if r.final_label == \"ERROR\" else 0) if (r.final_label in (\"CORRECT\", \"ERROR\") and r.label_tier in (\"A\", \"B\")\n                     and not r.reading_choice) else None for r in df.itertuples()]\n    Q = df[df.y_ABsys.notna() & df.parseable & df.c_frozen_raw.notna()].copy().reset_index(drop=True)\n    Q[\"end_MAJ\"] = (Q.c_frozen_raw < 0.5).astype(int)\n    Q[\"y_ABsys\"] = Q.y_ABsys.astype(int)\n    bq = SentBoot(Q.sentence_id.values, b=2000, seed=0)\n    Wq = bq.W()\n    sysrows = []\n    for sc, g in Q.groupby(\"system_class\"):\n        pos = np.where((Q.system_class == sc).values)[0]\n        for rec in MC.cell_stats(g, \"y_ABsys\", {\"MAJ\": \"end_MAJ\"}, bq, Wq, pos):\n            sysrows.append({\"regime\": \"tiers A+B any system\", \"dim\": \"system_class\", \"cell\": sc, **rec})\n    A[\"system_class_cut\"] = sysrows\n    # ---------------- mechanism tests\n    t0 = time.time()\n    A[\"M1_M2\"] = MC.mechanism_M1_M2(P, RULES)\n    logger.info(f\"M1/M2 done {time.time() - t0:.0f}s\")\n    A[\"NET\"] = {\"R_AB\": MC.net_test(P, boot), \"long_pool\": MC.net_test(P, boot, long_only=True)}\n    logger.info(f\"NET done {time.time() - t0:.0f}s\")\n    sc = MC.scatter_index(P, sms, cut)\n{\n  \"metadata\": {\n    \"evaluation_name\": \"Do wrong translations scatter? Consensus mechanism audit (T4 on dataset E) + verified record\",\n    \"description\": \"Label-free pairwise eqmv matrix over every parseable output of the 700 E sentences; exact e/d decomposition of binary cross-family consensus; M1/M2/NET/SCATTER/M3-local/M4; file-sourced verified recor...\",\n    \"gates\": {\n      \"G0\": {\n        \"R_AB_n\": 2686,\n        \"R_AB_err\": 1822,\n        \"R_AB_cor\": 864,\n        \"R_AB_sent\": 292,\n        \"R_A_L20EXC_n\": 449,\n        \"R_A_L20EXC_err\": 261,\n        \"R_A_L20EXC_cor\": 188,\n        \"pass\": true,\n        \"expected\": {\n          \"R_AB_n\": 2686,\n          \"R_AB_err\": 1822,\n          \"R_AB_cor\": 864,\n          \"R_AB_sent\": 292,\n          \"R_A_L20EXC_n\": 449,\n          \"R_A_L20EXC_err\": 261,\n          \"R_A_L20EXC_cor\": 188\n        },\n        \"exp6_flag_agreement\": 0.970024685553074,\n        \"exp6_flag_disagree_n\": 255,\n        \"rows_without_unique_exp6_match\": 0,\n        \"exp6_flag_disagreement_breakdown\": {\n          \"ours_in_exp6_out\": 0,\n          \"exp6_in_ours_out\": 255,\n          \"by_system_class\": {\n            \"reference_gold_as_system\": 240,\n            \"symbolic_eventsem\": 15\n          },\n          \"explanation\": \"exp 6 metadata_in_R_AB = tiers A+B CORRECT/ERROR of ANY system (incl. MALLS gold-as-system and ccg2lambda); exp 5 analyse_E.regime (used here, G0 counts reproduced) keeps llm rows only. Every disagree...\"\n        }\n      },\n      \"G1\": {\n        \"auroc_R_AB_pooled\": 0.7823775511241208,\n        \"target_R_AB\": 0.782,\n        \"auroc_R_A_L20EXC\": 0.8598985081927122,\n        \"target_R_A\": 0.86,\n        \"tolerance\": 0.0005,\n        \"pass\": true,\n        \"n_imputed_parseable_none_R_AB\": 14,\n        \"n_unparseable_R_AB\": 0\n      },\n      \"G2\": {\n        \"n_compared\": 7383,\n        \"n_mismatch\": 24,\n        \"mismatch_rate\": 0.003250711093051605,\n        \"none_iff_npc_lt2_violations\": 0,\n        \"n_unknown_pairs_in_matrix\": 0,\n        \"n_mismatch_in_R_AB\": 7,\n        \"accept\": true,\n        \"explanation\": \"no UNKNOWN pair exists in the recomputed matrix (max pair 4.5 s < 30 s cap); mismatches are deterministic fast pairs. eqmv's align()/fp() iterate sets / hash strings, which depend on PYTHONHASHSEED: e...\"\n      }\n    },\n    \"verdicts\": {\n      \"M1\": {\n        \"verdict\": \"INCONCLUSIVE\",\n        \"rule\": \"endorsed(END_MAJ) ~ z(ncond)+z(words)+C(stratum) among R_AB ERROR rows; CONFIRMED iff ncond coef < 0 with CI excluding 0; REFUTED iff > 0 with CI excluding 0\",\n        \"rival\": \"N-version programming (Eckhardt-Lee 1985; Knight-Leveson 1986): coincident failures concentrate on difficult inputs (positive slope)\",\n        \"note\": \"EXPLORATORY single-predictor fits are negative, but endorsement of ANY output falls with length (see M2 specificity_caveat), so a negative e-slope alone does not show that errors scatter more than cor...\",\n        \"coef_ncond\": {\n          \"b\": -0.04050605412669583,\n          \"se\": 0.2493995369077613,\n          \"ci\"2686\n{\n \"input\": \"{\\\"text\\\": \\\"When something is depressing, it is sad.\\\", \\\"candidate_fol\\\": \\\"\\u2200x (Depressing(x) \\u2192 Sad(x))\\\", \\\"family\\\": \\\"openai\\\", \\\"stratum\\\": \\\"CTRL\\\"}\",\n \"output\": \"CORRECT\",\n \"predict_c_score_align\": \"0.090909\",\n \"predict_c_score_exact\": \"0.090909\",\n \"predict_b_endmaj\": \"0.000000\",\n \"predict_b_endfam2\": \"0.000000\",\n \"predict_b_endplur\": \"0.000000\",\n \"predict_b_endfammaj\": \"0.000000\",\n \"predict_c_k3_best_oof\": \"0.000000\",\n \"metadata_sentence_id\": \"0000c2274e80\",\n \"metadata_row_key\": \"b87a8dda4faced11|fewshot_v1\",\n \"metadata_words\": 7,\n \"metadata_n_conditions\": 1,\n \"metadata_tier\": \"A\",\n \"metadata_vocab_exact\": true,\n \"metadata_consensus_scorable\": true,\n \"metadata_fold_E\": 1,\n \"metadata_correct_not_equivalent\": false,\n \"eval_endmaj_correct\": 1.0,\n \"eval_endorsed_maj\": 1.0\n}\nCounter({('ERROR', True): 1810, ('CORRECT', True): 862, ('ERROR', False): 12, ('CORRECT', False): 2})\n['evaluation_name', 'description', 'gates', 'verdicts', 'deviations', 'prereg_sha256', 'population', 'nontransitivity', 'vocab_exact', 'record_summary', 'scope_limit']\n335\nCounter({'L25': 873, 'L20': 821, 'EXC': 606, 'CTRL': 386})", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [23] THINKING · 2026-09-25 16:32:06 UTC

```
Since the z3 pairwise-matrix stage requires the vendored solver and 60+ MB of upstream inputs, I'll base the notebook on the per-row consensus scores in `full_eval_out.json`, rerunning the original `stats.py`/`mechanism.py`/`part_a.py` analysis (e/d decomposition, graded vs. binary AUROC with cluster bootstrap, and NET). Next I'll build the mini data file.
```

### [24] TOOL CALL — Bash · 2026-09-25 16:32:06 UTC

```
cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_FWy8D4_y9GBn; W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2
cat > make_mini_data.py <<'EOF'
"""Build mini_demo_data.json: 100 consensus-scorable R_AB rows (50 sentences x 2 rows, stratified by stratum,
one ERROR + one CORRECT row per sentence where possible) + the full-run metrics_agg and headline metadata for comparison."""
import json, sys
import numpy as np
from collections import defaultdict

SRC = sys.argv[1]
d = json.load(open(SRC))
ex = [e for e in d["datasets"][0]["examples"] if e["metadata_consensus_scorable"]]
by = defaultdict(list)
for e in ex:
    by[e["metadata_sentence_id"]].append(e)
rng = np.random.default_rng(0)
# sentences that have both labels, grouped by stratum
strat = defaultdict(list)
for sid, rows in sorted(by.items()):
    labs = {r["output"] for r in rows}
    if labs == {"ERROR", "CORRECT"}:
        strat[json.loads(rows[0]["input"])["stratum"]].append(sid)
picked = []
for st in sorted(strat):
    sids = list(strat[st])
    rng.shuffle(sids)
    for sid in sids[:13 if st != "CTRL" else 11]:
        rows = by[sid]
        err = [r for r in rows if r["output"] == "ERROR"]
        cor = [r for r in rows if r["output"] == "CORRECT"]
        picked += [err[rng.integers(len(err))], cor[rng.integers(len(cor))]]
picked = picked[:100]
md = d["metadata"]
out = {"metadata": {"evaluation_name": md["evaluation_name"], "description": md["description"],
                    "source_file": "full_eval_out.json (datasets[0] = E_R_AB_consensus, 2,686 rows)",
                    "selection": "100 consensus-scorable R_AB rows: 50 sentences with both labels, stratified over strata L25/L20/EXC/CTRL, "
                                 "one ERROR + one CORRECT row per sentence, numpy default_rng(0)",
                    "population_full": md["population"], "gates_full": {k: {kk: vv for kk, vv in v.items() if not isinstance(vv, (dict, list))} for k, v in md["gates"].items()},
                    "verdicts_full": {k: (v.get("verdict") if isinstance(v, dict) else v) for k, v in md["verdicts"].items()}},
       "metrics_agg_full": d["metrics_agg"],
       "examples": picked}
json.dump(out, open("mini_demo_data.json", "w"), indent=1, ensure_ascii=False)
from collections import Counter
print(len(picked), Counter(p["output"] for p in picked), Counter(json.loads(p["input"])["stratum"] for p in picked),
      len({p["metadata_sentence_id"] for p in picked}))
print(out["metadata"]["verdicts_full"])
EOF
python3 make_mini_data.py $W/full_eval_out.json && ls -la mini_demo_data.json
```

### [25] TOOL RESULT — Bash · 2026-09-25 16:32:06 UTC

```
{"stdout": "100 Counter({'ERROR': 50, 'CORRECT': 50}) Counter({'EXC': 26, 'L20': 26, 'L25': 26, 'CTRL': 22}) 50\n{'M1': 'INCONCLUSIVE', 'M2': 'CONFIRMED', 'NET': 'DEGRADES_WITH_COMPLEXITY (legitimate divergence dominates)', 'SCATTER': None, 'M3_local': 'INCONCLUSIVE', 'M4': 'CONFIRMED', 'LOFO': 'NO_SINGLE_FAMILY_CARRIES_EFFECT'}\n-rw-r--r-- 1 root root 121972 Sep 25 16:32 mini_demo_data.json", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [26] TOOL CALL — Bash · 2026-09-25 16:32:10 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2; python3 -c "
import json;d=json.load(open('$W/preview_eval_out.json'));print(json.dumps(d['metadata']['verdicts']['SCATTER'])[:600])"
```

### [27] TOOL RESULT — Bash · 2026-09-25 16:32:10 UTC

```
{"stdout": "{\"SI_err_falls_with_ncond\": \"CONFIRMED\", \"SI_cor_gt_SI_err\": \"CONFIRMED\"}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [28] TOOL CALL — Bash · 2026-09-25 16:32:14 UTC

```
cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_FWy8D4_y9GBn; sed -i 's/(v.get("verdict") if isinstance(v, dict) else v)/(v.get("verdict", v) if isinstance(v, dict) else v)/' make_mini_data.py; python3 make_mini_data.py /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/full_eval_out.json | tail -1
```

### [29] TOOL RESULT — Bash · 2026-09-25 16:32:14 UTC

```
{"stdout": "{'M1': 'INCONCLUSIVE', 'M2': 'CONFIRMED', 'NET': 'DEGRADES_WITH_COMPLEXITY (legitimate divergence dominates)', 'SCATTER': {'SI_err_falls_with_ncond': 'CONFIRMED', 'SI_cor_gt_SI_err': 'CONFIRMED'}, 'M3_local': 'INCONCLUSIVE', 'M4': 'CONFIRMED', 'LOFO': 'NO_SINGLE_FAMILY_CARRIES_EFFECT'}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [30] ASSISTANT · 2026-09-25 16:34:10 UTC

```
Mini data is done (100 rows, 50 sentences, 50/50 ERROR/CORRECT across the four strata). Next I'm writing the notebook.
```

### [31] TOOL CALL — Write · 2026-09-25 16:34:10 UTC

```
File: /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_FWy8D4_y9GBn/build_notebook.py

"""Builds code_demo.ipynb from the cell list below (markdown / code). Run: python3 build_notebook.py"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
cells = []


def md(s):
    cells.append({"cell_type": "markdown", "metadata": {}, "source": s.strip("\n").splitlines(keepends=True)})


def code(s):
    cells.a... [truncated, 32831 chars total]
```

### [32] TOOL RESULT — Write · 2026-09-25 16:34:10 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_FWy8D4_y9GBn/build_notebook.py", "content": "\"\"\"Builds code_demo.ipynb from the cell list below (markdown / code). Run: python3 build_notebook.py\"\"\"\nimport json\nfrom pathlib import Path\n\nHERE = Path(__file__).resolve().parent\ncells = []\n\n\ndef md(s):\n    cells.append({\"cell_type\": \"markdown\", \"metadata\": {}, \"source\"... [truncated, 34678 chars total]
```

### [33] ASSISTANT · 2026-09-25 16:34:16 UTC

```
The notebook builder is written. Running the first test at minimum config (B_BOOT=20).
```

### [34] TOOL CALL — Bash · 2026-09-25 16:34:16 UTC

```
cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_FWy8D4_y9GBn; python3 build_notebook.py && sed -i 's/B_BOOT = 2000        #/B_BOOT = 20        #/' code_demo.ipynb && grep -c "B_BOOT = 20 " code_demo.ipynb
E=/tmp/aii_nb_test_envs/art_FWy8D4_y9GBn-4ed788879ab6
UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 $E && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python $E/bin/python jupyter ipykernel && time $E/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -30
```

### [35] TOOL RESULT — Bash · 2026-09-25 16:34:44 UTC

```
{"stdout": "wrote code_demo.ipynb with 28 cells\n1\n[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n[IPKernelApp] WARNING | Kernel is running over TCP without encryption. All communication (including code and outputs) is sent in plain text and is susceptible to eavesdropping. Use IPC transport or launch with kernel manager-provisioned CurveZMQ keys to enable transport encryption.\n[NbConvertApp] Writing 195232 bytes to code_demo.ipynb\n\nreal\t0m24.221s\nuser\t0m20.838s\nsys\t0m1.652s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [36] TOOL CALL — Bash · 2026-09-25 16:34:50 UTC

```
cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_FWy8D4_y9GBn; python3 -c "
import json;nb=json.load(open('code_demo.ipynb'))
for c in nb['cells']:
  if c['cell_type']!='code': continue
  for o in c['outputs']:
    if o['output_type']=='stream': print(''.join(o['text'])[:2500])
    elif o['output_type']=='error': print('ERROR',o['ename'],o['evalue'])
    elif 'text/plain' in o.get('data',{}): print(''.join(o['data']['text/plain'])[:1500])
    elif 'image/png' in o.get('data',{}): print('[image]')
  print('-----')
"
```

### [37] TOOL RESULT — Bash · 2026-09-25 16:34:50 UTC

```
{"stdout": "-----\n-----\n-----\nDo wrong translations scatter? Consensus mechanism audit (T4 on dataset E) + verified record\n100 consensus-scorable R_AB rows: 50 sentences with both labels, stratified over strata L25/L20/EXC/CTRL, one ERROR + one CORRECT row per sentence, numpy default_rng(0)\n100 example rows, 335 full-run metrics for comparison\n\n-----\n-----\n(100, 22) {1: 50, 0: 50} sentences: 50\n\n    sentence_id stratum family_vendor final_label  c_frozen  end_MAJ  words  \\\n0  0735186af337    CTRL       mistral       ERROR  0.000000        1      6   \n1  0735186af337    CTRL          qwen     CORRECT  0.000000        1      6   \n2  8863f5f99f1c    CTRL          qwen       ERROR  1.000000        0      6   \n3  8863f5f99f1c    CTRL       mistral     CORRECT  0.636364        0      6   \n4  113b00880c5c    CTRL          meta       ERROR  0.200000        1     12   \n5  113b00880c5c    CTRL      deepseek     CORRECT  0.166667        1     12   \n\n   n_conditions                                      candidate_fol  \n0             0       SupportedBy(williamDickinson, portlandWhigs)  \n1             0         Supported(williamDickinson, portlandWhigs)  \n2             1  ∀d (Disease(d) → ∃x (Female(x) ∨ Male(x) ∧ Aff...  \n3             1  ∀x (Disease(x) → (Affects(x, females) ∨ Affect...  \n4             0  Play(psyche) ∧ BasedOn(psyche, jamesMirandaBarry)  \n5             0  Play(psyche) ∧ BasedOn(psyche, lifeOfJamesMira...  \n-----\n-----\n-----\n-----\nwords tercile cut points: [14.666666666666664, 24.0]\nfinal_label  CORRECT  ERROR\nwords_t                    \nT1                17     17\nT2                19     19\nT3                14     14 \n\nfinal_label  CORRECT  ERROR\nncond_bin                  \n0-1               15     15\n2                  4      4\n3                  5      5\n4+                26     26\nbootstrap: 20 replicates over 50 sentences\n\n-----\nidentity AUROC_b = 1 - (e+d)/2 asserted for every rule (to 1e-12)\n\n        rule  n_err  n_cor     e     d  auroc_b  strat_auroc_b  \\\n0        MAJ     50     50  0.08  0.68     0.62         0.6162   \n1       PLUR     50     50  0.20  0.44     0.68         0.6752   \n2       FAM2     50     50  0.26  0.34     0.70         0.6975   \n3     FAMMAJ     50     50  0.12  0.56     0.66         0.6545   \n4  MAJ_EXACT     50     50  0.00  0.80     0.60         0.5939   \n\n   identity_1-(e+d)/2  \n0                0.62  \n1                0.68  \n2                0.70  \n3                0.66  \n4                0.60  \n-----\nAUROC c_score_align (graded) : 0.723\nAUROC END_MAJ (binary)       : 0.620\ndelta graded - binary        : +0.103  95% CI [0.045, 0.205]\nAUROC c_score_exact          : 0.635  (align - exact +0.088 [0.017, 0.148])\nnamed operating points on the graded ROC:\n\n                             e     d  auroc_b\nany_peer_agrees (c<1)     0.42  0.22     0.68\nmajority END_MAJ (c<0.5)  0.08  0.68     0.62\nall_peers_agree (c==0)    0.06  0.96     0.49\n-----\n16:34:42|INFO   |NET done 0s\n\nR_AB      AME_e + AME_d per SD of words       : +0.132  CI [-0.604, 0.4] (n_boot=20)\nR_AB      AME_e + AME_d per SD of n_conditions: +0.038  CI [-0.575, 0.294] (n_boot=20)\nlong_pool AME_e + AME_d per SD of words       : +0.219  CI [-0.008, 0.5] (n_boot=20)\nlong_pool AME_e + AME_d per SD of n_conditions: +0.049  CI [-0.089, 0.205] (n_boot=20)\n\n  population           contrast  n_lo  n_hi   e_lo   e_hi   d_lo   d_hi  \\\n0       R_AB  words_T3_minus_T1    34    28  0.176  0.071  0.294  0.929   \n1       R_AB  ncond_4p_minus_01    30    52  0.200  0.038  0.400  0.885   \n2  long_pool  words_T3_minus_T1    14    28  0.000  0.071  0.286  0.929   \n3  long_pool  ncond_4p_minus_01     8    52  0.000  0.038  0.750  0.885   \n\n   delta_e_plus_d  ci_lo  ci_hi driver  \\\n0           0.529  0.110  0.789      d   \n1           0.323 -0.039  0.663      d   \n2           0.714  0.204  1.000      d   \n3           0.173 -0.125  0.964      d   \n\n                                             verdict  \n0  DEGRADES_WITH_COMPLEXITY (legitimate divergenc...  \n1                           BALANCED_OR_UNDETERMINED  \n2  DEGRADES_WITH_COMPLEXITY (legitimate divergenc...  \n3                           BALANCED_OR_UNDETERMINED  \n-----\n42 metrics written to demo_eval_out.json; total analysis time 0.4s\n\n-----\n                        metric  demo (100 rows)  full run (2,672 rows)\n           auroc_c_score_align            0.723                  0.784\n               auroc_b_END_MAJ            0.620                  0.669\n     delta_graded_minus_binary            0.103                  0.114\n           auroc_c_score_exact            0.635                  0.748\n                    e_maj_R_AB            0.080                  0.124\n                    d_maj_R_AB            0.680                  0.537\n              auroc_b_maj_R_AB            0.620                  0.669\n             auroc_b_fam2_R_AB            0.700                  0.748\n             auroc_b_plur_R_AB            0.680                  0.714\nstrat_auroc_c_score_align_R_AB            0.718                  0.742\n         net_words_T3_minus_T1            0.529                  0.356\n net_words_T3_minus_T1_delta_e           -0.105                 -0.252\n net_words_T3_minus_T1_delta_d            0.634                  0.608\n         net_ncond_4p_minus_01            0.323                  0.319\n\nFull-run verdicts: {\n \"M1\": \"INCONCLUSIVE\",\n \"M2\": \"CONFIRMED\",\n \"NET\": \"DEGRADES_WITH_COMPLEXITY (legitimate divergence dominates)\",\n \"SCATTER\": {\n  \"SI_err_falls_with_ncond\": \"CONFIRMED\",\n  \"SI_cor_gt_SI_err\": \"CONFIRMED\"\n },\n \"M3_local\": \"INCONCLUSIVE\",\n \"M4\": \"CONFIRMED\",\n \"LOFO\": \"NO_SINGLE_FAMILY_CARRIES_EFFECT\"\n}\nDemo NET verdict (words): DEGRADES_WITH_COMPLEXITY (legitimate divergence dominates)\n\n<Figure size 1500x440 with 3 Axes>\n-----", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [38] ASSISTANT · 2026-09-25 16:35:00 UTC

```
The first test passed in 24 s at B=20. Now checking that the figure was rendered and scaling the bootstrap to B=200, then B=2000.
```

### [39] TOOL CALL — Bash · 2026-09-25 16:35:00 UTC

```
cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_FWy8D4_y9GBn; python3 -c "
import json;nb=json.load(open('code_demo.ipynb'));print([list(o.get('data',{}).keys()) for o in nb['cells'][-1]['outputs']])"
python3 build_notebook.py && sed -i 's/B_BOOT = 2000        #/B_BOOT = 200        #/' code_demo.ipynb
E=/tmp/aii_nb_test_envs/art_FWy8D4_y9GBn-4ed788879ab6
UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 $E && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python $E/bin/python jupyter ipykernel && time $E/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -3; grep -o "NET done [0-9]*s\|total analysis time [0-9.]*s\|95% CI \[[0-9., -]*\]" code_demo.ipynb
```

### [40] TOOL RESULT — Bash · 2026-09-25 16:35:28 UTC

```
{"stdout": "[[], ['image/png', 'text/plain']]\nwrote code_demo.ipynb with 28 cells\n[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n[IPKernelApp] WARNING | Kernel is running over TCP without encryption. All communication (including code and outputs) is sent in plain text and is susceptible to eavesdropping. Use IPC transport or launch with kernel manager-provisioned CurveZMQ keys to enable transport encryption.\n[NbConvertApp] Writing 195263 bytes to code_demo.ipynb\n\nreal\t0m26.533s\nuser\t0m25.781s\nsys\t0m1.562s\n95% CI [0.018, 0.191]\nNET done 3s\ntotal analysis time 2.8s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [41] ASSISTANT · 2026-09-25 16:35:38 UTC

```
B=200 took 3 s for the analysis, so the original B=2000 fits easily. Before the final run I'm correcting the results text: the demo AUROCs come out lower than the full run, not "near" it.
```

### [42] TOOL CALL — Edit · 2026-09-25 16:35:38 UTC

```
File: /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_FWy8D4_y9GBn/build_notebook.py
OLD: AUROC and the e/d rates do not depend on class balance, so they
should land near the full-run values, up to sampling noise from 50 sentences.
NEW: AUROC and the e/d rates do not depend on class balance, but 50
sentences give wide CIs. The absolute values are noisy (on this subset the AUROCs come out a few points lower than
in the full run), while the qualitative pattern reproduces:
- graded > binary;
- END_MAJ has small `e` and large `d`;
- NET Δ(e+d) > 0, driven by `d`.
```

### [43] TOOL RESULT — Edit · 2026-09-25 16:35:38 UTC

```
{"filePath": "/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_FWy8D4_y9GBn/build_notebook.py", "oldString": "AUROC and the e/d rates do not depend on class balance, so they\nshould land near the full-run values, up to sampling noise from 50 sentences.", "newString": "AUROC and the e/d rates do not depend on class balance, but 50\nsentences give wide CIs. The absolute values are noisy (on this subset the AUROCs come out a few points lower than\nin the full run), while the qualitative pattern reproduces:\n- graded > binary;\n- END_MAJ has small `e` and large `d`;\n- NET Δ(e+d) > 0, driven by `d`.", "originalFile": null, "structuredPatch": [{"oldStart": 588, "oldLines": 8, "newStart": 588, "newLines": 12, "lines": [" ", " The table puts the demo's recomputed numbers (100 rows, 50 sentences) next to the full-run values (2,672 rows, 292", " sentences) from `metrics_agg_full`. The demo's rows are sampled **balanced** (one ERROR and one CORRECT row per", "-sentence), while the full population is about 68% ERROR. AUROC and the e/d rates do not depend on class balance, so they", "-should land near the full-run values, up to sampling noise from 50 sentences.", "+sentence), while the full population is about 68% ERROR. AUROC and the e/d rates do not depend on class balance, but 50", "+sentences give wide CIs. The absolute values are noisy (on this subset the AUROCs come out a few points lower than", "+in the full run), while the qualitative pattern reproduces:", "+- graded > binary;", "+- END_MAJ has small `e` and large `d`;", "+- NET Δ(e+d) > 0, driven by `d`.", " ", " The figures follow `eval.py`'s `figures()`:", " - **left**: the graded ROC with the named operating points (fig 4);"]}], "userModified": false, "replaceAll": false}
```

### [44] TOOL CALL — Bash · 2026-09-25 16:35:38 UTC

```
cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_FWy8D4_y9GBn; python3 build_notebook.py && grep -c "B_BOOT = 2000 " code_demo.ipynb
E=/tmp/aii_nb_test_envs/art_FWy8D4_y9GBn-4ed788879ab6
UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 $E && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python $E/bin/python jupyter ipykernel && time $E/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -3; grep -o "NET done [0-9]*s\|total analysis time [0-9.]*s\|95% CI \[[0-9., -]*\]\|\"ename\": \"[A-Za-z]*\"" code_demo.ipynb
```

### [45] TOOL RESULT — Bash · 2026-09-25 16:36:30 UTC

```
{"stdout": "wrote code_demo.ipynb with 28 cells\n1\n[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n[IPKernelApp] WARNING | Kernel is running over TCP without encryption. All communication (including code and outputs) is sent in plain text and is susceptible to eavesdropping. Use IPC transport or launch with kernel manager-provisioned CurveZMQ keys to enable transport encryption.\n[NbConvertApp] Writing 195472 bytes to code_demo.ipynb\n\nreal\t0m50.445s\nuser\t1m12.566s\nsys\t0m1.654s\n95% CI [0.027, 0.186]\nNET done 27s\ntotal analysis time 27.3s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [46] ASSISTANT · 2026-09-25 16:36:36 UTC

```
The run with B=2000 (the original value) finished in 50 s with no errors. Checking the rendered figure.
```

### [47] TOOL CALL — Bash · 2026-09-25 16:36:36 UTC

```
cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_FWy8D4_y9GBn; python3 -c "
import json,base64;nb=json.load(open('code_demo.ipynb'))
o=[o for o in nb['cells'][-1]['outputs'] if 'image/png' in o.get('data',{})][0]
open('/tmp/claude-0/-ai-inventor-aii-data-runs-run-An1uy2kF2SjZ-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-3-art-FWy8D4-y9GBn/f20e6559-4348-40a6-8871-3ec3664cc28b/scratchpad/fig.png','wb').write(base64.b64decode(o['data']['image/png']))"
```

### [48] TOOL RESULT — Bash · 2026-09-25 16:36:36 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [49] TOOL CALL — Read · 2026-09-25 16:36:36 UTC

```
/tmp/claude-0/-ai-inventor-aii-data-runs-run-An1uy2kF2SjZ-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-3-art-FWy8D4-y9GBn/f20e6559-4348-40a6-8871-3ec3664cc28b/scratchpad/fig.png
```

### [50] TOOL RESULT — Read · 2026-09-25 16:36:36 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [51] ASSISTANT · 2026-09-25 16:36:54 UTC

```
The figure looks right. Next: README, manifest and the structured output file.
```

### [52] TOOL CALL — Bash · 2026-09-25 16:36:54 UTC

````
cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_FWy8D4_y9GBn
cat > README.md <<'EOF'
# Consensus mechanism audit: demo notebook

This is a runnable, Colab-ready demo of the evaluation artifact **"Why cross-model agreement flags logic errors"** (T4
consensus-mechanism audit on dataset E, `eval.py`). The audit studies gold-free scoring of NL→FOL translations by
cross-family agreement. It decomposes binary majority consensus exactly as `AUROC_b = 1 − (e+d)/2`, where
`e` = P(endorsed | ERROR) and `d` = P(not endorsed | CORRECT). It then compares that binary rule with the graded consensus
score `c_score_align` and tests how the gap changes with sentence length (NET).

## What the notebook does
- It loads `mini_demo_data.json` from GitHub, falling back to the local copy.
- It re-runs the artifact's original analysis functions, copied unchanged from `src/stats.py`, `src/mechanism.py`,
  `src/part_a.py` and `eval.py`, on 100 curated R_AB rows:
  - the e/d decomposition for 5 endorsement rules;
  - graded vs binary AUROC with a sentence-cluster bootstrap (B = 2000, the original value);
  - the graded ROC trace;
  - the NET test.
- It compares the results with the full-run numbers (2,672 rows) shipped in the data file, and plots the ROC, e/d by
  length, and the AUROCs.
- Not re-run: the z3 pairwise-equivalence matrix stage (`src/run_matrix.py`). It needs the vendored `eqmv` code and
  about 60 MB of upstream inputs. The demo starts from that stage's per-row outputs, which are the consensus scores.

The run takes about 50 s locally, including the package install.

## Layout
- `code_demo.ipynb`: the demo notebook, executed, with outputs.
- `mini_demo_data.json`: 100 R_AB rows (50 sentences × one ERROR + one CORRECT row, stratified over L25/L20/EXC/CTRL,
  `default_rng(0)`). It also holds the full-run `metrics_agg` (335 metrics) and the headline gates and verdicts.
- `make_mini_data.py`: builds `mini_demo_data.json` from the artifact's `full_eval_out.json`, passed as the first argument.
- `build_notebook.py`: generates `code_demo.ipynb` from its cell list.
- `demo_eval_out.json`: written when the notebook runs; holds the recomputed metrics in `eval.py`'s `metrics_agg` key format.

## How to run
Open `code_demo.ipynb` in Colab or Jupyter and run all cells. Locally:
```bash
python3 build_notebook.py                        # (re)generate the notebook
jupyter nbconvert --to notebook --execute code_demo.ipynb --output code_demo.ipynb
```
Tunable parameters are in the config cell:
- `B_BOOT = 2000`: the original bootstrap size.
- `BOOT_SEED = 0`.
- `N_ROWS = 100`: all rows of the mini data. The original analysis used all 2,672 scorable rows.

## Restoring removed files
Nothing is marked for deletion: every file here is small text or code, and `.aii/manifest.yaml` has no entries.
`demo_eval_out.json` can be regenerated by running the notebook.
EOF
cat > .aii/manifest.yaml <<'EOF'
entries: []
EOF
cat > .terminal_claude_agent_struct_out.json <<'EOF'
{"out_expected_files": {"notebook": "code_demo.ipynb", "mini_data_file": "mini_demo_data.json"}}
EOF
grep -c 'GITHUB_DATA_URL = \\"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/fork/run_An1uy2kF2SjZ/round-3/evaluation-2/demo/mini_demo_data.json\\"' code_demo.ipynb; grep -c "urllib.request.urlopen(GITHUB_DATA_URL)" code_demo.ipynb; ls -la; du -sh .
````

### [53] TOOL RESULT — Bash · 2026-09-25 16:36:54 UTC

```
{"stdout": "1\n1\ntotal 3684\ndrwxr-xr-x 3 root root 1068248 Sep 25 16:36 .\ndrwxr-xr-x 6 root root 2000346 Sep 25 16:30 ..\ndrwxr-xr-x 2 root root    1200 Sep 25 16:36 .aii\n-rw------- 1 root root      54 Sep 25 16:30 .aii_claude_session.json\n-rw-r--r-- 1 root root  341200 Sep 25 16:36 .repl_agent.ptylog\n-rw-r--r-- 1 root root      97 Sep 25 16:36 .terminal_claude_agent_struct_out.json\n-rw-r--r-- 1 root root    2797 Sep 25 16:36 README.md\n-rw-r--r-- 1 root root   32892 Sep 25 16:35 build_notebook.py\n-rw-r--r-- 1 root root  195544 Sep 25 16:36 code_demo.ipynb\n-rw-r--r-- 1 root root    1871 Sep 25 16:36 demo_eval_out.json\n-rw-r--r-- 1 root root    2344 Sep 25 16:32 make_mini_data.py\n-rw-r--r-- 1 root root  122054 Sep 25 16:32 mini_demo_data.json\n1.7M\t.", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [54] ASSISTANT · 2026-09-25 16:37:06 UTC

```
I built the demo notebook (`code_demo.ipynb`) and its data file (`mini_demo_data.json`). The notebook runs from a clean environment in about 50 s, well under the 10-minute limit, using the original bootstrap size (2,000 resamples).

**What the notebook re-runs and what it doesn't.** The slowest step of `eval.py` isn't re-run. It checks 29,107 pairs of translations for logical equivalence with the z3 solver, and it needs the vendored `eqmv` code plus about 60 MB of upstream data. The notebook starts from that step's per-row consensus scores. On those rows it re-runs the original analysis code, copied unchanged from `src/stats.py`, `src/mechanism.py`, `src/part_a.py` and `eval.py`, split into cells with explanations in between:
- the error-rate split behind the binary majority vote, for all 5 voting rules, with the identity AUROC = 1 − (e+d)/2 checked on every rule;
- graded score vs. binary majority AUROC, with a confidence interval that resamples whole sentences;
- the graded ROC curve;
- the test of whether the majority vote gets worse on longer sentences (NET);
- metrics collected with the same helper and key names as `eval.py`, written to `demo_eval_out.json`.

**The data file.** It holds 100 rows from `full_eval_out.json`: 50 sentences, one wrong and one correct translation each, spread across the four sentence groups. It also carries all 335 full-run metrics and the headline verdicts, so the last cell can print them next to the demo's numbers.

**Results on the 100 rows:**

| Metric | Demo (100 rows) | Full run (2,672 rows) |
|---|---|---|
| Graded score `c_score_align` AUROC | 0.723 | 0.784 |
| Majority vote AUROC | 0.620 | 0.669 |
| Graded minus majority | +0.103 [0.027, 0.186] | +0.114 |
| e (wrong translations the majority accepts) | 0.08 | 0.124 |
| d (correct translations the majority rejects) | 0.68 | 0.537 |
| Longest vs. shortest third of sentences, change in e+d | +0.53 | +0.356 |

The demo's AUROCs come out a few points lower than the full run, so the exact values shouldn't be quoted from this subset. With only 50 sentences the intervals are wide. The pattern holds, though: the graded score beats the majority vote, and the majority vote gets worse on longer sentences because correct translations stop being reproduced by other models.

**Checks and deviations from your instructions:**
- The notebook contains the exact `GITHUB_DATA_URL` and loads it with the local fallback.
- I generated the notebook with a builder script (`build_notebook.py`) rather than NotebookEdit.
- No todo tool was available, so the todo list wasn't recorded.
- In the imports cell I left out the original self-restart that fixes the hash seed, and the 20 GB memory cap. The seed only matters for the solver step, which isn't re-run.

Nothing in the workspace is large, so `.aii/manifest.yaml` has no entries. I also wrote the `README.md` and `./.terminal_claude_agent_struct_out.json`.

Files are in `art_FWy8D4_y9GBn/`:
- `code_demo.ipynb`
- `mini_demo_data.json`
- `demo_eval_out.json`
- `make_mini_data.py`
- `build_notebook.py`
- `README.md`
```
