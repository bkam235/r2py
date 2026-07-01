---
id: graceful-import-error-handling
package: rlang
confidence: tentative
seed: false
created: 2026-07-01
last_review: 2026-07-01
tie_count: 0
---

# graceful-import-error-handling

## Guidance
Wrap optional package imports (bslib, shinywidgets) in try-except blocks at the function level rather than duplicating imports; move imports inside the interactive block to avoid import failures when packages are unavailable.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
(none)
