---
id: withr.with-locale
package: withr
confidence: tentative
seed: true
created: 2026-08-20
last_review: 2026-08-20
tie_count: 0
---

# withr.with-locale

## Guidance
Translate R `with_locale` (FunctionCall from withr) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "e94e70f7", "r_snippet": "with_locale(new = c(\"LC_TIME\" = \"en_GB\"), format(ISOdate(2000, 1:12, 1), \"%B\"))", "py_snippet": "set_locale('en_GB')\nprint([d.strftime('%B') for d in dates])", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)
