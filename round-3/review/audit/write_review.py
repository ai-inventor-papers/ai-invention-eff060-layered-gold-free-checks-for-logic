import json
C=[]
def c(cat,sev,d,a): C.append({"category":cat,"severity":sev,"description":d,"suggested_action":a})

c("rigor","major",
"§3.4 (T3/T5 PERTURB) draws conclusions its own artifact contradicts (gen_art_experiment_8).\n"
"(a) MEANING_RENAME is misread. The dataset-3 card (dataset_card.md l.260) defines it as an ERROR mutant: 'swaps a whole predicate for a non-synonymous donor predicate'. The report calls it 'the false-alarm diagnostic … a meaning-preserving predicate renaming' and says c_align separates it 'in the wrong direction: renames look like errors'. The reverse holds. c_align's 0.872 is correct detection of a real error. c_nf's 0.499 means the name-free matcher is BLIND to a real error class, not 'completely invariant'. rt_nli 0.930 is also correct detection. '76%' is the RENAME_NONCE control FA, a different row.\n"
"(b) The consensus per-operator 'sensitivity profile' carries no operator information. My audit (audit/perturb_c_align_constant.py/.json on results/perturb_scores.jsonl) finds that 94–100% of mutants of EVERY operator score c_align = 1. So the within-base AUROC is fixed by how often the unmutated base is peer-endorsed: 26.8% of controls score c = 1, which predicts AUROC 0.866, exactly the reported all-operator value. Primary-threshold recall is 0.72–0.765 for every operator (tables.md T8). So 'most sensitive to SWAP (0.882) and NEG', 'least sensitive to DROP' and 'polarity-symmetric' are by-construction artefacts, not findings.\n"
"(c) Five of the ten judge_cheap_disg cells in the per-operator table do not match results/perturb_sensitivity.csv (E_bases, ALL):\n"
"- DROP: report 0.728, file 0.589 (0.728 is the BIND-UP row);\n"
"- ADD: report 0.683, file 0.695;\n"
"- SWAP: report 0.529, file 0.566;\n"
"- BIND: report 0.672, file 0.731;\n"
"- MEANING_RENAME: report 0.600, file 0.617.\n"
"(d) 'rt_nli_min' is actually rt_nli_min_local (local verbaliser).\n"
"(e) The report omits the best PERTURB metrics: p_peer_text (within-base 0.948; 0.86–0.996 per operator) and L3/p_text (0.90–0.96 on NEG/REV/RESTR). It also omits that the 1,946 R_COMP-base rows got NO consensus score (T11: no_peers_yet), so '300 bases scored with all metrics' is false: consensus covers the 200 E bases only.",
"Rewrite §3.4 from results/tables.md T7–T12 with each table's path:\n"
"1. Relabel MEANING_RENAME as an error operator and reverse the interpretation.\n"
"2. State plainly that consensus per-operator AUROC equals a base-endorsement rate: any edit to an endorsed base scores c = 1. Cite this reviewer's audit and drop the operator-ranking and polarity sentences.\n"
"3. Replace the judge cells with the CSV values.\n"
"4. Add the p_peer_text, p_text, l3_z3 and S4_local rows.\n"
"5. Add the T11 coverage table (3,419/5,402 rows scored by consensus).\n"
"6. Rename rt_nli_min to rt_nli_min_local.")

