---
id: tidyr.complete
package: tidyr
confidence: tentative
seed: true
created: 2026-09-23
last_review: 2026-09-23
tie_count: 0
---

# tidyr.complete

## Guidance
Translate R `complete` (FunctionCall from tidyr) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "f13e516d", "r_snippet": "df |> complete(group, item_id, item_name)", "py_snippet": "cols = ['group', 'item_id', 'item_name']\nunique_vals = [df[c].unique() for c in cols]\nfull_grid = pd.DataFrame(list(itertools.product(*unique_vals)), columns=cols)\nres1 = pd.merge(full_grid, df, on=cols, how='left')\nprint(res1)\n\n# df |> complete(group, nesting(item_id, item_name))\n# Cross all possible `group` values with the unique pairs of `(item_id, item_name)`", "score": 0.9333, "script_id": "tidyr__rd_example__complete_Rd", "n_calls": 0}

## Edit Examples
(none)
