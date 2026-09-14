---
id: data.table.melt
package: data.table
confidence: tentative
seed: true
created: 2026-09-14
last_review: 2026-09-14
tie_count: 0
---

# data.table.melt

## Guidance
Translate R `melt` (FunctionCall from data.table) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "64f7a806", "r_snippet": "melt(DT, measure.vars = patterns(\"^x\", \"^y\", cols=names(DT)))", "py_snippet": "def patterns(*args, cols=None, ignore_case=False, perl=False, fixed=False, useBytes=False):\n    if cols is None:\n        # This is handled by the call site in the R script logic\n        raise ValueError(\"cols must be a character vector of column names\")\n    \n    patterns_list = []\n    for arg in args:\n        if isinstance(arg, list):\n            patterns_list.extend(arg)\n        else:\n            patterns_list.append(arg)\n            \n    if not all(isinstance(p, str) for p in patterns_list):\n        raise TypeError(\"Input patterns must be of type character.\")\n    \n    matched_results = []\n  ", "score": 0.9493, "script_id": "auto"}

## Edit Examples
(none)
