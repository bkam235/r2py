---
id: conditional-package-loading-with-is_installed
package: broom
confidence: tentative
seed: false
created: 2026-06-25
last_review: 2026-06-25
tie_count: 0
---

# conditional-package-loading-with-is_installed

## Guidance
`rlang::is_installed()` is documentation scaffolding — a guard that makes R examples optional. In our pipeline the guarded code ALWAYS executes in R, so Python must execute it unconditionally. Remove the `if (rlang::is_installed(...))` guard entirely and translate the code inside the block directly. Do NOT translate this as `importlib.util.find_spec()` — the R package name has no Python equivalent, and the guard would cause the block to be skipped.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
(none)
