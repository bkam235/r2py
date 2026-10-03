---
id: ggplot2.make-constructor
package: ggplot2
confidence: tentative
seed: true
created: 2026-09-30
last_review: 2026-09-30
tie_count: 0
---

# ggplot2.make-constructor

## Guidance
Translate R `make_constructor` (FunctionCall from ggplot2) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "71dad4ca", "r_snippet": "geom_simple_point <- make_constructor(GeomSimplePoint)", "py_snippet": "from plotnine import ggplot, aes, geom_point\nfrom plotnine.data import mpg", "score": 0.92, "script_id": "ggplot2__vignette__extending-ggplot2_s16", "n_calls": 0}

## Edit Examples
(none)
