---
id: base.getrversion
package: base
confidence: tentative
seed: true
created: 2026-10-07
last_review: 2026-10-07
tie_count: 0
---

# base.getrversion

## Guidance
Translate R `getrversion` from base to Python. The verified example below comes from another script that used it.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "08908ab8", "r_snippet": "if (rlang::is_installed(\"modeldata\")) (if (getRversion() >= \"3.4\") withAutoprint else force)({ # examplesIf", "py_snippet": "import pandas as pd\nimport numpy as np", "score": 1.0, "script_id": "recipes__rd_example__discretize_Rd.R", "n_calls": 1}

## Edit Examples
(none)
