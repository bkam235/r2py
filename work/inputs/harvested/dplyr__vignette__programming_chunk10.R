# r2py crawler metadata
# package: dplyr
# source_type: vignette
# topic: programming_chunk10
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\doc\programming.Rmd
# lines: 7

suppressPackageStartupMessages(library(dplyr))
summarise_mean <- function(data, vars) {
      data |> summarise(n = n(), across({{ vars }}, mean))
    }
    mtcars |>
      group_by(cyl) |>
      summarise_mean(where(is.numeric))