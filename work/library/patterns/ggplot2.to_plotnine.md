---
id: ggplot2.to_plotnine
package: ggplot2
confidence: tentative
seed: true
created: 2026-05-28
last_review: 2026-05-28
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
