---
id: lift_dl--dict-list-to-function-arguments
package: purrr
confidence: tentative
seed: true
created: 2026-06-20
last_review: 2026-06-20
tie_count: 0
---

# lift_dl--dict-list-to-function-arguments

## Guidance
When lifting a function with `lift_dl()`, the returned wrapper should accept a dict or list and expand its contents as function arguments. If a dict has an 'x' key, use it as the first positional argument; merge remaining keys as kwargs after converting dot notation to underscores.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "ebdeea84", "r_snippet": "suppressPackageStartupMessages(library(purrr))", "py_snippet": "# purrr library import\npass\n\n# mtcars dataset (built-in R dataset)\nmtcars = {\n    'mpg': [21.0, 21.0, 22.8, 21.4, 18.7, 18.1, 14.3, 24.4, 22.8, 19.2, 17.8, 16.4, 17.3, 15.2, 10.4, 10.4, 14.7, 32.4, 30.4, 33.9, 21.5, 15.5, 15.2, 13.3, 19.2, 27.3, 26.0, 30.4, 15.8, 19.7, 15.0, 21.4],\n    'cyl': [6, 6, 4, 6, 8, 6, 8, 4, 4, 6, 6, 8, 8, 8, 8, 8, 8, 4, 4, 4, 4, 8, 8, 8, 8, 4, 4, 4, 8, 6, 8, 4],\n    'disp': [160.0, 160.0, 108.0, 258.0, 360.0, 225.0, 360.0, 146.7, 140.8, 167.6, 167.6, 275.8, 275.8, 275.8, 472.0, 460.0, 440.0, 78.7, 75.7, 71.1, 120.1, 318.0, 304.0, 350.0, 400.0, 79.0, 120.3, 95.1, 351.", "score": 0.7667, "script_id": "ca3c7c4facac"}

## Edit Examples
(none)
