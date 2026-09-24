# gen_art_experiment_13 — test_idea

> Phase: `invention_loop` · round 5 · `gen_art`
> Run: `run_u75jRHUss0zo` — Gold-Free Faithfulness Metrics for NL-to-FOL Translation
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_art_experiment_13` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-09-24 11:08:10 UTC

```
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: An artifact exe... [truncated, 59497 chars total]
```

### [2] HUMAN-USER prompt · 2026-09-24 11:08:10 UTC

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

### [3] SKILL-INPUT — aii-python · 2026-09-24 11:08:18 UTC

The agent loaded the **aii-python** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-python
description: "Applies this repo's Python conventions to experiment and evaluation scripts: uv-only environment setup (never pip), loguru logging with stdout plus a rotating file sink, @logger.catch(reraise=True) with explicit exception types, pathlib file access, type hints, and a standard main() script skeleton. ALWAYS read before writing or editing any Python script that runs an experiment, evaluation, or data-processing job. Triggers: writing or refactoring a Python script, uv venv, uv pip install, pyproject dependencies, loguru, logging setup, try/except and error handling, pathlib, script structure, Python 3.12. NOT for: parallelism, GPU throughput or hardware sizing (use aii-parallel-computing and aii-use-hardware), scaling long autonomous jobs (use aii-long-running-tasks), splitting oversized output files (use aii-file-size-limit), calling LLMs (use aii-openrouter-llms), or notebooks meant for Colab (use aii-colab)."
---

## Environment Setup

- Python 3.12+
- **NEVER use `pip` or `.venv/bin/pip`** — they are not installed. Use `uv` for ALL package operations:
  ```bash
  uv venv .venv --python=3.12
  source .venv/bin/activate  # or: .venv/bin/python script.py
  uv pip install pandas loguru  # NOT: pip install
  ```
- Create `.toml` file with dependencies, create uv `.venv` and activate it
- NO inline dependencies (no `# /// script` headers)

## Logging

Use `loguru` for all logging. Add a file sink alongside stdout.

```python
from loguru import logger
import sys

logger.remove()  # Remove default handler
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add("logs/run.log", rotation="30 MB", level="DEBUG")
```

Rules:
- Log every major step (data loading, processing start/end, results)
- If applicable, log every LLM API call input and output
- Truncate long outputs in logs (add truncation logic for potentially large strings)
- Use `logger.error()` in except blocks (traceback auto-captured)

## Error Handling

- Wrap major operations in try/except blocks
- Use `@logger.catch(reraise=True)` decorator on main functions — without `reraise=True`, the script exits 0 even on uncaught exceptions, hiding failures from downstream consumers
- Use explicit exception types, not bare `except:`
- Never silently swallow exceptions — always log them

```python
@logger.catch(reraise=True)
def main():
    try:
        data = load_data(path)
    except FileNotFoundError:
        logger.error("Data file not found")
        raise
    except json.JSONDecodeError:
        logger.error("Invalid JSON in data file")
        raise
```

## Code Structure

- Use `pathlib.Path` for file operations: `Path("data/input.json").read_text()` not `open(...).read()`
- Use type hints for function signatures
- Use keyword arguments for functions with more than 4 parameters
- No hardcoded paths — derive from script location or accept as arguments

## Script Pattern

Standard pattern for experiment/evaluation scripts:

```python
#!/usr/bin/env python3
"""Brief description of what this script does."""

from loguru import logger
from pathlib import Path
import json
import sys

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add("logs/run.log", rotation="30 MB", level="DEBUG")

@logger.catch(reraise=True)
def main():
    # Load data
    data_path = Path("full_data_out.json")
    logger.info(f"Loading data from {data_path}")
    data = json.loads(data_path.read_text())
    logger.info(f"Loaded {len(data['examples'])} examples")

    # Process
    results = []
    for i, example in enumerate(data["examples"]):
        try:
            result = process(example)
            results.append(result)
        except Exception:
            logger.error(f"Failed on example {i}")
            continue

    # Save output
    output = {"examples": results}
    Path("method_out.json").write_text(json.dumps(output, indent=2))
    logger.info(f"Saved {len(results)} results")

if __name__ == "__main__":
    main()
```
````

### [4] SKILL-INPUT — aii-json · 2026-09-24 11:08:20 UTC

