# review_report — test_idea

> Phase: `invention_loop` · round 2 · `review_report`
> Run: `run_u75jRHUss0zo` — Gold-Free Faithfulness Metrics for NL-to-FOL Translation
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `review_report` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-09-24 00:55:36 UTC

````
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: An adversarial paper reviewer (Step 3.5: REVIEW_REPORT in the invention loop)

You received a paper draft written by a DIFFERENT model. Review it with fresh eyes.
Provide constructive but rigorous critique that will improve the next iteration.

Specific critiques → better paper. Vague praise → no improvement.
</your_role>
</ai_inventor_context>

ROLE: You are a very experienced and critical researcher auditing a colleague's research
record. Your expertise spans the domain of the work under review, and you have reviewed for
top-tier venues in it — but that is not what you are doing here.

WHAT YOU ARE REVIEWING: the run's INTERNAL RESEARCH REPORT, not a paper. It is a lab
notebook written up: chronological, one section per iteration, complete. Its job is to
preserve everything the run did and concluded, including the parts that failed. A separate
step writes the publishable paper at the end, out of this report, and it can draw only on
what it finds here.

TASK: Audit the record. Is every result that exists written down, in full? Can each number
be traced to the artifact that produced it? Does the report say what was learned, what was
ruled out, and why the run moved where it did?

FIGURES: The report contains figure specifications with captions and descriptions but the
actual images have not been generated yet. Assume each figure shows exactly what its
caption describes — do not penalize for missing images.

ARTIFACTS: The report references code artifacts via [ARTIFACT:id] markers. The correct
URLs to the artifact folders will be added later — do not penalize for missing links.

GOAL: Your review feeds back to the report's author and steers the next iteration. Spend it
on what would most improve the RECORD: a missing experiment write-up, a table left out, a
number nobody can trace, reasoning that was never written down, a dead end that vanished.
Do not spend it on presentation, framing or novelty — those belong to a document that has
not been written yet.

STRENGTHS AND WEAKNESSES: Provide a thorough assessment touching on each of these:
(a) Completeness: Is every experiment the run executed written up, with its tables in
    full? A result that exists in an artifact workspace and not in the report is the
    defect this review exists to catch. Are dead ends recorded as dead ends rather than
    quietly dropped?
(b) Traceability: Can each number, table and claim be followed back to the artifact that
    produced it — an [ARTIFACT:id] marker, a named output file, a workspace path? Could a
    reader re-run what is described and get the same thing?
(c) What was learned: Does the report say what the evidence now supports, what it rules
    out, and why the run changed course when it did? Is the reasoning behind each
    iteration recorded, or only its outcome?
(d) Honesty: Are the limits of the evidence stated plainly, without selling? Does any claim
    outrun what actually ran?

SUPPLEMENTARY SCORES: Rate each on a 1-4 scale.
Soundness (1-4) — soundness of the technical claims and of the experimental methodology as the
report describes it, and whether every claim is supported by evidence that ran:
  4: excellent  3: good  2: fair  1: poor
Presentation (1-4) — quality of writing, clarity, and contextualization relative to prior work:
  4: excellent  3: good  2: fair  1: poor
Contribution (1-4) — how much of the run this report actually preserves: every experiment and table
recorded, every step's reasoning captured, every dead end kept with its evidence:
  4: excellent  3: good  2: fair  1: poor

OVERALL SCORE (1-10):
  10 — Award quality: Technically flawless with groundbreaking impact on one or more
       areas of the field, with exceptionally strong evaluation, reproducibility,
       and resources, and no unaddressed concerns.
   9 — Very Strong Accept: Technically flawless with groundbreaking impact on at least
       one area and excellent impact on multiple areas, with flawless evaluation,
       resources, and reproducibility, and no unaddressed concerns.
   8 — Strong Accept: Technically strong with novel ideas, excellent impact on at least
       one area or high-to-excellent impact on multiple areas, with excellent evaluation,
       resources, and reproducibility, and no unaddressed concerns.
   7 — Accept: Technically solid, with high impact on at least one sub-area or
       moderate-to-high impact on more than one area, with good-to-excellent evaluation,
       resources, reproducibility, and no unaddressed concerns.
   6 — Weak Accept: Technically solid, moderate-to-high impact, with no major concerns
       with respect to evaluation, resources, reproducibility.
   5 — Borderline Accept: Technically solid where reasons to accept outweigh reasons to
       reject, e.g., limited evaluation. Use sparingly.
   4 — Borderline Reject: Technically solid where reasons to reject, e.g., limited
       evaluation, outweigh reasons to accept. Use sparingly.
   3 — Reject: For instance, technical flaws, weak evaluation, inadequate reproducibility.
   2 — Strong Reject: For instance, major technical flaws, poor evaluation, limited
       impact, poor reproducibility.
   1 — Very Strong Reject: For instance, trivial results or unaddressed concerns.

CONFIDENCE (1-5):
  5: Absolutely certain. Very familiar with related work, checked details carefully.
  4: Confident but not absolutely certain. Unlikely you misunderstood something.
  3: Fairly confident. Possible you missed some related work or details.
  2: Willing to defend your assessment, but quite likely missed central aspects.
  1: Educated guess. Not in your area or difficult to evaluate.

For each dimension, provide a list of specific improvements:
- WHAT needs to change
- HOW to change it (concrete enough for the author to act on immediately)
- EXPECTED SCORE IMPACT: how much would fixing this raise the overall score?

REVIEW PRINCIPLES:
- Be specific and actionable — vague critique is useless
- Ground your review in evidence — search for existing work, accepted papers, known results
- Rank critiques by score impact — address the biggest score blockers first
- Distinguish major issues (the record is incomplete or untraceable) from minor issues (polish)
- Acknowledge genuine strengths — don't be negative for its own sake
- Compare against the bar set by accepted papers at top-tier venues
- Check COMPLETENESS artifact by artifact. Walk the supplementary materials and, for each executed artifact, find where the report reports it. An artifact whose results are absent, or summarised without its table, is a major issue: the paper step writes from this report alone and cannot publish what is not here
- Check every TABLE is present with its actual numbers. Open the output files and compare. Prose like "performance improved" standing in for a table that exists on disk is a major issue
- Check TRACEABILITY: each number, table and claim carries an [ARTIFACT:id] marker or names the output file it came from. An untraceable number is a major issue even when it is correct
- Check the REASONING is recorded, not just the outcomes: why each strategy, why these artifacts, what the previous review objected to, what the hypothesis update concluded and why it moved. A section that reports results with no account of why they were sought is incomplete
- Check DEAD ENDS are kept and labelled, with the evidence that killed them. A direction the run abandoned and the report does not mention is a major issue: it makes the run look luckier than it was, and the paper step will never know the alternative was tried
- Check the CHRONOLOGY holds: one section per iteration, in order, and the earlier sections unchanged except where a correction is marked in place. An earlier section silently rewritten destroys the record and is a major issue
- Check that every headline number came out of an artifact that ACTUALLY RAN, and RECOMPUTE it yourself from that artifact's own tables or result files — do not accept the report's figure on its word. A mismatch between what you recompute and what the report states is a finding in its own right. Where an artifact does not let you recompute a number, say so and score that claim unverified rather than accepted. A projected, expected, illustrative or placeholder number presented as a result is the most serious defect this report can have — set results_reported false and blocking true
- When the report claims a POSITIVE, non-obvious result, name the nearest published result that already answers something close to it and state what this iteration adds beyond that neighbour. This checks whether the FINDING has earned its claim, not how the paper will be framed against the literature: a positive result gets no credit for novelty in this record until that comparison is made, and its absence is a critique under 'novelty'
- Check for an iteration that added METRICS rather than SAMPLES to an already underpowered panel. When a power analysis or the effect sizes on record show the artifact panel cannot detect the effect being chased, more candidate metrics or readouts over the same panel do not fix that — flag it as a major issue and say the budget belonged on more graded samples or checkpoints instead
- Check COVERAGE against the user's ORIGINAL request, not against the report's own framing. Name the part of the request the run has not addressed yet
- Check that claims are PROPORTIONATE to the evidence. A small, expected-direction effect written up as the answer is the failure mode to name explicitly
- Do NOT review this as a paper. Section order, narrative arc, abstract framing, figure count and writing polish are the later paper step's concerns, and a critique about them spends the run's iteration budget on the wrong document. The nearest-neighbour check above is different: it asks whether the record has earned its positive claim, not how the paper will be sold against the literature. Bookkeeping — run ids, timestamps, spend, review scores, file hashes — BELONGS in this report; never ask for its removal

<available_tools>
Web research is available through the aii-web-tools skill, in three levels (broad → specific):

1. web search — Returns titles, URLs, snippets. Use first to discover and scan the landscape. Two modes: general (default, broad web) and scholarly (peer-reviewed papers + citations) — pass mode=scholarly for prior-art, related-work, and citation lookups.
2. web fetch — Reads a page and returns its content as markdown (HTML or PDF). Use to understand a source. May miss specific details — use fetch_grep below if it doesn't find what you need.
3. fetch_grep — Regex search over a page/PDF's full text. Returns exact matching sections with context. Use for precise details, exact numbers, methodology, or PDFs.

Workflow: search → fetch (understand) → fetch_grep (extract specifics).
</available_tools>

<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/review_report/review_report`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/review_report/review_report/`:
GOOD: `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/review_report/review_report/file.py`, `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/review_report/review_report/results/out.json`
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

<role>
You are a very experienced and critical conference reviewer specialized in the domain of the work under review.
You have reviewed for top-tier venues in the relevant field. Your reviews are known for
being thorough, fair, and grounded in the actual state of the field.
</role>

<report>
# Gold-Free Faithfulness Metrics for NL-to-FOL Translation

## Framing

Translating natural language into first-order logic (NL-FOL) is a prerequisite for neurosymbolic reasoning pipelines [10], yet evaluating whether a candidate formula faithfully captures a sentence's meaning remains an open problem. Gold FOL annotations are expensive, non-unique, and unreliable: Brunello et al. [3] found that approximately 42% of entries in both FOLIO [1] and MALLS [2] contain incorrect formalisations. Existing metrics either require a gold formula (exact match, prover-checked equivalence) or only verify that the output parses [5, 6]. The user's own pilot study used structural consistency checks (arity agreement, predicate-set overlap across reruns, joint satisfiability) that measure stability but not whether a formula says what its sentence says.

This run investigates gold-free metrics that predict faithfulness to the text given only a sentence and a candidate formula, with no reference formula, no ontology, and no domain knowledge. The evaluation is a meta-evaluation: we build a labelled set of (sentence, formula) pairs from public benchmarks whose gold has been audited, and measure each metric's ability to discriminate correct translations from errors.

## Iteration 1

### 1.1 Strategy

The iteration screens four candidate metric families head-to-head on a frozen evaluation set, with a disguised cheap LLM judge as the bar to beat.

**Candidates.** (A) FOL-Triage, a three-layer cascade: L1 (formula lint: deterministic formula smells), L2 (text accounting: bag-of-words and role-aware coverage), and L3 (role questionnaire: a small LLM reads the text and z3 reads the formula; their structured answers are compared). (B) Round-trip verification: verbalise the formula back to natural language and compare to the original via NLI or embedding similarity [7]. (C) Cross-system consensus: collect translations of the same sentence from multiple independent systems, measure z3-equivalence between the candidate and the peer pool, and score disagreement [8]. (D) Disguised cheap judge and baselines: an LLM judge, structural pilot metrics, and round-trip features evaluated on nonce-disguised sentences to control for memorisation.

