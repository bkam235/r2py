---
id: base.rep-len
package: base
confidence: tentative
seed: true
created: 2026-09-20
last_review: 2026-09-20
tie_count: 0
---

# base.rep-len

## Guidance
Translate R `rep_len` from base to Python. The verified example below uses it inside a statement that may call other functions too.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "73c67837", "r_snippet": "val2 <- c(\"\\033[45m\", rep_len(val, length(x)))", "py_snippet": "val2 = [\"\\033[45m\"] + [val] * len(x)\n\n# r2py:entity:substr_ctl(x2, 2, 2, carry=TRUE)_1\ndef substr_ctl_replace_vec(x_vec, start, stop, values, carry=False):\n    results = []\n    for i in range(len(x_vec)):\n        s = x_vec[i]\n        if i == 0 and s.startswith('\\033['):\n            results.append(s)\n            continue\n        v = values[i] if i < len(values) else values[-1]\n        res = substr_ctl_replace([s], start, stop, v, carry)[0]\n        results.append(res)\n    return results\n\nx2 = substr_ctl_replace_vec(x2, 2, 2, val2, carry=True)", "score": 1.0, "script_id": "fansi__rd_example__substr_ctl_Rd", "n_calls": 2}

## Edit Examples
- {"failure_class": "data_output", "old_code": "val2 = [\"\\033[45m\"] + [val] * len(x)", "new_code": "val2 = [\"\\033[45m\"] + [val] * len(x)\n\n# r2py:entity:substr_ctl(x2, 2, 2, carry=TRUE)_1\ndef substr_ctl_replace_vec(x_vec, start, stop, values, carry=False):\n    results = []\n    for i in range(len(x_vec)):\n        s = x_vec[i]\n        if i == 0 and s.startswith('\\033['):\n            results.append(s)\n            continue\n        v = values[i] if i < len(values) else values[-1]\n        res = substr_ctl_replace([s], start, stop, v, carry)[0]\n        results.append(res)\n    return results\n\nx2 = substr_ctl_replace_vec(x2, 2, 2, val2, carry=True)", "score_delta": 0.0625, "script_id": "fansi__rd_example__substr_ctl_Rd", "r_snippet": "val2 <- c(\"\\033[45m\", rep_len(val, length(x)))", "functions": ["base::rep_len", "base::length"]}
