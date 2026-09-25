# gen_html_demo — report_results

> Phase: `gen_paper_repo` · `gen_html_demo`
> Run: `gen_paper_repo_a2e1d024cc16` — Cross-Family Solver Consensus as a Gold-Free Faithfulness Metric for Logic Translation
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_html_demo` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-09-25 18:43:36 UTC

````
<design_philosophy>
You are building ONE explorable web page for a research result. The reader should come away
having SEEN the result in the run's own data, because they operated it: they switched between
the conditions the run compared, dragged a threshold and watched the numbers move, pointed at a
mark to see which model or item it was, filtered down to the cases where the method failed, and
put an input beside its output. The page explains through interaction. It is not the paper with
nicer CSS, not a list of headline numbers, and not a gallery of the paper's figures.

WHAT EARNS AN INTERACTION
Every control answers a question a reader actually has at that point, and it changes a view drawn
from the run's real data:
- "Does it hold everywhere?" A chart of the per-condition, per-model or per-dataset results with a
  control over which ones are shown; the baseline always visible; pointing at a mark shows that
  record in full.
- "What does it do to one case?" An item browser over the real per-item records: filter, search
  or sort, and the selected item shows its input, the method's output, the baseline's output and
  the verdict side by side, as a before and after.
- "Where does it break?" A toggle that isolates the failures, the disagreements or the hardest
  slice, with the counts updating as it changes.
- "What if?" A slider over a parameter the recorded data lets the page recompute honestly, such as
  a decision threshold applied to the recorded per-item scores, with the metrics recomputed live.
- "Can I try it?" A live mini-demo of the method, only when the method runs exactly in a few
  dozen lines of JavaScript; it runs on the embedded examples and shows that its output matches
  the recorded one.
- "How does it work?" A stepper that walks ONE real example through the method's stages with the
  values recorded at each stage, over a pipeline diagram that highlights the current stage.
- "What does this word mean?" Term tooltips on hover, focus and tap, with a glossary.
Do not add an interaction that answers no question: no animated counters, no parallax, no
autoplaying carousel, no toggle that swaps one paragraph for a synonym of itself.

THE DATA IS REAL, OR IT IS NOT ON THE PAGE
Every data point comes from the run's output files, embedded as the file has it or trimmed to
the fields a view uses, and every number the prose states matches the paper. A view may compute
from real data (a mean, a filter, a threshold swept over recorded scores), but nothing is ever
invented, interpolated, simulated or smoothed to make a control feel richer. A page that looks
excellent and misreports one result is worse than no page.

ONE STORY
Top to bottom the page tells one story: the question, the answer shown in a view the reader can
operate at once, how the method works, the evidence to explore, where it fails, and what it does
not show. Each view opens with the question it answers and closes with one takeaway sentence
that rewrites itself to describe what the current selection shows.

CRAFT
- Type carries the design: one system font stack, a real scale with visible jumps between levels,
  body text around 17-19px with a measure of 65-75 characters and generous line height.
- Colour is restrained: a light, near-white ground, one dark ink for text, one accent for links,
  the active state and the highlighted series, a muted second colour for baselines, and a
  colour-blind-safe palette when series need more. No gradients as decoration, no purple-to-blue
  banner, no emoji, no icon fonts.
- Charts are read, not decorated: labelled axes with units, a legend when there is more than one
  series, gridlines light enough to recede, and the exact value one hover, focus or tap away.
- Controls look like controls: a visible affordance, a visible selected state, a visible focus
  ring, and a hit area of at least 40 by 40 pixels on a phone.
- Motion is a courtesy: short transitions on state changes only, and none at all under
  prefers-reduced-motion.
- Every interactive element works with a keyboard and tells a screen reader what it is and what
  state it is in. That is part of the craft, not a checklist bolted on at the end.

FINISH IT
The page is done when you have opened it in a headless browser, operated every control, seen no
script error, read it at a phone width and a desktop width, and found nothing to fix. Not before.
</design_philosophy>

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
Your workspace: `/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_assemble_paper/paper`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_assemble_paper/paper/`:
GOOD: `/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_assemble_paper/paper/file.py`, `/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_assemble_paper/paper/results/out.json`
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
Name each kept artifact in your results and your `README.md` by its path
RELATIVE to your cwd, and say it stays on the run's volume rather than in the
published repository. Never write an absolute server path into a file that is
published: a reader's machine has none of them.
</disposable_outputs>

<task>
Build ONE self-contained, explorable `interactive.html` for this run's result. The
reader operates views drawn from the run's REAL output data (switching conditions, dragging a
threshold, pointing at marks, filtering items, comparing an input with its output) and comes
away understanding the finding and the method. It is published next to the paper, and its most
prominent link is the paper PDF.
</task>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<what_is_already_here>
Your workspace is the finished paper folder. You are adding one file and, where needed, PNG
renders of figures, and linking that file from the presentation page. Change nothing else, and
keep your scratch work (extraction scripts, screenshots) in a temporary directory outside this
folder, because the folder is published.

- `paper.tex`: the paper as written. It is the source for every claim, name, term
  definition and number the prose states.
- `paper.pdf`: the compiled paper. Do not link to it by this local name; link to the
  full URL in the links section.
- `references.bib`: the bibliography, when the paper has one.
- `figures/`: every figure the paper uses, flattened into one folder.
- `index.html`, when present: the paper's static presentation page and the site's
  landing page. Change it in one way only: add the link to your page described under
  presentation_link.
- `workspace/`: the scratch folder the LaTeX task worked in. Ignore it.
</what_is_already_here>

<artifact_data>
Every artifact this run produced, with the directory it ran in and the output files it declared.
These directories are on disk and you can read them. Their JSON and CSV outputs hold the REAL
per-item and per-condition results: the recorded inputs and outputs, the scores, the verdicts,
the per-model and per-setting metrics. They are what the page's views are built from. Where a
file has `mini_` and `preview_` variants beside it, read those first to learn its shape.

- iteration: 1
  name: gen_art_experiment_1
  type: experiment
  title: Screening a three-layer logic-translation checker
  summary: >-
    FOL-Triage wide screen (iter-1 exp A), all under this workspace. Frozen shared screen: screen_items.json (track L = 753
    Logic-LM FOLIO-dev outputs of gpt-3.5/gpt-4/davinci-003 vs DSAVlab corrected gold, 112/202 conclusions + 271 agreed premises;
    track H = 302 curated original->corrected), href_items.json, invariance_set.json, screen_meta.json; item_id=sha1(system|norm(text)|fol)[:16]
    for joining with sibling experiments. Labels (iter-3 repair census, xor precedence fixed): L CORRECT 278 / ERROR 199 /
    UNCERTAIN 204 / UNPARSEABLE 60; 59% of ERRORs are pure ADD+DROP vocabulary artefacts (needs panel adjudication). Released
    functions in src/fol_triage.py: fol_lint (L1), content_accounting (L2-bow), role_accounting (L2-role), formula_role_profile
    + role_questionnaire (gemini-2.5-flash-lite, text only) + l3_compare (L3); fused logistic fitted on track H with sentence-leak
    guard, frozen in prereg.json before track-L labels. PRIMARY (L ERROR vs CORRECT, n=477, 199 pos): fused AUROC 0.759 [0.695,0.825];
    L2-bow 0.737; L3 0.756; L2-role 0.557; L1 0.508 (lint does not transfer to LLM outputs; 0.655 on track H); fused-L2bow
    +0.022 CI [-0.019,0.061] not significant; decomposed judge (LLM reads formula instead of z3) lowers L3 AUROC by 0.059
    (sig.); nonce-disguise shows no contamination (0.765 vs 0.770). Gates: AUROC/coverage 0.92/cost $0.0002 pass; rewrite-FA
    FAILS (0.275; originals flagged at same rate, fused FA on L CORRECT 0.19 vs 0.10 calibrated on H; flip rate <=0.06). Long/conditioned
    strata UNTESTABLE on this screen. L3 gate on HREF: role .91, claims .86, missing .92, extra .92 gated; force .69 excluded.
    Robustness rows: qwen3-30b and local Qwen2.5-1.5B (OpenRouter outage fallback). Headline AUROCs re-derived independently
    (results/audit_rederive.json, placebos ~0.5). Judge/round-trip/self-consistency baselines are NOT here (experiments C/D;
    join on item_id in iteration 2). Outputs: method_out.json (exp_gen_sol_out; predict_fol_triage + per-layer predict_* per
    item), results/metrics.json, results/per_item.jsonl, README.md. Spend $0.29.
  workspace: >-
    /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_1
  output_files:
  - method.py
  - full_method_out.json
  - mini_method_out.json
  - preview_method_out.json
- iteration: 1
  name: gen_art_experiment_3
  type: experiment
  title: Do other models' translations agree? Consensus metric for NL-to-logic
  summary: >-
    Experiment 3 screens candidate C, a text-free, gold-free consensus metric for NL->FOL faithfulness, on the shared frozen
    screen (label hash 0e43cbdd...). c_score = 1 - eq_frac: the share of OTHER systems' translations of the same sentence
    that are NOT z3-equivalent to the candidate modulo vocabulary alignment. The pool has 6 fresh OpenRouter families (llama-3.3-70b,
    qwen3-235b, deepseek-v3.1, mistral-small-3.2, gemini-2.5-flash-lite, gpt-4.1-mini) plus the 3 released Logic-LM systems,
    leave-one-out. Also scored: medoid repair depth and operators, and semantic entropy over z3 classes. Baselines: K=5 self-consistency
    (gpt-4.1-nano T=0.7 on all items; true same-model gpt-3.5-turbo SC for gpt-3.5 candidates), predicate-set stability, and
    FOL length. PRIMARY (track L, 297 CORRECT vs 249 ERROR, sentence-clustered bootstrap 2000): c_score AUROC 0.866 [0.821,
    0.906]; peers-only 0.872; non-OpenAI peers 0.863; other Logic-LM systems only 0.753; cluster entropy 0.773; medoid depth
    0.722; sc5_cheap 0.725 [0.669, 0.781] (n=546, now complete). Paired Δ c_score - sc5_cheap = +0.140 [0.085, 0.197]; c_score
    - sc5_same = +0.140 [0.057, 0.227] (n=167). Cross-fitted [c_score, sc5] vs [sc5] = +0.147. Vocab-clean subset (shared-aligner
    confound control): c_score 0.852 vs SC 0.714. At the medoid threshold: recall 0.62, false alarms 0.14. Shared blind spot:
    38% of errors are endorsed by the consensus (POLARITY 5%, COVERAGE 41%, STRUCT 57%). Repair operators match the labeller's
    81% of the time (chance 46%). RENAME rewrites cause 96% false alarms (the aligner does not survive synonym or constant
    renaming); z3-equivalent rewrites flip 0% by construction. Long/conditioned stratum n=5, descriptive only. Cost: $1.52
    total; the peer pool costs $0.0015 per sentence. This re-run completed the SC_cheap arm that the shared-key limit had
    cut to 231/307 units, and restored WordNet for RENAME.
  workspace: >-
    /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3
  output_files:
  - method.py
  - full_method_out.json
  - mini_method_out.json
  - preview_method_out.json
