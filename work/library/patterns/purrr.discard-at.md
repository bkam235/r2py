---
id: purrr.discard-at
package: purrr
confidence: tentative
seed: true
created: 2026-08-20
last_review: 2026-08-20
tie_count: 0
---

# purrr.discard-at

## Guidance
Translate R `discard_at` (FunctionCall from purrr) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "bca46649", "r_snippet": "x |> discard_at(letters)", "py_snippet": "print(x[~x.index.isin(list(string.ascii_lowercase))])\n\n# keep_at(\\(x) nchar(x) == 3)", "score": 0.9, "script_id": "auto"}

## Edit Examples
(none)