The agent loaded the **aii-json** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-json
description: "Validates JSON files against this repo's experiment-pipeline schemas (exp_sel_data_out, exp_gen_sol_out, exp_eval_sol_out, exp_proof_out) and generates size-optimized full, mini and preview variants of any JSON array file. ALWAYS use before treating a pipeline stage output as finished, whenever a schema or required-property error must be fixed, and whenever a large JSON file needs a small truncated version safe to read. Triggers: JSON schema validation, schema compliance, required property errors, pipeline stage outputs, the exp_*_out format names, mini and preview JSON generation, shrinking a large JSON before inspection. NOT for: discovering or downloading new datasets, which aii-hf-datasets and aii-owid-datasets cover; splitting oversized output files, which aii-file-size-limit covers; plotting JSON data, which aii-data-fig-gen covers; spreadsheet and .csv tabular data, which anthropic-xlsx covers."
---

## Contents

- Validating JSON (schema validation against experiment schemas)
- Formatting JSON (generate full/mini/preview versions)

**IMPORTANT - Parallel execution:** GNU `parallel` subshells do NOT inherit `source activate`. Use `export` for variables and **single-quoted** command templates so parallel's subshells can resolve them:
```
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json"
export PY="$SKILL_DIR/../.ability_client_venv/bin/python"
```

---

## Validating JSON

Validate JSON files against predefined schemas for experiment-based hypothesis selection, data collection, solution generation, and evaluation.

### Quick Start

1. Read the schema spec you need to adhere to (e.g., `schemas/exp_eval_sol_out.json`)
2. Create your output file following that schema structure
3. Validate:

```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_validate_schema.py --format exp_eval_sol_out --file /path/to/eval_out.json
```

### Script: aii_json_validate_schema.py

**Example input:**
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_validate_schema.py --format exp_eval_sol_out --file /tmp/eval_out.json
```

**Parallel execution (multiple validations):**

IMPORTANT: When validating multiple files, use GNU parallel instead of separate Bash tool calls:
```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
export PY="$SKILL_DIR/../.ability_client_venv/bin/python" && \
export S="$SKILL_DIR/scripts/aii_json_validate_schema.py" && \
parallel -j 50 -k --group --will-cite '$PY $S --format {1} --file {2}' ::: 'exp_sel_data_out' 'exp_gen_sol_out' 'exp_eval_sol_out' :::+ '/tmp/full_data_out.json' '/tmp/method_out.json' '/tmp/eval_out.json'
```

**Example output (success):**
```
Validating: aii_json_validate_schema.py
Format: exp_eval_sol_out

✓ Validation PASSED
```

**Example output (failure):**
```
Validating: aii_json_validate_schema.py
Format: exp_sel_data_out

✗ Validation FAILED

Errors:
  Path: datasets → 0 → examples → 0
  Error: 'output' is a required property
  Validator: required
```

**Parameters:**

`--format` (required)
- Format type to validate against
- Determines which schema to use

`--file` (required)
- Path to JSON file to validate
- Must be valid JSON
- **Always pass an absolute path.** Relative paths resolve from the
  ability server's CWD (typically ``/ai-inventor/aii_server``), not from
  your agent workspace, so ``data_out/x.json`` will silently look in the
  wrong directory and fail with "Could not load JSON file". The validate
  endpoint also accepts a ``workspace_dir`` arg if you need to keep a
  relative path — pass your workspace path there.

**Tips:**
- Fix errors in your JSON and rerun validation until it passes

### Schema Files

Schemas are stored in `.claude/skills/aii-json/schemas/`:

**Experiment Pipeline** — the four formats `schemas/` actually holds and
`AVAILABLE_FORMATS` in `scripts/aii_json_validate_schema.py` accepts (this
list used to name six hypothesis-selection schemas that exist nowhere and
omit the proof one; corrected 2026-09-03):
- `exp_sel_data_out.json` - Experiment Data Selection format
- `exp_gen_sol_out.json` - Experiment Solution Generation format
- `exp_eval_sol_out.json` - Experiment Solution Evaluation format
- `exp_proof_out.json` - Experiment Proof format

---

## Formatting JSON

Generate three size-optimized versions of a JSON file for efficient development and preview:
- **full**: Identical to original (all data)
- **mini**: First 3 items only (for quick testing)
- **preview**: Mini + all strings truncated to 200 chars (for quick inspection)

### Quick Start

```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_format_mini_preview.py --input method_out.json
```

### Script: aii_json_format_mini_preview.py

**Example input:**
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_format_mini_preview.py --input method_out.json
```

**Parallel execution (multiple files):**

IMPORTANT: When formatting multiple files, use GNU parallel instead of separate Bash tool calls:
```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
export PY="$SKILL_DIR/../.ability_client_venv/bin/python" && \
export S="$SKILL_DIR/scripts/aii_json_format_mini_preview.py" && \
parallel -j 50 -k --group --will-cite '$PY $S --input {}' ::: 'full_data_out.json' 'method_out.json' 'eval_out.json'
```

