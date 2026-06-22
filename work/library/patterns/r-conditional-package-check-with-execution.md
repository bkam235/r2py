---
id: r-conditional-package-check-with-execution
package: broom
confidence: tentative
seed: false
created: 2026-06-22
last_review: 2026-06-22
tie_count: 0
---

# r-conditional-package-check-with-execution

## Guidance
Translate `if (rlang::is_installed("package")) { ... }` to a Python function that checks package availability and wraps the conditional block; use `importlib.util.find_spec()` to test if a package can be imported.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
(none)
