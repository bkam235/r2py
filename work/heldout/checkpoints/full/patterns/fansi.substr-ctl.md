---
id: fansi.substr-ctl
package: fansi
confidence: tentative
seed: true
created: 2026-09-20
last_review: 2026-09-20
tie_count: 0
---

# fansi.substr-ctl

## Guidance
Translate R `substr_ctl` (FunctionCall from fansi) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "fbbc81a6", "r_snippet": "bleed <- substr_ctl(c(\"\\033[41mhello\", \"world\"), 1, 3, terminate=FALSE)", "py_snippet": "bleed = substr_ctl([\"\\033[41mhello\", \"world\"], 1, 3, terminate=False)", "score": 1.0, "script_id": "fansi__rd_example__substr_ctl_Rd", "n_calls": 0}

## Edit Examples
(none)
