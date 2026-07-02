---
id: r-conditional-execution-with-rlang--is_installed
package: broom
confidence: tentative
seed: false
created: 2026-06-24
last_review: 2026-06-24
tie_count: 0
---

# r-conditional-execution-with-rlang--is_installed

## Guidance
`rlang::is_installed()` is documentation scaffolding — a guard that makes R examples optional. In our pipeline the guarded code ALWAYS executes in R, so Python must execute it unconditionally. Remove the `if (rlang::is_installed(...))` guard entirely and translate the code inside the block directly.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
(none)
