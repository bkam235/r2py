---
id: r-package-to-python-library
package: shape
confidence: tentative
seed: false
created: 2026-06-08
last_review: 2026-06-08
tie_count: 0
---

# r-package-to-python-library

## Guidance
Translate R package imports to their nearest Python equivalents or a comment if the functionality is provided by already imported libraries (like numpy/matplotlib).

## Evidence
- dd2e0ea0b08b → score 0.002 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
- {"failure_class": "warnings", "old_code": "pass  # untranslatable: R package 'shape' has no direct Python equivalent; shape drawing requires matplotlib.patches or similar, with different API", "new_code": "# No specific import needed for basic shape analysis if using numpy/matplotlib", "score_delta": 0.0024, "script_id": "dd2e0ea0b08b"}
