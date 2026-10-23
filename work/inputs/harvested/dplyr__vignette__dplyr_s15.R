# r2py crawler metadata
# package: dplyr
# source_type: vignette
# topic: dplyr_s15
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\doc\dplyr.R
# lines: 4

suppressPackageStartupMessages(library(dplyr))
starwars |>
  mutate(height_m = height / 100) |>
  select(height_m, height, everything())