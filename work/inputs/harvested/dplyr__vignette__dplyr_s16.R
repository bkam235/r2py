# r2py crawler metadata
# package: dplyr
# source_type: vignette
# topic: dplyr_s16
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\doc\dplyr.R
# lines: 7

suppressPackageStartupMessages(library(dplyr))
starwars |>
  mutate(
    height_m = height / 100,
    BMI = mass / (height_m^2)
  ) |>
  select(BMI, everything())