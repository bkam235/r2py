# r2py crawler metadata
# package: purrr
# source_type: rd_example
# topic: safely.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\purrr\help
# lines: 16

suppressPackageStartupMessages(library(purrr))
safe_log <- safely(log)
safe_log(10)
safe_log("a")

list("a", 10, 100) |>
  map(safe_log) |>
  transpose()

# This is a bit easier to work with if you supply a default value
# of the same type and use the simplify argument to transpose():
safe_log <- safely(log, otherwise = NA_real_)
list("a", 10, 100) |>
  map(safe_log) |>
  transpose() |>
  simplify_all()