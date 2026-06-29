---
id: r-list-named-vector-return-to-python-custom-class
package: bit
confidence: tentative
seed: false
created: 2026-06-28
last_review: 2026-06-28
tie_count: 0
---

# r-list-named-vector-return-to-python-custom-class

## Guidance
When an R function returns a named list/vector meant for display (like chunks() returning indexed ranges), wrap the dictionary in a custom class that implements __repr__, __getitem__, items(), keys(), and values() to preserve both printability and dict-like access.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
(none)
