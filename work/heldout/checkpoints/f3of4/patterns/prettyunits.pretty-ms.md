---
id: prettyunits.pretty-ms
package: prettyunits
confidence: tentative
seed: true
created: 2026-09-20
last_review: 2026-09-20
tie_count: 0
---

# prettyunits.pretty-ms

## Guidance
Translate R `pretty_ms` (FunctionCall from prettyunits) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "ddb6133b", "r_snippet": "pretty_ms(c(1337, 13370, 133700, 1337000, 1337000000))", "py_snippet": "def parse_ms(ms):\n    ms = np.array(ms)\n    days = ms // (24 * 3600 * 1000)\n    rem = ms % (24 * 3600 * 1000)\n    hours = rem // (3600 * 1000)\n    rem = rem % (3600 * 1000)\n    minutes = rem // (60 * 1000)\n    rem = rem % (60 * 1000)\n    seconds = rem // 1000\n    return np.column_stack([days, hours, minutes, seconds])\n\ndef first_positive(col):\n    pos = np.where(col > 0)[0]\n    return pos[0] if pos.size > 0 else None\n\ndef pretty_ms(ms, compact=False):\n    ms = np.array(ms)\n    if not np.issubdtype(ms.dtype, np.number):\n        raise TypeError(\"ms must be numeric\")\n    \n    parsed = parse_ms(ms)\n    \n    if compact:\n        units = [\"d\", \"h\", \"m\", \"s\"]\n        parsed2 = np.array([[f\"{val}{unit}\" if val > 0 else \"\" for val, unit in zip(row, units)] for row in parsed])\n        \n        results = []\n        for i in range(len(ms)):\n            row = parsed[i]\n            idx = first_positive(row)\n            if idx is not None:\n                results.append(f\"~{parsed2[i, idx]}\")\n            else:\n                results.append(None)\n        return np.array(results)\n    else:\n        exact = np.array([f\"{int(np.ceil(val))}ms\" if not np.isnan(val) else None for val in ms])\n        \n        def merge_pieces(pieces):\n            if np.all(np.isnan(pieces)) or np.all(pieces == 0):\n                return None\n            parts = []\n            labels = [\"d\", \"h\", \"m\", \"s\"]\n            for val, label in zip(pieces, labels):\n                if val > 0:\n                    parts.append(f\"{val}{label}\")\n            return \" \".join(parts)\n\n        approx = np.array([merge_pieces(row) for row in parsed])\n        \n        final = []\n        for i in range(len(ms)):\n            if np.isnan(ms[i]):\n                final.append(None)\n            elif ms[i] < 1000:\n                final.append(exact[i])\n            else:\n                final.append(approx[i])\n        return np.array(final)\n\nms_vals = np.array([1337, 13370, 133700, 1337000, 1337000000])\nprint(pretty_ms(ms_vals))", "score": 0.9625, "script_id": "prettyunits__rd_example__pretty_ms_Rd", "n_calls": 0}

## Edit Examples
(none)
