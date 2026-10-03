---
id: lava.csplit
package: lava
confidence: tentative
seed: true
created: 2026-09-30
last_review: 2026-09-30
tie_count: 0
---

# lava.csplit

## Guidance
Translate R `csplit` (FunctionCall from lava) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "956d4978", "r_snippet": "csplit(iris[1:10,]) ## Split in two sets 1:(n/2) and (n/2+1):n", "py_snippet": "print(csplit(iris.iloc[0:10]))\n\n# csplit(iris[1:10,], 0.5)", "score": 0.9362, "script_id": "lava__rd_example__csplit_Rd", "n_calls": 0}

## Edit Examples
(none)