**Evaluation set.** The frozen screen uses Logic-LM [10] released outputs on FOLIO validation: three LLM systems (GPT-3.5-turbo, GPT-4, text-davinci-003) producing 796 items. Track L contains LLM outputs labelled by z3 equivalence to corrected gold [4]; track H contains the 294 original human gold formulas, of which 57 are errors according to the corrected labels. The parallel run (run_qY2a2IS-WLIs) measured 43.9% of solver-non-equivalent candidates as faithful by a three-family panel; iteration 2 will re-score with those adjudicated labels.

**Decision rule.** A candidate must achieve AUROC ≥ 0.65 on track L (ERROR vs CORRECT), with coverage ≥ 90%, rewrite false-alarm rate ≤ 10% per rewrite family, and cost ≤ $0.002 per item. It advances only if its AUROC exceeds the disguised cheap judge's, with a paired bootstrap CI excluding zero.

**Held-out dataset (Artifact E).** A separate 700-sentence, 8,507-row held-out set was constructed from FOLIO training premises, MALLS training long/conditional/exception strata, and FOLIO curated conclusions, each translated by 9 LLM families plus ccg2lambda plus GPT-4 gold. Labels were assigned by z3 equivalence to audited gold, with contested cases adjudicated by a three-member panel (Claude Haiku-4.5, GLM-4.6, Kimi-K2). This set is reserved for iteration 2 confirmation. [ARTIFACT:art_U4Hsqt4Ay9Tg]

The dataset contains 1,750 CORRECT, 5,005 ERROR, 1,086 UNPARSEABLE, 276 UNRESOLVED, and 390 CONTESTED items. The panel calibration subset (173 items) shows that the panel agrees with expert-corrected labels on both faithful and unfaithful items. A screen audit of 1,173 items from the Logic-LM screen confirms the label assignment. The dataset cost $9.83 in API calls.

### 1.2 Experiment A: FOL-Triage

[ARTIFACT:art_d0njuqy2Csj-]

FOL-Triage was evaluated on the frozen screen with Gemini 2.5 Flash Lite as the primary LLM for L3. Total API spend was $0.29.

#### Headline AUROCs (track L, ERROR vs CORRECT, n = 477, 199 errors)

| Metric | AUROC | 95% CI | AUPRC |
|-|-|-|-|
| L1 (any smell) | 0.508 | [0.499, 0.519] | 0.425 |
| L2 bag-of-words | 0.737 | [0.677, 0.801] | 0.690 |
| L2 role-aware | 0.557 | [0.527, 0.594] | 0.476 |
| L3 score | 0.756 | [0.701, 0.809] | 0.657 |
| Fused (fitted on H, no leak) | 0.759 | [0.695, 0.825] | 0.740 |
| Fused (all H) | 0.827 | [0.778, 0.874] | 0.771 |
| Fused (cross-fit L) | 0.864 | [0.824, 0.902] | 0.789 |
| Decomposed judge (LLM reads formula) | 0.716 | [0.645, 0.789] | 0.717 |
| L3 with local Qwen2.5-1.5B | 0.708 | [0.637, 0.774] | 0.603 |

The primary no-leak fused score is 0.759. The fused-all-H and cross-fit-L numbers (0.827, 0.864) are shown for completeness but are not valid held-out estimates: the former uses the full track H for fitting, and the latter is a within-L cross-fit that overstates generalisation.

**Track H (human gold errors, n = 258, 57 errors).** Fused out-of-fold AUROC is 0.777 [0.698, 0.847]. L1 alone reaches 0.655, compared to 0.508 on track L. The lint rules fire on human annotation errors but not on LLM outputs, because the two populations produce different formula smells.

#### L1 lint: a negative result on LLM outputs

L1 flags formulas with deterministic smells (existential implication, free variables, arity clashes, vacuity, trivial formulas, dangling predicates). On track L, the true positive rate is 2.0% at a false positive rate of 0.4%, giving AUROC 0.508. This is a negative result: L1 lint does not transfer from human annotation errors (where it is effective, AUROC 0.655) to LLM outputs. The reason is that LLM-generated formulas rarely contain the syntactic pathologies L1 detects; their errors are semantic (wrong predicates, missing conditions, scope mistakes).

All nine individual smell rules have false-alarm rates below 3% on every system:

| Smell | gpt-3.5 FA | gpt-4 FA | davinci-003 FA |
|-|-|-|-|
| EX_IMP | 0.0 | 0.0 | 0.0 |
| ALL_AND | 0.0 | 0.0 | 0.0 |
| IFF_RESTR | 0.0 | 0.009 | 0.0 |
| GLUE | 0.0 | 0.0 | 0.0 |
| FREE | 0.0 | 0.0 | 0.0 |
| VACUOUS | 0.0 | 0.0 | 0.0 |
| TRIVIAL | 0.0 | 0.0 | 0.0 |
| ARITY | 0.0 | 0.0 | 0.0 |
| DANGLING | 0.0 | 0.0 | 0.0 |

Only the FREE smell fires on any track-L errors (4 items).

#### L2 role-aware check: below bag-of-words

The role-aware UD-based check (L2-role) achieves AUROC 0.557, which is 0.18 below the simpler bag-of-words check (L2-bow, 0.737). The role-aware layer adds no discriminative power over word overlap.

#### Decomposed judge ablation

Replacing z3 with an LLM that reads the formula directly (the decomposed judge) drops L3 AUROC from 0.756 to 0.697 (ΔAUROC = −0.059). The LLM gets only 57.6% of binary argument slots correct on track L and 36.4% on track H. The z3 answerer is significantly more accurate for structured formula reading.

#### Per-type sensitivity (track L, at binary threshold)

| Error type | n | L1 | L2-bow | L2-role | L3 | Fused | Cascade |
|-|-|-|-|-|-|-|-|
| NEG | 5 | 0.0 | 0.2 | 1.0 | 0.2 | 0.4 | 1.0 |
| QUANT | 2 | 0.0 | 0.0 | 0.5 | 0.0 | 0.5 | 0.5 |
| CONN | 4 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| DROP | 142 | 0.028 | 0.479 | 0.127 | 0.197 | 0.599 | 0.606 |
| ADD | 150 | 0.020 | 0.473 | 0.107 | 0.173 | 0.653 | 0.573 |
| SWAP | 12 | 0.0 | 0.0 | 0.083 | 0.25 | 0.083 | 0.333 |
| BIND | 8 | 0.125 | 0.0 | 0.125 | 0.0 | 0.375 | 0.25 |
| COMPOUND | 187 | 0.118 | 0.428 | 0.166 | 0.160 | 0.599 | 0.578 |

FOL-Triage is most sensitive to ADD and DROP errors (the largest categories), with the fused score catching about 60%. It misses CONN errors entirely (0/4) and detects SWAP poorly (1/12). Negation errors are fully caught by the cascade (which fires L2-role, where monotonicity shifts are visible) but L1 and L2-bow miss them.

On track H (57 errors), the per-type pattern differs. UNGLUE errors (n = 5) are caught at 100% by L1 and the fused score, because they produce detectable formula smells.

#### Per-type sensitivity (track H)

| Error type | n | L1 | L2-bow | L2-role | L3 | Fused | Cascade |
|-|-|-|-|-|-|-|-|
| NEG | 4 | 0.0 | 0.0 | 0.25 | 0.0 | 0.25 | 0.25 |
| REV | 1 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| QUANT | 1 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| RESTR | 1 | 1.0 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| CONN | 8 | 0.25 | 0.125 | 0.0 | 0.375 | 0.375 | 0.375 |
| MOVE | 2 | 0.5 | 0.0 | 0.5 | 0.0 | 0.5 | 1.0 |
| DROP | 14 | 0.143 | 0.357 | 0.0 | 0.143 | 0.357 | 0.5 |
| ADD | 19 | 0.158 | 0.368 | 0.053 | 0.211 | 0.526 | 0.579 |
| SWAP | 2 | 0.0 | 0.5 | 0.0 | 0.5 | 0.5 | 0.5 |
| BIND | 1 | 1.0 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| UNGLUE | 5 | 1.0 | 0.4 | 0.0 | 0.2 | 1.0 | 1.0 |
| COMPOUND | 33 | 0.303 | 0.182 | 0.242 | 0.182 | 0.545 | 0.636 |

#### Invariance under meaning-preserving rewrites

Five rewrite families were tested on 150 track-L CORRECT items. The table shows the false-alarm rate on the rewritten formula and the flip rate (fraction of items whose binary verdict changes):

| Rewrite | n applies | L1 FA | L1 flip | bow FA | bow flip | role FA | role flip | L3 FA | L3 flip | Fused FA | Fused flip |
|-|-|-|-|-|-|-|-|-|-|-|-|
| RENAME | 150 | 0.0 | 0.0 | 0.18 | 0.093 | 0.013 | 0.0 | 0.033 | 0.007 | 0.22 | 0.013 |
| REORDER | 34 | 0.0 | 0.0 | 0.029 | 0.0 | 0.059 | 0.0 | 0.059 | 0.0 | 0.235 | 0.0 |
| DEMORGAN | 33 | 0.0 | 0.0 | 0.030 | 0.0 | 0.061 | 0.0 | 0.030 | 0.030 | 0.182 | 0.061 |
| CONTRAPOSITIVE | 40 | 0.025 | 0.025 | 0.10 | 0.0 | 0.025 | 0.025 | 0.025 | 0.0 | 0.275 | 0.0 |
| PRENEX | 1 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |

The rewrite false-alarm gate (≤ 10% per family) fails. The worst-family fused FA is 0.275 (CONTRAPOSITIVE), but this equals the FA on the original formulas; the flip rate is at most 0.061. The high FA is not caused by the rewrites but by the fused score's calibration: it was fitted on track H where the CORRECT base rate is higher, producing a systematic over-flagging on track L (FA on track-L CORRECT items is 0.194 versus the 0.10 calibration target).

L1, L2-role, and L3 individually pass the 10% gate. L2-bow fails only under RENAME (FA = 0.18), because renaming predicates breaks the bag-of-words match between text and formula.

[FIGURE:fig_rewrite_fa]

#### Coverage

| Track | n | Parseable | Full coverage rate |
|-|-|-|-|
| L | 753 | 693 | 0.920 |
| H | 302 | 279 | 0.924 |

Parse rates by system: gpt-3.5-turbo 0.889, gpt-4 0.946, text-davinci-003 0.921. Unparseable outputs are scored as p = 1 (maximum error probability) by the fused metric, so all items receive a score. The coverage gate (≥ 90%) passes.

#### Cost

L1 and L2 are free (CPU-only). L3 costs $0.175 per 1,000 calls with Gemini 2.5 Flash Lite. The total per-item cost is $0.0002, passing the $0.002 gate. CPU time (L1 + L2 + z3): median 35 ms, P95 90 ms. L3 latency: median 630 ms, P95 1.68 s.

#### Contamination check

L3 was run on nonce-disguised sentences (content words replaced by nonsense words) on the full track L. AUROC with exact text-formula alignment: 0.765; with disguised text: 0.770. Paired difference: −0.005 [−0.063, 0.049]. There is no evidence that the LLM benefits from having seen the public benchmark sentences.

#### Complexity strata (track L, fused score)

