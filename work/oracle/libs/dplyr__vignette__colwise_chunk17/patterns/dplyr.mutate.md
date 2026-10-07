---
id: dplyr.mutate
package: dplyr
confidence: tentative
seed: true
created: 2026-10-07
last_review: 2026-10-07
tie_count: 0
---

# dplyr.mutate

## Guidance
Translate R `mutate` from dplyr to Python. The verified example below comes from another script that used it.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "713c1a9d", "r_snippet": "  mutate(\n    score = score |>\n      recode_values(\n        from = lookup$from,\n        to = lookup$to,\n        unmatched = \"error\"\n      )\n  )", "py_snippet": "    mapping = dict(zip(lookup['from'], lookup['to']))\n    \n    # mutate + recode_values approximation\n    likert['score'] = likert['score'].map(mapping).fillna(\"error\")\n    \nexcept NameError:\n    # Handle case where 'lookup' is not defined in the environment", "score": 1.0, "script_id": "dplyr__vignette__recoding-replacing_s22.R", "n_calls": 0}

## Edit Examples
(none)
