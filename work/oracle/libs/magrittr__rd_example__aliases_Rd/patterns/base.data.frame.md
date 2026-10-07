---
id: base.data.frame
package: base
confidence: tentative
seed: true
created: 2026-10-07
last_review: 2026-10-07
tie_count: 0
---

# base.data.frame

## Guidance
Translate R `data.frame` from base to Python. The verified example below comes from another script that used it.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "2b01b4d1", "r_snippet": "CompRiskFrame <- data.frame(time=1:10,event=c(1,2,0,3,0,1,2,1,2,1))", "py_snippet": "TwoStateFrame = SimSurv(10)", "score": 1.0, "script_id": "prodlim__rd_example__Hist_Rd.R", "n_calls": 1}
- {"r_hash": "3fb03c44", "r_snippet": "icensFrame <- data.frame(L=c(1,1,3,4,6),R=c(2,NA,3,6,9),event=c(1,1,1,2,2))", "py_snippet": "plot(SurvHist)\n\nCompRiskFrame = pd.DataFrame({'time': np.arange(1, 11), 'event': [1, 2, 0, 3, 0, 1, 2, 1, 2, 1]})", "score": 1.0, "script_id": "prodlim__rd_example__Hist_Rd.R", "n_calls": 1}

## Edit Examples
(none)
