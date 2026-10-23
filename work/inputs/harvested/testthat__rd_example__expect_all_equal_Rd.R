# r2py crawler metadata
# package: testthat
# source_type: rd_example
# topic: expect_all_equal.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\testthat\help
# lines: 11

suppressPackageStartupMessages(library(testthat))
x1 <- c(1, 1, 1, 1, 1, 1)
expect_all_equal(x1, 1)

x2 <- c(1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2)
show_failure(expect_all_equal(x2, 1))

# expect_all_true() and expect_all_false() are helpers for common cases
set.seed(1016)
show_failure(expect_all_true(rpois(100, 10) < 20))
show_failure(expect_all_false(rpois(100, 10) > 20))