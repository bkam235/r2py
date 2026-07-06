---
id: ggplot2.facet-wrap
package: ggplot2
confidence: tentative
seed: true
created: 2026-07-06
last_review: 2026-07-06
tie_count: 0
---

# ggplot2.facet-wrap

## Guidance
Translate R `facet_wrap` (FunctionCall from ggplot2) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "5b56d202", "r_snippet": "    facet_wrap(~year)", "py_snippet": "    + facet_wrap('~year')\n)\n\n# To match R's output behavior where the plot is generated (and possibly shown)\nprint(plot)", "score": 0.9, "script_id": "auto"}

## Edit Examples
(none)
