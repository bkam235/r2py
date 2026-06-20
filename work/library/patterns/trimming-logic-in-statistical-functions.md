---
id: trimming-logic-in-statistical-functions
package: purrr
confidence: tentative
seed: false
created: 2026-06-20
last_review: 2026-06-20
tie_count: 0
---

# trimming-logic-in-statistical-functions

## Guidance
When implementing R's trim parameter (e.g., in mean), check `trim_count > 0` before slicing to avoid returning empty lists when trim would exclude all values. This matches R's behavior of raising an error rather than returning NaN for invalid trims.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
(none)
