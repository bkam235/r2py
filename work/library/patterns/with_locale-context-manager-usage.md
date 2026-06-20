---
id: with_locale-context-manager-usage
package: withr
confidence: tentative
seed: false
created: 2026-06-19
last_review: 2026-06-19
tie_count: 0
---

# with_locale-context-manager-usage

## Guidance
R's with_locale() should translate to Python's `with` statement using a context manager that sets locale, executes code in the block, and restores locale in finally. The code block itself goes in the `with` body, not as a separate `code=` parameter.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
(none)