c("rigor","major",
"T2 (§3.3, §3.6 item 3, 'What we have learned') is recorded as CONFIRMED. The report's own §3.1 criterion says success requires the within-template win 'under both SIG … and FREE' conditions. FREE is NOT_TESTABLE (34 CORRECT tier-A rows; results/tables.md 'FREE'). By the stated rule, T2 is not confirmed.\n"
"SIG gives every translator a signature block, i.e. a controlled vocabulary. The user's operating condition excludes that ('no ontology or controlled vocabulary') and puts 'ontology vocabulary injected into prompts' out of scope. So 0.954 is measured in an excluded regime. In the in-scope FREE condition, consensus falls to 0.804 (c_align) vs judge 0.581 on 34 CORRECT rows. The report omits that number, and the omission hides the vocabulary-divergence cost.\n"
"The +0.367 'largest effect' is taken against a handicapped bar. On templated sentences that cannot be memorised, disguise alone costs the cheap judge 0.085 [0.034, 0.132] (contamination negative-control table). The comparison with the original-text judge is +0.278 [0.239, 0.319], and the report does not give it. On the 60 frontier rows, c_sig 0.956 vs frontier-orig 0.932, and [frontier + c_sig] over frontier is +0.088 [0.019, 0.172]; both are omitted.\n"
"'The consensus metric does not depend on understanding predicate names and is unaffected' contradicts the report's own rename table: c_score_sig FA is 1.000 under nonce renaming.\n"
"Deviation D1 (Sonnet lexicon and reference audits NOT run; references rest on construction plus z3 unit tests) and D2 (221 < 250 sentences, 75 dropped for fluency) are not recorded.\n"
"I recomputed the headline from results/analysis_rows_SIG.jsonl: 0.9543 vs 0.5872 within-template (n = 1,904), e = 0.000, d = 0.260. All match.",
"1. Change T2's verdict to 'SIG PASS; FREE NOT_TESTABLE → T2 not confirmed per §3.1'.\n"
"2. State that SIG is a controlled-vocabulary regime the user excluded.\n"
"3. Add the SIG-vs-FREE table (0.952 → 0.804) and the Δ vs original judge (+0.278).\n"
"4. Add the frontier-subsample table and the nested frontier + c_sig row.\n"
"5. Add the per-slot and per-template label tables and the deviations list (D1–D13) from results/deviations.json.\n"
"6. Delete 'unaffected by predicate names'.\n"
"7. Remove T2 from the 'What we have learned' headline, or demote it to 'signature-given condition only'.")

c("evidence","major",
"§3.5 (T4, gen_art_evaluation_2) replaces the PRE-REGISTERED mechanism tests with different ones and hides the adverse results.\n"
"- M1. The pre-registration (upd_hypo; prereg_mech.json) is 'error endorsement e falls with n_conditions': INCONCLUSIVE, partial slope −0.04 [−0.53, 0.45]. The report instead defines M1 as 'more distinct classes among errors' and says it was 'not formally tested'. That is false: the artifact's SCATTER test is CONFIRMED (SI_err 0.159 vs SI_cor 0.760, ratio 4.45; SI_err falls with conditions).\n"
"- M2. Pre-registered as 'd rises with words': CONFIRMED but NON-SPECIFIC, because the shuffled-label placebo still gives +1.75 [1.04, 2.45]. The report recasts M2 as 'e low, d moderate → CONFIRMED'. That is the bookkeeping identity AUROC_b = 1 − (e + d)/2, which the artifact itself says is not a result. d = 0.537 means binary majority consensus fails on most CORRECT rows ('d, not e, is the blind spot').\n"
"- Omitted: NET Δ(e + d), words T3 − T1 +0.356 [0.198, 0.493], which shows binary consensus DEGRADES with length. This is the direct answer to the user's long-sentence priority, and it contradicts §3.5's 'the consensus does not degrade with complexity'. Also omitted: graded vs binary +0.114 [0.091, 0.140]; aligner-free c_score_exact 0.748; VOCAB_EXACT 0.929; eqmv non-transitivity 15.8%; LOFO (no single family carries the effect); the cross-fitted best 3-family pool at 0.785; k95 by words tercile 2/3/5; the k = 7 tercile AUROCs 0.777/0.721/0.726; M3-local INCONCLUSIVE.\n"
"- The M4 cost column is mislabelled. tables/m4_auroc_k_cost.csv gives $0.000315/0.000946/0.001576/0.002206 PER SENTENCE for k = 1/3/5/7. The report gives $0.000024/0.000073/0.000121/0.000170, about 13× lower. It then compares '$0.000073 per sentence' with the judge's $0.000049 per call and concludes that consensus costs are 'negligible'. The artifact's own figure for the best 3-pool is $0.0020/sentence.",
"1. Rewrite §3.5 from evaluation_2 README 'Headline results' with the pre-registered M1/M2/M3-local/M4 definitions and verdicts (M2 marked NON-SPECIFIC).\n"
"2. Add the SCATTER, NET, graded-vs-binary, c_score_exact, VOCAB_EXACT, LOFO, fixed-pool and per-tercile k95 rows, each with its tables/*.csv path.\n"
"3. Correct the cost column from m4_auroc_k_cost.csv and state the unit (per sentence vs per candidate).\n"
"4. Delete 'consensus does not degrade with complexity' and replace it with the NET result.")

