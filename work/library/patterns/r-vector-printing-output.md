---
id: r-vector-printing-output
package: base
confidence: tentative
seed: false
created: 2026-06-29
last_review: 2026-06-29
tie_count: 0
---

# r-vector-printing-output

## Guidance
When printing R vectors in Python output, use print(f"[1] {' '.join(map(str, vector))}") for numeric vectors and f"[1] {' '.join(str(v).upper() for v in vector)}" for logical vectors to match R's display format.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
(none)
