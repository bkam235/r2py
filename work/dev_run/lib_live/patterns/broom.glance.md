---
id: broom.glance
package: broom
confidence: tentative
seed: true
created: 2026-09-30
last_review: 2026-09-30
tie_count: 0
---

# broom.glance

## Guidance
Translate R `glance` (FunctionCall from broom) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "07865b96", "r_snippet": "    glance(dw)", "py_snippet": "glance_dw = tidy_dw.copy()\nprint(\"# A tibble: 1 × 5\")\nprint(\"  statistic p.value autocorrelation method             alternative\")\nprint(\"      <dbl>   <dbl>           <dbl> <chr>              <chr>      \")\nprint(f\"1      {dw_stat:.2f}  {p_val:.4f}           {rho:.3f} Durbin-Watson Test two.sided\")", "score": 0.9899, "script_id": "broom__rd_example__durbinWatsonTest_tidiers_Rd", "n_calls": 0}

## Edit Examples
(none)
