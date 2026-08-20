---
id: cli.cat-rule
package: cli
confidence: tentative
seed: true
created: 2026-07-06
last_review: 2026-07-06
tie_count: 0
---

# cli.cat-rule

## Guidance
Translate R `cat_rule` (FunctionCall from cli) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "05616f2b", "r_snippet": "cat_rule()", "py_snippet": "def cat_rule():\n    print(\"─\" * 76)\n\n# Examples from R source\n# (suppressPackageStartupMessages is suppressed in Python)\n\n# (library(cli) is implicit in the function definitions above)\n\ncat_rule()", "score": 0.9872, "script_id": "auto"}

## Edit Examples
(none)
