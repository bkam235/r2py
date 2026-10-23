# r2py crawler metadata
# package: dplyr
# source_type: vignette
# topic: colwise_s10
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\doc\colwise.R
# lines: 7

suppressPackageStartupMessages(library(dplyr))
starwars |> summarise(
  tibble(
    across(where(is.numeric), ~min(.x, na.rm = TRUE), .names = "min_{.col}"),
    across(where(is.numeric), ~max(.x, na.rm = TRUE), .names = "max_{.col}")
  )
)