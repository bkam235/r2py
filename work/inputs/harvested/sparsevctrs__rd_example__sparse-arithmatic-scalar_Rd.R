# r2py crawler metadata
# package: sparsevctrs
# source_type: rd_example
# topic: sparse-arithmatic-scalar.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\sparsevctrs\help
# lines: 7

suppressPackageStartupMessages(library(sparsevctrs))
x_sparse <- sparse_double(c(pi, 5, 0.1), c(2, 5, 10), 10)

sparse_division_scalar(x_sparse, 2)
sparse_multiplication_scalar(x_sparse, 2)
sparse_addition_scalar(x_sparse, 2)
sparse_subtraction_scalar(x_sparse, 2)