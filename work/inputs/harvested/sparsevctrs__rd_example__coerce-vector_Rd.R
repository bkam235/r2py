# r2py crawler metadata
# package: sparsevctrs
# source_type: rd_example
# topic: coerce-vector.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\sparsevctrs\help
# lines: 6

suppressPackageStartupMessages(library(sparsevctrs))
x_dense <- c(3, 0, 2, 0, 0, 0, 4, 0, 0, 0)
x_sparse <- as_sparse_double(x_dense)
x_sparse

is_sparse_double(x_sparse)