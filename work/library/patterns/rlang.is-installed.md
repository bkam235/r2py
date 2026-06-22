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
Translate R `is_installed` (ExternalSymbol from rlang) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "559f1f52", "r_snippet": "if (rlang::is_installed(\"car\")) {", "py_snippet": "def is_installed(package_name):\n    return importlib.util.find_spec(package_name) is not None", "score": 1.0, "script_id": "human-verified"}

## Edit Examples
(none)
