---
id: fix-duplicate-variable-name
package: 
confidence: tentative
seed: false
created: 2026-06-06
last_review: 2026-06-06
tie_count: 0
---

# fix-duplicate-variable-name

## Guidance
When translating R function calls to Python, ensure variable names referenced in function arguments match the actual variable names in scope. This is particularly important when colormaps or other objects are created with specific naming conventions.

## Evidence
- dd2e0ea0b08b → score 0.190 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
- {"failure_class": "stdout", "old_code": "contourf = ax.contourf(volcano, levels=15, cmap=graycol_colormap_colormap, aspect=1)", "new_code": "contourf = ax.contourf(volcano, levels=15, cmap=graycol_colormap, aspect=1)", "score_delta": 0.19, "script_id": "dd2e0ea0b08b"}
