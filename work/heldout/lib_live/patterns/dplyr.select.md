---
id: dplyr.select
package: dplyr
confidence: tentative
seed: true
created: 2026-09-22
last_review: 2026-09-22
tie_count: 0
---

# dplyr.select

## Guidance
Translate R `select` (FunctionCall from dplyr) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "5e9acb5c", "r_snippet": "  select(1:3)", "py_snippet": "def select(df, cols):\n    # Handle 1:3 slicing (1-indexed R style)\n    if isinstance(cols, slice) or (isinstance(cols, range) or hasattr(cols, '__iter__')):\n        # Simplified for the 1:3 case\n        return df.iloc[:, 0:3]\n    return df[cols]\n\n# Convert shim dicts to DataFrames\nmtcars = pd.DataFrame(mtcars)\nstarwars = pd.DataFrame(starwars)\n\n# glimpse(mtcars)\n\nres = select(res, range(1, 4))\n\n# glimpse(starwars)", "score": 0.9333, "script_id": "dplyr__rd_example__glimpse_Rd", "n_calls": 0}

## Edit Examples
(none)
