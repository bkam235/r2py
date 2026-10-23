# r2py crawler metadata
# package: tidyr
# source_type: vignette
# topic: pivot_chunk8
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tidyr\doc\pivot.Rmd
# lines: 9

suppressPackageStartupMessages(library(tidyr))
billboard |>
  pivot_longer(
    cols = starts_with("wk"),
    names_to = "week",
    names_transform = readr::parse_number,
    values_to = "rank",
    values_drop_na = TRUE,
  )