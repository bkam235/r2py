---
id: library---call-in-conditional-blocks
package: broom
confidence: tentative
seed: false
created: 2026-06-22
last_review: 2026-06-22
tie_count: 0
---

# library---call-in-conditional-blocks

## Guidance
When a library call is wrapped in a check like rlang::is_installed(), use a corresponding Python check (e.g., importlib.util.find_spec) and print the original R command to maintain session-like logs.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
(none)
