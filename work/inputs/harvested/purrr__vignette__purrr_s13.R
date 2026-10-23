# r2py crawler metadata
# package: purrr
# source_type: vignette
# topic: purrr_s13
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\purrr\doc\purrr.R
# lines: 6

suppressPackageStartupMessages(library(purrr))
mtcars |>
  split(mtcars$cyl) |> # from base R
  map(\(df) lm(mpg ~ wt, data = df)) |>
  map(summary) |>
  map_dbl(\(x) x$r.squared)