---
id: r-library-stub
package: 
confidence: tentative
seed: false
created: 2026-06-08
last_review: 2026-06-08
tie_count: 0
---

# r-library-stub

## Guidance
R's library() calls, especially wrapped in suppressPackageStartupMessages, are side-effectual imports. In Python, these are translated to import statements at the top of the file; if the functionality is already covered by other imports (like numpy or matplotlib), a comment suffices.

## Evidence
- dd2e0ea0b08b → score 0.007 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
- {"failure_class": "warnings", "old_code": "pass  # suppressPackageStartupMessages(library(shape))", "new_code": "# Library 'shape' in R is often for data manipulation or plotting utilities;\n# Python equivalent is usually handled by numpy/matplotlib/scipy already imported.", "score_delta": 0.0071, "script_id": "dd2e0ea0b08b"}
