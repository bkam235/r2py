---
id: r-named-arguments-with-special-names--class--title--etc.
package: rlang
confidence: tentative
seed: false
created: 2026-06-30
last_review: 2026-06-30
tie_count: 0
---

# r-named-arguments-with-special-names--class--title--etc.

## Guidance
When translating R named arguments that conflict with Python keywords or conventions (e.g., `class=`), convert them to keyword arguments with underscores (e.g., `class_=`) or use `**{"key": value}` dict unpacking to preserve the original names in the function call representation.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
(none)
