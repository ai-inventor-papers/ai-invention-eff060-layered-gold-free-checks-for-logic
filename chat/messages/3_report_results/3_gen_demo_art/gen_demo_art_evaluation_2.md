# gen_demo_art_evaluation_2 — report_results

> Phase: `gen_paper_repo` · `gen_demo_art`
> Run: `run_u75jRHUss0zo` — Gold-Free Faithfulness Metrics for NL-to-FOL Translation
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_demo_art_evaluation_2` (terminal_claude_agent, claude-opus-5-5)

### [1] CONFIG · 2026-09-24 18:35:02 UTC

```
model: claude-opus-5-5 | effort: high | permission: bypassPermissions
```

### [2] SYSTEM-USER prompt · 2026-09-24 18:35:08 UTC

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
Your workspace: `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_FWy8D4_y9GBn`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_FWy8D4_y9GBn/`:
GOOD: `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_FWy8D4_y9GBn/file.py`, `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_FWy8D4_y9GBn/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>
<disposable_outputs>
A SHARED CACHE ALREADY EXISTS FOR THIS RUN: `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/.shared_cache`
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
Raw data URL: https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/main/round-3/evaluation-2/demo/mini_demo_data.json

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
GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/main/round-3/evaluation-2/demo/mini_demo_data.json"
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
To test-run the notebook in a clean environment (simulating Colab), create a disposable `.nb_env` in your workspace:
```bash
/usr/local/bin/python3.12 -m venv .nb_env
.nb_env/bin/pip install -q pip jupyter ipykernel
.nb_env/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb
rm -rf .nb_env
```
The timeout is set to <max_notebook_total_runtime>. The entire notebook must finish within this time.

What happens: the .venv starts empty (just jupyter). When the notebook's install cell runs, `google.colab` is NOT in sys.modules, so ALL packages get installed — non-Colab packages unconditionally, and Colab packages (numpy, pandas, etc.) at Colab's exact versions via the guard block. The result mirrors Colab's environment as closely as possible. If a cell fails, fix the notebook and re-run.
</test_environment>

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.


<todos>
TODO 1. Read and STRICTLY follow these skills: aii-colab, aii-long-running-tasks.
TODO 2. Read demo file and relevant preview_* files (preview only). Understand script structure: imports, setup, processing, output. Identify ALL tunable parameters (iterations, epochs, n_samples, hidden_size, batch_size, etc.) — these go in the config cell.
TODO 3. Create `mini_demo_data.json`: curated subset from at most ONE dataset (no more than 100 diverse examples). CRITICAL: do NOT read/grep full output file — may crash. Use `head -c 5000` or stream first entries with Python to pick examples.
TODO 4. Create `code_demo.ipynb` via NotebookEdit following <notebook_structure>. Set ALL config parameters to ABSOLUTE MINIMUM values — the smallest that produce any output (e.g. 1 iteration, 2 samples, smallest array sizes). Test-run using <test_environment>. Fix all errors until it passes.
TODO 5. GRADUALLY SCALE (but don't overdo it): increase config params step by step (e.g. ~2x each round). After each increase: test-run, record runtime, fix errors. STOP SCALING as soon as results look meaningful — a working small-scale demo beats a failed large-scale one. If full original params fit within <max_notebook_total_runtime> (10% margin), use them. Otherwise keep whatever works and comment out the true original values. Do NOT spend more than 2-3 scaling rounds.
TODO 6. Verify: (1) code_demo.ipynb contains GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/main/round-3/evaluation-2/demo/mini_demo_data.json" exactly, (2) mini_demo_data.json exists, (3) uses GitHub URL pattern not just open('mini_demo_data.json').
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

### [3] HUMAN-USER prompt · 2026-09-24 18:35:08 UTC

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

### [4] TOOL CALL — Skill · 2026-09-24 18:35:12 UTC

```
aii-colab
```

### [5] TOOL CALL — Skill · 2026-09-24 18:35:12 UTC

```
aii-long-running-tasks
```

### [6] TOOL RESULT — Skill · 2026-09-24 18:35:12 UTC

```
{"success": true, "commandName": "aii-colab"}
```

### [7] TOOL RESULT — Skill · 2026-09-24 18:35:14 UTC

```
{"success": true, "commandName": "aii-long-running-tasks"}
```

### [8] TOOL CALL — Bash · 2026-09-24 18:35:16 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2; ls -la $W; ls $W/* | head -80; wc -l $W/eval.py; du -sh $W/*; pwd; ls -la
```

### [9] TOOL RESULT — Bash · 2026-09-24 18:35:16 UTC

```
{"stdout": "total 26067\ndrwxr-xr-x 12 root root 2005038 Sep 24 06:57 .\ndrwxr-xr-x  7 root root 3000107 Sep 24 01:33 ..\ndrwxr-xr-x  2 root root   98200 Sep 24 03:25 .aii\n-rw-------  1 root root      54 Sep 24 03:16 .aii_claude_session.json\n-rw-------  1 root root    7434 Sep 24 03:25 .aii_worker_result.json\n-rw-r--r--  1 root root  221720 Sep 24 03:25 .repl_agent.ptylog\n-rw-r--r--  1 root root    2767 Sep 24 03:23 .terminal_claude_agent_struct_out.json\n-rw-r--r--  1 root root   15340 Sep 24 03:15 README.md\ndrwxr-xr-x  2 root root 1001905 Sep 24 03:14 audit\n-rw-r--r--  1 root root   24856 Sep 24 03:15 eval.py\n-rw-r--r--  1 root root 2970006 Sep 24 03:21 eval_out.json\ndrwxr-xr-x  2 root root 1068840 Sep 24 01:58 figures\n-rw-r--r--  1 root root 3215695 Sep 24 03:21 full_eval_out.json\ndrwxr-xr-x  3 root root 2002556 Sep 24 02:00 inputs_copy\ndrwxr-xr-x  2 root root 1008397 Sep 24 03:17 logs\n-rw-r--r--  1 root root   45660 Sep 24 03:21 mini_eval_out.json\n-rw-r--r--  1 root root 3597729 Sep 24 03:18 pairwise_classes_E.jsonl\n-rw-r--r--  1 root root    5707 Sep 24 03:18 prereg_mech.json\n-rw-r--r--  1 root root      83 Sep 24 03:18 prereg_mech.sha256\n-rw-r--r--  1 root root   36997 Sep 24 03:21 preview_eval_out.json\n-rw-r--r--  1 root root    1067 Sep 24 03:12 pyproject.toml\n-rw-r--r--  1 root root      27 Sep 24 01:55 pytest.ini\n-rw-r--r--  1 root root    5950 Sep 24 03:15 reproducibility.md\ndrwxr-xr-x  5 root root 2001292 Sep 24 03:07 results\ndrwxr-xr-x  3 root root 1030230 Sep 24 07:12 src\ndrwxr-xr-x  2 root root 1026193 Sep 24 02:00 tables\ndrwxr-xr-x  2 root root 1000310 Sep 24 06:57 tests\n-rw-r--r--  1 root root  220888 Sep 24 03:12 uv.lock\ndrwxr-xr-x  8 root root 1069299 Sep 24 07:12 vendor_exp5\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/README.md\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/eval.py\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/eval_out.json\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/full_eval_out.json\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/mini_eval_out.json\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/pairwise_classes_E.jsonl\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/prereg_mech.json\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/prereg_mech.sha256\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/preview_eval_out.json\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/pyproject.toml\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/pytest.ini\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/reproducibility.md\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/uv.lock\n\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/audit:\nm2_specificity.json\nm2_specificity.py\nrederive.json\nrederive.py\n\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/figures:\nfig1_e_d_by_complexity.json\nfig1_e_d_by_complexity.pdf\nfig1_e_d_by_complexity.png\nfig2_auroc_k.json\nfig2_auroc_k.pdf\nfig2_auroc_k.png\nfig3_scatter_index.json\nfig3_scatter_index.pdf\nfig3_scatter_index.png\nfig4_graded_roc.json\nfig4_graded_roc.pdf\nfig4_graded_roc.png\n\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/inputs_copy:\n3_invention_loop\nhypothesis_iter2_upd.txt\n\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/logs:\neval.log\neval_final.log\neval_final_run2.log\neval_final_run2.pid\neval_final_run3.log\neval_final_run3.pid\neval_full_run.log\neval_full_run.pid\neval_run.log\nfreeze.txt\ninstall.log\nmatrix_bg.log\nmatrix_bg.pid\npart_a.log\npart_a_run.log\nrun_matrix.log\nuv_install.log\n\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/results:\ndiag\nframe_min.pkl\nmatrix_determinism_check.json\nmatrix_stage_rab.json\nmatrix_stage_rest.json\npair_matrix_E.jsonl\npart_a.json\npopulation_RAB.pkl\nprev_run\nprev_run2\nrab_all.pkl\n\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src:\n__pycache__\nconsensus_mx.py\ncopy_inputs.py\nframe.py\nm4.py\nmechanism.py\npairwise.py\npart_a.py\npaths.py\n383 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/eval.py\n15K\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/README.md\n998K\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/audit\n25K\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/eval.py\n2.9M\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/eval_out.json\n1.7M\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/figures\n3.1M\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/full_eval_out.json\n63M\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/inputs_copy\n1.1M\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/logs\n45K\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/mini_eval_out.json\n3.5M\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/pairwise_classes_E.jsonl\n6.0K\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/prereg_mech.json\n512\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/prereg_mech.sha256\n37K\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/preview_eval_out.json\n1.5K\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/pyproject.toml\n512\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/pytest.ini\n6.0K\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/reproducibility.md\n20M\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/results\n2.3M\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src\n1.3M\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/tables\n981K\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/tests\n216K\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/uv.lock\n9.4M\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/vendor_exp5\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_FWy8D4_y9GBn\ntotal 2982\ndrwxr-xr-x 3 root root 1003117 Sep 24 18:35 .\ndrwxr-xr-x 6 root root 2016480 Sep 24 18:34 ..\ndrwxr-xr-x 2 root root       1 Sep 24 18:34 .aii\n-rw------- 1 root root      54 Sep 24 18:35 .aii_claude_session.json\n-rw-r--r-- 1 root root   31873 Sep 24 18:35 .repl_agent.ptylog", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [10] TOOL CALL — Bash · 2026-09-24 18:35:18 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2; cat $W/eval.py
```

### [11] TOOL RESULT — Bash · 2026-09-24 18:35:18 UTC

```
{"stdout": "#!/usr/bin/env python3\n\"\"\"Consensus mechanism audit + verified record (iteration 3, T4 on dataset E). CPU only, $0, no LLM calls.\n\nusage: uv run eval.py --stage mini|rab|all [--skip-matrix]\n  mini : 12-sentence matrix smoke test only\n  rab  : matrix for the 292 R_AB sentences, then every analysis\n  all  : matrix for all 700 E sentences (R_AB first), then every analysis\nOutputs: results/ (matrix, part_a.json), tables/*.csv, figures/*, pairwise_classes_E.js... [truncated, 26720 chars total]
```

