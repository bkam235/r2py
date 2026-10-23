# r2py crawler metadata
# package: testthat
# source_type: rd_example
# topic: expect_null.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\testthat\help
# lines: 6

suppressPackageStartupMessages(library(testthat))
x <- NULL
y <- 10

expect_null(x)
show_failure(expect_null(y))