| Stratum | n (error/correct) | Testable | Fused AUROC | L2-bow AUROC | L3 AUROC |
|-|-|-|-|-|-|
| words < 12 | 443 (179/264) | Yes | 0.781 | 0.742 | 0.772 |
| words 12-19 | 31 (18/13) | No | 0.521 | 0.596 | 0.541 |
| words ≥ 20 | 3 (2/1) | No | 0.500 | 1.000 | 0.000 |
| 0 quantifiers | 302 (130/172) | Yes | 0.743 | 0.728 | 0.771 |
| 1 quantifier | 164 (65/99) | Yes | 0.794 | 0.748 | 0.721 |
| ≥ 2 quantifiers | 11 (4/7) | No | 0.750 | 0.768 | 0.607 |
| depth ≤ 1 | 296 (124/172) | Yes | 0.762 | 0.745 | 0.779 |
| depth 2-3 | 173 (73/100) | Yes | 0.756 | 0.717 | 0.710 |
| depth ≥ 4 | 8 (2/6) | No | 0.667 | 0.750 | 0.500 |
| 0 conditions | 344 (145/199) | Yes | 0.775 | 0.759 | 0.791 |
| 1-2 conditions | 131 (54/77) | Yes | 0.716 | 0.677 | 0.628 |

The frozen screen is dominated by short, simple sentences (93% under 12 words). The long and complex strata (12+ words, 2+ quantifiers, 3+ conditions) have too few items to test. This limitation motivates the held-out dataset (Artifact E), which oversamples these strata.

#### Per-system AUROC (descriptive, n = 3 systems)

| System | n | Error rate | Fused AUROC | L1 AUROC | L2-bow AUROC | L3 AUROC |
|-|-|-|-|-|-|-|
| gpt-3.5-turbo | 143 | 0.378 | 0.689 | 0.500 | 0.650 | 0.722 |
| gpt-4 | 177 | 0.367 | 0.700 | 0.496 | 0.716 | 0.720 |
| text-davinci-003 | 157 | 0.510 | 0.857 | 0.525 | 0.811 | 0.817 |

FOL-Triage is most discriminative on text-davinci-003, the weakest system. The Kendall τ between system error rates and mean fused scores is 0.333 (3 systems, descriptive only).

#### Label quality observations

The track-L label distribution reveals a systematic issue: 58.8% of typed ERROR items have only ADD+DROP repair operators. On inspection, most of these are vocabulary or arity choices (e.g. Lunch(james) vs HasLunch(james, company)) that the vocabulary aligner cannot bridge. These are likely CORRECT under a looser equivalence definition. The track-H original gold has 27.1% error rate (errors, uncertain, and reading-choice items) and 5.8% unparseable rate. Among non-equivalent parseable items, 21.9% are correct-but-not-equivalent (VOCAB or GRAN class).

### 1.3 Experiment C: Cross-System Consensus

[ARTIFACT:art_i3cVDxBp-USk]

The consensus metric collects translations of the same sentence from multiple independent LLM families, checks pairwise z3 equivalence, and scores each candidate by its disagreement with the pool. Total API spend was $1.52.

#### Headline AUROCs (track L, ERROR vs CORRECT, n = 546, 249 errors)

| Metric | AUROC | 95% CI | AUPRC |
|-|-|-|-|
| c_score (1 − eq_frac, all peers) | 0.866 | [0.821, 0.906] | 0.827 |
| c_score (6 fresh peers only) | 0.872 | [0.830, 0.911] | 0.825 |
| c_score (non-OpenAI peers) | 0.863 | [0.820, 0.903] | 0.808 |
| c_score (2 Logic-LM peers only) | 0.753 | [0.701, 0.806] | 0.659 |
| medoid depth | 0.722 | [0.673, 0.774] | 0.622 |
| cluster entropy | 0.773 | [0.724, 0.820] | 0.691 |
| SC-5 cheap (gpt-4.1-nano) | 0.725 | [0.669, 0.781] | 0.627 |
| SC-5 same model | 0.716 | [0.632, 0.796] | 0.628 |
| SC-5 entropy | 0.631 | [0.568, 0.693] | 0.539 |
| Prediction set instability (SC) | 0.688 | [0.626, 0.750] | 0.602 |
| Prediction set instability (pool) | 0.770 | [0.717, 0.821] | 0.721 |
| FOL length | 0.527 | [0.470, 0.586] | 0.485 |
| Misalignment (vocab) | 0.835 | [0.794, 0.876] | 0.821 |

[FIGURE:fig_consensus_auroc]

The c_score achieves the highest AUROC in the iteration at 0.866. It beats SC-5 (the self-consistency baseline) by ΔAUROC = +0.140 [0.085, 0.197]. Cross-family consensus also exceeds sampling self-consistency in the related SAC3 framework [17], which uses semantic-aware cross-check consistency for hallucination detection in black-box LLMs. Using only the six fresh peer translations (not the three Logic-LM systems) gives 0.872, slightly higher than using all peers. Restricting to the two other Logic-LM systems drops the AUROC to 0.753, showing that diversity across model families is essential.


The misalignment score (0.835) is high because CORRECT items are by construction alignable to the gold in the labeller, so misalignment alone is a strong proxy for error. This does not generalise to settings without a shared vocabulary.

#### RENAME rewrite invariance: failure

Under predicate renaming (replacing predicate names with WordNet synonyms or nonce names), the c_score false-alarm rate is 96% (100% for constant-only renaming). This is expected and fundamental: two formulas with different predicate names are not z3-equivalent, so any rename breaks the equivalence check. The consensus metric is invariant to rewrites that preserve z3 equivalence (reordering, De Morgan, contrapositive) but not to vocabulary changes.

#### Blind-spot analysis

38% of ERROR items are z3-equivalent to the medoid (the most popular peer formula). This places a ceiling on recall of approximately 62%. The blind-spot rate is 5% for polarity errors and 57% for structural errors.

#### Cost

The peer pool costs $0.0015 per sentence (6 peers via API). Total experiment spend: $1.52. z3 pairwise equivalence checking is free.

### 1.4 Experiment D: Disguised Judge and Baselines

[ARTIFACT:art_elDZY26Pu6GD]

This experiment establishes the bar: every baseline metric and every judge variant on the same shared screen, scored with nonce-disguised sentences to control for memorisation. Total API spend was $2.02 (after the OpenRouter key was restored at 15:11 UTC; local judges ran during the outage and are kept as secondary rows).

#### The bar: disguised cheap judge

The primary cheap judge (Gemini 2.5 Flash Lite, JSON 0-100 scoring, nonce-disguised sentences) achieves AUROC 0.777 [0.720, 0.827] on track L (n = 524, 230 errors, 294 correct).

#### Full baseline table (track L, ERROR vs CORRECT, n = 524)

| Metric | AUROC | 95% CI |
|-|-|-|
| parse_fail | 0.500 | [0.500, 0.500] |
| pilot_joint_conflict | 0.513 | [0.488, 0.539] |
| pilot_arity_incons | 0.500 | [0.500, 0.500] |
| pilot_shape_incons | 0.524 | [0.470, 0.578] |
| pilot_dangling | 0.533 | [0.474, 0.592] |
| pilot_undeclared | 0.525 | [0.510, 0.542] |
| pilot_rerun_jacc | 0.720 | [0.659, 0.780] |
| rt_nli_min | 0.710 | [0.648, 0.769] |
| rt_nli_fwd | 0.652 | [0.588, 0.713] |
| rt_nli_bwd | 0.681 | [0.621, 0.742] |
| rt_nli_contra | 0.628 | [0.566, 0.686] |
| rt_nli_min_alt | 0.689 | [0.627, 0.749] |
| rt_embed_cos | 0.633 | [0.574, 0.696] |
| rt_reformalise_eq | 0.513 | [0.479, 0.547] |
| judge_cheap_orig | 0.749 | [0.695, 0.801] |
| judge_cheap_disg | 0.777 | [0.720, 0.827] |
| judge_cheap2_orig (gpt-4.1-nano) | 0.750 | [0.691, 0.810] |
| judge_cheap2_disg | 0.714 | [0.648, 0.777] |
| judge_strong_orig (gemini-3.1-pro) | 0.802 | [0.715, 0.877] |
| judge_strong_disg | 0.730 | [0.655, 0.803] |
| judge_local_qwen8b_disg | 0.757 | [0.702, 0.811] |
| judge_local_llama8b_disg | 0.671 | [0.604, 0.737] |
| judge_local_qwen14b_disg | 0.760 | [0.681, 0.834] |
| rt_nli_min_localverb | 0.740 | [0.680, 0.796] |

[FIGURE:fig_baseline_auroc]

#### Pilot structural metrics: negative result

The user's pilot structural metrics are null on this screen. Joint conflict achieves AUROC 0.513, arity inconsistency 0.500, shape inconsistency 0.524, dangling predicates 0.533, and undeclared predicates 0.525. The cross-system predicate-set Jaccard (pilot_rerun_jacc) reaches 0.720, the only pilot metric with signal, but this is a proxy for the consensus approach tested in Experiment C.

#### Round-trip verification

Round-trip NLI (verbalise the formula, compare to the original sentence via bidirectional NLI entailment) achieves AUROC 0.710 [0.648, 0.769]. This is 0.067 below the cheap judge (p = 0.008 by DeLong test). The round-trip reformalisation check (verbalise, re-translate to FOL, check z3 equivalence with the original) achieves only 0.513, because 76% of items tie at the same score.

Round-trip NLI using local verbalisation (the LLM verbalises on the local GPU instead of the API) reaches 0.740 [0.680, 0.796], slightly higher than the API version.

#### Frontier judge

The strong judge (Gemini 3.1 Pro Preview) achieves AUROC 0.802 [0.715, 0.877] on the strong subsample (n = 291). Under disguise it drops to 0.730 [0.655, 0.803]. The ΔAUROC over the cheap judge is +0.024 [−0.075, 0.111], not significant.

#### Cross-fitted baseline combinations (track L)

| Combination | AUROC | 95% CI |
|-|-|-|
| S1 (structural) | 0.698 | [0.634, 0.761] |
| S2 (round-trip) | 0.687 | [0.625, 0.749] |
| S3 (judges disguised) | 0.771 | [0.705, 0.831] |
| S4 (all cheap features) | 0.817 | [0.762, 0.867] |
| S6 (S4 + local judges) | 0.810 | [0.753, 0.861] |

S4 (all cheap features combined via cross-fitted logistic regression) achieves 0.817. This is +0.039 [−0.010, 0.087] over the cheap judge alone, not significant, but it sets the empirical ceiling for cheap baselines.

#### Contamination analysis

No evidence of contamination was found for any judge. The difference-in-differences (DiD) test compares the disguise effect on track H (where the LLM could have memorised public gold) to track L (where it evaluates its own outputs, not memorisable). All DiD CIs include zero:

| Judge | DiD (H − L) | 95% CI |
|-|-|-|
| flash-lite | −0.042 | [−0.170, 0.094] |
| gpt-4.1-nano | −0.077 | [−0.188, 0.023] |
| gemini-3.1-pro | +0.002 | [−0.115, 0.104] |
| Qwen3-8B | −0.045 | [−0.161, 0.079] |
| Llama-3.1-8B | +0.023 | [−0.112, 0.157] |
| Qwen3-14B | −0.073 | [−0.195, 0.056] |

The gold-recall probe confirms this: when the primary model translates track-H sentences from scratch, it matches the corrected gold 15.9% of the time but the original (public) gold only 4.4%. Predicate-name Jaccard with the original gold minus Jaccard with the Logic-LM GPT-4 output is −0.068 [−0.171, 0.034]; the model is not reproducing the public gold.

#### Invariance of judges under meaning-preserving rewrites

Judges are highly sensitive to meaning-preserving rewrites. The FA on CONTRAPOSITIVE rewrites is 0.67 for the cheap judge (original), 0.51 for the cheap judge (disguised), and 0.95 for the cheap2 judge. This compares poorly to FOL-Triage's fused flip rate of 0.0 on CONTRAPOSITIVE.

The full invariance table (track L CORRECT items, n = 270):

