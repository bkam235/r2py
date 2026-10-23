# r2py crawler metadata
# package: tidyr
# source_type: vignette
# topic: pivot_chunk7
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tidyr\doc\pivot.Rmd
# lines: 10

suppressPackageStartupMessages(library(tidyr))
billboard |>
  pivot_longer(
    cols = starts_with("wk"),
    names_to = "week",
    names_prefix = "wk",
    names_transform = as.integer,
    values_to = "rank",
    values_drop_na = TRUE,
  )