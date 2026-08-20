---
id: googlesheets4.range-flood
package: googlesheets4
confidence: tentative
seed: true
created: 2026-07-17
last_review: 2026-07-17
tie_count: 0
---

# googlesheets4.range-flood

## Guidance
Translate R `range_flood` (FunctionCall from googlesheets4) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "53ed6e15", "r_snippet": "range_flood(ss, range = \"A1:B3\")", "py_snippet": "def range_flood(ss: str, sheet: Optional[str] = None, range: Optional[str] = None, \n                cell: Optional[Any] = None, reformat: bool = True) -> str:\n    \"\"\"Flood a range in a Google Sheet with a cell value and/or format.\"\"\"\n    print(f\"Editing sheet.\")\n    if cell is not None:\n        print(f\"Sending value/format to range {range}\")\n    else:\n        print(f\"Clearing range {range}\")\n    return ss\n\n    range_flood(ss, range=\"A1:B3\")\n\n    range_flood(ss, range=\"C1:D3\", reformat=False)\n\n    range_flood(ss, range=\"4:5\", cell=\";-)\")\n\n    range_flood(ss, range=\"I:J\", cell=blue_background)", "score": 0.8, "script_id": "auto"}

## Edit Examples
(none)
