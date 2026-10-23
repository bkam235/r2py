# r2py crawler metadata
# package: purrr
# source_type: rd_example
# topic: possibly.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\purrr\help
# lines: 9

suppressPackageStartupMessages(library(purrr))
# To replace errors with a default value, use possibly().
list("a", 10, 100) |>
  map_dbl(possibly(log, NA_real_))

# The default, NULL, will be discarded with `list_c()`
list("a", 10, 100) |>
  map(possibly(log)) |>
  list_c()