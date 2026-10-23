# r2py crawler metadata
# package: testthat
# source_type: rd_example
# topic: expect_length.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\testthat\help
# lines: 12

suppressPackageStartupMessages(library(testthat))
expect_length(1, 1)
expect_length(1:10, 10)
show_failure(expect_length(1:10, 1))

x <- matrix(1:9, nrow = 3)
expect_shape(x, nrow = 3)
show_failure(expect_shape(x, nrow = 4))
expect_shape(x, ncol = 3)
show_failure(expect_shape(x, ncol = 4))
expect_shape(x, dim = c(3, 3))
show_failure(expect_shape(x, dim = c(3, 4, 5)))