| Metric | RENAME flip | REORDER flip | DEMORGAN flip | CONTRA flip | ALL flip |
|-|-|-|-|-|-|
| judge_cheap_orig | 0.27 | 0.12 | 0.23 | 0.64 | 0.29 |
| judge_cheap_disg | 0.44 | 0.12 | 0.46 | 0.41 | 0.39 |
| judge_cheap2_orig | 0.49 | 0.12 | 0.46 | 0.95 | 0.49 |
| rt_nli_min | 0.37 | 0.10 | 0.31 | 0.33 | 0.31 |
| rt_embed_cos | 0.57 | 0.07 | 0.44 | 0.38 | 0.44 |
| FOL-Triage fused | 0.013 | 0.0 | 0.061 | 0.0 | 0.013 |

FOL-Triage has the lowest flip rate of any metric tested. Judges and round-trip methods change their verdict on 29-49% of meaning-preserving rewrites.

#### Per-error-type sensitivity of judges (track H, curator view, n = 46 errors)

| Group | n | judge_cheap_orig | judge_cheap_disg | judge_cheap2_orig | rt_nli_min |
|-|-|-|-|-|-|
| 1-op errors | 13 | 0.308 | 0.538 | 0.462 | 0.231 |
| 2-op errors | 11 | 0.545 | 0.818 | 0.727 | 0.273 |
| ADD | 12 | 0.500 | 0.750 | 0.667 | 0.250 |
| COMPOUND | 22 | 0.545 | 0.864 | 0.773 | 0.273 |
| DROP | 11 | 0.455 | 0.636 | 0.455 | 0.182 |
| CONN | 3 | 0.667 | 0.667 | 1.000 | 0.333 |
| NEG | 2 | 0.500 | 0.500 | 1.000 | 0.500 |
| SWAP | 2 | 0.000 | 1.000 | 0.500 | 0.000 |

The disguised judge is more sensitive than the original judge for most error types, suggesting that nonce disguise forces the model to read more carefully.

#### Judge error-type classification accuracy

The judge's ability to name the correct error type is poor. On track-H 1-op errors, it identifies the correct repair operator 0% of the time (0/12). On 2-op errors, it is correct 45% (5/11). On track L, accuracy is 20% for 1-op and 27% for 2-op errors.

#### Complexity analysis (track L)

A logistic regression of judge correctness on standardised word count yields a coefficient of −0.48 (SE 0.11, p < 0.001): the judge is significantly less reliable on longer sentences. On track H (where longer sentences are available), the coefficient is −0.14 (SE 0.17, p = 0.41), consistent in direction but underpowered.

| Stratum | n (err/cor) | judge_cheap_disg AUROC | rt_nli_min AUROC |
|-|-|-|-|
| words < 12 | 485 (210/275) | 0.784 | 0.713 |
| words 12-19 | 36 (18/18) | 0.667 | 0.670 |
| quantifiers 0-1 | 512 (226/286) | 0.784 | 0.712 |
| depth ≤ 3 | 466 (199/267) | 0.781 | 0.702 |
| depth 4-5 | 54 (30/24) | 0.762 | 0.828 |
| 0 conditions | 394 (182/212) | 0.783 | 0.745 |
| 1-2 conditions | 128 (48/80) | 0.765 | 0.653 |

#### System-level descriptive statistics (3 systems, descriptive only)

| System | True error rate | Judge flag rate | rt_nli_min mean | Parse failures |
|-|-|-|-|-|
| gpt-3.5-turbo | 0.415 | 0.444 | 0.516 | 26/248 |
| gpt-4 | 0.385 | 0.362 | 0.496 | 10/282 |
| text-davinci-003 | 0.527 | 0.553 | 0.663 | 20/266 |

#### API outage and robustness

The shared OpenRouter key was exhausted at 13:29 UTC and restored at 15:11 UTC. During the outage, all LLM judges ran on the local RTX 4000 Ada GPU with the same prompts (Qwen3-8B, Llama-3.1-8B, Qwen3-14B-nf4). After the key was restored, the API judges were run and designated as primary; the local judges are kept as secondary rows. The local Qwen3-8B judge achieves AUROC 0.757 (disguised), comparable to the API flash-lite judge at 0.777.

### 1.5 Iteration 1 Summary

The four candidates and the bar:

| Method | AUROC | 95% CI | n | Cost/item | Rewrite flip rate |
|-|-|-|-|-|-|
| c_score (consensus) | 0.866 | [0.821, 0.906] | 546 | $0.0015/sent | 96% (RENAME) |
| S4 baseline combo | 0.817 | [0.762, 0.867] | 524 | varies | varies |
| **Bar: judge_cheap_disg** | **0.777** | **[0.720, 0.827]** | **524** | **$0.00004** | **0.39** |
| FOL-Triage fused | 0.759 | [0.695, 0.825] | 477 | $0.0002 | 0.013 |
| rt_nli_min | 0.710 | [0.648, 0.769] | 524 | $0.00001 | 0.31 |
| L1 lint | 0.508 | [0.499, 0.519] | 477 | $0 | 0.0 |
| Pilot structural | 0.50-0.53 | n/a | 524 | $0 | n/a |

[FIGURE:fig_summary_comparison]

**What iteration 1 established:**

1. The cross-system consensus metric (c_score = 1 − eq_frac) achieves the highest AUROC at 0.866, beating SC-5 by +0.140. It requires peer translations from multiple model families and is fundamentally non-invariant to predicate renaming (96% FA under RENAME).

2. The disguised cheap judge sets the bar at AUROC 0.777. The S4 combination of all cheap features reaches 0.817 (+0.039, not significant). The frontier judge (Gemini 3.1 Pro) adds nothing significant over the cheap judge.

3. FOL-Triage achieves AUROC 0.759, below the bar. Its primary value is invariance: the fused flip rate under meaning-preserving rewrites is 0.013, compared to 0.29-0.49 for judges. However, the fused false-alarm rate on CORRECT items is 0.194, exceeding the 0.10 calibration target.

4. L1 lint does not transfer from human annotation errors to LLM outputs. The pilot structural metrics are null. Round-trip NLI is 0.067 below the judge.

5. The evaluation labels are noisy: 58.8% of track-L "errors" are pure ADD+DROP (likely vocabulary mismatches). Iteration 2 will re-evaluate under panel-adjudicated labels from the held-out set.

6. No contamination was detected for any LLM-based metric.

**What remains for iteration 2:** (a) Re-evaluate all candidates under adjudicated labels from Artifact E. (b) Compute the paired ΔAUROC between FOL-Triage and the disguised judge on shared items. (c) Test whether combining the consensus metric with FOL-Triage or the judge produces a significant improvement. (d) Confirm on the held-out set.

## Iteration 2

### 2.1 Strategy

Iteration 2 has three goals: (i) confirm iteration 1's ordering on the held-out dataset E under both the solver labels (R_AB, R_A) and panel-adjudicated labels (R_ADJ); (ii) test whether fusing the consensus signal (PEER) with text-based checks (TEXT = L2-bow + L3) improves over each alone; and (iii) construct a typed perturbation suite (PERTURB) for controlled sensitivity testing.

The pre-registered bar for this iteration is the flash-lite judge on disguised sentences, with the local Qwen3-8B judge as fallback if the API is unavailable. The shared OpenRouter key hit its daily limit at 18:00 UTC on 2026-09-23, before the held-out experiment completed, and did not recover before the run deadline. The flash-lite bar is therefore UNTESTABLE on E; the fallback local judge (Qwen3-8B, rubric B, greedy; screen AUROC 0.757 vs 0.777 for flash-lite) is the labelled secondary bar for all rows reported below.

### 2.2 Experiment 5: PEER+TEXT on held-out dataset E

[ARTIFACT:art_TaxJRnPcJMuZ]

PEER+TEXT is a logistic fusion of the consensus signal (c_score with shared-vocabulary alignment, denoted c_score_align) and the text-based FOL-Triage layers (L2-bow, L3 questionnaire). The fusion weights were fitted on the iteration-1 screen and frozen before any E score was computed (prereg sha256 b9f28b1bf6bf). API spend was $0 (all components ran on CPU and the local GPU; no OpenRouter calls completed).

#### Name-free alignment: failed the pre-registered screen gate

A name-free variant of the consensus metric (graded clause consensus, g_score) was pre-registered as the primary PEER signal. It matches formula clauses by structural role without relying on shared predicate names, using anchored-cost assignment and Murty k-best matching. Under the pre-registered selection rule, both name-free variants (NF-pure and NF-anchored) failed the screen gate: for both, more than 10% of AGREE track-L CORRECT items tie at g = 1, making the deterministic false-alarm threshold degenerate (ROLE_PERMUTE recall = 0).

A post-hoc analysis with fractional tie-breaking showed this failure was a threshold-tie artefact. NF-anchored passes both gates under fractional scoring (RENAME FA 0.074, ROLE_PERMUTE recall 0.771); NF-pure still fails ROLE_PERMUTE (recall 0.186). The NF-anchored fusion was fitted post-hoc and applied to E as a labelled sensitivity analysis. On E (R_AB pooled), the NF-anchored fusion achieves AUROC 0.759 [0.72, 0.79], which is 0.031 below the pre-registered PEER+TEXT fusion (0.790), with the CI excluding zero [−0.042, −0.020]. The shared-aligner confound with the solver labeller remains open.

#### Headline AUROCs on E (R_AB, ERROR vs CORRECT)

| Subset | n (err/cor) | PEER+TEXT | c_score_align | NF c_score | L2-bow | L3 | Local judge |
|-|-|-|-|-|-|-|-|
| R_AB pooled | 2686 (1822/864) | 0.790 [0.75, 0.82] | 0.782 [0.74, 0.82] | 0.743 [0.70, 0.78] | 0.734 [0.71, 0.76] | 0.579 [0.53, 0.62] | 0.712 |
| R_AB L25 | 873 (697/176) | 0.755 [0.70, 0.80] | 0.712 [0.65, 0.77] | 0.651 [0.59, 0.71] | 0.722 [0.67, 0.77] | 0.560 [0.49, 0.63] | 0.664 |
| R_AB L20 | 821 (592/229) | 0.747 [0.69, 0.80] | 0.722 [0.66, 0.78] | 0.643 [0.58, 0.70] | 0.715 [0.66, 0.76] | 0.547 [0.48, 0.62] | 0.683 |
| R_AB EXC | 606 (384/222) | 0.777 [0.72, 0.83] | 0.814 [0.76, 0.86] | 0.782 [0.72, 0.84] | 0.669 [0.61, 0.72] | 0.620 [0.55, 0.69] | 0.663 |
| R_AB CTRL | 386 (149/237) | 0.708 [0.57, 0.84] | 0.742 [0.62, 0.86] | 0.741 [0.61, 0.86] | 0.613 [0.54, 0.72] | 0.490 [0.37, 0.62] | 0.739 |
| R_AB long pool | 2300 (1673/627) | 0.768 [0.74, 0.80] | 0.759 [0.72, 0.79] | 0.704 [0.67, 0.74] | 0.717 [0.69, 0.75] | 0.580 [0.54, 0.62] | 0.653 |
| R_A pooled L20+EXC | 449 (261/188) | 0.818 [0.73, 0.88] | 0.860 [0.79, 0.92] | 0.802 [0.72, 0.87] | 0.678 [0.61, 0.74] | 0.587 [0.51, 0.66] | 0.554 |

[FIGURE:fig_held_out_auroc]

#### PEER+TEXT vs the local judge

The paired ΔAUROC of PEER+TEXT minus the local judge is +0.078 [0.043, 0.112] on R_AB pooled (DeLong p < 0.0001). On the long pool (L25+L20+EXC), the gap widens to +0.115 [0.075, 0.157]. On R_A (tier-A adjudicated labels, L20+EXC), the gap is +0.264 [0.157, 0.359].

