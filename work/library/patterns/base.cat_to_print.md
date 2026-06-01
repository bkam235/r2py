---
id: base.cat_to_print
package: base
confidence: tentative
seed: true
created: 2026-05-28
last_review: 2026-06-01
tie_count: 1
---

# base.cat_to_print

## Guidance
`cat(x)` → `print(x, end="")` (cat does not append newline by default).
`cat(x, "\n")` → `print(x)`. `cat(a, b, sep=", ")` → `print(a, b, sep=", ", end="")`.
`print(x)` in R → `print(x)` in Python (print adds newline in both). Use `str(x)` to
coerce non-string values before printing when cat would produce unexpected repr output.

## Evidence
(none)

## Contradictions
(none)
