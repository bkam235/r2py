---
id: with-locale-simple-execution
package: 
confidence: tentative
seed: false
created: 2026-06-06
last_review: 2026-06-06
tie_count: 0
---

# with-locale-simple-execution

## Guidance
When with_locale is called with a simple function that just returns a value (like locale.localeconv()), directly execute the locale change, run the function, and restore the locale. This avoids unnecessary lambda wrapping and produces the expected side effect of printing/executing the function result.

## Evidence
- 021894dec169 → score 0.028 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
- {"failure_class": "graphics", "old_code": "with_locale(new={\"LC_MONETARY\": \"it_IT\"}, func=lambda: locale.localeconv())", "new_code": "locale.setlocale(locale.LC_MONETARY, \"it_IT\")\nprint(locale.localeconv())\nlocale.setlocale(locale.LC_MONETARY, \"\")", "score_delta": 0.0282, "script_id": "021894dec169"}
