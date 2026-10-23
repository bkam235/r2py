# r2py crawler metadata
# package: purrr
# source_type: rd_example
# topic: pluck_depth.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\purrr\help
# lines: 8

suppressPackageStartupMessages(library(purrr))
x <- list(
  list(),
  list(list()),
  list(list(list(1)))
)
pluck_depth(x)
x |> map_int(pluck_depth)