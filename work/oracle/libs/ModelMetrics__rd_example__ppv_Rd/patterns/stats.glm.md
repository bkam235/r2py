---
id: stats.glm
package: stats
confidence: tentative
seed: true
created: 2026-10-07
last_review: 2026-10-07
tie_count: 0
---

# stats.glm

## Guidance
Translate R `glm` from stats to Python. The verified example below comes from another script that used it.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "72fc485c", "r_snippet": "glmfit <- glm(am ~ wt, mtcars, family = \"binomial\")", "py_snippet": "X = sm.add_constant(df_mtcars['wt'])\ny = df_mtcars['am']\nglmfit = sm.GLM(y, X, family=sm.families.Binomial()).fit()\n\n# tidy(glmfit)", "score": 1.0, "script_id": "broom__vignette__broom_chunk6.R", "n_calls": 1}

## Edit Examples
(none)
