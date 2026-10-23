# r2py crawler metadata
# package: sparsevctrs
# source_type: rd_example
# topic: sparse_integer.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\sparsevctrs\help
# lines: 8

suppressPackageStartupMessages(library(sparsevctrs))
sparse_integer(integer(), integer(), 10)

sparse_integer(c(4, 5, 7), c(2, 5, 10), 10)

str(
  sparse_integer(c(4, 5, 7), c(2, 5, 10), 1000000000)
)