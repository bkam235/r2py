# r2py crawler metadata
# package: sparsevctrs
# source_type: rd_example
# topic: sparse_dummy.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\sparsevctrs\help
# lines: 16

suppressPackageStartupMessages(library(sparsevctrs))
x <- factor(c("a", "a", "b", "c", "d", "b"))

sparse_dummy(x, one_hot = FALSE)

x <- factor(c("a", "a", "b", "c", "d", "b"))

sparse_dummy(x, one_hot = TRUE)

x <- factor(c("a", NA, "b", "c", "d", NA))

sparse_dummy(x, one_hot = FALSE)

x <- factor(c("a", NA, "b", "c", "d", NA))

sparse_dummy(x, one_hot = TRUE)