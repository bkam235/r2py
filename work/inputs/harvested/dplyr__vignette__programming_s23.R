# r2py crawler metadata
# package: dplyr
# source_type: vignette
# topic: programming_s23
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\doc\programming.R
# lines: 6

suppressPackageStartupMessages(library(dplyr))
my_summarise <- function(data, group_var, summarise_var) {
  data |>
    group_by(pick({{ group_var }})) |>
    summarise(across({{ summarise_var }}, mean, .names = "mean_{.col}"))
}