### [12] TOOL CALL — Bash · 2026-09-24 18:35:24 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2; wc -l $W/src/*.py $W/audit/*.py; ls $W/src/__pycache__ $W/vendor_exp5 $W/tables; cat $W/README.md | head -120
```

### [13] TOOL RESULT — Bash · 2026-09-24 18:35:24 UTC

````
{"stdout": "   187 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/consensus_mx.py\n    60 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/copy_inputs.py\n   120 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/frame.py\n   197 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/m4.py\n   441 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/mechanism.py\n   109 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/pairwise.py\n   379 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/part_a.py\n    25 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/paths.py\n   654 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/record.py\n   129 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/run_matrix.py\n   125 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/stats.py\n    48 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/audit/m2_specificity.py\n   227 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/audit/rederive.py\n  2701 total\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/__pycache__:\nconsensus_mx.cpython-312.pyc\nframe.cpython-312.pyc\nmechanism.cpython-312.pyc\npairwise.cpython-312.pyc\npaths.cpython-312.pyc\nrecord.cpython-312.pyc\nstats.cpython-312.pyc\n\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/tables:\nb2_dead_end.csv\ncorrections.csv\ncoverage_vs_request.csv\ned_decomposition_cuts.csv\nexp6_COVERAGE_pooled.csv\nexp6_Per_stratum_R_AB_AUROC.csv\nexp6_R_AB_long_L25_L20_EXC.csv\nexp6_R_AB_pooled.csv\nexp6_R_A_pooled_L20_EXC_CTRL.csv\nexp6_complexity_gee.csv\nexp6_contamination_DiD.csv\nexp6_deviations.csv\nexp6_frame_284.csv\nexp6_system_level.csv\nfunction_inventory.csv\ng2_mismatches.csv\ngraded_trace_c_score_align.csv\ngraded_trace_c_score_exact.csv\nhypothesis_verdicts.csv\nlabel_facts.csv\nm4_auroc_k_cost.csv\nm4_fixed_pools_k2.csv\nm4_fixed_pools_k3.csv\nm4_fixed_pools_k4.csv\nm4_lofo.csv\nperturb_counts.csv\npt_vs_s4_rerun.csv\nradj_gate.csv\nregimes_R_PANEL.csv\nscatter_sentence_table.csv\nsource_hashes.csv\n\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/vendor_exp5:\n__init__.py\n__pycache__\nanalyse_E.py\ndata_views.py\nkey_monitor.sh\nlocal_judge_E.py\nlogs\npeer_text.py\npool_scoring.py\nposthoc_nf_fusion.py\nrun_api_E.py\nscore_E.py\nscreen_fit.py\nvendor_a\nvendor_c\nvendor_d\nvendor_e\nwrite_deviations.py\n# Do wrong NL→FOL translations scatter? A consensus-mechanism audit (T4 on dataset E), plus a verified record\n\nThis is an iteration-3 evaluation artifact of the AI-Inventor run `run_u75jRHUss0zo`. It is **CPU only and spent $0 on OpenRouter: it makes no LLM calls.**\nWorkspace (kept artifacts live here, by absolute path):\n`/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2`\n\nThe artifact has two parts, both computed in one pass over dataset E:\n\n- **A. Mechanism (T4).** Why does cross-family solver consensus (`c_score_align`) predict NL→FOL faithfulness? The\n  \"Anna Karenina\" premise says correct translations converge while errors scatter. To test it:\n  - We recompute the **label-free pairwise z3 equivalence-modulo-vocabulary (eqmv) matrix** among every parseable output of each of the 700 E sentences (29,107 node pairs). It uses exactly the iteration-1 `eqmv` behind the frozen score.\n  - We prove that it reproduces exp 5's **frozen** `c_score_align` (gate G2).\n  - We decompose binary majority consensus exactly as `AUROC_b = 1 − (e + d)/2`. Here **e** is the error-endorsement rate (ERROR rows endorsed by the cross-family peer majority) and **d** is the correct-divergence rate (CORRECT rows not endorsed). This is balanced accuracy, a *bookkeeping identity*, not a novel result.\n  - We model e (M1) and d (M2) against complexity, test the NET balance, measure the scatter index, and run M4 peer-count scaling, fixed pools, leave-one-family-out (LOFO) and $/CPU cost.\n- **B. Verified record.** Every iteration-2 number that the review flagged is re-read programmatically from files. Each CSV\n  starts with `# source: <abs path> :: <key path>` lines. A value not found in any file would be written `NOT_IN_FILES`; after the fixes in this run, none remain.\n\n## Headline results (R_AB = tiers A+B, CORRECT/ERROR, LLM rows, no reading_choice; 2,672 consensus-scorable rows, 283 sentences)\n\n| Quantity | Value [95% sentence-cluster bootstrap CI, B=2000] |\n|---|---|\n| Gates | **G0** R_AB 2686 (1822/864, 292 sent), R_A L20+EXC 449 (261/188): PASS. **G1** frozen AUROC 0.7824 (0.782) and 0.8599 (0.860): PASS. **G2** re-derived c = frozen on 99.67% of 7,383 rows (24 mismatches, 7 in R_AB; ≤0.5% accept rule), 0 UNKNOWN pairs, `|P_c|<2 ⇔ None` 0 violations |\n| Matrix | 29,107 pairs: 26,184 none, 1,473 align, 1,165 gran, 285 exact. Median pair 0.005 s, max 3.2 s. **Bit-identical across 3 independent recomputations** (`results/matrix_determinism_check.json`) |\n| Non-transitivity of eqmv | 15.8% of wedges (a~b, b~c, a≁c), L25 21.7%. **>5%, flagged**: \"classes\" are approximate (components vs greedy cliques both shipped) |\n| Graded c_score_align vs END_MAJ binary | 0.784 vs 0.669; Δ = +0.114 [0.091, 0.140]. Majority voting throws away much of the signal |\n| END_MAJ e / d | e = 0.124 [0.086, 0.164]; d = 0.537 [0.456, 0.619]. **d, not e, is the blind spot** |\n| Other rules (AUROC_b) | PLUR 0.714, FAM2 0.748 (e 0.299, d 0.204), FAMMAJ 0.702, MAJ_EXACT 0.627 |\n| Aligner-free c_score_exact | AUROC 0.748; align − exact = +0.036 [0.010, 0.062]. 53% of endorsements need align/gran (75% for ERROR rows, 38% for CORRECT) |\n| VOCAB_EXACT (pure-z3 label, no aligner on the label side; 85 ERR / 412 COR, testable) | κ vs dataset label 0.910. c_score_align AUROC 0.929 vs y_exact; c_score_exact 0.892 |\n| **M1** (e falls with n_conditions, GEE partial slope) | −0.04 [−0.53, 0.45]: **INCONCLUSIVE**. The words slope carries it (−0.77 [−1.39, −0.14]). Words and n_conditions are collinear (r = 0.70, VIF up to 11 with stratum dummies). Exploratory single-predictor fits are negative (n_conditions −0.76 [−1.16, −0.37]), so the Eckhardt-Lee/Knight-Leveson rival (positive slope) is not supported |\n| **M2** (d rises with words) | +1.95 [1.12, 2.77] per SD: **CONFIRMED** by the pre-registered rule in every sensitivity. d = 0.73 for correct-but-not-equivalent rows vs 0.32 for reference-equivalent rows. **But it is NON-SPECIFIC** (audit): with shuffled labels the same fit still gives +1.75 [1.04, 2.45]; ERROR rows diverge with length almost as steeply (label×words interaction −0.29 [−0.77, 0.20]); only a small label-specific part survives a within-sentence shuffle (p = 0.005). Long sentences lose endorsement for *every* output |\n| **NET** Δ(e+d), words T3 − T1 | +0.356 [0.198, 0.493]: **DEGRADES with length; driver = d** (Δe −0.252, Δd +0.608). n_conditions 4+ vs 0-1: +0.319 [0.129, 0.502] degrades. Long pool, words: degrades. Long pool, n_conditions: balanced |\n| **SCATTER** | SI_err 0.159 [0.131, 0.189] vs SI_cor 0.760 [0.706, 0.810]; ratio 4.45 [3.57, 5.77]. SI_err falls with n_conditions (pair GEE −0.64 [−1.00, −0.28]): **CONFIRMED**. Joint failure P(both ERROR) *rises* 0.32→0.62 while identical-wrong stays 0.10–0.12 at 3/4+ conditions: errors co-occur but differ |\n| M3-local (secondary) | Correctness slope, consensus − local judge (flag rate matched exactly) = +0.07 [−0.13, 0.23]: INCONCLUSIVE |\n| **M4** AUROC(k), rows with all 7 other families (n = 2014) | k = 1…7: 0.685, 0.738, 0.757, 0.770, 0.776, 0.780, 0.784. **k95 = 3: CONFIRMED** (≤ 5). Per words tercile, k95 T1/T2/T3 = 2/3/5: long sentences need more peers |\n| Fixed 3-family pool (cross-fitted on exp 6 folds_E) | deepseek+microsoft+openai, picked in 5/5 folds. Out-of-fold AUROC 0.785 = the full pool. Worst pool (cohere+meta+qwen) 0.697 |\n| LOFO | Minimum Δ = −0.011 (deepseek). All LOFO AUROCs > 0.712: NO_SINGLE_FAMILY_CARRIES_EFFECT |\n| Cost | Generation $/sentence ≈ $0.00032·k (expected over random k-subsets; the openai family is dearest at $0.0019). Best 3-pool $0.0020/sentence vs frontier judge $0.0029/call. Solver ≈ 0.016 CPU-s per family per candidate (mean pair 0.011 s) |\n| Independent audit (`audit/`) | 13 headline numbers re-derived from raw files with separate code: all match to 1e-9. AUROC permutation p = 0.001 (null max 0.539). Placebos with shuffled labels fail as they should for NET (−0.034 [−0.108, 0.034]), M1 and SCATTER. **They do not fail for M2** (see above) |\n| Verified record | 48 of 48 checkable clauses VERIFIED_MATCH. The reviewer's PT − S4 audit reproduces to 1e-4 (points) and 0.01 (CIs). Stratified PT − S4_local +0.059 [0.023, 0.093] |\n\n**Interpretation.** The premise is half right. Errors do scatter:\n- identical-wrong rates are low and fall with conditions (SCATTER, and e falls with length);\n- the rival N-version prediction (coincident failures concentrate on hard inputs) is not supported for *identical* wrong outputs, although joint failures do rise.\n\nHowever, on long and heavily conditioned sentences, correct outputs **also** stop agreeing (d → 0.8–0.9), mostly legitimately (vocabulary and granularity divergence among correct-but-not-equivalent rows). So binary majority consensus *degrades* with complexity. The graded score degrades less, and adding peers helps most on long sentences.\n\nBecause M2 is non-specific, the label-specific evidence is NET (d rises much more than e falls) and SCATTER (identical-wrong ≪ identical-correct). \"d rises with words\" alone would also hold if labels were random.\n\nCaveats:\n- Tier-A CORRECT labels are aligned-equivalence to the reference. Tier-A CORRECT rows are exactly the VOCAB_EXACT CORRECT rows (412/412), so the label side of d needs no aligner, while the consensus side does.\n- The panel (tier B) over-calls ERROR (majority accuracy 0.727), which inflates e.\n\n## Scope limits and deviations (also in `prereg_mech.json` → `deviations`, and `eval_out.json` → `metadata`)\n\n- **D4: E only.** R_COMP has no candidates or labels yet; the iteration-3 T2 experiment owns them. `pairwise_matrix()` (src/pairwise.py) and `ed_decomposition()` (src/mechanism.py) are shipped so iteration 4 can apply them unchanged.\n- **E is development data**, not pristine held-out: it was scored in iteration 2. Nothing is tuned here except the fixed pool, which is cross-fitted. The prereg guards against analysis-choice drift, **not** against label peeking.\n- **D1:** eqmv timeout is 3000 ms, not the direction's 2 s, because reproduction needs identical settings.\n- **D2:** k = 1..7 (8 vendor families), not 1..9. The slot-level sensitivity (`family` field) goes to k = 9 on 856 rows (k95 = 3).\n- **D3:** the G2 mismatches (0.33%). eqmv's align/fingerprint iterate Python sets/str-hashes, which depend on PYTHONHASHSEED. Exp 5 set the seed inside spawned workers, which has no effect, so its hash seeds were random. `results/diag/` re-runs the mismatch sentences under 6 seeds, and 3 of 387 pairs flip. This artifact runs everything under PYTHONHASHSEED = 0. Every AUROC of `c_score_align` uses the FROZEN column.\n- **D5:** the prereg was written after the label-free matrix and before any label join.\n- **M1/M2 collinearity:** partial slopes with a VIF are reported. The EXPLORATORY single-predictor fits are labelled as such and are not the pre-registered test.\n- **M3-local:** the local judge score is discrete (0, .05, …). The primary flags exactly END_MAJ's flag rate (top rows by score, boundary ties split by `sha1('M3|'+row_key)`). The nearest plain threshold (0.05, flag rate 0.877) is a sensitivity (+slope diff −0.10 [−0.30, 0.08]). The API-judge M3 belongs to T1.\n- **Cost:** each slot is costed per sentence it actually covered (F = GPT-5.1 covers 200 sentences; G1b/G4/G5/G7/G8 cover 600), and a family's cost is the sum of its slots. The \"as-run\" totals/700 are also kept.\n- **Unparseable rows:** none in R_AB. Unparseable rows elsewhere get no matrix node and are listed per sentence (`unparseable_row_keys`). 14 R_AB rows with `|P_c| < 2` are excluded from the consensus-scorable population, with counts in `population`.\n- **G0 cross-check:** our R_AB flag agrees with exp 6's `metadata_in_R_AB` on 97.0% of rows. All 255 disagreements are non-LLM rows (240 gold-as-system, 15 ccg2lambda), which exp 6 included and exp 5's `regime()` excludes.\n\n## Layout\n\n| Path | What |\n|---|---|\n| `eval.py` | Orchestrator: copies inputs → matrix (staged) → PART A → PART B → figures → `eval_out.json` |\n| `src/pairwise.py` | **`pairwise_matrix(rows)`**: reusable label-free eqmv matrix for one sentence (vendored exp 5 eqmv, 3000 ms, 30 s pair cap) |\n| `src/run_matrix.py` | Staged, resumable, parallel (spawn, 4 workers, RLIMIT_AS 3.5 GB) matrix driver (`--stage mini/rab/rest`) |\n| `src/consensus_mx.py` | Matrix readouts: re-derived c (G2), c_exact, END_MAJ/PLUR/FAM2/FAMMAJ, classes, cliques, non-transitivity |\n| `src/mechanism.py` | **`ed_decomposition(y, endorsed)`**, cuts, graded trace, VOCAB_EXACT helpers, GEE, M1/M2/NET/SCATTER/M3-local |\n| `src/m4.py` | AUROC(k), fixed pools (cross-fitted), LOFO, cost table |\n| `src/frame.py`, `src/stats.py`, `src/paths.py` | Join + gates G0/G1; AUROC, stratified AUROC, sentence-cluster bootstrap (multiplicity weights); input paths |\n| `src/part_a.py`, `src/record.py`, `src/copy_inputs.py` | PART A driver; PART B verified record (i)–(x); input copy + sha256 |\n| `vendor_exp5/` | Read-only copy of exp 5 `src/` (peer_text, pool_scoring, vendor_c/common.py eqmv, …); hashes in `tables/source_hashes.csv` (identical_to_source=True) |\n| `audit/rederive.py`, `audit/m2_specificity.py` (+ `.json`) | Independent re-derivation of headline numbers (no `src/` import) + placebo tests; M2 specificity (interaction model, permutation nulls). Run by `eval.py` |\n| `reproducibility.md` | Exact environment, commands, seeds, runtimes and expected numbers |\n| `tests/test_identity.py` | 23 unit tests (identity, weighted AUROC = duplication, trapezoid, matrix readouts). `uv run pytest -q tests` |\n| `prereg_mech.json` (+`.sha256`) | Every analysis choice: rules, bins, frozen tercile cuts, GEE spec, confirm rules, seeds, B, min cells, deviations |\n| `results/pair_matrix_E.jsonl` | Raw matrix, 700 sentences (label-free) |\n| `pairwise_classes_E.jsonl` | **Join key for iteration 4**: per sentence, nodes/rows/families, pairs [i, j, equiv, reason, secs], components, cliques, non-transitive triples, z3 version, code sha. **No labels** |\n| `results/part_a.json` | Every PART A number (gates, G2, population, cuts headline, M1–M4, SCATTER, cost …) |\n| `results/population_RAB.pkl`, `results/rab_all.pkl`, `results/frame_min.pkl` | Analysis frames (regenerable) |\n| `results/matrix_determinism_check.json`, `results/prev_run*/` | Two earlier matrix computations; 0 of 29,107 pairs differ |\n| `results/diag/` | PYTHONHASHSEED diagnostic for the G2 mismatches |\n| `tables/ed_decomposition_cuts.csv` | e, d, AUROC_b, AUROC(c) with CIs by regime (R_AB, R_A, VOCAB_EXACT) × rule × {ALL, stratum, long pool, words tercile, n_conditions bin, exception type, tier} |\n| `tables/graded_trace_*.csv`, `tables/g2_mismatches.csv`, `tables/scatter_sentence_table.csv` | Graded ROC traces; G2 mismatch rows; per-sentence SI |\n| `tables/m4_*.csv` | AUROC(k) + cost frontier; all fixed pools k = 2/3/4; LOFO |\n| `tables/exp6_*.csv`, `b2_dead_end.csv`, `radj_gate.csv`, `pt_vs_s4_rerun.csv`, `corrections.csv`, `regimes_R_PANEL.csv`, `hypothesis_verdicts.csv`, `coverage_vs_request.csv`, `function_inventory.csv`, `perturb_counts.csv`, `label_facts.csv` | PART B verified record (i)–(x) |\n| `figures/fig1…fig4 (.png/.pdf/.json)` | e/d vs complexity; AUROC(k) + $; SI_err vs SI_cor; graded ROC with named operating points |\n| `eval_out.json` (+ `full_/mini_/preview_`) | `exp_eval_sol_out`: 324 `metrics_agg`, verdicts/deviations in `metadata`, one example per R_AB row (2,686) with `predict_c_score_align` (frozen), `predict_c_score_exact`, `predict_b_endmaj/endfam2/endplur/endfammaj`, `predict_c_k3_best_oof` |\n| `inputs_copy/` | Every small (<10 MB) input actually read, mirrored under `3_invention_loop/…` (large inputs are referenced by absolute path) |\n| `logs/` | Run logs (`eval_full_run.log` = the final run) |\n\n## How to run\n\n```bash\nuv venv .venv --python=3.12 && uv pip install --python .venv/bin/python -r pyproject.toml   # z3-solver==5.1.0.0 pinned (= exp 5)\nuv run pytest -q tests                        # 23 tests\nuv run eval.py --stage mini                   # 12-sentence matrix smoke test\nuv run eval.py --stage rab                    # matrix for the 292 R_AB sentences + every analysis\nuv run eval.py --stage all                    # all 700 sentences (≈ 2 min matrix + 3 min analysis on 4 vCPU)\nuv run eval.py --stage all --skip-matrix      # analyses only, reusing results/pair_matrix_E.jsonl\n```\n\nThe matrix stage appends to `results/pair_matrix_E.jsonl` and skips sentences already present. Move that file away to force a recompute. `eval.py` re-executes itself with `PYTHONHASHSEED=0`.\nTo regenerate the mini/preview files: `python .claude/skills/aii-json/scripts/aii_json_format_mini_preview.py --input eval_out.json`.\n\n## Restoring removed files\n\n`.aii/manifest.yaml` marks only these for deletion:\n\n- `.venv/` (regenerable): `uv venv .venv --python=3.12 && uv pip install --python .venv/bin/python -r pyproject.toml`\n- `__pycache__/`, `src/__pycache__/`, `tests/__pycache__/`, `vendor_exp5/**/__pycache__/`, `.pytest_cache/` (regenerable): created automatically by `uv run eval.py` or `uv run pytest -q tests`", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
````

