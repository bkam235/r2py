---
id: r-sys-localeconv-to-py-localeconv
package: 
confidence: tentative
seed: false
created: 2026-06-13
last_review: 2026-06-13
tie_count: 0
---

# r-sys-localeconv-to-py-localeconv

## Guidance
The R function Sys.localeconv() retrieves locale-specific formatting information. The Python equivalent is locale.localeconv(), which returns a dictionary of locale settings.

## Evidence
- 021894dec169 → score 0.078 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
- {"failure_class": "data", "old_code": "print(with_locale(new={\"LC_MONETARY\": \"en_US\"}, code=lambda: locale.getlocale()))", "new_code": "print(with_locale(new={\"LC_MONETARY\": \"en_US\"}, code=lambda: locale.localeconv()))", "score_delta": 0.0776, "script_id": "021894dec169"}
