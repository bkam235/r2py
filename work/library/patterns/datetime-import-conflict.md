---
id: datetime-import-conflict
package: 
confidence: tentative
seed: false
created: 2026-06-06
last_review: 2026-06-06
tie_count: 0
---

# datetime-import-conflict

## Guidance
When both `from datetime import datetime` and `import datetime` are present, the class import shadows the module. Use the fully qualified `datetime.datetime()` constructor after module-level import to avoid TypeError.

## Evidence
- 021894dec169 → score 0.197 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
- {"failure_class": "graphics", "old_code": "dates = [datetime(2000, month, 1) for month in range(1, 13)]", "new_code": "dates = [datetime.datetime(2000, month, 1) for month in range(1, 13)]", "score_delta": 0.1971, "script_id": "021894dec169"}
