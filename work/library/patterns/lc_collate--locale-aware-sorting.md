---
id: lc_collate--locale-aware-sorting
package: withr
confidence: tentative
seed: false
created: 2026-06-19
last_review: 2026-06-19
tie_count: 0
---

# lc_collate--locale-aware-sorting

## Guidance
When translating R's locale-based sorting, use Python's sorted() with key=locale.strcoll to ensure the current locale settings are actually applied to the string comparison.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
(none)
