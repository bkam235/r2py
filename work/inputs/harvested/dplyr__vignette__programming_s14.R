# r2py crawler metadata
# package: dplyr
# source_type: vignette
# topic: programming_s14
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\doc\programming.R
# lines: 8

suppressPackageStartupMessages(library(dplyr))
my_summarise2 <- function(data, expr) {
  data |> summarise(
    mean = mean({{ expr }}),
    sum = sum({{ expr }}),
    n = n()
  )
}