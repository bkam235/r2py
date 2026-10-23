# r2py crawler metadata
# package: dplyr
# source_type: vignette
# topic: rowwise_s3
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\doc\rowwise.R
# lines: 8

suppressPackageStartupMessages(library(dplyr))
nest_by <- function(df, ...) {
  df |>
    group_by(...) |>
    summarise(data = list(pick(everything()))) |>
    rowwise(...)
}
# mtcars |> nest_by(cyl)