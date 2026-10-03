---
id: timedate.getrmetricsoptions
package: timeDate
confidence: tentative
seed: true
created: 2026-09-20
last_review: 2026-09-20
tie_count: 0
---

# timedate.getrmetricsoptions

## Guidance
Translate R `getRmetricsOptions` (FunctionCall from timeDate) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "ac148117", "r_snippet": "getRmetricsOptions(\"currentYear\")", "py_snippet": "RmetricsOptions = {\n    \"currentYear\": datetime.now().year,\n    \"myFinCenter\": \"GMT\"\n}\n\ndef getRmetricsOptions(x=None, unset=\"\"):\n    if x is None:\n        return {k: v for k, v in RmetricsOptions.items()}\n    return RmetricsOptions.get(x, unset)\n\nres_year = getRmetricsOptions(\"currentYear\")\nprint(f\"currentYear \\n{res_year}\")\n\n# 12 months of current year", "score": 1.0, "script_id": "timeDate__rd_example__timeDate-Calendar_Rd", "n_calls": 0}

## Edit Examples
(none)
