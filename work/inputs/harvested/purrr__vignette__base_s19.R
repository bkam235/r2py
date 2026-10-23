# r2py crawler metadata
# package: purrr
# source_type: vignette
# topic: base_s19
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\purrr\doc\base.R
# lines: 6

suppressPackageStartupMessages(library(purrr))
mtcars |>
  split(mtcars$cyl) |> 
  map(\(df) lm(mpg ~ wt, data = df))|> 
  map(coef) |> 
  map_dbl(1)