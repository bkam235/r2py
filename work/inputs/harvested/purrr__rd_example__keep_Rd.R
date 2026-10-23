# r2py crawler metadata
# package: purrr
# source_type: rd_example
# topic: keep.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\purrr\help
# lines: 20

suppressPackageStartupMessages(library(purrr))
rep(10, 10) |>
  map(sample, 5) |>
  keep(function(x) mean(x) > 6)

# Or use shorthand form
rep(10, 10) |>
  map(sample, 5) |>
  keep(\(x) mean(x) > 6)

# Using a string instead of a function will select all list elements
# where that subelement is TRUE
x <- rerun(5, a = rbernoulli(1), b = sample(10))
x
x |> keep("a")
x |> discard("a")

# compact() discards elements that are NULL or that have length zero
list(a = "a", b = NULL, c = integer(0), d = NA, e = list()) |>
  compact()