- iteration: 1
  name: gen_art_experiment_4
  type: experiment
  title: Cheap LLM judge and baseline scores for logic translations
  summary: >-
    Experiment D (baseline/null arm) on the SHARED FROZEN SCREEN: data/screen_items.json, 1,090 items. Track L = 796 Logic-LM
    FOLIO-dev outputs labelled vs corrected gold or agreed premises: 294 CORRECT / 230 ERROR / 216 UNCERTAIN / 56 UNPARSEABLE.
    Track H = 294 curated original-vs-corrected items. Label-vector sha1 122d01df... FINAL judges are the planned API models,
    under prereg.json: judge_cheap = gemini-2.5-flash-lite (JSON 0-100, rubric A), judge_cheap2 = gpt-4.1-nano (P(YES)), judge_strong
    = gemini-3.1-pro-preview (frontier; 200L+96H subset). Open-weight local judges (Qwen3-8B, Llama-3.1-8B, Qwen3-14B-nf4;
    run during a key outage) are kept as judge_local_* rows. API spend $2.02. Track L AUROC [95% CI]: judge_cheap_disg 0.777
    [0.720, 0.827] = THE BAR; judge_cheap_orig 0.749; gpt-4.1-nano 0.750/0.714; frontier orig 0.802 on the subset, which is
    +0.077 [0.006, 0.154] over the cheap judge on the same items (DeLong p=.015), with the gap vanishing under disguise; rt_nli_min
    0.710 (API verbaliser) / 0.740 (local verbaliser); rt_embed_cos 0.633; rt_reformalise_eq 0.513 (near chance). User's pilot
    structural metrics are 0.50-0.53 (a negative result); cross-system rerun Jaccard 0.720. The cross-fitted S4 combination
    of all cheap baselines has OOF AUROC 0.817 [0.762, 0.867], which is +0.039 [-0.010, 0.087] over the judge (not significant).
    best_baseline_oof per item and data/folds.json are provided for nested deltas in iteration 2. Contamination: no evidence.
    Every DiD CI includes 0; the frontier judge loses ~0.07 under disguise on both tracks (lost lexical meaning); the recall
    probe matches the corrected gold 15.9% vs the erroneous original 4.4%. Invariance: the judges false-alarm on contrapositive
    (cheap 0.67, nano 0.97), De Morgan and rename rewrites. Judge correctness falls with sentence length (p=1.6e-5); long
    sentences are untestable on track L. Label noise: 56% of L ERRORs are subst_only; results/judge_label_disagreements.csv
    is there for dataset-E adjudication. All headline numbers were re-derived independently, with placebos, in results/audit_headlines.json.
    Outputs: method_out.json / full_method_out.json (workspace root; also results/method_out.json) (predict_* = oriented scores),
    results/analysis.json, results/summary.md.
  workspace: >-
    /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_4
  output_files:
  - method.py
  - full_method_out.json
  - mini_method_out.json
  - preview_method_out.json
- iteration: 1
  name: gen_art_dataset_1
  type: dataset
  title: Held-out logic translation test set, panel-checked
  summary: >-
    Held-out NL->FOL faithfulness meta-evaluation set (run_An1uy2kF2SjZ, iter 1, dataset E). full_data_out.json (exp_sel_data_out,
    27.7 MB) has 4 groups. (1) heldout_candidates: 8,507 rows = real FOL candidates for 700 screen-disjoint sentences. Strata:
    MALLS-train L25=300 (>=25 words, >=3 conditions; includes a pre-registered 100-sentence top-up), L20=150, EXC=100 (unless/except/without),
    and FOLIO-train CTRL=150. Generators: 10 LLM slots over 9 families, few-shot at temperature 0; zero-shot Llama-70B/Qwen3;
    GPT-5.1 on 200 sentences; ccg2lambda; the MALLS GPT-4 gold as a system. input=JSON{text,candidate_fol,reference_fol,system,prompt_variant};
    output=CORRECT/ERROR/CONTESTED/UNRESOLVED/UNPARSEABLE. Labels combine the shared z3 solver labeller with a blind, nonce-disguised,
    family-disjoint panel (Haiku-4.5/GLM-4.6/Kimi-K2; Haiku adjudicates only GLM/Kimi disagreements). The combination rule
    gives tier A (solver), B (panel-decided VOCAB_GRAN/COMPOUND) and C (no trusted reference). Metadata per row: sentence_id
    (bootstrap cluster), item_id, strata {words,n_quant,depth,n_conditions,exception_type,source_stratum,l25_topup_batch},
    auto_label, repair_ops, panel_votes, error_ops, label_tier, reference_status, correct_not_equivalent, reading_choice,
    disguised_text/fol. Tier A+B testable: L25 176 CORRECT/697 ERROR; L20, EXC and CTRL are also testable. (2) heldout_sentences:
    700 rows with reference status (GOLD_PANEL_OK 95, PANEL_REPAIRED 145, NO_TRUSTED_REFERENCE 295, TRUSTED_AGREED 36, DISPUTED
    112). (3) panel_calibration: 77 synthetic gate items plus 96 expert track-H real-error pairs with panel votes. (4) screen_audit:
    1,173 Logic-LM track-L and curated track-H rows keyed by the screen's item_id; also in screen_adjudicated_labels.json.
    Caveats: the panel is STRICT. Its majority accuracy on real errors is 0.727, and it accepts only 0.61 of expert-corrected
    formulas. It rejected 82% of MALLS gold, so ERROR is over-called: confirm on tier A too. HELD-OUT: iteration 2 must not
    tune thresholds on it. Primary analysis = tiers A+B excluding CONTESTED and reading_choice, bootstrapped by sentence_id.
    See dataset_card.md. Cost $9.83.
  workspace: >-
    /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_dataset_1
  output_files:
  - data.py
  - full_data_out.json
  - preview_data_out.json
  - mini_data_out.json
- iteration: 2
  name: gen_art_experiment_5
  type: experiment
  title: Peer agreement plus text checks, held-out test
  summary: >-
    Held-out confirmation of PEER+TEXT (NL->FOL faithfulness without gold) on dataset E (8,507 candidate rows, 700 sentences),
    frozen on the iteration-1 screen (prereg sha256 b9f28b1b, git a6896ce) and scored once. PEER = graded cross-family consensus
    (claim units, peer aligned into candidate vocabulary, finite-model refuter + z3 entailment; support/coverage/g_score,
    unit error codes); TEXT = iteration-1 L2-bow + L3 (text-only questionnaire vs z3 role profile); fused by a screen-fitted
    logistic. RESULTS (R_AB tiers A+B, 1822 ERR/864 COR): PEER+TEXT AUROC .790 [.75,.82] (stratified .753; long pool .768;
    tier-A L20+EXC .818) vs iteration-1 c_score_align .782, NF-anchored c_score .743, TEXT .693, local Qwen3-8B disguised
    judge .712. Delta vs local judge +.078 [.043,.112] pooled, +.115 long pool, +.075 stratified; CTRL -.031 n.s. The pre-registered
    flash-lite judge bar is UNTESTABLE (shared OpenRouter key hit $0 at 18:00 UTC; the replacement key was also exhausted,
    polled 19:10-22:13 UTC; 20 rows); the local judge is a labelled secondary bar. Fusion does NOT beat c_score_align alone
    (stratified +.011 n.s.; tier A c_score_align .860 > .818), and that aligner is shared with the solver labeller (confound
    open). Name-free alignment 'failed' the screen gate only through a threshold-tie artefact; post hoc NF-anchored passes
    (RENAME FA .074, ROLE_PERMUTE recall .77) and its fusion gives .759 on E. P1 INCONCLUSIVE (PEER>TEXT on ADD/DROP errors,
    TEXT>PEER on peer-endorsed), P2 REFUTED, P3 INCONCLUSIVE (gap vs judge grows with length, diff-in-delta +.146 CI>0), P4
    REFUTED (fused RENAME FA .385). Unit-code typing at chance (.37 vs .38). Disguise improves the judge (no contamination
    benefit). Within-stratum placebo .59 (composition), global .50. FILES: results/per_item_E.jsonl (row_key=item_id|prompt_variant,
    fold_E=sha1('E_folds_v1|'+sid)%5, every score) for the iteration-3 join; results/analysis.json, tables.md, p_tests.json,
    deviations.json, prereg.json; src/peer_text.py reusable functions; method_out.json (exp_gen_sol_out, predict_* for all
    metrics). Audits: tests/audit_rederive.py re-derives pooled AUROCs and headline delta to 1e-9; tests/placebo_headline.py
    (shuffled labels fail); prefilter audit 0 conflicts; judge prompt identity 30/30. OpenRouter spend $0.155.
  workspace: >-
    /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_5
  output_files:
  - method.py
  - full_method_out.json
  - mini_method_out.json
  - preview_method_out.json
