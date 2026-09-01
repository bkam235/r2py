---
id: hardhat.get-levels
package: hardhat
confidence: tentative
seed: true
created: 2026-09-01
last_review: 2026-09-01
tie_count: 0
---

# hardhat.get-levels

## Guidance
Translate R `get_levels` (FunctionCall from hardhat) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "e46778c9", "r_snippet": "get_levels(iris)", "py_snippet": "def get_levels(data: Any) -> Optional[dict]:\n    if not isinstance(data, pd.DataFrame):\n        return None\n    \n    levels_dict = {}\n    for col_name in data.columns:\n        col = data[col_name]\n        if isinstance(col.dtype, pd.CategoricalDtype):\n            levels_dict[col_name] = col.cat.categories.tolist()\n        # In some cases, R factors are shimmed as objects/strings, \n        # but the logic should follow if they are categorical.\n            \n    if not levels_dict:\n        return None\n    \n    return levels_dict\n\niris_df = pd.DataFrame(iris)\nif 'Species' in iris_df.columns:\n    i", "score": 0.993, "script_id": "auto"}

## Edit Examples
(none)
