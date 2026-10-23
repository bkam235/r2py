# r2py crawler metadata
# package: dplyr
# source_type: vignette
# topic: programming_s17
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\doc\programming.R
# lines: 9

suppressPackageStartupMessages(library(dplyr))
my_summarise <- function(.data, ...) {
  .data |>
    group_by(...) |>
    summarise(mass = mean(mass, na.rm = TRUE), height = mean(height, na.rm = TRUE))
}

starwars |> my_summarise(homeworld)
starwars |> my_summarise(sex, gender)