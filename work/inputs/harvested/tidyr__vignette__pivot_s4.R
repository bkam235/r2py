# r2py crawler metadata
# package: tidyr
# source_type: vignette
# topic: pivot_s4
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tidyr\doc\pivot.R
# lines: 7

suppressPackageStartupMessages(library(tidyr))
relig_income |>
  pivot_longer(
    cols = !religion,
    names_to = "income",
    values_to = "count"
  )