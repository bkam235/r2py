---
id: purrr.keep-at
package: purrr
confidence: tentative
seed: true
created: 2026-08-20
last_review: 2026-08-20
tie_count: 0
---

# purrr.keep-at

## Guidance
Translate R `keep_at` (FunctionCall from purrr) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "f85f74e7", "r_snippet": "x |> keep_at(letters)", "py_snippet": "print(x[x.index.isin(list(string.ascii_lowercase))])\n\n# discard_at(letters)", "score": 0.8333, "script_id": "auto"}

## Edit Examples
(none)
