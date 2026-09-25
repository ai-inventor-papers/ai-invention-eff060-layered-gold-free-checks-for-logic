# gen_demo_art_dataset_4 — report_results

> Phase: `gen_paper_repo` · `gen_demo_art`
> Run: `gen_paper_repo_a2e1d024cc16` — Cross-Family Solver Consensus as a Gold-Free Faithfulness Metric for Natural Language to First-Order Logic Translation
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_demo_art_dataset_4` (terminal_claude_agent, claude-opus-5-5)

### [1] CONFIG · 2026-09-25 13:09:55 UTC

```
model: claude-opus-5-5 | effort: high | permission: bypassPermissions
```

### [2] SYSTEM-USER prompt · 2026-09-25 13:10:01 UTC

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
Your workspace: `/ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_Ia_FT284H33j`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_Ia_FT284H33j/`:
GOOD: `/ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_Ia_FT284H33j/file.py`, `/ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_Ia_FT284H33j/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>
<disposable_outputs>
A SHARED CACHE ALREADY EXISTS FOR THIS RUN: `/ai-inventor/aii_data/runs/run_qck1d05BqxkX/.shared_cache`
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
out_demo_files:
- path: data.py
  description: Dataset fetching/generation script
</artifact_info>

<github_repo>
Repo URL: https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic
Raw data URL: https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/fork/run_qck1d05BqxkX/round-4/dataset-5/demo/mini_demo_data.json

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
GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/fork/run_qck1d05BqxkX/round-4/dataset-5/demo/mini_demo_data.json"
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
To test-run the notebook in a clean environment (simulating Colab), use the disposable venv at `/tmp/aii_nb_test_envs/art_Ia_FT284H33j-af39a9391776`. It is on this machine's local disk, outside your workspace, which is on a slow network volume: never create a venv inside your workspace.
```bash
UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_Ia_FT284H33j-af39a9391776
UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_Ia_FT284H33j-af39a9391776/bin/python jupyter ipykernel
/tmp/aii_nb_test_envs/art_Ia_FT284H33j-af39a9391776/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb
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
TODO 6. Verify: (1) code_demo.ipynb contains GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/fork/run_qck1d05BqxkX/round-4/dataset-5/demo/mini_demo_data.json" exactly, (2) mini_demo_data.json exists, (3) uses GitHub URL pattern not just open('mini_demo_data.json').
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

### [3] HUMAN-USER prompt · 2026-09-25 13:10:01 UTC

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

### [4] TOOL CALL — Skill · 2026-09-25 13:10:05 UTC

```
aii-colab
```

### [5] TOOL RESULT — Skill · 2026-09-25 13:10:05 UTC

```
{"success": true, "commandName": "aii-colab"}
```

### [6] TOOL CALL — Skill · 2026-09-25 13:10:05 UTC

```
aii-long-running-tasks
```

### [7] TOOL RESULT — Skill · 2026-09-25 13:10:05 UTC

```
{"success": true, "commandName": "aii-long-running-tasks"}
```

### [8] TOOL CALL — Bash · 2026-09-25 13:10:07 UTC

```
List artifact and workspace files:
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5; ls -la $W; ls -la $W/src 2>/dev/null; wc -l $W/data.py; ls -la .; ls -la .aii
```

### [9] TOOL RESULT — Bash · 2026-09-25 13:10:09 UTC