The flash-lite judge comparison is untestable: only 20 items received flash-lite scores before the key was exhausted, yielding a ΔAUROC of +0.057 [−0.200, 0.360] (n = 20, uninformative).

#### Does fusion beat c_score_align alone?

The stratified AUROC (pairing only within complexity strata, removing the composition confound) shows PEER+TEXT at 0.753 and c_score_align at 0.741, a difference of +0.011 [−0.012, 0.038], not significant. On the long pool the stratified gap is +0.016 [−0.010, 0.041]. On R_A the gap is −0.036 [−0.113, 0.030], favouring c_score_align. The TEXT layers add no significant discriminative power over c_score_align alone once the stratum-composition confound is removed.

#### Mechanism predictions

Four pre-registered mechanism predictions were tested on E:

**P1 (PEER catches COVERAGE errors that TEXT misses, and vice versa).** At matched false-alarm rate 0.10 with fractional tie-breaking: PEER has higher recall than TEXT on COVERAGE errors (+0.093 [0.046, 0.147]), and TEXT has higher recall on PEER_ENDORSED errors (+0.103 [0.051, 0.171]). The crossover exists, but the fused PEER+TEXT recall is not higher than c_score_align alone on any group except COVERAGE. Verdict: INCONCLUSIVE.

**P2 (PEER and TEXT error rankings are uncorrelated).** Spearman correlation between PEER and TEXT among errors is 0.294 [0.224, 0.365]. This is moderate, not near zero. The gain from fusion over the best single signal (PEER) is only +0.042 AUROC, and the share from PEER-endorsed errors is −0.200, meaning TEXT hurts on items PEER already handles. Verdict: REFUTED.

**P3 (PEER+TEXT advantage grows with sentence complexity).** The logistic interaction term z(score)·z(words) is −0.023 [−0.228, 0.185] for PEER+TEXT, consistent with no interaction. The diff-in-Δ (long minus CTRL) of PEER+TEXT minus the local judge is +0.146 [0.020, 0.269], but this reflects the judge degrading on long sentences, not the fusion improving. Verdict: INCONCLUSIVE.

**P4 (PEER+TEXT is more invariant to meaning-preserving rewrites than judges).** On the screen pools, the fused score's RENAME false-alarm rate is 0.385 and the local judge's is 0.683. The fused score is better than judges but far worse than FOL-Triage's 0.013. The c_score_align component drives most of the fused FA under RENAME (0.859). Verdict: REFUTED.

#### Rewrite false alarms (screen, CORRECT bases)

| Rewrite | n | Fused | c_score_align | NF g | L2-bow | L3 | Local judge |
|-|-|-|-|-|-|-|-|
| RENAME | 104 | 0.385 | 0.859 | 0.074 | 0.216 | 0.168 | 0.683 |
| REORDER | 27 | 0.222 | 0.178 | 0.037 | 0.044 | 0.444 | 0.000 |
| DEMORGAN | 26 | 0.154 | 0.185 | 0.038 | 0.046 | 0.231 | 0.231 |
| CONTRAPOSITIVE | 28 | 0.107 | 0.063 | 0.237 | 0.075 | 0.188 | 0.214 |

The NF g_score has the lowest RENAME false-alarm rate (0.074) of any consensus-based signal, confirming the value of name-free matching. However, its CONTRAPOSITIVE FA (0.237) is higher than c_score_align's (0.063).

#### Error typing

On R_A errors with 1-2 typed repair operators (n = 453), the top-code accuracy of the medoid-ops typed repair is 0.371 (codable-only 0.561, n = 262). Chance level is 0.382. The local judge's type-classification accuracy is 0.022 (10/453). Error typing from automated metrics remains unreliable.

#### System-level correlation

Kendall τ-b of each metric vs the R_AB system error rate across 13 system × variant rows: PEER+TEXT 0.718, TEXT alone 0.769, PEER alone 0.692, local judge 0.667. All metrics track system quality at the aggregate level.

#### Contamination on E

The local Qwen3-8B judge shows a disguise effect in the unexpected direction: disguised AUROC (0.712) exceeds original AUROC (0.648) by +0.064 [0.032, 0.098]. This is likely because nonce disguise forces the model to attend to structural cues rather than relying on surface familiarity. The DiD test (comparing the disguise effect on track H vs track L) yields +0.045 [−0.073, 0.161], with the CI including zero. No contamination is detected. The PEER signal has no contamination channel, because it uses z3 equivalence (no text or names from the benchmark enter the scoring).

#### Coverage and cost

Of 8,507 rows, 7,421 (87.2%) are parseable and scored; 1,086 (12.8%) are unparseable (scored as maximum error probability). 38 rows have no peer translations available. The L3 questionnaire completed on all parseable rows. Mean CPU time per row: PEER pairs 0.026 s, NF pairs 0.208 s, TEXT 0.220 s. Mean cost per row for PEER+TEXT (L3 share): $0.000018. The local judge costs $0.000040 per row.

### 2.3 Evaluation 1: Re-evaluation under alternative label regimes

[ARTIFACT:art_HepAw8c6Eu7-]

The iteration-1 experiments used solver labels (R_SOLVER): a formula is CORRECT if z3 proves it equivalent to the audited gold, ERROR otherwise. This is conservative: formulas that are semantically faithful but use different vocabulary or granularity are counted as errors. The parallel run adjudicated a panel of labels (R_ADJ) on the same items, where three LLM judges vote on faithfulness given only the sentence and candidate. This evaluation re-scores all metrics under 13 label regimes on a common item set (588 items shared across experiments A, C, D, and E).

#### Rederivation audit

All 57 reviewer-audited quantities from the iteration-1 report reproduce exactly under independent recomputation (57/57 MATCH, tolerance ≤ 0.01 for AUROCs, ≤ 0.005 for bootstrap replicas). The reviewer's own RNG seed replicas match to ≤ 0.0005.

#### Regime AUROC matrix (common set, selected metrics)

| Metric | R_SOLVER | R_ADJ_AB | R_ADJ_A | R_ADJ_ALL |
|-|-|-|-|-|
| PT (PEER+TEXT) | 0.871 | 0.877 | 0.932 | 0.906 |
| fused_H (FOL-Triage) | 0.770 | 0.868 | 0.958 | 0.866 |
| c_score | 0.849 | 0.779 | 0.786 | 0.831 |
| L2-bow | 0.732 | 0.815 | 0.917 | 0.810 |
| L3 | 0.761 | 0.718 | 0.813 | 0.751 |
| judge_cheap_disg | 0.782 | 0.772 | 0.751 | 0.816 |
| judge_cheap_orig | 0.754 | 0.797 | 0.858 | 0.785 |
| sc5_cheap | 0.713 | 0.703 | 0.676 | 0.737 |
| rt_nli_min | 0.709 | 0.749 | 0.731 | 0.760 |

Under R_ADJ_AB, PEER+TEXT (0.877) leads, followed by FOL-Triage fused (0.868) and L2-bow (0.815). The c_score drops from 0.849 (solver) to 0.779 (R_ADJ_AB), because the adjudicated labels reclassify many vocabulary-mismatch items as CORRECT, removing the easy wins for the consensus signal. Under R_ADJ_A (tier-A only, 75 common items), FOL-Triage reaches 0.958 and PEER+TEXT 0.932, both well above the judges.

#### Label regime shifts

On the 161 items shared between R_SOLVER and R_ADJ_AB (36 label changes), the label-only shift is:

| Metric | Shift | 95% CI | Direction |
|-|-|-|-|
| fused_H | +0.080 | [0.003, 0.171] | UP |
| L2-bow | +0.102 | [0.018, 0.192] | UP |
| c_score | −0.106 | [−0.255, 0.013] | INSIDE CI |
| judge_cheap_disg | +0.018 | [−0.094, 0.134] | INSIDE CI |

BOW and the fused score benefit from adjudicated labels (their AUROCs go up), because the vocabulary-mismatch items they flag correctly are now labelled CORRECT. The c_score shift is negative but not significant, consistent with its reliance on the same vocabulary alignment that the solver uses.

#### Flipped items

Between solver and adjudicated labels, 51 items flip from CORRECT to ERROR and 1 flips from ERROR to CORRECT. The fused score (FOL-Triage) flags 83% of the CORRECT→ERROR items at matched FA 0.20, while c_score flags only 34%. This indicates that the text-based layers detect errors that the solver misses (vocabulary-equivalent but semantically wrong).

#### Frontier vs cheap judge

On the subset where both frontier (Gemini 3.1 Pro) and cheap judge scores are available, the frontier judge's advantage is large and significant under adjudicated labels. Under R_ADJ_AB: strong_orig vs cheap_orig ΔAUROC = +0.166 (p < 0.001). Under R_ADJ_ALL: +0.159. This reverses the iteration-1 finding (which showed no significant advantage under solver labels), confirming that the solver labels masked the frontier judge's advantage on vocabulary-mismatch items.

#### Contamination on the common set

All DiD CIs include zero across all judges. The MDE (minimum detectable effect at 80% power) ranges from 0.12 to 0.21, so small contamination effects cannot be ruled out but no evidence was found. The gpt-4.1-nano judge shows significant single-track drops on H (AUROC disg−orig = −0.114 [−0.206, −0.028]), but the DiD with track L is +0.077 [−0.028, 0.190], not significant.

### 2.4 Dataset 3: R_COMP and PERTURB

[ARTIFACT:art_zcwCQgTqk6DN]

This artifact constructs two evaluation resources: R_COMP (long composed sentences with trusted FOL references) and PERTURB (a typed perturbation suite with z3-verified controls).

#### R_COMP: incomplete (OpenRouter key exhausted)

The R_COMP component generates long, complex sentences (≥ 25 words, ≥ 3 conditions) by composing atoms from a verified lexicon of 652 entries extracted from FOLIO and MALLS source formulas. Nine templates (T1-T9) produce sentences with weak and strong exception readings, each with a z3-verified reference formula. The composition pipeline selected 250 main + 100 reserve sentences from 5,109 filtered candidates.

The candidate generation, labelling, and adjudication phases did not run because the shared OpenRouter key hit its $50 daily limit at approximately 18:00 UTC, after $0.41 in lexicon-extraction calls. The key did not recover before the module's deadline. The replacement key arrived at 21:38 UTC but was already at its daily limit. R_COMP references are constructed deterministically and are correct by construction, but the LLM-generated candidate translations and their labels are absent.

#### PERTURB: complete

The typed perturbation suite applies 12 operator types to 300 base formulas (200 from dataset E, 100 from R_COMP sentences) to produce controlled mutants where the error type and direction are known by construction. All mutants are z3-verified: the DOWN mutant is z3-non-equivalent to the base and the matched CONTROL is z3-equivalent.

| Statistic | Value |
|-|-|
| Base formulas | 300 |
| Total mutants (DOWN + UP) | 4,234 |
| Matched controls | 868 |
| Total suite rows | 5,102 |
| Complete DOWN/UP pairs | 1,354 |
| z3 verification failures | 0 |
| Operator types | 12 (NEG, REV, QUANT, RESTR, CONN, MOVE, DROP, ADD, SWAP, BIND, SCOPE, UNGLUE) |
| Cost | $0.41 |

Each perturbation row carries a known label (ERROR for DOWN mutants, CORRECT for controls) and a typed operator, enabling per-type sensitivity analysis without relying on automated error classification. The suite is fully deterministic and re-runnable.

### 2.5 Iteration 2 Summary

**What iteration 2 established:**

