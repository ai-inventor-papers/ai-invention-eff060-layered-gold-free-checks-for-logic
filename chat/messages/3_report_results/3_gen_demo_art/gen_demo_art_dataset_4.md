# gen_demo_art_dataset_4 — report_results

> Phase: `gen_paper_repo` · `gen_demo_art`
> Run: `run_u75jRHUss0zo` — Gold-Free Faithfulness Metrics for NL-to-FOL Translation
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_demo_art_dataset_4` (terminal_claude_agent, claude-opus-5-5)

### [1] CONFIG · 2026-09-24 19:18:24 UTC

```
model: claude-opus-5-5 | effort: high | permission: bypassPermissions
```

### [2] SYSTEM-USER prompt · 2026-09-24 19:18:32 UTC

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
Your workspace: `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_Ia_FT284H33j`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_Ia_FT284H33j/`:
GOOD: `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_Ia_FT284H33j/file.py`, `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_Ia_FT284H33j/results/out.json`
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
Raw data URL: https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/main/round-4/dataset-5/demo/mini_demo_data.json

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
GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/main/round-4/dataset-5/demo/mini_demo_data.json"
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
TODO 6. Verify: (1) code_demo.ipynb contains GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/main/round-4/dataset-5/demo/mini_demo_data.json" exactly, (2) mini_demo_data.json exists, (3) uses GitHub URL pattern not just open('mini_demo_data.json').
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

### [3] HUMAN-USER prompt · 2026-09-24 19:18:32 UTC

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

### [4] TOOL CALL — Skill · 2026-09-24 19:18:36 UTC

```
aii-colab
```

### [5] TOOL RESULT — Skill · 2026-09-24 19:18:36 UTC

```
{"success": true, "commandName": "aii-colab"}
```

### [6] TOOL CALL — Skill · 2026-09-24 19:18:36 UTC

```
aii-long-running-tasks
```

### [7] TOOL RESULT — Skill · 2026-09-24 19:18:36 UTC

```
{"success": true, "commandName": "aii-long-running-tasks"}
```

### [8] TOOL CALL — Bash · 2026-09-24 19:18:36 UTC

```
cd /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_Ia_FT284H33j; ls -la; ls -la .aii; A=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5; ls -la $A $A/src; wc -l $A/data.py $A/src/*.py
```

### [9] TOOL RESULT — Bash · 2026-09-24 19:18:38 UTC

