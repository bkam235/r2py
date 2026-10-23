# r2py crawler metadata
# package: sparsevctrs
# source_type: rd_example
# topic: type-predicates.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\sparsevctrs\help
# lines: 15

suppressPackageStartupMessages(library(sparsevctrs))
x_sparse <- sparse_double(c(pi, 5, 0.1), c(2, 5, 10), 10)
x_dense <- c(0, pi, 0, 0, 0.5, 0, 0, 0, 0, 0.1)

is_sparse_vector(x_sparse)
is_sparse_vector(x_dense)

is_sparse_double(x_sparse)
is_sparse_double(x_dense)

is_sparse_character(x_sparse)
is_sparse_character(x_dense)

# Forced materialization
is_sparse_vector(x_sparse[])