---
id: base.lapply_to_listcomp
package: base
confidence: tentative
seed: true
created: 2026-05-28
last_review: 2026-05-28
tie_count: 0
---

# base.lapply_to_listcomp

## Guidance
`lapply(x, f)` → `[f(item) for item in x]`. `sapply(x, f)` → `[f(item) for item in x]`
or `np.array([f(item) for item in x])` when the result is numeric. `vapply(x, f, type)` →
list comprehension with the appropriate Python type. `Map(f, x, y)` → `[f(a, b) for a, b
in zip(x, y)]`. When f has extra arguments use a lambda: `lapply(x, f, extra=v)` →
`[f(item, extra=v) for item in x]`.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "1b785ce7", "r_snippet": "suppressPackageStartupMessages(library(bit))", "py_snippet": "warnings.filterwarnings('ignore')", "score": 1.0, "script_id": "0f2136d787dc"}
- {"r_hash": "9f4ae2da", "r_snippet": "suppressPackageStartupMessages(library(broom))", "py_snippet": "warnings.filterwarnings('ignore')", "score": 1.0, "script_id": "4e102aa60f9d"}

## Edit Examples
(none)
