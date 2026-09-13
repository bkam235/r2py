---
id: lubridate.semester
package: lubridate
confidence: tentative
seed: true
created: 2026-09-14
last_review: 2026-09-14
tie_count: 0
---

# lubridate.semester

## Guidance
Translate R `semester` (FunctionCall from lubridate) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "529d98b0", "r_snippet": "semester(x)", "py_snippet": "def semester(x, with_year=False):\n    months = x.month.values\n    years = x.year.values\n    # semesters <- rep(1:2, each = 6)\n    semesters_map = [1]*6 + [2]*6\n    s = np.array([semesters_map[m-1] for m in months])\n    \n    if with_year:\n        return years + (s / 10.0)\n    else:\n        return s.astype(int)\n\nprint(semester(x))", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)
