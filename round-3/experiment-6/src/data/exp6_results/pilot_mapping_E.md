# Pilot metrics on dataset E: adaptation

Dataset E rows are single sentences, so the pilot's 'document' (a set of formulas loaded together) is an artificial group:
(system|variant, source_stratum, int(sha1(sentence_id),16) % B) with B per stratum {'CTRL': 8, 'L20': 8, 'L25': 15, 'EXC': 5} (about 20 sentences per document).
CTRL (FOLIO) rows have no story id in dataset E and use the same bucket rule.

- pilot_joint_conflict: story = the other parseable formulas of the same document; 1 if story ∪ {cand} is UNSAT (z3, 5 s).
- pilot_arity_incons / pilot_shape_incons: arity / argument-kind clashes of cand against the rest of the document.
- pilot_dangling: fraction of cand predicates+constants that appear nowhere else in the document.
- pilot_undeclared: NOT APPLICABLE (dataset E generators output no predicate declarations).
- pilot_rerun_jacc: 1 - predicate-token Jaccard; zero-shot vs few-shot output of the same system for Llama-3.3-70B and Qwen3-235B (the only slots with two prompt variants), otherwise the mean Jaccard with the other LLM slots on the same sentence (cross-system proxy); column rerun_flag says which.
The joint-load conflict metric therefore has a different meaning from the user's pilot (documents are not coherent stories); it is reported as 'adapted'.