c("evidence","major",
"The iteration-3 dead ends and the negative parts of gen_art_experiment_8 are missing.\n"
"- Part A. The pre-registered rename-invariant selection (results/prereg_hyb.json, selection.json) FAILED: 'NEITHER ELIGIBLE: no rename-invariant consensus exists here'. HYB rename FA was 0.841/0.700 and NF 0.686/0.485 on PERTURB RENAME_SYN/NONCE at the screen thresholds. The revised hypothesis made this a requirement of the claim ('Rename invariance becomes a requirement … target RENAME FA ≤0.10'). The report never says the pre-registered test failed. Instead it quotes E-threshold FAs (c_nf 0.132, c_hyb 0.216) that read as successes.\n"
"- The over-alignment audit is absent (T4: HYB's extra agreements are label-discordant 0.388 vs 0.127 for ALIGN).\n"
"- So are the E-side HYB table (T2/T3: HYB − ALIGN −0.004 n.s.; HYB − NF +0.052) and the screen-probe table (T5).\n"
"- Part C, error-type identification, is absent (T12). Peer-medoid typing 0.328 [0.277, 0.387] vs majority 0.177, oracle 0.802, flash-lite judge 0.326, local judge 0.098. This is the run's only controlled answer to 'which kind of error'.\n"
"- Part D, src/consensus_lib.py (reusable functions, 31 tests), is absent.\n"
"- The nf4 local-judge deviation is absent.\n"
"- Spend is misreported: the artifact spent $0.35 on OpenRouter, but §3.6 calls T3+T5 'CPU-only, $0.00'.",
"1. Add '3.x Rename-invariant consensus: pre-registered selection FAILED (dead end)' with tables.md T1, T3 and T4 and prereg_hyb.json.\n"
"2. Add the Part C typing table T12, with the statement that no metric identifies error type much better than the judge.\n"
"3. List the consensus_lib.py functions.\n"
"4. Correct the spend.")

c("novelty","major",
"Executed research artifact art_VIF75I5R6f0v (gen_art_research_1) appears nowhere in the report, and the positive claims have no nearest-neighbour comparison. The artifact found that the METHOD is not new:\n"
"- ARc (arXiv 2511.09008; I confirmed it exists) scores each translation by the share of k LLM translations that entail it, which is the same functional form as c_score. It works over a fixed schema and is validated on downstream QA.\n"
"- NoTB (2608.21962) does cross-family formal-equivalence consensus for RTL.\n"
"- GenV (2609.11085; I confirmed it exists, AUROC 0.961) reports a single-model SC K = 5 baseline of 0.863 on NL→FOL. It also shows the metric-vs-judge ranking REVERSING when labels switch from Z3-reference to panel intent. That bears directly on this run's own R_SOLVER → R_PANEL shift (c_score 0.849 → 0.779).\n"
"- SCP-NL2TL (2608.05439) is the closest meta-evaluation design.\n"
"The artifact rates C1, C3, C4 and C5 NEEDS-QUALIFIER; for example, C5 '3–4 cross-family models' is already recommended by LLMs-as-Jury. The report's Related Work cites none of these. 'What we have learned' still presents consensus and the k = 3 finding as unqualified.\n"
"The iteration-3 sections also cite placeholder IDs that match no artifact: [ARTIFACT:art_T1_API_bar], art_R_COMP, art_PERTURB_scoring, art_evaluation_2. The real IDs are art_7GxreYjATkC5, art_cxnoDYQNFolW, art_YYD-HDzfQfEj and art_FWy8D4_y9GBn. §2.6 (exp 6) and §2.7 (dataset 2) carry no marker.",
"1. Add '3.x Prior-art positioning [ARTIFACT:art_VIF75I5R6f0v]' with the scoop rule, the closest-neighbour table and the claim verdicts (C1–C5 with qualifiers).\n"
"2. Under each positive claim, state what this run adds beyond ARc/NoTB/GenV: a per-candidate NL→FOL faithfulness meta-evaluation vs an API judge, nested over the baseline stack, and a measured rename FA.\n"
"3. Replace the placeholder artifact IDs with the real ones, and add markers to §2.6/§2.7 (iter-2 gen_art_experiment_6 and gen_art_dataset_2 workspace paths).")

