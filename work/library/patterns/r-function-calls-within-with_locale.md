---
id: r-function-calls-within-with_locale
package: withr
confidence: tentative
seed: false
created: 2026-06-19
last_review: 2026-06-19
tie_count: 0
---

# r-function-calls-within-with_locale

## Guidance
When R code calls functions inside with_locale (e.g., format(), sort()), translate the function call directly into the Python `with` block instead of wrapping it in a lambda or separate callable parameter.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
(none)
