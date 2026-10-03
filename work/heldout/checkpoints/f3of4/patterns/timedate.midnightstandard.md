---
id: timedate.midnightstandard
package: timeDate
confidence: tentative
seed: true
created: 2026-09-21
last_review: 2026-09-21
tie_count: 0
---

# timedate.midnightstandard

## Guidance
Translate R `midnightStandard` (FunctionCall from timeDate) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "b643ac0d", "r_snippet": "midnightStandard(ch)", "py_snippet": "def midnightStandard(charvec, format_val=None):\n    if format_val is None:\n        format_val = whichFormat(charvec)\n    ans = midnightStandard2(charvec, format_val)\n    return ans.strftime(\"%Y-%m-%d %H:%M:%S\")\n\nprint(f'[1] \"{midnightStandard(ch)}\"')", "score": 1.0, "script_id": "timeDate__rd_example__timeDate-midnightStandard_Rd", "n_calls": 0}

## Edit Examples
(none)
