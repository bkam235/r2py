# r2py crawler metadata
# package: sparsevctrs
# source_type: rd_example
# topic: has_sparse_elements.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\sparsevctrs\help
# lines: 13

suppressPackageStartupMessages(library(sparsevctrs))
if (rlang::is_installed("Matrix")) withAutoprint({ # examplesIf
set.seed(1234)
n_cols <- 10000
mat <- matrix(sample(0:1, n_cols * 10, TRUE, c(0.9, 0.1)), ncol = n_cols)
colnames(mat) <- as.character(seq_len(n_cols))
sparse_mat <- Matrix::Matrix(mat, sparse = TRUE)

res <- coerce_to_sparse_tibble(sparse_mat)
has_sparse_elements(res)

has_sparse_elements(mtcars)
}) # examplesIf