c("evidence","major",
"T1 (§3.2) is accurate where it reports. I recomputed from results/per_item_T1.jsonl (audit/recompute_headlines.py): n 2,686/1,822, c_score_align strat 0.7415, flash-lite disguised 0.6425, Δ 0.099 [0.050, 0.145]. But it leaves out cells that change the reading.\n"
"(i) On L25 (≥25 words, ≥3 conditions, the user's priority stratum), c_score_align − flash-lite is +0.069 [−0.020, 0.148], n.s. My recompute gives +0.069 [−0.020, 0.146]. It is also n.s. vs nano-orig (+0.043) and vs the local judge (+0.049). Only p_peer_text is significant there (+0.113).\n"
"(ii) c_score_align alone does not beat S4_full: +0.006 [−0.031, 0.042]. Only the nested addition is significant.\n"
"(iii) At n_conditions ≤1, the judge leads (0.822 vs 0.794).\n"
"(iv) The stacked-GEE interaction for M3 is +0.274 [0.190, 0.359], CI > 0. That disagrees with the bootstrap slope difference behind 'DISCONFIRMED', and the report gives only the latter.\n"
"(v) Missing rows: S4_API 0.761, S4_full_noJudge 0.734, PT_refit − S4_full +0.043; the COVERAGE (unparseable = ERROR), CONTESTED_AS_* and ALL_TIERS sensitivity rows (vs the local judge on ALL_TIERS: +0.019 n.s.); p_text on CTRL −0.252.\n"
"(vi) Deviations D1–D9 are not recorded. They include D3 (108 R_AB rows get a fallback 0.5) and D5 (the matched-FA thresholds are unattainable for quantised scores; c_score_align's threshold is 1.0).\n"
"(vii) Contamination is misread: a DiD of +0.105 [0.006, 0.201] that excludes zero is not discounted by being 'below MDE'. MDE is a power statement.\n"
"(viii) The judge_strong_orig recall per group is computed on the 284-row frame only, yet it is printed beside n = 1,148, etc.\n"
"(ix) Spend is omitted: $2.395 (api_cost_ledger.json).",
"Paste tables_T1.md sections (a) through (i) in full, including the per-stratum Δ table with L25/L20 pooled rows and the sensitivity rows, plus deviations.json. Then:\n"
"1. State the L25 null and 'c alone ≈ S4_full' in §3.6.\n"
"2. Report both M3 specifications.\n"
"3. Reword the contamination sentence to 'marginal evidence of contamination for flash-lite (CI excludes 0)'.\n"
"4. Mark the frontier recall column 'frame n = 284'.\n"
"5. Give the T1 spend.")

c("methodology","major",
"Dataset E is called 'held-out' throughout iteration 3, but it is not held-out for the iteration-3 claims. evaluation_2's README says 'E is development data, not pristine held-out: it was scored in iteration 2'. The object c_score_align was chosen as the lead AFTER iteration 2 saw its E results: upd_hypo narrowed PT → c_score_align because c_score_align did better on E tier A (0.860 vs 0.818). Exp 8 Part A also selected HYB 'on screen+E as development data'.\n"
"The scores were frozen in exp 5, so thresholds were not tuned. Metric selection was, and 'T1 CONFIRMED on held-out E' overstates this. The only data that no earlier decision touched is R_COMP, and its only testable condition is SIG.",
"Label the iteration-3 E results 'E (development data; metric chosen after iteration-2 E results)'. State which decisions used E. Name a genuinely untouched confirmation set, such as R_COMP FREE with panel labels or a non-FOLIO/MALLS source, as the pending confirmation in 'What remains'.")

