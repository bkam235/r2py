# r2py crawler metadata
# package: tidyr
# source_type: vignette
# topic: pivot_s15
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tidyr\doc\pivot.R
# lines: 8

suppressPackageStartupMessages(library(tidyr))
anscombe |>
  pivot_longer(
    cols = everything(),
    cols_vary = "slowest",
    names_to = c(".value", "set"),
    names_pattern = "(.)(.)"
  )