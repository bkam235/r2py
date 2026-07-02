---
id: r-package-conditionals-with-is_installed
package: base
confidence: tentative
seed: false
created: 2026-07-02
last_review: 2026-07-02
tie_count: 0
---

# r-package-conditionals-with-is_installed

## Guidance
`rlang::is_installed()` is documentation scaffolding — a guard that makes R examples optional. In our pipeline the guarded code ALWAYS executes in R, so Python must execute it unconditionally. Remove the `if (rlang::is_installed(...))` guard entirely and translate the code inside the block directly. Do NOT use `importlib.util.find_spec()` — the R package name has no Python equivalent.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
(none)