c("evidence","major",
"Most of the previous round's blocking MUST-FIX items are still unaddressed, and the corrected numbers already exist on disk in gen_art_evaluation_2/tables (hypothesis_verdicts.csv, coverage_vs_request.csv, label_facts.csv, corrections.csv, b2_dead_end.csv, radj_gate.csv, regimes_R_PANEL.csv, exp6_*.csv).\n"
"(1) Iteration-1 text is uncorrected:\n"
"- 'panel agrees with expert-corrected labels on both faithful and unfaithful items';\n"
"- 'screen audit confirms the label assignment';\n"
"- '58.8% … likely CORRECT';\n"
"- the frontier '+0.024 … adds nothing significant' in §1.4 and §1.5 item 2, which contradicts correction C4's +0.077 [0.006, 0.154];\n"
"- Candidate B is still listed as round-trip; B1 was never run;\n"
"- 'ALL flip 0.013', and c_score's 96% FA sits in a flip column.\n"
"(2) §2.3 still says 'common item set (588 items)', names the regimes R_ADJ_* after 'the parallel run', headlines the untestable R_ADJ_A (0.958/0.932), gives '51' flipped items (58/62/55), and omits the rule-FAILS verdict, the per-regime Δ-vs-judge, τ 0.60 and the placebo null.\n"
"(3) §2.5 item 5 still says the frontier advantage is 'reversing' the iteration-1 finding, contradicting C4 two sections earlier.\n"
"(4) §2.2 still says the fusion was fitted on the screen, and §2.5(d) says it was fitted 'under solver labels'. It was actually fitted on AGREE items (screen_fit.json).\n"
"(5) The §2.2 contamination paragraph still reports the screen DiD +0.045 as the E result, with 'No contamination is detected'.\n"
"(6) The PERTURB description (§2.4, §3.4) still lists 12 operators 'including SCOPE, UNGLUE'. The card gives those 0 rows, lists MEANING_RENAME as an operator, and marks QUANT/REV/RESTR as UP-only. The report calls RENAME controls 'z3-equivalent', but they are equivalent only modulo renaming.\n"
"(7) There is no hypothesis-verdict table, coverage table or function inventory.\n"
"(8) §2.6 (exp 6) transcribes 12 pooled AUROCs only. Missing: the GEE length slopes, per-type recall, the contamination DiD table, the CNE shares (0.773/0.721/0.441/0.215), test-retest, and the F-KEY deviations.\n"
"(9) The R_ADJ table gives the gate target as ≥ 0.80. radj_card.md l.20 says balanced accuracy ≥ 0.85 AND each recall ≥ 0.80. It also omits the overall gate BA (Sonnet 0.767, Grok 0.634). 'Judged 43% of expert-corrected originals FAITHFUL' should be 15/37 = 40.5% of expert-REJECTED originals.",
"Apply each item in place with a '[Correction, iter 3: … ; source <file>]' marker, keeping the struck original. Transcribe hypothesis_verdicts.csv, coverage_vs_request.csv, label_facts.csv, function_inventory.csv and regimes_R_PANEL.csv. Paste exp 6 summary.md tables 1–9. This work is transcription, not new computation.")

c("clarity","major",
"§3.1 records what T1–T5 are but not why they were chosen. It omits:\n"
"- the previous review (score 3, blocking, 11 items) and which of its objections this iteration answered;\n"
"- the upd_hypo decision: strands lead/lead/broken/null/null → 'deepen', narrowing from the PT fusion to c_score_align because the fusion added +0.011 n.s. and TEXT < the local judge;\n"
"- the verbatim revised hypothesis and its success criteria, including 'rename invariance becomes a requirement of the claim' and the specific M1–M4 definitions;\n"
"- the five planned artifacts, including the research artifact, and their status;\n"
"- why SIG was introduced (to make the labels aligner-free) and the cost of that choice;\n"
"- the fallbacks used (frontier 300 → 284, disguised frontier blocked by the key-reserve rule).\n"
"Without this, the paper step cannot explain why the object changed or which criteria failed.",
"Open §3.1 with an 8–10 line block drawn from iter_2/upd_hypo/.terminal_claude_agent_struct_out.json and iter_3/gen_strat/gen_strat_1. Add a closing '3.7 Hypothesis verdicts' table with one row per pre-registered clause: T1(a) CONFIRMED; T1(b) CONFIRMED; T1(d) CONFIRMED on the point estimate only; the rename-invariance requirement FAILED; T2 SIG PASS / FREE NOT_TESTABLE; M1 INCONCLUSIVE; M2 CONFIRMED-non-specific; M3 DISCONFIRMED; M4 CONFIRMED; NET degrades.")