**Example output:**
```
Generated 3 versions:
  Full (50 items): /path/to/full_method_out.json
  Mini (3 items): /path/to/mini_method_out.json
  Preview (3 items, truncated): /path/to/preview_method_out.json
```

**Parameters:**

`--input` (required)
- Path to input JSON file
- Must have a top-level array
- Example: `method_out.json`, `full_data_out.json`

`--output-dir` (optional)
- Output directory for generated files
- Default: same directory as input file
- Files are prefixed with `full_`, `mini_`, `preview_`

**Output Files:**

All three files use the same base name with different prefixes:
- `full_{basename}.json` - Complete dataset (identical to original)
- `mini_{basename}.json` - First 3 array items only
- `preview_{basename}.json` - First 3 items with strings truncated to 200 chars

**Tips:**
- Input JSON must have a top-level array structure
- String truncation is recursive (applies to nested objects and arrays)
- Use preview files for quick inspection without reading large datasets
- Use mini files for developing/testing code before running on full dataset

**If the script fails** with a connection error (ability server not running): create a local `.venv`, install server deps from `server_requirements.txt` into it, then import the `@aii_ability` function from the script and call it directly — bypassing the server:
```bash
uv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python -r "$SKILL_DIR/scripts/server_requirements.txt"
```
````

### [5] SKILL-INPUT — aii-long-running-tasks · 2026-09-24 11:08:20 UTC

The agent loaded the **aii-long-running-tasks** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-long-running-tasks
description: "Scales an experiment or evaluation up in stages — mini, 10, 50, 100, 200, then the largest run that fits — recording runtime at each step and extrapolating time-per-example against the remaining time budget before growing further, with background execution and hard RLIMIT_AS and RLIMIT_CPU caps. ALWAYS read before launching any script expected to run for many minutes or hours over a dataset. Triggers: long-running job, overnight or unattended run, time budget, how many examples fit, extrapolate runtime, start small then scale up, run in background and poll, avoid a timeout, full-dataset evaluation, resource limits. NOT for choosing the concurrency mechanism itself (aii-parallel-computing), measuring the machine's CPU, RAM or GPU (aii-use-hardware), or provisioning cloud pods (aii-runpod)."
---

## Core Principles

1. **Time budget first**: Read your time/runtime constraints before running anything. Set every Bash timeout to fit within the budget.
2. **Start small, scale up**: Run on minimal input first, fix errors, then increase scale.
3. **Extrapolate before scaling**: Use recorded runtimes to predict whether the next step fits in the budget. Don't guess — calculate.
4. **Background execution**: For anything that takes >1 min, run in background (`run_in_background=true`) and do useful work while waiting.
5. **Stop early if needed**: Quality results on less data beats a timeout or crash. It's always acceptable to stop at a smaller scale.

---

## Gradual Scaling Sequence

Run code at increasing data sizes, checking runtime at each step.

Substitute your actual file names:
- `{mini_file}` — mini JSON (3 examples) from dependency workspace
- `{full_file}` — full dataset from dependency workspace
- `{script}` — your processing script (e.g., `./method.py`, `./eval.py`)
- `{schema}` — JSON schema to validate output against

**STEP 1 — MINI DATA:** Run `{script}` on `{mini_file}`. Do NOT truncate logs. Fix all errors. Validate output against `{schema}`. Verify you are NOT using mock scripts, mock data, or mock APIs.

**STEP 2 — 10 EXAMPLES:** Modify `{script}` to load only the first 10 examples from `{full_file}`. Run and fix errors. Validate schema. Record the runtime.

**STEP 3 — 50 EXAMPLES:** Load first 50 examples from `{full_file}`. Run and fix errors. Record runtime. **EXTRAPOLATE**: Using runtimes from steps 2-3, estimate time per example. Calculate how many examples fit in your remaining time budget. If 50 already used most of the budget, stop here.

**STEP 4 — 100 EXAMPLES (if budget allows):** Load first 100 examples. Run and fix errors. Record runtime. Re-extrapolate with the new data point.

**STEP 5 — 200 EXAMPLES (if budget allows):** Load first 200 examples from `{full_file}`. Run and fix errors. Record runtime.

**STEP 6 — MAXIMIZE:** Using all recorded runtimes, extrapolate time-per-example (it may not be perfectly linear — account for overhead). Calculate the maximum number of examples that fits within your remaining time budget with a 10% safety margin. Load that many (or all if they fit). Run and validate.

## Final Testing Phase

After completing the scaling sequence, redo the entire sequence **one more time** up to your final example count:

