---
id: hms.round-hms
package: hms
confidence: tentative
seed: true
created: 2026-09-30
last_review: 2026-09-30
tie_count: 0
---

# hms.round-hms

## Guidance
Translate R `round_hms` (FunctionCall from hms) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "8e4599d9", "r_snippet": "round_hms(as_hms(\"12:34:56\"), 5)", "py_snippet": "def digits_to_secs(secs, digits):\n    if digits is None:\n        if secs is None:\n            raise ValueError(\"Exactly one of `secs` or `digits` is required.\")\n        return secs\n    if secs is not None:\n        raise ValueError(\"Exactly one of `secs` or `digits` is required.\")\n    \n    if not float(digits).is_integer():\n        raise ValueError(\"`digits` must be a whole number\")\n    \n    digits = int(digits)\n    if digits >= -1:\n        return 10**-digits\n    elif digits == -2:\n        return 60.0\n    elif digits == -3:\n        return 600.0\n    elif digits <= -4:\n        return 3600.0 * (10**(-digits - 4))\n    return None\n\ndef round_hms(x, secs=None, digits=None):\n    s_val = digits_to_secs(secs, digits)\n    return format_hms(round(x / s_val) * s_val)\n\nprint(round_hms(as_hms(\"12:34:56\"), 5))", "score": 1.0, "script_id": "hms__rd_example__round_hms_Rd", "n_calls": 0}

## Edit Examples
(none)
