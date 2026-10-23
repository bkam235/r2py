# r2py crawler metadata
# package: sparsevctrs
# source_type: rd_example
# topic: coerce_to_sparse_tibble.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\sparsevctrs\help
# lines: 14

suppressPackageStartupMessages(library(sparsevctrs))
if (rlang::is_installed("tibble")) withAutoprint({ # examplesIf
set.seed(1234)
mat <- matrix(sample(0:1, 100, TRUE, c(0.9, 0.1)), nrow = 10)
colnames(mat) <- letters[1:10]
sparse_mat <- Matrix::Matrix(mat, sparse = TRUE)
sparse_mat

res <- coerce_to_sparse_tibble(sparse_mat)
res

# All columns are sparse
vapply(res, is_sparse_vector, logical(1))
}) # examplesIf