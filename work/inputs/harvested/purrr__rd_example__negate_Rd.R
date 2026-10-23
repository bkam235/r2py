# r2py crawler metadata
# package: purrr
# source_type: rd_example
# topic: negate.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\purrr\help
# lines: 6

suppressPackageStartupMessages(library(purrr))
x <- list(x = 1:10, y = rbernoulli(10), z = letters)
x |> keep(is.numeric) |> names()
x |> keep(negate(is.numeric)) |> names()
# Same as
x |> discard(is.numeric)