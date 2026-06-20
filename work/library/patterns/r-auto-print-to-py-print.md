---
id: r-auto-print-to-py-print
package: 
confidence: tentative
seed: false
created: 2026-06-11
last_review: 2026-06-11
tie_count: 0
---

# r-auto-print-to-py-print

## Guidance
When R auto-prints a top-level expression result to stdout, wrap the equivalent Python expression with print() to produce visible output that matches the R behavior.

## Evidence
- d42c7e223bcd → score 0.084 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
- {"failure_class": "stdout", "old_code": "def intpalette(inputcol, numcol=None, x_from=None, x_to=None):", "new_code": "def graycol(n):\n    \"\"\"Generate n grayscale colors from black to white\"\"\"\n    return ['#' + format(int(round(i * 255)), '02x') * 3 for i in np.linspace(0, 1, n)]\n\nprint(graycol(10))\n\ndef intpalette(inputcol, numcol=None, x_from=None, x_to=None):", "score_delta": 0.0835, "script_id": "d42c7e223bcd"}
