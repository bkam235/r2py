---
id: callable-string-argument-polymorphism
package: timeDate
confidence: tentative
seed: false
created: 2026-06-20
last_review: 2026-06-20
tie_count: 0
---

# callable-string-argument-polymorphism

## Guidance
For R functions that accept either a string identifier or a function object as an argument (e.g., `Holiday = "Easter"` vs `Holiday = Easter`), use a mapping dictionary in Python to resolve the string to the corresponding callable.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
(none)
