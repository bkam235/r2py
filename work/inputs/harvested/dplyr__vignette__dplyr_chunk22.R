# r2py crawler metadata
# package: dplyr
# source_type: vignette
# topic: dplyr_chunk22
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\doc\dplyr.Rmd
# lines: 8

suppressPackageStartupMessages(library(dplyr))
starwars |>
  group_by(species, sex) |>
  select(height, mass) |>
  summarise(
    height = mean(height, na.rm = TRUE),
    mass = mean(mass, na.rm = TRUE)
  )