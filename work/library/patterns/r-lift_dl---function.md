---
id: r-lift_dl---function
package: purrr
confidence: tentative
seed: false
created: 2026-06-20
last_review: 2026-06-20
tie_count: 0
---

# r-lift_dl---function

## Guidance
Translate R's lift_dl(f, **defaults) to a Python wrapper function that accepts a dict or list, merges defaults with input arguments, and unpacks them into the target function using **kwargs. Handle dict inputs by merging defaults and the input dict, with input taking precedence.

Translate lift_dl(f) as a Python function that returns a wrapper accepting a dict/list and expanding it as arguments to f. Handle dict keys as kwargs (converting dots to underscores) and extract 'x' key as positional argument if present.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
(none)
