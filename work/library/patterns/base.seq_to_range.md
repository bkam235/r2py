---
id: base.seq_to_range
package: base
confidence: tentative
seed: true
created: 2026-05-28
last_review: 2026-05-28
---

# base.seq_to_range

## Guidance
`seq(1, n)` or `1:n` → `range(1, n+1)` (R is 1-based inclusive; Python range is
0-based exclusive). `seq(from, to, by=step)` → `np.arange(from, to+step, step)` for
numeric sequences. `seq_len(n)` → `range(n)` (0-based Python) — note the index shift.
`seq_along(x)` → `range(len(x))`. When used as a vector, wrap with `list(...)` or
`np.array(...)`.

## Evidence
(none)

## Contradictions
(none)
