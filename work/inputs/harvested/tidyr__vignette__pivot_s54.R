# r2py crawler metadata
# package: tidyr
# source_type: vignette
# topic: pivot_s54
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tidyr\doc\pivot.R
# lines: 7

suppressPackageStartupMessages(library(tidyr))
spec1 <- us_rent_income |>
  build_wider_spec(
    names_from = variable,
    values_from = c(estimate, moe)
  )
spec1