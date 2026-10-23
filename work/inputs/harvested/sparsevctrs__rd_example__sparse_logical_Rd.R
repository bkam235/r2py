# r2py crawler metadata
# package: sparsevctrs
# source_type: rd_example
# topic: sparse_logical.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\sparsevctrs\help
# lines: 8

suppressPackageStartupMessages(library(sparsevctrs))
sparse_logical(logical(), integer(), 10)

sparse_logical(c(TRUE, NA, TRUE), c(2, 5, 10), 10)

str(
  sparse_logical(c(TRUE, NA, TRUE), c(2, 5, 10), 1000000000)
)