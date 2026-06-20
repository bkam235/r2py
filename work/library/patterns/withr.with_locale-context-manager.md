---
id: withr.with_locale-context-manager
package: 
confidence: tentative
seed: false
created: 2026-06-16
last_review: 2026-06-16
tie_count: 0
---

# withr.with_locale-context-manager

## Guidance
withr::with_locale() in R executes code immediately within a temporary locale context. When translated, use a context manager generator that yields after executing the code parameter, allowing both direct code execution and 'with' statement usage.

## Evidence
- 021894dec169 → score 0.001 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
- {"failure_class": "graphics", "old_code": "@contextlib.contextmanager\ndef with_locale(new, code=None):\n    \"\"\"\n    Context manager for temporarily modified locale settings.\n    Supports both context manager syntax and code parameter.\n    \n    Args:\n        new: dict mapping locale category names (e.g., \"LC_TIME\") to locale strings\n        co", "new_code": "@contextlib.contextmanager\ndef with_locale(new, code=None):\n    \"\"\"\n    Context manager for temporarily modified locale settings.\n    When code is provided, executes it immediately within the locale context.\n    Otherwise works as a context manager for use with 'with' statements.\n    \n    Args:\n    ", "score_delta": 0.0006, "script_id": "021894dec169"}
