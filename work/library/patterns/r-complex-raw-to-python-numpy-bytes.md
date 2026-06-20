---
id: r-complex-raw-to-python-numpy-bytes
package: bit
confidence: tentative
seed: false
created: 2026-06-19
last_review: 2026-06-19
tie_count: 0
---

# r-complex-raw-to-python-numpy-bytes

## Guidance
Translate R's `complex(n)` to `np.zeros(n, dtype=np.complex128)` and `raw(n)` to `bytes(n)` or a numpy array with `dtype.kind` in ('u', 'i').

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
(none)