mini → 10 → 50 → 100 → 200 → max

At each scale: look for issues, fix problems, validate output, ensure it completes within time limits.

---

## Background Execution

For any step that takes >1 min, run as a **background task**:

1. Launch with Bash `run_in_background=true`
2. While it runs, use the time productively:
   - Sanity-check previous outputs
   - Verify file integrity (correct field names, non-empty values)
   - Review code for edge cases at larger scale
   - Prepare the next step
3. Check back on the background task to get results
4. If it failed, fix errors and re-run

---

## Resource Limits

Set hard RAM and CPU time limits so code fails fast instead of crashing the system. Read limits from `<hardware>` and leave headroom for the OS (e.g., if 16GB total, cap at 14GB).

Python example using stdlib `resource` module:
```python
import resource
resource.setrlimit(resource.RLIMIT_AS, (14 * 1024**3, 14 * 1024**3))  # 14GB RAM
resource.setrlimit(resource.RLIMIT_CPU, (3600, 3600))  # 1 hour CPU time
```
Exceeding RAM raises `MemoryError`. Exceeding CPU time sends `SIGKILL`.

## Monitoring

At each step, record runtime AND check resource usage (`free -h` for RAM, `top -bn1 | head -5` for CPU). If memory usage is climbing toward the limit or CPU is pegged, stop and investigate before scaling further.
````

### [6] SKILL-INPUT — aii-file-size-limit · 2026-09-24 11:08:24 UTC

The agent loaded the **aii-file-size-limit** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

```
---
name: aii-file-size-limit
description: "Splits an oversized generated output file into numbered parts that each fit a size limit: checks sizes with ls -lh, writes full_data_out_1.json, full_data_out_2.json and so on into a matching directory, deletes the original, repoints the reading code at a sorted glob, and regenerates mini and preview variants per part. ALWAYS run right after a script writes JSON output, and whenever a file is too big to keep, exceeds a stated file size limit, or gets rejected for its size. Triggers: file too large, output exceeds the size limit, oversized or huge JSON, ls -lh size check after generating results, splitting or chunking an output file into parts, output directory instead of one file. NOT for: schema validation or making mini and preview variants of a file already within the limit (use aii-json), or general Python script conventions (use aii-python)."
---

## File Size Check

After generating output files, run `ls -lh` to check sizes. If ANY file exceeds the provided file size limit:

1. Create directory with same base name (e.g., `full_data_out/` for `full_data_out.json`)
2. Split into parts under the limit named: `full_data_out_1.json`, `full_data_out_2.json`, etc.
3. Place parts in directory (e.g., `full_data_out/full_data_out_1.json`, `full_data_out/full_data_out_2.json`)
4. Delete the original oversized file
5. Update the script to read from split files: `for f in sorted(glob.glob('full_data_out/full_data_out_*.json')): data.extend(json.load(open(f)))`
6. For each split part, generate its own mini/preview versions with the json skill's format script
```

### [7] SKILL-INPUT — aii-use-hardware · 2026-09-24 11:08:24 UTC

The agent loaded the **aii-use-hardware** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-use-hardware
description: "Detects the CPU, RAM, GPU and VRAM actually available — cgroup v1 and v2 container quotas and CPU affinity rather than misleading host values — then sets RAM and VRAM budgets via resource.setrlimit and torch.cuda.set_per_process_memory_fraction so a script raises a catchable error instead of being OOM-killed, and picks the right torch wheel for the detected device. ALWAYS read before loading a large dataset, installing torch, or sizing batches and worker counts. Triggers: how much RAM or CPU or GPU is available, container memory limit, cgroup, OOM killed, MemoryError, os.cpu_count reports host cores, nproc, VRAM, CUDA available, CPU-only torch build, dataset too big for memory, chunking. NOT for spreading work across that hardware once measured (aii-parallel-computing), staged scale-up runs against a time budget (aii-long-running-tasks), or renting cloud machines (aii-runpod)."
---

