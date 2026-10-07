---
id: base.set.seed
package: base
confidence: tentative
seed: true
created: 2026-10-07
last_review: 2026-10-07
tie_count: 0
---

# base.set.seed

## Guidance
Translate R `set.seed` from base to Python. The verified example below comes from another script that used it.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "f5e49f14", "r_snippet": "set.seed(1)", "py_snippet": "np.random.seed(1)\n\n# To match R's runif(200) better, we can't easily without a specific R-engine, \n# but we maintain the logic.", "score": 1.0, "script_id": "caret__rd_example__lift_Rd.R", "n_calls": 1}
- {"r_hash": "db85c293", "r_snippet": "set.seed(107)", "py_snippet": "# set.seed(107)\nnp.random.seed(107)\n\n# inTrain <- createDataPartition(y = Sonar$Class, p = .75, list = FALSE)\ninTrain = create_data_partition(\n    y=Sonar['Class'],\n    p=0.75,\n    list_val=False", "score": 1.0, "script_id": "caret__vignette__caret_s3.R", "n_calls": 1}

## Edit Examples
(none)
