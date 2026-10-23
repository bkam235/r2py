# r2py crawler metadata
# package: dplyr
# source_type: vignette
# topic: colwise_s9
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\doc\colwise.R
# lines: 5

suppressPackageStartupMessages(library(dplyr))
starwars |> summarise(
  across(c(height, mass, birth_year), ~min(.x, na.rm = TRUE), .names = "min_{.col}"),
  across(c(height, mass, birth_year), ~max(.x, na.rm = TRUE), .names = "max_{.col}")
)