**Step 1** — Run `bash scripts/get_hardware.sh` (relative to this skill's directory).

Read the `=== CGROUP ===` section carefully. If `Type: cgroup v1` or `cgroup v2`:
- You are in a **container with hard resource limits**. Exceeding them = OOM kill, no recovery.
- **Never** use `psutil.virtual_memory().total`, `free -h`, `/proc/meminfo`, `os.cpu_count()`, or `nproc` for resource limits — these report **host** values, not your container's allocation.
- **Always** read limits from the cgroup paths shown in the output, or use the Python helpers below.
- For **runtime memory monitoring**, read current usage from cgroup too:
  - v2: `/sys/fs/cgroup/memory.current`
  - v1: `/sys/fs/cgroup/memory/memory.usage_in_bytes`

**Step 2** — Use Step 1 results to pick package variants **before** installing.

Defaults often target the most powerful environment — PyPI's `torch` ships with CUDA libs even on CPU-only hosts. Wrong variant = wasted disk, slow setup, possible import-time failures.

If `=== GPU ===` shows `No GPU`, install torch's CPU build (skips ~4.5GB of CUDA libs):
```bash
uv pip install torch --extra-index-url https://download.pytorch.org/whl/cpu
```
Same idea for any library whose wheel selection depends on detected hardware (GPU/CPU-only builds, architecture-specific wheels).

After install, sanity-check imports right away (`python -c "import torch"`). Disk-pressure or interrupted installs leave half-built wheels (e.g. `libtorch_global_deps.so` missing) — catch these before the experiment runs.

**Step 3** — Set Python constants from the Step 1 results:
```python
import os, math, torch, psutil
from pathlib import Path

def _detect_cpus() -> int:
    """Detect actual CPU allocation (containers/pods/bare metal)."""
    try:  # cgroups v2 quota
        parts = Path("/sys/fs/cgroup/cpu.max").read_text().split()
        if parts[0] != "max":
            return math.ceil(int(parts[0]) / int(parts[1]))
    except (FileNotFoundError, ValueError): pass
    try:  # cgroups v1 quota
        q = int(Path("/sys/fs/cgroup/cpu/cpu.cfs_quota_us").read_text())
        p = int(Path("/sys/fs/cgroup/cpu/cpu.cfs_period_us").read_text())
        if q > 0:
            return math.ceil(q / p)
    except (FileNotFoundError, ValueError): pass
    try:  # CPU affinity (cpuset — used by RunPod, Docker --cpuset-cpus)
        return len(os.sched_getaffinity(0))
    except (AttributeError, OSError): pass
    return os.cpu_count() or 1

def _container_ram_gb() -> float | None:
    """Read RAM limit from cgroup (containers/pods)."""
    for p in ["/sys/fs/cgroup/memory.max", "/sys/fs/cgroup/memory/memory.limit_in_bytes"]:
        try:
            v = Path(p).read_text().strip()
            if v != "max" and int(v) < 1_000_000_000_000:
                return int(v) / 1e9
        except (FileNotFoundError, ValueError): pass
    return None

NUM_CPUS = _detect_cpus()
HAS_GPU = torch.cuda.is_available()
VRAM_GB = torch.cuda.get_device_properties(0).total_mem / 1e9 if HAS_GPU else 0
DEVICE = torch.device("cuda" if HAS_GPU else "cpu")
TOTAL_RAM_GB = _container_ram_gb() or psutil.virtual_memory().total / 1e9
AVAILABLE_RAM_GB = min(psutil.virtual_memory().available / 1e9, TOTAL_RAM_GB)
```

## Step 4 — Set Memory Limits

OOM kills the entire container. **Every script MUST set RAM and VRAM limits at startup.**

Decide the budget based on what the script actually needs. Estimate data size × 2-5x for in-memory overhead, then add ~50% breathing room for temporaries. You may use up to 90% of available RAM/VRAM, but **scale gradually** — start small (e.g. 30-50%), verify it works, then increase toward the limit. Never exceed 90% to keep a buffer for the OS, system processes, and the agent runtime itself. Going over crashes the container/machine with no recovery.

```python
import resource, psutil

_avail = psutil.virtual_memory().available
RAM_BUDGET = ???  # YOU decide: estimate what this script needs (in bytes)
assert RAM_BUDGET < _avail, f"Budget {RAM_BUDGET/1e9:.1f}GB > available {_avail/1e9:.1f}GB"
resource.setrlimit(resource.RLIMIT_AS, (RAM_BUDGET * 3, RAM_BUDGET * 3))  # 3x: virtual > RSS; raises MemoryError on exceed

if HAS_GPU:
    _free, _total = torch.cuda.mem_get_info(0)
    VRAM_BUDGET = ???  # YOU decide: estimate GPU memory needs
    torch.cuda.set_per_process_memory_fraction(min(VRAM_BUDGET / _total, 0.95))  # raises OutOfMemoryError on exceed
```

## Memory-Safe Data Processing

- **One at a time**: load one large object → process → `del obj; gc.collect()` → next
- **Load only what you need**: select specific tables/columns/rows, not entire databases
- **Test small first**: run on a sample before scaling to full data to estimate memory/time
- **Free intermediates in loops**: don't accumulate large results — aggregate incrementally
- **Size before loading**: check file/dataset size before loading; if it's >30% of `RAM_BUDGET`, chunk it

## Common Mistakes (from real crashes)

- **Skipping this skill entirely** — loading data with no RAM detection, no limits, no budget. Container OOM-killed, all agents lost.
- **Using `psutil.virtual_memory().total` instead of `_container_ram_gb()`** — reports host RAM (e.g. 66 GB) when container limit is 28 GB. You MUST use the cgroup-aware functions above.
- **Loading all tables from a multi-table database at once** — one agent loaded 14 RelBench tables simultaneously, spiked past container limit.
- **Setting no memory limits** — without `resource.setrlimit` (RAM) and `set_per_process_memory_fraction` (VRAM), a runaway script OOM-kills the container instead of raising a catchable error.
- **Using `os.cpu_count()` directly** — returns host CPUs (e.g. 192) instead of container limit (e.g. 4) on RunPod/Docker. Always use `_detect_cpus()` above which checks cgroup quota → CPU affinity → `os.cpu_count()` in order.

## Hardware Use

- Keep these results in mind for ALL subsequent tasks — don't assume more than detected
- GPU if available and parallelizable, multiprocessing if multiple CPUs
- Push available resources to their full potential — don't leave hardware idle
````

### [8] SKILL-INPUT — aii-parallel-computing · 2026-09-24 11:08:24 UTC

The agent loaded the **aii-parallel-computing** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-parallel-computing
description: "Parallelises compute-heavy Python: asyncio with aiohttp and a bounded Semaphore for I/O-bound work, ProcessPoolExecutor under the spawn start method for CPU-bound work, NumPy vectorisation and batched PyTorch on GPU with an out-of-memory halving fallback. ALWAYS read before writing any script that loops over data, issues many API calls, downloads many files, or runs heavy computation — sequential loops are the default failure mode. Triggers: parallelise, make a slow script faster, concurrency, async, aiohttp, asyncio.gather, semaphore, multiprocessing, ProcessPoolExecutor, fork deadlock with loguru, worker count, batch size, CUDA out of memory, idle GPU, retries and rate limits. NOT for detecting what hardware exists or setting RAM and VRAM budgets (aii-use-hardware), staged scale-up against a time budget (aii-long-running-tasks), or provisioning cloud pods (aii-runpod)."
---

**ALWAYS parallelize. Sequential processing is unacceptable for any non-trivial workload.** A sequential script doing 1000 API calls takes hours and fails halfway. An async version finishes in minutes with proper error handling. ALWAYS ask: "Can this run in parallel?" — the answer is almost always yes.

Read aii-use-hardware skill first → get `NUM_CPUS`, `HAS_GPU`, `VRAM_GB`, `device`. Set `NUM_WORKERS` proportional to available CPU capacity — check `psutil.cpu_percent(interval=1)` and scale accordingly (e.g. 30% used → use ~70% of cores).

## Decision Tree (follow strictly)

- **I/O-bound** (API calls, downloads, web, file reads) → `asyncio` + `aiohttp` with `Semaphore(NUM_WORKERS * 4)`. NEVER do sequential HTTP requests in a loop.
- **CPU-bound, vectorizable** → GPU available: PyTorch on device / No GPU: NumPy vectorized ops. NEVER loop over array elements in Python.
- **CPU-bound, independent items** → `ProcessPoolExecutor(max_workers=NUM_WORKERS)`. NEVER process items one-by-one when they're independent.
- **Sequential** → only acceptable when items have data dependencies (each depends on the previous result).

## GPU Rules

- Use up to 90% of available VRAM — scale gradually (start small, increase after each successful run, keep 10% buffer)
- Move to device → compute → move back: `torch.tensor(data, device=device)` → `.cpu().numpy()`
- OOM fallback: catch `torch.cuda.OutOfMemoryError` → `empty_cache()` → halve batch size → retry on GPU. Keep reducing until it fits. Stay on GPU.
- Batch large data: chunk it, `del batch` between iterations to free VRAM

## Parallelism Rules

- **CPU-bound**: `ProcessPoolExecutor` + `as_completed`, pre-allocate result list indexed by submission order
- **I/O-bound**: `asyncio` + `aiohttp`, `Semaphore(NUM_WORKERS * 4)`, single shared `ClientSession`, `asyncio.gather(*tasks, return_exceptions=True)`
- Always add `tenacity` retries for transient failures, always set timeouts on HTTP requests
- **CRITICAL — `ProcessPoolExecutor` start method**: Default `fork` deadlocks with loguru (and any threading library). ALWAYS pass `mp_context=multiprocessing.get_context("spawn")` when constructing `ProcessPoolExecutor` in any script that uses loguru, threading, or async I/O. Example:
  ```python
  import multiprocessing as mp
  from concurrent.futures import ProcessPoolExecutor
  with ProcessPoolExecutor(max_workers=N, mp_context=mp.get_context("spawn")) as pool:
      ...
  ```
````

### [9] SKILL-INPUT — aii-handbook-auto-neurosymbolic · 2026-09-24 11:41:20 UTC

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

### [10] SYSTEM-USER prompt · 2026-09-24 11:45:50 UTC

````
<validation-feedback>
Attempt 1 failed validation.

The output file `./.terminal_claude_agent_struct_out.json` does not exist yet.



---

Output the result as JSON to: `./.terminal_claude_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "ExperimentExpectedFiles": {
      "description": "All expected output files from experiment artifact.",
      "properties": {
        "script": {
          "description": "Path to method.py script. Example: 'method.py'",
          "title": "Script",
          "type": "string"
        },
        "full_output": {
          "description": "Full method output JSON file. Example: 'full_method_out.json'",
          "title": "Full Output",
          "type": "string"
        },
        "mini_output": {
          "description": "Mini method output JSON file. Example: 'mini_method_out.json'",
          "title": "Mini Output",
          "type": "string"
        },
        "preview_output": {
          "description": "Preview method output JSON file. Example: 'preview_method_out.json'",
          "title": "Preview Output",
          "type": "string"
        },
        "reproducibility": {
          "description": "Path to reproducibility.md with step-by-step reproduction instructions. Example: 'reproducibility.md'",
          "title": "Reproducibility",
          "type": "string"
        }
      },
      "required": [
        "script",
        "full_output",
        "mini_output",
        "preview_output",
        "reproducibility"
      ],
      "title": "ExperimentExpectedFiles",
      "type": "object"
    }
  },
  "description": "Experiment artifact \u2014 structured output + file metadata.\n\nImplements research methodology with baseline comparison.\nProduces method.py and method_out.json files.",
  "properties": {
    "title": {
      "default": "",
      "description": "Artifact title in plain, everyday language \u2014 short and jargon-free so a non-expert grasps it at a glance and it fits the run visualizations. Aim for about 4-8 words (~40 characters); describe the content, not a status.",
      "maxLength": 90,
      "minLength": 12,
      "title": "Title",
      "type": "string"
    },
    "layman_summary": {
      "default": "",
      "description": "One-sentence plain-language summary of what this artifact does, accessible to non-experts. Used only in the per-artifact README, not in downstream prompts.",
      "maxLength": 250,
      "minLength": 80,
      "title": "Layman Summary",
      "type": "string"
    },
    "summary": {
      "default": "",
      "description": "Summary for downstream artifacts: what this artifact provides",
      "maxLength": 5000,
      "minLength": 500,
      "title": "Summary",
      "type": "string"
    },
    "out_expected_files": {
      "$ref": "#/$defs/ExperimentExpectedFiles",
      "description": "All output files you created. Must include method.py script plus full/mini/preview method output JSON files."
    },
    "upload_ignore_regexes": {
      "description": "Regex patterns for workspace paths that must NOT be published to the GitHub repo, matched against each file's path relative to this artifact's workspace root (POSIX form, e.g. 'cache/abc.json'). Applied ON TOP OF the deploy step's built-in exclusions. Use this for executor-specific caches, large transient intermediates, or content-addressed blob stores (e.g. a cache/ dir of thousands of hash-named files) that would bloat the repo. Examples: ['(^|/)cache/', '(^|/)\\\\.weight_cache/', '(^|/)checkpoints/']. Leave empty if every workspace file should be published.",
      "items": {
        "type": "string"
      },
      "title": "Upload Ignore Regexes",
      "type": "array"
    }
  },
  "required": [
    "out_expected_files"
  ],
  "title": "ExperimentArtifact",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `./.terminal_claude_agent_struct_out.json` exists and contains JSON matching the schema above.

Produce `./.terminal_claude_agent_struct_out.json` again so it contains corrected JSON that matches the schema. Do not invent new fields.
</validation-feedback>
````

### [11] SYSTEM-USER prompt · 2026-09-24 11:08:10 UTC

```
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: An artifact exe... [truncated, 59497 chars total]
```

### [12] HUMAN-USER prompt · 2026-09-24 11:08:10 UTC

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

### [13] SYSTEM-USER prompt · 2026-09-24 11:45:50 UTC

````
<validation-feedback>
Attempt 1 failed validation.

The output file `./.terminal_claude_agent_struct_out.json` does not exist yet.



---

Output the result as JSON to: `./.terminal_claude_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "ExperimentExpectedFiles": {
      "description": "All expected output files from experiment artifact.",
      "properties": {
        "script": {
          "description": "Path to method.py script. Example: 'method.py'",
          "title": "Script",
          "type": "string"
        },
        "full_output": {
          "description": "Full method output JSON file. Example: 'full_method_out.json'",
          "title": "Full Output",
          "type": "string"
        },
        "mini_output": {
          "description": "Mini method output JSON file. Example: 'mini_method_out.json'",
          "title": "Mini Output",
          "type": "string"
        },
        "preview_output": {
          "description": "Preview method output JSON file. Example: 'preview_method_out.json'",
          "title": "Preview Output",
          "type": "string"
        },
        "reproducibility": {
          "description": "Path to reproducibility.md with step-by-step reproduction instructions. Example: 'reproducibility.md'",
          "title": "Reproducibility",
          "type": "string"
        }
      },
      "required": [
        "script",
        "full_output",
        "mini_output",
        "preview_output",
        "reproducibility"
      ],
      "title": "ExperimentExpectedFiles",
      "type": "object"
    }
  },
  "description": "Experiment artifact \u2014 structured output + file metadata.\n\nImplements research methodology with baseline comparison.\nProduces method.py and method_out.json files.",
  "properties": {
    "title": {
      "default": "",
      "description": "Artifact title in plain, everyday language \u2014 short and jargon-free so a non-expert grasps it at a glance and it fits the run visualizations. Aim for about 4-8 words (~40 characters); describe the content, not a status.",
      "maxLength": 90,
      "minLength": 12,
      "title": "Title",
      "type": "string"
    },
    "layman_summary": {
      "default": "",
      "description": "One-sentence plain-language summary of what this artifact does, accessible to non-experts. Used only in the per-artifact README, not in downstream prompts.",
      "maxLength": 250,
      "minLength": 80,
      "title": "Layman Summary",
      "type": "string"
    },
    "summary": {
      "default": "",
      "description": "Summary for downstream artifacts: what this artifact provides",
      "maxLength": 5000,
      "minLength": 500,
      "title": "Summary",
      "type": "string"
    },
    "out_expected_files": {
      "$ref": "#/$defs/ExperimentExpectedFiles",
      "description": "All output files you created. Must include method.py script plus full/mini/preview method output JSON files."
    },
    "upload_ignore_regexes": {
      "description": "Regex patterns for workspace paths that must NOT be published to the GitHub repo, matched against each file's path relative to this artifact's workspace root (POSIX form, e.g. 'cache/abc.json'). Applied ON TOP OF the deploy step's built-in exclusions. Use this for executor-specific caches, large transient intermediates, or content-addressed blob stores (e.g. a cache/ dir of thousands of hash-named files) that would bloat the repo. Examples: ['(^|/)cache/', '(^|/)\\\\.weight_cache/', '(^|/)checkpoints/']. Leave empty if every workspace file should be published.",
      "items": {
        "type": "string"
      },
      "title": "Upload Ignore Regexes",
      "type": "array"
    }
  },
  "required": [
    "out_expected_files"
  ],
  "title": "ExperimentArtifact",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `./.terminal_claude_agent_struct_out.json` exists and contains JSON matching the schema above.

