# r2py crawler metadata
# package: dplyr
# source_type: vignette
# topic: grouping_s20
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\doc\grouping.R
# lines: 11

suppressPackageStartupMessages(library(dplyr))
# Subtract off global mean
starwars |>
  select(name, homeworld, mass) |>
  mutate(standard_mass = mass - mean(mass, na.rm = TRUE))

# Subtract off homeworld mean
starwars |>
  select(name, homeworld, mass) |>
  group_by(homeworld) |>
  mutate(standard_mass = mass - mean(mass, na.rm = TRUE))