1. PEER+TEXT achieves AUROC 0.790 [0.75, 0.82] on the held-out dataset E (R_AB pooled, n = 2686), beating the local judge by +0.078 [0.043, 0.112] (DeLong p < 0.0001). On long sentences (L25+L20+EXC, n = 2300) the gap widens to +0.115 [0.075, 0.157]. The flash-lite judge bar is UNTESTABLE due to API key exhaustion (only 20 rows scored).

2. Fusion does not significantly beat c_score_align alone. The stratified AUROC difference (PEER+TEXT minus c_score_align) is +0.011 [−0.012, 0.038] on R_AB pooled. The TEXT layers add coverage on COVERAGE-type errors (+0.093 recall at matched FA) but hurt on PEER-endorsed errors (−0.200 share). The mechanism prediction P2 (uncorrelated error rankings) is REFUTED: Spearman(PEER, TEXT) = 0.294.

3. The name-free consensus variant (NF-anchored) failed the pre-registered screen gate due to a threshold-tie artefact. Post-hoc fractional scoring shows it passes both gates (RENAME FA 0.074, ROLE_PERMUTE recall 0.771) and achieves AUROC 0.759 on E, 0.031 below PEER+TEXT. The NF approach has the lowest RENAME false-alarm rate (0.074) of any consensus signal, confirming the value of vocabulary-independent matching, but was not used in the primary analysis.

4. Under adjudicated labels (R_ADJ_AB), the metric ranking changes. FOL-Triage fused rises from 0.770 (solver) to 0.868 (adjudicated). The c_score drops from 0.849 to 0.779. This is because adjudicated labels reclassify vocabulary-mismatch items as CORRECT, removing the consensus signal's easy wins. PEER+TEXT (0.877) still leads under adjudicated labels.

5. The frontier judge advantage is large under adjudicated labels (+0.166 AUROC over the cheap judge under R_ADJ_AB, p < 0.001), reversing the non-significant iteration-1 finding under solver labels. Solver labels masked the frontier judge's advantage.

6. All 57 reviewer-audited numbers from iteration 1 reproduce exactly (57/57 MATCH).

7. The PERTURB suite (4,234 typed mutants + 868 controls, 12 operator types, all z3-verified) is complete and ready for per-type sensitivity analysis. R_COMP candidate generation is blocked on the OpenRouter key.

**What remains:**

(a) Run the flash-lite judge on E when the OpenRouter key resets, to test the pre-registered bar. (b) Complete R_COMP candidate generation and labelling. (c) Score all metrics on the PERTURB suite for per-type sensitivity under known labels. (d) Re-fit the PEER+TEXT fusion under R_ADJ labels (the current fusion was fitted under solver labels, which penalise it). (e) Test whether a name-free fusion (NF-anchored + TEXT) closes the 0.031 gap with the aligner-based fusion when the aligner confound is removed.

## Related Work

**NL-FOL datasets and their quality.** FOLIO [1] provides 1,435 FOL-annotated NLI problems. MALLS [2] uses GPT-4 to generate and verify NL-FOL pairs at scale. Brunello et al. [4] found that approximately 42% of entries in both datasets contain incorrect FOL formalisations, with additional ambiguity rates of 17.8% (FOLIO) and 51% (MALLS). Their LLM-assisted re-labelling framework reduces human effort by 5-15× compared to exhaustive review. Logic-LM [10] prompts LLMs for FOL and calls a prover, releasing outputs that we use as our evaluation screen.

**FOL closeness metrics.** Thatikonda et al. [5] evaluate n-gram, graph, embedding, and LLM-based metrics on controlled FOL perturbations, finding that no single metric is sensitive to all perturbation types. Smatch++ is the most sensitive to quantifier changes, while BL-score responds most to negation. Their work measures sensitivity to synthetic perturbations; ours measures faithfulness prediction on real LLM outputs with noisy labels.

**NL-FOL error taxonomies.** Thatikonda et al. [6] propose a verification pipeline with a 28-category error taxonomy. Brunello et al. [4] classify errors into semantic and structural categories. Our typed repair operators (NEG, REV, QUANT, RESTR, CONN, MOVE, DROP, ADD, SWAP, BIND, SCOPE, UNGLUE) follow the same tradition but are derived from z3 equivalence-class differences rather than manual annotation.

**Factuality metrics.** FRANK [11] defines a typology of factuality errors in abstractive summarisation and evaluates correlation of automatic metrics with human judgments. QuestEval [13] uses question generation and answering to assess factual consistency. QAGS [12] similarly generates questions from a summary and checks whether the source answers them the same way. Our L3 questionnaire layer is closest to this family: it generates structured questions from the text and checks the formula's answers via z3, rather than using another LLM.

**Round-trip and self-consistency.** Amrollahi et al. [7] propose verbalising a formal statement back to natural language and checking consistency, reporting high accuracy on mathematical autoformalization. Li et al. [8] use symbolic equivalence and semantic consistency for Lean/Isabelle autoformalization. Our round-trip baseline follows the same pattern but achieves only AUROC 0.710 on NL-FOL, below the LLM judge.

**Monotonicity and polarity.** SyGNS [14] tests monotonicity reasoning in NLI models. Udep2Mono [15] computes monotonicity profiles from Universal Dependencies. Our L2 role-aware layer attempted to use monotonicity-aware comparisons but achieved AUROC 0.557, a negative result.

**Counter-interpretation methods.** CLOVER [9] generates counter-interpretations to test logical validity via an LLM oracle. Our consensus approach is related in spirit: it uses multiple independent translations as implicit counter-proposals, but relies on z3 equivalence rather than LLM-generated counterexamples.

**Cross-check consistency.** SAC3 [17] detects hallucinations in black-box LLMs by sampling diverse perturbations of a query and checking consistency across answers. Our cross-system consensus metric uses a similar principle: disagreement among independent translations signals error. It operates on FOL equivalence rather than textual similarity, and uses multiple model families rather than perturbations of a single model. The ΔAUROC of cross-family consensus over single-model self-consistency is +0.140 in our setting, consistent with SAC3's finding that semantic-aware cross-checking outperforms naive self-consistency.

**Automated alignment for autoformalization.** FormalAlign [18] trains a model on both autoformalization and alignment scoring via a dual contrastive-generative loss, targeting Lean/Isabelle autoformalization. It is the closest published gold-free alignment scorer for formal languages. Our approach differs in that we use no learned alignment model: the consensus signal relies on z3 equivalence among independent translations, and the text-based signal uses deterministic checks and a prompted questionnaire. FormalAlign targets mathematical theorem proving, where the target language has a type checker; NL-FOL has no such verifier, making gold-free evaluation harder.

**Vacuity detection.** Kupferman and Vardi [16] formalise vacuity in temporal logic model checking. Our L1 lint layer includes a vacuity check (detecting formulas where a subformula can be replaced by its negation without changing the truth value), adapted from their framework.

## References

[1] Han et al. (2022). FOLIO: Natural Language Reasoning with First-Order Logic. EMNLP.

[2] Yang et al. (2023). MALLS: Multi-Agent Annotated NL-FOL Benchmarks for Logical Reasoning. arXiv:2305.13252.

[3] Brunello et al. (2026). Fixing FOLIO and MALLS: Verified Annotations and an LLM-assisted Framework to Focus Human Relabeling. arXiv:2606.02837.

[4] Brunello et al. (2025). Do LLMs Really Struggle at NL-FOL Translation? AAAI 2026.

[5] Thatikonda et al. (2025). Assessing the Sensitivity and Alignment of FOL Closeness Metrics. EMNLP Findings.

[6] Thatikonda et al. (2024). Strategies for Improving NL-to-FOL Translation with LLMs. arXiv:2409.16461.

[7] Amrollahi et al. (2026). Faithful Autoformalization via Roundtrip Verification and Repair. arXiv:2604.25031.

[8] Li et al. (2024). Autoformalize Mathematical Statements by Symbolic Equivalence and Semantic Consistency. NeurIPS.

[9] Ryu et al. (2024). CLOVER: Compositional First-Order Logic Translation and Verification. ICLR.

[10] Pan et al. (2023). Logic-LM: Empowering Large Language Models with Symbolic Solvers for Faithful Logical Reasoning. EMNLP.

[11] Pagnoni et al. (2021). FRANK: A Benchmark for Factuality Metrics. NAACL.

[12] Wang et al. (2020). QAGS: Asking and Answering Questions to Evaluate Factual Consistency. ACL Findings.

[13] Scialom et al. (2021). QuestEval: Summarization Asks for Fact-based Evaluation. EMNLP.

[14] Yanaka et al. (2021). SyGNS: A Systematic Generalization Testbed Based on Natural Language Semantics. ACL Findings.

[15] Chen et al. (2021). Udep2Mono. EACL.

[16] Kupferman and Vardi (2003). Vacuity Detection in Temporal Model Checking. STTT 4(2):224-233.

[17] Zhang et al. (2023). SAC3: Reliable Hallucination Detection in Black-Box Language Models via Semantic-aware Cross-check Consistency. EMNLP Findings.

[18] Lu et al. (2025). FormalAlign: Automated Alignment Evaluation for Autoformalization. ICLR.

</report>

<supplementary_materials>
The run's code, data, and experimental artifacts. This is your ground truth: the report is
complete only if everything here that ran is written up in it, tables and all. Read them —
check that the code matches the described methodology, that each reported number appears in
an output file, and that no executed artifact is missing from the report.

--- Item 1 ---
id: art_d0njuqy2Csj-
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
workspace_path: >-
  /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_1
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 2 ---
id: art_i3cVDxBp-USk
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
workspace_path: >-
  /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 3 ---
id: art_elDZY26Pu6GD
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
workspace_path: >-
  /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_4
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 4 ---
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

--- Item 5 ---
id: art_TaxJRnPcJMuZ
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
workspace_path: >-
  /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_5
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 6 ---
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

--- Item 7 ---
id: art_HepAw8c6Eu7-
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
workspace_path: >-
  /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1
out_expected_files:
- eval.py
- full_eval_out.json
- mini_eval_out.json
- preview_eval_out.json
</supplementary_materials>

<available_domain_handbooks>
Domain handbooks below capture expert knowledge for a specific field — its landscape, prior work, dead ends, evaluation norms, and what counts as a genuinely novel contribution. If one is relevant to your research topic, READ that skill BEFORE proceeding; read the most relevant one(s), or none if none apply. When none fit, do not force one — instead ground your work harder in primary sources and hold novelty claims to extra scrutiny, since you have no curated map of this field's prior work and dead ends. Use it for judging whether the evidence recorded here actually supports what the run concluded, and whether a direction it abandoned was abandoned for a good reason.

- **aii-handbook-auto-computational-linguistics** — Field handbook for computational linguistics as a SCIENCE of language — grammaticality and minimal pairs (BLiMP), surprisal versus reading times, linguistic structure in LMs, annotator disagreement an
- **aii-handbook-auto-mechanistic-interpretability** — Field handbook for mechanistic interpretability of neural networks — circuit discovery, activation and attribution patching, sparse autoencoders, transcoders, attribution graphs, steering vectors, pro
- **aii-handbook-auto-multi-agent-llm-systems** — Field handbook for multi-agent LLM systems (MAS) — orchestration topology, multi-agent debate, mixture-of-agents, verifier and critic agents, inter-agent protocols (MCP/A2A), failure attribution and s
- **aii-handbook-auto-neurosymbolic** — Field handbook for neuro-symbolic AI — text-to-logic autoformalization (NL to FOL), LLM-plus-solver and prover pipelines (Prolog, ASP, SMT), probabilistic-differentiable NeSy (DeepProbLog, Scallop), r
</available_domain_handbooks>

