---
id: chunk-length-dispatch
package: 
confidence: tentative
seed: false
created: 2026-06-18
last_review: 2026-06-18
tie_count: 0
---

# chunk-length-dispatch

## Guidance
When chunk(x) is called with a non-NULL vector/scalar, R dispatches to chunk.default which extracts length(x) and calls chunks() with from=1, to=length(x), and appropriate length.out. In Python, directly call chunks() with the extracted length and format output with backticks around range labels to match R's list printing format.

## Evidence
- ca1440d6104b → score 0.083 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
- {"failure_class": "syntax", "old_code": "result = chunk(complex(int(1e7)))", "new_code": "# chunk dispatches to chunk.default which extracts length and calls chunks\nx_val = complex(int(1e7))\nresult = chunks(from_val=1, to_val=int(1e7), length_out=10, maxindex=int(1e7))\n# Format output with backticks in keys\nfor key in result:\n    print(f'$`{key}`')\n    print(result[key])\n    print()", "score_delta": 0.083, "script_id": "ca1440d6104b"}
