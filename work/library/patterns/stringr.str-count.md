---
id: stringr.str-count
package: stringr
confidence: tentative
seed: true
created: 2026-08-21
last_review: 2026-08-21
tie_count: 0
---

# stringr.str-count

## Guidance
Translate R `str_count` (FunctionCall from stringr) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "861af018", "r_snippet": "str_count(fruit, \"a\")", "py_snippet": "print([s.count(\"a\") for s in fruit])\n\n# str_count(fruit, \"p\")", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)
