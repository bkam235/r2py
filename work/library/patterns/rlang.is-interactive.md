---
id: rlang.is-interactive
package: rlang
confidence: tentative
seed: true
created: 2026-07-04
last_review: 2026-07-04
tie_count: 0
---

# rlang.is-interactive

## Guidance
Translate R `is_interactive` (ExternalSymbol from rlang) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "19e0f1d8", "r_snippet": "if (rlang::is_interactive()) withAutoprint({ # examplesIf", "py_snippet": "def is_interactive() -> bool:\n    \"\"\"\n    Check if running in an interactive context.\n    \"\"\"\n    # Check for knitr in progress\n    import os\n    if os.getenv(\"TESTTHAT\") == \"true\":\n        return False\n    # Simplified version for Python\n    try:\n        return hasattr(sys, 'ps1') or sys.flags.debug\n    except:\n        return False", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)
