---
id: stats.predict
package: stats
confidence: tentative
seed: true
created: 2026-10-07
last_review: 2026-10-07
tie_count: 0
---

# stats.predict

## Guidance
Translate R `predict` from stats to Python. The verified example below comes from another script that used it.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "dee7bb5c", "r_snippet": "Preds <- predict(glmModel, type = 'response')", "py_snippet": "# Preds <- predict(glmModel, type = 'response')\nPreds = glmModel.predict(X_with_intercept)", "score": 1.0, "script_id": "ModelMetrics__rd_example__logLoss_Rd.R", "n_calls": 1}

## Edit Examples
(none)
