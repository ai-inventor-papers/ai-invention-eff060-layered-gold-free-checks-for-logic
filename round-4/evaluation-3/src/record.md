# Verified record (T8, iteration 4)

Every number in the tables below is read from a source file by code (`src/t8_part4.py`). Each hypothesis-side literal is also checked to occur verbatim in the iteration-4 hypothesis §0 (`hyp_literal_found`). **Where they disagree, the SOURCE value wins.** E and R_COMP are DEVELOPMENT data, so everything in Parts 1-2 is mechanism/selection evidence, not confirmation. The claims wait for E2 in iteration 5.

## Claim check

64 claims, 60 match, 1 mismatch, 0 NOT_IN_FILES. 3 rows are context-only, with no hypothesis literal.

| table | item | hypothesis | literal in §0 | source | match |
|---|---|---|---|---|---|
| a | M3 bootstrap diff | +0.146 | True | 0.14627685998181889 | True |
| a | M3 stacked-GEE interaction | +0.274 | True | 0.274 | True |
| a | T1(a) exp6 own verdict | CONFIRMED | True | CONFIRMED | True |
| a | T1(e) rename selection outcome | NEITHER ELIGIBLE | True | **Frozen variant: None** -- NEITHER ELIGIBLE: no rename-invariant cons | True |
| b | R_AB strat Δ vs flash-lite disg | +0.099 | True | 0.099 | True |
| b | long strat Δ | +0.116 | True | 0.116 | True |
| b | L25 Δ vs flash-lite disg | +0.069 | True | 0.069 | True |
| b | L25 Δ vs nano orig | +0.043 | True | 0.043 | True |
| b | L25 Δ vs local judge | +0.049 | True | 0.049 | True |
| b | L25 p_peer_text Δ | +0.113 | True | 0.113 | True |
| b | R_AB Δ vs nano orig | +0.089 | True | 0.089 | True |
| b | EXC Δ | +0.197 | True | 0.197 | True |
| b | CTRL Δ | −0.069 | True | -0.069 | True |
| b | R_A L20+EXC Δ | +0.299 | True | 0.29941908034691533 | True |
| b | nested [S4_full+c]-S4_full strat | +0.039 | True | 0.038774976834802466 | True |
| b | frontier ratio | 0.957 | True | 0.9573029948134515 | True |
| c | judge within-base AUROC DROP (E_bases, ALL) | 0.589 | True | 0.5887573964497042 | True |
| c | judge within-base AUROC ADD (E_bases, ALL) | 0.695 | True | 0.6952117863720073 | True |
| c | judge within-base AUROC SWAP (E_bases, ALL) | 0.566 | True | 0.5659340659340658 | True |
| c | judge within-base AUROC BIND (E_bases, ALL) | 0.731 | True | 0.731060606060606 | True |
| c | judge within-base AUROC MEANING_RENAME (E_bases, ALL) | 0.617 | True | 0.6173835125448028 | True |
| c | min share of mutants at c=1 (any operator) | 94 | True | 94.24 | True |
| c | share of NON-RENAME controls at c=1 (n-weighted over CONTROL:* except RENAME_*) | 26.8 | True | 26.819733570159855 | True |
| c | share of ALL controls at c=1 incl. renames (context, no hypothesis literal) | nan | True | 42.8373061760841 | nan |
| c | T11 consensus rows scored ok | 3,419 | True | 3419.0 | True |
| c | T11 R_COMP-base rows no_peers_yet | 1,946 | True | 1946.0 | True |
| c | T12 peer-medoid typing (ALL) | 0.328 | True | 0.328 | True |
| c | T12 majority (ALL) | 0.177 | True | 0.177 | True |
| c | T12 flash-lite (ALL) | 0.326 | True | 0.326 | True |
| c | T12 ORACLE (ALL) | 0.802 | True | 0.802 | True |
| d | over-alignment HYB-extra | 0.388 | True | 0.38764044943820225 | True |
| d | over-alignment ALIGN | 0.127 | True | 0.12695257029253054 | True |
| d | rename FA 0.841 in T1 selection table | 0.841 | True | 0.841 | True |
| d | rename FA 0.700 in T1 selection table | 0.700 | True | 0.7 | True |
| d | rename FA 0.686 in T1 selection table | 0.686 | True | 0.686 | True |
| d | rename FA 0.485 in T1 selection table | 0.485 | True | 0.485 | True |
| d | E paired Δ HYB-ALIGN (R_AB pooled) | −0.004 | True | -0.004 | True |
| d | E paired Δ HYB-NF (R_AB pooled) | +0.052 | True | 0.052 | True |
| e | SIG frontier nested [frontier + c_sig] - frontier | +0.088 | True | 0.08777777777777773 | True |
| e | T2 value 0.954 | 0.954 | True | 0.954 | True |
| e | T2 value +0.367 | +0.367 | True | 0.367 | True |
| e | T2 value +0.278 | +0.278 | True | 0.278 | True |
| e | T2 value 0.085 | 0.085 | True | 0.085 | True |
| e | T2 value 0.587 | 0.587 | True | 0.587 | True |
| e | SIG d (recomputed here, eval-2 functions) | 0.260 | True | 0.25956112852664576 | True |
| g | consensus $/item | $1.21e-4 | True | 0.000121 | True |
| g | flash-lite $/item-call | $4.9e-5 | True | 4.876573058684072e-05 | True |
| g | k-pool $/sentence k=1 | 0.000315 | True | 0.0003152007660473 | True |
| g | k-pool $/sentence k=3 | 0.000946 | True | 0.0009456022981419 | True |
| g | k-pool $/sentence k=5 | 0.001576 | True | 0.0015760038302366 | True |
| g | k-pool $/sentence k=7 | 0.002206 | True | 0.0022064053623312 | True |
| g | exp-7 peer generation $/candidate (plan literal; not in hypothesis) | $0.000996 | False | 0.00011640721628959276 | False |
| g | iteration-3 T1 spend | $2.395 | True | 2.3953603000000236 | True |
| g | iteration-3 T2 spend | $1.58 | True | 1.5809425042499974 | True |
| g | iteration-3 exp 8 spend | $0.35 | True | 0.35242190000000095 | True |
| g | iteration-3 spend total | $4.33 | True | 4.328724704250022 | True |
| j | label fact 0.773 | 0.773 | True | 0.7727 | True |
| j | label fact 0.721 | 0.721 | True | 0.7205 | True |
| j | label fact 0.441 | 0.441 | True | 0.4414 | True |
| j | label fact 0.215 | 0.215 | True | 0.2152 | True |
| j | label fact 0.822 | 0.822 | True | 0.8224 | True |
| j | label fact 0.613 | 0.613 | True | 0.613 | True |
| j | label fact 0.767 | nan | True | 0.7668 | nan |
| j | label fact 0.634 | nan | True | 0.6343 | nan |

