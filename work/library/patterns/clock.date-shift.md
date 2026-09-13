---
id: clock.date-shift
package: clock
confidence: tentative
seed: true
created: 2026-09-13
last_review: 2026-09-13
tie_count: 0
---

# clock.date-shift

## Guidance
Translate R `date_shift` (FunctionCall from clock) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "51a625d4", "r_snippet": "date_shift(x, monday)", "py_snippet": "def date_shift(x, target, which=\"next\", boundary=\"keep\"):\n    \"\"\"\n    Shifts date to the next/previous occurrence of the target weekday.\n    target: based on R output, if target=2 is Monday, then target-1 is pandas weekday.\n    \"\"\"\n    # Adjusted target for pandas: if R's Monday is 2, then target 2 -> pandas 0.\n    pandas_target = target - 2 if target >= 2 else 6 \n    # Correction: If R target is 2 for Monday, then pandas_target = target - 2.\n    # Let's be more robust:\n    # R target 2 -> pandas 0 (Mon)\n    # R target 3 -> pandas 1 (Tue)\n    # R target 1 -> pandas 6 (Sun)\n    # Wait, if R pro", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)
