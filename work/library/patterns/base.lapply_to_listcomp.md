---
id: base.lapply_to_listcomp
package: base
confidence: tentative
seed: true
created: 2026-05-28
last_review: 2026-05-28
---

# base.lapply_to_listcomp

## Guidance
`lapply(x, f)` → `[f(item) for item in x]`. `sapply(x, f)` → `[f(item) for item in x]`
or `np.array([f(item) for item in x])` when the result is numeric. `vapply(x, f, type)` →
list comprehension with the appropriate Python type. `Map(f, x, y)` → `[f(a, b) for a, b
in zip(x, y)]`. When f has extra arguments use a lambda: `lapply(x, f, extra=v)` →
`[f(item, extra=v) for item in x]`.

## Evidence
(none)

## Contradictions
(none)
