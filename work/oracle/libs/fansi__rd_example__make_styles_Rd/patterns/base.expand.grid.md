---
id: base.expand.grid
package: base
confidence: tentative
seed: true
created: 2026-10-07
last_review: 2026-10-07
tie_count: 0
---

# base.expand.grid

## Guidance
Translate R `expand.grid` from base to Python. The verified example below comes from another script that used it.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "55b8d38b", "r_snippet": "x <- summary(fit4,times=10,newdata=expand.grid(age=c(60,40,50),sex=c(\"male\",\"female\")))", "py_snippet": "print(fit3_summary.round(3))\n\n# stratified Beran estimator\n# -----------------------------------------------------------------------------------------\nfit4_results = []\nnewdata4 = pd.DataFrame({'age': [20, 50, 70], 'sex': ['female', 'male', 'male']})\nfor _, row in newdata4.iterrows():\n    subset = d[(d['sex'] == row['sex']) & (d['age'] >= row['age'] - 5) & (d['age'] <= row['age'] + 5)]\n    if len(subset) == 0: subset = d[d['sex'] == row['sex']]\n    st = prodlim_summary_table(subset, [1, 5, 10], percent=True)", "score": 1.0, "script_id": "prodlim__rd_example__summary_prodlim_Rd.R", "n_calls": 2}

## Edit Examples
(none)
