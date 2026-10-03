---
id: timedate.listholidays
package: timeDate
confidence: tentative
seed: true
created: 2026-09-30
last_review: 2026-09-30
tie_count: 0
---

# timedate.listholidays

## Guidance
Translate R `listHolidays` (FunctionCall from timeDate) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "e2b6edfb", "r_snippet": "listHolidays(\"CH\")", "py_snippet": "def listHolidays(pattern=\".*\"):\n    # In R: if (pattern == \"*\") pattern = \"\\\\*\"\n    # This handles the case where the user literally passes \"*\"\n    if pattern == \"*\":\n        pattern = r\"\\*\"\n    \n    # R's grep returns indices of elements that match the pattern\n    # we return the matching strings\n    matches = [h for h in _all_holidays if re.search(pattern, h)]\n    return matches\n\n# Local Swiss Holidays:\n\nprint(listHolidays(\"CH\"))", "score": 1.0, "script_id": "timeDate__rd_example__holiday-Listing_Rd", "n_calls": 0}

## Edit Examples
(none)
