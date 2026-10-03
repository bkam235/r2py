---
id: stats.rnorm
package: stats
confidence: tentative
seed: true
created: 2026-09-23
last_review: 2026-09-23
tie_count: 0
---

# stats.rnorm

## Guidance
Translate R `rnorm` from stats to Python. The verified example below uses it inside a statement that may call other functions too.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "19c2edb6", "r_snippet": "rnorm(100) %>% `*`(5) %>% `+`(5) %>% ", "py_snippet": "d = np.random.normal(0, 1, 100) * 5 + 5\n\n# { cat(\"Mean:\", mean(.), \"Variance:\", var(.), \"\\n\"); head(.) }", "score": 1.0, "script_id": "magrittr__vignette__magrittr_s11", "n_calls": 1}

## Edit Examples
(none)
