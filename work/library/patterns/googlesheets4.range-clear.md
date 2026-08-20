---
id: googlesheets4.range-clear
package: googlesheets4
confidence: tentative
seed: true
created: 2026-07-17
last_review: 2026-07-17
tie_count: 0
---

# googlesheets4.range-clear

## Guidance
Translate R `range_clear` (FunctionCall from googlesheets4) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "471ad668", "r_snippet": "range_clear(ss, range = \"9:9\")", "py_snippet": "def range_clear(ss: str, sheet: Optional[str] = None, range: Optional[str] = None, \n                reformat: bool = True) -> str:\n    \"\"\"Clear a range in a Google Sheet.\"\"\"\n    return range_flood(ss=ss, sheet=sheet, range=range, cell=None, reformat=reformat)\n\n    range_clear(ss, range=\"9:9\")\n\n    range_clear(ss, range=\"10:10\", reformat=False)", "score": 0.8, "script_id": "auto"}

## Edit Examples
(none)