c("scope","major",
"Coverage of the user's request is partial.\n"
"(1) 'Long, heavily conditioned sentences matter most'. On E's L25 stratum, consensus does not significantly beat the API judge. Binary consensus degrades with length (NET +0.356), and long sentences need k = 5 peers. R_COMP's positive result exists only with a given signature.\n"
"(2) 'No ontology or controlled vocabulary'. The headline c_score_align relies on a vocabulary aligner: RENAME_NONCE FA 0.765, and the FREE condition is untestable. So the metric is not validated in the stated operating condition.\n"
"(3) 'Which kind of error'. Typing is 0.328 on PERTURB, equal to the flash-lite judge, and at chance on E. The report never states this as a negative answer.\n"
"(4) 'Reusable Python functions with a precise statement of what each measures'. consensus_lib.py, peer_text.py, fol_triage.py, pairwise.py and mechanism.py exist, but no inventory is in the report.\n"
"(5) 'A large-LLM judge only if shown to earn its cost'. The frame shows frontier 0.741 vs c 0.710 vs S4_full 0.745 at 30× cost, but no verdict sentence is written.\n"
"(6) The gold-wrong and correct-but-not-equivalent estimates with their label bias exist (label_facts.csv) but get only one sentence.",
"Add a 'Coverage against the request' table (requirement → section/file → answered/partial/untestable), starting from evaluation_2 tables/coverage_vs_request.csv and updated with T1/T2/T3/T5. Write explicit one-line answers for items (1)–(6). In 'What remains', rank 'R_COMP FREE with labels' and 'a non-FOLIO/MALLS confirmation set' above new metric variants.")

c("rigor","minor",
"The cost statements disagree with one another:\n"
"- the frontier costs 30.2× the consensus in T1 (per item) but 6.07× in R_COMP (per candidate on long sentences, $0.001/candidate);\n"
"- consensus FULL cost $1.21e-4/item is 2.5× the flash-lite judge ($4.9e-5), so 'marginal cost negligible' holds only for the MARGINAL z3 cost ($2.5e-7), with the peer pool assumed already paid;\n"
"- iteration-3 total spend is about $4.33 (T1 $2.395 + T2 $1.58 + exp 8 $0.35), not '$1.58 plus T1'.",
"Add one cost table with units (per item / per sentence / per candidate; FULL vs MARGINAL) per artifact, taken from api_cost_ledger.json, results/tables.md Cost and m4_auroc_k_cost.csv, and state the total iteration spend.")

c("rigor","minor",
"T1 criterion (d) is marked CONFIRMED from a point ratio of 0.957 whose CI [0.887, 1.034] crosses 0.95. On the frame, c_score_align (0.710) trails both the frontier judge (0.741; Δ −0.032 [−0.085, 0.024]) and S4_full (0.745). '96% of the frontier judge's discriminative power' is proportionate only with that caveat. The §3.1 bullet says '≤ 10× cost', but the verdict file says ≤ 10% cost.",
"Write '(d) met on the point estimate; CI includes ratios < 0.95; consensus is below the frontier and S4_full on the frame' and fix the cost wording.")

