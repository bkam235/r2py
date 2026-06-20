---
id: r-raw-complex-vector-allocation
package: bit
confidence: tentative
seed: false
created: 2026-06-19
last_review: 2026-06-19
tie_count: 0
---

# r-raw-complex-vector-allocation

## Guidance
Translate R's `raw(n)` to Python's `bytes(n)` and `complex(n)` to `np.zeros(n, dtype=np.complex128)` to match the memory footprint and length properties used for byte-size calculations.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
(none)
