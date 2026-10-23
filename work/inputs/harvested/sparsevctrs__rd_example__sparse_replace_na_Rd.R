# r2py crawler metadata
# package: sparsevctrs
# source_type: rd_example
# topic: sparse_replace_na.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\sparsevctrs\help
# lines: 15

suppressPackageStartupMessages(library(sparsevctrs))
sparse_replace_na(
  sparse_double(c(10, NA, 11), c(1, 5, 10), 10),
  5
)

sparse_replace_na(
  sparse_integer(c(10L, NA, 11L), c(1, 5, 10), 10),
  5L
)

sparse_replace_na(
  sparse_character(c("A", NA, "E"), c(2, 5, 10), 10),
  "missing"
)