---
id: purrr.list-cbind
package: purrr
confidence: tentative
seed: true
created: 2026-09-30
last_review: 2026-09-30
tie_count: 0
---

# purrr.list-cbind

## Guidance
Translate R `list_cbind` (FunctionCall from purrr) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "bc2a8fa7", "r_snippet": "list_cbind(x2)", "py_snippet": "def list_cbind(x, name_repair=\"unique\", size=None):\n    \"\"\"\n    Combine a list of data frames by column.\n    \"\"\"\n    dfs = [df for df in x.values()] if isinstance(x, dict) else x\n    return pd.concat(dfs, axis=1)\n\n# --- Execution ---\n\nprint(list_cbind(x2))", "score": 0.9062, "script_id": "purrr__rd_example__list_c_Rd", "n_calls": 0}

## Edit Examples
(none)
