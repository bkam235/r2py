---
id: dplyr--filter
package: dplyr
confidence: tentative
seed: false
created: 2026-06-20
last_review: 2026-06-20
tie_count: 0
---

# dplyr--filter

## Guidance
Translate `filter()` to pandas boolean indexing, e.g., `df[df['column'] >= value]`, and use `.copy()` if the resulting DataFrame will be modified.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
(none)
