---
id: locale-aware-sorting
package: withr
confidence: tentative
seed: false
created: 2026-06-19
last_review: 2026-06-19
tie_count: 0
---

# locale-aware-sorting

## Guidance
When translating R's `sort()` with a specific `LC_COLLATE` locale, use Python's `sorted()` with `key=locale.strcoll` after setting the locale.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
(none)
