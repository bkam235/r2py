# r2py crawler metadata
# package: sparsevctrs
# source_type: rd_example
# topic: coerce_to_sparse_matrix.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\sparsevctrs\help
# lines: 10

suppressPackageStartupMessages(library(sparsevctrs))
if (rlang::is_installed("Matrix")) withAutoprint({ # examplesIf
sparse_tbl <- lapply(1:10, function(x) sparse_double(x, x, length = 10))
names(sparse_tbl) <- letters[1:10]
sparse_tbl <- as.data.frame(sparse_tbl)
sparse_tbl

res <- coerce_to_sparse_matrix(sparse_tbl)
res
}) # examplesIf