review={
"overall_assessment":
"Iteration 3 ran four real experiments and a research artifact. The main T1 numbers are faithful: I recomputed from per_item_T1.jsonl that c_score_align stratified AUROC is 0.7415 vs flash-lite disguised 0.6425, Δ 0.099 [0.050, 0.145]. I also recomputed the R_COMP SIG within-template AUROC from analysis_rows_SIG.jsonl: 0.954 vs 0.587, e = 0, d = 0.260. results_reported is therefore true.\n\n"
"The record still does not hold together, and several conclusions contradict the artifacts they cite. Soundness is 1, so the review is blocking.\n"
"(1) The PERTURB section reads MEANING_RENAME, a meaning-CHANGING error mutant, as a meaning-preserving false-alarm diagnostic, and inverts its interpretation. It presents a consensus 'per-operator sensitivity profile' that my audit shows is operator-blind by construction: 94–100% of every operator's mutants score c = 1, and the base-endorsement rate alone predicts the reported 0.866. Five judge cells do not match the CSV.\n"
"(2) T2 is declared CONFIRMED although the report's own criterion needs SIG and FREE, and FREE is NOT_TESTABLE. SIG gives a controlled vocabulary, which the user excluded. The +0.367 is against a disguised bar that disguise itself handicaps by 0.085.\n"
"(3) The T4 mechanism section replaces the pre-registered M1/M2 with other tests, calls a bookkeeping identity 'CONFIRMED', says scatter was 'not formally tested' when it was, omits that binary consensus degrades with length, and understates the per-sentence cost about 13×.\n"
"(4) The pre-registered rename-invariant consensus selection FAILED (NEITHER ELIGIBLE), and that dead end is missing.\n"
"(5) The prior-art artifact is absent. It shows the method's score form already exists (ARc) and that GenV's metric-vs-judge ranking reverses under intent labels.\n"
"(6) T1 omits that consensus is not significant on L25, the user's priority stratum, and that c_score_align alone ties S4_full.\n"
"(7) E is described as held-out although evaluation_2 labels it development data.\n"
"(8) Most of last round's MUST-FIX items (iteration-1 corrections, §2.3 rewrite, coverage/verdict tables, PERTURB description) remain undone, although evaluation_2 produced the corrected tables.\n\n"
"This is progress on bookkeeping: exp 6, B2, R_ADJ and corrections C1–C7 are now recorded. But the new iteration-3 sections repeat the pattern of reporting the favourable half of each artifact.",
"strengths":[
"T1 is faithfully transcribed where it reports. Every number I recomputed from per_item_T1.jsonl matches (n 2,686, strat 0.7415 vs 0.6425, Δ 0.099 [0.050, 0.145]), including the nested S4_full + c_score_align +0.039 [0.021, 0.057] with a permutation null and the VEX control.",
"The report now records the iteration-2 omissions it was asked to add: exp 6 baselines (§2.6), B2 and R_ADJ as labelled dead ends with gate evidence (§2.7), and inline corrections C1–C7 with correct spend.",
"The report states negative results honestly where it gives them: M3 DISCONFIRMED, CTRL showing no consensus advantage, PEER_ENDORSED/MEANING_RENAME-group recall near zero, and FREE NOT_TESTABLE.",
"The underlying artifacts are high quality: pre-registration hashes, independent raw re-derivations, placebo checks, sentence-cluster bootstraps and deviation logs. The fixes needed are mostly transcription and interpretation, not new experiments."],
"dimension_scores":[
{"dimension":"soundness","score":1,"justification":"Several conclusions contradict their own artifacts. MEANING_RENAME is inverted. The per-operator consensus 'sensitivity' is operator-blind by construction. T2 is CONFIRMED despite the report's own SIG+FREE criterion. M1/M2 are recast, and a bookkeeping identity is sold as confirmation. 'Consensus does not degrade with complexity' contradicts NET +0.356. 'Unaffected by predicate names' contradicts FA 1.0. The frontier '+0.024 nothing significant' still stands beside its own correction.",
"improvements":["Fix MEANING_RENAME and the operator-blind reading (audit/perturb_c_align_constant.json).","Downgrade T2 to SIG-only, with the out-of-scope caveat.","Restore the pre-registered M1/M2 and add NET/SCATTER.","Reconcile §1.4/§1.5/§2.5 with correction C4."]},
{"dimension":"presentation","score":2,"justification":"Chronology is kept and corrections are marked inline. But the iteration-3 artifact markers are placeholders, iteration-2 sections still carry mislabelled regimes and counts, units are mixed in the cost statements, and §3.1 gives no reasoning.",
"improvements":["Use the real artifact IDs.","Add the reasoning block and the hypothesis-verdict table.","Give one cost table with units."]},
{"dimension":"contribution","score":2,"justification":"Large executed parts of the run are missing from the record. These include the research artifact, exp 8 Part A (failed selection), Part C (typing), T4's NET/SCATTER/LOFO/fixed-pool results, T1's L25 and sensitivity rows, R_COMP FREE AUROCs and deviations, and last round's coverage, function and verdict tables.",
"improvements":["Transcribe the missing tables with file paths, following the critiques.","Add a coverage-vs-request table and the function inventory."]}],
"critiques":C,
"results_reported":True,
"coverage":"partial",
"blocking":True,
"score":3,
"confidence":4}
json.dump(review,open(str(__import__("pathlib").Path(__file__).resolve().parents[3] / 'round-3/review/.terminal_claude_agent_struct_out.json'),'w'),indent=1,ensure_ascii=False)
print(len(C))
