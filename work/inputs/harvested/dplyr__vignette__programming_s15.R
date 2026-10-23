# r2py crawler metadata
# package: dplyr
# source_type: vignette
# topic: programming_s15
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\doc\programming.R
# lines: 5

suppressPackageStartupMessages(library(dplyr))
my_summarise3 <- function(data, mean_var, sd_var) {
  data |>
    summarise(mean = mean({{ mean_var }}), sd = sd({{ sd_var }}))
}