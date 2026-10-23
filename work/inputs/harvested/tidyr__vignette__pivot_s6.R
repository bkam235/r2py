# r2py crawler metadata
# package: tidyr
# source_type: vignette
# topic: pivot_s6
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tidyr\doc\pivot.R
# lines: 8

suppressPackageStartupMessages(library(tidyr))
billboard |>
  pivot_longer(
    cols = starts_with("wk"),
    names_to = "week",
    values_to = "rank",
    values_drop_na = TRUE
  )