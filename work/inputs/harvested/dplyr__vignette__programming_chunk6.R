# r2py crawler metadata
# package: dplyr
# source_type: vignette
# topic: programming_chunk6
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\doc\programming.Rmd
# lines: 8

suppressPackageStartupMessages(library(dplyr))
var_summary <- function(data, var) {
      data |>
        summarise(n = n(), min = min({{ var }}), max = max({{ var }}))
    }
    mtcars |>
      group_by(cyl) |>
      var_summary(mpg)