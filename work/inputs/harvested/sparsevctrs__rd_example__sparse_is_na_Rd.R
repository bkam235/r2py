# r2py crawler metadata
# package: sparsevctrs
# source_type: rd_example
# topic: sparse_is_na.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\sparsevctrs\help
# lines: 9

suppressPackageStartupMessages(library(sparsevctrs))
sparse_is_na(
  sparse_double(c(10, NA, 11), c(1, 50, 111), 1000)
)

sparse_is_na(
  sparse_double(c(10, NA, 11), c(1, 50, 111), 1000),
  type = "integer"
)