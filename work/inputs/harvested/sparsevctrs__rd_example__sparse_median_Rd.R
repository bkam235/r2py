# r2py crawler metadata
# package: sparsevctrs
# source_type: rd_example
# topic: sparse_median.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\sparsevctrs\help
# lines: 21

suppressPackageStartupMessages(library(sparsevctrs))
sparse_median(
  sparse_double(1000, 1, 1000)
)

sparse_median(
  sparse_double(1000, 1, 1000, default = 1)
)

sparse_median(
  sparse_double(c(10, 50, 11), c(1, 50, 111), 1000)
)

sparse_median(
  sparse_double(c(10, NA, 11), c(1, 50, 111), 1000)
)

sparse_median(
  sparse_double(c(10, NA, 11), c(1, 50, 111), 1000),
  na_rm = TRUE
)