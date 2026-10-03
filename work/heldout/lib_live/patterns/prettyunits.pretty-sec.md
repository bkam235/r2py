---
id: prettyunits.pretty-sec
package: prettyunits
confidence: tentative
seed: true
created: 2026-09-21
last_review: 2026-09-21
tie_count: 0
---

# prettyunits.pretty-sec

## Guidance
Translate R `pretty_sec` (FunctionCall from prettyunits) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "2471d75e", "r_snippet": "pretty_sec(c(1337, 13370, 133700, 1337000, 13370000))", "py_snippet": "def parse_ms(ms):\n    \"\"\"Helper to simulate parse_ms logic (splitting ms into days, hours, mins, secs)\"\"\"\n    ms = np.atleast_1d(ms)\n    days = ms // (1000 * 60 * 60 * 24)\n    rem = ms % (1000 * 60 * 60 * 24)\n    hours = rem // (1000 * 60 * 60)\n    rem = rem % (1000 * 60 * 60)\n    mins = rem // (1000 * 60)\n    secs = (rem % (1000 * 60)) // 1000\n    return np.column_stack([days, hours, mins, secs])\n\ndef first_positive(x):\n    \"\"\"Helper to find index of first non-zero element\"\"\"\n    for i, val in enumerate(x):\n        if val > 0:\n            return i\n    return None\n\ndef pretty_ms(ms, compact=False):\n    ms = np.atleast_1d(ms)\n    parsed = parse_ms(ms)\n    \n    if compact:\n        units = [\"d\", \"h\", \"m\", \"s\"]\n        results = []\n        for i in range(len(ms)):\n            row = parsed[i]\n            idx = first_positive(row)\n            if idx is not None:\n                results.append(f\"~{int(row[idx])}{units[idx]}\")\n            else:\n                results.append(None)\n        return np.array(results)\n    else:\n        results = []\n        for i in range(len(ms)):\n            val_ms = ms[i]\n            if pd.isna(val_ms):\n                results.append(None)\n                continue\n            \n            if val_ms < 1000:\n                results.append(f\"{math.ceil(val_ms)}ms\")\n            else:\n                row = parsed[i].astype(int)\n                pieces = []\n                if row[0] > 0: pieces.append(f\"{row[0]}d \")\n                if row[1] > 0: pieces.append(f\"{row[1]}h \")\n                if row[2] > 0: pieces.append(f\"{row[2]}m \")\n                if row[3] > 0: pieces.append(f\"{row[3]}s \")\n                \n                res_str = \"\".join(pieces).strip()\n                results.append(res_str if res_str else None)\n        return np.array(results)\n\ndef pretty_sec(sec, compact=False):\n    return pretty_ms(np.atleast_1d(sec) * 1000, compact=compact)\n\n# Execution\n\nprint(pretty_sec(np.array([1337, 13370, 133700, 1337000, 13370000])))", "score": 1.0, "script_id": "prettyunits__rd_example__pretty_sec_Rd", "n_calls": 0}

## Edit Examples
(none)