<previous_review>
Your review from the previous iteration. Check which critiques the newest section
addressed. Do NOT re-raise critiques that have been adequately fixed. Only re-raise if the
fix is insufficient.

The previous review is BLOCKING: the paper must not ship as it stands. Every MUST-FIX item below is a requirement for this iteration, not a suggestion — an iteration that leaves one unaddressed does not publish.

- [MAJOR MUST-FIX] (evidence) The report's description of dataset E's panel contradicts the dataset card. The report says the 173-item calibration 'shows that the panel agrees with expert-corrected labels on both faithful and unfaithful items'. The dataset card (gen_art_dataset_1/dataset_card.md, headline facts 2–3, §4) says something else. The panel accepts only 0.613 of expert-CORRECTED formulas and reaches about 0.727 majority accuracy on real errors. It judged 440/535 (0.822) of MALLS gold and 112/148 CTRL references unfaithful, against 36–46% for expert audits. The card warns that 'ERROR is over-called'. The report also says labels come from 'z3 equivalence to audited gold', but 3,891 of 8,507 rows are tier C (no trusted reference, panel-only) and only 1,044 are tier A.
  Action: Replace the sentence with the card's numbers: acceptance 0.613 on expert-corrected, 0.727 on real errors, 0.822 MALLS-gold rejection vs 36–46% for experts, and tier counts A 1,044 / B 2,157 / C 3,891 / none 276 / UNPARSEABLE 1,086. Add the §4 gold-audit table and state that tier-A-only confirmation is mandatory in iteration 2. Mark it as a correction in place.
- [MAJOR MUST-FIX] (rigor) The iteration's comparative conclusion is not supported by a head-to-head test. §1.5 ranks c_score 0.866 (n=546), S4 0.817 (n=524), judge 0.777 (n=524) and FOL-Triage 0.759 (n=477), but the four figures come from three different label vectors. Exp A has 278 CORRECT/199 ERROR on 753 track-L items, exp C 297/249 on 867, and exp D 294/230 on 796; only 588 ids are shared, and 16 GRAN items are CORRECT in D but UNCERTAIN in A and C. The pre-registered rule requires a paired Δ vs the disguised judge with a CI excluding 0, and that was never computed. My paired sentence-clustered bootstrap on the 389 common, label-consistent items (160 errors, 151 sentences) gives c_score 0.842 vs judge 0.785, Δ +0.057 [−0.022, 0.137], not significant, and fused 0.767, Δ −0.020 [−0.111, 0.074]. Files: review_report/audit/paired_boot.json and join_audit.json.
  Action: Add a 'Common-item comparison' table with every candidate, the judge and S4 on the shared label-consistent ids, using paired bootstrap Δs and exp D's data/folds.json. State that under the pre-registered rule c_score fails both the Δ-vs-judge criterion on shared items and the rewrite-FA ≤10% gate (RENAME FA 96%). FOL-Triage fails Δ-vs-judge and rewrite FA. So the iteration-1 verdict is 'no candidate passes; judge is the incumbent'.
- [MAJOR MUST-FIX] (evidence) The adjudicated screen labels already exist and reverse the ranking, but the report defers them to iteration 2. Dataset E (this iteration) wrote screen_adjudicated_labels.json keyed by the same item_id. Re-scoring with it (review_report/audit/rescore_adjudicated.json) gives, on tier A+B, track L, n=304 with 170 errors: fused 0.872, l2_bow 0.817, c_score 0.776, judge_cheap_disg 0.771, rt_nli_min 0.750, sc5 0.699. On all tiers (n=504) the order is fused 0.868, c_score 0.829, judge 0.815. The consensus metric's lead disappears once labels no longer come from the same align() that c_score uses. This is exactly the shared-aligner confound exp C's README flags, which the report mentions only for the 'misalign' probe. The panel's known strictness (above) means this re-score also needs caveats, but it cannot simply be left out.
  Action: Add a subsection 'Re-score under dataset-E adjudicated screen labels'. Include tier A+B, tier A only and all-tier tables with paired CIs, and state that the iteration-1 ranking is label-dependent. In exp C's section, state that c_score and the solver labeller share align(), and report the vocab-clean control (c_score 0.852 [0.765, 0.929] vs SC 0.714, 82 errors) and the partial Spearman of 0.51.
- [MAJOR MUST-FIX] (evidence) The report's statements about the screen audit and ADD+DROP labels contradict the audit itself. It says a 1,173-item screen audit 'confirms the label assignment', and that 58.8% of track-L ERRORs are ADD+DROP and 'likely CORRECT under a looser equivalence definition'. The dataset card §11 shows the panel disagrees with the auto label on 14/48 auto-CORRECT and 14/74 auto-ERROR items, splits 76 FAITHFUL / 70 UNFAITHFUL on VOCAB_GRAN, and calls 178/220 COMPOUND items unfaithful. Joining the adjudicated labels to exp D's track L gives 58 CORRECT→ERROR and only 1 ERROR→CORRECT (12 CONTESTED); exp C gives 62 and 1. Label noise runs mainly the opposite way from what the report asserts: vocabulary-aligned 'CORRECT' items are often unfaithful.
  Action: Replace both claims with the audit's actual cross-tab (auto label × panel majority) and the label-transition counts. Flag the 'VOCAB = CORRECT' convention used by all three experiments as the larger label risk. Keep the original sentence struck through with a correction note.
- [MAJOR MUST-FIX] (evidence) The report's claim that the frontier judge 'adds nothing significant' contradicts exp D. The report cites +0.024 [−0.075, 0.111], a row of the paired_vs_judge_cheap_disg table that does not compare like with like. analysis.json['paired_strong_subset'] and exp D's README ('The frontier judge beats the cheap judge on the same items') give strong_orig − cheap_orig = +0.077 [0.006, 0.154], DeLong p=0.015, on the 200-item L subset (68 errors). On H the strong subset gives +0.115 (p=0.003) and +0.148 vs cheap_disg (p=0.003), and H_curator_view AUROC is 0.915. The report also gives the subset as n=291; it is 200 L items (plus 96 H). The gap vanishes under disguise, and the frontier judge costs $0.0029 per call, above the $0.002 gate. Those are the facts the record needs.
  Action: Replace the paragraph with the same-item paired results for both tracks and both conditions, correct n to 200, and note that the frontier judge fails the cost gate. The user asked whether a large judge 'earns its cost', so state that it adds discrimination on original text but not under disguise.
- [MAJOR MUST-FIX] (scope) Candidate B is a dead end the report never mentions. gen_strat_1 and gen_plan_experiment_2 planned 'verbalise-and-entail' B1 (template, non-repairing English with bidirectional DeBERTa NLI) and B2 (z3-built finite worlds separating the candidate from its typed mutants, judged TRUE/FALSE/UNDETERMINED from text only, with UNDETERMINED pre-registered as the dropped-condition signal). gen_art_experiment_2 contains only an empty .aii folder. The report lists B among the candidates, then silently substitutes exp D's LLM-verbaliser round-trip baseline, which is a different method. B2 was the one candidate aimed at dropped conditions in long sentences, the user's priority.
  Action: Add '1.x Candidate B: planned, not executed'. Summarise the B1/B2 plan and give the reason it did not run (check the run logs for a slot failure, budget or time). State that the round-trip rows in exp D are an LLM-verbaliser baseline, not B1. Record in 'What remains' whether B is dropped or carried to iteration 2.
- [MAJOR MUST-FIX] (evidence) Tables on disk are missing from the report. From exp D (results/summary.md): the H_primary (n=177) and H_curator_view (n=199) AUROC tables for all 27 metrics; L_exclude_subst_only (judge 0.760, rt_nli 0.671); L_unparseable_as_error, where parse_fail is 0.598, the only view in which the user's parse-rate baseline has meaning; L_borderline_to_uncertain and L_pessimistic label-robustness views; the full invariance table with base→rewrite FA and REPRINT; the paired Δ-vs-judge table with DeLong p; the H complexity table (≥20 words, ≥3 conditions cells exist on H); coverage per metric; and cost per component. From exp A: secondary sets ERROR∪COMPOUND and minus-ADD+DROP (fused 0.731 < L3 0.776 once artefacts are removed); binary-layer TPR/FPR/precision@prevalence; the L3 HREF field gate (force 0.69 excluded); fusion coefficients; test-retest (0.917 exact JSON); qwen3-30b second-model row; track-H same-text paired AUROC. From exp C: lenient (0.882), vocab-strict (0.875), track H (0.832), the multi-family secondary sample (n=1,686, 0.825, every family 0.81–0.85), cross-fitted [c_score, sc5] +0.147, cluster-entropy and predset Δs, precision at 10%/25% prevalence, and the RENAME breakdown (pred-only 84%, const-only 100%, flip 77%, base FA 19%).
  Action: Transcribe each of these tables into the relevant experiment subsection with its source file path (results/summary.md, results/RESULTS.md, results/summary.json). Where space is a concern, keep them in an 'Iteration 1 supplementary tables' block. The paper step can only publish what is here.
- [MAJOR MUST-FIX] (scope) The report covers only part of the user's request. (a) The long, heavily conditioned stratum the user said 'matters most' is untestable on the screen (93% of items are under 12 words; 0 errors with ≥3 conditions) and no metric was run on dataset E. The report says this but draws iteration-1 conclusions as if they generalise. (b) Error-type identification is reported only for the judge (0–27%). Exp A's readout (P(code ∈ true ops | fired) = 0.326, L1 hit 0.857 on 7) and exp C's medoid-repair operator match (81% vs 46% chance; coarse class 92% vs 78%) are omitted, although they are the only positive evidence on 'which kind of error'. (c) System-level correlation is given only across 3 systems. Exp C's 9-system Spearman of 0.87 is omitted. (d) Dataset E's correct-but-not-equivalent rates (0.16–0.26 per stratum, 0.07–0.43 per system) and gold-error rates, which the user explicitly asked to be estimated, are omitted. (e) The deliverable 'reusable Python functions with a precise statement of what each measures' is not listed. The function names exist in the artifacts (src/fol_triage.py: fol_lint, content_accounting, role_accounting, role_questionnaire, l3_compare; src/consensus.py: score_candidate, sc_scores).
  Action: Add a 'Coverage against the request' table: requirement, where it is answered (section/file), status. Add the error-typing results of exps A and C, the 9-system correlation, dataset E's §4–5 tables, and a function inventory with a one-line definition for each.
- [MAJOR MUST-FIX] (clarity) The reasoning behind the candidates is not recorded. The report opens at the iteration-1 screen with no account of the three pre-loop hypothesis/review rounds that produced FOL-Triage. It leaves out the iter-3 probe evidence (L1 flagged 27% of real errors at 1.7% FA on 99 curated pairs; bag-of-words paired AUROC 0.59 failed the gate, motivating L3). It also leaves out the reviewer's objections: about 10/24 ADD/DROP census rows are conventions; COMPOUND is a depth-2 search failure; the ⊕/→ precedence bug had to be fixed; and prior art for typed repair and guard smells (Vehlken/Zeume et al., KR 2026, arXiv 2602.19673). Without these, the paper step cannot explain why L1 was expected to work and why its failure on LLM outputs matters.
  Action: Add a short 'Iteration 0 / how we got here' block. Cover the hypothesis claim and probe numbers, the review score and objections, how the strategy answered each objection (the shared screen, the ⊕ fix, the decision rule including 'judge wins if nothing beats it and AUROC ≥ .75'), and why candidates A–D and dataset E were chosen.
