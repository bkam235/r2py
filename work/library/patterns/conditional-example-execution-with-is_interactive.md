---
id: conditional-example-execution-with-is_interactive
package: rlang
confidence: tentative
seed: false
created: 2026-06-30
last_review: 2026-06-30
tie_count: 0
---

# conditional-example-execution-with-is_interactive

## Guidance
When R code wraps examples in `if (rlang::is_interactive()) { ... }`, translate `is_interactive()` using `sys.stdin.isatty()` and wrap the example block in a Python `if is_interactive():` statement. Include `print()` statements that echo the R syntax for documentation/debugging.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
(none)
