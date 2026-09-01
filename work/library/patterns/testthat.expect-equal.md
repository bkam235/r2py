---
id: testthat.expect-equal
package: testthat
confidence: tentative
seed: true
created: 2026-09-01
last_review: 2026-09-01
tie_count: 0
---

# testthat.expect-equal

## Guidance
Translate R `expect_equal` (FunctionCall from testthat) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "8637e940", "r_snippet": "  expect_equal(dice(), 4)", "py_snippet": "    assert dice() == 4", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)
