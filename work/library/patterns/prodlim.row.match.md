---
id: prodlim.row.match
package: prodlim
confidence: tentative
seed: true
created: 2026-08-20
last_review: 2026-08-20
tie_count: 0
---

# prodlim.row.match

## Guidance
Translate R `row.match` (FunctionCall from prodlim) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "f95e96e1", "r_snippet": "row.match(x,tab)", "py_snippet": "def row_match(x, table, nomatch=np.nan):\n    if isinstance(table, np.ndarray):\n        table = pd.DataFrame(table)\n    \n    # If x is not a DataFrame (e.g., list, tuple, numpy array), convert to DataFrame\n    # R's as.data.frame(matrix(x, nrow=1)) creates a 1-row DF where elements of x are columns\n    if not isinstance(x, pd.DataFrame):\n        x = pd.DataFrame([x])\n    \n    # Convert rows to strings joined by \\r to create unique identifiers for matching\n    # R's paste(..., sep=\"\\r\") across columns\n    cx = x.astype(str).apply(lambda row: \"\\r\".join(row), axis=1)\n    ct = table.astype(str).app", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)
