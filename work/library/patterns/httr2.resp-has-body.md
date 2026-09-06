---
id: httr2.resp-has-body
package: httr2
confidence: tentative
seed: true
created: 2026-09-06
last_review: 2026-09-06
tie_count: 0
---

# httr2.resp-has-body

## Guidance
Translate R `resp_has_body` (FunctionCall from httr2) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "7fbbf071", "r_snippet": "resp |> resp_has_body()", "py_snippet": "has_body = len(resp.content) > 0\nprint(f\"[1] {'TRUE' if has_body else 'FALSE'}\")\n\n# R: resp |> resp_body_raw()", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)
