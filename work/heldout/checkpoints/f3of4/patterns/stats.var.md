---
id: stats.var
package: stats
confidence: tentative
seed: true
created: 2026-09-23
last_review: 2026-09-23
tie_count: 0
---

# stats.var

## Guidance
Translate R `var` from stats to Python. The verified example below uses it inside a statement that may call other functions too.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "558f3cb6", "r_snippet": "  cat(\"Mean:\", mean(.), \"Variance:\", var(.),  \"\\n\")", "py_snippet": "print(f\"Mean: {np.mean(d)} Variance: {np.var(d, ddof=1)}\")", "score": 1.0, "script_id": "magrittr__vignette__magrittr_s11", "n_calls": 3}

## Edit Examples
(none)