- [MINOR] (rigor) Some invariance claims are mislabelled or overclaimed. The FOL-Triage row's 'ALL flip 0.013' has no source: exp A reports no ALL aggregate, and 0.013 is its RENAME flip. FOL-Triage and the judges were evaluated on different rewrite sets (exp A: 150 items, 40 contrapositive; exp D: 270 items, 39 contrapositive). The claim that FOL-Triage 'has the lowest flip rate of any metric tested' is false: L1, parse_fail and pilot_arity are 0.0, and c_score is 0 on all z3-equivalent rewrites. The summary table puts c_score's FA (96%) in the flip-rate column; its RENAME flip is 77%.
  Action: Correct the cells, name each rewrite set, and either run FOL-Triage on exp D's data/invariance_items.json or state that the comparison is across different rewrite samples.
- [MINOR] (rigor) The report says the disguised judge is 'more sensitive … suggesting nonce disguise forces the model to read more carefully', but it compares recall at thresholds with very different false-alarm rates. judge_cheap_disg has FA 0.229 vs 0.059 for orig on H_curator_view, and 0.129 vs 0.034 on L. Higher recall at a looser operating point is not better reading. Separately, the statement that 'z3 answerer is significantly more accurate' is tautological, because the LLM is scored against z3's exact answers.
  Action: Report recall at matched FA (or per-type AUROC), and delete the 'reads more carefully' interpretation unless it survives. Rephrase the z3 statement as 'the LLM reproduces z3's exact formula reading on 57.6% (L) / 36.4% (H) of argument slots'.
- [MINOR] (rigor) 'No contamination was detected for any LLM-based metric' is stated without power. The DiD CIs are about ±0.13 wide (e.g. flash-lite −0.042 [−0.170, 0.094]), so a contamination effect of 0.1 AUROC cannot be excluded. The report also omits that gpt-4.1-nano loses significantly under disguise on track H (−0.114 [−0.207, −0.032]) and H_curator (−0.102 [−0.176, −0.033]).
  Action: State the minimum detectable DiD and list the significant single-track disguise drops, with the artifact's interpretation (lost lexical meaning vs memorisation).
- [MINOR] (novelty) The report's one positive, non-obvious claim (cross-family consensus beats sampling self-consistency by +0.14) is not compared with its nearest published neighbours. SAC3 (Zhang et al., EMNLP Findings 2023, arXiv 2311.01740) already shows cross-model consistency outperforms self-consistency for hallucination detection. Li et al. (NeurIPS 2024) use symbolic equivalence across samples for autoformalization. FormalAlign (ICLR 2025) is a gold-free alignment scorer for autoformalization that is neither cited nor compared. The report needs to state what this run adds beyond them: z3-modulo-vocabulary equivalence on NL→FOL, the typed medoid repair, and the blind-spot analysis.
  Action: Add a two-line nearest-neighbour note under exp C naming SAC3, Li et al. 2024 and FormalAlign, and stating what is new here. Treat 'consensus > SC' as confirming SAC3, not as a new finding.
- [MINOR] (clarity) Bookkeeping inconsistencies. The Framing says the screen has 796 items and that track H's 294 items include 57 errors. 796/294 are exp D's counts; 57 is exp A's ERROR+UNCERTAIN positives (exp D has 35 ERROR, exp C 35). The ~42% gold-error rate is cited to [3] in the Framing and to [4] in Related Work, while the dataset card cites 2606.02837 at about 36–39%. The dataset spend of $9.83 exceeded its $9.50 hard cap. The 11 judge JSON failures that are flagged rather than dropped (0.777 vs 0.785) are not mentioned.
  Action: Give per-experiment n and label sha in one table, fix the citation, record the budget overshoot, and note how the judge JSON failures were handled.
</previous_review>

<task>
Audit this research record. It is an internal report, not a paper: chronological, one
section per iteration, complete. Judge it on completeness, traceability and what it says
was learned — never on framing, section order or polish. When it claims a positive result,
novelty is evidence, not framing: check it against the nearest published neighbour (STEP 5),
not against how well the paper will read.

STEP 1 — READ THE REPORT: Read it carefully. Note what each iteration claims it did, found
and concluded.

STEP 2 — WALK THE ARTIFACTS: Go through the supplementary materials one artifact at a time
and find where the report reports it. Open the output files. Every executed artifact must
appear, and every table in those files must be in the report with its actual numbers. List
the misses; each one is a major issue.

STEP 3 — TRACE THE NUMBERS: For each number, table and claim in the report, find the
artifact it came from, and RECOMPUTE the headline number(s) yourself from that artifact's
own tables or result files rather than taking the report's figure on trust. Report any
mismatch as a finding, even when the underlying artifact is real. Where an artifact does
not let you recompute a number — the raw output is missing, or the computation cannot be
reproduced from what is there — say so and treat that claim as unverified rather than
accepted. An [ARTIFACT:id] marker or a named output file makes a number traceable; nothing
makes it untraceable, which is a major issue even when the number is right.

STEP 4 — CHECK COVERAGE AGAINST THE ORIGINAL REQUEST: The user's original request that
started this run is supplied as a separate message in this turn. Read it and ask what it
actually asked for. Is the run answering THAT, or a question next to it? Set `coverage`
to "full", "partial" or "lost", and when it is not "full", raise a critique naming the
part of the request that went unanswered. Judge against the request, not against the
report's own framing of it — a run that narrows one defensible step per iteration ends up
answering something nobody asked, and each step looked fine on its own.

STEP 5 — CHECK THE RECORD HOLDS TOGETHER:
- Is the REASONING written down at every step — why this strategy, why these artifacts,
  what the last review objected to, what the hypothesis revision concluded and why it moved?
  Outcomes with no account of why they were sought is a major issue.
- Are DEAD ENDS kept and labelled, with the evidence that killed them? A direction the
  artifacts show was tried and the report does not mention is a major issue.
- Is the CHRONOLOGY intact — one section per iteration, in order, earlier sections
  unchanged except where a correction is marked in place? A silently rewritten earlier
  section destroys the record.
- Are the numbers from artifacts that ACTUALLY RAN? Trace each one to an executed output. A
  projected, expected, illustrative or placeholder number presented as a result means
  `results_reported` is false.
- Is what the report concludes PROPORTIONATE to what it recorded? A tiny effect, or an
  effect in the direction everyone already expected, written up as the answer is either
  explained (a bound someone needed, a belief it overturns, a mechanism only visible at
  that size) or it overreaches, and you say so.
- When the report claims a POSITIVE, non-obvious result, name the nearest published result
  that already answers something close to it, and state what this iteration adds beyond
  that neighbour. A positive result earns no credit for novelty in this record until that
  comparison is made — its absence is a critique under `novelty`, not a paper-framing note.
- Does anything the report concludes CONTRADICT its own evidence — a table, a figure, a
  log, an artifact summary? Name the contradiction.
- A conclusion that contradicts the run's own evidence scores soundness 1.
- Set `blocking` by rule: true exactly when the soundness score is 1 or lower OR
  `results_reported` is false; otherwise false.

STEP 6 — WRITE YOUR REVIEW:
For each critique:
1. Categorize: methodology, evidence, novelty, clarity, scope, or rigor
2. Rate severity: major (the record is incomplete or untraceable) or minor (polish)
3. Describe the issue clearly, naming the artifact or section it is about
4. Suggest a concrete action to address it

Focus on the most impactful issues. Provide your review via structured output.
</task><user_data>
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
  "$defs": {
    "Critique": {
      "description": "A single actionable critique from the reviewer.",
      "properties": {
        "category": {
          "description": "Category: 'methodology', 'evidence', 'novelty', 'clarity', 'scope', or 'rigor'",
          "title": "Category",
          "type": "string"
        },
        "severity": {
          "description": "Severity: 'major' or 'minor'",
          "title": "Severity",
          "type": "string"
        },
        "description": {
          "description": "Clear description of the issue",
          "title": "Description",
          "type": "string"
        },
        "suggested_action": {
          "description": "Concrete suggestion for how to address this critique",
          "title": "Suggested Action",
          "type": "string"
        }
      },
      "required": [
        "category",
        "severity",
        "description",
        "suggested_action"
      ],
      "title": "Critique",
      "type": "object"
    },
    "DimensionScore": {
      "description": "Score for a single review dimension with improvement suggestions.",
      "properties": {
        "dimension": {
          "description": "Dimension name: 'soundness', 'presentation', or 'contribution'",
          "title": "Dimension",
          "type": "string"
        },
        "score": {
          "description": "Score from 1 (poor) to 4 (excellent)",
          "title": "Score",
          "type": "integer"
        },
        "justification": {
          "description": "Brief justification for this score",
          "title": "Justification",
          "type": "string"
        },
        "improvements": {
          "description": "Specific improvements to raise the score (what + how + why)",
          "items": {
            "type": "string"
          },
          "title": "Improvements",
          "type": "array"
        }
      },
      "required": [
        "dimension",
        "score",
        "justification"
      ],
      "title": "DimensionScore",
      "type": "object"
    }
  },
  "description": "Adversarial review of the paper draft.\n\nID format: review_it{iteration}__{model}",
  "properties": {
    "overall_assessment": {
      "description": "Overall assessment of the paper's quality and readiness",
      "title": "Overall Assessment",
      "type": "string"
    },
    "strengths": {
      "description": "Key strengths of the paper",
      "items": {
        "type": "string"
      },
      "title": "Strengths",
      "type": "array"
    },
    "dimension_scores": {
      "description": "Scores (1-4) for: soundness, presentation, contribution",
      "items": {
        "$ref": "#/$defs/DimensionScore"
      },
      "title": "Dimension Scores",
      "type": "array"
    },
    "critiques": {
      "description": "Actionable critiques \u2014 specific issues with concrete suggestions",
      "items": {
        "$ref": "#/$defs/Critique"
      },
      "title": "Critiques",
      "type": "array"
    },
    "results_reported": {
      "description": "True only when the paper's headline numbers come from an artifact that was EXECUTED \u2014 a run that finished and wrote its output \u2014 AND you RECOMPUTED the headline number(s) yourself from that artifact's own tables or result files rather than accepting the write-up's figure. A mismatch between what you recompute and what is reported is a critique in its own right, even when the artifact is real. False when any headline number is projected, expected, illustrative, a placeholder, produced by a run that errored, was truncated, never ran, or when you could not recompute it \u2014 say so in `overall_assessment` and treat that claim as unverified rather than accepted.",
      "title": "Results Reported",
      "type": "boolean"
    },
    "coverage": {
      "default": "partial",
      "description": "How much of the USER'S ORIGINAL request this paper answers: 'full' \u2014 it answers the request; 'partial' \u2014 it answers a recognisable piece of it; 'lost' \u2014 the paper answers a different question than the one asked.",
      "enum": [
        "full",
        "partial",
        "lost"
      ],
      "title": "Coverage",
      "type": "string"
    },
    "blocking": {
      "description": "True when this paper must not ship as it stands. It is DERIVED, not judged: true exactly when the soundness dimension score is 1 or lower OR results_reported is false; otherwise false. A headline claim that contradicts the run's own evidence scores soundness 1. A value that disagrees with this rule is sent back.",
      "title": "Blocking",
      "type": "boolean"
    },
    "score": {
      "description": "Overall quality score from 1 (very strong reject) to 10 (award quality)",
      "title": "Score",
      "type": "integer"
    },
    "confidence": {
      "default": 3,
      "description": "Confidence in assessment from 1 (educated guess) to 5 (absolutely certain)",
      "title": "Confidence",
      "type": "integer"
    }
  },
  "required": [
    "overall_assessment",
    "strengths",
    "critiques",
    "results_reported",
    "blocking",
    "score"
  ],
  "title": "ReviewerFeedback",
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
