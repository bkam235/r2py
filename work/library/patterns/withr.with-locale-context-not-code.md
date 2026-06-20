---
id: withr.with-locale-context-not-code
package: 
confidence: tentative
seed: false
created: 2026-06-16
last_review: 2026-06-16
tie_count: 0
---

# withr.with-locale-context-not-code

## Guidance
In R's withr::with_locale(), when used with curly braces (like `with_locale(new=..., {code})`), the expression is executed within the locale context. Python's context manager should use `with` statement syntax instead of passing a code callable parameter. The expression to be executed belongs inside the with block, not as a lambda passed to code=.

## Evidence
- 021894dec169 → score 0.071 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
- {"failure_class": "stdout", "old_code": "print(with_locale(new={\"LC_TIME\": \"en_GB\"}, code=lambda: \" \".join([dt.datetime(2000, month, 1).strftime(\"%B\") for month in range(1, 13)])))", "new_code": "with with_locale(new={\"LC_TIME\": \"en_GB\"}):\n    print(\" \".join([dt.datetime(2000, month, 1).strftime(\"%B\") for month in range(1, 13)]))", "score_delta": 0.0712, "script_id": "021894dec169"}
