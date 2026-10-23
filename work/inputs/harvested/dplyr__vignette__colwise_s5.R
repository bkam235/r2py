# r2py crawler metadata
# package: dplyr
# source_type: vignette
# topic: colwise_s5
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\doc\colwise.R
# lines: 13

suppressPackageStartupMessages(library(dplyr))
starwars |>
  summarise(across(where(is.character), n_distinct))

starwars |>
  group_by(species) |>
  filter(n() > 1) |>
  summarise(across(c(sex, gender, homeworld), n_distinct))

starwars |>
  group_by(homeworld) |>
  filter(n() > 1) |>
  summarise(across(where(is.numeric), ~ mean(.x, na.rm = TRUE)))