```
{"stdout": "total 3033\ndrwxr-xr-x 3 root root 1002644 Sep 24 19:18 .\ndrwxr-xr-x 7 root root 2073781 Sep 24 18:56 ..\ndrwxr-xr-x 2 root root       1 Sep 24 18:55 .aii\n-rw------- 1 root root      54 Sep 24 19:18 .aii_claude_session.json\n-rw-r--r-- 1 root root   27226 Sep 24 19:18 .repl_agent.ptylog\ntotal 980\ndrwxr-xr-x 2 root root       1 Sep 24 18:55 .\ndrwxr-xr-x 3 root root 1002644 Sep 24 19:18 ..\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5:\ntotal 37062\ndrwxr-xr-x 11 root root  2009731 Sep 24 10:50 .\ndrwxr-xr-x  7 root root  2038531 Sep 24 07:07 ..\ndrwxr-xr-x  2 root root    72500 Sep 24 07:55 .aii\n-rw-------  1 root root       54 Sep 24 07:08 .aii_claude_session.json\n-rw-r--r--  1 root root     1526 Sep 24 07:28 .aii_cost_ledger.jsonl\n-rw-------  1 root root     8646 Sep 24 07:55 .aii_worker_result.json\n-rw-r--r--  1 root root  2425895 Sep 24 07:55 .repl_agent.ptylog\n-rw-r--r--  1 root root     3026 Sep 24 07:54 .terminal_claude_agent_struct_out.json\n-rw-r--r--  1 root root     7886 Sep 24 07:53 README.md\n-rw-r--r--  1 root root     2054 Sep 24 07:12 VENDOR_SHA256.json\n-rw-r--r--  1 root root      819 Sep 24 07:45 cost_ledger.jsonl\n-rw-r--r--  1 root root     3714 Sep 24 07:53 data.py\n-rw-r--r--  1 root root    10436 Sep 24 07:46 dataset_card.md\n-rw-r--r--  1 root root     4460 Sep 24 07:36 deviations.json\n-rw-r--r--  1 root root 20238149 Sep 24 07:51 full_data_out.json\ndrwxr-xr-x  2 root root  1014830 Sep 24 07:48 logs\n-rw-r--r--  1 root root    25038 Sep 24 07:51 mini_data_out.json\n-rw-r--r--  1 root root    12063 Sep 24 07:25 prereg_freelab.json\n-rw-r--r--  1 root root       86 Sep 24 07:25 prereg_freelab.sha256\n-rw-r--r--  1 root root    11204 Sep 24 07:22 prereg_freelab_v1.json\n-rw-r--r--  1 root root       89 Sep 24 07:25 prereg_freelab_v1.sha256\n-rw-r--r--  1 root root    15836 Sep 24 07:51 preview_data_out.json\ndrwxr-xr-x  2 root root  1000110 Sep 24 07:22 prompts\n-rw-r--r--  1 root root      781 Sep 24 07:53 pyproject.toml\n-rw-r--r--  1 root root       27 Sep 24 07:20 pytest.ini\n-rw-r--r--  1 root root     8805 Sep 24 07:53 reproducibility.md\ndrwxr-xr-x  2 root root  2004356 Sep 24 07:46 results\ndrwxr-xr-x  2 root root  1014457 Sep 24 10:50 src\ndrwxr-xr-x  3 root root  2002457 Sep 24 07:50 temp\ndrwxr-xr-x  2 root root  1001128 Sep 24 10:50 tests\ndrwxr-xr-x  2 root root  1002841 Sep 24 10:50 vendor\ndrwxr-xr-x  2 root root  2000711 Sep 24 07:46 work\n\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src:\ntotal 3102\ndrwxr-xr-x  2 root root 1014457 Sep 24 10:50 .\ndrwxr-xr-x 11 root root 2009731 Sep 24 10:50 ..\n-rw-r--r--  1 root root    9766 Sep 24 07:37 assemble_labels.py\n-rw-r--r--  1 root root    6169 Sep 24 07:43 build_output.py\n-rw-r--r--  1 root root    2436 Sep 24 07:20 common.py\n-rw-r--r--  1 root root   37862 Sep 24 07:32 freelab.py\n-rw-r--r--  1 root root   12832 Sep 24 07:31 gate.py\n-rw-r--r--  1 root root    8622 Sep 24 07:30 gloss.py\n-rw-r--r--  1 root root    4014 Sep 24 07:28 hf_survey.py\n-rw-r--r--  1 root root    9645 Sep 24 07:20 inputs.py\n-rw-r--r--  1 root root    5518 Sep 24 07:37 post_seal_join.py\n-rw-r--r--  1 root root   12216 Sep 24 07:25 prereg.py\n-rw-r--r--  1 root root    2308 Sep 24 07:45 provisional_view.py\n-rw-r--r--  1 root root   12023 Sep 24 07:42 resume_gloss.py\n-rw-r--r--  1 root root    5114 Sep 24 07:24 run_search.py\n-rw-r--r--  1 root root    4296 Sep 24 07:34 sig_rename.py\n-rw-r--r--  1 root root   11806 Sep 24 07:43 soundness.py\n-rw-r--r--  1 root root    3419 Sep 24 07:12 vendor_copy.py\n    67 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/data.py\n   177 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/assemble_labels.py\n    98 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/build_output.py\n    70 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/common.py\n   838 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/freelab.py\n   279 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/gate.py\n   205 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/gloss.py\n    83 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/hf_survey.py\n   191 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/inputs.py\n   112 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/post_seal_join.py\n   141 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/prereg.py\n    42 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/provisional_view.py\n   247 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/resume_gloss.py\n   117 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/run_search.py\n    96 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/sig_rename.py\n   202 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/soundness.py\n    69 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/vendor_copy.py\n  3034 total", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [10] TOOL CALL — Bash · 2026-09-24 19:18:40 UTC

```
A=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5; cat $A/data.py; cat $A/pyproject.toml; head -c 6000 $A/preview_data_out.json
```

### [11] TOOL RESULT — Bash · 2026-09-24 19:18:40 UTC

```
{"stdout": "# /// script\n# requires-python = \">=3.12\"\n# dependencies = [\"loguru==0.7.3\"]\n# ///\n\"\"\"Build full_data_out.json (exp_sel_data_out) from the three chosen datasets, one example per data row:\n  rcomp_free_labels      2,652 FREE rows, name-free labels (search-only, sealed; see dataset_card.md)\n  gloss_gate_items         840 known-answer (symbol use, meaning) items\n  sig_soundness_replay   4,280 renamed SIG rows with known pure-z3 labels\nAll three are derived from this run's R_COMP artifacts by src/*.py (results/*.jsonl, work/sentences.json).\nusage: uv run data.py\n\"\"\"\nfrom __future__ import annotations\n\nimport json\nimport sys\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parent\nsys.path.insert(0, str(ROOT / \"src\"))\nsys.path.insert(0, str(ROOT / \"vendor\"))\n\nfrom loguru import logger  # noqa: E402\n\nlogger.remove()\nlogger.add(sys.stdout, level=\"INFO\", format=\"{time:HH:mm:ss}|{level:<7}|{message}\")\n(ROOT / \"logs\").mkdir(exist_ok=True)\nlogger.add(ROOT / \"logs\" / \"data.log\", rotation=\"30 MB\", level=\"DEBUG\")\n\nSELECTED = [\"rcomp_free_labels\", \"gloss_gate_items\", \"sig_soundness_replay\"]\n\n\n@logger.catch(reraise=True)\ndef main() -> None:\n    import build_output as B  # run-derived plan groups (reads results/*.jsonl, work/sentences.json)\n    groups = [B.free_group(), B.gate_group(), B.sig_group()]\n    for g in groups:\n        assert g[\"examples\"], g[\"dataset\"]\n        for e in g[\"examples\"]:\n            assert isinstance(e[\"input\"], str) and isinstance(e[\"output\"], str), g[\"dataset\"]\n            assert not ({\"split\", \"dataset\", \"context\"} & set(e)), g[\"dataset\"]\n    seal = json.loads((ROOT / \"results\" / \"seal.json\").read_text())[\"seals\"][-1]\n    t = json.loads((ROOT / \"results\" / \"testability_FREE_v2.json\").read_text())\n    out = {\"metadata\": {\n        \"artifact\": \"T7b name-free labels for free-vocabulary rule translations (run_u75jRHUss0zo, iter 4, gen_art_dataset_5)\",\n        \"workspace\": str(ROOT),\n        \"selection\": (\"the three plan groups (chosen as best 3 of 6 standardised candidates; folio / malls_test / \"\n                      \"logicnli_test were context only: no multi-system candidates, ~36-39% wrong gold, or no FOL; their \"\n                      \"standardised record is temp/candidates_data_out.json)\"),\n        \"label_mode\": seal[\"mode\"],\n        \"status_note\": (\"SEARCH-ONLY labels: the paid gloss step could not run (deviation D9: run OpenRouter budget \"\n                        \"exhausted before this artifact's first call; re-probed at packaging, still HTTP 403). ERROR_CERT is \"\n                        \"final and certificate-backed; MAPPED rows are UNRESOLVED_GLOSS_NOT_RUN until src/resume_gloss.py \"\n                        \"runs. metadata_label_binary_search_provisional (ERROR vs MAPPED) is a provisional view with audited \"\n                        \"contamination (results/soundness_audit.json).\"),\n        \"seal_all_rows_sha256\": seal[\"label_vector_sha256_all_rows\"],\n        \"seal_untouched_sha256\": seal.get(\"label_vector_sha256_untouched\"),\n        \"prereg_sha256\": seal[\"prereg_sha256\"],\n        \"testability_all_rows\": {k: t[\"all_rows\"][k] for k in (\"n_ERROR\", \"n_CORRECT\", \"TESTABLE\", \"label_counts\")},\n        \"testability_untouched\": {k: t[\"untouched_subset\"][k] for k in (\"n_ERROR\", \"n_CORRECT\", \"TESTABLE\", \"label_counts\")},\n        \"provisional_view_testable\": {k: t[\"search_provisional_view\"][k][\"TESTABLE\"] for k in (\"all_rows\", \"untouched_subset\")},\n    }, \"datasets\": [g for g in groups if g[\"dataset\"] in SELECTED]}\n    (ROOT / \"full_data_out.json\").write_text(json.dumps(out, ensure_ascii=False))\n    logger.info(f\"full_data_out.json: {[(g['dataset'], len(g['examples'])) for g in out['datasets']]}\")\n\n\nif __name__ == \"__main__\":\n    main()\n[project]\nname = \"freelab-u75j\"\nversion = \"0.1.0\"\ndescription = \"T7b: name-free (alignment-free) labels for free-vocabulary NL->FOL rule translations (run_u75jRHUss0zo iter 4, gen_art_dataset_5)\"\nrequires-python = \">=3.12\"\ndependencies = [\n    \"anyio==4.15.1\",\n    \"certifi==2026.7.22\",\n    \"click==8.5.0\",\n    \"cloudpickle==3.1.2\",\n    \"defusedxml==0.7.1\",\n    \"h11==0.16.0\",\n    \"httpcore==1.0.9\",\n    \"httpx==0.28.1\",\n    \"idna==3.20\",\n    \"iniconfig==2.3.0\",\n    \"joblib==1.6.0\",\n    \"loguru==0.7.3\",\n    \"nltk==3.10.3\",\n    \"numpy==2.5.3\",\n    \"packaging==26.3\",\n    \"pluggy==1.6.0\",\n    \"psutil==7.2.2\",\n    \"pygments==2.21.0\",\n    \"pytest==9.1.1\",\n    \"pyyaml==6.0.3\",\n    \"regex==2026.9.10\",\n    \"tqdm==4.70.1\",\n    \"typing-extensions==4.16.0\",\n    \"z3-solver==5.1.0.0\",\n]\n{\n  \"metadata\": {\n    \"artifact\": \"T7b name-free labels for free-vocabulary rule translations (run_u75jRHUss0zo, iter 4, gen_art_dataset_5)\",\n    \"workspace\": \"/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5\",\n    \"selection\": \"the three plan groups (chosen as best 3 of 6 standardised candidates; folio / malls_test / logicnli_test were context only: no multi-system candidates, ~36-39% wrong gold, or no FOL; their standardise...\",\n    \"label_mode\": \"search_only\",\n    \"status_note\": \"SEARCH-ONLY labels: the paid gloss step could not run (deviation D9: run OpenRouter budget exhausted before this artifact's first call; re-probed at packaging, still HTTP 403). ERROR_CERT is final and...\",\n    \"seal_all_rows_sha256\": \"9609ebbb725832c467389e9d04b6334ca906ba10d400e7a7dccd976d39ebe3dd\",\n    \"seal_untouched_sha256\": \"b364a49a8e21835de660689097b462212f3f72b96ef66b437a14cc60e039f500\",\n    \"prereg_sha256\": \"b081c39991f52da2f419a6cefe56da48705d8abddf292d0faa89cec0b393a799\",\n    \"testability_all_rows\": {\n      \"n_ERROR\": 759,\n      \"n_CORRECT\": 0,\n      \"TESTABLE\": false,\n      \"label_counts\": {\n        \"ERROR_CERT\": 759,\n        \"UNRESOLVED_GLOSS_NOT_RUN\": 1506,\n        \"UNPARSEABLE\": 188,\n        \"NO_OUTPUT\": 199\n      }\n    },\n    \"testability_untouched\": {\n      \"n_ERROR\": 636,\n      \"n_CORRECT\": 0,\n      \"TESTABLE\": false,\n      \"label_counts\": {\n        \"ERROR_CERT\": 636,\n        \"UNRESOLVED_GLOSS_NOT_RUN\": 1175,\n        \"UNPARSEABLE\": 188,\n        \"NO_OUTPUT\": 199\n      }\n    },\n    \"provisional_view_testable\": {\n      \"all_rows\": true,\n      \"untouched_subset\": true\n    }\n  },\n  \"datasets\": [\n    {\n      \"dataset\": \"rcomp_free_labels\",\n      \"examples\": [\n        {\n          \"input\": \"{\\\"text\\\": \\\"Each legislator who is at Board Game night, who visits a coffee shop regularly, and who can distinguish the taste of different condiments is Emily's friend, except if the legislator is an el...\",\n          \"output\": \"ERROR_CERT\",\n          \"metadata_row_key\": \"a81d2862772cd744|FREE|G1|fewshot_v1\",\n          \"metadata_item_id\": \"a81d2862772cd744\",\n          \"metadata_sentence_id\": \"001a7f0caf5a\",\n          \"metadata_template_id\": \"T1\",\n          \"metadata_clause_type\": \"unless\",\n          \"metadata_words\": 34,\n          \"metadata_word_tercile\": \"W2\",\n          \"metadata_nconds_weak\": 5,\n          \"metadata_negated_condition\": null,\n          \"metadata_nested\": false,\n          \"metadata_label_binary\": \"ERROR\",\n          \"metadata_label_binary_search_provisional\": \"ERROR\",\n          \"metadata_label_source\": \"exhaustive_map_v1\",\n          \"metadata_search_status\": \"ERROR_CERT\",\n          \"metadata_matched_reading\": null,\n          \"metadata_map_certificate\": null,\n          \"metadata_n_maps_enumerated\": 0,\n          \"metadata_n_maps_fingerprint_pass\": 0,\n          \"metadata_n_equiv_maps\": 0,\n          \"metadata_n_equiv_map_orbits\": 0,\n          \"metadata_nonequiv_certificate_type_counts\": {\n            \"count_prune_subtree\": 291,\n            \"no_polarity_compatible_target\": 10\n          },\n          \"metadata_gloss_pairs\": null,\n          \"metadata_gloss_decision\": null,\n          \"metadata_unresolved_reason\": null,\n          \"metadata_irrelevant_symbols\": [],\n          \"metadata_search_secs\": 0.06,\n          \"metadata_seen_iter3\": false,\n          \"metadata_old_label_iter3\": \"UNRESOLVED\",\n          \"metadata_fold\": \"RCOMP_FREE\"\n        },\n        {\n          \"input\": \"{\\\"text\\\": \\\"Each legislator who is at Board Game night, who visits a coffee shop regularly, and who can distinguish the taste of different condiments is Emily's friend, except if the legislator is an el...\",\n          \"output\": \"UNRESOLVED_GLOSS_NOT_RUN\",\n          \"metadata_row_key\": \"94bcb373f89b6d9a|FREE|G1b|fewshot_v1\",\n          \"metadata_item_id\": \"94bcb373f89b6d9a\",\n          \"metadata_sentence_id\": \"001a7f0caf5a\",\n          \"metadata_template_id\": \"T1\",\n          \"metadata_clause_type\": \"unless\",\n          \"metadata_words\": 34,\n          \"metadata_word_tercile\": \"W2\",\n          \"metadata_nconds_weak\": 5,\n          \"metadata_negated_condition\": null,\n          \"metadata_nested\": false,\n          \"metadata_label_binary\": \"EXCLUDED\",\n          \"metadata_label_binary_search_provisional\": \"MAPPED\",\n          \"metadata_label_source\": \"exhaustive_map_v1\",\n          \"metadata_search_status\": \"MAPPED\",\n          \"metadata_matched_reading\": \"strong\",\n          \"metadata_map_certificate\": {\n            \"status\": \"z3_equivalent_map_not_gloss_checked\",\n            \"reading\": \"strong\",\n            \"map\": [\n              \"Attends(x, boardGameNight) => At(x, boardGameNight)\",\n              \"CanDistinguish(x, condiments) => Can(x, distinguishTheTasteOfDifferentCondiments)\",\n              \"ElectedOfficial(x) => ElectedOfficial(x)\"\n            ],\n            \"bridges\": [\n              \"B2\"\n            ]\n          },\n          \"metadata_n_maps_enumerated\": 48,\n          \"metadata_n_maps_fingerprint_pass\": 48,\n          \"metadata_n_equiv_maps\": 48,\n          \"metadata_n_equiv_map_orbits\": 2,\n          \"metadata_nonequiv_certificate_type_counts\": {\n            \"count_prune_subtree\": 360\n          },\n          \"metadata_gloss_pairs\": [\n            {\n              \"cand_atom\": \"Attends(x, boardGameNight)\",\n              \"meaning\": \"x is at Board Game night\",\n              \"haiku\": null,\n              \"qwen\": null\n            },\n            {\n              \"cand_atom\": \"CanDistinguish(x, condiments)\",\n              \"meaning\": \"x can distinguish the taste of different condiments\",\n              \"haiku\": null,\n              \"qwen\": null\n            },\n            {\n              \"cand_atom\": \"ElectedOfficial(x)\",\n              \"meaning\": \"x is an elected official\",\n              \"haiku\": null,\n              \"qwen\": null\n            }\n          ],\n          \"metadata_gloss_decision\": null,\n          \"metadata_unresolved_reason\": \"gloss check not run (D9: API budget exhausted)\",\n          \"metadata_irrelevant_symb", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [12] TOOL CALL — Bash · 2026-09-24 19:18:44 UTC

```
A=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5; cat $A/src/build_output.py; ls -la $A/vendor $A/results $A/work | head -60; sed -n 1,80p $A/src/freelab.py
```

### [13] TOOL RESULT — Bash · 2026-09-24 19:18:44 UTC

```
{"stdout": "#!/usr/bin/env python3\n\"\"\"STEP I: full_data_out.json (exp_sel_data_out) with three groups:\n  rcomp_free_labels     one row per FREE generation record (2,652), label = name-free label (search-only now, D9)\n  gloss_gate_items      840 known-answer (symbol use, meaning) items, 7 classes, halves A/B\n  sig_soundness_replay  4,280 rows = 2,140 SIG rows x {nonce, synonym} renames, output = known pure-z3 SIG label\n\"\"\"\nfrom __future__ import annotations\n\nimport json\n\nfrom common import RES, ROOT, WORK, load_jsonl, setup_logger\n\nlogger = setup_logger(\"build_output\")\n\n\ndef md(d: dict) -> dict:\n    return {f\"metadata_{k}\": v for k, v in d.items()}\n\n\ndef free_group() -> dict:\n    rows = load_jsonl(RES / \"free_labels_v2.jsonl\")\n    ex = []\n    for r in rows:\n        inp = {\"text\": r[\"text\"], \"candidate_fol\": r[\"candidate_fol\"], \"system\": r[\"system\"], \"family\": r[\"family\"],\n               \"slot\": r[\"slot\"], \"prompt_variant\": r[\"prompt_variant\"], \"condition\": \"FREE\", \"template_id\": r[\"template_id\"]}\n        search_bin = {\"ERROR_CERT\": \"ERROR\", \"UNRESOLVED_GLOSS_NOT_RUN\": \"MAPPED\"}.get(r[\"label\"], \"EXCLUDED\")\n        meta = {\n            \"row_key\": r[\"row_key\"], \"item_id\": r[\"item_id\"], \"sentence_id\": r[\"sentence_id\"], \"template_id\": r[\"template_id\"],\n            \"clause_type\": r[\"clause_type\"], \"words\": r[\"words\"], \"word_tercile\": r[\"word_tercile\"],\n            \"nconds_weak\": r[\"nconds_weak\"], \"negated_condition\": r[\"negated_condition\"], \"nested\": r[\"nested\"],\n            \"label_binary\": r[\"label_binary\"], \"label_binary_search_provisional\": search_bin,\n            \"label_source\": r[\"label_source\"], \"search_status\": r.get(\"search_status\"),\n            \"matched_reading\": r.get(\"matched_reading\") or r.get(\"matched_reading_search\"),\n            \"map_certificate\": r.get(\"map_certificate\"),\n            \"n_maps_enumerated\": r.get(\"n_maps_enumerated\"), \"n_maps_fingerprint_pass\": r.get(\"n_maps_fingerprint_pass\"),\n            \"n_equiv_maps\": r.get(\"n_equiv_maps\"), \"n_equiv_map_orbits\": r.get(\"n_equiv_map_orbits\"),\n            \"nonequiv_certificate_type_counts\": r.get(\"nonequiv_certificate_type_counts\"),\n            \"gloss_pairs\": r.get(\"gloss_pairs\"), \"gloss_decision\": r.get(\"gloss_decision\"),\n            \"unresolved_reason\": r.get(\"unresolved_reason\"), \"irrelevant_symbols\": r.get(\"irrelevant_symbols\"),\n            \"search_secs\": r.get(\"search_secs\"), \"seen_iter3\": r.get(\"seen_iter3\"),\n            \"old_label_iter3\": r.get(\"old_label_iter3\"), \"fold\": \"RCOMP_FREE\"}\n        ex.append({\"input\": json.dumps(inp, ensure_ascii=False), \"output\": r[\"label\"], **md(meta)})\n    return {\"dataset\": \"rcomp_free_labels\", \"examples\": ex}\n\n\ndef gate_group() -> dict:\n    items = json.loads((RES / \"gate_items.json\").read_text())\n    ex = []\n    for i in items:\n        inp = {\"sentence\": i[\"sentence\"], \"candidate_atom\": i[\"candidate_atom\"], \"proposed_meaning\": i[\"proposed_meaning\"]}\n        meta = {\"item_id\": i[\"item_id\"], \"class\": i[\"class\"], \"half\": i[\"half\"], \"sentence_id\": i[\"sentence_id\"],\n                \"template_id\": i[\"template_id\"], \"note\": i[\"note\"], \"prompt_version\": \"gloss_v1\",\n                \"haiku_verdict\": i.get(\"haiku_gloss_v1\"), \"qwen_verdict\": i.get(\"qwen_gloss_v1\"), \"fold\": \"GLOSS_GATE\"}\n        ex.append({\"input\": json.dumps(inp, ensure_ascii=False), \"output\": i[\"gold\"], **md(meta)})\n    return {\"dataset\": \"gloss_gate_items\", \"examples\": ex}\n\n\ndef sig_group() -> dict:\n    sents = json.loads((WORK / \"sentences.json\").read_text())\n    rows = load_jsonl(RES / \"sig_replay_rows.jsonl\")\n    ex = []\n    for r in rows:\n        inp = {\"text\": sents[r[\"sentence_id\"]][\"text\"], \"candidate_fol\": r[\"renamed_fol\"], \"rename\": r[\"rename\"],\n               \"template_id\": r[\"template_id\"]}\n        meta = {k: r[k] for k in (\"row_key\", \"sentence_id\", \"slot\", \"template_id\", \"sig_matched_reading\", \"canon_fol\",\n                                  \"search_status\", \"identity_map_found\", \"non_identity_map_found\", \"n_equiv_maps\",\n                                  \"n_equiv_map_orbits\", \"n_maps_enumerated\", \"nonequiv_certificate_type_counts\",\n                                  \"oracle_end_to_end_label\", \"in_e2e_gloss_subsample_300\", \"e2e_gloss_label\")}\n        meta[\"map_equiv_found\"] = r[\"search_status\"] in (\"MAPPED\", \"READING_CHOICE\")\n        meta[\"fold\"] = f\"SIG_REPLAY_{r['rename'].upper()}\"\n        ex.append({\"input\": json.dumps(inp, ensure_ascii=False), \"output\": r[\"sig_label\"], **md(meta)})\n    return {\"dataset\": \"sig_soundness_replay\", \"examples\": ex}\n\n\ndef main() -> None:\n    seal = json.loads((RES / \"seal.json\").read_text())[\"seals\"]\n    t = json.loads((RES / \"testability_FREE_v2.json\").read_text())\n    out = {\"metadata\": {\n        \"artifact\": \"T7b name-free labels for free-vocabulary rule translations (run_u75jRHUss0zo, iter 4, gen_art_dataset_5)\",\n        \"workspace\": str(ROOT),\n        \"label_mode\": seal[-1][\"mode\"],\n        \"status_note\": (\"SEARCH-ONLY labels: the paid gloss step could not run (deviation D9: run OpenRouter budget \"\n                        \"exhausted before this artifact's first call). ERROR_CERT is final and certificate-backed; MAPPED rows \"\n                        \"are UNRESOLVED_GLOSS_NOT_RUN until src/resume_gloss.py runs. metadata_label_binary_search_provisional \"\n                        \"(ERROR vs MAPPED) is a provisional view with audited contamination (see results/soundness_audit.json).\"),\n        \"seal_all_rows_sha256\": seal[-1][\"label_vector_sha256_all_rows\"],\n        \"seal_untouched_sha256\": seal[-1].get(\"label_vector_sha256_untouched\"),\n        \"prereg_sha256\": seal[-1][\"prereg_sha256\"],\n        \"testability_all_rows\": {k: t[\"all_rows\"][k] for k in (\"n_ERROR\", \"n_CORRECT\", \"TESTABLE\", \"label_counts\")},\n        \"testability_untouched\": {k: t[\"untouched_subset\"][k] for k in (\"n_ERROR\", \"n_CORRECT\", \"TESTABLE\", \"label_counts\")}\n        if isinstance(t.get(\"untouched_subset\"), dict) else None,\n    }, \"datasets\": [free_group(), gate_group(), sig_group()]}\n    (ROOT / \"full_data_out.json\").write_text(json.dumps(out, ensure_ascii=False))\n    logger.info(f\"full_data_out.json: {[(d['dataset'], len(d['examples'])) for d in out['datasets']]}\")\n\n\nif __name__ == \"__main__\":\n    main()\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/results:\ntotal 48538\ndrwxr-xr-x  2 root root  2004356 Sep 24 07:46 .\ndrwxr-xr-x 11 root root  2009731 Sep 24 10:50 ..\n-rw-r--r--  1 root root    10436 Sep 24 07:46 dataset_card.md\n-rw-r--r--  1 root root  8143542 Sep 24 07:37 free_labels_v2.jsonl\n-rw-r--r--  1 root root   427414 Sep 24 07:32 gate_items.json\n-rw-r--r--  1 root root      303 Sep 24 07:45 gate_report.json\n-rw-r--r--  1 root root     1106 Sep 24 07:13 input_counts.json\n-rw-r--r--  1 root root 17748257 Sep 24 07:35 map_search.jsonl\n-rw-r--r--  1 root root    23765 Sep 24 07:37 old_label_agreement.json\n-rw-r--r--  1 root root     3623 Sep 24 07:37 seal.json\n-rw-r--r--  1 root root    31504 Sep 24 07:13 shape_census.json\n-rw-r--r--  1 root root  7459154 Sep 24 07:37 sig_replay_nonce.jsonl\n-rw-r--r--  1 root root  3820323 Sep 24 07:43 sig_replay_rows.jsonl\n-rw-r--r--  1 root root  7937822 Sep 24 07:39 sig_replay_syn.jsonl\n-rw-r--r--  1 root root    23836 Sep 24 07:43 soundness_audit.json\n-rw-r--r--  1 root root    52908 Sep 24 07:45 testability_FREE_v2.json\n\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/vendor:\ntotal 2973\ndrwxr-xr-x  2 root root 1002841 Sep 24 10:50 .\ndrwxr-xr-x 11 root root 2009731 Sep 24 10:50 ..\n-rw-r--r--  1 root root       0 Sep 24 07:12 __init__.py\n-rw-r--r--  1 root root    9244 Sep 24 07:12 fol.py\n-rw-r--r--  1 root root    4916 Sep 24 07:12 fol_triage_min.py\n-rw-r--r--  1 root root    1510 Sep 24 07:12 label_sig_min.py\n-rw-r--r--  1 root root    3557 Sep 24 07:12 perturb_min.py\n-rw-r--r--  1 root root    1584 Sep 24 07:12 repair_census_min.py\n-rw-r--r--  1 root root    1412 Sep 24 07:12 sig_prompt_min.py\n-rw-r--r--  1 root root    6871 Sep 24 07:12 templates.py\n\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/work:\ntotal 11210\ndrwxr-xr-x  2 root root 2000711 Sep 24 07:46 .\ndrwxr-xr-x 11 root root 2009731 Sep 24 10:50 ..\n-rw-r--r--  1 root root    2359 Sep 24 07:38 audit_errcert_keys.json\n-rw-r--r--  1 root root    2359 Sep 24 07:39 audit_mapped_keys.json\n-rw-r--r--  1 root root   43178 Sep 24 07:39 audit_mapped_view.txt\n-rw-r--r--  1 root root    1062 Sep 24 07:18 dev_trial_D1.py\n-rw-r--r--  1 root root    9223 Sep 24 07:40 executor_audit_verdicts.json\n-rw-r--r--  1 root root 1767883 Sep 24 07:13 free_rows.jsonl\n-rw-r--r--  1 root root  806127 Sep 24 07:21 models_snapshot.json\n-rw-r--r--  1 root root    1373 Sep 24 07:33 probe_free_models_D9.py\n-rw-r--r--  1 root root  685497 Sep 24 07:13 sentences.json\n-rw-r--r--  1 root root 1429393 Sep 24 07:34 sig_renamed_nonce.jsonl\n-rw-r--r--  1 root root 1663307 Sep 24 07:35 sig_renamed_syn.jsonl\n-rw-r--r--  1 root root 1053397 Sep 24 07:13 sig_rows.jsonl\n\"\"\"Name-free (alignment-free) labelling of free-vocabulary FOL candidates against template readings.\n\nNo name similarity is used anywhere: symbol names are only used (a) as identifiers, (b) by the B5 lexical-negation\nregex, which licenses the map ``P := ¬U`` (a gloss check still has to accept it). Which candidate symbol means which\ntemplate atom is decided by EXHAUSTIVE enumeration of a declared map family under SOUND semantic prunes, followed by\nz3 equivalence; the lexical plausibility of the winning map is decided separately by a gloss check (``checker``).\n\nMap family (frozen in prereg_freelab.json):\n  * A candidate predicate is a UNIT if, in every occurrence, all argument positions but one (the subject position)\n    hold the same constants, and those constants occur nowhere else (\"constant absorption\"; unary predicates are\n    trivially units). A template atom over the single variable x (U(x) or R(x, c)) is a template UNIT.\n  * UNIT maps a candidate unit to exactly one template unit (plain, B1 reification and B2 de-reification are all\n    this form: P(x) := R(x, c); P(x, k) := U(x); P(x, k) := R(x, c)). B5: P := ¬u (only if the name's first token is a\n    negation marker). B3 merge: P := u1 ∧ u2 (u1, u2 sibling conjuncts of the reading). B4 split: two candidate units\n    that only ever occur as positive sibling conjuncts both := u.\n  * REL maps a genuinely relational candidate predicate (arity 2, not a unit) to a template binary predicate, either\n    argument order; its non-absorbed constants map injectively to template constants or stay free (fresh).\n  * Injective: each template unit / predicate is the target of at most one candidate symbol (B4 excepted).\n    Structural bridge uses (B3 + B4) <= MAX_STRUCT per map; B1/B2/B5 are 1:1 unit forms and are not capped.\n  * Semantically inert candidate symbols (F ≡ F[s := fresh]) are dropped (kept as fresh symbols in the image).\nSound prunes: relevance (every relevant candidate symbol must be mapped; every template unit must be covered),\npolarity (z3-exact monotonicity is preserved by 1:1 generic substitutions), and a finite-model fingerprint\n(128 interpretations, domain 2-3, fixed seeds; a mismatch is a certified countermodel). Maps that pass the\nfingerprint go to z3 (2 s, retry 10 s).\n\nEXACT: ERROR (no equivalent map) is exact RELATIVE TO THIS FAMILY and these caps; every equivalent map is a z3 proof.\nBOUNDED: maps outside the family (extra quantified structure, ∃-for-constant, ternary relations with variables, ...)\nare not searched; the search stops at MAX_MAPS maps or MAX_SECS seconds per (candidate, reading) -> CAP.\n\"\"\"\nfrom __future__ import annotations\n\nimport itertools\nimport re\nimport time\nimport zlib\nfrom collections import Counter, defaultdict\nfrom functools import lru_cache\n\nimport z3\n\nfrom fol import mkpred, parse, preds, profile, to_z3, valid, U\nfrom repair_census_min import atoms, bound_vars\n\nMAX_MAPS = 200_000\nMAX_SECS = 90.0\nMAX_STRUCT = 2\nN_FP = 128\nZ3_MS, Z3_MS_RETRY = 2000, 10000\nNEG_TOKEN = re.compile(r\"^(not|non|no|un|in|im|il|ir|dis|never|lacks?|without)$\", re.I)\nNEG_PREFIX = re.compile(r\"^(Un|Non|In|Im|Dis)[A-Z]\")\nFLIP = {\"UP\": \"DOWN\", \"DOWN\": \"UP\", \"NONMONO\": \"NONMONO\"}\n\n\n# ------------------------------------------------------------------------------------------------ AST helpers\ndef to_str(e) -> str:\n    k = e[0]\n    if k == \"atom\":\n        return f\"{e[1]}({', '.join(e[2])})\" if e[2] else e[1]\n    if k in (\"all\", \"ex\"):\n        return f\"{'∀' if k == 'all' else '∃'}{e[1]} ({to_str(e[2])})\"\n    if k == \"not\":\n        return f\"¬{to_str(e[1])}\"\n    sym = {\"and\": \"∧\", \"or\": \"∨\", \"imp\": \"→\", \"iff\": \"↔\", \"xor\": \"⊕\"}[k]\n    return f\"({to_str(e[1])} {sym} {to_str(e[2])})\"\n\n\ndef name_tokens(n: str) -> list[str]:\n    return re.findall(r\"[A-Z]?[a-z]+|[A-Z]+(?![a-z])|\\d+\", n.replace(\"_\", \" \"))\n\n\ndef negation_named(name: str) -> bool:\n    \"\"\"B5 licence: first CamelCase/underscore token is a negation marker, or the name starts Un/Non/In/Im/Dis+Upper.\"\"\"\n    t = name_tokens(name)\n    return bool((t and NEG_TOKEN.match(t[0])) or NEG_PREFIX.match(name))\n\n\ndef free_consts(e) -> set:\n    out = set()\n\n    def walk(x, bv):", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [14] TOOL CALL — Bash · 2026-09-24 19:18:54 UTC

```
A=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5; cat $A/src/run_search.py; cat $A/src/common.py; head -c 3000 $A/results/free_labels_v2.jsonl; echo; python3 -c "
import json;s=json.load(open('$A/results/seal.json'));print(json.dumps(s,indent=1)[:2500])"
```

### [15] TOOL RESULT — Bash · 2026-09-24 19:18:54 UTC

```
{"stdout": "#!/usr/bin/env python3\n\"\"\"STEP C (and audit (i) search): exhaustive map search per unique (sentence, candidate) class, CPU only.\n\nusage: run_search.py free [--limit N]          -> results/map_search.jsonl       (FREE classes)\n       run_search.py sig --rename nonce|syn    -> results/sig_replay_{nonce,syn}.jsonl (renamed SIG classes)\nResumable (skips class keys already written). ProcessPoolExecutor(spawn), one task per sentence.\n\"\"\"\nfrom __future__ import annotations\n\nimport argparse\nimport json\nimport multiprocessing as mp\nimport re\nimport resource\nimport time\nfrom collections import defaultdict\nfrom concurrent.futures import ProcessPoolExecutor, as_completed\n\nfrom common import RES, WORK, load_jsonl, setup_logger, sha1\n\nNUM_WORKERS = 4\n\n\ndef class_key(sid: str, fol: str) -> str:\n    return sha1(sid + \"|\" + re.sub(r\"\\s+\", \"\", fol))[:16]\n\n\ndef work_sentence(job: dict) -> list[dict]:\n    import sys\n    sys.setrecursionlimit(10000)\n    import common  # noqa: F401  (paths)\n    import freelab as FL\n    s = job[\"sent\"]\n    rdfs = {\"weak\": s[\"reference_fol_weak\"], \"strong\": s[\"reference_fol_strong\"]}\n    if s.get(\"reading_converse\"):\n        rdfs[\"converse\"] = s[\"reading_converse\"]\n    rds = {k: FL.Reading(v, s[\"units\"]) for k, v in rdfs.items()}\n    out = []\n    for ck, fol in job[\"classes\"]:\n        t0 = time.time()\n        try:\n            cand = FL.Candidate(fol)\n        except (ValueError, IndexError, TypeError, KeyError, RecursionError) as ex:\n            out.append({\"class_key\": ck, \"sentence_id\": s[\"sentence_id\"], \"candidate_fol\": fol, \"status\": \"UNPARSEABLE\",\n                        \"error\": str(ex)[:160]})\n            continue\n        try:\n            r = FL.label_with(cand, rds, FL.MAX_MAPS * job.get(\"cap_mult\", 1), FL.MAX_SECS * job.get(\"cap_mult\", 1), t0)\n        except Exception as ex:  # noqa: BLE001 - one class must not kill the sentence\n            out.append({\"class_key\": ck, \"sentence_id\": s[\"sentence_id\"], \"candidate_fol\": fol,\n                        \"status\": \"UNRESOLVED_Z3_UNKNOWN\", \"error\": f\"{type(ex).__name__}: {str(ex)[:160]}\"})\n            continue\n        out.append({\"class_key\": ck, \"sentence_id\": s[\"sentence_id\"], \"candidate_fol\": fol, **r})\n    return out\n\n\ndef run(classes_by_sid: dict, sents: dict, outp, logger, limit: int | None, cap_mult: int = 1) -> None:\n    done = set()\n    if outp.exists():\n        done = {json.loads(l)[\"class_key\"] for l in outp.read_text().splitlines() if l.strip()}\n    jobs, n = [], 0\n    for sid in sorted(classes_by_sid):\n        cl = [(ck, f) for ck, f in classes_by_sid[sid] if ck not in done]\n        if not cl:\n            continue\n        if limit is not None and n >= limit:\n            break\n        if limit is not None:\n            cl = cl[: max(0, limit - n)]\n        n += len(cl)\n        jobs.append({\"sent\": sents[sid], \"classes\": cl, \"cap_mult\": cap_mult})\n    logger.info(f\"{outp.name}: {n} classes to search over {len(jobs)} sentences ({len(done)} already done), {NUM_WORKERS} workers\")\n    t0 = time.time()\n    k = 0\n    with ProcessPoolExecutor(max_workers=NUM_WORKERS, mp_context=mp.get_context(\"spawn\")) as ex, outp.open(\"a\") as fh:\n        futs = {ex.submit(work_sentence, j): j[\"sent\"][\"sentence_id\"] for j in jobs}\n        for f in as_completed(futs):\n            try:\n                res = f.result()\n            except Exception as e:  # noqa: BLE001 - worker crash: the sentence is retried on the next resume\n                logger.error(f\"sentence {futs[f]} failed: {type(e).__name__}: {e}\")\n                continue\n            for r in res:\n                fh.write(json.dumps(r, ensure_ascii=False) + \"\\n\")\n                k += 1\n            fh.flush()\n            logger.info(f\"{k}/{n} classes, {time.time() - t0:.0f}s elapsed, {(time.time() - t0) / max(k, 1):.2f}s/class\")\n    logger.info(f\"done {k} classes in {time.time() - t0:.0f}s\")\n\n\ndef main() -> None:\n    resource.setrlimit(resource.RLIMIT_AS, (60 * 1024**3, 60 * 1024**3))\n    ap = argparse.ArgumentParser()\n    ap.add_argument(\"mode\", choices=[\"free\", \"sig\"])\n    ap.add_argument(\"--rename\", choices=[\"nonce\", \"syn\"])\n    ap.add_argument(\"--limit\", type=int)\n    ap.add_argument(\"--cap-mult\", type=int, default=1)\n    ap.add_argument(\"--out\")\n    a = ap.parse_args()\n    logger = setup_logger(f\"search_{a.mode}{'_' + a.rename if a.rename else ''}\")\n    sents = json.loads((WORK / \"sentences.json\").read_text())\n    by = defaultdict(dict)\n    if a.mode == \"free\":\n        for r in load_jsonl(WORK / \"free_rows.jsonl\"):\n            if r[\"input_status\"] == \"PARSED\":\n                by[r[\"sentence_id\"]][class_key(r[\"sentence_id\"], r[\"candidate_fol\"])] = r[\"candidate_fol\"]\n        outp = RES / (a.out or \"map_search.jsonl\")\n    else:\n        for r in load_jsonl(WORK / f\"sig_renamed_{a.rename}.jsonl\"):\n            by[r[\"sentence_id\"]][class_key(r[\"sentence_id\"], r[\"renamed_fol\"])] = r[\"renamed_fol\"]\n        outp = RES / (a.out or f\"sig_replay_{a.rename}.jsonl\")\n    classes = {sid: sorted(d.items()) for sid, d in by.items()}\n    run(classes, sents, outp, logger, a.limit, a.cap_mult)\n\n\nif __name__ == \"__main__\":\n    main()\n\"\"\"Shared paths, hashing and JSON helpers for the FREE name-free labeller (no metric, evaluator-model or aligner code here).\"\"\"\nfrom __future__ import annotations\n\nimport hashlib\nimport json\nimport re\nimport sys\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nfor _p in (ROOT / \"vendor\", ROOT / \"src\"):\n    if str(_p) not in sys.path:\n        sys.path.insert(0, str(_p))\nsys.setrecursionlimit(10000)\n\nRUN = Path(\"/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop\")\nE7 = RUN / \"iter_3/gen_art/gen_art_experiment_7\"\nD3 = RUN / \"iter_2/gen_art/gen_art_dataset_3\"\nGEN_FREE = E7 / \"rcomp/raw/generations.jsonl\"          # FREE raw generations: no scores, no labels\nSENTS = E7 / \"rcomp/work/rcomp_sentences.json\"\nD3_FULL = D3 / \"full_data_out.json\"\nLEXICON = D3 / \"lexicon.json\"\nSIG_LABELS = E7 / \"results/sig_labels.jsonl\"            # SIG labels only (pure z3), no scores\nOLD_CANDIDATES = E7 / \"results/rcomp_candidates.jsonl\"  # opened ONLY in STEP H (post-seal) via a whitelist loader\nNLTK_DATA = E7 / \"data/nltk_data\"\nRES = ROOT / \"results\"\nWORK = ROOT / \"work\"\nLOGS = ROOT / \"logs\"\nfor _d in (RES, WORK, LOGS):\n    _d.mkdir(exist_ok=True)\n\n\ndef sha1(s: str) -> str:\n    return hashlib.sha1(s.encode()).hexdigest()\n\n\ndef sha256_bytes(b: bytes) -> str:\n    return hashlib.sha256(b).hexdigest()\n\n\ndef sha256_file(p: Path) -> str:\n    return hashlib.sha256(Path(p).read_bytes()).hexdigest()\n\n\ndef norm_text(s: str) -> str:\n    \"\"\"Dataset E's select_sentences.norm (verbatim logic) used in the item_id recipe.\"\"\"\n    s = s.lower().replace(\"’\", \"'\").replace(\"‘\", \"'\").replace(\"“\", '\"').replace(\"”\", '\"')\n    s = re.sub(r\"[^a-z0-9 ]\", \" \", s)\n    return re.sub(r\"\\s+\", \" \", s).strip()\n\n\ndef item_id(system: str, text: str, raw: str | None) -> str:\n    \"\"\"exp 7 / dataset 3 recipe: sha1(system | norm(text) | raw_output)[:16] (raw None -> '').\"\"\"\n    return sha1(system + \"|\" + norm_text(text) + \"|\" + (raw or \"\"))[:16]\n\n\ndef load_jsonl(p: Path) -> list[dict]:\n    return [json.loads(l) for l in Path(p).read_text().splitlines() if l.strip()]\n\n\ndef dump(p: Path, obj) -> None:\n    Path(p).write_text(json.dumps(obj, indent=1, ensure_ascii=False))\n\n\ndef setup_logger(name: str):\n    from loguru import logger\n    logger.remove()\n    logger.add(sys.stdout, level=\"INFO\", format=\"{time:HH:mm:ss}|{level:<7}|{message}\")\n    logger.add(LOGS / f\"{name}.log\", rotation=\"30 MB\", level=\"DEBUG\")\n    return logger\n{\"row_key\": \"a81d2862772cd744|FREE|G1|fewshot_v1\", \"item_id\": \"a81d2862772cd744\", \"sentence_id\": \"001a7f0caf5a\", \"slot\": \"G1\", \"system\": \"G1:meta-llama/llama-3.1-8b-instruct\", \"family\": \"meta\", \"model\": \"meta-llama/llama-3.1-8b-instruct\", \"prompt_variant\": \"fewshot_v1\", \"raw_output\": \"FOL: ∀x ((Legislator(x) ∧ At(x, boardGameNight) ∧ RegularlyVisits(x, coffeeShop) ∧ CanDistinguish(x, differentCondiments)) → (Friend(x, emily) ∧ ¬ElectedOfficial(x)))\", \"candidate_fol\": \"∀x ((Legislator(x) ∧ At(x, boardGameNight) ∧ RegularlyVisits(x, coffeeShop) ∧ CanDistinguish(x, differentCondiments)) → (Friend(x, emily) ∧ ¬ElectedOfficial(x)))\", \"template_id\": \"T1\", \"clause_type\": \"unless\", \"words\": 34, \"word_tercile\": \"W2\", \"nconds_weak\": 5, \"negated_condition\": null, \"nested\": false, \"text\": \"Each legislator who is at Board Game night, who visits a coffee shop regularly, and who can distinguish the taste of different condiments is Emily's friend, except if the legislator is an elected official.\", \"class_key\": \"fcec8bf86a1f52a3\", \"search_status\": \"ERROR_CERT\", \"matched_reading_search\": null, \"n_maps_enumerated\": 0, \"n_maps_fingerprint_pass\": 0, \"n_equiv_maps\": 0, \"n_equiv_pairsets\": 0, \"n_equiv_map_orbits\": 0, \"nonequiv_certificate_type_counts\": {\"count_prune_subtree\": 291, \"no_polarity_compatible_target\": 10}, \"irrelevant_symbols\": [], \"search_secs\": 0.06, \"label_source\": \"exhaustive_map_v1\", \"label\": \"ERROR_CERT\", \"unresolved_reason\": null, \"map_certificate\": null, \"gloss_pairs\": null, \"gloss_decision\": null, \"label_binary\": \"ERROR\", \"seen_iter3\": false, \"old_label_iter3\": \"UNRESOLVED\", \"old_label_tier_iter3\": \"none\"}\n{\"row_key\": \"94bcb373f89b6d9a|FREE|G1b|fewshot_v1\", \"item_id\": \"94bcb373f89b6d9a\", \"sentence_id\": \"001a7f0caf5a\", \"slot\": \"G1b\", \"system\": \"G1b:meta-llama/llama-3.3-70b-instruct\", \"family\": \"meta\", \"model\": \"meta-llama/llama-3.3-70b-instruct\", \"prompt_variant\": \"fewshot_v1\", \"raw_output\": \"FOL: ∀x (Legislator(x) ∧ Attends(x, boardGameNight) ∧ Visits(x, coffeeShop) ∧ CanDistinguish(x, condiments) → (FriendOf(x, emily) ↔ ¬ElectedOfficial(x)))\", \"candidate_fol\": \"∀x (Legislator(x) ∧ Attends(x, boardGameNight) ∧ Visits(x, coffeeShop) ∧ CanDistinguish(x, condiments) → (FriendOf(x, emily) ↔ ¬ElectedOfficial(x)))\", \"template_id\": \"T1\", \"clause_type\": \"unless\", \"words\": 34, \"word_tercile\": \"W2\", \"nconds_weak\": 5, \"negated_condition\": null, \"nested\": false, \"text\": \"Each legislator who is at Board Game night, who visits a coffee shop regularly, and who can distinguish the taste of different condiments is Emily's friend, except if the legislator is an elected official.\", \"class_key\": \"3c418cac14221076\", \"search_status\": \"MAPPED\", \"matched_reading_search\": \"strong\", \"n_maps_enumerated\": 48, \"n_maps_fingerprint_pass\": 48, \"n_equiv_maps\": 48, \"n_equiv_pairsets\": 48, \"n_equiv_map_orbits\": 2, \"nonequiv_certificate_type_counts\": {\"count_prune_subtree\": 360}, \"irrelevant_symbols\": [], \"search_secs\": 0.336, \"labe\n{\n \"seals\": [\n  {\n   \"utc\": \"2026-09-24T07:37:10Z\",\n   \"mode\": \"search_only\",\n   \"label_vector_sha256_all_rows\": \"9609ebbb725832c467389e9d04b6334ca906ba10d400e7a7dccd976d39ebe3dd\",\n   \"n_rows\": 2652,\n   \"label_counts\": {\n    \"ERROR_CERT\": 759,\n    \"UNRESOLVED_GLOSS_NOT_RUN\": 1506,\n    \"UNPARSEABLE\": 188,\n    \"NO_OUTPUT\": 199\n   },\n   \"prereg_sha256\": \"b081c39991f52da2f419a6cefe56da48705d8abddf292d0faa89cec0b393a799\",\n   \"prereg_v1_sha256\": \"8ee7213d618be5be592464a9e0c83e40c5347a63ca5725283cdc4e0e70f51472\",\n   \"vendor_sha256\": {\n    \"__init__.py\": \"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855\",\n    \"fol.py\": \"e37a655f98af4899b1bdee943c66b395b27847870d6788b5509cf92ef3f95fe4\",\n    \"fol_triage_min.py\": \"b074c41135b8c1e7fe67057afab852b650b9c66426e061ce2eb93971705a212f\",\n    \"label_sig_min.py\": \"8b275ba5b710b5014e4a5a667b242cf74eb47565f29c886125179a936fae9e3e\",\n    \"perturb_min.py\": \"577e2fae8cecc0144dfc7931796ef3379ba90400db205bf9685d4d7bc39e3c4a\",\n    \"repair_census_min.py\": \"9a97cfbf0846aa395bf752cf0fca727a3229799650202e59e14e5f43e32533dc\",\n    \"sig_prompt_min.py\": \"95cbc1050e1fa48d81964adb0a4858838afc979b1744cf0c4fcb8d5c902a7cf5\",\n    \"templates.py\": \"4fe4ad153406142bd81ce4d283f80f342f3f5dd511eb1fea38380d6e469e0393\"\n   },\n   \"code_sha256\": {\n    \"src/freelab.py\": \"06e14f582c5aa793a4f66817b23fea135922c1d78fdffb5d362991a7ba348be3\",\n    \"src/run_search.py\": \"7f651c0b73710316a66fbf6156bf3dc3503b559fa081a7caf015ec9904e296c7\",\n    \"src/assemble_labels.py\": \"1a87d3da56066729d63013014558885622590230bd4073c40d26fad1bfcf4d3b\"\n   },\n   \"map_search_sha256\": \"4335677f141013396ddadec4d7a68f407e3373e89dc4b8f8222633db00820826\",\n   \"old_labels_joined\": false\n  },\n  {\n   \"utc\": \"2026-09-24T07:37:38Z\",\n   \"mode\": \"search_only\",\n   \"label_vector_sha256_all_rows\": \"9609ebbb725832c467389e9d04b6334ca906ba10d400e7a7dccd976d39ebe3dd\",\n   \"n_rows\": 2652,\n   \"label_counts\": {\n    \"ERROR_CERT\": 759,\n    \"UNRESOLVED_GLOSS_NOT_RUN\": 1506,\n    \"UNPARSEABLE\": 188,\n    \"NO_OUTPUT\": 199\n   },\n   \"prereg_sha256\": \"b081c39991f52da2f419a6cefe56da48705d8abddf292d0faa89cec0b393a799\",\n   \"prereg_v1_sha256\": \"8ee7213d618be5be592464a9e0c83e40c5347a63ca5725283cdc4e0e70f51472\",\n   \"vendor_sha256\": {\n    \"__init__.py\": \"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855\",\n    \"fol.py\": \"e37a655f98af4899b1bdee943c66b395b27847870d6788b5509cf92ef3f95fe4\",\n    \"fol_triage_min.py\": \"b074c41135b8c1e7fe67057afab852b650b9c66426e061ce2eb93971705a212f\",\n    \"label_sig_min.py\": \"", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [16] TOOL CALL — Bash · 2026-09-24 19:19:02 UTC

```
A=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5; python3 -c "
import json
t=json.load(open('$A/results/testability_FREE_v2.json'))
def sk(d,ind=0):
  for k,v in d.items():
    print(' '*ind+k, type(v).__name__, (v if not isinstance(v,(dict,list)) else ''))
    if isinstance(v,dict) and ind<4: sk(v,ind+2)
sk(t)
" | head -80
```

### [17] TOOL RESULT — Bash · 2026-09-24 19:19:02 UTC

```
{"stdout": "mode str search_only\nutc str 2026-09-24T07:37:10Z\nrule str TESTABLE iff >= 50 ERROR and >= 50 CORRECT rows, each class spread over >= 25 sentences\nword_terciles dict \n  cut_1 int 30\n  cut_2 int 35\nall_rows dict \n  population str all FREE rows\n  n_rows int 2652\n  n_ERROR int 759\n  n_CORRECT int 0\n  sentences_with_ERROR int 208\n  sentences_with_CORRECT int 0\n  TESTABLE bool False\n  reportable_30_30 bool False\n  label_counts dict \n    ERROR_CERT int 759\n    UNRESOLVED_GLOSS_NOT_RUN int 1506\n    UNPARSEABLE int 188\n    NO_OUTPUT int 199\n  strata dict \n    template_id dict \n    clause_type dict \n    word_tercile dict \n    prompt_variant dict \n    slot dict \nuntouched_subset dict \n  population str untouched subset (not tier-A labelled in iteration 3) - PRIMARY\n  n_rows int 2198\n  n_ERROR int 636\n  n_CORRECT int 0\n  sentences_with_ERROR int 199\n  sentences_with_CORRECT int 0\n  TESTABLE bool False\n  reportable_30_30 bool False\n  label_counts dict \n    ERROR_CERT int 636\n    UNRESOLVED_GLOSS_NOT_RUN int 1175\n    UNPARSEABLE int 188\n    NO_OUTPUT int 199\n  strata dict \n    template_id dict \n    clause_type dict \n    word_tercile dict \n    prompt_variant dict \n    slot dict \nnote str SEARCH-ONLY labels (D9): no CORRECT class exists until the gloss step runs, so AUROC is NOT_TESTABLE; the ERROR_CERT class alone supports recall-type analyses; MAPPED rows are UNRESOLVED_GLOSS_NOT_RUN\nseen_iter3_subset dict \n  population str seen_iter3 subset\n  n_rows int 454\n  n_ERROR int 123\n  n_CORRECT int 0\n  sentences_with_ERROR int 71\n  sentences_with_CORRECT int 0\n  TESTABLE bool False\n  reportable_30_30 bool False\n  label_counts dict \n    UNRESOLVED_GLOSS_NOT_RUN int 331\n    ERROR_CERT int 123\n  strata dict \n    template_id dict \n    clause_type dict \n    word_tercile dict \n    prompt_variant dict \n    slot dict \nsearch_provisional_view dict \n  definition str class 'CORRECT' in this block = MAPPED (search-level, NOT gloss-checked); ERROR = ERROR_CERT\n  all_rows dict \n    population str all FREE rows, provisional ERROR_CERT vs MAPPED\n    n_rows int 2652\n    n_ERROR int 759\n    n_CORRECT int 1506\n    sentences_with_ERROR int 208\n    sentences_with_CORRECT int 215\n    TESTABLE bool True\n    reportable_30_30 bool True\n    label_counts dict \n    strata dict \n    auroc_se_at_0.75 float 0.0114\n    auroc_mde_approx float 0.032", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [18] ASSISTANT · 2026-09-24 19:19:12 UTC

```
Building the demo subset now: up to 100 raw label rows, stratified across the four label classes, plus the seal and testability records that `data.py` reads.
```

### [19] TOOL CALL — Bash · 2026-09-24 19:19:12 UTC

```
cd /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_Ia_FT284H33j; A=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5; python3 - <<EOF
import json, random
from collections import defaultdict
A="$A"
rows=[json.loads(l) for l in open(A+"/results/free_labels_v2.jsonl") if l.strip()]
by=defaultdict(list)
for r in rows: by[r["label"]].append(r)
rng=random.Random(0)
quota={"ERROR_CERT":34,"UNRESOLVED_GLOSS_NOT_RUN":34,"UNPARSEABLE":16,"NO_OUTPUT":16}
sel=[]
for lab,q in quota.items():
    pool=by[lab][:]; rng.shuffle(pool)
    # diversify: round-robin over (family, clause_type)
    seen=defaultdict(int); pick=[]
    for r in sorted(pool,key=lambda r:0):
        pass
    groups=defaultdict(list)
    for r in pool: groups[(r["family"],r["clause_type"])].append(r)
    keys=sorted(groups); i=0
    while len(pick)<q and any(groups.values()):
        k=keys[i%len(keys)]; i+=1
        if groups[k]: pick.append(groups[k].pop())
    sel+=pick
# ensure some seen_iter3 rows
print(len(sel), sum(r["seen_iter3"] for r in sel))
seal=json.load(open(A+"/results/seal.json"))
t=json.load(open(A+"/results/testability_FREE_v2.json"))
keep=("population","n_rows","n_ERROR","n_CORRECT","TESTABLE","label_counts")
tt={"all_rows":{k:t["all_rows"][k] for k in keep},"untouched_subset":{k:t["untouched_subset"][k] for k in keep},
    "search_provisional_view":{k:{kk:t["search_provisional_view"][k][kk] for kk in keep} for k in ("all_rows","untouched_subset")}}
out={"description":"Demo subset for art_Ia_FT284H33j: 100 raw FREE label rows (results/free_labels_v2.jsonl, stratified by label x family x clause_type, seed 0) + the seal record and the testability summary (strata dropped) that data.py reads. Source counts are for the full 2,652-row dataset.",
     "free_labels_rows":sel,"seal":{"seals":[seal["seals"][-1]]},"testability_FREE_v2":tt}
json.dump(out,open("mini_demo_data.json","w"),ensure_ascii=False,indent=1)
from collections import Counter
print(Counter(r["label"] for r in sel), Counter(r["family"] for r in sel), Counter(r["clause_type"] for r in sel))
EOF
ls -la mini_demo_data.json
```

### [20] TOOL RESULT — Bash · 2026-09-24 19:19:12 UTC

```
{"stdout": "100 12\nCounter({'ERROR_CERT': 34, 'UNRESOLVED_GLOSS_NOT_RUN': 34, 'UNPARSEABLE': 16, 'NO_OUTPUT': 16}) Counter({'cohere': 20, 'deepseek': 20, 'google-gemini': 17, 'meta': 15, 'google-gemma': 14, 'qwen': 14}) Counter({'provided_that+unless': 16, 'except_when+provided_that': 15, 'as_long_as+unless': 14, 'except_when': 14, 'provided_that': 14, 'unless': 14, 'but_only_if': 13})\n-rw-r--r-- 1 root root 274798 Sep 24 19:19 mini_demo_data.json", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [21] TOOL CALL — Bash · 2026-09-24 19:19:22 UTC

```
mkdir -p /tmp/claude-0/-ai-inventor-aii-data-runs-run-u75jRHUss0zo-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-4-art-Ia-FT284H33j/0edcdb6e-4812-423c-84c8-8f0363de97de/scratchpad
```

### [22] TOOL RESULT — Bash · 2026-09-24 19:19:22 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": true}
```

### [23] TOOL CALL — Write · 2026-09-24 19:20:26 UTC

```
File: /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_Ia_FT284H33j/make_nb.py

"""Builds code_demo.ipynb from the original data.py + src/build_output.py (cells + markdown). usage: python3 make_nb.py"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
cells = []


def md(s):
    cells.append({"cell_type": "markdown", "metadata": {}, "source": s.strip("\n")})


def code(s):
    cells.append({"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": s.strip("\n")})


md(r"""
# Name-free labels for free-vocabulary NL→FOL translations — dataset demo

This notebook is a walkthrough of the **dataset-building script** (`data.py` + the `free_group()` builder from `src/build_output.py`)
for artifact *T7b: name-free labels for R_COMP FREE rule translations*.

**Setting.** 221 templated English rules ("Each legislator who … is Emily's friend, except if …") were translated to first-order
logic by 10 LLM slots from 9 model families, with a **free vocabulary**: each model picks its own predicate names and
decompositions. That rules out exact match against a gold formula. Each candidate is labelled by an **exhaustive, name-free map search**:

* every injective map from the candidate's symbols to the template's atoms is enumerated. The map family also allows
  reification (B1/B2), merge (B3), split (B4) and lexical negation (B5);
* sound prunes (relevance, polarity, and a 128-model finite **countermodel** fingerprint) discard maps; z3 proves equivalence for any map that survives;
* **`ERROR_CERT`**: *no* map in the family makes the candidate equivalent to the template reading. This label is final and backed by certificates;
* **`UNRESOLVED_GLOSS_NOT_RUN`** (search level: `MAPPED`): some map makes it z3-equivalent. A gloss check ("does `Attends(x, boardGameNight)`
  really mean *x is at Board Game night*?") still has to accept that map. That check did not run because the OpenRouter budget ran out (deviation D9);
* `UNPARSEABLE` / `NO_OUTPUT`: coverage rows. They are counted and reported, never dropped.

The full dataset has 2,652 FREE rows. This demo loads **100 raw label rows** (stratified by label × model family × clause type)
together with the seal and testability records that `data.py` reads, and then runs the original assembly code on them
(the name-free search itself is `src/freelab.py`; its results are the inputs here).
""")

code(r"""
import subprocess, sys
def _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])

# loguru — NOT on Colab, always install (original data.py dependency)
_pip('loguru==0.7.3')

# pandas, matplotlib — pre-installed on Colab, install locally only (used by the summary / visualization cells)
if 'google.colab' not in sys.modules:
    _pip('numpy==2.0.2', 'pandas==2.2.2', 'matplotlib==3.10.0')
""")

md(r"""
## Imports and logging
These are the original `data.py` imports and loguru setup. `ROOT` was `Path(__file__).parent`; in a notebook it is the current directory.
The `sys.path` inserts for `src/` and `vendor/` are gone because the one builder we need (`free_group`) is inlined below.
""")

code(r"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(".").resolve()  # was: Path(__file__).resolve().parent

from loguru import logger  # noqa: E402

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
(ROOT / "logs").mkdir(exist_ok=True)
logger.add(ROOT / "logs" / "data.log", rotation="30 MB", level="DEBUG")

# extra imports for the summary / visualization cells
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
""")

md("## Data loading\nLoads `mini_demo_data.json` from GitHub, with a fallback to a local copy.")

code(r'''
GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/main/round-4/dataset-5/demo/mini_demo_data.json"
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

code(r"""
data = load_data()
print(data["description"])
print("raw FREE label rows available:", len(data["free_labels_rows"]))
""")

md(r"""
## Config
`data.py` has no numeric hyper-parameters: it assembles labels that have already been computed. The one knob is how many raw label rows to assemble.
The original run uses all 2,652 rows from `results/free_labels_v2.jsonl`. This demo file holds 100 of them.
`SELECTED` is the original list of output groups.
""")

code(r"""
N_ROWS = 100          # raw FREE label rows to assemble (demo file holds 100; original full run: 2652)
SELECTED = ["rcomp_free_labels", "gloss_gate_items", "sig_soundness_replay"]  # original data.py value
""")

md(r"""
## Row builder: `free_group()` (from `src/build_output.py`)
Each raw label row becomes one `exp_sel_data_out` example:
* `input` is a JSON string holding the sentence, the candidate FOL and which system produced it (slot, family, prompt variant);
* `output` is the name-free label (`ERROR_CERT`, `UNRESOLVED_GLOSS_NOT_RUN`, `UNPARSEABLE` or `NO_OUTPUT`);
* the `metadata_*` fields carry the strata (template, clause type, word tercile, …), the **map certificate** (which candidate symbol maps to which
  template atom, and which bridges were used), the counts of non-equivalence certificates, and the `gloss_pairs` that the checker will judge.

`label_binary_search_provisional` collapses the label to `ERROR` / `MAPPED` / `EXCLUDED`. That provisional binary view is the one that is currently
testable, because no `CORRECT` class exists until the gloss step runs.

The only change from the original is the first line: rows come from the loaded `data` instead of `load_jsonl(RES / "free_labels_v2.jsonl")`.
""")

code(r'''
def md(d: dict) -> dict:
    return {f"metadata_{k}": v for k, v in d.items()}


def free_group() -> dict:
    rows = data["free_labels_rows"][:N_ROWS]  # was: load_jsonl(RES / "free_labels_v2.jsonl")
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

md(r"""
### The other two groups (reference only, not run here)
The full `full_data_out.json` also has `gloss_gate_items`: 840 known-answer (symbol use, meaning) items used to validate the gloss checker.
It also has `sig_soundness_replay`: 4,280 renamed SIG rows with known pure-z3 labels, used to test the search's soundness under renaming.
Their builders are below, unchanged from `src/build_output.py`. They read run-local files (`results/gate_items.json`, `results/sig_replay_rows.jsonl`,
`work/sentences.json`), and the demo file (one dataset only) does not include those, so the builders are defined here but never called.
""")

code(r'''
RES, WORK = ROOT / "results", ROOT / "work"  # original paths (src/common.py); not present in the demo


def load_jsonl(p: Path) -> list[dict]:
    return [json.loads(l) for l in Path(p).read_text().splitlines() if l.strip()]


def gate_group() -> dict:
    items = json.loads((RES / "gate_items.json").read_text())
    ex = []
    for i in items:
        inp = {"sentence": i["sentence"], "candidate_atom": i["candidate_atom"], "proposed_meaning": i["proposed_meaning"]}
        meta = {"item_id": i["item_id"], "class": i["class"], "half": i["half"], "sentence_id": i["sentence_id"],
                "template_id": i["template_id"], "note": i["note"], "prompt_version": "gloss_v1",
                "haiku_verdict": i.get("haiku_gloss_v1"), "qwen_verdict": i.get("qwen_gloss_v1"), "fold": "GLOSS_GATE"}
        ex.append({"input": json.dumps(inp, ensure_ascii=False), "output": i["gold"], **md(meta)})
    return {"dataset": "gloss_gate_items", "examples": ex}


def sig_group() -> dict:
    sents = json.loads((WORK / "sentences.json").read_text())
    rows = load_jsonl(RES / "sig_replay_rows.jsonl")
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

md(r"""
## `main()` from `data.py`: assemble, validate, attach seal and testability
The original steps: build the groups; check the schema (string `input`/`output`, no reserved keys); read the last **seal** (sha256 of the label vector,
pre-registration hash) and the **testability** summary; write `full_data_out.json`.

Demo changes:
* `groups` holds only `free_group()`, the one group in the demo file (the original line is kept as a comment);
* `seal` and `t` come from `data` instead of `results/seal.json` and `results/testability_FREE_v2.json`. Their values describe the **full** 2,652-row dataset;
* the output file is named `demo_full_data_out.json` so it cannot be confused with the real artifact.
""")

code(r'''
@logger.catch(reraise=True)
def main() -> None:
    # groups = [B.free_group(), B.gate_group(), B.sig_group()]   # original (needs run-local files)
    groups = [free_group()]
    for g in groups:
        assert g["examples"], g["dataset"]
        for e in g["examples"]:
            assert isinstance(e["input"], str) and isinstance(e["output"], str), g["dataset"]
            assert not ({"split", "dataset", "context"} & set(e)), g["dataset"]
    seal = data["seal"]["seals"][-1]          # was: json.loads((ROOT / "results" / "seal.json").read_text())["seals"][-1]
    t = data["testability_FREE_v2"]           # was: json.loads((ROOT / "results" / "testability_FREE_v2.json").read_text())
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
    (ROOT / "demo_full_data_out.json").write_text(json.dumps(out, ensure_ascii=False))  # was: full_data_out.json
    logger.info(f"demo_full_data_out.json: {[(g['dataset'], len(g['examples'])) for g in out['datasets']]}")
    return out  # (added) keep the result for the summary cells


out = main()
''')

md(r"""
## Results: what the labels look like
First, the dataset-level metadata from the seal and testability summary. These numbers describe the **full** 2,652 rows, not the demo subset.
With search-only labels there is no `CORRECT` class yet, so AUROC is NOT_TESTABLE. The provisional ERROR_CERT-vs-MAPPED view *is* testable.
""")

code(r'''
m = out["metadata"]
print("label_mode:", m["label_mode"])
print("seal (all rows):  ", m["seal_all_rows_sha256"][:16], "...")
print("seal (untouched): ", (m["seal_untouched_sha256"] or "")[:16], "...")
print("prereg sha256:    ", m["prereg_sha256"][:16], "...")
full_tab = pd.DataFrame({
    "all rows (2,652)": m["testability_all_rows"]["label_counts"],
    "untouched (2,198, primary)": m["testability_untouched"]["label_counts"],
}).fillna(0).astype(int)
print("\nFULL-dataset label counts:\n", full_tab.to_string())
print("\nTESTABLE (ERROR vs CORRECT):", m["testability_all_rows"]["TESTABLE"],
      "| provisional ERROR_CERT vs MAPPED view TESTABLE:", m["provisional_view_testable"])
''')

md("Next, the assembled demo rows: labels by model family and by clause type, plus two example rows with their certificates.")

code(r'''
ex = out["datasets"][0]["examples"]
df = pd.DataFrame([{**json.loads(e["input"]), "label": e["output"],
                    **{k[9:]: v for k, v in e.items() if k.startswith("metadata_")}} for e in ex])
print(f"{len(df)} assembled rows | label counts: {dict(Counter(df['label']))}")
print("\nlabel x family:\n", pd.crosstab(df["family"], df["label"]).to_string())
print("\nsearch-provisional binary x clause type:\n",
      pd.crosstab(df["clause_type"], df["label_binary_search_provisional"]).to_string())

for lab in ("ERROR_CERT", "UNRESOLVED_GLOSS_NOT_RUN"):
    sub = df[df["label"] == lab]
    if len(sub) == 0:
        continue
    r = sub.iloc[0]
    print(f"\n=== example {lab} ({r['system']}) ===")
    print("TEXT:", r["text"])
    print("FOL: ", r["candidate_fol"])
    print("maps enumerated:", r["n_maps_enumerated"], "| equivalent maps:", r["n_equiv_maps"],
          "| non-equiv certificates:", r["nonequiv_certificate_type_counts"])
    if r["map_certificate"]:
        print("map certificate (reading =", r["map_certificate"]["reading"], ", bridges =", r["map_certificate"]["bridges"], "):")
        for mline in r["map_certificate"]["map"]:
            print("   ", mline)
        print("gloss pairs pending check:", [(g["cand_atom"], g["meaning"]) for g in r["gloss_pairs"]])
''')

code(r'''
order = ["ERROR_CERT", "UNRESOLVED_GLOSS_NOT_RUN", "UNPARSEABLE", "NO_OUTPUT"]
colors = ["#c0504d", "#4f81bd", "#9b9b9b", "#d9d9d9"]
fig, ax = plt.subplots(1, 3, figsize=(17, 4.6))

# (a) full-dataset label distribution (from the seal) vs demo subset
full = m["testability_all_rows"]["label_counts"]
ax[0].bar(order, [full.get(k, 0) for k in order], color=colors)
for i, k in enumerate(order):
    ax[0].text(i, full.get(k, 0), str(full.get(k, 0)), ha="center", va="bottom", fontsize=9)
ax[0].set_title("(a) Full dataset: 2,652 FREE rows")
ax[0].set_ylabel("rows")
ax[0].tick_params(axis="x", rotation=20)

# (b) provisional ERROR/MAPPED share per model family in the demo subset
ct = pd.crosstab(df["family"], df["label"]).reindex(columns=order, fill_value=0)
ct.plot(kind="barh", stacked=True, color=colors, ax=ax[1], legend=False)
ax[1].set_title(f"(b) Demo subset ({len(df)} rows) by model family")
ax[1].set_xlabel("rows")
ax[1].legend(fontsize=8, loc="lower right")

# (c) search effort: maps enumerated vs label (parseable rows only)
p = df[df["label"].isin(order[:2])]
for lab, c in zip(order[:2], colors[:2]):
    s = p[p["label"] == lab]
    ax[2].scatter(s["words"], s["search_secs"], label=lab, color=c, alpha=0.7, s=25)
ax[2].set_yscale("log")
ax[2].set_xlabel("sentence length (words)")
ax[2].set_ylabel("exhaustive search time (s, log)")
ax[2].set_title("(c) Search cost vs sentence length")
ax[2].legend(fontsize=8)
plt.tight_layout()
plt.show()
''')

md(r"""
**How to read this.**
* `ERROR_CERT` rows are final. No map in the declared family (injective maps plus the B1–B5 bridges) makes the candidate z3-equivalent to any
  template reading, and every rejected map has a certificate: a pruned subtree, a polarity conflict, or a finite countermodel. The executor audit
  gives ERROR_CERT a precision of 0.867. Its misses are faithful forms outside the family, such as a disjunctive split or ∃-for-constant.
* `UNRESOLVED_GLOSS_NOT_RUN` rows *can* be made equivalent. Whether the winning map is lexically plausible is decided by the pending gloss
  check (`src/resume_gloss.py`), which turns these rows into CORRECT or ERROR. In the SIG replay, non-identity maps rescued 9–10% of known-ERROR rows,
  and those are the cases the gloss check must stop.
* Search is cheap: fractions of a second per candidate. The gloss check is the only paid step (~$1.8 for the whole audit).
""")

nb = {"cells": cells, "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                                   "language_info": {"name": "python"}}, "nbformat": 4, "nbformat_minor": 5}
for i, c in enumerate(nb["cells"]):
    c["id"] = f"c{i:02d}"
(HERE / "code_demo.ipynb").write_text(json.dumps(nb, indent=1, ensure_ascii=False))
print("wrote code_demo.ipynb with", len(cells), "cells")
```

### [24] TOOL RESULT — Write · 2026-09-24 19:20:26 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_Ia_FT284H33j/make_nb.py", "content": "\"\"\"Builds code_demo.ipynb from the original data.py + src/build_output.py (cells + markdown). usage: python3 make_nb.py\"\"\"\nimport json\nfrom pathlib import Path\n\nHERE = Path(__file__).resolve().parent\ncells = []\n\n\ndef md(s):\n    cells.append({\"cell_type\": \"markdown\", \"metadata\": {}, \"source\": s.strip(\"\\n\")})\n\n\ndef code(s):\n    cells.append({\"cell_type\": \"code\", \"metadata\": {}, \"execution_count\": None, \"outputs\": [], \"source\": s.strip(\"\\n\")})\n\n\nmd(r\"\"\"\n# Name-free labels for free-vocabulary NL→FOL translations — dataset demo\n\nThis notebook is a walkthrough of the **dataset-building script** (`data.py` + the `free_group()` builder from `src/build_output.py`)\nfor artifact *T7b: name-free labels for R_COMP FREE rule translations*.\n\n**Setting.** 221 templated English rules (\"Each legislator who … is Emily's friend, except if …\") were translated to first-order\nlogic by 10 LLM slots from 9 model families, with a **free vocabulary**: each model picks its own predicate names and\ndecompositions. That rules out exact match against a gold formula. Each candidate is labelled by an **exhaustive, name-free map search**:\n\n* every injective map from the candidate's symbols to the template's atoms is enumerated. The map family also allows\n  reification (B1/B2), merge (B3), split (B4) and lexical negation (B5);\n* sound prunes (relevance, polarity, and a 128-model finite **countermodel** fingerprint) discard maps; z3 proves equivalence for any map that survives;\n* **`ERROR_CERT`**: *no* map in the family makes the candidate equivalent to the template reading. This label is final and backed by certificates;\n* **`UNRESOLVED_GLOSS_NOT_RUN`** (search level: `MAPPED`): some map makes it z3-equivalent. A gloss check (\"does `Attends(x, boardGameNight)`\n  really mean *x is at Board Game night*?\") still has to accept that map. That check did not run because the OpenRouter budget ran out (deviation D9);\n* `UNPARSEABLE` / `NO_OUTPUT`: coverage rows. They are counted and reported, never dropped.\n\nThe full dataset has 2,652 FREE rows. This demo loads **100 raw label rows** (stratified by label × model family × clause type)\ntogether with the seal and testability records that `data.py` reads, and then runs the original assembly code on them\n(the name-free search itself is `src/freelab.py`; its results are the inputs here).\n\"\"\")\n\ncode(r\"\"\"\nimport subprocess, sys\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\n\n# loguru — NOT on Colab, always install (original data.py dependency)\n_pip('loguru==0.7.3')\n\n# pandas, matplotlib — pre-installed on Colab, install locally only (used by the summary / visualization cells)\nif 'google.colab' not in sys.modules:\n    _pip('numpy==2.0.2', 'pandas==2.2.2', 'matplotlib==3.10.0')\n\"\"\")\n\nmd(r\"\"\"\n## Imports and logging\nThese are the original `data.py` imports and loguru setup. `ROOT` was `Path(__file__).parent`; in a notebook it is the current directory.\nThe `sys.path` inserts for `src/` and `vendor/` are gone because the one builder we need (`free_group`) is inlined below.\n\"\"\")\n\ncode(r\"\"\"\nfrom __future__ import annotations\n\nimport json\nimport sys\nfrom pathlib import Path\n\nROOT = Path(\".\").resolve()  # was: Path(__file__).resolve().parent\n\nfrom loguru import logger  # noqa: E402\n\nlogger.remove()\nlogger.add(sys.stdout, level=\"INFO\", format=\"{time:HH:mm:ss}|{level:<7}|{message}\")\n(ROOT / \"logs\").mkdir(exist_ok=True)\nlogger.add(ROOT / \"logs\" / \"data.log\", rotation=\"30 MB\", level=\"DEBUG\")\n\n# extra imports for the summary / visualization cells\nfrom collections import Counter\nimport pandas as pd\nimport matplotlib.pyplot as plt\n\"\"\")\n\nmd(\"## Data loading\\nLoads `mini_demo_data.json` from GitHub, with a fallback to a local copy.\")\n\ncode(r'''\nGITHUB_DATA_URL = \"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/main/round-4/dataset-5/demo/mini_demo_data.json\"\nimport json\nfrom pathlib import Path\n\ndef load_data():\n    try:\n        import urllib.request\n        with urllib.request.urlopen(GITHUB_DATA_URL) as response:\n            return json.loads(response.read().decode())\n    except Exception: pass\n    local = Path(\"mini_demo_data.json\")\n    if local.exists(): return json.loads(local.read_text())\n    raise FileNotFoundError(\"Could not load mini_demo_data.json\")\n''')\n\ncode(r\"\"\"\ndata = load_data()\nprint(data[\"description\"])\nprint(\"raw FREE label rows available:\", len(data[\"free_labels_rows\"]))\n\"\"\")\n\nmd(r\"\"\"\n## Config\n`data.py` has no numeric hyper-parameters: it assembles labels that have already been computed. The one knob is how many raw label rows to assemble.\nThe original run uses all 2,652 rows from `results/free_labels_v2.jsonl`. This demo file holds 100 of them.\n`SELECTED` is the original list of output groups.\n\"\"\")\n\ncode(r\"\"\"\nN_ROWS = 100          # raw FREE label rows to assemble (demo file holds 100; original full run: 2652)\nSELECTED = [\"rcomp_free_labels\", \"gloss_gate_items\", \"sig_soundness_replay\"]  # original data.py value\n\"\"\")\n\nmd(r\"\"\"\n## Row builder: `free_group()` (from `src/build_output.py`)\nEach raw label row becomes one `exp_sel_data_out` example:\n* `input` is a JSON string holding the sentence, the candidate FOL and which system produced it (slot, family, prompt variant);\n* `output` is the name-free label (`ERROR_CERT`, `UNRESOLVED_GLOSS_NOT_RUN`, `UNPARSEABLE` or `NO_OUTPUT`);\n* the `metadata_*` fields carry the strata (template, clause type, word tercile, …), the **map certificate** (which candidate symbol maps to which\n  template atom, and which bridges were used), the counts of non-equivalence certificates, and the `gloss_pairs` that the checker will judge.\n\n`label_binary_search_provisional` collapses the label to `ERROR` / `MAPPED` / `EXCLUDED`. That provisional binary view is the one that is currently\ntestable, because no `CORRECT` class exists until the gloss step runs.\n\nThe only change from the original is the first line: rows come from the loaded `data` instead of `load_jsonl(RES / \"free_labels_v2.jsonl\")`.\n\"\"\")\n\ncode(r'''\ndef md(d: dict) -> dict:\n    return {f\"metadata_{k}\": v for k, v in d.items()}\n\n\ndef free_group() -> dict:\n    rows = data[\"free_labels_rows\"][:N_ROWS]  # was: load_jsonl(RES / \"free_labels_v2.jsonl\")\n    ex = []\n    for r in rows:\n        inp = {\"text\": r[\"text\"], \"candidate_fol\": r[\"candidate_fol\"], \"system\": r[\"system\"], \"family\": r[\"family\"],\n               \"slot\": r[\"slot\"], \"prompt_variant\": r[\"prompt_variant\"], \"condition\": \"FREE\", \"template_id\": r[\"template_id\"]}\n        search_bin = {\"ERROR_CERT\": \"ERROR\", \"UNRESOLVED_GLOSS_NOT_RUN\": \"MAPPED\"}.get(r[\"label\"], \"EXCLUDED\")\n        meta = {\n            \"row_key\": r[\"row_key\"], \"item_id\": r[\"item_id\"], \"sentence_id\": r[\"sentence_id\"], \"template_id\": r[\"template_id\"],\n            \"clause_type\": r[\"clause_type\"], \"words\": r[\"words\"], \"word_tercile\": r[\"word_tercile\"],\n            \"nconds_weak\": r[\"nconds_weak\"], \"negated_condition\": r[\"negated_condition\"], \"nested\": r[\"nested\"],\n            \"label_binary\": r[\"label_binary\"], \"label_binary_search_provisional\": search_bin,\n            \"label_source\": r[\"label_source\"], \"search_status\": r.get(\"search_status\"),\n            \"matched_reading\": r.get(\"matched_reading\") or r.get(\"matched_reading_search\"),\n            \"map_certificate\": r.get(\"map_certificate\"),\n            \"n_maps_enumerated\": r.get(\"n_maps_enumerated\"), \"n_maps_fingerprint_pass\": r.get(\"n_maps_fingerprint_pass\"),\n            \"n_equiv_maps\": r.get(\"n_equiv_maps\"), \"n_equiv_map_orbits\": r.get(\"n_equiv_map_orbits\"),\n            \"nonequiv_certificate_type_counts\": r.get(\"nonequiv_certificate_type_counts\"),\n            \"gloss_pairs\": r.get(\"gloss_pairs\"), \"gloss_decision\": r.get(\"gloss_decision\"),\n            \"unresolved_reason\": r.get(\"unresolved_reason\"), \"irrelevant_symbols\": r.get(\"irrelevant_symbols\"),\n            \"search_secs\": r.get(\"search_secs\"), \"seen_iter3\": r.get(\"seen_iter3\"),\n            \"old_label_iter3\": r.get(\"old_label_iter3\"), \"fold\": \"RCOMP_FREE\"}\n        ex.append({\"input\": json.dumps(inp, ensure_ascii=False), \"output\": r[\"label\"], **md(meta)})\n    return {\"dataset\": \"rcomp_free_labels\", \"examples\": ex}\n''')\n\nmd(r\"\"\"\n### The other two groups (reference only, not run here)\nThe full `full_data_out.json` also has `gloss_gate_items`: 840 known-answer (symbol use, meaning) items used to validate the gloss checker.\nIt also has `sig_soundness_replay`: 4,280 renamed SIG rows with known pure-z3 labels, used to test the search's soundness under renaming.\nTheir builders are below, unchanged from `src/build_output.py`. They read run-local files (`results/gate_items.json`, `results/sig_replay_rows.jsonl`,\n`work/sentences.json`), and the demo file (one dataset only) does not include those, so the builders are defined here but never called.\n\"\"\")\n\ncode(r'''\nRES, WORK = ROOT / \"results\", ROOT / \"work\"  # original paths (src/common.py); not present in the demo\n\n\ndef load_jsonl(p: Path) -> list[dict]:\n    return [json.loads(l) for l in Path(p).read_text().splitlines() if l.strip()]\n\n\ndef gate_group() -> dict:\n    items = json.loads((RES / \"gate_items.json\").read_text())\n    ex = []\n    for i in items:\n        inp = {\"sentence\": i[\"sentence\"], \"candidate_atom\": i[\"candidate_atom\"], \"proposed_meaning\": i[\"proposed_meaning\"]}\n        meta = {\"item_id\": i[\"item_id\"], \"class\": i[\"class\"], \"half\": i[\"half\"], \"sentence_id\": i[\"sentence_id\"],\n                \"template_id\": i[\"template_id\"], \"note\": i[\"note\"], \"prompt_version\": \"gloss_v1\",\n                \"haiku_verdict\": i.get(\"haiku_gloss_v1\"), \"qwen_verdict\": i.get(\"qwen_gloss_v1\"), \"fold\": \"GLOSS_GATE\"}\n        ex.append({\"input\": json.dumps(inp, ensure_ascii=False), \"output\": i[\"gold\"], **md(meta)})\n    return {\"dataset\": \"gloss_gate_items\", \"examples\": ex}\n\n\ndef sig_group() -> dict:\n    sents = json.loads((WORK / \"sentences.json\").read_text())\n    rows = load_jsonl(RES / \"sig_replay_rows.jsonl\")\n    ex = []\n    for r in rows:\n        inp = {\"text\": sents[r[\"sentence_id\"]][\"text\"], \"candidate_fol\": r[\"renamed_fol\"], \"rename\": r[\"rename\"],\n               \"template_id\": r[\"template_id\"]}\n        meta = {k: r[k] for k in (\"row_key\", \"sentence_id\", \"slot\", \"template_id\", \"sig_matched_reading\", \"canon_fol\",\n                                  \"search_status\", \"identity_map_found\", \"non_identity_map_found\", \"n_equiv_maps\",\n                                  \"n_equiv_map_orbits\", \"n_maps_enumerated\", \"nonequiv_certificate_type_counts\",\n                                  \"oracle_end_to_end_label\", \"in_e2e_gloss_subsample_300\", \"e2e_gloss_label\")}\n        meta[\"map_equiv_found\"] = r[\"search_status\"] in (\"MAPPED\", \"READING_CHOICE\")\n        meta[\"fold\"] = f\"SIG_REPLAY_{r['rename'].upper()}\"\n        ex.append({\"input\": json.dumps(inp, ensure_ascii=False), \"output\": r[\"sig_label\"], **md(meta)})\n    return {\"dataset\": \"sig_soundness_replay\", \"examples\": ex}\n''')\n\nmd(r\"\"\"\n## `main()` from `data.py`: assemble, validate, attach seal and testability\nThe original steps: build the groups; check the schema (string `input`/`output`, no reserved keys); read the last **seal** (sha256 of the label vector,\npre-registration hash) and the **testability** summary; write `full_data_out.json`.\n\nDemo changes:\n* `groups` holds only `free_group()`, the one group in the demo file (the original line is kept as a comment);\n* `seal` and `t` come from `data` instead of `results/seal.json` and `results/testability_FREE_v2.json`. Their values describe the **full** 2,652-row dataset;\n* the output file is named `demo_full_data_out.json` so it cannot be confused with the real artifact.\n\"\"\")\n\ncode(r'''\n@logger.catch(reraise=True)\ndef main() -> None:\n    # groups = [B.free_group(), B.gate_group(), B.sig_group()]   # original (needs run-local files)\n    groups = [free_group()]\n    for g in groups:\n        assert g[\"examples\"], g[\"dataset\"]\n        for e in g[\"examples\"]:\n            assert isinstance(e[\"input\"], str) and isinstance(e[\"output\"], str), g[\"dataset\"]\n            assert not ({\"split\", \"dataset\", \"context\"} & set(e)), g[\"dataset\"]\n    seal = data[\"seal\"][\"seals\"][-1]          # was: json.loads((ROOT / \"results\" / \"seal.json\").read_text())[\"seals\"][-1]\n    t = data[\"testability_FREE_v2\"]           # was: json.loads((ROOT / \"results\" / \"testability_FREE_v2.json\").read_text())\n    out = {\"metadata\": {\n        \"artifact\": \"T7b name-free labels for free-vocabulary rule translations (run_u75jRHUss0zo, iter 4, gen_art_dataset_5)\",\n        \"workspace\": str(ROOT),\n        \"selection\": (\"the three plan groups (chosen as best 3 of 6 standardised candidates; folio / malls_test / \"\n                      \"logicnli_test were context only: no multi-system candidates, ~36-39% wrong gold, or no FOL; their \"\n                      \"standardised record is temp/candidates_data_out.json)\"),\n        \"label_mode\": seal[\"mode\"],\n        \"status_note\": (\"SEARCH-ONLY labels: the paid gloss step could not run (deviation D9: run OpenRouter budget \"\n                        \"exhausted before this artifact's first call; re-probed at packaging, still HTTP 403). ERROR_CERT is \"\n                        \"final and certificate-backed; MAPPED rows are UNRESOLVED_GLOSS_NOT_RUN until src/resume_gloss.py \"\n                        \"runs. metadata_label_binary_search_provisional (ERROR vs MAPPED) is a provisional view with audited \"\n                        \"contamination (results/soundness_audit.json).\"),\n        \"seal_all_rows_sha256\": seal[\"label_vector_sha256_all_rows\"],\n        \"seal_untouched_sha256\": seal.get(\"label_vector_sha256_untouched\"),\n        \"prereg_sha256\": seal[\"prereg_sha256\"],\n        \"testability_all_rows\": {k: t[\"all_rows\"][k] for k in (\"n_ERROR\", \"n_CORRECT\", \"TESTABLE\", \"label_counts\")},\n        \"testability_untouched\": {k: t[\"untouched_subset\"][k] for k in (\"n_ERROR\", \"n_CORRECT\", \"TESTABLE\", \"label_counts\")},\n        \"provisional_view_testable\": {k: t[\"search_provisional_view\"][k][\"TESTABLE\"] for k in (\"all_rows\", \"untouched_subset\")},\n    }, \"datasets\": [g for g in groups if g[\"dataset\"] in SELECTED]}\n    (ROOT / \"demo_full_data_out.json\").write_text(json.dumps(out, ensure_ascii=False))  # was: full_data_out.json\n    logger.info(f\"demo_full_data_out.json: {[(g['dataset'], len(g['examples'])) for g in out['datasets']]}\")\n    return out  # (added) keep the result for the summary cells\n\n\nout = main()\n''')\n\nmd(r\"\"\"\n## Results: what the labels look like\nFirst, the dataset-level metadata from the seal and testability summary. These numbers describe the **full** 2,652 rows, not the demo subset.\nWith search-only labels there is no `CORRECT` class yet, so AUROC is NOT_TESTABLE. The provisional ERROR_CERT-vs-MAPPED view *is* testable.\n\"\"\")\n\ncode(r'''\nm = out[\"metadata\"]\nprint(\"label_mode:\", m[\"label_mode\"])\nprint(\"seal (all rows):  \", m[\"seal_all_rows_sha256\"][:16], \"...\")\nprint(\"seal (untouched): \", (m[\"seal_untouched_sha256\"] or \"\")[:16], \"...\")\nprint(\"prereg sha256:    \", m[\"prereg_sha256\"][:16], \"...\")\nfull_tab = pd.DataFrame({\n    \"all rows (2,652)\": m[\"testability_all_rows\"][\"label_counts\"],\n    \"untouched (2,198, primary)\": m[\"testability_untouched\"][\"label_counts\"],\n}).fillna(0).astype(int)\nprint(\"\\nFULL-dataset label counts:\\n\", full_tab.to_string())\nprint(\"\\nTESTABLE (ERROR vs CORRECT):\", m[\"testability_all_rows\"][\"TESTABLE\"],\n      \"| provisional ERROR_CERT vs MAPPED view TESTABLE:\", m[\"provisional_view_testable\"])\n''')\n\nmd(\"Next, the assembled demo rows: labels by model family and by clause type, plus two example rows with their certificates.\")\n\ncode(r'''\nex = out[\"datasets\"][0][\"examples\"]\ndf = pd.DataFrame([{**json.loads(e[\"input\"]), \"label\": e[\"output\"],\n                    **{k[9:]: v for k, v in e.items() if k.startswith(\"metadata_\")}} for e in ex])\nprint(f\"{len(df)} assembled rows | label counts: {dict(Counter(df['label']))}\")\nprint(\"\\nlabel x family:\\n\", pd.crosstab(df[\"family\"], df[\"label\"]).to_string())\nprint(\"\\nsearch-provisional binary x clause type:\\n\",\n      pd.crosstab(df[\"clause_type\"], df[\"label_binary_search_provisional\"]).to_string())\n\nfor lab in (\"ERROR_CERT\", \"UNRESOLVED_GLOSS_NOT_RUN\"):\n    sub = df[df[\"label\"] == lab]\n    if len(sub) == 0:\n        continue\n    r = sub.iloc[0]\n    print(f\"\\n=== example {lab} ({r['system']}) ===\")\n    print(\"TEXT:\", r[\"text\"])\n    print(\"FOL: \", r[\"candidate_fol\"])\n    print(\"maps enumerated:\", r[\"n_maps_enumerated\"], \"| equivalent maps:\", r[\"n_equiv_maps\"],\n          \"| non-equiv certificates:\", r[\"nonequiv_certificate_type_counts\"])\n    if r[\"map_certificate\"]:\n        print(\"map certificate (reading =\", r[\"map_certificate\"][\"reading\"], \", bridges =\", r[\"map_certificate\"][\"bridges\"], \"):\")\n        for mline in r[\"map_certificate\"][\"map\"]:\n            print(\"   \", mline)\n        print(\"gloss pairs pending check:\", [(g[\"cand_atom\"], g[\"meaning\"]) for g in r[\"gloss_pairs\"]])\n''')\n\ncode(r'''\norder = [\"ERROR_CERT\", \"UNRESOLVED_GLOSS_NOT_RUN\", \"UNPARSEABLE\", \"NO_OUTPUT\"]\ncolors = [\"#c0504d\", \"#4f81bd\", \"#9b9b9b\", \"#d9d9d9\"]\nfig, ax = plt.subplots(1, 3, figsize=(17, 4.6))\n\n# (a) full-dataset label distribution (from the seal) vs demo subset\nfull = m[\"testability_all_rows\"][\"label_counts\"]\nax[0].bar(order, [full.get(k, 0) for k in order], color=colors)\nfor i, k in enumerate(order):\n    ax[0].text(i, full.get(k, 0), str(full.get(k, 0)), ha=\"center\", va=\"bottom\", fontsize=9)\nax[0].set_title(\"(a) Full dataset: 2,652 FREE rows\")\nax[0].set_ylabel(\"rows\")\nax[0].tick_params(axis=\"x\", rotation=20)\n\n# (b) provisional ERROR/MAPPED share per model family in the demo subset\nct = pd.crosstab(df[\"family\"], df[\"label\"]).reindex(columns=order, fill_value=0)\nct.plot(kind=\"barh\", stacked=True, color=colors, ax=ax[1], legend=False)\nax[1].set_title(f\"(b) Demo subset ({len(df)} rows) by model family\")\nax[1].set_xlabel(\"rows\")\nax[1].legend(fontsize=8, loc=\"lower right\")\n\n# (c) search effort: maps enumerated vs label (parseable rows only)\np = df[df[\"label\"].isin(order[:2])]\nfor lab, c in zip(order[:2], colors[:2]):\n    s = p[p[\"label\"] == lab]\n    ax[2].scatter(s[\"words\"], s[\"search_secs\"], label=lab, color=c, alpha=0.7, s=25)\nax[2].set_yscale(\"log\")\nax[2].set_xlabel(\"sentence length (words)\")\nax[2].set_ylabel(\"exhaustive search time (s, log)\")\nax[2].set_title(\"(c) Search cost vs sentence length\")\nax[2].legend(fontsize=8)\nplt.tight_layout()\nplt.show()\n''')\n\nmd(r\"\"\"\n**How to read this.**\n* `ERROR_CERT` rows are final. No map in the declared family (injective maps plus the B1–B5 bridges) makes the candidate z3-equivalent to any\n  template reading, and every rejected map has a certificate: a pruned subtree, a polarity conflict, or a finite countermodel. The executor audit\n  gives ERROR_CERT a precision of 0.867. Its misses are faithful forms outside the family, such as a disjunctive split or ∃-for-constant.\n* `UNRESOLVED_GLOSS_NOT_RUN` rows *can* be made equivalent. Whether the winning map is lexically plausible is decided by the pending gloss\n  check (`src/resume_gloss.py`), which turns these rows into CORRECT or ERROR. In the SIG replay, non-identity maps rescued 9–10% of known-ERROR rows,\n  and those are the cases the gloss check must stop.\n* Search is cheap: fractions of a second per candidate. The gloss check is the only paid step (~$1.8 for the whole audit).\n\"\"\")\n\nnb = {\"cells\": cells, \"metadata\": {\"kernelspec\": {\"display_name\": \"Python 3\", \"language\": \"python\", \"name\": \"python3\"},\n                                   \"language_info\": {\"name\": \"python\"}}, \"nbformat\": 4, \"nbformat_minor\": 5}\nfor i, c in enumerate(nb[\"cells\"]):\n    c[\"id\"] = f\"c{i:02d}\"\n(HERE / \"code_demo.ipynb\").write_text(json.dumps(nb, indent=1, ensure_ascii=False))\nprint(\"wrote code_demo.ipynb with\", len(cells), \"cells\")\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [25] TOOL CALL — Bash · 2026-09-24 19:20:32 UTC

```
cd /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_Ia_FT284H33j; sed -i 's/^N_ROWS = 100 /N_ROWS = 2 /' make_nb.py && python3 make_nb.py && grep -c "N_ROWS = 2 " code_demo.ipynb; /usr/local/bin/python3.12 -m venv .nb_env && .nb_env/bin/pip install -q pip jupyter ipykernel 2>&1 | tail -2; time .nb_env/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -5
```

### [26] TOOL RESULT — Bash · 2026-09-24 19:32:21 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false, "backgroundTaskId": "bikohg2ib", "timedOutAfterMs": 600000, "backgroundCwdHint": "Session cwd remains /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_Ia_FT284H33j; directory changes made by the backgrounded command do not apply to subsequent commands."}
```

### [27] TOOL CALL — Bash · 2026-09-24 19:32:21 UTC

```
cat /tmp/claude-0/-ai-inventor-aii-data-runs-run-u75jRHUss0zo-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-4-art-Ia-FT284H33j/0edcdb6e-4812-423c-84c8-8f0363de97de/tasks/bikohg2ib.output; ls /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_Ia_FT284H33j/.nb_env/lib/python3.12/site-packages | head -50 | wc -l
```

### [28] TOOL RESULT — Bash · 2026-09-24 19:32:21 UTC

```
{"stdout": "wrote code_demo.ipynb with 21 cells\n1\n[notice] A new release of pip is available: 25.0.1 -> 26.2.1\n[notice] To update, run: python3.12 -m pip install --upgrade pip\n50", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [29] ASSISTANT · 2026-09-24 19:32:21 UTC

```
While the test run finishes, I'll write the README and the manifest.
```

### [30] TOOL CALL — Bash · 2026-09-24 19:32:21 UTC

````
cd /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_Ia_FT284H33j
cat > .aii/manifest.yaml <<'EOF'
entries:
  - path: .nb_env/
    delete: regenerable
    source: "/usr/local/bin/python3.12 -m venv .nb_env && .nb_env/bin/pip install -q pip jupyter ipykernel"
  - path: logs/
    keep: small loguru log written by the notebook's data.py cell (text)
EOF
cat > README.md <<'EOF'
# Demo: name-free labels for free-vocabulary NL→FOL translations

A Colab-ready demo notebook for the dataset artifact *T7b name-free labels for R_COMP FREE* (round 4, dataset 5).
The notebook is the artifact's `data.py`, together with the `free_group()` builder from `src/build_output.py`,
split into cells with explanations. The code is otherwise unchanged. It runs on a 100-row curated subset.

## Layout
- `code_demo.ipynb` is the notebook, with outputs. It loads `mini_demo_data.json` from GitHub and falls back to a local copy. It runs in about 1 min, most of which is `pip install`.
- `mini_demo_data.json` holds 100 raw FREE label rows (`results/free_labels_v2.jsonl`, stratified by label × model family × clause type, seed 0: 34 ERROR_CERT, 34 UNRESOLVED_GLOSS_NOT_RUN, 16 UNPARSEABLE, 16 NO_OUTPUT), plus the final seal record and the testability summary (strata dropped) that `data.py` reads.
- `make_nb.py` rebuilds `code_demo.ipynb` from source (`python3 make_nb.py`).
- `demo_full_data_out.json` and `logs/` are written when the notebook runs (the demo-sized assembled output and the loguru log).

## Run
Open `code_demo.ipynb` in Colab and run all cells, or run it locally:
```bash
python3.12 -m venv .nb_env && .nb_env/bin/pip install -q pip jupyter ipykernel
.nb_env/bin/jupyter nbconvert --to notebook --execute code_demo.ipynb --output code_demo.ipynb
```
Config: `N_ROWS` (default 100, which is every row in the demo file). The original full run assembles all 2,652 rows and also the
`gloss_gate_items` (840) and `sig_soundness_replay` (4,280) groups. Their builders are in the notebook but are not called, because they read run-local files.

## Restoring removed files
- `.nb_env/` is a disposable test virtualenv: `/usr/local/bin/python3.12 -m venv .nb_env && .nb_env/bin/pip install -q pip jupyter ipykernel`
  (the notebook's first cell installs the rest).
EOF
````

### [31] TOOL RESULT — Bash · 2026-09-24 19:32:21 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [32] TOOL CALL — ToolSearch · 2026-09-24 19:32:21 UTC

```
{'query': 'select:Monitor', 'max_results': 1}
```

### [33] TOOL RESULT — ToolSearch · 2026-09-24 19:32:21 UTC

```
{"matches": ["Monitor"], "query": "select:Monitor", "total_deferred_tools": 27}
```

### [34] TOOL CALL — Bash · 2026-09-24 19:32:21 UTC

```
F=/tmp/claude-0/-ai-inventor-aii-data-runs-run-u75jRHUss0zo-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-4-art-Ia-FT284H33j/0edcdb6e-4812-423c-84c8-8f0363de97de/tasks/bikohg2ib.output; until grep -qE "real|Error|Traceback" $F; do sleep 5; done; cat $F
```

### [35] TOOL RESULT — Bash · 2026-09-24 19:36:17 UTC

```
{"stdout": "wrote code_demo.ipynb with 21 cells\n1\n[notice] A new release of pip is available: 25.0.1 -> 26.2.1\n[notice] To update, run: python3.12 -m pip install --upgrade pip\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m To update, run: \u001b[0m\u001b[32;49mpython3.12 -m pip install --upgrade pip\u001b[0m\n\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m A new release of pip is available: \u001b[0m\u001b[31;49m25.0.1\u001b[0m\u001b[39;49m -> \u001b[0m\u001b[32;49m26.2.1\u001b[0m\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m To update, run: \u001b[0m\u001b[32;49mpython3.12 -m pip install --upgrade pip\u001b[0m\n[NbConvertApp] Writing 135066 bytes to code_demo.ipynb\n\nreal\t4m48.366s\nuser\t0m15.873s\nsys\t0m3.222s\n\n[exited with code 0]", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [36] ASSISTANT · 2026-09-24 19:36:17 UTC

```
The minimum config (N_ROWS=2) passes. The 4m48s was almost all pip installs. I'll check the outputs, then scale to all 100 rows.
```

### [37] TOOL CALL — Bash · 2026-09-24 19:36:17 UTC

```
cd /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_Ia_FT284H33j; python3 -c "
import json;nb=json.load(open('code_demo.ipynb'))
for c in nb['cells']:
  for o in c.get('outputs',[]):
    if o['output_type']=='error': print('ERR',o['ename'],o['evalue'])
    elif 'text' in o: print(''.join(o['text'])[:1500])
    elif 'data' in o: print(list(o['data']))
"
```

### [38] TOOL RESULT — Bash · 2026-09-24 19:36:17 UTC

```
{"stdout": "\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m A new release of pip is available: \u001b[0m\u001b[31;49m25.0.1\u001b[0m\u001b[39;49m -> \u001b[0m\u001b[32;49m26.2.1\u001b[0m\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m To update, run: \u001b[0m\u001b[32;49mpython3.12 -m pip install --upgrade pip\u001b[0m\n\n\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m A new release of pip is available: \u001b[0m\u001b[31;49m25.0.1\u001b[0m\u001b[39;49m -> \u001b[0m\u001b[32;49m26.2.1\u001b[0m\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m To update, run: \u001b[0m\u001b[32;49mpython3.12 -m pip install --upgrade pip\u001b[0m\n\nDemo subset for art_Ia_FT284H33j: 100 raw FREE label rows (results/free_labels_v2.jsonl, stratified by label x family x clause_type, seed 0) + the seal record and the testability summary (strata dropped) that data.py reads. Source counts are for the full 2,652-row dataset.\nraw FREE label rows available: 100\n\n19:33:57|INFO   |demo_full_data_out.json: [('rcomp_free_labels', 2)]\n\nlabel_mode: search_only\nseal (all rows):   9609ebbb725832c4 ...\nseal (untouched):  b364a49a8e21835d ...\nprereg sha256:     b081c39991f52da2 ...\n\nFULL-dataset label counts:\n                           all rows (2,652)  untouched (2,198, primary)\nERROR_CERT                             759                         636\nUNRESOLVED_GLOSS_NOT_RUN              1506                        1175\nUNPARSEABLE                            188                         188\nNO_OUTPUT                              199                         199\n\nTESTABLE (ERROR vs CORRECT): False | provisional ERROR_CERT vs MAPPED view TESTABLE: {'all_rows': True, 'untouched_subset': True}\n\n2 assembled rows | label counts: {'ERROR_CERT': 2}\n\nlabel x family:\n label   ERROR_CERT\nfamily            \ncohere           2\n\n\nsearch-provisional binary x clause type:\n label_binary_search_provisional  ERROR\nclause_type                           \nas_long_as+unless                    1\nbut_only_if                          1\n\n=== example ERROR_CERT (G9:cohere/command-r7b-12-2024) ===\nTEXT: A manager who performs at the New Haven Symphony Orchestra and who steals government funds is a citizen of the European Union as long as the manager is not in Potterville, unless the manager captures images using a camera.\nFOL:  (∀x (PerformsAt(x, newHavenSymphonyOrchestra) ∧ Steals(x, governmentFunds) → Citizen(x, europeanUnion)) ∧ ¬In(x, potterville)) ↔ CapturesImages(x, camera)\nmaps enumerated: 0 | equivalent maps: 0 | non-equiv certificates: {'no_polarity_compatible_target': 2}\n\n['image/png', 'text/plain']", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [39] TOOL CALL — Bash · 2026-09-24 19:36:17 UTC

```
cd /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_Ia_FT284H33j; sed -i 's/^N_ROWS = 2 /N_ROWS = 100 /' make_nb.py && python3 make_nb.py && time .nb_env/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -2; python3 -c "
import json;nb=json.load(open('code_demo.ipynb'))
for c in nb['cells'][-5:]:
  for o in c.get('outputs',[]):
    if o['output_type']=='error': print('ERR',o['ename'],o['evalue'])
    elif 'text' in o: print(''.join(o['text'])[:3500])
    elif 'data' in o:
      print(list(o['data']))
      if 'image/png' in o['data']:
        import base64;open('/tmp/claude-0/-ai-inventor-aii-data-runs-run-u75jRHUss0zo-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-4-art-Ia-FT284H33j/0edcdb6e-4812-423c-84c8-8f0363de97de/scratchpad/fig.png','wb').write(base64.b64decode(o['data']['image/png']))
"
```

### [40] TOOL RESULT — Bash · 2026-09-24 19:36:17 UTC

```
{"stdout": "wrote code_demo.ipynb with 21 cells\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m To update, run: \u001b[0m\u001b[32;49mpython3.12 -m pip install --upgrade pip\u001b[0m\n[NbConvertApp] Writing 147867 bytes to code_demo.ipynb\n\nreal\t0m45.790s\nuser\t0m4.839s\nsys\t0m1.027s\nlabel_mode: search_only\nseal (all rows):   9609ebbb725832c4 ...\nseal (untouched):  b364a49a8e21835d ...\nprereg sha256:     b081c39991f52da2 ...\n\nFULL-dataset label counts:\n                           all rows (2,652)  untouched (2,198, primary)\nERROR_CERT                             759                         636\nUNRESOLVED_GLOSS_NOT_RUN              1506                        1175\nUNPARSEABLE                            188                         188\nNO_OUTPUT                              199                         199\n\nTESTABLE (ERROR vs CORRECT): False | provisional ERROR_CERT vs MAPPED view TESTABLE: {'all_rows': True, 'untouched_subset': True}\n\n100 assembled rows | label counts: {'ERROR_CERT': 34, 'UNRESOLVED_GLOSS_NOT_RUN': 34, 'UNPARSEABLE': 16, 'NO_OUTPUT': 16}\n\nlabel x family:\n label          ERROR_CERT  NO_OUTPUT  UNPARSEABLE  UNRESOLVED_GLOSS_NOT_RUN\nfamily                                                                     \ncohere                  7          0            7                         6\ndeepseek                7          0            6                         7\ngoogle-gemini           7          0            3                         7\ngoogle-gemma            7          0            0                         7\nmeta                    6          2            0                         7\nqwen                    0         14            0                         0\n\nsearch-provisional binary x clause type:\n label_binary_search_provisional  ERROR  EXCLUDED  MAPPED\nclause_type                                             \nas_long_as+unless                    5         5       4\nbut_only_if                          5         3       5\nexcept_when                          5         4       5\nexcept_when+provided_that            5         5       5\nprovided_that                        5         4       5\nprovided_that+unless                 5         6       5\nunless                               4         5       5\n\n=== example ERROR_CERT (G9:cohere/command-r7b-12-2024) ===\nTEXT: A manager who performs at the New Haven Symphony Orchestra and who steals government funds is a citizen of the European Union as long as the manager is not in Potterville, unless the manager captures images using a camera.\nFOL:  (∀x (PerformsAt(x, newHavenSymphonyOrchestra) ∧ Steals(x, governmentFunds) → Citizen(x, europeanUnion)) ∧ ¬In(x, potterville)) ↔ CapturesImages(x, camera)\nmaps enumerated: 0.0 | equivalent maps: 0.0 | non-equiv certificates: {'no_polarity_compatible_target': 2}\n\n=== example UNRESOLVED_GLOSS_NOT_RUN (G9:cohere/command-r7b-12-2024) ===\nTEXT: When a dog has hair, is injured, and produces milk to nourish its offspring, the dog is lazy, but only if the dog is flightless.\nFOL:  ∀x (Dog(x) ∧ Hair(x) ∧ Injured(x) ∧ ProducesMilk(x, offspring) → (Lazy(x) ↔ Flightless(x)))\nmaps enumerated: 48.0 | equivalent maps: 48.0 | non-equiv certificates: {'count_prune_subtree': 360}\nmap certificate (reading = strong , bridges = ['B2'] ):\n    Dog(x) => Dog(x)\n    Flightless(x) => Flightless(x)\n    Hair(x) => HasHair(x)\n    Injured(x) => Injured(x)\n    Lazy(x) => Lazy(x)\n    ProducesMilk(x, offspring) => ProducesMilk(x)\ngloss pairs pending check: [('Dog(x)', 'x is a dog'), ('Flightless(x)', 'x is flightless'), ('Hair(x)', 'x has hair'), ('Injured(x)', 'x is injured'), ('Lazy(x)', 'x is lazy'), ('ProducesMilk(x, offspring)', 'x produces milk to nourish its offspring'), ('Injured(x)', 'x produces milk to nourish its offspring'), ('ProducesMilk(x, offspring)', 'x is injured'), ('Hair(x)', 'x is injured'), ('Injured(x)', 'x has hair'), ('ProducesMilk(x, offspring)', 'x has hair'), ('Hair(x)', 'x produces milk to nourish its offspring'), ('Dog(x)', 'x has hair'), ('Hair(x)', 'x is a dog'), ('Injured(x)', 'x is a dog'), ('ProducesMilk(x, offspring)', 'x is a dog'), ('Dog(x)', 'x is injured'), ('Dog(x)', 'x produces milk to nourish its offspring'), ('Flightless(x)', 'x is lazy'), ('Lazy(x)', 'x is flightless')]\n\n['image/png', 'text/plain']", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [41] TOOL CALL — Bash · 2026-09-24 19:37:15 UTC

```
cd /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_Ia_FT284H33j; python3 - <<'EOF'
p="make_nb.py"; s=open(p).read()
s=s.replace('''print("maps enumerated:", r["n_maps_enumerated"], "| equivalent maps:", r["n_equiv_maps"],''','''print("maps enumerated:", int(r["n_maps_enumerated"]), "| equivalent maps:", int(r["n_equiv_maps"]),''')
s=s.replace('''print("gloss pairs pending check:", [(g["cand_atom"], g["meaning"]) for g in r["gloss_pairs"]])''','''print(f"gloss pairs pending check ({len(r['gloss_pairs'])}, first 6 shown):", [(g["cand_atom"], g["meaning"]) for g in r["gloss_pairs"][:6]])''')
open(p,"w").write(s)
EOF
grep -c 'int(r\["n_maps' make_nb.py; grep -c 'first 6 shown' make_nb.py
```

### [42] TOOL RESULT — Bash · 2026-09-24 19:37:15 UTC

```
{"stdout": "1\n1", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [43] TOOL CALL — Read · 2026-09-24 19:37:15 UTC

```
/tmp/claude-0/-ai-inventor-aii-data-runs-run-u75jRHUss0zo-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-4-art-Ia-FT284H33j/0edcdb6e-4812-423c-84c8-8f0363de97de/scratchpad/fig.png
```

### [44] TOOL RESULT — Read · 2026-09-24 19:37:15 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [45] TOOL CALL — Bash · 2026-09-24 19:37:15 UTC

```
A=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5; python3 -c "
import json,collections
c=collections.Counter()
for l in open('$A/results/free_labels_v2.jsonl'):
  r=json.loads(l); c[(r['family'],r['label'])]+=1
for k in sorted(c): print(k,c[k])"
```

### [46] TOOL RESULT — Bash · 2026-09-24 19:37:15 UTC

```
{"stdout": "('cohere', 'ERROR_CERT') 139\n('cohere', 'UNPARSEABLE') 36\n('cohere', 'UNRESOLVED_GLOSS_NOT_RUN') 46\n('deepseek', 'ERROR_CERT') 38\n('deepseek', 'UNPARSEABLE') 22\n('deepseek', 'UNRESOLVED_GLOSS_NOT_RUN') 161\n('google-gemini', 'ERROR_CERT') 57\n('google-gemini', 'UNPARSEABLE') 7\n('google-gemini', 'UNRESOLVED_GLOSS_NOT_RUN') 157\n('google-gemma', 'ERROR_CERT') 104\n('google-gemma', 'UNPARSEABLE') 10\n('google-gemma', 'UNRESOLVED_GLOSS_NOT_RUN') 107\n('meta', 'ERROR_CERT') 221\n('meta', 'NO_OUTPUT') 2\n('meta', 'UNPARSEABLE') 61\n('meta', 'UNRESOLVED_GLOSS_NOT_RUN') 379\n('microsoft', 'ERROR_CERT') 46\n('microsoft', 'UNPARSEABLE') 16\n('microsoft', 'UNRESOLVED_GLOSS_NOT_RUN') 159\n('mistral', 'ERROR_CERT') 55\n('mistral', 'UNPARSEABLE') 9\n('mistral', 'UNRESOLVED_GLOSS_NOT_RUN') 157\n('openai', 'ERROR_CERT') 46\n('openai', 'UNPARSEABLE') 14\n('openai', 'UNRESOLVED_GLOSS_NOT_RUN') 161\n('qwen', 'ERROR_CERT') 53\n('qwen', 'NO_OUTPUT') 197\n('qwen', 'UNPARSEABLE') 13\n('qwen', 'UNRESOLVED_GLOSS_NOT_RUN') 179", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [47] ASSISTANT · 2026-09-24 19:37:15 UTC

```
The sample leaves out 3 of the 9 families: round-robin over sorted (family, clause) keys used up the quota on the first families. I'll re-sample round-robin by family first.
```

### [48] TOOL CALL — Bash · 2026-09-24 19:37:15 UTC

```
cd /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_Ia_FT284H33j; A=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5; python3 - <<EOF
import json, random
from collections import defaultdict, Counter
A="$A"
rows=[json.loads(l) for l in open(A+"/results/free_labels_v2.jsonl") if l.strip()]
rng=random.Random(0)
quota={"ERROR_CERT":34,"UNRESOLVED_GLOSS_NOT_RUN":34,"UNPARSEABLE":16,"NO_OUTPUT":16}
sel=[]
for lab,q in quota.items():
    pool=[r for r in rows if r["label"]==lab]; rng.shuffle(pool)
    fam=defaultdict(lambda: defaultdict(list))
    for r in pool: fam[r["family"]][r["clause_type"]].append(r)
    fams=sorted(fam); used_ct=defaultdict(int); pick=[]; i=0
    while len(pick)<q and any(any(v for v in fam[f].values()) for f in fams):
        f=fams[i%len(fams)]; i+=1
        cts=[c for c in fam[f] if fam[f][c]]
        if not cts: continue
        c=min(cts,key=lambda c:(used_ct[c],c)); used_ct[c]+=1
        pick.append(fam[f][c].pop())
    sel+=pick
seal=json.load(open(A+"/results/seal.json"))
t=json.load(open(A+"/results/testability_FREE_v2.json"))
keep=("population","n_rows","n_ERROR","n_CORRECT","TESTABLE","label_counts")
tt={"all_rows":{k:t["all_rows"][k] for k in keep},"untouched_subset":{k:t["untouched_subset"][k] for k in keep},
    "search_provisional_view":{k:{kk:t["search_provisional_view"][k][kk] for kk in keep} for k in ("all_rows","untouched_subset")}}
out={"description":"Demo subset for art_Ia_FT284H33j: 100 raw FREE label rows (results/free_labels_v2.jsonl; per label a fixed quota 34/34/16/16, round-robin over model families then clause types, seed 0) + the seal record and the testability summary (strata dropped) that data.py reads. Source counts are for the full 2,652-row dataset.",
     "free_labels_rows":sel,"seal":{"seals":[seal["seals"][-1]]},"testability_FREE_v2":tt}
json.dump(out,open("mini_demo_data.json","w"),ensure_ascii=False,indent=1)
print(len(sel), sum(bool(r["seen_iter3"]) for r in sel))
print(Counter((r["family"]) for r in sel)); print(Counter(r["clause_type"] for r in sel)); print(Counter(r["slot"] for r in sel))
EOF
```

### [49] TOOL RESULT — Bash · 2026-09-24 19:37:15 UTC

```
{"stdout": "100 17\nCounter({'qwen': 21, 'meta': 12, 'cohere': 10, 'deepseek': 10, 'google-gemini': 10, 'google-gemma': 10, 'microsoft': 10, 'mistral': 10, 'openai': 7})\nCounter({'but_only_if': 16, 'as_long_as+unless': 15, 'except_when': 15, 'except_when+provided_that': 14, 'provided_that': 14, 'provided_that+unless': 14, 'unless': 12})\nCounter({'G2': 21, 'G9': 10, 'G4': 10, 'G8': 10, 'G5': 10, 'G6': 10, 'G3': 10, 'G7': 7, 'G1b': 7, 'G1': 5})", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [50] ASSISTANT · 2026-09-24 19:37:15 UTC

```
Now fix the plot layout (overlapping tick labels, legend over the bars, and a note that panel (b) is a quota sample), then rerun.
```

### [51] TOOL CALL — Bash · 2026-09-24 19:37:15 UTC

```
cd /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_Ia_FT284H33j; python3 - <<'EOF'
p="make_nb.py"; s=open(p).read()
rep=[('''ax[0].bar(order, [full.get(k, 0) for k in order], color=colors)''','''short = ["ERROR_CERT", "UNRESOLVED\\n(gloss not run)", "UNPARSEABLE", "NO_OUTPUT"]
ax[0].bar(short, [full.get(k, 0) for k in order], color=colors)'''),
('''ax[0].tick_params(axis="x", rotation=20)\n''','''ax[0].tick_params(axis="x", labelsize=8)\n'''),
('''ax[1].set_title(f"(b) Demo subset ({len(df)} rows) by model family")''','''ax[1].set_title(f"(b) Demo subset ({len(df)} rows, fixed quota per label) by family", fontsize=10)'''),
('''ax[1].legend(fontsize=8, loc="lower right")''','''ax[1].legend(fontsize=7, loc="upper center", bbox_to_anchor=(0.5, -0.15), ncol=2)'''),
("""* Search is cheap""","""* Panel (b) shows a quota sample (34/34/16/16 rows per label), so its per-family label shares are not the population rates. In the full data,
  197 of the 199 NO_OUTPUT rows come from the qwen slot.
* Search is cheap"""),
]
for a,b in rep:
    assert a in s, a; s=s.replace(a,b)
open(p,"w").write(s)
EOF
python3 make_nb.py && time .nb_env/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -1; python3 -c "
import json,base64;nb=json.load(open('code_demo.ipynb'))
for c in nb['cells']:
  for o in c.get('outputs',[]):
    if o['output_type']=='error': print('ERR',o['ename'],o['evalue'])
    elif 'data' in o and 'image/png' in o['data']: open('/tmp/claude-0/-ai-inventor-aii-data-runs-run-u75jRHUss0zo-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-4-art-Ia-FT284H33j/0edcdb6e-4812-423c-84c8-8f0363de97de/scratchpad/fig.png','wb').write(base64.b64decode(o['data']['image/png']))
for c in nb['cells'][-4:-3]:
  for o in c.get('outputs',[]): print(''.join(o.get('text',''))[:2500])
"
```

### [52] TOOL RESULT — Bash · 2026-09-24 19:37:15 UTC

```
{"stdout": "wrote code_demo.ipynb with 21 cells\n[NbConvertApp] Writing 136634 bytes to code_demo.ipynb\n\nreal\t0m46.025s\nuser\t0m4.947s\nsys\t0m1.066s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [53] TOOL CALL — Bash · 2026-09-24 19:37:15 UTC

```
cd /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_Ia_FT284H33j; python3 -c "
import json;nb=json.load(open('code_demo.ipynb'))
for i,c in enumerate(nb['cells']):
  for o in c.get('outputs',[]):
    if 'text' in o and i>14: print(i, ''.join(o['text'])[:2000])
"
```

### [54] TOOL RESULT — Bash · 2026-09-24 19:37:15 UTC

```
{"stdout": "16 label_mode: search_only\nseal (all rows):   9609ebbb725832c4 ...\nseal (untouched):  b364a49a8e21835d ...\nprereg sha256:     b081c39991f52da2 ...\n\nFULL-dataset label counts:\n                           all rows (2,652)  untouched (2,198, primary)\nERROR_CERT                             759                         636\nUNRESOLVED_GLOSS_NOT_RUN              1506                        1175\nUNPARSEABLE                            188                         188\nNO_OUTPUT                              199                         199\n\nTESTABLE (ERROR vs CORRECT): False | provisional ERROR_CERT vs MAPPED view TESTABLE: {'all_rows': True, 'untouched_subset': True}\n\n18 100 assembled rows | label counts: {'ERROR_CERT': 34, 'UNRESOLVED_GLOSS_NOT_RUN': 34, 'UNPARSEABLE': 16, 'NO_OUTPUT': 16}\n\nlabel x family:\n label          ERROR_CERT  NO_OUTPUT  UNPARSEABLE  UNRESOLVED_GLOSS_NOT_RUN\nfamily                                                                     \ncohere                  4          0            2                         4\ndeepseek                4          0            2                         4\ngoogle-gemini           4          0            2                         4\ngoogle-gemma            4          0            2                         4\nmeta                    4          2            2                         4\nmicrosoft               4          0            2                         4\nmistral                 4          0            2                         4\nopenai                  3          0            1                         3\nqwen                    3         14            1                         3\n\nsearch-provisional binary x clause type:\n label_binary_search_provisional  ERROR  EXCLUDED  MAPPED\nclause_type                                             \nas_long_as+unless                    5         5       5\nbut_only_if                          5         6       5\nexcept_when                          5         5       5\nexcept_when+provided_that            5         4       5\nprovided_that                        5         4       5\nprovided_that+unless                 5         4       5\nunless                               4         4       4\n\n=== example ERROR_CERT (G9:cohere/command-r7b-12-2024) ===\nTEXT: A manager who performs at the New Haven Symphony Orchestra and who steals government funds is a citizen of the European Union as long as the manager is not in Potterville, unless the manager captures images using a camera.\nFOL:  (∀x (PerformsAt(x, newHavenSymphonyOrchestra) ∧ Steals(x, governmentFunds) → Citizen(x, europeanUnion)) ∧ ¬In(x, potterville)) ↔ CapturesImages(x, camera)\nmaps enumerated: 0", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [55] TOOL CALL — Read · 2026-09-24 19:37:15 UTC

```
/tmp/claude-0/-ai-inventor-aii-data-runs-run-u75jRHUss0zo-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-4-art-Ia-FT284H33j/0edcdb6e-4812-423c-84c8-8f0363de97de/scratchpad/fig.png
```

### [56] TOOL RESULT — Read · 2026-09-24 19:37:15 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [57] ASSISTANT · 2026-09-24 19:37:15 UTC

```
All 9 families are now covered. Last step: a clean-environment run from scratch to confirm the total runtime stays under 600s.
```

### [58] TOOL CALL — Bash · 2026-09-24 19:37:15 UTC

```
cd /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_Ia_FT284H33j; rm -rf .nb_env logs demo_full_data_out.json; /usr/local/bin/python3.12 -m venv .nb_env && .nb_env/bin/pip install -q pip jupyter ipykernel 2>&1 | grep -v notice; S=$(date +%s); .nb_env/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -1; echo "nb_secs=$(( $(date +%s)-S ))"; python3 -c "
import json;nb=json.load(open('code_demo.ipynb'))
print('errors:',sum(o['output_type']=='error' for c in nb['cells'] for o in c.get('outputs',[])), 'unexecuted code cells:', sum(c['cell_type']=='code' and c['execution_count'] is None for c in nb['cells']))"; rm -rf .nb_env
```

### [59] TOOL RESULT — Bash · 2026-09-24 19:37:15 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false, "backgroundTaskId": "bipyp8q0b", "backgroundCwdHint": "Session cwd remains /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_Ia_FT284H33j; directory changes made by the backgrounded command do not apply to subsequent commands."}
```

### [60] ASSISTANT · 2026-09-24 19:37:15 UTC

```
Meanwhile, the verification checks from TODO 6 and the structured output:
```

### [61] TOOL CALL — Bash · 2026-09-24 19:37:15 UTC

```
cd /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_Ia_FT284H33j; grep -c 'GITHUB_DATA_URL = \\"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/main/round-4/dataset-5/demo/mini_demo_data.json\\"' code_demo.ipynb; grep -c "urllib.request.urlopen(GITHUB_DATA_URL)" code_demo.ipynb; ls -la mini_demo_data.json; grep -rn "/ai-inventor" README.md code_demo.ipynb mini_demo_data.json | cut -c1-200 | head
echo '{"out_expected_files": {"notebook": "code_demo.ipynb", "mini_data_file": "mini_demo_data.json"}}' > .terminal_claude_agent_struct_out.json
```

### [62] TOOL RESULT — Bash · 2026-09-24 19:37:15 UTC

```
{"stdout": "1\n1\n-rw-r--r-- 1 root root 275512 Sep 24 19:35 mini_demo_data.json\ncode_demo.ipynb:142:    \"GITHUB_DATA_URL = \\\"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/main/round-4/dataset-5/demo/mini_demo_data.json", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [63] TOOL CALL — Bash · 2026-09-24 19:37:15 UTC

```
F=/tmp/claude-0/-ai-inventor-aii-data-runs-run-u75jRHUss0zo-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-4-art-Ia-FT284H33j/0edcdb6e-4812-423c-84c8-8f0363de97de/tasks/bipyp8q0b.output; until grep -qE "nb_secs|Traceback" $F; do sleep 5; done; sleep 3; cat $F
```

### [64] TOOL RESULT — Bash · 2026-09-24 19:47:25 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false, "backgroundTaskId": "b2mndbkxv", "timedOutAfterMs": 600000}
```

### [65] TOOL CALL — Bash · 2026-09-24 19:48:15 UTC

```
cat /tmp/claude-0/-ai-inventor-aii-data-runs-run-u75jRHUss0zo-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-4-art-Ia-FT284H33j/0edcdb6e-4812-423c-84c8-8f0363de97de/tasks/bipyp8q0b.output; cd /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_Ia_FT284H33j; ls .nb_env/lib/python3.12/site-packages | grep -iE "^(numpy|pandas|matplotlib|loguru|jupyter)" ; ls -la
```

### [66] TOOL RESULT — Bash · 2026-09-24 19:48:15 UTC

```
{"stdout": "jupyter-1.1.1.dist-info\njupyter.py\njupyter_builder\njupyter_builder-1.2.3.dist-info\njupyter_client\njupyter_client-8.10.0.dist-info\njupyter_console\njupyter_console-6.6.3.dist-info\njupyter_core\njupyter_core-5.9.1.dist-info\njupyter_events\njupyter_events-0.12.1.dist-info\njupyter_lsp\njupyter_lsp-2.3.1.dist-info\njupyter_server\njupyter_server-2.21.1.dist-info\njupyter_server_terminals\njupyter_server_terminals-0.5.4.dist-info\njupyterlab\njupyterlab-4.6.4.dist-info\njupyterlab_pygments\njupyterlab_pygments-0.3.0.dist-info\njupyterlab_server\njupyterlab_server-2.28.1.dist-info\njupyterlab_widgets\njupyterlab_widgets-3.0.17.dist-info\nloguru\nloguru-0.7.3.dist-info\nmatplotlib_inline\nmatplotlib_inline-0.2.2.dist-info\nnumpy\nnumpy-2.0.2.dist-info\ntotal 7183\ndrwxr-xr-x 4 root root 2025603 Sep 24 19:37 .\ndrwxr-xr-x 7 root root 2094412 Sep 24 18:56 ..\ndrwxr-xr-x 2 root root   24900 Sep 24 19:30 .aii\n-rw------- 1 root root      54 Sep 24 19:18 .aii_claude_session.json\ndrwxr-xr-x 7 root root 2025490 Sep 24 19:38 .nb_env\n-rw-r--r-- 1 root root  747414 Sep 24 19:46 .repl_agent.ptylog\n-rw-r--r-- 1 root root      97 Sep 24 19:36 .terminal_claude_agent_struct_out.json\n-rw-r--r-- 1 root root    1885 Sep 24 19:30 README.md\n-rw-r--r-- 1 root root  136679 Sep 24 19:36 code_demo.ipynb\n-rw-r--r-- 1 root root   20096 Sep 24 19:35 make_nb.py\n-rw-r--r-- 1 root root  275512 Sep 24 19:35 mini_demo_data.json", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [67] ASSISTANT · 2026-09-24 19:48:15 UTC

```
The environment's pip downloads are slow on this machine. The notebook itself started around 19:38, so I'll wait for it to finish.
```

### [68] TOOL CALL — Bash · 2026-09-24 19:48:15 UTC

```
F=/tmp/claude-0/-ai-inventor-aii-data-runs-run-u75jRHUss0zo-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-4-art-Ia-FT284H33j/0edcdb6e-4812-423c-84c8-8f0363de97de/tasks/bipyp8q0b.output; until grep -qE "unexecuted|Traceback|Error" $F; do sleep 5; done; sleep 2; cat $F
```

### [69] TOOL RESULT — Bash · 2026-09-24 19:50:33 UTC

```
{"stdout": "[NbConvertApp] Writing 136721 bytes to code_demo.ipynb\nnb_secs=257\nerrors: 0 unexecuted code cells: 0", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [70] THINKING · 2026-09-24 19:50:35 UTC

```
The clean-environment run passed with no errors in 257s. I'll now remove `demo_full_data_out.json` and `logs/` since they contain the absolute workspace path and are regenerated on each run anyway.
```

### [71] TOOL CALL — Bash · 2026-09-24 19:50:35 UTC

```
cd /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_Ia_FT284H33j; ls -a; grep -c "/ai-inventor" code_demo.ipynb demo_full_data_out.json 2>/dev/null; rm -rf demo_full_data_out.json logs .nb_env
python3 - <<'EOF'
p="README.md"; s=open(p).read()
s=s.replace("It runs in about 1 min, most of which is `pip install`.","A clean-environment run takes about 4–5 min, almost all of it `pip install` (tested: 257 s, 0 errors).")
s=s.replace("- `demo_full_data_out.json` and `logs/` are written when the notebook runs (the demo-sized assembled output and the loguru log).",
 "- `demo_full_data_out.json` and `logs/` are created when the notebook runs (the demo-sized assembled output and the loguru log). They are not committed, because the output records the absolute path of the machine it ran on.")
open(p,"w").write(s)
EOF
cat > .aii/manifest.yaml <<'EOF'
entries:
  - path: .nb_env/
    delete: regenerable
    source: "/usr/local/bin/python3.12 -m venv .nb_env && .nb_env/bin/pip install -q pip jupyter ipykernel"
EOF
ls -la; cat .terminal_claude_agent_struct_out.json
```

### [72] TOOL RESULT — Bash · 2026-09-24 19:50:35 UTC

```
{"stdout": ".\n..\n.aii\n.aii_claude_session.json\n.nb_env\n.repl_agent.ptylog\n.terminal_claude_agent_struct_out.json\nREADME.md\ncode_demo.ipynb\ndemo_full_data_out.json\nlogs\nmake_nb.py\nmini_demo_data.json\ncode_demo.ipynb:1\ndemo_full_data_out.json:1\ntotal 6167\ndrwxr-xr-x 3 root root 2000123 Sep 24 19:50 .\ndrwxr-xr-x 7 root root 3000108 Sep 24 18:56 ..\ndrwxr-xr-x 2 root root   16000 Sep 24 19:30 .aii\n-rw------- 1 root root      54 Sep 24 19:18 .aii_claude_session.json\n-rw-r--r-- 1 root root  860370 Sep 24 19:50 .repl_agent.ptylog\n-rw-r--r-- 1 root root      97 Sep 24 19:36 .terminal_claude_agent_struct_out.json\n-rw-r--r-- 1 root root    2029 Sep 24 19:50 README.md\n-rw-r--r-- 1 root root  136766 Sep 24 19:49 code_demo.ipynb\n-rw-r--r-- 1 root root   20096 Sep 24 19:35 make_nb.py\n-rw-r--r-- 1 root root  275512 Sep 24 19:35 mini_demo_data.json\n{\"out_expected_files\": {\"notebook\": \"code_demo.ipynb\", \"mini_data_file\": \"mini_demo_data.json\"}}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [73] TOOL CALL — Bash · 2026-09-24 19:50:39 UTC

```
cd /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_Ia_FT284H33j; grep -o "/ai-inventor/[a-z_]*" code_demo.ipynb mini_demo_data.json README.md make_nb.py | sort | uniq -c
```

### [74] TOOL RESULT — Bash · 2026-09-24 19:50:39 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [75] ASSISTANT · 2026-09-24 19:50:50 UTC

```
I've built the demo notebook and its data file. After I scaled it to the full 100-row demo subset, it ran end to end in a clean Python 3.12 environment in 257s with no errors, under the 600s limit. Almost all of that time is package installs.

**`mini_demo_data.json`** (275 KB) holds 100 raw label rows from the artifact's `rcomp_free_labels` data, plus the seal record and the summary of which comparisons are testable that `data.py` reads.
- **Label mix:** a fixed number per label: 34 `ERROR_CERT`, 34 `UNRESOLVED_GLOSS_NOT_RUN`, 16 `UNPARSEABLE`, 16 `NO_OUTPUT`.
- **Coverage:** all 9 model families and all 7 clause types, picked in turn by family, then clause type (seed 0).
- **Fix:** my first sample missed 3 families, so I re-drew it.

**`code_demo.ipynb`** is `data.py` plus its row builder `free_group()`, split into cells with explanations between them. The code is unchanged except:
- rows, seal and testability summary are read from the loaded `data` instead of run-local files;
- `ROOT` is the current directory, since `__file__` doesn't exist in a notebook;
- output is written to `demo_full_data_out.json`, so it can't be mistaken for the real `full_data_out.json`;
- only the free-label group is built. The other two groups' builders (`gate_group`, `sig_group`) are kept verbatim but not called, because the demo file holds one dataset only.

The one setting is `N_ROWS = 100`, which uses every demo row; the original run uses all 2,652. The summary cells at the end show:
- the full-dataset label counts and the seal hashes;
- the demo rows broken down by model family and by clause type;
- an `ERROR_CERT` example and a `MAPPED` example, with the symbol map and the gloss pairs still waiting to be checked;
- a 3-panel figure.

The panel of labels by family comes from a fixed quota per label, so its per-family shares are not population rates; the notebook says so. In the full data, 197 of the 199 `NO_OUTPUT` rows come from the qwen slot.

Checks from TODO 6 all pass:
- the exact `GITHUB_DATA_URL` string is in the notebook;
- the loader tries the GitHub URL first and falls back to the local file;
- `mini_demo_data.json` exists.

The GitHub URL won't work until the files are pushed, so for now it loads the local copy.

I also wrote `README.md`, `.aii/manifest.yaml` (one entry: the test environment `.nb_env/`, marked regenerable) and `.terminal_claude_agent_struct_out.json`. I deleted the test environment. I also deleted the generated `demo_full_data_out.json` and `logs/`, because the output file records this server's absolute path. The notebook recreates both on every run. `make_nb.py` rebuilds the notebook from source.

Files are in the workspace:
- `code_demo.ipynb`
- `mini_demo_data.json`
- `README.md`
- `make_nb.py`
- `.aii/manifest.yaml`
- `.terminal_claude_agent_struct_out.json`
```

### [76] SYSTEM-USER prompt · 2026-09-24 19:50:51 UTC

```
<CRITICAL_ERROR>
The module-end file check FAILED (attempt 1/3).

PROBLEMS:
  - .aii/manifest.yaml: '.nb_env/' matches nothing that needs a decision — remove it (text, code and files under the auto-keep floor are always kept)

FIX IT:
1. Add one entry per uncovered path to `.aii/manifest.yaml` (create it if missing).
   Every path is RELATIVE TO YOUR CWD and must resolve inside it. Globs and
   whole directories are fine — a whole `hf_cache/` is ONE entry.

   entries:
     - path: results/
       keep: six GPU-hours of sweep output, not reproducible in this run
     - path: hf_cache/
       delete: redownloadable
       source: "huggingface-cli download meta-llama/Llama-3-8B"
     - path: checkpoints/
       delete: regenerable
       source: "uv run train.py --epochs 3"

   `keep:` takes a one-line reason. `delete:` takes `redownloadable` or
   `regenerable` and a `source:` that brings the files back.
2. Make sure `README.md` reads like a GitHub repository README: what you did,
   the layout (a line per important file/dir), how to run it, and a
   "Restoring removed files" section with the command for EVERY delete entry.
3. Text and code files never need a decision, and neither does anything under
   the auto-keep floor. Only large binaries and cache directories do.
</CRITICAL_ERROR>
```

### [77] TOOL CALL — Bash · 2026-09-24 19:50:57 UTC

```
cd /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_Ia_FT284H33j; printf 'entries: []\n' > .aii/manifest.yaml
python3 - <<'EOF'
p="README.md"; s=open(p).read()
i=s.index("## Restoring removed files")
s=s[:i]+"""## Restoring removed files
Nothing in this directory is marked for deletion; every file is small text or code and is kept.
The only disposable item used during testing was a local test virtualenv, `.nb_env/`. It has already been removed.
To recreate it: `/usr/local/bin/python3.12 -m venv .nb_env && .nb_env/bin/pip install -q pip jupyter ipykernel`
(the notebook's first cell installs everything else).
"""
open(p,"w").write(s)
EOF
cat .aii/manifest.yaml; tail -6 README.md; ls -a; du -sh .
```

### [78] TOOL RESULT — Bash · 2026-09-24 19:50:57 UTC

```
{"stdout": "entries: []\n\n## Restoring removed files\nNothing in this directory is marked for deletion; every file is small text or code and is kept.\nThe only disposable item used during testing was a local test virtualenv, `.nb_env/`. It has already been removed.\nTo recreate it: `/usr/local/bin/python3.12 -m venv .nb_env && .nb_env/bin/pip install -q pip jupyter ipykernel`\n(the notebook's first cell installs everything else).\n.\n..\n.aii\n.aii_claude_session.json\n.repl_agent.ptylog\n.terminal_claude_agent_struct_out.json\nREADME.md\ncode_demo.ipynb\nmake_nb.py\nmini_demo_data.json\n3.3M\t.", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [79] ASSISTANT · 2026-09-24 19:50:59 UTC

```
I've fixed the manifest. The check failed because it listed `.nb_env/`, the test environment I had already deleted, so the entry matched nothing.

- **`.aii/manifest.yaml`** is now `entries: []`. The whole workspace is 3.3 MB of text and code, all under the 10 MB floor, so nothing needs a keep or delete decision.
- **`README.md`**: the "Restoring removed files" section now says nothing is marked for deletion. It still gives the command to recreate the test environment, in case someone wants to re-run the local test.

The notebook, `mini_demo_data.json` and `.terminal_claude_agent_struct_out.json` are unchanged.
```
