---
id: httr2.req-perform
package: httr2
confidence: tentative
seed: true
created: 2026-09-06
last_review: 2026-09-06
tie_count: 0
---

# httr2.req-perform

## Guidance
Translate R `req_perform` (FunctionCall from httr2) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "f2710f33", "r_snippet": "resp <- request(\"https://httr2.r-lib.org\") |> req_perform()", "py_snippet": "resp_obj = requests.get(\"https://httr2.r-lib.org\")\nresp = resp_obj\n\n# R: resp", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)
