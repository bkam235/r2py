---
id: hms.floor-hms
package: hms
confidence: tentative
seed: true
created: 2026-09-30
last_review: 2026-09-30
tie_count: 0
---

# hms.floor-hms

## Guidance
Translate R `floor_hms` (FunctionCall from hms) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "260806c5", "r_snippet": "floor_hms(as_hms(\"12:34:56\"), 60)", "py_snippet": "def floor_hms(x, secs=None, digits=None):\n    s_val = digits_to_secs(secs, digits)\n    return format_hms(np.floor(x / s_val) * s_val)\n\n# Execution\n\nprint(floor_hms(as_hms(\"12:34:56\"), 60))", "score": 1.0, "script_id": "hms__rd_example__round_hms_Rd", "n_calls": 0}

## Edit Examples
(none)
