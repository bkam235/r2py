---
id: r-package-placeholder
package: shape
confidence: tentative
seed: false
created: 2026-06-08
last_review: 2026-06-08
tie_count: 0
---

# r-package-placeholder

## Guidance
When an R package has no direct Python 1:1 equivalent and is used for utility/plotting, replace the stub with a descriptive comment and pass.

## Evidence
- dd2e0ea0b08b → score 0.002 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
- {"failure_class": "warnings", "old_code": "pass  # untranslatable: R package 'shape' has no direct Python equivalent; shape drawing requires matplotlib.patches or similar, with different API", "new_code": "# R package 'shape' provides functions for shape analysis and drawing.\n# Typical Python equivalents are scipy.spatial for geometry or matplotlib for visualization.\npass", "score_delta": 0.0016, "script_id": "dd2e0ea0b08b"}
