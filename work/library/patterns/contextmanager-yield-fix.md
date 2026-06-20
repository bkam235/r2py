---
id: contextmanager-yield-fix
package: 
confidence: tentative
seed: false
created: 2026-06-11
last_review: 2026-06-11
tie_count: 0
---

# contextmanager-yield-fix

## Guidance
Context managers decorated with @contextmanager must use 'yield' instead of 'return' to properly function as generators. The yielded value becomes the target of the 'as' clause in 'with' statements, and execution resumes after the with block completes.

## Evidence
- 021894dec169 → score 0.486 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
- {"r_hash": "35d704fc", "r_snippet": "with_locale(new = c(\"LC_TIME\" = \"es_ES\"), format(ISOdate(2000, 1:12, 1), \"%B\"))", "py_snippet": "print(with_locale(new={\"LC_TIME\": \"es_ES\"}, code=format_months))", "score": 1.0, "script_id": "021894dec169"}

## Edit Examples
- {"failure_class": "stdout", "old_code": "return result", "new_code": "yield result", "score_delta": 0.4858, "script_id": "021894dec169"}
