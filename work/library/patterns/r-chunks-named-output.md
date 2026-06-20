---
id: r-chunks-named-output
package: 
confidence: tentative
seed: false
created: 2026-06-17
last_review: 2026-06-17
tie_count: 0
---

# r-chunks-named-output

## Guidance
The chunk() function call uses named arguments (from=, to=, by=) and should invoke chunks() with those parameters. The result is a dictionary of range indices that must be printed with keys formatted as $`key` followed by the range index representation on the next line, matching R's named list output format.

## Evidence
- ca1440d6104b → score 0.080 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
- {"failure_class": "syntax", "old_code": "print(chunk(1, 100, 10))", "new_code": "result = chunks(from_val=1, to=100, by=10)\nfor key, val in result.items():\n    print(f\"${key}\")\n    print(val)", "score_delta": 0.0799, "script_id": "ca1440d6104b"}
