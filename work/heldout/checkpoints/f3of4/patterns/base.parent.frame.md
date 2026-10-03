---
id: base.parent.frame
package: base
confidence: tentative
seed: true
created: 2026-09-22
last_review: 2026-09-22
tie_count: 0
---

# base.parent.frame

## Guidance
Translate R `parent.frame` from base to Python. The verified example below uses it inside a statement that may call other functions too.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "bee76ee3", "r_snippet": "renderFoo <- function(expr, env = parent.frame(), quoted = FALSE) {\n  if (!quoted) { expr <- substitute(expr) } # force quoted\n  htmlwidgets::shinyRenderWidget(expr, fooOutput, env, quoted = TRUE)\n}", "py_snippet": "def renderFoo(expr):\n    return render.ui(expr)", "score": 1.0, "script_id": "htmlwidgets__rd_example__htmlwidgets-shiny_Rd", "n_calls": 2}

## Edit Examples
(none)