### Mismatches and wording corrections (source wins)

- **exp-7 peer generation $/candidate (plan literal; not in hypothesis)**: stated `$0.000996` vs source `0.00011640721628959276` (../../../round-3/experiment-7/src/results/rcomp_candidates.jsonl :: mean cost_usd). The literal is in §0: False.
- **'26.8% of controls score c = 1'** is true only for the NON-RENAME controls. Across all controls, including RENAME_NONCE (100%) and RENAME_SYN (73.9%), the share is 42.8% (audit/perturb_c_align_constant.json).
- **Cost units.** SIG peer generation is $0.000116 per CANDIDATE and $0.00116 per SENTENCE (10 slots). Neither equals the plan's `$0.000996 per candidate`, and that literal does not occur in the hypothesis. `tables/cost_units.csv` gives every cost with an explicit unit column. Iteration-3 spend comes from the workspace `.aii_cost_ledger.jsonl` files: T1 $2.395, T2 $1.581, exp 8 $0.352, total $4.33. `results/costs.jsonl` of exp 7 holds only the judge calls ($1.04), which is why an earlier reading could come out low.

## New numbers from this artifact (for the paper; source files named)

- Part 1, 3-pool (PRIMARY): END_MAJ d 0.415; predicted d_floor 0.402 [0.336, 0.471]; bracket [0.396, 0.415]; R_exact 0.683; no-anchoring oracle floor 0.385 (labelled-denominator 0.345); e_ceiling 0.162 (`results/part1.json` pools.3pool).
- Part 1, 9-family: END_MAJ d 0.537; d_floor_pred 0.532; bracket [0.522, 0.537]; oracle 0.586.
- Part 2: SIG-minus-FREE cross-family exact-agreement drop 0.479 [0.447, 0.513]; share recovered post hoc: ALIGN 0.413, NF 0.184, ALIGN or NF 0.455. Validation of the Part-1 method: calibration error -0.372 [-0.423, -0.323], so NOT validated (the pass bar was |error| <= 0.05).
- Part 3: L25 yield 0.37. Detecting +0.069 at 80% power needs ~326 usable L25 sentences, i.e. ~882 planned.

## Positioning paragraph (TO-BE-CHECKED)

What CSC adds beyond ARc (fixed schema), SIG (external vocabulary) and predicate-list prompting (2509.22338): predicate availability gives +15-20% for TRANSLATION, whereas CSC uses the candidate's predicate list for VERIFICATION. ARc scores the share of k translations that entail a candidate on a FIXED schema, and SIG hands every translator an EXTERNAL signature. CSC instead re-translates with the CANDIDATE's own vocabulary, so the verifier inherits whatever the candidate chose, which is where anchoring can enter. Part 2 shows an external shared vocabulary raises cross-family exact agreement from 0.05 to 0.53. Part 1 shows that, on E, most of the disagreement behind d is with peers labelled ERROR, which no vocabulary can fix without anchoring. **TO-BE-CHECKED** against 2509.22338 and ARc 2511.09008 before it is used in the paper.
