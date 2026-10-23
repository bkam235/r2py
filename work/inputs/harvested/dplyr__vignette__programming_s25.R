# r2py crawler metadata
# package: dplyr
# source_type: vignette
# topic: programming_s25
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\doc\programming.R
# lines: 4

suppressPackageStartupMessages(library(dplyr))
mtcars |>
  names() |>
  purrr::map(~ count(mtcars, .data[[.x]]))