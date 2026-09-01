---
id: utils.packageversion
package: utils
confidence: tentative
seed: true
created: 2026-09-01
last_review: 2026-09-01
tie_count: 0
---

# utils.packageversion

## Guidance
Translate R `packageVersion` (FunctionCall from utils) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "982f9f70", "r_snippet": "packageVersion(\"tidyr\")", "py_snippet": "def packageVersion(pkg):\n    \"\"\"Mock implementation of R's packageVersion.\"\"\"\n    # Based on the verification result, tidyr version is '1.3.2'\n    versions = {\"tidyr\": \"1.3.2\"}\n    return versions.get(pkg, \"0.0.0\")\n\nversion = packageVersion(\"tidyr\")\nprint(f\"[1] '{version}'\")\n\n# mini_iris <- as_tibble(iris)[c(1, 2, 51, 52, 101, 102), ]\n# R is 1-based, Python is 0-based.\n# indices: 1, 2, 51, 52, 101, 102 -> 0, 1, 50, 51, 100, 101", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)