Produce `./.terminal_claude_agent_struct_out.json` again so it contains corrected JSON that matches the schema. Do not invent new fields.
</validation-feedback>
````

### [14] SYSTEM-USER prompt · 2026-09-24 11:49:45 UTC

```
<CRITICAL_ERROR>
The module-end file check FAILED (attempt 1/3).

PROBLEMS:
  - .aii/manifest.yaml: '.git/' names module bookkeeping, which is never a decision
  - .aii/manifest.yaml: 'results/' matches nothing that needs a decision — remove it (text, code and files under the auto-keep floor are always kept)
  - .aii/manifest.yaml: 'labeller/src/__pycache__/' is covered by both a keep and a delete entry — one path, one decision
  - .aii/manifest.yaml: 'labeller/tests/__pycache__/' is covered by both a keep and a delete entry — one path, one decision
  - .aii/manifest.yaml: 'labeller/vendor/__pycache__/' is covered by both a keep and a delete entry — one path, one decision

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

### [15] SYSTEM-USER prompt · 2026-09-24 11:50:34 UTC

```
<CRITICAL_ERROR>
The module-end file check FAILED (attempt 2/3).

THESE PATHS HAVE NO DECISION (one line per directory, with sizes):
  labeller/.pytest_cache/  1236 B  [known cache directory]

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
