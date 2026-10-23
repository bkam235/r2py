# r2py crawler metadata
# package: sparsevctrs
# source_type: rd_example
# topic: sparsity.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\sparsevctrs\help
# lines: 15

suppressPackageStartupMessages(library(sparsevctrs))
# data frame
sparsity(mtcars)

# Matrix
set.seed(1234)
mat <- matrix(sample(0:1, 100, TRUE, c(0.9, 0.1)), nrow = 10)
colnames(mat) <- letters[1:10]

sparsity(mat)

# Sparse matrix
sparse_mat <- Matrix::Matrix(mat, sparse = TRUE)

sparsity(sparse_mat)