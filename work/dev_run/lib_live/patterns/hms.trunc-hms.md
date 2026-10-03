---
id: hms.trunc-hms
package: hms
confidence: tentative
seed: true
created: 2026-09-30
last_review: 2026-09-30
tie_count: 0
---

# hms.trunc-hms

## Guidance
Translate R `trunc_hms` (FunctionCall from hms) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "11892618", "r_snippet": "trunc_hms(as_hms(\"12:34:56\"), 60)", "py_snippet": "def trunc_hms(x, secs=None, digits=None):\n    s_val = digits_to_secs(secs, digits)\n    return format_hms(np.trunc(x / s_val) * s_val)\n\nprint(trunc_hms(as_hms(\"12:34:56\"), 60))", "score": 1.0, "script_id": "hms__rd_example__round_hms_Rd", "n_calls": 0}

## Edit Examples
(none)
