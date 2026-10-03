---
id: hms.parse-hm
package: hms
confidence: tentative
seed: true
created: 2026-09-30
last_review: 2026-09-30
tie_count: 0
---

# hms.parse-hm

## Guidance
Translate R `parse_hm` (FunctionCall from hms) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "7c8922f2", "r_snippet": "parse_hm(\"12:34\")", "py_snippet": "def parse_hm(x):\n    \"\"\"\n    Parse string as hours:minutes.\n    \"\"\"\n    return parse_time(x, \"%H:%M\")\n\n# Main script execution\n\nprint(parse_hm(\"12:34\"))", "score": 1.0, "script_id": "hms__rd_example__parse_hms_Rd", "n_calls": 0}

## Edit Examples
(none)
