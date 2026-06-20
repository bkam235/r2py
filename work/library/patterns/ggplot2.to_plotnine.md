---
id: ggplot2.to_plotnine
package: ggplot2
confidence: tentative
seed: true
created: 2026-05-28
last_review: 2026-05-28
tie_count: 0
---

# ggplot2.to_plotnine

## Guidance
Translate ggplot2 code to plotnine (`from plotnine import *`). The grammar is nearly
identical: `ggplot(df, aes(x=col, y=col))` → `ggplot(df, aes(x="col", y="col"))`
(column names are quoted strings in plotnine). `geom_point()`, `geom_line()`,
`geom_bar()`, `facet_wrap()`, `theme_*()` all have direct equivalents. Save with
`p.save("file.png")` instead of `ggsave`. If plotnine is unavailable, fall back to
matplotlib with `plt.scatter` / `plt.plot` and note the approximation.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "a1c1297b", "r_snippet": "  library(ggplot2)", "py_snippet": "if has_ggplot2:\n    # Process the data for plotting\n    # r2py:entity:filter\n    df_filtered = storms[storms['year'] >= 2000].copy()\n    \n    # Create the combined column for the color aesthetic: paste(year, name)\n    df_filtered['year_name'] = df_filtered['year'].astype(str) + \" \" + df_filtered['name']\n\n    # r2py:entity:ggplot\n    # r2py:entity:geom_path\n    # r2py:entity:facet_wrap\n    p = (\n        ggplot(df_filtered, aes(x='long', y='lat', color='year_name')) +\n        geom_path(show_legend=False) +\n        facet_wrap('~year')\n    )\n    print(p)\n\nprint(storms)", "score": 0.9333, "script_id": "aeb58d2582e6"}

## Edit Examples
(none)
