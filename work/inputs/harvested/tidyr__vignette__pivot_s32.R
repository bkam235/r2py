# r2py crawler metadata
# package: tidyr
# source_type: vignette
# topic: pivot_s32
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tidyr\doc\pivot.R
# lines: 16

suppressPackageStartupMessages(library(tidyr))
percentages <- tibble(
  year = c(2018, 2019, 2020, 2020),
  type = factor(c("A", "B", "A", "B"), levels = c("A", "B")),
  percentage = c(100, 100, 40, 60)
)

percentages

percentages |>
  pivot_wider(
    names_from = c(year, type),
    values_from = percentage,
    names_expand = TRUE,
    values_fill = 0
  )