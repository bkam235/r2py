---
id: base.interactive
package: base
confidence: tentative
seed: true
created: 2026-09-20
last_review: 2026-09-20
tie_count: 0
---

# base.interactive

## Guidance
Translate R `interactive` (FunctionCall from base) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "dc0c763c", "r_snippet": "if (interactive()) withAutoprint({ # examplesIf", "py_snippet": "def interactive():\n    return True", "score": 1.0, "script_id": "tinytex__rd_example__check_installed_Rd", "n_calls": 2}

## Edit Examples
(none)