### [14] TOOL CALL — Bash · 2026-09-24 18:35:32 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2; cat $W/src/pairwise.py; ls -la $W/vendor_exp5/vendor_c; wc -l $W/vendor_exp5/vendor_c/*.py $W/vendor_exp5/*.py; du -sh $W/results/*; cat $W/pyproject.toml
```

### [15] TOOL RESULT — Bash · 2026-09-24 18:35:32 UTC

```
{"stdout": "\"\"\"Label-free pairwise equivalence-modulo-vocabulary (eqmv) matrix among ALL parseable outputs of one sentence.\n\npairwise_matrix(rows) is the reusable function (iteration 4 applies it unchanged to R_COMP):\n  rows = [{'row_key', 'fol', 'slot', 'family' (vendor family), 'family_field', 'system_class'}] of ONE sentence.\n  -> {'nodes': [{node_id, canon_fol, rows: [{row_key, slot, family, family_field, system_class, is_peer}]}],\n      'pairs': [[i, j, equiv(True/False/None), reason, secs]], 'unparseable': [row_key...]}\n\nIt calls EXACTLY the iteration-1 eqmv (vendored exp 5 vendor_c/common.py, DEFAULT ms=3000) on the canonical strings\nparsed by the dataset-E parser (peer_text.parse_fol + canon), with the canonical argument order (min, max) the frozen\neq() cache used and a hard SIGALRM pair cap of 30 s (-> UNKNOWN = None). GOLD / CCG rows are nodes but never peers.\n\"\"\"\nfrom __future__ import annotations\n\nimport hashlib\nimport os\nimport resource\nimport signal\nimport sys\nimport time\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parent.parent\nVEND = ROOT / \"vendor_exp5\"\nfor p in (VEND, VEND / \"vendor_c\"):\n    if str(p) not in sys.path:\n        sys.path.insert(0, str(p))\n\nPAIR_CAP_S = 30\nEQMV_MS = 3000\n\n\nclass _TO(Exception):\n    pass\n\n\ndef _alarm(signum, frame):  # noqa: ARG001\n    raise _TO()\n\n\ndef init_worker(mem_gb: float = 3.5) -> None:\n    \"\"\"Same worker limits as exp 5's pool_scoring.init_worker (RLIMIT_AS 3.5 GB, SIGALRM handler).\"\"\"\n    os.environ[\"PYTHONHASHSEED\"] = \"0\"\n    try:\n        resource.setrlimit(resource.RLIMIT_AS, (int(mem_gb * 1024 ** 3), int(mem_gb * 1024 ** 3)))\n    except (ValueError, OSError):\n        pass\n    signal.signal(signal.SIGALRM, _alarm)\n\n\ndef _with_alarm(secs: int, fn, *a, **kw):\n    signal.signal(signal.SIGALRM, _alarm)\n    signal.alarm(secs)\n    try:\n        return fn(*a, **kw), False\n    except _TO:\n        return None, True\n    finally:\n        signal.alarm(0)\n\n\ndef pairwise_matrix(rows: list[dict], eqmv_ms: int = EQMV_MS, pair_cap_s: int = PAIR_CAP_S) -> dict:\n    \"\"\"Full node x node eqmv matrix for one sentence (see module docstring).\"\"\"\n    import peer_text as PT  # binds `fol` to the dataset-E parser before vendor_c is imported\n    from common import eqmv\n\n    nodes: dict[str, dict] = {}\n    unparseable = []\n    for r in rows:\n        e = PT.parse_fol(r[\"fol\"])\n        if e is None:\n            unparseable.append(r[\"row_key\"])\n            continue\n        cs = PT.canon(e)\n        nd = nodes.setdefault(cs, {\"canon_fol\": cs, \"rows\": []})\n        nd[\"rows\"].append({\"row_key\": r[\"row_key\"], \"slot\": r[\"slot\"], \"family\": r[\"family\"],\n                           \"family_field\": r.get(\"family_field\"), \"system_class\": r[\"system_class\"],\n                           \"is_peer\": r[\"system_class\"] == \"llm\"})\n    keys = sorted(nodes)\n    out_nodes = [dict(node_id=i, **nodes[k]) for i, k in enumerate(keys)]\n    pairs = []\n    for i in range(len(keys)):\n        for j in range(i + 1, len(keys)):\n            a, b = keys[i], keys[j]  # keys sorted -> (a, b) == (min, max), the frozen cache order\n            t0 = time.time()\n            res, to = _with_alarm(pair_cap_s, eqmv, PT.parse_fol(a), PT.parse_fol(b), eqmv_ms)\n            secs = round(time.time() - t0, 4)\n            if to or res is None:\n                pairs.append([i, j, None, \"pair_cap_timeout\", secs])\n            else:\n                pairs.append([i, j, res[0], res[1], secs])\n    return {\"nodes\": out_nodes, \"pairs\": pairs, \"unparseable\": unparseable}\n\n\ndef work(task: dict) -> dict:\n    \"\"\"Worker entry: one sentence task -> matrix record (label-free).\"\"\"\n    t0 = time.time()\n    m = pairwise_matrix(task[\"rows\"])\n    m.update({\"sentence_id\": task[\"sentence_id\"], \"source_stratum\": task[\"source_stratum\"], \"words\": task[\"words\"],\n              \"n_conditions\": task[\"n_conditions\"], \"secs_total\": round(time.time() - t0, 3), \"eqmv_ms\": EQMV_MS,\n              \"pair_cap_s\": PAIR_CAP_S})\n    return m\n\n\ndef code_sha() -> str:\n    h = hashlib.sha256()\n    for p in (Path(__file__), VEND / \"vendor_c\" / \"common.py\", VEND / \"vendor_c\" / \"repair_census.py\",\n              VEND / \"peer_text.py\", VEND / \"vendor_e\" / \"fol.py\"):\n        h.update(p.read_bytes())\n    return h.hexdigest()[:16]\ntotal 3152\ndrwxr-xr-x 3 root root 1018728 Sep 24 07:12 .\ndrwxr-xr-x 8 root root 1069299 Sep 24 07:12 ..\ndrwxr-xr-x 2 root root 1005936 Sep 24 07:18 __pycache__\n-rw-r--r-- 1 root root   38787 Sep 24 01:36 analysis.py\n-rw-r--r-- 1 root root    7277 Sep 24 01:36 common.py\n-rw-r--r-- 1 root root   22428 Sep 24 01:36 consensus.py\n-rw-r--r-- 1 root root    6993 Sep 24 01:36 eqcache.py\n-rw-r--r-- 1 root root    8989 Sep 24 01:36 fol.py\n-rw-r--r-- 1 root root   21207 Sep 24 01:36 peers.py\n-rw-r--r-- 1 root root   17800 Sep 24 01:36 repair_census.py\n-rw-r--r-- 1 root root    7507 Sep 24 01:36 rewrites.py\n   613 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/vendor_exp5/vendor_c/analysis.py\n   210 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/vendor_exp5/vendor_c/common.py\n   470 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/vendor_exp5/vendor_c/consensus.py\n   178 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/vendor_exp5/vendor_c/eqcache.py\n   263 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/vendor_exp5/vendor_c/fol.py\n   457 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/vendor_exp5/vendor_c/peers.py\n   458 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/vendor_exp5/vendor_c/repair_census.py\n   214 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/vendor_exp5/vendor_c/rewrites.py\n     0 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/vendor_exp5/__init__.py\n   882 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/vendor_exp5/analyse_E.py\n   133 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/vendor_exp5/data_views.py\n    83 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/vendor_exp5/local_judge_E.py\n  1025 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/vendor_exp5/peer_text.py\n   203 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/vendor_exp5/pool_scoring.py\n    83 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/vendor_exp5/posthoc_nf_fusion.py\n   214 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/vendor_exp5/run_api_E.py\n   251 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/vendor_exp5/score_E.py\n   629 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/vendor_exp5/screen_fit.py\n    59 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/vendor_exp5/write_deviations.py\n  6425 total\n1.1M\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/results/diag\n375K\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/results/frame_min.pkl\n512\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/results/matrix_determinism_check.json\n512\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/results/matrix_stage_rab.json\n512\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/results/matrix_stage_rest.json\n3.4M\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/results/pair_matrix_E.jsonl\n119K\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/results/part_a.json\n1.4M\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/results/population_RAB.pkl\n5.3M\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/results/prev_run\n5.3M\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/results/prev_run2\n1019K\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/results/rab_all.pkl\n[project]\nname = \"consensus-mechanism-audit\"\nversion = \"0.1.0\"\ndescription = \"Do wrong NL->FOL translations scatter? e/d decomposition of cross-family solver consensus + verified record (CPU only, $0)\"\nrequires-python = \">=3.12\"\n# every package pinned to the exact version installed in .venv (uv pip freeze, 2026-09-24); z3-solver pinned = exp 5\ndependencies = [\n  \"cloudpickle==3.1.2\",\n  \"contourpy==1.4.0\",\n  \"cycler==0.12.1\",\n  \"fonttools==4.66.0\",\n  \"formulaic==1.2.2\",\n  \"iniconfig==2.3.0\",\n  \"interface-meta==2.0.1\",\n  \"joblib==1.6.0\",\n  \"kiwisolver==1.5.1\",\n  \"loguru==0.7.3\",\n  \"matplotlib==3.11.2\",\n  \"narwhals==2.26.0\",\n  \"numpy==2.5.3\",\n  \"packaging==26.3\",\n  \"pandas==3.0.6\",\n  \"patsy==1.0.3\",\n  \"pillow==12.3.0\",\n  \"pluggy==1.6.0\",\n  \"psutil==7.2.2\",\n  \"pygments==2.21.0\",\n  \"pyparsing==3.3.3\",\n  \"pytest==9.1.1\",\n  \"python-dateutil==2.9.0.post0\",\n  \"pyyaml==6.0.3\",\n  \"scikit-learn==1.9.1\",\n  \"scipy==1.18.1\",\n  \"six==1.17.0\",\n  \"statsmodels==0.15.0\",\n  \"threadpoolctl==3.7.0\",\n  \"typing-extensions==4.16.0\",\n  \"wrapt==2.4.1\",\n  \"z3-solver==5.1.0.0\",\n]", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [16] ASSISTANT · 2026-09-24 18:35:42 UTC

```
Reading the artifact's source to decide how to split `eval.py` into notebook cells; next I'll build the demo data.
```

### [17] TOOL CALL — Bash · 2026-09-24 18:35:42 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2; grep -n "def " $W/src/mechanism.py $W/src/stats.py | head -60; grep -n "def pt_vs_s4" -A60 $W/src/record.py | head -80; head -c 1500 $W/tables/pt_vs_s4_rerun.csv
```

### [18] TOOL RESULT — Bash · 2026-09-24 18:35:42 UTC

```
{"stdout": "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/mechanism.py:26:def ed_decomposition(y, endorsed) -> dict:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/mechanism.py:39:def normalise_name(s: str) -> str:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/mechanism.py:44:def make_bins(df: pd.DataFrame, cut: dict) -> pd.DataFrame:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/mechanism.py:57:def prereg_cuts(rab: pd.DataFrame) -> dict:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/mechanism.py:69:def cell_stats(sub: pd.DataFrame, ycol: str, rule_cols: dict, boot: SentBoot, W_all: np.ndarray, pos: np.ndarray,\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/mechanism.py:106:def run_cuts(P: pd.DataFrame, boot: SentBoot, regimes: dict, rule_cols: dict) -> pd.DataFrame:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/mechanism.py:127:def graded_trace(y, c) -> dict:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/mechanism.py:154:def gee_fit(data: pd.DataFrame, formula: str, groups: str = \"sentence_id\") -> dict:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/mechanism.py:180:def vif_table(data: pd.DataFrame, cols: list[str], strat: bool = True) -> dict:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/mechanism.py:188:def verdict_slope(coef: dict | None, key: str, want: str) -> str:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/mechanism.py:197:def zcols(d: pd.DataFrame) -> pd.DataFrame:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/mechanism.py:204:def mechanism_M1_M2(P: pd.DataFrame, rule_cols: dict) -> dict:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/mechanism.py:244:def _ame(X: np.ndarray, yv: np.ndarray, w: np.ndarray, j: int) -> float:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/mechanism.py:250:def net_test(P: pd.DataFrame, boot: SentBoot, col: str = \"end_MAJ\", long_only: bool = False) -> dict:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/mechanism.py:261:        def ed(Wm, m):\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/mechanism.py:301:def scatter_index(P_lab: pd.DataFrame, sms: dict, cut: dict, boot_seed: int = 0, B: int = 2000) -> dict:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/mechanism.py:344:    def summarise(mask) -> dict:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/mechanism.py:387:def m3_local(P: pd.DataFrame, boot: SentBoot, exp6_judge_slope) -> dict:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/mechanism.py:417:    def slope(yv, w):\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/stats.py:13:def auc(y, s) -> float:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/stats.py:25:def strat_auc(y, s, strata) -> float:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/stats.py:42:    def __init__(self, sids, b: int = B_DEFAULT, seed: int = 0):\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/stats.py:53:def ci(vals, lo=2.5, hi=97.5):\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/stats.py:60:def boot_stat(boot: ClusterBoot, fn) -> list:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/stats.py:68:    def __init__(self, y, s):\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/stats.py:73:    def __call__(self, w) -> float:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/stats.py:87:    def __init__(self, y, s, strata):\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/stats.py:93:    def __call__(self, w) -> float:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/stats.py:110:    def __init__(self, sids, b: int = B_DEFAULT, seed: int = 0):\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/stats.py:118:    def weights(self, b: int, mask=None):\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/stats.py:122:    def W(self, mask=None):\n225:def pt_vs_s4() -> dict:\n226-    \"\"\"Independent re-implementation of the reviewer audit (own join, own stack, own bootstrap), plus stratified rows.\"\"\"\n227-    e6 = J(E6 / \"full_method_out.json\")\n228-    six = defaultdict(list)\n229-    for ds in e6[\"datasets\"]:\n230-        if ds[\"dataset\"] == \"E_heldout\":\n231-            for ex in ds[\"examples\"]:\n232-                six[(ex[\"metadata_item_id\"], json.loads(ex[\"input\"]).get(\"prompt_variant\"))].append(ex)\n233-    del e6\n234-    five = defaultdict(list)\n235-    for r in jl(E5 / \"results\" / \"per_item_E.jsonl\"):\n236-        five[(r[\"item_id\"], r[\"prompt_variant\"])].append(r)\n237-    recs = []\n238-    for k, L in six.items():\n239-        if len(L) != 1 or len(five.get(k, [])) != 1:\n240-            continue\n241-        ex, r = L[0], five[k][0]\n242-        if not ex.get(\"metadata_in_R_AB\") or ex[\"output\"] not in (\"ERROR\", \"CORRECT\"):\n243-            continue\n244-        recs.append({\"y\": int(ex[\"output\"] == \"ERROR\"), \"sid\": ex[\"metadata_sentence_id\"], \"fold\": ex[\"metadata_fold_E\"],\n245-                     \"stratum\": ex[\"metadata_strata\"][\"source_stratum\"], \"tier\": ex.get(\"metadata_label_tier\"),\n246-                     \"pt\": _f(r[\"p_peer_text\"]), \"cal\": _f(r[\"c_score_align\"]), \"s4\": _f(ex.get(\"predict_S4_local_oof_RAB\")),\n247-                     \"s4nj\": _f(ex.get(\"predict_S4_local_noLLMjudge_oof_RAB\")), \"jl\": _f(ex.get(\"predict_judge_local_qwen8b_disg\"))})\n248-    n_join = len(recs)\n249-    D = pd.DataFrame([r for r in recs if None not in (r[\"pt\"], r[\"cal\"], r[\"s4\"], r[\"s4nj\"], r[\"jl\"])]).reset_index(drop=True)\n250-    y = D.y.values\n251-\n252-    def stack(cols):\n253-        Z = D[cols].values\n254-        oof = np.zeros(len(D))\n255-        for f in sorted(D.fold.unique()):\n256-            tr, te = (D.fold != f).values, (D.fold == f).values\n257-            mu, sd = Z[tr].mean(0), Z[tr].std(0) + 1e-9\n258-            oof[te] = LogisticRegression(C=1.0, max_iter=2000).fit((Z[tr] - mu) / sd, y[tr]).predict_proba((Z[te] - mu) / sd)[:, 1]\n259-        return oof\n260-    D[\"s4_plus_pt\"] = stack([\"s4\", \"pt\"])\n261-    D[\"s4_refit\"] = stack([\"s4\"])\n262-    rev = J(REVIEW / \"audit\" / \"pt_vs_s4.json\")\n263-    rows = []\n264-    boot = SentBoot(D.sid.values, b=2000, seed=0)\n265-\n266-    def pair(a, b, mask, label, strat=False):\n267-        m = mask\n268-        W = boot.W(m)\n269-        if strat:\n270-            fa, fb = WStratAuc(y[m], D[a].values[m], D.stratum.values[m]), WStratAuc(y[m], D[b].values[m], D.stratum.values[m])\n271-            pt_ = strat_auc(y[m], D[a].values[m], D.stratum.values[m]) - strat_auc(y[m], D[b].values[m], D.stratum.values[m])\n272-        else:\n273-            fa, fb = WAuc(y[m], D[a].values[m]), WAuc(y[m], D[b].values[m])\n274-            pt_ = auc(y[m], D[a].values[m]) - auc(y[m], D[b].values[m])\n275-        ds = [fa(W[i]) - fb(W[i]) for i in range(W.shape[0])]\n276-        return {\"subset\": label, \"statistic\": \"stratified\" if strat else \"pooled\", \"quantity\": f\"{a} - {b}\", \"n\": int(m.sum()),\n277-                \"n_err\": int(y[m].sum()), \"n_sent\": int(D.sid[m].nunique()), \"delta\": pt_, \"ci_lo\": ci(ds)[0], \"ci_hi\": ci(ds)[1]}\n278-    ALL = np.ones(len(D), bool)\n279-    LONG = D.stratum.isin([\"L25\", \"L20\", \"EXC\"]).values\n280-    RA = (D.tier == \"A\").values & D.stratum.isin([\"L20\", \"EXC\"]).values\n281-    revmap = {(\"pt\", \"s4\"): \"delta_pt_minus_s4local\", (\"cal\", \"s4\"): \"delta_cal_minus_s4local\", (\"pt\", \"s4nj\"): \"delta_pt_minus_s4_noLLMjudge\",\n282-              (\"pt\", \"jl\"): \"delta_pt_minus_judge_local\", (\"s4_plus_pt\", \"s4_refit\"): \"nested_s4pt_minus_s4refit\"}\n283-    for (a, b), rk in revmap.items():\n284-        for mask, lab in ((ALL, \"R_AB pooled\"), (LONG, \"R_AB long (L25+L20+EXC)\"), (RA, \"R_A L20+EXC\")):\n285-            for strat in (False, True):\n# source: /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_6/full_method_out.json :: datasets[E_heldout].examples (metadata_in_R_AB, output, predict_S4_local_oof_RAB, predict_S4_local_noLLMjudge_oof_RAB, predict_judge_local_qwen8b_disg, metadata_fold_E)\n# source: /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/results/per_item_E.jsonl :: p_peer_text, c_score_align (raw)\n# source: /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/review_report/review_report/audit/pt_vs_s4.json :: reviewer target values\n# source: method: own join on (item_id, prompt_variant) unique rows; stack = train-fold standardise + LogisticRegression(C=1, max_iter=2000); sentence-cluster bootstrap B=2000 default_rng(0) as multiplicity weights (RNG order differs from the reviewer's)\nsubset,statistic,quantity,n,delta,reviewer_delta,point_match_1e-4,n_err,n_sent,ci_lo,ci_hi,reviewer_ci_lo,reviewer_ci_hi,ci_match_0.01\nR_AB pooled,pooled,AUROC pt,2672,0.7903039314968402,0.7903,True,,,,,,,\nR_AB pooled,pooled,AUROC cal,2672,0.7836862750124982,0.7837,True,,,,,,,\nR_AB pooled,pooled,AUROC s4,2672,0.7483191472997398,0.7483,True,,,,,,,\nR_AB pooled,pooled,AUROC s4nj,2672,0.7036824934945072,0.7037,True,,,,,,,\nR_AB pooled,pooled,AUROC jl,2672,0.7102264424247863,0.7102,True,,,,,,,\nR_AB pooled,pooled,AUROC s4_plus_pt,2672,0.8005749189216905,0.8006,True,,,,,,,\nR_AB pooled,pooled,AUROC s4_refit,2672,0.745365397187", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [19] TOOL CALL — Bash · 2026-09-24 18:35:48 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2; sed -n 1,40p $W/src/mechanism.py; sed -n 127,153p $W/src/mechanism.py; sed -n 1,35p $W/src/stats.py; python3 -c "
import json;d=json.load(open('$W/results/part_a.json'));print(list(d.keys()));
import pandas as pd
P=pd.read_pickle('$W/results/population_RAB.pkl');R=pd.read_pickle('$W/results/rab_all.pkl');print(P.shape,R.shape);print(P.columns.tolist());print(R.columns.tolist());print(P.dtypes.to_dict())
"
```

### [20] TOOL RESULT — Bash · 2026-09-24 18:35:50 UTC

```
{"stdout": "\"\"\"PART 2 + STEP 4: exact decomposition AUROC_b = 1 - (e + d)/2 of binary cross-family consensus, its cuts, the graded\ntrace, the VOCAB_EXACT aligner-free control, and the mechanism tests M1 / M2 / NET / SCATTER / M3-local.\n\ned_decomposition(y, endorsed) is the reusable function (iteration 4 applies it unchanged to R_COMP).\"\"\"\nfrom __future__ import annotations\n\nimport re\nimport warnings\nfrom collections import Counter, defaultdict\n\nimport numpy as np\nimport pandas as pd\nimport statsmodels.api as sm\nimport statsmodels.formula.api as smf\nfrom loguru import logger\nfrom sklearn.linear_model import LogisticRegression\nfrom statsmodels.stats.outliers_influence import variance_inflation_factor\n\nfrom stats import SentBoot, WAuc, WStratAuc, auc, ci, strat_auc\n\nRULES = [\"MAJ\", \"PLUR\", \"FAM2\", \"FAMMAJ\", \"MAJ_EXACT\"]\nMIN_ROWS, MIN_SENT = 30, 10\n\n\n# =================================================================================================== identity\ndef ed_decomposition(y, endorsed) -> dict:\n    \"\"\"y: 1 = ERROR, 0 = CORRECT; endorsed: 1 = the cross-family peer rule endorses the candidate.\n    Returns e = P(endorsed | ERROR) (error-endorsement), d = P(not endorsed | CORRECT) (correct-divergence) and\n    AUROC_b of b = 1 - endorsed, asserting the bookkeeping identity AUROC_b = 1 - (e + d)/2 (balanced accuracy).\"\"\"\n    y = np.asarray(y, int)\n    en = np.asarray(endorsed, int)\n    e = float(en[y == 1].mean())\n    d = float((1 - en[y == 0]).mean())\n    a = auc(y, 1 - en)\n    assert abs(a - (1 - (e + d) / 2)) < 1e-12, (a, e, d)\n    return {\"n_err\": int((y == 1).sum()), \"n_cor\": int((y == 0).sum()), \"e\": e, \"d\": d, \"auroc_b\": a}\n\n\ndef normalise_name(s: str) -> str:\n    return re.sub(r\"[^a-z0-9]\", \"\", s.lower())\ndef graded_trace(y, c) -> dict:\n    \"\"\"(e_t, d_t) at every distinct threshold t of the graded score (flag = c >= t); the ROC = (d_t, 1 - e_t).\n    Asserts the trapezoid area equals the tie-aware AUROC to 1e-9.\"\"\"\n    y = np.asarray(y, int)\n    c = np.asarray(c, float)\n    ts = np.unique(c)\n    pts = [(0.0, 0.0)]\n    tr = []\n    for t in ts[::-1]:\n        fl = c >= t\n        tpr = fl[y == 1].mean()\n        fpr = fl[y == 0].mean()\n        tr.append({\"t\": float(t), \"e_t\": float(1 - tpr), \"d_t\": float(fpr)})\n        pts.append((fpr, tpr))\n    pts.append((1.0, 1.0))\n    xs, ys = zip(*pts)\n    area = float(np.trapezoid(ys, xs))\n    a = auc(y, c)\n    assert abs(area - a) < 1e-9, (area, a)\n    named = {}\n    for nm, en in ((\"any_peer_agrees (c<1)\", c < 1), (\"majority END_MAJ (c<0.5)\", c < 0.5), (\"all_peers_agree (c==0)\", c == 0)):\n        named[nm] = {\"e\": float(en[y == 1].mean()), \"d\": float((~en)[y == 0].mean()),\n                     \"auroc_b\": float(1 - (en[y == 1].mean() + (~en)[y == 0].mean()) / 2)}\n    return {\"trace\": tr, \"trapezoid_area\": area, \"auroc\": a, \"named_points\": named}\n\n\n# =================================================================================================== GEE\n\"\"\"Statistics shared by every analysis: tie-aware AUROC, stratified (within-stratum pair) AUROC, and a\nsentence-cluster bootstrap that yields resample index arrays (numpy default_rng(0), B=2000).\"\"\"\nfrom __future__ import annotations\n\nfrom collections import defaultdict\n\nimport numpy as np\nfrom scipy.stats import rankdata\n\nB_DEFAULT = 2000\n\n\ndef auc(y, s) -> float:\n    \"\"\"Mann-Whitney AUROC with ties = 0.5 (identical to sklearn roc_auc_score).\"\"\"\n    y = np.asarray(y, dtype=float)\n    s = np.asarray(s, dtype=float)\n    n1 = int(y.sum())\n    n0 = len(y) - n1\n    if n1 == 0 or n0 == 0:\n        return float(\"nan\")\n    r = rankdata(s)\n    return float((r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))\n\n\ndef strat_auc(y, s, strata) -> float:\n    \"\"\"Within-stratum pair AUROC: sum_s w_s AUROC_s with w_s = n_err,s * n_cor,s (exp 5 'stratified').\"\"\"\n    y, s, strata = np.asarray(y, float), np.asarray(s, float), np.asarray(strata)\n    num = den = 0.0\n    for st in np.unique(strata):\n        m = strata == st\n        n1 = int(y[m].sum())\n        n0 = int(m.sum()) - n1\n        if n1 and n0:\n            num += auc(y[m], s[m]) * n1 * n0\n            den += n1 * n0\n['frame_info', 'gates', 'G2', 'nontransitivity', 'matrix_summary', 'population', 'vocab_exact', 'cuts_headline', 'stratified', 'graded_vs_binary', 'system_class_cut', 'M1_M2', 'NET', 'SCATTER', 'M3_local', 'M4']\n(2672, 34) (2686, 16)\n['row_key', 'sentence_id', 'item_id', 'slot', 'family_vendor', 'system', 'stratum', 'words', 'n_conditions', 'words_t', 'ncond_bin', 'exc_bin', 'label_tier', 'correct_not_equivalent', 'final_label', 'y_AB', 'c_frozen', 'c_score_exact', 'end_MAJ', 'end_PLUR', 'end_FAM2', 'end_FAMMAJ', 'end_MAJ_EXACT', 'c_k3_best_oof', 'vocab_exact', 'y_exact', 'npc', 'stratum_long', 'n_eq', 'n_eq_exact', 'judge_local', 'text', 'candidate_fol', 'fold_E']\n['row_key', 'sentence_id', 'stratum', 'words', 'n_conditions', 'label_tier', 'final_label', 'y_AB', 'c_frozen', 'c_frozen_raw', 'parseable', 'correct_not_equivalent', 'text', 'candidate_fol', 'family_vendor', 'fold_E']\n{'row_key': <StringDtype(storage='python', na_value=nan)>, 'sentence_id': <StringDtype(storage='python', na_value=nan)>, 'item_id': <StringDtype(storage='python', na_value=nan)>, 'slot': <StringDtype(storage='python', na_value=nan)>, 'family_vendor': <StringDtype(storage='python', na_value=nan)>, 'system': <StringDtype(storage='python', na_value=nan)>, 'stratum': <StringDtype(storage='python', na_value=nan)>, 'words': dtype('int64'), 'n_conditions': dtype('int64'), 'words_t': <StringDtype(storage='python', na_value=nan)>, 'ncond_bin': <StringDtype(storage='python', na_value=nan)>, 'exc_bin': <StringDtype(storage='python', na_value=nan)>, 'label_tier': <StringDtype(storage='python', na_value=nan)>, 'correct_not_equivalent': dtype('bool'), 'final_label': <StringDtype(storage='python', na_value=nan)>, 'y_AB': dtype('float64'), 'c_frozen': dtype('float64'), 'c_score_exact': dtype('float64'), 'end_MAJ': dtype('int64'), 'end_PLUR': dtype('int64'), 'end_FAM2': dtype('int64'), 'end_FAMMAJ': dtype('int64'), 'end_MAJ_EXACT': dtype('int64'), 'c_k3_best_oof': dtype('float64'), 'vocab_exact': dtype('bool'), 'y_exact': dtype('float64'), 'npc': dtype('float64'), 'stratum_long': dtype('bool'), 'n_eq': dtype('float64'), 'n_eq_exact': dtype('float64'), 'judge_local': dtype('float64'), 'text': <StringDtype(storage='python', na_value=nan)>, 'candidate_fol': <StringDtype(storage='python', na_value=nan)>, 'fold_E': dtype('int64')}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [21] TOOL CALL — Bash · 2026-09-24 18:36:02 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2; ls -la $W/audit $W/tables/ed_decomposition_cuts.csv $W/tables/graded_trace*; head -5 $W/tables/ed_decomposition_cuts.csv; head -c 600 $W/tables/graded_trace_c_score_align.csv; python3 -c "
import json;d=json.load(open('$W/full_eval_out.json'));print(list(d['metadata'].keys()));print(json.dumps(d['metadata']['record_summary'])[:1500]); print(len(json.dumps(d['metadata']['record_summary'])))
import pandas as pd
P=pd.read_pickle('$W/results/population_RAB.pkl'); print(P.groupby(['stratum','final_label']).size())"
```

### [22] TOOL RESULT — Bash · 2026-09-24 18:36:02 UTC

```
{"stdout": "-rw-r--r-- 1 root root   66979 Sep 24 03:18 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/tables/ed_decomposition_cuts.csv\n-rw-r--r-- 1 root root    2410 Sep 24 03:18 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/tables/graded_trace_c_score_align.csv\n-rw-r--r-- 1 root root    2215 Sep 24 03:18 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/tables/graded_trace_c_score_exact.csv\n\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/audit:\ntotal 2957\ndrwxr-xr-x  2 root root 1001905 Sep 24 03:14 .\ndrwxr-xr-x 12 root root 2005038 Sep 24 06:57 ..\n-rw-r--r--  1 root root     897 Sep 24 03:21 m2_specificity.json\n-rw-r--r--  1 root root    2530 Sep 24 03:14 m2_specificity.py\n-rw-r--r--  1 root root    3928 Sep 24 03:21 rederive.json\n-rw-r--r--  1 root root   12158 Sep 24 03:13 rederive.py\n# source: /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/results/pair_matrix_E.jsonl :: eqmv matrix (this artifact)\n# source: /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/results/per_item_E.jsonl :: c_score_align (FROZEN)\n# source: /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/data/E_labels.jsonl :: final_label, label_tier\nregime,dim,cell,rule,n_err,n_cor,n_sent,e,d,auroc_b,auroc_c,inference,e_ci_lo,e_ci_hi,d_ci_lo,d_ci_hi,auroc_b_ci_lo,auroc_b_ci_hi,auroc_c_ci_lo,auroc_c_ci_hi\nR_AB,ALL,ALL,MAJ,1810,862,283,0.12430939226519337,0.537122969837587,0.6692838189486099,0.7836862750124982,tested,0.08632103940742976,0.16356345636705458,0.45604153555695404,0.6194096166088986,0.6276229439323532,0.7118954511910262,0.7454823661917239,0.8199370599556595\nt,e_t,d_t\n1.0,0.44419889502762433,0.13109048723897912\n0.9166666666666666,0.4392265193370166,0.13225058004640372\n0.9090909090909091,0.41436464088397795,0.1519721577726218\n0.9,0.38011049723756907,0.16589327146171692\n0.8888888888888888,0.3475138121546961,0.17981438515081208\n0.875,0.3364640883977901,0.18677494199535963\n0.8571428571428572,0.3281767955801105,0.18793503480278423\n0.8333333333333334,0.31767955801104975,0.2088167053364269\n0.8181818181818181,0.2900552486187845,0.2505800464037123\n0.8,0.26464088397790053,0.2888631090487239\n0.7777777777777778,0.24419889502762426,0.3039443155452436\n0.75,0.22['evaluation_name', 'description', 'gates', 'verdicts', 'deviations', 'prereg_sha256', 'population', 'nontransitivity', 'vocab_exact', 'record_summary', 'scope_limit']\n{\"exp6\": {\"exp6_R_AB_pooled.csv\": {\"rows\": 28, \"n_match\": 28, \"n_checked\": 28}, \"exp6_R_A_pooled_L20_EXC_CTRL.csv\": {\"rows\": 28, \"n_match\": 28, \"n_checked\": 28}, \"exp6_COVERAGE_pooled.csv\": {\"rows\": 28, \"n_match\": 28, \"n_checked\": 28}, \"exp6_R_AB_long_L25_L20_EXC.csv\": {\"rows\": 28, \"n_match\": 28, \"n_checked\": 28}, \"exp6_Per_stratum_R_AB_AUROC.csv\": {\"rows\": 28, \"n_match\": 0, \"n_checked\": 0}, \"b2\": [{\"quantity\": \"gate balanced accuracy (track-H corrected, non-thinking reader)\", \"value\": 0.476019030474476, \"target\": \">= 0.85\", \"source\": \"/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_6/results/b2_gate.json :: primary_gate_trackH_corrected.bal_acc\"}, {\"quantity\": \"b2_score AUROC R_AB pooled\", \"value\": 0.5744, \"target\": \"\", \"source\": \"/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_6/results/analysis_E.json :: sets.R_AB|pooled.metrics.b2_score.auroc\"}, {\"quantity\": \"b2_score AUROC R_AB long pool\", \"value\": 0.5091, \"target\": \"\", \"source\": \"/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_6/results/analysis_E.json :: sets.R_AB|long_L25_L20_EXC.metrics.b2_score.auroc\"}, {\"quantity\": \"dropped-condition UNDETERMINED AUROC\", \"value\": 0.5293, \"target\": \"\", \"source\": \"/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_6/results/analysis_E.json :: b2.undet_share_DROP_vs_CORRECT.auroc\"}, {\"quantity\": \"thinki\n11386\nstratum  final_label\nCTRL     CORRECT        237\n         ERROR          146\nEXC      CORRECT        221\n         ERROR          381\nL20      CORRECT        229\n         ERROR          589\nL25      CORRECT        175\n         ERROR          694\ndtype: int64", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [23] TOOL CALL — Bash · 2026-09-24 18:36:18 UTC

```
mkdir -p build && cat > build/make_mini_data.py <<'EOF'
"""Build mini_demo_data.json from the evaluation artifact's saved outputs (run once, locally)."""
import json, math
from pathlib import Path
import numpy as np
import pandas as pd

W = Path("/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2")
OUT = Path(__file__).resolve().parent.parent / "mini_demo_data.json"
N_PER_CELL = 12  # 8 (stratum x label) cells -> 96 consensus-scorable rows, + 4 non-scorable rows = 100

P = pd.read_pickle(W / "results" / "population_RAB.pkl")
R = pd.read_pickle(W / "results" / "rab_all.pkl")
rng = np.random.default_rng(0)
keys = []
for (st, lab), g in P.groupby(["stratum", "final_label"]):
    keys += list(g.row_key.values[rng.choice(len(g), N_PER_CELL, replace=False)])
nonscor = [k for k in R.row_key if k not in set(P.row_key)]
keys += nonscor[:4]
Rs = R[R.row_key.isin(keys)].copy()
Ps = P[P.row_key.isin(keys)].copy()


def recs(df):
    out = []
    for r in df.to_dict("records"):
        o = {}
        for k, v in r.items():
            if hasattr(v, "item"):
                v = v.item()
            if isinstance(v, float) and math.isnan(v):
                v = None
            o[k] = v
        out.append(o)
    return out


def csv(name):
    return recs(pd.read_csv(W / "tables" / name, comment="#"))


full = json.loads((W / "full_eval_out.json").read_text())
data = {
    "description": ("Curated subset of the consensus-mechanism audit (T4, dataset E): the PART A result dict (part_a.json), "
                    "the PART B record summary + PT-vs-S4 rows, audit JSONs, prereg, the tables read by figures(), and "
                    f"{len(Rs)} R_AB rows (stratified 12 per stratum x label, seed 0, plus {len(nonscor[:4])} non-scorable rows) "
                    "with their population columns (c_frozen, c_score_exact, end_* endorsements, c_k3_best_oof, ...)."),
    "part_a": json.loads((W / "results" / "part_a.json").read_text()),
    "record_summary": full["metadata"]["record_summary"],
    "pt_vs_s4_rows": csv("pt_vs_s4_rerun.csv"),
    "audit_rederive": json.loads((W / "audit" / "rederive.json").read_text()),
    "audit_m2_specificity": json.loads((W / "audit" / "m2_specificity.json").read_text()),
    "prereg_mech": json.loads((W / "prereg_mech.json").read_text()),
    "prereg_sha256": (W / "prereg_mech.sha256").read_text(),
    "tables": {"ed_decomposition_cuts": csv("ed_decomposition_cuts.csv"),
               "graded_trace_c_score_align": csv("graded_trace_c_score_align.csv"),
               "graded_trace_c_score_exact": csv("graded_trace_c_score_exact.csv")},
    "rab_rows": recs(Rs),
    "population_rows": recs(Ps),
}
s = json.dumps(data, default=lambda x: x.item() if hasattr(x, "item") else str(x))
s = s.replace("/ai-inventor/aii_data/runs/run_u75jRHUss0zo/", "")  # no absolute server paths in published files
OUT.write_text(s)
print(OUT, len(s) / 1e6, "MB", len(Rs), len(Ps))
EOF
python3 build/make_mini_data.py && grep -c "ai-inventor" mini_demo_data.json
```

### [24] TOOL RESULT — Bash · 2026-09-24 18:36:20 UTC

```
{"stdout": "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_FWy8D4_y9GBn/mini_demo_data.json 0.432415 MB 100 96\n0", "stderr": "", "interrupted": false, "isImage": false, "returnCodeInterpretation": "No matches found", "noOutputExpected": false}
```

### [25] TOOL CALL — Bash · 2026-09-24 18:36:50 UTC

```
cp /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/eval.py build/eval_original.py && python3 -c "
import json;d=json.load(open('mini_demo_data.json'));A=d['part_a'];print(A['graded_vs_binary'].keys());print(list(A['M4']['random_k_primary']['k'].keys()), list(A['M4']['fixed_pools'].keys()));print(A['population'])" ; pip list 2>/dev/null | grep -i nbformat
```

### [26] TOOL RESULT — Bash · 2026-09-24 18:36:50 UTC

```
{"stdout": "dict_keys(['auroc_c_score_align', 'auroc_b_END_MAJ', 'delta_graded_minus_binary', 'delta_ci', 'trapezoid_area_check', 'named_points', 'auroc_c_score_exact', 'delta_align_minus_exact', 'delta_align_minus_exact_ci', 'named_points_exact', 'share_endorsements_needing_align_or_gran', 'share_endorsements_needing_align_or_gran_ERROR', 'share_endorsements_needing_align_or_gran_CORRECT'])\n['1', '2', '3', '4', '5', '6', '7'] ['3', '2', '4']\n{'R_AB_rows': 2686, 'consensus_scorable': 2672, 'excluded_unparseable': 0, 'excluded_npc_lt2': 14, 'scorable_err': 1810, 'scorable_cor': 862, 'n_sent': 283}", "stderr": "", "interrupted": false, "isImage": false, "returnCodeInterpretation": "No matches found", "noOutputExpected": false}
```

### [27] TOOL CALL — Write · 2026-09-24 18:38:06 UTC

```
File: /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_FWy8D4_y9GBn/build/make_notebook.py

"""Build code_demo.ipynb from the artifact's eval.py (copied to build/eval_original.py).

The two analysis functions of eval.py (figures, build_eval_out) are copied VERBATIM by slicing the original source;
only file reads are swapped for the loaded `data` dict (each swap keeps the original line as a `# was:` comment)."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = (HERE / "eval_original.py").read_text()
OUT = HERE.parent / "code_demo.ipynb"
URL = ("https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/"
       "main/round-3/evaluation-2/demo/mini_demo_data.json")


def seg(start: str, end: str) -> str:
    i = SRC.index(start)
    j = SRC.index(end, i)
    return SRC[i:j].rstrip() + "\n"


def sub(s: str, old: str, new: str) -> str:
    assert old in s, old
    return s.replace(old, new)


# ------------------------------------------------------------------ verbatim segments with minimal swaps
jdump_src = seg("def jdump(", "# ====")

fig_src = seg("def figures(A: dict):", "# =================================================================================================== eval_out")
fig_src = sub(fig_src, '    matplotlib.use("Agg")\n',
              '    # matplotlib.use("Agg")  # notebook: keep the inline backend (figures are closed here and shown from PNG below)\n')
fig_src = sub(fig_src, 'cuts = pd.read_csv(ROOT / "tables" / "ed_decomposition_cuts.csv", comment="#")',
              'cuts = pd.DataFrame(data["tables"]["ed_decomposition_cuts"])  # was: pd.read_csv(ROOT / "tables" / "ed_decomposition_cuts.csv", comment="#")')
fig_src = sub(fig_src, 'tr = pd.read_csv(ROOT / "tables" / fn)',
              'tr = pd.DataFrame(data["tables"][fn[:-4]])  # was: pd.read_csv(ROOT / "tables" / fn)')
fig_src = fig_src.replace("dpi=200)", "dpi=FIG_DPI)")

beo_src = seg("def build_eval_out(A: dict, B: dict) -> dict:", "@logger.catch(reraise=True)")
beo_src = sub(beo_src, 'P = pd.read_pickle(ROOT / "results" / "population_RAB.pkl").set_index("row_key")',
              'P = pd.DataFrame(data["population_rows"]).set_index("row_key")  # was: pd.read_pickle(ROOT / "results" / "population_RAB.pkl").set_index("row_key")')
beo_src = sub(beo_src, 'R = pd.read_pickle(ROOT / "results" / "rab_all.pkl")',
              'R = pd.DataFrame(data["rab_rows"]).head(N_EXAMPLES)  # was: pd.read_pickle(ROOT / "results" / "rab_all.pkl")')
beo_src = sub(beo_src, 'au = json.loads((ROOT / "audit" / "rederive.json").read_text())',
              'au = data["audit_rederive"]  # was: json.loads((ROOT / "audit" / "rederive.json").read_text())')
beo_src = sub(beo_src, 'ms = json.loads((ROOT / "audit" / "m2_specificity.json").read_text())',
              'ms = data["audit_m2_specificity"]  # was: json.loads((ROOT / "audit" / "m2_specificity.json").read_text())')
beo_src = sub(beo_src, 'pre = json.loads((ROOT / "prereg_mech.json").read_text())',
              'pre = data["prereg_mech"]  # was: json.loads((ROOT / "prereg_mech.json").read_text())')
beo_src = sub(beo_src, '"prereg_sha256": (ROOT / "prereg_mech.sha256").read_text().split()[0]',
              '"prereg_sha256": data["prereg_sha256"].split()[0]')

cells = []


def md(s):
    cells.append({"cell_type": "markdown", "metadata": {}, "source": s.strip("\n")})


def code(s):
    cells.append({"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": s.strip("\n")})


md(r"""
# Why cross-model agreement flags logic errors — consensus-mechanism audit (demo)

This notebook is a runnable walk-through of the evaluation script **`eval.py`** of the artifact
*"Why cross-model agreement flags logic errors"* (T4 consensus-mechanism audit on NL→FOL dataset **E**; CPU only, no LLM calls).

**Question.** A candidate first-order-logic (FOL) translation of a sentence gets a *graded consensus score*
`c_score_align` = share of other vendor families' outputs for the same sentence that are **not** z3-equivalent
(modulo vocabulary alignment, "eqmv") to it. Why does that label-free score predict faithfulness (AUROC 0.784 on R_AB)?
The "Anna Karenina" premise says correct translations converge while wrong ones scatter.

**What `eval.py` does** (orchestrator):
1. copies inputs, computes the label-free pairwise z3 **eqmv matrix** (29,107 pairs over 700 sentences, ~2 min on 4 vCPU),
2. **PART A** (`src/part_a.py`): gates G0/G1/G2, the exact identity `AUROC_b = 1 − (e+d)/2` for binary majority consensus
   (e = P(endorsed | ERROR), d = P(not endorsed | CORRECT)), mechanism tests M1/M2/NET/SCATTER/M3-local/M4, LOFO and cost,
3. **PART B** (`src/record.py`): file-sourced verified record of iteration 2,
4. independent audits (`audit/*.py`), **`figures(A)`** and **`build_eval_out(A, B)`** → `eval_out.json`.

**In this demo** steps 1–3 (z3 matrix + ~2,000 lines of analysis over large private inputs) are *not* rerun: their saved
outputs (`part_a.json`, record summary, audit JSONs, the tables read by `figures()`) are shipped in `mini_demo_data.json`
together with **100 R_AB rows** (12 per stratum × label, plus 4 non-scorable rows). The notebook then
* recomputes the e/d decomposition, graded-vs-binary AUROC and graded ROC trace on those rows with the artifact's own
  `ed_decomposition()` / `graded_trace()` / `auc()` functions,
* runs `figures(A)` and `build_eval_out(A, B)` from `eval.py` unchanged except for file reads → `data`,
* shows the headline numbers and figures.
""")

code(r"""
import subprocess, sys
def _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])

# loguru — NOT pre-installed on Colab, always install
_pip('loguru==0.7.3')

# numpy, pandas, scipy, matplotlib — pre-installed on Colab, install locally only (at Colab's versions)
if 'google.colab' not in sys.modules:
    _pip('numpy==2.0.2', 'pandas==2.2.2', 'scipy==1.16.3', 'matplotlib==3.10.0')
""")

md(r"""
## Imports

The original import block of `eval.py`, copied as-is. Two notebook-only removals (kept as comments):
the `os.execv` re-launch that forces `PYTHONHASHSEED=0` (it only matters for the z3 eqmv matrix, which is not recomputed here)
and the 20 GB `RLIMIT_AS` cap (a script-level safety net, not wanted inside a Jupyter kernel).
""")

code(r'''
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

# if os.environ.get("PYTHONHASHSEED") != "0":  # eqmv's align()/fp() hash strings: fix the seed for reproducibility
#     os.environ["PYTHONHASHSEED"] = "0"
#     os.execv(sys.executable, [sys.executable] + sys.argv)
# (notebook: cannot re-exec the kernel; only the z3 matrix stage, which is not rerun here, depends on the hash seed)

import numpy as np
import pandas as pd
from loguru import logger

ROOT = Path.cwd()  # was: Path(__file__).resolve().parent — outputs (figures/, logs/, eval_out.json) go to the working dir
# sys.path.insert(0, str(ROOT / "src"))  # notebook: the src/ functions used below are inlined instead
(ROOT / "logs").mkdir(exist_ok=True)
logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(ROOT / "logs" / "eval.log", rotation="30 MB", level="DEBUG")

import resource  # noqa: E402

# resource.setrlimit(resource.RLIMIT_AS, (20 * 1024 ** 3, 20 * 1024 ** 3))  # 29 GB container; fail fast instead of OOM
# (notebook: not applied inside the kernel)

# notebook-only additions: src/stats.py AUROC needs rankdata; display for the saved figures
from scipy.stats import rankdata
import matplotlib.pyplot as plt
from IPython.display import Image, display
''')

md("## Data loading\n\nLoads `mini_demo_data.json` from GitHub, falling back to a local copy.")

code(f'''
GITHUB_DATA_URL = "{URL}"
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
''')

code(r'''
data = load_data()
print(data["description"])
print("keys:", list(data.keys()))
print("R_AB demo rows:", len(data["rab_rows"]), "| consensus-scorable (population) rows:", len(data["population_rows"]))
''')

md(r"""
## Config

The only tunable of the demo is how many R_AB rows are pushed through the per-row code
(`build_eval_out()` examples and the recomputation cell). The original run used **all 2,686 R_AB rows**
(2,672 consensus-scorable); the demo data holds a stratified 100-row subset, and the whole notebook runs in seconds,
so it uses all of them. `FIG_DPI` is the original figure resolution.
""")

code(r'''
N_EXAMPLES = 100   # R_AB rows processed (max 100 in mini_demo_data.json; original run: 2686)
FIG_DPI = 200      # original eval.py value
N_SHOW = 5         # example rows printed in the results section
''')

md(r"""
## JSON helper (from `eval.py`)
""")

code(jdump_src)

md(r"""
## Recompute the e/d decomposition on the demo rows

The heart of the audit is a bookkeeping identity for *binary* consensus rules. With `y = 1` for ERROR rows and
`endorsed = 1` when the cross-family peer rule (e.g. END_MAJ: a majority of other vendor families produce an eqmv-equivalent
formula) endorses the candidate:

* **e** = P(endorsed | ERROR) — wrong translations that peers agree with (error endorsement),
* **d** = P(not endorsed | CORRECT) — correct translations peers do *not* agree with (correct divergence),
* `AUROC_b = 1 − (e + d)/2` (balanced accuracy of the flag `1 − endorsed`).

The graded score `c_score_align` keeps the full fraction of disagreeing peers; `graded_trace()` gives its ROC as the
(e_t, d_t) pair at every threshold. The three functions below are copied **verbatim** from the artifact's
`src/stats.py` (`auc`) and `src/mechanism.py` (`ed_decomposition`, `graded_trace`), and applied to the demo rows' saved
per-row consensus columns (`c_frozen` = frozen c_score_align, `c_score_exact`, `end_MAJ`, `end_PLUR`, `end_FAM2`,
`end_FAMMAJ`, `end_MAJ_EXACT`). With only 96 scorable rows (balanced 48/48 by design, unlike the 1810/862 population) the
numbers are noisy; the full-population values from `part_a.json` are printed alongside.
""")

code(r'''
# ---- src/stats.py
def auc(y, s) -> float:
    """Mann-Whitney AUROC with ties = 0.5 (identical to sklearn roc_auc_score)."""
    y = np.asarray(y, dtype=float)
    s = np.asarray(s, dtype=float)
    n1 = int(y.sum())
    n0 = len(y) - n1
    if n1 == 0 or n0 == 0:
        return float("nan")
    r = rankdata(s)
    return float((r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


# ---- src/mechanism.py
def ed_decomposition(y, endorsed) -> dict:
    """y: 1 = ERROR, 0 = CORRECT; endorsed: 1 = the cross-family peer rule endorses the candidate.
    Returns e = P(endorsed | ERROR) (error-endorsement), d = P(not endorsed | CORRECT) (correct-divergence) and
    AUROC_b of b = 1 - endorsed, asserting the bookkeeping identity AUROC_b = 1 - (e + d)/2 (balanced accuracy)."""
    y = np.asarray(y, int)
    en = np.asarray(endorsed, int)
    e = float(en[y == 1].mean())
    d = float((1 - en[y == 0]).mean())
    a = auc(y, 1 - en)
    assert abs(a - (1 - (e + d) / 2)) < 1e-12, (a, e, d)
    return {"n_err": int((y == 1).sum()), "n_cor": int((y == 0).sum()), "e": e, "d": d, "auroc_b": a}


def graded_trace(y, c) -> dict:
    """(e_t, d_t) at every distinct threshold t of the graded score (flag = c >= t); the ROC = (d_t, 1 - e_t).
    Asserts the trapezoid area equals the tie-aware AUROC to 1e-9."""
    y = np.asarray(y, int)
    c = np.asarray(c, float)
    ts = np.unique(c)
    pts = [(0.0, 0.0)]
    tr = []
    for t in ts[::-1]:
        fl = c >= t
        tpr = fl[y == 1].mean()
        fpr = fl[y == 0].mean()
        tr.append({"t": float(t), "e_t": float(1 - tpr), "d_t": float(fpr)})
        pts.append((fpr, tpr))
    pts.append((1.0, 1.0))
    xs, ys = zip(*pts)
    area = float(np.trapezoid(ys, xs))
    a = auc(y, c)
    assert abs(area - a) < 1e-9, (area, a)
    named = {}
    for nm, en in (("any_peer_agrees (c<1)", c < 1), ("majority END_MAJ (c<0.5)", c < 0.5), ("all_peers_agree (c==0)", c == 0)):
        named[nm] = {"e": float(en[y == 1].mean()), "d": float((~en)[y == 0].mean()),
                     "auroc_b": float(1 - (en[y == 1].mean() + (~en)[y == 0].mean()) / 2)}
    return {"trace": tr, "trapezoid_area": area, "auroc": a, "named_points": named}
''')

code(r'''
# demo population: the consensus-scorable rows among the first N_EXAMPLES R_AB rows
_keys = set(pd.DataFrame(data["rab_rows"]).head(N_EXAMPLES).row_key)
Pd = pd.DataFrame(data["population_rows"])
Pd = Pd[Pd.row_key.isin(_keys)].reset_index(drop=True)
y = Pd.y_AB.astype(int).values
print(f"demo population: {len(Pd)} rows ({y.sum()} ERROR / {(1 - y).sum()} CORRECT), {Pd.sentence_id.nunique()} sentences")

A = data["part_a"]
full_head = {(r["regime"], r["rule"]): r for r in A["cuts_headline"]}
demo_ed = {}
for rule in ["MAJ", "PLUR", "FAM2", "FAMMAJ", "MAJ_EXACT"]:
    demo_ed[rule] = ed_decomposition(y, Pd[f"end_{rule}"].values)
demo_graded = {"c_score_align": graded_trace(y, Pd.c_frozen.values), "c_score_exact": graded_trace(y, Pd.c_score_exact.values)}

rows = []
for rule, r in demo_ed.items():
    f = full_head.get(("R_AB", rule), {})
    rows.append({"rule": f"END_{rule} (binary)", "demo e": r["e"], "demo d": r["d"], "demo AUROC": r["auroc_b"],
                 "full e": f.get("e"), "full d": f.get("d"), "full AUROC": f.get("auroc_b")})
g = A["graded_vs_binary"]
for nm, key in (("c_score_align", "auroc_c_score_align"), ("c_score_exact", "auroc_c_score_exact")):
    rows.append({"rule": f"{nm} (graded)", "demo AUROC": demo_graded[nm]["auroc"], "full AUROC": g[key]})
demo_table = pd.DataFrame(rows)
print(demo_table.round(3).to_string(index=False))
print("\nidentity AUROC_b = 1-(e+d)/2 asserted for every rule; graded trapezoid area == AUROC asserted")
''')

md(r"""
## PART A / PART B results (saved outputs of the heavy stages)

In `eval.py`'s `main()` the next steps are `subprocess` calls to `src/copy_inputs.py` and `src/run_matrix.py`
(z3 matrix), then `A = part_a.run()` and the PART B record builders (`RC.exp6_tables()`, `RC.pt_vs_s4()`, …) and the
two audit scripts. They need the full raw inputs of earlier iterations, so here `A` and `B` are rebuilt from their saved
outputs with the same structure `build_eval_out()` expects: `A` = `results/part_a.json`, `B["summary"]` = the record
summary stored in `eval_out.json`, `B["pt_vs_s4"]["rows"]` = `tables/pt_vs_s4_rerun.csv`.
""")

code(r'''
t0 = time.time()
# original main():  A = part_a.run();  B = {"summary": {...}};  B["pt_vs_s4"] = RC.pt_vs_s4(); ...
A = data["part_a"]
B = {"summary": data["record_summary"]}
B["pt_vs_s4"] = {"rows": data["pt_vs_s4_rows"]}
logger.info(f"PART A keys: {list(A.keys())}")
logger.info(f"PART B record summary keys: {list(B['summary'].keys())}; pt_vs_s4 rows: {len(B['pt_vs_s4']['rows'])}")
''')

md(r"""
## Figures (`figures(A)` from `eval.py`)

Copied verbatim; the only changes are that the three CSV tables are read from `data["tables"]` instead of `tables/*.csv`,
the Agg backend switch is commented out, and `dpi` uses `FIG_DPI`. It writes `figures/fig1…fig4` (.png/.pdf/.json):

1. **fig1** — e and d of END_MAJ by n_conditions bin and words tercile, per regime (R_AB, R_A, VOCAB_EXACT);
2. **fig2** — AUROC(k) of the graded score as the peer pool grows to k other vendor families, with $/sentence;
3. **fig3** — scatter index: P(two cross-family ERROR outputs are equivalent) vs the same for CORRECT outputs;
4. **fig4** — graded ROC of `c_score_align` / `c_score_exact` with the named binary operating points.
""")

code(fig_src)

code(r'''
figures(A)
logger.info(f"figures written to {ROOT / 'figures'}")
''')

md(r"""
## `eval_out.json` (`build_eval_out(A, B)` from `eval.py`)

Copied verbatim except for the input reads (`population_RAB.pkl`, `rab_all.pkl`, audit JSONs, prereg → `data`, and `R`
limited to `N_EXAMPLES` rows). It flattens PART A/B into `metrics_agg` (335 named metrics in the full run), attaches
the verdicts for M1/M2/NET/SCATTER/M3-local/M4/LOFO with their pre-registered rules, and writes one example per R_AB row
with the per-row predictions `predict_c_score_align`, `predict_c_score_exact`, `predict_b_endmaj`, … (non-scorable rows get `NA`).
""")

code(beo_src)

code(r'''
out = build_eval_out(A, B)
jdump(ROOT / "eval_out.json", out)
logger.info(f"eval_out.json written: {len(out['metrics_agg'])} metrics, {len(out['datasets'][0]['examples'])} examples; {time.time() - t0:.0f}s")
''')

md(r"""
## Results

Headline metrics (full 2,672-row population, from `metrics_agg`), the pre-registered verdicts, a few example rows,
a per-row score plot for the demo rows, and the four figures produced by `figures(A)`.
""")

code(r'''
ma = out["metrics_agg"]
head = [("graded c_score_align AUROC", "auroc_c_score_align"), ("binary END_MAJ AUROC", "auroc_b_END_MAJ"),
        ("delta graded - binary", "delta_graded_minus_binary"), ("  CI lo", "delta_graded_minus_binary_ci_lo"), ("  CI hi", "delta_graded_minus_binary_ci_hi"),
        ("END_MAJ e (error endorsement)", "e_maj_R_AB"), ("END_MAJ d (correct divergence)", "d_maj_R_AB"),
        ("aligner-free c_score_exact AUROC", "auroc_c_score_exact"),
        ("NET Delta(e+d), words T3-T1", "net_delta_words"),
        ("SI_err (identical-wrong rate)", "si_err_mean"), ("SI_cor (identical-correct rate)", "si_cor_mean"),
        ("SI ratio cor/err", "si_ratio_cor_over_err"), ("k95 (peers for 95% of max AUROC)", "k95"),
        ("best 3-family pool OOF AUROC", "m4_k3_crossfit_oof_auroc"), ("LOFO min delta", "lofo_min_delta"),
        ("G2 mismatch rate", "g2_mismatch_rate"), ("eqmv non-transitivity", "nontransitivity_rate")]
print(pd.DataFrame([{"quantity": n, "value": ma.get(k)} for n, k in head]).round(4).to_string(index=False))
print(f"\n{len(ma)} metrics in metrics_agg\n\nVerdicts:")
for k, v in out["metadata"]["verdicts"].items():
    print(f"  {k:9s} {v['verdict'] if isinstance(v, dict) and 'verdict' in v else v}")

ex = pd.DataFrame(out["datasets"][0]["examples"])
print("\nExample rows:")
for r in ex.head(N_SHOW).itertuples():
    inp = json.loads(r.input)
    print(f"- [{r.output}] {inp['text'][:110]}...\n    FOL: {inp['candidate_fol'][:110]}\n    c_score_align={r.predict_c_score_align}  b_endmaj={r.predict_b_endmaj}")

# per-row scores of the demo rows, by label (higher c = more peers disagree -> more likely ERROR)
fig, ax = plt.subplots(1, 2, figsize=(10, 3.8))
for lab, col in (("CORRECT", "#4c9f70"), ("ERROR", "#c8553d")):
    v = Pd.loc[Pd.final_label == lab, "c_frozen"].values
    ax[0].hist(v, bins=np.linspace(0, 1, 11), alpha=0.55, color=col, label=f"{lab} (n={len(v)})")
ax[0].set_xlabel("c_score_align (share of disagreeing peer families)")
ax[0].set_ylabel("demo rows")
ax[0].legend(frameon=False)
ax[0].set_title("Demo rows: graded consensus score by label", fontsize=9)
rl = list(demo_ed)
x = np.arange(len(rl))
ax[1].bar(x - 0.2, [demo_ed[r]["e"] for r in rl], 0.4, color="#1b6ca8", label="e = P(endorsed | ERROR)")
ax[1].bar(x + 0.2, [demo_ed[r]["d"] for r in rl], 0.4, color="#c8553d", label="d = P(not endorsed | CORRECT)")
ax[1].set_xticks(x, [f"END_{r}" for r in rl], fontsize=7)
ax[1].set_ylim(0, 1)
ax[1].legend(frameon=False, fontsize=7)
ax[1].set_title("Demo rows: e/d of binary consensus rules", fontsize=9)
fig.tight_layout()
plt.show()

for f in ("fig1_e_d_by_complexity", "fig2_auroc_k", "fig3_scatter_index", "fig4_graded_roc"):
    print(f)
    display(Image(filename=str(ROOT / "figures" / f"{f}.png"), width=800))
''')

nb = {"cells": cells, "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                                   "language_info": {"name": "python"}}, "nbformat": 4, "nbformat_minor": 5}
for i, c in enumerate(nb["cells"]):
    c["id"] = f"cell-{i:02d}"
OUT.write_text(json.dumps(nb, indent=1))
print(OUT, len(cells), "cells")
```

### [28] TOOL RESULT — Write · 2026-09-24 18:38:06 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_FWy8D4_y9GBn/build/make_notebook.py", "content": "\"\"\"Build code_demo.ipynb from the artifact's eval.py (copied to build/eval_original.py).\n\nThe two analysis functions of eval.py (figures, build_eval_out) are copied VERBATIM by slicing the original source;\nonly file reads are swapped for the loaded `data` dict (each swap keeps the original line as a `# was:` comment).\"\"\"\nimport json\nfrom pathlib import Path\n\nHERE = Path(__file__).resolve().parent\nSRC = (HERE / \"eval_original.py\").read_text()\nOUT = HERE.parent / \"code_demo.ipynb\"\nURL = (\"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/\"\n       \"main/round-3/evaluation-2/demo/mini_demo_data.json\")\n\n\ndef seg(start: str, end: str) -> str:\n    i = SRC.index(start)\n    j = SRC.index(end, i)\n    return SRC[i:j].rstrip() + \"\\n\"\n\n\ndef sub(s: str, old: str, new: str) -> str:\n    assert old in s, old\n    return s.replace(old, new)\n\n\n# ------------------------------------------------------------------ verbatim segments with minimal swaps\njdump_src = seg(\"def jdump(\", \"# ====\")\n\nfig_src = seg(\"def figures(A: dict):\", \"# =================================================================================================== eval_out\")\nfig_src = sub(fig_src, '    matplotlib.use(\"Agg\")\\n',\n              '    # matplotlib.use(\"Agg\")  # notebook: keep the inline backend (figures are closed here and shown from PNG below)\\n')\nfig_src = sub(fig_src, 'cuts = pd.read_csv(ROOT / \"tables\" / \"ed_decomposition_cuts.csv\", comment=\"#\")',\n              'cuts = pd.DataFrame(data[\"tables\"][\"ed_decomposition_cuts\"])  # was: pd.read_csv(ROOT / \"tables\" / \"ed_decomposition_cuts.csv\", comment=\"#\")')\nfig_src = sub(fig_src, 'tr = pd.read_csv(ROOT / \"tables\" / fn)',\n              'tr = pd.DataFrame(data[\"tables\"][fn[:-4]])  # was: pd.read_csv(ROOT / \"tables\" / fn)')\nfig_src = fig_src.replace(\"dpi=200)\", \"dpi=FIG_DPI)\")\n\nbeo_src = seg(\"def build_eval_out(A: dict, B: dict) -> dict:\", \"@logger.catch(reraise=True)\")\nbeo_src = sub(beo_src, 'P = pd.read_pickle(ROOT / \"results\" / \"population_RAB.pkl\").set_index(\"row_key\")',\n              'P = pd.DataFrame(data[\"population_rows\"]).set_index(\"row_key\")  # was: pd.read_pickle(ROOT / \"results\" / \"population_RAB.pkl\").set_index(\"row_key\")')\nbeo_src = sub(beo_src, 'R = pd.read_pickle(ROOT / \"results\" / \"rab_all.pkl\")',\n              'R = pd.DataFrame(data[\"rab_rows\"]).head(N_EXAMPLES)  # was: pd.read_pickle(ROOT / \"results\" / \"rab_all.pkl\")')\nbeo_src = sub(beo_src, 'au = json.loads((ROOT / \"audit\" / \"rederive.json\").read_text())',\n              'au = data[\"audit_rederive\"]  # was: json.loads((ROOT / \"audit\" / \"rederive.json\").read_text())')\nbeo_src = sub(beo_src, 'ms = json.loads((ROOT / \"audit\" / \"m2_specificity.json\").read_text())',\n              'ms = data[\"audit_m2_specificity\"]  # was: json.loads((ROOT / \"audit\" / \"m2_specificity.json\").read_text())')\nbeo_src = sub(beo_src, 'pre = json.loads((ROOT / \"prereg_mech.json\").read_text())',\n              'pre = data[\"prereg_mech\"]  # was: json.loads((ROOT / \"prereg_mech.json\").read_text())')\nbeo_src = sub(beo_src, '\"prereg_sha256\": (ROOT / \"prereg_mech.sha256\").read_text().split()[0]',\n              '\"prereg_sha256\": data[\"prereg_sha256\"].split()[0]')\n\ncells = []\n\n\ndef md(s):\n    cells.append({\"cell_type\": \"markdown\", \"metadata\": {}, \"source\": s.strip(\"\\n\")})\n\n\ndef code(s):\n    cells.append({\"cell_type\": \"code\", \"metadata\": {}, \"execution_count\": None, \"outputs\": [], \"source\": s.strip(\"\\n\")})\n\n\nmd(r\"\"\"\n# Why cross-model agreement flags logic errors — consensus-mechanism audit (demo)\n\nThis notebook is a runnable walk-through of the evaluation script **`eval.py`** of the artifact\n*\"Why cross-model agreement flags logic errors\"* (T4 consensus-mechanism audit on NL→FOL dataset **E**; CPU only, no LLM calls).\n\n**Question.** A candidate first-order-logic (FOL) translation of a sentence gets a *graded consensus score*\n`c_score_align` = share of other vendor families' outputs for the same sentence that are **not** z3-equivalent\n(modulo vocabulary alignment, \"eqmv\") to it. Why does that label-free score predict faithfulness (AUROC 0.784 on R_AB)?\nThe \"Anna Karenina\" premise says correct translations converge while wrong ones scatter.\n\n**What `eval.py` does** (orchestrator):\n1. copies inputs, computes the label-free pairwise z3 **eqmv matrix** (29,107 pairs over 700 sentences, ~2 min on 4 vCPU),\n2. **PART A** (`src/part_a.py`): gates G0/G1/G2, the exact identity `AUROC_b = 1 − (e+d)/2` for binary majority consensus\n   (e = P(endorsed | ERROR), d = P(not endorsed | CORRECT)), mechanism tests M1/M2/NET/SCATTER/M3-local/M4, LOFO and cost,\n3. **PART B** (`src/record.py`): file-sourced verified record of iteration 2,\n4. independent audits (`audit/*.py`), **`figures(A)`** and **`build_eval_out(A, B)`** → `eval_out.json`.\n\n**In this demo** steps 1–3 (z3 matrix + ~2,000 lines of analysis over large private inputs) are *not* rerun: their saved\noutputs (`part_a.json`, record summary, audit JSONs, the tables read by `figures()`) are shipped in `mini_demo_data.json`\ntogether with **100 R_AB rows** (12 per stratum × label, plus 4 non-scorable rows). The notebook then\n* recomputes the e/d decomposition, graded-vs-binary AUROC and graded ROC trace on those rows with the artifact's own\n  `ed_decomposition()` / `graded_trace()` / `auc()` functions,\n* runs `figures(A)` and `build_eval_out(A, B)` from `eval.py` unchanged except for file reads → `data`,\n* shows the headline numbers and figures.\n\"\"\")\n\ncode(r\"\"\"\nimport subprocess, sys\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\n\n# loguru — NOT pre-installed on Colab, always install\n_pip('loguru==0.7.3')\n\n# numpy, pandas, scipy, matplotlib — pre-installed on Colab, install locally only (at Colab's versions)\nif 'google.colab' not in sys.modules:\n    _pip('numpy==2.0.2', 'pandas==2.2.2', 'scipy==1.16.3', 'matplotlib==3.10.0')\n\"\"\")\n\nmd(r\"\"\"\n## Imports\n\nThe original import block of `eval.py`, copied as-is. Two notebook-only removals (kept as comments):\nthe `os.execv` re-launch that forces `PYTHONHASHSEED=0` (it only matters for the z3 eqmv matrix, which is not recomputed here)\nand the 20 GB `RLIMIT_AS` cap (a script-level safety net, not wanted inside a Jupyter kernel).\n\"\"\")\n\ncode(r'''\nfrom __future__ import annotations\n\nimport argparse\nimport json\nimport os\nimport subprocess\nimport sys\nimport time\nfrom pathlib import Path\n\n# if os.environ.get(\"PYTHONHASHSEED\") != \"0\":  # eqmv's align()/fp() hash strings: fix the seed for reproducibility\n#     os.environ[\"PYTHONHASHSEED\"] = \"0\"\n#     os.execv(sys.executable, [sys.executable] + sys.argv)\n# (notebook: cannot re-exec the kernel; only the z3 matrix stage, which is not rerun here, depends on the hash seed)\n\nimport numpy as np\nimport pandas as pd\nfrom loguru import logger\n\nROOT = Path.cwd()  # was: Path(__file__).resolve().parent — outputs (figures/, logs/, eval_out.json) go to the working dir\n# sys.path.insert(0, str(ROOT / \"src\"))  # notebook: the src/ functions used below are inlined instead\n(ROOT / \"logs\").mkdir(exist_ok=True)\nlogger.remove()\nlogger.add(sys.stdout, level=\"INFO\", format=\"{time:HH:mm:ss}|{level:<7}|{message}\")\nlogger.add(ROOT / \"logs\" / \"eval.log\", rotation=\"30 MB\", level=\"DEBUG\")\n\nimport resource  # noqa: E402\n\n# resource.setrlimit(resource.RLIMIT_AS, (20 * 1024 ** 3, 20 * 1024 ** 3))  # 29 GB container; fail fast instead of OOM\n# (notebook: not applied inside the kernel)\n\n# notebook-only additions: src/stats.py AUROC needs rankdata; display for the saved figures\nfrom scipy.stats import rankdata\nimport matplotlib.pyplot as plt\nfrom IPython.display import Image, display\n''')\n\nmd(\"## Data loading\\n\\nLoads `mini_demo_data.json` from GitHub, falling back to a local copy.\")\n\ncode(f'''\nGITHUB_DATA_URL = \"{URL}\"\nimport json\nfrom pathlib import Path\n\ndef load_data():\n    try:\n        import urllib.request\n        with urllib.request.urlopen(GITHUB_DATA_URL) as response:\n            return json.loads(response.read().decode())\n    except Exception: pass\n    local = Path(\"mini_demo_data.json\")\n    if local.exists(): return json.loads(local.read_text())\n    raise FileNotFoundError(\"Could not load mini_demo_data.json\")\n''')\n\ncode(r'''\ndata = load_data()\nprint(data[\"description\"])\nprint(\"keys:\", list(data.keys()))\nprint(\"R_AB demo rows:\", len(data[\"rab_rows\"]), \"| consensus-scorable (population) rows:\", len(data[\"population_rows\"]))\n''')\n\nmd(r\"\"\"\n## Config\n\nThe only tunable of the demo is how many R_AB rows are pushed through the per-row code\n(`build_eval_out()` examples and the recomputation cell). The original run used **all 2,686 R_AB rows**\n(2,672 consensus-scorable); the demo data holds a stratified 100-row subset, and the whole notebook runs in seconds,\nso it uses all of them. `FIG_DPI` is the original figure resolution.\n\"\"\")\n\ncode(r'''\nN_EXAMPLES = 100   # R_AB rows processed (max 100 in mini_demo_data.json; original run: 2686)\nFIG_DPI = 200      # original eval.py value\nN_SHOW = 5         # example rows printed in the results section\n''')\n\nmd(r\"\"\"\n## JSON helper (from `eval.py`)\n\"\"\")\n\ncode(jdump_src)\n\nmd(r\"\"\"\n## Recompute the e/d decomposition on the demo rows\n\nThe heart of the audit is a bookkeeping identity for *binary* consensus rules. With `y = 1` for ERROR rows and\n`endorsed = 1` when the cross-family peer rule (e.g. END_MAJ: a majority of other vendor families produce an eqmv-equivalent\nformula) endorses the candidate:\n\n* **e** = P(endorsed | ERROR) — wrong translations that peers agree with (error endorsement),\n* **d** = P(not endorsed | CORRECT) — correct translations peers do *not* agree with (correct divergence),\n* `AUROC_b = 1 − (e + d)/2` (balanced accuracy of the flag `1 − endorsed`).\n\nThe graded score `c_score_align` keeps the full fraction of disagreeing peers; `graded_trace()` gives its ROC as the\n(e_t, d_t) pair at every threshold. The three functions below are copied **verbatim** from the artifact's\n`src/stats.py` (`auc`) and `src/mechanism.py` (`ed_decomposition`, `graded_trace`), and applied to the demo rows' saved\nper-row consensus columns (`c_frozen` = frozen c_score_align, `c_score_exact`, `end_MAJ`, `end_PLUR`, `end_FAM2`,\n`end_FAMMAJ`, `end_MAJ_EXACT`). With only 96 scorable rows (balanced 48/48 by design, unlike the 1810/862 population) the\nnumbers are noisy; the full-population values from `part_a.json` are printed alongside.\n\"\"\")\n\ncode(r'''\n# ---- src/stats.py\ndef auc(y, s) -> float:\n    \"\"\"Mann-Whitney AUROC with ties = 0.5 (identical to sklearn roc_auc_score).\"\"\"\n    y = np.asarray(y, dtype=float)\n    s = np.asarray(s, dtype=float)\n    n1 = int(y.sum())\n    n0 = len(y) - n1\n    if n1 == 0 or n0 == 0:\n        return float(\"nan\")\n    r = rankdata(s)\n    return float((r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))\n\n\n# ---- src/mechanism.py\ndef ed_decomposition(y, endorsed) -> dict:\n    \"\"\"y: 1 = ERROR, 0 = CORRECT; endorsed: 1 = the cross-family peer rule endorses the candidate.\n    Returns e = P(endorsed | ERROR) (error-endorsement), d = P(not endorsed | CORRECT) (correct-divergence) and\n    AUROC_b of b = 1 - endorsed, asserting the bookkeeping identity AUROC_b = 1 - (e + d)/2 (balanced accuracy).\"\"\"\n    y = np.asarray(y, int)\n    en = np.asarray(endorsed, int)\n    e = float(en[y == 1].mean())\n    d = float((1 - en[y == 0]).mean())\n    a = auc(y, 1 - en)\n    assert abs(a - (1 - (e + d) / 2)) < 1e-12, (a, e, d)\n    return {\"n_err\": int((y == 1).sum()), \"n_cor\": int((y == 0).sum()), \"e\": e, \"d\": d, \"auroc_b\": a}\n\n\ndef graded_trace(y, c) -> dict:\n    \"\"\"(e_t, d_t) at every distinct threshold t of the graded score (flag = c >= t); the ROC = (d_t, 1 - e_t).\n    Asserts the trapezoid area equals the tie-aware AUROC to 1e-9.\"\"\"\n    y = np.asarray(y, int)\n    c = np.asarray(c, float)\n    ts = np.unique(c)\n    pts = [(0.0, 0.0)]\n    tr = []\n    for t in ts[::-1]:\n        fl = c >= t\n        tpr = fl[y == 1].mean()\n        fpr = fl[y == 0].mean()\n        tr.append({\"t\": float(t), \"e_t\": float(1 - tpr), \"d_t\": float(fpr)})\n        pts.append((fpr, tpr))\n    pts.append((1.0, 1.0))\n    xs, ys = zip(*pts)\n    area = float(np.trapezoid(ys, xs))\n    a = auc(y, c)\n    assert abs(area - a) < 1e-9, (area, a)\n    named = {}\n    for nm, en in ((\"any_peer_agrees (c<1)\", c < 1), (\"majority END_MAJ (c<0.5)\", c < 0.5), (\"all_peers_agree (c==0)\", c == 0)):\n        named[nm] = {\"e\": float(en[y == 1].mean()), \"d\": float((~en)[y == 0].mean()),\n                     \"auroc_b\": float(1 - (en[y == 1].mean() + (~en)[y == 0].mean()) / 2)}\n    return {\"trace\": tr, \"trapezoid_area\": area, \"auroc\": a, \"named_points\": named}\n''')\n\ncode(r'''\n# demo population: the consensus-scorable rows among the first N_EXAMPLES R_AB rows\n_keys = set(pd.DataFrame(data[\"rab_rows\"]).head(N_EXAMPLES).row_key)\nPd = pd.DataFrame(data[\"population_rows\"])\nPd = Pd[Pd.row_key.isin(_keys)].reset_index(drop=True)\ny = Pd.y_AB.astype(int).values\nprint(f\"demo population: {len(Pd)} rows ({y.sum()} ERROR / {(1 - y).sum()} CORRECT), {Pd.sentence_id.nunique()} sentences\")\n\nA = data[\"part_a\"]\nfull_head = {(r[\"regime\"], r[\"rule\"]): r for r in A[\"cuts_headline\"]}\ndemo_ed = {}\nfor rule in [\"MAJ\", \"PLUR\", \"FAM2\", \"FAMMAJ\", \"MAJ_EXACT\"]:\n    demo_ed[rule] = ed_decomposition(y, Pd[f\"end_{rule}\"].values)\ndemo_graded = {\"c_score_align\": graded_trace(y, Pd.c_frozen.values), \"c_score_exact\": graded_trace(y, Pd.c_score_exact.values)}\n\nrows = []\nfor rule, r in demo_ed.items():\n    f = full_head.get((\"R_AB\", rule), {})\n    rows.append({\"rule\": f\"END_{rule} (binary)\", \"demo e\": r[\"e\"], \"demo d\": r[\"d\"], \"demo AUROC\": r[\"auroc_b\"],\n                 \"full e\": f.get(\"e\"), \"full d\": f.get(\"d\"), \"full AUROC\": f.get(\"auroc_b\")})\ng = A[\"graded_vs_binary\"]\nfor nm, key in ((\"c_score_align\", \"auroc_c_score_align\"), (\"c_score_exact\", \"auroc_c_score_exact\")):\n    rows.append({\"rule\": f\"{nm} (graded)\", \"demo AUROC\": demo_graded[nm][\"auroc\"], \"full AUROC\": g[key]})\ndemo_table = pd.DataFrame(rows)\nprint(demo_table.round(3).to_string(index=False))\nprint(\"\\nidentity AUROC_b = 1-(e+d)/2 asserted for every rule; graded trapezoid area == AUROC asserted\")\n''')\n\nmd(r\"\"\"\n## PART A / PART B results (saved outputs of the heavy stages)\n\nIn `eval.py`'s `main()` the next steps are `subprocess` calls to `src/copy_inputs.py` and `src/run_matrix.py`\n(z3 matrix), then `A = part_a.run()` and the PART B record builders (`RC.exp6_tables()`, `RC.pt_vs_s4()`, …) and the\ntwo audit scripts. They need the full raw inputs of earlier iterations, so here `A` and `B` are rebuilt from their saved\noutputs with the same structure `build_eval_out()` expects: `A` = `results/part_a.json`, `B[\"summary\"]` = the record\nsummary stored in `eval_out.json`, `B[\"pt_vs_s4\"][\"rows\"]` = `tables/pt_vs_s4_rerun.csv`.\n\"\"\")\n\ncode(r'''\nt0 = time.time()\n# original main():  A = part_a.run();  B = {\"summary\": {...}};  B[\"pt_vs_s4\"] = RC.pt_vs_s4(); ...\nA = data[\"part_a\"]\nB = {\"summary\": data[\"record_summary\"]}\nB[\"pt_vs_s4\"] = {\"rows\": data[\"pt_vs_s4_rows\"]}\nlogger.info(f\"PART A keys: {list(A.keys())}\")\nlogger.info(f\"PART B record summary keys: {list(B['summary'].keys())}; pt_vs_s4 rows: {len(B['pt_vs_s4']['rows'])}\")\n''')\n\nmd(r\"\"\"\n## Figures (`figures(A)` from `eval.py`)\n\nCopied verbatim; the only changes are that the three CSV tables are read from `data[\"tables\"]` instead of `tables/*.csv`,\nthe Agg backend switch is commented out, and `dpi` uses `FIG_DPI`. It writes `figures/fig1…fig4` (.png/.pdf/.json):\n\n1. **fig1** — e and d of END_MAJ by n_conditions bin and words tercile, per regime (R_AB, R_A, VOCAB_EXACT);\n2. **fig2** — AUROC(k) of the graded score as the peer pool grows to k other vendor families, with $/sentence;\n3. **fig3** — scatter index: P(two cross-family ERROR outputs are equivalent) vs the same for CORRECT outputs;\n4. **fig4** — graded ROC of `c_score_align` / `c_score_exact` with the named binary operating points.\n\"\"\")\n\ncode(fig_src)\n\ncode(r'''\nfigures(A)\nlogger.info(f\"figures written to {ROOT / 'figures'}\")\n''')\n\nmd(r\"\"\"\n## `eval_out.json` (`build_eval_out(A, B)` from `eval.py`)\n\nCopied verbatim except for the input reads (`population_RAB.pkl`, `rab_all.pkl`, audit JSONs, prereg → `data`, and `R`\nlimited to `N_EXAMPLES` rows). It flattens PART A/B into `metrics_agg` (335 named metrics in the full run), attaches\nthe verdicts for M1/M2/NET/SCATTER/M3-local/M4/LOFO with their pre-registered rules, and writes one example per R_AB row\nwith the per-row predictions `predict_c_score_align`, `predict_c_score_exact`, `predict_b_endmaj`, … (non-scorable rows get `NA`).\n\"\"\")\n\ncode(beo_src)\n\ncode(r'''\nout = build_eval_out(A, B)\njdump(ROOT / \"eval_out.json\", out)\nlogger.info(f\"eval_out.json written: {len(out['metrics_agg'])} metrics, {len(out['datasets'][0]['examples'])} examples; {time.time() - t0:.0f}s\")\n''')\n\nmd(r\"\"\"\n## Results\n\nHeadline metrics (full 2,672-row population, from `metrics_agg`), the pre-registered verdicts, a few example rows,\na per-row score plot for the demo rows, and the four figures produced by `figures(A)`.\n\"\"\")\n\ncode(r'''\nma = out[\"metrics_agg\"]\nhead = [(\"graded c_score_align AUROC\", \"auroc_c_score_align\"), (\"binary END_MAJ AUROC\", \"auroc_b_END_MAJ\"),\n        (\"delta graded - binary\", \"delta_graded_minus_binary\"), (\"  CI lo\", \"delta_graded_minus_binary_ci_lo\"), (\"  CI hi\", \"delta_graded_minus_binary_ci_hi\"),\n        (\"END_MAJ e (error endorsement)\", \"e_maj_R_AB\"), (\"END_MAJ d (correct divergence)\", \"d_maj_R_AB\"),\n        (\"aligner-free c_score_exact AUROC\", \"auroc_c_score_exact\"),\n        (\"NET Delta(e+d), words T3-T1\", \"net_delta_words\"),\n        (\"SI_err (identical-wrong rate)\", \"si_err_mean\"), (\"SI_cor (identical-correct rate)\", \"si_cor_mean\"),\n        (\"SI ratio cor/err\", \"si_ratio_cor_over_err\"), (\"k95 (peers for 95% of max AUROC)\", \"k95\"),\n        (\"best 3-family pool OOF AUROC\", \"m4_k3_crossfit_oof_auroc\"), (\"LOFO min delta\", \"lofo_min_delta\"),\n        (\"G2 mismatch rate\", \"g2_mismatch_rate\"), (\"eqmv non-transitivity\", \"nontransitivity_rate\")]\nprint(pd.DataFrame([{\"quantity\": n, \"value\": ma.get(k)} for n, k in head]).round(4).to_string(index=False))\nprint(f\"\\n{len(ma)} metrics in metrics_agg\\n\\nVerdicts:\")\nfor k, v in out[\"metadata\"][\"verdicts\"].items():\n    print(f\"  {k:9s} {v['verdict'] if isinstance(v, dict) and 'verdict' in v else v}\")\n\nex = pd.DataFrame(out[\"datasets\"][0][\"examples\"])\nprint(\"\\nExample rows:\")\nfor r in ex.head(N_SHOW).itertuples():\n    inp = json.loads(r.input)\n    print(f\"- [{r.output}] {inp['text'][:110]}...\\n    FOL: {inp['candidate_fol'][:110]}\\n    c_score_align={r.predict_c_score_align}  b_endmaj={r.predict_b_endmaj}\")\n\n# per-row scores of the demo rows, by label (higher c = more peers disagree -> more likely ERROR)\nfig, ax = plt.subplots(1, 2, figsize=(10, 3.8))\nfor lab, col in ((\"CORRECT\", \"#4c9f70\"), (\"ERROR\", \"#c8553d\")):\n    v = Pd.loc[Pd.final_label == lab, \"c_frozen\"].values\n    ax[0].hist(v, bins=np.linspace(0, 1, 11), alpha=0.55, color=col, label=f\"{lab} (n={len(v)})\")\nax[0].set_xlabel(\"c_score_align (share of disagreeing peer families)\")\nax[0].set_ylabel(\"demo rows\")\nax[0].legend(frameon=False)\nax[0].set_title(\"Demo rows: graded consensus score by label\", fontsize=9)\nrl = list(demo_ed)\nx = np.arange(len(rl))\nax[1].bar(x - 0.2, [demo_ed[r][\"e\"] for r in rl], 0.4, color=\"#1b6ca8\", label=\"e = P(endorsed | ERROR)\")\nax[1].bar(x + 0.2, [demo_ed[r][\"d\"] for r in rl], 0.4, color=\"#c8553d\", label=\"d = P(not endorsed | CORRECT)\")\nax[1].set_xticks(x, [f\"END_{r}\" for r in rl], fontsize=7)\nax[1].set_ylim(0, 1)\nax[1].legend(frameon=False, fontsize=7)\nax[1].set_title(\"Demo rows: e/d of binary consensus rules\", fontsize=9)\nfig.tight_layout()\nplt.show()\n\nfor f in (\"fig1_e_d_by_complexity\", \"fig2_auroc_k\", \"fig3_scatter_index\", \"fig4_graded_roc\"):\n    print(f)\n    display(Image(filename=str(ROOT / \"figures\" / f\"{f}.png\"), width=800))\n''')\n\nnb = {\"cells\": cells, \"metadata\": {\"kernelspec\": {\"display_name\": \"Python 3\", \"language\": \"python\", \"name\": \"python3\"},\n                                   \"language_info\": {\"name\": \"python\"}}, \"nbformat\": 4, \"nbformat_minor\": 5}\nfor i, c in enumerate(nb[\"cells\"]):\n    c[\"id\"] = f\"cell-{i:02d}\"\nOUT.write_text(json.dumps(nb, indent=1))\nprint(OUT, len(cells), \"cells\")\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [29] ASSISTANT · 2026-09-24 18:38:14 UTC

```
Built the demo data (100 stratified rows, 0.43 MB) and a notebook generator; now test-running the notebook in a clean venv.
```

### [30] TOOL CALL — Bash · 2026-09-24 18:38:14 UTC

```
sed -i 's/^N_EXAMPLES = 100 /N_EXAMPLES = 20  /' build/make_notebook.py && python3 build/make_notebook.py && python3 -c "
import json;d=json.load(open('mini_demo_data.json'));import collections;print(collections.Counter((r['stratum'],r['final_label']) for r in d['rab_rows'][:20]))" && (/usr/local/bin/python3.12 -m venv .nb_env && .nb_env/bin/pip install -q pip jupyter ipykernel) > build/venv.log 2>&1; echo venv $?
```

### [31] TOOL RESULT — Bash · 2026-09-24 18:46:40 UTC

```
{"stdout": "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_FWy8D4_y9GBn/code_demo.ipynb 24 cells\nCounter({('CTRL', 'CORRECT'): 6, ('CTRL', 'ERROR'): 5, ('L20', 'CORRECT'): 4, ('L20', 'ERROR'): 3, ('L25', 'CORRECT'): 1, ('L25', 'ERROR'): 1})\nvenv 0", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [32] TOOL CALL — Bash · 2026-09-24 18:47:26 UTC

```
time .nb_env/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb > build/run1.log 2>&1; echo exit $?; tail -30 build/run1.log
```

### [33] TOOL RESULT — Bash · 2026-09-24 18:52:33 UTC

```
{"stdout": "real\t5m35.344s\nuser\t0m17.503s\nsys\t0m2.363s\nexit 0\n[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n[IPKernelApp] WARNING | Kernel is running over TCP without encryption. All communication (including code and outputs) is sent in plain text and is susceptible to eavesdropping. Use IPC transport or launch with kernel manager-provisioned CurveZMQ keys to enable transport encryption.\n\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m A new release of pip is available: \u001b[0m\u001b[31;49m25.0.1\u001b[0m\u001b[39;49m -> \u001b[0m\u001b[32;49m26.2.1\u001b[0m\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m To update, run: \u001b[0m\u001b[32;49mpython3.12 -m pip install --upgrade pip\u001b[0m\n\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m A new release of pip is available: \u001b[0m\u001b[31;49m25.0.1\u001b[0m\u001b[39;49m -> \u001b[0m\u001b[32;49m26.2.1\u001b[0m\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m To update, run: \u001b[0m\u001b[32;49mpython3.12 -m pip install --upgrade pip\u001b[0m\n[NbConvertApp] Writing 919755 bytes to code_demo.ipynb", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [34] TOOL CALL — Bash · 2026-09-24 18:53:33 UTC

```
python3 -c "
import json;nb=json.load(open('code_demo.ipynb'))
for c in nb['cells']:
  if c['cell_type']!='code': continue
  for o in c['outputs']:
    if o['output_type']=='stream': print(o['text'][:2500])
    elif o['output_type']=='error': print('ERR',o['ename'],o['evalue'])
    else: print('[',o['output_type'], list(o.get('data',{}).keys()),']')
"; ls figures
```

### [35] TOOL RESULT — Bash · 2026-09-24 18:53:33 UTC

```
{"stdout": "['\\n', '\\x1b[1m[\\x1b[0m\\x1b[34;49mnotice\\x1b[0m\\x1b[1;39;49m]\\x1b[0m\\x1b[39;49m A new release of pip is available: \\x1b[0m\\x1b[31;49m25.0.1\\x1b[0m\\x1b[39;49m -> \\x1b[0m\\x1b[32;49m26.2.1\\x1b[0m\\n', '\\x1b[1m[\\x1b[0m\\x1b[34;49mnotice\\x1b[0m\\x1b[1;39;49m]\\x1b[0m\\x1b[39;49m To update, run: \\x1b[0m\\x1b[32;49mpython3.12 -m pip install --upgrade pip\\x1b[0m\\n']\n['\\n', '\\x1b[1m[\\x1b[0m\\x1b[34;49mnotice\\x1b[0m\\x1b[1;39;49m]\\x1b[0m\\x1b[39;49m A new release of pip is available: \\x1b[0m\\x1b[31;49m25.0.1\\x1b[0m\\x1b[39;49m -> \\x1b[0m\\x1b[32;49m26.2.1\\x1b[0m\\n', '\\x1b[1m[\\x1b[0m\\x1b[34;49mnotice\\x1b[0m\\x1b[1;39;49m]\\x1b[0m\\x1b[39;49m To update, run: \\x1b[0m\\x1b[32;49mpython3.12 -m pip install --upgrade pip\\x1b[0m\\n']\n['Curated subset of the consensus-mechanism audit (T4, dataset E): the PART A result dict (part_a.json), the PART B record summary + PT-vs-S4 rows, audit JSONs, prereg, the tables read by figures(), and 100 R_AB rows (stratified 12 per stratum x label, seed 0, plus 4 non-scorable rows) with their population columns (c_frozen, c_score_exact, end_* endorsements, c_k3_best_oof, ...).\\n', \"keys: ['description', 'part_a', 'record_summary', 'pt_vs_s4_rows', 'audit_rederive', 'audit_m2_specificity', 'prereg_mech', 'prereg_sha256', 'tables', 'rab_rows', 'population_rows']\\n\", 'R_AB demo rows: 100 | consensus-scorable (population) rows: 96\\n']\n['demo population: 20 rows (9 ERROR / 11 CORRECT), 14 sentences\\n', '                  rule  demo e  demo d  demo AUROC  full e  full d  full AUROC\\n', '      END_MAJ (binary)   0.333   0.273       0.697   0.124   0.537       0.669\\n', '     END_PLUR (binary)   0.333   0.182       0.742   0.229   0.342       0.714\\n', '     END_FAM2 (binary)   0.444   0.091       0.732   0.299   0.204       0.748\\n', '   END_FAMMAJ (binary)   0.333   0.273       0.697   0.151   0.445       0.702\\n', 'END_MAJ_EXACT (binary)   0.000   0.545       0.727   0.014   0.732       0.627\\n', 'c_score_align (graded)     NaN     NaN       0.722     NaN     NaN       0.784\\n', 'c_score_exact (graded)     NaN     NaN       0.808     NaN     NaN       0.748\\n', '\\n', 'identity AUROC_b = 1-(e+d)/2 asserted for every rule; graded trapezoid area == AUROC asserted\\n']\n[\"18:51:29|INFO   |PART A keys: ['frame_info', 'gates', 'G2', 'nontransitivity', 'matrix_summary', 'population', 'vocab_exact', 'cuts_headline', 'stratified', 'graded_vs_binary', 'system_class_cut', 'M1_M2', 'NET', 'SCATTER', 'M3_local', 'M4']\\n\"]\n[\"18:51:29|INFO   |PART B record summary keys: ['exp6', 'pt_vs_s4', 'corrections', 'regimes_R_PANEL', 'label_facts_n', 'hypothesis_verdicts_status_counts', 'perturb_counts']; pt_vs_s4 rows: 48\\n\"]\n['18:51:33|INFO   |figures written to /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_FWy8D4_y9GBn/figures\\n']\n['18:51:33|INFO   |eval_out.json written: 335 metrics, 20 examples; 4s\\n']\n['                        quantity   value\\n', '      graded c_score_align AUROC  0.7837\\n', '            binary END_MAJ AUROC  0.6693\\n', '           delta graded - binary  0.1144\\n', '                           CI lo  0.0907\\n', '                           CI hi  0.1398\\n', '   END_MAJ e (error endorsement)  0.1243\\n', '  END_MAJ d (correct divergence)  0.5371\\n', 'aligner-free c_score_exact AUROC  0.7477\\n', '     NET Delta(e+d), words T3-T1  0.3562\\n', '   SI_err (identical-wrong rate)  0.1589\\n', ' SI_cor (identical-correct rate)  0.7604\\n', '                SI ratio cor/err  4.4522\\n', 'k95 (peers for 95% of max AUROC)  3.0000\\n', '    best 3-family pool OOF AUROC  0.7845\\n', '                  LOFO min delta -0.0108\\n', '                G2 mismatch rate  0.0033\\n', '           eqmv non-transitivity  0.1581\\n', '\\n', '335 metrics in metrics_agg\\n', '\\n', 'Verdicts:\\n', '  M1        INCONCLUSIVE\\n', '  M2        CONFIRMED\\n', '  NET       DEGRADES_WITH_COMPLEXITY (legitimate divergence dominates)\\n', \"  SCATTER   {'SI_err_falls_with_ncond': 'CONFIRMED', 'SI_cor_gt_SI_err': 'CONFIRMED'}\\n\", '  M3_local  INCONCLUSIVE\\n', '  M4        CONFIRMED\\n', '  LOFO      NO_SINGLE_FAMILY_CARRIES_EFFECT\\n', '\\n', 'Example rows:\\n', '- [ERROR] When something is depressing, it is sad....\\n', '    FOL: Depressing(x) → Sad(x)\\n', '    c_score_align=1.000000  b_endmaj=1.000000\\n', '- [CORRECT] When something is depressing, it is sad....\\n', '    FOL: ∀x (Depressing(x) → Sad(x))\\n', '    c_score_align=0.090909  b_endmaj=0.000000\\n', '- [CORRECT] When something is depressing, it is sad....\\n', '    FOL: ∀x (Depressing(x) → Sad(x))\\n', '    c_score_align=0.090909  b_endmaj=0.000000\\n', '- [CORRECT] A musical composition typically consisting of multiple movements, often featuring a solo instrument accompanie...\\n', '    FOL: ∀x (MusicalComposition(x) ∧ ConsistsOf(x, multipleMovements) ∧ OftenFeatures(x, soloInstrument) ∧ AccompaniedB\\n', '    c_score_align=0.700000  b_endmaj=1.000000\\n', '- [CORRECT] A geological formation that is created by the deposition of sediment, forms layers over time, and contains fos...\\n', '    FOL: ∀x ((GeologicalFormation(x) ∧ CreatedByDepositionOfSediment(x) ∧ FormsLayersOverTime(x) ∧ ContainsFossils(x)) \\n', '    c_score_align=0.181818  b_endmaj=0.000000\\n']\n[ display_data ['image/png', 'text/plain'] ]\n['fig1_e_d_by_complexity\\n']\n[ display_data ['image/png', 'text/plain'] ]\n['fig2_auroc_k\\n']\n[ display_data ['image/png', 'text/plain'] ]\n['fig3_scatter_index\\n']\n[ display_data ['image/png', 'text/plain'] ]\n['fig4_graded_roc\\n']\n[ display_data ['image/png', 'text/plain'] ]\nfig1_e_d_by_complexity.json\nfig1_e_d_by_complexity.pdf\nfig1_e_d_by_complexity.png\nfig2_auroc_k.json\nfig2_auroc_k.pdf\nfig2_auroc_k.png\nfig3_scatter_index.json\nfig3_scatter_index.pdf\nfig3_scatter_index.png\nfig4_graded_roc.json\nfig4_graded_roc.pdf\nfig4_graded_roc.png", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [36] ASSISTANT · 2026-09-24 18:53:33 UTC

```
Runs cleanly at N_EXAMPLES=20 (5.5 min, almost all pip install). Scaling to the full 100 demo rows.
```

### [37] TOOL CALL — Bash · 2026-09-24 18:53:33 UTC

```
sed -i 's/^N_EXAMPLES = 20  /N_EXAMPLES = 100 /' build/make_notebook.py && grep -n "^N_EXAMPLES" build/make_notebook.py && python3 build/make_notebook.py && time .nb_env/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb > build/run2.log 2>&1; echo exit $?; python3 -c "
import json;nb=json.load(open('code_demo.ipynb'))
for c in nb['cells'][9:16]:
  for o in c.get('outputs',[]):
    if o['output_type']=='stream': print(''.join(o['text'])[:1500])
    elif o['output_type']=='error': print('ERR',o['ename'],o['evalue'])
"
```

### [38] TOOL RESULT — Bash · 2026-09-24 18:54:15 UTC

```
{"stdout": "183:N_EXAMPLES = 100   # R_AB rows processed (max 100 in mini_demo_data.json; original run: 2686)\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_FWy8D4_y9GBn/code_demo.ipynb 24 cells\n\nreal\t0m45.379s\nuser\t0m5.881s\nsys\t0m0.712s\nexit 0\ndemo population: 96 rows (48 ERROR / 48 CORRECT), 82 sentences\n                  rule  demo e  demo d  demo AUROC  full e  full d  full AUROC\n      END_MAJ (binary)   0.208   0.500       0.646   0.124   0.537       0.669\n     END_PLUR (binary)   0.333   0.438       0.615   0.229   0.342       0.714\n     END_FAM2 (binary)   0.354   0.250       0.698   0.299   0.204       0.748\n   END_FAMMAJ (binary)   0.229   0.479       0.646   0.151   0.445       0.702\nEND_MAJ_EXACT (binary)   0.021   0.750       0.615   0.014   0.732       0.627\nc_score_align (graded)     NaN     NaN       0.722     NaN     NaN       0.784\nc_score_exact (graded)     NaN     NaN       0.686     NaN     NaN       0.748\n\nidentity AUROC_b = 1-(e+d)/2 asserted for every rule; graded trapezoid area == AUROC asserted\n\n18:52:28|INFO   |PART A keys: ['frame_info', 'gates', 'G2', 'nontransitivity', 'matrix_summary', 'population', 'vocab_exact', 'cuts_headline', 'stratified', 'graded_vs_binary', 'system_class_cut', 'M1_M2', 'NET', 'SCATTER', 'M3_local', 'M4']\n\n18:52:28|INFO   |PART B record summary keys: ['exp6', 'pt_vs_s4', 'corrections', 'regimes_R_PANEL', 'label_facts_n', 'hypothesis_verdicts_status_counts', 'perturb_counts']; pt_vs_s4 rows: 48", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [39] TOOL CALL — Read · 2026-09-24 18:54:15 UTC

```
/ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_FWy8D4_y9GBn/figures/fig1_e_d_by_complexity.png
```

### [40] TOOL RESULT — Read · 2026-09-24 18:54:15 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [41] TOOL CALL — Bash · 2026-09-24 18:54:15 UTC

```
sed -i "s|logger.info(f\"figures written to {ROOT / 'figures'}\")|logger.info(\"figures written to figures/ (fig1-fig4 .png/.pdf/.json)\")|" build/make_notebook.py && grep -n "figures written" build/make_notebook.py && python3 build/make_notebook.py && .nb_env/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb > build/run3.log 2>&1; echo exit $?; grep -c "ai-inventor/aii_data" code_demo.ipynb; grep -o 'GITHUB_DATA_URL = \\"[^\\]*' code_demo.ipynb; python3 -c "
import json;nb=json.load(open('code_demo.ipynb'));print(sum(1 for c in nb['cells'] for o in c.get('outputs',[]) if o['output_type']=='error'),'errors')"
```

### [42] TOOL RESULT — Bash · 2026-09-24 18:54:15 UTC

```
{"stdout": "331:logger.info(\"figures written to figures/ (fig1-fig4 .png/.pdf/.json)\")\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_FWy8D4_y9GBn/code_demo.ipynb 24 cells\nexit 0\n0\nGITHUB_DATA_URL = \\\"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/main/round-3/evaluation-2/demo/mini_demo_data.json\n0 errors", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [43] ASSISTANT · 2026-09-24 18:54:15 UTC

```
Notebook passes with no errors. Cleaning up and writing the README, manifest and output JSON.
```

### [44] TOOL CALL — Bash · 2026-09-24 18:54:15 UTC

```
rm -rf .nb_env figures logs eval_out.json build/venv.log && ls -la . build .aii && du -sh code_demo.ipynb mini_demo_data.json
```

### [45] TOOL RESULT — Bash · 2026-09-24 18:54:15 UTC

```
{"stdout": ".:\ntotal 6913\ndrwxr-xr-x 4 root root 2000196 Sep 24 18:54 .\ndrwxr-xr-x 6 root root 2063157 Sep 24 18:34 ..\ndrwxr-xr-x 2 root root       1 Sep 24 18:34 .aii\n-rw------- 1 root root      54 Sep 24 18:35 .aii_claude_session.json\n-rw-r--r-- 1 root root  663130 Sep 24 18:54 .repl_agent.ptylog\ndrwxr-xr-x 2 root root 1004957 Sep 24 18:54 build\n-rw-r--r-- 1 root root  921268 Sep 24 18:53 code_demo.ipynb\n-rw-r--r-- 1 root root  432415 Sep 24 18:36 mini_demo_data.json\n\n.aii:\ntotal 1954\ndrwxr-xr-x 2 root root       1 Sep 24 18:34 .\ndrwxr-xr-x 4 root root 2000196 Sep 24 18:54 ..\n\nbuild:\ntotal 2986\ndrwxr-xr-x 2 root root 1004957 Sep 24 18:54 .\ndrwxr-xr-x 4 root root 2000196 Sep 24 18:54 ..\n-rw-r--r-- 1 root root   24856 Sep 24 18:36 eval_original.py\n-rw-r--r-- 1 root root    2910 Sep 24 18:36 make_mini_data.py\n-rw-r--r-- 1 root root   20197 Sep 24 18:52 make_notebook.py\n-rw-r--r-- 1 root root     935 Sep 24 18:51 run1.log\n-rw-r--r-- 1 root root     935 Sep 24 18:52 run2.log\n-rw-r--r-- 1 root root     935 Sep 24 18:53 run3.log\n900K\tcode_demo.ipynb\n423K\tmini_demo_data.json", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [46] TOOL CALL — Bash · 2026-09-24 18:54:25 UTC

```
python3 - <<'EOF'
from pathlib import Path
p = Path("build/make_mini_data.py"); s = p.read_text()
s = s.replace('"""Build mini_demo_data.json from the evaluation artifact\'s saved outputs (run once, locally)."""\nimport json, math',
 '"""Build mini_demo_data.json from the evaluation artifact\'s saved outputs (run once, locally).\n\nusage: python build/make_mini_data.py <path to the evaluation artifact workspace (holds results/, tables/, audit/)>"""\nimport json, math, sys')
s = s.replace('W = Path("/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2")', 'W = Path(sys.argv[1])')
s = s.replace('s = s.replace("/ai-inventor/aii_data/runs/run_u75jRHUss0zo/", "")  # no absolute server paths in published files',
 's = s.replace(str(W.parents[3]) + "/", "")  # strip the run-root prefix: no absolute server paths in published files')
p.write_text(s)
EOF
grep -rn "ai-inventor/" build/ README.md 2>/dev/null; python3 -c "from pathlib import Path;W=Path('/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2');print(W.parents[3])"
cp mini_demo_data.json build/_old.json && python3 build/make_mini_data.py /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2 && cmp mini_demo_data.json build/_old.json && echo identical && rm build/_old.json
```

### [47] TOOL RESULT — Bash · 2026-09-24 18:54:27 UTC

```
{"stdout": "/ai-inventor/aii_data/runs/run_u75jRHUss0zo\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_FWy8D4_y9GBn/mini_demo_data.json 0.432415 MB 100 96\nidentical", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [48] TOOL CALL — Bash · 2026-09-24 18:54:45 UTC

````
cat > .aii/manifest.yaml <<'EOF'
# No heavy paths: every file in this workspace is small text/code (< 1 MB). The disposable test venv (.nb_env/)
# was already removed after the test run; recreate it with the commands in README.md if needed.
entries: []
EOF
cat > README.md <<'EOF'
# Demo notebook — Why cross-model agreement flags logic errors (consensus-mechanism audit, T4 on dataset E)

A runnable Colab/Jupyter walk-through of the evaluation script `eval.py` from the artifact
*"Why cross-model agreement flags logic errors"*. The audit asks why a label-free cross-family z3 consensus score
(`c_score_align`) predicts whether an NL→FOL translation is faithful. It splits binary majority consensus exactly as
`AUROC_b = 1 − (e + d)/2`, where e is the error-endorsement rate and d is the correct-divergence rate, and then tests
how e and d change with sentence complexity.

## What the notebook does

- Loads `mini_demo_data.json`, from GitHub or from the local copy.
- Recomputes e, d, the binary AUROCs of five consensus rules, and the graded AUROC and ROC trace on 96 consensus-scorable
  R_AB rows. It uses the artifact's own `auc()`, `ed_decomposition()` and `graded_trace()`, copied verbatim.
- Runs `figures(A)` and `build_eval_out(A, B)` from `eval.py`. The only changes are that file reads now come from `data`.
  These produce `figures/fig1…fig4` and an `eval_out.json` with 335 metrics, the verdicts, and 100 example rows.
- Prints the headline table and verdicts, plots the demo rows' scores, and shows the four figures.

The notebook does not rerun the heavy stages: the z3 eqmv matrix, `part_a.run()`, the PART B record and the audits.
They need the full raw inputs from earlier iterations. The notebook reads their saved outputs from `mini_demo_data.json` instead.

## Layout

| Path | What |
|---|---|
| `code_demo.ipynb` | The demo notebook, executed, with outputs. About 5.5 min in a clean env, almost all of it `pip install`; the cells themselves take under 10 s |
| `mini_demo_data.json` | 0.43 MB. Contains `part_a` (every PART A number), `record_summary`, `pt_vs_s4_rows`, the audit JSONs, the prereg and its sha256, the 3 tables `figures()` reads, and 100 R_AB rows (`rab_rows`) with their population columns (`population_rows`). The rows are 12 per stratum × label with seed 0, plus 4 non-scorable rows |
| `build/make_mini_data.py` | Rebuilds `mini_demo_data.json` from the artifact workspace (`python build/make_mini_data.py <artifact dir>`) |
| `build/make_notebook.py` | Rebuilds `code_demo.ipynb` by slicing `figures()` and `build_eval_out()` verbatim out of `build/eval_original.py` |
| `build/eval_original.py` | Unmodified copy of the artifact's `eval.py`, kept for reference |
| `build/run*.log` | nbconvert logs of the test runs |

## How to run

On Colab, open `code_demo.ipynb` and run all cells. The data loads from the GitHub raw URL.

Locally, to reproduce the clean-environment test:

```bash
/usr/local/bin/python3.12 -m venv .nb_env
.nb_env/bin/pip install -q pip jupyter ipykernel
.nb_env/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb
rm -rf .nb_env
```

The config cell sets `N_EXAMPLES = 100`, which is every row in the demo data; the original run used all 2,686 R_AB rows.
It also sets `FIG_DPI = 200`, the original resolution, and `N_SHOW`, the number of example rows printed.

## Restoring removed files

`.aii/manifest.yaml` has no `delete` entries. Nothing heavy was kept or removed. The only disposable directory, `.nb_env/`,
was deleted after testing; recreate it with the commands above. Running the notebook regenerates `figures/`, `logs/` and `eval_out.json`.
EOF
cat > .terminal_claude_agent_struct_out.json <<'EOF'
{"out_expected_files": {"notebook": "code_demo.ipynb", "mini_data_file": "mini_demo_data.json"}}
EOF
cat .terminal_claude_agent_struct_out.json; grep -c 'urllib.request.urlopen(GITHUB_DATA_URL)' code_demo.ipynb
````

### [49] TOOL RESULT — Bash · 2026-09-24 18:54:45 UTC

```
{"stdout": "{\"out_expected_files\": {\"notebook\": \"code_demo.ipynb\", \"mini_data_file\": \"mini_demo_data.json\"}}\n1", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [50] ASSISTANT · 2026-09-24 18:54:54 UTC

```
I've built `code_demo.ipynb` and `mini_demo_data.json`, and the notebook runs from scratch in a clean Python 3.12 environment with no errors. That run took about 5.5 minutes, almost all of it package installs, against the 10-minute limit.

**How much of `eval.py` actually runs:** the heavy stages are not rerun: the z3 equivalence matrix, `part_a.run()`, the iteration-2 record builders and the audit scripts. They need the full raw inputs from earlier iterations. Their saved outputs are packed into `mini_demo_data.json` (0.43 MB) instead. The parts that do run:
- **`figures()` and `build_eval_out()` from `eval.py`**, copied as they are. The only changes are that file and pickle reads now come from the loaded data (each keeps the original line as a `# was:` comment), and the figures use the configured resolution. I also removed two script-only lines, the `PYTHONHASHSEED` re-launch and the 20 GB memory cap. The first only matters for the matrix, which isn't rerun.
- **A recomputation cell** that applies the artifact's own `auc()`, `ed_decomposition()` and `graded_trace()`, copied unchanged from its `src/` folder, to the demo rows. The graded score beats every binary majority rule here too (AUROC 0.722 vs 0.646 for majority voting), and the identity AUROC_b = 1 − (e+d)/2 checks out for every rule. The full-population values are 0.784 vs 0.669. The demo sample has 96 rows and is balanced 48 errors to 48 correct, so its numbers are noisy.
- **A results section** with the headline metrics and verdicts, a few example rows, a plot of the demo rows' scores, and the four regenerated figures. The full run's headline numbers print as expected: graded 0.784 vs binary 0.669, e = 0.124, d = 0.537, k95 = 3.

**Demo data:** 100 rows, 12 from each of the 8 stratum × label groups (seed 0), plus 4 rows the consensus score can't be computed for. The config is `N_EXAMPLES = 100`, all the rows in the demo file; the original run used 2,686. I tested at 20 rows first, then at 100, with no errors either time.

**Checks:**
- The notebook contains the exact `GITHUB_DATA_URL` and loads with the GitHub-then-local fallback.
- The published files contain no absolute server paths.
- `.aii/manifest.yaml` has no entries because nothing in the workspace is large, and the test environment was deleted.
- The README describes the layout and how to run it.
- `.terminal_claude_agent_struct_out.json` is written.

The scripts that rebuild the demo data and the notebook are in `build/`.

Files are in the workspace:
- `code_demo.ipynb`
- `mini_demo_data.json`
- `README.md`
- `.aii/manifest.yaml`
- `.terminal_claude_agent_struct_out.json`
```
