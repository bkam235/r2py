# r2py crawler metadata
# package: sparsevctrs
# source_type: rd_example
# topic: sparse_sqrt.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\sparsevctrs\help
# lines: 12

suppressPackageStartupMessages(library(sparsevctrs))
sparse_sqrt(
  sparse_double(1000, 1, 10)
)

sparse_sqrt(
  sparse_integer(1000, 3, 10, default = 2)
)

sparse_sqrt(
  sparse_double(c(10, NA, 11), c(1, 5, 10), 10)
)