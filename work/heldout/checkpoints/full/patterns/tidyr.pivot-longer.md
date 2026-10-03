---
id: tidyr.pivot-longer
package: tidyr
confidence: tentative
seed: true
created: 2026-09-21
last_review: 2026-09-21
tie_count: 0
---

# tidyr.pivot-longer

## Guidance
Translate R `pivot_longer` (FunctionCall from tidyr) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "cebd4b1f", "r_snippet": "  pivot_longer(\n    wk1:wk76,\n    names_to = \"week\",\n    values_to = \"rank\",\n    values_drop_na = TRUE\n  )", "py_snippet": "cols_to_pivot = [f\"wk{i}\" for i in range(1, 77)]\nid_vars = [col for col in billboard.columns if col not in cols_to_pivot]\n\n# To mimic pivot_longer, we need to maintain the original row order.\n# pandas.melt usually does this, but we ensure it by adding an index.\nbillboard_with_idx = billboard.copy()\nbillboard_with_idx['_orig_idx'] = range(len(billboard))\n\nbillboard2 = pd.melt(\n    billboard_with_idx,\n    id_vars=['_orig_idx'] + id_vars,\n    value_vars=cols_to_pivot,\n    var_name=\"week\",\n    value_name=\"rank\"\n)\n\n# values_drop_na = TRUE\nbillboard2 = billboard2.dropna(subset=[\"rank\"])\n\n# R's pivot_longer sorts by original row first, then by the variable being pivoted.\n# Since melt's order is (variable, original_row), we must sort to (original_row, variable).\nbillboard2 = billboard2.sort_values(by=['_orig_idx', 'week']).drop(columns=['_orig_idx'])\nbillboard2 = billboard2.reset_index(drop=True)", "score": 1.0, "script_id": "tidyr__vignette__tidy-data_s9", "n_calls": 0}

## Edit Examples
(none)
