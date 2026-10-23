# r2py crawler metadata
# package: sparsevctrs
# source_type: rd_example
# topic: sparse_lag.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\sparsevctrs\help
# lines: 24

suppressPackageStartupMessages(library(sparsevctrs))
vec_dbl <- sparse_double(c(pi, 4, 5/2), c(1, 5, 7), 10)

sparse_lag(vec_dbl)
sparse_lag(vec_dbl, n = 3)
sparse_lag(vec_dbl, n = 3, default = 0)

vec_int <- sparse_integer(c(1, 2, 3), c(1, 5, 7), 10)

sparse_lag(vec_int)
sparse_lag(vec_int, n = 3)
sparse_lag(vec_int, n = 3, default = 0L)

vec_chr <- sparse_character(c("A", "B", "C"), c(1, 5, 7), 10)

sparse_lag(vec_chr)
sparse_lag(vec_chr, n = 3)
sparse_lag(vec_chr, n = 3, default = "before")

vec_lgl <- sparse_logical(c(TRUE, TRUE, TRUE), c(1, 5, 7), 10)

sparse_lag(vec_lgl)
sparse_lag(vec_lgl, n = 3)
sparse_lag(vec_lgl, n = 3, default = FALSE)