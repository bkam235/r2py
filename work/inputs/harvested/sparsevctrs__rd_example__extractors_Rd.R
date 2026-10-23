# r2py crawler metadata
# package: sparsevctrs
# source_type: rd_example
# topic: extractors.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\sparsevctrs\help
# lines: 14

suppressPackageStartupMessages(library(sparsevctrs))
x_sparse <- sparse_double(c(pi, 5, 0.1), c(2, 5, 10), 10)
x_dense <- c(0, pi, 0, 0, 0.5, 0, 0, 0, 0, 0.1)

sparse_positions(x_sparse)
sparse_values(x_sparse)
sparse_default(x_sparse)

sparse_positions(x_dense)
sparse_values(x_dense)
sparse_default(x_dense)

x_sparse_3 <- sparse_double(c(pi, 5, 0.1), c(2, 5, 10), 10, default = 3)
sparse_default(x_sparse_3)