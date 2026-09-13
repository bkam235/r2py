---
id: lubridate.quarter
package: lubridate
confidence: tentative
seed: true
created: 2026-09-14
last_review: 2026-09-14
tie_count: 0
---

# lubridate.quarter

## Guidance
Translate R `quarter` (FunctionCall from lubridate) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "079210ae", "r_snippet": "quarter(x)", "py_snippet": "def quarter(x, type_val=\"quarter\", fiscal_start=1, with_year=None):\n    if with_year is None:\n        with_year = (type_val == \"year.quarter\")\n    \n    # R logic: fs <- (fiscal_start - 1) %% 12\n    fs = (fiscal_start - 1) % 12\n    # shifted <- seq(fs, 11 + fs) %% 12 + 1\n    shifted = [(fs + i) % 12 + 1 for i in range(12)]\n    \n    months = x.month.values\n    years = x.year.values\n    \n    # quarters <- rep(1:4, each = 3)\n    quarters_map = [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4]\n    \n    # s <- match(m, shifted)\n    # match finds the first index. shifted contains 1..12 in some order.\n    q_vals =", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)
