---
id: base.factor
package: base
confidence: tentative
seed: true
created: 2026-10-07
last_review: 2026-10-07
tie_count: 0
---

# base.factor

## Guidance
Translate R `factor` from base to Python. The verified example below comes from another script that used it.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "e5b45ff8", "r_snippet": "d$sex <- factor(d$sex,levels=c(0,1),labels=c(\"female\",\"male\"))", "py_snippet": "eventtime = 10 + 0.01 * age - 0.4 * sex_numeric + np.random.normal(0, 1, n_sim)", "score": 1.0, "script_id": "prodlim__rd_example__summary_prodlim_Rd.R", "n_calls": 1}
- {"r_hash": "735a014d", "r_snippet": "d$Z <- factor(d$z,levels=c(1,0,2),labels=c(\"B\",\"A\",\"C\"))", "py_snippet": "eventtime = np.maximum(eventtime, 0.1)\nevent = np.random.binomial(1, 0.7, n_sim)", "score": 1.0, "script_id": "prodlim__rd_example__summary_prodlim_Rd.R", "n_calls": 1}

## Edit Examples
(none)
