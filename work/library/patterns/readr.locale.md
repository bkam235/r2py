---
id: readr.locale
package: readr
confidence: tentative
seed: true
created: 2026-09-13
last_review: 2026-09-13
tie_count: 0
---

# readr.locale

## Guidance
Translate R `locale` (FunctionCall from readr) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "939a4e64", "r_snippet": "locale()", "py_snippet": "class LocaleObject:\n    def __init__(self, date_names, date_format, time_format, decimal_mark, grouping_mark, tz, encoding):\n        self.date_names = date_names\n        self.date_format = date_format\n        self.time_format = time_format\n        self.decimal_mark = decimal_mark\n        self.grouping_mark = grouping_mark\n        self.tz = tz\n        self.encoding = encoding\n\n    def __repr__(self):\n        # Mimic R's print output for readr::locale\n        res = \"      <locale>\\n\"\n        res += f\"Numbers:  {self.grouping_mark}123{self.decimal_mark}456.78\\n\" # This is a simplification of R's ", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)
