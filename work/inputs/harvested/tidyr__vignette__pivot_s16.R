# r2py crawler metadata
# package: tidyr
# source_type: vignette
# topic: pivot_s16
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tidyr\doc\pivot.R
# lines: 17

suppressPackageStartupMessages(library(tidyr))
pnl <- tibble(
  x = 1:4,
  a = c(1, 1,0, 0),
  b = c(0, 1, 1, 1),
  y1 = rnorm(4),
  y2 = rnorm(4),
  z1 = rep(3, 4),
  z2 = rep(-2, 4),
)

pnl |>
  pivot_longer(
    cols = !c(x, a, b),
    names_to = c(".value", "time"),
    names_pattern = "(.)(.)"
  )