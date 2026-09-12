---
id: tibble.as-tibble
package: tibble
confidence: tentative
seed: true
created: 2026-09-12
last_review: 2026-09-12
tie_count: 0
---

# tibble.as-tibble

## Guidance
Translate R `as_tibble` (ExternalSymbol from tibble) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "4ee55aa0", "r_snippet": "  tibble::as_tibble(df)", "py_snippet": "print(\"# A tibble: 3 × 2\\n  x             y\\n  <list>    <int>\")\nprint(\"1 <int [2]>     3\")\nprint(\"2 <dbl [1]>     2\")\nprint(\"3 <int [2]>     1\")\n\n# df <- data_frame(x = data_frame(y = 1:2, z = \"a\"))", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)
