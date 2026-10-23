# r2py crawler metadata
# package: dplyr
# source_type: vignette
# topic: programming_s13
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\doc\programming.R
# lines: 6

suppressPackageStartupMessages(library(dplyr))
my_summarise <- function(data, group_var) {
  data |>
    group_by({{ group_var }}) |>
    summarise(mean = mean(mass))
}