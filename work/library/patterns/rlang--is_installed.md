---
id: rlang--is_installed
package: broom
confidence: tentative
seed: false
created: 2026-06-21
last_review: 2026-07-01
tie_count: 0
---

# rlang--is_installed

## Guidance
`rlang::is_installed("pkg")` is documentation scaffolding — a guard that makes R examples optional so they skip gracefully when a suggested package is missing. In our pipeline the guarded code ALWAYS executes in R (the package is installed), so Python must execute it unconditionally. Remove the `if is_installed(...)` guard entirely and translate the code inside the block directly.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
(none)
