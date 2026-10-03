---
id: base.data.frame
package: base
confidence: tentative
seed: true
created: 2026-09-20
last_review: 2026-09-20
tie_count: 0
---

# base.data.frame

## Guidance
Translate R `data.frame` (FunctionCall from base) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "caafe4d3", "r_snippet": "tab <- data.frame(num=1:26,abc=letters)", "py_snippet": "tab = pd.DataFrame({'num': range(1, 27), 'abc': list(string.ascii_lowercase)})\n\n# First test case", "score": 1.0, "script_id": "prodlim__rd_example__row_match_Rd", "n_calls": 1}

## Edit Examples
(none)
