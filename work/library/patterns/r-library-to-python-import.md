---
id: r-library-to-python-import
package: 
confidence: contradicted
seed: false
created: 2026-06-08
last_review: 2026-06-08
tie_count: 6
---

# r-library-to-python-import

## Guidance
Translate R's library() loading, potentially wrapped in suppressPackageStartupMessages(), to the appropriate Python import statements. If the package has no direct equivalent, use a comment to indicate the intended functionality.

## Evidence
- dd2e0ea0b08b → score 0.002 (path: exact, variable: )
- dd2e0ea0b08b → score 0.005 (path: exact, variable: )
- dd2e0ea0b08b → score 0.002 (path: exact, variable: )

## Contradictions
- dd2e0ea0b08b/: score regressed to 0.482
- dd2e0ea0b08b/: score regressed to 0.482
- dd2e0ea0b08b/: score regressed to 0.351
- dd2e0ea0b08b/: score regressed to 0.486
- dd2e0ea0b08b/: score regressed to 0.482
- dd2e0ea0b08b/: score regressed to 0.484

## Translation Examples
(none)

## Edit Examples
- {"failure_class": "warnings", "old_code": "pass  # suppressPackageStartupMessages(library(shape))", "new_code": "# library(shape) is not required as functionality is provided by numpy/matplotlib/scipy", "score_delta": 0.0047, "script_id": "dd2e0ea0b08b"}
- {"failure_class": "warnings", "old_code": "pass  # suppressPackageStartupMessages(library(shape))", "new_code": "# suppressPackageStartupMessages(library(shape))\npass", "score_delta": 0.0024, "script_id": "dd2e0ea0b08b"}
- {"failure_class": "warnings", "old_code": "pass  # untranslatable: R package 'shape' has no direct Python equivalent; shape drawing requires matplotlib.patches or similar, with different API", "new_code": "# suppressPackageStartupMessages(library(shape))\n# Python doesn't have a direct equivalent to the 'shape' package for all its functionality,\n# but we import the necessary libraries for plotting below.", "score_delta": 0.0016, "script_id": "dd2e0ea0b08b"}
