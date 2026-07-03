---
id: base.as.logical
package: base
confidence: tentative
seed: true
created: 2026-07-03
last_review: 2026-07-03
tie_count: 0
---

# base.as.logical

## Guidance
Translate R `as.logical` (FunctionCall from base) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "a6d27aa0", "r_snippet": "as.logical(w) # does not coerce back", "py_snippet": "print(w.astype(bool))", "score": 0.9, "script_id": "auto"}

## Edit Examples
(none)
