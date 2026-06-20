---
id: repr-trailing-space-removal
package: 
confidence: tentative
seed: false
created: 2026-06-18
last_review: 2026-06-18
tie_count: 0
---

# repr-trailing-space-removal

## Guidance
When R prints objects, trailing spaces in string representations may not be present. Python __repr__ methods translated from R's print methods should not include trailing spaces unless the expected output explicitly shows them.

## Evidence
- ca1440d6104b → score 0.000 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
- {"failure_class": "stdout", "old_code": "    def __repr__(self):\n        mi = self.maxindex if self.maxindex is not None else \"NA\"\n        return f\"range index (ri) from {self.from_} to {self.to_} maxindex {mi} \"", "new_code": "    def __repr__(self):\n        mi = self.maxindex if self.maxindex is not None else \"NA\"\n        return f\"range index (ri) from {self.from_} to {self.to_} maxindex {mi}\"", "score_delta": 0.0, "script_id": "ca1440d6104b"}
