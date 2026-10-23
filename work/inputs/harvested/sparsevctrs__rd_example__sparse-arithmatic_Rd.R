# r2py crawler metadata
# package: sparsevctrs
# source_type: rd_example
# topic: sparse-arithmatic.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\sparsevctrs\help
# lines: 4

suppressPackageStartupMessages(library(sparsevctrs))
x_sparse <- sparse_double(c(pi, 5, 0.1), c(2, 5, 10), 10)

sparse_multiplication(x_sparse, x_sparse)