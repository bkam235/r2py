---
id: base.sample
package: base
confidence: tentative
seed: true
created: 2026-09-30
last_review: 2026-09-30
tie_count: 0
---

# base.sample

## Guidance
Translate R `sample` from base to Python. The verified example below uses it inside a statement that may call other functions too.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "cc1eac87", "r_snippet": "list(sample(10), sample(10))", "py_snippet": "res2_list = [random.sample(range(1, 11), 10), random.sample(range(1, 11), 10)]\nr_print_list(res2_list)", "score": 1.0, "script_id": "magrittr__vignette__tradeoffs_chunk9", "n_calls": 1}

## Edit Examples
- {"failure_class": "side_effects", "old_code": "res2_list = [random.sample(range(10), 10), random.sample(range(10), 10)]", "new_code": "res2_list = [random.sample(range(1, 11), 10), random.sample(range(1, 11), 10)]\nr_print_list(res2_list)", "score_delta": 0.5, "script_id": "magrittr__vignette__tradeoffs_chunk9", "r_snippet": "list(sample(10), sample(10))", "functions": ["base::sample"]}
