---
id: base.sprintf_to_fstring
package: base
confidence: tentative
seed: true
created: 2026-05-28
last_review: 2026-05-28
---

# base.sprintf_to_fstring

## Guidance
`sprintf("%.2f", x)` → `f"{x:.2f}"`. `sprintf("%d items", n)` → `f"{n:d} items"`.
`sprintf("%s and %s", a, b)` → `f"{a} and {b}"`. When sprintf is called with a
vector of values, use a list comprehension. Note R's `%i` is equivalent to `%d` in
Python format strings.

## Evidence
(none)

## Contradictions
(none)
