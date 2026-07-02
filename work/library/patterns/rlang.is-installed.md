---
id: rlang.is-installed
package: rlang
confidence: tentative
seed: true
created: 2026-06-22
last_review: 2026-06-22
tie_count: 0
---

# rlang.is-installed

## Guidance
`rlang::is_installed()` is documentation scaffolding — a guard that makes R examples optional. In our pipeline the guarded code ALWAYS executes in R, so Python must execute it unconditionally. Remove the `if (rlang::is_installed(...))` guard and translate the code inside the block directly.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "559f1f52", "r_snippet": "if (rlang::is_installed(\"car\")) {", "py_snippet": "# is_installed guard removed — execute code unconditionally", "score": 1.0, "script_id": "human-verified"}

## Edit Examples
(none)
