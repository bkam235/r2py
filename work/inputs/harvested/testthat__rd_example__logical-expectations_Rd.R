# r2py crawler metadata
# package: testthat
# source_type: rd_example
# topic: logical-expectations.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\testthat\help
# lines: 14

suppressPackageStartupMessages(library(testthat))
expect_true(2 == 2)
# Failed expectations will throw an error
show_failure(expect_true(2 != 2))

# where possible, use more specific expectations, to get more informative
# error messages
a <- 1:4
show_failure(expect_true(length(a) == 3))
show_failure(expect_equal(length(a), 3))

x <- c(TRUE, TRUE, FALSE, TRUE)
show_failure(expect_true(all(x)))
show_failure(expect_all_true(x))