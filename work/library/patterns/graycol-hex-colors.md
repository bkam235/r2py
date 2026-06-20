---
id: graycol-hex-colors
package: 
confidence: tentative
seed: false
created: 2026-06-13
last_review: 2026-06-13
tie_count: 0
---

# graycol-hex-colors

## Guidance
R's shape::graycol(n) returns a vector of n grayscale color hex codes. In Python, generate an equivalent list of hex color strings by interpolating from black (#000000) to white (#ffffff) across n values.

## Evidence
- d42c7e223bcd → score 0.071 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
- {"failure_class": "files", "old_code": "graycol(10)", "new_code": "[f'#{int(255*i/9):02x}{int(255*i/9):02x}{int(255*i/9):02x}' for i in range(10)]", "score_delta": 0.0714, "script_id": "d42c7e223bcd"}