- iteration: 2
  name: gen_art_dataset_3
  type: dataset
  title: Long logic sentences and FOL error suite
  summary: >-
    Two held-out NL->FOL faithfulness tables (full_data_out.json, aii exp_sel_data_out, every row re-verified against its
    sources by data.py and z3-re-verified by src/verify.py, 0 failures). (1) PERTURB (group perturb_suite, COMPLETE): 4,234
    typed mutants (metadata_fold PERTURB, output ERROR, error_ops=[op]) plus 868 meaning-preserving controls (PERTURB_CONTROL,
    output CORRECT). They cover 300 bases: 36 TRUSTED_AGREED + 95 GOLD_PANEL_OK + 69 PANEL_REPAIRED dataset-E references,
    and 100 R_COMP weak readings. Operators are NEG, REV, QUANT, RESTR, CONN, MOVE, DROP, ADD (ADD_FOREIGN / ADD_INTERNAL),
    SWAP, BIND and MEANING_RENAME, at DOWN/UP positions (metadata_position_polarity, polarity_method, matched_pair_id; 1,354
    complete pairs). QUANT/REV/RESTR are UP-only; SCOPE and UNGLUE have 0 rows. Each mutant is z3 non-equivalent to every
    accepted reading. Controls are RENAME_SYN / RENAME_NONCE, REORDER and CONTRAPOSITIVE/DEMORGAN, each z3-equivalent. (2)
    R_COMP (group rcomp_sentences): 250 main + 100 reserve templated sentences, each with >=25 words, >=3 conditions and one
    unless/except/provided-that/only-if clause (9 templates). Weak and strong references come from the template (T8 also stores
    a not-accepted converse), are unit-tested and z3-checked, and are built from a 652-entry atom lexicon mined from verified
    FOLIO/MALLS references. Provenance fields: template_id, lexicon_ids, source_rule_ids. CAVEAT: the shared OpenRouter key
    hit its daily limit 5 minutes in ($0.41 spent); the 21:38 UTC replacement key was also already exhausted. Pending: the
    Sonnet lexicon and reference audits, fluency, generator candidates (rcomp_candidates), solver labels, adjudication and
    the testability declaration. ./run_all.sh completes them resumably under the pre-registered prereg_rcomp.json. Until then
    R_COMP must not be used for metric claims. PERTURB is ready for per-operator sensitivity and invariance analysis. Rows
    carry item_id (E's recipe) and disguised_text/fol. adjudicator_check_out.json holds 60 known-label QA items. See dataset_card.md.
  workspace: >-
    /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3
  output_files:
  - data.py
  - full_data_out.json
  - preview_data_out.json
  - mini_data_out.json
- iteration: 2
  name: gen_art_evaluation_1
  type: evaluation
  title: Re-checking earlier logic-metric results across label sets
  summary: >-
    Zero-LLM-spend, CPU-only re-analysis of the iteration-1 artifacts (exp A FOL-Triage, exp C consensus c_score, exp D judges/baselines,
    dataset E screen adjudication), joined on item_id. eval.py (+src/) writes eval_out.json (exp_eval_sol_out, validated;
    ~5.9k flat metrics_agg keys + structured metadata incl. VERDICT; 1,380 per-item examples with oriented scores, per-regime
    labels, PT OOF), tables/*.csv (each with a '# source:' line), figures/fig_regime_shift and fig_forest_common (json/png/pdf),
    and audit/ scripts. KEY FINDINGS. (1) Re-derivation gate: 57/57 reviewer audit numbers reproduce (n=389/160 err/151 sents;
    c_score .842, fused .767, judge_disg .785; tier A+B n=304 fused .872, bow .817, c_score .776, judge .771). (2) Same-item,
    same-label common sets for 13 regimes (testable: R_SOLVER_CONS n=373/155 err, own-label A/C/D, R_ADJ_AB 298/165, R_ADJ_ALL
    498/271, CONTESTED->C/E, L_UNPARSEABLE_AS_ERROR 413/195; R_ADJ_A and all track-H regimes are untestable, reported sign-only).
    (3) The iteration-1 rule FAILS for fused_H and c_score in every regime (rewrite FA 0.275 / 0.96). fused_H minus judge
    is -0.013 under solver labels but +0.096 [.020,.171] under A+B; c_score minus judge is +0.067 [-.012,.148] under solver
    labels and +0.006 under A+B. (4) Label-only shift solver->A+B on the same 161 items: bow +0.102 and fused +0.080 (CI>0)
    go up; c_score -0.106 goes down. Rank Kendall tau is 0.60. On the 58 flipped items, bow/fused flag 81-83% vs c_score 34%
    (instrument-sharing confirmed). (5) SCREEN PREVIEW: PT (cross-fitted c_score+bow_uncarried+l3) minus judge_cheap_disg
    is +0.089 [.010,.165] solver, +0.104 [.039,.175] A+B, +0.090 [.038,.142] all tiers, +0.118 unparseable-as-error. Nested
    S4+PT over refit S4 is +0.04-0.06 (CI>0). Screen bar that iteration-2 confirmation must beat = these deltas. (6) P1: the
    structural clause is untestable (all QUANT/SCOPE/BIND/SWAP/NEG cells have <15 errors); text beats peers on peer-endorsed
    errors (CI>0). P2a CONFIRMED only for all tiers. P2b depends on the comparator: vs c_score the gain comes from endorsed
    errors; vs bow it comes from non-endorsed errors. (7) At matched FA 0.10 the ORIGINAL cheap judge has higher recall than
    the disguised one (+0.11/+0.20). Contamination DiD CIs include 0 but MDE = 0.12-0.21, so a 0.05 effect is undetectable.
    Frontier minus cheap under A+B is +0.166. (8) Invariance comparisons across A/C/D used different rewrite sets. (9) Candidate
    B was planned but gen_art_experiment_2 is an empty .aii/ dir: it never ran. (10) Exp C's -0.94/SD length interaction reproduces
    exactly. Exp A's L2-bow = n_unanch+uncarried (0.737) vs bow_uncarried (0.711). Panel expert-pair acceptance is .613 (unambiguous).
    Independent re-derivation (different code path) matches all headline numbers. On permuted labels the cross-fitted PT is
    biased below 0.5; the observed deltas exceed all 20 null deltas (null max .047 solver / .087 A+B).
  workspace: >-
    /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1
  output_files:
  - eval.py
  - full_eval_out.json
  - mini_eval_out.json
  - preview_eval_out.json
- iteration: 3
  name: gen_art_experiment_6
  type: experiment
  title: Peer agreement vs paid AI judges on held-out logic
  summary: >-
    T1 head-on test on held-out NL->FOL dataset E (8,507 real candidates, 700 sentences). The frozen peer-agreement consensus
    metric (c_score_align, exp 5) and PEER+TEXT fusion (p_peer_text) are compared with newly scored paid API comparators:
    gemini-2.5-flash-lite rubric-A JSON judge (disguised + original, every parseable row), gpt-4.1-nano P(YES) judge (both
    views), gemini-3.1-pro-preview frontier judge (original view, 284-row frame; disguised view blocked by the pre-registered
    shared-key reserve rule), API round trip (flash-lite verbaliser -> DeBERTa NLI/mpnet) and API SC-5 (nano, T=0.7, z3 modulo
    vocabulary); plus S4_full, a cross-fitted stack of all 28 baselines. Pre-registered in prereg_T1.json (sha256 c2a6cf84,
    frozen before any sweep score). Main population R_AB E_POOL PRIMARY n=2,686 (1,822 ERROR/864 CORRECT, 292 sentences);
    sentence-cluster bootstrap B=2000. RESULTS: stratified AUROC c_score_align 0.741 vs flash-lite disguised 0.642 (pooled
    0.782 vs 0.696). (a) CONFIRMED: strat dAUROC +0.099 [0.049,0.146]; long pool +0.116 [0.070,0.163]; R_A L20+EXC +0.299;
    also vs best cheap judge (nano orig) +0.089 [0.043,0.134]. (b) CONFIRMED: nested [S4_full+c]-S4_full strat +0.039 [0.021,0.057],
    permutation-null p95 0.009; c alone ~= S4_full (+0.006 [-0.031,0.042]). (d) CONFIRMED: frame ratio vs frontier 0.957 [0.887,1.034],
    consensus $1.2e-4 vs frontier $3.65e-3/item, nested frame gain +0.037 [0.008,0.066]. VEX aligner-confound control CONFIRMED:
    +0.306 [0.232,0.376]. M3 (smaller length slope than the judge) DISCONFIRMED: +0.146 [-0.051,0.361]. Overall T1 (this artifact):
    CONFIRMED. Caveats: no advantage on the short FOLIO CTRL stratum (-0.069 [-0.23,0.10]) or on <12-word / <=1-condition
    sentences; the advantage concentrates in long, conditioned, exception sentences (EXC +0.197). Consensus misses aligner-masked
    MEANING_RENAME errors (recall 0.07 at FA 0.10 vs judges 0.13-0.20) and peer-endorsed errors (0.00). Flash-lite contamination
    DiD +0.105 [0.006,0.201] (MDE 0.14). Test-retest Spearman 0.975. API spend $2.395 (cap $4.60). Independent checks: tests/audit_T1.py
    (5 headline numbers match to 1e-3) and tests/audit_raw_T1.py (raw files -> identical confirmatory/long-pool delta and
    frame ratio; placebos fail as required). Files: results/analysis_T1.json, verdict_T1.json, tables_T1.md, per_item_T1.jsonl,
    deviations.json, api_cost_ledger.json, llm_cache.jsonl; figures/forest_T1, complexity_curves; full_method_out.json (predict_*
    oriented scores for every metric).
  workspace: >-
    /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6
  output_files:
  - method.py
  - full_method_out.json
  - mini_method_out.json
  - preview_method_out.json
  - reproducibility.md
- iteration: 3
  name: gen_art_experiment_7
  type: experiment
  title: Model agreement vs judges on long rule sentences
  summary: >-
    R_COMP (221 templated long rule sentences, >=25 words, >=3 conditions, one unless/except/provided-that/only-if clause;
    references trusted by construction) translated by 10 few-shot LLM slots (9 families) in two conditions. SIG (signature
    block given) is labelled by pure z3 equivalence to the weak or strong reading; FREE uses dataset 3's solver labels (tier
    A only: the dataset-E panel was not run because the shared key was exhausted, so FREE is NOT_TESTABLE and descriptive).
    PRIMARY (pre-registered, criterion c): within-template AUROC of c_score_sig (share of family-disjoint peers not z3-equivalent)
    vs the disguised gemini-2.5-flash-lite rubric-A judge on 1,904 SIG rows (395 ERROR / 1,509 CORRECT, 220 sentences): 0.954
    vs 0.587, delta +0.367 [0.328, 0.404] (sentence-clustered, template-stratified bootstrap, B=2000) -> PASS. vs the original-text
    judge: +0.278 [0.239, 0.319]. Nested [judge + c_sig] over [judge] +0.377; the judge adds ~0 over c_sig. Frontier gemini-3.1-pro
    on a 60-row subsample: c_sig 0.956 vs frontier orig 0.932 / disg 0.735; [frontier + c_sig] over frontier +0.088 [0.019,
    0.172]. On R_COMP the disguise itself costs judges AUROC (cheap +0.085, local Qwen3-8B +0.175 orig - disg), because templated
    sentences cannot be memorised. Rename invariance: NF-anchored and HYB consensus are invariant (FA 0.26 = unrenamed), ALIGN
    and SIG-exact are not (FA 1.0 on nonce renames). Mechanism: error endorsement e = 0; consensus false alarms are correct
    translations of the minority strong reading (flagged 96% vs 14% for weak). Complexity: no length slope for consensus (GEE).
    FREE tier A: c_align - judge +0.214 [-0.034, 0.377], and consensus AUROC falls from 0.95 (SIG) to about 0.80, the vocabulary-divergence
    cost. Every headline number was re-derived from the raw files via an independent brute-force path (tests/rederive_raw.py,
    all match to 1e-9; placebos fail). Outputs: method_out.json (R_COMP_SIG, R_COMP_FREE; predict_* oriented higher = error),
    results/rcomp_candidates.jsonl (per-row labels, strata, z3 class ids, all scores), results/analysis.json, results/tables.md,
    results/deviations.json (15 deviations), src/consensus_rcomp.py (consensus_exact, consensus_scores). Spend $1.58.
  workspace: >-
    /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7
  output_files:
  - method.py
  - full_method_out.json
  - mini_method_out.json
  - preview_method_out.json
  - reproducibility.md
- iteration: 3
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
    unrenamed-reference FA (references often unendorsed on long sentences). E R_AB stratified AUROC (sentence-cluster CI):
    c_hyb 0.738, c_align 0.741, c_nf 0.686; HYB-ALIGN -0.004 [-0.011,0.004]; HYB-NF +0.052; HYB-local Qwen judge +0.060 [0.018,0.100];
    placebo 0.515. Over-alignment: HYB's extra agreements are label-discordant 0.388 vs 0.127 for ALIGN agreements. PART B:
    27 metrics on 4,234 PERTURB mutants + 868 controls + 300 bases (results/perturb_scores.jsonl, perturb_sensitivity.csv,
    perturb_downup.csv, invariance_table.csv, tradeoff.csv, coverage_perturb.csv; prereg_perturb.json). Within-base AUROC
    over all E-base mutants: PEER+TEXT 0.948, c_align 0.866, c_hyb 0.847, p_text 0.845, l3 0.816, c_nf 0.785 (0.50 on MEANING_RENAME),
    S4_local 0.753, round-trip NLI 0.749, flash-lite judge (disguised) 0.680, SC-5 0.666, L2-bow 0.659, local Llama/Qwen judges
    (nf4) 0.653/0.643, pilot metrics ~0.50. Consensus polarity-symmetric (|DOWN-UP|<0.01); local judges, embedding round trip
    and L3 miss DOWN edits (-0.12 to -0.15). PART C: peer-medoid typed-repair typing 0.328 [0.277,0.387] > majority 0.177;
    oracle 0.802; 20 s fallback unchanged. PART D: src/consensus_lib.py (consensus_score exact/align/nf/hyb, graded_consensus,
    peer_pool, equivalent_modulo_vocab, minimal_typed_repair) + tests (31 pass). Deviations: 16 GB GPU -> nf4 local judges
    with thresholds refit on nf4 E calibration rows (AUROC cost 0.015-0.035); S4 full-E fit. Cost $0.35 OpenRouter. Independent
    raw re-derivation (tests/audit_raw.py) reproduces all headline numbers exactly; placebos ~0.5.
  workspace: >-
    /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_8
  output_files:
  - method.py
  - full_method_out.json
  - mini_method_out.json
  - preview_method_out.json
  - reproducibility.md
- iteration: 3
  name: gen_art_evaluation_2
  type: evaluation
  title: Why cross-model agreement flags logic errors
  summary: >-
    T4 consensus-mechanism audit on dataset E (CPU only, $0, no LLM calls) plus a file-sourced verified record of iteration
    2. Recomputed the label-free pairwise z3 eqmv matrix over every parseable output of all 700 E sentences (29,107 pairs;
    bit-identical across 3 runs); it reproduces the FROZEN c_score_align (G2 mismatch 0.33%, explained by PYTHONHASHSEED);
    gates G0/G1 pass. R_AB (2,672 scorable rows): graded c_score_align AUROC 0.784 vs binary majority END_MAJ 0.669 (delta
    +0.114 [0.091,0.140]); END_MAJ e=0.124, d=0.537 (AUROC_b = 1-(e+d)/2, a bookkeeping identity). Aligner-free c_score_exact
    0.748. VOCAB_EXACT pure-z3 labels (85/412): c_score_align 0.929. eqmv non-transitivity 15.8% (classes approximate). Verdicts:
    M1 (e falls with n_conditions, partial) INCONCLUSIVE; M2 (d rises with words) CONFIRMED by the prereg rule but NON-SPECIFIC
    (shuffled-label placebo still +1.75; label x words interaction -0.29 [-0.77,0.20]); NET Delta(e+d) words T3-T1 +0.356
    [0.198,0.493] -> binary consensus DEGRADES with length, driven by d (placebo -0.034, covers 0); SCATTER SI_err 0.159 vs
    SI_cor 0.760 (ratio 4.45), SI_err falls with conditions, joint failure rises (errors co-occur but differ); M3-local INCONCLUSIVE;
    M4 k95=3 CONFIRMED (AUROC(k) 0.685..0.784; long-sentence tercile k95=5); cross-fitted best 3-family pool deepseek+microsoft+openai
    OOF 0.785 = full pool at ~$0.002/sentence; LOFO min delta -0.011 (no single family carries it). Verified record: 48/48
    hypothesis clauses VERIFIED_MATCH; reviewer PT-S4 audit reproduced (points 1e-4, CIs 0.01) plus stratified rows (PT-S4
    strat +0.059); corrections, R_PANEL renames, R_ADJ gate (DROPPED), B2 dead end, PERTURB counts (4234/868/1354), label
    facts. Independent audit re-derived 13 headline numbers to 1e-9 with placebo checks. Scope: E only (R_COMP rerun via shipped
    pairwise_matrix()/ed_decomposition() in iteration 4). Files: eval_out.json (335 metrics, one example per R_AB row with
    predict_c_score_align/exact/b_endmaj/endfam2/c_k3_best_oof), pairwise_classes_E.jsonl (label-free join key), tables/*.csv
    with '# source:' lines, figures fig1-4, prereg_mech.json, audit/, results/part_a.json.
  workspace: >-
    /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2
  output_files:
  - eval.py
  - full_eval_out.json
  - mini_eval_out.json
  - preview_eval_out.json
  - reproducibility.md
- iteration: 3
  name: gen_art_research_1
  type: research
  title: What is new about peer agreement for logic
  summary: >-
    Prior-art positioning (web research, $0 LLM spend, 63 sources, 139 verbatim quotes machine-checked against fetched text)
    for the iteration-3 claim that cross-family solver consensus is a gold-free NL->FOL faithfulness metric. SCOOP RULE (multi-family
    translations + solver equivalence + faithfulness-label meta-eval on NL->FOL): no hit meets all three, so C1 is not scooped.
    Closest neighbours meet two of three each: ARc 2511.09008 (NL->SMT, k LLMs, per-translation confidence = share of k translations
    entailing it, i.e. the same score form as c_score, but a fixed schema and downstream-QA labels); NoTB 2608.21962 (RTL,
    4 families, precision 63/85.3/87/94.7% at >=1..4 families, coverage 100/49/33/27%, spec-level, no AUROC); GenV 2609.11085
    (NL->FOL, single trained verifier, AUROC 0.961 on Z3-reference labels; single-model SC K=5 = 0.863; the judge beats GenV
    0.778 vs 0.679 when labels switch to panel intent). The closest meta-evaluation design is SCP-NL2TL 2608.05439 (NL->temporal
    logic, single-model SC vs judge vs back-translation AUROC by difficulty tier; SC AUROC rises with tier). VERDICTS: C1
    NEEDS-QUALIFIER (the method is not new; claim the first meta-evaluation of cross-family consensus as a per-candidate NL->FOL
    faithfulness score vs an API judge, nested over the baseline stack; win and loss wordings are given); C2 SAFE (cite GenV's
    label-target reversal and wrong-gold rates, 2606.02837 v1 39%/36% vs v2 42.5%/42%); C3 NEEDS-QUALIFIER (predicate alignment
    exists in LogicLLaMA and Vossel; no neighbour reports a rename false-alarm rate); C4 NEEDS-QUALIFIER (balanced-accuracy
    maths; the scatter premise is stated by LLMs-as-Jury, CLOVER and Chen & Avizienis 1978, who noted identical wrong results
    from missing logic; the new piece is a measured identical-wrong vs both-wrong curve over number of conditions, set against
    Eckhardt-Lee's coincident-failure-rises-with-difficulty); C5 NEEDS-QUALIFIER (LLMs-as-Jury already recommend 3-4 cross-family
    models; effective-N results: 7 models ~ 2.58, 9 judges ~ 2). Also supplies: the positioning table on 10 axes; a premise-evidence
    table (60% agree-when-both-wrong on MCQ, rho 0.20-0.59, beta 0.052-0.127, KL 1255 tests); judge-degradation evidence (AutoEval:
    equivalence verification fails beyond toy complexity; >20 operators <50%); cost norms; 8 required extra rows (single-family
    SC, precision@coverage by k, endorsement vs both-wrong by conditions, k-curve per tercile, rename FA per matcher, label-protocol
    sensitivity, n_eff, cite ARc); AuthorYYYY citation strings; and a search log. Files: research_report.md (main), notes/QUOTES.md
    (quote ledger).
  workspace: >-
    /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_research_1
  output_files:
  - research_out.json
  - reproducibility.md
- iteration: 4
  name: gen_art_experiment_9
  type: experiment
  title: Peers given the formula's symbols copy its errors
  summary: >-
    T6-E (iteration 4, DEVELOPMENT set E): Candidate-Signature Consensus (CSC). 3 family-disjoint cheap peers (DeepSeek-V3.2
    / Phi-4 / GPT-4.1-mini / Qwen3-235B) translate the sentence with the dataset-E few-shot prompt plus the candidate's own
    symbol list; c_csc = 1 - share of peers z3-equivalent to the candidate (lowercased name+arity, no aligner); higher = more
    likely ERROR. BUDGET EVENT: the platform refused paid calls (HTTP 403, shared 'Test idea' phase budget exhausted by siblings)
    after 1,033 of ~9,000 planned calls; this artifact spent $0.108. CSC is evaluated on PRIMARY = 354 R_AB rows (196 ERROR/158
    CORRECT) whose 3 peer calls completed (fixed in prereg addendum before scoring); FORMAT-ONLY, PLACEBO, RENAME NOT_RUN;
    L25 NOT_READ. $0 analyses use all 2,686 rows. RESULT (sharp negative, provisional): CSC lowers correct-row divergence
    d (0.139 vs 0.323 for the same free peers scored exactly) but raises error endorsement e (0.459 vs 0.173; MEANING_RENAME-type
    0.82 vs 0.04; ADD 0.49 vs 0.14) = anchoring. Strat AUROC c_csc 0.614 [0.49,0.74] vs FREE-matched exact 0.770, c_score_align
    0.774, flash-lite judge 0.664; paired delta vs FREE exact -0.156 [-0.290,-0.031] (holds on GE2/MINI200 and after removing
    phi-4 exemplar leakage). d still rises with length (GEE slope +1.25 [+0.41,+2.09]); no nesting gain over S4_full (+0.006).
    Gates (csc_gate_E.json, PROVISIONAL): G1 FAIL, G2 FAIL (R_AB; L25 NOT_READ), G3-E NOT_RUN, G4 null, G5 PASS ($5.25e-4/candidate).
    Recommendation for iteration-5 rule: CSC not a fix; fall back to frozen c_score_align + p_peer_text. $0 FULL-population
    facts: matched free peers exact vs ALIGN d 0.583 vs 0.328; 53% of free-exact disagreements with CORRECT candidates are
    structural (only 20% of flagged CORRECT rows fully vocabulary-resolvable); 9-peer c_score_align rename FA 0.595->0.868
    under WordNet-synonym rename. Reproduction checks pass (eval-2 3-pool strat 0.7428 vs 0.7427). Headline CSC/FREE numbers
    independently re-derived (results/audit_rederive.json; permuted-label placebo CI includes 0). Files: method.py (stage
    runner), src/csc.py (library + tests), tables.md, csc_gate_E.json, results/per_item_csc_E.jsonl, results/analysis.json,
    results/llm_cache.jsonl (only copy of 599 paid peer generations), method_out.json (exp_gen_sol_out; predict_* higher=ERROR;
    NA where CSC not generated), deviations.json.
  workspace: >-
    /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_experiment_9
  output_files:
  - method.py
  - full_method_out.json
  - mini_method_out.json
  - preview_method_out.json
  - reproducibility.md
- iteration: 4
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
    is 1.000 and recall given base endorsed is 1.000. On the same 74 long bases, correct-base FA d is 0.149 cued vs 0.757
    uncued FREE3-ALIGN, a paired diff of -0.608 [-0.716, -0.500]. Rename FA is 1.000 under a base-signature cue, which shows
    renames need re-cueing. (2) SIG labelled check, k=3 family-matched: within-template AUROC 0.930 [0.916, 0.943] vs 9-peer
    c_score_sig 0.952 and disguised flash-lite judge 0.587. (3) Same-vocabulary typed repair: ORACLE 0.928 on E (exp 8 oracle
    0.802); SIGPROXY majority 0.784 [0.711, 0.849] on R_COMP; uncued FREE3 majority 0.123 on E (exp 8 baselines: medoid 0.328,
    judge 0.326). (4) Uncued d grows with length on E (c_align 0.47/0.80/0.91 by word tercile). (5) LOCAL2 is a secondary
    arm (qwen2.5-1.5b and gemma-2-2b, same CSC prompt, 27 E bases). Small peers use genuine listed symbols 0.81 and synonyms
    0.70, but foreign, donor and nonce symbols only 0.11-0.16. Using a foreign or donor symbol never reproduced the mutant
    (0/25). Delta-anchor was 0 for ADD_FOREIGN and MEANING_RENAME; power is low (base endorsement 0.30). Independent re-derivation:
    tests/rederive.py makes 429 table checks with 0 mismatches; tests/rederive_headline.py recomputes the AUROC, the paired
    d, typing and the d terciles from raw files with failing placebos. Outputs: method_out.json (PERTURB_E_CSC 3,456, PERTURB_RCOMP_CSC
    1,946, RCOMP_SIG_CSC 2,210; predict_* strings, higher = error; c_csc = NA), results/tables.md, anchoring.csv, controls_fa.csv,
    typing_csc.csv, rcomp_sig_csc.json, local2_anchoring.json, csc_gate_P.json, firewall.json (FREE labels never read), perturb_csc_scores.jsonl.
  workspace: >-
    /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_experiment_10
  output_files:
  - method.py
  - full_method_out.json
  - mini_method_out.json
  - preview_method_out.json
  - reproducibility.md
- iteration: 4
  name: gen_art_dataset_4
  type: dataset
  title: Fresh logic test set, paused by budget
  summary: >-
    E2 (PARTIAL, budget-stopped): the frozen, sealed design of a fresh NL->FOL faithfulness confirmation set disjoint from
    dataset E, labelled by E's byte-identical code (code_freeze.json). The run-level 'Test idea' OpenRouter budget ($7, shared
    by all concurrent artifacts) ran out at 07:26 UTC after this artifact spent $0.24. The proxy refuses paid calls until
    the user raises the budget. WHAT EXISTS: (1) 550 active sentences with gold references, pre-registered and hashed before
    generation (prereg_E2.json): L25 350 (MALLS-v0.1-train, >=25 words, >=3 conditions, 45% in the 30-34-word bin, mean 28.8
    words / 4.65 conditions); EXC 100; DT 100 (ProverQA dev, prover-built gold, 1 per entity skeleton, >=15 words and >=2
    conditions). Also a ranked L25 surplus order (98) and a DT reserve (10). EXC CAVEAT: the core-exception supply is exhausted
    (E took all 67 MALLS-train items; MALLS-test has 3, all excluded), so E2-EXC is 92 'without' + 8 non-XOR 'but not' items,
    core-marker share 0.0. (2) A 30-sentence pilot (12 L25 / 8 EXC / 10 DT): 300 real candidates from E's 10 few-shot slots
    (9 families, temperature 0) + 30 gold-as-system rows, solver-labelled by E's labeller. Without panel votes E's final rule
    gives 36 ERROR (tier A_unaudited_ref), 244 UNRESOLVED, 20 UNPARSEABLE, 0 CORRECT. (3) A partial panel drift check: the
    77 synthetic gate items were replayed with a fresh cache (majority agreement with E's stored votes 0.974; balanced accuracy
    P1 0.861 / P3 0.875 / R1 0.837 vs E 0.861 / 0.85 / 0.863). Track H was cut off, so the stop rule is UNDECIDED. (4) A seal:
    candidates_E2_nolabels.jsonl vs sealed/labels_E2.jsonl + references, sha256 in seal.json, verify_seal.py passes. (5) testability_E2.json:
    NO cell is testable now. Projected MDE80 if completed is 0.112 at L25=350 and 0.099 at 450; the direction's '400 L25 detect
    +0.08' claim is wrong (needs ~690). full_data_out.json groups: e2_candidates (300), e2_gold_as_system (30), e2_sentences
    (550, status PENDING_GENERATION_BUDGET_STOP for 520), e2_panel_drift (173). All source-checked rows verify. RESUME: `bash
    src_e2/run_all.sh` (resumable; projected $6.8, ~2.5 h). DOWNSTREAM: in this state E2 cannot confirm any metric. Iteration
    5 must either wait for the resume or use E2 only as a pipeline/seal smoke test. Deviations D0-D7 are in dataset_card.md.
  workspace: >-
    /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4
  output_files:
  - data.py
  - full_data_out.json
  - preview_data_out.json
  - mini_data_out.json
  - reproducibility.md
- iteration: 4
  name: gen_art_dataset_5
  type: dataset
  title: Name-free labels for free-vocabulary logic translations
  summary: >-
    T7b name-free labels for R_COMP FREE (free-vocabulary NL->FOL rule translations; 221 templated sentences, 10 LLM slots
    / 9 families). full_data_out.json (exp_sel_data_out) has 3 groups: (1) rcomp_free_labels, 2,652 rows (one per FREE generation
    record, row_key = exp-7 recipe), label from an exhaustive, certificate-backed, name-free map search (injective symbol
    maps + B1/B2 reification, B3 merge, B4 split, B5 lexical negation; z3 relevance/polarity prunes, 128-model finite countermodels,
    z3 equivalence; 0 caps, 0 z3 unknown) under a hashed prereg v1.1. IMPORTANT: labels are SEARCH-ONLY (deviation D9: run
    OpenRouter budget exhausted before this artifact's first call, $0 spent): ERROR_CERT 759 (final, exact relative to the
    family), UNRESOLVED_GLOSS_NOT_RUN 1,506 (z3-equivalent under some map, gloss check pending), UNPARSEABLE 188, NO_OUTPUT
    199; no CORRECT class yet -> AUROC NOT_TESTABLE; metadata_label_binary_search_provisional (ERROR_CERT vs MAPPED) is TESTABLE
    (all 759/1,506; untouched 636/1,175) with audited contamination ~13% each side. Metadata: seen_iter3 (454 rows; untouched
    subset 2,198 is primary), map_certificate, gloss_pairs, certificate counts, strata (template, clause_type, word_tercile,
    prompt_variant). Seal sha256 9609ebbb... (all), b364a49a... (untouched). (2) gloss_gate_items: 840 known-answer (symbol
    use, meaning) items, 7 classes x 120, halves A/B; checker verdicts pending. (3) sig_soundness_replay: 4,280 = 2,140 SIG
    rows x {nonce, synonym} renames with known pure-z3 labels: false ERROR_CERT on known-CORRECT 0/1,595, identity map recovery
    100%, known-ERROR rescue by non-identity maps 9-10% (what the gloss check must stop), oracle-checker ceiling recall 1.00
    / false-CORRECT 0.00. Executor (non-blind) audit: ERROR_CERT precision 0.867 [0.76,0.93] (out-of-family faithful forms:
    disjunctive split, one predicate with two constants, exists-for-constant, in-name negation); MAPPED faithful 0.867. Old
    iter-3 tier-A labels: 34/34 CORRECT are MAPPED; 297/420 old ERROR are MAPPED, 17/20 hand-checked are old aligner false
    errors. Reusable functions in src/freelab.py (exhaustive_map_label, equivalent_modulo_vocab_exhaustive, gloss_decision);
    src/resume_gloss.py runs gate -> FREE gloss -> final labels/seal -> SIG e2e -> Sonnet-5 audit (~$1.8) once budget is available.
    See dataset_card.md, deviations.json.
  workspace: >-
    /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5
  output_files:
  - data.py
  - full_data_out.json
  - preview_data_out.json
  - mini_data_out.json
  - reproducibility.md
- iteration: 4
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
    d_floor (R_point_label, an oracle-assisted prediction) 0.402 [0.336, 0.471]; bracket [0.396, 0.415]; exact-only 0.683;
    no-anchoring oracle floor 0.385 (0.345 with a labelled denominator); e_ceiling 0.162. 9-family: 0.537 / 0.532 / 0.522,
    with oracle 0.586. The pre-registered gap_closed rule is ill-conditioned: its denominator is 0.013. Behind d, 77% (9-family)
    / 61% (3-pool) of non-agreeing peers of CORRECT candidates are labelled ERROR, and only 9% of CORRECT-CORRECT disagreements
    are NF/HYB-resolvable. The specificity placebo shows VOCAB agreements are not label-specific (ratio 1.98 [0.43, 11.4]
    3-pool; 0.83 9-family). c_vres does not beat c_score_align on L25 (-0.014 [-0.028, -0.001]), which predicts that G2 fails.
    NET stays DEGRADES under every rule. PART 2 (R_COMP): SIG e 0.000, d 0.2596 (weak 0.143 / strong 0.965), SCATTER ratio
    4.38. Paired same-slot-pair exact agreement is SIG 0.528 vs FREE 0.048, a drop of +0.479 [0.447, 0.513]. Post-hoc ALIGN
    recovers 41% of it, NF 18%, ALIGN∪NF 45%. The out-of-sample validation of the Part-1 method FAILED: predicted 0.20 vs
    actual SIG endorsement 0.575, calibration error -0.37 [-0.42, -0.32]; Spearman across templates 0.97. So the instruments
    under-count vocabulary effects. PART 3 (power_E2.json): yield is L25 0.37, L20 0.53, EXC 0.64, CTRL 0.25. Planned L25
    250/300/350/400 gives MDE80 0.130/0.119/0.110/0.103, all MARGINAL. Detecting +0.069 needs about 882 planned L25 sentences,
    or about 237 usable sentences in the long pool. R_COMP FREE needs at least 200 CORRECT rows. PART 4: 13 record tables
    (a)-(m) read by code with source lines; 64 claims, 60 match, 1 mismatch (the plan's $0.000996/candidate is a unit error:
    the source gives $0.000116 per candidate). The '26.8% of controls' figure holds for non-rename controls only. Audit: 11/11
    independent re-derivations pass, and the placebos behave as expected. Outputs: eval_out.json (157 metrics; 2,672 E rows
    + 4,862 R_COMP rows), tables/*.csv, record.md, power_E2.json, pairwise_classes_RCOMP.jsonl, figures, README.md, reproducibility.md.
  workspace: >-
    /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3
  output_files:
  - eval.py
  - full_eval_out.json
  - mini_eval_out.json
  - preview_eval_out.json
  - reproducibility.md
- iteration: 5
  name: gen_art_experiment_11
  type: experiment
  title: Consensus vs LLM judges on fresh logic data
  summary: >-
    E2-A (iter 5): the pre-registered confirmation of frozen cross-family consensus c_score_align (V0) on the untouched E2
    NL->FOL set. STATUS PARTIAL / NOT_TESTABLE: the run-level OpenRouter 'Test idea' budget ($12, shared) ran out at ~11:40
    UTC after this artifact spent $2.05; key polled to the pre-registered 15:30 cutoff, never recovered. Done: drift gate
    PASS (panel majority agreement 0.955 on 269 items, providers pinned, M2 e2/E2_DRIFT_DECISION.json); all 5,500 candidates
    (550 sentences x 10 slots) generated; solver labels for all; panel labels only for the first sha1-order prefix of 110
    sentences (37 L25/37 EXC/36 DT; random prefix); every label-free score sealed before labels (V0, PT, c_exact, V1-V5, L2,
    L3, user's pilot metrics, local Qwen3-8B judge both views); flash-lite judge on 707 rows only; nano/round trip not run.
    RESULTS on the prefix (R_AB, strat AUROC, sentence-cluster bootstrap B=2000): long pool 94 rows (76 ERR/18 COR) -> (a)
    NOT_TESTABLE, (b) not testable, (c) NOT_TESTABLE in R_COMP sibling. DT (179 rows, prover-built gold): V0 0.916 [0.858,0.970]
    vs local judge 0.913, delta +0.003 [-0.042,+0.052]; ALL (273): V0 0.890, S4 stack 0.931, [S4+V0]-S4 -0.009 [-0.034,+0.014]
    -> consensus ties a local 8B judge and adds nothing over it. User's pilot metrics do NOT track correctness: joint-conflict
    0.500, arity 0.507, shape 0.510, dangling 0.413 (inverted); only 1-rerun-Jaccard 0.713 (a lexical cross-system agreement
    proxy). V0 is not rename-invariant: nonce-renamed correct formulas flagged 100% (n=145, base 0.26), synonym 94% (n=36).
    H-MECH: (i) 0.909 of peers disagreeing with CORRECT candidates are ERROR; (iv) ALIGN lowers false alarms 0.74->0.18 but
    endorses more rename-type errors; (ii) NOT_READ; (iii) CI includes 0. H-IMPROVE: V0 stands (freeze winner NONE); H-RENAME
    NOT CONFIRMED (GG failed dev gate). E2-B union adds no R_AB rows. Headline numbers independently re-derived (audit/rederive.py,
    sklearn from raw files, exact match; shuffled-label placebo 0.497). FILES: per_item_E2A.jsonl (scores+labels; M3 marker
    e2/E2A_FINAL_READY.json with sha256), scores_E2A.jsonl + score_seal.json, e2src/sealed/labels_E2.jsonl, results/*.json,
    tables.md, method_out.json (exp_gen_sol_out, predict_* higher=ERROR), lib/nl2fol_metrics.py (reusable (text,fol,peers)
    metrics with 'measures / does not measure' docstrings), deviations.json (17), README.md. Resume scripts finish the full
    test if the budget is raised.
  workspace: >-
    /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_11
  output_files:
  - method.py
  - full_method_out.json
  - mini_method_out.json
  - preview_method_out.json
  - reproducibility.md
- iteration: 5
  name: gen_art_experiment_12
  type: experiment
  title: Second fresh sample of long logic sentences
  summary: >-
    E2-B (iteration 5, gen_art_experiment_12): a pre-registered second untouched L25 sample (MALLS-train, >=25 words, >=3
    conditions) for confirming frozen cross-family consensus V0 = c_score_align against LLM judges. STATUS: PARTIAL, NOTHING
    CONFIRMATORY. The run-level OpenRouter budget ($12, shared by all concurrent artifacts) was exhausted at 11:39 UTC, after
    this artifact had spent $0.83; every later paid call returned HTTP 403, and probes until 14:41 all failed. WHAT EXISTS:
    (1) 400 sentences drawn by E2's frozen sha1 rule (E2 pool reproduced byte-exactly; 98 surplus + 302 continuation; 93.5%
    25-29 words; 0 collisions with E/E2; reserve 150), with prereg_iter5_E2B.json frozen before generation. (2) 4,000 candidates
    from E2's 10 frozen generator slots (parse rate 0.883). (3) Solver labels for all 400 sentences with E2's byte-identical
    code (78 files hash-verified). The blind panel completed NO batch (the incomplete batch is excluded), so labels are E's
    final rule without votes: 48 CORRECT / 334 ERROR (tier A vs UNAUDITED MALLS gold), 3,151 UNRESOLVED, 467 UNPARSEABLE.
    R_AB has no CORRECT class; R_A_UNAUDITED misses E's testability floor (48 < 50), so B1-B4 and the union U1-U4 are NOT
    TESTABLE; E2-A's M3 never appeared. (4) Label-free scores, sealed before the join under a file-access guard: V0/PT via
    exp-5 code (reproduces stored E values 50/50), V1-V5 (M1 winner NONE), flash-lite disguised on 2,735 rows in batch order;
    nano, flash-lite original, deepseek and the frontier run were refused (frontier 10-row pilot only). EXPLORATORY numbers
    (analysis/tables.md; not a faithfulness test, because CORRECT = z3-equivalent to an unaudited gold): V0 strat AUROC 0.737
    [0.645, 0.827] vs flash-lite disguised 0.496; V0 - flash-lite +0.208 [0.066, 0.363] on 276 paired rows (31 CORRECT); nested
    [S4+V0]-S4 +0.120 [0.013, 0.237]. A label-coupling diagnostic shows about half of this gap is structural: with gold-equivalent
    peers removed, V0 falls to 0.611 and its lead to +0.133 [-0.024, 0.314]. Label-free: cross-family agreement 13.4% of pairs;
    Spearman(V0, flash-lite) 0.296; rename paired flips 0.088 (SYN) / 0.107 (NONCE), reverse flips 0, shuffled-peer placebo
    AUROC 0.50. V0 costs $0 marginal and 0.06 s of z3 per candidate. Every headline number was re-derived independently (analysis/rederive_headline.json);
    the permuted-label and random-score placebos fail as required. Everything is resumable: if budget returns, e2bsrc/src_e2b/run_batches_resume.sh,
    src/judge_resume.sh and src/finalize.sh complete the plan. src/union.py runs later with --e2a <E2-A per-row file>. See
    README.md, deviations.json.
  workspace: >-
    /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_12
  output_files:
  - method.py
  - full_method_out.json
  - mini_method_out.json
  - preview_method_out.json
  - reproducibility.md
- iteration: 5
  name: gen_art_experiment_13
  type: experiment
  title: Free-vocabulary logic labels and metric test
  summary: >-
    R_COMP FREE confirmation attempt of criterion (c) (iter 5, gen_art_experiment_13). Scores were sealed before any gloss
    call (results/score_seal_rcomp.json; prereg_rcomp_confirm.json git-committed 11:18:46Z). The dataset-5 labeller was resumed
    once: the gloss gate FAILED twice (gloss_v1 half A: Haiku BA 0.776, Qwen 0.855; the one revision gloss_v2 on held-out
    half B: Haiku 0.561 [0.861 on verdicted items, 141 NO_VERDICT], Qwen 0.883; neither checker passes alone), so FALLBACK
    B applies: all 1,506 MAPPED rows are UNRESOLVED_GLOSS_GATE_FAILED, 0 CORRECT, and criterion (c) = NOT_TESTABLE (final
    label seal b7916aea.../untouched 79eb623a...). PROVISIONAL, NON-CONFIRMATORY (ERROR_CERT vs MAPPED, untouched, templated
    text): within-template AUROC c_score_align 0.801 vs flash-lite judge disguised 0.584 (delta +0.217 [0.175,0.260], n=1706)
    and original 0.804 vs 0.633 (delta +0.171 [0.135,0.206], n=1709; orig view completed label-blind pre-seal, D16); positive
    in every sensitivity (s1a,s1b,s3,s5,s7,s9,s10) and 8/9 templates; nested [judge+c]-[judge] +0.23/+0.20, [c+judge]-[c]
    +0.02. Blind two-family audit (Sonnet-5 + GLM-4.6, 100+100 rows, kappa 0.62): ERROR_CERT precision 0.84/0.72, MAPPED faithful
    0.72/0.90 (consensus 0.84/0.92); on auditor-consensus labels (n=146) c_align 0.899 vs judge_disg 0.522 (+0.377 [0.256,0.502]),
    vs judge_orig +0.105 [0.011,0.215]. Noise correction assuming non-differential contamination is INVALID (corrected AUROCs
    >1: contamination is differential). Frontier judge gemini-3.1-pro (150 rows, orig): AUROC 0.852 vs c_align 0.801 (delta
    -0.051 [-0.153,0.044]); [c+frontier]-[c] +0.086 [0.003,0.166]. Orig-view advantage shrinks with length (W1 +0.285 -> W3
    +0.084). H-MECH (i) bar failed (non-agreeing peers of MAPPED are mostly MAPPED: ERROR share 0.30 exact/0.41 align); SCATTER
    ratio ~5.8; ALIGN lowers d by 0.24 vs exact. V1-V5 (M1-frozen, identical code) do not beat V0. Placebo: 17/20 shuffles
    cover 0 (bar 18; post-hoc 100-shuffle supplement 95/100); headline, audit-view and frontier deltas independently re-derived
    from raw files to 1e-9 (tests/rederive_raw.py), permuted-label test fails as it should. Spend $1.97 of $4 cap; run-level
    budget then exhausted (D25). Files: results/confirm_verdict_rcomp.json, analysis_rcomp.json, tables.md, per_item_rcomp_free.jsonl,
    audit_report.json, gate_diagnostics.json, deviations.json (D1-D26), method_out.json.
  workspace: >-
    /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_13
  output_files:
  - method.py
  - full_method_out.json
  - mini_method_out.json
  - preview_method_out.json
  - reproducibility.md
- iteration: 5
  name: gen_art_experiment_14
  type: experiment
  title: Screening fixes for model-agreement false alarms
  summary: >-
    Iteration-5 FREEZE on dataset E (DEVELOPMENT data; nothing here confirms). PART A ($0): five label-free rescorings of
    frozen V0 = c_score_align, computed only from eval-2's pairwise eqmv matrix, sealed (sha256) before any label join. V1
    plurality-normalised, V2 reliability-weighted (out-of-fold family weights), V3 = V1+V2, V4 cross-fitted exact/align logistic,
    V5 = V3 on the 3-pool. Gates reproduce exactly: G0 V0 strat 0.7415 and Δ +0.099 [0.049, 0.146]; G1 24/8,469 = 0.28% (the
    6-decimal rounding of the frozen column is handled at 1e-6, D1); c_exact 0.748; 3-pool 0.7845; eval-3 oracle 0.385 / 0.542.
    Z = 2,672 rows. LONG-strat AUROC: V0 0.743; Δ V1 -0.004, V2 +0.0075 [0.004, 0.011], V3 +0.007, V4 +0.009 [-0.004, 0.021],
    V5 +0.003. The pre-registered rule (Δ LONG >= +0.015, L25 >= V0, CTRL >= V0 - 0.01) gives 'NONE: V0 stands'. Stability:
    NONE 87.6%, V4 11.8%. Null: some variant qualifies in 3.5% of permutations. Mechanism: plurality normalisation trades
    d for e (ALL d 0.490 -> 0.174, e 0.140 -> 0.343; MEANING_RENAME-type e 0.502 -> 0.872). No variant lowers d without raising
    e. The 9-family oracle gap is ILL_CONDITIONED (d_oracle 0.586 > d_V0 0.490). Marker M1 freeze/CONSENSUS_FREEZE_READY.json
    was written 12 min after the first code, with freeze/selection.json and consensus_variants.py (20-row reproduction to
    1e-9). PART B ($0.22): GG = exact z3 equivalence OR an exhaustive injective arity-consistent symbol map giving z3 equivalence
    AND gemini-2.5-flash (non-thinking) says YES for every renamed pair. Checker gate G-A: dev v1 0.780 fails; the one allowed
    revision v2 scores 0.907 on the confirm half. G-B (R_COMP renames): 0.950 / 0.941, NOT_TESTABLE as a gate with only 53
    YES pairs (D2). Dev gates: g1 SYN paired flip 0.034 and g2 MEANING_RENAME recall 1.0 both pass, trivially because base
    FA is 0.83. g3 FAILS: E ALL-strat 0.696 vs V0 0.742, Δ -0.046 [-0.071, -0.021], so GG = FAIL(g3) and the boundary statement
    is written. GG halves error endorsement (e 0.140 -> 0.081; MEANING_RENAME-type 0.502 -> 0.224) but raises d (0.490 ->
    0.629): all 678 granularity (gran) pairs fail the bijection prefilter and 268 align pairs are gloss-rejected. Cost per
    candidate: 0.038 CPU-s + <= $0.00005. Secondary GG_B (freelab B1-B5 bridges) searched 11,202 pairs; its gloss is UNTESTED(budget)
    because the run-level OpenRouter budget was exhausted (HTTP 403, D13). Its all-accepted bracket is worse (ALL-strat 0.653;
    e 0.334): the bridges absorb ADD/DROP errors. PART C: lib/api.py over byte-identically vendored code (lib/PROVENANCE.json
    sha256), with modes align/exact/nf/hyb/pn/rw/gg, graded_consensus, pairwise_matrix/ed_decomposition, peer_text_score,
    eqmv(+exhaustive), minimal_typed_repair, freelab labelling tools and FOL-Triage layers. smoke_lib.py passes on 10 E rows.
    Checks: 14 pytest tests pass; tests/audit_rederive.py re-derives the decision, the Δ (1e-9) and the GG gates; the shuffled-label
    placebo gives ~0.48-0.49. Outputs: method_out.json (exp_gen_sol_out: E_heldout 8,507 rows with predict_V0..V5, c_exact,
    gg, gg_allyes, gg_b_allyes; PERTURB_E_bases 722; GG_checker_gates 1,069), tables.md, screen_E.json, gg_dev.json, ggb_dev.json,
    deviations.json (D1-D13), cost_ledger.jsonl.
  workspace: >-
    /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_14
  output_files:
  - method.py
  - full_method_out.json
  - mini_method_out.json
  - preview_method_out.json
  - reproducibility.md
- iteration: 5
  name: gen_art_evaluation_4
  type: evaluation
  title: 'Corrected record: every paper number checked'
  summary: >-
    CPU-only, $0, no-LLM corrected record for the iteration-4 paper (review score 3, blocking, 11 critiques). KEY FILES: record_final.md
    = paste-ready §0 summary + 17 sections with '~~original~~ [Correction, iter 4: ...; source <abs path>] (paper_draft.md
    Lnnn)' markers (43 markers, 42 originals found) covering §3.3-§3.7, §4.1-§4.7, 'What we have learned'; every number carries
    <!-- n:id --> tracing to numbers.csv (554 rows: 244 claims from hypothesis §0.2-0.3 + review, all 244 MATCH their source
    files; 258 transcribed cells; 52 computed). Paper-vs-file: 15 MISMATCH (all six §4.2 CIs narrower than source, e.g. c_csc
    [0.545,0.679] vs file [0.493,0.736]; COMPOUND 0.643/0.246 vs 0.282/0.107; G2 FAIL vs NOT_READ; M3 CI; §3.6 spend 1.58
    vs $4.33; §3.5 k-cost column per-candidate mislabelled; frontier 6.07x vs 30.2x per item). 8 lints pass (held-out E, recall
    w/o base FA, FA w/o flip, 0.683-as-AUROC, verbatim CIs, cost units, marker paths, untraced numbers). claims_ledger.csv:
    45 claims tagged DEV 23 / CONFIRM-PENDING 7 / DESCRIPTIVE 11 / OUT-OF-SCOPE-SIG 2 / GOLD-USING-ORACLE 2, each naming the
    iter-5 sibling file::field that confirms it. reviewer_checklist.csv: 9 CLOSED, 2 PARTIAL (critique 7 scope needs iter-5
    data; 8 spend partly unaccounted). Spend (ledgers, deduped across 59 files): iter-4 artifacts $0.349; iter-3 records in
    the same window $4.338; $2.313 of the $7.00 phase budget unaccounted (no ledger records it). Independent audit (audit/rederive.py,
    separate code path from raw per-item files): 17/17 pass incl. c_csc 0.614, FREE_exact 0.770, c_score_align 0.774, e 0.459/0.173,
    d 0.139/0.323, base FA 0.712/0.803/0.986/0.757, E2 36/274/20/0, R_COMP FREE 759/1506/188/199, 77%/61% wrong-peer shares,
    iter-4 spend; shuffled-label placebo AUROC 0.458 (CI covers 0.5); exp-9 strat AUROC is PAIR-weighted (n-weighted gives
    0.598). Checker mutation 10/10 caught. skeleton_iter5.md: §5.1 reasoning + §5.2-5.10 shells {{file::json.path}} with skeleton_resolution.json
    (found freeze/selection 'NONE: V0 stands', drift decision PASS; confirm_verdict files absent at run time; re-run eval.py
    at paper time). Figures F1 dev forest, F2 d-for-e trade, F3 wrong-peer decomposition, F4 k-curve with $/sentence axis
    (pdf/png/json). tables/placeholder_ids.csv: 4 placeholder IDs resolved with sed lines.
  workspace: >-
    /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_evaluation_4
  output_files:
  - eval.py
  - full_eval_out.json
  - mini_eval_out.json
  - preview_eval_out.json
  - reproducibility.md
</artifact_data>

<available_figures>
Each line gives the path the page must use, then the figure's title and caption.

- figures/fig_headline_v0.png [render from fig_headline_v0.pdf first] — "Headline result on shared-vocabulary long sentences" (caption: "Cross-family consensus against LLM judges on templated long sentences under a shared symbol vocabulary (R\_COMP-SIG). Each row shows a metric's AUROC for separating erroneous from correct candidate formalisations (dot) with its 95\% sentence-clustered bootstrap CI (bar); consensus is in blue and the judges in grey; the dotted line marks chance (0.5). (a) Pre-registered primary test (1,904 candidates from 220 sentences; 395 erroneous, 1,509 correct; within-template AUROC): consensus reaches 0.954 [0.939, 0.968] against 0.587 [0.551, 0.622] for the disguised cheap judge (dashed line), a confirmed advantage of $\Delta = +0.367$ [0.328, 0.404]. (b) Descriptive frontier-judge subsample (60 candidates, 30 erroneous and 30 correct; pooled AUROC): consensus (0.956) is level with a frontier judge that sees the original text (0.932) and above the same judge on disguised text (0.735), while the disguised cheap judge is at chance (0.499; $n = 56$ with a judge score). Panel (b) is a different and much smaller population than panel (a), so its values are not directly comparable with those in (a).")
- figures/fig_devset_v0.png [render from fig_devset_v0.pdf first] — "Development-set evaluation on Dataset E" (caption: "Stratified AUROC of cross-family consensus and PEER+TEXT fusion (blue) versus five baselines (grey) on the development evaluation set (Dataset E, tiers A+B, 2,686 candidates: 1,822 ERROR / 864 CORRECT, 292 sentences). Dots mark each metric's within-stratum AUROC (value printed at right) and horizontal bars show 95\% sentence-clustered percentile bootstrap CIs ($B=2{,}000$). The dashed grey line marks the disguised cheap judge (0.642). Baseline stack (S4) is the cross-fitted stack of all baselines; the disguised and original cheap judges are the same flash-lite judge with and without nonce-disguised symbols; ``nano'' is the gpt-4.1-nano P(YES) judge. Consensus exceeds the disguised cheap judge by +0.099 [0.049, 0.146] on this development set, but is statistically indistinguishable from the S4 stack of all baselines (0.741 vs.\ 0.735).")
- figures/fig_perturb_v0.png [render from fig_perturb_v0.pdf first] — "Perturbation sensitivity across metrics" (caption: "Within-base AUROC of 16 gold-free metrics on the typed perturbation suite. Each bar ranks a base formula's typed error mutants against that base's own meaning-preserving controls (contrapositive, reordering, De~Morgan, unmutated base), and averages over bases. The scored subset is the 198 development-set (E) bases on which every metric is defined: 2{,}658 mutants vs.\ 563 controls, out of the full suite of 4{,}234 mutants and 868 controls from 300 bases. No row was unparseable. Bars start at chance (dashed line, 0.5), so bar length is the gain over chance. Whiskers are 95\% base-clustered bootstrap CIs, and the number beside each bar is the point estimate. Dark blue: proposed metrics. Light blue: a single layer or variant of a proposed metric. Grey: baselines. PEER+TEXT fusion ranks highest (0.948 [0.934, 0.961]), ahead of consensus (0.866) and text checks (0.845). The best baselines are the S4 stack (0.753) and round-trip NLI (0.749). LLM judges and self-consistency score 0.64--0.68. Three of the four structural pilot metrics are at chance (0.500--0.502), and joint conflict is just above it (0.539). These are synthetic perturbations, not real translation errors. Consensus scores 1 on 98.9\% of mutants, so its bar mainly reflects how often peers endorse the unmutated base.")
- figures/fig_kcurve_v0.png [render from fig_kcurve_v0.pdf first] — "Consensus AUROC vs number of peer families" (caption: "Pooled AUROC of cross-family solver consensus (ERROR vs.\ CORRECT) as a function of the number of peer families $k$ on development set E. The data are the 2,014 candidates (1,309 errors, 705 correct; 186 sentences) for which all seven other LLM vendor families are available. At each $k$, 50 random $k$-family subsets are drawn per candidate, and markers show the mean AUROC over the draws. Blue circles: all candidates; the shaded band spans the 2.5th--97.5th percentile across draws (zero width at $k=7$, where only one subset exists). Orange squares: the longest third of sentences ($>26$ words), mean over draws. The dashed line marks the all-candidate 7-family pool (0.784). For all candidates, performance saturates quickly: $k=3$ reaches 0.757, 97\% of the 7-family value. Long sentences saturate later and stay below the all-candidate curve at every $k$: they need $k=5$ to reach 96\% of their own 7-family value (0.698 vs.\ 0.726). The band reflects only which families are drawn. The sentence-bootstrap 95\% CI of each mean is wider, about $\pm 0.04$ at every $k$.")
</available_figures>

<data_requirements>
- Embed each dataset the views use as its own
  `<script type="application/json" id="data-..." data-source="...">` element, where
  `data-source` names the artifact and the output file it came from (for example
  `experiment_1/method_out.json`), never an absolute path. The inline script reads each one with
  `JSON.parse(document.getElementById(id).textContent)` and builds every chart, table, count and
  control from it; no number a view shows is typed into the markup by hand.
- Produce the embedded JSON with a script that reads the output files, not by copying values, so
  it is exactly what the files hold. Keep only the fields the views use.
- When a file is too large to embed whole, embed a subset chosen by a rule the page states (for
  example every failure plus a seeded random sample of the rest) and the aggregates computed from
  the full file.
- The numbers the prose states match the paper. A view may compute from the embedded data (a
  mean, a filter, a threshold swept over recorded scores), and says so; it never invents,
  interpolates, simulates or smooths a data point.
- Every number the paper states (a headline rate, a confidence interval, a table cell, a p-value)
  appears on the page exactly as the paper states it, at the paper's precision. Embed it from the
  artifact output file that holds it and print that value; never re-derive it in the browser. A
  bootstrap re-run in the page draws different resamples, and a mean recomputed from rounded or
  subsampled rows rounds differently, so a CI of [0.38, 0.68] turns into [0.37, 0.68] and a
  0.364 into 0.363. Where a live view recomputes a quantity the paper states (a threshold sweep,
  a filter over the items), the setting that matches the paper must show the paper's value: take
  that row from the file, or check the live result against it before shipping.
</data_requirements>

<figure_requirements>
- The page draws its own charts from the embedded data; the paper's figures are not its visuals.
  Show at most 3 of them, and only where a figure shows what the data cannot
  (the method diagram, an example rendering), never a data plot the page can draw live.
- Reference a figure as `figures/` plus its filename, exactly as listed above. The
  page and the figures folder are published together, so that relative path resolves on the live
  site and anything else breaks.
- A browser cannot draw a PDF in an image element. For a figure listed as "render from ...
  first", use the PNG of that name in `figures/` when it is already there, and
  otherwise render one there at about 200 DPI with pdftoppm or pymupdf. Renderable formats:
  .avif, .gif, .jpeg, .jpg, .png, .svg, .webp.
- Use the figure's own caption, and look at the figure before placing it.
</figure_requirements>

<page_structure>
Top to bottom:

1. HEADER: the title, the author line as the paper gives it, and the paper link as the primary
   button, labelled "Read the paper (PDF)". The other links from the links section sit beside it.
2. THE FINDING: the question and the answer in plain language, with the single number that
   carries it, and beside them the headline view, operable at once: the result drawn from the
   embedded data, the baseline shown with it, and a control over the conditions it was measured
   under.
3. HOW IT WORKS: a stepper that walks ONE real example from the data through the method's
   stages, showing at each stage what goes in, what is done to it, what comes out (the recorded
   values where the run kept them) and why. A pipeline diagram in inline SVG highlights the
   current stage; previous and next buttons, clickable stage markers and the left and right arrow
   keys move between stages.
4. EXPLORE THE EVIDENCE: two or more views over the real data, chosen from the kinds in the
   design philosophy to fit this result. At least one is an item browser: filter, search or sort
   over the real per-item records, and a detail panel that puts the selected item's input, the
   method's output and the baseline's output (or its before and after) side by side.
5. TRY IT: the live mini-demo when the method runs exactly in the page; otherwise a what-if view
   that sweeps a threshold or parameter over the recorded scores and recomputes the metrics live.
   Leave it out only when neither would be honest for this result, and say why in your summary.
6. WHERE IT FAILS: the failure cases from the data one control away, then what the paper says it
   does not show.
7. FOOTER: every link from the links section again, a data provenance list naming the artifact
   file behind each view, the glossary of every term with a tooltip, and the citation if the
   paper carries one.

A compact section navigation marks where the reader currently is. Each view opens with the
question it answers and ends with a takeaway sentence that updates with the selection.
</page_structure>

<interaction_requirements>
- Controls are real form controls or ARIA widgets: a range input with its current value printed
  beside it, a select, checkboxes, a radio group or tab list, buttons with aria-pressed. Each one
  changes a view without a page jump, and the view's counts and takeaway sentence change with it.
- Charts are inline SVG you generate, or canvas when there are thousands of marks: labelled axes
  with units, bars that start at zero, the baseline always shown, a legend when there is more than
  one series, and values printed at the precision the source has. Every mark shows its record on
  hover, on keyboard focus and on tap.
- Tooltips: each term trigger is a button with the term as its text, showing its definition on
  hover, on keyboard focus and on tap, dismissed by Escape and by tapping elsewhere, and exposed to
  assistive technology through aria-describedby. Define each term from the paper's own wording.
  A mouse click fires hover, focus and click in turn, and a tap fires focus and click, so a click
  handler that toggles closes the definition the moment it opened: every one of those events
  OPENS the tooltip, and only Escape, a click or tap elsewhere, or leaving the trigger closes it.
- Stepper: the current stage is announced through an aria-live region, the buttons disable at
  the ends, and the current stage marker carries aria-current.
- The page works with no network at all and logs no error or warning to the browser console.
</interaction_requirements>

<technical_requirements>
- ONE file: all CSS in a style element and all JavaScript in a script element, both inline in
  `interactive.html`, beside the data elements. No framework, no external script,
  stylesheet, web font or analytics. The only files the page may point at are the figures listed
  above.
- A complete HTML document: the file opens with exactly this markup, then the title and the
  style element, and closes head before the body. Without the viewport tag a phone lays the page
  out 980px wide and shrinks it to tiny text.
```html
<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
```
- Chart text never collides: in every chart, axis titles, tick labels, value labels and legend
  entries each keep their own space at every width. A rotated y-axis title sits left of the
  widest tick label with a gap: size the left margin from the measured label widths (getBBox or
  getComputedTextLength), not from a fixed guess.
- Plain modern JavaScript, no build step.
- Formulas use HTML sub and sup elements or inline MathML. TeX notation such as `^`, `_` or
  `\frac` must not reach the page.
- System font stack only. Light theme.
- Responsive from a 360px phone to a wide desktop with no horizontal page scroll; wide tables and
  charts scroll inside their own container or reflow, and charts redraw to their container width.
- Honour prefers-reduced-motion.
- Keyboard-navigable in a sensible Tab order with a visible focus ring and a skip link to the
  main content.
- Semantic HTML: one top-level heading, headings that descend without skipping, landmark
  elements, and alt text on every image that says what it shows.
- Keep the whole file under 3 MB.
</technical_requirements>

<page_gate>
When you finish, the page is loaded in a headless browser and sent back to you if its script
throws an error; if it has no `application/json` data element that its inline script reads by
id; if it shows more than 3 static images; or if, once its script has run, it
draws fewer than 2 charts (svg or canvas) or offers fewer than 3
controls; if it does not open with the document head above; or if, at 1280px wide, the
text boxes of two labels in one chart overlap (an axis title over a tick label, two legend
entries). It is also sent back if `index.html` is present and does not link to
`interactive.html`.
</page_gate>

<writing_register>
Write in the register of the field's best papers (the paper this page teaches, which was written to them), not in the register of a language
model. Four things are measured on the finished draft, and a draft outside them is sent back with
the numbers:
- Never use: delve, underscore, showcase, intricate, pivotal, realm, commendable, meticulous, tapestry, garner, multifaceted, it is worth noting, plays a crucial role, not only ... but also. These are 10 to 30 times more frequent in machine-written abstracts than in
  human ones, and reviewers read them as such.
- Em dashes: at most 3 per 1,000 words. Use a comma, a colon or a full stop.
- Sentence rhythm: mix short and long sentences. An interquartile range of sentence length under
  8 words reads as machine-written.
- Hedging: at most 15 hedges (may, likely, suggests, appears) per 1,000
  words. State what the evidence supports plainly; hedge where it is thin, not everywhere.
Style never changes substance: numbers, claims, citations and figure markers stay exactly as the
evidence gives them. The user's original request (delivered as a separate message) overrides all
of this wherever the two conflict.
</writing_register>

<links>
Use these URLs VERBATIM. Do not shorten them, do not make any of them relative, and do not
compose one of your own.

- The paper PDF: https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic@fork/run_An1uy2kF2SjZ/paper.pdf
  Label it "Read the paper (PDF)"; it is the page's primary call to action.
- The code repository: https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_An1uy2kF2SjZ
- The full research report, every experiment and every table: https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic@fork/run_An1uy2kF2SjZ/report.pdf
  Label it "Read the full research report" and place it beside the paper link.

Each carries the branch this run publishes to, and they begin resolving only after this run
finishes publishing, so do NOT try to open or verify them.
</links>

<presentation_link>
When `index.html` is present, it is what a reader lands on, so your page is found only
if it links there. In `index.html`, add a link whose href is exactly
`interactive.html`, labelled "Explore the interactive demo", beside the paper link in the
hero and again beside it in the footer, styled like the links next to it; a link to it that
already reads differently gets relabelled. This one link is relative, unlike the URLs above,
because both pages are published into the same folder. Change nothing else in
`index.html`.
</presentation_link>

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.

<todos>
TODO 1. Read `paper.tex` end to end and list `figures/`. Write down
the title, the author line, the question and the finding, the method's stages in order, every
technical term with the sentence that defines it, every headline number with the sentence it
appears in, and the limitations.
TODO 2. Open the output files in <artifact_data>, the `mini_` or `preview_` variant first. Write
down which files hold per-item records (inputs, outputs, scores, verdicts), which hold
per-condition, per-model or per-setting results, which hold the values a method stage recorded,
their fields, and how many rows each has. Note the ones that carry the paper's headline
numbers.
TODO 3. Design the page before writing it. For each view in the page_structure, write down the
reader's question, the file and fields it draws, the control, the chart, and the takeaway
sentence. Pick the views that make the finding VISIBLE (the gap between method and baseline, the
cases where it fails, the one example that shows the mechanism), not ones that restate a number
the prose already gives.
TODO 4. Write a script that reads those output files and writes the JSON each view embeds, then
check that every headline number it produces matches the paper.
TODO 5. Render the PNGs of the figures you will show (at most 3) into
`figures/`, then LOOK at each one.
TODO 6. Write `interactive.html` following the data_requirements, page_structure,
interaction_requirements and technical_requirements sections above.
TODO 7. VERIFY THE NUMBERS: every number in the prose appears in `paper.tex` with the
same meaning, and every embedded value traces to the output file its data-source names. Then
read the numbers the page shows once its script ran (intervals, table cells, the default setting
of every live view) and confirm each one the paper also states is digit-for-digit the paper's.
Delete or fix anything you cannot trace.
TODO 8. VERIFY THE PAGE: confirm it has no external script, stylesheet or font reference; that
every image path starts with `figures/` and names a file in `figures/`;
and that the paper, repository and report links are character-for-character the URLs in the
links section.
TODO 9. LINK YOUR PAGE from `index.html` when it is present, as the presentation_link
section says, then open `index.html` and confirm the link is in its hero and its footer
and that nothing else on that page changed.
TODO 10. OPERATE THE PAGE in a headless browser. `chromium-headless-shell` is already installed,
the same browser the finished page is checked in: drive it with Playwright (`uv pip install
playwright` in a scratch virtual environment, then launch Chromium with `executable_path` set
to the output of `which chromium-headless-shell`, with no `playwright install`). Only if that
command finds nothing, run `playwright install --with-deps chromium` instead. Open the page at
390px and 1440px wide, operate every control, hover and tap chart marks, step the stepper, select
items in the browser, click a term and confirm its definition is STILL showing after the click,
and confirm each view and its takeaway sentence change as they should. Use real clicks (the
browser's click, not a dispatched event), since that is what a reader's mouse and finger
produce. Screenshot each state, read the screenshots, and confirm the console shows no errors
and the page never scrolls sideways. Fix anything broken, cramped, overlapping, empty or cut
off, then operate it again.
</todos>

---

Output the result as JSON to: `./.terminal_claude_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "InteractivePaperExpectedFiles": {
      "description": "All expected output files from interactive-page generation.",
      "properties": {
        "page_html_path": {
          "description": "Path to the single self-contained HTML page. Example: 'interactive.html'",
          "title": "Page Html Path",
          "type": "string"
        }
      },
      "required": [
        "page_html_path"
      ],
      "title": "InteractivePaperExpectedFiles",
      "type": "object"
    }
  },
  "description": "Interactive paper page: structured output from gen_html_demo.",
  "properties": {
    "summary": {
      "description": "Brief summary of the page you built: each view and control, the question it answers, and the artifact output file its data came from.",
      "maxLength": 5000,
      "minLength": 300,
      "title": "Summary",
      "type": "string"
    },
    "out_expected_files": {
      "$ref": "#/$defs/InteractivePaperExpectedFiles",
      "description": "All output files you created. Must include interactive.html."
    }
  },
  "required": [
    "summary",
    "out_expected_files"
  ],
  "title": "InteractivePaper",
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

### [2] SYSTEM-USER prompt · 2026-09-25 18:59:56 UTC

```
[Image: original 1440x9858, displayed at 292x2000. Multiply coordinates by 4.93 to map to original image.]
```
