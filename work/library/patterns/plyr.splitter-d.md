---
id: plyr.splitter-d
package: plyr
confidence: tentative
seed: true
created: 2026-08-25
last_review: 2026-08-25
tie_count: 0
---

# plyr.splitter-d

## Guidance
Translate R `splitter_d` (ExternalSymbol from plyr) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "1be97275", "r_snippet": "plyr:::splitter_d(mtcars, .(cyl))", "py_snippet": "def splitter_d(data, variables, drop=True):\n    \"\"\"\n    Python equivalent of plyr:::splitter_d.\n    \"\"\"\n    if isinstance(variables, str):\n        vars_list = [variables]\n    elif isinstance(variables, (list, tuple)):\n        vars_list = list(variables)\n    else:\n        vars_list = list(variables)\n    \n    df = data.copy()\n    \n    # Determine levels for each variable\n    all_levels = []\n    for var in vars_list:\n        if isinstance(df[var].dtype, pd.CategoricalDtype):\n            all_levels.append(df[var].cat.categories.tolist())\n        else:\n            # For non-categorical, get unique ", "score": 0.999, "script_id": "auto"}

## Edit Examples
(none)
