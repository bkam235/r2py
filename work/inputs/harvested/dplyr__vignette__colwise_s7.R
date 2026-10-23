# r2py crawler metadata
# package: dplyr
# source_type: vignette
# topic: colwise_s7
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\doc\colwise.R
# lines: 7

suppressPackageStartupMessages(library(dplyr))
min_max <- list(
  min = ~min(.x, na.rm = TRUE),
  max = ~max(.x, na.rm = TRUE)
)
starwars |> summarise(across(where(is.numeric), min_max))
starwars |> summarise(across(c(height, mass, birth_year), min_max))