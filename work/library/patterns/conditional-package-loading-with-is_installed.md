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
Use `if is_installed(package_name):` to conditionally execute code blocks that depend on optional packages, replacing R's `if (rlang::is_installed(...)) { ... }` pattern. This allows graceful handling of missing dependencies in Python.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
(none)