```
{"stdout": "total 37062\ndrwxr-xr-x 11 root root  2009731 Sep 24 10:50 .\ndrwxr-xr-x  7 root root  2038553 Sep 24 07:07 ..\ndrwxr-xr-x  2 root root    72500 Sep 24 07:55 .aii\n-rw-------  1 root root       54 Sep 24 07:08 .aii_claude_session.json\n-rw-r--r--  1 root root     1526 Sep 24 07:28 .aii_cost_ledger.jsonl\n-rw-------  1 root root     8646 Sep 24 07:55 .aii_worker_result.json\n-rw-r--r--  1 root root  2425895 Sep 24 07:55 .repl_agent.ptylog\n-rw-r--r--  1 root root     3026 Sep 24 07:54 .terminal_claude_agent_struct_out.json\n-rw-r--r--  1 root root     7886 Sep 24 07:53 README.md\n-rw-r--r--  1 root root     2054 Sep 24 07:12 VENDOR_SHA256.json\n-rw-r--r--  1 root root      819 Sep 24 07:45 cost_ledger.jsonl\n-rw-r--r--  1 root root     3714 Sep 24 07:53 data.py\n-rw-r--r--  1 root root    10436 Sep 24 07:46 dataset_card.md\n-rw-r--r--  1 root root     4460 Sep 24 07:36 deviations.json\n-rw-r--r--  1 root root 20238149 Sep 24 07:51 full_data_out.json\ndrwxr-xr-x  2 root root  1014830 Sep 24 07:48 logs\n-rw-r--r--  1 root root    25038 Sep 24 07:51 mini_data_out.json\n-rw-r--r--  1 root root    12063 Sep 24 07:25 prereg_freelab.json\n-rw-r--r--  1 root root       86 Sep 24 07:25 prereg_freelab.sha256\n-rw-r--r--  1 root root    11204 Sep 24 07:22 prereg_freelab_v1.json\n-rw-r--r--  1 root root       89 Sep 24 07:25 prereg_freelab_v1.sha256\n-rw-r--r--  1 root root    15836 Sep 24 07:51 preview_data_out.json\ndrwxr-xr-x  2 root root  1000110 Sep 24 07:22 prompts\n-rw-r--r--  1 root root      781 Sep 24 07:53 pyproject.toml\n-rw-r--r--  1 root root       27 Sep 24 07:20 pytest.ini\n-rw-r--r--  1 root root     8805 Sep 24 07:53 reproducibility.md\ndrwxr-xr-x  2 root root  2004356 Sep 24 07:46 results\ndrwxr-xr-x  2 root root  1014457 Sep 24 10:50 src\ndrwxr-xr-x  3 root root  2002457 Sep 24 07:50 temp\ndrwxr-xr-x  2 root root  1001128 Sep 24 10:50 tests\ndrwxr-xr-x  2 root root  1002841 Sep 24 10:50 vendor\ndrwxr-xr-x  2 root root  2000711 Sep 24 07:46 work\ntotal 3102\ndrwxr-xr-x  2 root root 1014457 Sep 24 10:50 .\ndrwxr-xr-x 11 root root 2009731 Sep 24 10:50 ..\n-rw-r--r--  1 root root    9766 Sep 24 07:37 assemble_labels.py\n-rw-r--r--  1 root root    6169 Sep 24 07:43 build_output.py\n-rw-r--r--  1 root root    2436 Sep 24 07:20 common.py\n-rw-r--r--  1 root root   37862 Sep 24 07:32 freelab.py\n-rw-r--r--  1 root root   12832 Sep 24 07:31 gate.py\n-rw-r--r--  1 root root    8622 Sep 24 07:30 gloss.py\n-rw-r--r--  1 root root    4014 Sep 24 07:28 hf_survey.py\n-rw-r--r--  1 root root    9645 Sep 24 07:20 inputs.py\n-rw-r--r--  1 root root    5518 Sep 24 07:37 post_seal_join.py\n-rw-r--r--  1 root root   12216 Sep 24 07:25 prereg.py\n-rw-r--r--  1 root root    2308 Sep 24 07:45 provisional_view.py\n-rw-r--r--  1 root root   12023 Sep 24 07:42 resume_gloss.py\n-rw-r--r--  1 root root    5114 Sep 24 07:24 run_search.py\n-rw-r--r--  1 root root    4296 Sep 24 07:34 sig_rename.py\n-rw-r--r--  1 root root   11806 Sep 24 07:43 soundness.py\n-rw-r--r--  1 root root    3419 Sep 24 07:12 vendor_copy.py\n67 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/data.py\ntotal 2966\ndrwxr-xr-x 3 root root 1003109 Sep 25 13:09 .\ndrwxr-xr-x 6 root root 2000210 Sep 25 13:09 ..\ndrwxr-xr-x 2 root root       1 Sep 25 13:09 .aii\n-rw------- 1 root root      54 Sep 25 13:09 .aii_claude_session.json\n-rw-r--r-- 1 root root   31841 Sep 25 13:10 .repl_agent.ptylog\ntotal 981\ndrwxr-xr-x 2 root root       1 Sep 25 13:09 .\ndrwxr-xr-x 3 root root 1003109 Sep 25 13:09 ..", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [10] TOOL CALL — Bash · 2026-09-25 13:10:11 UTC

```
Read demo script, builder and preview:
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5; cat $W/data.py; echo ----; cat $W/src/build_output.py; echo ---; head -c 4000 $W/preview_data_out.json
```

### [11] TOOL RESULT — Bash · 2026-09-25 13:10:11 UTC

```
{"stdout": "# /// script\n# requires-python = \">=3.12\"\n# dependencies = [\"loguru==0.7.3\"]\n# ///\n\"\"\"Build full_data_out.json (exp_sel_data_out) from the three chosen datasets, one example per data row:\n  rcomp_free_labels      2,652 FREE rows, name-free labels (search-only, sealed; see dataset_card.md)\n  gloss_gate_items         840 known-answer (symbol use, meaning) items\n  sig_soundness_replay   4,280 renamed SIG rows with known pure-z3 labels\nAll three are derived from this run's R_COMP artifacts by src/*.py (results/*.jsonl, work/sentences.json).\nusage: uv run data.py\n\"\"\"\nfrom __future__ import annotations\n\nimport json\nimport sys\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parent\nsys.path.insert(0, str(ROOT / \"src\"))\nsys.path.insert(0, str(ROOT / \"vendor\"))\n\nfrom loguru import logger  # noqa: E402\n\nlogger.remove()\nlogger.add(sys.stdout, level=\"INFO\", format=\"{time:HH:mm:ss}|{level:<7}|{message}\")\n(ROOT / \"logs\").mkdir(exist_ok=True)\nlogger.add(ROOT / \"logs\" / \"data.log\", rotation=\"30 MB\", level=\"DEBUG\")\n\nSELECTED = [\"rcomp_free_labels\", \"gloss_gate_items\", \"sig_soundness_replay\"]\n\n\n@logger.catch(reraise=True)\ndef main() -> None:\n    import build_output as B  # run-derived plan groups (reads results/*.jsonl, work/sentences.json)\n    groups = [B.free_group(), B.gate_group(), B.sig_group()]\n    for g in groups:\n        assert g[\"examples\"], g[\"dataset\"]\n        for e in g[\"examples\"]:\n            assert isinstance(e[\"input\"], str) and isinstance(e[\"output\"], str), g[\"dataset\"]\n            assert not ({\"split\", \"dataset\", \"context\"} & set(e)), g[\"dataset\"]\n    seal = json.loads((ROOT / \"results\" / \"seal.json\").read_text())[\"seals\"][-1]\n    t = json.loads((ROOT / \"results\" / \"testability_FREE_v2.json\").read_text())\n    out = {\"metadata\": {\n        \"artifact\": \"T7b name-free labels for free-vocabulary rule translations (run_u75jRHUss0zo, iter 4, gen_art_dataset_5)\",\n        \"workspace\": str(ROOT),\n        \"selection\": (\"the three plan groups (chosen as best 3 of 6 standardised candidates; folio / malls_test / \"\n                      \"logicnli_test were context only: no multi-system candidates, ~36-39% wrong gold, or no FOL; their \"\n                      \"standardised record is temp/candidates_data_out.json)\"),\n        \"label_mode\": seal[\"mode\"],\n        \"status_note\": (\"SEARCH-ONLY labels: the paid gloss step could not run (deviation D9: run OpenRouter budget \"\n                        \"exhausted before this artifact's first call; re-probed at packaging, still HTTP 403). ERROR_CERT is \"\n                        \"final and certificate-backed; MAPPED rows are UNRESOLVED_GLOSS_NOT_RUN until src/resume_gloss.py \"\n                        \"runs. metadata_label_binary_search_provisional (ERROR vs MAPPED) is a provisional view with audited \"\n                        \"contamination (results/soundness_audit.json).\"),\n        \"seal_all_rows_sha256\": seal[\"label_vector_sha256_all_rows\"],\n        \"seal_untouched_sha256\": seal.get(\"label_vector_sha256_untouched\"),\n        \"prereg_sha256\": seal[\"prereg_sha256\"],\n        \"testability_all_rows\": {k: t[\"all_rows\"][k] for k in (\"n_ERROR\", \"n_CORRECT\", \"TESTABLE\", \"label_counts\")},\n        \"testability_untouched\": {k: t[\"untouched_subset\"][k] for k in (\"n_ERROR\", \"n_CORRECT\", \"TESTABLE\", \"label_counts\")},\n        \"provisional_view_testable\": {k: t[\"search_provisional_view\"][k][\"TESTABLE\"] for k in (\"all_rows\", \"untouched_subset\")},\n    }, \"datasets\": [g for g in groups if g[\"dataset\"] in SELECTED]}\n    (ROOT / \"full_data_out.json\").write_text(json.dumps(out, ensure_ascii=False))\n    logger.info(f\"full_data_out.json: {[(g['dataset'], len(g['examples'])) for g in out['datasets']]}\")\n\n\nif __name__ == \"__main__\":\n    main()\n----\n#!/usr/bin/env python3\n\"\"\"STEP I: full_data_out.json (exp_sel_data_out) with three groups:\n  rcomp_free_labels     one row per FREE generation record (2,652), label = name-free label (search-only now, D9)\n  gloss_gate_items      840 known-answer (symbol use, meaning) items, 7 classes, halves A/B\n  sig_soundness_replay  4,280 rows = 2,140 SIG rows x {nonce, synonym} renames, output = known pure-z3 SIG label\n\"\"\"\nfrom __future__ import annotations\n\nimport json\n\nfrom common import RES, ROOT, WORK, load_jsonl, setup_logger\n\nlogger = setup_logger(\"build_output\")\n\n\ndef md(d: dict) -> dict:\n    return {f\"metadata_{k}\": v for k, v in d.items()}\n\n\ndef free_group() -> dict:\n    rows = load_jsonl(RES / \"free_labels_v2.jsonl\")\n    ex = []\n    for r in rows:\n        inp = {\"text\": r[\"text\"], \"candidate_fol\": r[\"candidate_fol\"], \"system\": r[\"system\"], \"family\": r[\"family\"],\n               \"slot\": r[\"slot\"], \"prompt_variant\": r[\"prompt_variant\"], \"condition\": \"FREE\", \"template_id\": r[\"template_id\"]}\n        search_bin = {\"ERROR_CERT\": \"ERROR\", \"UNRESOLVED_GLOSS_NOT_RUN\": \"MAPPED\"}.get(r[\"label\"], \"EXCLUDED\")\n        meta = {\n            \"row_key\": r[\"row_key\"], \"item_id\": r[\"item_id\"], \"sentence_id\": r[\"sentence_id\"], \"template_id\": r[\"template_id\"],\n            \"clause_type\": r[\"clause_type\"], \"words\": r[\"words\"], \"word_tercile\": r[\"word_tercile\"],\n            \"nconds_weak\": r[\"nconds_weak\"], \"negated_condition\": r[\"negated_condition\"], \"nested\": r[\"nested\"],\n            \"label_binary\": r[\"label_binary\"], \"label_binary_search_provisional\": search_bin,\n            \"label_source\": r[\"label_source\"], \"search_status\": r.get(\"search_status\"),\n            \"matched_reading\": r.get(\"matched_reading\") or r.get(\"matched_reading_search\"),\n            \"map_certificate\": r.get(\"map_certificate\"),\n            \"n_maps_enumerated\": r.get(\"n_maps_enumerated\"), \"n_maps_fingerprint_pass\": r.get(\"n_maps_fingerprint_pass\"),\n            \"n_equiv_maps\": r.get(\"n_equiv_maps\"), \"n_equiv_map_orbits\": r.get(\"n_equiv_map_orbits\"),\n            \"nonequiv_certificate_type_counts\": r.get(\"nonequiv_certificate_type_counts\"),\n            \"gloss_pairs\": r.get(\"gloss_pairs\"), \"gloss_decision\": r.get(\"gloss_decision\"),\n            \"unresolved_reason\": r.get(\"unresolved_reason\"), \"irrelevant_symbols\": r.get(\"irrelevant_symbols\"),\n            \"search_secs\": r.get(\"search_secs\"), \"seen_iter3\": r.get(\"seen_iter3\"),\n            \"old_label_iter3\": r.get(\"old_label_iter3\"), \"fold\": \"RCOMP_FREE\"}\n        ex.append({\"input\": json.dumps(inp, ensure_ascii=False), \"output\": r[\"label\"], **md(meta)})\n    return {\"dataset\": \"rcomp_free_labels\", \"examples\": ex}\n\n\ndef gate_group() -> dict:\n    items = json.loads((RES / \"gate_items.json\").read_text())\n    ex = []\n    for i in items:\n        inp = {\"sentence\": i[\"sentence\"], \"candidate_atom\": i[\"candidate_atom\"], \"proposed_meaning\": i[\"proposed_meaning\"]}\n        meta = {\"item_id\": i[\"item_id\"], \"class\": i[\"class\"], \"half\": i[\"half\"], \"sentence_id\": i[\"sentence_id\"],\n                \"template_id\": i[\"template_id\"], \"note\": i[\"note\"], \"prompt_version\": \"gloss_v1\",\n                \"haiku_verdict\": i.get(\"haiku_gloss_v1\"), \"qwen_verdict\": i.get(\"qwen_gloss_v1\"), \"fold\": \"GLOSS_GATE\"}\n        ex.append({\"input\": json.dumps(inp, ensure_ascii=False), \"output\": i[\"gold\"], **md(meta)})\n    return {\"dataset\": \"gloss_gate_items\", \"examples\": ex}\n\n\ndef sig_group() -> dict:\n    sents = json.loads((WORK / \"sentences.json\").read_text())\n    rows = load_jsonl(RES / \"sig_replay_rows.jsonl\")\n    ex = []\n    for r in rows:\n        inp = {\"text\": sents[r[\"sentence_id\"]][\"text\"], \"candidate_fol\": r[\"renamed_fol\"], \"rename\": r[\"rename\"],\n               \"template_id\": r[\"template_id\"]}\n        meta = {k: r[k] for k in (\"row_key\", \"sentence_id\", \"slot\", \"template_id\", \"sig_matched_reading\", \"canon_fol\",\n                                  \"search_status\", \"identity_map_found\", \"non_identity_map_found\", \"n_equiv_maps\",\n                                  \"n_equiv_map_orbits\", \"n_maps_enumerated\", \"nonequiv_certificate_type_counts\",\n                                  \"oracle_end_to_end_label\", \"in_e2e_gloss_subsample_300\", \"e2e_gloss_label\")}\n        meta[\"map_equiv_found\"] = r[\"search_status\"] in (\"MAPPED\", \"READING_CHOICE\")\n        meta[\"fold\"] = f\"SIG_REPLAY_{r['rename'].upper()}\"\n        ex.append({\"input\": json.dumps(inp, ensure_ascii=False), \"output\": r[\"sig_label\"], **md(meta)})\n    return {\"dataset\": \"sig_soundness_replay\", \"examples\": ex}\n\n\ndef main() -> None:\n    seal = json.loads((RES / \"seal.json\").read_text())[\"seals\"]\n    t = json.loads((RES / \"testability_FREE_v2.json\").read_text())\n    out = {\"metadata\": {\n        \"artifact\": \"T7b name-free labels for free-vocabulary rule translations (run_u75jRHUss0zo, iter 4, gen_art_dataset_5)\",\n        \"workspace\": str(ROOT),\n        \"label_mode\": seal[-1][\"mode\"],\n        \"status_note\": (\"SEARCH-ONLY labels: the paid gloss step could not run (deviation D9: run OpenRouter budget \"\n                        \"exhausted before this artifact's first call). ERROR_CERT is final and certificate-backed; MAPPED rows \"\n                        \"are UNRESOLVED_GLOSS_NOT_RUN until src/resume_gloss.py runs. metadata_label_binary_search_provisional \"\n                        \"(ERROR vs MAPPED) is a provisional view with audited contamination (see results/soundness_audit.json).\"),\n        \"seal_all_rows_sha256\": seal[-1][\"label_vector_sha256_all_rows\"],\n        \"seal_untouched_sha256\": seal[-1].get(\"label_vector_sha256_untouched\"),\n        \"prereg_sha256\": seal[-1][\"prereg_sha256\"],\n        \"testability_all_rows\": {k: t[\"all_rows\"][k] for k in (\"n_ERROR\", \"n_CORRECT\", \"TESTABLE\", \"label_counts\")},\n        \"testability_untouched\": {k: t[\"untouched_subset\"][k] for k in (\"n_ERROR\", \"n_CORRECT\", \"TESTABLE\", \"label_counts\")}\n        if isinstance(t.get(\"untouched_subset\"), dict) else None,\n    }, \"datasets\": [free_group(), gate_group(), sig_group()]}\n    (ROOT / \"full_data_out.json\").write_text(json.dumps(out, ensure_ascii=False))\n    logger.info(f\"full_data_out.json: {[(d['dataset'], len(d['examples'])) for d in out['datasets']]}\")\n\n\nif __name__ == \"__main__\":\n    main()\n---\n{\n  \"metadata\": {\n    \"artifact\": \"T7b name-free labels for free-vocabulary rule translations (run_u75jRHUss0zo, iter 4, gen_art_dataset_5)\",\n    \"workspace\": \"/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5\",\n    \"selection\": \"the three plan groups (chosen as best 3 of 6 standardised candidates; folio / malls_test / logicnli_test were context only: no multi-system candidates, ~36-39% wrong gold, or no FOL; their standardise...\",\n    \"label_mode\": \"search_only\",\n    \"status_note\": \"SEARCH-ONLY labels: the paid gloss step could not run (deviation D9: run OpenRouter budget exhausted before this artifact's first call; re-probed at packaging, still HTTP 403). ERROR_CERT is final and...\",\n    \"seal_all_rows_sha256\": \"9609ebbb725832c467389e9d04b6334ca906ba10d400e7a7dccd976d39ebe3dd\",\n    \"seal_untouched_sha256\": \"b364a49a8e21835de660689097b462212f3f72b96ef66b437a14cc60e039f500\",\n    \"prereg_sha256\": \"b081c39991f52da2f419a6cefe56da48705d8abddf292d0faa89cec0b393a799\",\n    \"testability_all_rows\": {\n      \"n_ERROR\": 759,\n      \"n_CORRECT\": 0,\n      \"TESTABLE\": false,\n      \"label_counts\": {\n        \"ERROR_CERT\": 759,\n        \"UNRESOLVED_GLOSS_NOT_RUN\": 1506,\n        \"UNPARSEABLE\": 188,\n        \"NO_OUTPUT\": 199\n      }\n    },\n    \"testability_untouched\": {\n      \"n_ERROR\": 636,\n      \"n_CORRECT\": 0,\n      \"TESTABLE\": false,\n      \"label_counts\": {\n        \"ERROR_CERT\": 636,\n        \"UNRESOLVED_GLOSS_NOT_RUN\": 1175,\n        \"UNPARSEABLE\": 188,\n        \"NO_OUTPUT\": 199\n      }\n    },\n    \"provisional_view_testable\": {\n      \"all_rows\": true,\n      \"untouched_subset\": true\n    }\n  },\n  \"datasets\": [\n    {\n      \"dataset\": \"rcomp_free_labels\",\n      \"examples\": [\n        {\n          \"input\": \"{\\\"text\\\": \\\"Each legislator who is at Board Game night, who visits a coffee shop regularly, and who can distinguish the taste of different condiments is Emily's friend, except if the legislator is an el...\",\n          \"output\": \"ERROR_CERT\",\n          \"metadata_row_key\": \"a81d2862772cd744|FREE|G1|fewshot_v1\",\n          \"metadata_item_id\": \"a81d2862772cd744\",\n          \"metadata_sentence_id\": \"001a7f0caf5a\",\n          \"metadata_template_id\": \"T1\",\n          \"metadata_clause_type\": \"unless\",\n          \"metadata_words\": 34,\n          \"metadata_word_tercile\": \"W2\",\n          \"metadata_nconds_weak\": 5,\n          \"metadata_negated_condition\": null,\n          \"metadata_nested\": false,\n          \"metadata_label_binary\": \"ERROR\",\n          \"metadata_label_binary_search_provisional\": \"ERROR\",\n          \"metadata_label_source\": \"exhaustive_map_v1\",\n          \"metadata_search_status\": \"ERROR_CERT\",\n          \"metadata_matched_reading\": null,\n          \"metadata_map_certificate\": null,\n          \"metadata_n_maps_enumerated\": 0,\n          \"metadata_n_maps_fingerprint_pass\": 0,\n          \"metadata_n_equiv_maps\": 0,\n          \"metadata_n_equiv_map_orbits\": 0,\n          \"metadata_nonequiv_certificate_type_counts\": {\n            \"count_prune_subtree\": 291,\n            \"no_polarity_compatible_target\": 10\n          },\n          \"metadata_gloss_pairs\": null,\n          \"metadata_gloss_decision\": null,\n          \"metadata_unresolved_reason\": null,\n          \"metadata_irrelevant_symbols\": [],\n          \"metadata_search_secs\": 0.06,\n          \"metadata_seen_iter3\": false,\n          \"metadata_old_label_iter3\": \"UNRESOLVED\",\n          \"metadata_fold\": \"RCOMP_FREE\"\n        },\n        {\n          \"input\": \"{\\\"text\\\": \\\"Each legislator who is at Board Game night, who visits a coffee shop regularly, and who can distinguish the taste of different condiments is Emily's friend, except if the legislator is an el...\",\n          \"output\": \"UNRESOLVED_GLOSS_NOT_RUN\",\n          \"metadata_row_key\": \"94bcb373f89b6d9a|FREE|G1b|fewshot_v1\",\n          \"metadata_item_id\": \"94bcb373f89b6d9a\",\n          \"metadata_sentence_id\": \"001a7f0caf5a\",\n          \"metadata_template_id\": \"T1\",\n          \"metadata_clause_type\": \"unless\",\n          \"metadata_words\":", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [12] TOOL CALL — Bash · 2026-09-25 13:10:17 UTC

```
Inspect common.py and results files:
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5; cat $W/src/common.py; ls -la $W/results $W/work $W/vendor; cat $W/pyproject.toml
```

### [13] TOOL RESULT — Bash · 2026-09-25 13:10:17 UTC

```
{"stdout": "\"\"\"Shared paths, hashing and JSON helpers for the FREE name-free labeller (no metric, evaluator-model or aligner code here).\"\"\"\nfrom __future__ import annotations\n\nimport hashlib\nimport json\nimport re\nimport sys\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nfor _p in (ROOT / \"vendor\", ROOT / \"src\"):\n    if str(_p) not in sys.path:\n        sys.path.insert(0, str(_p))\nsys.setrecursionlimit(10000)\n\nRUN = Path(\"/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop\")\nE7 = RUN / \"iter_3/gen_art/gen_art_experiment_7\"\nD3 = RUN / \"iter_2/gen_art/gen_art_dataset_3\"\nGEN_FREE = E7 / \"rcomp/raw/generations.jsonl\"          # FREE raw generations: no scores, no labels\nSENTS = E7 / \"rcomp/work/rcomp_sentences.json\"\nD3_FULL = D3 / \"full_data_out.json\"\nLEXICON = D3 / \"lexicon.json\"\nSIG_LABELS = E7 / \"results/sig_labels.jsonl\"            # SIG labels only (pure z3), no scores\nOLD_CANDIDATES = E7 / \"results/rcomp_candidates.jsonl\"  # opened ONLY in STEP H (post-seal) via a whitelist loader\nNLTK_DATA = E7 / \"data/nltk_data\"\nRES = ROOT / \"results\"\nWORK = ROOT / \"work\"\nLOGS = ROOT / \"logs\"\nfor _d in (RES, WORK, LOGS):\n    _d.mkdir(exist_ok=True)\n\n\ndef sha1(s: str) -> str:\n    return hashlib.sha1(s.encode()).hexdigest()\n\n\ndef sha256_bytes(b: bytes) -> str:\n    return hashlib.sha256(b).hexdigest()\n\n\ndef sha256_file(p: Path) -> str:\n    return hashlib.sha256(Path(p).read_bytes()).hexdigest()\n\n\ndef norm_text(s: str) -> str:\n    \"\"\"Dataset E's select_sentences.norm (verbatim logic) used in the item_id recipe.\"\"\"\n    s = s.lower().replace(\"’\", \"'\").replace(\"‘\", \"'\").replace(\"“\", '\"').replace(\"”\", '\"')\n    s = re.sub(r\"[^a-z0-9 ]\", \" \", s)\n    return re.sub(r\"\\s+\", \" \", s).strip()\n\n\ndef item_id(system: str, text: str, raw: str | None) -> str:\n    \"\"\"exp 7 / dataset 3 recipe: sha1(system | norm(text) | raw_output)[:16] (raw None -> '').\"\"\"\n    return sha1(system + \"|\" + norm_text(text) + \"|\" + (raw or \"\"))[:16]\n\n\ndef load_jsonl(p: Path) -> list[dict]:\n    return [json.loads(l) for l in Path(p).read_text().splitlines() if l.strip()]\n\n\ndef dump(p: Path, obj) -> None:\n    Path(p).write_text(json.dumps(obj, indent=1, ensure_ascii=False))\n\n\ndef setup_logger(name: str):\n    from loguru import logger\n    logger.remove()\n    logger.add(sys.stdout, level=\"INFO\", format=\"{time:HH:mm:ss}|{level:<7}|{message}\")\n    logger.add(LOGS / f\"{name}.log\", rotation=\"30 MB\", level=\"DEBUG\")\n    return logger\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/results:\ntotal 48538\ndrwxr-xr-x  2 root root  2004356 Sep 24 07:46 .\ndrwxr-xr-x 11 root root  2009731 Sep 24 10:50 ..\n-rw-r--r--  1 root root    10436 Sep 24 07:46 dataset_card.md\n-rw-r--r--  1 root root  8143542 Sep 24 07:37 free_labels_v2.jsonl\n-rw-r--r--  1 root root   427414 Sep 24 07:32 gate_items.json\n-rw-r--r--  1 root root      303 Sep 24 07:45 gate_report.json\n-rw-r--r--  1 root root     1106 Sep 24 07:13 input_counts.json\n-rw-r--r--  1 root root 17748257 Sep 24 07:35 map_search.jsonl\n-rw-r--r--  1 root root    23765 Sep 24 07:37 old_label_agreement.json\n-rw-r--r--  1 root root     3623 Sep 24 07:37 seal.json\n-rw-r--r--  1 root root    31504 Sep 24 07:13 shape_census.json\n-rw-r--r--  1 root root  7459154 Sep 24 07:37 sig_replay_nonce.jsonl\n-rw-r--r--  1 root root  3820323 Sep 24 07:43 sig_replay_rows.jsonl\n-rw-r--r--  1 root root  7937822 Sep 24 07:39 sig_replay_syn.jsonl\n-rw-r--r--  1 root root    23836 Sep 24 07:43 soundness_audit.json\n-rw-r--r--  1 root root    52908 Sep 24 07:45 testability_FREE_v2.json\n\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/vendor:\ntotal 2973\ndrwxr-xr-x  2 root root 1002841 Sep 24 10:50 .\ndrwxr-xr-x 11 root root 2009731 Sep 24 10:50 ..\n-rw-r--r--  1 root root       0 Sep 24 07:12 __init__.py\n-rw-r--r--  1 root root    9244 Sep 24 07:12 fol.py\n-rw-r--r--  1 root root    4916 Sep 24 07:12 fol_triage_min.py\n-rw-r--r--  1 root root    1510 Sep 24 07:12 label_sig_min.py\n-rw-r--r--  1 root root    3557 Sep 24 07:12 perturb_min.py\n-rw-r--r--  1 root root    1584 Sep 24 07:12 repair_census_min.py\n-rw-r--r--  1 root root    1412 Sep 24 07:12 sig_prompt_min.py\n-rw-r--r--  1 root root    6871 Sep 24 07:12 templates.py\n\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/work:\ntotal 11210\ndrwxr-xr-x  2 root root 2000711 Sep 24 07:46 .\ndrwxr-xr-x 11 root root 2009731 Sep 24 10:50 ..\n-rw-r--r--  1 root root    2359 Sep 24 07:38 audit_errcert_keys.json\n-rw-r--r--  1 root root    2359 Sep 24 07:39 audit_mapped_keys.json\n-rw-r--r--  1 root root   43178 Sep 24 07:39 audit_mapped_view.txt\n-rw-r--r--  1 root root    1062 Sep 24 07:18 dev_trial_D1.py\n-rw-r--r--  1 root root    9223 Sep 24 07:40 executor_audit_verdicts.json\n-rw-r--r--  1 root root 1767883 Sep 24 07:13 free_rows.jsonl\n-rw-r--r--  1 root root  806127 Sep 24 07:21 models_snapshot.json\n-rw-r--r--  1 root root    1373 Sep 24 07:33 probe_free_models_D9.py\n-rw-r--r--  1 root root  685497 Sep 24 07:13 sentences.json\n-rw-r--r--  1 root root 1429393 Sep 24 07:34 sig_renamed_nonce.jsonl\n-rw-r--r--  1 root root 1663307 Sep 24 07:35 sig_renamed_syn.jsonl\n-rw-r--r--  1 root root 1053397 Sep 24 07:13 sig_rows.jsonl\n[project]\nname = \"freelab-u75j\"\nversion = \"0.1.0\"\ndescription = \"T7b: name-free (alignment-free) labels for free-vocabulary NL->FOL rule translations (run_u75jRHUss0zo iter 4, gen_art_dataset_5)\"\nrequires-python = \">=3.12\"\ndependencies = [\n    \"anyio==4.15.1\",\n    \"certifi==2026.7.22\",\n    \"click==8.5.0\",\n    \"cloudpickle==3.1.2\",\n    \"defusedxml==0.7.1\",\n    \"h11==0.16.0\",\n    \"httpcore==1.0.9\",\n    \"httpx==0.28.1\",\n    \"idna==3.20\",\n    \"iniconfig==2.3.0\",\n    \"joblib==1.6.0\",\n    \"loguru==0.7.3\",\n    \"nltk==3.10.3\",\n    \"numpy==2.5.3\",\n    \"packaging==26.3\",\n    \"pluggy==1.6.0\",\n    \"psutil==7.2.2\",\n    \"pygments==2.21.0\",\n    \"pytest==9.1.1\",\n    \"pyyaml==6.0.3\",\n    \"regex==2026.9.10\",\n    \"tqdm==4.70.1\",\n    \"typing-extensions==4.16.0\",\n    \"z3-solver==5.1.0.0\",\n]", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [14] TOOL CALL — Bash · 2026-09-25 13:10:27 UTC

```
Inspect freelab.py and a label row:
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5; grep -n "^def \|^class \|^from\|^import" $W/src/freelab.py; head -60 $W/src/freelab.py; python3 -c "
import json
rows=[json.loads(l) for l in open('$W/results/free_labels_v2.jsonl')]
print(len(rows)); r=[x for x in rows if x['label']=='UNRESOLVED_GLOSS_NOT_RUN'][0]
print(json.dumps(r,indent=1)[:5000]); print(sorted(rows[0].keys()))
"
```

### [15] TOOL RESULT — Bash · 2026-09-25 13:10:27 UTC

```
{"stdout": "30:from __future__ import annotations\n32:import itertools\n33:import re\n34:import time\n35:import zlib\n36:from collections import Counter, defaultdict\n37:from functools import lru_cache\n39:import z3\n41:from fol import mkpred, parse, preds, profile, to_z3, valid, U\n42:from repair_census_min import atoms, bound_vars\n55:def to_str(e) -> str:\n67:def name_tokens(n: str) -> list[str]:\n71:def negation_named(name: str) -> bool:\n77:def free_consts(e) -> set:\n93:def occurrences(e):\n110:def conj_chains(e):\n138:def rename_const(e, old: str, new: str, bv=frozenset()):\n149:def z3_equiv(a, b, ms: int) -> bool | None:\n155:def z3_equiv_retry(a, b) -> bool | None:\n165:def _atom_val(i: int, name: str, args: tuple) -> bool:\n170:def _const_val(i: int, name: str) -> int:\n174:def dom_size(i: int) -> int:\n178:def ev(e, i: int, env: dict) -> bool:\n202:def fingerprint(e, n: int = N_FP) -> tuple:\n206:def first_mismatch(e, ref_fp: tuple) -> int | None:\n215:def analyse_symbols(e) -> dict:\n263:def unit_display(u: dict, subj: str = \"x\") -> str:\n269:class Reading:\n316:def unit_display_of_atom(a, units: dict) -> str | None:\n324:class Candidate:\n363:def _pol_ok(p, q) -> bool:\n370:def unit_options(key: str, cand: Candidate, rd: Reading) -> list[tuple]:\n391:def rel_options(key: str, cand: Candidate, rd: Reading) -> list[tuple]:\n403:def build_image(cand: Candidate, rd: Reading, assign: dict, cmap: dict):\n442:def map_to_json(assign: dict, cmap: dict, cand: Candidate, rd: Reading) -> dict:\n462:def bridges_of(assign: dict, cand: Candidate, rd: Reading) -> list[str]:\n483:def search(cand: Candidate, rd: Reading, max_maps: int = MAX_MAPS, max_secs: float = MAX_SECS,\n537:def _covers(opt) -> list[str]:\n545:def _dfs(i, syms, assign, used_units, used_rels, n_struct, need, consts, cand, rd, res, t0, max_maps, max_secs, keep):\n591:def _leaf(assign, consts, cand, rd, res, t0, max_maps, max_secs, keep):\n623:def _finish(res, t0):\n631:def pair_items(m: dict, cand: Candidate, rd: Reading) -> list[tuple[str, str]]:\n685:def label_candidate(candidate_fol: str, readings: dict, glosses: dict | None = None, max_maps: int = MAX_MAPS,\n700:def label_with(cand: Candidate, rds: dict, max_maps: int, max_secs: float, t0: float | None = None) -> dict:\n765:def gloss_decision(maps: list[dict], pairs_union: list, verdict: dict) -> tuple[str, int | None]:\n791:def exhaustive_map_label(candidate_fol: str, readings: dict, atoms: dict | None = None, glosses: dict | None = None,\n818:def equivalent_modulo_vocab_exhaustive(a_fol: str, b_fol: str, max_maps: int = MAX_MAPS, max_secs: float = MAX_SECS\n\"\"\"Name-free (alignment-free) labelling of free-vocabulary FOL candidates against template readings.\n\nNo name similarity is used anywhere: symbol names are only used (a) as identifiers, (b) by the B5 lexical-negation\nregex, which licenses the map ``P := ¬U`` (a gloss check still has to accept it). Which candidate symbol means which\ntemplate atom is decided by EXHAUSTIVE enumeration of a declared map family under SOUND semantic prunes, followed by\nz3 equivalence; the lexical plausibility of the winning map is decided separately by a gloss check (``checker``).\n\nMap family (frozen in prereg_freelab.json):\n  * A candidate predicate is a UNIT if, in every occurrence, all argument positions but one (the subject position)\n    hold the same constants, and those constants occur nowhere else (\"constant absorption\"; unary predicates are\n    trivially units). A template atom over the single variable x (U(x) or R(x, c)) is a template UNIT.\n  * UNIT maps a candidate unit to exactly one template unit (plain, B1 reification and B2 de-reification are all\n    this form: P(x) := R(x, c); P(x, k) := U(x); P(x, k) := R(x, c)). B5: P := ¬u (only if the name's first token is a\n    negation marker). B3 merge: P := u1 ∧ u2 (u1, u2 sibling conjuncts of the reading). B4 split: two candidate units\n    that only ever occur as positive sibling conjuncts both := u.\n  * REL maps a genuinely relational candidate predicate (arity 2, not a unit) to a template binary predicate, either\n    argument order; its non-absorbed constants map injectively to template constants or stay free (fresh).\n  * Injective: each template unit / predicate is the target of at most one candidate symbol (B4 excepted).\n    Structural bridge uses (B3 + B4) <= MAX_STRUCT per map; B1/B2/B5 are 1:1 unit forms and are not capped.\n  * Semantically inert candidate symbols (F ≡ F[s := fresh]) are dropped (kept as fresh symbols in the image).\nSound prunes: relevance (every relevant candidate symbol must be mapped; every template unit must be covered),\npolarity (z3-exact monotonicity is preserved by 1:1 generic substitutions), and a finite-model fingerprint\n(128 interpretations, domain 2-3, fixed seeds; a mismatch is a certified countermodel). Maps that pass the\nfingerprint go to z3 (2 s, retry 10 s).\n\nEXACT: ERROR (no equivalent map) is exact RELATIVE TO THIS FAMILY and these caps; every equivalent map is a z3 proof.\nBOUNDED: maps outside the family (extra quantified structure, ∃-for-constant, ternary relations with variables, ...)\nare not searched; the search stops at MAX_MAPS maps or MAX_SECS seconds per (candidate, reading) -> CAP.\n\"\"\"\nfrom __future__ import annotations\n\nimport itertools\nimport re\nimport time\nimport zlib\nfrom collections import Counter, defaultdict\nfrom functools import lru_cache\n\nimport z3\n\nfrom fol import mkpred, parse, preds, profile, to_z3, valid, U\nfrom repair_census_min import atoms, bound_vars\n\nMAX_MAPS = 200_000\nMAX_SECS = 90.0\nMAX_STRUCT = 2\nN_FP = 128\nZ3_MS, Z3_MS_RETRY = 2000, 10000\nNEG_TOKEN = re.compile(r\"^(not|non|no|un|in|im|il|ir|dis|never|lacks?|without)$\", re.I)\nNEG_PREFIX = re.compile(r\"^(Un|Non|In|Im|Dis)[A-Z]\")\nFLIP = {\"UP\": \"DOWN\", \"DOWN\": \"UP\", \"NONMONO\": \"NONMONO\"}\n\n\n# ------------------------------------------------------------------------------------------------ AST helpers\ndef to_str(e) -> str:\n    k = e[0]\n    if k == \"atom\":\n        return f\"{e[1]}({', '.join(e[2])})\" if e[2] else e[1]\n    if k in (\"all\", \"ex\"):\n        return f\"{'∀' if k == 'all' else '∃'}{e[1]} ({to_str(e[2])})\"\n2652\n{\n \"row_key\": \"94bcb373f89b6d9a|FREE|G1b|fewshot_v1\",\n \"item_id\": \"94bcb373f89b6d9a\",\n \"sentence_id\": \"001a7f0caf5a\",\n \"slot\": \"G1b\",\n \"system\": \"G1b:meta-llama/llama-3.3-70b-instruct\",\n \"family\": \"meta\",\n \"model\": \"meta-llama/llama-3.3-70b-instruct\",\n \"prompt_variant\": \"fewshot_v1\",\n \"raw_output\": \"FOL: \\u2200x (Legislator(x) \\u2227 Attends(x, boardGameNight) \\u2227 Visits(x, coffeeShop) \\u2227 CanDistinguish(x, condiments) \\u2192 (FriendOf(x, emily) \\u2194 \\u00acElectedOfficial(x)))\",\n \"candidate_fol\": \"\\u2200x (Legislator(x) \\u2227 Attends(x, boardGameNight) \\u2227 Visits(x, coffeeShop) \\u2227 CanDistinguish(x, condiments) \\u2192 (FriendOf(x, emily) \\u2194 \\u00acElectedOfficial(x)))\",\n \"template_id\": \"T1\",\n \"clause_type\": \"unless\",\n \"words\": 34,\n \"word_tercile\": \"W2\",\n \"nconds_weak\": 5,\n \"negated_condition\": null,\n \"nested\": false,\n \"text\": \"Each legislator who is at Board Game night, who visits a coffee shop regularly, and who can distinguish the taste of different condiments is Emily's friend, except if the legislator is an elected official.\",\n \"class_key\": \"3c418cac14221076\",\n \"search_status\": \"MAPPED\",\n \"matched_reading_search\": \"strong\",\n \"n_maps_enumerated\": 48,\n \"n_maps_fingerprint_pass\": 48,\n \"n_equiv_maps\": 48,\n \"n_equiv_pairsets\": 48,\n \"n_equiv_map_orbits\": 2,\n \"nonequiv_certificate_type_counts\": {\n  \"count_prune_subtree\": 360\n },\n \"irrelevant_symbols\": [],\n \"search_secs\": 0.336,\n \"label_source\": \"exhaustive_map_v1\",\n \"label\": \"UNRESOLVED_GLOSS_NOT_RUN\",\n \"unresolved_reason\": \"gloss check not run (D9: API budget exhausted)\",\n \"gloss_decision\": null,\n \"map_certificate\": {\n  \"status\": \"z3_equivalent_map_not_gloss_checked\",\n  \"reading\": \"strong\",\n  \"map\": [\n   \"Attends(x, boardGameNight) => At(x, boardGameNight)\",\n   \"CanDistinguish(x, condiments) => Can(x, distinguishTheTasteOfDifferentCondiments)\",\n   \"ElectedOfficial(x) => ElectedOfficial(x)\",\n   \"FriendOf(x, emily) => EmilysFriend_2(x)\",\n   \"Legislator(x) => Legislator(x)\",\n   \"Visits(x, coffeeShop) => VisitRegularly(x, coffeeShop)\"\n  ],\n  \"bridges\": [\n   \"B2\"\n  ]\n },\n \"gloss_pairs\": [\n  {\n   \"cand_atom\": \"Attends(x, boardGameNight)\",\n   \"meaning\": \"x is at Board Game night\",\n   \"haiku\": null,\n   \"qwen\": null\n  },\n  {\n   \"cand_atom\": \"CanDistinguish(x, condiments)\",\n   \"meaning\": \"x can distinguish the taste of different condiments\",\n   \"haiku\": null,\n   \"qwen\": null\n  },\n  {\n   \"cand_atom\": \"ElectedOfficial(x)\",\n   \"meaning\": \"x is an elected official\",\n   \"haiku\": null,\n   \"qwen\": null\n  },\n  {\n   \"cand_atom\": \"FriendOf(x, emily)\",\n   \"meaning\": \"x is Emily's friend\",\n   \"haiku\": null,\n   \"qwen\": null\n  },\n  {\n   \"cand_atom\": \"Legislator(x)\",\n   \"meaning\": \"x is a legislator\",\n   \"haiku\": null,\n   \"qwen\": null\n  },\n  {\n   \"cand_atom\": \"Visits(x, coffeeShop)\",\n   \"meaning\": \"x visits a coffee shop regularly\",\n   \"haiku\": null,\n   \"qwen\": null\n  },\n  {\n   \"cand_atom\": \"CanDistinguish(x, condiments)\",\n   \"meaning\": \"x visits a coffee shop regularly\",\n   \"haiku\": null,\n   \"qwen\": null\n  },\n  {\n   \"cand_atom\": \"Visits(x, coffeeShop)\",\n   \"meaning\": \"x can distinguish the taste of different condiments\",\n   \"haiku\": null,\n   \"qwen\": null\n  },\n  {\n   \"cand_atom\": \"Attends(x, boardGameNight)\",\n   \"meaning\": \"x visits a coffee shop regularly\",\n   \"haiku\": null,\n   \"qwen\": null\n  },\n  {\n   \"cand_atom\": \"Visits(x, coffeeShop)\",\n   \"meaning\": \"x is at Board Game night\",\n   \"haiku\": null,\n   \"qwen\": null\n  },\n  {\n   \"cand_atom\": \"CanDistinguish(x, condiments)\",\n   \"meaning\": \"x is at Board Game night\",\n   \"haiku\": null,\n   \"qwen\": null\n  },\n  {\n   \"cand_atom\": \"Attends(x, boardGameNight)\",\n   \"meaning\": \"x can distinguish the taste of different condiments\",\n   \"haiku\": null,\n   \"qwen\": null\n  },\n  {\n   \"cand_atom\": \"Attends(x, boardGameNight)\",\n   \"meaning\": \"x is a legislator\",\n   \"haiku\": null,\n   \"qwen\": null\n  },\n  {\n   \"cand_atom\": \"Legislator(x)\",\n   \"meaning\": \"x is at Board Game night\",\n   \"haiku\": null,\n   \"qwen\": null\n  },\n  {\n   \"cand_atom\": \"Visits(x, coffeeShop)\",\n   \"meaning\": \"x is a legislator\",\n   \"haiku\": null,\n   \"qwen\": null\n  },\n  {\n   \"cand_atom\": \"CanDistinguish(x, condiments)\",\n   \"meaning\": \"x is a legislator\",\n   \"haiku\": null,\n   \"qwen\": null\n  },\n  {\n   \"cand_atom\": \"Legislator(x)\",\n   \"meaning\": \"x visits a coffee shop regularly\",\n   \"haiku\": null,\n   \"qwen\": null\n  },\n  {\n   \"cand_atom\": \"Legislator(x)\",\n   \"meaning\": \"x can distinguish the taste of different condiments\",\n   \"haiku\": null,\n   \"qwen\": null\n  },\n  {\n   \"cand_atom\": \"ElectedOfficial(x)\",\n   \"meaning\": \"x is Emily's friend\",\n   \"haiku\": null,\n   \"qwen\": null\n  },\n  {\n   \"cand_atom\": \"FriendOf(x, emily)\",\n   \"meaning\": \"x is an elected official\",\n   \"haiku\": null,\n   \"qwen\": null\n  }\n ],\n \"label_binary\": \"EXCLUDED\",\n \"seen_iter3\": false,\n \"old_label_iter3\": \"UNRESOLVED\",\n \"old_label_tier_iter3\": \"none\"\n}\n['candidate_fol', 'class_key', 'clause_type', 'family', 'gloss_decision', 'gloss_pairs', 'irrelevant_symbols', 'item_id', 'label', 'label_binary', 'label_source', 'map_certificate', 'matched_reading_search', 'model', 'n_equiv_map_orbits', 'n_equiv_maps', 'n_equiv_pairsets', 'n_maps_enumerated', 'n_maps_fingerprint_pass', 'nconds_weak', 'negated_condition', 'nested', 'nonequiv_certificate_type_counts', 'old_label_iter3', 'old_label_tier_iter3', 'prompt_variant', 'raw_output', 'row_key', 'search_secs', 'search_status', 'seen_iter3', 'sentence_id', 'slot', 'system', 'template_id', 'text', 'unresolved_reason', 'word_tercile', 'words']", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [16] ASSISTANT · 2026-09-25 13:10:35 UTC

```
Inspecting done; now building the mini demo data (a diverse ≤100-row subset of the raw inputs data.py reads).
```

### [17] TOOL CALL — Bash · 2026-09-25 13:10:35 UTC

```
Inspect gate, sig, sentences, seal, testability:
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5; python3 -c "
import json
g=json.load(open('$W/results/gate_items.json')); print(len(g)); print(json.dumps(g[0],indent=1)[:1500])
from collections import Counter; print(Counter(i['class'] for i in g))
r=json.loads(open('$W/results/sig_replay_rows.jsonl').readline()); print(json.dumps(r,indent=1)[:2500])
s=json.load(open('$W/work/sentences.json')); print(type(s), len(s)); k=list(s)[0]; print(json.dumps(s[k])[:800])
seal=json.load(open('$W/results/seal.json')); print(json.dumps(seal)[:1500])
t=json.load(open('$W/results/testability_FREE_v2.json')); print(list(t)); print({k:list(v) if isinstance(v,dict) else v for k,v in t.items()})
"
```

### [18] TOOL RESULT — Bash · 2026-09-25 13:10:35 UTC

```
{"stdout": "840\n{\n \"item_id\": \"5dce1bab60185c9f\",\n \"class\": \"YES_IDENT\",\n \"gold\": \"YES\",\n \"sentence_id\": \"13c415817af3\",\n \"sentence\": \"When a customer is not in our family and can cook, and the customer also is writing a novel, the customer is from China, except when the customer is at Board Game night.\",\n \"template_id\": \"T2\",\n \"half\": \"A\",\n \"candidate_atom\": \"Can(x, cook)\",\n \"proposed_meaning\": \"x can cook\",\n \"note\": \"\",\n \"haiku_gloss_v1\": null,\n \"qwen_gloss_v1\": null\n}\nCounter({'YES_IDENT': 120, 'YES_SYN': 120, 'YES_FORM': 120, 'NO_NONCE': 120, 'NO_DONOR': 120, 'NO_ROLE': 120, 'NO_MERGE': 120})\n{\n \"row_key\": \"917ac90fc8143e08|SIG|G7\",\n \"sentence_id\": \"001a7f0caf5a\",\n \"slot\": \"G7\",\n \"template_id\": \"T1\",\n \"sig_label\": \"CORRECT\",\n \"sig_matched_reading\": \"weak\",\n \"rename\": \"nonce\",\n \"canon_fol\": \"\\u2200x ((((((Legislator(x) \\u2227 At(x, boardGameNight)) \\u2227 VisitRegularly(x, coffeeShop)) \\u2227 Can(x, distinguishTheTasteOfDifferentCondiments)) \\u2227 \\u00ac(ElectedOfficial(x))) \\u2192 EmilysFriend_2(x)))\",\n \"renamed_fol\": \"\\u2200x ((((((Buzil(x) \\u2227 Getoz(x, lopod)) \\u2227 Gebeb(x, kamik)) \\u2227 Pubad(x, petog)) \\u2227 \\u00acGuzit(x)) \\u2192 Dogip(x)))\",\n \"search_status\": \"MAPPED\",\n \"identity_map_found\": {\n  \"weak\": true,\n  \"strong\": false,\n  \"converse\": false\n },\n \"non_identity_map_found\": true,\n \"n_equiv_maps\": 48,\n \"n_equiv_map_orbits\": 2,\n \"n_maps_enumerated\": 48,\n \"nonequiv_certificate_type_counts\": {\n  \"count_prune_subtree\": 291,\n  \"no_polarity_compatible_target\": 10\n },\n \"oracle_end_to_end_label\": \"CORRECT\",\n \"in_e2e_gloss_subsample_300\": false,\n \"e2e_gloss_label\": null\n}\n<class 'dict'> 221\n{\"sentence_id\": \"001a7f0caf5a\", \"text\": \"Each legislator who is at Board Game night, who visits a coffee shop regularly, and who can distinguish the taste of different condiments is Emily's friend, except if the legislator is an elected official.\", \"reference_fol_weak\": \"\\u2200x (Legislator(x) \\u2227 At(x, boardGameNight) \\u2227 VisitRegularly(x, coffeeShop) \\u2227 Can(x, distinguishTheTasteOfDifferentCondiments) \\u2227 \\u00acElectedOfficial(x) \\u2192 EmilysFriend_2(x))\", \"reference_fol_strong\": \"\\u2200x (Legislator(x) \\u2227 At(x, boardGameNight) \\u2227 VisitRegularly(x, coffeeShop) \\u2227 Can(x, distinguishTheTasteOfDifferentCondiments) \\u2192 (EmilysFriend_2(x) \\u2194 \\u00acElectedOfficial(x)))\", \"reading_converse\": null, \"template_id\": \"T1\", \"clause_type\": \"unless\", \"nested\": false, \"w\n{\"seals\": [{\"utc\": \"2026-09-24T07:37:10Z\", \"mode\": \"search_only\", \"label_vector_sha256_all_rows\": \"9609ebbb725832c467389e9d04b6334ca906ba10d400e7a7dccd976d39ebe3dd\", \"n_rows\": 2652, \"label_counts\": {\"ERROR_CERT\": 759, \"UNRESOLVED_GLOSS_NOT_RUN\": 1506, \"UNPARSEABLE\": 188, \"NO_OUTPUT\": 199}, \"prereg_sha256\": \"b081c39991f52da2f419a6cefe56da48705d8abddf292d0faa89cec0b393a799\", \"prereg_v1_sha256\": \"8ee7213d618be5be592464a9e0c83e40c5347a63ca5725283cdc4e0e70f51472\", \"vendor_sha256\": {\"__init__.py\": \"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855\", \"fol.py\": \"e37a655f98af4899b1bdee943c66b395b27847870d6788b5509cf92ef3f95fe4\", \"fol_triage_min.py\": \"b074c41135b8c1e7fe67057afab852b650b9c66426e061ce2eb93971705a212f\", \"label_sig_min.py\": \"8b275ba5b710b5014e4a5a667b242cf74eb47565f29c886125179a936fae9e3e\", \"perturb_min.py\": \"577e2fae8cecc0144dfc7931796ef3379ba90400db205bf9685d4d7bc39e3c4a\", \"repair_census_min.py\": \"9a97cfbf0846aa395bf752cf0fca727a3229799650202e59e14e5f43e32533dc\", \"sig_prompt_min.py\": \"95cbc1050e1fa48d81964adb0a4858838afc979b1744cf0c4fcb8d5c902a7cf5\", \"templates.py\": \"4fe4ad153406142bd81ce4d283f80f342f3f5dd511eb1fea38380d6e469e0393\"}, \"code_sha256\": {\"src/freelab.py\": \"06e14f582c5aa793a4f66817b23fea135922c1d78fdffb5d362991a7ba348be3\", \"src/run_search.py\": \"7f651c0b73710316a66fbf6156bf3dc3503b559fa081a7caf015ec9904e296c7\", \"src/assemble_labels.py\": \"1a87d3da56066729d63013014558885622590230bd4073c40d26fad1bfcf4d3b\"}, \"map_search_sha256\": \"4335677f141013396dda\n['mode', 'utc', 'rule', 'word_terciles', 'all_rows', 'untouched_subset', 'note', 'seen_iter3_subset', 'search_provisional_view']\n{'mode': 'search_only', 'utc': '2026-09-24T07:37:10Z', 'rule': 'TESTABLE iff >= 50 ERROR and >= 50 CORRECT rows, each class spread over >= 25 sentences', 'word_terciles': ['cut_1', 'cut_2'], 'all_rows': ['population', 'n_rows', 'n_ERROR', 'n_CORRECT', 'sentences_with_ERROR', 'sentences_with_CORRECT', 'TESTABLE', 'reportable_30_30', 'label_counts', 'strata'], 'untouched_subset': ['population', 'n_rows', 'n_ERROR', 'n_CORRECT', 'sentences_with_ERROR', 'sentences_with_CORRECT', 'TESTABLE', 'reportable_30_30', 'label_counts', 'strata'], 'note': 'SEARCH-ONLY labels (D9): no CORRECT class exists until the gloss step runs, so AUROC is NOT_TESTABLE; the ERROR_CERT class alone supports recall-type analyses; MAPPED rows are UNRESOLVED_GLOSS_NOT_RUN', 'seen_iter3_subset': ['population', 'n_rows', 'n_ERROR', 'n_CORRECT', 'sentences_with_ERROR', 'sentences_with_CORRECT', 'TESTABLE', 'reportable_30_30', 'label_counts', 'strata'], 'search_provisional_view': ['definition', 'all_rows', 'untouched_subset', 'contamination']}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [19] TOOL CALL — Bash · 2026-09-25 13:10:49 UTC

```
Build stratified mini_demo_data.json:
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5 python3 - <<'EOF'
import json, os, random
from collections import defaultdict
W=os.environ['W']
def jl(p): return [json.loads(l) for l in open(p) if l.strip()]
rnd=random.Random(0)
def strat(rows, key, n):
    b=defaultdict(list)
    for r in rows: b[key(r)].append(r)
    for v in b.values(): rnd.shuffle(v)
    out=[]; ks=sorted(b)
    while len(out)<n and any(b.values()):
        for k in ks:
            if b[k] and len(out)<n: out.append(b[k].pop())
    return out
free=jl(f'{W}/results/free_labels_v2.jsonl')
free_s=strat(free, lambda r:(r['label'],r['family']), 60)
gate=json.load(open(f'{W}/results/gate_items.json'))
gate_s=strat(gate, lambda i:(i['class'],i['half']), 20)
sig=jl(f'{W}/results/sig_replay_rows.jsonl')
sig_s=strat(sig, lambda r:(r['rename'],r['sig_label'],r['search_status']), 20)
sents=json.load(open(f'{W}/work/sentences.json'))
sents_s={r['sentence_id']:sents[r['sentence_id']] for r in sig_s}
seal=json.load(open(f'{W}/results/seal.json'))
t=json.load(open(f'{W}/results/testability_FREE_v2.json'))
keep=("n_ERROR","n_CORRECT","TESTABLE","label_counts")
t_s={"all_rows":{k:t["all_rows"][k] for k in keep},"untouched_subset":{k:t["untouched_subset"][k] for k in keep},
     "search_provisional_view":{k:{"TESTABLE":t["search_provisional_view"][k]["TESTABLE"]} for k in ("all_rows","untouched_subset")}}
out={"description":"Curated demo subset of the raw inputs read by data.py/src/build_output.py (art_Ia_FT284H33j): 60 FREE label rows (stratified over label x model family), 20 gloss-gate items (class x half), 20 SIG replay rows (rename x label x search status) + the sentences they need, the label seal and testability summary of the FULL dataset.",
 "free_labels_v2":free_s,"gate_items":gate_s,"sig_replay_rows":sig_s,"sentences":sents_s,
 "seal":{"seals":[seal["seals"][-1]]},"testability_FREE_v2":t_s}
json.dump(out,open('mini_demo_data.json','w'),ensure_ascii=False)
from collections import Counter
print(Counter(r['label'] for r in free_s)); print(Counter(r['family'] for r in free_s)); print(Counter(i['class'] for i in gate_s)); print(Counter((r['rename'],r['sig_label'],r['search_status']) for r in sig_s))
EOF
ls -la mini_demo_data.json
```

### [20] TOOL RESULT — Bash · 2026-09-25 13:10:49 UTC

```
{"stdout": "Counter({'ERROR_CERT': 20, 'UNPARSEABLE': 18, 'UNRESOLVED_GLOSS_NOT_RUN': 18, 'NO_OUTPUT': 4})\nCounter({'meta': 8, 'qwen': 8, 'cohere': 7, 'deepseek': 7, 'google-gemini': 6, 'google-gemma': 6, 'microsoft': 6, 'mistral': 6, 'openai': 6})\nCounter({'NO_DONOR': 4, 'NO_MERGE': 4, 'NO_NONCE': 4, 'NO_ROLE': 2, 'YES_FORM': 2, 'YES_IDENT': 2, 'YES_SYN': 2})\nCounter({('nonce', 'CORRECT', 'MAPPED'): 3, ('nonce', 'ERROR', 'ERROR_CERT'): 3, ('nonce', 'ERROR', 'MAPPED'): 3, ('nonce', 'READING_CHOICE', 'MAPPED'): 3, ('syn', 'CORRECT', 'MAPPED'): 2, ('syn', 'ERROR', 'ERROR_CERT'): 2, ('syn', 'ERROR', 'MAPPED'): 2, ('syn', 'READING_CHOICE', 'MAPPED'): 2})\n-rw-r--r-- 1 root root 212016 Sep 25 13:10 mini_demo_data.json", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [21] TOOL CALL — Bash · 2026-09-25 13:12:09 UTC

```
Generate code_demo.ipynb:
cat > /tmp/claude-0/-ai-inventor-aii-data-runs-run-qck1d05BqxkX-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-4-art-Ia-FT284H33j/5d0cec99-18d7-49eb-816d-46db335ac1b7/scratchpad/mk.py <<'PYEOF'
import json
cells=[]
def md(s): cells.append({"cell_type":"markdown","metadata":{},"source":s.strip("\n")})
def code(s): cells.append({"cell_type":"code","metadata":{},"execution_count":None,"outputs":[],"source":s.strip("\n")})

md(r'''
# Name-free labels for free-vocabulary NL→FOL translations: dataset builder demo

This notebook is a runnable walk-through of **`data.py`**, the script that packages the **T7b name-free label dataset** (`full_data_out.json`, `exp_sel_data_out` format). The dataset supports gold-free faithfulness metrics for natural-language → first-order-logic (NL→FOL) translation.

**Where the labels come from.** Ten LLM slots from 9 model families translated 221 templated rule sentences into FOL. Each model could name its predicates freely (FREE condition). The model's predicate names never match the template's reference vocabulary, so ordinary "equivalent to the gold formula" labelling does not apply. Each candidate was therefore labelled by an **exhaustive, certificate-backed, name-free map search** (`src/freelab.py`):
- the search enumerates every injective map from candidate symbols to template atoms, including reification (B1/B2), merge (B3), split (B4) and lexical-negation (B5) bridges;
- sound z3 relevance/polarity checks and 128-model finite countermodel fingerprints prune the search;
- z3 then checks equivalence for every surviving map.

A candidate with **no** equivalent map is `ERROR_CERT` (a certified error, relative to the map family). A candidate with at least one z3-equivalent map is `UNRESOLVED_GLOSS_NOT_RUN`: it still needs an LLM *gloss check* (does each mapped symbol actually mean the template atom?). That check could not run because the run's API budget was exhausted (deviation **D9**).

`data.py` assembles three groups:

| group | rows (full) | what it is |
|---|---|---|
| `rcomp_free_labels` | 2,652 | one row per FREE generation: (text, candidate FOL) → name-free label + map certificate + strata |
| `gloss_gate_items` | 840 | known-answer (symbol use, meaning) items, 7 classes × 120, halves A/B, for validating the gloss checker |
| `sig_soundness_replay` | 4,280 | 2,140 fixed-vocabulary (SIG) rows renamed with nonce/synonym names, with known pure-z3 labels, for testing the soundness of the name-free search |

The notebook runs the **original assembly code** from `data.py` and `src/build_output.py` with minimal changes. It reads a curated subset of the raw inputs from `mini_demo_data.json` (60 FREE rows, 20 gate items and 20 SIG rows, stratified), not from `results/*.jsonl`. The seal and testability summary come from the full dataset.
''')

code(r'''
import subprocess, sys
def _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])

# loguru — NOT on Colab, always install (data.py's only dependency)
_pip('loguru==0.7.3')

# pandas, matplotlib — pre-installed on Colab, install locally only (used for the results/visualization cells)
if 'google.colab' not in sys.modules:
    _pip('numpy==2.0.2', 'pandas==2.2.2', 'matplotlib==3.10.0')
''')

md(r'''
## Imports and logging setup

This is the import and logger block from `data.py`, unchanged except that `ROOT` is the notebook's working directory (a notebook has no `__file__`). The `sys.path` inserts for `src/` and `vendor/` are dropped because the functions they provided are copied into cells below. `json` and `Path` stand in for the imports of `src/common.py`. `pandas` and `matplotlib` are added for the results cells.
''')

code(r'''
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path.cwd()  # original: Path(__file__).resolve().parent

from loguru import logger  # noqa: E402

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
(ROOT / "logs").mkdir(exist_ok=True)
logger.add(ROOT / "logs" / "data.log", rotation="30 MB", level="DEBUG")

# extra imports for the notebook's summary/visualization cells
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
''')

md(r'''
## Load the demo data

The curated inputs are fetched from GitHub. If that fails (for example before the repository is published), the notebook falls back to a local `mini_demo_data.json`.
''')

code(r'''
GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/fork/run_qck1d05BqxkX/round-4/dataset-5/demo/mini_demo_data.json"
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
print({k: len(v) for k, v in data.items() if isinstance(v, (list, dict)) and k != "description"})
''')

md(r'''
## Configuration

`data.py` has only one fixed setting: `SELECTED`, the groups written to the output. The row limits below are notebook additions. They cap how many rows of each raw input are packaged. The originals had no cap: 2,652 FREE rows, 840 gate items and 4,280 SIG replay rows from `results/`. The demo file holds 60 / 20 / 20. `None` means "use every row in the loaded demo data".
''')

code(r'''
SELECTED = ["rcomp_free_labels", "gloss_gate_items", "sig_soundness_replay"]

# rows taken from each raw input (original: all rows of results/free_labels_v2.jsonl (2,652),
# results/gate_items.json (840), results/sig_replay_rows.jsonl (4,280)); None = all rows in mini_demo_data.json
N_FREE = None
N_GATE = None
N_SIG = None
''')

md(r'''
## Group 1: `rcomp_free_labels`, one row per FREE generation

This is `free_group()` from `src/build_output.py`. Each example's `input` is a JSON string holding the sentence, the candidate FOL and the generating system, family, slot and prompt variant. Its `output` is the name-free label:

- `ERROR_CERT`: no map in the declared family makes the candidate z3-equivalent to any template reading. The label is final, with certificate counts such as `count_prune_subtree` (subtrees pruned by a certified finite countermodel) and `no_polarity_compatible_target`.
- `UNRESOLVED_GLOSS_NOT_RUN`: at least one z3-equivalent map exists (`map_certificate` lists it). The gloss check that decides CORRECT vs ERROR is pending.
- `UNPARSEABLE` / `NO_OUTPUT`: coverage failures. They are kept as rows, not dropped.

`label_binary_search_provisional` collapses these to ERROR / MAPPED / EXCLUDED. The only change from the original is the input source: rows come from `data["free_labels_v2"]` instead of `load_jsonl(RES / "free_labels_v2.jsonl")`.
''')

code(r'''
def md(d: dict) -> dict:
    return {f"metadata_{k}": v for k, v in d.items()}


def free_group() -> dict:
    rows = data["free_labels_v2"][:N_FREE]  # original: load_jsonl(RES / "free_labels_v2.jsonl")
    ex = []
    for r in rows:
        inp = {"text": r["text"], "candidate_fol": r["candidate_fol"], "system": r["system"], "family": r["family"],
               "slot": r["slot"], "prompt_variant": r["prompt_variant"], "condition": "FREE", "template_id": r["template_id"]}
        search_bin = {"ERROR_CERT": "ERROR", "UNRESOLVED_GLOSS_NOT_RUN": "MAPPED"}.get(r["label"], "EXCLUDED")
        meta = {
            "row_key": r["row_key"], "item_id": r["item_id"], "sentence_id": r["sentence_id"], "template_id": r["template_id"],
            "clause_type": r["clause_type"], "words": r["words"], "word_tercile": r["word_tercile"],
            "nconds_weak": r["nconds_weak"], "negated_condition": r["negated_condition"], "nested": r["nested"],
            "label_binary": r["label_binary"], "label_binary_search_provisional": search_bin,
            "label_source": r["label_source"], "search_status": r.get("search_status"),
            "matched_reading": r.get("matched_reading") or r.get("matched_reading_search"),
            "map_certificate": r.get("map_certificate"),
            "n_maps_enumerated": r.get("n_maps_enumerated"), "n_maps_fingerprint_pass": r.get("n_maps_fingerprint_pass"),
            "n_equiv_maps": r.get("n_equiv_maps"), "n_equiv_map_orbits": r.get("n_equiv_map_orbits"),
            "nonequiv_certificate_type_counts": r.get("nonequiv_certificate_type_counts"),
            "gloss_pairs": r.get("gloss_pairs"), "gloss_decision": r.get("gloss_decision"),
            "unresolved_reason": r.get("unresolved_reason"), "irrelevant_symbols": r.get("irrelevant_symbols"),
            "search_secs": r.get("search_secs"), "seen_iter3": r.get("seen_iter3"),
            "old_label_iter3": r.get("old_label_iter3"), "fold": "RCOMP_FREE"}
        ex.append({"input": json.dumps(inp, ensure_ascii=False), "output": r["label"], **md(meta)})
    return {"dataset": "rcomp_free_labels", "examples": ex}
''')

md(r'''
## Group 2: `gloss_gate_items`, known-answer items for the gloss checker

This is `gate_group()`. Each item asks: "in this sentence, does candidate atom `A` mean `proposed_meaning`?" The gold answer is YES or NO. There are 7 classes:
- YES classes: identical wording (`YES_IDENT`), synonym (`YES_SYN`), different surface form (`YES_FORM`);
- NO classes: nonce name (`NO_NONCE`), meaning taken from another atom (`NO_DONOR`), swapped role (`NO_ROLE`), two atoms merged (`NO_MERGE`).

A gloss checker must pass these items before its verdicts can turn MAPPED rows into CORRECT or ERROR. The Haiku and Qwen verdicts are still `null` because of deviation D9. Only the input source changed.
''')

code(r'''
def gate_group() -> dict:
    items = data["gate_items"][:N_GATE]  # original: json.loads((RES / "gate_items.json").read_text())
    ex = []
    for i in items:
        inp = {"sentence": i["sentence"], "candidate_atom": i["candidate_atom"], "proposed_meaning": i["proposed_meaning"]}
        meta = {"item_id": i["item_id"], "class": i["class"], "half": i["half"], "sentence_id": i["sentence_id"],
                "template_id": i["template_id"], "note": i["note"], "prompt_version": "gloss_v1",
                "haiku_verdict": i.get("haiku_gloss_v1"), "qwen_verdict": i.get("qwen_gloss_v1"), "fold": "GLOSS_GATE"}
        ex.append({"input": json.dumps(inp, ensure_ascii=False), "output": i["gold"], **md(meta)})
    return {"dataset": "gloss_gate_items", "examples": ex}
''')

md(r'''
## Group 3: `sig_soundness_replay`, renamed SIG rows with known labels

This is `sig_group()`. The SIG condition used the template's own vocabulary, so its labels are pure z3 (equivalent to a template reading or not). Each SIG candidate is renamed twice, with **nonce** names (`Buzil`, `Getoz`, …) and with **synonyms**, and the name-free search is re-run on it. The known labels expose:
- *false ERROR_CERT*: the search certifies an error on a row known to be CORRECT (0/1,595 in the full data);
- *identity-map recovery*: the search finds the true renaming back to the template vocabulary (100%);
- *rescue*: known errors that some non-identity map makes equivalent (9–10%). The gloss check has to catch these.

`sentences` supplies the text for each `sentence_id`. Only the two input sources changed.
''')

code(r'''
def sig_group() -> dict:
    sents = data["sentences"]  # original: json.loads((WORK / "sentences.json").read_text())
    rows = data["sig_replay_rows"][:N_SIG]  # original: load_jsonl(RES / "sig_replay_rows.jsonl")
    ex = []
    for r in rows:
        inp = {"text": sents[r["sentence_id"]]["text"], "candidate_fol": r["renamed_fol"], "rename": r["rename"],
               "template_id": r["template_id"]}
        meta = {k: r[k] for k in ("row_key", "sentence_id", "slot", "template_id", "sig_matched_reading", "canon_fol",
                                  "search_status", "identity_map_found", "non_identity_map_found", "n_equiv_maps",
                                  "n_equiv_map_orbits", "n_maps_enumerated", "nonequiv_certificate_type_counts",
                                  "oracle_end_to_end_label", "in_e2e_gloss_subsample_300", "e2e_gloss_label")}
        meta["map_equiv_found"] = r["search_status"] in ("MAPPED", "READING_CHOICE")
        meta["fold"] = f"SIG_REPLAY_{r['rename'].upper()}"
        ex.append({"input": json.dumps(inp, ensure_ascii=False), "output": r["sig_label"], **md(meta)})
    return {"dataset": "sig_soundness_replay", "examples": ex}
''')

md(r'''
## Assemble `full_data_out.json`, as in `data.py`'s `main()`

This cell builds the three groups and runs the original schema assertions: string `input`/`output`, and no reserved `split`/`dataset`/`context` keys. It then attaches the label **seal** (a sha256 of the full label vector, recorded under a hashed pre-registration) and the testability summary, and writes the JSON. The only change from the original is the source of `seal` and `t` (the loaded data instead of `results/*.json`). The seal and testability numbers describe the **full** 2,652-row dataset. The examples are the demo subset.
''')

code(r'''
@logger.catch(reraise=True)
def main() -> None:
    groups = [free_group(), gate_group(), sig_group()]
    for g in groups:
        assert g["examples"], g["dataset"]
        for e in g["examples"]:
            assert isinstance(e["input"], str) and isinstance(e["output"], str), g["dataset"]
            assert not ({"split", "dataset", "context"} & set(e)), g["dataset"]
    seal = data["seal"]["seals"][-1]  # original: json.loads((ROOT / "results" / "seal.json").read_text())["seals"][-1]
    t = data["testability_FREE_v2"]  # original: json.loads((ROOT / "results" / "testability_FREE_v2.json").read_text())
    out = {"metadata": {
        "artifact": "T7b name-free labels for free-vocabulary rule translations (run_u75jRHUss0zo, iter 4, gen_art_dataset_5)",
        "workspace": str(ROOT),
        "selection": ("the three plan groups (chosen as best 3 of 6 standardised candidates; folio / malls_test / "
                      "logicnli_test were context only: no multi-system candidates, ~36-39% wrong gold, or no FOL; their "
                      "standardised record is temp/candidates_data_out.json)"),
        "label_mode": seal["mode"],
        "status_note": ("SEARCH-ONLY labels: the paid gloss step could not run (deviation D9: run OpenRouter budget "
                        "exhausted before this artifact's first call; re-probed at packaging, still HTTP 403). ERROR_CERT is "
                        "final and certificate-backed; MAPPED rows are UNRESOLVED_GLOSS_NOT_RUN until src/resume_gloss.py "
                        "runs. metadata_label_binary_search_provisional (ERROR vs MAPPED) is a provisional view with audited "
                        "contamination (results/soundness_audit.json)."),
        "seal_all_rows_sha256": seal["label_vector_sha256_all_rows"],
        "seal_untouched_sha256": seal.get("label_vector_sha256_untouched"),
        "prereg_sha256": seal["prereg_sha256"],
        "testability_all_rows": {k: t["all_rows"][k] for k in ("n_ERROR", "n_CORRECT", "TESTABLE", "label_counts")},
        "testability_untouched": {k: t["untouched_subset"][k] for k in ("n_ERROR", "n_CORRECT", "TESTABLE", "label_counts")},
        "provisional_view_testable": {k: t["search_provisional_view"][k]["TESTABLE"] for k in ("all_rows", "untouched_subset")},
    }, "datasets": [g for g in groups if g["dataset"] in SELECTED]}
    (ROOT / "full_data_out.json").write_text(json.dumps(out, ensure_ascii=False))
    logger.info(f"full_data_out.json: {[(g['dataset'], len(g['examples'])) for g in out['datasets']]}")


main()
''')

md(r'''
## Results

The output file is read back and summarised:
1. dataset-level metadata: seal, testability, and why AUROC is not yet testable;
2. one worked example of each FREE label kind, including the z3-equivalent map certificate of a MAPPED row;
3. label distributions: demo subset vs full dataset, labels per model family, gate classes, and SIG-replay soundness.
''')

code(r'''
out = json.loads((ROOT / "full_data_out.json").read_text())
M = out["metadata"]
print("label_mode:", M["label_mode"], "| seal (all rows):", M["seal_all_rows_sha256"][:16], "...",
      "| seal (untouched):", str(M["seal_untouched_sha256"])[:16], "...")
print("full-data testability (ERROR vs CORRECT):", M["testability_all_rows"]["TESTABLE"],
      f"(n_ERROR={M['testability_all_rows']['n_ERROR']}, n_CORRECT={M['testability_all_rows']['n_CORRECT']})")
print("provisional ERROR-vs-MAPPED view testable:", M["provisional_view_testable"])
print()

G = {g["dataset"]: g["examples"] for g in out["datasets"]}
free = G["rcomp_free_labels"]
for lab in ["ERROR_CERT", "UNRESOLVED_GLOSS_NOT_RUN", "UNPARSEABLE", "NO_OUTPUT"]:
    e = next((x for x in free if x["output"] == lab), None)
    if e is None:
        continue
    inp = json.loads(e["input"])
    print(f"=== {lab}  [{inp['system']}, template {inp['template_id']}, {e['metadata_words']} words]")
    print("TEXT :", inp["text"])
    print("FOL  :", inp["candidate_fol"] or "<none>")
    if e["metadata_map_certificate"]:
        c = e["metadata_map_certificate"]
        print(f"CERT : {c['status']} (reading={c['reading']}, bridges={c['bridges']})")
        for m in c["map"]:
            print("       ", m)
    if e["metadata_nonequiv_certificate_type_counts"]:
        print("non-equivalence certificates:", e["metadata_nonequiv_certificate_type_counts"])
    print()
''')

code(r'''
full_counts = M["testability_all_rows"]["label_counts"]
demo_counts = Counter(x["output"] for x in free)
labs = list(full_counts)
tbl = pd.DataFrame({"full (n=%d)" % sum(full_counts.values()): [full_counts[l] for l in labs],
                    "demo (n=%d)" % len(free): [demo_counts.get(l, 0) for l in labs]}, index=labs)
print("FREE label counts\n", tbl.to_string(), "\n")

fam = pd.crosstab([json.loads(x["input"])["family"] for x in free], [x["output"] for x in free])
print("FREE labels per model family (demo)\n", fam.to_string(), "\n")

gate = G["gloss_gate_items"]
print("Gloss-gate items (demo)\n", pd.crosstab([x["metadata_class"] for x in gate], [x["output"] for x in gate]).to_string(), "\n")

sig = G["sig_soundness_replay"]
sig_df = pd.DataFrame({"rename": [json.loads(x["input"])["rename"] for x in sig],
                       "known_label": [x["output"] for x in sig],
                       "search_status": [x["metadata_search_status"] for x in sig],
                       "identity_map_found": [any(x["metadata_identity_map_found"].values()) for x in sig]})
print("SIG replay: known pure-z3 label vs name-free search outcome (demo)\n",
      pd.crosstab([sig_df.rename, sig_df.known_label], sig_df.search_status).to_string())
n_corr = (sig_df.known_label == "CORRECT").sum()
false_err = ((sig_df.known_label == "CORRECT") & (sig_df.search_status == "ERROR_CERT")).sum()
print(f"\nfalse ERROR_CERT on known-CORRECT rows: {false_err}/{n_corr}; "
      f"identity map recovered on known-CORRECT rows: {sig_df[sig_df.known_label=='CORRECT'].identity_map_found.sum()}/{n_corr}")
''')

code(r'''
fig, axes = plt.subplots(1, 3, figsize=(16, 4.5))

frac = tbl / tbl.sum()
frac.plot.bar(ax=axes[0], color=["#4C72B0", "#DD8452"], rot=20)
axes[0].set_title("FREE label distribution: full vs demo")
axes[0].set_ylabel("fraction of rows")
axes[0].tick_params(axis="x", labelsize=8)

fam.reindex(columns=labs, fill_value=0).plot.barh(stacked=True, ax=axes[1],
    color=["#C44E52", "#8172B3", "#937860", "#8C8C8C"])
axes[1].set_title("FREE labels per model family (demo)")
axes[1].set_xlabel("rows")
axes[1].legend(fontsize=7)

ct = pd.crosstab(sig_df.known_label, sig_df.search_status)
ct.plot.bar(ax=axes[2], rot=0, color=["#C44E52", "#55A868"][:ct.shape[1]])
axes[2].set_title("SIG replay: known label vs search outcome (demo)")
axes[2].set_ylabel("rows")

plt.tight_layout()
plt.show()
''')

md(r'''
**How to read this.** `ERROR_CERT` rows are final errors relative to the declared map family. They are the only label class that exists until the gloss check runs, so an ERROR-vs-CORRECT AUROC is **NOT_TESTABLE** for now. The provisional ERROR-vs-MAPPED split is testable, but an executor audit put about 13% contamination on each side.

In the SIG replay, the search should never certify an error on a known-CORRECT row. Known-ERROR rows that land in `MAPPED` are "rescues" by non-identity maps, which the pending gloss check has to reject.

To rebuild the real dataset, run `uv run data.py` inside the artifact workspace. It reads all 2,652 / 840 / 4,280 rows from `results/`. Once API budget is available, `src/resume_gloss.py` turns the MAPPED rows into final CORRECT/ERROR labels.
''')

nb={"cells":cells,"metadata":{"kernelspec":{"display_name":"Python 3","language":"python","name":"python3"},"language_info":{"name":"python"}},"nbformat":4,"nbformat_minor":5}
for i,c in enumerate(nb["cells"]): c["id"]=f"c{i:02d}"
json.dump(nb,open("code_demo.ipynb","w"),indent=1,ensure_ascii=False)
PYEOF
python3 /tmp/claude-0/-ai-inventor-aii-data-runs-run-qck1d05BqxkX-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-4-art-Ia-FT284H33j/5d0cec99-18d7-49eb-816d-46db335ac1b7/scratchpad/mk.py && echo ok
```

### [22] TOOL RESULT — Bash · 2026-09-25 13:12:09 UTC

```
{"stdout": "ok", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [23] TOOL CALL — Bash · 2026-09-25 13:12:15 UTC

```
Set config to minimum values:
sed -i 's/^N_FREE = None/N_FREE = 2/; s/^N_GATE = None/N_GATE = 2/; s/^N_SIG = None/N_SIG = 2/' code_demo.ipynb; grep -c '"N_FREE = 2' code_demo.ipynb; python3 -c "import json;[print(c['source'][-60:]) for c in json.load(open('code_demo.ipynb'))['cells'] if 'N_SIG =' in ''.join(c['source'])]"
```

### [24] TOOL RESULT — Bash · 2026-09-25 13:12:15 UTC

```
{"stdout": "0\nmini_demo_data.json\nN_FREE = None\nN_GATE = None\nN_SIG = None", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [25] TOOL CALL — Bash · 2026-09-25 13:12:23 UTC

```
Test-run notebook with minimum config:
cat > setn.py <<'EOF'
import json,sys
v=sys.argv[1]; nb=json.load(open('code_demo.ipynb'))
import re
for c in nb['cells']:
    if c['cell_type']=='code' and 'N_SIG =' in c['source']:
        c['source']=re.sub(r'^(N_(FREE|GATE|SIG)) = \S+', lambda m:f'{m.group(1)} = {v}', c['source'], flags=re.M)
json.dump(nb,open('code_demo.ipynb','w'),indent=1,ensure_ascii=False)
EOF
python3 setn.py 2 && E=/tmp/aii_nb_test_envs/art_Ia_FT284H33j-af39a9391776 && UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 $E && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python $E/bin/python jupyter ipykernel && time $E/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -5
```

### [26] TOOL RESULT — Bash · 2026-09-25 13:12:45 UTC

```
{"stdout": "\u001b[36mFile \u001b[39m\u001b[32mpandas/_libs/hashtable_class_helper.pxi:7195\u001b[39m, in \u001b[36mpandas._libs.hashtable.PyObjectHashTable._unique\u001b[39m\u001b[34m()\u001b[39m\n\u001b[32m-> \u001b[39m\u001b[32m7195\u001b[39m \u001b[33m'Could not get source, probably due dynamically evaluated source code.'\u001b[39m\n\n\u001b[31mTypeError\u001b[39m: unhashable type: 'Series'\n\n\nreal\t0m19.446s\nuser\t0m16.126s\nsys\t0m1.245s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [27] TOOL CALL — Bash · 2026-09-25 13:12:51 UTC

```
Fix rename bug and re-test:
S=/tmp/claude-0/-ai-inventor-aii-data-runs-run-qck1d05BqxkX-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-4-art-Ia-FT284H33j/5d0cec99-18d7-49eb-816d-46db335ac1b7/scratchpad/mk.py && sed -i 's/\[sig_df\.rename, sig_df\.known_label\]/[sig_df["rename"], sig_df.known_label]/' $S && grep -c 'sig_df\["rename"\]' $S && python3 $S && python3 setn.py 2 && E=/tmp/aii_nb_test_envs/art_Ia_FT284H33j-af39a9391776 && UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 $E && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python $E/bin/python jupyter ipykernel && time $E/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -5
```

### [28] TOOL RESULT — Bash · 2026-09-25 13:13:15 UTC

```
{"stdout": "1\n[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n[IPKernelApp] WARNING | Kernel is running over TCP without encryption. All communication (including code and outputs) is sent in plain text and is susceptible to eavesdropping. Use IPC transport or launch with kernel manager-provisioned CurveZMQ keys to enable transport encryption.\n[NbConvertApp] Writing 112566 bytes to code_demo.ipynb\n\nreal\t0m21.052s\nuser\t0m17.659s\nsys\t0m1.405s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [29] ASSISTANT · 2026-09-25 13:13:19 UTC

```
Minimum config passes (~21 s). Scaling to the full demo subset (60/20/20) and re-testing.
```

### [30] TOOL CALL — Bash · 2026-09-25 13:13:19 UTC

```
Run notebook with all demo rows and show outputs:
python3 setn.py None && E=/tmp/aii_nb_test_envs/art_Ia_FT284H33j-af39a9391776 && UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 $E && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python $E/bin/python jupyter ipykernel && time $E/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -2; python3 -c "
import json
for c in json.load(open('code_demo.ipynb'))['cells']:
  if c['cell_type']=='code':
    for o in c['outputs']:
      if o.get('output_type')=='error': print('ERR',o['ename'])
      if 'text' in o: print(''.join(o['text'])[:3500]); print('----')
      if 'data' in o and 'image/png' in o['data']: print('[image]')
"
```

### [31] TOOL RESULT — Bash · 2026-09-25 13:13:43 UTC

```
{"stdout": "[IPKernelApp] WARNING | Kernel is running over TCP without encryption. All communication (including code and outputs) is sent in plain text and is susceptible to eavesdropping. Use IPC transport or launch with kernel manager-provisioned CurveZMQ keys to enable transport encryption.\n[NbConvertApp] Writing 112566 bytes to code_demo.ipynb\n\nreal\t0m20.620s\nuser\t0m17.284s\nsys\t0m1.422s\nCurated demo subset of the raw inputs read by data.py/src/build_output.py (art_Ia_FT284H33j): 60 FREE label rows (stratified over label x model family), 20 gloss-gate items (class x half), 20 SIG replay rows (rename x label x search status) + the sentences they need, the label seal and testability summary of the FULL dataset.\n{'free_labels_v2': 60, 'gate_items': 20, 'sig_replay_rows': 20, 'sentences': 18, 'seal': 1, 'testability_FREE_v2': 3}\n\n----\n13:13:39|INFO   |full_data_out.json: [('rcomp_free_labels', 2), ('gloss_gate_items', 2), ('sig_soundness_replay', 2)]\n\n----\nlabel_mode: search_only | seal (all rows): 9609ebbb725832c4 ... | seal (untouched): b364a49a8e21835d ...\nfull-data testability (ERROR vs CORRECT): False (n_ERROR=759, n_CORRECT=0)\nprovisional ERROR-vs-MAPPED view testable: {'all_rows': True, 'untouched_subset': True}\n\n=== ERROR_CERT  [G9:cohere/command-r7b-12-2024, template T8, 29 words]\nTEXT : If a vaccine receives voice and data, is used for drinking, and emits light, then the vaccine is designed for high-performance calculations, but only if the vaccine preserves food.\nFOL  : (∀x (Receive(x, voice, data) ∧ Use(x, drinking) ∧ Emit(x, light) → Design(x, highPerformanceCalculations))) ↔ (∀x (Preserve(x, food) → Design(x, highPerformanceCalculations)))\nnon-equivalence certificates: {'no_polarity_compatible_target': 6}\n\n\n----\nFREE label counts\n                           full (n=2652)  demo (n=2)\nERROR_CERT                          759           2\nUNRESOLVED_GLOSS_NOT_RUN           1506           0\nUNPARSEABLE                         188           0\nNO_OUTPUT                           199           0 \n\nFREE labels per model family (demo)\n col_0     ERROR_CERT\nrow_0               \ncohere             1\ndeepseek           1 \n\nGloss-gate items (demo)\n col_0     NO\nrow_0       \nNO_DONOR   2 \n\nSIG replay: known pure-z3 label vs name-free search outcome (demo)\n search_status       ERROR_CERT  MAPPED\nrename known_label                    \nnonce  CORRECT               0       1\n       ERROR                 1       0\n\nfalse ERROR_CERT on known-CORRECT rows: 0/1; identity map recovered on known-CORRECT rows: 1/1\n\n----\n[image]", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [32] TOOL CALL — Bash · 2026-09-25 13:13:49 UTC

```
Check config cell contents:
python3 -c "
import json;[print(repr(c['source'][-80:])) for c in json.load(open('code_demo.ipynb'))['cells'] if 'N_SIG =' in c['source']]"
```

### [33] TOOL RESULT — Bash · 2026-09-25 13:13:49 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [34] TOOL CALL — Bash · 2026-09-25 13:13:59 UTC

```
Fix config setter, reorder rows, label crosstabs:
sed -i "s/^    if c\['cell_type'\]=='code' and 'N_SIG =' in c\['source'\]:/    c['source']=''.join(c['source'])\n    if c['cell_type']=='code' and 'N_SIG =' in c['source']:/" setn.py && cat setn.py && python3 - <<'EOF'
# reorder FREE rows round-robin by label (and gate/sig by class) so any prefix N_* is diverse
import json
from collections import defaultdict
d=json.load(open('mini_demo_data.json'))
def rr(rows,key):
    b=defaultdict(list)
    for r in rows: b[key(r)].append(r)
    out=[]; ks=sorted(b)
    while any(b.values()):
        for k in ks:
            if b[k]: out.append(b[k].pop(0))
    return out
d['free_labels_v2']=rr(d['free_labels_v2'],lambda r:r['label'])
d['gate_items']=rr(d['gate_items'],lambda r:r['gold'])
d['sig_replay_rows']=rr(d['sig_replay_rows'],lambda r:r['sig_label'])
print([r['label'] for r in d['free_labels_v2'][:6]],[r['sig_label'] for r in d['sig_replay_rows'][:4]])
json.dump(d,open('mini_demo_data.json','w'),ensure_ascii=False)
EOF
S=/tmp/claude-0/-ai-inventor-aii-data-runs-run-qck1d05BqxkX-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-4-art-Ia-FT284H33j/5d0cec99-18d7-49eb-816d-46db335ac1b7/scratchpad/mk.py
python3 - "$S" <<'EOF'
import sys; p=sys.argv[1]; s=open(p).read()
s=s.replace('[x["output"] for x in free])\n','[x["output"] for x in free], rownames=["family"], colnames=["label"])\n')
s=s.replace('[x["output"] for x in gate]).to_string()','[x["output"] for x in gate], rownames=["class"], colnames=["gold"]).to_string()')
open(p,'w').write(s); print(s.count('rownames'))
EOF
python3 $S && python3 setn.py None && python3 -c "
import json;[print(''.join(c['source'])[-50:]) for c in json.load(open('code_demo.ipynb'))['cells'] if 'N_SIG =' in ''.join(c['source'])]"
```

### [35] TOOL RESULT — Bash · 2026-09-25 13:13:59 UTC

```
{"stdout": "import json,sys\nv=sys.argv[1]; nb=json.load(open('code_demo.ipynb'))\nimport re\nfor c in nb['cells']:\n    c['source']=''.join(c['source'])\n    if c['cell_type']=='code' and 'N_SIG =' in c['source']:\n        c['source']=re.sub(r'^(N_(FREE|GATE|SIG)) = \\S+', lambda m:f'{m.group(1)} = {v}', c['source'], flags=re.M)\njson.dump(nb,open('code_demo.ipynb','w'),indent=1,ensure_ascii=False)\n['ERROR_CERT', 'NO_OUTPUT', 'UNPARSEABLE', 'UNRESOLVED_GLOSS_NOT_RUN', 'ERROR_CERT', 'NO_OUTPUT'] ['CORRECT', 'ERROR', 'READING_CHOICE', 'CORRECT']\n2\ndata.json\nN_FREE = None\nN_GATE = None\nN_SIG = None", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [36] TOOL CALL — Bash · 2026-09-25 13:14:05 UTC

```
Scale runs N=10 then all rows:
E=/tmp/aii_nb_test_envs/art_Ia_FT284H33j-af39a9391776 && for N in 10 None; do python3 setn.py $N; UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 $E && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python $E/bin/python jupyter ipykernel && s=$(date +%s); $E/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -1; echo "N=$N took $(( $(date +%s)-s ))s"; done; python3 -c "
import json
for c in json.load(open('code_demo.ipynb'))['cells']:
  if c['cell_type']=='code':
    for o in c['outputs']:
      if o.get('output_type')=='error': print('ERR',o['ename'])
      if 'text' in o: print(''.join(o['text'])[:6000]); print('----')
      if 'data' in o and 'image/png' in o['data']: print('[image]')
"
```

### [37] TOOL RESULT — Bash · 2026-09-25 13:14:51 UTC

```
{"stdout": "[NbConvertApp] Writing 126906 bytes to code_demo.ipynb\nN=10 took 21s\n[NbConvertApp] Writing 132734 bytes to code_demo.ipynb\nN=None took 20s\nCurated demo subset of the raw inputs read by data.py/src/build_output.py (art_Ia_FT284H33j): 60 FREE label rows (stratified over label x model family), 20 gloss-gate items (class x half), 20 SIG replay rows (rename x label x search status) + the sentences they need, the label seal and testability summary of the FULL dataset.\n{'free_labels_v2': 60, 'gate_items': 20, 'sig_replay_rows': 20, 'sentences': 18, 'seal': 1, 'testability_FREE_v2': 3}\n\n----\n13:14:47|INFO   |full_data_out.json: [('rcomp_free_labels', 60), ('gloss_gate_items', 20), ('sig_soundness_replay', 20)]\n\n----\nlabel_mode: search_only | seal (all rows): 9609ebbb725832c4 ... | seal (untouched): b364a49a8e21835d ...\nfull-data testability (ERROR vs CORRECT): False (n_ERROR=759, n_CORRECT=0)\nprovisional ERROR-vs-MAPPED view testable: {'all_rows': True, 'untouched_subset': True}\n\n=== ERROR_CERT  [G9:cohere/command-r7b-12-2024, template T8, 29 words]\nTEXT : If a vaccine receives voice and data, is used for drinking, and emits light, then the vaccine is designed for high-performance calculations, but only if the vaccine preserves food.\nFOL  : (∀x (Receive(x, voice, data) ∧ Use(x, drinking) ∧ Emit(x, light) → Design(x, highPerformanceCalculations))) ↔ (∀x (Preserve(x, food) → Design(x, highPerformanceCalculations)))\nnon-equivalence certificates: {'no_polarity_compatible_target': 6}\n\n=== UNRESOLVED_GLOSS_NOT_RUN  [G9:cohere/command-r7b-12-2024, template T5, 31 words]\nTEXT : Each adult who is in our family and who attends yoga classes regularly spends money, provided that the adult has ample space, except if the adult is eligible for overtime pay.\nFOL  : ∀x ((Adult(x) ∧ In(x, ourFamily) ∧ AttendsYogaClasses(x, regularly) ∧ AmpleSpace(x)) → ¬EligibleForOvertimePay(x) → SpendsMoney(x))\nCERT : z3_equivalent_map_not_gloss_checked (reading=weak, bridges=['B1', 'B1'])\n        Adult(x) => Adult(x)\n        AmpleSpace(x) => AttendRegularly(x, yogaClass)\n        AttendsYogaClasses(x, regularly) => In(x, ourFamily)\n        EligibleForOvertimePay(x) => EligibleForOvertimePay(x)\n        In(x, ourFamily) => Have(x, ampleSpace)\n        SpendsMoney(x) => Spend(x, money)\nnon-equivalence certificates: {'count_prune_subtree': 291, 'no_polarity_compatible_target': 10}\n\n=== UNPARSEABLE  [G9:cohere/command-r7b-12-2024, template T6, 29 words]\nTEXT : Except if the penguin sleeps, each penguin that is in Antarctica and that feeds its offspring with milk is in a race, provided that the penguin is not injured.\nFOL  : ∀x ((In(x, antarctica) ∧ Penguin(x) ∧ Feeds(x, offspring, milk)) → (∀y (In(y, race) ↔ (Penguin(y) ∧ ¬Injury(y) ∧ ¬Sleeps(x))))\n\n=== NO_OUTPUT  [G1b:meta-llama/llama-3.3-70b-instruct, template T5, 26 words]\nTEXT : Every king who does not know about breath-first-search and who is uncomfortable is harmful, provided that the king loves the opera, unless the king is hardworking.\nFOL  : <none>\n\n\n----\nFREE label counts\n                           full (n=2652)  demo (n=60)\nERROR_CERT                          759           20\nUNRESOLVED_GLOSS_NOT_RUN           1506           18\nUNPARSEABLE                         188           18\nNO_OUTPUT                           199            4 \n\nFREE labels per model family (demo)\n label          ERROR_CERT  NO_OUTPUT  UNPARSEABLE  UNRESOLVED_GLOSS_NOT_RUN\nfamily                                                                     \ncohere                  3          0            2                         2\ndeepseek                3          0            2                         2\ngoogle-gemini           2          0            2                         2\ngoogle-gemma            2          0            2                         2\nmeta                    2          2            2                         2\nmicrosoft               2          0            2                         2\nmistral                 2          0            2                         2\nopenai                  2          0            2                         2\nqwen                    2          2            2                         2 \n\nGloss-gate items (demo)\n gold       NO  YES\nclass             \nNO_DONOR    4    0\nNO_MERGE    4    0\nNO_NONCE    4    0\nNO_ROLE     2    0\nYES_FORM    0    2\nYES_IDENT   0    2\nYES_SYN     0    2 \n\nSIG replay: known pure-z3 label vs name-free search outcome (demo)\n search_status          ERROR_CERT  MAPPED\nrename known_label                       \nnonce  CORRECT                  0       3\n       ERROR                    3       3\n       READING_CHOICE           0       3\nsyn    CORRECT                  0       2\n       ERROR                    2       2\n       READING_CHOICE           0       2\n\nfalse ERROR_CERT on known-CORRECT rows: 0/5; identity map recovered on known-CORRECT rows: 5/5\n\n----\n[image]", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [38] TOOL CALL — Bash · 2026-09-25 13:15:03 UTC

```
Add note, final test run, verify URL:
S=/tmp/claude-0/-ai-inventor-aii-data-runs-run-qck1d05BqxkX-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-4-art-Ia-FT284H33j/5d0cec99-18d7-49eb-816d-46db335ac1b7/scratchpad/mk.py && python3 - "$S" <<'EOF'
import sys; p=sys.argv[1]; s=open(p).read()
old="Known-ERROR rows that land in `MAPPED` are \"rescues\" by non-identity maps, which the pending gloss check has to reject."
new=old+"\n\nThe MAPPED worked example above shows why a z3-equivalent map alone is not enough. Its certificate sends `AmpleSpace(x)` to *attends yoga regularly* and `In(x, ourFamily)` to *has ample space*. The formula is logically equivalent under this map, but the map is lexically wrong, and the gloss check exists to reject it."
assert old in s; s=s.replace(old,new); open(p,'w').write(s)
EOF
python3 $S && python3 setn.py None && E=/tmp/aii_nb_test_envs/art_Ia_FT284H33j-af39a9391776 && UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 $E && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python $E/bin/python jupyter ipykernel && $E/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -1 && python3 -c "
import json,base64
nb=json.load(open('code_demo.ipynb'))
for c in nb['cells']:
  for o in c.get('outputs',[]):
    if o.get('output_type')=='error': print('ERR')
    if 'data' in o and 'image/png' in o['data']: open('$(dirname $S)/fig.png','wb').write(base64.b64decode(o['data']['image/png']))
"; grep -c 'GITHUB_DATA_URL = \"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/fork/run_qck1d05BqxkX/round-4/dataset-5/demo/mini_demo_data.json\"' code_demo.ipynb; rm -f setn.py
```

### [39] TOOL RESULT — Bash · 2026-09-25 13:15:25 UTC

```
{"stdout": "[NbConvertApp] Writing 133072 bytes to code_demo.ipynb\n0", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [40] TOOL CALL — Bash · 2026-09-25 13:15:27 UTC

```
Check URL string in notebook JSON:
grep -o 'GITHUB_DATA_URL = [^n]*' code_demo.ipynb | head -2; grep -c 'urlopen(GITHUB_DATA_URL)' code_demo.ipynb
```

### [41] TOOL RESULT — Bash · 2026-09-25 13:15:27 UTC

```
{"stdout": "GITHUB_DATA_URL = \\\"https://raw.githubuserco\n1", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [42] THINKING · 2026-09-25 13:15:35 UTC

```
The final run passed all demo rows (60/20/20) in ~20s, and the URL grep miss was just due to escaped quotes in the JSON. I'll verify the URL via the parsed notebook, check the figure, then write the README, manifest, and output JSON.
```

### [43] TOOL CALL — Bash · 2026-09-25 13:15:35 UTC

```
Verify exact URL and list workspace:
python3 -c "
import json; s=''.join(''.join(c['source']) for c in json.load(open('code_demo.ipynb'))['cells'])
print('GITHUB_DATA_URL = \"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/fork/run_qck1d05BqxkX/round-4/dataset-5/demo/mini_demo_data.json\"' in s)"; ls -la; du -sh .
```

### [44] TOOL RESULT — Bash · 2026-09-25 13:15:35 UTC

```
{"stdout": "True\ntotal 3932\ndrwxr-xr-x 4 root root 1082559 Sep 25 13:15 .\ndrwxr-xr-x 7 root root 2000430 Sep 25 13:13 ..\ndrwxr-xr-x 2 root root       1 Sep 25 13:09 .aii\n-rw------- 1 root root      54 Sep 25 13:09 .aii_claude_session.json\n-rw-r--r-- 1 root root  314333 Sep 25 13:15 .repl_agent.ptylog\n-rw-r--r-- 1 root root  133134 Sep 25 13:15 code_demo.ipynb\n-rw-r--r-- 1 root root  187599 Sep 25 13:15 full_data_out.json\ndrwxr-xr-x 2 root root   95100 Sep 25 13:12 logs\n-rw-r--r-- 1 root root  212016 Sep 25 13:13 mini_demo_data.json\n2.0M\t.", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [45] TOOL CALL — Read · 2026-09-25 13:15:35 UTC

```
/tmp/claude-0/-ai-inventor-aii-data-runs-run-qck1d05BqxkX-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-4-art-Ia-FT284H33j/5d0cec99-18d7-49eb-816d-46db335ac1b7/scratchpad/fig.png
```

### [46] TOOL RESULT — Read · 2026-09-25 13:15:35 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [47] TOOL CALL — Bash · 2026-09-25 13:15:47 UTC

```
Fix legend overlap and re-run notebook:
S=/tmp/claude-0/-ai-inventor-aii-data-runs-run-qck1d05BqxkX-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-4-art-Ia-FT284H33j/5d0cec99-18d7-49eb-816d-46db335ac1b7/scratchpad/mk.py && python3 - "$S" <<'EOF'
import sys; p=sys.argv[1]; s=open(p).read()
a='axes[1].legend(fontsize=7)'; assert a in s
s=s.replace(a,'axes[1].legend(fontsize=7, loc="upper center", bbox_to_anchor=(0.5, -0.15), ncol=2)')
b='axes[2].set_ylabel("rows")'; assert b in s
s=s.replace(b,b+'\naxes[2].legend(title="search_status", loc="upper left", fontsize=8)\naxes[2].set_ylim(0, ct.values.max() + 2)')
open(p,'w').write(s)
EOF
python3 $S && E=/tmp/aii_nb_test_envs/art_Ia_FT284H33j-af39a9391776 && UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 $E && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python $E/bin/python jupyter ipykernel && $E/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -1 && python3 -c "
import json,base64
nb=json.load(open('code_demo.ipynb'))
for c in nb['cells']:
  if c['cell_type']=='code' and 'N_SIG =' in ''.join(c['source']): print(''.join(c['source'])[-45:])
  for o in c.get('outputs',[]):
    if o.get('output_type')=='error': print('ERR')
    if 'data' in o and 'image/png' in o['data']: open('$(dirname $S)/fig.png','wb').write(base64.b64decode(o['data']['image/png']))
"; rm -rf full_data_out.json logs
```

### [48] TOOL CALL — Read · 2026-09-25 13:15:47 UTC

```
/tmp/claude-0/-ai-inventor-aii-data-runs-run-qck1d05BqxkX-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-4-art-Ia-FT284H33j/5d0cec99-18d7-49eb-816d-46db335ac1b7/scratchpad/fig.png
```

### [49] TOOL RESULT — Bash · 2026-09-25 13:16:07 UTC

```
{"stdout": "[NbConvertApp] Writing 131050 bytes to code_demo.ipynb\njson\nN_FREE = None\nN_GATE = None\nN_SIG = None", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [50] TOOL RESULT — Read · 2026-09-25 13:16:07 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [51] ASSISTANT · 2026-09-25 13:16:17 UTC

```
Now the README, manifest and output JSON.
```

### [52] TOOL CALL — Bash · 2026-09-25 13:16:17 UTC

```
Write README, manifest and struct output:
cat > README.md <<'EOF'
# Demo: name-free labels for free-vocabulary NL→FOL translations

This is a Colab-ready notebook demo of the **T7b name-free label dataset**. The dataset labels free-vocabulary NL→FOL rule translations without a gold vocabulary: an exhaustive, certificate-backed symbol-map search plus z3 equivalence decides each label. The notebook runs the original assembly code of `data.py` and `src/build_output.py`, split into cells with explanations and minimal changes, on a curated subset of the raw inputs.

## Layout

| path | what |
|---|---|
| `code_demo.ipynb` | the demo notebook: install → imports → data loading → config → `free_group` / `gate_group` / `sig_group` → `main()` (writes `full_data_out.json`) → results tables and figure |
| `mini_demo_data.json` | curated 100-row input subset: 60 FREE label rows (stratified over label × model family), 20 gloss-gate items, 20 SIG-replay rows, the sentences they need, and the full dataset's label seal and testability summary |
| `README.md` | this file |

The notebook loads `mini_demo_data.json` from the GitHub raw URL and falls back to the local copy. When it runs, it writes `full_data_out.json` (the demo-scale dataset) and `logs/data.log` into its working directory.

## Run

Open `code_demo.ipynb` in Colab or Jupyter and run all cells (about 20 s, most of it package installs). The only extra dependency is `loguru`. The config cell sets `N_FREE`, `N_GATE` and `N_SIG`, which limit the rows used from each input. `None` uses all rows in the demo file. The original `data.py` uses all 2,652 / 840 / 4,280 rows from the artifact's `results/` directory.

## Restoring removed files

Nothing in this directory is marked for deletion; see `.aii/manifest.yaml`, which has no entries. `full_data_out.json` and `logs/` are small notebook outputs. Re-running the notebook regenerates them.
EOF
printf 'entries: []\n' > .aii/manifest.yaml
cat > .terminal_claude_agent_struct_out.json <<'EOF'
{"out_expected_files": {"notebook": "code_demo.ipynb", "mini_data_file": "mini_demo_data.json"}}
EOF
cat .terminal_claude_agent_struct_out.json; ls -la . .aii
```

### [53] TOOL RESULT — Bash · 2026-09-25 13:16:19 UTC

```
{"stdout": "{\"out_expected_files\": {\"notebook\": \"code_demo.ipynb\", \"mini_data_file\": \"mini_demo_data.json\"}}\n.:\ntotal 3697\ndrwxr-xr-x 3 root root 1069457 Sep 25 13:16 .\ndrwxr-xr-x 7 root root 2000452 Sep 25 13:13 ..\ndrwxr-xr-x 2 root root    1200 Sep 25 13:16 .aii\n-rw------- 1 root root      54 Sep 25 13:09 .aii_claude_session.json\n-rw-r--r-- 1 root root  368360 Sep 25 13:16 .repl_agent.ptylog\n-rw-r--r-- 1 root root      97 Sep 25 13:16 .terminal_claude_agent_struct_out.json\n-rw-r--r-- 1 root root    1857 Sep 25 13:16 README.md\n-rw-r--r-- 1 root root  131112 Sep 25 13:16 code_demo.ipynb\n-rw-r--r-- 1 root root  212016 Sep 25 13:13 mini_demo_data.json\n\n.aii:\ntotal 1047\ndrwxr-xr-x 2 root root    1200 Sep 25 13:16 .\ndrwxr-xr-x 3 root root 1069457 Sep 25 13:16 ..\n-rw-r--r-- 1 root root      12 Sep 25 13:16 manifest.yaml", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [54] ASSISTANT · 2026-09-25 13:16:30 UTC

```
I've built `code_demo.ipynb` and `mini_demo_data.json`. The notebook runs cleanly in the fresh Colab-like test environment with every demo row, in about 20 seconds, most of it package installs.

**What the notebook runs.** It walks through `data.py` and the three functions it calls from `src/build_output.py` (`free_group`, `gate_group`, `sig_group`), copied as-is. The only changes are:
- rows come from the loaded demo data instead of files in `results/`;
- `ROOT` is the working directory, since a notebook has no script path;
- the paths to the artifact's `src/` and `vendor/` folders are dropped;
- `main()` is called at the end of its cell.

The original checks on each output row all pass, and the notebook writes a demo-scale `full_data_out.json`. The z3 map search itself is not re-run. The notebook only packages labels that search already produced, because that is all `data.py` does.

**Demo data.** `mini_demo_data.json` (212 KB) holds 100 rows taken from the raw files `data.py` reads:
- 60 free-vocabulary label rows, spread across all 4 labels and all 9 model families;
- 20 gloss-check test items across all 7 classes;
- 20 renamed fixed-vocabulary rows, covering both renaming types and every known-label / search-outcome combination;
- the full dataset's label seal and testability summary.

The rows are ordered so that even a small row limit gets a mix of labels. The task asked for examples from at most one dataset; I read that as one artifact, so the 100 rows span all three groups. That keeps `data.py`'s check that no group is empty from failing.

**Results section.** It shows:
- the seal and testability status: ERROR vs CORRECT can't be tested yet because no row is labelled CORRECT, while the provisional ERROR-vs-MAPPED split can;
- one worked example of each label;
- label counts for the demo next to the full dataset, and labels per model family;
- gloss-check items by class;
- the renamed-row check: 0 of 5 known-correct rows were wrongly certified as errors, and the true renaming was recovered 5 out of 5 times;
- a 3-panel figure.

The MAPPED worked example is a useful case. Its map is logically equivalent but wrong in meaning (`AmpleSpace` is mapped to "attends yoga regularly"), which shows why the pending gloss check is needed.

**Scaling.** The config has one row limit per group. I tested at 2, then 10, then all rows; runtime stayed at about 20 seconds each time, so the final version uses all rows. The original values (2,652 / 840 / 4,280 rows) are noted in the config cell.

**Checks.** The notebook contains the exact `GITHUB_DATA_URL` and fetches through it, falling back to the local `mini_demo_data.json`. I also wrote a `README.md`, an empty `.aii/manifest.yaml` (nothing large is stored), and `.terminal_claude_agent_struct_out.json`. I deleted the files the test runs generated so they aren't published as if they were the real dataset; the notebook recreates them. My tool set had no to-do list tool, so I worked through the six to-dos in order without tracking them in one.

Files are in `art_Ia_FT284H33j/`:
- `code_demo.ipynb`
- `mini_demo_data.json`
- `README.md`
- `.aii/manifest.yaml`
- `.terminal_claude_agent_struct_out.json`
```
