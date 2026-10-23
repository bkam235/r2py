# r2py crawler metadata
# package: tidyr
# source_type: vignette
# topic: pivot_s23
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tidyr\doc\pivot.R
# lines: 7

suppressPackageStartupMessages(library(tidyr))
warpbreaks |>
  pivot_wider(
    names_from = wool,
    values_from = breaks,
    values_fn = mean
  )