---
id: r-triple-colon-namespace-access
package: plyr
confidence: tentative
seed: false
created: 2026-06-21
last_review: 2026-06-21
tie_count: 0
---

# r-triple-colon-namespace-access

## Guidance
R's `package:::function()` syntax accesses internal functions; in Python, translate to direct function calls after defining or importing the function, as the package structure is not directly translatable.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
(none)
