# r2py crawler metadata
# package: tidyr
# source_type: vignette
# topic: pivot_s51
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tidyr\doc\pivot.R
# lines: 8

suppressPackageStartupMessages(library(tidyr))
spec <- relig_income |>
  build_longer_spec(
    cols = !religion,
    names_to = "income",
    values_to = "count"
  )
pivot_longer_spec(relig_income, spec)