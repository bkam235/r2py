# r2py crawler metadata
# package: dplyr
# source_type: vignette
# topic: programming_s21
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\doc\programming.R
# lines: 8

suppressPackageStartupMessages(library(dplyr))
my_summarise <- function(data, summary_vars) {
  data |>
    summarise(across({{ summary_vars }}, ~ mean(., na.rm = TRUE)))
}
starwars |>
  group_by(species) |>
  my_summarise(c(mass, height))