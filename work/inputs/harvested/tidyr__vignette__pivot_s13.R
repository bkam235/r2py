# r2py crawler metadata
# package: tidyr
# source_type: vignette
# topic: pivot_s13
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tidyr\doc\pivot.R
# lines: 8

suppressPackageStartupMessages(library(tidyr))
household |>
  pivot_longer(
    cols = !family,
    names_to = c(".value", "child"),
    names_sep = "_",
    values_drop_na = TRUE
  )