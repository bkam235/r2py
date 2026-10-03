---
id: broom.tidy
package: broom
confidence: tentative
seed: true
created: 2026-09-30
last_review: 2026-09-30
tie_count: 0
---

# broom.tidy

## Guidance
Translate R `tidy` (FunctionCall from broom) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "64e70e0a", "r_snippet": "    tidy(dw)", "py_snippet": "tidy_dw = pd.DataFrame({\n    'statistic': [dw_stat],\n    'p.value': [p_val],\n    'autocorrelation': [rho],\n    'method': ['Durbin-Watson Test'],\n    'alternative': ['two.sided']\n})\nprint(\"# A tibble: 1 × 5\")\nprint(\"  statistic p.value autocorrelation method             alternative\")\nprint(\"      <dbl>   <dbl>           <dbl> <chr>              <chr>      \")\nprint(f\"1      {dw_stat:.2f}  {p_val:.4f}           {rho:.3f} Durbin-Watson Test two.sided\")\n\n# glance(dw) returns the same as tidy for durbinWatsonTest", "score": 0.9899, "script_id": "broom__rd_example__durbinWatsonTest_tidiers_Rd", "n_calls": 0}

## Edit Examples
(none)
