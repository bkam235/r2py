# r2py crawler metadata
# package: dplyr
# source_type: vignette
# topic: programming_s16
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\doc\programming.R
# lines: 15

suppressPackageStartupMessages(library(dplyr))
my_summarise4 <- function(data, expr) {
  data |> summarise(
    "mean_{{expr}}" := mean({{ expr }}),
    "sum_{{expr}}" := sum({{ expr }}),
    "n_{{expr}}" := n()
  )
}
my_summarise5 <- function(data, mean_var, sd_var) {
  data |>
    summarise(
      "mean_{{mean_var}}" := mean({{ mean_var }}),
      "sd_{{sd_var}}" := sd({{ sd_var }})
    )
}