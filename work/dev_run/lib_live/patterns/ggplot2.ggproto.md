---
id: ggplot2.ggproto
package: ggplot2
confidence: tentative
seed: true
created: 2026-09-30
last_review: 2026-09-30
tie_count: 0
---

# ggplot2.ggproto

## Guidance
Translate R `ggproto` (FunctionCall from ggplot2) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "07f6dec9", "r_snippet": "GeomSimplePoint <- ggproto(\"GeomSimplePoint\", Geom,\n  required_aes = c(\"x\", \"y\"),\n  default_aes = aes(shape = 19, colour = \"black\"),\n  draw_key = draw_key_point,\n\n  draw_panel = function(data, panel_params, coord) {\n    coords <- coord$transform(data, panel_params)\n    grid::pointsGrob(\n      coords$x, coords$y,\n      pch = coords$shape,\n      gp = grid::gpar(col = coords$colour)\n    )\n  }\n)", "py_snippet": "# In plotnine (the Python implementation of ggplot2), \n# custom Geoms are handled via the underlying matplotlib engine.\n# Since plotnine does not expose the ggproto API for creating \n# custom low-level drawing functions like draw_panel in the same way R does,\n# the equivalent functional behavior is achieved using geom_point.\n\n# The R code defines a 'SimplePoint' that mimics the default behavior of geom_point\n# (shape 19, black color).\n\n# To replicate the logic of the provided R snippet:\nd = mpg\n\n# The plot call", "score": 0.92, "script_id": "ggplot2__vignette__extending-ggplot2_s16", "n_calls": 0}

## Edit Examples
(none)
